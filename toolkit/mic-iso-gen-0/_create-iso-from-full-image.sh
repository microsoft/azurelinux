#!/bin/bash

set -x
set -e

scriptDir=$(dirname "$BASH_SOURCE")

buildDir=$1
buildRootfs=$2

if [[ -z $buildDir ]]; then
    echo "Specify output build directory."
    exit 1
fi

#------------------------------------------------------------------------------
function mic_poc_log() {
    set +x
    echo $1
    set -x
}

#------------------------------------------------------------------------------
function create_full_image() {
    mic_poc_log "---------------- create_full_image [enter] --------"
    local configFile=$1
    local outputDiskRawFile=$2
    local outputRootfsRawFile=$3
    local outputRootfsRawGzFile=$4

    # outputs:
    #
    #  full disk:
    #   ./out/images/disk0.raw
    #   ./build/imagegen/disk0.raw
    #   ./build/imagegen/baremetal/imager_output/disk0.raw
    #   ./out/images/baremetal/core-2.0.20231206.1707.vhdx
    #
    #  rootfs partition:
    #
    #   ./out/images/baremetal/mariner-rootfs-ext4-2.0.20231206.1707.ext4.gz
    #   ./out/images/baremetal/mariner-rootfs-ext4-2.0.20231206.1707.ext4
    #
    #   ./out/images/baremetal/mariner-rootfs-raw-2.0.20231206.1707.raw
    #   ./out/images/baremetal/mariner-rootfs-raw-2.0.20231206.1707.raw.gz
    #
    #

    sudo rm -rf ./build/imagegen/baremetal
    sudo rm -rf ./out/images/baremetal

    pushd toolkit
    sudo make image \
        -j$(nproc) \
        REBUILD_TOOLS=y \
        REBUILD_TOOLCHAIN=n \
        REBUILD_PACKAGES=n \
        CONFIG_FILE=$configFile

    mkdir -p $(dirname "$outputDiskRawFile")
    cp ../build/imagegen/baremetal/imager_output/disk0.raw $outputDiskRawFile

    # ./out/images/baremetal/mariner-rootfs-raw-2.0.20231206.1707.raw
    sourceRootfsRawFile=$(find ../out/images/baremetal -name "mariner-rootfs-raw*.raw")
    cp $sourceRootfsRawFile $outputRootfsRawFile

    # ./out/images/baremetal/mariner-rootfs-raw-2.0.20231208.1322.raw.gz
    sourceRootfsRawGzFile=$(find ../out/images/baremetal -name "mariner-rootfs-raw*.raw.gz")
    cp $sourceRootfsRawGzFile $outputRootfsRawGzFile

    popd

    mic_poc_log "---------------- create_full_image [exit] --------"
}

#------------------------------------------------------------------------------
function prepare_root_partition() {
    mic_poc_log "---------------- prepare_root_partition [enter] --------"

    rootfsRawFile=$1
    modifiedRootfsRawFile=$2
    modifiedRootfsSquashFile=$3

    cp $rootfsRawFile \
        $modifiedRootfsRawFile

    # mount
    sudo mkdir -p /mnt/hack
    loDevice=$(sudo losetup -f -P --show $modifiedRootfsRawFile)
    sudo mount $loDevice /mnt/hack

    # modify
    sudo rm -f /mnt/hack/etc/fstab

    # create the squashfs (must be run under sudo or else some files/folder
    # will not be copied correctly)
    sudo mksquashfs /mnt/hack \
        $modifiedRootfsSquashFile

    # umount
    sudo umount /mnt/hack
    # sudo rm -f /mnt/hack
    sudo losetup -d $loDevice

    mic_poc_log "---------------- prepare_root_partition [exit] --------"
}

#------------------------------------------------------------------------------
function mount_raw_disk() {
    local originalRawDisk=$1
    local rawDiskMountDir=$2
    local workingDir=$3

    set +e
    mounted=$(mount | grep $rawDiskMountDir)
    set -e

    if [[ ! -z $mounted ]]; then
        sudo umount $rawDiskMountDir
        sudo rm -r $rawDiskMountDir
    fi

    cp $originalRawDisk $workingDir/
    rawDisk=$workingDir/$(basename "$originalRawDisk")

    loDevice=$(sudo losetup --show -f -P $rawDisk)
    echo "Found lo device: $loDevice"
    
    sudo rm -rf $rawDiskMountDir
    sudo mkdir -p $rawDiskMountDir
    sudo mount ${loDevice}p2 $rawDiskMountDir
}

#------------------------------------------------------------------------------
function unmount_raw_disk() {
    local rawDiskMountDir=$1
    sudo umount $rawDiskMountDir
}

#------------------------------------------------------------------------------
function copy_vmlinuz_from_full_disk() {

    local rawDiskMountDir=$1
    local extractedVmLinuzFile=$2

    extractedVmLinuzFileRootDir=$(dirname $extractedVmLinuzFile)

    sudo rm -rf $extractedVmLinuzFileRootDir
    mkdir -p $extractedVmLinuzFileRootDir

    pushd $extractedVmLinuzFileRootDir

    linuzvm=$(sudo find $rawDiskMountDir/boot/ -name "vmlinuz*")
    sudo cp $linuzvm $extractedVmLinuzFile
    sudo chown $USER:$USER $extractedVmLinuzFile
    ls -la $extractedVmLinuzFile

    popd
}

#------------------------------------------------------------------------------
function extract_artifacts_from_full_image() {
    mic_poc_log "---------------- extract_artifacts_from_full_image [enter] --------"
    local outFullImageRawDisk=$1
    local tmpMount=$2
    local tmpDir=$3
    local extractedVmLinuzFile=$4

    sudo rm -rf $tmpDir
    mkdir -p $tmpDir
    pushd $tmpDir

    mount_raw_disk $outFullImageRawDisk $tmpMount $tmpDir
    copy_vmlinuz_from_full_disk $tmpMount $extractedVmLinuzFile
    unmount_raw_disk $tmpMount

    popd

    sudo chown $USER:$USER -R $(dirname $extractedVmLinuzFile)

    mic_poc_log "---------------- extract_artifacts_from_full_image [exit] --------"
}

#------------------------------------------------------------------------------
function stage_initrd_build_file () {
    local sourceFile=$1
    local targetFile=$2

    sudo cp $sourceFile $targetFile
    sudo chown root:root $targetFile
}

#------------------------------------------------------------------------------
function build_inird() {
    local rawImage=$1
    local initrdArtifactsDir=$2
    local workingFolder=$3
    local initrdImage=$4

    rawImageFolder=$(dirname $rawImage)
    rawImageName=$(basename $rawImage)

    rawImageCopy=$workingFolder/$rawImageName

    mkdir -p $workingFolder
    cp $rawImage $rawImageCopy
    loopDev=$(sudo losetup -f --show $rawImageCopy)
    echo "loopDev=$loopDev"

    mountFolder=/mnt/chroot-raw-image-$$
    sudo mkdir -p $mountFolder
    sudo mount $loopDev $mountFolder

    stage_initrd_build_file $initrdArtifactsDir/20-live-cd.conf     $mountFolder/etc/dracut.conf.d/20-live-cd.conf
    stage_initrd_build_file $initrdArtifactsDir/build-initrd-img.sh $mountFolder/build-initrd-img.sh

    # patch dmsquash-live-root to supress user prompt during boot when the overlay is temporary.
    sudo chmod +w $mountFolder/usr/lib/dracut/modules.d/90dmsquash-live/dmsquash-live-root.sh
    sudo patch -p1 -i $initrdArtifactsDir/no_user_prompt.patch $mountFolder/usr/lib/dracut/modules.d/90dmsquash-live/dmsquash-live-root.sh
    sudo chmod 755 $mountFolder/usr/lib/dracut/modules.d/90dmsquash-live/dmsquash-live-root.sh

    cp $mountFolder/usr/lib/dracut/modules.d/90dmsquash-live/dmsquash-live-root.sh ~/temp/blah.sh

    sudo chroot $mountFolder /bin/bash -c "sudo /build-initrd-img.sh"

    mkdir -p $(dirname $initrdImage)
    sudo cp $mountFolder/initrd.img $initrdImage
    sudo chown $USER:$USER $initrdImage

    sudo umount $mountFolder
    sudo losetup -d $loopDev
    rm $rawImageCopy
}

#------------------------------------------------------------------------------
function CreateEfibootImage () {
    grubCfg=$1
    workingDir=$2
    efitbootImage=$3

    outDir=$(dirname $efitbootImage)
    mkdir -p $workingDir
    mkdir -p $outDir

    rm -f $workingDir/bootx64.efi

    # create bootx64.efi with the our custom grub
    grub-mkstandalone \
        --format=x86_64-efi \
        --locales="" \
        --fonts="" \
        --output=$workingDir/bootx64.efi \
        boot/grub/grub.cfg=$grubCfg

    # Generate the fs to hold the bootx64.efi - i.e. out/efiboot.img
    rm -f $workingDir/efiboot.img

    dd if=/dev/zero of=$efitbootImage bs=1M count=3
    mkfs.vfat $efitbootImage

    LC_CTYPE=C mmd -i $efitbootImage efi efi/boot
    LC_CTYPE=C mcopy -i $efitbootImage $workingDir/bootx64.efi ::efi/boot/

    echo "Created -------- " $efitbootImage
}

#------------------------------------------------------------------------------
function CreateBiosImage () {
    grubCfg=$1
    workingDir=$2
    biosbootImage=$3

    outDir=$(dirname $biosbootImage)
    mkdir -p $workingDir
    mkdir -p $outDir

    rm -f $workingDir/core.img

    grub-mkstandalone \
        --format=i386-pc \
        --install-modules="linux normal iso9660 biosdisk memdisk search tar ls all_video" \
        --modules="linux normal iso9660 biosdisk search" \
        --locales="" \
        --fonts="" \
        --output=$workingDir/core.img \
        boot/grub/grub.cfg=$grubCfg

    # Generate the fs to hold the bios.img - i.e. out/core.img
    if [[ -f $workingDir/bios.img ]]; then
        rm $workingDir/bios.img
    fi

    cat /usr/lib/grub/i386-pc/cdboot.img $workingDir/core.img > $biosbootImage

    echo "Created -------- " $biosbootImage
}


function create_iso_image () {
    inputInitrdFile=$1
    inputVmlinuz=$2
    inputGrubCfg=$3
    inputSquashFS=$4
    mediaSquashFS=$5
    outputIsoLabel=$6
    outputIsoDir=$7

    sudo apt-get install -y mtools dosfstools grub-pc-bin grub-pc xorriso

    intermediateOutputDir=$outputIsoDir/iso-intermediate-artifacts
    mkdir -p $intermediateOutputDir

    stagedIsoArtifactsDir=$outputIsoDir/iso-staged-layout
    sudo rm -r $stagedIsoArtifactsDir
    mkdir -p $stagedIsoArtifactsDir

    finalIsoDir=$outputIsoDir/iso
    mkdir -p $finalIsoDir

    outputIsoImageName=$finalIsoDir/baremetal-$(printf "%(%Y%m%d-%H%M%S)T").iso

    mkdir -p $stagedIsoArtifactsDir/boot
    cp $inputInitrdFile $stagedIsoArtifactsDir/boot/initrd.img
    cp $inputVmlinuz $stagedIsoArtifactsDir/boot/vmlinuz

    if [[ ! -z $inputSquashFS ]] && [[ $inputSquashFS != "none" ]]; then
        stagedSquashFSFile=${stagedIsoArtifactsDir}${mediaSquashFS}
        mkdir -p $(dirname $stagedSquashFSFile)
        cp $inputSquashFS $stagedSquashFSFile
    fi

    CreateEfibootImage \
        $inputGrubCfg \
        $intermediateOutputDir \
        $stagedIsoArtifactsDir/boot/grub/efiboot.img

    CreateBiosImage \
        $inputGrubCfg \
        $intermediateOutputDir \
        $stagedIsoArtifactsDir/boot/grub/bios.img

    # -----------------------------------------------------------------------------
    # Generate the iso

    echo "-- Listing staged iso layout:"
    echo
    pwd
    find $stagedIsoArtifactsDir
    echo

    mkdir -p $outputIsoDir

    sudo xorriso \
        -as mkisofs \
        -iso-level 3 \
        -full-iso9660-filenames \
        -volid $outputIsoLabel \
        -eltorito-boot boot/grub/bios.img \
        -no-emul-boot \
        -boot-load-size 4 \
        -boot-info-table \
        --eltorito-catalog boot/grub/boot.cat \
        --grub2-boot-info \
        --grub2-mbr /usr/lib/grub/i386-pc/boot_hybrid.img \
        -eltorito-alt-boot \
        -e boot/grub/efiboot.img \
        -no-emul-boot \
        -append_partition 2 0xef $stagedIsoArtifactsDir/boot/grub/efiboot.img \
        -graft-points \
            $stagedIsoArtifactsDir \
            /boot/grub/bios.img=$stagedIsoArtifactsDir/boot/grub/bios.img \
            /EFI/efiboot.img=$stagedIsoArtifactsDir/boot/grub/efiboot.img \
        -output $outputIsoImageName

    echo $outputIsoImageName

    set +x
    echo "-------- create-iso-from-initrd-vmlinuz.sh [exit] --------"
}

#------------------------------------------------------------------------------
#-- main ----------------------------------------------------------------------

fullImageConfigFile=~/git/CBL-Mariner/toolkit/imageconfigs/baremetal.json

mkdir -p $buildDir

buildWorkingDir=$buildDir/intermediates
mkdir -p $buildWorkingDir

BUILD_OUT_DIR=$buildDir/out
mkdir -p $BUILD_OUT_DIR

pushd $scriptDir/../../

fullImageRawDisk=$buildWorkingDir/raw-disk-output/disk0.raw

rootfsRawFile=$buildWorkingDir/raw-disk-output/rootfs.img
rootfsRawGzFile=$buildWorkingDir/raw-disk-output/rootfs.img.tgz

modifiedRootfsDir=$buildWorkingDir/raw-disk-output-modified
modifiedRootfsRawFile=$modifiedRootfsDir/rootfs.img
modifiedRootfsSquashFile=$modifiedRootfsDir/rootfs.squashfs

initrdBuildWorkingDir=$buildWorkingDir/initrd-build
initrdBuildOutputFile=$initrdBuildWorkingDir/output/initrd.img

extractArtifactsTmpDir=$buildWorkingDir/extract-artifacts-from-rootfs-tmp-dir
extractArtifactsOutDir=$buildWorkingDir/extract-artifacts-from-rootfs-out-dir
extractedVmlinuz=$extractArtifactsOutDir/extracted-vmlinuz-file/vmlinuz

mediaRootfsSquashfsFile="/LiveOS/rootfs.img"

if [[ ! -z $buildRootfs ]]; then
    create_full_image  \
        $fullImageConfigFile \
        $fullImageRawDisk \
        $rootfsRawFile \
        $rootfsRawGzFile

    extract_artifacts_from_full_image \
        $fullImageRawDisk \
        "/mnt/full-disk-rootfs-mount" \
        $extractArtifactsTmpDir \
        $extractArtifactsOutDir/extracted-vmlinuz-file/vmlinuz

    mkdir -p $modifiedRootfsDir
    prepare_root_partition \
        $rootfsRawFile \
        $modifiedRootfsRawFile \
        $modifiedRootfsSquashFile
fi

build_inird \
    $modifiedRootfsRawFile \
    $scriptDir/initrd-build-artifacts \
    $initrdBuildWorkingDir \
    $initrdBuildOutputFile

create_iso_image \
    $initrdBuildOutputFile \
    $extractedVmlinuz \
    "$scriptDir/grub.cfg" \
    $modifiedRootfsSquashFile \
    $mediaRootfsSquashfsFile \
    "baremetal-iso" \
    $BUILD_OUT_DIR

popd