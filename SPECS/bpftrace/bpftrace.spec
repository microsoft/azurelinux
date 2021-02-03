Summary:        Berkeley Packet Filter Tracing Language
Name:           bpftrace
Version:        0.11.4
Release:        1%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://github.com/iovisor/bpftrace
Source0:        https://github.com/iovisor/%{name}/%{name}-%{version}.tar.gz
BuildRequires:  bcc-devel
BuildRequires:  binutils-devel
BuildRequires:  bison
BuildRequires:  clang-devel
BuildRequires:  cmake
BuildRequires:  elfutils-libelf-devel
BuildRequires:  flex
BuildRequires:  gcc
BuildRequires:  git
BuildRequires:  llvm-devel >= 8.0.1-5
BuildRequires:  make
BuildRequires:  systemtap-sdt-devel
BuildRequires:  zlib-devel
Requires:       bcc
Requires:       binutils
Requires:       clang
Requires:       glibc
Requires:       libgcc
Requires:       libstdc++
Requires:       llvm >= 8.0.1-5

%description
bpftrace is a high-level tracing language for Linux enhanced Berkeley Packet Filter (eBPF)

%prep
%autosetup -p1

%build
mkdir build; cd build; cmake -DCMAKE_BUILD_TYPE=Release -DOFFLINE_BUILDS=true ..
make bpftrace

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
* Wed Feb 03 2021 Henry Beberman <henry.beberman@microsoft.com> - 0.11.4-1
- Add bpftrace spec.
- License verified
- Original version for CBL-Mariner