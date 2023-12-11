// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package ccachemanager

import (
	"context"
	"errors"
	"fmt"
	"io/ioutil"
	"os"
	"path/filepath"
	"time"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/azureblobstorage"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/directory"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/jsonutils"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/shell"
)

// CCacheManager
//
// CCacheManager is a central place to hold the ccache configuration and
// abstract its work into easy to use functions.
//
// The configurations include:
// - Whether ccache is enabled or not.
// - Whether to download ccache artifacts from a previous build or not.
// - Whether to upload the newly generated ccache artifacts or not.
// - Other configuration like local working folders, etc.
//
// The main object exposed to the caller/user is CCacheManager and is
// instantiated through the CreateManager() function.
//
// An instance of CCacheManager can then be set to a specific package family by
// calling SetCurrentPkgGroup(). This function causes the CCacheManager to
// calculate a number of settings for this particular package group.
//
// After a successful call to SetcurrentPkgGroup(), the user can then use the
// DownloadPkgGroupCCache() or UploadPkgGroupCache() to download or upload
// ccache artifacts respectively.
//
// UploadMultiPkgGroupCCaches() is provided to call at the end of the build
// (where individual contexts for each pkg is not available) to enumerate
// the generated ccache artifacts from the folders and upload those that have
// not been uploaded - namely, package groups that have more than one package.
//
// Note that the design allows for storing multiple versions of the ccache
// artifacts on the remote store. This also means that the user may choose to
// download from any of these versions, and upload to a new location.
//
// The design supports a 'latest' notion - where the user can just indicate
// that the download is to use  the 'latest' and the CCacheManager will find
// out the latest version and download.
//
// Also, the user may choose to upload the artifacts generated in this build,
// and marker them latest - so that a subsequent build can make use of them.
//
// The 'latest' flow is implemented by creating one text file per package
// family that holds the folder where the latest artifacts are. On downloading
// the latest, that file is read (downloaded from the blob storage and read).
// On uploading, the file is created locally and uploaded (to overwrite the
// existing version if it exists).
//
// While we can store the ccache artifacts from multiple builds, and consumer
// builds can choose which ones to download from, this is not the typical
// scenario.
//
// Instead, an official production build is to upload ccache artifacts and mark
// them 'latest'. And consumer builds will just always pick-up the latest.
//
// This implies that we do not need to keep older ccache artifacts on the
// remote store and we should delete them. To support that, there is a flag
// 'KeepLatestOnly' that tells CCacheManager to delete unused older versions.
// It identifies unused versions by capturing the latest version information
// right before it updates it to the current build. Then, it knows that the
// previous latest version is no longer in use and delete it.
//
// This has an implication if we keep switching the KeepLatestOnly flag on and
// off. CCacheManager will not be able to delete older unused versions unless
// they are the versions that we just switched away from. If this proves to be
// a problem, we can always write a tool to enumerate all the versions in use
// , and anything that is not in that list can be removed. This is not the
// default behavior because such enumeration takes about 10 minutes and we do
// not want this to be part of each build.
//

const (
	CCacheTarSuffix = "-ccache.tar.gz"
	CCacheTagSuffix = "-latest-build.txt"
	// This are just place holders when constructing a new manager object.
	UninitializedGroupName         = "unknown"
	UninitializedGroupSize         = 0
	UninitializedGroupArchitecture = "unknown"
)

// RemoveStoreConfig holds the following:
// - The remote store end-point and the necessary credentials.
// - The behavior of the download from the remote store.
// - The behavior of the upload to the remote store.
// - The clean-up policy of the remote store.
type RemoteStoreConfig struct {
	// The remote store type. Currently, there is only one type support;
	// Azure blob storage.
	Type string `json:"type"`

	// Azure subscription tenant id.
	TenantId string `json:"tenantId"`

	// Service principal client id with write-permissions to the Azure blob
	// storage. This can be left empty if upload is disabled.
	UserName string `json:"userName"`

	// Service principal secret with write-permissions to the Azure blob
	// storage. This can be left empty if upload is disabled.
	Password string `json:"password"`

	// Azure storage account name.
	StorageAccount string `json:"storageAccount"`

	// Azure storage container name.
	ContainerName string `json:"containerName"`

	// Tags folder is the location where the files holding information about
	// the latest folders are kept.
	TagsFolder string `json:"tagsFolder"`

	// If true, the build will download ccache artifacts from the remote store
	// (before the package family builds).
	DownloadEnabled bool `json:"downloadEnabled"`

	// If true, the build will determine the latest build and download its
	// artifacts. If true, DownloadFolder does not need to be set.
	DownloadLatest bool `json:"downloadLatest"`

	// The folder on the remote store where the ccache artifacts to use are.
	// There should be a folder for each build.
	// If DownloadLatest is true, this does not need to be set.
	DownloadFolder string `json:"downloadFolder"`

	// If true, the build will upload ccache artifacts to the remote store
	// after the package family builds).
	UploadEnabled bool `json:"uploadEnabled"`

	// The folder on the remote store where the ccache artifacts are to be
	// uploaded.
	UploadFolder string `json:"uploadFolder"`

	// If true, the tags specifying the latest artifacts will be updated to
	// point to the current upload.
	UpdateLatest bool `json:"updateLatest"`

	// If true, previous 'latest' ccache artifacts will be deleted from the
	// remote store.
	KeepLatestOnly bool `json:"keepLatestOnly"`
}

// CCacheGroupConfig is where package groups are defined.
// A package group is a group of packages that can share the same ccache
// artifacts. This is typical for packages like kernel and kernel-hci, for
// example.
// A package group can have an arbitrary name, and a list of package names
// associated with it.
// A package group can also be disabled if the ccache breaks its build. This
// is usually a bug - and would need to be investigated further. The field
// 'comment' can be used to clarify any configuration related to this package
// family.
type CCacheGroupConfig struct {
	Name         string   `json:"name"`
	Comment      string   `json:"comment"`
	Enabled      bool     `json:"enabled"`
	PackageNames []string `json:"packageNames"`
}

type CCacheConfiguration struct {
	RemoteStoreConfig *RemoteStoreConfig  `json:"remoteStore"`
	Groups            []CCacheGroupConfig `json:"groups"`
}

// Note that the design separate the artifacts we download (source) from those
// that we upload (target).
// What we start with (source), has a remote path on the remote storage, and is
// downloaded to disk  at the local path).
// What the generate (target), has a local path where we create the archive, and
// uploaded to the remote store at the remote target path.
type CCacheArchive struct {
	LocalSourcePath  string
	RemoteSourcePath string
	LocalTargetPath  string
	RemoteTargetPath string
}

// CCachePkgGroup is calculated for each package as we encounter it during the
// build. It is derived from the CCacheGroupConfig + runtime parameters.
type CCachePkgGroup struct {
	Name      string
	Enabled   bool
	Size      int
	Arch      string
	CCacheDir string

	TarFile *CCacheArchive
	TagFile *CCacheArchive
}

// CCacheManager is the main object...
type CCacheManager struct {
	// Full path to the ccache json configuration file.
	ConfigFileName string

	// The in-memory representation of the ConfigFile contents.
	Configuration *CCacheConfiguration

	// ccache root folder as specified by build pipelines.
	RootWorkDir string

	// Working folder where CCacheManager will download artifacts.
	LocalDownloadsDir string

	// Working folder where CCacheManager will create archives in preparation
	// for uploading them.
	LocalUploadsDir string

	// Pointer to the current active pkg group state/configuration.
	CurrentPkgGroup *CCachePkgGroup

	// A utility helper for downloading/uploading archives from/to Azure blob
	// storage.
	AzureBlobStorage *azureblobstorage.AzureBlobStorage
}

func buildRemotePath(arch, folder, name, suffix string) string {
	return arch + "/" + folder + "/" + name + suffix
}

func (g *CCachePkgGroup) buildTarRemotePath(folder string) string {
	return buildRemotePath(g.Arch, folder, g.Name, CCacheTarSuffix)
}

func (g *CCachePkgGroup) buildTagRemotePath(folder string) string {
	return buildRemotePath(g.Arch, folder, g.Name, CCacheTagSuffix)
}

func (g *CCachePkgGroup) UpdateTagsPaths(remoteStoreConfig *RemoteStoreConfig, localDownloadsDir string, localUploadsDir string) {

	tagFile := &CCacheArchive{
		LocalSourcePath:  localDownloadsDir + "/" + g.Name + CCacheTagSuffix,
		RemoteSourcePath: g.buildTagRemotePath(remoteStoreConfig.TagsFolder),
		LocalTargetPath:  localUploadsDir + "/" + g.Name + CCacheTagSuffix,
		RemoteTargetPath: g.buildTagRemotePath(remoteStoreConfig.TagsFolder),
	}

	logger.Log.Infof("  tag local source  : (%s)", tagFile.LocalSourcePath)
	logger.Log.Infof("  tag remote source : (%s)", tagFile.RemoteSourcePath)
	logger.Log.Infof("  tag local target  : (%s)", tagFile.LocalTargetPath)
	logger.Log.Infof("  tag remote target : (%s)", tagFile.RemoteTargetPath)

	g.TagFile = tagFile
}

func (g *CCachePkgGroup) UpdateTarPaths(remoteStoreConfig *RemoteStoreConfig, localDownloadsDir string, localUploadsDir string) {

	tarFile := &CCacheArchive{
		LocalSourcePath:  localDownloadsDir + "/" + g.Name + CCacheTarSuffix,
		RemoteSourcePath: g.buildTarRemotePath(remoteStoreConfig.DownloadFolder),
		LocalTargetPath:  localUploadsDir + "/" + g.Name + CCacheTarSuffix,
		RemoteTargetPath: g.buildTarRemotePath(remoteStoreConfig.UploadFolder),
	}

	logger.Log.Infof("  tar local source  : (%s)", tarFile.LocalSourcePath)
	logger.Log.Infof("  tar remote source : (%s)", tarFile.RemoteSourcePath)
	logger.Log.Infof("  tar local target  : (%s)", tarFile.LocalTargetPath)
	logger.Log.Infof("  tar remote target : (%s)", tarFile.RemoteTargetPath)

	g.TarFile = tarFile
}

func (g *CCachePkgGroup) getLatestTag(azureBlobStorage *azureblobstorage.AzureBlobStorage, containerName string) (string, error) {

	logger.Log.Infof("  checking if (%s) already exists...", g.TagFile.LocalSourcePath)
	_, err := os.Stat(g.TagFile.LocalSourcePath)
	if err != nil {
		// If file is not available locally, try downloading it...
		logger.Log.Infof("  downloading (%s) to (%s)...", g.TagFile.RemoteSourcePath, g.TagFile.LocalSourcePath)
		err = azureBlobStorage.Download(context.Background(), containerName, g.TagFile.RemoteSourcePath, g.TagFile.LocalSourcePath)
		if err != nil {
			return "", fmt.Errorf("Unable to download ccache tag file:\n%w", err)
		}
	}

	latestBuildTagData, err := ioutil.ReadFile(g.TagFile.LocalSourcePath)
	if err != nil {
		return "", fmt.Errorf("Unable to read ccache tag file contents:\n%w", err)
	}

	return string(latestBuildTagData), nil
}

// SetCurrentPkgGroup() is called once per package.
func (m *CCacheManager) SetCurrentPkgGroup(basePackageName string, arch string) (err error) {
	// Note that findGroup() always succeeds.
	// If it cannot find the package, it assumes the packages belongs to the
	// 'common' group.
	groupName, groupEnabled, groupSize := m.findGroup(basePackageName)

	return m.setCurrentPkgGroupInternal(groupName, groupEnabled, groupSize, arch)
}

// setCurrentPkgGroupInternal() is called once per package.
func (m *CCacheManager) setCurrentPkgGroupInternal(groupName string, groupEnabled bool, groupSize int, arch string) (err error) {

	ccachePkgGroup := &CCachePkgGroup{
		Name:    groupName,
		Enabled: groupEnabled,
		Size:    groupSize,
		Arch:    arch,
	}

	ccachePkgGroup.CCacheDir, err = m.buildPkgCCacheDir(ccachePkgGroup.Name, ccachePkgGroup.Arch)
	if err != nil {
		return fmt.Errorf("Failed to construct the ccache directory name:\n%w", err)
	}

	// Note that we create the ccache working folder here as opposed to the
	// download function because there is a case where the group is configured
	// to enable ccache, but does not download.
	if ccachePkgGroup.Enabled {
		logger.Log.Infof("  ccache pkg folder : (%s)", ccachePkgGroup.CCacheDir)
		err = directory.EnsureDirExists(ccachePkgGroup.CCacheDir)
		if err != nil {
			return fmt.Errorf("Cannot create ccache download folder:\n%w", err)
		}

		ccachePkgGroup.UpdateTagsPaths(m.Configuration.RemoteStoreConfig, m.LocalDownloadsDir, m.LocalUploadsDir)

		if m.Configuration.RemoteStoreConfig.DownloadLatest {

			logger.Log.Infof("  ccache is configured to use the latest from the remote store...")
			latestTag, err := ccachePkgGroup.getLatestTag(m.AzureBlobStorage, m.Configuration.RemoteStoreConfig.ContainerName)
			if err == nil {
				// Adjust the download folder from 'latest' to the tag loaded from the file...
				logger.Log.Infof("  updating (%s) to (%s)...", m.Configuration.RemoteStoreConfig.DownloadFolder, latestTag)
				m.Configuration.RemoteStoreConfig.DownloadFolder = latestTag
			} else {
				logger.Log.Warnf("  unable to get the latest ccache tag. Might be the first run and no ccache tag has been uploaded before.")
			}
		}

		if m.Configuration.RemoteStoreConfig.DownloadFolder == "" {
			logger.Log.Infof("  ccache archive source download folder is an empty string. Disabling ccache download.")
			m.Configuration.RemoteStoreConfig.DownloadEnabled = false
		}

		ccachePkgGroup.UpdateTarPaths(m.Configuration.RemoteStoreConfig, m.LocalDownloadsDir, m.LocalUploadsDir)
	}

	m.CurrentPkgGroup = ccachePkgGroup

	return nil
}

func loadConfiguration(configFileName string) (configuration *CCacheConfiguration, err error) {

	logger.Log.Infof("  loading ccache configuration file: %s", configFileName)

	err = jsonutils.ReadJSONFile(configFileName, &configuration)
	if err != nil {
		return nil, fmt.Errorf("Failed to load file:\n%w", err)
	}

	logger.Log.Infof("    Type           : %s", configuration.RemoteStoreConfig.Type)
	logger.Log.Infof("    TenantId       : %s", configuration.RemoteStoreConfig.TenantId)
	logger.Log.Infof("    UserName       : %s", configuration.RemoteStoreConfig.UserName)
	logger.Log.Infof("    StorageAccount : %s", configuration.RemoteStoreConfig.StorageAccount)
	logger.Log.Infof("    ContainerName  : %s", configuration.RemoteStoreConfig.ContainerName)
	logger.Log.Infof("    Tagsfolder     : %s", configuration.RemoteStoreConfig.TagsFolder)
	logger.Log.Infof("    DownloadEnabled: %v", configuration.RemoteStoreConfig.DownloadEnabled)
	logger.Log.Infof("    DownloadLatest : %v", configuration.RemoteStoreConfig.DownloadLatest)
	logger.Log.Infof("    DownloadFolder : %s", configuration.RemoteStoreConfig.DownloadFolder)
	logger.Log.Infof("    UploadEnabled  : %v", configuration.RemoteStoreConfig.UploadEnabled)
	logger.Log.Infof("    UploadFolder   : %s", configuration.RemoteStoreConfig.UploadFolder)
	logger.Log.Infof("    UpdateLatest   : %v", configuration.RemoteStoreConfig.UpdateLatest)
	logger.Log.Infof("    KeepLatestOnly : %v", configuration.RemoteStoreConfig.KeepLatestOnly)

	return configuration, err
}

func compressDir(sourceDir string, archiveName string) (err error) {

	// Ensure the output file does not exist...
	_, err = os.Stat(archiveName)
	if err == nil {
		err = os.Remove(archiveName)
		if err != nil {
			return fmt.Errorf("Unable to delete ccache out tar:\n%w", err)
		}
	}

	// Create the archive...
	logger.Log.Infof("  compressing (%s) into (%s).", sourceDir, archiveName)
	compressStartTime := time.Now()
	tarArgs := []string{
		"cf",
		archiveName,
		"-C",
		sourceDir,
		"."}

	_, stderr, err := shell.Execute("tar", tarArgs...)
	if err != nil {
		return fmt.Errorf("Unable compress ccache files into archive:\n%s", stderr)
	}
	compressEndTime := time.Now()
	logger.Log.Infof("  compress time: %s", compressEndTime.Sub(compressStartTime))
	return nil
}

func uncompressFile(archiveName string, targetDir string) (err error) {
	logger.Log.Infof("  uncompressing (%s) into (%s).", archiveName, targetDir)
	uncompressStartTime := time.Now()
	tarArgs := []string{
		"xf",
		archiveName,
		"-C",
		targetDir,
		"."}

	_, stderr, err := shell.Execute("tar", tarArgs...)
	if err != nil {
		return fmt.Errorf("Unable extract ccache files from archive:\n%s", stderr)
	}
	uncompressEndTime := time.Now()
	logger.Log.Infof("  uncompress time: %v", uncompressEndTime.Sub(uncompressStartTime))
	return nil
}

func CreateManager(rootDir string, configFileName string) (m *CCacheManager, err error) {
	logger.Log.Infof("* Creating a ccache manager instance *")
	logger.Log.Infof("  ccache root folder         : (%s)", rootDir)
	logger.Log.Infof("  ccache remote configuration: (%s)", configFileName)

	if rootDir == "" {
		return nil, errors.New("CCache root directory cannot be empty.")
	}

	if configFileName == "" {
		return nil, errors.New("CCache configuration file cannot be empty.")
	}

	configuration, err := loadConfiguration(configFileName)
	if err != nil {
		return nil, fmt.Errorf("Failed to load remote store configuration:\n%w", err)
	}

	logger.Log.Infof("  creating blob storage client...")
	accessType := azureblobstorage.AnonymousAccess
	if configuration.RemoteStoreConfig.UploadEnabled {
		accessType = azureblobstorage.ManagedIdentityAccess
	}

	azureBlobStorage, err := azureblobstorage.Create(configuration.RemoteStoreConfig.TenantId, configuration.RemoteStoreConfig.UserName, configuration.RemoteStoreConfig.Password, configuration.RemoteStoreConfig.StorageAccount, accessType)
	if err != nil {
		return nil, fmt.Errorf("Unable to init azure blob storage client:\n%w", err)
	}

	err = directory.EnsureDirExists(rootDir)
	if err != nil {
		return nil, fmt.Errorf("Cannot create ccache working folder:\n%w", err)
	}

	rootWorkDir := rootDir + "/work"
	err = directory.EnsureDirExists(rootWorkDir)
	if err != nil {
		return nil, fmt.Errorf("Cannot create ccache work folder:\n%w", err)
	}

	localDownloadsDir := rootDir + "/downloads"
	err = directory.EnsureDirExists(localDownloadsDir)
	if err != nil {
		return nil, fmt.Errorf("Cannot create ccache downloads folder:\n%w", err)
	}

	localUploadsDir := rootDir + "/uploads"
	err = directory.EnsureDirExists(localUploadsDir)
	if err != nil {
		return nil, fmt.Errorf("Cannot create ccache uploads folder:\n%w", err)
	}

	ccacheManager := &CCacheManager{
		ConfigFileName:    configFileName,
		Configuration:     configuration,
		RootWorkDir:       rootWorkDir,
		LocalDownloadsDir: localDownloadsDir,
		LocalUploadsDir:   localUploadsDir,
		AzureBlobStorage:  azureBlobStorage,
	}

	ccacheManager.setCurrentPkgGroupInternal(UninitializedGroupName, false, UninitializedGroupSize, UninitializedGroupArchitecture)

	return ccacheManager, nil
}

// This function returns groupName="common" and groupSize=0 if any failure is
// encountered. This allows the ccachemanager to 'hide' the details of packages
// that are not part of any remote storage group.
func (m *CCacheManager) findGroup(basePackageName string) (groupName string, groupEnabled bool, groupSize int) {
	//
	// We assume that:
	// - all packages want ccache enabled for them.
	// - each package belongs to its own group.
	// Then, we iterate to see if those assumptions do not apply for a certain
	// package and overwrite them with the actual configuration.
	//
	groupName = basePackageName
	groupEnabled = true
	groupSize = 1
	found := false

	for _, group := range m.Configuration.Groups {
		for _, packageName := range group.PackageNames {
			if packageName == basePackageName {
				logger.Log.Infof("  found group (%s) for base package (%s)...", group.Name, basePackageName)
				groupName = group.Name
				groupEnabled = group.Enabled
				groupSize = len(group.PackageNames)
				if !groupEnabled {
					logger.Log.Infof("  ccache is explicitly disabled for this group in the ccache configuration.")
				}
				found = true
				break
			}
		}
		if found {
			break
		}
	}

	return groupName, groupEnabled, groupSize
}

func (m *CCacheManager) findCCacheGroupInfo(groupName string) (groupEnabled bool, groupSize int) {
	//
	// We assume that:
	// - all packages want ccache enabled for them.
	// - each package belongs to its own group.
	// Then, we iterate to see if those assumptions do not apply for a certain
	// package and overwrite them with the actual configuration.
	//
	groupEnabled = true
	groupSize = 1

	for _, group := range m.Configuration.Groups {
		if groupName == group.Name {
			groupEnabled = group.Enabled
			groupSize = len(group.PackageNames)
		}
	}

	return groupEnabled, groupSize
}

func (m *CCacheManager) buildPkgCCacheDir(pkgCCacheGroupName string, pkgArchitecture string) (string, error) {
	if pkgArchitecture == "" {
		return "", errors.New("CCache package pkgArchitecture cannot be empty.")
	}
	if pkgCCacheGroupName == "" {
		return "", errors.New("CCache package group name cannot be empty.")
	}
	return m.RootWorkDir + "/" + pkgArchitecture + "/" + pkgCCacheGroupName, nil
}

func (m *CCacheManager) DownloadPkgGroupCCache() (err error) {

	logger.Log.Infof("* processing download of ccache artifacts...")

	remoteStoreConfig := m.Configuration.RemoteStoreConfig
	if !remoteStoreConfig.DownloadEnabled {
		logger.Log.Infof("  downloading archived ccache artifacts is disabled. Skipping download...")
		return nil
	}

	logger.Log.Infof("  downloading (%s) to (%s)...", m.CurrentPkgGroup.TarFile.RemoteSourcePath, m.CurrentPkgGroup.TarFile.LocalSourcePath)
	err = m.AzureBlobStorage.Download(context.Background(), remoteStoreConfig.ContainerName, m.CurrentPkgGroup.TarFile.RemoteSourcePath, m.CurrentPkgGroup.TarFile.LocalSourcePath)
	if err != nil {
		return fmt.Errorf("Unable to download ccache archive:\n%w", err)
	}

	err = uncompressFile(m.CurrentPkgGroup.TarFile.LocalSourcePath, m.CurrentPkgGroup.CCacheDir)
	if err != nil {
		return fmt.Errorf("Unable uncompress ccache files from archive:\n%w", err)
	}

	return nil
}

func (m *CCacheManager) UploadPkgGroupCCache() (err error) {

	logger.Log.Infof("* processing upload of ccache artifacts...")

	// Check if ccache has actually generated any content.
	// If it has, it would have created a specific folder structure - so,
	// checking for folders is reasonable enough.
	pkgCCacheDirContents, err := directory.GetChildDirs(m.CurrentPkgGroup.CCacheDir)
	if err != nil {
		return fmt.Errorf("Failed to enumerate the contents of (%s):\n%w", m.CurrentPkgGroup.CCacheDir, err)
	}
	if len(pkgCCacheDirContents) == 0 {
		logger.Log.Infof("  %s is empty. Nothing to archive and upload. Skipping...", m.CurrentPkgGroup.CCacheDir)
		return nil
	}

	remoteStoreConfig := m.Configuration.RemoteStoreConfig
	if !remoteStoreConfig.UploadEnabled {
		logger.Log.Infof("  ccache update is disabled for this build.")
		return nil
	}

	err = compressDir(m.CurrentPkgGroup.CCacheDir, m.CurrentPkgGroup.TarFile.LocalTargetPath)
	if err != nil {
		return fmt.Errorf("Unable compress ccache files into archive:\n%w", err)
	}

	// Upload the ccache archive
	logger.Log.Infof("  uploading ccache archive (%s) to (%s)...", m.CurrentPkgGroup.TarFile.LocalTargetPath, m.CurrentPkgGroup.TarFile.RemoteTargetPath)
	err = m.AzureBlobStorage.Upload(context.Background(), m.CurrentPkgGroup.TarFile.LocalTargetPath, remoteStoreConfig.ContainerName, m.CurrentPkgGroup.TarFile.RemoteTargetPath)
	if err != nil {
		return fmt.Errorf("Unable to upload ccache archive:\n%w", err)
	}

	if remoteStoreConfig.UpdateLatest {
		logger.Log.Infof("  update latest is enabled.")
		// If KeepLatestOnly is true, we need to capture the current source
		// ccache archive path which is about to be dereferenced. That way,
		// we can delete it after we update the latest tag to point to the
		// new ccache archive.
		//
		// First we assume it does not exist (i.e. first time to run).
		//
		previousLatestTarSourcePath := ""
		if remoteStoreConfig.KeepLatestOnly {
			logger.Log.Infof("  keep latest only is enabled. Capturing path to previous ccache archive if it exists...")
			// getLatestTag() will check locally first if the tag file has
			// been downloaded and use it. If not, it will attempt to
			// download it. If not, then there is no way to get to the
			// previous latest tar (if it exists at all).
			latestTag, err := m.CurrentPkgGroup.getLatestTag(m.AzureBlobStorage, m.Configuration.RemoteStoreConfig.ContainerName)
			if err == nil {
				// build the archive remote path based on the latestTag.
				previousLatestTarSourcePath = m.CurrentPkgGroup.buildTarRemotePath(latestTag)
				logger.Log.Infof("  (%s) is about to be de-referenced.", previousLatestTarSourcePath)
			} else {
				logger.Log.Warnf("  unable to get the latest ccache tag. This might be the first run and no latest ccache tag has been uploaded before.")
			}
		}

		// Create the latest tag file...
		logger.Log.Infof("  creating a tag file (%s) with content: (%s)...", m.CurrentPkgGroup.TagFile.LocalTargetPath, remoteStoreConfig.UploadFolder)
		err = ioutil.WriteFile(m.CurrentPkgGroup.TagFile.LocalTargetPath, []byte(remoteStoreConfig.UploadFolder), 0644)
		if err != nil {
			return fmt.Errorf("Unable to write tag information to temporary file:\n%w", err)
		}

		// Upload the latest tag file...
		logger.Log.Infof("  uploading tag file (%s) to (%s)...", m.CurrentPkgGroup.TagFile.LocalTargetPath, m.CurrentPkgGroup.TagFile.RemoteTargetPath)
		err = m.AzureBlobStorage.Upload(context.Background(), m.CurrentPkgGroup.TagFile.LocalTargetPath, remoteStoreConfig.ContainerName, m.CurrentPkgGroup.TagFile.RemoteTargetPath)
		if err != nil {
			return fmt.Errorf("Unable to upload ccache archive:\n%w", err)
		}

		if remoteStoreConfig.KeepLatestOnly {
			logger.Log.Infof("  keep latest only is enabled. Checking if we need to remove previous latest archive...")
			logger.Log.Infof("  - old: (%s)", previousLatestTarSourcePath)
			logger.Log.Infof("  - new: (%s)", m.CurrentPkgGroup.TarFile.RemoteTargetPath)
			if previousLatestTarSourcePath == "" {
				logger.Log.Infof("  cannot remove old archive with an empty name. No previous ccache archive to remove.")
			} else if previousLatestTarSourcePath == m.CurrentPkgGroup.TarFile.RemoteTargetPath {
				logger.Log.Infof("  previous latest archive has been overwritten with the current latest archive. Nothing to remove.")
			} else {
				logger.Log.Infof("  removing ccache archive (%s) from remote store...", previousLatestTarSourcePath)
				err = m.AzureBlobStorage.Delete(context.Background(), remoteStoreConfig.ContainerName, previousLatestTarSourcePath)
				if err != nil {
					return fmt.Errorf("Unable to remove previous ccache archive:\n%w", err)
				}
			}
		}
	}

	return nil
}

// After building a package or more, the ccache folder is expected to look as
// follows:
//
// <rootDir> (i.e. /ccache)
//
//	<m.LocalDownloadsDir>
//	<m.LocalUploadsDir>
//	<m.RootWorkDir>
//	  x86_64
//	    <groupName-1>
//	    <groupName-2>
//	  noarch
//	    <groupName-3>
//	    <groupName-4>
//
// This function is typically called at the end of the build - after all
// packages have completed building.
//
// At that point, there is not per package information about the group name
// or the architecture.
//
// We use this directory structure to encode the per package group information
// at build time, so we can use them now.
func (m *CCacheManager) UploadMultiPkgGroupCCaches() (err error) {

	architectures, err := directory.GetChildDirs(m.RootWorkDir)
	errorsOccured := false
	if err != nil {
		return fmt.Errorf("failed to enumerate ccache child folders under (%s):\n%w", m.RootWorkDir, err)
	}

	for _, architecture := range architectures {
		groupNames, err := directory.GetChildDirs(filepath.Join(m.RootWorkDir, architecture))
		if err != nil {
			logger.Log.Warnf("failed to enumerate child folders under (%s):\n%v", m.RootWorkDir, err)
			errorsOccured = true
		} else {
			for _, groupName := range groupNames {
				// Enable this continue only if we enable uploading as
				// soon as packages are done building.
				groupEnabled, groupSize := m.findCCacheGroupInfo(groupName)

				if !groupEnabled {
					// This should never happen unless a previous run had it
					// enabled and the folder got created. The correct behavior
					// is that the folder is not even created before the pkg
					// build starts and hence by reaching this method, it
					// should not be there.
					//
					logger.Log.Infof("  ccache is explicitly disabled for this group in the ccache configuration. Skipping...")
					continue
				}

				if groupSize < 2 {
					// This has either been processed earlier or there is
					// nothing to process.
					continue
				}

				groupCCacheDir, err := m.buildPkgCCacheDir(groupName, architecture)
				if err != nil {
					logger.Log.Warnf("Failed to get ccache dir for architecture (%s) and group name (%s):\n%v", architecture, groupName, err)
					errorsOccured = true
				}
				logger.Log.Infof("  processing ccache folder (%s)...", groupCCacheDir)

				m.setCurrentPkgGroupInternal(groupName, groupEnabled, groupSize, architecture)

				err = m.UploadPkgGroupCCache()
				if err != nil {
					errorsOccured = true
					logger.Log.Warnf("CCache will not be archived for (%s) (%s):\n%v", architecture, groupName, err)
				}
			}
		}
	}

	if errorsOccured {
		return errors.New("CCache archiving and upload failed. See above warnings for more details.")
	}
	return nil
}
