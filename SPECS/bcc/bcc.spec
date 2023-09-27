%global debug_package %{nil}
Summary:        BPF Compiler Collection (BCC)
Name:           bcc
Version:        0.27.0
Release:        2%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/iovisor/bcc
# Upstream now provides a release with the git submodule embedded in it
Source0:        https://github.com/iovisor/bcc/releases/download/v%{version}/%{name}-src-with-submodule.tar.gz#/%{name}-%{version}.tar.gz
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

%prep
%setup -q -n %{name}

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

%install
pushd build
make install/strip DESTDIR=%{buildroot}
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

%changelog
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
