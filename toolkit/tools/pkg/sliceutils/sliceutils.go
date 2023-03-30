// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package sliceutils

import "reflect"

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
func FindMatches(slice []string, isMatch func(string) bool) []string {
	result := []string{}
	for _, v := range slice {
		if isMatch(v) {
			result = append(result, v)
		}
	}
	return result
}

// StringMatch is intended to be used with "Find" for slices of strings.
func StringMatch(expected, given interface{}) bool {
	return expected.(string) == given.(string)
}

func StringsSetToSlice(inputSet map[string]bool) []string {
	index := 0
	outputSlice := make([]string, len(inputSet))

	for element, elementInSet := range inputSet {
		if elementInSet {
			outputSlice[index] = element
			index++
		}
	}

	return outputSlice[:index]
}
