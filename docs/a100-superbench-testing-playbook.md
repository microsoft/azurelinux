# Running SuperBench on an A100 VM with locally-built AZL4 GPU-stack RPMs

Manual playbook for smoke-testing the GPU/container-toolkit stack built in this
repo (`nvidia-open`, `nvidia-driver`, `nvidia-persistenced`, `gdrcopy`,
`nvidia-container-toolkit`, `libnvidia-container`, `nvidia-fabric-manager`)
against SuperBench on a real A100 VM. This bypasses the `azlinux-ai-ml` ADO
pipelines, which are currently AZL 3.0-only.

## 1. Provision the VM

- SKU: `Standard_NC24ads_A100_v4` (single/few A100, **no NVSwitch**) or
  `Standard_NC80adis_H100_v5` (2x PCIe H100, **no NVSwitch**) or
  `Standard_ND96asr_v4` / `Standard_ND96amsr_A100_v4` (8x A100, **NVSwitch**).
- Image: official Azure Linux 4.0 marketplace image.
- Fabric Manager (see step 4) is only relevant for the NVSwitch-equipped SKUs.

## 2. Copy the built RPMs onto the VM and expose them as a repo

```bash
# From this repo, on your build machine:
scp -r base/out/rpms/rpm-base base/out/rpms/rpm-sdk azureuser@<vm>:/tmp/azl-rpms/

# On the VM:
sudo dnf install -y createrepo_c
sudo install -d /opt/local-repo
sudo find /tmp/azl-rpms -type f -name '*.rpm' \
  -exec cp -t /opt/local-repo {} +
sudo createrepo_c /opt/local-repo
sudo tee /etc/yum.repos.d/local-gpu-stack.repo <<'EOF'
[local-gpu-stack]
name=local-rpm
baseurl=file:///opt/local-repo
enabled=1
gpgcheck=0
EOF
```

## 3. ⚠️ Install the matching kernel first, then reboot

`kmod-nvidia-open` / `kmod-gdrcopy` are kernel subpackages
(`Requires: kernel-core-uname-r = <exact KVERREL>`), not generic DKMS modules.
They only load against the *exact* kernel build produced alongside them
(e.g. `6.18.39-1.10.azl4`) — not whatever stock kernel ships in the base image.

```bash
sudo dnf install -y kernel kernel-core kernel-modules kernel-modules-core \
    kernel-modules-extra kernel-devel kernel-tools kernel-tools-libs \
    mlnx-ofa_kernel mlnx-ofa_kernel-modules
sudo reboot
uname -r   # confirm it matches the kernel build's KVERREL, e.g. 6.18.39-1.10.azl4.x86_64
```

### Install the DOCA/MLNX OFED userspace stack

This repository builds the NVIDIA DOCA/MLNX OFED 26.04 components as separate
RPMs; there is no single `doca-ofed` metapackage. Install the verbs and RDMA
libraries, diagnostics, UCX transports, and benchmark tools from the local
repository. Do not mix these packages with the community `rdma-core`, `ucx`,
or `perftest` RPMs that the `-ofed` packages replace.

```bash
sudo dnf install -y \
  rdma-core-ofed rdma-core-ofed-devel \
  libibverbs-ofed libibverbs-utils-ofed libibumad-ofed \
  librdmacm-ofed librdmacm-utils-ofed infiniband-diags-ofed \
  ucx-ofed ucx-ofed-devel ucx-ofed-ib ucx-ofed-ib-mlx5 \
  ucx-ofed-rdmacm \
  perftest-ofed mlnx-tools-ofed ofed-scripts

sudo ldconfig
ofed_info -s
rdma link show
ibv_devices
ibstat
ucx_info -d
lsmod | grep -E '^(mlx5_core|mlx5_ib)\b'
```

On a VM without an InfiniBand device, `ibstat` may report no adapters. On the
ND-series A100/H100 SKUs, both `mlx5_core` and `mlx5_ib` should be loaded and
the RDMA/InfiniBand commands should list the Mellanox devices before running
distributed SuperBench tests.

## 4. Install the GPU / driver / container stack

```bash
sudo dnf install -y \
    nvidia-open kmod-nvidia-open \
    nvidia-driver-common nvidia-driver-cuda nvidia-driver-cuda-libs \
    nvidia-kmod-common nvidia-modprobe nvidia-persistenced \
    gdrcopy gdrcopy-devel kmod-gdrcopy \
    nvidia-container-toolkit nvidia-container-toolkit-base \
    libnvidia-container1 libnvidia-container-tools

nvidia-smi   # sanity check
```

### NVSwitch SKUs only: `nvidia-fabric-manager`

Do not install or enable Fabric Manager on `Standard_NC80adis_H100_v5`. Its two
H100 GPUs communicate over PCIe and the CPU interconnect (`SYS` in
`nvidia-smi topo -m`), not NVLink/NVSwitch. On this SKU the driver may create
the control node `/dev/nvidia-nvswitchctl`, but
`/proc/driver/nvidia-nvswitch/devices` remains empty because there are no
physical NVSwitch devices. Fabric Manager then exits with
`NV_WARN_NOTHING_TO_DO`, which is expected.

If it was enabled on a non-NVSwitch SKU, disable it:

```bash
sudo systemctl disable --now nvidia-fabricmanager

on h100 ND enable and run it
sudo systemctl enable --now nvidia-fabricmanager
sudo systemctl status nvidia-fabricmanager --no-pager -l
systemctl show nvidia-fabricmanager \
  -p ActiveState -p SubState -p Result -p ExecMainStatus

```

On an NVSwitch-equipped SKU:

```bash
sudo dnf install -y nvidia-fabric-manager
sudo systemctl enable --now nvidia-fabricmanager
```

The rebuilt driver, open kernel module, and Fabric Manager packages are all
pinned to `610.43.02`. Confirm the running kernel and loaded driver before
debugging Fabric Manager itself:

```bash
test "$(uname -r)" = "6.18.39-1.10.azl4.x86_64"
test "$(modinfo -F version nvidia)" = "610.43.02"
test "$(nvidia-smi --query-gpu=driver_version --format=csv,noheader | sort -u)" = "610.43.02"
ls -l /dev/nvidia-nvswitch*
```

Fabric Manager queries NVSwitch through device nodes created by the loaded
`nvidia` module. If startup reports `request to query NVSwitch device
information from NVSwitch driver failed`, collect the probe state before
restarting it:

```bash
sudo modprobe nvidia
sudo nvidia-modprobe -c 0 -u

lspci -Dnn | grep -i nvidia
lsmod | grep '^nvidia'
ls -l /dev/nvidia* /dev/nvidia-nvswitch* 2>&1
sudo dmesg --color=never | grep -Ei 'NVRM|nvidia|nvswitch|Xid|GSP' | tail -200
sudo journalctl -b -u nvidia-fabricmanager --no-pager -o cat
```

If `uname -r` or either version check differs, reinstall the local `1.10` and
`610.43.02` RPMs and reboot before retrying. If versions match but no
`/dev/nvidia-nvswitch*` nodes exist, the failure is in the kernel driver's
NVSwitch probe; use the `dmesg` output above to identify the first NVRM/Xid/GSP
error. `No CX Bridge devices detected!` from the service precheck is not fatal
on a pre-NVL5 H100 system.

## 5. Register the NVIDIA container runtime

```bash
sudo nvidia-ctk runtime configure --runtime=containerd --set-as-default
sudo systemctl restart containerd
```

## 6. Install the CUDA toolkit (not built in this repo — pull from NVIDIA)

We only built `cuda-cudart-devel`/`cuda-driver-devel` as *build-time* deps for
`gdrcopy` (wired into the mock config only). SuperBench needs a full CUDA
toolkit (`nvcc`, cuBLAS, etc.) at runtime:

```bash
sudo tee /etc/yum.repos.d/cuda.repo <<'EOF'
[cuda]
name=cuda
baseurl=https://developer.download.nvidia.com/compute/cuda/repos/azl3/x86_64
enabled=1
gpgcheck=0
EOF
sudo dnf install -y cuda-toolkit-13-2
echo 'export PATH=/usr/local/cuda-13.2/bin:$PATH' | sudo tee -a ~/.bashrc
source ~/.bashrc
```

## 7. SuperBench setup

```bash
# numactl is invoked directly by several SuperBench benchmark wrappers
# (e.g. cublas-function); without it they fail with
# "numactl: command not found", surfaced as a non-zero return code. The
# numactl-devel package provides numa.h for the cpu_copy native benchmark.
sudo dnf install -y python3 python3-pip ansible boost-devel rsync git make gcc \
  numactl numactl-devel \
  openmpi-ofed prrte
test -f /usr/include/numa.h
sudo ln -sf /usr/bin/python3 /usr/bin/python

# torch/torchvision: cu132 wheels exist for CUDA 13.2. Install the explicit
# cuDNN wheel as well because cuda-toolkit-13-2 does not include cuDNN.
python3 -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cu132
python3 -m pip install nvidia-cudnn-cu13

# SuperBench does not require torchaudio. Remove any stale wheel because a
# cu130 build cannot be imported alongside the cu132 PyTorch wheel.
python3 -m pip uninstall -y torchaudio

python3 - <<'PY'
import torch
import torchvision

assert torch.version.cuda == "13.2", torch.version.cuda
print(f"torch={torch.__version__}, torchvision={torchvision.__version__}, CUDA={torch.version.cuda}")
PY

# transformers is imported unconditionally by superbench's model_benchmarks
# package (pytorch_bert.py), so it's needed even for non-BERT test runs.
python3 -m pip install transformers wheel pybind11

# py3nvml is normally pulled in via setup.py's [nvworker] extra
# (install_superbench.sh runs `pip install .[nvworker]`), but we install
# torch/torchvision manually above to control CUDA wheel versions, so it's
# missing. Without it, `sb run`'s Monitor process fails:
# "Failed to launch the monitor process - error message: No module named
# 'py3nvml'"
python3 -m pip install py3nvml

# NOTE: use the actual fork+branch the azlinux-ai-ml pipeline uses, not
# upstream microsoft/superbenchmark — it carries required AZL patches.
sudo git clone --recursive -b lihl/run-sb-on-azl https://github.com/henryli001/superbenchmark.git /opt/superbench
sudo chown -R "$(id -un):$(id -gn)" /opt/superbench
cd /opt/superbench

# AZL-specific patches applied by install_superbench.sh:
sudo rm -rf superbench/benchmarks/micro_benchmarks/cuda_decode_performance
sed -i 's/ID=\.\*fedora/ID=.*fedora|azurelinux/' third_party/nvbandwidth/CMakeLists.txt

# Python 3.14 defaults to the "forkserver" multiprocessing start method on
# Linux. SuperBench's Monitor contains a sched.scheduler RLock that cannot be
# pickled for forkserver. Bind Monitor to an explicit fork context instead of
# relying on sitecustomize.py, which may not load in an Ansible-launched Python.
python3 - <<'PY'
from pathlib import Path

path = Path("/opt/superbench/superbench/monitor/monitor.py")
source = path.read_text(encoding="utf-8")
if "class Monitor(multiprocessing.Process):" in source:
  source = source.replace(
    "import multiprocessing\n",
    "import multiprocessing\n\nForkProcess = multiprocessing.get_context('fork').Process\n",
    1,
  )
  source = source.replace(
    "class Monitor(multiprocessing.Process):",
    "class Monitor(ForkProcess):",
    1,
  )
  source = source.replace(
    "multiprocessing.Process.__init__(self)",
    "ForkProcess.__init__(self)",
    1,
  )
if source.count("class Monitor(ForkProcess):") != 1:
  raise RuntimeError("SuperBench Monitor fork patch did not apply exactly once")
path.write_text(source, encoding="utf-8")
PY

python3 -m pip install .
```

If SuperBench was installed before applying the Python 3.14 patch, run the
patch above from `/opt/superbench`, then reinstall the local source and verify
that `Monitor` uses `ForkProcess`:

```bash
cd /opt/superbench
python3 -m pip install --force-reinstall --no-deps .
python3 - <<'PY'
from superbench.monitor import Monitor

assert Monitor.__mro__[1].__name__ == "ForkProcess", Monitor.__mro__
print(Monitor.__mro__)
PY
```

### Persist the CUDA, MPI, NCCL, and SuperBench environment

`make cppbuild` runs CMake independently for each native benchmark. Setting
only `CUDAARCHS` is insufficient: CMake also needs `CUDACXX` or
`CMAKE_CUDA_COMPILER` to locate `nvcc`. Add the complete environment to
`~/.bashrc` once, then source it before building or running SuperBench.

The OFED Open MPI package uses a release-versioned prefix such as
`/usr/mpi/gcc/openmpi-ofed-5.0.10rc2.2605121430`. The block derives that prefix
from the installed RPM instead of hard-coding its version. Open MPI 5's
separately packaged launcher is `/usr/lib64/openmpi/bin/prterun`, not under the
OFED prefix; that path is likewise discovered from the `prrte` RPM. The block
also reuses the NCCL headers and libraries installed by the PyTorch wheel.

```bash
if ! grep -q '^# SuperBench AZL4 environment$' ~/.bashrc; then
  cat >> ~/.bashrc <<'EOF'
# SuperBench AZL4 environment
export CUDA_HOME=/usr/local/cuda-13.2
export CUDA_PATH="$CUDA_HOME"
export CUDACXX="$CUDA_HOME/bin/nvcc"
export CMAKE_CUDA_COMPILER="$CUDACXX"
export CUDAHOSTCXX=/usr/bin/g++
export CUDAARCHS=80

export SB_HOME=/opt/superbench
export SB_MICRO_PATH=/usr/local

MPI_BIN=$(rpm -ql openmpi-ofed-runtime 2>/dev/null | grep '/bin/mpirun$' | head -n1)
if [[ -z "$MPI_BIN" ]]; then
  MPI_BIN=$(rpm -ql openmpi-ofed 2>/dev/null | grep '/bin/mpirun$' | head -n1)
fi
if [[ -z "$MPI_BIN" ]]; then
  MPI_BIN=$(rpm -ql openmpi 2>/dev/null | grep '/bin/mpirun$' | head -n1)
fi
if [[ -n "$MPI_BIN" ]]; then
  export MPI_HOME=${MPI_BIN%/bin/mpirun}
  export OPAL_PREFIX="$MPI_HOME"
fi

PRTERUN_BIN=$(rpm -ql prrte 2>/dev/null | grep '/bin/prterun$' | head -n1)
if [[ -n "$PRTERUN_BIN" ]]; then
  export OMPI_PRTERUN="$PRTERUN_BIN"
  export PRRTE_BIN_DIR=${PRTERUN_BIN%/prterun}
fi

NCCL_PY_DIR=$(python3 -c \
  'import nvidia.nccl; print(list(nvidia.nccl.__path__)[0])' 2>/dev/null || true)
export NCCL_PY_DIR
export NCCL_HOME=/usr/local

CUDNN_PY_DIR=$(python3 -c \
  'import nvidia.cudnn; print(list(nvidia.cudnn.__path__)[0])' 2>/dev/null || true)
export CUDNN_PY_DIR

export PATH="$CUDA_HOME/bin${MPI_HOME:+:$MPI_HOME/bin}${PRRTE_BIN_DIR:+:$PRRTE_BIN_DIR}:$SB_MICRO_PATH/bin:$PATH"
export CPATH="${CUDNN_PY_DIR:+$CUDNN_PY_DIR/include:}${NCCL_PY_DIR:+$NCCL_PY_DIR/include:}${CPATH:-}"
export LIBRARY_PATH="${CUDNN_PY_DIR:+$CUDNN_PY_DIR/lib:}${NCCL_PY_DIR:+$NCCL_PY_DIR/lib:}${LIBRARY_PATH:-}"
export CMAKE_LIBRARY_PATH="${CUDNN_PY_DIR:+$CUDNN_PY_DIR/lib:}${CMAKE_LIBRARY_PATH:-}"
export LD_LIBRARY_PATH="$CUDA_HOME/lib64${MPI_HOME:+:$MPI_HOME/lib}${CUDNN_PY_DIR:+:$CUDNN_PY_DIR/lib}${NCCL_PY_DIR:+:$NCCL_PY_DIR/lib}:$SB_MICRO_PATH/lib:${LD_LIBRARY_PATH:-}"
EOF
fi

# Per-benchmark rank prefixes select GPUs. Remove the global mask used by
# earlier versions of this playbook so discovery sees the complete device set.
sed -i '/^export CUDA_VISIBLE_DEVICES=/d' ~/.bashrc
unset CUDA_VISIBLE_DEVICES

# Open MPI 5 delegates process launch to the separately packaged PRRTE binary.
# Replace the old same-prefix assumption in shells configured from an earlier
# version of this playbook.
PRTERUN_BIN=$(rpm -ql prrte 2>/dev/null | grep '/bin/prterun$' | head -n1)
test -x "$PRTERUN_BIN"
PRTED_BIN=$(rpm -ql prrte 2>/dev/null | grep '/bin/prted$' | head -n1)
test -x "$PRTED_BIN"
sed -i '/^export OMPI_PRTERUN=/d' ~/.bashrc
sed -i '/^export PRRTE_BIN_DIR=/d' ~/.bashrc
printf 'export OMPI_PRTERUN=%q\n' "$PRTERUN_BIN" >> ~/.bashrc
printf 'export PRRTE_BIN_DIR=%q\n' "${PRTED_BIN%/prted}" >> ~/.bashrc
printf 'export PATH="$PRRTE_BIN_DIR:$PATH"\n' >> ~/.bashrc

source ~/.bashrc

test -x "$CUDACXX"
"$CUDACXX" --version
echo "MPI_HOME=${MPI_HOME:-not found}"
command -v mpirun
test -x "$OMPI_PRTERUN"
command -v prted
"$OMPI_PRTERUN" --version
mpirun --version
mpirun --allow-run-as-root -np 1 /bin/true
```

Do not add `$CUDA_HOME/lib64/stubs` to `LD_LIBRARY_PATH`; the stub `libcuda.so`
is for linking only and causes CUDA device discovery to fail at runtime.

### NCCL headers/library for the native `dist_inference_cpp` benchmark

`azlinux-ai-ml` builds its own `libnccl`/`libnccl-devel` RPMs from source
(`SPECS/libnccl/libnccl.spec`), baked into its golden image ahead of time —
NVIDIA does **not** publish NCCL RPMs in either the `azl3` or `rhel9` CUDA
repos (confirmed empty package listings), so `dnf install libnccl-devel`
will never resolve. Without `nccl.h`/`libnccl.so`, `make cppbuild` fails
compiling `dist_inference_cpp` with `fatal error: nccl.h: No such file or
directory`.

Fastest fix on an ad-hoc VM: reuse the `nvidia-nccl-cuXX` pip wheel already
pulled in as a `torch` dependency instead of building NCCL from source. Expose
its headers and library through `/usr/local`, which is also `SB_MICRO_PATH`, so
nested Make invocations and the runtime linker resolve the same installation.

```bash
NCCL_PY_DIR=$(python3 -c \
  'import nvidia.nccl; print(list(nvidia.nccl.__path__)[0])')
NCCL_LIBRARY=$(readlink -f "$NCCL_PY_DIR/lib/libnccl.so.2")
test -f "$NCCL_PY_DIR/include/nccl.h"
test -f "$NCCL_LIBRARY"

sudo install -d /usr/local/include /usr/local/lib
sudo ln -sfn "$NCCL_PY_DIR/include/nccl.h" /usr/local/include/nccl.h
sudo ln -sfn "$NCCL_LIBRARY" /usr/local/lib/libnccl.so.2
sudo ln -sfn libnccl.so.2 /usr/local/lib/libnccl.so
sudo ldconfig

export NCCL_HOME=/usr/local
test -e "$NCCL_HOME/lib/libnccl.so"
ldconfig -p | grep -F libnccl.so.2
```

The persistent environment block above exports the NCCL include and library
paths used by `make cppbuild`.

### cuDNN headers/library for the native `cudnn-function` benchmark

The CUDA toolkit does not include cuDNN. The `nvidia-cudnn-cu13` wheel installed
above supplies `cudnn.h` and `libcudnn.so.9`, but CMake's `find_library(...
cudnn)` requires an unversioned `libcudnn.so` name. Expose the wheel directory
and add that development symlink before running `make cppbuild`:

```bash
CUDNN_PY_DIR=$(python3 -c \
  'import nvidia.cudnn; print(list(nvidia.cudnn.__path__)[0])')
export CUDNN_PY_DIR
ln -sf "$CUDNN_PY_DIR"/lib/libcudnn.so.9* "$CUDNN_PY_DIR/lib/libcudnn.so"

test -f "$CUDNN_PY_DIR/include/cudnn.h"
test -e "$CUDNN_PY_DIR/lib/libcudnn.so"
export CPATH="$CUDNN_PY_DIR/include:${CPATH:-}"
export LIBRARY_PATH="$CUDNN_PY_DIR/lib:${LIBRARY_PATH:-}"
export CMAKE_LIBRARY_PATH="$CUDNN_PY_DIR/lib:${CMAKE_LIBRARY_PATH:-}"
export LD_LIBRARY_PATH="$CUDNN_PY_DIR/lib:${LD_LIBRARY_PATH:-}"
```

### `CMAKE_CUDA_ARCHITECTURES` must be set for CUDA 13.2

The failure at `gpu_copy_performance/CMakeLists.txt:14` occurs while its
`cuda_common.cmake` include calls `enable_language(CUDA)`, before the target's
`CUDA_ARCHITECTURES` property is set. An exported `CUDAARCHS` may still lose to
an explicitly defined empty CMake cache value. Patch SuperBench's shared build
loop to pass the selected compute capability directly to every CMake configure
(`80` for A100, `90` for H100), then clear all per-benchmark caches:

```bash
# Use 90 instead on an H100 host.
export CUDAARCHS=80
test -n "$CUDAARCHS"
case "$CUDAARCHS" in 80|90) ;; *) echo "Unsupported CUDAARCHS=$CUDAARCHS" >&2; exit 1;; esac

sed -i \
  's|cmake -DCMAKE_PREFIX_PATH=|cmake -DCMAKE_CUDA_ARCHITECTURES="${CUDAARCHS}" -DCMAKE_PREFIX_PATH=|' \
  superbench/benchmarks/build.sh
grep -F -- '-DCMAKE_CUDA_ARCHITECTURES="${CUDAARCHS}"' \
  superbench/benchmarks/build.sh

find superbench/benchmarks/micro_benchmarks -type d -name build -prune -exec rm -rf {} +
find third_party -type d -name build -prune -exec rm -rf {} + 2>/dev/null
```

### Build all SuperBench native dependencies

`gemm-flops` requires CUTLASS's `cutlass_profiler`, which is built by the
third-party `cuda_cutlass` target rather than `make cppbuild`. Likewise,
`gpu-burn` belongs to the third-party `cuda_gpuburn` target, and `nccl-bw`
requires `all_reduce_perf` from `cuda_nccl_tests`. CUDA Samples removed the
`bandwidthTest` executable used by `mem-bw` in CUDA 12.9; build the supported
`nvbandwidth` replacement instead. Run all required Make targets in one
fail-fast shell after configuring the CUDA, MPI, NCCL, and cuDNN environment
above. Do not use the aggregate `cuda` target: it includes unrelated
dependencies and may stop before reaching the required targets.

On CUDA 13.2, pass the CUDA compiler and A100 architecture explicitly through
`sudo`; otherwise CMake can report `No CMAKE_CUDA_COMPILER could be found` or
`Failed to detect a default CUDA architecture`. Use `CUDAARCHS=90` and
`ARCHS=90` on H100:

```bash
cd /opt/superbench
source ~/.bashrc
sudo dnf install -y bc gcc-c++
git submodule update --init --recursive third_party/nccl-tests
test -f third_party/nccl-tests/Makefile

# Materialize a conventional NCCL development prefix from the PyTorch wheel.
# Do this here as well as in the NCCL section so this build block is rerunnable
# in shells configured by an older version of the playbook.
NCCL_PY_DIR=$(python3 -c \
  'import nvidia.nccl; print(list(nvidia.nccl.__path__)[0])')
NCCL_LIBRARY=$(find "$NCCL_PY_DIR/lib" -maxdepth 1 -type f \
  -name 'libnccl.so.2*' -print -quit)
test -f "$NCCL_PY_DIR/include/nccl.h"
test -f "$NCCL_LIBRARY"
sudo install -d /usr/local/include /usr/local/lib
sudo ln -sfn "$NCCL_PY_DIR/include/nccl.h" /usr/local/include/nccl.h
sudo ln -sfn "$NCCL_LIBRARY" /usr/local/lib/libnccl.so.2
sudo ln -sfn libnccl.so.2 /usr/local/lib/libnccl.so
sudo ldconfig
export NCCL_PY_DIR NCCL_HOME=/usr/local
ls -l "$NCCL_HOME"/lib/libnccl.so*

# Build NCCL Tests as the current user so compiler errors are shown directly.
echo "Building NCCL Tests for sm_${CUDAARCHS}"
make -C third_party/nccl-tests clean
LIBRARY_PATH="$NCCL_HOME/lib:$MPI_HOME/lib:${LIBRARY_PATH:-}" \
LD_RUN_PATH="$NCCL_HOME/lib:$MPI_HOME/lib" \
make -C third_party/nccl-tests \
  MPI=1 MPI_HOME="$MPI_HOME" NCCL_HOME="$NCCL_HOME" \
  CUDA_HOME="$CUDA_HOME" NVCC="$CUDACXX" \
  NVCC_GENCODE="-gencode=arch=compute_$CUDAARCHS,code=sm_$CUDAARCHS" \
  -j"$(nproc)"
for binary in all_reduce_perf all_gather_perf broadcast_perf reduce_perf \
  reduce_scatter_perf alltoall_perf; do
  test -x "third_party/nccl-tests/build/$binary"
  sudo install -m 0755 "third_party/nccl-tests/build/$binary" \
    "/usr/local/bin/$binary"
done
/usr/local/bin/all_reduce_perf --help >/dev/null
/usr/local/bin/alltoall_perf --help >/dev/null

# Build the remaining native dependencies under the installation prefix.
set -o pipefail
sudo env PATH="$PATH" LD_LIBRARY_PATH="$LD_LIBRARY_PATH" \
  CPATH="$CPATH" LIBRARY_PATH="$LIBRARY_PATH" \
  CMAKE_LIBRARY_PATH="$CMAKE_LIBRARY_PATH" \
  CUDA_HOME="$CUDA_HOME" CUDA_PATH="$CUDA_PATH" \
  CUDACXX="$CUDACXX" CMAKE_CUDA_COMPILER="$CMAKE_CUDA_COMPILER" \
  CUDAHOSTCXX="$CUDAHOSTCXX" CUDAARCHS="$CUDAARCHS" \
  MPI_HOME="$MPI_HOME" OPAL_PREFIX="$OPAL_PREFIX" \
  OMPI_PRTERUN="$OMPI_PRTERUN" \
  NCCL_PY_DIR="$NCCL_PY_DIR" NCCL_HOME="$NCCL_HOME" \
  SB_HOME="$SB_HOME" SB_MICRO_PATH="$SB_MICRO_PATH" \
  bash -euxo pipefail 2>&1 <<'NATIVE_BUILD' | tee superbench-native-build.log
    make postinstall
    make cppbuild
    make -C third_party \
      SB_MICRO_PATH="$SB_MICRO_PATH" CUDA_VER=13.2 ARCHS="$CUDAARCHS" \
      cuda_cutlass
    if [[ ! -x "$SB_MICRO_PATH/bin/cutlass_profiler" ]]; then
      make -C third_party \
        SB_MICRO_PATH="$SB_MICRO_PATH" CUDA_VER=13.2 ARCHS="$CUDAARCHS" \
        cuda_cutlass
    fi
    make -C third_party SB_MICRO_PATH="$SB_MICRO_PATH" cuda_gpuburn
    make -C third_party SB_MICRO_PATH="$SB_MICRO_PATH" nvbandwidth
NATIVE_BUILD

ls -l /usr/local/bin/cutlass_profiler
/usr/local/bin/cutlass_profiler --help >/dev/null
python3 examples/benchmarks/gemm_flops_cuda_performance.py

test -x /usr/local/bin/gpu_burn
test -f /usr/local/bin/compare.ptx
for binary in all_reduce_perf all_gather_perf broadcast_perf reduce_perf \
  reduce_scatter_perf alltoall_perf; do
  test -x "/usr/local/bin/$binary"
  if ldd "/usr/local/bin/$binary" | grep -q 'not found'; then
    ldd "/usr/local/bin/$binary"
    exit 1
  fi
done
/usr/local/bin/all_reduce_perf --help >/dev/null
test -x /usr/local/bin/nvbandwidth
/usr/local/bin/nvbandwidth --list >/dev/null
(
  cd /usr/local/bin
  CUDA_VISIBLE_DEVICES=0 ./gpu_burn 10
)
```

The conditional second `cuda_cutlass` invocation handles a Makefile quirk: the
first invocation may only clone CUTLASS because its `CMakeLists.txt` check is
evaluated before the clone recipe runs. The direct GPU-Burn test runs beside
`compare.ptx`, which GPU-Burn resolves relative to its working directory.

### Match local benchmark ranks to the installed GPUs

The upstream default local mode assumes eight GPUs:

```yaml
proc_num: 8
prefix: CUDA_VISIBLE_DEVICES={proc_rank}
```

On a single-A100 `Standard_NC24ads_A100_v4` VM, ranks 1 through 7 therefore
receive nonexistent CUDA device IDs. Native tests then fail at their first CUDA
call; `cudnn-function`, for example, reports `cudaDeviceReset() failed` with
`no CUDA-capable device is detected`. This is a rank/config mismatch, not a
cuDNN algorithm failure.

Create a runtime copy of the selected config whose local CUDA modes match the
number of GPUs visible to the driver. This preserves
`CUDA_VISIBLE_DEVICES={proc_rank}` while preventing invalid ranks:

```bash
cd /opt/superbench
SB_CONFIG=<config>.yaml
SB_RUNTIME_CONFIG=./sb-runtime-config.yaml
unset CUDA_VISIBLE_DEVICES
export GPU_COUNT=$(nvidia-smi --query-gpu=index --format=csv,noheader | wc -l)
test "$GPU_COUNT" -gt 0

python3 - "$SB_CONFIG" "$SB_RUNTIME_CONFIG" "$GPU_COUNT" <<'PY'
import sys
from pathlib import Path
import yaml

source, destination, gpu_count = sys.argv[1], sys.argv[2], int(sys.argv[3])
with open(source, encoding="utf-8") as stream:
  config = yaml.safe_load(stream)

benchmarks = config["superbench"]["benchmarks"]

# CUDA Samples removed bandwidthTest in CUDA 12.9. Its SuperBench wrapper is
# mem-bw; use the separately built nvbandwidth benchmark on CUDA 13.2.
if "mem-bw" in benchmarks:
  benchmarks["mem-bw"]["enable"] = False
nvbandwidth = benchmarks.setdefault("nvbandwidth", {
  "modes": [{"name": "local", "parallel": False}],
  "parameters": {
    "buffer_size": 128,
    "test_cases": [
      "host_to_device_memcpy_ce",
      "device_to_host_memcpy_ce",
      "host_to_device_memcpy_sm",
      "device_to_host_memcpy_sm",
    ],
    "num_loops": 18,
    "skip_verification": False,
    "disable_affinity": False,
    "use_mean": False,
  },
})
nvbandwidth["enable"] = True

for benchmark in benchmarks.values():
  for mode in benchmark.get("modes", []):
    prefix = str(mode.get("prefix", ""))
    if mode.get("name") == "local" and "CUDA_VISIBLE_DEVICES" in prefix:
      mode["proc_num"] = gpu_count

for name, benchmark in benchmarks.items():
  for mode in benchmark.get("modes", []):
    prefix = str(mode.get("prefix", ""))
    if mode.get("name") == "local" and "CUDA_VISIBLE_DEVICES" in prefix:
      proc_num = int(mode.get("proc_num", 1))
      if proc_num > gpu_count:
        raise RuntimeError(
          f"{name} launches {proc_num} CUDA ranks, but only {gpu_count} GPUs are visible"
        )

with open(destination, "w", encoding="utf-8") as stream:
  yaml.safe_dump(config, stream, sort_keys=False)
PY

CUDA_VISIBLE_DEVICES=0 python3 examples/benchmarks/cudnn_function.py
python3 - <<'PY'
import torch

count = torch.cuda.device_count()
assert count > 0, "PyTorch cannot see any CUDA devices"
for index in range(count):
  with torch.cuda.device(index):
    torch.empty(1, device="cuda")
  print(f"CUDA rank {index}: {torch.cuda.get_device_name(index)}")
PY
```

Both direct checks must pass before `sb run`. If they do, use
`$SB_RUNTIME_CONFIG` rather than the original eight-GPU config below.

## 8. Run SuperBench

```bash
cd /opt/superbench
echo "[all]
localhost ansible_connection=local" > mix.ini
sb run --no-docker --host-file mix.ini -c "$SB_RUNTIME_CONFIG" --output-dir ./sb-results
```

Pick `<config>.yaml` per SKU, matching `scripts/tests/run_sb_tests.sh` in
`azlinux-ai-ml`: `superbench_nd-a100_config.yaml` (single-node) or
`superbench_a100_distributed_config.yaml` (multi-node).

## 9. Adapt this playbook for a two-node H100 VMSS

These instructions assume `Standard_ND96isr_H100_v5`: each VM has eight H100
GPUs, NVSwitch, and eight InfiniBand adapters. Confirm the SKU and topology on
both VMs before proceeding:

```bash
curl -fsS -H Metadata:true \
  'http://169.254.169.254/metadata/instance/compute/vmSize?api-version=2021-02-01&format=text'
nvidia-smi -L
nvidia-smi topo -m
ibstat
```

Apply steps 2 through 7 to **both** VMs so they have the same kernel, NVIDIA
packages, CUDA toolkit, SuperBench checkout, native binaries, Python packages,
MPI paths, and NCCL libraries. The following H100 differences are mandatory:

- Use CUDA compute capability `90`: replace every `CUDAARCHS=80` and
  `ARCHS=80` with `CUDAARCHS=90` and `ARCHS=90` before rebuilding.
- Do not persist `CUDA_VISIBLE_DEVICES=0`; distributed jobs need all eight GPUs.
- Fabric Manager must be running because this SKU uses NVSwitch. Confirm both
  Fabric Manager and the loaded NVIDIA driver report `610.43.02` before
  testing.

On both VMs:

```bash
curl -fsSL \
  https://raw.githubusercontent.com/Azure/azhpc-images/master/topology/ndv5-topo.xml \
  -o "$HOME/ndv5-topo.xml"
python3 - "$HOME/ndv5-topo.xml" <<'PY'
import sys
import xml.etree.ElementTree as ET

root = ET.parse(sys.argv[1]).getroot()
assert root.tag == "system", root.tag
PY
sudo install -D -m 0644 "$HOME/ndv5-topo.xml" \
  /opt/microsoft/ndv5-topo.xml
sudo install -d -m 0755 /opt/microsoft/ndv5
sudo ln -sfn /opt/microsoft/ndv5-topo.xml /opt/microsoft/ndv5/topo.xml
test -r /opt/microsoft/ndv5-topo.xml

sed -i '/^export CUDA_VISIBLE_DEVICES=/d' ~/.bashrc
sed -i 's/^export CUDAARCHS=.*/export CUDAARCHS=90/' ~/.bashrc
source ~/.bashrc

test "$(nvidia-smi --query-gpu=index --format=csv,noheader | wc -l)" -eq 8
test "$(nvidia-smi --query-gpu=compute_cap --format=csv,noheader | sort -u)" = "9.0"
systemctl is-active --quiet nvidia-fabricmanager
test -x "$OMPI_PRTERUN"
test -x /usr/local/bin/all_reduce_perf
```

Rebuild native CUDA benchmarks and CUTLASS with `CUDAARCHS=90` / `ARCHS=90`
if they were previously built for A100 (`sm_80`).

### Configure the controller and inventory

Run `sb` from VM 0. Use the private IP of VM 1 and an SSH key accepted by VM 1.
Replace the placeholders below; VMSS instance names are not guaranteed to
resolve through DNS, so private IPs are the safer inventory targets.

```bash
export NODE1_IP=<vm1-private-ip>
export SSH_KEY=~/.ssh/id_ed25519
export VM_USER=$(id -un)

# -i must point to the private key. The matching .pub file belongs in
# ~/.ssh/authorized_keys on VM 1 and cannot be used as an SSH identity file.
test -f "$SSH_KEY"
chmod 600 "$SSH_KEY"
ssh -i "$SSH_KEY" -o BatchMode=yes "$VM_USER@$NODE1_IP" hostname

cat > /opt/superbench/h100-vmss.ini <<EOF
[all]
localhost ansible_connection=local
h100-node1 ansible_host=$NODE1_IP ansible_user=$VM_USER ansible_ssh_private_key_file=$SSH_KEY
EOF

cd /opt/superbench
ansible all -i h100-vmss.ini -m ping
ansible all -i h100-vmss.ini -m shell -a \
  'source ~/.bashrc && test $(nvidia-smi -L | wc -l) -eq 8 && test -x $OMPI_PRTERUN'
```

### Validate MPI and all 16 GPUs

Before involving SuperBench, verify that Open MPI can launch one process on
each VM. The environment paths must be valid and identical on both nodes:

```bash
cd /opt/superbench
NODE1_HOST=$(awk '/^h100-node1 / {print $2}' h100-vmss.ini | cut -d= -f2)

mpirun --host "localhost:1,$NODE1_HOST:1" \
  -x PATH -x LD_LIBRARY_PATH -x OMPI_PRTERUN \
  bash -lc 'hostname; nvidia-smi -L | wc -l'
```

Then run a focused two-node NCCL test. One MPI rank per VM drives all eight
local GPUs, for 16 GPUs total:

```bash
mpirun --host "localhost:1,$NODE1_HOST:1" \
  -x PATH -x LD_LIBRARY_PATH -x OMPI_PRTERUN \
  -x NCCL_DEBUG=INFO \
  /usr/local/bin/all_reduce_perf -b 8M -e 8G -f 2 -g 8
```

Confirm in the NCCL log that it selected the InfiniBand transport rather than
falling back to sockets. Do not set `NCCL_IB_DISABLE=1`.

### Run SuperBench across both VMs

Start from the distributed config used by `azlinux-ai-ml`, then create the
runtime copy from the "Match local benchmark ranks" section. On H100 the
detected `GPU_COUNT` must be `8`, so local modes launch ranks 0 through 7. For
distributed `mpi` or `torch.distributed` modes, set `proc_num: 8` when each
process owns one GPU and omit `node_num` (or set it to `all`) to use both VMs.
For `nccl-bw` configured with `parameters.ngpus: 8`, use `proc_num: 1` because
each MPI process already drives all eight GPUs on its VM.

```bash
cd /opt/superbench
export GPU_COUNT=8
export SB_CONFIG=./superbench/config/default.yaml
export SB_RUNTIME_CONFIG=./sb-h100-2node-runtime.yaml

test -f "$SB_CONFIG"
python3 - "$SB_CONFIG" "$SB_RUNTIME_CONFIG" "$GPU_COUNT" <<'PY'
import sys
from pathlib import Path
import yaml

source, destination, gpu_count = sys.argv[1], sys.argv[2], int(sys.argv[3])
with open(source, encoding="utf-8") as stream:
  config = yaml.safe_load(stream)

benchmarks = config["superbench"]["benchmarks"]
if "mem-bw" in benchmarks:
  benchmarks["mem-bw"]["enable"] = False
nvbandwidth = benchmarks.setdefault("nvbandwidth", {
  "modes": [{"name": "local", "parallel": False}],
  "parameters": {},
})
nvbandwidth["enable"] = True

for benchmark in benchmarks.values():
  for mode in benchmark.get("modes", []):
    prefix = str(mode.get("prefix", ""))
    if mode.get("name") == "local" and "CUDA_VISIBLE_DEVICES" in prefix:
      mode["proc_num"] = gpu_count
    env = mode.get("env", {})
    topology_file = env.get("NCCL_TOPO_FILE")
    if topology_file and not Path(topology_file).is_file():
      del env["NCCL_TOPO_FILE"]

with open(destination, "w", encoding="utf-8") as stream:
  yaml.safe_dump(config, stream, sort_keys=False)
PY

test -s "$SB_RUNTIME_CONFIG"
python3 -c 'import sys, yaml; yaml.safe_load(open(sys.argv[1], encoding="utf-8"))' \
  "$SB_RUNTIME_CONFIG"

test -f "$SSH_KEY"
test -f ./h100-vmss.ini
ssh -i "$SSH_KEY" -o BatchMode=yes -o ConnectTimeout=10 \
  "$VM_USER@$NODE1_IP" 'source ~/.bashrc; command -v python3; nvidia-smi -L'
ANSIBLE_HOST_KEY_CHECKING=False ansible all -i ./h100-vmss.ini \
  --timeout 10 -m ping
ANSIBLE_HOST_KEY_CHECKING=False ansible all -i ./h100-vmss.ini \
  --timeout 10 -m shell -a \
  'bash -lc "source ~/.bashrc; command -v sb; command -v prted; test \$(nvidia-smi -L | wc -l) -eq 8"'

set -o pipefail
ANSIBLE_HOST_KEY_CHECKING=False PYTHONUNBUFFERED=1 \
sb run --no-docker \
  --host-file ./h100-vmss.ini \
  --private-key "$SSH_KEY" \
  --config-file "$SB_RUNTIME_CONFIG" \
  --output-dir ./sb-h100-results 2>&1 | tee ./sb-h100-console.log
```

Run local GPU benchmarks first, then enable `nccl-bw` and other distributed
benchmarks. This separates per-node CUDA/NVSwitch failures from cross-node
SSH, MPI, InfiniBand, and GPUDirect RDMA failures.

If the command appears idle, inspect the orchestration log from another VM 0
shell. No process in `nvidia-smi` means the runner has not reached a GPU
benchmark yet:

```bash
tail -F /opt/superbench/sb-h100-console.log \
  /opt/superbench/sb-h100-results/sb-run.log 2>/dev/null
ps -ef | grep -E '[s]b run|[a]nsible|[s]sh|[m]pirun|[p]rted'
```

If result collection reports that
`~/sb-workspace/sb-h100-results` does not exist, the benchmark command failed
before creating its output directory. The trailing `rsync` error is secondary.
Find the first failure in the controller logs, then verify the exact no-docker
environment that SuperBench generated on both nodes:

```bash
grep -nEi 'FAILED|command not found|Run failed|Traceback|error' \
  ./sb-h100-results/sb-run.log ./sb-h100-console.log 2>/dev/null | head -100

grep -nE 'Runner is going to run|Run .* on remote|Run failed' \
  ./sb-h100-results/sb-run.log | tail -50
sed -n '180,220p' ./sb-h100-results/sb-run.log

cat ./sb-h100-results/hostfile
while read -r host; do
  getent hosts "$host" || printf 'UNRESOLVED: %s\n' "$host"
done < ./sb-h100-results/hostfile

ANSIBLE_HOST_KEY_CHECKING=False ansible all -i ./h100-vmss.ini \
  -m shell -a 'bash -lc '\''set -o allexport
source /tmp/sb.env
set +o allexport
printf "SB_WORKSPACE=%s\n" "$SB_WORKSPACE"
command -v sb
test -f "$SB_WORKSPACE/sb.config.yaml"
mkdir -p "$SB_WORKSPACE/sb-exec-probe"
sb exec --output-dir "$SB_WORKSPACE/sb-exec-probe" \
  -c "$SB_WORKSPACE/sb.config.yaml" \
  -C superbench.enable=kernel-launch'\'''
```

The probe runs `kernel-launch` independently on each node and leaves its logs
under `~/sb-workspace/sb-exec-probe`. Do not retry the distributed run until
this command succeeds on both hosts.

If that probe succeeds but `nccl-bw` exits with return code `254` after exactly
its configured timeout, inspect the effective NCCL rank layout and reproduce
the same MPI launch without CUDA:

```bash
python3 - "$SB_RUNTIME_CONFIG" <<'PY'
import sys
import yaml

with open(sys.argv[1], encoding="utf-8") as stream:
  benchmarks = yaml.safe_load(stream)["superbench"]["benchmarks"]
for name, benchmark in benchmarks.items():
  if name.startswith("nccl-bw"):
    print(name, "modes=", benchmark.get("modes"),
          "ngpus=", benchmark.get("parameters", {}).get("ngpus"))
PY

ANSIBLE_HOST_KEY_CHECKING=False ansible all -i ./h100-vmss.ini \
  -m shell -a 'bash -lc '\''source /tmp/sb.env
printf "node=%s workspace=%s\n" "$(hostname)" "$SB_WORKSPACE"
cat "$SB_WORKSPACE/hostfile"
while read -r host; do
  getent ahostsv4 "$host" || exit 1
done < "$SB_WORKSPACE/hostfile"
if [[ -n "${NCCL_TOPO_FILE:-}" ]]; then
  test -r "$NCCL_TOPO_FILE"
fi'\'''

source ~/.bashrc
cd /opt/superbench
NODE1_HOST=$(awk '/^h100-node1 / {print $2}' h100-vmss.ini | cut -d= -f2)
MPI_HOSTFILE=/opt/superbench/h100-mpi-hostfile
printf 'localhost slots=8\n%s slots=8\n' "$NODE1_HOST" > "$MPI_HOSTFILE"
cat "$MPI_HOSTFILE"
timeout 60 mpirun -tag-output -allow-run-as-root \
  -hostfile "$MPI_HOSTFILE" -map-by ppr:8:node -bind-to numa \
  -mca routed direct \
  -x PATH -x LD_LIBRARY_PATH -x OMPI_PRTERUN \
  bash -lc 'printf "rank=%s host=%s gpu=%s\n" \
    "$OMPI_COMM_WORLD_RANK" "$(hostname)" "$OMPI_COMM_WORLD_LOCAL_RANK"'

# Match SuperBench exactly: eight MPI ranks per node and one GPU per rank.
# INFO logging makes initialization progress visible before any bandwidth row.
timeout 180 mpirun -tag-output -allow-run-as-root \
  -hostfile "$MPI_HOSTFILE" -map-by ppr:8:node -bind-to numa \
  -mca routed direct \
  -x PATH -x LD_LIBRARY_PATH -x OMPI_PRTERUN \
  -x NCCL_TOPO_FILE=/opt/microsoft/ndv5-topo.xml \
  -x NCCL_IB_PCI_RELAXED_ORDERING=1 -x NCCL_NET_GDR_LEVEL=5 \
  -x NCCL_DEBUG=INFO -x NCCL_DEBUG_SUBSYS=INIT,NET \
  /usr/local/bin/all_reduce_perf -b 8M -e 1G -f 2 -g 1
```

The MPI probe must print 16 ranks. Every hostname must resolve to a private
IPv4 address from both VMs; an IPv6 link-local result is not sufficient for
cross-node PRRTE traffic. An omitted `ngpus` uses the benchmark's default of
one GPU per process, so `proc_num: 8` is correct for an eight-GPU node. If
`ngpus: 8` is set explicitly, use `proc_num: 1` so each node has one process
controlling its eight local GPUs. A profile may reference
`/opt/microsoft/ndv5-topo.xml` from a prepared HPC image; the runtime-config
generator removes that override when the file is absent so NCCL discovers the
topology itself.

## Known gaps / not covered here

- HPC-X, cuSPARSELt, and `transformer_engine` installs are skipped for a
  minimal first pass — add back only if a specific test needs them (see
  `install_nvidia_cuSPARSELT`, `install_nvidia_transformer_engine` in `azlinux-ai-ml`'s
  `scripts/superbench/install_superbench.sh` for the full versions).
- No AZL4 path exists yet in `azlinux-ai-ml`'s ADO pipelines
  (`hpc_image_build.yml`, `hpc_image_build_dev.yml` are hardcoded to
  `imageOffer: azure-linux-3`) — this playbook is a manual workaround, not a
  pipeline integration.
