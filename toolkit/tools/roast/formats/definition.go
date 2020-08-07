// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package formats

// Converter allows to save the raw disk image as a different image format
type Converter interface {
	Convert(input, output string, isInputFile bool) error
	Extension() string
}
