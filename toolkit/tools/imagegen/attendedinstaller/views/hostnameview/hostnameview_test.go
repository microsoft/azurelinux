// Copyright Microsoft Corporation.
// Licensed under the MIT License.

package hostnameview

import (
	"os"
	"testing"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"

	"github.com/stretchr/testify/assert"
)

func TestMain(m *testing.M) {
	logger.InitStderrLog()
	os.Exit(m.Run())
}

func TestTooLongFQDNShouldReturnInvalid(t *testing.T) {
	// 65 length string
	const tooLongName = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
	err := validateFQDN(tooLongName)

	assert.NotNil(t, err)
}

func TestMultiDomainFQDNShouldReturnValid(t *testing.T) {
	const fqdn = "Test0.test1-test2.test3"
	err := validateFQDN(fqdn)

	assert.Nil(t, err)
}

func TestDashSuffixFQDNShouldReturnInvalid(t *testing.T) {
	const fqdn = "Test0.test-"
	err := validateFQDN(fqdn)

	assert.NotNil(t, err)
}

func TestDashPrefixFQDNShouldReturnInvalid(t *testing.T) {
	const fqdn = "-Test0.test"
	err := validateFQDN(fqdn)

	assert.NotNil(t, err)
}

func TestNonAlphaPrefixFQDNShouldReturnInvalid(t *testing.T) {
	const fqdn = "1Test0.test"
	err := validateFQDN(fqdn)

	assert.NotNil(t, err)
}

func TestAllAlphaCharFQDNShouldReturnValid(t *testing.T) {
	const fqdn = "abcdefghijklmnopqrstuvwxyz.ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
	err := validateFQDN(fqdn)

	assert.Nil(t, err)
}

func TestAllValidNonAlphaCharFQDNShouldReturnValid(t *testing.T) {
	const fqdn = "a-1234567890.A---0123.A1234"
	err := validateFQDN(fqdn)

	assert.Nil(t, err)
}

func TestEmptyDomainFQDNShouldReturnInvalid(t *testing.T) {
	const fqdn = "1Test0."
	err := validateFQDN(fqdn)

	assert.NotNil(t, err)
}

func TestNestedEmptyDomainFQDNShouldReturnInvalid(t *testing.T) {
	const fqdn = "1Test0..test"
	err := validateFQDN(fqdn)

	assert.NotNil(t, err)
}

func TestNonValidCharFQDNShouldReturnInvalid(t *testing.T) {
	const fqdn = "a@"
	err := validateFQDN(fqdn)

	assert.NotNil(t, err)
}
