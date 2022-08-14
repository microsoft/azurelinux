package pkgworker

type Config struct {
	SrpmFile             string
	WorkDir              string
	WorkerTar            string
	RepoFile             string
	RpmsDirPath          string
	SrpmsDirPath         string
	CacheDir             string
	NoCleanup            bool
	DistTag              string
	DistroReleaseVersion string
	DistroBuildNumber    string
	RpmmacrosFile        string
	RunCheck             bool
	PackagesToInstall    []string
}
