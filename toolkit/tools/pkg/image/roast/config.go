package roast

type Config struct {
	InputDir       string
	OutputDir      string
	ConfigFile     string
	TmpDir         string
	ReleaseVersion string
	Workers        int
	ImageTag       string
}
