if [ "$SSH_AUTH_SOCK" = "" ]; then
SSH_AUTH_SOCK="$XDG_RUNTIME_DIR/ssh-agent.socket"
export SSH_AUTH_SOCK
fi
