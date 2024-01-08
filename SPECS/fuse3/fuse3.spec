Summary:        File System in Userspace (FUSE) v3 utilities
Name:           fuse3
Version:        3.16.2
Release:        1%{?dist}
License:        GPL+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/libfuse/libfuse
Source0:        https://github.com/libfuse/libfuse/archive/fuse-%{version}.tar.gz
Source1:        fuse.conf
Patch0:         fuse3-gcc11.patch
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libselinux-devel
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  libudev-devel
BuildRequires:  which
Requires:       fuse-common = %{version}-%{release}

%description
With FUSE it is possible to implement a fully functional filesystem in a
userspace program. This package contains the FUSE v3 userspace tools to
mount a FUSE filesystem.

%package libs
Summary:        File System in Userspace (FUSE) v3 libraries
License:        LGPLv2+

%description libs
Devel With FUSE it is possible to implement a fully functional filesystem in a
userspace program. This package contains the FUSE v3 libraries.

%package devel
Summary:        File System in Userspace (FUSE) v3 devel files
License:        LGPLv2+
Requires:       %{name}-libs = %{version}-%{release}
Requires:       pkg-config

%description devel
With FUSE it is possible to implement a fully functional filesystem in a
userspace program. This package contains development files (headers,
pgk-config) to develop FUSE v3 based applications/filesystems.

%package -n fuse-common
Summary:        Common files for File System in Userspace (FUSE) v2 and v3
License:        GPL+

%description -n fuse-common
Common files for FUSE v2 and FUSE v3.

%prep
%autosetup -p1 -n fuse-%{version}

%build
export LC_ALL=en_US.UTF-8
%if ! 0%{?_vpath_srcdir:1}
%global _vpath_srcdir .
%endif
%if ! 0%{?_vpath_builddir:1}
%global _vpath_builddir build
%endif
%meson

(cd %{_vpath_builddir}
# don't have root for installation
meson configure -D useroot=false
ninja-build reconfigure
)
%meson_build

%install
export MESON_INSTALL_DESTDIR_PREFIX=%{buildroot}%{_prefix} %meson_install
find %{buildroot} -type f -name "*.la" -delete -print
find %{buildroot} -type f -name "*.a" -delete -print
# change from 4755 to 0755 to allow stripping -- fixed later in files
chmod 0755 %{buildroot}/%{_bindir}/fusermount3

# No need to create init-script
rm -f %{buildroot}%{_sysconfdir}/init.d/fuse3

# Install config-file
install -p -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}

# Delete pointless udev rules, which do not belong in /usr/lib (brc#748204)
rm -f %{buildroot}%{_libdir}/udev/rules.d/99-fuse3.rules

%ldconfig_scriptlets libs

%files
%license LICENSE GPL2.txt
%doc AUTHORS ChangeLog.rst README.md
%{_sbindir}/mount.fuse3
%attr(4755,root,root) %{_bindir}/fusermount3
%{_mandir}/man1/*
%{_mandir}/man8/*

%files libs
%license LGPL2.txt
%{_libdir}/libfuse3.so.*

%files devel
%{_libdir}/libfuse3.so
%{_libdir}/pkgconfig/fuse3.pc
%{_includedir}/fuse3/

%files -n fuse-common
%config(noreplace) %{_sysconfdir}/fuse.conf

%changelog
* Thu Dec 21 2023 Muhammad Falak <mwani@microsoft.com> - 3.16.2-1
- Upgrade version to 3.16.2
- Add a requires on fuse-common instead of a config-file

* Wed Sep 22 2021 Thomas Crain <thcrain@microsoft.com> - 3.10.5-2
- Initial CBL-Mariner import from Fedora 35 (license: MIT)
- Spec linted
- License verified

* Thu Sep 16 2021 Tom Callaway <spot@fedoraproject.org> - 3.10.5-1
- update to 3.10.5

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 15 2021 Tom Callaway <spot@fedoraproject.org> - 3.10.4-1
- update to 3.10.4

* Thu May  6 2021 Tom Callaway <spot@fedoraproject.org> - 3.10.3-1
- update to 3.10.3

* Fri Feb  5 2021 Tom Callaway <spot@fedoraproject.org> - 3.10.2-1
- update to 3.10.2

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Dec  7 2020 Tom Callaway <spot@fedoraproject.org> - 3.10.1-1
- update to 3.10.1

* Wed Oct 14 2020 Jeff Law <law@redhat.com> - 3.10.0-2
- Add missing #include for gcc-11

* Mon Oct 12 2020 Tom Callaway <spot@fedoraproject.org> - 3.10.0-1
- update to 3.10.0
- enable lto

* Mon Aug 10 2020 Tom Callaway <spot@fedoraproject.org> - 3.9.4-1
- update to 3.9.4

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul  1 2020 Jeff Law <law@redhat.com> - 3.9.2-2
- Disable LTO

* Thu Jun 18 2020 Tom Callaway <spot@fedoraproject.org> - 3.9.2-1
- update to 3.9.2

* Thu Mar 19 2020 Tom Callaway <spot@fedoraproject.org> - 3.9.1-1
- update to 3.9.1

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Dec 16 2019 Tom Callaway <spot@fedoraproject.org> - 3.9.0-1
- update to 3.9.0

* Mon Nov  4 2019 Tom Callaway <spot@fedoraproject.org> - 3.8.0-1
- update to 3.8.0

* Fri Sep 27 2019 Tom Callaway <spot@fedoraproject.org> - 3.7.0-1
- update to 3.7.0

* Sun Sep  1 2019 Peter Lemenkov <lemenkov@gmail.com> - 3.6.2-1
- Update to 3.6.2

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 03 2019 Dave Dykstra <dwd@fedoraproject.org> - 3.6.1-3
- Update to the final version of pr #421

* Wed Jul 03 2019 Dave Dykstra <dwd@fedoraproject.org> - 3.6.1-2
- Update to newer version of pr #421
- Disable building examples on el7

* Thu Jun 13 2019 Tom Callaway <spot@fedoraproject.org> - 3.6.1-1
- Update to 3.6.1

* Fri May 24 2019 Dave Dykstra <dwd@fedoraproject.org> - 3.5.0-1
- Upgrade to upstream 3.5.0

* Sat May 04 2019 Dave Dykstra <dwd@fedoraproject.org> - 3.4.2-7
- Fix building on el6

* Wed May 01 2019 Dave Dykstra <dwd@fedoraproject.org> - 3.4.2-6
- Need Conflicts: fuse-common < 3.4.2-4, because <= 3.4.2-3 isn't quite
  enough.

* Wed May 01 2019 Dave Dykstra <dwd@fedoraproject.org> - 3.4.2-5
- Update the Conflicts: fuse-common <= version to 3.4.2-3

* Wed May 01 2019 Dave Dykstra <dwd@fedoraproject.org> - 3.4.2-4
- Bump release number in order to larger than a rebuild of fuse package
  done before separation pull request was merged.

* Mon Apr 08 2019 Dave Dykstra <dwd@fedoraproject.org> - 3.4.2-3
- Separate out from fuse package
