package mic

import (
	"path"

	"github.com/Azure/aad-pod-identity/pkg/cloudprovider"

	"github.com/Azure/go-autorest/autorest/azure"
	corev1 "k8s.io/api/core/v1"
	"k8s.io/apimachinery/pkg/api/errors"
)

type vmssGroup struct {
	nodes map[string]bool // index of node refs assigned to this vmss group
}

type vmssGroupList struct {
	groups  map[string]*vmssGroup
	nodeIdx map[string]*vmssGroup // index node refs for matching to a vmss group
}

func (ls *vmssGroupList) addNode(vmss, node string) {
	g := ls.groups[vmss]
	if g == nil {
		g = &vmssGroup{nodes: make(map[string]bool)}
		ls.groups[vmss] = g
	}
	g.nodes[node] = true
	ls.nodeIdx[node] = g
}

// getByNode takes a node reference and returns the vmss group it belongs to
func (ls *vmssGroupList) getByNode(ref string) *vmssGroup {
	return ls.nodeIdx[ref]
}

// get takes a vmss id and returns the corresponding vmss group
func (ls *vmssGroupList) get(id string) *vmssGroup {
	return ls.groups[id]
}

func (g *vmssGroup) hasNode(ref string) bool {
	if g.nodes == nil {
		return false
	}
	return g.nodes[ref]
}

func vmssFromNodeRef(nc NodeGetter, ref string) (string, bool, error) {
	n, err := nc.Get(ref)
	if err != nil {
		if !errors.IsNotFound(err) {
			return "", false, err
		}
		return "", false, nil
	}

	return isVMSS(n)
}

// getVMSSGroups takes a list of node references and groups them by vmss ID
// nodes not in a vmss are elided
func getVMSSGroups(nc NodeGetter, refs map[string]bool) (*vmssGroupList, error) {
	ls := &vmssGroupList{groups: make(map[string]*vmssGroup), nodeIdx: make(map[string]*vmssGroup)}
	for ref := range refs {
		id, ok, err := vmssFromNodeRef(nc, ref)
		if err != nil {
			if !errors.IsNotFound(err) {
				return nil, err
			}
			continue
		}

		if !ok {
			continue
		}

		ls.addNode(id, ref)
	}

	return ls, nil
}

func isVMSS(n *corev1.Node) (string, bool, error) {
	r, err := cloudprovider.ParseResourceID(n.Spec.ProviderID)
	if err != nil && n.Spec.ProviderID != "" {
		return "", false, err
	}

	if r.ResourceType != cloudprovider.VMSSResourceType {
		return "", false, nil
	}
	return makeVMSSID(r), true, nil
}

func makeVMSSID(r azure.Resource) string {
	return path.Join(r.SubscriptionID, r.ResourceGroup, r.ResourceName)
}

func getVMSSName(vmssID string) string {
	_, resourceName := path.Split(vmssID)
	return resourceName
}

// Either get a vmss group by node reference or lookup the vmss ID from the node's provider ID.
// The reason for this is we may have request to delete an identity from a node and it is the last identity, so
// the node will not be referenced by any pods and will be absent from the group list
//
// This does end up caching any missing node references into the vmss group list.
func getVMSSGroupFromPossiblyUnreferencedNode(nc NodeGetter, groups *vmssGroupList, ref string) (*vmssGroup, error) {
	vmss := groups.getByNode(ref)
	if vmss != nil {
		return vmss, nil
	}

	vmssID, isVMSS, err := vmssFromNodeRef(nc, ref)
	if err != nil && !errors.IsNotFound(err) {
		return nil, err
	}
	if isVMSS {
		groups.addNode(vmssID, ref) // cache this reference so we don't have to parse again
		return groups.get(vmssID), nil
	}

	// not a vmss
	return nil, nil
}
