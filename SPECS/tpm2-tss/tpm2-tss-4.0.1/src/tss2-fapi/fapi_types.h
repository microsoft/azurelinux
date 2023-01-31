/* SPDX-License-Identifier: BSD-2-Clause */
/*******************************************************************************
 * Copyright 2018-2019, Fraunhofer SIT sponsored by Infineon Technologies AG
 * All rights reserved.
 ******************************************************************************/
#ifndef FAPI_TYPES_H
#define FAPI_TYPES_H

#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>

/** The data structure representing an unit8_t array.
  */
typedef struct {
    size_t size;
    uint8_t *buffer;
} UINT8_ARY;

/** The data structure storing a linked list of strings.
 *
 * The structure is used for the processing of file paths
 */
typedef struct str_node {
    char *str;              /**< A string of the string list */
    bool free_string;       /**< Indicates whether a free has to called on cleanup */
    struct str_node *next;  /**< Pointer to next element */
} NODE_STR_T;

/** The data structure storing a linked list of objects.
 *
 * The structure is used for the processing of file paths
 */
typedef struct object_node {
    void   *object;             /**< The pointer to the object  */
    size_t size;                /**< Will be used only for BYTE arrays */
    struct object_node *next;   /**< Pointer to next element */
} NODE_OBJECT_T;

#endif /* FAPI_TYPES_H */
