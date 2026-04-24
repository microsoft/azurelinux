# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# This breaks basic usage of the package:
# ocamlfind ocamlopt -package labltk tktest.ml -linkpkg -o tktest
# gcc: fatal error: environment variable ‘RPM_ARCH’ not defined
%undefine _package_note_flags

# OCaml packages not built on i686 since OCaml 5 / Fedora 39.
ExcludeArch: %{ix86}

%global giturl https://github.com/garrigue/labltk

Name:          ocaml-labltk
Version:       8.06.15
Release: 4%{?dist}

Summary:       Tcl/Tk interface for OCaml

License:       LGPL-2.1-or-later WITH OCaml-LGPL-linking-exception

URL:           https://garrigue.github.io/labltk/
VCS:           git:%{giturl}.git
Source0:       %{giturl}/archive/%{version}/labltk-%{version}.tar.gz

# This adds debugging (-g) everywhere.
Patch1:        labltk-8.06.11-enable-debugging.patch

# Resolve an issue with ./configure and Tcl detection.
Patch2:        labltk-8.06.12-use-fpic-configure.patch

BuildRequires: make
BuildRequires: ocaml
BuildRequires: ocaml-ocamldoc
BuildRequires: ocaml-rpm-macros
BuildRequires: tcl-devel, tk-devel

%global _desc %{expand:
labltk or mlTk is a library for interfacing OCaml with the scripting
language Tcl/Tk (all versions since 8.0.3, but no betas).}


%description %_desc


%package devel
Summary:       Tcl/Tk interface for OCaml

Requires:      %{name}%{?_isa} = %{version}-%{release}
Requires:      tcl-devel%{?_isa}
Requires:      tk-devel%{?_isa}


%description devel %_desc

This package contains the development files.


%package doc
Summary:       Documentation for labltk
BuildArch:     noarch


%description doc %_desc

This package contains the API reference.


%prep
%autosetup -n labltk-%{version} -p1

# Remove version control files which might get copied into documentation.
find -name .gitignore -delete

# Don't build ocamlbrowser.
mv browser browser.old
mkdir browser
echo -e 'all:\ninstall:\n' > browser/Makefile

# Use of the hardening linker flags without the hardening C flags leads to
# failure of the configure script.  We don't need linker flags for this step.
sed -i 's/^cclibs=.*/cclibs=/' configure


%build
./configure -verbose

# Build does not work in parallel.
unset MAKEFLAGS

%ifarch %{ocaml_native_compiler}
make all opt \
     SHAREDCCCOMPOPTS='%{build_cflags} -fPIC' \
     TK_LINK="%{build_ldflags} $(pkg-config --libs tk)"
%else
make byte
%endif

# Build documentation
# make apiref does not work
MLIS=$(ls -1d labltk/*.mli | grep -Fv _tkgen.mli)
mkdir apiref
/usr/bin/ocamldoc -I +unix -I +threads -I support -I labltk -I camltk \
  support/fileevent.mli support/support.mli support/textvariable.mli \
  support/timer.mli support/tkthread.mli support/widget.mli $MLIS \
  labltk/tk.ml -sort -d apiref -html


%install
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_libdir}/ocaml/labltk
mkdir -p $RPM_BUILD_ROOT%{_libdir}/ocaml/stublibs
make install \
    BINDIR=$RPM_BUILD_ROOT%{_bindir} \
    INSTALLDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml/labltk \
    STUBLIBDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml/stublibs \
    RANLIB=:

sed 's/8\.06\.6/%{version}/' support/META > \
    $RPM_BUILD_ROOT%{ocamldir}/labltk/META

%ocaml_files


%files -f .ofiles
%doc Changes README.mlTk


%files devel -f .ofiles-devel
%doc README.mlTk


%files doc
%doc examples_camltk
%doc examples_labltk
%doc apiref


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 8.06.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jul 11 2025 Jerry James  <loganjerry@gmail.com> - 8.06.15-2
- Rebuild to fix OCaml dependencies

* Mon Feb 03 2025 Richard W.M. Jones <rjones@redhat.com> - 8.06.15-1
- New upstream version 8.06.15
- Includes Tcl 9 support (RHBZ#2337740)

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 8.06.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jan  9 2025 Jerry James <loganjerry@gmail.com> - 8.06.14-2
- OCaml 5.3.0 rebuild for Fedora 42

* Thu Aug  1 2024 Jerry James <loganjerry@gmail.com> - 8.06.14-1
- Version 8.06.14
- Drop upstreamed patch to avoid implicit int in configure

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 8.06.13-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 19 2024 Richard W.M. Jones <rjones@redhat.com> - 8.06.13-12
- OCaml 5.2.0 ppc64le fix

* Wed May 29 2024 Richard W.M. Jones <rjones@redhat.com> - 8.06.13-11
- OCaml 5.2.0 for Fedora 41

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 8.06.13-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 8.06.13-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 18 2023 Richard W.M. Jones <rjones@redhat.com> - 8.06.13-8
- OCaml 5.1.1 + s390x code gen fix for Fedora 40

* Tue Dec 12 2023 Richard W.M. Jones <rjones@redhat.com> - 8.06.13-7
- OCaml 5.1.1 rebuild for Fedora 40

* Thu Oct 05 2023 Richard W.M. Jones <rjones@redhat.com> - 8.06.13-6
- OCaml 5.1 rebuild for Fedora 40

* Wed Oct  4 2023 Jerry James <loganjerry@gmail.com> - 8.06.13-5
- Depend on ocaml-rpm-macros instead of python3

* Sat Sep  9 2023 Jerry James <loganjerry@gmail.com> - 8.06.13-4
- Add devel package dependency on tcl-/tk-devel

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 8.06.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Richard W.M. Jones <rjones@redhat.com> - 8.06.13-2
- OCaml 5.0 rebuild for Fedora 39

* Mon Jul 10 2023 Jerry James <loganjerry@gmail.com> - 8.06.13-1
- Version 8.06.13
- Convert License tag to SPDX
- Update project URL
- Install META file
- New doc subpackage for the documentation
- Fix configure script failure
- Compute linker flags more robustly
- Use new OCaml macros

* Sat Apr 15 2023 Florian Weimer <fweimer@redhat.com> - 8.06.12-4
- Port configure stage to C99

* Tue Jan 24 2023 Richard W.M. Jones <rjones@redhat.com> - 8.06.12-3
- Rebuild OCaml packages for F38

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 8.06.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Sep 20 2022 Richard W.M. Jones <rjones@redhat.com> - 8.06.12-1
- New upstream version 8.06.12
- Enable verbose output from configure script.

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 8.06.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jun 18 2022 Richard W.M. Jones <rjones@redhat.com> - 8.06.11-4
- OCaml 4.14.0 rebuild

* Fri Feb 04 2022 Richard W.M. Jones <rjones@redhat.com> - 8.06.11-3
- OCaml 4.13.1 rebuild to remove package notes

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 8.06.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Oct 04 2021 Richard W.M. Jones <rjones@redhat.com> - 8.06.11-1
- New upstream version 8.06.11
- OCaml 4.13.1 build

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 8.06.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Mar 15 2021 Richard W.M. Jones <rjones@redhat.com> - 8.06.10-2
- Bump and rebuild for ELN broken deps.

* Mon Mar  1 22:24:19 GMT 2021 Richard W.M. Jones <rjones@redhat.com> - 8.06.10-1
- New upstream version 8.06.10.
- Now hosted on github.

* Sun Feb 28 22:24:19 GMT 2021 Richard W.M. Jones <rjones@redhat.com> - 8.06.5-23
- Bump release and rebuild.

* Sun Feb 28 22:16:43 GMT 2021 Richard W.M. Jones <rjones@redhat.com> - 8.06.5-22
- OCaml 4.12.0 build

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 8.06.5-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Sep 01 2020 Richard W.M. Jones <rjones@redhat.com> - 8.06.5-20
- OCaml 4.11.1 rebuild

* Fri Aug 21 2020 Richard W.M. Jones <rjones@redhat.com> - 8.06.5-19
- OCaml 4.11.0 rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 8.06.5-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon May 04 2020 Richard W.M. Jones <rjones@redhat.com> - 8.06.5-17
- OCaml 4.11.0+dev2-2020-04-22 rebuild

* Tue Apr 21 2020 Richard W.M. Jones <rjones@redhat.com> - 8.06.5-16
- OCaml 4.11.0 pre-release attempt 2

* Fri Apr 17 2020 Richard W.M. Jones <rjones@redhat.com> - 8.06.5-15
- OCaml 4.11.0 pre-release

* Thu Apr 02 2020 Richard W.M. Jones <rjones@redhat.com> - 8.06.5-14
- Update all OCaml dependencies for RPM 4.16.

* Wed Feb 26 2020 Richard W.M. Jones <rjones@redhat.com> - 8.06.5-13
- OCaml 4.10.0 final.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 8.06.5-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jan 18 2020 Richard W.M. Jones <rjones@redhat.com> - 8.06.5-11
- OCaml 4.10.0+beta1 rebuild.

* Thu Jan 09 2020 Richard W.M. Jones <rjones@redhat.com> - 8.06.5-10
- Bump release and rebuild.

* Tue Jan 07 2020 Richard W.M. Jones <rjones@redhat.com> - 8.06.5-9
- OCaml 4.09.0 for riscv64

* Thu Dec 05 2019 Richard W.M. Jones <rjones@redhat.com> - 8.06.5-8
- Bump and rebuild for fixed ocaml(runtime) dependency.

* Thu Dec 05 2019 Richard W.M. Jones <rjones@redhat.com> - 8.06.5-7
- Bump release and rebuild.

* Thu Dec 05 2019 Richard W.M. Jones <rjones@redhat.com> - 8.06.5-6
- OCaml 4.09.0 (final) rebuild.

* Fri Aug 16 2019 Richard W.M. Jones <rjones@redhat.com> - 8.06.5-5
- OCaml 4.08.1 (final) rebuild.

* Wed Jul 31 2019 Richard W.M. Jones <rjones@redhat.com> - 8.06.5-4
- OCaml 4.08.1 (rc2) rebuild.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 8.06.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jun 27 2019 Richard W.M. Jones <rjones@redhat.com> - 8.06.5-2
- OCaml 4.08.0 (final) rebuild.

* Mon Apr 29 2019 Richard W.M. Jones <rjones@redhat.com> - 8.06.5-1
- New upstream version 8.06.5.
- Try harder to set CFLAGS and LDFLAGS.
- Don't build ocamlbrowser.
- OCaml 4.08.0 (beta 3) rebuild.

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 8.06.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 8.06.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Richard W.M. Jones <rjones@redhat.com> - 8.06.4-6
- OCaml 4.07.0 (final) rebuild.

* Tue Jun 19 2018 Richard W.M. Jones <rjones@redhat.com> - 8.06.4-5
- OCaml 4.07.0-rc1 rebuild.

* Thu Apr 26 2018 Richard W.M. Jones <rjones@redhat.com> - 8.06.4-4
- OCaml 4.07.0-beta2 rebuild.
- Kill -warn-error.

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 8.06.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Nov 07 2017 Richard W.M. Jones <rjones@redhat.com> - 8.06.4-2
- OCaml 4.06.0 rebuild.
- Add -g flag to all calls to gcc as well.

* Tue Nov 07 2017 Richard W.M. Jones <rjones@redhat.com> - 8.06.4-1
- New upstream version 8.06.4.

* Mon Aug 07 2017 Richard W.M. Jones <rjones@redhat.com> - 8.06.3-1
- New upstream version 8.06.3 (including fixes for OCaml 4.05).
- OCaml 4.05.0 rebuild.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 8.06.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 8.06.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 26 2017 Richard W.M. Jones <rjones@redhat.com> - 8.06.2-4
- OCaml 4.04.2 rebuild.

* Wed May 10 2017 Richard W.M. Jones <rjones@redhat.com> - 8.06.2-3
- Rebuild for OCaml 4.04.1.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 8.06.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Nov 04 2016 Richard W.M. Jones <rjones@redhat.com> - 8.06.2-1
- New upstream version 8.06.2.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 8.06.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jul 28 2015 Richard W.M. Jones <rjones@redhat.com> - 8.06.0-5
- OCaml 4.02.3 rebuild.

* Wed Jul 22 2015 Richard W.M. Jones <rjones@redhat.com> - 8.06.0-4
- s390x: Don't copy *.o files when building bytecode.

* Wed Jun 24 2015 Richard W.M. Jones <rjones@redhat.com> - 8.06.0-3
- ocaml-4.02.2 final rebuild.

* Wed Jun 17 2015 Richard W.M. Jones <rjones@redhat.com> - 8.06.0-2
- ocaml-4.02.2 rebuild.

* Mon Feb 16 2015 Richard W.M. Jones <rjones@redhat.com> - 8.06.0-1
- New upstream version 8.06.0.
- Big jump in upstream version numbers to match Tk versions.
- ocaml-4.02.1 rebuild.

* Sat Aug 30 2014 Richard W.M. Jones <rjones@redhat.com> - 4.02-0.7.beta1
- ocaml-4.02.0 final rebuild.

* Fri Aug 22 2014 Richard W.M. Jones <rjones@redhat.com> - 4.02-0.6.beta1
- ocaml-4.02.0+rc1 rebuild.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.02-0.5.beta1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 01 2014 Richard W.M. Jones <rjones@redhat.com> - 4.02-0.4.beta1
- ocaml-4.02.0-0.8.git10e45753.fc22 rebuild.

* Tue Jul 22 2014 Richard W.M. Jones <rjones@redhat.com> - 4.02-0.3.beta1
- OCaml 4.02.0 beta rebuild.

* Tue Jul 22 2014 Richard W.M. Jones <rjones@redhat.com> - 4.02-0.2.beta1
- Enable debugging.
- Move labltk to -devel package.
- Enable _smp_flags.

* Tue Jul 22 2014 Richard W.M. Jones <rjones@redhat.com> - 4.02-0.1.beta1
- Initial packaging of new out-of-tree ocaml-labltk.
