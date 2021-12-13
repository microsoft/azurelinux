Vendor:         Microsoft Corporation
Distribution:   Mariner
%global maj 0
%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Name:       sord
Version:    0.16.4
Release:    5%{?dist}
Summary:    A lightweight Resource Description Framework (RDF) C library

License:    ISC
URL:        https://drobilla.net/software/sord
Source0:    https://download.drobilla.net/%{name}-%{version}.tar.bz2

BuildRequires: boost-devel
BuildRequires: doxygen
BuildRequires: graphviz
BuildRequires: glib2-devel
BuildRequires: python3
BuildRequires: serd-devel >= 0.30.0
BuildRequires: gcc
BuildRequires: gcc-c++

%description
%{name} is a lightweight C library for storing Resource Description
Framework (RDF) data in memory. %{name} and parent library serd form 
a lightweight RDF tool-set for resource limited or performance critical 
applications.

%package devel
Summary:    Development libraries and headers for %{name}
Requires:   %{name}%{_isa} = %{version}-%{release}

%description devel
%{name} is a lightweight C library for storing Resource Description
Framework (RDF) data in memory.

This package contains the headers and development libraries for %{name}.

%prep
%setup -q
# we'll run ldconfig, and add our optflags 
sed -i -e "s|bld.add_post_fun(autowaf.run_ldconfig)||" \
       -e "s|cflags          = [ '-DSORD_INTERNAL' ]\
|cflags          = [ '-DSORD_INTERNAL' ] + '%optflags'.split(' ') |" wscript

%build
%set_build_flags
# Work around a possible GCC 10 bug
# GCC 10 crashes on these arches in for loop with ZixBTreeIter
%ifarch %{power64} %{arm} aarch64 s390 s390x
CFLAGS+=" -O1"
CXXFLAGS+=" -O1"
%endif
export LINKFLAGS="%{__global_ldflags}"
python3 waf configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --mandir=%{_mandir} \
    --datadir=%{_datadir} \
    --docdir=%{_pkgdocdir} \
    --test \
    --docs 
python3 waf build -v %{?_smp_mflags}

%install
DESTDIR=%{buildroot} python3 waf install
chmod +x %{buildroot}%{_libdir}/lib%{name}-%{maj}.so.*
install -pm 644 AUTHORS NEWS README.md COPYING %{buildroot}%{_pkgdocdir}

%files
%{_pkgdocdir}
%exclude %{_pkgdocdir}/%{name}-%{maj}/
%exclude %{_pkgdocdir}/COPYING
%license COPYING
%{_libdir}/lib%{name}-%{maj}.so.*
%{_bindir}/sordi
%{_bindir}/sord_validate
%{_mandir}/man1/%{name}*.1*

%files devel
%{_pkgdocdir}/%{name}-%{maj}/
%{_libdir}/lib%{name}-%{maj}.so
%{_libdir}/pkgconfig/%{name}-%{maj}.pc
%{_includedir}/%{name}-%{maj}/
%{_mandir}/man3/%{name}*.3*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.16.4-5
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Sun Jul 12 2020 Guido Aulisi <guido.aulisi@gmail.com> - 0.16.4-4
- Work around optimization bug on s390x too

* Sun Mar 15 2020 Guido Aulisi <guido.aulisi@gmail.com> - 0.16.4-3
- Rebuilt for possible GCC 10 bug on power64 and arm

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Dec 06 2019 Guido Aulisi <guido.aulisi@gmail.com> - 0.16.4-1
- Update to 0.16.4
- Use python3

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jul 31 2018 Florian Weimer <fweimer@redhat.com> - 0.16.2-2
- Rebuild with fixed binutils

* Mon Jul 30 2018 Guido Aulisi <guido.aulisi@gmail.com> - 0.16.2-1
- Update to 0.16.2
- Remove ldconfig scriptlets
- Minor spec cleanup

* Sun Jul 15 2018 Guido Aulisi <guido.aulisi@gmail.com> - 0.16.0-6
- Fix FTBFS due to the move of /usr/bin/python into a separate package

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Mar 14 2017 Guido Aulisi <guido.aulisi@gmail.com> - 0.16.0-1
- Update to 0.16.0
- Use hardened LDFLAGS
- Use license macro

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 27 2017 Jonathan Wakely <jwakely@redhat.com> - 0.12.2-9
- Rebuilt for Boost 1.63

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 15 2016 Jonathan Wakely <jwakely@redhat.com> - 0.12.2-7
- Rebuilt for Boost 1.60

* Thu Aug 27 2015 Jonathan Wakely <jwakely@redhat.com> - 0.12.2-6
- Rebuilt for Boost 1.59

* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.2-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 0.12.2-4
- rebuild for Boost 1.58

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jan 26 2015 Petr Machata <pmachata@redhat.com> - 0.12.2-2
- Rebuild for boost 1.57.0

* Wed Aug 20 2014 Brendan Jones <brendan.jones.it@gmail.com> 0.12.2-1
- Update to 0.12.2

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 Petr Machata <pmachata@redhat.com> - 0.12.0-5
- Rebuild for boost 1.55.0

* Sun Dec 15 2013 Ville Skyttä <ville.skytta@iki.fi> - 0.12.0-4
- Install docs to %%{_pkgdocdir} where available (#994099).
- Move *.1 manpages to main package.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 30 2013 Petr Machata <pmachata@redhat.com> - 0.12.0-2
- Rebuild for boost 1.54.0

* Tue May 21 2013 Brendan Jones <brendan.jones.it@gmail.com> 0.12.0-1
- New upstream release

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Dec 15 2012 Brendan Jones <brendan.jones.it@gmail.com> 0.10.4-2
- Rebuilt for serd

* Sat Dec 15 2012 Brendan Jones <brendan.jones.it@gmail.com> 0.10.4-1
- New upstream release

* Tue Jul 24 2012 Brendan Jones <brendan.jones.it@gmail.com> 0.8.0-2
- Remove unwanted man file

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Apr 20 2012 Brendan Jones <brendan.jones.it@gmail.com> - 0.8.0-1
- New upstream release

* Thu Jan 19 2012 Brendan Jones <brendan.jones.it@gmail.com> - 0.5.0-3
- Correct macros in description, expand summary.

* Mon Jan 16 2012 Brendan Jones <brendan.jones.it@gmail.com> - 0.5.0-2
- Correct macros in description, expand summary.

* Fri Dec 23 2011 Brendan Jones <brendan.jones.it@gmail.com> - 0.5.0-1
- Initial build
