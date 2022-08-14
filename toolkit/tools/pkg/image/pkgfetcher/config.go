package pkgfetcher

type Config struct {
	ConfigFile           string
	OutDir               string
	BaseDirPath          string
	ExistingRpmDir       string
	TmpDir               string
	WorkerTar            string
	RepoFiles            []string
	UsePreviewRepo       bool
	DisableUpstreamRepos bool
	TlsClientCert        string
	TlsClientKey         string
	ExternalOnly         bool
	InputGraph           string
	InputSummaryFile     string
	OutputSummaryFile    string
}
