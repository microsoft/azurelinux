Summary:        File manager
Name:           mc
Version:        4.8.27
Release:        2%{?dist}
License:        GPLv3+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://www.midnight-commander.org
Source0:        http://ftp.midnight-commander.org/%{name}-%{version}.tar.xz
Patch0:         disable-extfs-test.patch
BuildRequires:  glib-devel
BuildRequires:  pcre-devel
BuildRequires:  python3-devel
BuildRequires:  slang-devel
Requires:       glib
Requires:       pcre
Requires:       slang

%description
MC (Midnight Commander) is a text-mode full-screen file manager and visual shell

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install
%py3_shebang_fix %{buildroot}%{_libexecdir}/mc/extfs.d/{s3+,uc1541}

%check
%make_build -k check

%files
%defattr(-,root,root)
%license COPYING
%{_sysconfdir}/*
%{_bindir}/*
%exclude %{_libdir}
%{_libexecdir}/*
%{_datadir}/*
%exclude %{_prefix}/src

%changelog
* Tue Jul 12 2022 Olivia Crain <oliviacrain@microsoft.com> - 4.8.27-2
- Fix unversioned python shebangs in extfs helpers

* Mon Nov 01 2021 Olivia Crain <oliviacrain@microsoft.com> - 4.8.27-1
- Upgrade to latest version to fix CVE-2021-36370
- License verified

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 4.8.21-4
- Added %%license line automatically

* Tue Apr 21 2020 Eric Li <eli@microsoft.com> - 4.8.21-3
- Fix Source0: and delete sha1. License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 4.8.21-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Thu Sep 06 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> - 4.8.21-1
- Update to version 4.8.21

* Fri Aug 18 2017 Dheeraj Shetty <dheerajs@vmware.com> - 4.8.19-2
- Disable extfs test

* Fri Mar 31 2017 Michelle Wang <michellew@vmware.com> - 4.8.19-1
- Update package version

* Tue Jul 12 2016 Alexey Makhalov <amakhalov@vmware.com> - 4.8.17-1
- Initial build. First version
