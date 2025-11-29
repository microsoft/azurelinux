# OCaml packages not built on i686 since OCaml 5 / Fedora 39.
ExcludeArch: %{ix86}

%ifnarch %{ocaml_native_compiler}
%global debug_package %{nil}
%endif

%global giturl  https://github.com/camlp5/camlp5

Name:           ocaml-camlp5
Version:        8.04.00
Release:        3%{?dist}
Summary:        Preprocessor and pretty printer for OCaml

License:        BSD-3-Clause
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://camlp5.github.io/
VCS:            git:%{giturl}.git
Source0:        %{giturl}/archive/%{version}/camlp5-%{version}.tar.gz#/%{name}-%{version}.tar.gz

# Kill -warn-error A
Patch0:         camlp5-8.00-kill-warn-error.patch

BuildRequires:  diffutils
BuildRequires:  make
BuildRequires:  ocaml >= 4.10
BuildRequires:  ocaml-bos-devel
BuildRequires:  ocaml-camlp-streams-devel >= 5.0
BuildRequires:  ocaml-camlp5-buildscripts >= 0.06
BuildRequires:  ocaml-findlib
BuildRequires:  ocaml-fmt-devel
BuildRequires:  ocaml-ounit-devel
BuildRequires:  ocaml-pcre2-devel >= 8.0.3
BuildRequires:  ocaml-re-devel >= 1.11.0
BuildRequires:  ocaml-rpm-macros
BuildRequires:  ocaml-rresult-devel
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(IPC::System::Simple)
BuildRequires:  perl(String::ShellQuote)

BuildRequires:  ocaml-ocamldoc

# Do not provide symbols already provided by the OCaml compiler
%global __ocaml_provides_opts -i Dynlink -i Dynlink_common -i Dynlink_config -i Dynlink_platform_intf -i Dynlink_symtable -i Dynlink_types
# Do not require symbols that we don't provide
%global __ocaml_requires_opts -i Dynlink_cmo_format -i MLast

# Camlp5 RPM currently auto-requires ocaml(O_keywords), but its -devel subpackage provides it. That creates a circular dependency because the generator doesn’t know it’s internal.
%global __ocaml_requires_opts -i O_keywords -i R_keywords

%description
Camlp5 is a preprocessor-pretty-printer of OCaml.

It is compatible with all versions of OCaml from 4.05.0 thru 4.14.0.
Previous versions of Camlp5 have supported OCaml versions down to 1.07
and jocaml 3.12.0 to 3.12.1, but this version cuts off support at
4.10.0.  Camlp5 is heavily tested with OCaml versions from 4.10.0
forward, with an extensive and ever-growing testsuite.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ocaml-camlp-streams-devel%{?_isa}
Requires:       ocaml-re-devel%{?_isa}


%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.


%prep
%autosetup -n camlp5-%{version} -p1
find . -name .gitignore -delete

# Avoid obsolescence warning
sed -i 's/egrep/grep -E/' configure


%build
# Upstream uses hand-written configure, grrrrrr.
./configure \
    --prefix %{_prefix} \
    --bindir %{_bindir} \
    --libdir %{_libdir}/ocaml \
    --mandir %{_mandir}
%ifarch %{ocaml_native_compiler}
%make_build DEBUG=-g
%else
%make_build world DEBUG=-g
%endif


%install
%make_install
%ocaml_files
sed -i '\@%{_bindir}@d;\@%{_mandir}@d' .ofiles


%ifarch %{ocaml_native_compiler}
# The testsuite relies on ocamlopt
%check
make -C testsuite all-tests
make -C test all
%endif


%files -f .ofiles
%license LICENSE
%doc README.md


%files devel -f .ofiles-devel
%doc CHANGES ICHANGES DEVEL UPGRADING doc/html doc/htmlp
%{_bindir}/camlp5*
%{_bindir}/mkcamlp5*
%{_bindir}/ocpp5
%{_mandir}/man1/*.1*


%changelog
* Fri Nov 28 2025 Aninda Pradhan <v-anipradhan@microsoft.com> - 8.04.00-3
- Initial Azure Linux import from Fedora 44 (license: MIT)
- License Verified

* Tue Oct 14 2025 Richard W.M. Jones <rjones@redhat.com> - 8.04.00-2
- OCaml 5.4.0 rebuild

* Mon Oct 13 2025 Richard W.M. Jones <rjones@redhat.com> - 8.04.00-1
- New upstream version 8.04.00

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 8.03.05-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Mar 21 2025 Jerry James <loganjerry@gmail.com> - 8.03.03-1
- Version 8.03.03

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 8.03.01-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jan 10 2025 Jerry James <loganjerry@gmail.com> - 8.03.01-1
- OCaml 5.3.0 rebuild for Fedora 42
- Version 8.03.01

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 8.03.00-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 19 2024 Richard W.M. Jones <rjones@redhat.com> - 8.03.00-3
- OCaml 5.2.0 ppc64le fix

* Thu May 30 2024 Richard W.M. Jones <rjones@redhat.com> - 8.03.00-2
- OCaml 5.2.0 for Fedora 41

* Thu May 23 2024 Jerry James <loganjerry@gmail.com> - 8.03.00-1
- Version 8.03.00

* Mon Jan 29 2024 Richard W.M. Jones <rjones@redhat.com> - 8.02.01-7
- Bump and rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 8.02.01-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 8.02.01-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 18 2023 Richard W.M. Jones <rjones@redhat.com> - 8.02.01-4
- OCaml 5.1.1 + s390x code gen fix for Fedora 40

* Tue Dec 12 2023 Richard W.M. Jones <rjones@redhat.com> - 8.02.01-3
- OCaml 5.1.1 rebuild for Fedora 40

* Thu Oct 05 2023 Richard W.M. Jones <rjones@redhat.com> - 8.02.01-2
- OCaml 5.1 rebuild for Fedora 40

* Wed Oct  4 2023 Jerry James <loganjerry@gmail.com> - 8.02.01-1
- Version 8.02.01
- Depend on ocaml-pcre2 instead of ocaml-pcre

* Sat Sep  9 2023 Jerry James <loganjerry@gmail.com> - 8.02.00-2
- Add camlp-streams-/pcre-devel dependencies to devel subpackage

* Tue Aug 15 2023 Jerry James <loganjerry@gmail.com> - 8.02.00-1
- Version 8.02.00
- Drop unnecessary function-ref patch

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 8.01.00-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Richard W.M. Jones <rjones@redhat.com> - 8.01.00-2
- OCaml 5.0 rebuild for Fedora 39

* Mon Jul 10 2023 Jerry James <loganjerry@gmail.com> - 8.01.00-1
- Version 8.01.00
- Convert License tag to SPDX
- Add function-ref patch to fix FTBFS with OCaml 5.0.0
- Add %%check script
- Use new OCaml macros

* Tue Jan 24 2023 Richard W.M. Jones <rjones@redhat.com> - 8.00.03-4
- Rebuild OCaml packages for F38

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 8.00.03-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 8.00.03-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jun 18 2022 Richard W.M. Jones <rjones@redhat.com> - 8.00.03-1
- Update to released 8.00.03 supporting OCaml 4.14.0
- OCaml 4.14.0 rebuild

* Fri Feb 04 2022 Richard W.M. Jones <rjones@redhat.com> - 8.00.03-0.4
- OCaml 4.13.1 rebuild to remove package notes

* Wed Jan 26 2022 Richard W.M. Jones <rjones@redhat.com> - 8.00.03-0.3
- Rebuild to pick up new ocaml dependency

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 8.00.03-0.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Oct  5 2021 Richard W.M. Jones <rjones@redhat.com> - 8.00.03-0.1
- Move to pre-release of 8.00.03 (git commit f1ede8037e)
- Remove upstream patch.
- Remove %%opt macro as its not used.

* Mon Oct 04 2021 Richard W.M. Jones <rjones@redhat.com> - 8.00-4
- OCaml 4.13.1 build

* Tue Jul 27 2021 Richard W.M. Jones <rjones@redhat.com> - 8.00-3
- Rebuild for changed ocamlx(Dynlink)

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 8.00-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun Feb 28 22:24:15 GMT 2021 Richard W.M. Jones <rjones@redhat.com> - 8.00-1
- New upstream version 8.00.
- OCaml 4.12.0 build

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 7.12-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Sep 02 2020 Richard W.M. Jones <rjones@redhat.com> - 7.12-9
- Rebuild with correct tag.

* Tue Sep 01 2020 Richard W.M. Jones <rjones@redhat.com> - 7.12-8
- OCaml 4.11.1 rebuild

* Fri Aug 21 2020 Richard W.M. Jones <rjones@redhat.com> - 7.12-1
- New upstream version 7.12.
- Remove upstream patches.
- OCaml 4.11.0 rebuild
- Remove topfind.camlp5 - seems to have been removed from upstream.

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon May 04 2020 Richard W.M. Jones <rjones@redhat.com> - 7.11-5
- OCaml 4.11.0+dev2-2020-04-22 rebuild

* Mon May 04 2020 Richard W.M. Jones <rjones@redhat.com> - 7.11-4
- Include all upstream pre-7.12 patches.
- Fixes support for OCaml 4.11.

* Fri Apr 17 2020 Richard W.M. Jones <rjones@redhat.com> - 7.11-3
- OCaml 4.11.0 pre-release

* Thu Apr 02 2020 Richard W.M. Jones <rjones@redhat.com> - 7.11-2
- Update all OCaml dependencies for RPM 4.16.

* Sun Mar 08 2020 Richard W.M. Jones <rjones@redhat.com> - 7.11-1
- Update to 7.11.
- Remove OCaml 4.10 support patch, now included upstream.

* Wed Feb 26 2020 Richard W.M. Jones <rjones@redhat.com> - 7.10-6
- OCaml 4.10.0 final.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jan 19 2020 Richard W.M. Jones <rjones@redhat.com> - 7.10-4
- Add patch for OCaml 4.10 support.

* Sat Jan 18 2020 Richard W.M. Jones <rjones@redhat.com> - 7.10-3
- OCaml 4.10.0+beta1 rebuild.

* Thu Jan 09 2020 Richard W.M. Jones <rjones@redhat.com> - 7.10-2
- OCaml 4.09.0 for riscv64

* Thu Dec 05 2019 Richard W.M. Jones <rjones@redhat.com> - 7.10-1
- Update to release 7.10.
- OCaml 4.09.0 (final) rebuild.

* Fri Aug 16 2019 Richard W.M. Jones <rjones@redhat.com> - 7.08-0.5.git9b9eb124c
- OCaml 4.08.1 (final) rebuild.

* Wed Jul 31 2019 Richard W.M. Jones <rjones@redhat.com> - 7.08-0.4.git9b9eb124c
- OCaml 4.08.1 (rc2) rebuild.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.08-0.3.git9b9eb124c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jun 27 2019 Richard W.M. Jones <rjones@redhat.com> - 7.08-0.2.git9b9eb124c
- OCaml 4.08.0 (final) rebuild.

* Thu Jun 27 2019 Richard W.M. Jones <rjones@redhat.com> - 7.08-0.1
- Update to prerelease of 7.08 which will support OCaml 4.08.
- Enable parallel builds.

* Mon Apr 29 2019 Richard W.M. Jones <rjones@redhat.com> - 7.05-8
- Bump release and rebuild.

* Mon Apr 29 2019 Richard W.M. Jones <rjones@redhat.com> - 7.05-7
- Bump release and rebuild.

* Mon Apr 29 2019 Richard W.M. Jones <rjones@redhat.com> - 7.05-6
- OCaml 4.08.0 (beta 3) rebuild.

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.05-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7.05-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Richard W.M. Jones <rjones@redhat.com> - 7.05-3
- OCaml 4.07.0 (final) rebuild.

* Tue Jun 19 2018 Richard W.M. Jones <rjones@redhat.com> - 7.05-2
- New upstream version 7.05.
- Bump and rebuild for OCaml 4.07.0-rc1.

* Thu Apr 26 2018 Richard W.M. Jones <rjones@redhat.com> - 7.03-3
- OCaml 4.07.0-beta2 rebuild.

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7.03-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Nov 17 2017 Richard W.M. Jones <rjones@redhat.com> - 7.03-1
- New upstream version 7.03.
- OCaml 4.06.0 rebuild.

* Tue Aug 08 2017 Richard W.M. Jones <rjones@redhat.com> - 7.00-4
- OCaml 4.05.0 rebuild.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.00-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.00-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 27 2017 Richard W.M. Jones <rjones@redhat.com> - 7.00-1
- New upstream version 7.00, including support for
  OCaml 4.04.2 rebuild.

* Sat May 13 2017 Richard W.M. Jones <rjones@redhat.com> - 6.17-3
- OCaml 4.04.1 rebuild.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Dec 03 2016 Richard W.M. Jones <rjones@redhat.com> - 6.17-1
- New upstream version 6.17 with support for OCaml 4.04.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 6.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jul 30 2015 Richard W.M. Jones <rjones@redhat.com> - 6.14-1
- New upstream version 6.14.

* Tue Jul 28 2015 Richard W.M. Jones <rjones@redhat.com> - 6.13-3
- OCaml 4.02.3 rebuild.

* Wed Jun 24 2015 Richard W.M. Jones <rjones@redhat.com> - 6.13-2
- ocaml-4.02.2 final rebuild.

* Wed Jun 17 2015 Richard W.M. Jones <rjones@redhat.com> - 6.13-1
- New upstream version 6.13.
- ocaml-4.02.2 rebuild.

* Fri May 15 2015 Ville Skyttä <ville.skytta@iki.fi> - 6.12-3
- Mark LICENSE as %%license, don't ship .gitignore

* Mon Feb 16 2015 Richard W.M. Jones <rjones@redhat.com> - 6.12-2
- ocaml-4.02.1 rebuild.

* Thu Nov  6 2014 Jerry James <loganjerry@gmail.com> - 6.12-1
- Update to 6.12 final
- Drop upstreamed patches (all but -kill-warn-error)
- Drop debuginfo workaround; fixed upstream

* Sat Aug 30 2014 Richard W.M. Jones <rjones@redhat.com> - 6.12-0.5.git63a8c30f
- ocaml-4.02.0 final rebuild.

* Sun Aug 24 2014 Richard W.M. Jones <rjones@redhat.com> - 6.12-0.4.git63a8c30f
- Fixes for 4.02.0+rc1.
- Kill -warn-error everywhere hopefully.
- Update parsing/location.mli from OCaml sources.
- Fix release numbering.

* Sat Aug 23 2014 Richard W.M. Jones <rjones@redhat.com> - 6.12-0.git63a8c30f.3
- ocaml-4.02.0+rc1 rebuild.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.12-0.git63a8c30f.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 01 2014 Richard W.M. Jones <rjones@redhat.com> - 6.12-0.git63a8c30f.1
- ocaml-4.02.0-0.8.git10e45753.fc22 build.

* Fri Aug 01 2014 Richard W.M. Jones <rjones@redhat.com> - 6.12-0.git63a8c30f
- Rebase to 6.12 prerelease which supports OCaml 4.02.
- OCaml 4.02.0 beta rebuild.
- New source URL.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 15 2014 Richard W.M. Jones <rjones@redhat.com> - 6.11-3
- Remove ocaml_arches macro (RHBZ#1087794).

* Thu Apr 10 2014 Michel Normand <normand@linux.vnet.ibm.com> 6.11-2
- increase stack size for ppc64/ppc64le (RHBZ#1085850)

* Sat Sep 14 2013 Jerry James <loganjerry@gmail.com> - 6.11-1
- New upstream version 6.11 (provides OCaml 4.01.0 support)
- Build with debug information
- Drop upstreamed -typevar patch
- Upstream now provides its own META file

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.07-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.07-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Oct 17 2012 Jerry James <loganjerry@gmail.com> - 6.07-1
- New upstream version 6.07 (provides OCaml 4.00.1 support)
- Add -typevar patch to fix the build

* Sat Jul 28 2012 Richard W.M. Jones <rjones@redhat.com> - 6.06-4
- Rebuild for OCaml 4.00.0 official release.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.06-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 10 2012 Richard W.M. Jones <rjones@redhat.com> - 6.06-2
- Rebuild for OCaml 4.00.0.

* Fri Jun  8 2012 Jerry James <loganjerry@gmail.com> - 6.06-1
- New upstream version 6.06 (provides OCaml 4.0 support)
- Add HTML documentation to the -devel package

* Fri Jan 06 2012 Richard W.M. Jones <rjones@redhat.com> - 6.02.3-2
- Rebuild for OCaml 3.12.1.

* Thu Oct 27 2011 Jerry James <loganjerry@gmail.com> - 6.02.3-1
- New upstream version 6.02.3 (bz 691913).
- Switch from ExcludeArch to ExclusiveArch %%{ocaml_arches}.
- Drop unnecessary spec file elements (BuildRoot, etc.).
- Preserve timestamp on META.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.02.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan  6 2011 Richard W.M. Jones <rjones@redhat.com> - 6.02.1-1
- New upstream version 6.02.1.
- Remove upstream patches (both upstream).
- Rebuild for OCaml 3.12.0.

* Wed Jan 13 2010 Richard W.M. Jones <rjones@redhat.com> - 5.12-6
- Ignore bogus provides Dynlink and Dynlinkaux.

* Wed Jan  6 2010 Richard W.M. Jones <rjones@redhat.com> - 5.12-5
- Ignore ocaml(Pa_extend) bogus generated requires and provides.

* Tue Jan  5 2010 Richard W.M. Jones <rjones@redhat.com> - 5.12-4
- Include Debian patch to fix support for OCaml 3.11.2.
- Include Debian patch to fix typos in man page.
- Replace %%define with %%global.
- Use upstream RPM 4.8 OCaml dependency generator.
- Put ./configure in %%build section.

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 5.12-3
- Rebuild for OCaml 3.11.2.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 5.12-1
- New upstream version 5.12, excepted to fix 3.11.1 build problems.

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 5.11-1
- Rebuild for OCaml 3.11.1
- New upstream version 5.11.
- Remove META file listed twice in %%files.

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 5.10-2
- Rebuild for OCaml 3.11.0+rc1.

* Thu Nov 20 2008 Richard W.M. Jones <rjones@redhat.com> - 5.10-1
- New upstream version 5.10.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 5.09-2
- Rebuild for OCaml 3.11.0

* Sun Aug 31 2008 Richard W.M. Jones <rjones@redhat.com> - 5.09-1
- New upstream version 5.09.

* Wed Apr 23 2008 Richard W.M. Jones <rjones@redhat.com> - 5.08-3
- Rebuild for OCaml 3.10.2.

* Sat Mar  1 2008 Richard W.M. Jones <rjones@redhat.com> - 5.08-2
- Build on ppc64.

* Thu Feb 21 2008 Richard W.M. Jones <rjones@redhat.com> - 5.08-1
- New upstream version 5.08.
- BR ocaml >= 3.10.1.

* Tue Feb 12 2008 Richard W.M. Jones <rjones@redhat.com> - 5.04-2
- Strip the *.opt binaries.

* Thu Dec 13 2007 Stijn Hoop <stijn@win.tue.nl> - 5.04-1
- Update to 5.04

* Wed Aug  8 2007 Richard W.M. Jones <rjones@redhat.com> - 4.07-2
- Add a META file.

* Wed Aug  8 2007 Richard W.M. Jones <rjones@redhat.com> - 4.07-1
- Initial RPM release.
