Summary:        The New GNU Portable Threads Library.
Name:           npth
Version:        1.7
Release:        1%{?dist}
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          System Environment/Libraries.
URL:            https://gnupg.org/software/npth/index.html
Source0:        https://gnupg.org/ftp/gcrypt/%{name}/%{name}-%{version}.tar.bz2

%description
This is a library to provide the GNU Pth API and thus a non-preemptive threads implementation.
In contrast to GNU Pth, it is based on the system's standard threads implementation.
This allows the use of libraries which are not compatible to GNU Pth.
Experience with a Windows Pth emulation showed that this is a solid way to provide
a co-routine based framework.

%package devel
Summary:       GNU npth development header and libraries.
Group:         Development/Libraries.
Requires:      %{name} = %{version}-%{release}

%description devel
Development package for npth.

%prep
%autosetup

%build
%configure \
    --disable-static
%make_build

%install
%make_install
find %{buildroot} -type f -name "*.la" -delete -print

%check
%make_build -k check

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%license AUTHORS COPYING.LIB
%{_bindir}/%{name}-config
%{_libdir}/libnpth.so.0*

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}.h
%{_libdir}/libnpth.so
%{_datadir}/aclocal/%{name}.m4

%changelog
* Fri Feb 23 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.7-1
- Auto-upgrade to 1.7 - Azure Linux 3.0 Upgrades

* Mon Nov 22 2021 Thomas Crain <thcrain@microsoft.com> - 1.6-4
- Use official URL/Source0 from gnupg.org
- Lint spec
- License verified

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.6-3
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.6-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Mon Sep 10 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 1.6-1
- Upgrade to 1.6.

* Tue Apr 11 2017 Danut Moraru <dmoraru@vmware.com> 1.3-1
- Initial Build.
