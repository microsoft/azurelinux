// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// tools to to parse ccache configuration file

package ccachemanager

import (
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/jsonutils"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
)

type CCacheGroup struct {
	Name     string `json:"name"`
    PackageNames []string `json:"packageNames"`
}

type RemoteStoreConfig struct {
	Type            string `json:"type"`
	TenantId        string `json:"tenantId"`
	UserName        string `json:"userName"`
	Password        string `json:"password"`
	StorageAccount  string `json:"storageAccount"`
	ContainerName   string `json:"containerName"`
	VersionsFolder  string `json:"versionsFolder"`
	DownloadEnabled bool   `json:"downloadEnabled"`
	DownloadFolder  string `json:"downloadFolder"`
	UploadEnabled   bool   `json:"uploadEnabled"`
	UploadFolder    string `json:"uploadFolder"`
	UpdateLatest    bool   `json:"updateLatest"`
}

type CCacheConfiguration struct {
	RemoteStoreConfig RemoteStoreConfig `json:"remoteStore"`
	Groups            []CCacheGroup     `json:"groups"`
}

func GetCCacheRemoteStoreConfig() (remoteStoreConfig RemoteStoreConfig, err error) {

	ccacheGroupsFile := "./resources/manifests/package/ccache_configuration.json"

	logger.Log.Infof("  loading ccache configuration file: %s", ccacheGroupsFile)
	var ccacheConfiguration CCacheConfiguration
	err = jsonutils.ReadJSONFile(ccacheGroupsFile, &ccacheConfiguration)
	if err != nil {
		logger.Log.Infof("Failed to load file. %v", err)
	} else {
		logger.Log.Infof("  Type           : %s", ccacheConfiguration.RemoteStoreConfig.Type)
		logger.Log.Infof("  TenantId       : %s", ccacheConfiguration.RemoteStoreConfig.TenantId)
		logger.Log.Infof("  UserName       : %s", ccacheConfiguration.RemoteStoreConfig.UserName)
		// logger.Log.Infof("  Password      : %s", ccacheConfiguration.RemoteStoreConfig.Password)
		logger.Log.Infof("  StorageAccount : %s", ccacheConfiguration.RemoteStoreConfig.StorageAccount)
		logger.Log.Infof("  ContainerName  : %s", ccacheConfiguration.RemoteStoreConfig.ContainerName)
		logger.Log.Infof("  Versionsfolder : %s", ccacheConfiguration.RemoteStoreConfig.VersionsFolder)
		logger.Log.Infof("  DownloadEnabled: %v", ccacheConfiguration.RemoteStoreConfig.DownloadEnabled)
		logger.Log.Infof("  DownloadFolder : %s", ccacheConfiguration.RemoteStoreConfig.DownloadFolder)
		logger.Log.Infof("  UploadEnabled  : %v", ccacheConfiguration.RemoteStoreConfig.UploadEnabled)
		logger.Log.Infof("  UploadFolder   : %s", ccacheConfiguration.RemoteStoreConfig.UploadFolder)
		logger.Log.Infof("  UpdateLatest   : %v", ccacheConfiguration.RemoteStoreConfig.UpdateLatest)
	}

	return ccacheConfiguration.RemoteStoreConfig, err	
}

func FindCCacheGroup(basePackageName string) (packageCCacheGroupName string) {

	ccacheGroupsFile := "resources/manifests/package/ccache_configuration.json"
	logger.Log.Infof("  loading ccache configuration file: %s", ccacheGroupsFile)
	var ccacheConfiguration CCacheConfiguration
	err := jsonutils.ReadJSONFile(ccacheGroupsFile, &ccacheConfiguration)
	if err != nil {
		logger.Log.Infof("Failed to load file. %v", err)
	} else {
		logger.Log.Infof("Loaded file.")
		for _, group := range ccacheConfiguration.Groups {
			logger.Log.Infof("Found group: %s", group.Name)
			for _, packageName := range group.PackageNames {
				logger.Log.Infof("  Found package: %s", packageName)
				if packageName == basePackageName {
					logger.Log.Infof("  Found group: %s", group.Name)
					packageCCacheGroupName = group.Name
					break
				}
			}
			if packageCCacheGroupName != "" {
				break
			}
		}
	}

	if packageCCacheGroupName != "" {
		logger.Log.Infof("Found ccache group: %s", packageCCacheGroupName)
	} else {
		logger.Log.Infof("Did not find ccache group.")
	}

	return packageCCacheGroupName
}
