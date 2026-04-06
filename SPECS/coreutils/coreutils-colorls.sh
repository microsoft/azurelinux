# color-ls initialization

# Skip all for noninteractive shells.
[ ! -t 0 ] && return

#when USER_LS_COLORS defined do not override user LS_COLORS, but use them.
if [ -z "$USER_LS_COLORS" ]; then

  alias ll='ls -l' 2>/dev/null
  alias l.='ls -d .*' 2>/dev/null

  INCLUDE=
  COLORS=

  for colors in "$HOME/.dir_colors.$TERM" "$HOME/.dircolors.$TERM" \
      "$HOME/.dir_colors" "$HOME/.dircolors"; do
    [ -e "$colors" ] && COLORS="$colors" && \
    INCLUDE="`/usr/bin/cat "$COLORS" | /usr/bin/grep '^INCLUDE' | /usr/bin/cut -d ' ' -f2-`" && \
    break
  done

  [ -z "$COLORS" ] && [ -e "/etc/DIR_COLORS.$TERM" ] && \
  COLORS="/etc/DIR_COLORS.$TERM"

  [ -z "$COLORS" ] && [ -e "/etc/DIR_COLORS" ] && \
  COLORS="/etc/DIR_COLORS"

  # Existence of $COLORS already checked above.
  [ -n "$COLORS" ] || return

  if [ -e "$INCLUDE" ];
  then
    TMP="`/usr/bin/mktemp .colorlsXXX -q --tmpdir=/tmp`"
    [ -z "$TMP" ] && return

    /usr/bin/cat "$INCLUDE" >> $TMP
    /usr/bin/grep -v '^INCLUDE' "$COLORS" >> $TMP

    eval "`/usr/bin/dircolors --sh $TMP 2>/dev/null`"
    /usr/bin/rm -f $TMP
  else
    eval "`/usr/bin/dircolors --sh $COLORS 2>/dev/null`"
  fi

  [ -z "$LS_COLORS" ] && return
  /usr/bin/grep -qi "^COLOR.*none" $COLORS >/dev/null 2>/dev/null && return
fi

unset TMP COLORS INCLUDE

alias ll='ls -l --color=auto' 2>/dev/null
alias l.='ls -d .* --color=auto' 2>/dev/null
alias ls='ls --color=auto' 2>/dev/null
