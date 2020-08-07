Summary:	Program shows full path of (shell) commands
Name:		which
Version:	2.21
Release:        7%{?dist}
License:	GPLv3+
URL:		http://savannah.gnu.org/projects/which
Source0:	http://ftp.gnu.org/gnu/which/%{name}-%{version}.tar.gz
%define sha1 which=6b6bec3d2b3d4661c164feb81b9b1d22d1359ded
Group:		Development/Tools
Vendor:         Microsoft Corporation
Distribution:   Mariner
Conflicts:      toybox
%description
Program for showing the full the path of (shell) commands.
%prep
%setup -q
%build
%configure
%make_build
%install
%make_install
rm -rf %{buildroot}%{_infodir}
%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/*
%{_mandir}/man1/*
%changelog
* Sat May 09 00:21:25 PST 2020 Nick Samson <nisamson@microsoft.com> - 2.21-7
- Added %%license line automatically

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.21-6
-   Initial CBL-Mariner import from Photon (license: Apache2).
* Thu Oct 19 2017 Alexey Makhalov <amakhalov@vmware.com> 2.21-5
- Remove infodir
- Use standard configure/build macros
* Mon Oct 02 2017 Alexey Makhalov <amakhalov@vmware.com> 2.21-4
- Added conflicts toybox
* Mon Oct 10 2016 ChangLee <changlee@vmware.com> 2.21-3
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.21-2
- GA - Bump release of all rpms
* Wed Jan 20 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.21-1
- Update to 2.21-1.
* Wed Oct 21 2014 Divya Thaluru <dthaluru@vmware.com> 2.20-1
- Initial build. First version
