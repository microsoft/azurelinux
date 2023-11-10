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

// SetToSlice converts a map[K]bool to a slice containing the map's keys, iff the key's value is true.
func SetToSlice[K comparable](inputSet map[K]bool) []K {
	index := 0
	outputSlice := make([]K, len(inputSet))
	for element, elementInSet := range inputSet {
		// Add key to slice if value is true
		if elementInSet {
			outputSlice[index] = element
			index++
		}
	}
	return outputSlice[:index]
}

// SetToSliceAll converts a map[K]V to a slice containing the map's keys.
func SetToSliceAll[K comparable, V any](inputSet map[K]V) []K {
	outputSlice := make([]K, len(inputSet))
	for element := range inputSet {
		outputSlice = append(outputSlice, element)
	}
	return outputSlice
}

// SliceToSet converts a slice of K to a map[K]bool, with each value set to true.
func SliceToSet[K comparable](inputSlice []K) (outputSet map[K]bool) {
	outputSet = make(map[K]bool, len(inputSlice))
	for _, element := range inputSlice {
		outputSet[element] = true
	}
	return outputSet
}

// RemoveDuplicatesFromSlice removes duplicate elements from a slice.
func RemoveDuplicatesFromSlice[K comparable](inputSlice []K) (outputSlice []K) {
	return SetToSlice(SliceToSet(inputSlice))
}

func nilCheck(expected interface{}, given interface{}) (checkValid, checkResult bool) {
	return (expected == nil || given == nil), (expected == nil && given == nil)
}

// Can be replaced by slices.Contains in Go 1.21.
func ContainsValue[K comparable](inputSlice []K, value K) bool {
	for _, item := range inputSlice {
		if item == value {
			return true
		}
	}
	return false
}

// Can be replaced by slices.ContainsFunc in Go 1.21.
func ContainsFunc[K any](inputSlice []K, fn func(K) bool) bool {
	for _, item := range inputSlice {
		if fn(item) {
			return true
		}
	}
	return false
}
