# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# OCaml packages not built on i686 since OCaml 5 / Fedora 39.
ExcludeArch: %{ix86}

# NOTE: there is no devel subpackage because the main package *IS* a devel
# package.

%ifnarch %{ocaml_native_compiler}
%global debug_package %{nil}
%endif

Name:          ocaml-ocamlbuild
Version:       0.16.1
Release: 3%{?dist}

Summary:       Build tool for OCaml libraries and programs

License:       LGPL-2.1-or-later WITH OCaml-LGPL-linking-exception

URL:           https://github.com/ocaml/ocamlbuild
VCS:           git:%{url}.git
Source0:       %{url}/archive/%{version}/ocamlbuild-%{version}.tar.gz

BuildRequires: make
BuildRequires: ocaml >= 4.08
BuildRequires: ocaml-rpm-macros
BuildRequires: ncurses
BuildRequires: asciidoc
BuildRequires: python3-pygments

# Ocamlbuild can invoke tput; see src/display.ml
Requires:      ncurses

# This can be removed when F42 reaches EOL
Obsoletes:     %{name}-devel < 0.14.0-37
Provides:      %{name}-devel = %{version}-%{release}


%description
OCamlbuild is a build tool for building OCaml libraries and programs.


%package doc
Summary:       Documentation for %{name}
License:       CC0-1.0
BuildArch:     noarch


%description doc
This package contains the manual for %{name}.


%prep
%autosetup -n ocamlbuild-%{version}


%build
make configure \
  OCAMLBUILD_PREFIX=%{_prefix} \
  OCAMLBUILD_BINDIR=%{_bindir} \
  OCAMLBUILD_LIBDIR=%{_libdir}/ocaml \
  OCAMLBUILD_MANDIR=%{_mandir} \
%ifarch %{ocaml_native_compiler}
  OCAML_NATIVE=true \
  OCAML_NATIVE_TOOLS=true
%else
  OCAML_NATIVE=false \
  OCAML_NATIVE_TOOLS=false
%endif

# Parallel builds fail.
make \
%ifarch %{ocaml_native_compiler}
     OCAMLC="ocamlc.opt -g" \
     OCAMLOPT="ocamlopt.opt -g"
%else
     OCAMLC="ocamlc -g" \
     OCAMLOPT="ocamlopt -g"
%endif

# Build the manual
asciidoc manual/manual.adoc


%install
%make_install CHECK_IF_PREINSTALLED=false

# The install copies ocamlbuild & ocamlbuild.{byte or native}.
# Symlink them instead.
pushd $RPM_BUILD_ROOT/usr/bin
%ifarch %{ocaml_native_compiler}
ln -sf ocamlbuild.native ocamlbuild
%else
ln -sf ocamlbuild.byte ocamlbuild
%endif
popd

%ocaml_files -n


%files -f .ofiles
%doc Changes Readme.md VERSION
%license LICENSE


%files doc
%license manual/LICENSE
%doc manual/manual.html


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jul 11 2025 Jerry James  <loganjerry@gmail.com> - 0.16.1-1
- Version 0.16.1

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jan  9 2025 Jerry James <loganjerry@gmail.com> - 0.15.0-2
- OCaml 5.3.0 rebuild for Fedora 42
- Add VCS field

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jul 04 2024 Richard W.M. Jones <rjones@redhat.com> - 0.15.0-1
- New upstream version 0.15.0 (RHBZ#1992935)

* Wed Jun 19 2024 Richard W.M. Jones <rjones@redhat.com> - 0.14.3-5
- OCaml 5.2.0 ppc64le fix

* Wed May 29 2024 Richard W.M. Jones <rjones@redhat.com> - 0.14.3-4
- OCaml 5.2.0 for Fedora 41

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Jan 02 2024 Richard W.M. Jones <rjones@redhat.com> - 0.14.3-1
- New upstream version 0.14.3 (RHBZ#1992935)

* Mon Dec 18 2023 Richard W.M. Jones <rjones@redhat.com> - 0.14.2-6
- OCaml 5.1.1 + s390x code gen fix for Fedora 40

* Tue Dec 12 2023 Richard W.M. Jones <rjones@redhat.com> - 0.14.2-5
- OCaml 5.1.1 rebuild for Fedora 40

* Thu Oct 05 2023 Richard W.M. Jones <rjones@redhat.com> - 0.14.2-4
- OCaml 5.1 rebuild for Fedora 40

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Richard W.M. Jones <rjones@redhat.com> - 0.14.2-2
- OCaml 5.0 rebuild for Fedora 39

* Mon Jul 10 2023 Jerry James <loganjerry@gmail.com> - 0.14.2-1
- Version 0.14.2
- Convert License tag to SPDX
- Change license for the doc subpackage to CC0
- Make the doc subpackage noarch
- Fold the devel subpackage into the main package
- Ship the manual as HTML instead of asciidoc source
- Use new OCaml macros

* Tue Jan 24 2023 Richard W.M. Jones <rjones@redhat.com> - 0.14.0-36
- Rebuild OCaml packages for F38

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jun 18 2022 Richard W.M. Jones <rjones@redhat.com> - 0.14.0-33
- OCaml 4.14.0 rebuild

* Fri Feb 04 2022 Richard W.M. Jones <rjones@redhat.com> - 0.14.0-32
- Bump release and rebuild.

* Fri Feb 04 2022 Richard W.M. Jones <rjones@redhat.com> - 0.14.0-31
- OCaml 4.13.1 rebuild to remove package notes

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Oct 04 2021 Richard W.M. Jones <rjones@redhat.com> - 0.14.0-29
- Bump and rebuild for OCaml 4.13.1

* Mon Oct 04 2021 Richard W.M. Jones <rjones@redhat.com> - 0.14.0-28
- OCaml 4.13.1 build

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jul 19 2021 Jerry James <loganjerry@gmail.com> - 0.14.0-26
- Specify OCAMLBUILD_MANDIR to fix man page installation

* Mon Mar 15 2021 Richard W.M. Jones <rjones@redhat.com> - 0.14.0-26
- Bump and rebuild for ELN broken deps.

* Sun Feb 28 22:16:45 GMT 2021 Richard W.M. Jones <rjones@redhat.com> - 0.14.0-25
- Bump release and rebuild.

* Sun Feb 28 22:08:24 GMT 2021 Richard W.M. Jones <rjones@redhat.com> - 0.14.0-24
- OCaml 4.12.0 build

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Dec 31 2020 Richard W.M. Jones <rjones@redhat.com> - 0.14.0-22
- Fix license field (RHBZ#1911667).

* Tue Sep 01 2020 Richard W.M. Jones <rjones@redhat.com> - 0.14.0-21
- OCaml 4.11.1 rebuild

* Fri Aug 21 2020 Richard W.M. Jones <rjones@redhat.com> - 0.14.0-20
- OCaml 4.11.0 rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-19
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon May 04 2020 Richard W.M. Jones <rjones@redhat.com> - 0.14.0-17
- OCaml 4.11.0+dev2-2020-04-22 rebuild

* Tue Apr 21 2020 Richard W.M. Jones <rjones@redhat.com> - 0.14.0-16
- OCaml 4.11.0 pre-release attempt 2

* Fri Apr 17 2020 Richard W.M. Jones <rjones@redhat.com> - 0.14.0-15
- OCaml 4.11.0 pre-release

* Thu Apr 02 2020 Richard W.M. Jones <rjones@redhat.com> - 0.14.0-14
- Update all OCaml dependencies for RPM 4.16.

* Wed Feb 26 2020 Richard W.M. Jones <rjones@redhat.com> - 0.14.0-13
- OCaml 4.10.0 final.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jan 18 2020 Richard W.M. Jones <rjones@redhat.com> - 0.14.0-11
- OCaml 4.10.0+beta1 rebuild.

* Thu Jan 09 2020 Richard W.M. Jones <rjones@redhat.com> - 0.14.0-10
- Bump release and rebuild.

* Wed Jan 08 2020 Richard W.M. Jones <rjones@redhat.com> - 0.14.0-9
- Bump and rebuild.

* Tue Jan 07 2020 Richard W.M. Jones <rjones@redhat.com> - 0.14.0-8
- OCaml 4.09.0 for riscv64

* Thu Dec 05 2019 Richard W.M. Jones <rjones@redhat.com> - 0.14.0-7
- Bump and rebuild for fixed ocaml(runtime) dependency.

* Thu Dec 05 2019 Richard W.M. Jones <rjones@redhat.com> - 0.14.0-6
- OCaml 4.09.0 (final) rebuild.

* Fri Aug 16 2019 Richard W.M. Jones <rjones@redhat.com> - 0.14.0-5
- OCaml 4.08.1 (final) rebuild.

* Wed Jul 31 2019 Richard W.M. Jones <rjones@redhat.com> - 0.14.0-4
- OCaml 4.08.1 (rc2) rebuild.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jun 27 2019 Richard W.M. Jones <rjones@redhat.com> - 0.14.0-2
- OCaml 4.08.0 (final) rebuild.

* Mon Apr 29 2019 Richard W.M. Jones <rjones@redhat.com> - 0.14.0-1
- New upstream version 0.14.0.
- OCaml 4.08.0 (beta 3) rebuild.
- Remove the source tarball which was accidentally added to git.

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Richard W.M. Jones <rjones@redhat.com> - 0.12.0-5
- OCaml 4.07.0 (final) rebuild.

* Tue Jun 19 2018 Richard W.M. Jones <rjones@redhat.com> - 0.12.0-4
- OCaml 4.07.0-rc1 rebuild.

* Thu Apr 26 2018 Richard W.M. Jones <rjones@redhat.com> - 0.12.0-3
- OCaml 4.07.0-beta2 rebuild.

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Dec 12 2017 Richard W.M. Jones <rjones@redhat.com> - 0.12.0-1
- New upstream version 0.12.0.

* Tue Nov 07 2017 Richard W.M. Jones <rjones@redhat.com> - 0.11.0-11
- Bump release and rebuild.

* Tue Nov 07 2017 Richard W.M. Jones <rjones@redhat.com> - 0.11.0-10
- OCaml 4.06.0 rebuild.

* Mon Aug 07 2017 Richard W.M. Jones <rjones@redhat.com> - 0.11.0-9
- Bump and rebuild.

* Mon Aug 07 2017 Richard W.M. Jones <rjones@redhat.com> - 0.11.0-8
- Bump and rebuild.

* Mon Aug 07 2017 Richard W.M. Jones <rjones@redhat.com> - 0.11.0-7
- OCaml 4.05.0 rebuild.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Mon Jul 31 2017 Richard W.M. Jones <rjones@redhat.com> - 0.11.0-5
- Enable debug symbols (-g).

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 26 2017 Richard W.M. Jones <rjones@redhat.com> - 0.11.0-3
- OCaml 4.04.2 rebuild.

* Thu May 11 2017 Richard W.M. Jones <rjones@redhat.com> - 0.11.0-2
- OCaml 4.04.1 rebuild.

* Wed May 10 2017 Richard W.M. Jones <rjones@redhat.com> - 0.11.0-1
- New upstream version 0.11.0.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Nov 04 2016 Richard W.M. Jones <rjones@redhat.com> - 0.9.3-5
- New package, ocamlbuild used to be part of ocaml.
