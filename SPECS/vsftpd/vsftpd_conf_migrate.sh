#!/bin/bash
#move old config files and symlink them
#shipped with vsftpd-2.0.1-6
shopt -s nullglob
PREFIX="vsftpd"
for file in /etc/${PREFIX}.*; do
    if [ ! -L $file ]; then
        new=`echo $file | sed s/${PREFIX}\./${PREFIX}\\\\//g | sed s/\.rpmsave//g`
        mv -f ${file} ${new}
	ln -s ${new} ${file}
	echo $file moved to $new
    fi
done
