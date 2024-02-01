%global python3_pkgversion 3
Name:           scons
Version:        4.6.0
Release:        3%{?dist}
Summary:        An Open Source software construction tool
Group:          Development/Tools
License:        MIT
URL:            http://scons.org
Source0:        https://sourceforge.net/projects/scons/files/scons/4.6.0/scons-4.6.0.tar.gz
Patch0:         0001-Remove-unnecessary-build-deps.patch
Vendor:         Microsoft Corporation
Distribution:   Mariner
BuildRequires:  python%{python3_pkgversion}-devel 
BuildRequires:  python%{python3_pkgversion}-pip
Requires:       python3
BuildArch:      noarch

%description
SCons is an Open Source software construction tool—that is, a next-generation build tool.
Think of SCons as an improved, cross-platform substitute for the classic Make utility
with integrated functionality similar to autoconf/automake and compiler caches such as ccache.
In short, SCons is an easier, more reliable and faster way to build software.

%prep
%autosetup -p1 -n SCons-%{version}

%build
%py3_build

%install
%{py3_install "--prefix=%{_prefix}" "--standard-lib" "--install-data=%{_datadir}"}
%py3_shebang_fix %{buildroot}%{_bindir}/*

%files
%defattr(-,root,root,-)
%license LICENSE.txt
%{python3_sitelib}/*
%{_bindir}/*
%{_datadir}/*

%changelog
* Thu Jan 18 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 4.6.0-1
- Auto-upgrade to 4.6.0 - For 3.0 release

* Thu Feb 17 2022 Thomas Crain <thcrain@microsoft.com> - 3.0.1-6
- Build with python3 instead of python2

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.0.1-5
- Removing the explicit %%clean stage.
- License verified.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 3.0.1-4
- Added %%license line automatically

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 3.0.1-3
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Mon Jan 07 2019 Alexey Makhalov <amakhalov@vmware.com> 3.0.1-2
-   BuildRequires: python2
*   Tue Sep 18 2018 Srinidhi Rao <srinidhir@vmware.com> 3.0.1-1
-   Upgraded to version 3.0.1
*   Sun Oct 15 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.5.1-1
-   Initial build.  First version
