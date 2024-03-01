// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Json utilities

package jsonutils

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
)

const (
	defaultJsonFilePermission os.FileMode = 0664
)

// ReadJSONDescriptor reads a .JSON file. Behaves as Go's built-in encoding/json.Unmarshal()
// but accepts a file descriptor instead of a byte slice.
func ReadJSONDescriptor(jsonFile *os.File, data interface{}) error {
	if jsonFile == nil {
		return fmt.Errorf("passed nil file descriptor to WriteJSONDescriptor()")
	}

	jsonData, err := ioutil.ReadAll(jsonFile)
	if err != nil {
		return err
	}

	logger.Log.Tracef("Read %#x bytes of JSON data.", len(jsonData))

	return json.Unmarshal(jsonData, &data)
}

// ReadJSONFile reads a .JSON file. Behaves as Go's built-in encoding/json.Unmarshal()
// but accepts a file path instead of a byte slice.
func ReadJSONFile(path string, data interface{}) error {
	jsonFile, err := os.Open(path)
	if err != nil {
		return err
	}
	defer jsonFile.Close()

	return ReadJSONDescriptor(jsonFile, data)
}

// WriteJSONFile writes a .JSON file. Behaves as Go's built-in encoding/json.MarshalIndent()
// but accepts a file descriptor in addition to the  data.
func WriteJSONDescriptor(jsonFile *os.File, data interface{}) error {
	outputBytes, err := json.MarshalIndent(data, "", " ")
	if err != nil {
		return err
	}

	if jsonFile == nil {
		return fmt.Errorf("passed nil file descriptor to WriteJSONDescriptor()")
	}

	logger.Log.Tracef("Writing %#x bytes of JSON data.", len(outputBytes))
	err = jsonFile.Truncate(0)
	if err != nil {
		return err
	}

	numBytes, err := jsonFile.WriteAt(outputBytes, 0)
	if numBytes != len(outputBytes) && err == nil {
		err = fmt.Errorf("only wrote %d byte of the expected %d", numBytes, len(outputBytes))
	}
	return err
}

// WriteJSONFile writes a .JSON file. Behaves as Go's built-in encoding/json.MarshalIndent()
// but accepts a file path in addition to the  data.
func WriteJSONFile(outputFilePath string, data interface{}) error {
	outputBytes, err := json.MarshalIndent(data, "", " ")
	if err != nil {
		return err
	}

	logger.Log.Tracef("Writing %#x bytes of JSON data.", len(outputBytes))

	return ioutil.WriteFile(outputFilePath, outputBytes, defaultJsonFilePermission)
}
