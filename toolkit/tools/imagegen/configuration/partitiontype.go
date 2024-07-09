// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package configuration

// Common partition types: https://wiki.archlinux.org/title/GPT_fdisk#Partition_type
// More type UUIDs can be found here: https://uapi-group.org/specifications/specs/discoverable_partitions_specification/
var PartitionTypeNameToUUID = map[string]string{
	"linux":            "0fc63daf-8483-4772-8e79-3d69d8477de4",
	"esp":              "c12a7328-f81f-11d2-ba4b-00a0c93ec93b",
	"xbootldr":         "bc13c2ff-59e6-4262-a352-b275fd6f7172",
	"linux-root-amd64": "4f68bce3-e8cd-4db1-96e7-fbcaf984b709",
	"linux-swap":       "0657fd6d-a4ab-43c4-84e5-0933c84b4f4f",
	"linux-home":       "933ac7e1-2eb4-4f13-b844-0e14e2aef915",
	"linux-srv":        "3b8f8425-20e0-4f3b-907f-1a25a76f98e8",
	"linux-var":        "4d21b016-b534-45c2-a9fb-5c16e091fd2d",
	"linux-tmp":        "7ec6f557-3bc5-4aca-b293-16ef5df639d1",
	"linux-lvm":        "e6d6d379-f507-44c2-a23c-238f2a3df928",
	"linux-raid":       "a19d880f-05fc-4d3b-a006-743f0f84911e",
	"linux-luks":       "ca7d7ccb-63ed-4c53-861c-1742536059cc",
	"linux-dm-crypt":   "7ffec5c9-2d00-49b7-8941-3ea10a5586b7",
}
