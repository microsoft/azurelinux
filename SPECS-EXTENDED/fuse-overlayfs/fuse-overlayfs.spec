Vendor:         Microsoft Corporation
Distribution:   Mariner
%define git0 https://github.com/containers/%{name}
%define commit0 27bf038d0ece553e5d2c431eaebc7acaa2e3d254
%define shortcommit0 %(c=%{commit0}; echo ${c:0:7})

# Used for comparing with latest upstream tag
# to decide whether to autobuild (non-rawhide only)
%define built_tag v1.4.0
%define built_tag_strip %(b=%{built_tag}; echo ${b:1})
%define download_url https://github.com/containers/%{name}/archive/%{built_tag}.tar.gz

%{!?_modulesloaddir:%global _modulesloaddir %{_usr}/lib/modules-load.d}

Name: fuse-overlayfs
Version: 1.4.0
Release: 2%{?dist}
Summary: FUSE overlay+shiftfs implementation for rootless containers
License: GPLv3+
URL: %{git0}
Source0: %{download_url}#/%{name}-%{version}.tar.gz
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: fuse3-devel
BuildRequires: gcc
BuildRequires: git
BuildRequires: make
BuildRequires: systemd-rpm-macros
Requires: kmod
Provides: bundled(gnulib) = cb634d40c7b9bbf33fa5198d2e27fdab4c0bf143
Requires: fuse3

%description
%{summary}.

%package devel
Summary: %{summary}
BuildArch: noarch

%description devel
%{summary}

This package contains library source intended for
building other packages which use import path with
%{import_path} prefix.

%prep
%autosetup -Sgit -n %{name}-%{built_tag_strip}

%build
./autogen.sh
./configure --prefix=%{_usr} --libdir=%{_libdir}
%{__make}

%install
make DESTDIR=%{buildroot} install
install -d %{buildroot}%{_modulesloaddir}
echo fuse > %{buildroot}%{_modulesloaddir}/fuse-overlayfs.conf

%post
modprobe fuse > /dev/null 2>&1 || :

%check

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%files
%license COPYING
%doc README.md
%{_bindir}/%{name}
%{_mandir}/man1/*
%{_modulesloaddir}/fuse-overlayfs.conf

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.4.0-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Jan 22 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.4.0-1
- autobuilt v1.4.0

* Wed Nov 25 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.3.0-1
- autobuilt v1.3.0

* Fri Oct  9 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.2.0-1
- autobuilt v1.2.0

* Tue Jul 07 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.1.2-1
- autobuilt v1.1.2

* Sat Jun 20 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.1.1-1
- autobuilt v1.1.1

* Thu Jun 18 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.1.0-1
- autobuilt v1.1.0

* Mon Apr 20 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.0.0-1
- autobuilt v1.0.0

* Tue Mar 17 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 0.7.8-1
- autobuilt v0.7.8

* Tue Mar 17 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 0.7.7-1
- autobuilt v0.7.7

* Tue Feb 04 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 0.7.6-2.0.dev.gitce61c7e
- bump to 0.7.6
- autobuilt ce61c7e

* Sat Feb 01 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 0.7.5-4.0.dev.git9266fca
- autobuilt 9266fca

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.5-3.0.dev.git9076145
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 17 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 0.7.5-2.0.dev.git9076145
- bump to 0.7.5
- autobuilt 9076145

* Fri Jan 17 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 0.7.4-2.0.dev.git32d867b
- bump to 0.7.4
- autobuilt 32d867b

* Thu Jan 16 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 0.7.3-4.0.dev.git6044520
- autobuilt 6044520

* Tue Jan 14 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 0.7.3-3.0.dev.gitdd7cf03
- autobuilt dd7cf03

* Thu Jan 09 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 0.7.3-2.0.dev.gite01ba30
- bump to 0.7.3
- autobuilt e01ba30

* Wed Jan 08 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 0.7.2-8.0.dev.gita0ba681
- autobuilt a0ba681

* Wed Jan 08 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 0.7.2-7.0.dev.git9f27377
- autobuilt 9f27377

* Wed Jan 08 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 0.7.2-6.0.dev.gita6f9e32
- autobuilt a6f9e32

* Wed Dec 11 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 0.7.2-5.0.dev.git53c17da
- autobuilt 53c17da

* Mon Dec 09 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 0.7.2-4.0.dev.gitb5dfac4
- autobuilt b5dfac4

* Tue Dec 03 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 0.7.2-3.0.dev.gitf6cbfc6
- autobuilt f6cbfc6

* Fri Nov 29 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 0.7.2-2.0.dev.git8c59873
- bump to 0.7.2
- autobuilt 8c59873

* Fri Nov 29 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 0.7.1-3.0.dev.gitfe47dba
- autobuilt fe47dba

* Thu Nov 28 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 0.7.1-2.0.dev.gite0d2ffa
- bump to 0.7.1
- autobuilt e0d2ffa

* Thu Nov 28 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 0.7-7.0.dev.gitfc688fb
- autobuilt fc688fb

* Wed Nov 27 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 0.7-6.0.dev.git675b7b9
- autobuilt 675b7b9

* Tue Nov 26 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 0.7-5.0.dev.gitb57e5c8
- autobuilt b57e5c8

* Mon Nov 18 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 0.7-4.0.dev.git58101db
- autobuilt 58101db

* Sat Nov 16 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 0.7-3.0.dev.git34794cf
- autobuilt 34794cf

* Tue Nov 05 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 0.7-2.0.dev.gitb3b6765
- bump to 0.7
- autobuilt b3b6765

* Mon Nov 04 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 0.6.5-5.0.dev.git5f028d2
- autobuilt 5f028d2

* Thu Oct 31 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 0.6.5-4.0.dev.gitfa0cd99
- autobuilt fa0cd99

* Sun Oct 20 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 0.6.5-3.0.dev.gitae96c48
- autobuilt ae96c48

* Wed Oct 16 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 0.6.5-2.0.dev.git3bc0aa6
- bump to 0.6.5
- autobuilt 3bc0aa6

* Fri Oct 04 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 0.6.4-2.0.dev.git098d9ad
- bump to 0.6.4
- autobuilt 098d9ad

* Thu Oct 03 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 0.6.3-4.0.dev.git5048628
- autobuilt 5048628

* Thu Oct 03 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 0.6.3-3.0.dev.git1955ff6
- autobuilt 1955ff6

* Thu Sep 26 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 0.6.3-2.0.dev.git46c0f8e
- bump to 0.6.3
- autobuilt 46c0f8e

* Wed Sep 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.2-7.0.dev.gitb0a9bda
- autobuilt b0a9bda

* Fri Sep 13 2019 Jindrich Novy <jnovy@redhat.com> - 0.6.2-6.0.dev.git66e01c8
- require fuse3 so that fuse-overlayfs will pull in /usr/bin/fusermount3

* Fri Sep 13 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.2-5.0.dev.git66e01c8
- autobuilt 66e01c8

* Wed Sep 11 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.2-4.0.dev.git74fb3dd
- autobuilt 74fb3dd

* Mon Sep 09 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.2-3.0.dev.git16f39b1
- autobuilt 16f39b1

* Wed Sep 04 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.2-2.0.dev.git67a4afe
- bump to 0.6.2
- autobuilt 67a4afe

* Fri Aug 30 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.1-3.0.dev.gitcb4b35e
- autobuilt cb4b35e

* Mon Aug 26 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.1-2.0.dev.gitc548530
- bump to 0.6.1
- autobuilt c548530

* Sun Aug 25 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6-2.0.dev.git43b641d
- bump to 0.6
- autobuilt 43b641d

* Wed Aug 21 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.5.2-1.1.dev.gitf8ba9ad
- change release tag to preserve upgrade path

* Wed Aug 21 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.5.2-0.2.dev.gitf8ba9ad
- autobuilt f8ba9ad

* Mon Aug 19 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.5.2-0.1.dev.git4dc60f0
- bump to 0.5.2
- autobuilt 4dc60f0

* Fri Aug 16 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.5.1-0.3.dev.git89b814d
- autobuilt 89b814d

* Mon Aug 12 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.5.1-0.2.dev.gitc756bbe
- autobuilt c756bbe

* Thu Aug 08 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.5.1-0.1.dev.git58e3f7c
- bump to 0.5.1
- autobuilt 58e3f7c

* Tue Aug 06 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.5-3.1.dev.git80eb59d
- autobuilt 80eb59d

* Thu Aug 01 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.5-2.1.dev.gitb92a654
- autobuilt b92a654

* Tue Jul 30 2019 Giuseppe Scrivano <gscrivan@redhat.com> - 0.5
- built commit v0.5

* Mon Jul 15 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.4.1-4
- update release tag

* Mon Jul 15 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.4.1-3.git7bc2dd9
- update release tag

* Mon Jul 15 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.1-2.dev.git7bc2dd9
- bump to 0.4.1
- autobuilt tag v0.

* Fri Jun 21 2019 Giuseppe Scrivano <gscrivan@redhat.com> - 0.4.2-0.dev.git7bc2dd9
- built commit 7bc2dd9

* Thu Jun 13 2019 Giuseppe Scrivano <gscrivan@redhat.com> - 0.4.1-0.dev.git1ff7c64
- built commit 1ff7c64

* Thu Jun 06 2019 Giuseppe Scrivano <gscrivan@redhat.com> - 0.4-1.dev.git8d92da6
- built commit 8d92da6

* Fri May 17 2019 Giuseppe Scrivano <gscrivan@redhat.com> - 0.3-10.dev.gita7c829
- built commit a7c829

* Mon May 06 2019 Giuseppe Scrivano <gscrivan@redhat.com> - 0.3-9.dev.git89bd69b
- built commit 89bd69b

* Thu Mar 28 2019 Giuseppe Scrivano <gscrivan@redhat.com> - 0.3-8.dev.gita6958ce
- built commit a6958ce

* Mon Mar 25 2019 Giuseppe Scrivano <gscrivan@redhat.com> - 0.3-7.dev.git8ec68ae
- Add loading of fuse file system

* Thu Mar 21 2019 Dan Walsh <dwalsh@redhat.com> - 0.3-6.dev.git8ec68ae
- Add loading of fuse file system

* Sun Mar 10 2019 Giuseppe Scrivano <gscrivan@redhat.com> - 0.3-5.dev.git8ec68ae
- built commit 8ec68ae

* Tue Feb 26 2019 Giuseppe Scrivano <gscrivan@redhat.com> - 0.3-4.dev.gitea72572
- built commit ea72572

* Wed Feb 13 2019 Giuseppe Scrivano <gscrivan@redhat.com> - 0.3-3.dev.gitff65ede
- built commit ff65ede

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3-2.dev.git6d269aa
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 15 2019 Giuseppe Scrivano <gscrivan@redhat.com> - 0.3-1.dev.git6d269aa
- built commit 6d269aa

* Tue Jan 08 2019 Giuseppe Scrivano <gscrivan@redhat.com> - 0.1-9.dev.git5c9742d
- built commit 5c9742d

* Thu Dec 20 2018 Giuseppe Scrivano <gscrivan@redhat.com> - 0.1-8.dev.git91bb401
- built commit 91bb401

* Tue Dec 18 2018 Giuseppe Scrivano <gscrivan@redhat.com> - 0.1-7.dev.gitf48e1ef
- built commit f48e1ef

* Fri Nov 23 2018 Giuseppe Scrivano <gscrivan@redhat.com> - 0.1-6.dev.git3d48bf9
- built commit 3d48bf9

* Fri Aug 10 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1-5.dev.gitd40ac75
- built commit d40ac75

* Mon Jul 30 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1-4.dev.git79c70fd
- Resolves: #1609598 - initial upload to Fedora
- bundled gnulib

* Mon Jul 30 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1-3.dev.git79c70fd
- correct license field

* Mon Jul 30 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1-2.dev.git79c70fd
- fix license

* Sun Jul 29 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1-1.dev.git13575b6
- First package for Fedora
