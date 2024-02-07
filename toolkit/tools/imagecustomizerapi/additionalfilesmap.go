// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"fmt"
)

type AdditionalFilesMap map[string]FileConfigList

func (afmap *AdditionalFilesMap) IsValid() error {
	var aggregateErr error
	for sourcePath, fileConfigList := range *afmap {
		if len(sourcePath) == 0 {
			aggregateErr = AggregateErrors(aggregateErr, fmt.Errorf("invalid source path. Source path cannot be empty."))
		}
		err := fileConfigList.IsValid()
		if err != nil {
			aggregateErr = AggregateErrors(aggregateErr, fmt.Errorf("invalid file configs for (%s):\n%w", sourcePath, err))
		}
	}
	return aggregateErr
}
