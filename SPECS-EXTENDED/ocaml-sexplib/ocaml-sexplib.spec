Vendor:         Microsoft Corporation
Distribution:   Mariner
%ifnarch %{ocaml_native_compiler}
%global debug_package %{nil}
%endif

%bcond_with vim

%global srcname sexplib

Name:           ocaml-%{srcname}
Version:        0.15.0
Release:        1%{?dist}
Summary:        Automated S-expression conversion

# The project as a whole is MIT, but code in the src subdirectory is BSD.
License:        MIT and BSD
URL:            https://github.com/janestreet/%{srcname}
Source0:        %{url}/archive/v%{version}/%{srcname}-%{version}.tar.gz

BuildRequires:  ocaml >= 4.04.2
BuildRequires:  ocaml-dune >= 2.0.0
BuildRequires:  ocaml-findlib
BuildRequires:  ocaml-num-devel
BuildRequires:  ocaml-parsexp-devel
BuildRequires:  ocaml-sexplib0-devel
%if %{with vim}
BuildRequires:  vim-filesystem
%endif

%description
This package contains a library for serializing OCaml values to and from
S-expressions.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ocaml-num-devel%{?_isa}
Requires:       ocaml-parsexp-devel%{?_isa}

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%if %{with vim}
%package        vim
Summary:        Support for sexplib syntax in vim
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       vim-filesystem

%description    vim
This package contains a vim syntax file for Sexplib.
%endif

%prep
%autosetup -n %{srcname}-%{version}

%build
dune build %{?_smp_mflags}

%install
dune install --destdir=%{buildroot}

%if %{with vim}
# Install the vim support
mkdir -p %{buildroot}%{vimfiles_root}/syntax
cp -p vim/syntax/sexplib.vim %{buildroot}%{vimfiles_root}/syntax
%endif

# We install the documentation with the doc macro
rm -fr %{buildroot}%{_prefix}/doc

%ifarch %{ocaml_native_compiler}
# Add missing executable bits
find %{buildroot}%{_libdir}/ocaml -name \*.cmxs -exec chmod 0755 {} \+
%endif

%files
%doc CHANGES.md README.org
%license COPYRIGHT.txt LICENSE.md LICENSE-Tywith.txt THIRD-PARTY.txt
%dir %{_libdir}/ocaml/%{srcname}/
%dir %{_libdir}/ocaml/%{srcname}/num/
%dir %{_libdir}/ocaml/%{srcname}/unix/
%{_libdir}/ocaml/%{srcname}/META
%{_libdir}/ocaml/%{srcname}/%{srcname}*.cma
%{_libdir}/ocaml/%{srcname}/%{srcname}*.cmi
%{_libdir}/ocaml/%{srcname}/num/*.cma
%{_libdir}/ocaml/%{srcname}/num/*.cmi
%{_libdir}/ocaml/%{srcname}/unix/*.cma
%{_libdir}/ocaml/%{srcname}/unix/*.cmi
%ifarch %{ocaml_native_compiler}
%{_libdir}/ocaml/%{srcname}/%{srcname}*.cmxs
%{_libdir}/ocaml/%{srcname}/num/*.cmxs
%{_libdir}/ocaml/%{srcname}/unix/*.cmxs
%endif

%files devel
%{_libdir}/ocaml/%{srcname}/dune-package
%{_libdir}/ocaml/%{srcname}/opam
%ifarch %{ocaml_native_compiler}
%{_libdir}/ocaml/%{srcname}/%{srcname}*.a
%{_libdir}/ocaml/%{srcname}/%{srcname}*.cmx
%{_libdir}/ocaml/%{srcname}/%{srcname}*.cmxa
%{_libdir}/ocaml/%{srcname}/num/*.a
%{_libdir}/ocaml/%{srcname}/num/*.cmx
%{_libdir}/ocaml/%{srcname}/num/*.cmxa
%{_libdir}/ocaml/%{srcname}/unix/*.a
%{_libdir}/ocaml/%{srcname}/unix/*.cmx
%{_libdir}/ocaml/%{srcname}/unix/*.cmxa
%endif
%{_libdir}/ocaml/%{srcname}/%{srcname}*.cmt
%{_libdir}/ocaml/%{srcname}/%{srcname}*.cmti
%{_libdir}/ocaml/%{srcname}/*.ml
%{_libdir}/ocaml/%{srcname}/*.mli
%{_libdir}/ocaml/%{srcname}/num/*.cmt
%{_libdir}/ocaml/%{srcname}/num/*.cmti
%{_libdir}/ocaml/%{srcname}/num/*.ml
%{_libdir}/ocaml/%{srcname}/num/*.mli
%{_libdir}/ocaml/%{srcname}/unix/*.cmt
%{_libdir}/ocaml/%{srcname}/unix/*.ml

%if %{with vim}
%files vim
%{vimfiles_root}/syntax/sexplib.vim
%endif

%changelog
* Tue Jan 18 2022 Olivia Crain <oliviacrain@microsoft.com> - 0.15.0-1
- Upgrade to latest version
- License verified

* Thu Dec  2 2021 Muhammad Falak <mwani@microsoft.com> - 0.14.0-7
- Remove epoch.

* Mon Aug 09 2021 Olivia Crain <oliviacrain@microsoft.com> - 1:0.14.0-6
- Initial CBL-Mariner import from Fedora 34 (license: MIT).
- Diable vim subpackage by default

* Tue Feb  2 2021 Richard W.M. Jones <rjones@redhat.com> - 1:0.14.0-5
- Bump and rebuild for updated ocaml-camomile dep (RHBZ#1923853).

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.14.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Sep 01 2020 Richard W.M. Jones <rjones@redhat.com> - 1:0.14.0-3
- OCaml 4.11.1 rebuild

* Fri Aug 21 2020 Richard W.M. Jones <rjones@redhat.com> - 1:0.14.0-2
- OCaml 4.11.0 rebuild

* Tue Aug  4 2020 Jerry James <loganjerry@gmail.com> - 1:0.14.0-1
- Version 0.14.0

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.13.0-12
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.13.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul 23 2020 Richard W.M. Jones <rjones@redhat.com> - 1:0.13.0-10
- Rebuild to resolve build order symbol problems.

* Tue May 05 2020 Richard W.M. Jones <rjones@redhat.com> - 1:0.13.0-9
- OCaml 4.11.0+dev2-2020-04-22 rebuild

* Tue Apr 21 2020 Richard W.M. Jones <rjones@redhat.com> - 1:0.13.0-8
- OCaml 4.11.0 pre-release attempt 2

* Fri Apr 03 2020 Richard W.M. Jones <rjones@redhat.com> - 1:0.13.0-7
- Update all OCaml dependencies for RPM 4.16.

* Wed Feb 26 2020 Richard W.M. Jones <rjones@redhat.com> - 1:0.13.0-6
- OCaml 4.10.0 final.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.13.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jan 19 2020 Richard W.M. Jones <rjones@redhat.com> - 1:0.13.0-4
- Bump release and rebuild.

* Sun Jan 19 2020 Richard W.M. Jones <rjones@redhat.com> - 1:0.13.0-3
- OCaml 4.10.0+beta1 rebuild.

* Thu Jan 16 2020 Jerry James <loganjerry@gmail.com> - 1:0.13.0-2
- Add ocaml-parsexp-devel R to -devel
- Build in parallel

* Fri Jan 10 2020 Jerry James <loganjerry@gmail.com> - 1:0.13.0-1
- Switch to the Jane Street version

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.5-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.5-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.5-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Richard W.M. Jones <rjones@redhat.com> - 7.0.5-31
- OCaml 4.07.0 (final) rebuild.

* Wed Jun 20 2018 Richard W.M. Jones <rjones@redhat.com> - 7.0.5-30
- OCaml 4.07.0-rc1 rebuild.

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.5-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Nov 17 2017 Richard W.M. Jones <rjones@redhat.com> - 7.0.5-28
- OCaml 4.06.0 rebuild.

* Tue Aug 08 2017 Richard W.M. Jones <rjones@redhat.com> - 7.0.5-27
- OCaml 4.05.0 rebuild.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.5-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.5-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 27 2017 Richard W.M. Jones <rjones@redhat.com> - 7.0.5-24
- OCaml 4.04.2 rebuild.

* Fri May 12 2017 Richard W.M. Jones <rjones@redhat.com> - 7.0.5-23
- OCaml 4.04.1 rebuild.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.5-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Nov 08 2016 Richard W.M. Jones <rjones@redhat.com> - 7.0.5-21
- Rebuild for OCaml 4.04.0.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.5-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jul 28 2015 Richard W.M. Jones <rjones@redhat.com> - 7.0.5-19
- OCaml 4.02.3 rebuild.

* Wed Jun 24 2015 Richard W.M. Jones <rjones@redhat.com> - 7.0.5-18
- ocaml-4.02.2 final rebuild.

* Wed Jun 17 2015 Richard W.M. Jones <rjones@redhat.com> - 7.0.5-17
- ocaml-4.02.2 rebuild.

* Tue Feb 17 2015 Richard W.M. Jones <rjones@redhat.com> - 7.0.5-16
- ocaml-4.02.1 rebuild.

* Thu Sep 25 2014 Jerry James <loganjerry@gmail.com> - 7.0.5-15
- Drop obsolete ExcludeArch
- Fix license handling
- Fix changelog dates

* Sun Aug 31 2014 Richard W.M. Jones <rjones@redhat.com> - 7.0.5-14
- ocaml-4.02.0 final rebuild.

* Sat Aug 23 2014 Richard W.M. Jones <rjones@redhat.com> - 7.0.5-13
- ocaml-4.02.0+rc1 rebuild.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.0.5-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Aug 02 2014 Richard W.M. Jones <rjones@redhat.com> - 7.0.5-11
- ocaml-4.02.0-0.8.git10e45753.fc22 rebuild.

* Mon Jul 21 2014 Richard W.M. Jones <rjones@redhat.com> - 7.0.5-10
- OCaml 4.02.0 beta rebuild.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.0.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Mar 19 2014 Richard W.M. Jones <rjones@redhat.com> - 7.0.5-8
- Rebuild against latest Arg module.

* Thu Sep 19 2013 Richard W.M. Jones <rjones@redhat.com> - 7.0.5-7
- OCaml 4.01.0 rebuild.
- Modernize the spec file.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.0.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.0.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 30 2012 Richard W.M. Jones <rjones@redhat.com> - 7.0.5-4
- Rebuild for OCaml 4.00.1.

* Mon Jul 30 2012 Richard W.M. Jones <rjones@redhat.com> - 7.0.5-3
- Patch for OCaml 4.00.0 official.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Richard W.M. Jones <rjones@redhat.com> - 7.0.5-1
- Update to latest upstream version 7.0.5.
- Rebuild for OCaml 4.00.0.

* Fri Jan 06 2012 Richard W.M. Jones <rjones@redhat.com> - 7.0.4-2
- Rebuild for OCaml 3.12.1.

* Tue Sep 27 2011 Michael Ekstrand <michael@elehack.net> - 7.0.4-1
- New upstream release 7.0.4 from forge.ocamlcore.org (#741483)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan  6 2011 Richard W.M. Jones <rjones@redhat.com> - 6.0.4-1
- New upstream version 6.0.4.
- Rebuild for OCaml 3.12.0.

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 4.2.15-2
- Rebuild for OCaml 3.11.2.

* Sun Oct  4 2009 Richard W.M. Jones <rjones@redhat.com> - 4.2.15-1
- New upstream version 4.2.15.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 12 2009 Richard W.M. Jones <rjones@redhat.com> - 4.2.10-2
- Rebuild to try to fix rpmdepsize FTBFS problem.

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 4.2.10-1
- Rebuild for OCaml 3.11.1.
- New upstream version 4.2.10.

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Mon Mar 30 2009 Richard W.M. Jones <rjones@redhat.com> - 4.2.7-2
- Force rebuild against latest ocaml-type-conv.

* Tue Mar 10 2009 Richard W.M. Jones <rjones@redhat.com> - 4.2.7-1
- New upstream version 4.2.7.
- Fixed source URL.
- Removed the patch as it is now upstream.
- Fixed the doc line.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 4.2.1-2
- Rebuild for OCaml 3.11.0+rc1.

* Thu Nov 20 2008 Richard W.M. Jones <rjones@redhat.com> - 4.2.1-1
- New upstream version 4.2.1.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 4.0.1-2
- Rebuild for OCaml 3.11.0

* Sun Aug 31 2008 Richard W.M. Jones <rjones@redhat.com> - 4.0.1-1
- New upstream release 4.0.1.
- Patch a build problem in the test suite.
- ml file should be packaged in the -devel subpackage, not in main.

* Mon May 12 2008 Richard W.M. Jones <rjones@redhat.com> - 3.7.4-2
- Added BR ocaml-camlp4-devel.
- Added a check section to run the included tests.

* Sat May  3 2008 Richard W.M. Jones <rjones@redhat.com> - 3.7.4-1
- New upstream version 3.7.4.

* Wed Apr 23 2008 Richard W.M. Jones <rjones@redhat.com> - 3.7.1-1
- New upstream version 3.7.1.
- Fixed upstream URL.
- Depend on latest type-conv.

* Wed Mar  5 2008 Richard W.M. Jones <rjones@redhat.com> - 3.5.0-2
- Remove ExcludeArch ppc64.

* Sun Feb 24 2008 Richard W.M. Jones <rjones@redhat.com> - 3.5.0-1
- Initial RPM release.
