// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package mathops

import (
	"errors"
	"math"
)

var ErrOverflow = errors.New("integer overflow")
var ErrUnderflow = errors.New("integer underflow")

// AddInts adds two integers and returns the result.
// If the result overflows or underflows, an error is returned.
func AddInts(left, right int) (int, error) {
	if right > 0 {
		if left > math.MaxInt-right {
			return 0, ErrOverflow
		}
	} else if left < math.MinInt-right {
		return 0, ErrUnderflow
	}

	return left + right, nil
}
