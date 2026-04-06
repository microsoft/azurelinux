# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Need to be specific for flatpak builds, otherwise it'll create rules
# in other directory than /app/etc which will make builds fail.
# On Fedora, this should be the same definition.
%if 0%{?flatpak}
%global _udevrulesdir %{_prefix}/lib/udev/rules.d
%endif

%global xyz_version 3.17.1
%global xy_version %(sed 's/\\(.*\\)\\..*/\\1/'<<<%{xyz_version})

Name:		fuse3
Version:	%{xyz_version}
Release:	3%{?dist}
Summary:	File System in Userspace (FUSE) v3 utilities
License:	GPL-1.0-or-later
URL:		http://fuse.sf.net
Source0:	https://github.com/libfuse/libfuse/releases/download/fuse-%{version}/fuse-%{version}.tar.gz
Source1:	https://github.com/libfuse/libfuse/releases/download/fuse-%{version}/fuse-%{version}.tar.gz.sig
Source2:	https://raw.githubusercontent.com/libfuse/libfuse/master/signify/fuse-%{xy_version}.pub
Source3:	fuse.conf
Patch:		fuse3-0001-lib-remove-second-fuse_main_real_versioned-declarati.patch

%if %{undefined rhel}
BuildRequires:	signify
%endif
BuildRequires:	which
BuildRequires:	libselinux-devel
BuildRequires:	meson, ninja-build, gcc, gcc-c++
BuildRequires:	systemd-udev
# for fuse.conf
Requires:	fuse-common

# The dependency from fuse3 to fuse3-libs is already implicit through
# the generated library dependency, but unless we force the exact
# version then we risk mixing different fuse3 & fuse3-libs versions
# which is not likely to be a well-tested situation upstream.
Requires:	%{name}-libs = %{version}-%{release}

%description
With FUSE it is possible to implement a fully functional filesystem in a
userspace program. This package contains the FUSE v3 userspace tools to
mount a FUSE filesystem.

%package libs
Summary:	File System in Userspace (FUSE) v3 libraries
License:	LGPL-2.1-or-later

%description libs
Devel With FUSE it is possible to implement a fully functional filesystem in a
userspace program. This package contains the FUSE v3 libraries.

%package devel
Summary:	File System in Userspace (FUSE) v3 devel files
Requires:	%{name}-libs = %{version}-%{release}
Requires:	pkgconfig
License:	LGPL-2.1-or-later

%description devel
With FUSE it is possible to implement a fully functional filesystem in a
userspace program. This package contains development files (headers,
pgk-config) to develop FUSE v3 based applications/filesystems.

%package -n fuse-common
Summary:	Common files for File System in Userspace (FUSE) v2 and v3
License:	GPL-1.0-or-later

%description -n fuse-common
Common files for FUSE v2 and FUSE v3.

%prep
%if %{undefined rhel}
# Fuse is using signify rather than PGG since 3.15.1 For more details see:
#	https://github.com/libfuse/libfuse/releases/tag/fuse-3.15.1
signify -V -m  '%{SOURCE0}' -p '%{SOURCE2}'
%endif

%autosetup -p1 -n fuse-%{version}

%build
export LC_ALL=en_US.UTF-8
%meson -D udevrulesdir=%{_udevrulesdir} -D useroot=false
%meson_build

%install
%meson_install
find %{buildroot} .
# change from 4755 to 0755 to allow stripping -- fixed later in files
chmod 0755 %{buildroot}/%{_bindir}/fusermount3

# No need to create init-script
rm -f %{buildroot}%{_sysconfdir}/init.d/fuse3
# This path is hardcoded:
# https://github.com/libfuse/libfuse/blob/master/util/install_helper.sh#L43
# so flatpaks will fail unless we delete it below.
rm -f %{buildroot}/etc/init.d/fuse3


# Install config-file
install -p -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}

# Delete pointless udev rules (brc#748204)
rm -f %{buildroot}%{_udevrulesdir}/99-fuse3.rules

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
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.17.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jul 16 2025 Peter Lemenkov <lemenkov@gmail.com> - 3.17.1-2
- Fix building with modern GCC

* Mon Mar 24 2025 Pavel Reichl <preichl@redhat.com> - 3.17.1-1
- Update to upstream v3.17.1

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.16.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.16.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.16.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.16.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Oct 13 2023 Pavel Reichl <preichl@redhat.com> - 3.16.2-1
- Rebase to upstream version 3.16.2

* Tue Oct 03 2023 Pavel Reichl <preichl@redhat.com> - 3.16.1-3
- Convert License tag to SPDX format

* Tue Aug 15 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 3.16.1-2
- Skip tarball signature verification in RHEL builds

* Wed Aug 09 2023 Pavel Reichl <preichl@redhat.com> - 3.16.1-1
- update to 3.16.1
- Add tarball signature verification

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.14.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jun 26 2023 Richard W.M. Jones <rjones@redhat.com> - 3.14.1-2
- Force fuse3 and fuse3-libs versions to be identical
  https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/thread/LYQUYUAS7FG6FFGJBBWP7XEV563V4LBS/

* Mon Apr  3 2023 Tom Callaway <spot@fedoraproject.org> - 3.14.1-1
- update to 3.14.1

* Tue Feb 28 2023 Richard W.M. Jones <rjones@redhat.com> - 3.14.0-1
- Update to 3.14.0

* Wed Feb  8 2023 Tom Callaway <spot@fedoraproject.org> - 3.13.1-1
- update to 3.13.1

* Fri Jan 20 2023 Tom Callaway <spot@fedoraproject.org> - 3.13.0-1
- update to 3.13.0

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Sep  9 2022 Tom Callaway <spot@fedoraproject.org> - 3.12.0-1
- update to 3.12.0

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Feb 21 2022 Tom Callaway <spot@fedoraproject.org> - 3.10.5-4
- force udevrulesdir option for flatpak builds

* Wed Feb 16 2022 Tom Callaway <spot@fedoraproject.org> - 3.10.5-3
- fix flatpak issues

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

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
