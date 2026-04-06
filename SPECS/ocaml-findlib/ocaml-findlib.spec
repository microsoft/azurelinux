# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# OCaml packages not built on i686 since OCaml 5 / Fedora 39.
ExcludeArch: %{ix86}

%ifnarch %{ocaml_native_compiler}
%global debug_package %{nil}
%endif

Name:           ocaml-findlib
Version:        1.9.8
Release:        4%{?dist}
Summary:        Objective CAML package manager and build helper
License:        MIT

URL:            http://projects.camlcity.org/projects/findlib.html
VCS:            git:https://github.com/ocaml/ocamlfind.git
Source0:        http://download.camlcity.org/download/findlib-%{version}.tar.gz

# Fix the toolbox build with OCaml 5.x
Patch0:         %{name}-toolbox.patch

BuildRequires:  ocaml >= 4.02.0
BuildRequires:  ocaml-labltk-devel
BuildRequires:  ocaml-ocamlbuild
BuildRequires:  ocaml-compiler-libs
BuildRequires:  ocaml-ocamldoc
BuildRequires:  ocaml-rpm-macros
BuildRequires:  m4, ncurses-devel
BuildRequires:  make
Requires:       ocaml

# Do not require ocaml-compiler-libs at runtime
%global __ocaml_requires_opts -i Asttypes -i Build_path_prefix_map -i Cmi_format -i Env -i Format_doc -i Ident -i Identifiable -i Load_path -i Location -i Longident -i Misc -i Oprint -i Outcometree -i Parsetree -i Path -i Primitive -i Shape -i Subst -i Topdirs -i Toploop -i Type_immediacy -i Types -i Unit_info -i Warnings


%description
Objective CAML package manager and build helper.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}


%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -p1 -n findlib-%{version}

# Fix character encoding
iconv -f ISO8859-1 -t UTF-8 doc/README > doc/README.utf8
touch -r doc/README doc/README.utf8
mv doc/README.utf8 doc/README

# Fix the OCaml core man directory
sed -i 's,/usr/local/man,%{_mandir},' configure

# Build an executable that is not damaged by stripping
sed -i 's/\(custom=\)-custom/\1-output-complete-exe/' configure

# Skip broken test for ocamlopt -g
sed -i '/^ocamlopt -g/d' configure


%build
ocamlc -version
ocamlc -where
(cd tools/extract_args && make)
tools/extract_args/extract_args -o src/findlib/ocaml_args.ml ocamlc ocamlcp ocamlmktop ocamlopt ocamldep ocamldoc ||:
cat src/findlib/ocaml_args.ml
./configure -config %{_sysconfdir}/findlib.conf \
  -bindir %{_bindir} \
  -sitelib `ocamlc -where` \
  -mandir %{_mandir} \
  -with-toolbox
%make_build all
%ifarch %{ocaml_native_compiler}
%make_build opt
%endif
rm doc/guide-html/TIMESTAMP


%install
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
%make_install \
     OCAMLFIND_BIN=%{_bindir} \
     OCAMLFIND_CONF=%{_sysconfdir} \
     OCAMLFIND_MAN=%{_mandir}
rmdir $RPM_BUILD_ROOT%{_mandir}/man3

%ocaml_files
sed -i '/etc/d' .ofiles


%files -f .ofiles
%doc LICENSE doc/README
%config(noreplace) %{_sysconfdir}/findlib.conf


%files devel -f .ofiles-devel
%doc LICENSE doc/README doc/guide-html


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jul 11 2025 Jerry James  <loganjerry@gmail.com> - 1.9.8-3
- Rebuild to fix OCaml dependencies

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jan  9 2025 Jerry James <loganjerry@gmail.com> - 1.9.8-1
- OCaml 5.3.0 rebuild for Fedora 42
- Version 1.9.8
- Drop workaround for upstream dynlink_subdir bug
- Change config name to findlib.conf to match upstream
- Update __ocaml_requires_opts for OCaml 5.3.0

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.6-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 19 2024 Richard W.M. Jones <rjones@redhat.com> - 1.9.6-13
- OCaml 5.2.0 ppc64le fix

* Wed May 29 2024 Richard W.M. Jones <rjones@redhat.com> - 1.9.6-12
- OCaml 5.2.0 for Fedora 41

* Mon Jan 29 2024 Richard W.M. Jones <rjones@redhat.com> - 1.9.6-11
- Bump and rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 18 2023 Richard W.M. Jones <rjones@redhat.com> - 1.9.6-8
- OCaml 5.1.1 + s390x code gen fix for Fedora 40

* Tue Dec 12 2023 Richard W.M. Jones <rjones@redhat.com> - 1.9.6-7
- OCaml 5.1.1 rebuild for Fedora 40

* Thu Oct 05 2023 Richard W.M. Jones <rjones@redhat.com> - 1.9.6-6
- OCaml 5.1 rebuild for Fedora 40

* Wed Oct  4 2023 Jerry James <loganjerry@gmail.com> - 1.9.6-5
- Build an executable that is not damaged by stripping

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Richard W.M. Jones <rjones@redhat.com> - 1.9.6-4
- OCaml 5.0 rebuild for Fedora 39

* Mon Jul 10 2023 Jerry James <loganjerry@gmail.com> - 1.9.6-3
- OCaml 5.0.0 rebuild
- Verify the License is valid SPDX
- Fix natdynlink detection
- Add patch to fix toolbox build for OCaml 5.x
- Convert README to UTF-8
- Use new OCaml macros

* Tue Jan 24 2023 Richard W.M. Jones <rjones@redhat.com> - 1.9.6-2
- Rebuild OCaml packages for F38

* Mon Jan 23 2023 Richard W.M. Jones <rjones@redhat.com> - 1.9.6-1
- New upstream version 1.9.6

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun Jun 19 2022 Richard W.M. Jones <rjones@redhat.com> - 1.9.5-1
- New upstream version 1.9.5

* Sat Jun 18 2022 Richard W.M. Jones <rjones@redhat.com> - 1.9.4-2
- OCaml 4.14.0 rebuild

* Wed Jun 08 2022 Richard W.M. Jones <rjones@redhat.com> - 1.9.4-1
- Update to findlib 1.9.4

* Fri Feb 04 2022 Richard W.M. Jones <rjones@redhat.com> - 1.9.3-2
- OCaml 4.13.1 rebuild to remove package notes

* Wed Jan 26 2022 Richard W.M. Jones <rjones@redhat.com> - 1.9.3-1
- Update to findlib 1.9.3

* Sat Jan 22 2022 Richard W.M. Jones <rjones@redhat.com> - 1.9.2-1
- Update to findlib 1.9.2
- Remove patch which has been applied upstream.

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jan  7 2022 Jerry James <loganjerry@gmail.com> - 1.9.1-4
- Fix labltk detection
- Change license from BSD to MIT

* Mon Oct 04 2021 Richard W.M. Jones <rjones@redhat.com> - 1.9.1-3
- Bump and rebuild for updated ocaml-labltk

* Mon Oct 04 2021 Richard W.M. Jones <rjones@redhat.com> - 1.9.1-2
- OCaml 4.13.1 build

* Mon Oct 04 2021 Richard W.M. Jones <rjones@redhat.com> - 1.9.1-1
- New upstream development version 1.9.1

* Tue Jul 27 2021 Richard W.M. Jones <rjones@redhat.com> - 1.9-3
- Rebuild for changed ocamlx(Dynlink)

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Mar 15 2021 Richard W.M. Jones <rjones@redhat.com> - 1.9-1
- New upstream version 1.9.

* Mon Mar 15 2021 Richard W.M. Jones <rjones@redhat.com> - 1.8.1-26
- Bump and rebuild for ELN broken deps.

* Mon Mar  1 2021 Richard W.M. Jones <rjones@redhat.com> - 1.8.1-25
- Rebuild for updated ocaml-labltk

* Mon Mar  1 09:37:08 GMT 2021 Richard W.M. Jones <rjones@redhat.com> - 1.8.1-24
- OCaml 4.12.0 build

* Mon Feb  1 2021 Richard W.M. Jones <rjones@redhat.com> - 1.8.1-23
- Bump and rebuild for updated ocaml Dynlink dependency.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.1-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Sep 01 2020 Richard W.M. Jones <rjones@redhat.com> - 1.8.1-21
- OCaml 4.11.1 rebuild

* Fri Aug 21 2020 Richard W.M. Jones <rjones@redhat.com> - 1.8.1-20
- OCaml 4.11.0 rebuild

* Mon Aug 03 2020 Richard W.M. Jones <rjones@redhat.com> - 1.8.1-19
- Bump and rebuild to fix Dynlink dependency.

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.1-18
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon May 04 2020 Richard W.M. Jones <rjones@redhat.com> - 1.8.1-16
- OCaml 4.11.0+dev2-2020-04-22 rebuild

* Tue Apr 21 2020 Richard W.M. Jones <rjones@redhat.com> - 1.8.1-15
- OCaml 4.11.0 pre-release attempt 2

* Fri Apr 17 2020 Richard W.M. Jones <rjones@redhat.com> - 1.8.1-14
- OCaml 4.11.0 pre-release

* Thu Apr 02 2020 Richard W.M. Jones <rjones@redhat.com> - 1.8.1-13
- Update all OCaml dependencies for RPM 4.16.

* Wed Feb 26 2020 Richard W.M. Jones <rjones@redhat.com> - 1.8.1-12
- OCaml 4.10.0 final.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jan 19 2020 Richard W.M. Jones <rjones@redhat.com> - 1.8.1-10
- OCaml 4.10.0+beta1 rebuild.

* Thu Jan 09 2020 Richard W.M. Jones <rjones@redhat.com> - 1.8.1-9
- Bump release and rebuild.

* Wed Jan 08 2020 Richard W.M. Jones <rjones@redhat.com> - 1.8.1-8
- OCaml 4.09.0 for riscv64

* Thu Dec 05 2019 Richard W.M. Jones <rjones@redhat.com> - 1.8.1-7
- Bump and rebuild for fixed ocaml(runtime) dependency.

* Thu Dec 05 2019 Richard W.M. Jones <rjones@redhat.com> - 1.8.1-6
- OCaml 4.09.0 (final) rebuild.

* Thu Dec 05 2019 Richard W.M. Jones <rjones@redhat.com> - 1.8.1-5
- Final removal of camlp4.

* Mon Sep 02 2019 Richard W.M. Jones <rjones@redhat.com> - 1.8.1-4
- Rebuild with camlp4.

* Fri Aug 16 2019 Richard W.M. Jones <rjones@redhat.com> - 1.8.1-3
- OCaml 4.08.1 (final) rebuild.

* Wed Jul 31 2019 Richard W.M. Jones <rjones@redhat.com> - 1.8.1-2
- OCaml 4.08.1 (rc2) rebuild.

* Tue Jul 30 2019 Richard W.M. Jones <rjones@redhat.com> - 1.8.1-1
- New upstream version 1.8.1.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jun 27 2019 Richard W.M. Jones <rjones@redhat.com> - 1.8.0-8
- OCaml 4.08.0 (final) rebuild.

* Mon Apr 29 2019 Richard W.M. Jones <rjones@redhat.com> - 1.8.0-7
- OCaml 4.08.0 (beta 3) rebuild.

* Mon Apr 29 2019 Richard W.M. Jones <rjones@redhat.com> - 1.8.0-6
- Disable ocaml-camlp4 dependency until ported to 4.08.

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Richard W.M. Jones <rjones@redhat.com> - 1.8.0-3
- OCaml 4.07.0 (final) rebuild.

* Tue Jun 19 2018 Richard W.M. Jones <rjones@redhat.com> - 1.8.0-2
- OCaml 4.07.0-rc1 rebuild.

* Thu Apr 26 2018 Richard W.M. Jones <rjones@redhat.com> - 1.8.0-1
- Update to findlib 1.8.0.
- Remove upstream patches.

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Nov 08 2017 Richard W.M. Jones <rjones@redhat.com> - 1.7.3-9
- Bump release and rebuild.

* Wed Nov 08 2017 Richard W.M. Jones <rjones@redhat.com> - 1.7.3-8
- BR ocaml-num-devel (unfortunately a circular dependency).

* Tue Nov 07 2017 Richard W.M. Jones <rjones@redhat.com> - 1.7.3-7
- OCaml 4.06.0 rebuild.

* Fri Sep 22 2017 Richard W.M. Jones <rjones@redhat.com> - 1.7.3-6
- Enable stripping and debuginfo on s390x.
- Use ocaml_native_compiler macro instead of opt test.

* Mon Aug 07 2017 Richard W.M. Jones <rjones@redhat.com> - 1.7.3-5
- OCaml 4.05.0 rebuild.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 26 2017 Richard W.M. Jones <rjones@redhat.com> - 1.7.3-2
- OCaml 4.04.2 rebuild.

* Mon Jun  5 2017 Richard W.M. Jones <rjones@redhat.com> - 1.7.3-1
- New upstream version 1.7.3.

* Wed May 10 2017 Richard W.M. Jones <rjones@redhat.com> - 1.7.1-3
- Rebuild for OCaml 4.04.1.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Nov 22 2016 Richard W.M. Jones <rjones@redhat.com> - 1.7.1-1
- New upstream version 1.7.1.

* Wed Nov 09 2016 Dan Horák <dan@danny.cz> - 1.6.3-3
- rebuild for s390x codegen bug

* Sat Nov 05 2016 Richard W.M. Jones <rjones@redhat.com> - 1.6.3-2
- Force ocamlbuild and labltk to be installed so findlib creates META for them.

* Fri Nov 04 2016 Richard W.M. Jones <rjones@redhat.com> - 1.6.3-1
- New upstream version 1.6.3.

* Tue Jul 19 2016 Richard W.M. Jones <rjones@redhat.com> - 1.6.2-1
- New upstream version 1.6.2.
- Fix make install rule.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jul 28 2015 Richard W.M. Jones <rjones@redhat.com> - 1.5.5-7
- OCaml 4.02.3 rebuild.

* Wed Jul 22 2015 Richard W.M. Jones <rjones@redhat.com> - 1.5.5-6
- s/390x: Disable debuginfo generation (which strips binaries) when building
  bytecode.

* Fri Jul 17 2015 Richard W.M. Jones <rjones@redhat.com> - 1.5.5-5
- s/390x: Don't strip the ocamlfind binary when building bytecode.

* Wed Jun 24 2015 Richard W.M. Jones <rjones@redhat.com> - 1.5.5-4
- ocaml-4.02.2 final rebuild.

* Wed Jun 17 2015 Richard W.M. Jones <rjones@redhat.com> - 1.5.5-3
- Bump release and rebuild for ocaml-4.02.2

* Mon Feb 16 2015 Richard W.M. Jones <rjones@redhat.com> - 1.5.5-2
- Bump release and rebuild.

* Mon Feb 16 2015 Richard W.M. Jones <rjones@redhat.com> - 1.5.5-1
- New upstream version 1.5.5 for ocaml-4.02.1 rebuild.

* Sat Aug 30 2014 Richard W.M. Jones <rjones@redhat.com> - 1.5.2-3
- Bump release and rebuild.

* Sat Aug 30 2014 Richard W.M. Jones <rjones@redhat.com> - 1.5.2-2
- ocaml-4.02.0 final rebuild.

* Fri Aug 22 2014 Richard W.M. Jones <rjones@redhat.com> - 1.5.2-1
- New upstream release 1.5.2.
- ocaml-4.02.0+rc1 rebuild.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 01 2014 Richard W.M. Jones <rjones@redhat.com> - 1.5.1-3
- ocaml-4.02.0-0.8.git10e45753.fc22 rebuild.

* Thu Jul 17 2014 Richard W.M. Jones <rjones@redhat.com> - 1.5.1-2
- Rebuild for new camlp4 package for OCaml 4.02.0 beta rebuild.

* Sat Jul 12 2014 Richard W.M. Jones <rjones@redhat.com> - 1.5.1-1
- New upstream version 1.5.1.
- Disable labltk and camlp4.  We will reenable when they are added back
  into Fedora.
- Remove findlib/make_wizard and findlib/make_wizard.pattern.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Dan Horák <dan[at]danny.cz> - 1.4-2
- drop ExcludeArch

* Fri Sep 13 2013 Richard W.M. Jones <rjones@redhat.com> - 1.4-1
- New upstream version 1.4.
- Build debuginfo.
- Add -g option when running ocamlopt to generate debuginfo.
- Don't need anti-prelink / stripping hacks for modern OCaml.
- Modernize spec file.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 27 2012 Richard W.M. Jones <rjones@redhat.com> - 1.3.3-3
- BR >= OCaml 4.00.1 so we can't build against the wrong OCaml version.

* Tue Oct 16 2012 Richard W.M. Jones <rjones@redhat.com> - 1.3.3-2
- Rebuild for OCaml 4.00.1.

* Sat Jul 28 2012 Richard W.M. Jones <rjones@redhat.com> - 1.3.3-1
- New upstream version 1.3.3.
- Remove patch for OCaml 4 which has been obsoleted by upstream changes.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 10 2012 Richard W.M. Jones <rjones@redhat.com> - 1.3.1-2
- Rebuild for OCaml 4.00.0.

* Thu Jun  7 2012 Richard W.M. Jones <rjones@redhat.com> - 1.3.1-1
- New upstream version 1.3.1.
- This is required for programs using findlib and OCaml 4.00.0.
- Add small patch to fix build of topfind.

* Sat Apr 28 2012 Richard W.M. Jones <rjones@redhat.com> - 1.2.8-1
- New upstream version 1.2.8.

* Fri Jan  6 2012 Richard W.M. Jones <rjones@redhat.com> - 1.2.7-1
- New upstream version 1.2.7.

* Thu Dec  8 2011 Richard W.M. Jones <rjones@redhat.com> - 1.2.6-5
- Don't strip bytecode binary (see RHBZ#435559).

* Fri Jun 3 2011 Orion Poplawski - 1.2.6-3
- Add Requires: ocaml (Bug #710290)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan  5 2011 Richard W.M. Jones <rjones@redhat.com> - 1.2.6-1
- New upstream version 1.2.6.

* Tue Dec 29 2009 Richard W.M. Jones <rjones@redhat.com> - 1.2.5-4
- Rebuild for OCaml 3.11.2.

* Wed Dec 16 2009 Richard W.M. Jones <rjones@redhat.com> - 1.2.5-3
- Use __ocaml_requires_opts / __ocaml_provides_opts.

* Wed Dec 16 2009 Richard W.M. Jones <rjones@redhat.com> - 1.2.5-2
- Update to use RPM dependency generator.

* Sun Oct  4 2009 Richard W.M. Jones <rjones@redhat.com> - 1.2.5-1
- New upstream version 1.2.5.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri May 22 2009 Richard W.M. Jones <rjones@redhat.com> - 1.2.4-3
- Rebuild for OCaml 3.11.1.
- New upstream version 1.2.4.
- camlp4/META patch is now upstream.

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec  4 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.3-5
- Change to camlp4/META means that this package really depends on
  the latest OCaml compiler.

* Thu Dec  4 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.3-4
- camlp4/META: camlp4.lib should depend on dynlink.

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.3-3
- Rebuild for OCaml 3.11.0+rc1.

* Fri Nov 21 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.3-2
- Force rebuild.

* Thu Nov 20 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.3-1
- New upstream version 1.2.3.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.2-2
- Rebuild for OCaml 3.11.0

* Sun Aug 31 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.2-1
- New upstream version 1.2.2.
- Strip ocamlfind binary.
- Remove zero-length file.

* Mon Apr 21 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-3
- New upstream URLs.

* Sat Mar  1 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-2
- Experimental rebuild for ppc64.

* Tue Feb 12 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-1
- New upstream version 1.2.1.

* Thu Sep  6 2007 Richard W.M. Jones <rjones@redhat.com> - 1.1.2pl1-14
- Ignore Parsetree module, it's a part of the toplevel.

* Mon Sep  3 2007 Richard W.M. Jones <rjones@redhat.com> - 1.1.2pl1-13
- Bump version to force rebuild against ocaml -6 release.

* Thu Aug 30 2007 Richard W.M. Jones <rjones@redhat.com> - 1.1.2pl1-12
- Added BR: gawk.

* Thu Aug 30 2007 Richard W.M. Jones <rjones@redhat.com> - 1.1.2pl1-11
- Force rebuild because of changed BRs in base OCaml.

* Thu Aug  2 2007 Richard W.M. Jones <rjones@redhat.com> - 1.1.2pl1-10
- BR added ocaml-ocamldoc so that ocamlfind ocamldoc works.
- Fix path of camlp4 parsers in Makefile.

* Thu Jul 12 2007 Richard W.M. Jones <rjones@redhat.com> - 1.1.2pl1-9
- Added ExcludeArch: ppc64

* Thu Jul 12 2007 Richard W.M. Jones <rjones@redhat.com> - 1.1.2pl1-8
- Expanded tabs to spaces.
- Readded conditional opt section for files.

* Wed Jul 04 2007 Xavier Lamien <lxtnow[at]gmail.com> - 1.1.2pl1-7
- Fixed BR.

* Wed Jun 27 2007 Richard W.M. Jones <rjones@redhat.com> - 1.1.2pl1-6
- Fix configure line.
- Install doc/guide-html.
- Added dependency on ncurses-devel.

* Mon Jun 11 2007 Richard W.M. Jones <rjones@redhat.com> - 1.1.2pl1-5
- Build against 3.10.
- Update to latest package guidelines.

* Sat Jun  2 2007 Richard W.M. Jones <rjones@redhat.com> - 1.1.2pl1-4
- Handle bytecode-only architectures.

* Sat May 26 2007 Richard W.M. Jones <rjones@redhat.com> - 1.1.2pl1-3
- Missing builddep m4.

* Fri May 25 2007 Richard W.M. Jones <rjones@redhat.com> - 1.1.2pl1-2
- Use OCaml find-requires and find-provides.

* Fri May 18 2007 Richard W.M. Jones <rjones@redhat.com> - 1.1.2pl1-1
- Initial RPM release.

