#!/bin/bash

set -x
set -e

dracutSourceDir=~/git/CBL-Mariner/toolkit/mic-iso-gen/dracut-patches
dracutBuildMachineIP=10.137.194.51
dracutBuildMachineUser=afo123

# dracut artifacts
scp $dracutSourceDir/artifacts/dmsquash-generator.sh $dracutBuildMachineUser@$dracutBuildMachineIP:~/
scp $dracutSourceDir/artifacts/dmsquash-live-root.sh $dracutBuildMachineUser@$dracutBuildMachineIP:~/
scp $dracutSourceDir/artifacts/dracut-emergency.sh $dracutBuildMachineUser@$dracutBuildMachineIP:~/
scp $dracutSourceDir/artifacts/dracut-mount.sh $dracutBuildMachineUser@$dracutBuildMachineIP:~/
scp $dracutSourceDir/artifacts/iso-scan.sh $dracutBuildMachineUser@$dracutBuildMachineIP:~/
scp $dracutSourceDir/artifacts/20-gmileka.conf $dracutBuildMachineUser@$dracutBuildMachineIP:~/

# re-building script
scp $dracutSourceDir/rebuild-initrd.sh $dracutBuildMachineUser@$dracutBuildMachineIP:~/