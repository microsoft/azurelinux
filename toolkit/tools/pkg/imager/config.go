package imager

type Config struct {
	BuildDir        string
	ConfigFile      string
	LocalRepo       string
	TdnfTar         string
	RepoFile        string
	Assets          string
	BaseDirPath     string
	OutputDir       string
	LiveInstallFlag bool
	EmitProgress    bool
	SystemConfig    int
}
