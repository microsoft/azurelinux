set -eu
export LANG=C.utf-8

taskid=$(echo "$1" | sed -E 's/.*=|^([0-9]+)/\1/')
filter='.*-debugsource-.*\.(x86_64|aarch64)\.rpm'

download_stdout=$(koji download-task $taskid --filter "$filter" | tee /dev/stderr)
files=$(echo "$download_stdout" | grep -E '^Downloading ' | sed -E 's/.*\s+(\S+)/\1/' | sort)

for file in $files; do
  nvra=${file/.rpm}
  snvra=${nvra/-debugsource}
  version=$(echo $nvra | sed -E -e 's|.*-([^-]+)-[^-]+|\1|' -e 's|~||')
  arch=$(echo $nvra | sed -E 's|.*\.([^.]+)|\1|')
  rpm2cpio $file | cpio -idmv ./usr/src/debug/${snvra}/build/{debug,optimized}/jit_stencils-${arch}-redhat-linux-gnu.h
  for build in debug optimized; do
    mv -v ./usr/src/debug/${snvra}/build/${build}/jit_stencils-${arch}-redhat-linux-gnu.h Python-${version}-${arch}-${build}-jit_stencils.h > /dev/stderr
    echo Python-${version}-${arch}-${build}-jit_stencils.h
  done
  rmdir ./usr/src/debug/${snvra}{/build{/{debug,optimized},},} || :
  rm -v $file > /dev/stderr
done
rmdir ./usr{/src{/debug,},} || :
