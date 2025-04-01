
%ifnarch %{ocaml_native_compiler}
%global debug_package %{nil}
%endif

%global forgeurl https://github.com/ncannasse/xml-light
Version: 2.5
%forgemeta

Name:           ocaml-xml-light
Release:        13%{?dist}
Summary:        Minimal XML parser and printer for OCaml

License:        LGPL-2.1-or-later WITH OCaml-LGPL-linking-exception
URL:            http://tech.motion-twin.com/xmllight.html
Source0:        https://github.com/ncannasse/xml-light/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  ocaml >= 4.03
BuildRequires:  ocaml-dune >= 2.7


%description
Xml-Light is a minimal XML parser & printer for OCaml. It provides
functions to parse an XML document into an OCaml data structure, work
with it, and print it back to an XML document. It also supports DTD
parsing and checking, and is entirely written in OCaml; hence it does
not require a C library.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}


%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.


%prep
%forgesetup


%build
%dune_build


%check
%dune_check


%install
%dune_install -s


%files -f .ofiles-xml-light
%license LICENSE


%files devel -f .ofiles-xml-light-devel
%doc README.md
%license LICENSE


%changelog
* Mon Mar 17 2025 Durga Jagadeesh Palli <v-dpalli@microsoft.com> - 2.5-13
- Initial Azure Linux import from Fedora 41 (license: MIT)
- License verified

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.5-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 19 2024 Richard W.M. Jones <rjones@redhat.com> - 2.5-11
- OCaml 5.2.0 ppc64le fix

* Wed May 29 2024 Richard W.M. Jones <rjones@redhat.com> - 2.5-10
- OCaml 5.2.0 for Fedora 41

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 18 2023 Richard W.M. Jones <rjones@redhat.com> - 2.5-7
- OCaml 5.1.1 + s390x code gen fix for Fedora 40

* Tue Dec 12 2023 Richard W.M. Jones <rjones@redhat.com> - 2.5-6
- OCaml 5.1.1 rebuild for Fedora 40

* Thu Oct 05 2023 Richard W.M. Jones <rjones@redhat.com> - 2.5-5
- OCaml 5.1 rebuild for Fedora 40

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Richard W.M. Jones <rjones@redhat.com> - 2.5-3
- OCaml 5.0 rebuild for Fedora 39

* Mon Jul 10 2023 Jerry James <loganjerry@gmail.com> - 2.5-2
- OCaml 5.0.0 rebuild
- Convert License tag to SPDX
- Trim BuildRequires

* Wed Feb 22 2023 Richard W.M. Jones <rjones@redhat.com> - 2.5-1
- New upstream version 2.5
- Use forge macros.
- Use dune for building.
- Rename README.
- Include LICENSE file.

* Tue Jan 24 2023 Richard W.M. Jones <rjones@redhat.com> - 2.4-8
- Bump release and rebuild.

* Tue Jan 24 2023 Richard W.M. Jones <rjones@redhat.com> - 2.4-7
- Rebuild OCaml packages for F38

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jun 18 2022 Richard W.M. Jones <rjones@redhat.com> - 2.4-4
- OCaml 4.14.0 rebuild

* Fri Feb 04 2022 Richard W.M. Jones <rjones@redhat.com> - 2.4-3
- OCaml 4.13.1 rebuild to remove package notes

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Dec 27 2021 Jerry James <loganjerry@gmail.com> - 2.4-1
- Version 2.4
- New upstream URL
- Clarify that license includes the OCaml exception
- Add patch to fix parsing of hex entities

* Mon Oct 04 2021 Richard W.M. Jones <rjones@redhat.com> - 2.3-0.56.svn234
- Bump release and rebuild.

* Mon Oct 04 2021 Richard W.M. Jones <rjones@redhat.com> - 2.3-0.55.svn234
- OCaml 4.13.1 build

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-0.54.svn234
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Mar  1 13:12:07 GMT 2021 Richard W.M. Jones <rjones@redhat.com> - 2.3-0.53.svn234
- OCaml 4.12.0 build

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-0.52.svn234
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Sep 01 2020 Richard W.M. Jones <rjones@redhat.com> - 2.3-0.51.svn234
- OCaml 4.11.1 rebuild

* Fri Aug 21 2020 Richard W.M. Jones <rjones@redhat.com> - 2.3-0.50.svn234
- Bump release and rebuild.

* Fri Aug 21 2020 Richard W.M. Jones <rjones@redhat.com> - 2.3-0.49.svn234
- OCaml 4.11.0 rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-0.48.svn234
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon May 04 2020 Richard W.M. Jones <rjones@redhat.com> - 2.3-0.47.svn234
- OCaml 4.11.0+dev2-2020-04-22 rebuild

* Tue Apr 21 2020 Richard W.M. Jones <rjones@redhat.com> - 2.3-0.46.svn234
- OCaml 4.11.0 pre-release attempt 2

* Fri Apr 17 2020 Richard W.M. Jones <rjones@redhat.com> - 2.3-0.45.svn234
- OCaml 4.11.0 pre-release

* Thu Apr 02 2020 Richard W.M. Jones <rjones@redhat.com> - 2.3-0.44.svn234
- Update all OCaml dependencies for RPM 4.16.

* Wed Feb 26 2020 Richard W.M. Jones <rjones@redhat.com> - 2.3-0.43.svn234
- OCaml 4.10.0 final.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-0.42.svn234
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jan 19 2020 Richard W.M. Jones <rjones@redhat.com> - 2.3-0.41.svn234
- Bump release and rebuild.

* Sun Jan 19 2020 Richard W.M. Jones <rjones@redhat.com> - 2.3-0.40.svn234
- OCaml 4.10.0+beta1 rebuild.

* Thu Jan 09 2020 Richard W.M. Jones <rjones@redhat.com> - 2.3-0.39.svn234
- OCaml 4.09.0 for riscv64

* Fri Dec 06 2019 Richard W.M. Jones <rjones@redhat.com> - 2.3-0.38.svn234
- OCaml 4.09.0 (final) rebuild.

* Fri Aug 16 2019 Richard W.M. Jones <rjones@redhat.com> - 2.3-0.37.svn234
- OCaml 4.08.1 (final) rebuild.

* Wed Jul 31 2019 Richard W.M. Jones <rjones@redhat.com> - 2.3-0.36.svn234
- OCaml 4.08.1 (rc2) rebuild.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-0.35.svn234
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jun 27 2019 Richard W.M. Jones <rjones@redhat.com> - 2.3-0.34.svn234
- OCaml 4.08.0 (final) rebuild.

* Mon Apr 29 2019 Richard W.M. Jones <rjones@redhat.com> - 2.3-0.33.svn234
- OCaml 4.08.0 (beta 3) rebuild.

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-0.32.svn234
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-0.31.svn234
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Richard W.M. Jones <rjones@redhat.com> - 2.3-0.30.svn234
- OCaml 4.07.0 (final) rebuild.

* Tue Jun 19 2018 Richard W.M. Jones <rjones@redhat.com> - 2.3-0.29.svn234
- OCaml 4.07.0-rc1 rebuild.

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-0.28.svn234
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Nov 07 2017 Richard W.M. Jones <rjones@redhat.com> - 2.3-0.27.svn234
- OCaml 4.06.0 rebuild.

* Mon Aug 07 2017 Richard W.M. Jones <rjones@redhat.com> - 2.3-0.26.svn234
- OCaml 4.05.0 rebuild.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-0.25.svn234
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-0.24.svn234
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 26 2017 Richard W.M. Jones <rjones@redhat.com> - 2.3-0.23.svn234
- OCaml 4.04.2 rebuild.

* Fri May 12 2017 Richard W.M. Jones <rjones@redhat.com> - 2.3-0.22.svn234
- Bump release and rebuild.

* Thu May 11 2017 Richard W.M. Jones <rjones@redhat.com> - 2.3-0.21.svn234
- OCaml 4.04.1 rebuild.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-0.20.svn234
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Nov 05 2016 Richard W.M. Jones <rjones@redhat.com> - 2.3-0.19.svn234
- Rebuild for OCaml 4.04.0.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-0.18.svn234
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jul 28 2015 Richard W.M. Jones <rjones@redhat.com> - 2.3-0.17.svn234
- OCaml 4.02.3 rebuild.

* Wed Jul 22 2015 Richard W.M. Jones <rjones@redhat.com> - 2.3-0.16.svn234
- Enable bytecode builds.

* Wed Jun 24 2015 Richard W.M. Jones <rjones@redhat.com> - 2.3-0.15.svn234
- ocaml-4.02.2 final rebuild.

* Wed Jun 17 2015 Richard W.M. Jones <rjones@redhat.com> - 2.3-0.14.svn234
- ocaml-4.02.2 rebuild.

* Mon Feb 16 2015 Richard W.M. Jones <rjones@redhat.com> - 2.3-0.13.svn234
- ocaml-4.02.1 rebuild.

* Sat Aug 30 2014 Richard W.M. Jones <rjones@redhat.com> - 2.3-0.12.svn234
- ocaml-4.02.0 final rebuild.

* Sat Aug 23 2014 Richard W.M. Jones <rjones@redhat.com> - 2.3-0.11.svn234
- ocaml-4.02.0+rc1 rebuild.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-0.10.svn234
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Aug 02 2014 Richard W.M. Jones <rjones@redhat.com> - 2.3-0.9.svn234
- ocaml-4.02.0-0.8.git10e45753.fc22 rebuild.

* Mon Jul 21 2014 Richard W.M. Jones <rjones@redhat.com> - 2.3-0.8.svn234
- OCaml 4.02.0 beta rebuild.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-0.7.svn234
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Sep 19 2013 Richard W.M. Jones <rjones@redhat.com> - 2.3-0.6.svn234
- OCaml 4.01.0 rebuild.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-0.5.svn234
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-0.4.svn234
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 27 2012 Richard W.M. Jones <rjones@redhat.com> - 2.3-0.3.svn234
- BR >= OCaml 4.00.1 so we can't be built against the wrong OCaml.

* Tue Oct 30 2012 Richard W.M. Jones <rjones@redhat.com> - 2.3-0.2.svn234
- Rebuild for OCaml 4.00.1.

* Tue Aug 21 2012 Richard W.M. Jones <rjones@redhat.com> - 2.3-0.1.svn234
- Update to latest version (subversion release 234).
- Includes fix for CVE-2012-3514 - moderate impact hash table collisions
  (resolves: rhbz#787890).
- Clean up the spec file and bring up to modern standards.
- Add tests.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.cvs20070817-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 10 2012 Richard W.M. Jones <rjones@redhat.com> - 2.2.cvs20070817-18
- Rebuild for OCaml 4.00.0.

* Fri Jan 06 2012 Richard W.M. Jones <rjones@redhat.com> - 2.2.cvs20070817-17
- Rebuild for OCaml 3.12.1.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.cvs20070817-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 06 2011 Richard W.M. Jones <rjones@redhat.com> - 2.2.cvs20070817-15
- Rebuild for OCaml 3.12 (http://fedoraproject.org/wiki/Features/OCaml3.12).

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 2.2.cvs20070817-14
- Rebuild for OCaml 3.11.2.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.cvs20070817-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 2.2.cvs20070817-12
- Rebuild for OCaml 3.11.1

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.cvs20070817-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 2.2.cvs20070817-10
- Rebuild for OCaml 3.11.0+rc1.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 2.2.cvs20070817-9
- Rebuild for OCaml 3.11.0

* Wed Apr 23 2008 Richard W.M. Jones <rjones@redhat.com> - 2.2.cvs20070817-8
- Rebuild for OCaml 3.10.2

* Sat Mar  1 2008 Richard W.M. Jones <rjones@redhat.com> - 2.2.cvs20070817-7
- Rebuild for ppc64.

* Tue Feb 12 2008 Richard W.M. Jones <rjones@redhat.com> - 2.2.cvs20070817-6
- Rebuild for OCaml 3.10.1

* Thu Sep  6 2007 Richard W.M. Jones <rjones@redhat.com> - 2.2.cvs20070817-5
- Don't package test.cmi file (it's a test program).

* Thu Sep  6 2007 Richard W.M. Jones <rjones@redhat.com> - 2.2.cvs20070817-4
- Force rebuild because of updated requires/provides scripts in OCaml.

* Thu Aug 30 2007 Richard W.M. Jones <rjones@redhat.com> - 2.2.cvs20070817-3
- Force rebuild because of changed BRs in base OCaml.

* Fri Aug 24 2007 Richard W.M. Jones <rjones@redhat.com> - 2.2.cvs20070817-2
- Clarified that the license is LGPLv2+.

* Fri Aug 17 2007 Richard W.M. Jones <rjones@redhat.com> - 2.2.cvs20070817-1
- Initial RPM release.
