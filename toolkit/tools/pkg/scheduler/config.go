package scheduler

type Config struct {
	InputGraphFile       string
	OutputGraphFile      string
	OutputCSVFile        string
	WorkDir              string
	WorkerTar            string
	RepoFile             string
	RpmDir               string
	SrpmDir              string
	CacheDir             string
	BuildLogsDir         string
	ImageConfig          string
	BaseDirPath          string
	DistTag              string
	DistroReleaseVersion string
	DistroBuildNumber    string
	RpmmacrosFile        string
	BuildAttempts        int
	RunCheck             bool
	NoCleanup            bool
	NoCache              bool
	StopOnFailure        bool
	ReservedFileListFile string
	DeltaBuild           bool
	ValidBuildAgentFlags []string
	BuildAgent           string
	BuildAgentProgram    string
	Workers              int
	IgnoredPackages      string
	PkgsToBuild          string
	PkgsToRebuild        string
	LogFile              string
	LogLevel             string
}
