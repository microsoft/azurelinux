## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 2;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# All Azure Linux specs with overlays include this macro file, irrespective of whether new macros have been added.
%{load:%{_sourcedir}/libusb1.azl.macros}

%bcond mingw %[0%{?fedora} && !0%{?flatpak}]

Summary:        Library for accessing USB devices
Name:           libusb1
Version:        1.0.30
Release:        %autorelease
Source0:        https://github.com/libusb/libusb/releases/download/v%{version}/libusb-%{version}.tar.bz2
Source1:        https://github.com/libusb/libusb/releases/download/v%{version}/libusb-%{version}.tar.bz2.asc
Source2:        https://keyserver.ubuntu.com/pks/lookup?op=get&search=0xc68187379b23de9efc46651e2c80ff56c6830a0e#/%{name}.keyring
Source9999: libusb1.azl.macros
License:        LGPL-2.1-or-later
URL:            http://libusb.info
BuildRequires:  systemd-devel doxygen libtool
BuildRequires:  umockdev-devel
BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  gnupg2
# libusbx was removed in F34
Provides:       libusbx = %{version}-%{release}
Obsoletes:      libusbx < %{version}-%{release}

%if %{with mingw}
BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw64-gcc-c++
# mingw-libusbx was removed in F42
Provides:       mingw-libusbx = %{version}-%{release}
Obsoletes:      mingw-libusbx < %{version}-%{release}
%endif

%description
This package provides a way for applications to access USB devices.

libusb is a library for USB device access from Linux, macOS,
Windows, OpenBSD/NetBSD, Haiku and Solaris userspace.

libusb is abstracted internally in such a way that it can hopefully
be ported to other operating systems.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       libusbx-devel = %{version}-%{release}
Obsoletes:      libusbx-devel < %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package devel-doc
Summary:        Development files for %{name}
Requires:       libusb1-devel = %{version}-%{release}
Provides:       libusbx-devel-doc = %{version}-%{release}
Obsoletes:      libusbx-devel-doc < %{version}-%{release}
BuildArch:      noarch

%description devel-doc
This package contains API documentation for %{name}.


%package        tests-examples
Summary:        Tests and examples for %{name}
# The fxload example is GPL-2.0-or-later, the rest is LGPL-2.1-or-later, like libusb itself.
License:        LGPL-2.1-or-later AND GPL-2.0-or-later
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       libusbx-tests-examples = %{version}-%{release}
Obsoletes:      libusbx-tests-examples < %{version}-%{release}

%description tests-examples
This package contains tests and examples for %{name}.

%if %{with mingw}
%package -n mingw32-%{name}
Summary:       MinGW Windows %{name} library
Provides:      mingw32-libusbx = %{version}-%{release}
Obsoletes:     mingw32-libusbx < %{version}-%{release}

%description -n mingw32-%{name}
MinGW Windows %{name} library.

%package -n mingw64-%{name}
Summary:       MinGW Windows %{name} library
Provides:      mingw64-libusbx = %{version}-%{release}
Obsoletes:     mingw64-libusbx < %{version}-%{release}

%description -n mingw64-%{name}
MinGW Windows %{name} library.
%endif

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -p1 -n libusb-%{version}

%build
mkdir %{_target_os}
pushd %{_target_os}
%define _configure ../configure
%configure --disable-static --enable-examples-build
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
%{make_build}
pushd doc
make docs
popd
pushd tests
make
popd
popd

%if %{with mingw}
# MinGW build
%mingw_configure --disable-static
%mingw_make_build
%endif


%install
pushd %{_target_os}
%{make_install}
mkdir -p $RPM_BUILD_ROOT%{_bindir}
install -m 755 tests/init_context $RPM_BUILD_ROOT%{_bindir}/libusb-test-init_context
install -m 755 tests/set_option $RPM_BUILD_ROOT%{_bindir}/libusb-test-set_option
install -m 755 tests/stress $RPM_BUILD_ROOT%{_bindir}/libusb-test-stress
install -m 755 tests/stress_mt $RPM_BUILD_ROOT%{_bindir}/libusb-test-stress_mt
install -m 755 tests/.libs/umockdev $RPM_BUILD_ROOT%{_bindir}/libusb-test-umockdev
install -m 755 examples/.libs/testlibusb \
    $RPM_BUILD_ROOT%{_bindir}/libusb-test-libusb
# Some examples are very device-specific / require specific hw and miss --help
# So we only install a subset of more generic / useful examples
for i in fxload listdevs xusb; do
    install -m 755 examples/.libs/$i \
        $RPM_BUILD_ROOT%{_bindir}/libusb-example-$i
done
rm $RPM_BUILD_ROOT%{_libdir}/*.la
popd

%if %{with mingw}
%mingw_make_install
%endif


%check
pushd %{_target_os}
LD_LIBRARY_PATH=libusb/.libs ldd $RPM_BUILD_ROOT%{_bindir}/libusb-test-stress
LD_LIBRARY_PATH=libusb/.libs $RPM_BUILD_ROOT%{_bindir}/libusb-test-init_context
LD_LIBRARY_PATH=libusb/.libs $RPM_BUILD_ROOT%{_bindir}/libusb-test-set_option
LD_LIBRARY_PATH=libusb/.libs $RPM_BUILD_ROOT%{_bindir}/libusb-test-stress
LD_LIBRARY_PATH=libusb/.libs $RPM_BUILD_ROOT%{_bindir}/libusb-test-umockdev
LD_LIBRARY_PATH=libusb/.libs $RPM_BUILD_ROOT%{_bindir}/libusb-test-libusb
LD_LIBRARY_PATH=libusb/.libs $RPM_BUILD_ROOT%{_bindir}/libusb-example-listdevs
popd


%ldconfig_scriptlets


%files
%license COPYING
%doc AUTHORS README ChangeLog
%{_libdir}/*.so.*

%files devel
%{_includedir}/libusb-1.0
%{_libdir}/*.so
%{_libdir}/pkgconfig/libusb-1.0.pc

%files devel-doc
%doc %{_target_os}/doc/api-1.0 examples/*.c

%files tests-examples
%{_bindir}/libusb-example-fxload
%{_bindir}/libusb-example-listdevs
%{_bindir}/libusb-example-xusb
%{_bindir}/libusb-test-init_context
%{_bindir}/libusb-test-set_option
%{_bindir}/libusb-test-stress
%{_bindir}/libusb-test-stress_mt
%{_bindir}/libusb-test-umockdev
%{_bindir}/libusb-test-libusb

%if %{with mingw}
%files -n mingw32-libusb1
%license COPYING
%doc AUTHORS README ChangeLog
%{mingw32_bindir}/libusb-1.0.dll
%{mingw32_includedir}/libusb-1.0
%{mingw32_libdir}/*.dll.a
%{mingw32_libdir}/pkgconfig/libusb-1.0.pc

%files -n mingw64-libusb1
%license COPYING
%doc AUTHORS README ChangeLog
%{mingw64_bindir}/libusb-1.0.dll
%{mingw64_includedir}/libusb-1.0
%{mingw64_libdir}/*.dll.a
%{mingw64_libdir}/pkgconfig/libusb-1.0.pc
%endif

%changelog
## START: Generated by rpmautospec
* Tue Sep 01 2026 Unknown User <please-configure-git-user@example.com> - 1.0.30-2
- Uncommitted changes

* Wed May 20 2026 Kate Hsuan <hpa@redhat.com> - 1.0.30-1
- Update to the upstream version 1.0.30

* Wed Jan 28 2026 Miroslav Suchý <msuchy@redhat.com> - 1.0.29-6
- migrate license to SPDX

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.29-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Fri Aug 29 2025 Kate Hsuan <hpa@redhat.com> - 1.0.29-4
- Revert "Add patches to skip uninitialized devices" (rhbz#2390535)

* Mon Aug 11 2025 Benjamin Berg <benjamin@sipsolutions.net> - 1.0.29-3
- Add patches to skip uninitialized devices

* Tue Aug 05 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 1.0.29-2
- Always regenerate autotools

* Tue Aug 05 2025 Kate Hsuan <hpa@redhat.com> - 1.0.29-1
- Update to the upstream version 1.0.29 and migrate to tmt test

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.28-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Mar 27 2025 Kate Hsuan <hpa@redhat.com> - 1.0.28-2
- Fix the automake 1.17 issue for the versions less than f43 and rhel11

* Wed Mar 26 2025 LuK1337 <priv.luk@gmail.com> - 1.0.28-1
- Update to 1.0.28

* Wed Mar 26 2025 LuK1337 <priv.luk@gmail.com> - 1.0.27-10
- Verify source code with GPG

* Thu Jan 30 2025 Marc-André Lureau <marcandre.lureau@redhat.com> - 1.0.27-9
- Provides/Obsoletes mingw-libusbx

* Mon Jan 20 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.27-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.27-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Jan 13 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 1.0.27-6
- Fix ELN build

* Fri Jan 10 2025 Kate Hsuan <hpa@redhat.com> - 1.0.27-5
- Fix the build failure with automake-1.17

* Tue Oct 22 2024 Jean THOMAS <virgule@jeanthomas.me> - 1.0.27-4
- Add MinGW builds

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.27-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed May 08 2024 Kate Hsuan <hpa@redhat.com> - 1.0.27-2
- Build the test code without a rpath

* Mon Mar 04 2024 Kate Hsuan <hpa@redhat.com> - 1.0.27-1
- Update to 1.0.27
- Update to 1.0.27
- Add tests, including init_context, set_option, and stress_mt

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.26-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.26-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Sep 19 2023 Miroslav Suchý <msuchy@redhat.com> - 1.0.26-4
- Migrate to SPDX license

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.26-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Sep 30 2022 Kate Hsuan <hpa@redhat.com> 1.0.26-1
- Update to 1.0.26 

* Wed Feb 02 2022 Benjamin Berg <bberg@redhat.com> 1.0.25-1
- Update to 1.0.25

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.24-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.24-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 19 18:47:55 CET 2021 Benjamin Berg <bberg@redhat.com> - 1.0.24-3
- New libusb1 package replacing libusbx
  Resolves: #1918269

## END: Generated by rpmautospec
