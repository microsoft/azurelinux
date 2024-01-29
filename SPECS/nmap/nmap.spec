Summary:        Nmap Network Mapper
Name:           nmap
Version:        7.94
Release:        1%{?dist}
License:        Nmap
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://nmap.org/
Source0:        https://nmap.org/dist/%{name}-%{version}.tar.bz2
BuildRequires:  binutils
BuildRequires:  gcc
BuildRequires:  kernel-headers
BuildRequires:  libpcap-devel
BuildRequires:  libssh2-devel
BuildRequires:  lua-devel
BuildRequires:  make
BuildRequires:  openssl-devel
BuildRequires:  zlib-devel

Patch1:         remove_openssl_macro.patch

%description
Nmap ("Network Mapper") is a free and open source utility for network discovery and security auditing.

%package ncat
Summary:        Nmap replacement for ncat
Provides:       nc

%description ncat
Nmap implementation of the ncat tool

%prep
%autosetup -p1

# Remove bundled copies of several libraries. Leave pcre since we dont have a static version.
rm -rf libpcap macosx mswin32 libssh2 libz

%build
%configure
%make_build

%install
%make_install

rm -rf %{buildroot}%{_datadir}/ncat
ln -s ncat %{buildroot}%{_bindir}/nc

%files
%license LICENSE
%exclude %{_mandir}
%{_bindir}/nmap
%{_bindir}/nping
%{_datadir}/nmap

%files ncat
%license LICENSE
%{_bindir}/ncat
%{_bindir}/nc

%changelog
* Mon Jan 29 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 7.94-1
- Auto-upgrade to 7.94 - none

* Mon Apr 17 2023 Saul Paredes <saulparedes@microsoft.com> - 7.93-1
- Upgrading to latest version to fix CVE-2018-25032

* Wed Feb 16 2022 Max Brodeur-Urbas <maxbr@microsoft.com> - 7.92-1
- Upgrading to latest version.

* Tue Aug 10 2021 Jon Slobodzian <joslobo@microsoft.com> 7.90-3
- Bumped version for merge.

* Mon May 17 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> 7.90-2 (merge from 1.0 branch)
- nmap-unix_crash.patch fix for crash with unix sockets.

* Mon May 03 2021 Thomas Crain <thcrain@microsoft.com> - 7.90-2
- Remove zenmap/ndiff from configuration 

* Tue Feb 02 2021 Henry Beberman <henry.beberman@microsoft.com> - 7.90-1
- Add nmap spec
- License verified
- Original version for CBL-Mariner
