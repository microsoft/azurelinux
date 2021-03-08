#!/bin/bash
# grub2 and grub2-pc package are required
# for building legacy core images.
# Once fix running postinstall script
# after installLegacyBootloader
# uncomment below two commands

echo "Running post install cleanup packages."
# tdnf remove grub2 -y
echo "Completed post install cleanup packages."