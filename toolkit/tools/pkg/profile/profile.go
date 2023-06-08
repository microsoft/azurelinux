package profile

import (
	"os"
	"runtime"
	"runtime/pprof"
	"runtime/trace"
)

type Profiler struct {
	cpuProfFile *os.File
	memProfFile *os.File
	traceFile   *os.File
}

func StartProfiling(cpuProfFile, memProfFile, traceFile string, enableCpuProf, enableMemProf, enableTrace bool) (*Profiler, error) {
	p := &Profiler{
		cpuProfFile: nil,
		memProfFile: nil,
		traceFile:   nil,
	}

	if enableCpuProf {
		cpf, err := os.Create(cpuProfFile)
		if err != nil {
			return nil, err
		}
		p.cpuProfFile = cpf
		pprof.StartCPUProfile(cpf)
	}

	if enableMemProf {
		mpf, err := os.Create(cpuProfFile)
		if err != nil {
			return nil, err
		}
		p.memProfFile = mpf

		runtime.GC() // get up-to-date statistics
		if err := pprof.WriteHeapProfile(mpf); err != nil {
			return nil, err
		}
	}

	if enableTrace {
		tf, err := os.Create(traceFile)
		if err != nil {
			return nil, err
		}
		p.traceFile = tf

		if err := trace.Start(tf); err != nil {
			return nil, err
		}
	}

	return p, nil
}

func (p *Profiler) StopProfiler() {
	if p.cpuProfFile != nil {
		pprof.StopCPUProfile()
		p.cpuProfFile.Close()
	}

	if p.memProfFile != nil {
		p.memProfFile.Close()
	}

	if p.traceFile != nil {
		trace.Stop()
		p.traceFile.Close()
	}
}
