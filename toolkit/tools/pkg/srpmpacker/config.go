package srpmpacker

type Config struct {
	SpecsDir             string
	OutDir               string
	BuildDir             string
	DistTag              string
	PackListFile         string
	RunCheck             bool
	Workers              int
	RepackAll            bool
	NestedSourcesDir     bool
	SourceURL            string
	CaCertFile           string
	TlsClientCert        string
	TlsClientKey         string
	WorkerTar            string
	ValidSignatureLevels []string
	SignatureHandling    string
}
