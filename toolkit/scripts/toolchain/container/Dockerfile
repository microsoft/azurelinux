# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
#
# Dockerfile to Mariner toolchain from scratch
#
FROM ubuntu:18.04

# Define LFS root directory and setup environment variables
ENV LFS=/temptoolchain/lfs
ENV LC_ALL=POSIX
ENV PATH=/tools/bin:/bin:/usr/bin:/sbin:/usr/sbin

COPY [ "./version-check-container.sh", \
       "$LFS/tools/" ]

# Install toolchain build dependencies
RUN apt-get update -y -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get -yq install \
    bison \
    gawk \
    gcc \
    g++ \
    make \
    patch \
    python-aptdaemon \
    rpm \
    texinfo \
    sudo \
    vim \
    wget \
    openjdk-8-jdk \
    libx11-dev \
    libxext-dev \
    libxrender-dev \
    libxtst-dev \
    libxt-dev \
    libcups2-dev \
    libfreetype6-dev \
    libasound2-dev \
    libpng16-16 \
    cpio \
    file \
    unzip \
    zip \
    ccache \
    libgif-dev \
    libfontconfig1-dev \
    flex && \
    apt-get clean && \
    ln    -sf bash /bin/sh && \
    mkdir -pv $LFS/sources && \
    chmod -v a+wt $LFS/sources && \
    mkdir -pv $LFS/logs/temptoolchain && \
    mkdir -pv $LFS/tools && \
    ln    -sv $LFS/tools / && \
    $LFS/tools/version-check-container.sh

COPY [ "./toolchain-sha256sums", \
       "./toolchain-remote-wget-list", \
       "./toolchain-local-wget-list", \
       "./rpm-define-RPM-LD-FLAGS.patch", \
       "./linker-script-readonly-keyword-support.patch", \
       "./toolchain-jdk8-wget.sh", \
       "./0002-add-linux-syscall-license-info.patch", \
       "$LFS/tools/" ]

# Download source, then create lfs user and group.
# Append "; exit 0" after wget commands to ignore download errors that might be expected. The sha256sum command will verify all downloads.
# Note: Fetch the kernel sources differently to ensure we rename the source tarball appropriately. The rename is needed to comply with
# the naming convention of the source cache (convention used to prevent naming collisions).
WORKDIR $LFS/sources
RUN wget -nv --no-clobber --timeout=30 --no-check-certificate --continue --input-file=$LFS/tools/toolchain-local-wget-list --directory-prefix=$LFS/sources; exit 0
RUN wget -nv --no-clobber --timeout=30 --continue --input-file=$LFS/tools/toolchain-remote-wget-list --directory-prefix=$LFS/sources; exit 0
RUN wget -nv --no-clobber --timeout=30 --continue https://github.com/microsoft/CBL-Mariner-Linux-Kernel/archive/rolling-lts/mariner/5.10.78.1.tar.gz -O kernel-5.10.78.1.tar.gz --directory-prefix=$LFS/sources; exit 0
USER root
RUN /tools/toolchain-jdk8-wget.sh; exit 0
RUN sha256sum -c $LFS/tools/toolchain-sha256sums && \
    groupadd lfs && \
    useradd -s /bin/bash -g lfs -m -k /dev/null lfs && \
    echo "lfs:lfs" | chpasswd && \
    adduser lfs sudo && \
    chown -v lfs $LFS/tools && \
    chown -v lfs $LFS/sources && \
    chown -Rv lfs $LFS/logs && \
    echo "lfs ALL = NOPASSWD : ALL" >> /etc/sudoers && \
    echo 'Defaults env_keep += "LFS LC_ALL LFS_TGT PATH MAKEFLAGS FETCH_TOOLCHAIN_MODE LFS_TEST LFS_DOCS JOB_COUNT LOOP IMAGE_SIZE INITRD_TREE IMAGE"' >> /etc/sudoers

RUN echo "exec env -i HOME=$HOME TERM=$TERM PS1='\u:\w\$ ' /bin/bash" >> /home/lfs/.bash_profile
COPY [ "./.bashrc", \
       "/home/lfs/" ]

USER lfs
COPY [ "./toolchain_build_temp_tools.sh", \
       "./04-fix-sigstksz.patch", \
       "./m4-1.4.18-glibc-change-work-around.patch", \
       "./coreutils-fix-get-sys_getdents-aarch64.patch", \
       "$LFS/tools/" ]
RUN /tools/toolchain_build_temp_tools.sh

COPY [ "./toolchain_initial_chroot_setup.sh", \
       "./toolchain_build_in_chroot.sh", \
       "./mount_chroot_start_build.sh", \
       "./unmount_chroot.sh", \
       "./jdk8-build-raw.sh", \
       "./toolchain-jdk8-build.sh", \
       "./Awt_build_headless_only.patch", \
       "./check-system-ca-certs.patch", \
       "./go14_bootstrap_aarch64.patch", \
       "./rpm-define-RPM-LD-FLAGS.patch", \
       "./cpio_extern_nocommon.patch", \
       "$LFS/tools/" ]

USER root

ENTRYPOINT [ "/tools/mount_chroot_start_build.sh" ]
