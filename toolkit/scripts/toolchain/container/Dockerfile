# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
#
# Dockerfile to build Mariner toolchain from scratch
#
FROM mcr.microsoft.com/cbl-mariner/base/core:2.0.20231004

# Tag the layers so we can clean up all the containers associated with a build directory
ARG MARINER_BUILD_DIR
LABEL marinertoolchain=$MARINER_BUILD_DIR

# Define LFS root directory and setup environment variables
ENV LFS=/temptoolchain/lfs
ENV LC_ALL=POSIX
ENV PATH=/tools/bin:/bin:/usr/bin:/sbin:/usr/sbin

COPY [ "./version-check-container.sh", \
       "$LFS/tools/" ]

# Install toolchain build dependencies
RUN tdnf install -y \
    bison \
    build-essential \
    byacc \
    ca-certificates \
    ccache \
    cpio \
    file \
    flex \
    gawk \
    gcc \
    make \
    patch \
    perl \
    rpm \
    sudo \
    tar \
    texinfo \
    unzip \
    util-linux \
    vim \
    wget \
    zip && \
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
       "$LFS/tools/" ]

# Download source, then create lfs user and group.
# Append "; exit 0" after wget commands to ignore download errors that might be expected. The sha256sum command will verify all downloads.
# Note: Fetch the kernel sources differently to ensure we rename the source tarball appropriately. The rename is needed to comply with
# the naming convention of the source cache (convention used to prevent naming collisions).
WORKDIR $LFS/sources
RUN wget -nv --no-clobber --timeout=30 --continue --input-file=$LFS/tools/toolchain-local-wget-list --directory-prefix=$LFS/sources; exit 0
# Disable downloading from remote sources by default. The 'toolchain-local-wget-list' generated for the above line will download from $(SOURCE_URL)
# The 'toolchain-remote-wget-list' is still available and can be used as an alternate to $(SOURCE_URL) if desired.
#RUN wget -nv --no-clobber --timeout=30 --continue --input-file=$LFS/tools/toolchain-remote-wget-list --directory-prefix=$LFS/sources; exit 0
RUN wget -nv --no-clobber --timeout=30 --continue https://github.com/microsoft/CBL-Mariner-Linux-Kernel/archive/rolling-lts/mariner-2/5.15.48.1.tar.gz -O kernel-5.15.48.1.tar.gz --directory-prefix=$LFS/sources; exit 0
USER root

RUN mkdir -pv $LFS/{etc,var} $LFS/usr/{bin,lib,sbin} && \
    ln -sv usr/bin $LFS/bin && \
    ln -sv usr/lib $LFS/lib && \
    ln -sv usr/sbin $LFS/sbin && \
    mkdir -pv $LFS/lib64 && \
    mkdir -pv $LFS/usr/share

RUN sha256sum -c $LFS/tools/toolchain-sha256sums && \
    groupadd lfs && \
    useradd -s /bin/bash -g lfs -m -k /dev/null lfs && \
    usermod -a -G sudo lfs && \
    chown -Rv lfs $LFS/usr && \
    chown -v lfs $LFS/tools && \
    chown -Rv lfs $LFS/{usr{,/*},lib,var,etc,bin,sbin,tools} && \
    chown -v lfs $LFS/lib64 && \
    chown -v lfs $LFS/sources && \
    chown -Rv lfs $LFS/logs && \
    echo "lfs ALL = NOPASSWD : ALL" >> /etc/sudoers && \
    echo 'Defaults env_keep += "LFS LC_ALL LFS_TGT PATH MAKEFLAGS FETCH_TOOLCHAIN_MODE LFS_TEST LFS_DOCS JOB_COUNT LOOP IMAGE_SIZE INITRD_TREE IMAGE"' >> /etc/sudoers

RUN echo "exec env -i HOME=$HOME TERM=$TERM PS1='\u:\w\$ ' /bin/bash" >> /home/lfs/.bash_profile
COPY [ "./.bashrc", \
       "/home/lfs/" ]

USER lfs
COPY [ "./toolchain_build_temp_tools.sh", \
       "./coreutils-fix-get-sys_getdents-aarch64.patch", \
       "./cpio_extern_nocommon.patch", \
       "./CVE-2021-38185.patch", \
       "./CVE-2023-4039.patch", \
       "./linker-script-readonly-keyword-support.patch", \
       "./rpm-define-RPM-LD-FLAGS.patch", \
       "$LFS/tools/" ]

USER root
RUN  chown -Rv lfs $LFS/tools && \
     chown -Rv lfs $LFS/usr && \
     chown -Rv lfs:lfs /home/lfs/

USER lfs
RUN /tools/toolchain_build_temp_tools.sh

COPY [ "./toolchain_initial_chroot_setup.sh", \
       "./toolchain_build_in_chroot.sh", \
       "./mount_chroot_start_build.sh", \
       "./unmount_chroot.sh", \
       "$LFS/tools/" ]

USER root

ENTRYPOINT [ "/tools/mount_chroot_start_build.sh" ]
