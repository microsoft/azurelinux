#!/bin/bash
#open the file "../build/worker/chroot/ghc-8.10.7-121.cm2/mountpoints_list" and umount all the mountpoints
#in the file
#usage: ./umount_mtpts.sh

#store file name in variable file
#file="../build/worker/chroot/ghc-8.10.7-121.cm2/mountpoints_list"
#while read line
#do
#	sudo umount $line
#done < $file

remaining_mtpoints=$(mount | grep chroot | awk '{ for(i=1;i<=NF;i++) { if($i=="on") print $(i+1) } }')
while [ ! -z "$remaining_mtpoints" ]; do
	echo "Unmounting the following mount points: $remaining_mtpoints"
	echo $remaining_mtpoints | xargs -r sudo umount
	remaining_mtpoints=$(mount | grep chroot | awk '{ for(i=1;i<=NF;i++) { if($i=="on") print $(i+1) } }')
done


#mount | grep chroot | awk '{ for(i=1;i<=NF;i++) { if($i=="on") print $(i+1) } }' | xargs -r sudo umount

#print current working directory
echo "Current working directory: $PWD"
chroot_folder="../build/worker/chroot"
#remove the chroot folder
sudo rm -rf $chroot_folder
ls $chroot_folder
#multi-line comment in bash starting below line
: '
#check if above command is successful
if [ $? -eq 0 ]; then
	echo "Successfully removed chroot folder $chroot_folder"
else
	echo "Failed to remove chroot folder"
	#print the error message
	echo $?
fi
'
