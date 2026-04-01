Summary:        Metapackage for essential build tools
Name:           build-essential
Version:        1.0
Release:        1%{?dist}
License:        MIT
BuildArch:      noarch

Requires:       gcc
Requires:       gcc-c++
Requires:       make
Requires:       binutils
Requires:       glibc-devel
Requires:       kernel-headers
Requires:       pkgconf

%description
A meta-package that installs the essential tools needed for building software from source: compiler (gcc, g++), linker (binutils), make, C library headers, kernel headers, and pkg-config.

%build

%install

%files

%changelog
* Tue Apr 01 2026 Madhur Aggarwal <madaggarwal@microsoft.com> - 1.0-1
- Added build-essential metapackage for Azure Linux 4.0
