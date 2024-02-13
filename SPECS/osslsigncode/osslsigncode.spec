Summary:        Verify and sign routines for PE binaries
Name:           osslsigncode
Version:        2.7
Release:        1%{?dist}
License:        GPLv3
Group:          Applications/System
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://github.com/mtrojnar/%{name}/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  python3
BuildRequires:  cmake
BuildRequires:  openssl-devel
BuildRequires:  libcurl-devel
BuildRequires:  zlib-devel

%description
Verify and sign routines for PE binaries (EXE,DLL)

%prep
%autosetup -p1

%build
mkdir build
cd build
cmake -S ..
cmake --build .

%install
install -d %{buildroot}%{_bindir}
install -D -m 755 ./build/osslsigncode %{buildroot}%{_bindir}/osslsigncode

%files
%license LICENSE.txt
%{_bindir}/osslsigncode

%changelog
*   Tue Feb 13 2024 Cameron Baird <cameronbaird@microsoft.com.com> 2.7-1
-   Initial build for verification of Windows binaries.
-   License verified
