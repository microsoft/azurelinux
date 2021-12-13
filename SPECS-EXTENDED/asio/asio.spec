Vendor:         Microsoft Corporation
Distribution:   Mariner
# asio only ships headers, so no debuginfo package is needed
%global debug_package %{nil}

%global commit 28d9b8d6df708024af5227c551673fdb2519f5bf
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           asio
Version:        1.10.8
Release:        12%{?dist}
Summary:        A cross-platform C++ library for network programming

License:        Boost
URL:            https://think-async.com
Source0:        https://github.com/chriskohlhoff/%{name}/archive/%{commit}.tar.gz#/%{name}-%{shortcommit}.tar.gz

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  openssl-devel
BuildRequires:  boost-devel
BuildRequires:  perl-generators

%description
The asio package contains a cross-platform C++ library for network programming
that provides developers with a consistent asynchronous I/O model using a
modern C++ approach.

%package devel
Summary:        Header files for asio
Requires:       openssl-devel
Requires:       boost-devel

%description devel
Header files you can use to develop applications with asio.

The asio package contains a cross-platform C++ library for network programming
that provides developers with a consistent asynchronous I/O model using a
modern C++ approach.

%prep
%setup -qn %{name}-%{commit}/%{name}

%build
./autogen.sh
%configure
%make_build

%install
%make_install

%files devel
%doc src/doc/*
%license LICENSE_1_0.txt
%{_includedir}/asio/
%{_includedir}/asio.hpp

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.10.8-12
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.8-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.8-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 03 2017 Jonathan Wakely <jwakely@redhat.com> - 1.10.8-4
- Rebuilt for Boost 1.64

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 27 2017 Jonathan Wakely <jwakely@redhat.com> - 1.10.8-2
- Rebuilt for Boost 1.63

* Sun Dec 11 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.10.8-1
- Update to 1.10.8

* Tue Sep 13 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.10.7-1
- Update to 1.10.7

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 14 2016 Jonathan Wakely <jwakely@redhat.com> - 1.10.6-6
- Rebuilt for Boost 1.60

* Sat Jan 02 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.10.6-5
- Remove useless pieces of the spec
- Conform to more recent SPEC style
- Fix date in changelog that was giving warnings

* Sat Jan 02 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.10.6-4
- Move from define to global

* Thu Aug 27 2015 Jonathan Wakely <jwakely@redhat.com> - 1.10.6-3
- Rebuilt for Boost 1.59

* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.6-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159

* Sun Jul 26 2015 Fabio Alessandro Locati <fale@fedoraproject.org> -1.10.6-1
- Update to 1.10.6 version

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 1.10.4-5
- rebuild for Boost 1.58

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jan 26 2015 Petr Machata <pmachata@redhat.com> - 1.10.4-3
- Rebuild for boost 1.57.0

* Sat Oct 11 2014 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.10.4-2
- Forgot to update the commit id

* Sat Oct 11 2014 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.10.4-1
- Update to 1.10.4 version

* Sun Aug 10 2014 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.10.3-1
- Update to 1.10.3 version

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 Petr Machata <pmachata@redhat.com> - 1.4.8-8
- Rebuild for boost 1.55.0

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 30 2013 Petr Machata <pmachata@redhat.com> - 1.4.8-6
- Rebuild for boost 1.54.0

* Sun Feb 10 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.4.8-5
- Rebuild for Boost-1.53.0

* Sat Feb 09 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.4.8-4
- Rebuild for Boost-1.53.0

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Aug  3 2011 Peter Robinson <pbrobinson@gmail.com> - 1.4.8-1
- Update to 1.4.8 bugfix release

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jun 18 2010 Dan Horák <dan[at]danny.cz> 1.4.1-3
- fix FTBFS #538893 and #599857 (patch by Petr Machata)

* Mon Jul 27 2009 Marc Maurer <uwog@uwog.net> 1.4.1-2
- The tarball is now a gzip archive

* Mon Jul 27 2009 Marc Maurer <uwog@uwog.net> 1.4.1-1
- New upstream release

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec 25 2008 Marc Maurer <uwog@uwog.net> 1.2.0-1
- New upstream release

* Sun Apr 06 2008 Marc Maurer <uwog@uwog.net> 1.0.0-2
- Upstream removed the executable permissions on the docs

* Sun Apr 06 2008 Marc Maurer <uwog@uwog.net> 1.0.0-1
- New upstream release

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.3.8-8
- Autorebuild for GCC 4.3

* Sun Dec 02 2007 Marc Maurer <uwog@uwog.net> 0.3.8-7
- Rebuild to include a tarball with original timestamps

* Thu Nov 29 2007 Marc Maurer <uwog@uwog.net> 0.3.8-6
- Use release %%{?dist} tag
- Move BuildRequires to the main package
- Preserve timestamps
- Remove spurious executable permissions from documentation

* Wed Nov 28 2007 Marc Maurer <uwog@uwog.net> 0.3.8-5
- Don't require a nonexisting %%{name} package for -devel
- Add openssl-devel and boost-devel to the buildRequires list
- Remove unused post/postun sections for now
- Fix -devel description
- Use %%{version} in source URL
- Add COPYING to the doc section
- Preserve timestamps of installed files
- Use %%defattr(-,root,root,-)
- Include developer documentation
- Move the make call to the %%check section

* Sun Nov 25 2007 Marc Maurer <uwog@uwog.net> 0.3.8-4
- Don't use BA noarch

* Fri Nov 23 2007 Marc Maurer <uwog@uwog.net> 0.3.8-3
- Move the license file to the -devel package, so no
  main package will be created for now
- Added BuildArch: noarch

* Fri Nov 23 2007 Marc Maurer <uwog@uwog.net> 0.3.8-2
- Make BuildRoot fedora packaging standard compliant
- Disable building of debuginfo packages
- Include full source URL

* Wed Nov 21 2007 Marc Maurer <uwog@uwog.net> 0.3.8-1
- Initial spec file
