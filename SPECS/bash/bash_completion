#                                                          -*- shell-script -*-
#
#   bash_completion - programmable completion functions for bash 4.1+
#
#   Copyright © 2006-2008, Ian Macdonald <ian@caliban.org>
#             © 2009-2013, Bash Completion Maintainers
#                     <bash-completion-devel@lists.alioth.debian.org>
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2, or (at your option)
#   any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software Foundation,
#   Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
#   The latest version of this software can be obtained here:
#
#   http://bash-completion.alioth.debian.org/
#
#   RELEASE: 2.1

if [[ $- == *v* ]]; then
    BASH_COMPLETION_ORIGINAL_V_VALUE="-v"
else
    BASH_COMPLETION_ORIGINAL_V_VALUE="+v"
fi

if [[ ${BASH_COMPLETION_DEBUG-} ]]; then
    set -v
else
    set +v
fi

# Set the following to the location of the backwards compat completion dir.
#
: ${BASH_COMPLETION_COMPAT_DIR:=/etc/bash_completion.d}
readonly BASH_COMPLETION_COMPAT_DIR

# Blacklisted completions, causing problems with our code.
#
_blacklist_glob='@(acroread.sh)'

# Turn on extended globbing and programmable completion
shopt -s extglob progcomp

# A lot of the following one-liners were taken directly from the
# completion examples provided with the bash 2.04 source distribution

# Make directory commands see only directories
complete -d pushd

# start of section containing compspecs that can be handled within bash

# user commands see only users
complete -u write chfn groups slay w sux runuser

# bg completes with stopped jobs
complete -A stopped -P '"%' -S '"' bg

# other job commands
complete -j -P '"%' -S '"' fg jobs disown

# readonly and unset complete with shell variables
complete -v readonly unset

# set completes with set options
complete -A setopt set

# shopt completes with shopt options
complete -A shopt shopt

# helptopics
complete -A helptopic help

# unalias completes with aliases
complete -a unalias

# bind completes with readline bindings (make this more intelligent)
complete -A binding bind

# type and which complete on commands
complete -c command type which

# builtin completes on builtins
complete -b builtin

# start of section containing completion functions called by other functions

# Check if we're running on the given userland
# @param $1 userland to check for
_userland()
{
    local userland=$( uname -s )
    [[ $userland == @(Linux|GNU/*) ]] && userland=GNU
    [[ $userland == $1 ]]
}

# This function sets correct SysV init directories
#
_sysvdirs()
{
    sysvdirs=( )
    [[ -d /etc/rc.d/init.d ]] && sysvdirs+=( /etc/rc.d/init.d )
    [[ -d /etc/init.d ]] && sysvdirs+=( /etc/init.d )
    # Slackware uses /etc/rc.d
    [[ -f /etc/slackware-version ]] && sysvdirs=( /etc/rc.d )
}

# This function checks whether we have a given program on the system.
#
_have()
{
    # Completions for system administrator commands are installed as well in
    # case completion is attempted via `sudo command ...'.
    PATH=$PATH:/usr/sbin:/sbin:/usr/local/sbin type $1 &>/dev/null
}

# Backwards compatibility for compat completions that use have().
# @deprecated should no longer be used; generally not needed with dynamically
#             loaded completions, and _have is suitable for runtime use.
have()
{
    unset -v have
    _have $1 && have=yes
}

# This function checks whether a given readline variable
# is `on'.
#
_rl_enabled()
{
    [[ "$( bind -v )" = *$1+([[:space:]])on* ]]
}

# This function shell-quotes the argument
quote()
{
    local quoted=${1//\'/\'\\\'\'}
    printf "'%s'" "$quoted"
}

# @see _quote_readline_by_ref()
quote_readline()
{
    local quoted
    _quote_readline_by_ref "$1" ret
    printf %s "$ret"
} # quote_readline()


# This function shell-dequotes the argument
dequote()
{
    eval printf %s "$1" 2> /dev/null
}


# Assign variable one scope above the caller
# Usage: local "$1" && _upvar $1 "value(s)"
# Param: $1  Variable name to assign value to
# Param: $*  Value(s) to assign.  If multiple values, an array is
#            assigned, otherwise a single value is assigned.
# NOTE: For assigning multiple variables, use '_upvars'.  Do NOT
#       use multiple '_upvar' calls, since one '_upvar' call might
#       reassign a variable to be used by another '_upvar' call.
# See: http://fvue.nl/wiki/Bash:_Passing_variables_by_reference
_upvar()
{
    if unset -v "$1"; then           # Unset & validate varname
        if (( $# == 2 )); then
            eval $1=\"\$2\"          # Return single value
        else
            eval $1=\(\"\${@:2}\"\)  # Return array
        fi
    fi
}


# Assign variables one scope above the caller
# Usage: local varname [varname ...] &&
#        _upvars [-v varname value] | [-aN varname [value ...]] ...
# Available OPTIONS:
#     -aN  Assign next N values to varname as array
#     -v   Assign single value to varname
# Return: 1 if error occurs
# See: http://fvue.nl/wiki/Bash:_Passing_variables_by_reference
_upvars()
{
    if ! (( $# )); then
        echo "${FUNCNAME[0]}: usage: ${FUNCNAME[0]} [-v varname"\
            "value] | [-aN varname [value ...]] ..." 1>&2
        return 2
    fi
    while (( $# )); do
        case $1 in
            -a*)
                # Error checking
                [[ ${1#-a} ]] || { echo "bash: ${FUNCNAME[0]}: \`$1': missing"\
                    "number specifier" 1>&2; return 1; }
                printf %d "${1#-a}" &> /dev/null || { echo "bash:"\
                    "${FUNCNAME[0]}: \`$1': invalid number specifier" 1>&2
                    return 1; }
                # Assign array of -aN elements
                [[ "$2" ]] && unset -v "$2" && eval $2=\(\"\${@:3:${1#-a}}\"\) &&
                shift $((${1#-a} + 2)) || { echo "bash: ${FUNCNAME[0]}:"\
                    "\`$1${2+ }$2': missing argument(s)" 1>&2; return 1; }
                ;;
            -v)
                # Assign single value
                [[ "$2" ]] && unset -v "$2" && eval $2=\"\$3\" &&
                shift 3 || { echo "bash: ${FUNCNAME[0]}: $1: missing"\
                "argument(s)" 1>&2; return 1; }
                ;;
            *)
                echo "bash: ${FUNCNAME[0]}: $1: invalid option" 1>&2
                return 1 ;;
        esac
    done
}


# Reassemble command line words, excluding specified characters from the
# list of word completion separators (COMP_WORDBREAKS).
# @param $1 chars  Characters out of $COMP_WORDBREAKS which should
#     NOT be considered word breaks. This is useful for things like scp where
#     we want to return host:path and not only path, so we would pass the
#     colon (:) as $1 here.
# @param $2 words  Name of variable to return words to
# @param $3 cword  Name of variable to return cword to
#
__reassemble_comp_words_by_ref()
{
    local exclude i j line ref
    # Exclude word separator characters?
    if [[ $1 ]]; then
        # Yes, exclude word separator characters;
        # Exclude only those characters, which were really included
        exclude="${1//[^$COMP_WORDBREAKS]}"
    fi

    # Default to cword unchanged
    eval $3=$COMP_CWORD
    # Are characters excluded which were former included?
    if [[ $exclude ]]; then
        # Yes, list of word completion separators has shrunk;
        line=$COMP_LINE
        # Re-assemble words to complete
        for (( i=0, j=0; i < ${#COMP_WORDS[@]}; i++, j++)); do
            # Is current word not word 0 (the command itself) and is word not
            # empty and is word made up of just word separator characters to
            # be excluded and is current word not preceded by whitespace in
            # original line?
            while [[ $i -gt 0 && ${COMP_WORDS[$i]} == +([$exclude]) ]]; do
                # Is word separator not preceded by whitespace in original line
                # and are we not going to append to word 0 (the command
                # itself), then append to current word.
                [[ $line != [$' \t']* ]] && (( j >= 2 )) && ((j--))
                # Append word separator to current or new word
                ref="$2[$j]"
                eval $2[$j]=\${!ref}\${COMP_WORDS[i]}
                # Indicate new cword
                [[ $i == $COMP_CWORD ]] && eval $3=$j
                # Remove optional whitespace + word separator from line copy
                line=${line#*"${COMP_WORDS[$i]}"}
                # Start new word if word separator in original line is
                # followed by whitespace.
                [[ $line == [$' \t']* ]] && ((j++))
                # Indicate next word if available, else end *both* while and
                # for loop
                (( $i < ${#COMP_WORDS[@]} - 1)) && ((i++)) || break 2
            done
            # Append word to current word
            ref="$2[$j]"
            eval $2[$j]=\${!ref}\${COMP_WORDS[i]}
            # Remove optional whitespace + word from line copy
            line=${line#*"${COMP_WORDS[i]}"}
            # Indicate new cword
            [[ $i == $COMP_CWORD ]] && eval $3=$j
        done
        [[ $i == $COMP_CWORD ]] && eval $3=$j
    else
        # No, list of word completions separators hasn't changed;
        eval $2=\( \"\${COMP_WORDS[@]}\" \)
    fi
} # __reassemble_comp_words_by_ref()


# @param $1 exclude  Characters out of $COMP_WORDBREAKS which should NOT be
#     considered word breaks. This is useful for things like scp where
#     we want to return host:path and not only path, so we would pass the
#     colon (:) as $1 in this case.
# @param $2 words  Name of variable to return words to
# @param $3 cword  Name of variable to return cword to
# @param $4 cur  Name of variable to return current word to complete to
# @see __reassemble_comp_words_by_ref()
__get_cword_at_cursor_by_ref()
{
    local cword words=()
    __reassemble_comp_words_by_ref "$1" words cword

    local i cur index=$COMP_POINT lead=${COMP_LINE:0:$COMP_POINT}
    # Cursor not at position 0 and not leaded by just space(s)?
    if [[ $index -gt 0 && ( $lead && ${lead//[[:space:]]} ) ]]; then
        cur=$COMP_LINE
        for (( i = 0; i <= cword; ++i )); do
            while [[
                # Current word fits in $cur?
                ${#cur} -ge ${#words[i]} &&
                # $cur doesn't match cword?
                "${cur:0:${#words[i]}}" != "${words[i]}"
            ]]; do
                # Strip first character
                cur="${cur:1}"
                # Decrease cursor position
                ((index--))
            done

            # Does found word match cword?
            if [[ $i -lt $cword ]]; then
                # No, cword lies further;
                local old_size=${#cur}
                cur="${cur#"${words[i]}"}"
                local new_size=${#cur}
                index=$(( index - old_size + new_size ))
            fi
        done
        # Clear $cur if just space(s)
        [[ $cur && ! ${cur//[[:space:]]} ]] && cur=
        # Zero $index if negative
        [[ $index -lt 0 ]] && index=0
    fi

    local "$2" "$3" "$4" && _upvars -a${#words[@]} $2 "${words[@]}" \
        -v $3 "$cword" -v $4 "${cur:0:$index}"
}


# Get the word to complete and optional previous words.
# This is nicer than ${COMP_WORDS[$COMP_CWORD]}, since it handles cases
# where the user is completing in the middle of a word.
# (For example, if the line is "ls foobar",
# and the cursor is here -------->   ^
# Also one is able to cross over possible wordbreak characters.
# Usage: _get_comp_words_by_ref [OPTIONS] [VARNAMES]
# Available VARNAMES:
#     cur         Return cur via $cur
#     prev        Return prev via $prev
#     words       Return words via $words
#     cword       Return cword via $cword
#
# Available OPTIONS:
#     -n EXCLUDE  Characters out of $COMP_WORDBREAKS which should NOT be
#                 considered word breaks. This is useful for things like scp
#                 where we want to return host:path and not only path, so we
#                 would pass the colon (:) as -n option in this case.
#     -c VARNAME  Return cur via $VARNAME
#     -p VARNAME  Return prev via $VARNAME
#     -w VARNAME  Return words via $VARNAME
#     -i VARNAME  Return cword via $VARNAME
#
# Example usage:
#
#    $ _get_comp_words_by_ref -n : cur prev
#
_get_comp_words_by_ref()
{
    local exclude flag i OPTIND=1
    local cur cword words=()
    local upargs=() upvars=() vcur vcword vprev vwords

    while getopts "c:i:n:p:w:" flag "$@"; do
        case $flag in
            c) vcur=$OPTARG ;;
            i) vcword=$OPTARG ;;
            n) exclude=$OPTARG ;;
            p) vprev=$OPTARG ;;
            w) vwords=$OPTARG ;;
        esac
    done
    while [[ $# -ge $OPTIND ]]; do
        case ${!OPTIND} in
            cur)   vcur=cur ;;
            prev)  vprev=prev ;;
            cword) vcword=cword ;;
            words) vwords=words ;;
            *) echo "bash: $FUNCNAME(): \`${!OPTIND}': unknown argument" \
                1>&2; return 1
        esac
        let "OPTIND += 1"
    done

    __get_cword_at_cursor_by_ref "$exclude" words cword cur

    [[ $vcur   ]] && { upvars+=("$vcur"  ); upargs+=(-v $vcur   "$cur"  ); }
    [[ $vcword ]] && { upvars+=("$vcword"); upargs+=(-v $vcword "$cword"); }
    [[ $vprev && $cword -ge 1 ]] && { upvars+=("$vprev" ); upargs+=(-v $vprev
        "${words[cword - 1]}"); }
    [[ $vwords ]] && { upvars+=("$vwords"); upargs+=(-a${#words[@]} $vwords
        "${words[@]}"); }

    (( ${#upvars[@]} )) && local "${upvars[@]}" && _upvars "${upargs[@]}"
}


# Get the word to complete.
# This is nicer than ${COMP_WORDS[$COMP_CWORD]}, since it handles cases
# where the user is completing in the middle of a word.
# (For example, if the line is "ls foobar",
# and the cursor is here -------->   ^
# @param $1 string  Characters out of $COMP_WORDBREAKS which should NOT be
#     considered word breaks. This is useful for things like scp where
#     we want to return host:path and not only path, so we would pass the
#     colon (:) as $1 in this case.
# @param $2 integer  Index number of word to return, negatively offset to the
#     current word (default is 0, previous is 1), respecting the exclusions
#     given at $1.  For example, `_get_cword "=:" 1' returns the word left of
#     the current word, respecting the exclusions "=:".
# @deprecated  Use `_get_comp_words_by_ref cur' instead
# @see _get_comp_words_by_ref()
_get_cword()
{
    local LC_CTYPE=C
    local cword words
    __reassemble_comp_words_by_ref "$1" words cword

    # return previous word offset by $2
    if [[ ${2//[^0-9]/} ]]; then
        printf "%s" "${words[cword-$2]}"
    elif [[ "${#words[cword]}" -eq 0 || "$COMP_POINT" == "${#COMP_LINE}" ]]; then
        printf "%s" "${words[cword]}"
    else
        local i
        local cur="$COMP_LINE"
        local index="$COMP_POINT"
        for (( i = 0; i <= cword; ++i )); do
            while [[
                # Current word fits in $cur?
                "${#cur}" -ge ${#words[i]} &&
                # $cur doesn't match cword?
                "${cur:0:${#words[i]}}" != "${words[i]}"
            ]]; do
                # Strip first character
                cur="${cur:1}"
                # Decrease cursor position
                ((index--))
            done

            # Does found word matches cword?
            if [[ "$i" -lt "$cword" ]]; then
                # No, cword lies further;
                local old_size="${#cur}"
                cur="${cur#${words[i]}}"
                local new_size="${#cur}"
                index=$(( index - old_size + new_size ))
            fi
        done

        if [[ "${words[cword]:0:${#cur}}" != "$cur" ]]; then
            # We messed up! At least return the whole word so things
            # keep working
            printf "%s" "${words[cword]}"
        else
            printf "%s" "${cur:0:$index}"
        fi
    fi
} # _get_cword()


# Get word previous to the current word.
# This is a good alternative to `prev=${COMP_WORDS[COMP_CWORD-1]}' because bash4
# will properly return the previous word with respect to any given exclusions to
# COMP_WORDBREAKS.
# @deprecated  Use `_get_comp_words_by_ref cur prev' instead
# @see _get_comp_words_by_ref()
#
_get_pword()
{
    if [[ $COMP_CWORD -ge 1 ]]; then
        _get_cword "${@:-}" 1
    fi
}


# If the word-to-complete contains a colon (:), left-trim COMPREPLY items with
# word-to-complete.
# With a colon in COMP_WORDBREAKS, words containing
# colons are always completed as entire words if the word to complete contains
# a colon.  This function fixes this, by removing the colon-containing-prefix
# from COMPREPLY items.
# The preferred solution is to remove the colon (:) from COMP_WORDBREAKS in
# your .bashrc:
#
#    # Remove colon (:) from list of word completion separators
#    COMP_WORDBREAKS=${COMP_WORDBREAKS//:}
#
# See also: Bash FAQ - E13) Why does filename completion misbehave if a colon
# appears in the filename? - http://tiswww.case.edu/php/chet/bash/FAQ
# @param $1 current word to complete (cur)
# @modifies global array $COMPREPLY
#
__ltrim_colon_completions()
{
    if [[ "$1" == *:* && "$COMP_WORDBREAKS" == *:* ]]; then
        # Remove colon-word prefix from COMPREPLY items
        local colon_word=${1%"${1##*:}"}
        local i=${#COMPREPLY[*]}
        while [[ $((--i)) -ge 0 ]]; do
            COMPREPLY[$i]=${COMPREPLY[$i]#"$colon_word"}
        done
    fi
} # __ltrim_colon_completions()


# This function quotes the argument in a way so that readline dequoting
# results in the original argument.  This is necessary for at least
# `compgen' which requires its arguments quoted/escaped:
#
#     $ ls "a'b/"
#     c
#     $ compgen -f "a'b/"       # Wrong, doesn't return output
#     $ compgen -f "a\'b/"      # Good
#     a\'b/c
#
# See also:
# - http://lists.gnu.org/archive/html/bug-bash/2009-03/msg00155.html
# - http://www.mail-archive.com/bash-completion-devel@lists.alioth.\
#   debian.org/msg01944.html
# @param $1  Argument to quote
# @param $2  Name of variable to return result to
_quote_readline_by_ref()
{
    if [ -z "$1" ]; then
        # avoid quoting if empty
        printf -v $2 %s "$1"
    elif [[ $1 == \'* ]]; then
        # Leave out first character
        printf -v $2 %s "${1:1}"
    elif [[ $1 == ~* ]]; then
        # avoid escaping first ~
        printf -v $2 ~%q "${1:1}"
    else
        printf -v $2 %q "$1"
    fi

    # Replace double escaping ( \\ ) by single ( \ )
    # This happens always when argument is already escaped at cmdline,
    # and passed to this function as e.g.: file\ with\ spaces
    [[ ${!2} == *\\* ]] && printf -v $2 %s "${1//\\\\/\\}"

    # If result becomes quoted like this: $'string', re-evaluate in order to
    # drop the additional quoting.  See also: http://www.mail-archive.com/
    # bash-completion-devel@lists.alioth.debian.org/msg01942.html
    [[ ${!2} == \$* ]] && eval $2=${!2}
} # _quote_readline_by_ref()


# This function performs file and directory completion. It's better than
# simply using 'compgen -f', because it honours spaces in filenames.
# @param $1  If `-d', complete only on directories.  Otherwise filter/pick only
#            completions with `.$1' and the uppercase version of it as file
#            extension.
#
_filedir()
{
    local i IFS=$'\n' xspec

    _tilde "$cur" || return 0

    local -a toks
    local quoted x tmp

    _quote_readline_by_ref "$cur" quoted
    x=$( compgen -d -- "$quoted" ) &&
    while read -r tmp; do
        toks+=( "$tmp" )
    done <<< "$x"

    if [[ "$1" != -d ]]; then
        # Munge xspec to contain uppercase version too
        # http://thread.gmane.org/gmane.comp.shells.bash.bugs/15294/focus=15306
        xspec=${1:+"!*.@($1|${1^^})"}
        x=$( compgen -f -X "$xspec" -- $quoted ) &&
        while read -r tmp; do
            toks+=( "$tmp" )
        done <<< "$x"
    fi

    # If the filter failed to produce anything, try without it if configured to
    [[ -n ${COMP_FILEDIR_FALLBACK:-} && \
        -n "$1" && "$1" != -d && ${#toks[@]} -lt 1 ]] && \
        x=$( compgen -f -- $quoted ) &&
        while read -r tmp; do
            toks+=( "$tmp" )
        done <<< "$x"


    if [[ ${#toks[@]} -ne 0 ]]; then
        # 2>/dev/null for direct invocation, e.g. in the _filedir unit test
        compopt -o filenames 2>/dev/null
        COMPREPLY+=( "${toks[@]}" )
    fi
} # _filedir()


# This function splits $cur=--foo=bar into $prev=--foo, $cur=bar, making it
# easier to support both "--foo bar" and "--foo=bar" style completions.
# `=' should have been removed from COMP_WORDBREAKS when setting $cur for
# this to be useful.
# Returns 0 if current option was split, 1 otherwise.
#
_split_longopt()
{
    if [[ "$cur" == --?*=* ]]; then
        # Cut also backslash before '=' in case it ended up there
        # for some reason.
        prev="${cur%%?(\\)=*}"
        cur="${cur#*=}"
        return 0
    fi

    return 1
}

# Complete variables.
# @return  True (0) if variables were completed,
#          False (> 0) if not.
_variables()
{
    if [[ $cur =~ ^(\$\{?)([A-Za-z0-9_]*)$ ]]; then
        [[ $cur == *{* ]] && local suffix=} || local suffix=
        COMPREPLY+=( $( compgen -P ${BASH_REMATCH[1]} -S "$suffix" -v -- \
            "${BASH_REMATCH[2]}" ) )
        return 0
    fi
    return 1
}

# Initialize completion and deal with various general things: do file
# and variable completion where appropriate, and adjust prev, words,
# and cword as if no redirections exist so that completions do not
# need to deal with them.  Before calling this function, make sure
# cur, prev, words, and cword are local, ditto split if you use -s.
#
# Options:
#     -n EXCLUDE  Passed to _get_comp_words_by_ref -n with redirection chars
#     -e XSPEC    Passed to _filedir as first arg for stderr redirections
#     -o XSPEC    Passed to _filedir as first arg for other output redirections
#     -i XSPEC    Passed to _filedir as first arg for stdin redirections
#     -s          Split long options with _split_longopt, implies -n =
# @return  True (0) if completion needs further processing,
#          False (> 0) no further processing is necessary.
#
_init_completion()
{
    local exclude= flag outx errx inx OPTIND=1

    while getopts "n:e:o:i:s" flag "$@"; do
        case $flag in
            n) exclude+=$OPTARG ;;
            e) errx=$OPTARG ;;
            o) outx=$OPTARG ;;
            i) inx=$OPTARG ;;
            s) split=false ; exclude+== ;;
        esac
    done

    # For some reason completion functions are not invoked at all by
    # bash (at least as of 4.1.7) after the command line contains an
    # ampersand so we don't get a chance to deal with redirections
    # containing them, but if we did, hopefully the below would also
    # do the right thing with them...

    COMPREPLY=()
    local redir="@(?([0-9])<|?([0-9&])>?(>)|>&)"
    _get_comp_words_by_ref -n "$exclude<>&" cur prev words cword

    # Complete variable names.
    _variables && return 1

    # Complete on files if current is a redirect possibly followed by a
    # filename, e.g. ">foo", or previous is a "bare" redirect, e.g. ">".
    if [[ $cur == $redir* || $prev == $redir ]]; then
        local xspec
        case $cur in
            2'>'*) xspec=$errx ;;
            *'>'*) xspec=$outx ;;
            *'<'*) xspec=$inx ;;
            *)
                case $prev in
                    2'>'*) xspec=$errx ;;
                    *'>'*) xspec=$outx ;;
                    *'<'*) xspec=$inx ;;
                esac
                ;;
        esac
        cur="${cur##$redir}"
        _filedir $xspec
        return 1
    fi

    # Remove all redirections so completions don't have to deal with them.
    local i skip
    for (( i=1; i < ${#words[@]}; )); do
        if [[ ${words[i]} == $redir* ]]; then
            # If "bare" redirect, remove also the next word (skip=2).
            [[ ${words[i]} == $redir ]] && skip=2 || skip=1
            words=( "${words[@]:0:i}" "${words[@]:i+skip}" )
            [[ $i -le $cword ]] && cword=$(( cword - skip ))
        else
            i=$(( ++i ))
        fi
    done

    [[ $cword -le 0 ]] && return 1
    prev=${words[cword-1]}

    [[ ${split-} ]] && _split_longopt && split=true

    return 0
}

# Helper function for _parse_help and _parse_usage.
__parse_options()
{
    local option option2 i IFS=$' \t\n,/|'

    # Take first found long option, or first one (short) if not found.
    option=
    for i in $1; do
        case $i in
            ---*) break ;;
            --?*) option=$i ; break ;;
            -?*)  [[ $option ]] || option=$i ;;
            *)    break ;;
        esac
    done
    [[ $option ]] || return 0

    IFS=$' \t\n' # affects parsing of the regexps below...

    # Expand --[no]foo to --foo and --nofoo etc
    if [[ $option =~ (\[((no|dont)-?)\]). ]]; then
        option2=${option/"${BASH_REMATCH[1]}"/}
        option2=${option2%%[<{().[]*}
        printf '%s\n' "${option2/=*/=}"
        option=${option/"${BASH_REMATCH[1]}"/"${BASH_REMATCH[2]}"}
    fi

    option=${option%%[<{().[]*}
    printf '%s\n' "${option/=*/=}"
}

# Parse GNU style help output of the given command.
# @param $1  command; if "-", read from stdin and ignore rest of args
# @param $2  command options (default: --help)
#
_parse_help()
{
    eval local cmd=$( quote "$1" )
    local line
    { case $cmd in
        -) cat ;;
        *) LC_ALL=C "$( dequote "$cmd" )" ${2:---help} 2>&1 ;;
      esac } \
    | while read -r line; do

        [[ $line == *([ $'\t'])-* ]] || continue
        # transform "-f FOO, --foo=FOO" to "-f , --foo=FOO" etc
        while [[ $line =~ \
            ((^|[^-])-[A-Za-z0-9?][[:space:]]+)\[?[A-Z0-9]+\]? ]]; do
            line=${line/"${BASH_REMATCH[0]}"/"${BASH_REMATCH[1]}"}
        done
        __parse_options "${line// or /, }"

    done
}

# Parse BSD style usage output (options in brackets) of the given command.
# @param $1  command; if "-", read from stdin and ignore rest of args
# @param $2  command options (default: --usage)
#
_parse_usage()
{
    eval local cmd=$( quote "$1" )
    local line match option i char
    { case $cmd in
        -) cat ;;
        *) LC_ALL=C "$( dequote "$cmd" )" ${2:---usage} 2>&1 ;;
      esac } \
    | while read -r line; do

        while [[ $line =~ \[[[:space:]]*(-[^]]+)[[:space:]]*\] ]]; do
            match=${BASH_REMATCH[0]}
            option=${BASH_REMATCH[1]}
            case $option in
                -?(\[)+([a-zA-Z0-9?]))
                    # Treat as bundled short options
                    for (( i=1; i < ${#option}; i++ )); do
                        char=${option:i:1}
                        [[ $char != '[' ]] && printf '%s\n' -$char
                    done
                    ;;
                *)
                    __parse_options "$option"
                    ;;
            esac
            line=${line#*"$match"}
        done

    done
}

# This function completes on signal names (minus the SIG prefix)
# @param $1 prefix
_signals()
{
    local -a sigs=( $( compgen -P "$1" -A signal "SIG${cur#$1}" ) )
    COMPREPLY+=( "${sigs[@]/#${1}SIG/${1}}" )
}

# This function completes on known mac addresses
#
_mac_addresses()
{
    local re='\([A-Fa-f0-9]\{2\}:\)\{5\}[A-Fa-f0-9]\{2\}'
    local PATH="$PATH:/sbin:/usr/sbin"

    # Local interfaces
    # - ifconfig on Linux: HWaddr or ether
    # - ifconfig on FreeBSD: ether
    # - ip link: link/ether
    COMPREPLY+=( $( \
        { LC_ALL=C ifconfig -a || ip link show; } 2>/dev/null | sed -ne \
        "s/.*[[:space:]]HWaddr[[:space:]]\{1,\}\($re\)[[:space:]].*/\1/p" -ne \
        "s/.*[[:space:]]HWaddr[[:space:]]\{1,\}\($re\)[[:space:]]*$/\1/p" -ne \
        "s|.*[[:space:]]\(link/\)\{0,1\}ether[[:space:]]\{1,\}\($re\)[[:space:]].*|\2|p" -ne \
        "s|.*[[:space:]]\(link/\)\{0,1\}ether[[:space:]]\{1,\}\($re\)[[:space:]]*$|\2|p"
        ) )

    # ARP cache
    COMPREPLY+=( $( { arp -an || ip neigh show; } 2>/dev/null | sed -ne \
        "s/.*[[:space:]]\($re\)[[:space:]].*/\1/p" -ne \
        "s/.*[[:space:]]\($re\)[[:space:]]*$/\1/p" ) )

    # /etc/ethers
    COMPREPLY+=( $( sed -ne \
        "s/^[[:space:]]*\($re\)[[:space:]].*/\1/p" /etc/ethers 2>/dev/null ) )

    COMPREPLY=( $( compgen -W '${COMPREPLY[@]}' -- "$cur" ) )
    __ltrim_colon_completions "$cur"
}

# This function completes on configured network interfaces
#
_configured_interfaces()
{
    if [[ -f /etc/debian_version ]]; then
        # Debian system
        COMPREPLY=( $( compgen -W "$( sed -ne 's|^iface \([^ ]\{1,\}\).*$|\1|p'\
            /etc/network/interfaces )" -- "$cur" ) )
    elif [[ -f /etc/SuSE-release ]]; then
        # SuSE system
        COMPREPLY=( $( compgen -W "$( printf '%s\n' \
            /etc/sysconfig/network/ifcfg-* | \
            sed -ne 's|.*ifcfg-\(.*\)|\1|p' )" -- "$cur" ) )
    elif [[ -f /etc/pld-release ]]; then
        # PLD Linux
        COMPREPLY=( $( compgen -W "$( command ls -B \
            /etc/sysconfig/interfaces | \
            sed -ne 's|.*ifcfg-\(.*\)|\1|p' )" -- "$cur" ) )
    else
        # Assume Red Hat
        COMPREPLY=( $( compgen -W "$( printf '%s\n' \
            /etc/sysconfig/network-scripts/ifcfg-* | \
            sed -ne 's|.*ifcfg-\(.*\)|\1|p' )" -- "$cur" ) )
    fi
}

# Local IP addresses.
#
_ip_addresses()
{
    local PATH=$PATH:/sbin
    COMPREPLY+=( $( compgen -W \
        "$( { LC_ALL=C ifconfig -a || ip addr show; } 2>/dev/null |
            sed -ne 's/.*addr:\([^[:space:]]*\).*/\1/p' \
                -ne 's|.*inet[[:space:]]\{1,\}\([^[:space:]/]*\).*|\1|p' )" \
        -- "$cur" ) )
}

# This function completes on available kernels
#
_kernel_versions()
{
    COMPREPLY=( $( compgen -W '$( command ls /lib/modules )' -- "$cur" ) )
}

# This function completes on all available network interfaces
# -a: restrict to active interfaces only
# -w: restrict to wireless interfaces only
#
_available_interfaces()
{
    local cmd PATH=$PATH:/sbin

    if [[ ${1:-} == -w ]]; then
        cmd="iwconfig"
    elif [[ ${1:-} == -a ]]; then
        cmd="{ ifconfig || ip link show up; }"
    else
        cmd="{ ifconfig -a || ip link show; }"
    fi

    COMPREPLY=( $( eval $cmd 2>/dev/null | awk \
        '/^[^ \t]/ { if ($1 ~ /^[0-9]+:/) { print $2 } else { print $1 } }' ) )
    COMPREPLY=( $( compgen -W '${COMPREPLY[@]/%[[:punct:]]/}' -- "$cur" ) )
}

# Echo number of CPUs, falling back to 1 on failure.
_ncpus()
{
    local var=NPROCESSORS_ONLN
    [[ $OSTYPE == *linux* ]] && var=_$var
    local n=$( getconf $var 2>/dev/null )
    printf %s ${n:-1}
}

# Perform tilde (~) completion
# @return  True (0) if completion needs further processing,
#          False (> 0) if tilde is followed by a valid username, completions
#          are put in COMPREPLY and no further processing is necessary.
_tilde()
{
    local result=0
    if [[ $1 == \~* && $1 != */* ]]; then
        # Try generate ~username completions
        COMPREPLY=( $( compgen -P '~' -u "${1#\~}" ) )
        result=${#COMPREPLY[@]}
        # 2>/dev/null for direct invocation, e.g. in the _tilde unit test
        [[ $result -gt 0 ]] && compopt -o filenames 2>/dev/null
    fi
    return $result
}


# Expand variable starting with tilde (~)
# We want to expand ~foo/... to /home/foo/... to avoid problems when
# word-to-complete starting with a tilde is fed to commands and ending up
# quoted instead of expanded.
# Only the first portion of the variable from the tilde up to the first slash
# (~../) is expanded.  The remainder of the variable, containing for example
# a dollar sign variable ($) or asterisk (*) is not expanded.
# Example usage:
#
#    $ v="~"; __expand_tilde_by_ref v; echo "$v"
#
# Example output:
#
#       v                  output
#    --------         ----------------
#    ~                /home/user
#    ~foo/bar         /home/foo/bar
#    ~foo/$HOME       /home/foo/$HOME
#    ~foo/a  b        /home/foo/a  b
#    ~foo/*           /home/foo/*
#
# @param $1  Name of variable (not the value of the variable) to expand
__expand_tilde_by_ref()
{
    # Does $1 start with tilde (~)?
    if [[ ${!1} == \~* ]]; then
        # Does $1 contain slash (/)?
        if [[ ${!1} == */* ]]; then
            # Yes, $1 contains slash;
            # 1: Remove * including and after first slash (/), i.e. "~a/b"
            #    becomes "~a".  Double quotes allow eval.
            # 2: Remove * before the first slash (/), i.e. "~a/b"
            #    becomes "b".  Single quotes prevent eval.
            #       +-----1----+ +---2----+
            eval $1="${!1/%\/*}"/'${!1#*/}'
        else
            # No, $1 doesn't contain slash
            eval $1="${!1}"
        fi
    fi
} # __expand_tilde_by_ref()


# This function expands tildes in pathnames
#
_expand()
{
    # FIXME: Why was this here?
    #[ "$cur" != "${cur%\\}" ] && cur+="\\"

    # Expand ~username type directory specifications.  We want to expand
    # ~foo/... to /home/foo/... to avoid problems when $cur starting with
    # a tilde is fed to commands and ending up quoted instead of expanded.

    if [[ "$cur" == \~*/* ]]; then
        eval cur=$cur 2>/dev/null
    elif [[ "$cur" == \~* ]]; then
        cur=${cur#\~}
        COMPREPLY=( $( compgen -P '~' -u "$cur" ) )
        [[ ${#COMPREPLY[@]} -eq 1 ]] && eval COMPREPLY[0]=${COMPREPLY[0]}
        return ${#COMPREPLY[@]}
    fi
}

# This function completes on process IDs.
# AIX and Solaris ps prefers X/Open syntax.
[[ $OSTYPE == *@(solaris|aix)* ]] &&
_pids()
{
    COMPREPLY=( $( compgen -W '$( command ps -efo pid | sed 1d )' -- "$cur" ))
} ||
_pids()
{
    COMPREPLY=( $( compgen -W '$( command ps axo pid= )' -- "$cur" ) )
}

# This function completes on process group IDs.
# AIX and SunOS prefer X/Open, all else should be BSD.
[[ $OSTYPE == *@(solaris|aix)* ]] &&
_pgids()
{
    COMPREPLY=( $( compgen -W '$( command ps -efo pgid | sed 1d )' -- "$cur" ))
} ||
_pgids()
{
    COMPREPLY=( $( compgen -W '$( command ps axo pgid= )' -- "$cur" ))
}

# This function completes on process names.
# AIX and SunOS prefer X/Open, all else should be BSD.
[[ $OSTYPE == *@(solaris|aix)* ]] &&
_pnames()
{
    COMPREPLY=( $( compgen -X '<defunct>' -W '$( command ps -efo comm | \
        sed -e 1d -e "s:.*/::" -e "s/^-//" | sort -u )' -- "$cur" ) )
} ||
_pnames()
{
    # FIXME: completes "[kblockd/0]" to "0". Previously it was completed
    # to "kblockd" which isn't correct either. "kblockd/0" would be
    # arguably most correct, but killall from psmisc 22 treats arguments
    # containing "/" specially unless -r is given so that wouldn't quite
    # work either. Perhaps it'd be best to not complete these to anything
    # for now.
    # Not using "ps axo comm" because under some Linux kernels, it
    # truncates command names (see e.g. http://bugs.debian.org/497540#19)
    COMPREPLY=( $( compgen -X '<defunct>' -W '$( command ps axo command= | \
        sed -e "s/ .*//" -e "s:.*/::" -e "s/:$//" -e "s/^[[(-]//" \
            -e "s/[])]$//" | sort -u )' -- "$cur" ) )
}

# This function completes on user IDs
#
_uids()
{
    if type getent &>/dev/null; then
        COMPREPLY=( $( compgen -W '$( getent passwd | cut -d: -f3 )' -- "$cur" ) )
    elif type perl &>/dev/null; then
        COMPREPLY=( $( compgen -W '$( perl -e '"'"'while (($uid) = (getpwent)[2]) { print $uid . "\n" }'"'"' )' -- "$cur" ) )
    else
        # make do with /etc/passwd
        COMPREPLY=( $( compgen -W '$( cut -d: -f3 /etc/passwd )' -- "$cur" ) )
    fi
}

# This function completes on group IDs
#
_gids()
{
    if type getent &>/dev/null; then
        COMPREPLY=( $( compgen -W '$( getent group | cut -d: -f3 )' \
            -- "$cur" ) )
    elif type perl &>/dev/null; then
        COMPREPLY=( $( compgen -W '$( perl -e '"'"'while (($gid) = (getgrent)[2]) { print $gid . "\n" }'"'"' )' -- "$cur" ) )
    else
        # make do with /etc/group
        COMPREPLY=( $( compgen -W '$( cut -d: -f3 /etc/group )' -- "$cur" ) )
    fi
}

# Glob for matching various backup files.
#
_backup_glob='@(#*#|*@(~|.@(bak|orig|rej|swp|dpkg*|rpm@(orig|new|save))))'

# Complete on xinetd services
#
_xinetd_services()
{
    local xinetddir=/etc/xinetd.d
    if [[ -d $xinetddir ]]; then
        local restore_nullglob=$(shopt -p nullglob); shopt -s nullglob
        local -a svcs=( $( printf '%s\n' $xinetddir/!($_backup_glob) ) )
        $restore_nullglob
        COMPREPLY+=( $( compgen -W '${svcs[@]#$xinetddir/}' -- "$cur" ) )
    fi
}

# This function completes on services
#
_services()
{
    local sysvdirs
    _sysvdirs

    local restore_nullglob=$(shopt -p nullglob); shopt -s nullglob
    COMPREPLY=( $( printf '%s\n' ${sysvdirs[0]}/!($_backup_glob|functions) ) )
    $restore_nullglob

    COMPREPLY+=( $( systemctl list-units --full --all 2>/dev/null | \
        awk '$1 ~ /\.service$/ { sub("\\.service$", "", $1); print $1 }' ) )

    COMPREPLY=( $( compgen -W '${COMPREPLY[@]#${sysvdirs[0]}/}' -- "$cur" ) )
}

# This completes on a list of all available service scripts for the
# 'service' command and/or the SysV init.d directory, followed by
# that script's available commands
#
_service()
{
    local cur prev words cword
    _init_completion || return

    # don't complete past 2nd token
    [[ $cword -gt 2 ]] && return 0

    if [[ $cword -eq 1 && $prev == ?(*/)service ]]; then
        _services
        [[ -e /etc/mandrake-release ]] && _xinetd_services
    else
        local sysvdirs
        _sysvdirs
        COMPREPLY=( $( compgen -W '`sed -e "y/|/ /" \
            -ne "s/^.*\(U\|msg_u\)sage.*{\(.*\)}.*$/\2/p" \
            ${sysvdirs[0]}/${prev##*/} 2>/dev/null` start stop' -- "$cur" ) )
    fi
} &&
complete -F _service service
_sysvdirs
for svcdir in ${sysvdirs[@]}; do
    for svc in $svcdir/!($_backup_glob); do
        [[ -x $svc ]] && complete -F _service $svc
    done
done
unset svc svcdir sysvdirs

# This function completes on modules
#
_modules()
{
    local modpath
    modpath=/lib/modules/$1
    COMPREPLY=( $( compgen -W "$( command ls -RL $modpath 2>/dev/null | \
        sed -ne 's/^\(.*\)\.k\{0,1\}o\(\.[gx]z\)\{0,1\}$/\1/p' )" -- "$cur" ) )
}

# This function completes on installed modules
#
_installed_modules()
{
    COMPREPLY=( $( compgen -W "$( PATH="$PATH:/sbin" lsmod | \
        awk '{if (NR != 1) print $1}' )" -- "$1" ) )
}

# This function completes on user or user:group format; as for chown and cpio.
#
# The : must be added manually; it will only complete usernames initially.
# The legacy user.group format is not supported.
#
# @param $1  If -u, only return users/groups the user has access to in
#            context of current completion.
_usergroup()
{
    if [[ $cur = *\\\\* || $cur = *:*:* ]]; then
        # Give up early on if something seems horribly wrong.
        return
    elif [[ $cur = *\\:* ]]; then
        # Completing group after 'user\:gr<TAB>'.
        # Reply with a list of groups prefixed with 'user:', readline will
        # escape to the colon.
        local prefix
        prefix=${cur%%*([^:])}
        prefix=${prefix//\\}
        local mycur="${cur#*[:]}"
        if [[ $1 == -u ]]; then
            _allowed_groups "$mycur"
        else
            local IFS=$'\n'
            COMPREPLY=( $( compgen -g -- "$mycur" ) )
        fi
        COMPREPLY=( $( compgen -P "$prefix" -W "${COMPREPLY[@]}" ) )
    elif [[ $cur = *:* ]]; then
        # Completing group after 'user:gr<TAB>'.
        # Reply with a list of unprefixed groups since readline with split on :
        # and only replace the 'gr' part
        local mycur="${cur#*:}"
        if [[ $1 == -u ]]; then
            _allowed_groups "$mycur"
        else
            local IFS=$'\n'
            COMPREPLY=( $( compgen -g -- "$mycur" ) )
        fi
    else
        # Completing a partial 'usernam<TAB>'.
        #
        # Don't suffix with a : because readline will escape it and add a
        # slash. It's better to complete into 'chown username ' than 'chown
        # username\:'.
        if [[ $1 == -u ]]; then
            _allowed_users "$cur"
        else
            local IFS=$'\n'
            COMPREPLY=( $( compgen -u -- "$cur" ) )
        fi
    fi
}

_allowed_users()
{
    if _complete_as_root; then
        local IFS=$'\n'
        COMPREPLY=( $( compgen -u -- "${1:-$cur}" ) )
    else
        local IFS=$'\n '
        COMPREPLY=( $( compgen -W \
            "$( id -un 2>/dev/null || whoami 2>/dev/null )" -- "${1:-$cur}" ) )
    fi
}

_allowed_groups()
{
    if _complete_as_root; then
        local IFS=$'\n'
        COMPREPLY=( $( compgen -g -- "$1" ) )
    else
        local IFS=$'\n '
        COMPREPLY=( $( compgen -W \
            "$( id -Gn 2>/dev/null || groups 2>/dev/null )" -- "$1" ) )
    fi
}

# This function completes on valid shells
#
_shells()
{
    local shell rest
    while read -r shell rest; do
        [[ $shell == /* && $shell == "$cur"* ]] && COMPREPLY+=( $shell )
    done 2>/dev/null < /etc/shells
}

# This function completes on valid filesystem types
#
_fstypes()
{
    local fss

    if [[ -e /proc/filesystems ]]; then
        # Linux
        fss="$( cut -d$'\t' -f2 /proc/filesystems )
             $( awk '! /\*/ { print $NF }' /etc/filesystems 2>/dev/null )"
    else
        # Generic
        fss="$( awk '/^[ \t]*[^#]/ { print $3 }' /etc/fstab 2>/dev/null )
             $( awk '/^[ \t]*[^#]/ { print $3 }' /etc/mnttab 2>/dev/null )
             $( awk '/^[ \t]*[^#]/ { print $4 }' /etc/vfstab 2>/dev/null )
             $( awk '{ print $1 }' /etc/dfs/fstypes 2>/dev/null )
             $( [[ -d /etc/fs ]] && command ls /etc/fs )"
    fi

    [[ -n $fss ]] && COMPREPLY+=( $( compgen -W "$fss" -- "$cur" ) )
}

# Get real command.
# - arg: $1  Command
# - stdout:  Filename of command in PATH with possible symbolic links resolved.
#            Empty string if command not found.
# - return:  True (0) if command found, False (> 0) if not.
_realcommand()
{
    type -P "$1" > /dev/null && {
        if type -p realpath > /dev/null; then
            realpath "$(type -P "$1")"
        elif type -p greadlink > /dev/null; then
            greadlink -f "$(type -P "$1")"
        elif type -p readlink > /dev/null; then
            readlink -f "$(type -P "$1")"
        else
            type -P "$1"
        fi
    }
}

# This function returns the first argument, excluding options
# @param $1 chars  Characters out of $COMP_WORDBREAKS which should
#     NOT be considered word breaks. See __reassemble_comp_words_by_ref.
_get_first_arg()
{
    local i

    arg=
    for (( i=1; i < COMP_CWORD; i++ )); do
        if [[ "${COMP_WORDS[i]}" != -* ]]; then
            arg=${COMP_WORDS[i]}
            break
        fi
    done
}


# This function counts the number of args, excluding options
# @param $1 chars  Characters out of $COMP_WORDBREAKS which should
#     NOT be considered word breaks. See __reassemble_comp_words_by_ref.
_count_args()
{
    local i cword words
    __reassemble_comp_words_by_ref "$1" words cword

    args=1
    for i in "${words[@]:1:cword-1}"; do
        [[ "$i" != -* ]] && args=$(($args+1))
    done
}

# This function completes on PCI IDs
#
_pci_ids()
{
    COMPREPLY+=( $( compgen -W \
        "$( PATH="$PATH:/sbin" lspci -n | awk '{print $3}')" -- "$cur" ) )
}

# This function completes on USB IDs
#
_usb_ids()
{
    COMPREPLY+=( $( compgen -W \
        "$( PATH="$PATH:/sbin" lsusb | awk '{print $6}' )" -- "$cur" ) )
}

# CD device names
_cd_devices()
{
    COMPREPLY+=( $( compgen -f -d -X "!*/?([amrs])cd*" -- "${cur:-/dev/}" ) )
}

# DVD device names
_dvd_devices()
{
    COMPREPLY+=( $( compgen -f -d -X "!*/?(r)dvd*" -- "${cur:-/dev/}" ) )
}

# TERM environment variable values
_terms()
{
    COMPREPLY+=( $( compgen -W \
        "$( sed -ne 's/^\([^[:space:]#|]\{2,\}\)|.*/\1/p' /etc/termcap \
            2>/dev/null )" -- "$cur" ) )
    COMPREPLY+=( $( compgen -W "$( { toe -a 2>/dev/null || toe 2>/dev/null; } \
        | awk '{ print $1 }' | sort -u )" -- "$cur" ) )
}

# a little help for FreeBSD ports users
[[ $OSTYPE == *freebsd* ]] && complete -W 'index search fetch fetch-list
    extract patch configure build install reinstall deinstall clean
    clean-depends kernel buildworld' make

# This function provides simple user@host completion
#
_user_at_host()
{
    local cur prev words cword
    _init_completion -n : || return

    if [[ $cur == *@* ]]; then
        _known_hosts_real "$cur"
    else
        COMPREPLY=( $( compgen -u -- "$cur" ) )
    fi

    return 0
}
shopt -u hostcomplete && complete -F _user_at_host -o nospace talk ytalk finger

# NOTE: Using this function as a helper function is deprecated.  Use
#       `_known_hosts_real' instead.
_known_hosts()
{
    local cur prev words cword
    _init_completion -n : || return

    # NOTE: Using `_known_hosts' as a helper function and passing options
    #       to `_known_hosts' is deprecated: Use `_known_hosts_real' instead.
    local options
    [[ "$1" == -a || "$2" == -a ]] && options=-a
    [[ "$1" == -c || "$2" == -c ]] && options+=" -c"
    _known_hosts_real $options -- "$cur"
} # _known_hosts()

# Helper function for completing _known_hosts.
# This function performs host completion based on ssh's config and known_hosts
# files, as well as hostnames reported by avahi-browse if
# COMP_KNOWN_HOSTS_WITH_AVAHI is set to a non-empty value.  Also hosts from
# HOSTFILE (compgen -A hostname) are added, unless
# COMP_KNOWN_HOSTS_WITH_HOSTFILE is set to an empty value.
# Usage: _known_hosts_real [OPTIONS] CWORD
# Options:  -a             Use aliases
#           -c             Use `:' suffix
#           -F configfile  Use `configfile' for configuration settings
#           -p PREFIX      Use PREFIX
# Return: Completions, starting with CWORD, are added to COMPREPLY[]
_known_hosts_real()
{
    local configfile flag prefix
    local cur curd awkcur user suffix aliases i host
    local -a kh khd config

    local OPTIND=1
    while getopts "acF:p:" flag "$@"; do
        case $flag in
            a) aliases='yes' ;;
            c) suffix=':' ;;
            F) configfile=$OPTARG ;;
            p) prefix=$OPTARG ;;
        esac
    done
    [[ $# -lt $OPTIND ]] && echo "error: $FUNCNAME: missing mandatory argument CWORD"
    cur=${!OPTIND}; let "OPTIND += 1"
    [[ $# -ge $OPTIND ]] && echo "error: $FUNCNAME("$@"): unprocessed arguments:"\
    $(while [[ $# -ge $OPTIND ]]; do printf '%s\n' ${!OPTIND}; shift; done)

    [[ $cur == *@* ]] && user=${cur%@*}@ && cur=${cur#*@}
    kh=()

    # ssh config files
    if [[ -n $configfile ]]; then
        [[ -r $configfile ]] && config+=( "$configfile" )
    else
        for i in /etc/ssh/ssh_config ~/.ssh/config ~/.ssh2/config; do
            [[ -r $i ]] && config+=( "$i" )
        done
    fi

    # Known hosts files from configs
    if [[ ${#config[@]} -gt 0 ]]; then
        local OIFS=$IFS IFS=$'\n' j
        local -a tmpkh
        # expand paths (if present) to global and user known hosts files
        # TODO(?): try to make known hosts files with more than one consecutive
        #          spaces in their name work (watch out for ~ expansion
        #          breakage! Alioth#311595)
        tmpkh=( $( awk 'sub("^[ \t]*([Gg][Ll][Oo][Bb][Aa][Ll]|[Uu][Ss][Ee][Rr])[Kk][Nn][Oo][Ww][Nn][Hh][Oo][Ss][Tt][Ss][Ff][Ii][Ll][Ee][ \t]+", "") { print $0 }' "${config[@]}" | sort -u ) )
        IFS=$OIFS
        for i in "${tmpkh[@]}"; do
            # First deal with quoted entries...
            while [[ $i =~ ^([^\"]*)\"([^\"]*)\"(.*)$ ]]; do
                i=${BASH_REMATCH[1]}${BASH_REMATCH[3]}
                j=${BASH_REMATCH[2]}
                __expand_tilde_by_ref j # Eval/expand possible `~' or `~user'
                [[ -r $j ]] && kh+=( "$j" )
            done
            # ...and then the rest.
            for j in $i; do
                __expand_tilde_by_ref j # Eval/expand possible `~' or `~user'
                [[ -r $j ]] && kh+=( "$j" )
            done
        done
    fi

    if [[ -z $configfile ]]; then
        # Global and user known_hosts files
        for i in /etc/ssh/ssh_known_hosts /etc/ssh/ssh_known_hosts2 \
            /etc/known_hosts /etc/known_hosts2 ~/.ssh/known_hosts \
            ~/.ssh/known_hosts2; do
            [[ -r $i ]] && kh+=( "$i" )
        done
        for i in /etc/ssh2/knownhosts ~/.ssh2/hostkeys; do
            [[ -d $i ]] && khd+=( "$i"/*pub )
        done
    fi

    # If we have known_hosts files to use
    if [[ ${#kh[@]} -gt 0 || ${#khd[@]} -gt 0 ]]; then
        # Escape slashes and dots in paths for awk
        awkcur=${cur//\//\\\/}
        awkcur=${awkcur//\./\\\.}
        curd=$awkcur

        if [[ "$awkcur" == [0-9]*[.:]* ]]; then
            # Digits followed by a dot or a colon - just search for that
            awkcur="^$awkcur[.:]*"
        elif [[ "$awkcur" == [0-9]* ]]; then
            # Digits followed by no dot or colon - search for digits followed
            # by a dot or a colon
            awkcur="^$awkcur.*[.:]"
        elif [[ -z $awkcur ]]; then
            # A blank - search for a dot, a colon, or an alpha character
            awkcur="[a-z.:]"
        else
            awkcur="^$awkcur"
        fi

        if [[ ${#kh[@]} -gt 0 ]]; then
            # FS needs to look for a comma separated list
            COMPREPLY+=( $( awk 'BEGIN {FS=","}
            /^\s*[^|\#]/ {
            sub("^@[^ ]+ +", ""); \
            sub(" .*$", ""); \
            for (i=1; i<=NF; ++i) { \
            sub("^\\[", "", $i); sub("\\](:[0-9]+)?$", "", $i); \
            if ($i !~ /[*?]/ && $i ~ /'"$awkcur"'/) {print $i} \
            }}' "${kh[@]}" 2>/dev/null ) )
        fi
        if [[ ${#khd[@]} -gt 0 ]]; then
            # Needs to look for files called
            # .../.ssh2/key_22_<hostname>.pub
            # dont fork any processes, because in a cluster environment,
            # there can be hundreds of hostkeys
            for i in "${khd[@]}" ; do
                if [[ "$i" == *key_22_$curd*.pub && -r "$i" ]]; then
                    host=${i/#*key_22_/}
                    host=${host/%.pub/}
                    COMPREPLY+=( $host )
                fi
            done
        fi

        # apply suffix and prefix
        for (( i=0; i < ${#COMPREPLY[@]}; i++ )); do
            COMPREPLY[i]=$prefix$user${COMPREPLY[i]}$suffix
        done
    fi

    # append any available aliases from config files
    if [[ ${#config[@]} -gt 0 && -n "$aliases" ]]; then
        local hosts=$( sed -ne 's/^[ \t]*[Hh][Oo][Ss][Tt]\([Nn][Aa][Mm][Ee]\)\{0,1\}['"$'\t '"']\{1,\}\([^#*?]*\)\(#.*\)\{0,1\}$/\2/p' "${config[@]}" )
        COMPREPLY+=( $( compgen -P "$prefix$user" \
            -S "$suffix" -W "$hosts" -- "$cur" ) )
    fi

    # This feature is disabled because it does not scale to
    #  larger networks. See:
    # https://bugs.launchpad.net/ubuntu/+source/bash-completion/+bug/510591
    # https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=574950

    # Add hosts reported by avahi-browse, if desired and it's available.
    #if [[ ${COMP_KNOWN_HOSTS_WITH_AVAHI:-} ]] && \
        #type avahi-browse &>/dev/null; then
        # The original call to avahi-browse also had "-k", to avoid lookups
        # into avahi's services DB. We don't need the name of the service, and
        # if it contains ";", it may mistify the result. But on Gentoo (at
        # least), -k wasn't available (even if mentioned in the manpage) some
        # time ago, so...
        #COMPREPLY+=( $( compgen -P "$prefix$user" -S "$suffix" -W \
        #    "$( avahi-browse -cpr _workstation._tcp 2>/dev/null | \
        #         awk -F';' '/^=/ { print $7 }' | sort -u )" -- "$cur" ) )
    #fi

    # Add hosts reported by ruptime.
    COMPREPLY+=( $( compgen -W \
        "$( ruptime 2>/dev/null | awk '!/^ruptime:/ { print $1 }' )" \
        -- "$cur" ) )

    # Add results of normal hostname completion, unless
    # `COMP_KNOWN_HOSTS_WITH_HOSTFILE' is set to an empty value.
    if [[ -n ${COMP_KNOWN_HOSTS_WITH_HOSTFILE-1} ]]; then
        COMPREPLY+=(
            $( compgen -A hostname -P "$prefix$user" -S "$suffix" -- "$cur" ) )
    fi

    __ltrim_colon_completions "$prefix$user$cur"

    return 0
} # _known_hosts_real()
complete -F _known_hosts traceroute traceroute6 tracepath tracepath6 \
    fping fping6 telnet rsh rlogin ftp dig mtr ssh-installkeys showmount

# This meta-cd function observes the CDPATH variable, so that cd additionally
# completes on directories under those specified in CDPATH.
#
_cd()
{
    local cur prev words cword
    _init_completion || return

    local IFS=$'\n' i j k

    compopt -o filenames

    # Use standard dir completion if no CDPATH or parameter starts with /,
    # ./ or ../
    if [[ -z "${CDPATH:-}" || "$cur" == ?(.)?(.)/* ]]; then
        _filedir -d
        return 0
    fi

    local -r mark_dirs=$(_rl_enabled mark-directories && echo y)
    local -r mark_symdirs=$(_rl_enabled mark-symlinked-directories && echo y)

    # we have a CDPATH, so loop on its contents
    for i in ${CDPATH//:/$'\n'}; do
        # create an array of matched subdirs
        k="${#COMPREPLY[@]}"
        for j in $( compgen -d $i/$cur ); do
            if [[ ( $mark_symdirs && -h $j || $mark_dirs && ! -h $j ) && ! -d ${j#$i/} ]]; then
                j+="/"
            fi
            COMPREPLY[k++]=${j#$i/}
        done
    done

    _filedir -d

    if [[ ${#COMPREPLY[@]} -eq 1 ]]; then
        i=${COMPREPLY[0]}
        if [[ "$i" == "$cur" && $i != "*/" ]]; then
            COMPREPLY[0]="${i}/"
        fi
    fi

    return 0
}
if shopt -q cdable_vars; then
    complete -v -F _cd -o nospace cd
else
    complete -F _cd -o nospace cd
fi

# a wrapper method for the next one, when the offset is unknown
_command()
{
    local offset i

    # find actual offset, as position of the first non-option
    offset=1
    for (( i=1; i <= COMP_CWORD; i++ )); do
        if [[ "${COMP_WORDS[i]}" != -* ]]; then
            offset=$i
            break
        fi
    done
    _command_offset $offset
}

# A meta-command completion function for commands like sudo(8), which need to
# first complete on a command, then complete according to that command's own
# completion definition.
#
_command_offset()
{
    # rewrite current completion context before invoking
    # actual command completion

    # find new first word position, then
    # rewrite COMP_LINE and adjust COMP_POINT
    local word_offset=$1 i j
    for (( i=0; i < $word_offset; i++ )); do
        for (( j=0; j <= ${#COMP_LINE}; j++ )); do
            [[ "$COMP_LINE" == "${COMP_WORDS[i]}"* ]] && break
            COMP_LINE=${COMP_LINE:1}
            ((COMP_POINT--))
        done
        COMP_LINE=${COMP_LINE#"${COMP_WORDS[i]}"}
        ((COMP_POINT-=${#COMP_WORDS[i]}))
    done

    # shift COMP_WORDS elements and adjust COMP_CWORD
    for (( i=0; i <= COMP_CWORD - $word_offset; i++ )); do
        COMP_WORDS[i]=${COMP_WORDS[i+$word_offset]}
    done
    for (( i; i <= COMP_CWORD; i++ )); do
        unset COMP_WORDS[i]
    done
    ((COMP_CWORD -= $word_offset))

    COMPREPLY=()
    local cur
    _get_comp_words_by_ref cur

    if [[ $COMP_CWORD -eq 0 ]]; then
        local IFS=$'\n'
        compopt -o filenames
        COMPREPLY=( $( compgen -d -c -- "$cur" ) )
    else
        local cmd=${COMP_WORDS[0]} compcmd=${COMP_WORDS[0]}
        local cspec=$( complete -p $cmd 2>/dev/null )

        # If we have no completion for $cmd yet, see if we have for basename
        if [[ ! $cspec && $cmd == */* ]]; then
            cspec=$( complete -p ${cmd##*/} 2>/dev/null )
            [[ $cspec ]] && compcmd=${cmd##*/}
        fi
        # If still nothing, just load it for the basename
        if [[ ! $cspec ]]; then
            compcmd=${cmd##*/}
            _completion_loader $compcmd
            cspec=$( complete -p $compcmd 2>/dev/null )
        fi

        if [[ -n $cspec ]]; then
            if [[ ${cspec#* -F } != $cspec ]]; then
                # complete -F <function>

                # get function name
                local func=${cspec#*-F }
                func=${func%% *}

                if [[ ${#COMP_WORDS[@]} -ge 2 ]]; then
                    $func $cmd "${COMP_WORDS[${#COMP_WORDS[@]}-1]}" "${COMP_WORDS[${#COMP_WORDS[@]}-2]}"
                else
                    $func $cmd "${COMP_WORDS[${#COMP_WORDS[@]}-1]}"
                fi

                # restore initial compopts
                local opt
                while [[ $cspec == *" -o "* ]]; do
                    # FIXME: should we take "+o opt" into account?
                    cspec=${cspec#*-o }
                    opt=${cspec%% *}
                    compopt -o $opt
                    cspec=${cspec#$opt}
                done
            else
                cspec=${cspec#complete}
                cspec=${cspec%%$compcmd}
                COMPREPLY=( $( eval compgen "$cspec" -- '$cur' ) )
            fi
        elif [[ ${#COMPREPLY[@]} -eq 0 ]]; then
            # XXX will probably never happen as long as completion loader loads
            #     *something* for every command thrown at it ($cspec != empty)
            _minimal
        fi
    fi
}
complete -F _command aoss command do else eval exec ltrace nice nohup padsp \
    then time tsocks vsound xargs

_root_command()
{
    local PATH=$PATH:/sbin:/usr/sbin:/usr/local/sbin
    local root_command=$1
    _command
}
complete -F _root_command fakeroot gksu gksudo kdesudo really

# Return true if the completion should be treated as running as root
_complete_as_root()
{
    [[ $EUID -eq 0 || ${root_command:-} ]]
}

_longopt()
{
    local cur prev words cword split
    _init_completion -s || return

    case "${prev,,}" in
        --help|--usage|--version)
            return 0
            ;;
        --*dir*)
            _filedir -d
            return 0
            ;;
        --*file*|--*path*)
            _filedir
            return 0
            ;;
        --+([-a-z0-9_]))
            local argtype=$( $1 --help 2>&1 | sed -ne \
                "s|.*$prev\[\{0,1\}=[<[]\{0,1\}\([-A-Za-z0-9_]\{1,\}\).*|\1|p" )
            case ${argtype,,} in
                *dir*)
                    _filedir -d
                    return 0
                    ;;
                *file*|*path*)
                    _filedir
                    return 0
                    ;;
            esac
            ;;
    esac

    $split && return 0

    if [[ "$cur" == -* ]]; then
        COMPREPLY=( $( compgen -W "$( $1 --help 2>&1 | \
            sed -ne 's/.*\(--[-A-Za-z0-9]\{1,\}=\{0,1\}\).*/\1/p' | sort -u )" \
            -- "$cur" ) )
        [[ $COMPREPLY == *= ]] && compopt -o nospace
    elif [[ "$1" == @(mk|rm)dir ]]; then
        _filedir -d
    else
        _filedir
    fi
}
# makeinfo and texi2dvi are defined elsewhere.
complete -F _longopt a2ps awk base64 bash bc bison cat colordiff cp csplit \
    cut date df diff dir du enscript env expand fmt fold gperf \
    grep grub head indent irb ld ldd less ln ls m4 md5sum mkdir mkfifo mknod \
    mv netstat nl nm objcopy objdump od paste pr ptx readelf rm rmdir \
    sed seq sha{,1,224,256,384,512}sum shar sort split strip sum tac tail tee \
    texindex touch tr uname unexpand uniq units vdir wc who

declare -A _xspecs
_filedir_xspec()
{
    local cur prev words cword
    _init_completion || return

    _tilde "$cur" || return 0

    local IFS=$'\n' xspec=${_xspecs[${1##*/}]} tmp
    local -a toks

    toks=( $(
        compgen -d -- "$(quote_readline "$cur")" | {
        while read -r tmp; do
            printf '%s\n' $tmp
        done
        }
        ))

    # Munge xspec to contain uppercase version too
    # http://thread.gmane.org/gmane.comp.shells.bash.bugs/15294/focus=15306
    eval xspec="${xspec}"
    local matchop=!
    if [[ $xspec == !* ]]; then
        xspec=${xspec#!}
        matchop=@
    fi
    xspec="$matchop($xspec|${xspec^^})"

    toks+=( $(
        eval compgen -f -X "!$xspec" -- "\$(quote_readline "\$cur")" | {
        while read -r tmp; do
            [[ -n $tmp ]] && printf '%s\n' $tmp
        done
        }
        ))

    if [[ ${#toks[@]} -ne 0 ]]; then
        compopt -o filenames
        COMPREPLY=( "${toks[@]}" )
    fi
}

_install_xspec()
{
    local xspec=$1 cmd
    shift
    for cmd in $@; do
        _xspecs[$cmd]=$xspec
    done
    complete -F _filedir_xspec $@
}
# bzcmp, bzdiff, bz*grep, bzless, bzmore intentionally not here, see Debian: #455510
_install_xspec '!*.?(t)bz?(2)' bunzip2 bzcat pbunzip2 pbzcat lbunzip2 lbzcat
_install_xspec '!*.@(zip|[ejsw]ar|exe|pk3|wsz|zargo|xpi|s[tx][cdiw]|sx[gm]|o[dt][tspgfc]|od[bm]|oxt|epub|apk|do[ct][xm]|p[op]t[mx]|xl[st][xm])' unzip zipinfo
_install_xspec '*.Z' compress znew
# zcmp, zdiff, z*grep, zless, zmore intentionally not here, see Debian: #455510
_install_xspec '!*.@(Z|[gGd]z|t[ag]z)' gunzip zcat unpigz
_install_xspec '!*.Z' uncompress
# lzcmp, lzdiff intentionally not here, see Debian: #455510
_install_xspec '!*.@(tlz|lzma)' lzcat lzegrep lzfgrep lzgrep lzless lzmore unlzma
_install_xspec '!*.@(?(t)xz|tlz|lzma)' unxz xzcat
_install_xspec '!*.lrz' lrunzip
_install_xspec '!*.@(gif|jp?(e)g|miff|tif?(f)|pn[gm]|p[bgp]m|bmp|xpm|ico|xwd|tga|pcx)' ee
_install_xspec '!*.@(gif|jp?(e)g|tif?(f)|png|p[bgp]m|bmp|x[bp]m|rle|rgb|pcx|fits|pm|svg)' qiv
_install_xspec '!*.@(gif|jp?(e)g|tif?(f)|png|p[bgp]m|bmp|x[bp]m|rle|rgb|pcx|fits|pm|?(e)ps)' xv
_install_xspec '!*.@(@(?(e)ps|?(E)PS|pdf|PDF)?(.gz|.GZ|.bz2|.BZ2|.Z))' gv ggv kghostview
_install_xspec '!*.@(dvi|DVI)?(.@(gz|Z|bz2))' xdvi kdvi
_install_xspec '!*.dvi' dvips dviselect dvitype dvipdf advi dvipdfm dvipdfmx
_install_xspec '!*.[pf]df' acroread gpdf
_install_xspec '!*.@(pdf|fdf)?(.@(gz|xz|Z|bz2))' xpdf
_install_xspec '!*.@(?(e)ps|pdf)' kpdf
_install_xspec '!*.@(okular|@(?(e|x)ps|?(E|X)PS|[pf]df|[PF]DF|dvi|DVI|cb[rz]|CB[RZ]|djv?(u)|DJV?(U)|dvi|DVI|gif|jp?(e)g|miff|tif?(f)|pn[gm]|p[bgp]m|bmp|xpm|ico|xwd|tga|pcx|GIF|JP?(E)G|MIFF|TIF?(F)|PN[GM]|P[BGP]M|BMP|XPM|ICO|XWD|TGA|PCX|epub|EPUB|odt|ODT|fb?(2)|FB?(2)|mobi|MOBI|g3|G3|chm|CHM)?(.?(gz|GZ|bz2|BZ2)))' okular
_install_xspec '!*.pdf' epdfview
_install_xspec '!*.@(cb[rz7t]|djv?(u)|?(e)ps|pdf)' zathura
_install_xspec '!*.@(?(e)ps|pdf)' ps2pdf ps2pdf12 ps2pdf13 ps2pdf14 ps2pdfwr
_install_xspec '!*.texi*' makeinfo texi2html
_install_xspec '!*.@(?(la)tex|texi|dtx|ins|ltx|dbj)' tex latex slitex jadetex pdfjadetex pdftex pdflatex texi2dvi
_install_xspec '!*.mp3' mpg123 mpg321 madplay
_install_xspec '!*@(.@(mp?(e)g|MP?(E)G|wma|avi|AVI|asf|vob|VOB|bin|dat|divx|DIVX|vcd|ps|pes|fli|flv|FLV|fxm|FXM|viv|rm|ram|yuv|mov|MOV|qt|QT|wmv|mp[234]|MP[234]|m4[pv]|M4[PV]|mkv|MKV|og[agmvx]|OG[AGMVX]|t[ps]|T[PS]|m2t?(s)|M2T?(S)|wav|WAV|flac|FLAC|asx|ASX|mng|MNG|srt|m[eo]d|M[EO]D|s[3t]m|S[3T]M|it|IT|xm|XM)|+([0-9]).@(vdr|VDR))?(.part)' xine aaxine fbxine
_install_xspec '!*@(.@(mp?(e)g|MP?(E)G|wma|avi|AVI|asf|vob|VOB|bin|dat|divx|DIVX|vcd|ps|pes|fli|flv|FLV|fxm|FXM|viv|rm|ram|yuv|mov|MOV|qt|QT|wmv|mp[234]|MP[234]|m4[pv]|M4[PV]|mkv|MKV|og[agmvx]|OG[AGMVX]|t[ps]|T[PS]|m2t?(s)|M2T?(S)|wav|WAV|flac|FLAC|asx|ASX|mng|MNG|srt|m[eo]d|M[EO]D|s[3t]m|S[3T]M|it|IT|xm|XM|iso|ISO)|+([0-9]).@(vdr|VDR))?(.part)' kaffeine dragon
_install_xspec '!*.@(avi|asf|wmv)' aviplay
_install_xspec '!*.@(rm?(j)|ra?(m)|smi?(l))' realplay
_install_xspec '!*.@(mpg|mpeg|avi|mov|qt)' xanim
_install_xspec '!*.@(og[ag]|m3u|flac|spx)' ogg123
_install_xspec '!*.@(mp3|og[ag]|pls|m3u)' gqmpeg freeamp
_install_xspec '!*.fig' xfig
_install_xspec '!*.@(mid?(i)|cmf)' playmidi
_install_xspec '!*.@(mid?(i)|rmi|rcp|[gr]36|g18|mod|xm|it|x3m|s[3t]m|kar)' timidity
_install_xspec '!*.@(669|abc|am[fs]|d[bs]m|dmf|far|it|mdl|m[eo]d|mid?(i)|mt[2m]|okta|p[st]m|s[3t]m|ult|umx|wav|xm)' modplugplay modplug123
_install_xspec '*.@(o|so|so.!(conf|*/*)|a|[rs]pm|gif|jp?(e)g|mp3|mp?(e)g|avi|asf|ogg|class)' vi vim gvim rvim view rview rgvim rgview gview emacs xemacs sxemacs kate kwrite
_install_xspec '!*.@(zip|z|gz|tgz)' bzme
# konqueror not here on purpose, it's more than a web/html browser
_install_xspec '!*.@(?([xX]|[sS])[hH][tT][mM]?([lL]))' netscape mozilla lynx galeon dillo elinks amaya firefox mozilla-firefox iceweasel google-chrome chromium-browser epiphany
_install_xspec '!*.@(sxw|stw|sxg|sgl|doc?([mx])|dot?([mx])|rtf|txt|htm|html|?(f)odt|ott|odm)' oowriter
_install_xspec '!*.@(sxi|sti|pps?(x)|ppt?([mx])|pot?([mx])|?(f)odp|otp)' ooimpress
_install_xspec '!*.@(sxc|stc|xls?([bmx])|xlw|xlt?([mx])|[ct]sv|?(f)ods|ots)' oocalc
_install_xspec '!*.@(sxd|std|sda|sdd|?(f)odg|otg)' oodraw
_install_xspec '!*.@(sxm|smf|mml|odf)' oomath
_install_xspec '!*.odb' oobase
_install_xspec '!*.[rs]pm' rpm2cpio
_install_xspec '!*.aux' bibtex
_install_xspec '!*.po' poedit gtranslator kbabel lokalize
_install_xspec '!*.@([Pp][Rr][Gg]|[Cc][Ll][Pp])' harbour gharbour hbpp
_install_xspec '!*.[Hh][Rr][Bb]' hbrun
_install_xspec '!*.ly' lilypond ly2dvi
_install_xspec '!*.@(dif?(f)|?(d)patch)?(.@([gx]z|bz2|lzma))' cdiff
_install_xspec '!@(*.@(ks|jks|jceks|p12|pfx|bks|ubr|gkr|cer|crt|cert|p7b|pkipath|pem|p10|csr|crl)|cacerts)' portecle
_install_xspec '!*.@(mp[234c]|og[ag]|@(fl|a)ac|m4[abp]|spx|tta|w?(a)v|wma|aif?(f)|asf|ape)' kid3 kid3-qt
_install_xspec '!*.py' pyflakes
unset -f _install_xspec

# Minimal completion to use as fallback in _completion_loader.
_minimal()
{
    local cur prev words cword split
    _init_completion -s || return
    $split && return
    _filedir
}
# Complete the empty string to allow completion of '>', '>>', and '<'
# http://lists.gnu.org/archive/html/bug-bash/2012-01/msg00045.html
complete -F _minimal ''


# set up dynamic completion loading
_completion_loader()
{
    local compfile=./completions
    [[ $BASH_SOURCE == */* ]] && compfile="${BASH_SOURCE%/*}/completions"
    compfile+="/${1##*/}"

    # Avoid trying to source dirs; https://bugzilla.redhat.com/903540
    [[ -f "$compfile" ]] && . "$compfile" &>/dev/null && return 124

    # Need to define *something*, otherwise there will be no completion at all.
    complete -F _minimal "$1" && return 124
} &&
complete -D -F _completion_loader

# Function for loading and calling functions from dynamically loaded
# completion files that may not have been sourced yet.
# @param $1 completion file to load function from in case it is missing
# @param $2... function and its arguments
_xfunc()
{
    set -- "$@"
    local srcfile=$1
    shift
    declare -F $1 &>/dev/null || {
        local compdir=./completions
        [[ $BASH_SOURCE == */* ]] && compdir="${BASH_SOURCE%/*}/completions"
        . "$compdir/$srcfile"
    }
    "$@"
}

# source compat completion directory definitions
if [[ -d $BASH_COMPLETION_COMPAT_DIR && -r $BASH_COMPLETION_COMPAT_DIR && \
    -x $BASH_COMPLETION_COMPAT_DIR ]]; then
    for i in $(LC_ALL=C command ls "$BASH_COMPLETION_COMPAT_DIR"); do
        i=$BASH_COMPLETION_COMPAT_DIR/$i
        [[ ${i##*/} != @($_backup_glob|Makefile*|$_blacklist_glob) \
            && -f $i && -r $i ]] && . "$i"
    done
fi
unset i _blacklist_glob

# source user completion file
[[ ${BASH_SOURCE[0]} != ~/.bash_completion && -r ~/.bash_completion ]] \
    && . ~/.bash_completion
unset -f have
unset have

set $BASH_COMPLETION_ORIGINAL_V_VALUE
unset BASH_COMPLETION_ORIGINAL_V_VALUE

# ex: ts=4 sw=4 et filetype=sh
