Vendor:         Microsoft Corporation
Distribution:   Mariner
%global apiversion 0.5

Name: libcmis
Version: 0.5.2
Release: 5%{?dist}
Summary: A C/C++ client library for CM interfaces

License: GPLv2+ or LGPLv2+ or MPLv1.1
URL: https://github.com/tdf/libcmis
Source: https://github.com/tdf/libcmis/releases/download/v%{version}/%{name}-%{version}.tar.xz

BuildRequires: boost-devel
BuildRequires: gcc-c++
BuildRequires: pkgconfig(cppunit)
BuildRequires: pkgconfig(libcurl)
BuildRequires: pkgconfig(libxml-2.0)
BuildRequires: xmlto

%description
LibCMIS is a C/C++ client library for working with CM (content management)
interfaces. The primary supported interface (which gave the library its
name) is CMIS, which allows applications to connect to any ECM behaving
as a CMIS server (Alfresco or Nuxeo are examples of open source ones).
Another supported interface is Google Drive.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package tools
Summary: Command line tool to access CMIS
Requires: %{name}%{?_isa} = %{version}-%{release}

%description tools
The %{name}-tools package contains a tool for accessing CMIS from the
command line.

%prep
%autosetup -p1

%build
%configure --disable-silent-rules --disable-static --disable-werror \
    DOCBOOK2MAN='xmlto man'
sed -i \
    -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
    -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' \
    libtool
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
rm -f %{buildroot}/%{_libdir}/*.la

%ldconfig_scriptlets

%check
export LD_LIBRARY_PATH=%{buildroot}/%{_libdir}${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
make %{?_smp_mflags} check

%files
%doc AUTHORS NEWS
%license COPYING.*
%{_libdir}/%{name}-%{apiversion}.so.*
%{_libdir}/%{name}-c-%{apiversion}.so.*

%files devel
%doc ChangeLog
%{_includedir}/%{name}-%{apiversion}
%{_includedir}/%{name}-c-%{apiversion}
%{_libdir}/%{name}-%{apiversion}.so
%{_libdir}/%{name}-c-%{apiversion}.so
%{_libdir}/pkgconfig/%{name}-%{apiversion}.pc
%{_libdir}/pkgconfig/%{name}-c-%{apiversion}.pc

%files tools
%{_bindir}/cmis-client
%{_mandir}/man1/cmis-client.1*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.5.2-5
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jan 25 2019 Jonathan Wakely <jwakely@redhat.com> - 0.5.2-2
- Rebuilt for Boost 1.69

* Thu Dec 27 2018 David Tardon <dtardon@redhat.com> - 0.5.2-1
- new upstream release

* Mon Dec 10 2018 Caolán McNamara <caolanm@redhat.com> - 0.5.1-14
- allow building with c++17

* Wed Sep 12 2018 Stephan Bergmann <sbergman@redhat.com> - 0.5.1-13
- fix Google Drive login

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 23 2018 Jonathan Wakely <jwakely@redhat.com> - 0.5.1-10
- Rebuilt for Boost 1.66

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 03 2017 Jonathan Wakely <jwakely@redhat.com> - 0.5.1-7
- Rebuilt for Boost 1.64

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Mon Feb 27 2017 David Tardon <dtardon@redhat.com> - 0.5.1-5
- Resolves: rhbz#1410197 work around infinite redirection loop

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 27 2017 Jonathan Wakely <jwakely@redhat.com> - 0.5.1-3
- Rebuilt for Boost 1.63

* Wed May 04 2016 David Tardon <dtardon@redhat.com> - 0.5.1-2
- fix Google Drive login

* Fri Mar 04 2016 David Tardon <dtardon@redhat.com> - 0.5.1-1
- new upstream release

* Wed Mar 02 2016 David Tardon <dtardon@redhat.com> - 0.5.0-12
- add a bunch of fixes for problems found by coverity

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 15 2016 Jonathan Wakely <jwakely@redhat.com> - 0.5.0-10
- Rebuilt for Boost 1.60

* Wed Sep 02 2015 Jonathan Wakely <jwakely@redhat.com> 0.5.0-9
- Patched and rebuilt for Boost 1.59

* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-8
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159

* Fri Jul 24 2015 Adam Williamson <awilliam@redhat.com> - 0.5.0-7
- rebuild for Boost 1.58 (for f23, for real this time)

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 0.5.0-6
- rebuild for Boost 1.58

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Apr 12 2015 David Tardon <dtardon@redhat.com> - 0.5.0-4
- rebuild for yet another C++ ABI break

* Fri Feb 20 2015 David Tardon <dtardon@redhat.com> - 0.5.0-3
- rebuild for C++ stdlib ABI change in gcc5

* Tue Jan 27 2015 Petr Machata <pmachata@redhat.com> - 0.5.0-2
- Rebuild for boost 1.57.0

* Sun Dec 21 2014 David Tardon <dtardon@redhat.com> - 0.5.0-1
- new upstream release

* Fri Sep 05 2014 David Tardon <dtardon@redhat.com> - 0.4.1-8
- coverity: fix mismatching exceptions

* Thu Sep 04 2014 David Tardon <dtardon@redhat.com> - 0.4.1-7
- a few use-after-free fixes for the C wrapper

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 Petr Machata <pmachata@redhat.com> - 0.4.1-4
- Rebuild for boost 1.55.0

* Fri Feb 28 2014 David Tardon <dtardon@redhat.com> - 0.4.1-3
- Resolves: rhbz#1070691 test failing on big endians

* Thu Nov 21 2013 David Tardon <dtardon@redhat.com> - 0.4.1-2
- disable tests on arm

* Wed Nov 06 2013 David Tardon <dtardon@redhat.com> - 0.4.1-1
- new upstream release

* Fri Aug 30 2013 David Tardon <dtardon@redhat.com> - 0.3.1-8
- Resolves: rhbz#1000819 pkgconfig file for libcmis-c is broken

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 27 2013 pmachata@redhat.com - 0.3.1-6
- Rebuild for boost 1.54.0

* Wed Apr 24 2013 David Tardon <dtardon@redhat.com> - 0.3.1-5
- Resolves: rhbz#918079 libcmis::sha1() can return digests with fewer
  than 40 hexadecimal digits
- Resolves: rhbz#918080 restrict redirection protocols

* Mon Apr 08 2013 David Tardon <dtardon@redhat.com> - 0.3.1-4
- Resolves: rhbz#918044 memory leaks on exception path in C wrapper

* Sun Feb 10 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 0.3.1-3
- Rebuild for Boost-1.53.0

* Sat Feb 09 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 0.3.1-2
- Rebuild for Boost-1.53.0

* Mon Feb 04 2013 David Tardon <dtardon@redhat.com> - 0.3.1-1
- new release

* Wed Dec 19 2012 David Tardon <dtardon@redhat.com> - 0.3.0-6
- use xmlto for generating man page

* Sat Dec 08 2012 David Tardon <dtardon@redhat.com> - 0.3.0-5
- another pointless bump

* Fri Dec 07 2012 David Tardon <dtardon@redhat.com> - 0.3.0-4
- another pointless rebuild

* Fri Dec 07 2012 David Tardon <dtardon@redhat.com> - 0.3.0-3
- pointless rebuild

* Fri Dec 07 2012 David Tardon <dtardon@redhat.com> - 0.3.0-2
- force rebuild

* Thu Dec 06 2012 David Tardon <dtardon@redhat.com> - 0.3.0-1
- new upstream release

* Tue Nov 06 2012 Caolán McNamara <caolanm@redhat.com> - 0.2.3-4
- clarify license

* Fri Jul 27 2012 David Tardon <dtardon@redhat.com> - 0.2.3-3
- rebuilt for boost 1.50

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 28 2012 David Tardon <dtardon@redhat.com> - 0.2.3-1
- new upstream version

* Wed Jun 20 2012 David Tardon <dtardon@redhat.com> - 0.2.2-1
- latest upstream version

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-2
- Rebuilt for c++ ABI breakage

* Wed Dec 21 2011 David Tardon <dtardon@redhat.com> 0.1.0-1
- initial import
