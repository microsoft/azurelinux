#!/bin/bash

set -x
set -e

scriptDir=$(dirname "$BASH_SOURCE")

while getopts ":i:o:" OPTIONS; do
  case "${OPTIONS}" in
    i ) inputImageFile=$OPTARG ;;
    o ) outDir=$OPTARG ;;

    \? )
        echo "-- Error - Invalid Option: -$OPTARG" 1>&2
        exit 1
        ;;
    : )
        echo "-- Error - Invalid Option: -$OPTARG requires an argument" 1>&2
        exit 1
        ;;
  esac
done

if [[ -z $inputImageFile ]]; then
    echo "Specify input image (-i image-file-name)."
    exit 1
fi

if [[ -z $outDir ]]; then
    echo "Specify a output directory (-o dir-name)."
    exit 1
fi

echo "inputImageFile = $inputImageFile"
echo "outDir         = $outDir"

#------------------------------------------------------------------------------
function mic_poc_log() {
    set +x
    echo $1
    set -x
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
    tmpMount=/mnt/$$-rw-rootfs-prepare
    sudo mkdir -p $tmpMount
    loDevice=$(sudo losetup -f -P --show $modifiedRootfsRawFile)
    sudo mount $loDevice $tmpMount

    # modify
    sudo rm -f $tmpMount/etc/fstab

    # create the squashfs (must be run under sudo or else some files/folder
    # will not be copied correctly)
    sudo rm -rf $modifiedRootfsSquashFile
    sudo mksquashfs $tmpMount \
        $modifiedRootfsSquashFile

    # umount
    sudo umount $tmpMount
    sudo losetup -d $loDevice
    sudo rm -r $tmpMount

    mic_poc_log "---------------- prepare_root_partition [exit] --------"
}

#------------------------------------------------------------------------------
function mount_raw_disk() {
    local originalRawDiskFile=$1
    local rawDiskMountDir=$2
    local workingDir=$3
    local loDeviceLogFile=$4

    set +e
    mounted=$(mount | grep $rawDiskMountDir)
    set -e

    if [[ ! -z $mounted ]]; then
        sudo umount $rawDiskMountDir
        sudo rm -r $rawDiskMountDir
    fi

    # create a copy because we have seen examples where the mounted file gets
    # corrupted.
    rawDisk=$workingDir/$(basename "$originalRawDiskFile")
    cp $originalRawDiskFile $rawDisk

    loDevice=$(sudo losetup --show -f -P $rawDisk)
    echo "Found lo device: $loDevice"
    
    sudo rm -rf $rawDiskMountDir
    sudo mkdir -p $rawDiskMountDir
    sudo mount ${loDevice}p2 $rawDiskMountDir

    echo $loDevice > $loDeviceLogFile
}

#------------------------------------------------------------------------------
function unmount_raw_disk() {
    local rawDiskMountDir=$1
    sudo umount $rawDiskMountDir
    sudo rm -r $rawDiskMountDir
}

#------------------------------------------------------------------------------
function guestmount_disk_partition() {
    local originalDiskFile=$1
    local originalDevicePartition=$2
    local diskPartitionMountDir=$3
    local workingDir=$4

    sudo apt-get install -y libguestfs-tools   

    # create a copy because we have seen examples where the mounted file gets
    # corrupted.
    diskFile=$workingDir/$(basename "$originalDiskFile")
    cp $originalDiskFile $diskFile

    sudo rm -rf $diskPartitionMountDir
    sudo mkdir -p $diskPartitionMountDir
    sudo guestmount \
        -a $diskFile \
        -m $originalDevicePartition \
        $diskPartitionMountDir
}

#------------------------------------------------------------------------------
function guestunmount_disk_partition() {
    local diskPartitionMountDir=$1
    sudo guestunmount $diskPartitionMountDir
    sudo rm -r $diskPartitionMountDir
}

#------------------------------------------------------------------------------
function copy_vmlinuz_from_rootfs() {

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
function copy_rootfs_from_device() {
    mic_poc_log "---------------- copy_rootfs_from_device [enter] --------"
    local rawDiskDevice=$1
    local rootfsImageFile=$2

    mkdir -p $(dirname $rootfsImageFile)
    sudo dd if=${rawDiskDevice}p2 of=$rootfsImageFile
    mic_poc_log "---------------- copy_rootfs_from_device [exit] --------"
}

#------------------------------------------------------------------------------
function copy_rootfs_from_dir() {
    mic_poc_log "---------------- copy_rootfs_from_dir [enter] --------"
    local rootfsDir=$1
    local rootfsImageFile=$2

    # 76G
    # 8.8M
    # 124K
    contentSize=$(sudo du -sh $rootfsDir | awk '{print $1}')
    unit=${contentSize: -1}
    unitCount=${contentSize%?}
    toMBFactor=1
    case $unit in
      'K')
        echo "error: rootfs is too small. not supported."
        exit 1
        ;;
      'M')
        toMBFactor=1
        ;;
      'G')
        toMBFactor=1024
        ;;
    esac
    safetyFactor=2
    contentSizeInM=$(( unitCount * toMBFactor * 2 ))
    # wasteFactor=1.5
    # imageSizeInK=$(( contentSizeInK * wasteFactor ))
    mkdir -p $(dirname $rootfsImageFile)
    dd if=/dev/zero of=$rootfsImageFile bs=1M count=$contentSizeInM
    mkfs.ext4 -b 4096 $rootfsImageFile

    rootfsImageDevice=$(sudo losetup -f --show $rootfsImageFile)
    rootfsImageMount=/mnt/$$-rw-rootfs-copy
    sudo mkdir -p $rootfsImageMount
    sudo mount $rootfsImageDevice $rootfsImageMount
    sudo cp -aT $rootfsDir $rootfsImageMount
    sudo umount $rootfsImageMount
    sudo losetup -d $rootfsImageDevice
    sudo rm -r $rootfsImageMount
    mic_poc_log "---------------- copy_rootfs_from_dir [exit] --------"
}

#------------------------------------------------------------------------------
function extract_artifacts_from_full_image() {
    mic_poc_log "---------------- extract_artifacts_from_full_image [enter] --------"
    local imageFile=$1
    local tmpDir=$2
    local extractedVmLinuzFile=$3
    local extractedRootfsImgFile=$4

    sudo rm -rf $tmpDir
    mkdir -p $tmpDir
    pushd $tmpDir

    tmpMount="/mnt/$$-ro-rootfs-extract"

    imageExtension=${imageFile##*.}

    if [[ "$imageExtension" == "raw" ]]; then
        loDeviceLogFile=$tmpDir/lo-device.txt

        mount_raw_disk $imageFile $tmpMount $tmpDir $loDeviceLogFile

        mkdir -p $(dirname $extractedVmLinuzFile)
        copy_vmlinuz_from_rootfs $tmpMount $extractedVmLinuzFile

        loDevice=$(cat $loDeviceLogFile)

        mkdir -p $(dirname $extractedRootfsImgFile)
        copy_rootfs_from_device ${loDevice} $extractedRootfsImgFile

        unmount_raw_disk $tmpMount
        rm loDeviceLogFile
    else
        partitionDevice="/dev/sda2"

        guestmount_disk_partition  \
            $imageFile \
            $partitionDevice \
            $tmpMount \
            $tmpDir

        mkdir -p $(dirname $extractedVmLinuzFile)
        copy_vmlinuz_from_rootfs $tmpMount $extractedVmLinuzFile

        mkdir -p $(dirname $extractedRootfsImgFile)
        copy_rootfs_from_dir $tmpMount $extractedRootfsImgFile
        
        guestunmount_disk_partition $tmpMount
    fi

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

    tmpMount=/mnt/$$-rw-rootfs-chroot
    sudo mkdir -p $tmpMount
    sudo mount $loopDev $tmpMount

    stage_initrd_build_file $initrdArtifactsDir/20-live-cd.conf     $tmpMount/etc/dracut.conf.d/20-live-cd.conf
    stage_initrd_build_file $initrdArtifactsDir/build-initrd-img.sh $tmpMount/build-initrd-img.sh

    # patch dmsquash-live-root to supress user prompt during boot when the overlay is temporary.
    sudo chmod +w $tmpMount/usr/lib/dracut/modules.d/90dmsquash-live/dmsquash-live-root.sh
    sudo patch -p1 -i $initrdArtifactsDir/no_user_prompt.patch $tmpMount/usr/lib/dracut/modules.d/90dmsquash-live/dmsquash-live-root.sh
    sudo chmod 755 $tmpMount/usr/lib/dracut/modules.d/90dmsquash-live/dmsquash-live-root.sh

    cp $tmpMount/usr/lib/dracut/modules.d/90dmsquash-live/dmsquash-live-root.sh ~/temp/blah.sh

    sudo chroot $tmpMount /bin/bash -c "sudo /build-initrd-img.sh"

    mkdir -p $(dirname $initrdImage)
    sudo cp $tmpMount/initrd.img $initrdImage
    sudo chown $USER:$USER $initrdImage

    sudo umount $tmpMount
    sudo losetup -d $loopDev
    sudo rm -r $tmpMount
    rm $rawImageCopy
}

#------------------------------------------------------------------------------
function create_efi_boot_image () {
    grubCfg=$1
    workingDir=$2
    efitbootImage=$3

    outDir=$(dirname $efitbootImage)
    mkdir -p $workingDir
    mkdir -p $outDir

    local bootx64EfiFile=$workingDir/bootx64.efi
    rm -f $bootx64EfiFile

    # create bootx64.efi with the our custom grub
    grub-mkstandalone \
        --format=x86_64-efi \
        --locales="" \
        --fonts="" \
        --output=$bootx64EfiFile \
        boot/grub/grub.cfg=$grubCfg

    # Generate the fs to hold the bootx64.efi - i.e. out/efiboot.img
    rm -f $efitbootImage

    dd if=/dev/zero of=$efitbootImage bs=1M count=3
    mkfs.vfat $efitbootImage
    LC_CTYPE=C mmd -i $efitbootImage efi efi/boot
    LC_CTYPE=C mcopy -i $efitbootImage $bootx64EfiFile ::efi/boot/

    echo "Created -------- " $efitbootImage
}

#------------------------------------------------------------------------------
function create_bios_boot_image () {
    grubCfg=$1
    workingDir=$2
    biosbootImage=$3

    outDir=$(dirname $biosbootImage)
    mkdir -p $workingDir
    mkdir -p $outDir


    coreImage=$workingDir/core.img
    rm -f $coreImage

    grub-mkstandalone \
        --format=i386-pc \
        --install-modules="linux normal iso9660 biosdisk memdisk search tar ls all_video" \
        --modules="linux normal iso9660 biosdisk search" \
        --locales="" \
        --fonts="" \
        --output=$coreImage \
        boot/grub/grub.cfg=$grubCfg

    # Generate the fs to hold the bios.img - i.e. out/core.img
    rm -f $biosbootImage
    cat /usr/lib/grub/i386-pc/cdboot.img $coreImage > $biosbootImage

    echo "Created -------- " $biosbootImage
}

#------------------------------------------------------------------------------
function create_iso_image () {
    mic_poc_log "---------------- create_iso_image [enter] --------"
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
    sudo rm -rf $stagedIsoArtifactsDir
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

    create_efi_boot_image \
        $inputGrubCfg \
        $intermediateOutputDir \
        $stagedIsoArtifactsDir/boot/grub/efiboot.img

    create_bios_boot_image \
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

    mic_poc_log "---------------- create_iso_image [exit] --------"
}

#------------------------------------------------------------------------------
#-- main ----------------------------------------------------------------------

sudo rm -rf $outDir
mkdir -p $outDir

buildWorkingDir=$outDir/intermediates
mkdir -p $buildWorkingDir

isoOutDir=$outDir/iso-out
mkdir -p $isoOutDir

pushd $scriptDir/../../

modifiedRootfsDir=$buildWorkingDir/raw-disk-output-modified
modifiedRootfsRawFile=$modifiedRootfsDir/rootfs.img
modifiedRootfsSquashFile=$modifiedRootfsDir/rootfs.squashfs

initrdBuildWorkingDir=$buildWorkingDir/initrd-build
initrdBuildOutputFile=$initrdBuildWorkingDir/output/initrd.img

extractArtifactsTmpDir=$buildWorkingDir/extract-artifacts-from-rootfs-tmp-dir
extractArtifactsOutDir=$buildWorkingDir/extract-artifacts-from-rootfs-out-dir
extractedVmlinuz=$extractArtifactsOutDir/extracted-vmlinuz-file/vmlinuz
extractedRootfs=$extractArtifactsOutDir/extracted-rootfs-file/rootfs.img

mediaRootfsSquashfsFile="/LiveOS/rootfs.img"

extract_artifacts_from_full_image \
    $inputImageFile \
    $extractArtifactsTmpDir \
    $extractedVmlinuz \
    $extractedRootfs

mkdir -p $modifiedRootfsDir
prepare_root_partition \
    $extractedRootfs \
    $modifiedRootfsRawFile \
    $modifiedRootfsSquashFile

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
    $isoOutDir

popd