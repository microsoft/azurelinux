# skip everything for non-interactive shells
if (! $?prompt) exit

# color-ls initialization
if ( $?USER_LS_COLORS ) then
  if ( "$USER_LS_COLORS" != "" ) then
     #when USER_LS_COLORS defined do not override user
     #specified LS_COLORS and use them
     goto finish
  endif
endif

alias ll 'ls -l'
alias l. 'ls -d .*'
set COLORS=/etc/DIR_COLORS

if ($?TERM) then
  if ( -e "/etc/DIR_COLORS.$TERM" ) then
     set COLORS="/etc/DIR_COLORS.$TERM"
  endif
endif
if ( -f ~/.dircolors ) set COLORS=~/.dircolors
if ( -f ~/.dir_colors ) set COLORS=~/.dir_colors
if ($?TERM) then
  if ( -f ~/.dircolors."$TERM" ) set COLORS=~/.dircolors."$TERM"
  if ( -f ~/.dir_colors."$TERM" ) set COLORS=~/.dir_colors."$TERM"
endif
set INCLUDE="`/usr/bin/cat "$COLORS" | /usr/bin/grep '^INCLUDE' | /usr/bin/cut -d ' ' -f2-`"

if ( ! -e "$COLORS" ) exit

set _tmp="`/usr/bin/mktemp .colorlsXXX -q --tmpdir=/tmp`"
#if mktemp fails, exit when include was active, otherwise use $COLORS file
if ( "$_tmp" == '' ) then
  if ( "$INCLUDE" == '' ) then
    eval "`/usr/bin/dircolors -c $COLORS`"
  endif
  goto cleanup
endif

if ( "$INCLUDE" != '' ) /usr/bin/cat "$INCLUDE" >> $_tmp
/usr/bin/grep -v '^INCLUDE' "$COLORS" >> $_tmp

eval "`/usr/bin/dircolors -c $_tmp`"

/usr/bin/rm -f $_tmp

if ( "$LS_COLORS" == '' ) exit
cleanup:
set color_none=`/usr/bin/sed -n '/^COLOR.*none/Ip' < $COLORS`
if ( "$color_none" != '' ) then
   unset color_none
   exit
endif
unset color_none
unset _tmp
unset INCLUDE
unset COLORS

finish:
alias ll 'ls -l --color=auto'
alias l. 'ls -d .* --color=auto'
alias ls 'ls --color=auto'
