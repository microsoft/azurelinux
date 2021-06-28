package mic

import (
	corev1 "k8s.io/api/core/v1"
	informerv1 "k8s.io/client-go/informers/core/v1"
	"k8s.io/client-go/tools/cache"
)

// NodeClient handles fetching node details from kubernetes
type NodeClient struct {
	informer informerv1.NodeInformer
}

// Get gets the specified kubernetes node.
//
// Note that this is using a local, eventually consistent cache which may not
// be up to date with the actual state of the cluster.
func (c *NodeClient) Get(name string) (*corev1.Node, error) {
	return c.informer.Lister().Get(name)
}

// Start starts syncing the underlying cache with kubernetes.
//
// The passed in channel should be used to signal that the client should stop
// syncing. Close this channel when you want syncing to stop.
func (c *NodeClient) Start(exit <-chan struct{}) {
	go c.informer.Informer().Run(exit)
	cache.WaitForCacheSync(exit, c.informer.Informer().HasSynced)
}
