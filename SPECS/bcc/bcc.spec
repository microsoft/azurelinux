%global debug_package %{nil}
Summary:        BPF Compiler Collection (BCC)
Name:           bcc
Version:        0.29.1
Release:        4%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Languages
URL:            https://github.com/iovisor/bcc
# Upstream now provides a release with the git submodule embedded in it
Source0:        https://github.com/iovisor/bcc/releases/download/v%{version}/%{name}-src-with-submodule.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         CVE-2024-2314.patch
Patch1:         CVE-2025-29481.patch
BuildRequires:  bison
BuildRequires:  clang-devel
BuildRequires:  cmake >= 2.8.7
BuildRequires:  elfutils-libelf-devel
BuildRequires:  flex
BuildRequires:  gcc
BuildRequires:  libstdc++
BuildRequires:  llvm-devel
BuildRequires:  make
BuildRequires:  ncurses-devel
BuildRequires:  pkg-config
BuildRequires:  python3-devel
BuildRequires:  zip
Requires:       elfutils-libelf

%description
BCC is a toolkit for creating efficient kernel tracing and manipulation programs,
and includes several useful tools and examples. It makes use of
extended BPF (Berkeley Packet Filters), formally known as eBPF,
a new feature that was first added to Linux 3.15.
Much of what BCC uses requires Linux 4.1 and above.

%package devel
Summary:        Shared Library for BPF Compiler Collection (BCC)
Requires:       %{name} = %{version}-%{release}

%description devel
%{name}-devel contains shared libraries and header files for
developing application.

%package -n python3-%{name}
Summary:        Python3 bindings for BPF Compiler Collection (BCC)
%{?python_provide:%python_provide python3-bcc}
Requires:       %{name} = %{version}-%{release}

%description -n python3-%{name}
Python bindings for BPF Compiler Collection (BCC)

%package examples
Summary:        Examples for BPF Compiler Collection (BCC)
Requires:       python3-%{name} = %{version}-%{release}

%description examples
Examples for BPF Compiler Collection (BCC)

%package tools
Summary:        Command line tools for BPF Compiler Collection (BCC)
Requires:       python3-%{name} = %{version}-%{release}

%description tools
Command line tools for BPF Compiler Collection (BCC)

%package -n libbpf-tools
Summary:        Command line libbpf tools for BPF Compiler Collection (BCC)
BuildRequires:  libbpf-devel
BuildRequires:  bpftool
 
%description -n libbpf-tools
Command line libbpf tools for BPF Compiler Collection (BCC)

%prep
%autosetup -p1 -n %{name}

%build
mkdir build
pushd build
cmake .. \
      -DBUILD_SHARED_LIBS:BOOL=ON \
      -DCMAKE_INSTALL_PREFIX=%{_prefix} \
      -DENABLE_LLVM_SHARED=1 \
      -DPYTHON_CMD=python3 \
      -DREVISION_LAST=%{version} \
      -DREVISION=%{version}

make %{?_smp_mflags}
popd
# It was discussed and agreed to package libbpf-tools with
# 'bpf-' prefix (https://github.com/iovisor/bcc/pull/3263)
# Installing libbpf-tools binaries in temp directory and
# renaming them in there and the install code will just
# take them.
# Note this is no longer needed in versions which contain 
# commit https://github.com/iovisor/bcc/commit/3469bf1d94a6b8f5deb34586e6c8e4ffec8dd0be
# as APP_PREFIX can be used (ex: APP_PREFIX='bpf-' \)

pushd libbpf-tools
make BPFTOOL=bpftool CFLAGS="%{optflags}" LDFLAGS="%{build_ldflags}"
make DESTDIR=./tmp-install prefix= install
(
    cd tmp-install/bin
    for file in *; do
        mv $file bpf-$file
    done
    # now fix the broken symlinks
    for file in `find . -type l`; do
        dest=$(readlink "$file")
        ln -s -f bpf-$dest $file
    done
)
popd

%install
pushd build
make install/strip DESTDIR=%{buildroot}
popd

# Install libbpf-tools
# We cannot use `install` because some of the tools are symlinks and `install`
# follows those. Since all the tools already have the correct permissions set,
# we just need to copy them to the right place while preserving those
pushd libbpf-tools
mkdir -p %{buildroot}%{_sbindir}
install -m 755 tmp-install/bin/* %{buildroot}%{_sbindir}/
popd

# mangle shebangs
find %{buildroot}/usr/share/bcc/{tools,examples} -type f -exec \
    sed -i -e '1 s|^#!/usr/bin/python$|#!'%{__python3}'|' \
           -e '1 s|^#!/usr/bin/env python$|#!'%{__python3}'|' {} \;

# Remove static libraries
find %{buildroot}%{_lib64dir} -name '*.a' -delete

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc README.md
%license LICENSE.txt
%{_lib64dir}/lib%{name}.so.*
%{_lib64dir}/libbcc_bpf.so.*

%files devel
%{_lib64dir}/lib%{name}.so
%{_lib64dir}/libbcc_bpf.so
%{_lib64dir}/pkgconfig/lib%{name}.pc
%{_includedir}/%{name}/

%files -n python3-bcc
%{python3_sitelib}/%{name}*

%files examples
%{_datadir}/%{name}/examples/*
%exclude %{_datadir}/%{name}/examples/*.pyc
%exclude %{_datadir}/%{name}/examples/*.pyo
%exclude %{_datadir}/%{name}/examples/*/*.pyc
%exclude %{_datadir}/%{name}/examples/*/*.pyo
%exclude %{_datadir}/%{name}/examples/*/*/*.pyc
%exclude %{_datadir}/%{name}/examples/*/*/*.pyo

%files tools
%{_datadir}/%{name}/introspection/*
%{_datadir}/%{name}/tools/*
%{_datadir}/%{name}/man/*

%files -n libbpf-tools
%{_sbindir}/bpf-*

%changelog
* Tue Dec 16 2025 Rachel Menge <rachelmenge@microsoft.com> - 0.29.1-4
- Add libbpf-tools subpackage

* Mon Apr 14 2025 Jyoti Kanase <v-jykanase@microsoft.com> - 0.29.1-3
- Patch CVE-2025-29481

* Tue Mar 18 2025 Jyoti Kanase <v-jykanase@microsoft.com> - 0.29.1-2
- Fix CVE-2024-2314

* Wed Dec 20 2023 Muhammad Falak <mwani@microsoft.com> - 0.29.1-1
- Bump version to 0.29.1

* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.28.0-1
- Auto-upgrade to 0.28.0 - Azure Linux 3.0 - package upgrades

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 0.27.0-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Fri Apr 28 2023 Muhammad Falak <mwani@microsoft.com> - 0.27.0-1
- Add an explicit BR on zip
- Update to 0.27.0

* Wed Feb 09 2022 Chris Co <chrco@microsoft.com> - 0.24.0-1
- Update to 0.24.0

* Fri Sep 17 2021 Chris Co <chrco@microsoft.com> - 0.22.0-1
- Update to 0.22.0
- Using shared `elfutils-libelf` libraries instead of static ones.

* Fri Jun 05 2020 Suresh Babu Chalamalasetty <schalam@microsoft.com> 0.12.0-1
- Update bcc version

* Tue Apr 21 2020 Eric Li <eli@microsoft.com> 0.10.0-4
- Fix #Source0

* Tue Apr 07 2020 Paul Monson <paulmon@microsoft.com> 0.10.0-3
- Add #Source0. License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 0.10.0-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Wed Jun 26 2019  Keerthana K <keerthanak@vmware.com> 0.10.0-1
- Initial bcc package for PhotonOS.
