package validatechroot

type Config struct {
	ToolchainRpmsDir       string
	TmpDir                 string
	WorkerTar              string
	WorkerManifest         string
	LeaveChrootFilesOnDisk bool
}
