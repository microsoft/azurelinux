package specreader

type Config struct {
	SpecsDir  string
	Output    string
	Workers   int
	BuildDir  string
	SrpmsDir  string
	RpmsDir   string
	DistTag   string
	WorkerTar string
	RunCheck  bool
}
