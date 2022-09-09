// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package main

import (
	"crypto/tls"
	"crypto/x509"
	"io/ioutil"
	"os"
	"path/filepath"
	"runtime"
	"strings"
	"time"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/buildpipeline"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/directory"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/exe"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/network"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/retry"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/rpm"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/safechroot"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/srpm"

	"gopkg.in/alecthomas/kingpin.v2"
)

const (
	defaultBuildDir    = "./build/SRPMS"
	defaultWorkerCount = "10"
)

type sourceRetrievalConfiguration struct {
	sourceURLs []string
	caCerts    *x509.CertPool
	tlsCerts   []tls.Certificate
}

var (
	app = kingpin.New("srpmpacker", "A tool to package a SRPM.")

	specsDir = exe.InputDirFlag(app, "Path to the SPEC directory to create SRPMs from.")
	outDir   = exe.OutputDirFlag(app, "Directory to place the output SRPM.")
	logFile  = exe.LogFileFlag(app)
	logLevel = exe.LogLevelFlag(app)

	buildDir = app.Flag("build-dir", "Directory to store temporary files while building.").Default(defaultBuildDir).String()
	distTag  = app.Flag("dist-tag", "The distribution tag SRPMs will be built with.").Required().String()
	runCheck = app.Flag("run-check", "Whether or not to run the spec file's check section during package build.").Bool()

	workers = app.Flag("workers", "Number of concurrent goroutines to parse with.").Default(defaultWorkerCount).Int()

	// Use String() and not ExistingFile() as the Makefile may pass an empty string if the user did not specify any of these options
	srpmUrlList   = app.Flag("srpm-url-list", "urls for SRPM repo.").String()
	srpmListFile  = app.Flag("srpm-list", "Path to a list of SPECs to pack. If empty will pack all SPECs.").ExistingFile()
	caCertFile    = app.Flag("ca-cert", "Root certificate authority to use when downloading files.").String()
	tlsClientCert = app.Flag("tls-cert", "TLS client certificate to use when downloading files.").String()
	tlsClientKey  = app.Flag("tls-key", "TLS client key to use when downloading files.").String()

	workerTar = app.Flag("worker-tar", "Full path to worker_chroot.tar.gz. If this argument is empty, SRPMs will be packed in the host environment.").ExistingFile()
)

func main() {
	app.Version(exe.ToolkitVersion)
	kingpin.MustParse(app.Parse(os.Args[1:]))
	logger.InitBestEffort(*logFile, *logLevel)

	if *workers <= 0 {
		logger.Log.Fatalf("Value in --workers must be greater than zero. Found %d", *workers)
	}

	// Create a template configuration that all packed SRPM will be based on.
	var templateSrcConfig sourceRetrievalConfiguration
	// Setup remote source configuration
	var err error
	templateSrcConfig.caCerts, err = x509.SystemCertPool()
	logger.PanicOnError(err, "Received error calling x509.SystemCertPool(). Error: %v", err)
	if *caCertFile != "" {
		newCACert, err := ioutil.ReadFile(*caCertFile)
		if err != nil {
			logger.Log.Panicf("Invalid CA certificate (%s), error: %s", *caCertFile, err)
		}

		templateSrcConfig.caCerts.AppendCertsFromPEM(newCACert)
	}

	if *tlsClientCert != "" && *tlsClientKey != "" {
		cert, err := tls.LoadX509KeyPair(*tlsClientCert, *tlsClientKey)
		if err != nil {
			logger.Log.Panicf("Invalid TLS client key pair (%s) (%s), error: %s", *tlsClientCert, *tlsClientKey, err)
		}

		templateSrcConfig.tlsCerts = append(templateSrcConfig.tlsCerts, cert)

	}
	if *srpmUrlList != "" {
		// Assumes that srpmUrlList come in as ',' seperated
		urls := strings.Split(*srpmUrlList, " ")
		templateSrcConfig.sourceURLs = urls
	}

	// A pack list may be provided, if so only pack this subset.
	// If none is provided, pack all srpms.
	srpmList, err := srpm.ParsePackListFile(*srpmListFile)
	logger.PanicOnError(err)

	logger.Log.Infof("SRPM list %s", srpmList)

	err = getSRPMQueryWrapper(*specsDir, *distTag, *buildDir, *outDir, *workerTar, *workers, *runCheck, srpmList, templateSrcConfig)
	logger.PanicOnError(err)

}

// getSRPMQueryWrapper wraps getSRPMQuery to conditionally run it inside a chroot.
// If workerTar is non-empty, packing will occur inside a chroot, otherwise it will run on the host system.
func getSRPMQueryWrapper(specsDir, distTag, buildDir, outDir, workerTar string, workers int, runCheck bool, srpmList []string, templateSrcConfig sourceRetrievalConfiguration) (err error) {
	var chroot *safechroot.Chroot
	originalOutDir := outDir
	if workerTar != "" {
		const leaveFilesOnDisk = false
		chroot, buildDir, outDir, specsDir, err = srpm.CreateChroot(workerTar, buildDir, outDir, specsDir)
		if err != nil {
			return
		}
		defer chroot.Close(leaveFilesOnDisk)
	}

	doCreateAll := func() error {
		err = getSRPMQuery(specsDir, distTag, buildDir, outDir, workers, runCheck, srpmList, templateSrcConfig)
		return err
	}

	if chroot != nil {
		logger.Log.Info("Grabbing SRPMs URL inside a chroot environment")
		err = chroot.Run(doCreateAll)
	} else {
		logger.Log.Info("Grabbing SRPMs URL SRPMs in the host environment")
		err = doCreateAll()
	}

	if err != nil {
		return err
	}

	// If this is container build then the bind mounts will not have been created.
	// Copy the chroot output to host output folder.
	if !buildpipeline.IsRegularBuild() {
		srpmsInChroot := filepath.Join(chroot.RootDir(), outDir)
		err = directory.CopyContents(srpmsInChroot, originalOutDir)
		if err != nil {
			return err
		}
	}

	return
}

// getSRPMQuery queries for the name, version and release of the SRPM
func getSRPMQuery(specsDir, distTag, buildDir, outDir string, workers int, runCheck bool, srpmList []string, srcConfig sourceRetrievalConfiguration) (err error) {
	const (
		emptyQueryFormat = ``
		querySrpm        = `%{NAME}-%{VERSION}-%{RELEASE}.src.rpm`
	)
	// Find the general SPEC query arguments
	defines := rpm.DefaultDefines(runCheck)
	defines[rpm.DistTagDefine] = distTag
	arch, err := rpm.GetRpmArch(runtime.GOARCH)
	if err != nil {
		logger.Log.Warn(err)
		return
	}
	specFiles, err := srpm.FindSPECFiles(specsDir, srpmList)
	if err != nil {
		return
	}

	// Parse each SPEC for name and version and hydrate SRPM
	for _, specfile := range specFiles {
		sourcedir := filepath.Dir(specfile)
		logger.Log.Infof("specfile for %s", specfile)
		var packageSRPMs []string
		packageSRPMs, err = rpm.QuerySPEC(specfile, sourcedir, querySrpm, arch, defines, rpm.QueryHeaderArgument)
		if err != nil {
			logger.Log.Warn(err)
			return err
		}
		packageSRPM := packageSRPMs[0]
		downloadSRPM(packageSRPM, outDir, srcConfig)
	}
	return err
}

// downloadSRPM downloads SRPM trying each of srcConfig's urls
func downloadSRPM(fileName string, newSourceDir string, srcConfig sourceRetrievalConfiguration) {
	const (
		downloadRetryAttempts = 3
		downloadRetryDuration = time.Second
	)
	destinationFile := filepath.Join(newSourceDir, fileName)

	var err error
	var urlChosen string
	srpmDownloaded := false
	for _, urlSrc := range srcConfig.sourceURLs {
		if srpmDownloaded {
			break
		}
		logger.Log.Debugf("Trying (%s) from (%s)", fileName, urlSrc)
		url := network.JoinURL(urlSrc, fileName)

		err = retry.Run(func() error {
			err := network.DownloadFile(url, destinationFile, srcConfig.caCerts, srcConfig.tlsCerts)
			urlChosen = url
			if err != nil {
				logger.Log.Warnf("Failed to download (%s). Error: %s", url, err)
				os.Remove(destinationFile)
			} else {
				srpmDownloaded = true
			}

			return err
		}, downloadRetryAttempts, downloadRetryDuration)
	}

	if !srpmDownloaded {
		logger.Log.Panicf("All attempts failed to download (%s). Error: %s", fileName, err)
		return
	}

	logger.Log.Debugf("Hydrated (%s) from (%s)", fileName, urlChosen)

}
