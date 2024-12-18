# OCaml packages not built on i686 since OCaml 5 / Fedora 39.
ExcludeArch: %{ix86}

Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           ocaml-csv
Version:        2.4
Release:        1%{?dist}
Summary:        OCaml library for reading and writing CSV files
License:        LGPL-2.1-only WITH OCaml-LGPL-linking-exception

URL:            https://github.com/Chris00/ocaml-csv/
Source0:        https://github.com/Chris00/ocaml-csv/archive/%{version}/%{name}-%{version}.tar.gz
# Remove references to a bytes library for OCaml 5.0 support
Patch0:         %{name}-bytes.patch

BuildRequires:  ocaml >= 4.03.0
BuildRequires:  ocaml-dune
BuildRequires:  ocaml-uutf-devel
BuildRequires:  ocaml-lwt-devel


%description
This OCaml library can read and write CSV files, including all
extensions used by Excel - eg. quotes, newlines, 8 bit characters in
fields, quote-0 etc.

The library comes with a handy command line tool called csvtool for
handling CSV files from shell scripts.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}


%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.


%package        lwt
Summary:        LWT bindings for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}


%description    lwt
The %{name}-lwt package contains LWT bindings for %{name}.


%package        lwt-devel
Summary:        LWT development files for %{name}
Requires:       %{name}-lwt%{?_isa} = %{version}-%{release}
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}
Requires:       ocaml-lwt-devel%{?_isa}


%description    lwt-devel
The %{name}-devel package contains libraries and signature files for
developing applications that use LWT with %{name}.


%prep
%autosetup -p1


%build
# _smp_mflags breaks the build for some reason.
# https://github.com/Chris00/ocaml-csv/issues/34
%dune_build -j1


%install
%dune_install -s

# Remove the csvtool META file and opam project
rm -r %{buildroot}%{ocamldir}/csvtool


%files -f .ofiles-csv
%license LICENSE.md
%{_bindir}/csvtool


%files devel -f .ofiles-csv-devel
%doc CHANGES.md README.md


%files lwt -f .ofiles-csv-lwt


%files lwt-devel -f .ofiles-csv-lwt-devel


%changelog
* Thu Dec 19 2024 Durga Jagadeesh Palli <v-dpalli@microsoft.com> - 2.4-1
- Update to 2.4
- License verified

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.7-17
- Switching to using full number for the 'Release' tag.
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Feb 26 2020 Richard W.M. Jones <rjones@redhat.com> - 1.7-16
- OCaml 4.10.0 final.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jan 19 2020 Richard W.M. Jones <rjones@redhat.com> - 1.7-14
- OCaml 4.10.0+beta1 rebuild.

* Fri Dec 06 2019 Richard W.M. Jones <rjones@redhat.com> - 1.7-13
- Bump release and rebuild.

* Fri Dec 06 2019 Richard W.M. Jones <rjones@redhat.com> - 1.7-12
- OCaml 4.09.0 (final) rebuild.

* Fri Aug 16 2019 Richard W.M. Jones <rjones@redhat.com> - 1.7-11
- OCaml 4.08.1 (final) rebuild.

* Wed Jul 31 2019 Richard W.M. Jones <rjones@redhat.com> - 1.7-10
- OCaml 4.08.1 (rc2) rebuild.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jun 27 2019 Richard W.M. Jones <rjones@redhat.com> - 1.7-8
- OCaml 4.08.0 (final) rebuild.

* Mon Apr 29 2019 Richard W.M. Jones <rjones@redhat.com> - 1.7-7
- OCaml 4.08.0 (beta 3) rebuild.

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Richard W.M. Jones <rjones@redhat.com> - 1.7-4
- OCaml 4.07.0 (final) rebuild.

* Wed Jun 20 2018 Richard W.M. Jones <rjones@redhat.com> - 1.7-3
- OCaml 4.07.0-rc1 rebuild.

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Nov 08 2017 Richard W.M. Jones <rjones@redhat.com> - 1.7-1
- New upstream version 1.7.

* Wed Nov 08 2017 Richard W.M. Jones <rjones@redhat.com> - 1.3.1-24
- OCaml 4.06.0 rebuild.

* Mon Aug 07 2017 Richard W.M. Jones <rjones@redhat.com> - 1.3.1-23
- OCaml 4.05.0 rebuild.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 26 2017 Richard W.M. Jones <rjones@redhat.com> - 1.3.1-20
- OCaml 4.04.2 rebuild.

* Fri May 12 2017 Richard W.M. Jones <rjones@redhat.com> - 1.3.1-19
- OCaml 4.04.1 rebuild.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Nov 09 2016 Dan Horák <dan@danny.cz> - 1.3.1-17
- rebuild for s390x codegen bug

* Sat Nov 05 2016 Richard W.M. Jones <rjones@redhat.com> - 1.3.1-16
- Rebuild for OCaml 4.04.0.
- Add dependency on ocamlbuild.

* Wed Oct 19 2016 Dan Horák <dan[at]danny.cz> - 1.3.1-15
- disable debuginfo subpackage on interpreted builds

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jul 28 2015 Richard W.M. Jones <rjones@redhat.com> - 1.3.1-13
- OCaml 4.02.3 rebuild.

* Mon Jul 20 2015 Richard W.M. Jones <rjones@redhat.com> - 1.3.1-12
- Fix/enable bytecode build.

* Wed Jun 24 2015 Richard W.M. Jones <rjones@redhat.com> - 1.3.1-11
- ocaml-4.02.2 final rebuild.

* Wed Jun 17 2015 Richard W.M. Jones <rjones@redhat.com> - 1.3.1-10
- ocaml-4.02.2 rebuild.

* Tue Feb 17 2015 Richard W.M. Jones <rjones@redhat.com> - 1.3.1-9
- ocaml-4.02.1 rebuild.

* Sat Aug 30 2014 Richard W.M. Jones <rjones@redhat.com> - 1.3.1-8
- ocaml-4.02.0 final rebuild.

* Sat Aug 23 2014 Richard W.M. Jones <rjones@redhat.com> - 1.3.1-7
- ocaml-4.02.0+rc1 rebuild.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Aug 02 2014 Richard W.M. Jones <rjones@redhat.com> - 1.3.1-5
- ocaml-4.02.0-0.8.git10e45753.fc22 rebuild.

* Mon Jul 21 2014 Richard W.M. Jones <rjones@redhat.com> - 1.3.1-4
- Bump release and rebuild.

* Mon Jul 21 2014 Richard W.M. Jones <rjones@redhat.com> - 1.3.1-3
- OCaml 4.02.0 beta rebuild.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Sep 14 2013 Richard W.M. Jones <rjones@redhat.com> - 1.3.1-1
- New upstream version 1.3.1.
- Rebuild for OCaml 4.01.0.
- Enable debuginfo.
- Modernize the spec file some more.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 27 2012 Richard W.M. Jones <rjones@redhat.com> - 1.2.3-3
- BR >= OCaml 4.00.1 so we can't be built against the wrong OCaml.

* Mon Nov 26 2012 Richard W.M. Jones <rjones@redhat.com> - 1.2.3-2
- New upstream version 1.2.3.
- New upstream location.
- Clean up the spec file.
- Remove patches since they are no longer relevant.
- New setup appears to require ocamldoc.

* Mon Oct 29 2012 Richard W.M. Jones <rjones@redhat.com> - 1.1.7-13
- Rebuild for OCaml 4.00.1.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.7-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun  7 2012 Richard W.M. Jones <rjones@redhat.com> - 1.1.7-11
- Rebuild for OCaml 4.00.0.

* Fri Jan 06 2012 Richard W.M. Jones <rjones@redhat.com> - 1.1.7-10
- Rebuild for OCaml 3.12.1.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.7-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 05 2011 Richard W.M. Jones <rjones@redhat.com> - 1.1.7-8
- Rebuild for OCaml 3.12 (http://fedoraproject.org/wiki/Features/OCaml3.12).

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 1.1.7-7
- Rebuild for OCaml 3.11.2.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 1.1.7-5
- Rebuild for OCaml 3.11.1

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec  4 2008 Richard W.M. Jones <rjones@redhat.com> - 1.1.7-3
- Rebuild.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 1.1.7-2
- Rebuild for OCaml 3.11.0

* Mon Oct 27 2008 Richard W.M. Jones <rjones@redhat.com> - 1.1.7-1
- New upstream version 1.1.7.

* Wed Apr 23 2008 Richard W.M. Jones <rjones@redhat.com> - 1.1.6-8
- Rebuild for OCaml 3.10.2

* Sat Mar  1 2008 Richard W.M. Jones <rjones@redhat.com> - 1.1.6-7
- Rebuild for ppc64.

* Tue Feb 12 2008 Richard W.M. Jones <rjones@redhat.com> - 1.1.6-6
- Force rebuild for OCaml 3.10.1.

* Thu Sep  6 2007 Richard W.M. Jones <rjones@redhat.com> - 1.1.6-5
- Force rebuild because of base OCaml.

* Thu Aug 30 2007 Richard W.M. Jones <rjones@redhat.com> - 1.1.6-4
- Force rebuild because of changed BRs in base OCaml.

* Fri Aug 24 2007 Richard W.M. Jones <rjones@redhat.com> - 1.1.6-3
- License clarified to LGPLv2+ (and fixed/clarified upstream).
- Added ExcludeArch ppc64

* Mon Jun 11 2007 Richard W.M. Jones <rjones@redhat.com> - 1.1.6-2
- Updated to latest packaging guidelines.

* Tue May 29 2007 Richard W.M. Jones <rjones@redhat.com> - 1.1.6-1
- Initial RPM release.
