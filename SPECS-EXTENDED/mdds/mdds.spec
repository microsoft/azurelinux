Vendor:         Microsoft Corporation
Distribution:   Azure Linux
# header-only library
%global debug_package %{nil}

%global apiversion 1.5

Name: mdds
Version: 1.5.0
Release: 3%{?dist}
Summary: A collection of multi-dimensional data structures and indexing algorithms

License: MIT
URL: https://gitlab.com/mdds/mdds
Source0: https://kohei.us/files/%{name}/src/%{name}-%{version}.tar.bz2

BuildRequires: boost-devel
BuildRequires: gcc-c++
BuildRequires: autoconf

%description
%{name} is a collection of multi-dimensional data structures and
indexing algorithms.

%package devel
Summary: Headers for %{name}
BuildArch: noarch
Requires: boost-devel
Provides: %{name}-static = %{version}-%{release}

%description devel
%{name} is a collection of multi-dimensional data structures and
indexing algorithms.
 
It implements the following data structures:
* segment tree
* flat segment tree 
* rectangle set
* point quad tree
* multi type matrix
* multi type vector

See README.md for a brief description of the structures.

%prep
%autosetup -p1

%build
autoconf
%configure

%install
%make_install
rm -rf %{buildroot}%{_docdir}/%{name}

%check
make check %{?_smp_mflags}

%files devel
%{_includedir}/%{name}-%{apiversion}
%{_datadir}/pkgconfig/%{name}-%{apiversion}.pc
%doc AUTHORS README.md
%license LICENSE

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.5.0-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Aug 15 2019 Caolán McNamara <caolanm@redhat.com> - 1.5.0-1
- new upstream release

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jan 25 2019 Jonathan Wakely <jwakely@redhat.com> - 1.4.3-2
- Rebuilt for Boost 1.69

* Wed Oct 31 2018 Caolán McNamara <caolanm@redhat.com> - 1.4.3-1
- new upstream release

* Wed Sep 19 2018 Caolán McNamara <caolanm@redhat.com> - 1.4.2-1
- new upstream release

* Tue Aug 28 2018 Caolán McNamara <caolanm@redhat.com> - 1.4.1-1
- new upstream release

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 23 2018 Jonathan Wakely <jwakely@redhat.com> - 1.3.0-2
- Rebuilt for Boost 1.66

* Wed Nov 01 2017 David Tardon <dtardon@redhat.com> - 1.3.0-1
- new upstream release

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 03 2017 Jonathan Wakely <jwakely@redhat.com> - 1.2.3-2
- Rebuilt for Boost 1.64

* Thu May 25 2017 David Tardon <dtardon@redhat.com> - 1.2.3-1
- new upstream release

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 27 2017 Jonathan Wakely <jwakely@redhat.com> - 1.2.2-2
- Rebuilt for Boost 1.63

* Mon Sep 12 2016 David Tardon <dtardon@redhat.com> - 1.2.2-1
- new upstream release

* Mon Jun 27 2016 David Tardon <dtardon@redhat.com> - 1.2.1-1
- new upstream release

* Wed Jun 22 2016 David Tardon <dtardon@redhat.com> - 1.2.0-2
- fix double delete in mtv::swap

* Thu May 12 2016 David Tardon <dtardon@redhat.com> - 1.2.0-1
- new upstream release

* Fri Feb 12 2016 David Tardon <dtardon@redhat.com> - 1.1.0-1
- new upstream release

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 15 2016 Jonathan Wakely <jwakely@redhat.com> - 0.12.1-6
- Rebuilt for Boost 1.60

* Thu Aug 27 2015 Jonathan Wakely <jwakely@redhat.com> - 0.12.1-5
- Rebuilt for Boost 1.59

* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.1-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 0.12.1-3
- rebuild for Boost 1.58

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 12 2015 David Tardon <dtardon@redhat.com> - 0.12.1-1
- new upstream release

* Thu Mar 05 2015 David Tardon <dtardon@redhat.com> - 0.12.0-2
- add missing includes

* Tue Feb 17 2015 David Tardon <dtardon@redhat.com> - 0.12.0-1
- new upstream release

* Thu Jan 29 2015 David Tardon <dtardon@redhat.com> - 0.11.2-3
- fix includes in header file

* Tue Jan 27 2015 Petr Machata <pmachata@redhat.com> - 0.11.2-2
- Rebuild for boost 1.57.0

* Sun Dec 21 2014 David Tardon <dtardon@redhat.com> - 0.11.2-1
- new upstream release

* Fri Oct 03 2014 David Tardon <dtardon@redhat.com> - 0.11.1-1
- new bugfix release

* Mon Sep 22 2014 David Tardon <dtardon@redhat.com> - 0.11.0-1
- new upstream release

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 Petr Machata <pmachata@redhat.com> - 0.10.3-2
- Rebuild for boost 1.55.0

* Thu Apr 24 2014 David Tardon <dtardon@redhat.com> - 0.10.3-1
- new upstream release

* Thu Feb 13 2014 David Tardon <dtardon@redhat.com> - 0.10.2-1
- new bugfix release

* Thu Jan 09 2014 David Tardon <dtardon@redhat.com> - 0.10.1-1
- new upstream release

* Tue Jan 07 2014 David Tardon <dtardon@redhat.com> - 0.10.0-1
- new upstream release

* Wed Nov 06 2013 David Tardon <dtardon@redhat.com> - 0.9.1-1
- new upstream release

* Wed Sep 04 2013 David Tardon <dtardon@redhat.com> - 0.8.1-5
- run tests on all platforms

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 30 2013 Petr Machata <pmachata@redhat.com> - 0.8.1-3
- Rebuild for boost 1.54.0

* Mon Jun 10 2013 David Tardon <dtardon@redhat.com> - 0.8.1-2
- trivial changes

* Tue May 21 2013 David Tardon <dtardon@redhat.com> - 0.8.1-1
- new release

* Tue May 14 2013 David Tardon <dtardon@redhat.com> - 0.8.0-1
- new release

* Mon Mar 18 2013 David Tardon <dtardon@redhat.com> - 0.7.1-1
- new release

* Thu Feb 28 2013 David Tardon <dtardon@redhat.com> - 0.7.0-1
- new release

* Sun Feb 10 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 0.6.1-3
- Rebuild for Boost-1.53.0

* Sat Feb 09 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 0.6.1-2
- Rebuild for Boost-1.53.0

* Tue Sep 18 2012 David Tardon <dtardon@redhat.com> - 0.6.1-1
- new version

* Sat Jul 28 2012 David Tardon <dtardon@redhat.com> - 0.6.0-2
- rebuilt for boost 1.50

* Mon Jul 23 2012 David Tardon <dtardon@redhat.com> - 0.6.0-1
- new version

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 18 2011 David Tardon <dtardon@redhat.com> - 0.5.4-1
- new version

* Thu Jul 14 2011 David Tardon <dtardon@redhat.com> - 0.5.3-1
- new version

* Wed Mar 30 2011 David Tardon <dtardon@redhat.com> - 0.5.2-2
- install license

* Tue Mar 29 2011 David Tardon <dtardon@redhat.com> - 0.5.2-1
- new version

* Thu Mar 24 2011 David Tardon <dtardon@redhat.com> - 0.5.1-3
- Resolves: rhbz#680766 fix a crash and two other bugs

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 08 2011 David Tardon <dtardon@redhat.com> - 0.5.1-1
- new version

* Tue Dec 21 2010 David Tardon <dtardon@redhat.com> - 0.4.0-1
- new version

* Tue Nov 16 2010 David Tardon <dtardon@redhat.com> - 0.3.1-1
- new version

* Wed Jul 07 2010 Caolán McNamara <caolanm@redhat.com> - 0.3.0-2
- rpmlint warnings

* Wed Jun 30 2010 David Tardon <dtardon@redhat.com> - 0.3.0-1
- initial import
