Vendor:         Microsoft Corporation
Distribution:   Mariner
%global _hardened_build 1
%global commit0 e60d4cca3d0e702c60ad0f9e2eecaa461baa4744

Name: libcli
Version: 1.9.7
Release: 1%{?dist}
Summary: A shared library for a Cisco-like cli
License: LGPLv2+
URL: https://github.com/dparrish/libcli
Source0: https://github.com/dparrish/libcli/archives/%{commit0}.tar.gz
Patch0: libcli-win32issue.patch

%package devel
Summary: Development files for libcli
Requires: %{name}%{?_isa} = %{version}-%{release}

BuildRequires:  gcc
%description
Libcli provides a shared library for including a Cisco-like command-line 
interface into other software. It's a telnet interface which supports 
command-line editing, history, authentication and callbacks for a 
user-definable function tree. 

%description devel
Libcli provides a shared library for including a Cisco-like command-line 
interface into other software. It's a telnet interface which supports 
command-line editing, history, authentication and callbacks for a 
user-definable function tree. 

These are the development files.

%prep
%setup -qn %{name}-%{commit0}

%patch0 -p1

%build

make %{?_smp_mflags}

%install
install -d -p %{buildroot}%{_includedir}
install -p -m 644 libcli*.h %{buildroot}%{_includedir}/
install -d -p %{buildroot}%{_libdir}
install -p -m 755 libcli.so.1.9.7 %{buildroot}%{_libdir}/
ln -s %{_libdir}/libcli.so.1.9.7 %{buildroot}%{_libdir}/libcli.so.1.9
ln -s %{_libdir}/libcli.so.1.9 %{buildroot}%{_libdir}/libcli.so

%ldconfig_scriptlets

%files
%doc COPYING
%{_libdir}/*.so.*

%files devel
%doc README
%{_libdir}/*.so
%{_includedir}/*.h

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.9.7-1
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.7-0.20160136gite60d4cc
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.7-0.20160135gite60d4cc
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.7-0.20160134gite60d4cc
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 14 2019 Björn Esser <besser82@fedoraproject.org> - 1.9.7-0.20160133gite60d4cc
- Rebuilt for libcrypt.so.2 (#1666033)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.7-0.20160132gite60d4cc
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.7-0.20160131gite60d4cc
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 1.9.7-0.20160130gite60d4cc
- Rebuilt for switch to libxcrypt

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.7-0.20160129gite60d4cc
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.7-0.20160128gite60d4cc
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.7-0.20160127gite60d4cc
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.7-0.20160126gite60d4cc
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 25 2016 Jason Taylor <jtfas90@gmail.com> - 1.9.7-0
- Updated to latest upstream stable commit
- Updates to spec file

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 02 2012 Jon Ciesla <limburgher@gmail.com> - 1.9.6-1
- Latest upstream.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 29 2011 Jon Ciesla <limb@jcomserv.net> - 1.9.5-3
- Corrected buildroot tag.

* Wed Nov 23 2011 Jon Ciesla <limb@jcomserv.net> - 1.9.5-2
- Added isa for -devel requires.
- Dropped setting of PREFIX from build section.
- Added README to -devel.

* Mon Oct 17 2011 Jon Ciesla <limb@jcomserv.net> - 1.9.5-1
- create.
