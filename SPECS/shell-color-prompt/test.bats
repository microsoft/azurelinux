setup_file() {
    [ -d bats-support ] || git clone https://github.com/bats-core/bats-support.git
    [ -d bats-assert ] || git clone https://github.com/bats-core/bats-assert.git
}

setup() {
    load 'bats-support/load'
    load 'bats-assert/load'
    # get the containing directory of this file
    bash_prompt_color_force=1
    bash_prompt_color_test=1
    container=
    unset DESKTOP_SESSION
    BASH_COLOR_PROMPT_FILE=${BASH_COLOR_PROMPT_DIR:-/etc/profile.d}/bash-color-prompt.sh

    # expected output
    COL=32
    HOST=$(hostname -s)
    DIR="$( cd "$( dirname "$BATS_TEST_FILENAME" )" >/dev/null 2>&1 && pwd )"
    PRETTY_DIR="$(echo $DIR | sed -e s\%$HOME\%~\%)"
    PROMPTCHAR='$'
    case $USER in
        root)
            COL=35
            PROMPTCHAR='#'
            NOHOST="[${COL}m$USER@$HOST[0m:"
            ;;
        mockbuild)
            NOHOST="[${COL}m$USER@$HOST[0m:"
            ;;
    esac
}

get_prompt() {
    echo -e "${PS1@P}"
}

@test "can source bash-color-prompt.sh" {
    source $BASH_COLOR_PROMPT_FILE
}

@test "print prompt" {
    source $BASH_COLOR_PROMPT_FILE
    get_prompt
}

@test "default" {
    source $BASH_COLOR_PROMPT_FILE
    run get_prompt
    assert_output "[0m[${COL}m$USER@$HOST[0m:[${COL}m$PRETTY_DIR[0m$PROMPTCHAR "
}

@test "default gnome" {
    DESKTOP_SESSION="gnome"
    source $BASH_COLOR_PROMPT_FILE
    run get_prompt
    assert_output "[0m[1m[${COL}m$USER@$HOST[0m:[1m[${COL}m$PRETTY_DIR[0m$PROMPTCHAR "
}

@test "highlight" {
    source $BASH_COLOR_PROMPT_FILE
    prompt_highlight
    run get_prompt
    assert_output "[0m[1m[${COL}m$USER@$HOST[0m:[1m[${COL}m$PRETTY_DIR[0m$PROMPTCHAR "
}

@test "no highlight" {
    DESKTOP_SESSION="gnome"
    source $BASH_COLOR_PROMPT_FILE
    prompt_no_highlight
    run get_prompt
    assert_output "[0m[${COL}m$USER@$HOST[0m:[${COL}m$PRETTY_DIR[0m$PROMPTCHAR "
}

@test "container" {
    container=1
    source $BASH_COLOR_PROMPT_FILE
    run get_prompt
    assert_output "[0m[${COL}m⬢ $USER@$HOST[0m:[${COL}m$PRETTY_DIR[0m$PROMPTCHAR "
}

@test "no userhost" {
    source $BASH_COLOR_PROMPT_FILE
    prompt_container_host $USER
    run get_prompt
    assert_output "[0m$NOHOST[${COL}m$PRETTY_DIR[0m$PROMPTCHAR "
}

@test "host" {
    source $BASH_COLOR_PROMPT_FILE
    prompt_container_host $USER
    run get_prompt
    assert_output "[0m$NOHOST[${COL}m$PRETTY_DIR[0m$PROMPTCHAR "
}

@test "container host" {
    source $BASH_COLOR_PROMPT_FILE
    container=1
    prompt_container_host $USER
    run get_prompt
    assert_output "[0m[${COL}m⬢ $PROMPT_USERHOST[0m:[${COL}m$PRETTY_DIR[0m$PROMPTCHAR "
}

@test "git" {
    source $BASH_COLOR_PROMPT_FILE
    PROMPT_GIT_BRANCH=main
    prompt_git_color 35
    run get_prompt
    assert_output "[0m[${COL}m$USER@$HOST[0m:[${COL}m$PRETTY_DIR[0m:[${COL}m[35mmain[0m$PROMPTCHAR "
}

@test "plain" {
    source $BASH_COLOR_PROMPT_FILE
    prompt_no_color
    run get_prompt
    assert_output "[0m$USER@$HOST[0m:$PRETTY_DIR[0m$PROMPTCHAR "
}
