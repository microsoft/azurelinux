package pkgfetcher

type Config struct {
	InputGraph           string
	OutputGraph          string
	OutDir               string
	ExistingRpmDir       string
	TmpDir               string
	WorkerTar            string
	RepoFiles            []string
	UsePreviewRepo       bool
	DisableUpstreamRepos bool
	ToolchainManifest    string
	TlsClientCert        string
	TlsClientKey         string
	StopOnFailure        bool
	InputSummaryFile     string
	OutputSummaryFile    string
}
