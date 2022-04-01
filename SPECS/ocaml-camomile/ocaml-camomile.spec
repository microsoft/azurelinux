# FIXME: Broken in 1.0.1 for unknown reasons.
%global debug_package %{nil}

Summary:        Unicode library for OCaml
Name:           ocaml-camomile
Version:        1.0.2
Release:        9%{?dist}
# Several files are MIT and UCD licensed, but the overall work is LGPLv2+
# and the LGPL/GPL supercedes compatible licenses.
# https://www.redhat.com/archives/fedora-legal-list/2008-March/msg00005.html
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/yoriyuki/Camomile
Source0:        https://github.com/yoriyuki/Camomile/archive/refs/tags/%{version}.tar.gz#/camomile-%{version}.tar.gz

BuildRequires:  ocaml >= 3.12.1-12
BuildRequires:  ocaml-cppo
BuildRequires:  ocaml-dune
BuildRequires:  ocaml-findlib-devel
BuildRequires:  ocaml-ocamldoc

# The base package requires the data files.  Note that it is possible
# to install the data files on their own to support other packages
# that need the mappings, and some packages (eg. guestfs-browser) do
# exactly this.
Requires:       %{name}-data = %{version}-%{release}

%description
Camomile is a Unicode library for ocaml. Camomile provides Unicode
character type, UTF-8, UTF-16, UTF-32 strings, conversion to/from
about 200 encodings, collation and locale-sensitive case mappings, and
more.

%package        devel
Summary:        Development files for %{name}

Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%package        data
Summary:        Data files for %{name}

%description    data
The %{name}-data package contains data files for developing
applications that use %{name}.

%prep
%setup -q -n Camomile-%{version}

%build
# This avoids a stack overflow in the OCaml 4.05 compiler on POWER only.
%ifarch %{power64}
ulimit -Hs 65536
ulimit -Ss 65536
%endif
dune build --verbose --profile release


%install
dune install \
         --destdir=%{buildroot} \
         --libdir=%{_libdir}/ocaml \
         --verbose \
         --profile release

# Remove /usr/doc because we will use %%doc rules instead.
rm -rf %{buildroot}%{_prefix}/doc

# Install the *.mli files by hand.
cp _build/install/default/lib/camomile/library/*.mli %{buildroot}%{_libdir}/ocaml/camomile/

%check
# Broken in 1.0.2.
# https://github.com/yoriyuki/Camomile/issues/82
#jbuilder runtest --profile release

%files
%doc README.md CHANGES.md
%license LICENSE.md
%{_libdir}/ocaml/camomile
%ifarch %{ocaml_native_compiler}
%exclude %{_libdir}/ocaml/camomile/*.a
%exclude %{_libdir}/ocaml/camomile/*.cmxa
%exclude %{_libdir}/ocaml/camomile/*.cmx
%endif
%exclude %{_libdir}/ocaml/camomile/*.mli
%ifarch %{ocaml_native_compiler}
%endif

%files devel
%license LICENSE.md
%ifarch %{ocaml_native_compiler}
%{_libdir}/ocaml/camomile/*.a
%{_libdir}/ocaml/camomile/*.cmxa
%{_libdir}/ocaml/camomile/*.cmx
%endif
%{_libdir}/ocaml/camomile/*.mli

%files data
%license LICENSE.md
%{_datadir}/camomile/

%changelog
* Thu Mar 31 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.2-9
- Cleaning-up spec. License verified.

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.2-8
- Switching to using full number for the 'Release' tag.
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Feb 28 2020 Richard W.M. Jones <rjones@redhat.com> - 1.0.2-7.1
- OCaml 4.10.0 final (Fedora 32).

* Wed Feb 26 2020 Richard W.M. Jones <rjones@redhat.com> - 1.0.2-7
- OCaml 4.10.0 final.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jan 19 2020 Richard W.M. Jones <rjones@redhat.com> - 1.0.2-5
- OCaml 4.10.0+beta1 rebuild.
- Use dune instead of jbuilder.

* Fri Dec 06 2019 Richard W.M. Jones <rjones@redhat.com> - 1.0.2-4
- OCaml 4.09.0 (final) rebuild.

* Fri Aug 16 2019 Richard W.M. Jones <rjones@redhat.com> - 1.0.2-3
- OCaml 4.08.1 (final) rebuild.

* Fri Aug 09 2019 Richard W.M. Jones <rjones@redhat.com> - 1.0.2-2
- Reenable armv7 architecture now that nodynlink issue has been worked around.
  https://github.com/ocaml/dune/issues/2527

* Thu Aug 08 2019 Richard W.M. Jones <rjones@redhat.com> - 1.0.2-1
- New upstream version 1.0.2.

* Wed Jul 31 2019 Richard W.M. Jones <rjones@redhat.com> - 1.0.1-6
- OCaml 4.08.1 (rc2) rebuild.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jun 27 2019 Richard W.M. Jones <rjones@redhat.com> - 1.0.1-4
- OCaml 4.08.0 (final) rebuild.

* Tue Apr 30 2019 Richard W.M. Jones <rjones@redhat.com> - 1.0.1-3
- Use jbuilder --profile release to disable warn-error.
- Use jbuilder install instead of hand-installing.
- Use %%doc and %%license.
- Remove some binaries which are no longer installed.

* Mon Apr 29 2019 Richard W.M. Jones <rjones@redhat.com> - 1.0.1-2
- OCaml 4.08.0 (beta 3) rebuild.

* Mon Apr 29 2019 Richard W.M. Jones <rjones@redhat.com> - 1.0.1-1
- New upstream version 1.0.1.
- Remove ocaml-camlp4 dependency, no longer needed.

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Richard W.M. Jones <rjones@redhat.com> - 0.8.7-3
- OCaml 4.07.0 (final) rebuild.

* Tue Jun 19 2018 Richard W.M. Jones <rjones@redhat.com> - 0.8.7-2
- OCaml 4.07.0-rc1 rebuild.

* Mon Mar 05 2018 Sergey Avseyev <sergey.avseyev@gmail.com> - 0.8.7-1
- New upstream version 0.8.7

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Nov 08 2017 Richard W.M. Jones <rjones@redhat.com> - 0.8.6-3
- OCaml 4.06.0 rebuild.
- Dereference symlinks when copying data files.

* Tue Oct 17 2017 Richard W.M. Jones <rjones@redhat.com> - 0.8.6-1
- New upstream version 0.8.6.
- Switch back to versioned releases.
- Use new build system.
- Enable parallel builds.
- Drop -g patch since that seems to work by default now.
- Run tests.

* Mon Aug 07 2017 Richard W.M. Jones <rjones@redhat.com> - 0.8.6-0.1
- Build from git releases.
- OCaml 4.05.0 rebuild.
- Use ocaml_native_compiler instead of opt.
- Do not disable debuginfo.
- Add new BR ocaml-cppo.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.5-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.5-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 26 2017 Richard W.M. Jones <rjones@redhat.com> - 0.8.5-21
- OCaml 4.04.2 rebuild.

* Fri May 12 2017 Richard W.M. Jones <rjones@redhat.com> - 0.8.5-20
- OCaml 4.04.1 rebuild.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.5-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Nov 04 2016 Richard W.M. Jones <rjones@redhat.com> - 0.8.5-18
- Rebuild for OCaml 4.04.0.

* Mon Sep 12 2016 Dan Horák <dan[at]danny.cz> - 0.8.5-17
- disable debuginfo subpackage on interpreted builds

* Sat May 14 2016 Richard Jones <rjones@redhat.com> - 0.8.5-16
- Base package should depend on -data, not other way round (RHBZ#1336000).

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.5-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 26 2016 Richard Jones <rjones@redhat.com> - 0.8.5-14
- Remove useless defattr in files section.

* Tue Jul 28 2015 Richard W.M. Jones <rjones@redhat.com> - 0.8.5-13
- OCaml 4.02.3 rebuild.

* Tue Jul 21 2015 Richard W.M. Jones <rjones@redhat.com> - 0.8.5-12
- Enable bytecode builds.

* Tue Jun 23 2015 Richard W.M. Jones <rjones@redhat.com> - 0.8.5-10
- Bump release and rebuild.

* Wed Jun 17 2015 Richard W.M. Jones <rjones@redhat.com> - 0.8.5-9
- ocaml-4.02.2 rebuild.

* Tue Feb 17 2015 Richard W.M. Jones <rjones@redhat.com> - 0.8.5-8
- Bump release and rebuild.

* Mon Feb 16 2015 Richard W.M. Jones <rjones@redhat.com> - 0.8.5-7
- ocaml-4.02.1 rebuild.

* Sat Aug 30 2014 Richard W.M. Jones <rjones@redhat.com> - 0.8.5-6
- ocaml-4.02.0 final rebuild.

* Sat Aug 23 2014 Richard W.M. Jones <rjones@redhat.com> - 0.8.5-5
- ocaml-4.02.0+rc1 rebuild.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Aug 02 2014 Richard W.M. Jones <rjones@redhat.com> - 0.8.5-3
- ocaml-4.02.0-0.8.git10e45753.fc22 rebuild.

* Mon Jul 21 2014 Richard W.M. Jones <rjones@redhat.com> - 0.8.5-2
- OCaml 4.02.0 beta rebuild.

* Tue Jul 15 2014 Richard W.M. Jones <rjones@redhat.com> - 0.8.5-1
- New upstream version 0.8.5.
- Rebuild for OCaml 4.02.0.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Sep 14 2013 Richard W.M. Jones <rjones@redhat.com> - 0.8.3-13
- Rebuild for OCaml 4.01.0.
- Enable debuginfo.
- Prevent parallel builds.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Oct 19 2012 Richard W.M. Jones <rjones@redhat.com> - 0.8.3-10
- Rebuild for OCaml 4.00.1.
- Clean up the spec file.

* Sat Jul 28 2012 Richard W.M. Jones <rjones@redhat.com> - 0.8.3-9
- Bump and rebuild against new OCaml 4.00.0 official release.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 09 2012 Richard W.M. Jones <rjones@redhat.com> - 0.8.3-7
- Rebuild for OCaml 4.00.0.

* Wed Jun  6 2012 Richard W.M. Jones <rjones@redhat.com> - 0.8.3-6
- Remove sed hack which worked around segfault on ppc64.  Now fixed
  in OCaml >= 3.12.1-12.

* Sun Jun  3 2012 Richard W.M. Jones <rjones@redhat.com> - 0.8.3-5
- Remove patch which worked around segfault on ARM.  Now fixed
  in OCaml >= 3.12.1-9.

* Wed May 30 2012 Richard W.M. Jones <rjones@redhat.com> - 0.8.3-4
- Remove ExcludeArch ppc64.
- Add sed hack to reduce size of long entry function which breaks
  ppc64 code generator.  See comment in spec file for full details.

* Sat May 19 2012 Richard W.M. Jones <rjones@redhat.com> - 0.8.3-2
- Include workaround for segfault in gen_mappings.ml on ARM.
- Bump release and rebuild for new OCaml on ARM.

* Fri Jan  6 2012 Richard W.M. Jones <rjones@redhat.com> - 0.8.3-1
- New upstream version 0.8.3.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan  5 2011 Richard W.M. Jones <rjones@redhat.com> - 0.8.1-1
- New upstream version 0.8.1.
- Rebuild for OCaml 3.12.0.
- camomilecharmap and camomilelocaledef no longer installed by default,
  install them by hand instead.

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 0.7.2-2
- Rebuild for OCaml 3.11.2.

* Thu Oct  8 2009 Richard W.M. Jones <rjones@redhat.com> - 0.7.2-1
- New upstream version 0.7.2.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 0.7.1-11
- Rebuild for OCaml 3.11.1

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 0.7.1-9
- Rebuild for OCaml 3.11.0+rc1.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 0.7.1-8
- Rebuild for OCaml 3.11.0

* Wed Apr 23 2008 Richard W.M. Jones <rjones@redhat.com> - 0.7.1-7
- Rebuild for OCaml 3.10.2

* Fri Mar 21 2008 Richard W.M. Jones <rjones@redhat.com> - 0.7.1-6
- ExcludeArch ppc64 (#438486).

* Mon Mar 17 2008 Richard W.M. Jones <rjones@redhat.com> - 0.7.1-5
- Definitive license.
- Move ./configure into the build section.
- Remove a superfluous comment in the install section.
- Fix rpmlint error 'configure-without-libdir-spec'.
- Scratch build in Koji.

* Wed Mar  5 2008 Richard W.M. Jones <rjones@redhat.com> - 0.7.1-4
- License is LGPLv2+ (no OCaml exception).

* Wed Mar  5 2008 Richard W.M. Jones <rjones@redhat.com> - 0.7.1-3
- Remove ExcludeArch ppc64.

* Tue Feb 12 2008 Richard W.M. Jones <rjones@redhat.com> - 0.7.1-2
- Added BR ocaml-camlp4-devel.
- Rename /usr/bin/*.opt as /usr/bin.

* Wed Aug 08 2007 Richard W.M. Jones <rjones@redhat.com> - 0.7.1-1
- Initial RPM release.
