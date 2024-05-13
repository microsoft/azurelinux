// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

type PasswordType string

const (
	PasswordTypeLocked        PasswordType = "locked"
	PasswordTypePlainText     PasswordType = "plain-text"
	PasswordTypeHashed        PasswordType = "hashed"
	PasswordTypePlainTextFile PasswordType = "plain-text-file"
	PasswordTypeHashedFile    PasswordType = "hashed-file"
)
