package profile

import (
	"fmt"
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
			return nil, fmt.Errorf("Unable to create cpu-pprof file: %s", err)
		}
		pprof.StartCPUProfile(cpf)
		// Assign the file pointer after starting the profile operation
		p.cpuProfFile = cpf
	}

	if enableMemProf {
		mpf, err := os.Create(cpuProfFile)
		if err != nil {
			return nil, fmt.Errorf("Unable to create mem-pprof file: %s", err)
		}
		runtime.GC() // get up-to-date statistics
		if err := pprof.WriteHeapProfile(mpf); err != nil {
			return nil, fmt.Errorf("Unable to write mem-pprof file: %s", err)
		}
		// Assign the file pointer after starting the profile operation
		p.memProfFile = mpf
	}

	if enableTrace {
		tf, err := os.Create(traceFile)
		if err != nil {
			return nil, fmt.Errorf("Unable to create trace file: %s", err)
		}
		if err := trace.Start(tf); err != nil {
			return nil, fmt.Errorf("Unable to write trace file: %s", err)
		}
		// Assign the file pointer after starting the trace
		p.traceFile = tf
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
