package probes

import (
	"net/http"

	"k8s.io/klog/v2"
)

// InitHealthProbe - sets up a health probe which responds with success (200 - OK) once its initialized.
// The contents of the healthz endpoint will be the string "Active" if the condition is satisfied.
// The condition is set to true when the sync cycle has become active in case of MIC and the iptables
// rules set in case of NMI.
func InitHealthProbe(condition *bool) {
	http.HandleFunc("/healthz", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(200)
		if *condition {
			_, _ = w.Write([]byte("Active"))
		} else {
			_, _ = w.Write([]byte("Not Active"))
		}
	})
}

func startAsync(port string) {
	err := http.ListenAndServe(":"+port, nil)
	if err != nil {
		klog.Fatalf("http listen and serve error: %+v", err)
	}

	klog.Info("http listen and serve started !")
}

// Start starts the required http server to start the probe to respond.
func Start(port string) {
	go startAsync(port)
}

// InitAndStart initializes the default probes and starts the http listening port.
func InitAndStart(port string, condition *bool) {
	InitHealthProbe(condition)
	klog.Infof("initialized health probe on port %s", port)
	// start the probe.
	Start(port)
	klog.Info("started health probe")
}
