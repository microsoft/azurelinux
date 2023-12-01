%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)
%global __ocaml_requires_opts -i Asttypes -i Parsetree
%global __ocaml_provides_opts -i Pr_gettext

Summary:        OCaml library for i18n
Name:           ocaml-gettext
Version:        0.4.2
Release:        2%{?dist}
License:        LGPLv2+ WITH exceptions
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/gildor478/ocaml-gettext
Source0:        https://github.com/gildor478/ocaml-gettext/releases/download/v%{version}/gettext-v%{version}.tbz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  chrpath
BuildRequires:  docbook-style-xsl
BuildRequires:  libxml2
BuildRequires:  libxslt
BuildRequires:  ocaml >= 4.00.1
BuildRequires:  ocaml-camomile-data
BuildRequires:  ocaml-camomile-devel >= 0.8.6-3
BuildRequires:  ocaml-compiler-libs
BuildRequires:  ocaml-cppo
BuildRequires:  ocaml-dune-devel
BuildRequires:  ocaml-fileutils-devel >= 0.4.4-4
BuildRequires:  ocaml-findlib-devel >= 1.3.3-3
BuildRequires:  ocaml-ocamldoc
BuildRequires:  ocaml-ounit-devel

# ocaml-gettext program needs camomile data files
Requires:       ocaml-camomile-data

%description
Ocaml-gettext provides support for internationalization of Ocaml
programs.

Constraints :

* provides a pure Ocaml implementation,
* the API should be as close as possible to GNU gettext,
* provides a way to automatically extract translatable
  strings from Ocaml source code.

%package        devel
Summary:        Development files for %{name}

Requires:       %{name} = %{version}-%{release}
# BZ 446919.
Requires:       ocaml-fileutils-devel >= 0.4.0

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%package        camomile
Summary:        Parts of %{name} which depend on Camomile

Requires:       %{name} = %{version}-%{release}

%description    camomile
The %{name}-camomile package contains the parts of %{name} which
depend on Camomile.

%package        camomile-devel
Summary:        Development files for %{name}-camomile

Requires:       %{name}-camomile = %{version}-%{release}
Requires:       %{name}-devel = %{version}-%{release}

%description    camomile-devel
The %{name}-camomile-devel package contains libraries and
signature files for developing applications that use
%{name}-camomile.

%prep
%autosetup -n gettext-v%{version}

# Remove dependency on batteries.
sed -i -e 's/batteries//' test/dune
sed -i -e 's/batteries//' test/test-stub/dune

%build
make build

#check
# Tests require batteries, so they are disabled at present.
# Under discussion with upstream.

%install
mkdir -p %{buildroot}%{_libdir}/ocaml
mkdir -p %{buildroot}%{_bindir}
dune install --destdir=%{buildroot}

# Remove this, we will use our own rules for documentation.
rm -rf %{buildroot}%{_prefix}/doc

%files
%license LICENSE.txt
%{_libdir}/ocaml/gettext
%{_libdir}/ocaml/gettext-stub
%if %{opt}
%exclude %{_libdir}/ocaml/gettext/*.cmxa
%exclude %{_libdir}/ocaml/gettext/*/*.a
%exclude %{_libdir}/ocaml/gettext/*/*.cmxa
%exclude %{_libdir}/ocaml/gettext/*/*.cmx
%exclude %{_libdir}/ocaml/gettext-stub/*.a
%exclude %{_libdir}/ocaml/gettext-stub/*.cmxa
%exclude %{_libdir}/ocaml/gettext-stub/*.cmx
%endif
%exclude %{_libdir}/ocaml/gettext/*/*.ml
%exclude %{_libdir}/ocaml/gettext/*/*.mli
%exclude %{_libdir}/ocaml/gettext-stub/*.ml
%{_libdir}/ocaml/stublibs/*.so

%files devel
%doc README.md CHANGES.md THANKS TODO.md
%if %{opt}
%{_libdir}/ocaml/gettext/*.cmxa
%{_libdir}/ocaml/gettext/*/*.a
%{_libdir}/ocaml/gettext/*/*.cmxa
%{_libdir}/ocaml/gettext/*/*.cmx
%{_libdir}/ocaml/gettext-stub/*.a
%{_libdir}/ocaml/gettext-stub/*.cmxa
%{_libdir}/ocaml/gettext-stub/*.cmx
%endif
%{_libdir}/ocaml/gettext/*/*.ml
%{_libdir}/ocaml/gettext/*/*.mli
%{_libdir}/ocaml/gettext-stub/*.ml
%{_bindir}/ocaml-gettext
%{_bindir}/ocaml-xgettext
%{_mandir}/man1/ocaml-gettext.1*
%{_mandir}/man1/ocaml-xgettext.1*
%{_mandir}/man5/ocaml-gettext.5*

%files camomile
%license LICENSE.txt
%{_libdir}/ocaml/gettext-camomile
%if %{opt}
%exclude %{_libdir}/ocaml/gettext-camomile/*.a
%exclude %{_libdir}/ocaml/gettext-camomile/*.cmxa
%exclude %{_libdir}/ocaml/gettext-camomile/*.cmx
%endif
%exclude %{_libdir}/ocaml/gettext-camomile/*.mli

%files camomile-devel
%doc README.md
%if %{opt}
%{_libdir}/ocaml/gettext-camomile/*.a
%{_libdir}/ocaml/gettext-camomile/*.cmxa
%{_libdir}/ocaml/gettext-camomile/*.cmx
%endif
%{_libdir}/ocaml/gettext-camomile/*.mli

%changelog
* Thu Mar 31 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.4.2-2
- Cleaning-up spec. License verified.

* Tue Jan 18 2022 Olivia Crain <oliviacrain@microsoft.com> - 0.4.2-1
- Upgrade to latest upstream version
- Remove RHEL distro check macros
- Lint spec
- License verified

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.3.8-1
- Switching to using full number for the 'Release' tag.
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Feb 28 2020 Richard W.M. Jones <rjones@redhat.com> - 0.3.8-0.5.git3aecf8e5350f.1
- OCaml 4.10.0 final (Fedora 32).

* Thu Feb 27 2020 Richard W.M. Jones <rjones@redhat.com> - 0.3.8-0.5.git3aecf8e5350f
- OCaml 4.10.0 final.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.8-0.4.git3aecf8e5350f
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jan 19 2020 Richard W.M. Jones <rjones@redhat.com> - 0.3.8-0.3.git3aecf8e5350f
- OCaml 4.10.0+beta1 rebuild.

* Fri Dec 06 2019 Richard W.M. Jones <rjones@redhat.com> - 0.3.8-0.2.git3aecf8e5350f
- OCaml 4.09.0 (final) rebuild.

* Tue Oct  1 2019 Richard W.M. Jones <rjones@redhat.com> - 0.3.8-0.1
- Move to pre-release of 0.3.8.
- Requires dune.

* Fri Aug 16 2019 Richard W.M. Jones <rjones@redhat.com> - 0.3.7-13
- Bump release and rebuild.

* Fri Aug 16 2019 Richard W.M. Jones <rjones@redhat.com> - 0.3.7-12
- OCaml 4.08.1 (final) rebuild.

* Wed Jul 31 2019 Richard W.M. Jones <rjones@redhat.com> - 0.3.7-11
- OCaml 4.08.1 (rc2) rebuild.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.7-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jul 19 2019 Richard W.M. Jones <rjones@redhat.com> - 0.3.7-9
- Remove camlp4 dependency.
- Add all upstream patches since 0.3.7.

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Richard W.M. Jones <rjones@redhat.com> - 0.3.7-5
- OCaml 4.07.0 (final) rebuild.

* Wed Jun 20 2018 Richard W.M. Jones <rjones@redhat.com> - 0.3.7-4
- OCaml 4.07.0-rc1 rebuild.

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Nov 08 2017 Richard W.M. Jones <rjones@redhat.com> - 0.3.7-2
- OCaml 4.06.0 rebuild.
- Add fix for immutable strings.

* Sat Sep 23 2017 Richard W.M. Jones <rjones@redhat.com> - 0.3.7-1
- Update to new upstream version 0.3.7.
- New URL.
- Include upstream patches since 0.3.7 was released.

* Wed Aug 30 2017 Richard W.M. Jones <rjones@redhat.com> - 0.3.5-18
- Subpackage ocaml-gettext-camomile-devel should depend on
  ocaml-gettext-camomile (thanks: Pino Toscano).

* Mon Aug 07 2017 Richard W.M. Jones <rjones@redhat.com> - 0.3.5-17
- OCaml 4.05.0 rebuild.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.5-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.5-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 26 2017 Richard W.M. Jones <rjones@redhat.com> - 0.3.5-14
- Bump release and rebuild.

* Mon Jun 26 2017 Richard W.M. Jones <rjones@redhat.com> - 0.3.5-13
- OCaml 4.04.2 rebuild.

* Fri May 12 2017 Richard W.M. Jones <rjones@redhat.com> - 0.3.5-12
- Bump release and rebuild.

* Fri May 12 2017 Richard W.M. Jones <rjones@redhat.com> - 0.3.5-11
- OCaml 4.04.1 rebuild.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Nov 04 2016 Richard W.M. Jones <rjones@redhat.com> - 0.3.5-9
- Disable a warning produced with OCaml 4.04.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jul 28 2015 Richard W.M. Jones <rjones@redhat.com> - 0.3.5-7
- OCaml 4.02.3 rebuild.

* Tue Jul 21 2015 Richard W.M. Jones <rjones@redhat.com> - 0.3.5-6
- Enable bytecode builds.
- Disable the tests on bytecode-only platforms.

* Tue Jun 23 2015 Richard W.M. Jones <rjones@redhat.com> - 0.3.5-5
- Bump release and rebuild.

* Wed Jun 17 2015 Richard W.M. Jones <rjones@redhat.com> - 0.3.5-4
- ocaml-4.02.2 rebuild.

* Tue Feb 17 2015 Richard W.M. Jones <rjones@redhat.com> - 0.3.5-3
- Bump release and rebuild.
- Drop upstream patch.

* Mon Feb 16 2015 Richard W.M. Jones <rjones@redhat.com> - 0.3.5-1
- New upstream version 0.3.5.
- ocaml-4.02.1 rebuild.

* Sat Aug 30 2014 Richard W.M. Jones <rjones@redhat.com> - 0.3.4-18
- ocaml-4.02.0 final rebuild.

* Sat Aug 23 2014 Richard W.M. Jones <rjones@redhat.com> - 0.3.4-17
- ocaml-4.02.0+rc1 rebuild.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.4-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Aug 02 2014 Richard W.M. Jones <rjones@redhat.com> - 0.3.4-15
- ocaml-4.02.0-0.8.git10e45753.fc22 rebuild.

* Mon Jul 21 2014 Richard W.M. Jones <rjones@redhat.com> - 0.3.4-14
- OCaml 4.02.0 beta rebuild.

* Tue Jul 15 2014 Richard W.M. Jones <rjones@redhat.com> - 0.3.4-13
- Rebuild for OCaml 4.02.0.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Sep 14 2013 Richard W.M. Jones <rjones@redhat.com> - 0.3.4-11
- Rebuild for OCaml 4.01.0.
- Enable debuginfo.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 27 2012 Richard W.M. Jones <rjones@redhat.com> - 0.3.4-8
- BR >= OCaml 4.00.1 so we can't be built against the wrong OCaml.

* Fri Oct 19 2012 Richard W.M. Jones <rjones@redhat.com> - 0.3.4-7
- Rebuild for OCaml 4.00.1.
- Remove Group lines from the spec file.

* Tue Sep 25 2012 Richard W.M. Jones <rjones@redhat.com> - 0.3.4-6
- (RHEL only) Disable camomile, ocaml-ounit, tests.
- Modernize the spec file.

* Sat Jul 28 2012 Richard W.M. Jones <rjones@redhat.com> - 0.3.4-5
- Bump and rebuild against new OCaml 4.00.0 official release.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 09 2012 Richard W.M. Jones <rjones@redhat.com> - 0.3.4-3
- Rebuild for OCaml 4.00.0.

* Sat May 19 2012 Richard W.M. Jones <rjones@redhat.com> - 0.3.4-2
- Bump release and rebuild for new OCaml on ARM.
- Enable ppc64 support for camomile.

* Fri Jan  6 2012 Richard W.M. Jones <rjones@redhat.com> - 0.3.4-1
- New upstream version 0.3.4.
- Remove patch, now upstream.

* Wed Dec 21 2011 Karsten Hopp <karsten@redhat.com> 0.3.3-8
- fix configure line

* Wed Dec 21 2011 Karsten Hopp <karsten@redhat.com> 0.3.3-7
- build with 'make all', not 'make' as that defaults to 'make test' and fails on ppc64
  due to the missing gettext-camomile

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan  6 2011 Richard W.M. Jones <rjones@redhat.com> - 0.3.3-5
- Add patch for compiling against camomile 0.8.

* Wed Jan 05 2011 Richard W.M. Jones <rjones@redhat.com> - 0.3.3-4
- Rebuild for OCaml 3.12 (http://fedoraproject.org/wiki/Features/OCaml3.12).

* Mon Jan 11 2010 Richard W.M. Jones <rjones@redhat.com> - 0.3.3-3
- Remove BR ocaml-camlidl.  No longer required to build this.

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 0.3.3-2
- Rebuild for OCaml 3.11.2.

* Mon Nov  2 2009 Richard W.M. Jones <rjones@redhat.com> - 0.3.3-1
- New upstream release 0.3.3 (mainly small bugfixes).
- This requires ocaml-fileutils 0.4.0 and is incompatible with
  any earlier version.
- Fixed a number of rpmlint warnings with *.ml files in the
  non-devel package.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 0.3.2-8
- Rebuild for OCaml 3.11.1

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Dec  5 2008 Richard W.M. Jones <rjones@redhat.com> - 0.3.2-6
- Patch to temporarily fix missing dynlink.cma.
- Rebuild for OCaml 3.11.0.

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 0.3.2-5
- Rebuild for OCaml 3.11.0+rc1.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 0.3.2-4
- Rebuild for OCaml 3.11.0

* Mon Jun  9 2008 Richard W.M. Jones <rjones@redhat.com> - 0.3.2-2
- Need to disable tests on ppc64 as well since the tests only work
  with gettext-camomile.

* Mon Jun  9 2008 Richard W.M. Jones <rjones@redhat.com> - 0.3.2-1
- New upstream release 0.3.2 (fixeds rhbz 446916).

* Tue May 27 2008 Richard W.M. Jones <rjones@redhat.com> - 0.3.1-3
- Enable tests, add check section.

* Tue May 27 2008 Richard W.M. Jones <rjones@redhat.com> - 0.3.1-2
- Patch to fix BZ 446916.

* Tue May 27 2008 Richard W.M. Jones <rjones@redhat.com> - 0.3.1-1
- New upstream version 0.3.1.
- Extra runtime requirements (BZ 446919).

* Wed Apr 30 2008 Richard W.M. Jones <rjones@redhat.com> - 0.3.0-1
- New upstream version 0.3.0.
- Big patch no longer required (integrated with upstream).
- findlib < 1.2.1-3 known not to work with this.
- build/ -> _build/
- Re-enable documentation.
- Prevent *.o files from being distributed.
- Distribute *.cmx and *.mli files.

* Sat Apr 26 2008 Richard W.M. Jones <rjones@redhat.com> - 0.2.0-3.20080321patch
- Change the naming scheme to conform with "Snapshot packages" guideline.
- Don't duplicate all the docs in camomile-devel.
- Disable documentation.  Wants 'fop', but 'fop' throws a giant Java
  exception when present.

* Thu Apr 17 2008 Richard W.M. Jones <rjones@redhat.com> - 0.2.0-2rwmj20080321
- Build camomile subpackages because the camomile dependency is
  rather large.  However we can't build camomile on ppc64 yet so
  don't build those subpackages there.

* Fri Mar 21 2008 Richard W.M. Jones <rjones@redhat.com> - 0.2.0-1rwmj20080321
- Initial RPM release.
