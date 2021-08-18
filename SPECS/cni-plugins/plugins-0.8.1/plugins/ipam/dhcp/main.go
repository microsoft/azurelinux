// Copyright 2015 CNI authors
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"log"
	"net/rpc"
	"os"
	"path/filepath"

	"github.com/containernetworking/cni/pkg/skel"
	"github.com/containernetworking/cni/pkg/types"
	"github.com/containernetworking/cni/pkg/types/current"
	"github.com/containernetworking/cni/pkg/version"
	bv "github.com/containernetworking/plugins/pkg/utils/buildversion"
)

const defaultSocketPath = "/run/cni/dhcp.sock"

func main() {
	if len(os.Args) > 1 && os.Args[1] == "daemon" {
		var pidfilePath string
		var hostPrefix string
		var socketPath string
		daemonFlags := flag.NewFlagSet("daemon", flag.ExitOnError)
		daemonFlags.StringVar(&pidfilePath, "pidfile", "", "optional path to write daemon PID to")
		daemonFlags.StringVar(&hostPrefix, "hostprefix", "", "optional prefix to host root")
		daemonFlags.StringVar(&socketPath, "socketpath", "", "optional dhcp server socketpath")
		daemonFlags.Parse(os.Args[2:])

		if socketPath == "" {
			socketPath = defaultSocketPath
		}

		if err := runDaemon(pidfilePath, hostPrefix, socketPath); err != nil {
			log.Printf(err.Error())
			os.Exit(1)
		}
	} else {
		skel.PluginMain(cmdAdd, cmdCheck, cmdDel, version.All, bv.BuildString("dhcp"))
	}
}

func cmdAdd(args *skel.CmdArgs) error {
	// Plugin must return result in same version as specified in netconf
	versionDecoder := &version.ConfigDecoder{}
	confVersion, err := versionDecoder.Decode(args.StdinData)
	if err != nil {
		return err
	}

	result := &current.Result{}
	if err := rpcCall("DHCP.Allocate", args, result); err != nil {
		return err
	}

	return types.PrintResult(result, confVersion)
}

func cmdDel(args *skel.CmdArgs) error {
	result := struct{}{}
	if err := rpcCall("DHCP.Release", args, &result); err != nil {
		return err
	}
	return nil
}

func cmdCheck(args *skel.CmdArgs) error {
	// TODO: implement
	//return fmt.Errorf("not implemented")
	// Plugin must return result in same version as specified in netconf
	versionDecoder := &version.ConfigDecoder{}
	//confVersion, err := versionDecoder.Decode(args.StdinData)
	_, err := versionDecoder.Decode(args.StdinData)
	if err != nil {
		return err
	}

	result := &current.Result{}
	if err := rpcCall("DHCP.Allocate", args, result); err != nil {
		return err
	}

	return nil
}

type SocketPathConf struct {
	DaemonSocketPath string `json:"daemonSocketPath,omitempty"`
}

type TempNetConf struct {
	IPAM SocketPathConf `json:"ipam,omitempty"`
}

func getSocketPath(stdinData []byte) (string, error) {
	conf := TempNetConf{}
	if err := json.Unmarshal(stdinData, &conf); err != nil {
		return "", fmt.Errorf("error parsing socket path conf: %v", err)
	}
	if conf.IPAM.DaemonSocketPath == "" {
		return defaultSocketPath, nil
	}
	return conf.IPAM.DaemonSocketPath, nil
}

func rpcCall(method string, args *skel.CmdArgs, result interface{}) error {
	socketPath, err := getSocketPath(args.StdinData)
	if err != nil {
		return fmt.Errorf("error obtaining socketPath: %v", err)
	}

	client, err := rpc.DialHTTP("unix", socketPath)
	if err != nil {
		return fmt.Errorf("error dialing DHCP daemon: %v", err)
	}

	// The daemon may be running under a different working dir
	// so make sure the netns path is absolute.
	netns, err := filepath.Abs(args.Netns)
	if err != nil {
		return fmt.Errorf("failed to make %q an absolute path: %v", args.Netns, err)
	}
	args.Netns = netns

	err = client.Call(method, args, result)
	if err != nil {
		return fmt.Errorf("error calling %v: %v", method, err)
	}

	return nil
}
