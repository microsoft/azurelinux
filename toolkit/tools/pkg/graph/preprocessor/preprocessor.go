package preprocessor

import (
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/graph/pkggraph"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/logger"
)

func (cfg *Config) ReadAndPreprocessGraph() (*pkggraph.PkgGraph, error) {
	scrubbedGraph := pkggraph.NewPkgGraph()

	err := pkggraph.ReadDOTGraphFile(scrubbedGraph, cfg.InputGraphFile)
	if err != nil {
		logger.Log.Infof("Failed to read graph to file, %s. Error: %s", cfg.InputGraphFile, err)
		return nil, err
	}
	if cfg.HydratedBuild {
		logger.Log.Debugf("Nodes before replacing prebuilt nodes: %d", len(scrubbedGraph.AllNodes()))
		err = replaceRunNodesWithPrebuiltNodes(scrubbedGraph)
		logger.Log.Debugf("Nodes after replacing prebuilt nodes: %d", len(scrubbedGraph.AllNodes()))
		if err != nil {
			logger.Log.Infof("Failed to replace run nodes with preBuilt nodes. Error: %s", err)
			return nil, err
		}
	}
	return scrubbedGraph, nil
}

func PreprocessGraph(g *pkggraph.PkgGraph) (*pkggraph.PkgGraph, error) {
	err := replaceRunNodesWithPrebuiltNodes(g)
	return g, err
}

func replaceRunNodesWithPrebuiltNodes(pkgGraph *pkggraph.PkgGraph) (err error) {
	for _, node := range pkgGraph.AllNodes() {

		if node.Type != pkggraph.TypeRun {
			continue
		}

		isPrebuilt, _, missing := pkggraph.IsSRPMPrebuilt(node.SrpmPath, pkgGraph, nil)

		if isPrebuilt == false {
			logger.Log.Tracef("Can't mark %s as prebuilt, missing: %v", node.SrpmPath, missing)
			continue
		}

		preBuiltNode := pkgGraph.CloneNode(node)
		preBuiltNode.State = pkggraph.StateUpToDate
		preBuiltNode.Type = pkggraph.TypePreBuilt

		parentNodes := pkgGraph.To(node.ID())
		for parentNodes.Next() {
			parentNode := parentNodes.Node().(*pkggraph.PkgNode)

			if parentNode.Type != pkggraph.TypeGoal {
				pkgGraph.RemoveEdge(parentNode.ID(), node.ID())

				logger.Log.Debugf("Adding a 'PreBuilt' node '%s' with id %d. For '%s'", preBuiltNode.FriendlyName(), preBuiltNode.ID(), parentNode.FriendlyName())
				err = pkgGraph.AddEdge(parentNode, preBuiltNode)

				if err != nil {
					logger.Log.Errorf("Adding edge failed for %v -> %v", parentNode, preBuiltNode)
					return err
				}
			}
		}
	}

	return nil
}
