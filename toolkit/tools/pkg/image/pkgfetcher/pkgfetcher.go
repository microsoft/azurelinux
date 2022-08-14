package pkgfetcher

import (
	"errors"
	"strings"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/packagerepo/repocloner"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/packagerepo/repocloner/rpmrepocloner"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/packagerepo/repoutils"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/pkggraph"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/pkgjson"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/imagegen/configuration"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/imagegen/installutils"
)

func FetchPkgsAndCreateRepo(cfg *Config) error {
	if cfg.ExternalOnly && strings.TrimSpace(cfg.InputGraph) == "" {
		logger.Log.Info("input-graph must be provided if external-only is set.")
		return errors.New("input-graph must be provided")
	}

	cloner := rpmrepocloner.New()
	err := cloner.Initialize(cfg.OutDir, cfg.TmpDir, cfg.WorkerTar, cfg.ExistingRpmDir, cfg.UsePreviewRepo, cfg.RepoFiles)
	if err != nil {
		logger.Log.Infof("Failed to initialize RPM repo cloner. Error: %s", err)
		return err
	}
	defer cloner.Close()

	if !cfg.DisableUpstreamRepos {
		tlsKey, tlsCert := strings.TrimSpace(cfg.TlsClientKey), strings.TrimSpace(cfg.TlsClientCert)
		err = cloner.AddNetworkFiles(tlsCert, tlsKey)
		if err != nil {
			logger.Log.Infof("Failed to customize RPM repo cloner. Error: %s", err)
			return err
		}
	}

	if strings.TrimSpace(cfg.InputSummaryFile) != "" {
		// If an input summary file was provided, simply restore the cache using the file.
		err = repoutils.RestoreClonedRepoContents(cloner, cfg.InputSummaryFile)
	} else {
		err = cloneSystemConfigs(cloner, cfg.ConfigFile, cfg.BaseDirPath, cfg.ExternalOnly, cfg.InputGraph)
	}

	if err != nil {
		logger.Log.Infof("Failed to clone RPM repo. Error: %s", err)
		return err
	}

	logger.Log.Info("Configuring downloaded RPMs as a local repository")
	err = cloner.ConvertDownloadedPackagesIntoRepo()
	if err != nil {
		logger.Log.Infof("Failed to convert downloaded RPMs into a repo. Error: %s", err)
		return err
	}

	if strings.TrimSpace(cfg.OutputSummaryFile) != "" {
		err = repoutils.SaveClonedRepoContents(cloner, cfg.OutputSummaryFile)
		if err != nil {
			return err
		}
	}

	return nil
}

func cloneSystemConfigs(cloner repocloner.RepoCloner, configFile, baseDirPath string, externalOnly bool, inputGraph string) (err error) {
	const cloneDeps = true

	cfg, err := configuration.LoadWithAbsolutePaths(configFile, baseDirPath)
	if err != nil {
		return
	}

	packageVersionsInConfig, err := installutils.PackageNamesFromConfig(cfg)
	if err != nil {
		return
	}

	// Add kernel packages from KernelOptions
	packageVersionsInConfig = append(packageVersionsInConfig, installutils.KernelPackages(cfg)...)

	if externalOnly {
		packageVersionsInConfig, err = filterExternalPackagesOnly(packageVersionsInConfig, inputGraph)
		if err != nil {
			return
		}
	}

	// Add any packages required by the install tools
	packageVersionsInConfig = append(packageVersionsInConfig, installutils.GetRequiredPackagesForInstall()...)

	logger.Log.Infof("Cloning: %v", packageVersionsInConfig)
	// The image tools don't care if a package was created locally or not, just that it exists. Disregard if it is prebuilt or not.
	_, err = cloner.Clone(cloneDeps, packageVersionsInConfig...)
	return
}

// filterExternalPackagesOnly returns the subset of packageVersionsInConfig that only contains external packages.
func filterExternalPackagesOnly(packageVersionsInConfig []*pkgjson.PackageVer, inputGraph string) (filteredPackages []*pkgjson.PackageVer, err error) {
	dependencyGraph := pkggraph.NewPkgGraph()
	err = pkggraph.ReadDOTGraphFile(dependencyGraph, inputGraph)
	if err != nil {
		return
	}

	for _, pkgVer := range packageVersionsInConfig {
		pkgNode, _ := dependencyGraph.FindBestPkgNode(pkgVer)

		// There are two ways an external package will be represented by pkgNode.
		// 1) pkgNode may be nil. This is possible if the package is never consumed during the build phase,
		//    which means it will not be in the graph.
		// 2) pkgNode will be of 'StateUnresolved'. This will be the case if a local package has it listed as
		//    a Requires or BuildRequires.
		if pkgNode == nil || pkgNode.RunNode.State == pkggraph.StateUnresolved {
			filteredPackages = append(filteredPackages, pkgVer)
		}
	}

	return
}
