# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Local definition of version_no_tilde when it doesn't exist
%{!?version_no_tilde: %define version_no_tilde %{shrink:%(echo '%{version}' | tr '~' '-')}}

Name:           btrfs-progs
Version:        6.19
Release: 2%{?dist}
Summary:        Userspace programs for btrfs

License:        GPL-2.0-only
URL:            https://btrfs.readthedocs.io
Source0:        https://www.kernel.org/pub/linux/kernel/people/kdave/%{name}/%{name}-v%{version_no_tilde}.tar.xz
Source1:        https://www.kernel.org/pub/linux/kernel/people/kdave/%{name}/%{name}-v%{version_no_tilde}.tar.sign
Source2:        gpgkey-F2B41200C54EFB30380C1756C565D5F9D76D583B.gpg

# Special patch source, conditionally applied
## Disable RAID56 modes (RHEL-only)
Source1001:     1001-balance-mkfs-Disable-raid56-modes.patch

BuildRequires:  gnupg2
BuildRequires:  gcc, autoconf, automake, make
BuildRequires:  git-core
BuildRequires:  e2fsprogs-devel
BuildRequires:  libacl-devel, lzo-devel
BuildRequires:  pkgconfig(blkid)
BuildRequires:  pkgconfig(uuid)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(libgcrypt) >= 1.8.0
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(libzstd) >= 1.0.0
BuildRequires:  python3-sphinx
BuildRequires:  python3dist(sphinx-rtd-theme)
BuildRequires:  systemd
BuildRequires:  python3-devel >= 3.4

%description
The btrfs-progs package provides all the userspace programs needed to create,
check, modify and correct any inconsistencies in the btrfs filesystem.

%package -n libbtrfs
Summary:        btrfs filesystem-specific runtime libraries
License:        GPL-2.0-only
# Upstream deprecated this library
Provides:       deprecated()
# This was not properly split out before
Conflicts:      %{name} < 4.20.2

%description -n libbtrfs
libbtrfs contains the main library used by btrfs
filesystem-specific programs.

%package -n libbtrfsutil
Summary:        btrfs filesystem-specific runtime utility libraries
License:        LGPL-2.1-or-later
# This was not properly split out before
Conflicts:      %{name}-devel < 4.20.2

%description -n libbtrfsutil
libbtrfsutil contains an alternative utility library used by btrfs
filesystem-specific programs.

%package devel
Summary:        btrfs filesystem-specific libraries and headers
# libbtrfsutil is LGPLv2+
License:        GPL-2.0-only and LGPL-2.1-or-later
Requires:       %{name} = %{version}-%{release}
Requires:       libbtrfs%{?_isa} = %{version}-%{release}
Requires:       libbtrfsutil%{?_isa} = %{version}-%{release}

%description devel
btrfs-progs-devel contains the libraries and header files needed to
develop btrfs filesystem-specific programs.

It includes development files for two libraries:
- libbtrfs (GPLv2)
- libbtrfsutil (LGPLv2+)

You should install btrfs-progs-devel if you want to develop
btrfs filesystem-specific programs.

%package -n python3-btrfsutil
Summary:        Python 3 bindings for libbtrfsutil
License:        LGPL-2.1-or-later
Requires:       libbtrfsutil%{?_isa} = %{version}-%{release}
%{?python_provide:%python_provide python3-btrfsutil}

%description -n python3-btrfsutil
python3-btrfsutil contains Python 3 bindings to the libbtrfsutil library,
which can be used for btrfs filesystem-specific programs in Python.

You should install python3-btrfsutil if you want to use or develop
btrfs filesystem-specific programs in Python.


%prep
xzcat '%{SOURCE0}' | %{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data=-
%autosetup -n %{name}-v%{version_no_tilde} -S git_am

%if 0%{?rhel}
# Specially apply this source
%{?__scm_source_timestamp:GIT_COMMITTER_DATE=%{__scm_source_timestamp}} git am --reject %{SOURCE1001}
%endif

# this generates version.py so we have to run it early
./autogen.sh
%configure CFLAGS="%{optflags} -fno-strict-aliasing" --with-crypto=libgcrypt --disable-python

%generate_buildrequires
pushd libbtrfsutil/python >/dev/null
%pyproject_buildrequires
popd >/dev/null


%build
%make_build

pushd libbtrfsutil/python
%pyproject_wheel
popd


%install
%make_install mandir=%{_mandir} bindir=%{_sbindir} libdir=%{_libdir} incdir=%{_includedir}
install -Dpm0644 btrfs-completion %{buildroot}%{_datadir}/bash-completion/completions/btrfs
# Nuke the static lib
rm -v %{buildroot}%{_libdir}/*.a

pushd libbtrfsutil/python >/dev/null
%pyproject_install
%pyproject_save_files -L btrfsutil
popd >/dev/null


%files
%license COPYING
%{_sbindir}/btrfsck
%{_sbindir}/fsck.btrfs
%{_sbindir}/mkfs.btrfs
%{_sbindir}/btrfs-image
%{_sbindir}/btrfs-convert
%{_sbindir}/btrfs-select-super
%{_sbindir}/btrfstune
%{_sbindir}/btrfs
%{_sbindir}/btrfs-map-logical
%{_sbindir}/btrfs-find-root
%{_mandir}/man5/*btrfs*
%{_mandir}/man8/*btrfs*
%{_udevrulesdir}/64-btrfs-dm.rules
%{_udevrulesdir}/64-btrfs-zoned.rules
%{_datadir}/bash-completion/completions/btrfs

%files -n libbtrfs
%license COPYING
%{_libdir}/libbtrfs.so.0*

%files -n libbtrfsutil
%license libbtrfsutil/COPYING
%{_libdir}/libbtrfsutil.so.1*

%files devel
%{_includedir}/btrfs/
%{_includedir}/btrfsutil.h
%{_libdir}/libbtrfs.so
%{_libdir}/libbtrfsutil.so
%{_libdir}/pkgconfig/libbtrfsutil.pc
%{_mandir}/man2/*btrfs*

%files -n python3-btrfsutil -f %{pyproject_files}
%license libbtrfsutil/COPYING


%changelog
* Fri Feb 13 2026 Packit <hello@packit.dev> - 6.19-1
- Update to version 6.19
- Resolves: rhbz#2439784

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 6.17.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 6.17.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Tue Dec 23 2025 Georg Sauthoff <mail@gms.tf> - 6.17.1-2
- Update URL

* Fri Nov 07 2025 Packit <hello@packit.dev> - 6.17.1-1
- Update to version 6.17.1
- Resolves: rhbz#2413317

* Mon Sep 29 2025 Packit <hello@packit.dev> - 6.17-1
- Update to version 6.17
- Resolves: rhbz#2400219

* Wed Sep 10 2025 Packit <hello@packit.dev> - 6.16.1-1
- Update to version 6.16.1
- Resolves: rhbz#2394433

* Wed Aug 13 2025 Packit <hello@packit.dev> - 6.16-1
- Update to version 6.16
- Resolves: rhbz#2388440

* Sun Aug 03 2025 Michel Lind <salimma@fedoraproject.org> - 6.15-4
- Enable automatic build requirement generation

* Sat Aug 02 2025 Michel Lind <salimma@fedoraproject.org> - 6.15-3
- Stop using deprecated Python macros; Resolves: RHBZ#2377213

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 23 2025 Packit <hello@packit.dev> - 6.15-1
- Update to version 6.15
- Resolves: rhbz#2374347

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 6.14-2
- Rebuilt for Python 3.14

* Wed Mar 26 2025 Packit <hello@packit.dev> - 6.14-1
- Update to version 6.14
- Resolves: rhbz#2355205

* Fri Feb 14 2025 Packit <hello@packit.dev> - 6.13-1
- Update to version 6.13
- Resolves: rhbz#2345871

* Fri Jan 24 2025 Neal Gompa <ngompa@centosproject.org> - 6.12-3
- Add RHEL-only downstream patch to disable raid56 modes for now

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Nov 29 2024 Packit <hello@packit.dev> - 6.12-1
- Update to version 6.12
- Resolves: rhbz#2329568

* Tue Sep 17 2024 Neal Gompa <ngompa@fedoraproject.org> - 6.11-1
- Update to 6.11
  Resolves: rhbz#2312879

* Thu Aug 15 2024 Packit <hello@packit.dev> - 6.10.1-1
- Update to version 6.10.1
- Resolves: rhbz#2305131

* Mon Aug 12 2024 Michel Lind <salimma@fedoraproject.org> - 6.10-1
- Update to version 6.10
- Resolves: rhbz#2301782

* Thu Jul 25 2024 Neal Gompa <ngompa@fedoraproject.org> - 6.9.2-1
- Update to 6.9.2
- Backport fix for Python 3.13 (rhbz#2245650)

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jun 18 2024 Python Maint <python-maint@redhat.com> - 6.9-2
- Rebuilt for Python 3.13

* Wed Jun 12 2024 Neal Gompa <ngompa@fedoraproject.org> - 6.9-1
- Update to 6.9

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 6.8.1-2
- Rebuilt for Python 3.13

* Tue Mar 26 2024 Neal Gompa <ngompa@fedoraproject.org> - 6.8-1
- Update to 6.8

* Wed Feb 14 2024 Neal Gompa <ngompa@fedoraproject.org> - 6.7.1-1
- Update to 6.7.1
- Make file list globs more specific

* Mon Jan 22 2024 Neal Gompa <ngompa@fedoraproject.org> - 6.7-1
- Update to 6.7

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Nov 24 2023 Neal Gompa <ngompa@fedoraproject.org> - 6.6.2-1
- Update to 6.6.2

* Thu Sep 14 2023 Neal Gompa <ngompa@fedoraproject.org> - 6.5.1-1
- Update to 6.5.1

* Sun Aug 20 2023 Neal Gompa <ngompa@fedoraproject.org> - 6.3.3-1
- Update to 6.3.3

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jun 26 2023 Python Maint <python-maint@redhat.com> - 6.3.2-2
- Rebuilt for Python 3.12

* Wed Jun 21 2023 Neal Gompa <ngompa@fedoraproject.org> - 6.3.2-1
- Update to 6.3.2

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 6.3.1-2
- Rebuilt for Python 3.12

* Tue May 30 2023 Neal Gompa <ngompa@fedoraproject.org> - 6.3.1-1
- Update to 6.3.1

* Sun Mar 26 2023 Neal Gompa <ngompa@fedoraproject.org> - 6.2.2-1
- Update to 6.2.2

* Wed Mar 22 2023 Neal Gompa <ngompa@fedoraproject.org> - 6.2.1-2
- Add patch to force default sectorsize to 4k

* Mon Mar 06 2023 Neal Gompa <ngompa@fedoraproject.org> - 6.2.1-1
- Update to 6.2.1

* Wed Jan 25 2023 Neal Gompa <ngompa@fedoraproject.org> - 6.1.3-1
- Update to 6.1.3
- Switch to SPDX license identifiers

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jan 05 2023 Neal Gompa <ngompa@fedoraproject.org> - 6.1.2-1
- Update to 6.1.2

* Tue Jan 03 2023 Neal Gompa <ngompa@fedoraproject.org> - 6.1.1-1
- Update to 6.1.1

* Fri Dec 30 2022 Neal Gompa <ngompa@fedoraproject.org> - 6.1-2
- Add fix to show UUID with "btrfs subvolume list -u"

* Fri Dec 23 2022 Neal Gompa <ngompa@fedoraproject.org> - 6.1-1
- Update to 6.1
- Use libgcrypt for cryptographic hash functions

* Fri Nov 25 2022 Neal Gompa <ngompa@fedoraproject.org> - 6.0.2-1
- Update to 6.0.2

* Fri Nov 04 2022 Igor Raits <ignatenkobrain@fedoraproject.org> - 6.0.1-1
- Update to 6.0.1

* Thu Oct 13 2022 Neal Gompa <ngompa@fedoraproject.org> - 6.0-1
- Update to 6.0

* Thu Oct 13 2022 Neal Gompa <ngompa@fedoraproject.org> - 5.19.1-1
- Update to 5.19.1

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 5.18-2
- Rebuilt for Python 3.11

* Wed May 25 2022 Neal Gompa <ngompa@fedoraproject.org> - 5.18-1
- Update to 5.18

* Wed Feb 16 2022 Neal Gompa <ngompa@fedoraproject.org> - 5.16.2-1
- Update to 5.16.2

* Sat Feb 05 2022 Igor Raits <igor.raits@gmail.com> - 5.16.1-1
- Update to 5.16.1

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Jan 17 2022 Neal Gompa <ngompa@fedoraproject.org> - 5.16-1
- Update to 5.16

* Mon Nov 22 2021 Neal Gompa <ngompa@fedoraproject.org> - 5.15.1-1
- Update to 5.15.1

* Fri Nov 05 2021 Neal Gompa <ngompa@fedoraproject.org> - 5.15-1
- Update to 5.15

* Sat Oct 30 2021 Neal Gompa <ngompa@fedoraproject.org> - 5.14.91-1
- Update to 5.14.91 (5.15~rc1)

* Sat Oct 09 2021 Neal Gompa <ngompa@fedoraproject.org> - 5.14.2-1
- Update to 5.14.2

* Mon Sep 20 2021 Neal Gompa <ngompa@fedoraproject.org> - 5.14.1-1
- Update to 5.14.1

* Fri Sep 10 2021 Neal Gompa <ngompa@fedoraproject.org> - 5.14-2
- Mark libbtrfs as deprecated, per upstream release notes

* Fri Sep 10 2021 Neal Gompa <ngompa@fedoraproject.org> - 5.14-1
- Update to 5.14

* Fri Jul 30 2021 Neal Gompa <ngompa@fedoraproject.org> - 5.13.1-1
- Update to 5.13.1

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jul 13 2021 Neal Gompa <ngompa@fedoraproject.org> - 5.13-1
- Update to 5.13

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 5.12.1-2
- Rebuilt for Python 3.10

* Thu May 13 2021 Neal Gompa <ngompa13@gmail.com> - 5.12.1-1
- Update to 5.12.1

* Mon May 10 2021 Neal Gompa <ngompa13@gmail.com> - 5.12-1
- Update to 5.12

* Sun Mar 28 2021 Igor Raits <ignatenkobrain@fedoraproject.org> - 5.11.1-1
- Update to 5.11.1

* Fri Mar 05 2021 Igor Raits <ignatenkobrain@fedoraproject.org> - 5.11-1
- Update to 5.11

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jan 19 2021 Neal Gompa <ngompa13@gmail.com> - 5.10-1
- New upstream release

* Fri Jan 15 2021 Igor Raits <ignatenkobrain@fedoraproject.org> - 5.10~rc1-1
- Update to 5.10-rc1

* Fri Oct 23 2020 Neal Gompa <ngompa13@gmail.com> - 5.9-1
- New upstream release
- Build Python bindings
- Drop patches incorporated into this release

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 24 2020 Neal Gompa <ngompa13@gmail.com> - 5.7-4
- Backport fix for converting 64-bit ext4 filesystems (#1851674)

* Tue Jul 21 2020 Neal Gompa <ngompa13@gmail.com> - 5.7-3
- Backport fix to not use raid0 by default for mkfs multi-disk (#1855174)

* Wed Jul 08 2020 Carl George <carl@george.computer> - 5.7-2
- Include bash completion

* Thu Jul 02 2020 Neal Gompa <ngompa13@gmail.com> - 5.7-1
- New upstream release

* Tue Jun 30 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 5.7~rc1-1
- Update to 5.7-rc1

* Mon Jun 15 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 5.6.1-2
- Rebuild

* Mon Jun 08 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 5.6.1-1
- Update to 5.6.1

* Sun Apr 05 2020 Neal Gompa <ngompa13@gmail.com> - 5.6-1
- New upstream release

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Dec 06 2019 Neal Gompa <ngompa13@gmail.com> - 5.4-1
- New upstream release

* Sat Aug 24 2019 Neal Gompa <ngompa13@gmail.com> - 5.2.1-1
- New upstream release

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Neal Gompa <ngompa13@gmail.com> - 5.1-1
- New upstream release

* Sun Mar 10 2019 Neal Gompa <ngompa13@gmail.com> - 4.20.2-1
- New upstream release
- Properly split out libraries into libs subpackages
- Slightly modernize the spec

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.19.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Dec 05 2018 Eric Sandeen <sandeen@redhat.com> 4.19.-1
- New usptream release

* Mon Aug 06 2018 Eric Sandeen <sandeen@redhat.com> 4.17.1-1
- New upstream release

* Mon Jul 23 2018 Eric Sandeen <sandeen@redhat.com> 4.17-1
- New upstream release
- Removes deprecated btrfs-debug-tree, btrfs-zero-log

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 4.16-3
- Rebuilt for Python 3.7

* Sun Apr 08 2018 Eric Sandeen <sandeen@redhat.com> 4.16-2
- Fix up header install paths in devel package (#1564881)

* Fri Apr 06 2018 Eric Sandeen <sandeen@redhat.com> 4.16-1
- New upstream release

* Mon Feb 26 2018 Eric Sandeen <sandeen@redhat.com> 4.15.1-2
- BuildRequires: gcc

* Fri Feb 16 2018 Eric Sandeen <sandeen@redhat.com> 4.15.1-1
- New upstream release

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.14.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 05 2018 Eric Sandeen <sandeen@redhat.com> 4.14.1-1
- New upstream release

* Tue Oct 17 2017 Eric Sandeen <sandeen@redhat.com> 4.13.3-1
- New upstream release

* Fri Oct 06 2017 Eric Sandeen <sandeen@redhat.com> 4.13.2-1
- New upstream release

* Tue Sep 26 2017 Eric Sandeen <sandeen@redhat.com> 4.13.1-1
- New upstream release

* Fri Sep 08 2017 Eric Sandeen <sandeen@redhat.com> 4.13-1
- New upstream release

* Mon Aug 28 2017 Eric Sandeen <sandeen@redhat.com> 4.12.1-1
- New upstream release

* Mon Jul 31 2017 Eric Sandeen <sandeen@redhat.com> 4.12-1
- New upstream release

* Mon Jul 31 2017 Igor Gnatenko <ignatenko@redhat.com> - 4.11.1-3
- Add missing BuildRequires: systemd

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.11.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 03 2017 Eric Sandeen <sandeen@redhat.com> 4.11.1-1
- New upstream release

* Thu May 18 2017 Eric Sandeen <sandeen@redhat.com> 4.11-1
- New upstream release

* Wed May 03 2017 Eric Sandeen <sandeen@redhat.com> 4.10.2-1
- New upstream release

* Fri Mar 17 2017 Eric Sandeen <sandeen@redhat.com> 4.10.1-1
- New upstream release

* Wed Mar 8 2017 Eric Sandeen <sandeen@redhat.com> 4.10-1
- New upstream release

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 27 2017 Eric Sandeen <sandeen@redhat.com> 4.9.1-1
- New upstream release

* Wed Jan 25 2017 Eric Sandeen <sandeen@redhat.com> 4.9-2
- Remove unapplied patches

* Fri Dec 23 2016 Eric Sandeen <sandeen@redhat.com> 4.9-1
- New upstream release

* Wed Nov 30 2016 Eric Sandeen <sandeen@redhat.com> 4.8.5-1
- New upstream release

* Fri Nov 25 2016 Eric Sandeen <sandeen@redhat.com> 4.8.4-1
- New upstream release
- btrfs-show-super removed (deprecated upstream)

* Sat Nov 12 2016 Eric Sandeen <sandeen@redhat.com> 4.8.3-1
- New upstream release

* Fri Oct 28 2016 Eric Sandeen <sandeen@redhat.com> 4.8.2-2
- Remove ioctl patch, different fix upstream

* Thu Oct 13 2016 Eric Sandeen <sandeen@redhat.com> 4.8.1-2
- Fix build of apps including ioctl.h (bz#1384413)

* Wed Oct 12 2016 Eric Sandeen <sandeen@redhat.com> 4.8.1-1
- New upstream release

* Wed Oct 12 2016 Eric Sandeen <sandeen@redhat.com> 4.8-1
- New upstream release (FTBFS on 32-bit)

* Wed Sep 21 2016 Eric Sandeen <sandeen@redhat.com> 4.7.3-1
- New upstream release

* Mon Sep 05 2016 Eric Sandeen <sandeen@redhat.com> 4.7.2-1
- New upstream release

* Sat Aug 27 2016 Eric Sandeen <sandeen@redhat.com> 4.7.1-1
- New upstream release

* Mon Aug 01 2016 Eric Sandeen <sandeen@redhat.com> 4.7-1
- New upstream release

* Fri Jun 24 2016 Eric Sandeen <sandeen@redhat.com> 4.6.1-1
- New upstream release

* Wed Jun 15 2016 Eric Sandeen <sandeen@redhat.com> 4.6-1
- New upstream release

* Fri May 13 2016 Eric Sandeen <sandeen@redhat.com> 4.5.3-1
- New upstream release

* Mon May 02 2016 Eric Sandeen <sandeen@redhat.com> 4.5.2-1
- New upstream release

* Thu Mar 31 2016 Eric Sandeen <sandeen@redhat.com> 4.5.1-1
- New upstream release

* Wed Mar 30 2016 Eric Sandeen <sandeen@redhat.com> 4.5-1
- New upstream release

* Fri Feb 26 2016 Eric Sandeen <sandeen@redhat.com> 4.4.1-1
- New upstream release

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 25 2016 Eric Sandeen <sandeen@redhat.com> 4.4-1
- New upstream release

* Wed Nov 18 2015 Eric Sandeen <sandeen@redhat.com> 4.3.1-1
- New upstream release

* Thu Oct 08 2015 Eric Sandeen <sandeen@redhat.com> 4.2.2-1
- New upstream release

* Tue Sep 22 2015 Eric Sandeen <sandeen@redhat.com> 4.2.1-1
- New upstream release

* Thu Sep 03 2015 Eric Sandeen <sandeen@redhat.com> 4.2-1
- New upstream release

* Thu Aug 06 2015 Eric Sandeen <sandeen@redhat.com> 4.1.2-1
- New upstream release
- Fix to reject unknown mkfs options (#1246468)

* Mon Jun 22 2015 Eric Sandeen <sandeen@redhat.com> 4.1-1
- New upstream release

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 20 2015 Eric Sandeen <sandeen@redhat.com> 4.0.1-1
- New upstream release

* Wed Apr 29 2015 Eric Sandeen <sandeen@redhat.com> 4.0-1
- New upstream release

* Thu Mar 26 2015 Eric Sandeen <sandeen@redhat.com> 3.19.1-1
- New upstream release

* Wed Mar 11 2015 Eric Sandeen <sandeen@redhat.com> 3.19-1
- New upstream release

* Tue Jan 27 2015 Eric Sandeen <sandeen@redhat.com> 3.18.2-1
- New upstream release

* Mon Jan 12 2015 Eric Sandeen <sandeen@redhat.com> 3.18.1-1
- New upstream release

* Fri Jan 02 2015 Eric Sandeen <sandeen@redhat.com> 3.18-1
- New upstream release

* Fri Dec 05 2014 Eric Sandeen <sandeen@redhat.com> 3.17.3-1
- New upstream release

* Fri Nov 21 2014 Eric Sandeen <sandeen@redhat.com> 3.17.2-1
- New upstream release

* Mon Oct 20 2014 Eric Sandeen <sandeen@redhat.com> 3.17-1
- New upstream release

* Fri Oct 03 2014 Eric Sandeen <sandeen@redhat.com> 3.16.2-1
- New upstream release
- Update upstream source location

* Wed Aug 27 2014 Eric Sandeen <sandeen@redhat.com> 3.16-1
- New upstream release

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.14.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jun 16 2014 Eric Sandeen <sandeen@redhat.com> 3.14.2-3
- Support specification of UUID at mkfs time (#1094857)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.14.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 30 2014 Eric Sandeen <sandeen@redhat.com> 3.14.2-1
- New upstream release

* Tue Apr 22 2014 Eric Sandeen <sandeen@redhat.com> 3.14.1-1
- New upstream release

* Wed Apr 16 2014 Eric Sandeen <sandeen@redhat.com> 3.14-1
- New upstream release

* Mon Jan 20 2014 Eric Sandeen <sandeen@redhat.com> 3.12-2
- Add proper Source0 URL, switch to .xz

* Mon Nov 25 2013 Eric Sandeen <sandeen@redhat.com> 3.12-1
- It's a new upstream release!

* Thu Nov 14 2013 Eric Sandeen <sandeen@redhat.com> 0.20.rc1.20131114git9f0c53f-1
- New upstream snapshot

* Tue Sep 17 2013 Eric Sandeen <sandeen@redhat.com> 0.20.rc1.20130917git194aa4a-1
- New upstream snapshot
- Deprecated btrfsctl, btrfs-show, and btrfs-vol; still available in btrfs cmd

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20.rc1.20130501git7854c8b-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon May 13 2013 Richard W.M. Jones <rjones@redhat.com> 0.20.rc1.20130501git7854c8b-3
- Add accepted upstream patch to fix SONAME libbtrfs.so -> libbtrfs.so.0

* Thu May 02 2013 Eric Sandeen <sandeen@redhat.com> 0.20.rc1.20130501git7854c8b-2
- Fix subpackage brokenness

* Wed May 01 2013 Eric Sandeen <sandeen@redhat.com> 0.20.rc1.20130501git7854c8b-1
- New upstream snapshot
- btrfs-progs-devel subpackage

* Fri Mar 08 2013 Eric Sandeen <sandeen@redhat.com> 0.20.rc1.20130308git704a08c-1
- New upstream snapshot
- btrfs-restore is now a command in the btrfs utility

* Wed Feb 13 2013 Richard W.M. Jones <rjones@redhat.com> 0.20.rc1.20121017git91d9eec-3
- Include upstream patch to clear caches as a partial fix for RHBZ#863978.

* Thu Nov  1 2012 Josef Bacik <josef@toxicpanda.com> 0.20.rc1.20121017git91d9eec-2
- fix a bug when mkfs'ing a file (rhbz# 871778)

* Wed Oct 17 2012 Josef Bacik <josef@toxicpanda.com> 0.20.rc1.20121017git91d9eec-1
- update to latest btrfs-progs

* Wed Oct 10 2012 Richard W.M. Jones <rjones@redhat.com> 0.19.20120817git043a639-2
- Add upstream patch to correct uninitialized fsid variable
  (possible fix for RHBZ#863978).

* Fri Aug 17 2012 Josef Bacik <josef@toxicpanda.com> 0.19.20120817git043a639-1
- update to latest btrfs-progs

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Apr 25 2012 Josef Bacik <josef@toxicpanda.com> 0.19-19
- make btrfs filesystem show <uuid> actually work (rhbz# 816293)

* Wed Apr 11 2012 Josef Bacik <josef@toxicpanda.com> 0.19-18
- updated to latest btrfs-progs

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Aug 05 2011 Josef Bacik <josef@toxicpanda.com> 0.19-16
- fix build-everything patch to actually build everything

* Fri Aug 05 2011 Josef Bacik <josef@toxicpanda.com> 0.19-15
- actually build btrfs-zero-log

* Thu Aug 04 2011 Josef Bacik <josef@toxicpanda.com> 0.19-14
- bring btrfs-progs uptodate with upstream

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Aug 20 2010 Adam Tkac <atkac redhat com> 0.19-12
- rebuild to ensure F14 has bigger NVR than F13

* Wed Mar 24 2010 Josef Bacik <josef@toxicpanda.com> 0.19-11
- bring btrfs-progs uptodate with upstream, add btrfs command and other
  features.

* Thu Mar 11 2010 Josef Bacik <josef@toxicpanda.com> 0.19-10
- fix dso linking issue and bring btrfs-progs uptodate with upstream

* Tue Feb 2 2010 Josef Bacik <josef@toxicpanda.com> 0.19-9
- fix btrfsck so it builds on newer glibcs

* Tue Feb 2 2010 Josef Bacik <josef@toxicpanda.com> 0.19-8
- fix btrfsctl to return 0 on success and 1 on failure

* Tue Aug 25 2009 Josef Bacik <josef@toxicpanda.com> 0.19-7
- add btrfs-progs-valgrind.patch to fix memory leaks and segfaults

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Josef Bacik <josef@toxicpanda.com> 0.19-5
- add e2fsprogs-devel back to BuildRequires since its needed for the converter

* Wed Jul 15 2009 Josef Bacik <josef@toxicpanda.com> 0.19-4
- change BuildRequires for e2fsprogs-devel to libuuid-devel

* Fri Jun 19 2009 Josef Bacik <josef@toxicpanda.com> 0.19-3
- added man pages to the files list and made sure they were installed properly

* Fri Jun 19 2009 Josef Bacik <josef@toxicpanda.com> 0.19-2
- add a patch for the Makefile to make it build everything again

* Fri Jun 19 2009 Josef Bacik <josef@toxicpanda.com> 0.19-1
- update to v0.19 of btrfs-progs for new format

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 22 2009 Josef Bacik <josef@toxicpanda.com> 0.18-3
- updated label patch

* Thu Jan 22 2009 Josef Bacik <josef@toxicpanda.com> 0.18-2
- add a patch to handle having /'s in labels

* Sat Jan 17 2009 Josef Bacik <josef@toxicpanda.com> 0.18-1
- updated to 0.18 because of the ioctl change in 2.6.29-rc2

* Fri Jan 16 2009 Marek Mahut <mmahut@fedoraproject.org> 0.17-4
- RHBZ#480219 btrfs-convert is missing

* Mon Jan 12 2009 Josef Bacik <josef@toxicpanda.com> 0.17-2
- fixed wrong sources upload

* Mon Jan 12 2009 Josef Bacik <josef@toxicpanda.com> 0.17
- Upstream release 0.17

* Sat Jan 10 2009 Kyle McMartin <kyle@redhat.com> 0.16.git1-1
- Upstream git sync from -g72359e8 (needed for kernel...)

* Sat Jan 10 2009 Marek Mahut <mmahut@fedoraproject.org> 0.16-1
- Upstream release 0.16

* Wed Jun 25 2008 Josef Bacik <josef@toxicpanda.com> 0.15-4
-use fedoras normal CFLAGS

* Mon Jun 23 2008 Josef Bacik <josef@toxicpanda.com> 0.15-3
-Actually defined _root_sbindir
-Fixed the make install line so it would install to the proper dir

* Mon Jun 23 2008 Josef Bacik <josef@toxicpanda.com> 0.15-2
-Removed a . at the end of the description
-Fixed the copyright to be GPLv2 since GPL doesn't work anymore

* Mon Jun 23 2008 Josef Bacik <josef@toxicpanda.com> 0.15-1
-Initial build
