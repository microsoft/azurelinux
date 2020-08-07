// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package sliceutils

// Find returns an index of the first occurrence of thing in slice, or -1 if it does not appear in the slice.
func Find(slice []string, thing string) int {
	for i := range slice {
		if thing == slice[i] {
			return i
		}
	}
	return -1
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
