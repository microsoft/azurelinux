%define _use_internal_dependency_generator 0
%define __find_provides sh %{SOURCE1} %{prev__find_provides}
%define __find_requires sh %{SOURCE1} %{prev__find_requires}

Summary:        Library to access different kinds of (video) capture devices
Name:           libunicap
Version:        0.9.12
Release:        28%{?dist}
License:        GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.unicap-imaging.org/
Source0:        %{_mariner_sources_url}/%{name}-%{version}.tar.gz
Source1:        %{name}-filter.sh
Patch0:         libunicap-0.9.12-includes.patch
Patch1:         libunicap-0.9.12-memerrs.patch
Patch2:         libunicap-0.9.12-arraycmp.patch
Patch3:         libunicap-0.9.12-warnings.patch
Patch4:         libunicap-bz641623.patch
Patch5:         libunicap-bz642118.patch
Patch6:         libunicap-0.9.12-videodev.patch
Patch7:         libunicap-0.9.12-datadirname.patch
Patch8:         libunicap-0.9.12-gcc10.patch
BuildRequires:  %{_bindir}/perl
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gettext
BuildRequires:  glib2-devel >= 2.10.0
BuildRequires:  gtk-doc >= 1.4
BuildRequires:  intltool
BuildRequires:  libtool
BuildRequires:  libv4l-devel >= 0.8.3-1
BuildRequires:  systemd
BuildRequires:  perl(XML::Parser)
%{expand:%%define prev__find_provides %{__find_provides}}
%{expand:%%define prev__find_requires %{__find_requires}}
%ifnarch s390 s390x
BuildRequires:  libraw1394-devel >= 1.1.0
%endif

%description
Unicap provides a uniform interface to video capture devices. It allows
applications to use any supported video capture device via a single API.
The unicap library offers a high level of hardware abstraction while
maintaining maximum performance. Zero copy capture of video buffers is
possible for devices supporting it allowing fast video capture with low
CPU usage even on low-speed architectures.

%package devel
Summary:        Development files for the unicap library
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description devel
The libunicap-devel package includes header files and libraries necessary
for for developing programs which use the unicap library. It contains the
API documentation of the library, too.

%prep
%setup -q
%patch0 -p1 -b .includes
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1

# Needed to get rid of rpath
libtoolize --force
# fixes for gtk-doc 1.26
sed -i -e '/^DOC_SOURCE_DIR/s/--source-dir=//g' doc/libunicap/Makefile.am
autoreconf --force --install

%build
%configure --disable-rpath --disable-gtk-doc --enable-libv4l
%make_build

%install
%make_install

# Don't install any static .a and libtool .la files
rm -f %{buildroot}%{_libdir}/{,unicap2/cpi/}*.{a,la}

# Use ATTRS rather SYSFS for udev where appropriate
sed -e 's/\(SYSFS\|ATTRS\)/ATTRS/g' -i %{buildroot}%{_sysconfdir}/udev/rules.d/50-euvccam.rules
touch -c -r {data,%{buildroot}%{_sysconfdir}/udev/rules.d}/50-euvccam.rules

# Move udev rules file to appropriate rules directory

mkdir -p %{buildroot}%{_udevrulesdir}/
mv -f %{buildroot}%{_sysconfdir}/udev/rules.d/50-euvccam.rules %{buildroot}%{_udevrulesdir}/


%find_lang unicap

%ldconfig_scriptlets

%files -f unicap.lang
%license COPYING
%doc AUTHORS ChangeLog README

%{_udevrulesdir}/50-euvccam.rules

%{_libdir}/%{name}.so.*
%{_libdir}/unicap2

%files devel
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/unicap
%exclude %{_datadir}/gtk-doc/html/%{name}

%changelog
* Wed Dec 28 2022 Muhammad Falak <mwani@microsoft.com> - 0.9.12-28
- Configure with 'disable-gtk-doc'
- License verified

* Thu Mar 18 2021 Henry Li <lihl@microsoft.com> - 0.9.12-27
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Fix distro condition checking

* Sun Feb 09 2020 Robert Scheck <robert@fedoraproject.org> - 0.9.12-26
- Added patch to declare variable as extern in header file (#1799604)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.12-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.12-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.12-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.12-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.12-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.12-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.12-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.12-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.12-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.12-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun May 31 2015 Robert Scheck <robert@fedoraproject.org> 0.9.12-15
- Added patch to avoid a /usr/@DATADIRNAME@/locale/ directory
- Use %%{_udevrulesdir} macro rather /etc/udev/rules.d/ (#1226681)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.12-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.12-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.12-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.12-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.12-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.12-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Oct 09 2011 Robert Scheck <robert@fedoraproject.org> 0.9.12-8
- Added a patch to use the libv4l1compat header (#676470, #716118)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.12-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Nov 02 2010 Kamil Dudka <kdudka@redhat.com> 0.9.12-6
- fix a crasher bug introduced by libunicap-0.9.12-memerrs.patch (#647880)

* Fri Oct 29 2010 Robert Scheck <robert@fedoraproject.org> 0.9.12-5
- Use ATTRS rather SYSFS for udev where appropriate (#643729)

* Tue Oct 12 2010 Kamil Dudka <kdudka@redhat.com> 0.9.12-4
- do not use "private" as identifier in a public header (#642118)

* Sat Oct 09 2010 Kamil Dudka <kdudka@redhat.com> 0.9.12-3
- avoid SIGSEGV in v4l2_capture_start() (#641623)

* Thu Oct 07 2010 Kamil Dudka <kdudka@redhat.com> 0.9.12-2
- build the package in %%build
- fix tons of compile-time warnings
- fix some memory errors in the code

* Mon Oct 04 2010 Robert Scheck <robert@fedoraproject.org> 0.9.12-1
- Upgrade to 0.9.12 (#635377)

* Sun Feb 21 2010 Robert Scheck <robert@fedoraproject.org> 0.9.8-1
- Upgrade to 0.9.8 (#530702, #567109, #567110, #567111)
- Splitting of unicap into libunicap, libucil and libunicapgtk

* Sat Oct 24 2009 Robert Scheck <robert@fedoraproject.org> 0.9.7-1
- Upgrade to 0.9.7 (#530702)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 18 2009 Dan Horak <dan[at]danny.cz> 0.9.5-2
- don't require libraw1394 on s390/s390x

* Sun May 03 2009 Robert Scheck <robert@fedoraproject.org> 0.9.5-1
- Upgrade to 0.9.5

* Mon Feb 23 2009 Robert Scheck <robert@fedoraproject.org> 0.9.3-2
- Rebuild against gcc 4.4 and rpm 4.6

* Mon Oct 13 2008 Robert Scheck <robert@fedoraproject.org> 0.9.3-1
- Upgrade to 0.9.3 (#466825, thanks to Hans de Goede)
- Enabled libv4l support for the new gspca kernel driver

* Sat Aug 09 2008 Robert Scheck <robert@fedoraproject.org> 0.2.23-4
- Rebuild to get missing dependencies back (#443015, #458527)

* Tue Aug 05 2008 Robert Scheck <robert@fedoraproject.org> 0.2.23-3
- Filter the unicap plugins which overlap with libv4l libraries

* Tue Jul 22 2008 Robert Scheck <robert@fedoraproject.org> 0.2.23-2
- Rebuild for libraw1394 2.0.0

* Mon May 19 2008 Robert Scheck <robert@fedoraproject.org> 0.2.23-1
- Upgrade to 0.2.23
- Corrected packaging of cpi/*.so files (thanks to Arne Caspari)

* Sat May 17 2008 Robert Scheck <robert@fedoraproject.org> 0.2.22-1
- Upgrade to 0.2.22 (#446021)

* Sat Feb 16 2008 Robert Scheck <robert@fedoraproject.org> 0.2.19-3
- Added patch to correct libdir paths (thanks to Ralf Corsepius)

* Mon Feb 04 2008 Robert Scheck <robert@fedoraproject.org> 0.2.19-2
- Changes to match with Fedora Packaging Guidelines (#431381)

* Mon Feb 04 2008 Robert Scheck <robert@fedoraproject.org> 0.2.19-1
- Upgrade to 0.2.19
- Initial spec file for Fedora and Red Hat Enterprise Linux
