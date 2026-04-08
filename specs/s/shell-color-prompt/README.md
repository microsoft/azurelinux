# Simple colored bash prompt

Defined in `/etc/profile.d/bash-color-prompt.sh`

(The latest version of this file lives at:
<https://src.fedoraproject.org/rpms/shell-color-prompt>)

The prompt color theme can be customized simply with
the `prompt_color` function, and optionally `prompt_dir_color`.
`prompt_highlight` affects the userhost and directory parts
of the prompt, but not their separator (`prompt_separator`).

For example `prompt_color '33;44'` gives yellow on a blue background.
`prompt_highlight '1;7'` gives bold inverse-video

The `prompt_dir_color` function similarly changes the color of
the working directory, which otherwise defaults to the `prompt_color` setting.

Since 0.6 coloring is inherited from the left:
   PROMPT_HIGHLIGHT -> PROMPT_COLOR -> (PROMPT_SEPARATOR_COLOR) ->
   PROMPT_DIR_COLOR -> (PROMPT_SEPARATOR_COLOR) -> PROMPT_GIT_COLOR

Note `prompt_separator_color` is specific to the separators
between user-host and directory (and optionally git-branch if setup by user).

bash-color-prompt should not use any subprocesses in its default configuration.

## Coloring Examples

```shell
$ prompt_color 0 # disable colors/attribs
$ prompt_color 1 # bold prompt
$ prompt_color 2 # dim prompt
$ prompt_color 4 # underline prompt
$ prompt_color '2;7' # dim reverse video
$ prompt_color '42' # green background
$ prompt_color '53' # overline separator
$ prompt_color '1;33;44' # bold yellow on blue
$ prompt_color '43;30' # black on yellow
$ prompt_color '1;32' # bold green
```

See <https://en.wikipedia.org/wiki/ANSI_escape_code#SGR> for ANSI code details.

## Shell Color Prompt configuration functions

Although for basic configuration setting the aforementioned environment
variables is fine and continues to work dynamically, in the long term
and for a more consistent experience the functions below are recommended
and should behave better. (However note that at least until version 1.0
these functions are still subject to change, though we will try to avoid
breakage.)

You can see the definitions in `/etc/profile.d/bash-color-prompt.sh`.

Example usage (in `~/.bashrc`):
```
# this should source bash-color-prompt.sh
source /etc/bashrc

prompt_os_color 107
prompt_highlight 1\;7
prompt_dir_color 33
prompt_container $USER
prompt_git_color 35
```

Descriptions of the available functions:

### `prompt_highlight()`
_(since 0.5)_

Sets `PROMPT_HIGHLIGHT` to bold or the specified "highlighting".
```
$ prompt_highlighting 2
```

### `prompt_color()`
_(since 0.5)_

Sets `PROMPT_COLOR` to the default color for user or root or
the specified color code(s):
```
$ prompt_color 33
```

### `prompt_default_highlight()`
_(since 0.5)_

Sets `PROMPT_HIGHLIGHT` bold *only* for GNOME or specified "highlighting".

### `prompt_separator_color()`
(since 0.6)

Sets `PROMPT_SEPARATOR_COLOR`.

### `prompt_dir_color()`
_(since 0.5)_

Sets `PROMPT_DIR_COLOR` or unsets if no argument.
```
$ prompt_dir_color 44
```

### `prompt_default_color()`
_(since 0.5)_

Sets up default coloring (theme)

Specifically it runs `prompt_color`, `prompt_default_highlight`,
`prompt_separator_color`, and unsets `PROMPT_DIR_COLOR`.

### `prompt_default_format()`
_(since 0.5)_

Sets default format strings for `PROMPT_USERHOST`, `PROMPT_SEPARATOR`,
`PROMPT_DIRECTORY`, and empty `PROMPT_START` & `PROMPT_END`.

### `prompt_default()`
_(since 0.3)_

Runs `prompt_default_color` and `prompt_default_format`.

### `prompt_os_color()`
_(since 0.5)_

Sets `PROMPT_COLOR` to `ANSI_COLOR` from `/etc/os-release`.

### `prompt_separator()`
(since 0.6)

Sets `PROMPT_SEPARATOR`

### `prompt_host_os()`
(since 0.6)

Sets `PROMPT_USERHOST` to try to identify host OS and version.

### `prompt_no_userhost()`
(since 0.6)

Unsets `PROMPT_USERHOST`.

### `prompt_container()`
_(since 0.5)_

Sets `PROMPT_CONTAINER` if `$container` is non-empty.

### `prompt_container_host()`
(since 0.6)

Runs `prompt_container` and `prompt_host_os` if `$container` set,
otherwise `prompt_no_userhost` for default `HOSTNAME` and `USER`.

### `prompt_git_color()`
(since 0.6)

Sets `PROMPT_GIT_COLOR`.

### `prompt_no_color()`
_(since 0.5)_

Unsets `PROMPT_COLOR`, `PROMPT_DIR_COLOR`, and `PROMPT_GIT_COLOR`.

### `prompt_no_highlight()`
_(since 0.5)_

Unsets `PROMPT_HIGHLIGHT`.

### `prompt_plain()`
_(since 0.5)_

Runs `prompt_no_color` and `prompt_no_highlight`.

### `prompt_traditional_format()`
_(since 0.5)_

Sets the old Red Hat prompt format.

### `prompt_traditional()`
_(since 0.3)_

Runs `prompt_plain` and `prompt_traditional_format`.

### `prompt_reset_traditional_ps1()`
_(since 0.5)_

Completely resets `PS1` to the old Red Hat prompt.

To restore bash-color-prompt PS1 one then needs to run `prompt_setup_color_ps1`.

### `prompt_setup_color_ps1()`
(since 0.5)

This resets `PS1` to the default bash-color-prompt.

### `prompt_default_setup()`
(since 0.6)

Sets up default bash-color-prompt settings without any terminal checks.

### `prompt_default_setup_checked()`
(since 0.6)

Activates bash-color-prompt if enabled for terminal in Fedora.

This is run by default in `/etc/profile.d/bash-color-prompt.sh` if not disabled.

It first checks if `TERM` ends in "color" or is "linux" or
since 0.7 whether `COLORTERM` is set.

### `set_ansi()`
(since 0.6.2)

User convenience: for usage see the exit code display example below.

Note this uses a subprocess.

## Background details on the environment variables
***Note their direct use is being deprecated and should not be relied on long-term***
As far as possible use the above accessor functions.

bash-color-prompt's PS1 has the following general structure:
`[PROMPT_START]^PROMPT_USERHOST PROMPT_SEPARATOR PROMPT_DIRECTORY [PROMPT_GIT_BRANCH] ^[PROMPT_END]^`
(`^` means color reset).

### `PROMPT_START` (optional)
Displayed at the start of the prompt.

### `PROMPT_HIGHLIGHT`
Prepended before `PROMPT_COLOR` after `PROMPT_START` .

eg `PROMPT_HIGHLIGHT=1` makes prompt bold
or `PROMPT_HIGHLIGHT=7` inverts prompt coloring

### `PROMPT_USERHOST`
Default: `PROMPT_USERHOST='\u@\h'`

Color defaults to `PROMPT_COLOR`.

See the PROMPTING section of `man bash` or
*Controlling the Prompt* in `info bash` for
the available backslash-escaped special characters.

### `PROMPT_SEPARATOR`
Default: `PROMPT_SEPARATOR=':'`

eg you can change it to `'\n'` or `' \t\n'`

Color is overriden by default by `PROMPT_SEPARATOR_COLOR`.

### `PROMPT_DIRECTORY`
Default: `PROMPT_DIRECTORY='\w'`

eg can be changed to `'\W'`

Defaults to `PROMPT_DIR_COLOR` if set otherwise `PROMPT_COLOR`.

### `PROMPT_END`
Displayed at the end of the prompt (before `\$`).

## More examples

### Traditional Red Hat prompt
```
PROMPT_START='['
PROMPT_END=']'
PROMPT_SEPARATOR=' '
PROMPT_DIRECTORY='\W'
PROMPT_COLOR='0'
```

Equivalent to `prompt_traditional`

### Multiline prompt example
```
PROMPT_START='\t\n'
PROMPT_COLOR='30;43'
PROMPT_DIR_COLOR='44'
PROMPT_SEPARATOR='\n'
```
You can also set `PS0='\t'` say to timestamp the start of commands.

### Git branch integration example
```
function prompt_command {
    ref=$(/usr/bin/git rev-parse --abbrev-ref HEAD 2> /dev/null)
    PROMPT_GIT_BRANCH=${ref:+:$ref}
}
PROMPT_COMMAND=prompt_command
```
(It is considered better Bash practice to use an array for PROMPT_COMMAND.)

### Terminal title
Using bash `PROMPT_COMMAND` one can also set the terminal title with:
```
echo -n -e "\e]0;${PROMPT_USERHOST@P}${PROMPT_USERHOST:+:}${PROMPT_DIRECTORY}"
```

### Container support
See `prompt_container` and `prompt_container_host` above.

Basic container support can be setup with say:
```
PROMPT_CONTAINER='⬢'
```

### Show exit code for error in red
```
PROMPT_END="$(set_ansi 31)"'${?#0}'"$(set_ansi 0)"
```

## Sourcing
Set `bash_color_prompt_force`
(before sourcing `/etc/bashrc` or `bash-color-prompt.sh` directly)
to turn on bash-color-prompt unconditionally (for an interactive bash shell),
otherwise by default it is only setup for a bash shell
if PS1 is the fedora or bash default *and*
either `$TERM` ends in "color" (or is "linux")
or since 0.7 if `COLORTERM` is set.


For example:
```shellsession
if [ -t 0 ]; then
bash_color_prompt_force=1
source /etc/profile.d/bash-color-prompt.sh
fi
```
can be added to `~/.bashrc` to turn on bash-color-prompt "everywhere".

(Before 0.7 the variable was called `bash_prompt_color_force`.)

## Disabling
Set the `bash_color_prompt_disable` variable non-empty in `.bashrc` before
sourcing `/etc/profile.d/*.sh` to prevent setting up bash-color-prompt
(ie before sourcing `/etc/bashrc`).
(Before 0.7 this variable was called `bash_prompt_color_disable`.)

Since 0.7, the `NO_COLOR` environment variable (<https://no-color.org/>)
is also respected, and results in a default monochrome prompt.
One can set `BASH_PROMPT_USE_COLOR` to override this.

## Contribute
Please open issues against
[shell-color-prompt](https://src.fedoraproject.org/rpms/shell-color-prompt)
in bugzilla.

shell-color-prompt is distributed under the GPL license version 2 or later.
