# bash_completion for conda.
#
# This was initially based on completion support for `fish`, but later extended
# complete options for subcommands and files/dirs/paths as appropriate.
#
# Dynamic option lookup uses a cache that persists for the duration of the shell.
# Updates to the conda command options are relatively rare, but there is a small chance
# that this cache will hold incorrect/incomplete values. A restart of your shell will
# fix this.

# If this completion file is 'installed' under
#
#   /etc/bash_completion.d/,
#   /usr/share/bash-completion/completions/, or
#   ~/.local/share/bash-completion/completions/,
#
# rather than being managed via the `conda shell.bash hook`, then this file may
# be sourced before conda is setup.  To support this we allow for a potential
# late initialization of the CONDA_ROOT and CONDA_SOURCE environment
# variables.

# The extglob option is set by the bash_completion library anyway,
# Setting it here to work around some rare edge cases.
shopt -s extglob

function __comp_conda_ensure_root() {
    if [[ -z "${CONDA_SOURCE-}" && -n "${CONDA_EXE-}" ]] ; then
        if [[ -n "${_CE_CONDA-}" && -n "${WINDIR-}" ]]; then
            CONDA_ROOT=$(\dirname "${CONDA_EXE}")
        else
            CONDA_ROOT=$(\dirname "${CONDA_EXE}")
            CONDA_ROOT=$(\dirname "${CONDA_ROOT}")
        fi
        \local script="
        :    from __future__ import print_function
        :    import os
        :    import conda
        :    print(os.path.dirname(conda.__file__))
        "
        script="${script//        :    /}"
        # don't assume an active base environment
        CONDA_SOURCE=$(conda activate base; python -c "$script")
    fi
}

function __comp_conda_commands () {
    # default core commands
    echo clean config create help info init install list package
    echo remove uninstall run search update upgrade

    # implied by conda shell function
    echo activate deactivate

    # check commands from full anaconda install
    for f in "$CONDA_SOURCE"/cli/main_*.py
    do
        # skip pip -- not a sub-command
        [[ "$f" == */main_pip.py ]] && continue
        if [[ "$f" =~ .*_([a-z]+)\.py$ ]]; then
            echo "${BASH_REMATCH[1]}"
        fi
    done

    # check extra pluggins
    for f in "$CONDA_ROOT"/bin/conda-*
    do
        if [[ -x "$f" && ! -d "$f" ]]
        then
            if [[ "$f" =~ .*/conda-(.*) ]]; then
                echo "${BASH_REMATCH[1]}"
            fi
        fi
    done
}

function __comp_conda_env_commands() {
    for f in "$CONDA_SOURCE"/../conda_env/cli/main_*.py
    do
        [[ "$f" == */main_vars.py ]] && continue
        if [[ "$f" =~ .*_([a-z]+)\.py$ ]]; then
            echo "${BASH_REMATCH[1]}"
        fi
    done
}

function __comp_conda_envs() {
    \local script="
    :    from __future__ import print_function
    :    import json, os, sys
    :    from os.path import isdir, join
    :    print('\n'.join(
    :       d for ed in json.load(sys.stdin)['envs_dirs'] if isdir(ed)
    :       for d in os.listdir(ed) if isdir(join(ed, d)))
    :    )
    "
    script="${script//    :    /}"
    conda config --json --show envs_dirs | $CONDA_PYTHON_EXE -c "$script"
}

function __comp_conda_packages() {
    conda list | awk 'NR > 3 {print $1}'
}

function __comp_conda_cmds_str() {
    # get a list of commands, skipping options
    \local cmd
    \local -a cmds
    for cmd in "$@"; do
        case "$cmd" in
            -*) continue ;;
            *) cmds+=("$cmd") ;;
        esac
    done
    echo "${cmds[@]}"
}

# helper for debugging issues with the cache
function __comp_conda_cache_dump() {
    for k in "${!__comp_conda_cache[@]}"; do
        printf "%s:\n" "$k"
        for w in ${__comp_conda_cache[$k]}; do
            printf "\t%s\n" "$w"
        done
    done
}

function __comp_conda_option_lookup() {
    \local word_list cmd_str cmd_key
    cmd_str=$1

    # make a key to look up the cached result of the command help
    # (We should be able to just use $cmd_str, since spaces in an array key are fine,
    # but this produces an error with an empty cache. I'm not sure why though)
    cmd_key=${cmd_str// /_}

    if [[ -z "${__comp_conda_cache[$cmd_key]}" ]]; then
        # parse the output of command help to get completions
        word_list=$($cmd_str --help 2>&1 | _parse_help -)
        if [[ ${PIPESTATUS[0]} -eq 0 && -n $word_list ]]; then
            __comp_conda_cache[$cmd_key]=$word_list
        else
            # something went wrong, so abort completion attempt
            return 1
        fi
    else
        word_list=${__comp_conda_cache[$cmd_key]}
    fi
    echo "$word_list"
}

# cache conda subcommand help lookups for the duration of the shell
unset __comp_conda_cache
declare -A __comp_conda_cache

# If conda has not been fully setup/activated yet, some of the above functions may fail
# and print error messages. This is not helpful during normal usage, so we discard all
# error output by default.
__comp_conda_ensure_root 2>/dev/null || :

_comp_conda()
{
    # shellcheck disable=SC2034
    \local cur prev words cword
    _init_completion || return

    __comp_conda_ensure_root 2>/dev/null

    \local word_list cmd_str
    if [[ $cur == -* ]]; then
        # get the current list of commands as a string sans options
        cmd_str=$(__comp_conda_cmds_str "${words[@]}")
        word_list=$(__comp_conda_option_lookup "$cmd_str")
    else
        case "$prev" in
            conda)
                word_list=$(__comp_conda_commands 2>/dev/null)
                ;;
            env)
                word_list=$(__comp_conda_env_commands 2>/dev/null)
                ;;
            activate)
                if [[ $cur == */* ]]
                then
                    _filedir -d  # environment directories
                else
                    word_list=$(__comp_conda_envs 2>/dev/null)
                fi
                ;;
            remove|uninstall|upgrade|update)
                word_list=$(__comp_conda_packages 2>/dev/null)
                ;;
            --name|--clone)
                word_list=$(__comp_conda_envs 2>/dev/null)
                ;;
            --*-file|--file|--which|convert)
                _filedir                        # filenames
                ;;
            --*-dir|--*-folder|--subdir|--prefix|--cwd|index)
                _filedir -d                     # directories
                ;;
            verify|debug)
                _filedir 'tar.bz2'              # package paths and directories
                ;;
            build)
                _filedir 'tar.bz2'              # package paths and directories
                word_list='purge purge-all'     # special keywords
                ;;
        esac
    fi
    if [[ -n $word_list ]]; then
        # append completion suggestions to COMPREPLY
        mapfile -t -O "${#COMPREPLY[@]}" COMPREPLY < \
            <(compgen -W "$word_list" -- "$cur")
    fi
} &&
complete -F _comp_conda conda

# vim: ft=sh
