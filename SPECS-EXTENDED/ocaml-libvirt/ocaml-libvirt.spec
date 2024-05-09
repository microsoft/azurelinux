Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           ocaml-libvirt
Version:        0.6.1.5
Release:        8%{?dist}
Summary:        OCaml binding for libvirt
License:        LGPLv2+

URL:            https://libvirt.org/ocaml/
Source0:        https://libvirt.org/sources/ocaml/%{name}-%{version}.tar.gz

# Fixes build with OCaml >= 4.09.
# Upstream commit 75b13978f85b32c7a121aa289d8ebf41ba14ee5a.
Patch1:         0001-Make-const-the-return-value-of-caml_named_value.patch

# Fixes for OCaml 4.10, sent upstream 2020-01-19.
Patch2:         0001-block_peek-memory_peek-Use-bytes-for-return-buffer.patch
Patch3:         0002-String_val-returns-const-char-in-OCaml-4.10.patch
Patch4:         0003-Don-t-try-to-memcpy-into-a-String_val.patch

BuildRequires:  ocaml >= 3.10.0
BuildRequires:  ocaml-ocamldoc
BuildRequires:  ocaml-findlib-devel

BuildRequires:  libvirt-devel >= 0.2.1
BuildRequires:  perl-interpreter
BuildRequires:  gawk


%description
OCaml binding for libvirt.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}


%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.


%prep
%setup -q
%autopatch -p1


%build
%configure
make all doc
%ifarch %{ocaml_native_compiler}
make opt
%endif


%install
# These rules work if the library uses 'ocamlfind install' to install itself.
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs
mkdir -p $RPM_BUILD_ROOT%{_bindir}
%ifarch %{ocaml_native_compiler}
make install-opt
%else
make install-byte
%endif


%files
%doc COPYING.LIB README ChangeLog
%{_libdir}/ocaml/libvirt
%ifarch %{ocaml_native_compiler}
%exclude %{_libdir}/ocaml/libvirt/*.a
%exclude %{_libdir}/ocaml/libvirt/*.cmxa
%exclude %{_libdir}/ocaml/libvirt/*.cmx
%endif
%exclude %{_libdir}/ocaml/libvirt/*.mli
%{_libdir}/ocaml/stublibs/*.so
%{_libdir}/ocaml/stublibs/*.so.owner


%files devel
%doc COPYING.LIB README TODO.libvirt ChangeLog html/*
%ifarch %{ocaml_native_compiler}
%{_libdir}/ocaml/libvirt/*.a
%{_libdir}/ocaml/libvirt/*.cmxa
%{_libdir}/ocaml/libvirt/*.cmx
%endif
%{_libdir}/ocaml/libvirt/*.mli


%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.6.1.5-8
- Switching to using full number for the 'Release' tag.
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Feb 27 2020 Richard W.M. Jones <rjones@redhat.com> - 0.6.1.5-7.1
- OCaml 4.10.0 final (Fedora 32).

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
- Rebuild for OCaml 3.12 (https://fedoraproject.org/wiki/Features/OCaml3.12).

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
- Upstream website is now https://libvirt.org/ocaml/

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
