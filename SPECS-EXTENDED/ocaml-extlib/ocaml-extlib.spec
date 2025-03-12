%ifnarch %{ocaml_native_compiler}
%global debug_package %{nil}
%endif

Name:           ocaml-extlib
Version:        1.7.9
Release:        1%{?dist}
Summary:        OCaml ExtLib additions to the standard library
License:        LGPL-2.1-or-later with OCaml-LGPL-linking-exception
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/ygrek/ocaml-extlib
Source0:        https://github.com/ygrek/ocaml-extlib/releases/download/%{version}/extlib-%{version}.tar.gz

BuildRequires:  make
BuildRequires:  ocaml >= 4.02
BuildRequires:  ocaml-findlib-devel >= 1.3.3-3
BuildRequires:  ocaml-ocamldoc
BuildRequires:  ocaml-cppo
BuildRequires:  ocaml-rpm-macros
# In order to apply patches:
BuildRequires:  git-core


%description
ExtLib is a project aiming at providing a complete - yet small -
standard library for the OCaml programming language. The purpose of
this library is to add new functions to OCaml Standard Library
modules, to modify some functions in order to get better performances
or more safety (tail-recursive) but also to provide new modules which
should be useful for the average OCaml programmer.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}


%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.


%prep
%autosetup -S git -n extlib-%{version}

# Remove references to the bytes library for OCaml 5.0
sed -i '/bytes/d' src/META


%build
# https://bugzilla.redhat.com/show_bug.cgi?id=1837823
export minimal=1
%ifarch %{ocaml_native_compiler}
%make_build
%else
%make_build -C src all
%endif


%install
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs

export minimal=1
%make_install
%ocaml_files


%check
export minimal=1
%ifarch %{ocaml_native_compiler}
make test
%else
make -C test all run
%endif


%files -f .ofiles
%doc README.md
%license LICENSE


%files devel -f .ofiles-devel


%changelog
* Fri Dec 20 2024 Durga Jagadeesh Palli <v-dpalli@microsoft.com> - 1.7.9-1
- Update to 1.7.9
- License verified

* Tue Feb 08 2022 Thomas Crain <thcrain@microsoft.com> - 1.7.8-1
- Upgrade to latest upstream version
- Lint spec
- License verified

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.7.5-15
- Switching to using full number for the 'Release' tag.
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Feb 28 2020 Richard W.M. Jones <rjones@redhat.com> - 1.7.5-14.1
- OCaml 4.10.0 final (Fedora 32).

* Wed Feb 26 2020 Richard W.M. Jones <rjones@redhat.com> - 1.7.5-14
- OCaml 4.10.0 final.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.5-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jan 19 2020 Richard W.M. Jones <rjones@redhat.com> - 1.7.5-12
- OCaml 4.10.0+beta1 rebuild.

* Fri Dec 06 2019 Richard W.M. Jones <rjones@redhat.com> - 1.7.5-11
- OCaml 4.09.0 (final) rebuild.

* Fri Aug 16 2019 Richard W.M. Jones <rjones@redhat.com> - 1.7.5-10
- OCaml 4.08.1 (final) rebuild.

* Wed Jul 31 2019 Richard W.M. Jones <rjones@redhat.com> - 1.7.5-9
- OCaml 4.08.1 (rc2) rebuild.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jun 27 2019 Richard W.M. Jones <rjones@redhat.com> - 1.7.5-7
- OCaml 4.08.0 (final) rebuild.

* Mon Apr 29 2019 Richard W.M. Jones <rjones@redhat.com> - 1.7.5-6
- OCaml 4.08.0 (beta 3) rebuild.

* Mon Apr 29 2019 Richard W.M. Jones <rjones@redhat.com> - 1.7.5-5
- Remove BR on camlp4.  Not needed since 1.7.0.

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Richard W.M. Jones <rjones@redhat.com> - 1.7.5-2
- OCaml 4.07.0 (final) rebuild.

* Wed Jul 11 2018 Richard W.M. Jones <rjones@redhat.com> - 1.7.5-1
- New upstream version 1.7.5.
- Remove patches which are all included in this release.

* Wed Jun 20 2018 Richard W.M. Jones <rjones@redhat.com> - 1.7.4-3
- Bump release and rebuild.

* Wed Jun 20 2018 Richard W.M. Jones <rjones@redhat.com> - 1.7.4-2
- Add all upstream patches since 1.7.4, including fixes for OCaml 4.07.
- Use autosetup.
- Remove obsolete old patch.

* Tue Jun 19 2018 Richard W.M. Jones <rjones@redhat.com> - 1.7.4-1
- New upstream version 1.7.4.
- OCaml 4.07.0-rc1 rebuild.

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.7.2-8
- Escape macros in %%changelog

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Nov 07 2017 Richard W.M. Jones <rjones@redhat.com> - 1.7.2-6
- OCaml 4.06.0 rebuild.

* Mon Aug 07 2017 Richard W.M. Jones <rjones@redhat.com> - 1.7.2-5
- OCaml 4.05.0 rebuild.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 26 2017 Richard W.M. Jones <rjones@redhat.com> - 1.7.2-2
- OCaml 4.04.2 rebuild.

* Thu May 11 2017 Richard W.M. Jones <rjones@redhat.com> - 1.7.2-1
- New upstream version 1.7.2 (for OCaml 4.04.1).

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Nov 09 2016 Dan Horák <dan@danny.cz> - 1.7.0-2
- rebuild for s390x codegen bug

* Sat Nov 05 2016 Richard W.M. Jones <rjones@redhat.com> - 1.7.0-1
- New upstream version 1.7.0.
- Fix upstream URL and Source0.
- Rationalize the build.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jul 28 2015 Richard W.M. Jones <rjones@redhat.com> - 1.6.1-12
- OCaml 4.02.3 rebuild.

* Mon Jul 27 2015 Richard W.M. Jones <rjones@redhat.com> - 1.6.1-11
- Remove ExcludeArch since bytecode build should now work.

* Wed Jun 24 2015 Richard W.M. Jones <rjones@redhat.com> - 1.6.1-10
- Bump release and rebuild.

* Wed Jun 17 2015 Richard W.M. Jones <rjones@redhat.com> - 1.6.1-9
- ocaml-4.02.2 rebuild.

* Mon Feb 16 2015 Richard W.M. Jones <rjones@redhat.com> - 1.6.1-8
- ocaml-4.02.1 rebuild.

* Sat Aug 30 2014 Richard W.M. Jones <rjones@redhat.com> - 1.6.1-7
- ocaml-4.02.0 final rebuild.

* Sat Aug 23 2014 Richard W.M. Jones <rjones@redhat.com> - 1.6.1-6
- ocaml-4.02.0+rc1 rebuild.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 01 2014 Richard W.M. Jones <rjones@redhat.com> - 1.6.1-4
- ocaml-4.02.0-0.8.git10e45753.fc22 build.

* Mon Jul 21 2014 Richard W.M. Jones <rjones@redhat.com> - 1.6.1-3
- Bump release and rebuild.

* Thu Jul 17 2014 Richard W.M. Jones <rjones@redhat.com> - 1.6.1-2
- New upstream version 1.6.1.
- Rebuild for OCaml 4.02.0 beta.
- Remove enable debug patch which is now upstream.
- New version requires camlp4.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Sep 14 2013 Richard W.M. Jones <rjones@redhat.com> - 1.5.4-1
- New upstream version 1.5.4.
- Rebuild against OCaml 4.01.0.
- Enable debuginfo.
  Does not work yet because the dumbass build system removed object files.
- Small modernizations of the specfile.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 27 2012 Richard W.M. Jones <rjones@redhat.com> - 1.5.3-2
- BR >= OCaml 4.00.1 so we can't be built against the wrong OCaml.

* Mon Oct 29 2012 Richard W.M. Jones <rjones@redhat.com> - 1.5.3-1
- New upstream version 1.5.3.
- Remove patch, now upstream.
- Clean up the spec file.
- Rebuild for OCaml 4.00.1.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 10 2012 Richard W.M. Jones <rjones@redhat.com> - 1.5.2-3
- Rebuild for OCaml 4.00.0.

* Thu Jun  7 2012 Richard W.M. Jones <rjones@redhat.com> - 1.5.2-2
- Fix for OCaml 4.00.0.

* Fri Jan  6 2012 Richard W.M. Jones <rjones@redhat.com> - 1.5.2-1
- New upstream version 1.5.2.

* Wed Jan  5 2011 Richard W.M. Jones <rjones@redhat.com> - 1.5.1-10
- Rebuild for OCaml 3.12.0.

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 1.5.1-9
- Rebuild for OCaml 3.11.2.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 1.5.1-7
- Rebuild for OCaml 3.11.1

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 1.5.1-5
- Rebuild for OCaml 3.11.0+rc1.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 1.5.1-4
- Rebuild for OCaml 3.11.0

* Wed Apr 23 2008 Richard W.M. Jones <rjones@redhat.com> - 1.5.1-3
- Rebuild for OCaml 3.10.2

* Sat Mar  1 2008 Richard W.M. Jones <rjones@redhat.com> - 1.5.1-2
- License is LGPLv2+ with exceptions.
- Rebuild for ppc64.

* Tue Feb 12 2008 Richard W.M. Jones <rjones@redhat.com> - 1.5.1-1
- New upstream version 1.5.1.
- New home page.
- Rebuild for OCaml 3.10.1.

* Thu Sep  6 2007 Richard W.M. Jones <rjones@redhat.com> - 1.5-8
- Force rebuild because of updated requires/provides scripts in OCaml.

* Mon Sep  3 2007 Richard W.M. Jones <rjones@redhat.com> - 1.5-7
- Force rebuild because of base OCaml.

* Thu Aug 30 2007 Richard W.M. Jones <rjones@redhat.com> - 1.5-6
- Force rebuild because of changed BRs in base OCaml.

* Wed Aug  1 2007 Richard W.M. Jones <rjones@redhat.com> - 1.5-5
- ExcludeArch ppc64
- Added BR on ocaml-ocamldoc
- Use %%doc to install documentation.

* Mon Jun 11 2007 Richard W.M. Jones <rjones@redhat.com> - 1.5-4
- Updated to latest packaging guidelines.

* Sat Jun  2 2007 Richard W.M. Jones <rjones@redhat.com> - 1.5-3
- Support for bytecode-only architectures.
- *.cmx files are needed.

* Fri May 25 2007 Richard W.M. Jones <rjones@redhat.com> - 1.5-2
- Use OCaml find-requires and find-provides.

* Fri May 18 2007 Richard W.M. Jones <rjones@redhat.com> - 1.5-1
- Initial RPM release.

