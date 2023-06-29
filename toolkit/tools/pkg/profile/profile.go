package profile

import (
	"fmt"
	"os"
	"runtime"
	"runtime/pprof"
	"runtime/trace"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/exe"
)

type Profiler struct {
	cpuProfFile *os.File
	memProfFile *os.File
	traceFile   *os.File
}

func StartProfiling(pf *exe.ProfileFlags) (*Profiler, error) {
	p := &Profiler{
		cpuProfFile: nil,
		memProfFile: nil,
		traceFile:   nil,
	}

	if *pf.EnableCpuProf {
		cpf, err := os.Create(*pf.CpuProfFile)
		if err != nil {
			return nil, fmt.Errorf("unable to create cpu-pprof file: %s", err)
		}
		err = pprof.StartCPUProfile(cpf)
		if err != nil {
			return nil, fmt.Errorf("unable to start cpu-pprof: %s", err)
		}
		// Assign the file pointer after starting the profile operation
		p.cpuProfFile = cpf
	}

	if *pf.EnableMemProf {
		mpf, err := os.Create(*pf.CpuProfFile)
		if err != nil {
			return nil, fmt.Errorf("unable to create mem-pprof file: %s", err)
		}
		runtime.GC() // get up-to-date statistics
		if err := pprof.WriteHeapProfile(mpf); err != nil {
			return nil, fmt.Errorf("unable to write mem-pprof file: %s", err)
		}
		// Assign the file pointer after starting the profile operation
		p.memProfFile = mpf
	}

	if *pf.EnableTrace {
		tf, err := os.Create(*pf.TraceFile)
		if err != nil {
			return nil, fmt.Errorf("unable to create trace file: %s", err)
		}
		if err := trace.Start(tf); err != nil {
			return nil, fmt.Errorf("unable to write trace file: %s", err)
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
