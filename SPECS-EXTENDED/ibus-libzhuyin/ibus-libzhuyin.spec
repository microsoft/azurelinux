Vendor:         Microsoft Corporation
Distribution:   Azure Linux
# This package depends on automagic byte compilation
# https://fedoraproject.org/wiki/Changes/No_more_automagic_Python_bytecompilation_phase_2
%global _python_bytecompile_extra 1

%global snapshot 0

Name:       ibus-libzhuyin
Version:    1.9.1
Release:    6%{?dist}
Summary:    New Zhuyin engine based on libzhuyin for IBus
License:    GPLv2+
URL:        https://github.com/libzhuyin/ibus-libzhuyin
Source0:    https://downloads.sourceforge.net/libzhuyin/ibus-libzhuyin/%{name}-%{version}.tar.gz
%if %snapshot
Patch0:     ibus-libzhuyin-1.9.x-HEAD.patch
%endif

BuildRequires:  gcc-c++
BuildRequires:  perl(File::Find)
BuildRequires:  gettext-devel
BuildRequires:  intltool
BuildRequires:  libtool
BuildRequires:  pkgconfig
BuildRequires:  sqlite-devel
BuildRequires:  ibus-devel >= 1.3
BuildRequires:  libpinyin-devel >= 2.0.91
BuildRequires:  python3-devel
BuildRequires:  libpinyin-tools

# Requires(post): sqlite

Requires:   ibus >= 1.3.0
Provides:   libzhuyin-data = 1.1.2
Obsoletes:  libzhuyin-data < 1.1.2

%description
It includes a Chinese Zhuyin (Bopomofo) input method
based on libzhuyin for IBus.

%prep
%setup -q
%if %snapshot
%patch 0 -p1 -b .head
%endif


%build
%configure --disable-static \
           --disable-boost \
           --with-python=python3

# make -C po update-gmo
make %{?_smp_mflags} V=1

%install
make install DESTDIR=${RPM_BUILD_ROOT} INSTALL="install -p"

%find_lang %{name}

%files -f %{name}.lang
%license COPYING
%doc AUTHORS README ChangeLog INSTALL NEWS
%{_datadir}/appdata/*.appdata.xml
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_datadir}/applications/ibus-setup-libzhuyin.desktop
%{_libexecdir}/ibus-engine-libzhuyin
%{_libexecdir}/ibus-setup-libzhuyin
%{_datadir}/ibus-libzhuyin/setup
%dir %{_datadir}/ibus-libzhuyin
%{_datadir}/ibus/component/*
%{_datadir}/ibus-libzhuyin/icons
%{_datadir}/ibus-libzhuyin/*symbol.txt
%{_libdir}/ibus-libzhuyin/


%changelog
* Wed Feb 16 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.9.1-6
- License verified.

* Tue Feb 15 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.9.1-5
- Adding missing BRs on Perl modules.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.9.1-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon May 20 2019 Peng Wu <pwu@redhat.com> - 1.9.1-1
- Update to 1.9.1
- fixes page up and page down shortcut key
- fixes special symbols
- fixes escape handling
- fixes numpad

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 22 2019 Peng Wu <pwu@redhat.com> - 1.9.0-1
- Update to 1.9.0
- fixes special symbol
- add need-tone option

* Fri Nov  2 2018 Peng Wu <pwu@redhat.com> - 1.8.93-1
- Update to 1.8.93
- fixes Space handling

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.92-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.8.92-2
- Rebuilt for Python 3.7

* Mon Apr  9 2018 Peng Wu <pwu@redhat.com> - 1.8.92-1
- Update to 1.8.92
- fixes easy symbol and user symbol

* Thu Mar 22 2018 Peng Wu <pwu@redhat.com> - 1.8.91-1
- Update to 1.8.91
- migrate to use GSettings

* Wed Feb  7 2018 Peng Wu <pwu@redhat.com> - 1.8.3-1
- Update to 1.8.3
- translate input method name in ibus menu

* Wed Dec 13 2017 Peng Wu <pwu@redhat.com> - 1.8.2-1
- Update to 1.8.2
- fixes cursor move

* Thu Oct 26 2017 Peng Wu <pwu@redhat.com> - 1.8.1-1
- Update to 1.8.1
- bug fixes

* Fri Aug 25 2017 Peng Wu <pwu@redhat.com> - 1.8.0-1
- Update to 1.8.0

* Fri Aug 25 2017 Peng Wu <pwu@redhat.com> - 1.7.91-4
- Rebuilt for libpinyin 2.1.0

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.91-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.91-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun  8 2017 Peng Wu <pwu@redhat.com> - 1.7.91-1
- Update to 1.7.91
- merge libzhuyin data

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Oct 13 2016 Peng Wu <pwu@redhat.com> - 1.7.10-1
- Update to 1.7.10

* Thu Sep 29 2016 Peng Wu <pwu@redhat.com> - 1.7.9-1
- Update to 1.7.9

* Mon Sep  5 2016 Peng Wu <pwu@redhat.com> - 1.7.8-1
- Update to 1.7.8

* Fri Jun  3 2016 Peng Wu <pwu@redhat.com> - 1.7.7-1
- Update to 1.7.7

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Dec 11 2015 Peng Wu <pwu@redhat.com> - 1.7.6-1
- Update to 1.7.6

* Tue Dec  8 2015 Peng Wu <pwu@redhat.com> - 1.7.5-2
- Fixes crash

* Thu Nov 19 2015 Peng Wu <pwu@redhat.com> - 1.7.5-1
- Update to 1.7.5

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.4-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Sep 17 2015 Peng Wu <pwu@redhat.com> - 1.7.4-2
- Fixes cursor behavior

* Wed Aug 19 2015 Peng Wu <pwu@redhat.com> - 1.7.4-1
- Update to 1.7.4

* Wed Jul  1 2015 Peng Wu <pwu@redhat.com> - 1.7.3-1
- Update to 1.7.3

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 11 2015 Peng Wu <pwu@redhat.com> - 1.7.2-1
- Update to 1.7.2

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.7.1-2
- Rebuilt for GCC 5 C++11 ABI change

* Tue Apr  7 2015 Peng Wu <pwu@redhat.com> - 1.7.1-1
- Update to 1.7.1

* Tue Mar 24 2015 Peng Wu <pwu@redhat.com> - 1.7.0-1
- Update to 1.7.0

* Wed Jan  7 2015 Peng Wu <pwu@redhat.com> - 1.6.99.20140929-2
- Use opencc 1.0.2

* Mon Sep 29 2014 Peng Wu <pwu@redhat.com> - 1.6.99.20140929-1
- Update to 1.6.99.20140929

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.99.20140718-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul 18 2014 Peng Wu <pwu@redhat.com> - 1.6.99.20140718-1
- Update to 1.6.99.20140718

* Thu Jul  3 2014 Peng Wu <pwu@redhat.com> - 1.6.99.20140626-2
- Improves spec.

* Fri Jun 01 2012  Peng Wu <pwu@redhat.com> - 1.6.99.20140626-1
- The first version.
