# SPI TCTI Helper

The SPI TCTI helper can be used for TPM communication over SPI e.g. in embedded systems like the ESP32.
It uses user supplied methods for SPI and timing operations in order to be platform independent.
These methods are supplied to `Tss2_Tcti_Spi_Helper_Init` via the `TSS2_TCTI_SPI_HELPER_PLATFORM` struct.

## Platform methods

Documentation on what the implementation for the platform methods should do can be found in `tss2_tcti_spi_helper.h`.
See also the example implementation for an ESP32 using the ESP-IDF below.

## Example platform methods and TCTI creation for the ESP32 using ESP-IDF

```C
/* SPDX-License-Identifier: BSD-2-Clause */
/*
 * Copyright 2020 Fraunhofer SIT. All rights reserved.
 */
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>
#include <freertos/FreeRTOS.h>
#include <freertos/task.h>
#include <driver/gpio.h>
#include <driver/spi_master.h>
#include <tss2/tss2_tcti_spi_helper.h>

// Example pin defines
#define PIN_NUM_MISO 19
#define PIN_NUM_MOSI 27
#define PIN_NUM_CLK  5
#define PIN_NUM_CS   18
#define PIN_NUM_RST  14

// Custom SPI TCTI user data storing SPI handles & timeouts
typedef struct {
    spi_device_handle_t spi;
    gpio_num_t cs_pin;
    int64_t timeout_expiry;
} PLATFORM_USERDATA;

// Aquire SPI bus and keep pulling CS
TSS2_RC platform_spi_acquire (void* user_data)
{
    // Cast our user data
    PLATFORM_USERDATA* platform_data = (PLATFORM_USERDATA*) user_data;

    // Reserve SPI bus until transaction is over and keep pulling CS
    gpio_set_level(platform_data->cs_pin, 0);
    spi_device_acquire_bus(platform_data->spi, portMAX_DELAY);

    return TSS2_RC_SUCCESS;
}

// Release SPI bus and CS
TSS2_RC platform_spi_release (void* user_data)
{
    // Cast our user data
    PLATFORM_USERDATA* platform_data = (PLATFORM_USERDATA*) user_data;

    // Release CS and release the bus for other devices
    gpio_set_level(platform_data->cs_pin, 1);
    spi_device_release_bus(platform_data->spi);

    return TSS2_RC_SUCCESS;
}

// Transfer cnt bytes from data_out to device and read response into data_in
TSS2_RC platform_spi_transfer (void* user_data, const void *data_out, void *data_in, size_t cnt)
{
    // Cast our user data
    PLATFORM_USERDATA* platform_data = (PLATFORM_USERDATA*) user_data;

    // Maximum transfer size is 64 byte because we don't use DMA (and the TPM doesn't support more anyway)
    if (cnt > 64) {
        return TSS2_TCTI_RC_BAD_VALUE;
    }

    // At least one of the buffers has to be set
    if (data_out == NULL && data_in == NULL) {
        return TSS2_TCTI_RC_BAD_VALUE;
    }

    // Clear receive buffer
    if (data_in != NULL) {
        memset(data_in, 0, cnt);
    }

    // Setup transaction
    spi_transaction_t t;
    memset(&t, 0, sizeof(t));
    t.length = cnt*8;
    t.tx_buffer = data_out;
    t.rx_buffer = data_in;

    // Transmit
    esp_err_t ret = spi_device_polling_transmit(platform_data->spi, &t);
    if (ret != ESP_OK) {
        return TSS2_TCTI_RC_IO_ERROR;
    }

    return TSS2_RC_SUCCESS;
}

// Sleeps for the specified amount of milliseconds
void platform_sleep_ms (void* user_data, int32_t milliseconds)
{
    // Sleep the specified amount of milliseconds
    vTaskDelay(milliseconds / portTICK_PERIOD_MS);
}

// Start a timeout timer with specified expiry in milliseconds
void platform_start_timeout (void* user_data, int32_t milliseconds)
{
    // Cast our user data
    PLATFORM_USERDATA* platform_data = (PLATFORM_USERDATA*) user_data;

    // Store timeout expiry time
    platform_data->timeout_expiry = esp_timer_get_time() + (milliseconds*1000);
}

// Check if the timeout timer started by platform_start_timeout has already expired
bool platform_timeout_expired (void* user_data)
{
    // Cast our user data
    PLATFORM_USERDATA* platform_data = (PLATFORM_USERDATA*) user_data;

    // Check if timeout already expired
    return esp_timer_get_time() < platform_data->timeout_expiry;
}

// Frees the platform user_data struct and everything inside
void platform_finalize(void* user_data)
{
    // Cast our user data
    PLATFORM_USERDATA* platform_data = (PLATFORM_USERDATA*) user_data;

    // Free resources inside user_data like SPI device handles here
    // ...

    // Free user_data
    free(platform_data);
}

// Creates a new platform struct with the given SPI device handle and chip select
TSS2_TCTI_SPI_HELPER_PLATFORM create_tcti_spi_helper_platform(spi_device_handle_t spi, gpio_num_t cs_pin)
{
    // Create required platform user data
    PLATFORM_USERDATA* platform_data = malloc(sizeof(PLATFORM_USERDATA));
    platform_data->spi = spi;
    platform_data->cs_pin = cs_pin;
    platform_data->timeout_expiry = 0;

    // Create TCTI SPI platform struct with custom platform methods
    TSS2_TCTI_SPI_HELPER_PLATFORM platform;
    platform.user_data = platform_data;
    platform.sleep_ms = platform_sleep_ms;
    platform.start_timeout = platform_start_timeout;
    platform.timeout_expired = platform_timeout_expired;
    platform.spi_acquire = platform_spi_acquire;
    platform.spi_release = platform_spi_release;
    platform.spi_transfer = platform_spi_transfer;
    platform.finalize = platform_finalize;

    return platform;
}

// Creates a SPI TCTI using the example pin defines
TSS2_TCTI_CONTEXT* create_tcti_ctx()
{
    // SPI bus & devive configuration
    spi_bus_config_t bus_cfg = {
        .miso_io_num = PIN_NUM_MISO,
        .mosi_io_num = PIN_NUM_MOSI,
        .sclk_io_num = PIN_NUM_CLK,
        .quadwp_io_num = -1,
        .quadhd_io_num = -1,
        .max_transfer_sz = 64
    };
    spi_device_interface_config_t dev_cfg = {
        .clock_speed_hz = 10*1000*1000, // 10MHz, but tested up to 22MHz
        .mode = 0,
        .spics_io_num = -1,
        .queue_size = 1,
        .pre_cb = NULL,
        .post_cb = NULL,
    };

    // Initializing CS pin
    gpio_pad_select_gpio(PIN_NUM_CS);
    gpio_set_direction(PIN_NUM_CS, GPIO_MODE_OUTPUT);
    gpio_set_level(PIN_NUM_CS, 1);

    // Initialize the SPI bus and device
    esp_err_t ret;
    ret = spi_bus_initialize(HSPI_HOST, &bus_cfg, 0);
    ESP_ERROR_CHECK(ret);

    // Attach the device to the SPI bus
    spi_device_handle_t spi;
    ret = spi_bus_add_device(HSPI_HOST, &dev_cfg, &spi);
    ESP_ERROR_CHECK(ret);

    // Reset TPM device (and wait a bit in between)
    gpio_pad_select_gpio(PIN_NUM_RST);
    gpio_set_direction(PIN_NUM_RST, GPIO_MODE_OUTPUT);
    gpio_set_level(PIN_NUM_RST, 0);
    vTaskDelay(10 / portTICK_PERIOD_MS);
    gpio_set_level(PIN_NUM_RST, 1);
    vTaskDelay(10 / portTICK_PERIOD_MS);

    // Create TCTI config with our custom platform methods
    TSS2_TCTI_SPI_HELPER_PLATFORM tcti_platform;
    tcti_platform = create_tcti_spi_helper_platform(spi, PIN_NUM_CS);

    // Create TCTI
    size_t size;
    TSS2_RC rc;
    TSS2_TCTI_CONTEXT* tcti_ctx;

    // Get requested TCTI context size
    rc = Tss2_Tcti_Spi_Helper_Init(NULL, &size, &tcti_platform);
    if (rc != TSS2_RC_SUCCESS) {
        printf("Failed to get allocation size for device tcti context: 0x%x\n", rc);
        return NULL;
    }

    // Allocate TCTI context size
    tcti_ctx = (TSS2_TCTI_CONTEXT*) calloc(1, size);
    if (tcti_ctx == NULL) {
        printf("Allocation for device TCTI context failed\n");
        return NULL;
    }

    // Initialize TCTI context
    rc = Tss2_Tcti_Spi_Helper_Init(tcti_ctx, &size, &tcti_platform);
    if (rc != TSS2_RC_SUCCESS) {
        printf("Failed to initialize device TCTI context: 0x%x\n", rc);
        free(tcti_ctx);
        return NULL;
    }

    return tcti_ctx;
}
```