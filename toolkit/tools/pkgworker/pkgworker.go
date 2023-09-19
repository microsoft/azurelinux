// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// A worker for building packages locally

package main

import (
	"context"
	"errors"
	"fmt"
	"io/ioutil"
	"os"
	"path/filepath"
	"regexp"
	"strings"
	"time"

    // "github.com/microsoft/CBL-Mariner/toolkit/tools/internal/ccache"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/exe"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/file"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/packagerepo/repomanager/rpmrepomanager"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/rpm"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/safechroot"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/shell"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/sliceutils"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/tdnf"

	"github.com/Azure/azure-sdk-for-go/sdk/azidentity"
	"github.com/Azure/azure-sdk-for-go/sdk/storage/azblob"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/jsonutils"

	"gopkg.in/alecthomas/kingpin.v2"
)

type CCacheGroup struct {
	Name     string `json:"name"`
    PackageNames []string `json:"packageNames"`
}

type RemoteStore struct {
	Type           string `json:"type"`
	TenantId       string `json:"tenantId"`
	UserName       string `json:"userName"`
	Password       string `json:"password"`
	StorageAccount string `json:"storageAccount"`
	ContainerName  string `json:"containerName"`
	VersionsFolder string `json:"versionsFolder"`
	InputFolder    string `json:"inputFolder"`
	UpdateEnabled  bool   `json:"updateEnabled"`
	UpdateFolder   string `json:"updateFolder"`
}

type CCacheConfiguration struct {
	RemoteStore RemoteStore `json:"remoteStore"`
	Groups   []CCacheGroup  `json:"groups"`
}

func GetCCacheRemoteStore() (remoteStore RemoteStore, err error) {
	ccacheGroupsFile := "resources/manifests/package/ccache_configuration.json"
	logger.Log.Infof("Loading ccache configuration file: %s", ccacheGroupsFile)
	var ccacheConfiguration CCacheConfiguration
	err = jsonutils.ReadJSONFile(ccacheGroupsFile, &ccacheConfiguration)
	if err != nil {
		logger.Log.Infof("Failed to load file. %v", err)
	} else {
		logger.Log.Infof("Loaded file.")

		logger.Log.Infof("  Type          : %s", ccacheConfiguration.RemoteStore.Type)
		logger.Log.Infof("  TenantId      : %s", ccacheConfiguration.RemoteStore.TenantId)
		logger.Log.Infof("  UserName      : %s", ccacheConfiguration.RemoteStore.UserName)
		// logger.Log.Infof("  Password      : %s", ccacheConfiguration.RemoteStore.Password)
		logger.Log.Infof("  StorageAccount: %s", ccacheConfiguration.RemoteStore.StorageAccount)
		logger.Log.Infof("  ContainerName : %s", ccacheConfiguration.RemoteStore.ContainerName)
		logger.Log.Infof("  Versionsfolder: %s", ccacheConfiguration.RemoteStore.VersionsFolder)
		logger.Log.Infof("  InputFolder   : %s", ccacheConfiguration.RemoteStore.InputFolder)
		logger.Log.Infof("  UpdateEnabled : %v", ccacheConfiguration.RemoteStore.UpdateEnabled)
		logger.Log.Infof("  UpdateFolder  : %s", ccacheConfiguration.RemoteStore.UpdateFolder)
	}

	return ccacheConfiguration.RemoteStore, err	
}

const (
	chrootLocalRpmsDir      = "/localrpms"
	chrootLocalToolchainDir = "/toolchainrpms"
	chrootLocalRpmsCacheDir = "/upstream-cached-rpms"
	chrootCcacheDir         = "/ccache-dir"
)

var (
	app                  = kingpin.New("pkgworker", "A worker for building packages locally")
	srpmFile             = exe.InputFlag(app, "Full path to the SRPM to build")
	workDir              = app.Flag("work-dir", "The directory to create the build folder").Required().String()
	workerTar            = app.Flag("worker-tar", "Full path to worker_chroot.tar.gz").Required().ExistingFile()
	repoFile             = app.Flag("repo-file", "Full path to local.repo").Required().ExistingFile()
	rpmsDirPath          = app.Flag("rpm-dir", "The directory to use as the local repo and to submit RPM packages to").Required().ExistingDir()
	srpmsDirPath         = app.Flag("srpm-dir", "The output directory for source RPM packages").Required().String()
	toolchainDirPath     = app.Flag("toolchain-rpms-dir", "Directory that contains already built toolchain RPMs. Should contain a top level directory for each architecture.").Required().ExistingDir()
	cacheDir             = app.Flag("cache-dir", "The cache directory containing downloaded dependency RPMS from CBL-Mariner Base").Required().ExistingDir()
	ccacheDirTarsIn      = app.Flag("ccache-dir-tars-in", "<ToDo>").Required().String()
	ccacheDirTarsOut     = app.Flag("ccache-dir-tars-out", "<ToDo>").Required().String()
	ccacheDir            = app.Flag("ccache-dir", "The directory used to store ccache outputs").Required().String()
	ccacheGroupName      = app.Flag("ccache-group-name", "<ToDo>").Required().String()
	noCleanup            = app.Flag("no-cleanup", "Whether or not to delete the chroot folder after the build is done").Bool()
	distTag              = app.Flag("dist-tag", "The distribution tag the SPEC will be built with.").Required().String()
	distroReleaseVersion = app.Flag("distro-release-version", "The distro release version that the SRPM will be built with").Required().String()
	distroBuildNumber    = app.Flag("distro-build-number", "The distro build number that the SRPM will be built with").Required().String()
	rpmmacrosFile        = app.Flag("rpmmacros-file", "Optional file path to an rpmmacros file for rpmbuild to use").ExistingFile()
	runCheck             = app.Flag("run-check", "Run the check during package build").Bool()
	packagesToInstall    = app.Flag("install-package", "Filepaths to RPM packages that should be installed before building.").Strings()
	outArch              = app.Flag("out-arch", "Architecture of resulting package").String()
	useCcache            = app.Flag("use-ccache", "Automatically install and use ccache during package builds").Bool()
	maxCPU               = app.Flag("max-cpu", "Max number of CPUs used for package building").Default("").String()

	logFile  = exe.LogFileFlag(app)
	logLevel = exe.LogLevelFlag(app)
)

var (
	packageUnavailableRegex = regexp.MustCompile(`^No package \\x1b\[1m\\x1b\[30m(.+) \\x1b\[0mavailable`)
)

func main() {
	app.Version(exe.ToolkitVersion)
	kingpin.MustParse(app.Parse(os.Args[1:]))
	logger.InitBestEffort(*logFile, *logLevel)

	rpmsDirAbsPath, err := filepath.Abs(*rpmsDirPath)
	logger.PanicOnError(err, "Unable to find absolute path for RPMs directory '%s'", *rpmsDirPath)

	toolchainDirAbsPath, err := filepath.Abs(*toolchainDirPath)
	logger.PanicOnError(err, "Unable to find absolute path for toolchain RPMs directory '%s'", *toolchainDirPath)

	srpmsDirAbsPath, err := filepath.Abs(*srpmsDirPath)
	logger.PanicOnError(err, "Unable to find absolute path for SRPMs directory '%s'", *srpmsDirPath)

	chrootDir := buildChrootDirPath(*workDir, *srpmFile, *runCheck)

	defines := rpm.DefaultDefinesWithDist(*runCheck, *distTag)
	defines[rpm.DistroReleaseVersionDefine] = *distroReleaseVersion
	defines[rpm.DistroBuildNumberDefine] = *distroBuildNumber
	defines[rpm.MarinerModuleLdflagsDefine] = "-Wl,-dT,%{_topdir}/BUILD/module_info.ld"
	if *useCcache {
		defines[rpm.MarinerCCacheDefine] = "true"
	}
	if *maxCPU != "" {
		defines[rpm.MaxCPUDefine] = *maxCPU
	}

	builtRPMs, err := buildSRPMInChroot(chrootDir, rpmsDirAbsPath, toolchainDirAbsPath, *workerTar, *srpmFile, *repoFile, *rpmmacrosFile, *outArch, defines, *noCleanup, *runCheck, *packagesToInstall, *useCcache)
	logger.PanicOnError(err, "Failed to build SRPM '%s'. For details see log file: %s .", *srpmFile, *logFile)

	err = copySRPMToOutput(*srpmFile, srpmsDirAbsPath)
	logger.PanicOnError(err, "Failed to copy SRPM '%s' to output directory '%s'.", *srpmFile, rpmsDirAbsPath)

	// On success write a comma-seperated list of RPMs built to stdout that can be parsed by the invoker.
	// Any output from logger will be on stderr so stdout will only contain this output.
	if !*runCheck {
		fmt.Print(strings.Join(builtRPMs, ","))
	}
}

func copySRPMToOutput(srpmFilePath, srpmOutputDirPath string) (err error) {
	srpmFileName := filepath.Base(srpmFilePath)
	srpmOutputFilePath := filepath.Join(srpmOutputDirPath, srpmFileName)

	err = file.Copy(srpmFilePath, srpmOutputFilePath)

	return
}

func buildChrootDirPath(workDir, srpmFilePath string, runCheck bool) (chrootDirPath string) {
	buildDirName := strings.TrimSuffix(filepath.Base(*srpmFile), ".src.rpm")
	if runCheck {
		buildDirName += "_TEST_BUILD"
	}

	return filepath.Join(workDir, buildDirName)
}

// https://pkg.go.dev/github.com/Azure/azure-sdk-for-go/sdk/storage/azblob#section-readme
func upload(
	theClient *azblob.Client,
	ctx context.Context,
	fullFileName string,
	containerName string,
	blobName string) (err error) {

	logger.Log.Infof("Uploading %s...", fullFileName)

	localFile, err := os.OpenFile(fullFileName, os.O_RDONLY, 0)
	if err != nil {
		fmt.Printf("Failed to open local file for upload. Error: %v", err)
		return err
	}
	if localFile == nil {
		fmt.Printf("Failed to open local file for upload 2.")
	}
	defer localFile.Close()

	// close the file after it is no longer required.
	// defer func(file *os.File) {
	// 	err = file.Close()
	// 	handleError(err)
	// }(fileHandler)

	logger.Log.Infof("Container %s", containerName)
	logger.Log.Infof("blob %s", blobName)

	_, err = theClient.UploadFile(ctx, containerName, blobName, localFile, nil)
	if err != nil {
		fmt.Printf("Failed to upload local file to blob. Error: %v.", err)
		return err
	}

	return nil
}

func download(
	theClient *azblob.Client,
	ctx context.Context,
	containerName string,
	blobName string,
	fullFileName string) (err error) {

	localFile, err := os.Create(fullFileName)
	if err != nil {
		fmt.Printf("Failed to create local file for download. Error: %v", err)
		return err
	}
	defer localFile.Close()

	_, err = theClient.DownloadFile(ctx, containerName, blobName, localFile, nil)
	if err != nil {
		fmt.Printf("Failed to download blob to local file. Error: %v.", err)
		return err
	}

	return nil
}

const (
	CCacheVersionSuffix = "-latest-build.txt"
	CCacheTarSuffix = "-ccache.tar.gz"
	AnonymousAccess = 0
	AuthenticatedAccess = 1
)

func createContainerClient(remoteStore RemoteStore, authenticationType int) (client *azblob.Client, err error ) {

	url := "https://" + remoteStore.StorageAccount + ".blob.core.windows.net/"

	if authenticationType == AnonymousAccess {

		client, err := azblob.NewClientWithNoCredential(url, nil)
		if err != nil {
			logger.Log.Warnf("Unable to init azure blob storage read-only client. Error: %v", err)
			return nil, err
		}

		return client, nil

	} else if authenticationType == AuthenticatedAccess {

		credential, err := azidentity.NewClientSecretCredential(remoteStore.TenantId, remoteStore.UserName, remoteStore.Password, nil)
		if err != nil {
			logger.Log.Warnf("Unable to init azure identity. Error: %v", err)
			return nil, err
		}

		client, err = azblob.NewClient(url, credential, nil)
		if err != nil {
			logger.Log.Warnf("Unable to init azure blob storage read-write client. Error: %v", err)
			return nil, err
		}

		return client, nil

	} else {
		logger.Log.Warnf("Unknown authentication type.")
		return nil, errors.New("Unknown authentication type.")
	}
}


// ensure the following are set:
// - ccacheDirTarsIn
// - ccacheDirTarsOut
// - ccacheDir
func installCCache(ccacheDirTarsIn string, ccacheGroupName string) (err error) {

	logger.Log.Infof("ccache is enabled - Installing --------------------")

	logger.Log.Infof("  checking if ccache working folder (%s) exists.", *ccacheDir)
	_, err = os.Stat(*ccacheDir)
	if err == nil {
		logger.Log.Infof("  CCache working folder does exists. Re-using...")
		return nil
	}

	logger.Log.Infof("  creating ccache working folder...")
	err = os.Mkdir(*ccacheDir, 0755)
	if err != nil {
		logger.Log.Warnf("Unable to create ccache working folder. Error: %v", err)
		return err
	}

	logger.Log.Infof("  checking if ccache tars input folder (%s) exists.", ccacheDirTarsIn)
	_, err = os.Stat(ccacheDirTarsIn)
	if err != nil {
		logger.Log.Infof("  creating ccache tars input folder...")
		err = os.Mkdir(ccacheDirTarsIn, 0755)
		if err != nil {
			logger.Log.Warnf("Unable to create ccache working folder. Error: %v", err)
			return err
		}			
	}

	logger.Log.Infof("  retrieving remote store information...")
	remoteStore, err := GetCCacheRemoteStore()
	if err != nil {
		logger.Log.Warnf("Unable to get ccache remote store configuration. Error: %v", err)
		return err
	}

	// Connect to blob storage...
	logger.Log.Infof("  creating container client...")
	theClient, err := createContainerClient(remoteStore, AnonymousAccess)
	if err != nil {
		logger.Log.Warnf("Unable to init azure blob storage client. Error: %v", err)
		return err
	}

	if remoteStore.InputFolder == "latest" {

		logger.Log.Infof("  ccache is configured to use the latest...")

		// Download the versions file...
		var ccacheVersionFullBlobName = remoteStore.VersionsFolder + "/" + ccacheGroupName + CCacheVersionSuffix
		var ccacheInputVersionFullPath = ccacheDirTarsIn + "/" + ccacheGroupName + CCacheVersionSuffix

		logger.Log.Infof("  downloading  (%s) to (%s)...", ccacheVersionFullBlobName, ccacheInputVersionFullPath)
		downloadStartTime := time.Now()
		err = download(theClient, context.Background(), remoteStore.ContainerName, ccacheVersionFullBlobName, ccacheInputVersionFullPath)
		if err != nil {
			logger.Log.Warnf("Unable to download ccache archive. Error: %v", err)
			return err
		}
		downloadEndTime := time.Now()
		logger.Log.Infof("  download time: %v", downloadEndTime.Sub(downloadStartTime))

		// Read the text contents...
		ccacheInputVersionBuffer, err := ioutil.ReadFile(ccacheInputVersionFullPath)
		if err != nil {
			logger.Log.Warnf("Unable to read ccache version file contents. Error: %v", err)
			return err
		}

		remoteStore.InputFolder = string(ccacheInputVersionBuffer) 

		logger.Log.Infof("  ccache latest build is (%s)...", remoteStore.InputFolder)
	}

	// Download the actual cache...
	var ccacheFullBlobName = remoteStore.InputFolder + "/" + ccacheGroupName + CCacheTarSuffix
	var ccacheInputTarFullPath = ccacheDirTarsIn + "/" + ccacheGroupName + CCacheTarSuffix

	logger.Log.Infof("  downloading (%s) to (%s)...", ccacheFullBlobName, ccacheInputTarFullPath)
	downloadStartTime := time.Now()
	err = download(theClient, context.Background(), remoteStore.ContainerName, ccacheFullBlobName, ccacheInputTarFullPath)
	if err != nil {
		logger.Log.Warnf("Unable to download ccache archive. Error: %v", err)
		return err
	}
	downloadEndTime := time.Now()
	logger.Log.Infof("  download time: %v", downloadEndTime.Sub(downloadStartTime))

	logger.Log.Infof("  uncompressing (%s) into (%s).", ccacheInputTarFullPath, *ccacheDir)
	uncompressStartTime := time.Now()
	tarArgs := []string{
		"xf",
		ccacheInputTarFullPath,
		"-C",
		*ccacheDir,
		"."}

	_, stderr, err := shell.Execute("tar", tarArgs...)
	if err != nil {
		logger.Log.Warnf("Unable extract ccache files from archive. Error: %v", stderr)
		return err
	}
	uncompressEndTime := time.Now()
	logger.Log.Infof("  uncompress time: %v", uncompressEndTime.Sub(uncompressStartTime))

	return nil
}

// ensure the following are set:
// - ccacheDirTarsIn
// - ccacheDirTarsOut
// - ccacheDir
func archiveCCache(ccacheDirTarsOut string, ccacheGroupName string) (err error) {

	logger.Log.Infof("ccache is enabled - Capturing --------------------")
    remoteStore, err := GetCCacheRemoteStore()
	if err != nil {
		logger.Log.Warnf("Unable to get ccache remote store configuration. Error: %v", err)
		return err
	}

	if !remoteStore.UpdateEnabled {
		logger.Log.Infof("CCache update is disabled for this build.")
		return
	}

	// Ensure the output folder exists...
	logger.Log.Infof("  ensuring ccache tar output folder (%s) exists..", ccacheDirTarsOut)
	_, err = os.Stat(ccacheDirTarsOut)
	if err != nil {
		if os.IsNotExist(err) {
			// If not, create it...
			err = os.Mkdir(ccacheDirTarsOut, 0755)
			if err != nil {
				logger.Log.Warnf("Unable create ccache out tar folder. Error: %v", err)
				return err
			}
		} else {
			logger.Log.Warnf("An error occured while check if ccache out tar folder exists. Error: %v", err)
			return err
		}
	}

	// Ensure the output file does not exist...
	ccacheOutputTarFullPath := ccacheDirTarsOut + "/" + ccacheGroupName + CCacheTarSuffix

	logger.Log.Infof("  removing older ccache tar output file (%s) if it exists...", ccacheOutputTarFullPath)
	_, err = os.Stat(ccacheOutputTarFullPath)
	if err == nil {
		logger.Log.Infof("  found ccache tar output file (%s). Removing...", ccacheOutputTarFullPath)
		err = os.Remove(ccacheOutputTarFullPath)
		if err != nil {
			logger.Log.Warnf("  unable to delete ccache out tar. Error: %v", err)
			return err
		}
	}
	
	// Create the archive...
	logger.Log.Infof("  compressing (%s) into (%s).", *ccacheDir, ccacheOutputTarFullPath)
	compressStartTime := time.Now()
	tarArgs := []string{
		"cf",
		ccacheOutputTarFullPath,
		"-C",
		*ccacheDir,
		"."}

	_, stderr, err := shell.Execute("tar", tarArgs...)
	if err != nil {
		logger.Log.Warnf("Unable compress ccache files itno archive. Error: %v", stderr)
		return err	
	}
	compressEndTime := time.Now()
	logger.Log.Infof("  compress time: %s", compressEndTime.Sub(compressStartTime))

	// ** Temporary ** Uploading should take place at the end of the build
	// because other package family group members may update it.
	//

	// Test uploading
	logger.Log.Infof("  connecting to azure storage blob...")
	theClient, err := createContainerClient(remoteStore, AuthenticatedAccess)
	if err != nil {
		logger.Log.Warnf("Unable create azure blob storage client. Error: %v", stderr)
		return err
	}

	// Upload the ccache archive
	var outputBlobName = remoteStore.UpdateFolder + "/" + ccacheGroupName + CCacheTarSuffix

	logger.Log.Infof("  uploading ccache archive (%s) to (%s)...", ccacheOutputTarFullPath, outputBlobName)

	uploadStartTime := time.Now()
	err = upload(theClient, context.Background(), ccacheOutputTarFullPath, remoteStore.ContainerName, outputBlobName)
	if err != nil {
		logger.Log.Warnf("Unable to upload ccache archive. Error: %v", err)
		return err
	}
	uploadEndTime := time.Now()
	logger.Log.Infof("  upload Time: %s", uploadEndTime.Sub(uploadStartTime))

	// Create the latest version file...

	logger.Log.Infof("  creating a temporary version file with content: (%s)...", remoteStore.UpdateFolder)

	tempFile, err := ioutil.TempFile("", ccacheGroupName + CCacheVersionSuffix)
	if err != nil {
		logger.Log.Warnf("Unable to create temporary file to hold new version information. Error: %v", err)
		return err
	}
	defer tempFile.Close()

	_, err = tempFile.WriteString(remoteStore.UpdateFolder)
	if err != nil {
		logger.Log.Warnf("Unable to write version information to temporary file. Error: %v", err)
		return err
	}	

    // Upload the latest version file...
	var ccacheVersionFullBlobName = remoteStore.VersionsFolder + "/" + ccacheGroupName + CCacheVersionSuffix

	logger.Log.Infof("  uploading latest version (%s) to (%s)...", tempFile.Name(), ccacheVersionFullBlobName)

	uploadStartTime = time.Now()
	err = upload(theClient, context.Background(), tempFile.Name(), remoteStore.ContainerName, ccacheVersionFullBlobName)
	if err != nil {
		logger.Log.Warnf("Unable to upload ccache archive. Error: %v", err)
		return err
	}
	uploadEndTime = time.Now()
	logger.Log.Infof("  upload Time: %s", uploadEndTime.Sub(uploadStartTime))

	// Do no clean it because it might be used by other packages in the same
	// ccache group...
	//
	// logger.Log.Infof("Cleaning ccache working folder (%s).", *ccacheDir)	
	// err = os.RemoveAll(*ccacheDir)
	// if err != nil {
	// 	logger.Log.Warnf("Unable rermove ccache working directory. Error: %v", err)
	// }

	return
}

func buildSRPMInChroot(chrootDir, rpmDirPath, toolchainDirPath, workerTar, srpmFile, repoFile, rpmmacrosFile, outArch string, defines map[string]string, noCleanup, runCheck bool, packagesToInstall []string, useCcache bool) (builtRPMs []string, err error) {
	const (
		buildHeartbeatTimeout = 30 * time.Minute

		existingChrootDir = false

		overlaySource           = ""
		overlayWorkDirRpms      = "/overlaywork_rpms"
		overlayWorkDirToolchain = "/overlaywork_toolchain"
	)

	srpmBaseName := filepath.Base(srpmFile)

	quit := make(chan bool)
	go func() {
		logger.Log.Infof("Building (%s).", srpmBaseName)

		for {
			select {
			case <-quit:
				if err == nil {
					logger.Log.Infof("Built (%s) -> %v.", srpmBaseName, builtRPMs)
				}
				return
			case <-time.After(buildHeartbeatTimeout):
				logger.Log.Infof("Heartbeat: still building (%s).", srpmBaseName)
			}
		}
	}()
	defer func() {
		quit <- true
	}()

	logger.Log.Infof("** Running ccache POC. **")

	if useCcache {
		err = installCCache(*ccacheDirTarsIn, *ccacheGroupName)
		if err != nil {
			logger.Log.Warnf("CCache will be disabled.")
		}
	}
	
	// Create the chroot used to build the SRPM
	chroot := safechroot.NewChroot(chrootDir, existingChrootDir)

	outRpmsOverlayMount, outRpmsOverlayExtraDirs := safechroot.NewOverlayMountPoint(chroot.RootDir(), overlaySource, chrootLocalRpmsDir, rpmDirPath, chrootLocalRpmsDir, overlayWorkDirRpms)
	toolchainRpmsOverlayMount, toolchainRpmsOverlayExtraDirs := safechroot.NewOverlayMountPoint(chroot.RootDir(), overlaySource, chrootLocalToolchainDir, toolchainDirPath, chrootLocalToolchainDir, overlayWorkDirToolchain)
	rpmCacheMount := safechroot.NewMountPoint(*cacheDir, chrootLocalRpmsCacheDir, "", safechroot.BindMountPointFlags, "")
	ccacheMount := safechroot.NewMountPoint(*ccacheDir, chrootCcacheDir, "", safechroot.BindMountPointFlags, "")
	mountPoints := []*safechroot.MountPoint{outRpmsOverlayMount, toolchainRpmsOverlayMount, rpmCacheMount, ccacheMount}
	extraDirs := append(outRpmsOverlayExtraDirs, chrootLocalRpmsCacheDir, chrootCcacheDir)
	extraDirs = append(extraDirs, toolchainRpmsOverlayExtraDirs...)

	err = chroot.Initialize(workerTar, extraDirs, mountPoints)
	if err != nil {
		return
	}
	defer chroot.Close(noCleanup)

	// Place extra files that will be needed to build into the chroot
	srpmFileInChroot, err := copyFilesIntoChroot(chroot, srpmFile, repoFile, rpmmacrosFile, runCheck)
	if err != nil {
		return
	}

	err = chroot.Run(func() (err error) {
		return buildRPMFromSRPMInChroot(srpmFileInChroot, outArch, runCheck, defines, packagesToInstall, useCcache)
	})
	if err != nil {
		return
	}

	if !runCheck {
		builtRPMs, err = moveBuiltRPMs(chroot.RootDir(), rpmDirPath)
	}

	if useCcache {
		err = archiveCCache(*ccacheDirTarsOut, *ccacheGroupName)
		if err != nil {
			logger.Log.Warnf("CCache will not be archived.")
		}
	}
	return
}

func buildRPMFromSRPMInChroot(srpmFile, outArch string, runCheck bool, defines map[string]string, packagesToInstall []string, useCcache bool) (err error) {
	// Convert /localrpms into a repository that a package manager can use.
	err = rpmrepomanager.CreateRepo(chrootLocalRpmsDir)
	if err != nil {
		return
	}

	// Convert /toolchainrpms into a repository that a package manager can use.
	err = rpmrepomanager.CreateRepo(chrootLocalToolchainDir)
	if err != nil {
		return
	}

	// install any additional packages, such as build dependencies.
	err = tdnfInstall(packagesToInstall)
	if err != nil {
		return
	}

	if useCcache {
		ccachePkgName := []string{"ccache"}
		logger.Log.Infof("USE_CCACHE: installing package: %s", ccachePkgName[0])
		err = tdnfInstall(ccachePkgName)
		if err != nil {
			return
		}
	}

	// Remove all libarchive files on the system before issuing a build.
	// If the build environment has libtool archive files present, gnu configure
	// could detect it and create more libtool archive files which can cause
	// build failures.
	err = removeLibArchivesFromSystem()
	if err != nil {
		return
	}

	// Build the SRPM
	if runCheck {
		err = rpm.TestRPMFromSRPM(srpmFile, outArch, defines)
	} else {
		err = rpm.BuildRPMFromSRPM(srpmFile, outArch, defines)
	}

	return
}

func moveBuiltRPMs(chrootRootDir, dstDir string) (builtRPMs []string, err error) {
	const (
		chrootRpmBuildDir = "/usr/src/mariner/RPMS"
		rpmExtension      = ".rpm"
	)

	rpmOutDir := filepath.Join(chrootRootDir, chrootRpmBuildDir)
	err = filepath.Walk(rpmOutDir, func(path string, info os.FileInfo, fileErr error) (err error) {
		if fileErr != nil {
			return fileErr
		}

		// Only copy regular files (not unix sockets, directories, links, ...)
		if !info.Mode().IsRegular() {
			return
		}

		if !strings.HasSuffix(path, rpmExtension) {
			return
		}

		// Get the relative path of the RPM, this will include the architecture directory it lives in.
		// Then join the relative path to the destination directory, this will ensure the RPM gets placed
		// in its correct architecture directory.
		relPath, err := filepath.Rel(rpmOutDir, path)
		if err != nil {
			return
		}

		dstFile := filepath.Join(dstDir, relPath)
		err = file.Move(path, dstFile)
		if err != nil {
			return
		}

		builtRPMs = append(builtRPMs, dstFile)
		return
	})

	return
}

func tdnfInstall(packages []string) (err error) {
	const (
		alreadyInstalledPostfix = "is already installed"
		noMatchingPackagesErr   = "Error(1011) : No matching packages"
		packageMatchGroup       = 1
	)

	var (
		releaseverCliArg string
	)

	if len(packages) == 0 {
		return
	}

	// TDNF supports requesting versioned packages in the form of {name}-{version}.{dist}.{arch}.
	// The packages to install list may contain file paths to rpm files so those will need to be filtered:
	// - Strip any .rpm from packages as TDNF does not support requesting a package with the extension.
	// - Strip any filepath from packages.
	for i := range packages {
		packages[i] = filepath.Base(strings.TrimSuffix(packages[i], ".rpm"))
	}

	releaseverCliArg, err = tdnf.GetReleaseverCliArg()
	if err != nil {
		return
	}

	installArgs := []string{"install", "-y", releaseverCliArg}
	installArgs = append(installArgs, packages...)
	stdout, stderr, err := shell.Execute("tdnf", installArgs...)
	foundNoMatchingPackages := false

	if err != nil {
		logger.Log.Warnf("Failed to install build requirements. stderr: %s\nstdout: %s", stderr, stdout)
		// TDNF will output an error if all packages are already installed.
		// Ignore it iff there is no other error present in stderr.
		splitStderr := strings.Split(stderr, "\n")
		for _, line := range splitStderr {
			trimmedLine := strings.TrimSpace(line)
			if trimmedLine == "" {
				continue
			}

			if strings.Contains(trimmedLine, noMatchingPackagesErr) {
				foundNoMatchingPackages = true
			}

			if !strings.HasSuffix(trimmedLine, alreadyInstalledPostfix) && trimmedLine != noMatchingPackagesErr {
				err = fmt.Errorf(trimmedLine)
				return
			}
		}
		err = nil
	}

	// TDNF will ignore unavailable packages that have been requested to be installed without reporting an error code.
	// Search the stdout of TDNF for such a failure and warn the user.
	// This may happen if a SPEC requires the the path to a tool (e.g. /bin/cp), so mark it as a warning for now.
	var failedToInstall []string
	splitStdout := strings.Split(stdout, "\n")
	for _, line := range splitStdout {
		trimmedLine := strings.TrimSpace(line)
		matches := packageUnavailableRegex.FindStringSubmatch(trimmedLine)
		if len(matches) == 0 {
			continue
		}

		failedToInstall = append(failedToInstall, matches[packageMatchGroup])
	}

	// TDNF will output the error "Error(1011) : No matching packages" if all packages could not be found.
	// In this case it will not print any of the individual packages that failed.
	if foundNoMatchingPackages && len(failedToInstall) == 0 {
		failedToInstall = packages
	}

	if len(failedToInstall) != 0 {
		err = fmt.Errorf("unable to install the following packages: %v", failedToInstall)
	}

	return
}

// removeLibArchivesFromSystem removes all libarchive files on the system. If
// the build environment has libtool archive files present, gnu configure could
// detect it and create more libtool archive files which can cause build failures.
func removeLibArchivesFromSystem() (err error) {
	dirsToExclude := []string{"/proc", "/dev", "/sys", "/run", "/ccache-dir"}

	err = filepath.Walk("/", func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}

		// Skip directories that are meant for device files and kernel virtual filesystems.
		// These will not contain .la files and are mounted into the safechroot from the host.
		// Also skip /ccache-dir, which is shared between chroots
		if info.IsDir() && sliceutils.Contains(dirsToExclude, path, sliceutils.StringMatch) {
			return filepath.SkipDir
		}

		if strings.HasSuffix(info.Name(), ".la") {
			return os.Remove(path)
		}

		return nil
	})

	if err != nil {
		logger.Log.Warnf("Unable to remove lib archive file: %s", err)
	}

	return
}

// copyFilesIntoChroot copies several required build specific files into the chroot.
func copyFilesIntoChroot(chroot *safechroot.Chroot, srpmFile, repoFile, rpmmacrosFile string, runCheck bool) (srpmFileInChroot string, err error) {
	const (
		chrootRepoDestDir = "/etc/yum.repos.d"
		chrootSrpmDestDir = "/root/SRPMS"
		resolvFilePath    = "/etc/resolv.conf"
		rpmmacrosDest     = "/usr/lib/rpm/macros.d/macros.override"
	)

	repoFileInChroot := filepath.Join(chrootRepoDestDir, filepath.Base(repoFile))
	srpmFileInChroot = filepath.Join(chrootSrpmDestDir, filepath.Base(srpmFile))

	filesToCopy := []safechroot.FileToCopy{
		safechroot.FileToCopy{
			Src:  repoFile,
			Dest: repoFileInChroot,
		},
		safechroot.FileToCopy{
			Src:  srpmFile,
			Dest: srpmFileInChroot,
		},
	}

	if rpmmacrosFile != "" {
		rpmmacrosCopy := safechroot.FileToCopy{
			Src:  rpmmacrosFile,
			Dest: rpmmacrosDest,
		}
		filesToCopy = append(filesToCopy, rpmmacrosCopy)
	}

	if runCheck {
		logger.Log.Debug("Enabling network access because we're running package tests.")

		resolvFileCopy := safechroot.FileToCopy{
			Src:  resolvFilePath,
			Dest: resolvFilePath,
		}
		filesToCopy = append(filesToCopy, resolvFileCopy)
	}

	err = chroot.AddFiles(filesToCopy...)
	return
}
