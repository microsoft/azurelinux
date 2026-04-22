#!/bin/bash -eu

# Webpack needs more than the default 4GB RAM
export NODE_OPTIONS="${NODE_OPTIONS:-} --max_old_space_size=6144"

# Build the frontend
yarn run build

# Build the bundled plugins
mkdir plugins-bundled/external
yarn run plugins:build-bundled
for plugin in plugins-bundled/internal/input-datasource; do
  mv $plugin $plugin.tmp
  mv $plugin.tmp/dist $plugin
  rm -rf $plugin.tmp
done
rm plugins-bundled/README.md plugins-bundled/.gitignore plugins-bundled/external.json

# Fix permissions (webpack sometimes outputs files with mode = 666 due to reasons unknown (race condition/umask issue afaics))
chmod -R g-w,o-w public/build plugins-bundled
