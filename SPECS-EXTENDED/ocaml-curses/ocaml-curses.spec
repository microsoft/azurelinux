Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)

Name:           ocaml-curses
Version:        1.0.4
Release:        13%{?dist}
Summary:        OCaml bindings for ncurses
License:        LGPLv2+

URL:            https://savannah.nongnu.org/projects/ocaml-tmk/
Source0:        https://download.savannah.gnu.org/releases/ocaml-tmk/%{name}-%{version}.tar.gz

BuildRequires:  ocaml >= 4.00.1
BuildRequires:  ocaml-findlib-devel >= 1.3.3-3
BuildRequires:  ncurses-devel
BuildRequires:  gawk

# Doesn't include a configure script, so we have to make one.
BuildRequires:  autoconf, automake, libtool


%description
OCaml bindings for ncurses.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

# On aarch64, it is reported that ncurses-devel is not pulled in
# implicitly by ocaml (as is the case on x86-64 for some reason).  In
# any case, it is likely that people installing ocaml-curses-devel
# will desire ncurses-devel, hence:
Requires:       ncurses-devel


%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.


%prep
%setup -q

autoreconf


%build
%configure --enable-widec
make all
%if %opt
make opt
%endif


%install
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs
%if %opt
ocamlfind install curses META *.cmi *.cmx *.cma *.cmxa *.a *.so *.mli
%else
ocamlfind install curses META *.cmi *.cma *.a *.so *.mli
%endif


%files
%doc COPYING
%{_libdir}/ocaml/curses
%if %opt
%exclude %{_libdir}/ocaml/curses/*.a
%exclude %{_libdir}/ocaml/curses/*.cmxa
%exclude %{_libdir}/ocaml/curses/*.cmx
%endif
%exclude %{_libdir}/ocaml/curses/*.mli
%{_libdir}/ocaml/stublibs/*.so
%{_libdir}/ocaml/stublibs/*.so.owner


%files devel
%doc COPYING
%if %opt
%{_libdir}/ocaml/curses/*.a
%{_libdir}/ocaml/curses/*.cmxa
%{_libdir}/ocaml/curses/*.cmx
%endif
%{_libdir}/ocaml/curses/*.mli


%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.4-13
- Switching to using full number for the 'Release' tag.
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Feb 27 2020 Richard W.M. Jones <rjones@redhat.com> - 1.0.4-12.1
- OCaml 4.10.0 final (Fedora 32).

* Wed Feb 26 2020 Richard W.M. Jones <rjones@redhat.com> - 1.0.4-12
- OCaml 4.10.0 final.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jan 19 2020 Richard W.M. Jones <rjones@redhat.com> - 1.0.4-10
- OCaml 4.10.0+beta1 rebuild.

* Thu Jan 09 2020 Richard W.M. Jones <rjones@redhat.com> - 1.0.4-9
- OCaml 4.09.0 for riscv64

* Fri Dec 06 2019 Richard W.M. Jones <rjones@redhat.com> - 1.0.4-8
- OCaml 4.09.0 (final) rebuild.

* Fri Aug 16 2019 Richard W.M. Jones <rjones@redhat.com> - 1.0.4-7
- OCaml 4.08.1 (final) rebuild.

* Wed Jul 31 2019 Richard W.M. Jones <rjones@redhat.com> - 1.0.4-6
- OCaml 4.08.1 (rc2) rebuild.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jun 27 2019 Richard W.M. Jones <rjones@redhat.com> - 1.0.4-4
- OCaml 4.08.0 (final) rebuild.

* Mon Apr 29 2019 Richard W.M. Jones <rjones@redhat.com> - 1.0.4-3
- OCaml 4.08.0 (beta 3) rebuild.

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Nov 20 2018 Richard W.M. Jones <rjones@redhat.com> - 1.0.4-1
- New upstream version 1.0.4.
- Remove patch which is now fixed upstream.

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-45
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-44
- OCaml 4.07.0 (final) rebuild.

* Wed Jun 20 2018 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-43
- OCaml 4.07.0-rc1 rebuild.

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-42
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Nov 17 2017 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-41
- OCaml 4.06.0 rebuild.

* Tue Aug 08 2017 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-40
- OCaml 4.05.0 rebuild.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 27 2017 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-37
- OCaml 4.04.2 rebuild.
- Fix detection of <term.h> header for ncurses 6.0-10.20170520.

* Fri May 12 2017 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-35
- OCaml 4.04.1 rebuild.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Nov 05 2016 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-33
- Rebuild for OCaml 4.04.0.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jul 28 2015 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-31
- OCaml 4.02.3 rebuild.

* Tue Jul 21 2015 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-30
- Enable bytecode compilation.

* Wed Jun 24 2015 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-29
- ocaml-4.02.2 final rebuild.

* Wed Jun 17 2015 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-28
- ocaml-4.02.2 rebuild.

* Tue Feb 17 2015 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-27
- ocaml-4.02.1 rebuild.

* Sat Aug 30 2014 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-26
- ocaml-4.02.0 final rebuild.

* Sat Aug 23 2014 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-25
- ocaml-4.02.0+rc1 rebuild.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Aug 02 2014 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-23
- ocaml-4.02.0-0.8.git10e45753.fc22 rebuild.

* Mon Jul 21 2014 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-22
- Bump release and rebuild.

* Mon Jul 21 2014 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-21
- OCaml 4.02.0 beta rebuild.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May  9 2014 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-19
- Add explicit requires ncurses to ocaml-curses-devel subpackage.

* Sat Sep 14 2013 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-18
- Rebuild for OCaml 4.01.0.
- Enable debuginfo.
- Modernize the spec file.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 27 2012 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-15
- BR >= OCaml 4.00.1 so we can't be built against the wrong OCaml.

* Mon Oct 29 2012 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-14
- Rebuild for OCaml 4.00.1.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 10 2012 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-12
- Rebuild for OCaml 4.00.0.

* Fri Jan 06 2012 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-11
- Rebuild for OCaml 3.12.1.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 06 2011 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-9
- Rebuild for OCaml 3.12 (https://fedoraproject.org/wiki/Features/OCaml3.12).

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-8
- Rebuild for OCaml 3.11.2.

* Mon Oct  5 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-7
- Use ncursesw for wide character support.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-5
- Rebuild for OCaml 3.11.1

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-3
- Rebuild for OCaml 3.11.0+rc1.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-2
- Rebuild for OCaml 3.11.0

* Mon Nov 17 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-1
- Major version leap to the latest, supported, released version.

* Wed Apr 23 2008 Richard W.M. Jones <rjones@redhat.com> - 0.1-8
- Rebuild for OCaml 3.10.2

* Sat Mar  1 2008 Richard W.M. Jones <rjones@redhat.com> - 0.1-7.20020319
- Rebuild for ppc64.

* Tue Feb 12 2008 Richard W.M. Jones <rjones@redhat.com> - 0.1-6.20020319
- Rebuild for OCaml 3.10.1

* Thu Sep  6 2007 Richard W.M. Jones <rjones@redhat.com> - 0.1-5.20020319
- Force rebuild because of updated requires/provides scripts in OCaml.

* Thu Aug 30 2007 Richard W.M. Jones <rjones@redhat.com> - 0.1-4.20020319
- Force rebuild because of changed BRs in base OCaml.

* Mon Aug 27 2007 Richard W.M. Jones <rjones@redhat.com> - 0.1-3.20020319
- License is LGPL 2.1 or any later version.

* Mon Aug  6 2007 Richard W.M. Jones <rjones@redhat.com> - 0.1-2.20020319
- The archive is called 'mlcurses.*'.

* Mon Aug  6 2007 Richard W.M. Jones <rjones@redhat.com> - 0.1-1.20020319
- Initial RPM release.
