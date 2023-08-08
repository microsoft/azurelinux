// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package ptrutils

func PtrTo[Type any](value Type) *Type {
	return &value
}
