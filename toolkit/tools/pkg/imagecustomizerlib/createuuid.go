// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerlib

import (
	"crypto/rand"
	"fmt"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
)

const (
	UuidSize uint32 = 16
)

// Create the uuid and return byte array and string representation
func createUuid() ([UuidSize]byte, string, error) {
	uuid, err := generateRandom128BitNumber()
	if err != nil {
		return uuid, "", err
	}
	uuidStr := convertUuidToString(uuid)
	logger.Log.Infof("Image UUID: %s", uuidStr)

	return uuid, uuidStr, nil
}

// Generates a random 128-bit number
func generateRandom128BitNumber() ([UuidSize]byte, error) {
	var randomBytes [UuidSize]byte
	_, err := rand.Read(randomBytes[:])
	if err != nil {
		return randomBytes, fmt.Errorf("failed to generate random 128-bit number for uuid:\n%w", err)
	}
	return randomBytes, nil
}

func convertUuidToString(uuid [UuidSize]byte) string {
	uuidStr := fmt.Sprintf("%08x-%04x-%04x-%04x-%012x",
		uuid[0:4],
		uuid[4:6],
		uuid[6:8],
		uuid[8:10],
		uuid[10:16],
	)

	return uuidStr
}
