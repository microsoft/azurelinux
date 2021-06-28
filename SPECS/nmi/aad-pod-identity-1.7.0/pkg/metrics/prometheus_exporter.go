package metrics

import (
	"fmt"
	"net/http"

	"contrib.go.opencensus.io/exporter/prometheus"
	"k8s.io/klog/v2"
)

// newPrometheusExporter creates prometheus exporter and run the same on given port
func newPrometheusExporter(namespace string, portNumber string) (*prometheus.Exporter, error) {

	prometheusExporter, err := prometheus.NewExporter(prometheus.Options{
		Namespace: namespace,
	})

	if err != nil {
		return nil, fmt.Errorf("failed to create the Prometheus exporter, error: %+v", err)
	}
	klog.Info("starting Prometheus exporter")
	// Run the Prometheus exporter as a scrape endpoint.
	go func() {
		mux := http.NewServeMux()
		mux.Handle("/metrics", prometheusExporter)
		address := fmt.Sprintf(":%v", portNumber)
		if err := http.ListenAndServe(address, mux); err != nil {
			klog.Errorf("failed to run Prometheus scrape endpoint, error: %+v", err)
		}
	}()
	return prometheusExporter, nil
}
