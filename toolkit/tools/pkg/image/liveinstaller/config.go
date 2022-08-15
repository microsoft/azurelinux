package liveinstaller

type Config struct {
	ConfigFile         string
	TemplateConfigFile string
	ForceAttended      bool
	ImagerTool         string
	BuildDir           string
	BaseDirPath        string
	ImagerLogFile      string
}
