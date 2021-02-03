Supported k8s versions match versions AKS (Azure Kubernetes Service) currently supports.
Run 'az aks get-versions ...' command to know them.
(see https://docs.microsoft.com/en-us/azure/aks/supported-kubernetes-versions)

etcd and coredns versions are the ones that k8s requires:
-> from cmd/kubeadm/app/constants/constants.go (look for DefaultEtcdVersion and CoreDNSVersion)

k8s version | etcd version | coredns version
1.17.13     | 3.4.3        | 1.6.5
1.17.16     | 3.4.3        | 1.6.5
1.18.10     | 3.4.3        | 1.6.7
1.18.14     | 3.4.3        | 1.6.7
1.19.3      | 3.4.13       | 1.7.0
1.19.6      | 3.4.13       | 1.7.0