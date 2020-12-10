// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Parser for the image builder's configuration schemas.

package configuration

import (
	"encoding/json"
	"fmt"
	"path/filepath"

	"microsoft.com/pkggen/internal/file"
	"microsoft.com/pkggen/internal/jsonutils"
	"microsoft.com/pkggen/internal/logger"
)

// Artifact [non-ISO image building only] defines the name, type
// and optional compression of the output Mariner image.
type Artifact struct {
	Compression string `json:"Compression"`
	Name        string `json:"Name"`
	Type        string `json:"Type"`
}

// Partition defines the size, name and file system type
// for a partition.
// "Start" and "End" fields define the offset from the beginning of the disk in MBs.
// An "End" value of 0 will determine the size of the partition using the next
// partition's start offset or the value defined by "MaxSize", if this is the last
// partition on the disk.
type Partition struct {
	FsType    string     `json:"FsType"`
	ID        string     `json:"ID"`
	Name      string     `json:"Name"`
	End       uint64     `json:"End"`
	Start     uint64     `json:"Start"`
	Flags     []string   `json:"Flags"`
	Artifacts []Artifact `json:"Artifacts"`
}

// RawBinary allow the users to specify a binary they would
// like to copy byte-for-byte onto the disk.
type RawBinary struct {
	BinPath   string `json:"BinPath"`
	BlockSize uint64 `json:"BlockSize"`
	Seek      uint64 `json:"Seek"`
}

// TargetDisk [kickstart-only] defines the physical disk, to which
// Mariner should be installed.
type TargetDisk struct {
	Type  string `json:"Type"`
	Value string `json:"Value"`
}

// PartitionSetting holds the mounting information for each partition.
type PartitionSetting struct {
	RemoveDocs   bool   `json:"RemoveDocs"`
	ID           string `json:"ID"`
	MountOptions string `json:"MountOptions"`
	MountPoint   string `json:"MountPoint"`
}

// PostInstallScript defines a script to be ran after other installation
// steps are finished and provides a way to pass parameters to it.
type PostInstallScript struct {
	Args string `json:"Args"`
	Path string `json:"Path"`
}

// Group defines a single group to be created on the new system.
type Group struct {
	Name string `json:"Name"`
	GID  string `json:"GID"`
}

// RootEncryption enables encryption on the root partition
type RootEncryption struct {
	Enable   bool   `json:"Enable"`
	Password string `json:"Password"`
}

// Config holds the parsed values of the configuration schemas as well as
// a few computed values simplifying access to certain pieces of the configuration.
type Config struct {
	// Values representing the contents of the config JSON file.
	Disks         []Disk         `json:"Disks"`
	SystemConfigs []SystemConfig `json:"SystemConfigs"`

	// Computed values not present in the config JSON.
	DefaultSystemConfig *SystemConfig // A system configuration with the "IsDefault" field set or the first system configuration if there is no explicit default.
}

// IsValid returns an error if the Config is not valid
func (c *Config) IsValid() (err error) {
	for _, disk := range c.Disks {
		if err = disk.IsValid(); err != nil {
			return fmt.Errorf("invalid [Disks]: %w", err)
		}
	}

	if len(c.SystemConfigs) == 0 {
		return fmt.Errorf("config file must provide at least one system configuration inside the [SystemConfigs] field")
	}
	for _, sysConfig := range c.SystemConfigs {
		if err = sysConfig.IsValid(); err != nil {
			return fmt.Errorf("invalid [SystemConfigs]: %w", err)
		}
	}
	defaultFound := false
	for _, sysConfig := range c.SystemConfigs {
		if sysConfig.IsDefault {
			if defaultFound {
				return fmt.Errorf("config file must have no more than one default system configuration. Please remove redundant [IsDefault] fields")
			}
			defaultFound = true
		}
	}
	return
}

// UnmarshalJSON Unmarshals a Config entry
func (c *Config) UnmarshalJSON(b []byte) (err error) {
	// Use an intermediate type which will use the default JSON unmarshal implementation
	type IntermediateTypeConfig Config
	err = json.Unmarshal(b, (*IntermediateTypeConfig)(c))
	if err != nil {
		return fmt.Errorf("failed to parse [Config]: %w", err)
	}

	// Now validate the resulting unmarshaled object
	err = c.IsValid()
	if err != nil {
		return fmt.Errorf("failed to parse [Config]: %w", err)
	}
	return
}

// Load loads the config schema from a JSON file found under the 'configFilePath'.
func Load(configFilePath string) (config Config, err error) {
	logger.Log.Debugf("Reading config file from '%s'.", configFilePath)

	err = jsonutils.ReadJSONFile(configFilePath, &config)
	if err != nil {
		return
	}

	config.setDefaultConfig()

	return
}

// LoadWithAbsolutePaths loads the config schema from a JSON file found under the 'configFilePath'
// and resolves all relative paths into absolute ones using 'baseDirPath' as a starting point for all
// relative paths.
func LoadWithAbsolutePaths(configFilePath, baseDirPath string) (config Config, err error) {
	config, err = Load(configFilePath)
	if err != nil {
		return
	}

	baseDirPath, err = resolveBaseDirPath(baseDirPath, configFilePath)
	if err != nil {
		logger.Log.Errorf("Failed to resolve base directory path (%s) for config under (%s)", baseDirPath, configFilePath)
		return
	}

	config.convertToAbsolutePaths(baseDirPath)

	return
}

// convertToAbsolutePaths converts all of the config's local file paths into absolute ones.
func (c *Config) convertToAbsolutePaths(baseDirPath string) {
	for i := range c.Disks {
		diskConfig := &c.Disks[i]
		convertRawBinariesPath(baseDirPath, diskConfig)
	}

	for i := range c.SystemConfigs {
		systemConfig := &c.SystemConfigs[i]

		convertAdditionalFilesPath(baseDirPath, systemConfig)
		convertPackageListPaths(baseDirPath, systemConfig)
		convertPostInstallScriptsPaths(baseDirPath, systemConfig)
		convertSSHPubKeys(baseDirPath, systemConfig)
	}
}

func convertRawBinariesPath(baseDirPath string, diskConfig *Disk) {
	for i, rawBinary := range diskConfig.RawBinaries {
		diskConfig.RawBinaries[i].BinPath = file.GetAbsPathWithBase(baseDirPath, rawBinary.BinPath)
	}
}

func convertAdditionalFilesPath(baseDirPath string, systemConfig *SystemConfig) {
	absAdditionalFiles := make(map[string]string)
	for localFilePath, targetFilePath := range systemConfig.AdditionalFiles {
		localFilePath = file.GetAbsPathWithBase(baseDirPath, localFilePath)
		absAdditionalFiles[localFilePath] = targetFilePath
	}
	systemConfig.AdditionalFiles = absAdditionalFiles
}

func convertPackageListPaths(baseDirPath string, systemConfig *SystemConfig) {
	for i, packageListPath := range systemConfig.PackageLists {
		systemConfig.PackageLists[i] = file.GetAbsPathWithBase(baseDirPath, packageListPath)
	}
}

func convertPostInstallScriptsPaths(baseDirPath string, systemConfig *SystemConfig) {
	for i, postInstallScript := range systemConfig.PostInstallScripts {
		systemConfig.PostInstallScripts[i].Path = file.GetAbsPathWithBase(baseDirPath, postInstallScript.Path)
	}
}

func convertSSHPubKeys(baseDirPath string, systemConfig *SystemConfig) {
	for _, user := range systemConfig.Users {
		for i, sshKeyPath := range user.SSHPubKeyPaths {
			user.SSHPubKeyPaths[i] = file.GetAbsPathWithBase(baseDirPath, sshKeyPath)
		}
	}
}

// resolveBaseDirPath returns an absolute path to the base directory or
// the absolute path to the config file directory if `baseDirPath` is empty.
func resolveBaseDirPath(baseDirPath, configFilePath string) (absoluteBaseDirPath string, err error) {
	if baseDirPath == "" {
		baseDirPath = filepath.Dir(configFilePath)
	}

	return filepath.Abs(baseDirPath)
}

func (c *Config) setDefaultConfig() {
	c.DefaultSystemConfig = &c.SystemConfigs[0]
	for i, systemConfig := range c.SystemConfigs {
		if systemConfig.IsDefault {
			c.DefaultSystemConfig = &c.SystemConfigs[i]
			return
		}
	}
}
