# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# OCaml packages not built on i686 since OCaml 5 / Fedora 39.
ExcludeArch: %{ix86}

%ifnarch %{ocaml_native_compiler}
%global debug_package %{nil}
%endif

%global giturl  https://github.com/gildor478/ocaml-fileutils

Name:           ocaml-fileutils
Version:        0.6.6
Release:        4%{?dist}
Summary:        OCaml library for common file and filename operations

License:        LGPL-2.1-or-later WITH OCaml-LGPL-linking-exception
URL:            https://gildor478.github.io/ocaml-fileutils/
VCS:            git:%{giturl}.git
Source0:        %{giturl}/releases/download/v%{version}/fileutils-%{version}.tbz

BuildRequires:  ocaml >= 4.14
BuildRequires:  ocaml-dune >= 2.9
%if 0%{?fedora}
BuildRequires:  ocaml-ounit-devel >= 2.0.0
%endif


%description
This library is intended to provide a basic interface to the most
common file and filename operations.  It provides several different
filename functions: reduce, make_absolute, make_relative...  It also
enables you to manipulate real files: cp, mv, rm, touch...

It is separated into two modules: SysUtil and SysPath.  The first one
manipulates real files, the second one is made for manipulating
abstract filenames.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}


%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.


%prep
%autosetup -n fileutils-%{version} -p1


%build
%dune_build


%install
%dune_install


# Do not run the tests (RHEL 7+ only) since they require ocaml-ounit.
%if 0%{?fedora} || 0%{?rhel} <= 6
%check
%dune_check
%endif


%files -f .ofiles
%license LICENSE.txt


%files devel -f .ofiles-devel
%doc README.md CHANGES.md
%license LICENSE.txt


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jul 12 2025 Jerry James  <loganjerry@gmail.com> - 0.6.6-3
- Rebuild to fix OCaml dependencies

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jan  9 2025 Jerry James <loganjerry@gmail.com> - 0.6.6-1
- OCaml 5.3.0 rebuild for Fedora 42
- Version 0.6.6
- All patches have been upstreamed

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 19 2024 Richard W.M. Jones <rjones@redhat.com> - 0.6.4-10
- OCaml 5.2.0 ppc64le fix

* Wed May 29 2024 Richard W.M. Jones <rjones@redhat.com> - 0.6.4-9
- OCaml 5.2.0 for Fedora 41

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 18 2023 Richard W.M. Jones <rjones@redhat.com> - 0.6.4-6
- OCaml 5.1.1 + s390x code gen fix for Fedora 40

* Tue Dec 12 2023 Richard W.M. Jones <rjones@redhat.com> - 0.6.4-5
- OCaml 5.1.1 rebuild for Fedora 40

* Thu Oct 05 2023 Richard W.M. Jones <rjones@redhat.com> - 0.6.4-4
- OCaml 5.1 rebuild for Fedora 40

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Richard W.M. Jones <rjones@redhat.com> - 0.6.4-2
- OCaml 5.0 rebuild for Fedora 39

* Mon Jul 10 2023 Jerry James <loganjerry@gmail.com> - 0.6.4-1
- Version 0.6.4
- New project URLs
- Convert License tag to SPDX
- Drop upstreamed bytes and ounit2 patches
- Build with dune

* Tue Jan 24 2023 Richard W.M. Jones <rjones@redhat.com> - 0.5.2-36
- Bump release and rebuild

* Tue Jan 24 2023 Richard W.M. Jones <rjones@redhat.com> - 0.5.2-35
- Rebuild OCaml packages for F38

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.2-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.2-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun Jun 19 2022 Richard W.M. Jones <rjones@redhat.com> - 0.5.2-32
- OCaml 4.14.0 rebuild

* Fri Feb 04 2022 Richard W.M. Jones <rjones@redhat.com> - 0.5.2-31
- OCaml 4.13.1 rebuild to remove package notes

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.2-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Oct 05 2021 Richard W.M. Jones <rjones@redhat.com> - 0.5.2-29
- OCaml 4.13.1 build

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.2-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Mar 30 2021 Richard W.M. Jones <rjones@redhat.com> - 0.5.2-27
- Bump and rebuild for ELN.

* Mon Mar  1 21:31:03 GMT 2021 Richard W.M. Jones <rjones@redhat.com> - 0.5.2-26
- OCaml 4.12.0 build

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.2-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Sep 01 2020 Richard W.M. Jones <rjones@redhat.com> - 0.5.2-24
- OCaml 4.11.1 rebuild

* Fri Aug 21 2020 Richard W.M. Jones <rjones@redhat.com> - 0.5.2-23
- OCaml 4.11.0 rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.2-22
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.2-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 05 2020 Richard W.M. Jones <rjones@redhat.com> - 0.5.2-20
- Bump and rebuild for s390x.

* Tue May 05 2020 Richard W.M. Jones <rjones@redhat.com> - 0.5.2-19
- OCaml 4.11.0+dev2-2020-04-22 rebuild

* Tue Apr 21 2020 Richard W.M. Jones <rjones@redhat.com> - 0.5.2-18
- OCaml 4.11.0 pre-release attempt 2

* Sat Apr 04 2020 Richard W.M. Jones <rjones@redhat.com> - 0.5.2-17
- Update all OCaml dependencies for RPM 4.16.

* Wed Feb 26 2020 Richard W.M. Jones <rjones@redhat.com> - 0.5.2-16
- OCaml 4.10.0 final.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.2-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jan 19 2020 Richard W.M. Jones <rjones@redhat.com> - 0.5.2-14
- OCaml 4.10.0+beta1 rebuild.

* Thu Jan 09 2020 Richard W.M. Jones <rjones@redhat.com> - 0.5.2-13
- OCaml 4.09.0 for riscv64

* Fri Dec 06 2019 Richard W.M. Jones <rjones@redhat.com> - 0.5.2-12
- OCaml 4.09.0 (final) rebuild.

* Fri Aug 16 2019 Richard W.M. Jones <rjones@redhat.com> - 0.5.2-11
- OCaml 4.08.1 (final) rebuild.

* Wed Jul 31 2019 Richard W.M. Jones <rjones@redhat.com> - 0.5.2-10
- OCaml 4.08.1 (rc2) rebuild.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jun 27 2019 Richard W.M. Jones <rjones@redhat.com> - 0.5.2-8
- OCaml 4.08.0 (final) rebuild.

* Mon Apr 29 2019 Richard W.M. Jones <rjones@redhat.com> - 0.5.2-7
- OCaml 4.08.0 (beta 3) rebuild.

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Richard W.M. Jones <rjones@redhat.com> - 0.5.2-4
- OCaml 4.07.0 (final) rebuild.

* Wed Jun 20 2018 Richard W.M. Jones <rjones@redhat.com> - 0.5.2-3
- OCaml 4.07.0-rc1 rebuild.

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Nov 08 2017 Richard W.M. Jones <rjones@redhat.com> - 0.5.2-1
- New upstream version 0.5.2.
- OCaml 4.06.0 rebuild.

* Mon Aug 07 2017 Richard W.M. Jones <rjones@redhat.com> - 0.5.1-8
- OCaml 4.05.0 rebuild.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 26 2017 Richard W.M. Jones <rjones@redhat.com> - 0.5.1-5
- OCaml 4.04.2 rebuild.

* Fri May 12 2017 Richard W.M. Jones <rjones@redhat.com> - 0.5.1-4
- OCaml 4.04.1 rebuild.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Nov 09 2016 Dan Horák <dan@danny.cz> - 0.5.1-2
- rebuild for s390x codegen bug

* Fri Nov 04 2016 Richard W.M. Jones <rjones@redhat.com> - 0.5.1-1
- New upstream version 0.5.1.
- Add explicit dependency on ocamlbuild.

* Mon Sep 12 2016 Dan Horák <dan[at]danny.cz> - 0.4.5-17
- disable debuginfo subpackage on interpreted builds

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.5-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jul 28 2015 Richard W.M. Jones <rjones@redhat.com> - 0.4.5-15
- OCaml 4.02.3 rebuild.

* Mon Jul 27 2015 Richard W.M. Jones <rjones@redhat.com> - 0.4.5-14
- Remove ExcludeArch since bytecode build should now work.

* Tue Jun 23 2015 Richard W.M. Jones <rjones@redhat.com> - 0.4.5-13
- Bump release and rebuild.

* Wed Jun 17 2015 Richard W.M. Jones <rjones@redhat.com> - 0.4.5-12
- ocaml-4.02.2 rebuild.

* Mon Feb 16 2015 Richard W.M. Jones <rjones@redhat.com> - 0.4.5-11
- ocaml-4.02.1 rebuild.

* Sat Aug 30 2014 Richard W.M. Jones <rjones@redhat.com> - 0.4.5-10
- ocaml-4.02.0 final rebuild.

* Sat Aug 23 2014 Richard W.M. Jones <rjones@redhat.com> - 0.4.5-9
- ocaml-4.02.0+rc1 rebuild.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Aug 02 2014 Richard W.M. Jones <rjones@redhat.com> - 0.4.5-7
- ocaml-4.02.0-0.8.git10e45753.fc22 rebuild.

* Mon Jul 21 2014 Richard W.M. Jones <rjones@redhat.com> - 0.4.5-6
- OCaml 4.02.0 beta rebuild.

* Mon Jul 14 2014 Richard W.M. Jones <rjones@redhat.com> - 0.4.5-5
- Rebuild for OCaml 4.02.0.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Sep 14 2013 Richard W.M. Jones <rjones@redhat.com> - 0.4.5-1
- New upstream version 0.4.5.
- Enable debuginfo.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 27 2012 Richard W.M. Jones <rjones@redhat.com> - 0.4.4-4
- BR >= OCaml 4.00.1 so we can't be built against the wrong OCaml.

* Tue Nov 27 2012 Richard W.M. Jones <rjones@redhat.com> - 0.4.4-3
- Disable the tests on RHEL 7, since they require ocaml-ounit.

* Fri Oct 19 2012 Richard W.M. Jones <rjones@redhat.com> - 0.4.4-2
- New upstream version 0.4.4.
- Clean up the spec file.
- Fix homepage and download URLs.
- Don't use configure macro.  Upstream are using some sort of non-autoconf
  brokenness.
- Rename text files as *.txt.  There is no 'api' directory any more.

* Sat Jul 28 2012 Richard W.M. Jones <rjones@redhat.com> - 0.4.0-10
- Bump and rebuild against new OCaml 4.00.0 official release.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 09 2012 Richard W.M. Jones <rjones@redhat.com> - 0.4.0-8
- Rebuild for OCaml 4.00.0.

* Mon May 14 2012 Richard W.M. Jones <rjones@redhat.com> - 0.4.0-7
- Bump release and rebuild for new OCaml on ARM.

* Fri Jan 06 2012 Richard W.M. Jones <rjones@redhat.com> - 0.4.0-6
- Rebuild for OCaml 3.12.1.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 05 2011 Richard W.M. Jones <rjones@redhat.com> - 0.4.0-4
- Rebuild for OCaml 3.12 (http://fedoraproject.org/wiki/Features/OCaml3.12).

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 0.4.0-3
- Rebuild for OCaml 3.11.2.

* Thu Oct  8 2009 Richard W.M. Jones <rjones@redhat.com> - 0.4.0-2
- New upstream version 0.4.0.
- Upstream build system has been rationalized, so remove all the
  hacks we were using.
- Upstream now contains tests, run them.
- Needs ounit in order to carry out the tests.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 0.3.0-10
- Rebuild for OCaml 3.11.1

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 0.3.0-8
- Rebuild for OCaml 3.11.0+rc1.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 0.3.0-7
- Rebuild for OCaml 3.11.0

* Wed Apr 23 2008 Richard W.M. Jones <rjones@redhat.com> - 0.3.0-5
- Rebuild for OCaml 3.10.2

* Sat Mar  1 2008 Richard W.M. Jones <rjones@redhat.com> - 0.3.0-4
- Rebuild for ppc64.

* Thu Feb 21 2008 Richard W.M. Jones <rjones@redhat.com> - 0.3.0-3
- Fixed grammar in the description section.
- License is LGPLv2 with exceptions
- Include license file with both RPMs.
- Include other documentation only in the -devel RPM.

* Tue Feb 12 2008 Richard W.M. Jones <rjones@redhat.com> - 0.3.0-2
- Added BR ocaml-camlp4-devel.
- Build into tmp directory under the build root.

* Wed Aug  8 2007 Richard W.M. Jones <rjones@redhat.com> - 0.3.0-1
- Initial RPM release.
