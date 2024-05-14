Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%if 0%{?rhel} && 0%{?rhel} < 8
%bcond_without legacy_python
%endif

#global gitdate 20150818
#global gitversion eba96a4

Name:           evemu
Version:        2.7.0
Release:        14%{?dist}
Summary:        Event Device Query and Emulation Program

License:        GPLv3+
URL:            https://www.freedesktop.org/wiki/Evemu

%if 0%{?gitdate}
Source0:        %{name}-%{gitdate}.tar.bz2
Source1:        make-git-snapshot.sh
Source2:        commitid
%else
Source0:        https://www.freedesktop.org/software/%{name}/%{name}-%{version}.tar.xz
%endif

BuildRequires:  automake libtool gcc gcc-c++
%if %{with legacy_python}
BuildRequires:  python2-devel
%else
BuildRequires:  python3-devel
%endif
BuildRequires:  xmlto asciidoc
BuildRequires:  libevdev-devel >= 1.3
Requires:       libevdev >= 0.5
Requires:       %{name}-libs = %{version}-%{release}

%description
%{name} is a simple utility to capture the event stream from input devices
and replay that stream on a virtual input device.

%package libs
Summary:        Event Device Query and Emulation Program Library
License:        LGPLv3+
Conflicts:      evemu < 2.7.0-8

%description libs
%{name} base library, used by the evemu tools.

%package devel
Summary:        Event Device Query and Emulation Program Development Package
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description devel
%{name} development files.

%prep
%setup -q -n %{name}-%{?gitdate:%{gitdate}}%{!?gitdate:%{version}}

%build
autoreconf -v --install --force || exit 1
%if %{with legacy_python}
export PYTHON=python2
%else
export PYTHON=python3
%endif
%configure --disable-static --disable-silent-rules
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

# We intentionally don't ship *.la files
rm -f %{buildroot}%{_libdir}/*.la

%ldconfig_scriptlets

%files
%license COPYING
%{_bindir}/evemu-describe
%{_bindir}/evemu-device
%{_bindir}/evemu-play
%{_bindir}/evemu-event
%{_bindir}/evemu-record
%{_mandir}/man1/evemu-*

%files libs
%{_libdir}/libevemu.so.*

%files devel
%{_includedir}/evemu.h
%{_libdir}/libevemu.so
%{_libdir}/pkgconfig/evemu.pc
%if %{with legacy_python}
%{python2_sitelib}/evemu
%else
%{python3_sitelib}/evemu
%endif

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.7.0-14
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 2.7.0-12
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 2.7.0-11
- Rebuilt for Python 3.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jul 16 2018 Peter Hutterer <peter.hutterer@redhat.com> 2.7.0-8
- Split the lib into its own subpackage, it's LGPLv3+
- remove utouch-evemu Obsoletes line, it's been over 5 years

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 2.7.0-6
- Rebuilt for Python 3.7

* Fri Mar 30 2018 Carl George <carl@george.computer> - 2.7.0-5
- Build with python3 on Fedora
- Fix license handling
- Use %%ldconfig_scriptlets macro

* Thu Mar 08 2018 Peter Hutterer <peter.hutterer@redhat.com> 2.7.0-4
- Add BuildRequires for gcc-c++, needed for a test build

* Mon Feb 19 2018 Peter Hutterer <peter.hutterer@redhat.com> 2.7.0-3
- Add BuildRequires for gcc

* Tue Feb 06 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2.7.0-2
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Mon Sep 25 2017 Benjamin Tissoires <benjamin.tissoires@redhat.com> 2.7.0-1
- Evemu 2.7.0

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed May 03 2017 Peter Hutterer <peter.hutterer@redhat.com> 2.6.0-1
- evemu 2.6.0

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Sep 16 2016 Benjamin Tissoires <benjamin.tissoires@redhat.com> 2.5.0-1
- Evemu v2.5.0

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.0-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Mon Apr 04 2016 Benjamin Tissoires <benjamin.tissoires@redhat.com> 2.4.0-1
- Evemu v2.4.0

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Oct 14 2015 Benjamin Tissoires <benjamin.tissoires@redhat.com> 2.3.1-1
- Evemu v2.3.1

* Tue Aug 18 2015 Benjamin Tissoires <benjamin.tissoires@redhat.com> 2.2.0-2.20150818giteba96a4
- git snapshot to fix rhbz #1251015

* Tue Aug 04 2015 Benjamin Tissoires <benjamin.tissoires@redhat.com> 2.2.0-1
- Evemu v2.2.0

* Wed Jul 22 2015 Benjamin Tissoires <benjamin.tissoires@redhat.com> 2.1.0-4.20150722git79b29f0
- Update to current git master: add dmi info and EV_SW and EV_LED states

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 11 2015 Benjamin Tissoires <benjamin.tissoires@redhat.com> 2.1.0-2
- Apply 2 upstream patches: handle holes in the input node list,
  add uname to the header comment

* Wed Nov 12 2014 Peter Hutterer <peter.hutterer@redhat.com> 2.1.0-1
- Update to version 2.1.0

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jun 19 2014 Benjamin Tissoires <benjamin.tissoires@redhat.com> 2.0.0-1
- Update to version 2.0.0

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.99.0-4.20140324gitaf60032
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Mar 23 2014 Peter Hutterer <peter.hutterer@redhat.com> - 1.99.0-3.20140324gitaf60032
- Update to current git, stray debugging output lead to invalid traces

* Mon Feb 10 2014 Peter Hutterer <peter.hutterer@redhat.com> - 1.99.0-2.20131213gitb8f3f57
- Rebuild for libevdev soname bump

* Fri Dec 13 2013 Benjamin Tissoires <benjamin.tissoires@redhat.com> 1.99.0-1.20131213gitb8f3f57
- Update to current git, before 2.0 is released
- fixes #1037056 (evemu FTBFS if "-Werror=format-security" flag is used)
- use libevdev backend (libevdev >= 0.5 is required)

* Thu Nov 21 2013 Benjamin Tissoires <benjamin.tissoires@redhat.com> 1.2.0-0
- Update to version 1.2.0

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-5.20130724git304eb65f
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 Benjamin Tissoires <benjamin.tissoires@redhat.com> 1.1.0-4.20130724git304eb65f
- Update to current git, record the resolution and bump the file format to 1.2

* Wed Jul 10 2013 Peter Hutterer <peter.hutterer@redhat.com> - 1.1.0-3.20130708gitf2eb0f2cd
- disable silent rules

* Mon Jul 08 2013 Peter Hutterer <peter.hutterer@redhat.com> - 1.1.0-2.20130708gitf2eb0f2cd
- Update to current git, avoids printing unused bits

* Thu May 23 2013 Peter Hutterer <peter.hutterer@redhat.com>
- Drop unused patch

* Fri May 03 2013 Benjamin Tissoires <benjamin.tissoires@redhat.com> 1.1.0-1
- Update to version 1.1.0, hosted now on freedesktop

* Thu Jan 31 2013 Peter Hutterer <peter.hutterer@redhat.com> 1.0.10-3
- fclose output only once

* Tue Jan 08 2013 Peter Hutterer <peter.hutterer@redhat.com> 1.0.10-2
- Test for device grab in evemu-record

* Fri Jul 06 2012 Peter Hutterer <peter.hutterer@redhat.com> 1.0.10-1
- Update to version 1.0.10, rename. upstream changed name to "evemu" with
  this version

* Thu Feb 09 2012 Peter Hutterer <peter.hutterer@redhat.com> 1.0.8-2
- autoreconf --force to stop weird libtool build errors

* Tue Feb 07 2012 Peter Hutterer <peter.hutterer@redhat.com> 1.0.8-1
- Initial package
