# Ensure GNU nano is set as EDITOR if it isn't already set

if ( ! ($?EDITOR) ) then
	setenv EDITOR "/usr/bin/nano"
endif
