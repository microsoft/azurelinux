Summary:        OCaml library for common file and filename operations
Name:           ocaml-fileutils
Version:        0.6.4
Release:        1%{?dist}
License:        LGPLv2 WITH exceptions
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/gildor478/ocaml-fileutils
# NOTE: the "_2" suffix was added to avoid conflicts with an older source tarball for the same version of the sources.
#       Please remove it during a version update.
Source0:        %{url}/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Fedora does not need the stdlib-shims or seq forward compatibility packages
Patch0:         ocaml-fileutils-0.6.4-forward-compat.patch
# Given two distinct files with identical contents, the cmp function evaluates
# to "Some x", where x is the size of each file, instead of None.  This breaks
# the ocaml-gettext tests, which expect None in that case.
Patch1:         ocaml-fileutils-0.6.4-cmp.patch

BuildRequires:  ocaml >= 5.1.1
BuildRequires:  ocaml-dune >= 1.11.0
%if 0%{?fedora} || 0%{?rhel} <= 6
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
%autosetup -n %{name}-%{version} -p1

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
* Tue May 07 2024 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 0.6.4-1
- Upgrade to 0.6.4
- Use ocaml 5.1.1 to build

* Thu Mar 31 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.5.2-18
- Cleaning-up spec. License verified.

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.5.2-17
- Switching to using full number for the 'Release' tag.
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Feb 28 2020 Richard W.M. Jones <rjones@redhat.com> - 0.5.2-16.1
- OCaml 4.10.0 final (Fedora 32).

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
