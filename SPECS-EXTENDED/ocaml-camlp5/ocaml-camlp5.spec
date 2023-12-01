%global __ocaml_requires_opts -i Asttypes -i Parsetree -i Pa_extend
%global __ocaml_provides_opts -i Dynlink -i Dynlinkaux -i Pa_extend
Summary:        Classical version of camlp4 OCaml preprocessor
Name:           ocaml-camlp5
Version:        8.00.02
Release:        11%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://camlp5.github.io/
Source0:        https://github.com/camlp5/camlp5/archive/rel%{version}.tar.gz#/camlp5-rel%{version}.tar.gz
BuildRequires:  make
BuildRequires:  ocaml
BuildRequires:  ocaml-ocamldoc
BuildRequires:  perl

%description
Camlp5 is a preprocessor-pretty-printer of OCaml.

It is the continuation of the classical camlp4 with new features.

OCaml 3.10 and above have an official camlp4 which is incompatible
with classical (<= 3.09) versions.  You can find that in the
ocaml-camlp4 package.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%prep
%autosetup -p1 -n camlp5-rel%{version}
find . -name .gitignore -delete

# Build with debug information
sed -i 's,WARNERR="",WARNERR="-g",' configure
sed -i 's,-linkall,& -g,g' top/Makefile
for fil in compile/compile.sh $(find . -name Makefile); do
  sed -i 's,\$[({]OCAMLN[})]c,& -g,;s,\$[({]OCAMLN[})]opt,& -g,;s,LINKFLAGS=,&-g ,' $fil
done

%build
# Upstream uses hand-written configure, grrrrrr.
./configure \
    --prefix %{_prefix} \
    --bindir %{_bindir} \
    --libdir %{_libdir}/ocaml \
    --mandir %{_mandir}
%make_build world.opt

%install
mkdir -p %{buildroot}%{_libdir}/ocaml
# This is a hack because the make install rule is broken upstream.
# We move the file later.
mkdir -p %{buildroot}%{_libdir}/ocaml/ocaml
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}
%make_install
cp -p etc/META %{buildroot}%{_libdir}/ocaml/camlp5
rm -f doc/htmlp/{*.sh,Makefile,html2*}
mv %{buildroot}%{_libdir}/ocaml/{ocaml/topfind.camlp5,}


%files
%license LICENSE
%doc README.md
%{_libdir}/ocaml/camlp5
%{_libdir}/ocaml/topfind.camlp5
%exclude %{_libdir}/ocaml/camlp5/*.a
%exclude %{_libdir}/ocaml/camlp5/*.cmxa
%exclude %{_libdir}/ocaml/camlp5/*.cmx
%exclude %{_libdir}/ocaml/camlp5/*.mli

%files devel
%doc CHANGES ICHANGES DEVEL UPGRADING doc/html
%{_libdir}/ocaml/camlp5/*.a
%{_libdir}/ocaml/camlp5/*.cmxa
%{_libdir}/ocaml/camlp5/*.cmx
%{_libdir}/ocaml/camlp5/*.mli
%{_bindir}/camlp5*
%{_bindir}/mkcamlp5*
%{_bindir}/ocpp5
%{_mandir}/man1/*.1*

%changelog
* Fri Jan 21 2022 Olivia Crain <oliviacrain@microsoft.com> - 8.00.02-1
- Upgrade to latest upstream version
- Lint spec
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 7.12-11
- Initial CBL-Mariner import from Fedora 34 (license: MIT).

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
