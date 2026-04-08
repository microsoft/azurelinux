#!/bin/bash

# The Fedora WSL out of box experience script.
#
# This command runs the first time the user opens an interactive shell if
# `cloud-init-main` is not enabled.
#
# A non-zero exit code indicates to WSL that setup failed.

set -ueo pipefail

DEFAULT_USER_ID=1000

# When `cloud-init-main` is enabled it might take care of user creation and other bits, depending on its
# configuration contained within the WSL image; or the WSL configuration as provided by the host.
if systemctl is-enabled cloud-init-main.service > /dev/null ; then
  echo 'cloud-init-main is enabled, skipping user account creation. Waiting for cloud-init to finish.'

  # We need to run cloud-init in a sub-shell that disables errexit so we can inspect its error code
  # Without the script exiting.
  (set +e cloud-init status --wait > /dev/null 2>&1)

  cloud_status=$?

  # We only exit unsuccesfully on a cloud-init exit status of 1. This means an unrecoverable error,
  # and the system might not be usable. Any other exit status (0 for success, or 2 for warning) can
  # be ignored and happens commonly, for example when there is a default configuration but the fallback
  # data source was used.
  if [ "${cloud_status}" -eq 1 ]; then
    echo 'cloud-init failed unrecoverably. Failed to provision system.'
    cloud-init status --long
    exit 1
  fi

  exit 0
fi

echo 'Please create a default user account. The username does not need to match your Windows username.'
echo 'For more information visit: https://aka.ms/wslusers'

if getent passwd $DEFAULT_USER_ID > /dev/null ; then
  echo 'User account already exists, skipping creation'
  exit 0
fi

# Prompt from the username
read -r -p 'Enter new UNIX username: ' username

# Create the user
/usr/sbin/useradd -m -G wheel --uid $DEFAULT_USER_ID "$username"

cat > /etc/sudoers.d/wsluser << EOF
# Ensure the WSL initial user can use sudo without a password.
#
# Since the user is in the wheel group, this file can be removed
# if you wish to require a password for sudo. Be sure to set a
# user password before doing so with 'sudo passwd $username'!
$username ALL=(ALL) NOPASSWD: ALL
EOF

echo 'Your user has been created, is included in the wheel group, and can use sudo without a password.'
echo "To set a password for your user, run 'sudo passwd $username'"
