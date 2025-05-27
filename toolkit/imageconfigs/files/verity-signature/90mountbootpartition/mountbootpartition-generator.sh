#!/bin/sh

set -x
set -e

echo "Running mountbootpartition-generator.sh" > /dev/kmsg

# type getarg > /dev/null 2>&1 || . /lib/dracut-lib.sh

function updateVeritySetupUnit () {
    systemdDropInDir=/etc/systemd/system
    verityDropInDir=$systemdDropInDir/systemd-veritysetup@root.service.d

    mkdir -p $verityDropInDir
    verityConfiguration=$verityDropInDir/verity-azl-extension.conf

    cat <<EOF > $verityConfiguration
[Unit]
After=bootmountmonitor.service
Requires=bootmountmonitor.service
EOF

    chmod 644 $verityConfiguration
    chown root:root $verityConfiguration
}

# -----------------------------------------------------------------------------
function createBootPartitionMonitorScript () {
    local bootPartitionMonitorCmd=$1
    local semaphorefile=$2

    cat <<EOF > $bootPartitionMonitorCmd
#!/bin/sh
while [ ! -e "$semaphorefile" ]; do
    echo "Waiting for $semaphorefile to exist..."
    sleep 1
done    
EOF
    chmod +x $bootPartitionMonitorCmd
}

# -----------------------------------------------------------------------------
function createBootPartitionMonitorUnit() {
    local bootPartitionMonitorCmd=$1

    bootMountMonitorName="bootmountmonitor.service"
    systemdDropInDir=/etc/systemd/system
    bootMountMonitorDir=$systemdDropInDir
    bootMountMonitorUnitFile=$bootMountMonitorDir/$bootMountMonitorName

    cat <<EOF > $bootMountMonitorUnitFile
[Unit]
Description=bootpartitionmounter
DefaultDependencies=no

[Service]
Type=oneshot
ExecStart=$bootPartitionMonitorCmd
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
EOF
}

# -----------------------------------------------------------------------------

updateVeritySetupUnit

systemdScriptsDir=/usr/local/bin
bootPartitionMonitorCmd=$systemdScriptsDir/boot-partition-monitor.sh
semaphorefile=/run/boot-parition-mount-complete.sem

mkdir -p $systemdScriptsDir

# ToDo: we should generate this boot mounting logic only when it is needed -
#       i.e. by reading kernel command line parameters.
createBootPartitionMonitorScript $bootPartitionMonitorCmd $semaphorefile
createBootPartitionMonitorUnit $bootPartitionMonitorCmd

echo "mountbootpartition-generator.sh completed successfully." > /dev/kmsg
