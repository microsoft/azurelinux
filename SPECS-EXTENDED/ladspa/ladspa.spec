Name:           ladspa
Version:        1.17
Release:        6%{?dist}

Summary:        Linux Audio Developer's Simple Plug-in API, examples and tools

License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://www.ladspa.org/
Source:         https://www.ladspa.org/download/%{name}_sdk_%{version}.tgz
Patch1:         ladspa-1.17.patch

BuildRequires:  perl-interpreter
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(sndfile)

%description
There is a large number of synthesis packages in use or development on
the Linux platform at this time. The Linux Audio Developer's Simple
Plugin API (LADSPA) attempts to give programmers the ability to write
simple `plugin' audio processors in C/C++ and link them dynamically
against a range of host applications.

This package contains the example plug-ins and tools from the LADSPA SDK.

%package        devel
Summary:        Linux Audio Developer's Simple Plug-in API
Requires:       %{name} = %{version}-%{release}

%description    devel
ladspa-devel contains the ladspa.h header file.

Definitive technical documentation on LADSPA plug-ins for both the host
and plug-in is contained within copious comments within the ladspa.h
header file.

%prep
%setup -q -n ladspa_sdk_%{version}
%patch -P1 -p1 -b .0001
# respect RPM_OPT_FLAGS
perl -pi -e 's/^(CFLAGS.*)-O2(.*)/$1\$\(RPM_OPT_FLAGS\)$2 -DDEFAULT_LADSPA_PATH=\$\(PLUGINDIR\)/' src/Makefile
# avoid X.org dependency
perl -pi -e 's/-mkdirhier/-mkdir -p/' src/Makefile

# Respect our CC and CPP choices
perl -pi -e 's/CC(.*)=(.*)cc//' src/makefile
perl -pi -e 's/CPP(.*)=(.*)c\+\+//' src/makefile

# fix links to the header file in the docs
cd doc
perl -pi -e "s!HREF=\"ladspa.h.txt\"!href=\"file:///usr/include/ladspa.h\"!" *.html

%build
%set_build_flags
cd src
PLUGINDIR=%{_libdir}/ladspa make targets %{?_smp_mflags} LD="ld --build-id"

#make test
#make check

%install
cd src
%make_install \
  INSTALL_PLUGINS_DIR=$RPM_BUILD_ROOT%{_libdir}/ladspa \
  INSTALL_INCLUDE_DIR=$RPM_BUILD_ROOT%{_includedir} \
  INSTALL_BINARY_DIR=$RPM_BUILD_ROOT%{_bindir}

## this is where plugins will install their rdf
mkdir -p $RPM_BUILD_ROOT%{_datadir}/ladspa/rdf

%files
%doc doc/COPYING
%dir %{_libdir}/ladspa
%{_libdir}/ladspa/*.so
%{_bindir}/analyseplugin
%{_bindir}/applyplugin
%{_bindir}/listplugins
%{_datadir}/ladspa

%files devel
%doc doc/*.html
%{_includedir}/ladspa.h

%changelog
* Mon Apr 7 2025 Aninda Pradhan <v-anipradhan@microsoft.com> - 1.17-6
- Initial Azure Linux import from Fedora 41 (license: MIT)
- License Verified

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.17-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 14 2024 Sérgio Basto <sergio@serjux.com> - 1.17-2
- bump version to tag the build

* Sun Jan 14 2024 Sérgio Basto <sergio@serjux.com> - 1.17-1
- Update to 1.17
- Update to 1.15 Wim Taymans <wtaymans@fedoraproject.org>

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.13-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.13-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.13-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.13-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.13-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.13-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.13-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.13-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.13-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.13-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.13-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.13-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.13-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.13-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.13-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.13-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.13-14
- Rebuilt for GCC 5 C++11 ABI change

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Mar 22 2009 Robert Scheck <robert@fedoraproject.org> - 1.13-5
- Really added the plugindir patch now (thanks to Karsten Hopp)
- Avoid the make errors because of mkdirhier better than until now

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Nov 23 2008 Thomas Vander Stichele <thomas at apestaart dot org>
- 1.13-2
- updated summary
- not rebuilt yet

* Fri Sep  5 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 1.13-1
- link with build-id to fix rawhide build
- upgrade to 1.13 (GCC4 build-fix and string fixes) (#449542)
- add -plugindir patch so listplugin and friends will work by default
  (Anthony Green #324741)

* Tue Aug  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.12-10
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org>
- 1.12-9
- Autorebuild for GCC 4.3

* Mon Apr 23 2007 Thomas Vander Stichele <thomas at apestaart dot org>
- 1.12-8
- own the datadir.  Fixes #231706.

* Sat Sep 16 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 1.12-7
- include gcc 4.1 patch from Mandriva

* Sun Mar 05 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 1.12-6
- rebuilt for FE5

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 1.12-5
- rebuild on all arches

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sun Sep 07 2003 Thomas Vander Stichele <thomas at apestaart dot org>
- 0:1.12-0.fdr.3: readded epoch, fixed group

* Fri Sep 05 2003 Thomas Vander Stichele <thomas at apestaart dot org>
- 1.12-0.fdr.2: fixed RPM_OPT_FLAGS respect

* Thu May 29 2003 Thomas Vander Stichele <thomas at apestaart dot org>
- 0:1.12-0.fdr.1: initial RPM release
