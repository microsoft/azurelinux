# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%define _hardened_build 1
Name:           stress
Version:        1.0.7
Release:        7%{?dist}
Summary:        A tool to put given subsystems under a specified load

License:        GPL-2.0-or-later
URL:            https://github.com/resurrecting-open-source-projects/stress
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
BuildRequires: make
BuildRequires: gcc
BuildRequires: autoconf automake

%description
stress is not a benchmark, but is rather a tool designed to put given
subsytems under a specified load. Instances in which this is useful
include those in which a system administrator wishes to perform tuning
activities, a kernel or libc programmer wishes to evaluate denial of 
service possibilities, etc.

%prep
%setup -q
chmod -x README TODO AUTHORS NEWS src/stress.c

%build
./autogen.sh
%configure
%make_build


%install
%make_install

rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%files
%doc AUTHORS ChangeLog COPYING NEWS README TODO
%{_bindir}/stress
%{_mandir}/man1/stress.1*


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Mar 01 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.0.7-2
- migrated to SPDX license

* Mon Jan 23 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.0.7-1
- 1.0.7

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan 18 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.0.6-1
- 1.0.6

* Tue Dec 06 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.0.5-1
- 1.0.5

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jan 28 2021 Timm Bäder <tbaeder@redhat.com> - 1.0.4-28
- Use make macros
- https://docs.fedoraproject.org/en-US/packaging-guidelines/#_parallel_make

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-26
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Nov 16 2017 Gwyn Ciesla <limburgher@gmail.com> - 1.0.4-19
- Updated to new upstream tarball.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Feb 26 2014 Jon Ciesla <limburgher@gmail.com> - 1.0.4-11
- Update URL and Source0, BZ 1070090.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Apr 13 2012 Jon Ciesla <limburgher@gmail.com> - 1.0.4-7
- Add hardened build.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri May 07 2010 Jon Ciesla <limb@jcomserv.net> - 1.0.4-4
- Info requires fix, dropped INSTALL.

* Thu May 06 2010 Jon Ciesla <limb@jcomserv.net> - 1.0.4-3
- Corrected license tag.
- Moved chmod to setup.

* Thu May 06 2010 Jon Ciesla <limb@jcomserv.net> - 1.0.4-2
- Fixed spurious executable perms.

* Wed May 05 2010 Jon Ciesla <limb@jcomserv.net> - 1.0.4-1
- First build.
