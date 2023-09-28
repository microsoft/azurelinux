Summary:        Berkeley Packet Filter Tracing Language
Name:           bpftrace
Version:        0.16.0
Release:        2%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://github.com/iovisor/bpftrace
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  bcc-devel
BuildRequires:  binutils-devel
BuildRequires:  bison
BuildRequires:  cereal-devel
BuildRequires:  clang-devel
BuildRequires:  cmake
BuildRequires:  elfutils-libelf-devel
BuildRequires:  flex
BuildRequires:  gcc
BuildRequires:  git
BuildRequires:  libbpf-devel
BuildRequires:  libpcap-devel
BuildRequires:  llvm-devel >= 12.0.1-1
BuildRequires:  make
BuildRequires:  systemtap-sdt-devel
BuildRequires:  vim-extra
BuildRequires:  zlib-devel
Requires:       bcc
Requires:       binutils
Requires:       clang
Requires:       glibc
Requires:       libgcc
Requires:       libstdc++
Requires:       llvm >= 12.0.1-1
%if %{with_check}
BuildRequires:  gmock
BuildRequires:  gmock-devel
BuildRequires:  gtest
BuildRequires:  gtest-devel
%endif

%description
bpftrace is a high-level tracing language for Linux enhanced Berkeley Packet Filter (eBPF)

%prep
%autosetup -p1

%build

mkdir build
cd build

%cmake \
    -DCMAKE_BUILD_TYPE=Release \
    -DBUILD_SHARED_LIBS:BOOL=OFF \
%if !%{with_check}
    -DBUILD_TESTING=0 \
%endif
    ..

make bpftrace

%check
cd build
make test

%install
mkdir -p %{buildroot}%{_bindir}/
mkdir -p %{buildroot}%{_datadir}/bpftrace/tools/doc
install -p -m 755 build/src/bpftrace %{buildroot}%{_bindir}/
install -p -m 755 tools/*.bt %{buildroot}%{_datadir}/bpftrace/tools
install -p -m 644 tools/*.txt %{buildroot}%{_datadir}/bpftrace/tools/doc

%files
%license LICENSE
%doc README.md CONTRIBUTING-TOOLS.md
%{_bindir}/bpftrace
%{_datadir}/bpftrace/tools

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 0.16.0-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Tue Oct 04 2022 Muhammad Falak <mwani@microsoft.com> - 0.16.0-1
- Bump version to 0.16.0

* Wed Aug 17 2022 Muhammad Falak <mwani@microsoft.com> - 0.15.0-1
- Bump version to 0.15.0

* Tue Mar 08 2022 Muhammad Falak <mwani@microsoft.com> - 0.14.1-1
- Bump version to 0.14.1

* Wed Feb 09 2022 Chris Co <chrco@microsoft.com> - 0.13.0-2
- Disable building of shared libraries

* Fri Sep 17 2021 Chris Co <chrco@microsoft.com> - 0.13.0-1
- Update to 0.13.0.
- Fixed source URL.
- Enabled tests.

* Wed Feb 03 2021 Henry Beberman <henry.beberman@microsoft.com> - 0.11.4-1
- Add bpftrace spec.
- License verified
- Original version for CBL-Mariner
