# Move the SSH host keys off the read-only /etc directory, so that sshd can run.
SSH_VAR_DIR="/var/etc/ssh/"
mkdir -p "$SSH_VAR_DIR"

cat << EOF >> /etc/ssh/sshd_config

HostKey $SSH_VAR_DIR/ssh_host_rsa_key
HostKey $SSH_VAR_DIR/ssh_host_ecdsa_key
HostKey $SSH_VAR_DIR/ssh_host_ed25519_key
EOF
