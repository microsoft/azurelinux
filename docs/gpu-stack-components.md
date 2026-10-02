# AZL4 GPU/InfiniBand Stack — Component Inventory

Inventory of the components added on `edehghani/4.0-gpu-stack` (diffed against
`origin/4.0`) to support NVIDIA GPU workloads and NVIDIA/Mellanox InfiniBand
(OFED) networking on Azure Linux 4.0.

## NVIDIA proprietary driver stack

| Component | Version | Source | Open source? | Purpose | Status |
|---|---|---|---|---|---|
| `nvidia-driver` | 610.43.02 | NVIDIA `.run` installer, `download.nvidia.com` | No (NVIDIA License) | Userspace CUDA/OpenCL driver components, `nvidia-smi`, `nvidia-powerd`, driver libs | Locally built (topic branch, not merged) |
| `nvidia-open` | 610.43.02 | Meta-package (no source, only deps) | No (NVIDIA License) | Meta-package pulling in `nvidia-kmod`, `nvidia-driver-cuda`, `libnvidia-ml` | Locally built (topic branch, not merged) |
| `nvidia-kmod-common` | 610.43.02 | NVIDIA `.run` installer | No (NVIDIA License) | Shared firmware, udev rules, modprobe config for the kernel modules | Locally built (topic branch, not merged) |
| `nvidia-fabric-manager` | 610.43.02 | `developer.download.nvidia.com` fabricmanager archive | No (NVIDIA License) | NVSwitch fabric management daemon (multi-GPU NVLink topologies) | Locally built (topic branch, not merged) |
| `cuda-compat` | 610.43.02 | NVIDIA `.run` installer | No (NVIDIA License) | CUDA forward-compatibility package | Locally built (topic branch, not merged) |
| `nvidia-modprobe` | 610.43.02 | `download.nvidia.com` tarball | Yes (GPLv2+) | Helper to load the `nvidia` module and create device nodes | Locally built (topic branch, not merged) |
| `nvidia-persistenced` | 610.43.02 | `download.nvidia.com` tarball | Yes (MIT) | Daemon that keeps GPU driver state persistent | Locally built (topic branch, not merged) |
| `kmod-nvidia-open` (in `kernel.spec`) | 610.43.02 | `github.com/NVIDIA/open-gpu-kernel-modules` | Yes (dual MIT/GPL) | NVIDIA open GPU kernel modules, incl. `nvidia-peermem` | Locally built (topic branch, not merged) |
| `gdrcopy` / `kmod-gdrcopy` (in `kernel.spec`) | 2.6 | `github.com/NVIDIA/gdrcopy` | Yes (BSD/MIT/GPL mix) | Low-latency GPUDirect RDMA memory-copy library + kernel module | Locally built (topic branch, not merged) |

## Container GPU tooling

| Component | Version | Source | Open source? | Purpose | Status |
|---|---|---|---|---|---|
| `libnvidia-container` | 1.20.0 | `github.com/NVIDIA/libnvidia-container` | Yes (Apache-2.0/GPL/LGPL/MIT mix) | Library that injects GPU devices/libs into containers | Locally built (topic branch, not merged) |
| `nvidia-container-toolkit` | 1.20.0 | `github.com/NVIDIA/nvidia-container-toolkit` | Yes (Apache-2.0) | CLI + runtime hooks for GPU-enabled container runtimes | Locally built (topic branch, not merged) |

## NVIDIA/Mellanox OFED stack

All from the `MLNX_OFED_SRC-26.04` bundle (`linux.mellanox.com`) unless noted.

| Component | Version | Open source? | Purpose | Status |
|---|---|---|---|---|
| `mlnx-ofa_kernel*` (in `kernel.spec`) | 26.04 (OFED.26.04.0.8.5.1) | Yes (GPLv2/BSD) | Core Mellanox InfiniBand/RoCE driver stack: `mlx5_core`, `mlx5_ib`, `ib_core`, etc. | Locally built (topic branch, not merged) |
| `kmod-iser` (in `kernel.spec`) | 26.04 | Yes | iSCSI Extensions for RDMA (iSER) initiator kernel module | Locally built (topic branch, not merged) |
| `kmod-isert` (in `kernel.spec`) | 26.04 | Yes | iSER target kernel module | Locally built (topic branch, not merged) |
| `kmod-mlnx-nfsrdma` (in `kernel.spec`) | 26.04 | Yes | NFS-over-RDMA kernel module | Locally built (topic branch, not merged) |
| `kmod-srp` (in `kernel.spec`) | 26.04 | Yes | SCSI RDMA Protocol (SRP) initiator kernel module | Locally built (topic branch, not merged) |
| `kernel-mft`/`kmod-mft` (in `kernel.spec`) | 4.36.0 | Yes | Mellanox Firmware Tools kernel driver (device access for `mst`) | Locally built (topic branch, not merged) |
| `xpmem` (in `kernel.spec`) | 2604.0.2 | Yes (GPL-2.0/LGPL-2.1) | Cross-process shared-memory kernel module + userspace lib (used by MPI) | Locally built (topic branch, not merged) |
| `ofed-scripts` | 26.04 | Yes (GPL/BSD) | `openibd` service + udev/interface-manager helper scripts | Locally built (topic branch, not merged) |
| `rdma-core-ofed` | 2604.0.7 | Yes (GPLv2/BSD) | Userspace RDMA verbs libraries/daemons (replaces community `rdma-core`) | Locally built (topic branch, not merged) |
| `mlnx-tools-ofed` | 2604.0.13 | Yes (GPLv2/BSD) | Mellanox userland diagnostic/tuning tools | Locally built (topic branch, not merged) |
| `mlnx-ethtool` | 2604.0.0 | Yes (GPL) | Mellanox-patched `ethtool` for mlx5 NIC tuning | Locally built (topic branch, not merged) |
| `mlnx-iproute2` | 2604.0.0 | Yes (GPL) | Mellanox-patched `iproute2` | Locally built (topic branch, not merged) |
| `openmpi-ofed` | 5.0.10rc2.2605121430 | Yes (BSD) | Open MPI build tuned for the OFED/UCX stack | Locally built (topic branch, not merged) |
| `ucx-ofed` | 1.21.0.20260504 | Yes (BSD) | Unified Communication X transport library (used by MPI/NCCL) | Locally built (topic branch, not merged) |
| `perftest-ofed` | 26.04.16 | Yes (BSD/GPLv2) | RDMA microbenchmarks (`ib_write_bw`, etc.) | Locally built (topic branch, not merged) |
| `multiperf` | 3.0 | Yes (BSD/GPLv2) | Multi-QP RDMA performance benchmark tool | Locally built (topic branch, not merged) |
| `ibsim-ofed` | 0.12.1 | Yes (GPLv2/BSD) | InfiniBand fabric simulator for management/testing | Locally built (topic branch, not merged) |
| `ibarr` | 2604.0.0 | Yes (GPL-2.0/BSD-2-Clause) | NVIDIA address/route resolution userspace service for InfiniBand | Locally built (topic branch, not merged) |
| `rshim-ofed` | 2.7.3 | Yes (GPLv2) | BlueField/DPU rshim management driver and tools | Locally built (topic branch, not merged) |

## Notes

- All "NVIDIA License" entries are proprietary — that's the closed driver
  payload extracted from the `.run` installer or NVIDIA's binary
  redistributables (fabric manager).
- Everything under the OFED table and the open kernel-module row is open
  source, though pulled from vendor-hosted bundles (Mellanox's DOCA mirror or
  NVIDIA's GitHub) rather than Fedora upstream — this is why they're local
  specs rather than Fedora-sourced components.
- The kernel-embedded subpackages (`kmod-*`, `xpmem`, `mlnx-ofa_kernel*`,
  `gdrcopy`) aren't separate `azldev` components; they're `.inc` files
  included directly into `base/comps/kernel/kernel.spec`. See
  [`oss-kmod-packaging-strategy.md`](oss-kmod-packaging-strategy.md) for how
  that phase-gated include pattern works.
