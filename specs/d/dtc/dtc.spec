# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global with_mingw 0

%if 0%{?fedora}
%global with_mingw 1
%endif

%undefine _auto_set_build_flags

Name:          dtc
Version:       1.7.2
Release: 8%{?dist}
Summary:       Device Tree Compiler
License:       GPL-2.0-or-later
URL:           https://devicetree.org/

Source0:       https://www.kernel.org/pub/software/utils/%{name}/%{name}-%{version}.tar.xz
Patch0001:     0001-build-fix-Dtools-false-build.patch

BuildRequires: gcc make
BuildRequires: flex bison swig
BuildRequires: python3-devel
BuildRequires: python3-pip
BuildRequires: python3-setuptools
BuildRequires: python3-setuptools_scm
BuildRequires: python3-wheel

%if %{with_mingw}
BuildRequires: mingw32-filesystem >= 95
BuildRequires: mingw32-gcc-c++

BuildRequires: meson

BuildRequires: mingw64-filesystem >= 95
BuildRequires: mingw64-gcc-c++
%endif

%description
Devicetree is a data structure for describing hardware. Rather than hard coding
every detail of a device into an operating system, many aspects of the hardware
can be described in a data structure that is passed to the operating system at
boot time. The devicetree is used by OpenFirmware, OpenPOWER Abstraction Layer
(OPAL), Power Architecture Platform Requirements (PAPR) and in the standalone
Flattened Device Tree (FDT) form.

%package -n libfdt
Summary: Device tree library

%description -n libfdt
libfdt is a library to process Open Firmware style device trees on various
architectures.

%package -n libfdt-devel
Summary: Development headers for device tree library
Requires: libfdt = %{version}-%{release}

%description -n libfdt-devel
This package provides development files for libfdt

%package -n libfdt-static
Summary: Static version of device tree library
Requires: libfdt-devel = %{version}-%{release}

%description -n libfdt-static
This package provides the static library of libfdt

%package -n python3-libfdt
Summary: Python 3 bindings for device tree library
%{?python_provide:%python_provide python2-libfdt}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description -n python3-libfdt
This package provides python2 bindings for libfdt

%if %{with_mingw}
%package -n mingw32-libfdt
Summary: MinGW Device tree library
BuildArch: noarch

%description -n mingw32-libfdt
libfdt is a library to process Open Firmware style device trees on various
architectures.

%package -n mingw32-libfdt-static
Summary: Static version of MinGW Device tree library
Requires: mingw32-libfdt = %{version}-%{release}
BuildArch: noarch

%description -n mingw32-libfdt-static
This package provides the static library of mingw32-libfdt

%package -n mingw64-libfdt
Summary: MinGW Device tree library
BuildArch: noarch

%description -n mingw64-libfdt
libfdt is a library to process Open Firmware style device trees on various
architectures.

%package -n mingw64-libfdt-static
Summary: Static version of MinGW Device tree library
Requires: mingw64-libfdt = %{version}-%{release}
BuildArch: noarch

%description -n mingw64-libfdt-static
This package provides the static library of mingw64-libfdt

%{?mingw_debug_package}
%endif

%prep
%autosetup -p1
# to prevent setuptools from installing an .egg, we need to pass --root to setup.py install
# since $(PREFIX) already contains %%{buildroot}, we set root to /
# .eggs are going to be deprecated, see https://github.com/pypa/pip/issues/11501
sed -i 's@--prefix=$(PREFIX)@--prefix=$(PREFIX) --root=/@' pylibfdt/Makefile.pylibfdt


%build
export SETUPTOOLS_SCM_PRETEND_VERSION=%{version}
%{make_build} EXTRA_CFLAGS="%{build_cflags}" LDFLAGS="%{build_ldflags}"

%if %{with_mingw}
%mingw_meson -Dtools=false -Dtests=false
%mingw_ninja
%endif

%install
export SETUPTOOLS_SCM_PRETEND_VERSION=%{version}
%{make_install} V=1 DESTDIR=%{buildroot} PREFIX=%{buildroot}/%{_prefix} \
                LIBDIR=%{_libdir} BINDIR=%{_bindir} INCLUDEDIR=%{_includedir}

%if %{with_mingw}
%mingw_ninja_install
%mingw_debug_install_post
%endif

%ldconfig_scriptlets -n libfdt

%files
%license GPL
%doc Documentation/manual.txt
%{_bindir}/*

%files -n libfdt
%license GPL
%{_libdir}/libfdt.so.1*

%files -n libfdt-static
%{_libdir}/libfdt.a

%files -n libfdt-devel
%{_libdir}/libfdt.so
%{_includedir}/*fdt*

%files -n python3-libfdt
%{python3_sitearch}/libfdt-%{version}-py%{python3_version}.egg-info/
%{python3_sitearch}/_libfdt%{python3_ext_suffix}
%pycached %{python3_sitearch}/libfdt.py

%if %{with_mingw}
%files -n mingw32-libfdt
%license GPL
%{mingw32_bindir}/libfdt-1.dll
%{mingw32_includedir}/*fdt*.h
%{mingw32_libdir}/libfdt.dll.a
%{mingw32_libdir}/pkgconfig/libfdt.pc

%files -n mingw32-libfdt-static
%{mingw32_libdir}/libfdt.a

%files -n mingw64-libfdt
%license GPL
%{mingw64_bindir}/libfdt-1.dll
%{mingw64_includedir}/*fdt*.h
%{mingw64_libdir}/libfdt.dll.a
%{mingw64_libdir}/pkgconfig/libfdt.pc

%files -n mingw64-libfdt-static
%{mingw64_libdir}/libfdt.a
%endif

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.7.2-7
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.7.2-6
- Rebuilt for Python 3.14.0rc2 bytecode

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 1.7.2-4
- Rebuilt for Python 3.14

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Nov 11 2024 Marc-André Lureau <marcandre.lureau@redhat.com> - 1.7.2-2
- Enable back mingw build

* Sun Nov 10 2024 Peter Robinson <pbrobinson@fedoraproject.org> - 1.7.2-1
- Update to 1.7.2

* Thu Sep 19 2024 Peter Robinson <pbrobinson@fedoraproject.org> - 1.7.1-1
- Update to 1.7.1

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jul 11 2024 Dan Horák <dan[at]danny.cz> - 1.7.0-10
- use distro flags to compile the python extension

* Thu Jun 27 2024 Dan Horák <dan[at]danny.cz> - 1.7.0-9
- avoid rebuilding python extension during %%install without distro-wide compiler/linker flags

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.7.0-8
- Rebuilt for Python 3.13

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Sep 27 2023 Miro Hrončok <mhroncok@redhat.com> - 1.7.0-5
- Don't install a Python .egg

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 05 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 1.7.0-3
- Rebuilt for Python 3.12

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 1.7.0-2
- Rebuilt for Python 3.12

* Mon Mar 20 2023 Peter Robinson <pbrobinson@fedoraproject.org> - 1.7.0-1
- Update to 1.7.0

* Mon Feb 13 2023 Josh Boyer <jwboyer@fedoraproject.org> - 1.6.1-8
- migrated to SPDX license

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Sep 14 2022 Marc-André Lureau <marcandre.lureau@redhat.com> - 1.6.1-6
- Add mingw sub-packages. Fixes rhbz#1997511

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.6.1-4
- Rebuilt for Python 3.11

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 08 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 1.6.1-1
- Update to 1.6.1

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.6.0-5
- Rebuilt for Python 3.10

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.6.0-2
- Rebuilt for Python 3.9

* Fri Mar 13 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 1.6.0-1
- Update to 1.6.0

* Thu Jan 30 2020 Peter Robinson <pbrobinson@fedoraproject.org> 1.5.1-4
- Upstream patch to fix gcc-10 build

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 14 2020 Tom Stellard <tstellar@redhat.com> - 1.5.1-2
- Use __cc macro instead of hard-coding gcc

* Wed Sep 11 2019 Peter Robinson <pbrobinson@fedoraproject.org> 1.5.1-1
- New dtc 1.5.1 release

* Tue Sep 10 2019 Miro Hrončok <mhroncok@redhat.com> - 1.5.0-3
- Rebuilt for Python 3.8

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Mar 12 2019 Peter Robinson <pbrobinson@fedoraproject.org> 1.5.0-1
- New dtc 1.5.0 release

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 15 2019 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.7-2
- Upstream fix for crash (rhbz 1663054)

* Sat Aug 18 2018 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.7-1
- New dtc 1.4.7 release

* Tue Jul 17 2018 Miro Hrončok <mhroncok@redhat.com> - 1.4.6-7
- Update Python macros to new packaging standards
  (See https://fedoraproject.org/wiki/Changes/Move_usr_bin_python_into_separate_package)

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 06 2018 Bas Mevissen <abuse@basmevissen.nl> 1.4.6-5
- Add static library package, see BZ#1440975

* Wed Mar  7 2018 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.6-4
- Add gcc BR

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 26 2018 Florian Weimer <fweimer@redhat.com> - 1.4.6-2
- Use Fedora build flags during build

* Mon Jan 22 2018 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.6-1
- New dtc 1.4.6 release

* Thu Sep 28 2017 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.5-1
- New dtc 1.4.5 release

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 12 2017 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.4-2
- Add upstream patches for python bindings

* Fri Mar 17 2017 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.4-1
- New dtc 1.4.4 release

* Tue Feb 28 2017 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.2-3.0931cea
- Rebase to same git snapshot that kernel is using for DT Overlays

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Sep 11 2016 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.2-1
- New dtc 1.4.2 release

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jun 16 2015 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.1-4
- Use %%license

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 1.4.1-3
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Mon Jan  5 2015 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.1-2
- Use tar file from kernel.org

* Mon Jan  5 2015 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.1-1
- New dtc 1.4.1 release
- Update URL and Sources
- Cleanup spec

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Dec 21 2013 Ville Skyttä <ville.skytta@iki.fi> - 1.4.0-3
- Avoid shell invocation and fix deps of libfdt %%post* scripts.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 24 2013 Josh Boyer <jwboyer@redhat.com> - 1.4.0-1
- New dtc 1.4.0 release (rhbz 977480)

* Thu Jun 06 2013 Josh Boyer <jwboyer@redhat.com> - 1.3.0-8
- Fix type specifier error (from Dan Horák)

* Mon Jun 03 2013 Josh Boyer <jwboyer@redhat.com> - 1.3.0-7
- Update dtc to include libfdt_env.h (rhbz 969955)

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Feb 27 2012 Josh Boyer <jwboyer@redhat.com>
- Don't package ftdump (rhbz 797805)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 28 2011 Josh Boyer <jwboyer@gmail.com>
- Fixup error during tarball upload

* Tue Jun 28 2011 Josh Boyer <jwboyer@gmail.com>
- Point to git tree for URL (#717217)
- Add libfdt subpackages based on patch from Paolo Bonzini (#443882)
- Update to latest release

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Aug 28 2008 Josh Boyer <jwboyer@gmail.com>
- Update to latest release

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.1.0-2
- Autorebuild for GCC 4.3

* Thu Jan 24 2008 Josh Boyer <jwboyer@gmail.com>
- Update to 1.1.0

* Tue Aug 21 2007 Josh Boyer <jwboyer@jdub.homelinux.org>
- Bump and rebuild

* Thu Aug 09 2007 Josh Boyer <jwboyer@jdub.homelinux.org>
- Update to official 1.0.0 release

* Fri Aug 03 2007 Josh Boyer <jwboyer@jdub.homelinux.org>
- Update license field

* Mon Jul 09 2007 Josh Boyer <jwboyer@jdub.homelinux.org>
- Update to new snapshot

* Tue Jul 03 2007 Josh Boyer <jwboyer@jdub.homelinux.org>
- Update to new snapshot
- Drop upstreamed install patch

* Fri Jun 29 2007 Josh Boyer <jwboyer@jdub.homelinux.org>
- Fix packaging errors

* Thu Jun 28 2007 Josh Boyer <jwboyer@jdub.homelinux.org>
- Initial packaging
