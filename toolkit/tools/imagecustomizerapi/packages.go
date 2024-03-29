// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

type Packages struct {
	UpdateExistingPackages bool     `yaml:"updateExistingPackages"`
	InstallLists           []string `yaml:"installLists"`
	Install                []string `yaml:"install"`
	RemoveLists            []string `yaml:"removeLists"`
	Remove                 []string `yaml:"remove"`
	UpdateLists            []string `yaml:"updateLists"`
	Update                 []string `yaml:"update"`
}
