module github.com/Azure/aad-pod-identity

go 1.15

require (
	contrib.go.opencensus.io/exporter/prometheus v0.1.0
	github.com/Azure/azure-sdk-for-go v40.4.0+incompatible
	github.com/Azure/go-autorest/autorest v0.10.0
	github.com/Azure/go-autorest/autorest/adal v0.8.2
	github.com/Azure/go-autorest/autorest/azure/auth v0.1.0
	github.com/Azure/go-autorest/autorest/to v0.2.0 // indirect
	github.com/Azure/go-autorest/autorest/validation v0.1.0 // indirect
	github.com/coreos/go-iptables v0.3.0
	github.com/fsnotify/fsnotify v1.4.9
	github.com/google/go-cmp v0.4.0
	github.com/pkg/errors v0.9.1
	github.com/spf13/pflag v1.0.5
	github.com/stretchr/testify v1.4.0
	go.opencensus.io v0.22.2
	golang.org/x/crypto v0.0.0-20200622213623-75b288015ac9
	golang.org/x/sync v0.0.0-20190911185100-cd5d95a43a6e
	gopkg.in/yaml.v2 v2.2.8
	k8s.io/api v0.19.2
	k8s.io/apimachinery v0.19.2
	k8s.io/client-go v0.19.2
	k8s.io/component-base v0.19.2
	k8s.io/klog/v2 v2.3.0
)
