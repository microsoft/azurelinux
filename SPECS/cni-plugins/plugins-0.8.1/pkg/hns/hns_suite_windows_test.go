package hns_test

import (
	"testing"

	. "github.com/onsi/ginkgo"
	. "github.com/onsi/gomega"
)

func TestHns(t *testing.T) {
	RegisterFailHandler(Fail)
	RunSpecs(t, "Hns Suite")
}
