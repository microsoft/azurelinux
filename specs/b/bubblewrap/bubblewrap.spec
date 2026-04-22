# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:    bubblewrap
Version: 0.11.0
Release: 3%{?dist}
Summary: Core execution tool for unprivileged containers

License: LGPL-2.0-or-later
URL:     https://github.com/containers/bubblewrap/
Source0: https://github.com/containers/bubblewrap/releases/download/v%{version}/bubblewrap-%{version}.tar.xz

BuildRequires: pkgconfig(bash-completion) >= 2.0
BuildRequires: gcc
BuildRequires: docbook-style-xsl
BuildRequires: meson
BuildRequires: pkgconfig(libcap)
BuildRequires: pkgconfig(libselinux)
BuildRequires: /usr/bin/xsltproc

%description
Bubblewrap (/usr/bin/bwrap) is a core execution engine for unprivileged
containers that works as a setuid binary on kernels without
user namespaces.

%prep
%autosetup

%build
%meson -Dman=enabled -Dselinux=enabled
%meson_build

%install
%meson_install

%files
%license COPYING
%doc README.md
%dir %{_datadir}/bash-completion
%dir %{_datadir}/bash-completion/completions
%{_datadir}/bash-completion/completions/bwrap
%dir %{_datadir}/zsh
%dir %{_datadir}/zsh/site-functions
%{_datadir}/zsh/site-functions/_bwrap
%if (0%{?rhel} != 0 && 0%{?rhel} <= 7)
%attr(0755,root,root) %caps(cap_sys_admin,cap_net_admin,cap_sys_chroot,cap_setuid,cap_setgid=ep) %{_bindir}/bwrap
%else
%{_bindir}/bwrap
%endif
%{_mandir}/man1/bwrap.1*

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Mar 05 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 0.11.0-1
- Update to 0.11.0 (#2322866)
- Fix the build with GCC 15 (#2339949)

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Aug 22 2024 Debarshi Ray <rishi@fedoraproject.org> - 0.10.0-1
- Update to 0.10.0 (#2271977)

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Apr 08 2024 Debarshi Ray <rishi@fedoraproject.org> - 0.9.0-1
- Update to 0.9.0 (#2271977)

* Tue Jan 23 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Nov 16 2023 Debarshi Ray <rishi@fedoraproject.org> - 0.8.0-1
- Update to 0.8.0 (#2173820)

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Feb 07 2023 David King <amigadave@amigadave.com> - 0.7.0-1
- Update to 0.7.0 (#2058474)

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Aug 25 2021 Kalev Lember <klember@redhat.com> - 0.5.0-1
- Update to 0.5.0
- Drop https://github.com/containers/bubblewrap/pull/426 patch as it breaks tests

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu May 27 2021 Colin Walters <walters@verbum.org> - 0.4.1-4
- Backport https://github.com/containers/bubblewrap/pull/426

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Mar 30 2020 David King <amigadave@amigadave.com> - 0.4.1-1
- Update to 0.4.1

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Nov 27 2019 Kalev Lember <klember@redhat.com> - 0.4.0-1
- Update to 0.4.0

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed May 01 2019 Colin Walters <walters@redhat.com> - 0.3.3-2
- New upstream release

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Oct 01 2018 Kalev Lember <klember@redhat.com> - 0.3.1-1
- Update to 0.3.1

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Colin Walters <walters@verbum.org> - 0.3.0-1
- https://github.com/projectatomic/bubblewrap/releases/tag/v0.3.0

* Wed May 16 2018 Kalev Lember <klember@redhat.com> - 0.2.1-1
- Update to 0.2.1

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Oct 09 2017 Colin Walters <walters@verbum.org> - 0.2.0-2
- New upstream version
- https://github.com/projectatomic/bubblewrap/releases/tag/v0.2.0

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Mar 28 2017 Colin Walters <walters@verbum.org> - 0.1.8-1
- New upstream version
  https://github.com/projectatomic/bubblewrap/releases/tag/v0.1.8

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 18 2017 Colin Walters <walters@verbum.org> - 0.1.7-1
- New upstream version;
  https://github.com/projectatomic/bubblewrap/releases/tag/v0.1.7
- Resolves: #1411814

* Tue Jan 10 2017 Colin Walters <walters@verbum.org> - 0.1.6-1
- New upstream version with security fix
- Resolves: #1411814

* Mon Dec 19 2016 Kalev Lember <klember@redhat.com> - 0.1.5-1
- Update to 0.1.5

* Tue Dec 06 2016 walters@redhat.com - 0.1.4-4
- Backport fix for regression in previous commit for rpm-ostree

* Thu Dec 01 2016 walters@redhat.com - 0.1.4-3
- Backport patch to fix running via nspawn, which should fix rpm-ostree-in-bodhi

* Tue Nov 29 2016 Kalev Lember <klember@redhat.com> - 0.1.4-1
- Update to 0.1.4

* Fri Oct 14 2016 Colin Walters <walters@verbum.org> - 0.1.3-2
- New upstream version

* Mon Sep 12 2016 Kalev Lember <klember@redhat.com> - 0.1.2-1
- Update to 0.1.2

* Tue Jul 12 2016 Igor Gnatenko <ignatenko@redhat.com> - 0.1.1-2
- Trivial fixes in packaging

* Fri Jul 08 2016 Colin Walters <walters@verbum.org> - 0.1.1
- Initial package
