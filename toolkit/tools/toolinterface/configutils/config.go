// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package configutils

import (
	"fmt"
	"strings"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"

)

var config map[string]string
const configFile = "/home/neha/config.txt"

func PopulateConfigFromFile() (err error) {
	config = make(map[string]string)
	// TODO: get base_dir from pwd
	lines, err := file.ReadLines(configFile)
	if err != nil {
		fmt.Println("failed to open file:\n%w", err)
	}
	for _, line := range lines {
		fmt.Println("line is", line)
		entry := strings.Split(line,":")
		SetConfig(entry[0], entry[1])
		fmt.Println("entry is is", entry[0], ": ",entry[1] )
		i,_ := GetConfig(entry[0])
		fmt.Println("returnied ",i)
	}
	return
}

func SetConfig(key, val string) (err error) {
	config[key] = val
	return
}

func GetConfig(key string) (val string, err error) {
	fmt.Println("****** MAP ******** ")
	for k, v := range config {
        fmt.Println(k, "value is", v)
    }


	val, exists := config[key]
	if exists {
		fmt.Println("val: ", val)
	} else {
		fmt.Println("key not found")
		err = fmt.Errorf("key does not exist")
	}
	return
}
