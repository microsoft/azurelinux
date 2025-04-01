# OCaml packages not built on i686 since OCaml 5 / Fedora 39.
ExcludeArch: %{ix86}

Name:           virt-top
Version:        1.1.1
Release:        21%{?dist}
Summary:        Utility like top(1) for displaying virtualization stats
License:        GPL-2.0-or-later

%if 0%{?rhel}
# No qemu-kvm on POWER (RHBZ#1946532).
ExcludeArch:    %{power64}
%endif

URL:            http://people.redhat.com/~rjones/virt-top/
Source0:        http://people.redhat.com/~rjones/virt-top/files/%{name}-%{version}.tar.gz
Source1:        http://people.redhat.com/~rjones/virt-top/files/%{name}-%{version}.tar.gz.sig

# Post-process output of CSV file (RHBZ#665817, RHBZ#912020).
Source2:        processcsv.py
Source3:        processcsv.py.pod

# Keyring used to verify tarball signature.
Source4:        libguestfs.keyring

# Adds a link to processcsv to the man page.  This patch is only
# included in RHEL builds.
Patch1:         virt-top-1.0.9-processcsv-documentation.patch

# Fix "Input/output error" in journal (RHBZ#2148798)
Patch2:         0001-virt-top-fix-to-explicitly-disconnect-from-libvirtd.patch

# Fix problem parsing init-file.
Patch3:         0002-virt-top-fix-to-parse-init-file-correctly.patch

# Fix libxml2 2.12.1 build problems.
Patch4:         0003-src-Include-libxml-parser.h.patch

# Fix linking problems on bytecode-only architectures
Patch5:         virt-top-1.1.1-ocaml-bytecode.patch

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  ocaml >= 3.10.2
BuildRequires:  ocaml-ocamldoc
BuildRequires:  ocaml-findlib-devel
# Need the ncurses / ncursesw (--enable-widec) fix.
BuildRequires:  ocaml-curses-devel >= 1.0.3-7
BuildRequires:  ocaml-calendar-devel
BuildRequires:  ocaml-libvirt-devel >= 0.6.1.5
BuildRequires:  ocaml-gettext-devel >= 0.3.3
BuildRequires:  ocaml-fileutils-devel
# For msgfmt:
BuildRequires:  gettext

# Non-OCaml BRs.
BuildRequires:  libvirt-devel
BuildRequires:  libxml2-devel
BuildRequires:  perl-interpreter
BuildRequires:  perl(Pod::Perldoc)
BuildRequires:  gawk
BuildRequires:  gnupg2


%description
virt-top is a 'top(1)'-like utility for showing stats of virtualized
domains.  Many keys and command line options are the same as for
ordinary 'top'.

It uses libvirt so it is capable of showing stats across a variety of
different virtualization systems.


%prep
%{gpgverify} --keyring='%{SOURCE4}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%setup -q

%if 0%{?rhel} >= 6
%patch -P1 -p1
%endif
%patch -P2 -p1
%patch -P3 -p1
%patch -P4 -p1
%ifnarch %{ocaml_native_compiler}
%patch -P5 -p1
%endif

# "ocamlfind byte" has been removed as an alias
sed -i 's/\(OCAMLBEST=\)byte/\1ocamlc/' configure


%build
%configure
make

# Force rebuild of man page.
# There is a missing man_MANS rule, will fix upstream in next version.
rm -f src/virt-top.1
make -C src virt-top.1

%if 0%{?rhel} >= 6
# Build processcsv.py.1.
pod2man -c "Virtualization Support" --release "%{name}-%{version}" \
  %{SOURCE3} > processcsv.py.1
%endif


%install
make DESTDIR=$RPM_BUILD_ROOT install

# Install translations.
%find_lang %{name}

# Install virt-top manpage by hand for now - see above.
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
install -m 0644 src/virt-top.1 $RPM_BUILD_ROOT%{_mandir}/man1

%if 0%{?rhel} >= 6
# Install processcsv.py.
install -m 0755 %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}

# Install processcsv.py(1).
install -m 0644 processcsv.py.1 $RPM_BUILD_ROOT%{_mandir}/man1/
%endif


%files -f %{name}.lang
%doc README TODO
%license COPYING
%{_bindir}/virt-top
%{_mandir}/man1/virt-top.1*
%if 0%{?rhel} >= 6
%{_bindir}/processcsv.py
%{_mandir}/man1/processcsv.py.1*
%endif


%changelog
* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 19 2024 Richard W.M. Jones <rjones@redhat.com> - 1.1.1-20
- OCaml 5.2.0 ppc64le fix

* Thu May 30 2024 Richard W.M. Jones <rjones@redhat.com> - 1.1.1-19
- OCaml 5.2.0 for Fedora 41

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 18 2023 Richard W.M. Jones <rjones@redhat.com> - 1.1.1-17
- OCaml 5.1.1 + s390x code gen fix for Fedora 40

* Tue Dec 12 2023 Richard W.M. Jones <rjones@redhat.com> - 1.1.1-16
- OCaml 5.1.1 rebuild for Fedora 40

* Mon Nov 27 2023 Richard W.M. Jones <rjones@redhat.com> - 1.1.1-15
- Fix build issue with libxml2 2.12.1

* Thu Oct 05 2023 Richard W.M. Jones <rjones@redhat.com> - 1.1.1-14
- OCaml 5.1 rebuild for Fedora 40

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Richard W.M. Jones <rjones@redhat.com> - 1.1.1-12
- OCaml 5.0 rebuild for Fedora 39

* Mon Jul 10 2023 Jerry James <loganjerry@gmail.com> - 1.1.1-11
- OCaml 5.0.0 rebuild
- Add patch to fix linking on bytecode-only architectures
- Update deprecated %%patchN usage
- Use %%license macro

* Mon Jun 05 2023 Richard W.M. Jones <rjones@redhat.com> - 1.1.1-10
- Migrated to SPDX license

* Tue Jan 24 2023 Richard W.M. Jones <rjones@redhat.com> - 1.1.1-9
- Rebuild OCaml packages for F38

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Nov 28 2022 Richard W.M. Jones <rjones@redhat.com> - 1.1.1-7
- Fix "Input/output error" in journal (RHBZ#2148798)

* Tue Oct 18 2022 Richard W.M. Jones <rjones@redhat.com> - 1.1.1-6
- Check tarball signature

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun Jun 19 2022 Richard W.M. Jones <rjones@redhat.com> - 1.1.1-4
- OCaml 4.14.0 rebuild

* Fri Feb 04 2022 Richard W.M. Jones <rjones@redhat.com> - 1.1.1-3
- OCaml 4.13.1 rebuild to remove package notes

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Nov 03 2021 Richard W.M. Jones <rjones@redhat.com> - 1.1.1-1
- New upstream development version 1.1.1
- No longer depends on ocaml-csv, ocaml-extlib or ocaml-xml-light
- Adds new dependency on libxml2

* Tue Oct 05 2021 Richard W.M. Jones <rjones@redhat.com> - 1.1.0-2
- OCaml 4.13.1 build

* Fri Oct 01 2021 Richard W.M. Jones <rjones@redhat.com> - 1.1.0-1
- New upstream development version 1.1.0
- Upstream switched to automake, simplifying the downstream build slightly.
- Remove Changelog file, no longer included upstream.

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.9-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 07 2021 Richard W.M. Jones <rjones@redhat.com> - 1.0.9-20
- Do not include the package on POWER on RHEL 9
  resolves: rhbz#1956935

* Mon Mar  8 2021 Richard W.M. Jones <rjones@redhat.com> - 1.0.9-19
- Bump and rebuild for ocaml-gettext update.

* Tue Mar  2 10:06:37 GMT 2021 Richard W.M. Jones <rjones@redhat.com> - 1.0.9-18
- OCaml 4.12.0 build

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.9-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Sep 01 2020 Richard W.M. Jones <rjones@redhat.com> - 1.0.9-16
- OCaml 4.11.1 rebuild

* Fri Aug 21 2020 Richard W.M. Jones <rjones@redhat.com> - 1.0.9-15
- OCaml 4.11.0 rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.9-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat May 30 2020 Richard W.M. Jones <rjones@redhat.com> - 1.0.9-13
- Rebuild for updated ocaml-extlib (RHBZ#1837823).

* Tue May 05 2020 Richard W.M. Jones <rjones@redhat.com> - 1.0.9-12
- OCaml 4.11.0+dev2-2020-04-22 rebuild

* Tue May  5 2020 Richard W.M. Jones <rjones@redhat.com> - 1.0.9-11
- Fix broken documentation patch (RHEL/ELN only).

* Wed Apr 22 2020 Richard W.M. Jones <rjones@redhat.com> - 1.0.9-10
- OCaml 4.11.0 pre-release attempt 2

* Thu Apr 09 2020 Richard W.M. Jones <rjones@redhat.com> - 1.0.9-9
- Port RHEL 8.3.0 gating test to Fedora.

* Sat Apr 04 2020 Richard W.M. Jones <rjones@redhat.com> - 1.0.9-7
- Update all OCaml dependencies for RPM 4.16.

* Thu Feb 27 2020 Richard W.M. Jones <rjones@redhat.com> - 1.0.9-6
- OCaml 4.10.0 final.

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jan 19 2020 Richard W.M. Jones <rjones@redhat.com> - 1.0.9-4
- OCaml 4.10.0+beta1 rebuild.

* Fri Dec 06 2019 Richard W.M. Jones <rjones@redhat.com> - 1.0.9-3
- OCaml 4.09.0 (final) rebuild.

* Wed Aug 21 2019 Richard W.M. Jones <rjones@redhat.com> - 1.0.9-2
- Rebuild against ocaml-libvirt 0.6.1.5.

* Tue Aug 20 2019 Richard W.M. Jones <rjones@redhat.com> - 1.0.9-1
- New upstream version 1.0.9.
- Remove patches which are upstream and aarch64 build fix.

* Fri Aug 16 2019 Richard W.M. Jones <rjones@redhat.com> - 1.0.8-37
- OCaml 4.08.1 (final) rebuild.

* Thu Aug 01 2019 Richard W.M. Jones <rjones@redhat.com> - 1.0.8-36
- OCaml 4.08.1 (rc2) rebuild.

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.8-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.8-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.8-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Richard W.M. Jones <rjones@redhat.com> - 1.0.8-32
- OCaml 4.07.0 (final) rebuild.

* Wed Jun 20 2018 Richard W.M. Jones <rjones@redhat.com> - 1.0.8-31
- OCaml 4.07.0-rc1 rebuild.

* Wed Mar 28 2018 Richard W.M. Jones <rjones@redhat.com> - 1.0.8-30
- Modify processcsv.py for Python 3.

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.8-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Nov 18 2017 Richard W.M. Jones <rjones@redhat.com> - 1.0.8-28
- OCaml 4.06.0 rebuild.

* Wed Aug 09 2017 Richard W.M. Jones <rjones@redhat.com> - 1.0.8-27
- OCaml 4.05.0 rebuild.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.8-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.8-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 27 2017 Richard W.M. Jones <rjones@redhat.com> - 1.0.8-24
- OCaml 4.04.2 rebuild.

* Sat May 13 2017 Richard W.M. Jones <rjones@redhat.com> - 1.0.8-23
- OCaml 4.04.1 rebuild.

* Tue Mar 28 2017 Richard W.M. Jones <rjones@redhat.com> - 1.0.8-22
- Include all upstream patches since 1.0.8 was released.
- BR ocaml-libvirt with virConnectGetAllDomainStats API.
- Remove execstack hack, no longer needed on any arch.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.8-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Nov 09 2016 Dan Horák <dan@danny.cz> - 1.0.8-20
- remove ExcludeArch

* Sat Nov 05 2016 Richard W.M. Jones <rjones@redhat.com> - 1.0.8-19
- Rebuild for OCaml 4.04.0.
- Kill further instances of -warn-error.

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.8-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jul 28 2015 Richard W.M. Jones <rjones@redhat.com> - 1.0.8-17
- OCaml 4.02.3 rebuild.

* Wed Jun 24 2015 Richard W.M. Jones <rjones@redhat.com> - 1.0.8-16
- ocaml-4.02.2 final rebuild.

* Thu Jun 18 2015 Richard W.M. Jones <rjones@redhat.com> - 1.0.8-15
- ocaml-4.02.2 rebuild.

* Tue Feb 17 2015 Richard W.M. Jones <rjones@redhat.com> - 1.0.8-14
- ocaml-4.02.1 rebuild.

* Sun Aug 31 2014 Richard W.M. Jones <rjones@redhat.com> - 1.0.8-13
- ocaml-4.02.0 final rebuild.

* Sat Aug 23 2014 Richard W.M. Jones <rjones@redhat.com> - 1.0.8-12
- ocaml-4.02.0+rc1 rebuild.

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.8-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Aug 02 2014 Richard W.M. Jones <rjones@redhat.com> - 1.0.8-10
- ocaml-4.02.0-0.8.git10e45753.fc22 rebuild.

* Sat Aug 02 2014 Richard W.M. Jones <rjones@redhat.com> - 1.0.8-9
- Do not warn about immutable strings.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Aug 05 2013 Richard W.M. Jones <rjones@redhat.com> - 1.0.8-7
- Bump and rebuild.

* Mon Jul 29 2013 Richard W.M. Jones <rjones@redhat.com> - 1.0.8-6
- Include processcsv.py script and man page, but on RHEL only
  (RHBZ#665817, RHBZ#912020)
- Clear executable stack flag on PPC, PPC64 (RHBZ#605124).

* Fri Jun 28 2013 Cole Robinson <crobinso@redhat.com> - 1.0.8-5
- Update configure for aarch64 (bz #926701)

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Dec 14 2012 Richard W.M. Jones <rjones@redhat.com> - 1.0.8-3
- Rebuild for OCaml 4.00.1.

* Fri Oct 12 2012 Richard W.M. Jones <rjones@redhat.com> - 1.0.8-2
- New upstream version 1.0.8.
- Requires tiny change to ocaml-libvirt, hence dep bump.
- Clean up the spec file.
- Remove explicit BR ocaml-camomile (not used AFAIK).

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Mar 23 2012 Richard W.M. Jones <rjones@redhat.com> - 1.0.7-2
- Require fixed ocaml-libvirt.

* Tue Mar  6 2012 Richard W.M. Jones <rjones@redhat.com> - 1.0.7-1
- New upstream version 1.0.7.
- Includes true physical CPU reporting (when libvirt supports this).

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Aug 12 2011 Richard W.M. Jones <rjones@redhat.com> - 1.0.6-1
- New upstream version 1.0.6.

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan  6 2011 Richard W.M. Jones <rjones@redhat.com> - 1.0.5-1
- New upstream version 1.0.5.
- Rebuild against OCaml 3.12.0.
- Project website moved to people.redhat.com.
- Remove upstream patches.

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.4-3
- Force rebuild against latest ocaml-gettext 0.3.3 (RHBZ#508197#c10).

* Mon Oct  5 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.4-2
- New upstream release 1.0.4.
- Includes new translations (RHBZ#493799).
- Overall hardware memory is now displayed in CSV file (RHBZ#521785).
- Several fixes to Japanese support (RHBZ#508197).
- Japanese PO file also has bogus plural forms.
- Additional BR on gettext (for msgfmt).

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-3
- Rebuild for OCaml 3.11.0+rc1.

* Tue Oct 21 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-2
- Fix incorrect sources file.
- Remove bogus Plural-Forms line from zh_CN PO file.

* Tue Oct 21 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-1
- New upstream version 1.0.3.

* Mon May 19 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0.1-2
- Use RPM percent-configure.
- Add list of BRs for gettext.
- Use find_lang to find PO files.
- Comment out the OCaml dependency generator.  Not a library so not
  needed.

* Thu May  1 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0.1-1
- New upstream release 1.0.1.
- Don't BR ocaml-gettext-devel, it's not used at the moment.
- Don't gzip the manpage, it happens automatically.
- Add BR libvirt-devel.
- Remove spurious executable bit on COPYING.

* Thu Apr 17 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0.0-2
- New upstream release 1.0.0.
- Force rebuild of manpage.

* Tue Mar 18 2008 Richard W.M. Jones <rjones@redhat.com> - 0.4.1.1-1
- New upstream release 0.4.1.1.
- Move configure to build section.
- Pass RPM_OPT_FLAGS.

* Tue Mar  4 2008 Richard W.M. Jones <rjones@redhat.com> - 0.4.1.0-2
- Fix source URL.
- Install virt-df manpage.

* Tue Mar  4 2008 Richard W.M. Jones <rjones@redhat.com> - 0.4.1.0-1
- New upstream release 0.4.1.0.
- Upstream now requires ocaml-dbus >= 0.06, ocaml-lablgtk >= 2.10.0,
  ocaml-dbus-devel.
- Enable virt-df.

* Sat Mar  1 2008 Richard W.M. Jones <rjones@redhat.com> - 0.4.0.3-3
- Rebuild for ppc64.

* Wed Feb 13 2008 Richard W.M. Jones <rjones@redhat.com> - 0.4.0.3-2
- Add BR gtk2-devel

* Tue Feb 12 2008 Richard W.M. Jones <rjones@redhat.com> - 0.4.0.3-1
- New upstream version 0.4.0.3.
- Rebuild for OCaml 3.10.1.

* Tue Nov 20 2007 Richard W.M. Jones <rjones@redhat.com> - 0.3.3.4-1
- New upstream release 0.3.3.4.
- Upstream website is now http://libvirt.org/ocaml/

* Fri Oct 19 2007 Richard W.M. Jones <rjones@redhat.com> - 0.3.3.0-2
- Mistake: BR is ocaml-calendar-devel.

* Fri Oct 19 2007 Richard W.M. Jones <rjones@redhat.com> - 0.3.3.0-1
- New upstream release 0.3.3.0.
- Added support for virt-df, but disabled it by default.
- +BR ocaml-calendar.

* Mon Sep 24 2007 Richard W.M. Jones <rjones@redhat.com> - 0.3.2.8-1
- New upstream release 0.3.2.8.

* Thu Sep 20 2007 Richard W.M. Jones <rjones@redhat.com> - 0.3.2.7-1
- New upstream release 0.3.2.7.
- Ship the upstream ChangeLog file.

* Thu Sep  6 2007 Richard W.M. Jones <rjones@redhat.com> - 0.3.2.6-2
- Force dependency on ocaml >= 3.10.0-7 which has fixed requires/provides
  scripts.

* Thu Sep  6 2007 Richard W.M. Jones <rjones@redhat.com> - 0.3.2.6-1
- New upstream version 0.3.2.6.

* Wed Aug 29 2007 Richard W.M. Jones <rjones@redhat.com> - 0.3.2.5-1
- New upstream version 0.3.2.5.
- Keep TODO out of the main package, but add (renamed) TODO.libvirt and
  TODO.virt-top to the devel and virt-top packages respectively.
- Add BR gawk.

* Thu Aug 23 2007 Richard W.M. Jones <rjones@redhat.com> - 0.3.2.4-1
- New upstream version 0.3.2.4.

* Thu Aug 23 2007 Richard W.M. Jones <rjones@redhat.com> - 0.3.2.3-2
- build_* macros so we can choose what subpackages to build.

* Thu Aug 23 2007 Richard W.M. Jones <rjones@redhat.com> - 0.3.2.3-1
- Upstream version 0.3.2.3.
- Add missing BR libvirt-devel.

* Wed Aug 22 2007 Richard W.M. Jones <rjones@redhat.com> - 0.3.2.2-1
- Upstream version 0.3.2.2.

* Wed Aug 22 2007 Richard W.M. Jones <rjones@redhat.com> - 0.3.2.1-2
- Fix unclosed if-statement in spec file.

* Wed Aug 22 2007 Richard W.M. Jones <rjones@redhat.com> - 0.3.2.1-1
- Upstream version 0.3.2.1.
- Put HTML documentation in -devel package.

* Mon Aug  6 2007 Richard W.M. Jones <rjones@redhat.com> - 0.3.1.2-1
- Initial RPM release.
