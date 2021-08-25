Summary:        Change rpath of binaries
Name:           chrpath
Version:        0.16
Release:        4%{?dist}
License:        GPLv2
URL:            https://chrpath.alioth.debian.org/
Group:          Development/Tools
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://alioth-archive.debian.org/releases/%{name}/%{name}/%{version}/%{name}-%{version}.tar.gz

%description
Command line tool to adjust the RPATH or RUNPATH of ELF binaries.

%prep
%setup -q


%build
%configure
make %{?_smp_mflags}

%check
make check

%install
make install DESTDIR=%{buildroot} INSTALL="install -p"
rm -rf %{buildroot}/usr/doc


%files
%license COPYING
%doc AUTHORS README NEWS ChangeLog* COPYING
%{_bindir}/chrpath
%{_mandir}/man1/chrpath.1*

%changelog
* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 0.16-4
- Added %%license line automatically

*   Tue Apr 07 2020 Paul Monson <paulmon@microsoft.com> 0.16-3
-   Fix Source0. License verified.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 0.16-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Wed Apr 05 2017 Anish Swaminathan <anishs@vmware.com> 0.16-1
-   Initial packaging
