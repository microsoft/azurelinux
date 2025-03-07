// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package pkgjson

import (
	"testing"

	"fmt"
)

const infinity = 99

// Re-implementation of the superset calculation to compare against the interval method
func supersetTest(startSuper, endSuper, startSub, endSub int, inculsiveStartSuper, inclusive1EndSuper, inclusiveStartSub, inclusiveEndSub bool) bool {
	type interval struct {
		start, end             int
		inclusiveS, inclusiveE bool
	}

	// Flip the conditions if the start is greater than the end
	if startSuper > endSuper {
		startSuper, endSuper = endSuper, startSuper
		inculsiveStartSuper, inclusive1EndSuper = inclusive1EndSuper, inculsiveStartSuper
	}

	if startSub > endSub {
		startSub, endSub = endSub, startSub
		inclusiveStartSub, inclusiveEndSub = inclusiveEndSub, inclusiveStartSub
	}

	i1 := interval{startSuper, endSuper, inculsiveStartSuper, inclusive1EndSuper}
	i2 := interval{startSub, endSub, inclusiveStartSub, inclusiveEndSub}

	// Treat infinity as a large number and force it to be inclusive
	if intAbs(i1.start) == infinity {
		i1.inclusiveS = true
	}

	if intAbs(i1.end) == infinity {
		i1.inclusiveE = true
	}

	if intAbs(i2.start) == infinity {
		i2.inclusiveS = true
	}

	if intAbs(i2.end) == infinity {
		i2.inclusiveE = true
	}

	// If any part of i2 is outside of i1, return false
	if i2.start < i1.start {
		return false
	}
	if i2.start == i1.start {
		if !i1.inclusiveS && i2.inclusiveS {
			return false
		}
	}

	if i2.end > i1.end ||
		(i2.end == i1.end &&
			(!i1.inclusiveE && i2.inclusiveE)) {
		return false
	}

	return true
}

func intAbs(i int) int {
	if i < 0 {
		return -i
	}
	return i
}

func buildPackage(v1, v2 int, i1, i2 bool) *PackageVer {
	cond1 := "="
	cond2 := ""

	v1Str := fmt.Sprintf("%d", v1)
	v2Str := ""

	// v1 never infinity
	if intAbs(v1) == infinity {
		return nil
	} else {
		if v1 < 0 || v1 > 5 {
			return nil
		}
	}

	// Limit to +- 5 for all non-infinity values
	if intAbs(v2) != infinity &&
		(v2 < 0 || v2 > 5) {
		return nil
	}

	if v1 == v2 {
		// Can't have a single number with exclusive conditions
		if !i1 || !i2 {
			return nil
		}
		return &PackageVer{Version: v1Str, Condition: cond1}
	}

	if v1 < v2 {
		// One of > or >= for cond 1
		if i1 {
			cond1 = ">="
		} else {
			cond1 = ">"
		}
	} else {
		// One of < or <= for cond 1
		if i1 {
			cond1 = "<="
		} else {
			cond1 = "<"
		}
	}

	// Check if 2nd version is unbounded
	if intAbs(v2) != infinity {
		v2Str = fmt.Sprintf("%d", v2)
		if v1 < v2 {
			if i2 {
				cond2 = "<="
			} else {
				cond2 = "<"
			}
		} else {
			if i2 {
				cond2 = ">="
			} else {
				cond2 = ">"
			}
		}
	}

	return &PackageVer{
		Version:    v1Str,
		Condition:  cond1,
		SVersion:   v2Str,
		SCondition: cond2}
}

// Run with 'go test -run=FuzzGuaranteedSatisfies
func FuzzGuaranteedSatisfies(f *testing.F) {
	// Allowable versions (others cause skip): -99, 0 <= version <= 5, 99
	// L/R doesn't need to be in order, functions will sort them
	f.Add(1, infinity, 1, 1, false, false, false, false)
	f.Add(1, 1, 1, 1, false, false, false, false)
	f.Add(infinity, infinity, infinity, infinity, false, false, false, false)
	f.Add(-infinity, 4, 1, 2, false, false, false, false)
	f.Fuzz(func(t *testing.T, v1l int, v1r, v2l, v2r int, inculsive1L, inclusive1R, inclusive2L, inclusive2R bool) {

		p1 := buildPackage(v1l, v1r, inculsive1L, inclusive1R)
		p2 := buildPackage(v2l, v2r, inclusive2L, inclusive2R)

		if p1 == nil || p2 == nil {
			return
		}

		interval1, err := p1.Interval()
		if err != nil {
			// buildPackage should only return valid packages
			t.Errorf("p1 (%v) failed to create interval: %v", p1, err)
			return
		}

		interval2, err := p2.Interval()
		if err != nil {
			// buildPackage should only return valid packages
			t.Errorf("p2 (%v) failed to create interval: %v", p2, err)
			return
		}

		testRes := interval1.GuaranteedSatisfies(&interval2)
		alternateCalc := supersetTest(v2l, v2r, v1l, v1r, inclusive2L, inclusive2R, inculsive1L, inclusive1R)

		if testRes != alternateCalc {
			t.Logf("inputs: %d, %d, %d, %d, %v, %v, %v, %v", v1l, v1r, v2l, v2r, inculsive1L, inclusive1R, inclusive2L, inclusive2R)
			t.Logf("Test: %v,  check: %v", testRes, alternateCalc)
			t.Errorf("Test failed for pkg1:%v    pkg2:%v", p1, p2)
		}
	})

}
