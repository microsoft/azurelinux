# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global gitdate 20240205
%global commit0 c8ad98249af541514ff7a81634d3295e712f1a39
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global tag0 VERSION_%{version}

Name:           signon
Version:        8.60^%{gitdate}.%{shortcommit0}
Release: 5%{?dist}
Summary:        Accounts framework for Linux and POSIX based platforms

License:        LGPL-2.1-only
URL:            https://gitlab.com/accounts-sso/signond

# Temporary source, for plasma6 compatibility
Source0:        https://gitlab.com/nicolasfella/signond/-/archive/%{commit0}/signond-%{commit0}.tar.gz

# Original Sources
#%%if 0%{?tag0:1}
#Source0:        https://gitlab.com/accounts-sso/signond/repository/archive.tar.gz?ref=%%{tag0}#/%%{name}-%{version}.tar.gz
#%%else
#Source0:        https://gitlab.com/accounts-sso/signond/repository/archive.tar.gz?ref=%%{commit0}#/%%{name}-%%{shortcommit0}.tar.gz
#%%endif

BuildRequires: make
BuildRequires:  dbus-x11
BuildRequires:  doxygen
BuildRequires:  gcc-c++
BuildRequires:  graphviz
BuildRequires:  libproxy-devel
BuildRequires:  qt5-qtbase-devel
BuildRequires:  time
BuildRequires:  qt6-qtbase-devel

# signon-qt5 was in ktp-5 COPR
Obsoletes:      signon-qt5 < 8.57-5
Provides:       signon-qt5 = %{version}-%{release}

# upstream name: signond
Provides:       signond = %{version}-%{release}

# conflicting implementation: gsignond
Conflicts:      gsignond

Requires:       dbus

%description
Single Sign-On is a framework for centrally storing authentication credentials
and handling authentication on behalf of applications as requested by
applications. It consists of a secure storage of login credentials (for example
usernames and passwords), plugins for different authentication systems and a
client library for applications to communicate with this system.

%package qt5
Summary:        Single Sign On client library for Qt5-based applications
%description qt5
%{summary}.

%package qt6
Summary:        Single Sign On client library for Qt6-based applications
%description qt6
%{summary}.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
# upstream name: signond
Provides:       signond-devel = %{version}-%{release}
%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package qt5-devel
Summary:        Development files for %{name}-qt5
%description qt5-devel
%{summary}.

%package qt6-devel
Summary:        Development files for %{name}-qt6
%description qt6-devel
%{summary}.

%package doc
Summary:        Documentation for %{name}
BuildArch:      noarch

%description doc
The %{name}-doc package contains documentation for %{name}.


%prep
%autosetup -n signond-%{commit0} -p1


%build
mkdir %{name}_qt5
pushd %{name}_qt5
%qmake_qt5 \
  CONFIG+=release \
  QMF_INSTALL_ROOT=%{_prefix} LIBDIR=%{_libdir} ../signon.pro
popd
%make_build -C %{name}_qt5

mkdir %{name}_qt6
pushd %{name}_qt6
%qmake_qt6 \
  CONFIG+=release \
  QMF_INSTALL_ROOT=%{_prefix} LIBDIR=%{_libdir} ../signon.pro
popd
%make_build -C %{name}_qt6

%install
make install INSTALL_ROOT=%{buildroot} -C %{name}_qt5
make install INSTALL_ROOT=%{buildroot} -C %{name}_qt6
# Removing additional unneeded files
rm %{buildroot}%{_libdir}/libsignon-qt5.a
rm %{buildroot}%{_libdir}/libsignon-qt6.a

# create/own libdir/extensions
mkdir -p %{buildroot}%{_libdir}/extensions/

%files
## fixme: common/shared _docdir/signon content below gets in the way
#doc README.md TODO NOTES
%license COPYING
%config(noreplace) %{_sysconfdir}/signond.conf
%{_bindir}/signond
%{_bindir}/signonpluginprocess
%{_libdir}/libsignon-extension.so.1*
%{_libdir}/libsignon-plugins-common.so.1*
%{_libdir}/libsignon-plugins.so.1*
%{_libdir}/signon/
%{_datadir}/dbus-1/services/*.service

%files qt5
%{_libdir}/libsignon-qt5.so.1{,.*}

%files qt6
%{_libdir}/libsignon-qt6.so.1{,.*}

%files devel
%{_includedir}/signon-extension/
%{_includedir}/signon-plugins/
%{_includedir}/signond/
%{_libdir}/libsignon-extension.so
%{_libdir}/libsignon-plugins-common.so
%{_libdir}/libsignon-plugins.so
%{_libdir}/pkgconfig/SignOnExtension.pc
%{_libdir}/pkgconfig/signon-plugins-common.pc
%{_libdir}/pkgconfig/signon-plugins.pc
%{_libdir}/pkgconfig/signond.pc

%files qt5-devel
%{_includedir}/signon-qt5/
%{_libdir}/cmake/SignOnQt5/
%{_libdir}/pkgconfig/libsignon-qt5.pc
%{_libdir}/libsignon-qt5.so

%files qt6-devel
%{_includedir}/signon-qt6/
%{_libdir}/cmake/SignOnQt6/
%{_libdir}/pkgconfig/libsignon-qt6.pc
%{_libdir}/libsignon-qt6.so

%files doc
%{_docdir}/signon/
%{_docdir}/libsignon-qt/
%{_docdir}/signon-plugins/
%{_docdir}/signon-plugins-dev/


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 8.60^20240205.c8ad982-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 8.60^20240205.c8ad982-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 8.60^20240205.c8ad982-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Feb 05 2024 Alessandro Astone <ales.astone@gmail.com> - 8.60^20240205.c8ad982-1
- Update git snapshot

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 8.60^20231015.171500.011bd15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Dec 26 2023 Alessandro Astone <ales.astone@gmail.com> - 8.60^20231015.171500.011bd15-3
- Split libsignon-qt in subpackages

* Sun Dec 3 2023 Steve Cossette <farchord@gmail.com> - 8.60^20231015.171500.011bd15-2
- Rebuild

* Tue Nov 21 2023 Steve Cossette <farchord@gmail.com> - 8.60^20231015.171500.011bd15-1
- Qt6 Build

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 8.60-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 8.60-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 8.60-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 8.60-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 8.60-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 8.60-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sun Nov 08 2020 Rex Dieter <rdieter@fedoraproject.org> - 8.60-7
- build without -Werror -fno-rtti (#1891251)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 8.60-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 8.60-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 8.60-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue May 07 2019 Fabio Valentini <decathorpe@gmail.com> - 8.60-3
- Make conflict with gsignond explicit to fix upgrade issues.

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 8.60-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Oct 20 2018 Rex Dieter <rdieter@fedoraproject.org> - 8.60-1
- signon-8.60 (#1640986)

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 8.59-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 8.59-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 8.59-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 8.59-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 8.59-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jun 08 2016 Rex Dieter <rdieter@fedoraproject.org> 8.59-2
- %%check: time checks

* Tue Jun 07 2016 Rex Dieter <rdieter@fedoraproject.org> - 8.59-1
- 8.59 (#1343792) 

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 8.58-0.2.9fcfc9e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Dec 21 2015 Rex Dieter <rdieter@fedoraproject.org> 8.58-0.1
- 8.58 snapshot, FTBFS against qt-5.6

* Mon Dec 21 2015 Rex Dieter <rdieter@fedoraproject.org> 8.57-8
- fix/update URL/Source0, move xml interface files to -devel, Provides: signond, use %%license

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.57-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 04 2015 Daniel Vrátil <dvratil@redhat.com> - 8.57-6
- Obsoletes/Provides signon-qt5 (for compatibility with COPR)

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 8.57-5
- Rebuilt for GCC 5 C++11 ABI change

* Wed Apr 08 2015 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 8.57-4
- force proper libdir - fixes build on 64-bit architectures other than x86-64

* Wed Apr 01 2015 Rex Dieter <rdieter@fedoraproject.org> - 8.57-3
- %%files: track closer, less globs (sonames, pkgconfig)
- own libdir/extensions/
- patch out building of (unused) static lib

* Sat Mar 28 2015 Daniel Vrátil <dvratil@redhat.com> - 8.57-2
- rename to signon
- drop glib2-devel dep
- fix %%changelog

* Tue Mar 17 2015 Daniel Vrátil <dvratil@redhat.com> - 8.57-1
- rename to signon-qt5, update

* Wed Feb 26 2014 Daniel Vrátil <dvratil@redhat.com> - 8.56-1
- initial version

