Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Summary:        C library for portable packet creation and injection
Name:           libnet
Version:        1.3
Release:        1%{?dist}
License:        BSD-2-Clause AND BSD-3-Clause
URL:            https://github.com/libnet/libnet
Source0:        https://github.com/libnet/libnet/releases/download/v%{version}/%{name}-%{version}.tar.gz
Patch0:         libnet-config.patch
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  %{_bindir}/pod2man

%description
Libnet is an API to help with the construction and handling of network
packets. It provides a portable framework for low-level network packet
writing and handling (use libnet in conjunction with libpcap and you can
write some really cool stuff). Libnet includes packet creation at the IP
layer and at the link layer as well as a host of supplementary and
complementary functionality.

%package devel
Summary:        Development files for the libnet library
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig

%description devel
The libnet-devel package includes header files and libraries necessary
for developing programs which use the libnet library. Libnet is very
handy with which to write network tools and network test code. See the
man page and sample test code for more detailed information.

%if 0%{!?_without_doc:1}
%package doc
Summary:        Documentation files for the libnet library
BuildArch:      noarch
BuildRequires:  doxygen
BuildRequires:  graphviz

%description doc
Libnet is an API to help with the construction and handling of network
packets. It provides a portable framework for low-level network packet
writing and handling. This package contains the API documentation for
developing applications that use libnet.
%endif

%prep
%setup -q
%patch -P 0 -p1
# Avoid library soname bump (https://github.com/libnet/libnet/issues/115)
sed -e 's/-version-info 9:0:0/-version-info 9:0:8/' -i src/Makefile.{am,in}

%build
%configure
%make_build

%install
%make_install INSTALL='install -p'

# Don't install any libtool .la files
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}.{a,la}

# Clean up for later usage in documentation
rm -rf $RPM_BUILD_ROOT%{_defaultdocdir}

# Prepare samples for usage in documentation
rm -rf sample/{Makefile*,win32}
for file in sample/*.[hc]; do
  sed \
    -e 's@#include "../include/libnet.h"@#include <libnet.h>@' \
    -e 's@#include "../include/config.h"@#include <config.h>@' \
    $file > $file.new
    touch -c -r $file{,.new}
    mv -f $file{.new,}
done

%ldconfig_scriptlets

%files
%license LICENSE
%doc README.md ChangeLog.md
%{_libdir}/%{name}.so.*

%files devel
%doc doc/MIGRATION.md doc/RAWSOCKET.md sample/
%{_bindir}/%{name}-config
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/%{name}.h
%{_includedir}/%{name}/
%{_mandir}/man1/%{name}*.1*
%{_mandir}/man3/%{name}*.3*

%if 0%{!?_without_doc:1}
%files doc
%doc doc/html/
%endif

%changelog
* Mon Nov 18 2024 Akarsh Chaudhary <v-akarshc@microsoft.com> -1.3-1
- upgrade to version 1.3
-License Verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.2-2
- Initial CBL-Mariner import from Fedora 33 (license: MIT).

* Sat Jan 02 2021 Robert Scheck <robert@fedoraproject.org> 1.2-1
- Upgrade to 1.2 (#1912031)

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Dec 20 2013 Robert Scheck <robert@fedoraproject.org> 1.1.6-7
- Run autoreconf to recognize aarch64 (#925813)
- Conditionalized usage of %%{_lib} vs %%{_libdir} for RHEL < 7
- Tight run-time dependencies between sub-packages via %%{?_isa}

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 02 2012 Jon Ciesla <limburgher@gmail.com> - 1.1.6-3
- Removed redundant leading slashes.

* Mon Apr 02 2012 Jon Ciesla <limburgher@gmail.com> - 1.1.6-2
- Move from lib to libdir.

* Fri Mar 30 2012 Jon Ciesla <limburgher@gmail.com> - 1.1.6-1
- Upgrade to 1.1.6, BZ 808394.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 28 2010 Robert Scheck <robert@fedoraproject.org> 1.1.5-1
- Upgrade to 1.1.5

* Fri Jul 09 2010 Robert Scheck <robert@fedoraproject.org> 1.1.4-4
- Added patch for capability support rather UID check (#589770)

* Fri Aug 21 2009 Robert Scheck <robert@fedoraproject.org> 1.1.4-3
- Move libnet.so.* to /lib[64] to avoid static linking (#518150)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 11 2009 Robert Scheck <robert@fedoraproject.org> 1.1.4-1
- Upgrade to 1.1.4

* Sat Jun 06 2009 Robert Scheck <robert@fedoraproject.org> 1.1.3-2
- Added upstream patch to solve HAVE_CONFIG_H (#501633, #502400)

* Sat May 16 2009 Robert Scheck <robert@fedoraproject.org> 1.1.3-1
- Upgrade to 1.1.3

* Sun Apr 19 2009 Robert Scheck <robert@fedoraproject.org> 1.1.2.1-14
- Enabled a shared library and made lots of spec file cleanups

* Mon Feb 23 2009 Robert Scheck <robert@fedoraproject.org> 1.1.2.1-13
- Rebuild against gcc 4.4 and rpm 4.6

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.1.2.1-12
- Autorebuild for GCC 4.3

* Wed Aug  1 2007 Patrice Dumas <pertusus@free.fr> 1.1.2.1-11
- build with -fPIC (#250296)

* Fri Jan 12 2007 Patrice Dumas <pertusus@free.fr> 1.1.2.1-10
- add debian patch to correct bad checksums

* Tue Aug 29 2006 Patrice Dumas <pertusus@free.fr> 1.1.2.1-9
- rebuild for FC6

* Fri Feb 17 2006 Patrice Dumas <pertusus@free.fr> 1.1.2.1-8
- rebuild for fc5

* Thu Dec 22 2005 Patrice Dumas <pertusus@free.fr> 1.1.2.1-7
- rebuild

* Mon Sep 12 2005 Patrice Dumas <pertusus@free.fr> 1.1.2.1-6
- bump release and add dist tag

* Tue Aug 30 2005 Paul Howarth <paul@city-fan.org> 1.1.2.1-5
- spec file cleanup

* Fri Aug 26 2005 Patrice Dumas <pertusus@free.fr> 1.1.2.1-4
- use pushd and popd (from Oliver Falk) 

* Mon Aug 22 2005 Patrice Dumas <pertusus@free.fr> 1.1.2.1-3
- Correct dos end of lines
- add in devel: Provides: %%{name} = %%{version}-%%{release} 

* Fri Aug 12 2005 Patrice Dumas <pertusus@free.fr> 1.1.2.1-2
- put everything in a devel subpackage
- add smpflags
- clean in sample

* Fri Aug 12 2005 Patrice Dumas <pertusus@free.fr> 1.1.2.1-1
- rebuild changing only name

* Wed Jun 02 2004 Marcin Garski <garski@poczta.onet.pl> 1.1.2.1-2.fc2
- Rebuild for Fedora Core 2

* Sat May 08 2004 Marcin Garski <garski@poczta.onet.pl> 1.1.2.1-1
- Initial specfile
