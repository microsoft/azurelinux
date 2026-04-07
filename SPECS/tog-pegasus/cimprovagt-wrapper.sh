#!/bin/bash
   
# simple wrapper for Pegasus's cimprovagt
# which allows providers to have separate
# SELinux policy
# see README.RedHat.Security for more info
    
provcimprovagt=/usr/libexec/pegasus/"$5"-cimprovagt
     
if [[ -x "$provcimprovagt" ]]
then
  "$provcimprovagt" "$@"
else
  /usr/libexec/pegasus/cimprovagt "$@"
fi
