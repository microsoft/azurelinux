# change default from rsh to ssh for cvs command
if ( "$?CVS_RSH" == 0 ) setenv CVS_RSH ssh
