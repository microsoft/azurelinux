// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package sliceutils

import (
	"reflect"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/pkgjson"
)

// NotFound value is returned by Find(), if a given value is not present in the slice.
const NotFound = -1

// Contains checks if the slice contains the 'searched' element.
func Contains(slice interface{}, searched interface{}, cond func(interface{}, interface{}) bool) bool {
	return Find(slice, searched, cond) != NotFound
}

// Find returns an index of the first occurrence of the "searched" argument in slice, or NotFound if it does not appear in the slice.
func Find(slice interface{}, searched interface{}, cond func(interface{}, interface{}) bool) int {
	contentValue := reflect.ValueOf(slice)

	for i := 0; i < contentValue.Len(); i++ {
		if cond(searched, contentValue.Index(i).Interface()) {
			return i
		}
	}

	return NotFound
}

// FindMatches returns a new slice keeping only these elements from slice that matcher returned true for.
func FindMatches[T comparable](slice []T, isMatch func(T) bool) []T {
	result := []T{}
	for _, v := range slice {
		if isMatch(v) {
			result = append(result, v)
		}
	}
	return result
}

// StringMatch is intended to be used with "Contains" and "Find" for slices of strings.
func StringMatch(expected, given interface{}) bool {
	if checkValid, checkResult := nilCheck(expected, given); checkValid {
		return checkResult
	}

	return expected.(string) == given.(string)
}

// PackageVerMatch is intended to be used with "Contains" and "Find" for slices of *pkgjson.PackageVers.
func PackageVerMatch(expected, given interface{}) bool {
	if checkValid, checkResult := nilCheck(expected, given); checkValid {
		return checkResult
	}

	return reflect.DeepEqual(expected.(*pkgjson.PackageVer), given.(*pkgjson.PackageVer))
}

func RemoveDuplicates[T comparable](inputSlice []T) []T {
	return SetToSlice(SliceToSet(inputSlice))
}

// SetToSlice converts a map[T]bool to a slice containing the map's keys.
func SetToSlice[T comparable](inputSet map[T]bool) []T {
	index := 0
	outputSlice := make([]T, len(inputSet))
	for element, elementInSet := range inputSet {
		if elementInSet {
			outputSlice[index] = element
			index++
		}
	}
	return outputSlice[:index]
}

// SliceToSet converts a slice ot T to a map[T]bool.
func SliceToSet[T comparable](inputSlice []T) map[T]bool {
	outputSet := make(map[T]bool)
	for _, element := range inputSlice {
		outputSet[element] = true
	}
	return outputSet
}

func nilCheck(expected interface{}, given interface{}) (checkValid, checkResult bool) {
	return (expected == nil || given == nil), (expected == nil && given == nil)
}
