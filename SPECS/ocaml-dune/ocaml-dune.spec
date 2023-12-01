%global libname dune

# Since menhir now requires dune to build, but dune needs menhir only for the
# tests, build in bootstrap mode to skip the tests and the need for menhir.
%bcond_with menhir
%bcond_with emacs

Summary:        A composable build system for OCaml
Name:           ocaml-%{libname}
Version:        2.8.5
Release:        3%{?dist}
# Dune itself is MIT.  Some bundled libraries have a different license:
# ISC:
# - vendor/cmdliner
# LGPLv2:
# - vendor/incremental-cycles
# LGPLv2 with exceptions:
# - vendor/opam-file-format
# - vendor/re
License:        MIT AND LGPLv2 AND LGPLv2 WITH exceptions AND ISC
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://dune.build
Source0:        https://github.com/ocaml/%{libname}/archive/%{version}/%{libname}-%{version}.tar.gz

BuildRequires:  %{py3_dist sphinx-rtd-theme}
BuildRequires:  %{py3_dist sphinx}
BuildRequires:  make
BuildRequires:  ocaml >= 4.08
BuildRequires:  ocaml-csexp-devel >= 1.3.0
BuildRequires:  ocaml-findlib

%if %{with emacs}
BuildRequires:  emacs
%endif

%if %{with menhir}
# Required by tests.
BuildRequires:  ocaml-menhir
%endif

# Dune has vendored deps (ugh):
# I'm not clear on how to unbundle them.
# It seems to be unsupported upstream; the bootstrap process for dune
# doesn't seem to be able to detect libraries installed systemwide.
# https://github.com/ocaml/dune/issues/220
Provides:       bundled(ocaml-build-path-prefix-map) = 0.2
Provides:       bundled(ocaml-opam-file-format) = 2.0.0
Provides:       bundled(ocaml-cmdliner) = 1.0.4
Provides:       bundled(ocaml-re) = 1.9.0
Provides:       dune = %{version}-%{release}
Provides:       jbuilder = %{version}-%{release}

%description
Dune is a build system designed for OCaml/Reason projects only. It focuses
on providing the user with a consistent experience and takes care of most of
the low-level details of OCaml compilation. All you have to do is provide a
description of your project and Dune will do the rest.

The scheme it implements is inspired from the one used inside Jane Street and
adapted to the open source world. It has matured over a long time and is used
daily by hundred of developers, which means that it is highly tested and
productive.

%package        devel
Summary:        Development files for %{name}
License:        MIT AND LGPLv2 AND LGPLv2 WITH exceptions AND ISC

Requires:       %{name}%{?isa} = %{version}-%{release}
Requires:       ocaml-csexp-devel%{?_isa}

%description    devel
The %{name}-devel package contains libraries and
signature files for developing applications that use %{name}.

%package        doc
Summary:        HTML documentation for %{name}
License:        MIT AND LGPLv2 AND LGPLv2 WITH exceptions AND ISC

BuildArch:      noarch

Requires:       %{name} = %{version}-%{release}

%description    doc
HTML documentation for dune, a composable build system for OCaml.

%if %{with emacs}
%package        emacs
Summary:        Emacs support for %{name}
License:        ISC

BuildArch:      noarch

Requires:       %{name} = %{version}-%{release}

%description    emacs
The %{name}-devel package contains Emacs integration with the dune build
system, a mode to edit dune files, and flymake support for dune files.
%endif

%prep
%autosetup -n %{libname}-%{version} -p1

%build
./configure --libdir %{_libdir}/ocaml --mandir %{_mandir}

# This command fails, because ppx_bench, ppx_expect, and core_bench are missing.
# However, it is only tests that fail, not the actual build, so ignore the
# failures and continue.
%make_build release || :
./dune.exe build @install
%make_build doc

# Relink the stublibs.  See https://github.com/ocaml/dune/issues/2977.
cd _build/default/src/stdune
ocamlmklib -g -ldopt "%{build_ldflags}" -o stdune_stubs fcntl_stubs.o
cd -
cd _build/default/src/dune_filesystem_stubs
ocamlmklib -g -ldopt "%{build_ldflags}" -o dune_filesystem_stubs_stubs \
  $(ar t libdune_filesystem_stubs_stubs.a)
cd -

%install
# "make install" only installs the binary.  We want the libraries, too.
./dune.exe install --destdir %{buildroot}

%ifarch %{ocaml_native_compiler}
# Add missing executable bits
find %{buildroot}%{_libdir}/ocaml -name \*.cmxs -exec chmod 0755 {} \+
%endif

%if %{with emacs}
# Byte compile the Emacs files
cd %{buildroot}%{_emacs_sitelispdir}
%_emacs_bytecompile dune.el dune-flymake.el
cd -
%else
rm -rf %{buildroot}%{_datadir}/emacs
%endif

# Install documentation by way of pkgdocdir.
rm -fr %{buildroot}%{_prefix}/doc
mkdir -p %{buildroot}%{_pkgdocdir}/
cp -ar README.md CHANGES.md MIGRATION.md doc/_build/* %{buildroot}%{_pkgdocdir}/

%if %{with menhir}
%check
# These are the only tests we can run.  The others require components that
# either depend on dune themselves or are not available at all.
%{buildroot}%{_bindir}/dune runtest test/unit-tests
%endif

%files
%license LICENSE.md
%doc %{_pkgdocdir}/README.md
%doc %{_pkgdocdir}/CHANGES.md
%doc %{_pkgdocdir}/MIGRATION.md
%{_bindir}/dune
%{_mandir}/man*/dune*
%dir %{_pkgdocdir}/
%dir %{_libdir}/ocaml/dune/
%dir %{_libdir}/ocaml/dune-action-plugin/
%dir %{_libdir}/ocaml/dune-build-info/
%dir %{_libdir}/ocaml/dune-configurator/
%dir %{_libdir}/ocaml/dune-glob/
%dir %{_libdir}/ocaml/dune-private-libs/
%dir %{_libdir}/ocaml/dune-private-libs/dune-lang/
%dir %{_libdir}/ocaml/dune-private-libs/dune_re/
%dir %{_libdir}/ocaml/dune-private-libs/ocaml-config/
%dir %{_libdir}/ocaml/dune-private-libs/stdune/
%dir %{_libdir}/ocaml/dune-site/
%dir %{_libdir}/ocaml/dune-site/plugins/
%{_libdir}/ocaml/dune*/META
%{_libdir}/ocaml/dune*/*.cma
%{_libdir}/ocaml/dune*/*.cmi
%{_libdir}/ocaml/dune-configurator/.private/
%{_libdir}/ocaml/dune-private-libs/*/*.cma
%{_libdir}/ocaml/dune-private-libs/*/*.cmi
%{_libdir}/ocaml/dune-site/*/*.cma
%{_libdir}/ocaml/dune-site/*/*.cmi
%ifarch %{ocaml_native_compiler}
%{_libdir}/ocaml/dune*/*.cmxs
%{_libdir}/ocaml/dune-private-libs/*/*.cmxs
%{_libdir}/ocaml/dune-site/*/*.cmxs
%{_libdir}/ocaml/stublibs/dllstdune_stubs.so
%{_libdir}/ocaml/stublibs/dlldune_filesystem_stubs_stubs.so
%endif

%files devel
%{_libdir}/ocaml/dune*/dune-package
%{_libdir}/ocaml/dune*/opam
%{_libdir}/ocaml/dune*/*.cmt
%{_libdir}/ocaml/dune*/*.cmti
%{_libdir}/ocaml/dune*/*.ml
%{_libdir}/ocaml/dune*/*.mli
%{_libdir}/ocaml/dune-private-libs/*/*.cmt
%{_libdir}/ocaml/dune-private-libs/*/*.cmti
%{_libdir}/ocaml/dune-private-libs/*/*.ml
%{_libdir}/ocaml/dune-private-libs/*/*.mli
%{_libdir}/ocaml/dune-site/*/*.cmt
%{_libdir}/ocaml/dune-site/*/*.cmti
%{_libdir}/ocaml/dune-site/*/*.ml
%{_libdir}/ocaml/dune-site/*/*.mli
%ifarch %{ocaml_native_compiler}
%{_libdir}/ocaml/dune*/*.a
%{_libdir}/ocaml/dune*/*.cmx
%{_libdir}/ocaml/dune*/*.cmxa
%{_libdir}/ocaml/dune-private-libs/*/*.a
%{_libdir}/ocaml/dune-private-libs/*/*.cmx
%{_libdir}/ocaml/dune-private-libs/*/*.cmxa
%{_libdir}/ocaml/dune-site/*/*.a
%{_libdir}/ocaml/dune-site/*/*.cmx
%{_libdir}/ocaml/dune-site/*/*.cmxa
%endif

%files doc
%exclude %{_pkgdocdir}/README.md
%exclude %{_pkgdocdir}/CHANGES.md
%doc %{_pkgdocdir}/*

%if %{with emacs}
%files emacs
%{_emacs_sitelispdir}/dune*
%endif

%changelog
* Thu Mar 31 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.8.5-3
- Cleaning-up spec. License verified.

* Mon Aug 09 2021 Olivia Crain <oliviacrain@microsoft.com> - 2.8.5-2
- Initial CBL-Mariner import from Fedora 34 (license: MIT).
- Remove emacs, menhir support.

* Mon Mar 29 2021 Jerry James <loganjerry@gmail.com> - 2.8.5-1
- Version 2.8.5

* Mon Mar  8 2021 Jerry James <loganjerry@gmail.com> - 2.8.4-1
- Version 2.8.4

* Mon Mar  8 2021 Jerry James <loganjerry@gmail.com> - 2.8.3-1
- Version 2.8.3

* Mon Feb  1 2021 Richard W.M. Jones <rjones@redhat.com> - 2.8.2-3
- Bump and rebuild for updated ocaml Dynlink dependency.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan 21 2021 Jerry James <loganjerry@gmail.com> - 2.8.2-1
- Version 2.8.2

* Thu Jan 14 2021 Jerry James <loganjerry@gmail.com> - 2.8.1-1
- Version 2.8.1

* Wed Jan 13 2021 Jerry James <loganjerry@gmail.com> - 2.8.0-1
- Version 2.8.0
- Drop upstreamed patch from pull request 3757

* Fri Sep 18 2020 Jerry James <loganjerry@gmail.com> - 2.7.1-2
- Add ocaml-csexp-devel R to the -devel subpackage

* Mon Sep 14 2020 Jerry James <loganjerry@gmail.com> - 2.7.1-1
- Version 2.7.1
- Csexp is no longer vendored in
- Drop upstreamed patches for issue 3736 and pull request 3739
- Fix configuration with patch from pull request 3757

* Tue Sep 01 2020 Richard W.M. Jones <rjones@redhat.com> - 2.7.0-6
- OCaml 4.11.1 rebuild

* Mon Aug 24 2020 Richard W.M. Jones <rjones@redhat.com> - 2.7.0-5
- Add fix for https://github.com/ocaml/dune/issues/3736

* Fri Aug 21 2020 Richard W.M. Jones <rjones@redhat.com> - 2.7.0-2
- OCaml 4.11.0 rebuild

* Fri Aug 14 2020 Jerry James <loganjerry@gmail.com> - 2.7.0-1
- Version 2.7.0
- Drop upstreamed patch for issue 3671

* Tue Aug  4 2020 Richard W.M. Jones <rjones@redhat.com> - 2.6.2-2
- Pass -g option when compiling ppx extensions.
  https://github.com/ocaml/dune/pull/3671

* Mon Aug  3 2020 Jerry James <loganjerry@gmail.com> - 2.6.2-1
- New version 2.6.2

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul  2 2020 Jerry James <loganjerry@gmail.com> - 2.6.1-1
- New version 2.6.1

* Sat Jun  6 2020 Jerry James <loganjerry@gmail.com> - 2.6.0-1
- New version 2.6.0

* Mon May 04 2020 Richard W.M. Jones <rjones@redhat.com> - 2.5.1-4
- OCaml 4.11.0+dev2-2020-04-22 rebuild

* Tue Apr 21 2020 Richard W.M. Jones <rjones@redhat.com> - 2.5.1-3
- OCaml 4.11.0 pre-release attempt 2
- Rename cond "bootstrap" as "menhir".

* Sun Apr 19 2020 Jerry James <loganjerry@gmail.com> - 2.5.1-1
- New version 2.5.1

* Sat Apr 18 2020 Richard W.M. Jones <rjones@redhat.com> - 2.5.0-5
- Bump release and rebuild.

* Sat Apr 18 2020 Richard W.M. Jones <rjones@redhat.com> - 2.5.0-4
- Bump release and rebuild.

* Fri Apr 17 2020 Richard W.M. Jones <rjones@redhat.com> - 2.5.0-3
- Bump release and rebuild.

* Fri Apr 17 2020 Richard W.M. Jones <rjones@redhat.com> - 2.5.0-2
- OCaml 4.11.0 pre-release

* Fri Apr 10 2020 Jerry James <loganjerry@gmail.com> - 2.5.0-1
- Version 2.5.0

* Thu Apr 02 2020 Richard W.M. Jones <rjones@redhat.com> - 2.4.0-2
- Update all OCaml dependencies for RPM 4.16.

* Fri Mar  6 2020 Jerry James <loganjerry@gmail.com> - 2.4.0-1
- New version 2.4.0
- Add bootstrap conditional for builds without ocaml-menhir

* Wed Feb 26 2020 Richard W.M. Jones <rjones@redhat.com> - 2.3.1-2
- OCaml 4.10.0 final.

* Thu Feb 20 2020 Jerry James <loganjerry@gmail.com> - 2.3.1-1
- New version 2.3.1 (bz 1805578)

* Tue Feb 18 2020 Jerry James <loganjerry@gmail.com> - 2.3.0-1
- New version 2.3.0 (bz 1803374)

* Fri Feb  7 2020 Jerry James <loganjerry@gmail.com> - 2.2.0-1
- New version 2.2.0 (bz 1742638)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jan 19 2020 Richard W.M. Jones <rjones@redhat.com> - 2.1.2-2
- OCaml 4.10.0+beta1 rebuild.

* Fri Jan 10 2020 Ben Rosser <rosser.bjr@gmail.com> - 2.1.2-1
- Update to latest upstream release, 2.1.2.
- Remove doc patches (as they were accepted upstream).

* Sat Jan  4 2020 Jerry James <loganjerry@gmail.com> - 2.1.0-1
- New version 2.1.0 (bz 1742638)
- Invoke the configure script (bz 1740196)
- Add LGPLv2 to License due to incremental-cycles
- Add -emacs subpackage and byte compile the Emacs Lisp files
- Drop upstreamed 15c04b09a8c06871635d5fd98c3a37089bbde6d9.patch
- Add -doc-emphasis and -doc-scheme patches
- Run the unit tests in %%check

* Fri Dec 06 2019 Richard W.M. Jones <rjones@redhat.com> - 1.11.0-4
- OCaml 4.09.0 (final) rebuild.

* Fri Aug 16 2019 Richard W.M. Jones <rjones@redhat.com> - 1.11.0-3
- OCaml 4.08.1 (final) rebuild.

* Fri Aug 09 2019 Richard W.M. Jones <rjones@redhat.com> - 1.11.0-2
- Work around nodynlink issue on armv7.
  https://github.com/ocaml/dune/issues/2527

* Thu Aug 08 2019 Richard W.M. Jones <rjones@redhat.com> - 1.11.0-1
- New version 1.11.0 (also required for camomile 1.0.2).

* Tue Aug 06 2019 Ben Rosser <rosser.bjr@gmail.com> - 1.10.0-5
- Install dune libraries. Add new ocaml-dune subpackage (rhbz#1737414).

* Wed Jul 31 2019 Richard W.M. Jones <rjones@redhat.com> - 1.10.0-4
- OCaml 4.08.1 (rc2) rebuild.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jun 27 2019 Richard W.M. Jones <rjones@redhat.com> - 1.10.0-2
- OCaml 4.08.0 (final) rebuild.

* Sun Jun 16 2019 Andy Li <andy@onthewings.net> - 1.10.0-1
- Updated to latest upstream release (#1715394).

* Thu May 16 2019 Andy Li <andy@onthewings.net> - 1.9.3-1
- Updated to latest upstream release (#1705660).

* Tue Apr 30 2019 Richard W.M. Jones <rjones@redhat.com> - 1.9.1-2
- OCaml 4.08.0 (beta 3) rebuild.

* Thu Apr 11 2019 Andy Li <andy@onthewings.net> - 1.9.1-1
- Updated to latest upstream release (#1698732).

* Wed Apr 10 2019 Andy Li <andy@onthewings.net> - 1.9.0-1
- Updated to latest upstream release (#1698022).

* Wed Mar 13 2019 Andy Li <andy@onthewings.net> - 1.8.2-1
- Updated to latest upstream release (#1686836).
- Add missing dependency on sphinx_rtd_theme.

* Fri Mar 08 2019 Andy Li <andy@onthewings.net> - 1.8.0-1
- Updated to latest upstream release (#1686466).

* Fri Mar 01 2019 Andy Li <andy@onthewings.net> - 1.7.3-1
- Renamed source package from jbuilder to ocaml-dune.
- Updated URLs and license according to upstream changes.
- Updated to latest upstream release (#1600105).
- Removed 1113.patch which has been applied upstream in eariler version.
- Removed rpm check section since the upstream tests depend on opam.

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Aug 07 2018 Ben Rosser <rosser.bjr@gmail.com> - 1.0.1-1
- Updated to latest upstream release.
- Manpages have been renamed to 'dune'. A 'dune' binary is now provided as well.

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.12.beta20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed May 02 2018 Ben Rosser <rosser.bjr@gmail.com> - 1.0-0.11.beta20
- Updated to latest upstream release (#1537836).

* Tue Mar 06 2018 Ben Rosser <rosser.bjr@gmail.com> - 1.0-0.10.beta18
- Updated to latest upstream release (#1537836).

* Mon Feb 12 2018 Ben Rosser <rosser.bjr@gmail.com> - 1.0-0.9.beta17
- Update to upstream re-release of beta 17.

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.8.beta17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 30 2018 Ben Rosser <rosser.bjr@gmail.com> - 1.0-0.7.beta18
- Fix build failure on ppc64 by always using bytecode ocaml compiler to bootstrap.

* Wed Jan 24 2018 Ben Rosser <rosser.bjr@gmail.com> 1.0-0.6.beta17
- Update to latest upstream release, beta17 (#1537836).
- Remove unit tests that require external deps (that themselves require jbuilder).

* Tue Nov 14 2017 Ben Rosser <rosser.bjr@gmail.com> 1.0-0.5.beta16
- Update to latest upstream release, beta16 (#1509749).
- Add pre_tag version suffix to source flie name to avoid confusion.

* Mon Oct 23 2017 Ben Rosser <rosser.bjr@gmail.com> 1.0-0.4.beta14
- Update to latest upstream release, beta14 (#1504414).

* Mon Aug 28 2017 Ben Rosser <rosser.bjr@gmail.com> 1.0-0.3.beta12
- Update to latest upstream release, beta12.
- Fix typo in description.
- Use simpler github source URL.
- Use make_build macros when compiling.

* Tue Aug 15 2017 Ben Rosser <rosser.bjr@gmail.com> 1.0-0.2.beta11
- Update to a git snapshot so opam can be built against.
- Modernize ocaml packaging.

* Tue Aug  1 2017 Ben Rosser <rosser.bjr@gmail.com> 1.0-0.1.beta11
- Initial package.
