Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           ocaml-libvirt
Version:        0.6.1.7
Release:        13%{?dist}
Summary:        OCaml binding for libvirt
License:        LGPL-2.1-or-later

URL:            https://ocaml.libvirt.org/
Source0:        https://libvirt.org/sources/ocaml/%{name}-%{version}.tar.gz

BuildRequires:  make
BuildRequires:  ocaml >= 3.10.0
BuildRequires:  ocaml-ocamldoc
BuildRequires:  ocaml-findlib-devel
BuildRequires:  ocaml-rpm-macros

BuildRequires:  libvirt-devel >= 0.2.1
BuildRequires:  perl-interpreter

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool


%description
OCaml binding for libvirt.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}


%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.


%prep
%setup -q
%autopatch -p1

# Fix detection of ocamlopt and ocamldoc
# https://gitlab.com/libvirt/libvirt-ocaml/-/merge_requests/27
sed -i '/AM_CONDITIONAL/s/"x"/"xno"/' configure.ac

# Regenerate the configure script
autoreconf -fi -I m4 .


%build
# Parallel builds do not work.
unset MAKEFLAGS
%configure
make


%install
# These rules work if the library uses 'ocamlfind install' to install itself.
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs
mkdir -p $RPM_BUILD_ROOT%{_bindir}
make install
%ocaml_files


%files -f .ofiles
%doc README
%license COPYING.LIB


%files devel -f .ofiles-devel
%doc README TODO.libvirt
%license COPYING.LIB


%changelog
* Fri Dec 20 2024 Durga Jagadeesh Palli <v-dpalli@microsoft.com> - 0.6.1.7-13
- Initial Azure Linux import from Fedora 41 (license: MIT)
- License verified

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1.7-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 19 2024 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.7-11
- OCaml 5.2.0 ppc64le fix

* Wed May 29 2024 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.7-10
- OCaml 5.2.0 for Fedora 41

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1.7-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 18 2023 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.7-7
- OCaml 5.1.1 + s390x code gen fix for Fedora 40

* Tue Dec 12 2023 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.7-6
- OCaml 5.1.1 rebuild for Fedora 40

* Thu Oct 05 2023 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.7-5
- OCaml 5.1 rebuild for Fedora 40

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.7-3
- OCaml 5.0 rebuild for Fedora 39

* Mon Jul 10 2023 Jerry James <loganjerry@gmail.com> - 0.6.1.7-2
- OCaml 5.0.0 rebuild
- New project URL
- Convert License tag to SPDX
- Fix build on bytecode-only architectures
- Use %%license macro
- Use new OCaml macros

* Mon Feb 13 2023 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.7-1
- New upstream version 0.6.1.7
- Do not try parallel builds.
- Upstream now uses automake.

- Remove ChangeLog file and HTML docs, dropped upstream.

* Tue Jan 24 2023 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.6-5
- Rebuild OCaml packages for F38

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jun 18 2022 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.6-2
- OCaml 4.14.0 rebuild

* Thu Apr 28 2022 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.6-1
- New upstream version 0.6.1.6
- Remove patches which are all upstream.

* Fri Feb 04 2022 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.5-20
- OCaml 4.13.1 rebuild to remove package notes

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1.5-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild


* Mon Oct 04 2021 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.5-18
- OCaml 4.13.1 build

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1.5-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Mar  1 14:31:55 GMT 2021 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.5-16
- OCaml 4.12.0 build

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1.5-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Sep 01 2020 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.5-14
- OCaml 4.11.1 rebuild

* Fri Aug 21 2020 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.5-13
- OCaml 4.11.0 rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1.5-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon May 04 2020 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.5-11
- OCaml 4.11.0+dev2-2020-04-22 rebuild

* Tue Apr 21 2020 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.5-10
- OCaml 4.11.0 pre-release attempt 2

* Fri Apr 17 2020 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.5-9
- OCaml 4.11.0 pre-release

* Thu Apr 02 2020 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.5-8
- Update all OCaml dependencies for RPM 4.16.

* Wed Feb 26 2020 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.5-7
- OCaml 4.10.0 final.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jan 19 2020 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.5-5
- OCaml 4.10.0+beta1 rebuild.

* Thu Jan 09 2020 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.5-4
- OCaml 4.09.0 for riscv64

* Fri Dec 06 2019 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.5-3
- Include upstream patch to fix build for OCaml 4.09.

* Fri Dec 06 2019 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.5-2
- OCaml 4.09.0 (final) rebuild.

* Wed Aug 21 2019 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.5-1
- New upstream version 0.6.1.5.
- Remove all patches as they are upstream.

* Fri Aug 16 2019 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.4-35
- OCaml 4.08.1 (final) rebuild.

* Wed Jul 31 2019 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.4-34
- OCaml 4.08.1 (rc2) rebuild.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1.4-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jun 27 2019 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.4-32
- OCaml 4.08.0 (final) rebuild.

* Mon Apr 29 2019 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.4-31
- OCaml 4.08.0 (beta 3) rebuild.

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1.4-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1.4-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.4-28
- OCaml 4.07.0 (final) rebuild.

* Tue Jun 19 2018 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.4-27
- OCaml 4.07.0-rc1 rebuild.

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1.4-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Nov 08 2017 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.4-25
- Fix -safe-string.

* Tue Nov 07 2017 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.4-22
- OCaml 4.06.0 rebuild.

* Mon Aug 07 2017 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.4-21
- OCaml 4.05.0 rebuild.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1.4-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1.4-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 26 2017 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.4-18
- OCaml 4.04.2 rebuild.

* Fri May 12 2017 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.4-17
- Bump release and rebuild.

* Thu May 11 2017 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.4-16
- OCaml 4.04.1 rebuild.

* Tue Mar 28 2017 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.4-15
- Further upstream patches, adding binding for virConnectGetAllDomainStats.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1.4-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Nov 04 2016 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.4-13
- Rebuild for OCaml 4.04.0.

* Fri Feb 05 2016 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.4-12
- Add upstream patch to remove unused function.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jul 28 2015 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.4-10
- OCaml 4.02.3 rebuild.

* Mon Jul 27 2015 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.4-9
- Remove ExcludeArch since bytecode build should now work.

* Wed Jun 24 2015 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.4-8
- Bump release and rebuild.
- Fix bogus date in changelog.

* Wed Jun 17 2015 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.4-7
- ocaml-4.02.2 rebuild.

* Tue Mar 17 2015 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.4-6
- Add upstream patches to fix error handling.

* Fri Mar  6 2015 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.4-5
- Add binding for virDomainCreateXML.

* Mon Feb 16 2015 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.4-4
- ocaml-4.02.1 rebuild.

* Sat Aug 30 2014 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.4-3
- ocaml-4.02.0 final rebuild.
- Fix int types.

* Mon Aug 25 2014 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.4-1
- New upstream version 0.6.1.4.
- Patch removed, now upstream.

* Sat Aug 23 2014 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.2-14
- ocaml-4.02.0+rc1 rebuild.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Aug 02 2014 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.2-12
- ocaml-4.02.0-0.8.git10e45753.fc22 rebuild.

* Mon Jul 21 2014 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.2-11
- OCaml 4.02.0 beta rebuild.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Sep 18 2013 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.2-9
- OCaml 4.01.0 rebuild.
- Enable debuginfo.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 29 2012 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.2-6
- Rebuild for OCaml 4.00.1.

* Fri Oct 12 2012 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.2-5
- Modernise the spec file.
- Add upstream patch to remove unnecessary get_cpu_stats second parameter
  (thanks Hu Tao).

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 09 2012 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.2-2
- Rebuild for OCaml 4.00.0.

* Fri Mar 23 2012 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.2-1
- New upstream version 0.6.1.2.

* Tue Mar  6 2012 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.1-1
- New upstream version 0.6.1.1.
- Remove mlvirsh subpackage, no longer upstream.
- Replace custom configure with RPM macro configure.
- Use RPM global instead of define.
- Use built-in RPM OCaml dependency generator.

* Fri Jan 06 2012 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.0-10
- Rebuild for OCaml 3.12.1.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 05 2011 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.0-8
- Rebuild for OCaml 3.12 (http://fedoraproject.org/wiki/Features/OCaml3.12).

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.0-7
- Rebuild for OCaml 3.11.2.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.0-5
- Force rebuild to test FTBFS issue.

* Fri Jun 12 2009 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.0-3
- Force rebuild to test FTBFS issue.

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.0-2
- Rebuild for OCaml 3.11.1

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Tue Mar 10 2009 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.0-1
- New upstream release 0.6.1.0.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 0.4.4.2-3
- Rebuild for OCaml 3.11.0+rc1.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 0.4.4.2-2
- Rebuild for OCaml 3.11.0

* Wed Jul  9 2008 Richard W.M. Jones <rjones@redhat.com> - 0.4.4.2-1
- New upstream version.
- In upstream, 'make install' became 'make install-byte' or 'make install-opt'

* Tue Jun 10 2008 Richard W.M. Jones <rjones@redhat.com> - 0.4.2.4-1
- New upstream version.

* Thu Jun  5 2008 Richard W.M. Jones <rjones@redhat.com> - 0.4.2.3-1
- New upstream version.

* Thu Jun  5 2008 Richard W.M. Jones <rjones@redhat.com> - 0.4.2.2-1
- New upstream version.
- Removed virt-ctrl, virt-df, virt-top subpackages, since these are
  now separate Fedora packages.

* Tue May 20 2008 Richard W.M. Jones <rjones@redhat.com> - 0.4.1.1-4
- Disable virt-top (bz 442871).
- Disable virt-ctrl (bz 442875).

* Mon May 19 2008 Richard W.M. Jones <rjones@redhat.com> - 0.4.1.1-3
- Disable virt-df (bz 442873).

* Wed Apr 23 2008 Richard W.M. Jones <rjones@redhat.com> - 0.4.1.1-2
- Rebuild for OCaml 3.10.2

* Thu Mar 20 2008 Richard W.M. Jones <rjones@redhat.com> - 0.4.1.1-1
- New upstream release 0.4.1.1.
- Move configure to build section.
- Pass RPM_OPT_FLAGS.

* Tue Mar  4 2008 Richard W.M. Jones <rjones@redhat.com> - 0.4.1.0-2
- Fix source URL.
- Install virt-df manpage.

* Tue Mar  4 2008 Richard W.M. Jones <rjones@redhat.com> - 0.4.1.0-1
- New upstream release 0.4.1.0.
- Upstream now requires ocaml-dbus >= 0.06, ocaml-lablgtk >= 2.10.0,
  ocaml-dbus-devel.
- Enable virt-df.

* Sat Mar  1 2008 Richard W.M. Jones <rjones@redhat.com> - 0.4.0.3-3
- Rebuild for ppc64.

* Wed Feb 13 2008 Richard W.M. Jones <rjones@redhat.com> - 0.4.0.3-2
- Add BR gtk2-devel

* Tue Feb 12 2008 Richard W.M. Jones <rjones@redhat.com> - 0.4.0.3-1
- New upstream version 0.4.0.3.
- Rebuild for OCaml 3.10.1.

* Tue Nov 20 2007 Richard W.M. Jones <rjones@redhat.com> - 0.3.3.4-1
- New upstream release 0.3.3.4.
- Upstream website is now http://libvirt.org/ocaml/

* Fri Oct 19 2007 Richard W.M. Jones <rjones@redhat.com> - 0.3.3.0-2
- Mistake: BR is ocaml-calendar-devel.

* Fri Oct 19 2007 Richard W.M. Jones <rjones@redhat.com> - 0.3.3.0-1
- New upstream release 0.3.3.0.
- Added support for virt-df, but disabled it by default.
- +BR ocaml-calendar.

* Mon Sep 24 2007 Richard W.M. Jones <rjones@redhat.com> - 0.3.2.8-1
- New upstream release 0.3.2.8.

* Thu Sep 20 2007 Richard W.M. Jones <rjones@redhat.com> - 0.3.2.7-1
- New upstream release 0.3.2.7.
- Ship the upstream ChangeLog file.

* Thu Sep  6 2007 Richard W.M. Jones <rjones@redhat.com> - 0.3.2.6-2
- Force dependency on ocaml >= 3.10.0-7 which has fixed requires/provides
  scripts.

* Thu Sep  6 2007 Richard W.M. Jones <rjones@redhat.com> - 0.3.2.6-1
- New upstream version 0.3.2.6.

* Wed Aug 29 2007 Richard W.M. Jones <rjones@redhat.com> - 0.3.2.5-1
- New upstream version 0.3.2.5.
- Keep TODO out of the main package, but add (renamed) TODO.libvirt and
  TODO.virt-top to the devel and virt-top packages respectively.
- Add BR gawk.

* Thu Aug 23 2007 Richard W.M. Jones <rjones@redhat.com> - 0.3.2.4-1
- New upstream version 0.3.2.4.

* Thu Aug 23 2007 Richard W.M. Jones <rjones@redhat.com> - 0.3.2.3-2
- build_* macros so we can choose what subpackages to build.

* Thu Aug 23 2007 Richard W.M. Jones <rjones@redhat.com> - 0.3.2.3-1
- Upstream version 0.3.2.3.
- Add missing BR libvirt-devel.

* Wed Aug 22 2007 Richard W.M. Jones <rjones@redhat.com> - 0.3.2.2-1
- Upstream version 0.3.2.2.

* Wed Aug 22 2007 Richard W.M. Jones <rjones@redhat.com> - 0.3.2.1-2
- Fix unclosed if-statement in spec file.

* Wed Aug 22 2007 Richard W.M. Jones <rjones@redhat.com> - 0.3.2.1-1
- Upstream version 0.3.2.1.
- Put HTML documentation in -devel package.

* Mon Aug  6 2007 Richard W.M. Jones <rjones@redhat.com> - 0.3.1.2-1
- Initial RPM release.
