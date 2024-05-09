%global apiversion 0.10

Summary:        A library for import of WordPerfect documents
Name:           libwpd
Version:        0.10.3
Release:        6%{?dist}
License:        LGPLv2+ OR MPLv2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://libwpd.sf.net/
Source:         https://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.xz
Patch0:         libwpd-gcc11.patch
BuildRequires:  boost-devel
BuildRequires:  doxygen
BuildRequires:  gcc-c++
BuildRequires:  help2man
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(librevenge-0.0)
BuildRequires:  pkgconfig(librevenge-generators-0.0)
BuildRequires:  pkgconfig(librevenge-stream-0.0)
BuildRequires:  pkgconfig(zlib)

%description
%{name} is a library for import of WordPerfect documents.

%package tools
Summary:        Tools to transform WordPerfect documents into other formats
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description tools
Tools to transform WordPerfect documents into other formats.
Currently supported: HTML, raw, text.

%package devel
Summary:        Files for developing with libwpd
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Includes and definitions for developing with libwpd.

%package doc
Summary:        Documentation of %{name} API
BuildArch:      noarch

%description doc
The %{name}-doc package contains API documentation for %{name}.

%prep
%autosetup -p1

%build
%configure --disable-static --disable-silent-rules
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -type f -name "*.la" -delete -print
# we install API docs directly from build
rm -rf %{buildroot}/%{_docdir}/%{name}

# generate and install man pages
export LD_LIBRARY_PATH=%{buildroot}%{_libdir}${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
for tool in wpd2html wpd2raw wpd2text; do
    help2man -N -S '%{name} %{version}' -o ${tool}.1 %{buildroot}%{_bindir}/${tool}
done
install -m 0755 -d %{buildroot}/%{_mandir}/man1
install -m 0644 wpd2*.1 %{buildroot}/%{_mandir}/man1

%ldconfig_scriptlets

%files
%doc CREDITS NEWS README
%license COPYING.LGPL COPYING.MPL
%{_libdir}/%{name}-%{apiversion}.so.*

%files tools
%{_bindir}/wpd2html
%{_bindir}/wpd2raw
%{_bindir}/wpd2text
%{_mandir}/man1/wpd2html.1*
%{_mandir}/man1/wpd2raw.1*
%{_mandir}/man1/wpd2text.1*

%files devel
%doc HACKING TODO
%{_libdir}/%{name}-%{apiversion}.so
%{_libdir}/pkgconfig/%{name}-%{apiversion}.pc
%{_includedir}/%{name}-%{apiversion}

%files doc
%license COPYING.LGPL COPYING.MPL
%doc docs/doxygen/html
%doc docs/%{name}.dia
%doc docs/%{name}.png

%changelog
* Tue Dec 27 2022 Muhammad Falak <mwani@microsoft.com> - 0.10.3-6
- Introduce patch to fix build with gcc11
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.10.3-5
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Dec 29 2018 David Tardon <dtardon@redhat.com> - 0.10.3-1
- new upstream release

* Tue Oct 30 2018 Caolán McNamara <caolanm@redhat.com> - 0.10.2-4
- Resolves: rhbz#1643752 crash in specific wpd file

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Sep 12 2017 David Tardon <dtardon@redhat.com> - 0.10.2-1
- new upstream release

* Thu Sep 07 2017 Caolán McNamara <caolanm@redhat.com> - 0.10.1-8
- Related: rhbz#1489337 extend to earlier file format version

* Thu Sep 07 2017 Caolán McNamara <caolanm@redhat.com> - 0.10.1-7
- Resolves: rhbz#1489337 crashing wpd

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Dec 30 2015 David Tardon <dtardon@redhat.com> - 0.10.1-1
- new upstream release

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.10.0-4
- Rebuilt for GCC 5 C++11 ABI change

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 26 2014 David Tardon <dtardon@redhat.com> - 0.10.0-1
- new upstream release

* Wed Apr 09 2014 David Tardon <dtardon@redhat.com> - 0.9.9-2
- generate man pages

* Mon Aug 19 2013 David Tardon <dtardon@redhat.com> - 0.9.9-1
- new release

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 21 2013 David Tardon <dtardon@redhat.com> - 0.9.8-2
- drop build dep on libgsf-devel that has not been needed for years

* Tue May 14 2013 David Tardon <dtardon@redhat.com> - 0.9.8-1
- new release

* Sun Apr 21 2013 David Tardon <dtardon@redhat.com> - 0.9.7-1
- new release

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Sep 25 2012 David Tardon <dtardon@redhat.com> - 0.9.6-1
- new release

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4-3
- Rebuilt for c++ ABI breakage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 08 2011 Caolán McNamara <caolanm@redhat.com> - 0.9.4-1
- latest version

* Sun May 22 2011 Caolán McNamara <caolanm@redhat.com> - 0.9.2-1
- latest version
- drop integrated libwpd-gcc4.6.0.patch

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 24 2011 Caolán McNamara <caolanm@redhat.com> - 0.9.1-1
- latest version

* Sun Dec 05 2010 Caolán McNamara <caolanm@redhat.com> - 0.9.0-1
- latest version

* Sat Feb 13 2010 Caolán McNamara <caolanm@redhat.com> - 0.8.14-5
- Resolves: rhbz#226060 merge review

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 06 2009 Lubomir Rintel <lkundrak@v3.sk> - 0.8.14-2
- Rebuild for provides

* Wed Feb 13 2008 Caolán McNamara <caolanm@redhat.com> - 0.8.14-1
- next version

* Mon Dec 17 2007 Caolán McNamara <caolanm@redhat.com> - 0.8.13-2
- strangely 0.8.13-1 never appeared in rawhide

* Thu Dec 13 2007 Caolán McNamara <caolanm@redhat.com> - 0.8.13-1
- next version

* Sat Oct 13 2007 Caolán McNamara <caolanm@redhat.com> - 0.8.12-1
- next version

* Fri Aug 24 2007 Caolán McNamara <caolanm@redhat.com> - 0.8.11-1
- next version

* Fri Aug 03 2007 Caolán McNamara <caolanm@redhat.com> - 0.8.10-2
- clarify license

* Fri Jun 15 2007 Caolán McNamara <caolanm@redhat.com> - 0.8.10-1
- next version

* Tue Mar 27 2007 Caolán McNamara <caolanm@redhat.com> - 0.8.9-2
- Resolves: rhbz#233876: add unowned directory fix from Michael Schwendt 

* Fri Mar 16 2007 Caolán McNamara <caolanm@redhat.com> - 0.8.9-1
- next version

* Fri Feb 09 2007 Caolán McNamara <caolanm@redhat.com> - 0.8.8-2
- spec cleanups

* Thu Jan 11 2007 Caolán McNamara <caolanm@redhat.com> - 0.8.8-1
- next version

* Mon Oct 09 2006 Caolán McNamara <caolanm@redhat.com> - 0.8.7-1
- next version

* Mon Jul 17 2006 Caolán McNamara <caolanm@redhat.com> - 0.8.6-1
- next version

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.8.5-3.1
- rebuild

* Sun Jun 11 2006  Caolán McNamara <caolanm@redhat.com> 0.8.5-3
- add wp5nofontlistcrash

* Fri Jun 02 2006  Caolán McNamara <caolanm@redhat.com> 0.8.5-2
- build through brew

* Thu Jun 01 2006  Caolán McNamara <caolanm@redhat.com> 0.8.5-1
- next version

* Tue Mar 21 2006  Caolán McNamara <caolanm@redhat.com> 0.8.4-2
- rebuild for libgsf

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.8.4-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.8.4-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com> 0.8.4-1.1
- rebuilt

* Fri Dec 02 2005 Caolán McNamara <caolanm@redhat.com> 0.8.4-1
- next version

* Fri Dec 02 2005 Caolán McNamara <caolanm@redhat.com> 0.8.3-2
- rebuild because of libgsf

* Tue Jun 28 2005 Caolán McNamara <caolanm@redhat.com> 0.8.3-1
- update to latest libwpd

* Tue Jun 28 2005 Caolán McNamara <caolanm@redhat.com> 0.8.2-2.fc5
- export to other formats twiddle

* Wed Jun 22 2005 Caolán McNamara <caolanm@redhat.com> 0.8.2-1
- bump to latest version

* Fri Apr 29 2005 Caolán McNamara <caolanm@redhat.com> 0.8.1-1
- bump to latest version kudos Fridrich Strba
- drop integrated patch

* Wed Apr  6 2005 Caolán McNamara <caolanm@redhat.com> 0.8.0-4
- add libwpd devel provided patch for endless loops on some wpd documents

* Wed Mar 30 2005 Caolán McNamara <caolanm@redhat.com> 0.8.0-3
- rh#152503# add some Requires for -devel package

* Wed Mar  2 2005 Caolán McNamara <caolanm@redhat.com> 0.8.0-2
- rebuild with gcc4

* Fri Feb 11 2005 Caolán McNamara <caolanm@redhat.com> 0.8.0-1
- new version

* Wed Feb 9 2005 Caolán McNamara <caolanm@redhat.com> 0.7.2-2
- rebuild

* Fri Jul 23 2004 Caolán McNamara <caolanm@redhat.com> 0.7.2-1
- bump to 0.7.2

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb 19 2004 Jeremy Katz <katzj@redhat.com> - 0.7.1-1
- update to 0.7.1

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Dec 16 2003 Jeremy Katz <katzj@redhat.com> 0.6.6-1
- 0.6.6

* Tue Nov  4 2003 Jeremy Katz <katzj@redhat.com> 0.6.5-1
- 0.6.5

* Mon Sep 15 2003 Jeremy Katz <katzj@redhat.com> 0.6.2-1
- 0.6.2

* Sun Jul  6 2003 Jeremy Katz <katzj@redhat.com> 0.5.0-1
- initial build for Red Hat Linux, tweak accordingly

* Sat Apr 26 2003 Rui M. Seabra <rms@1407.org>
- Create rpm spec
