Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)
%global debug_package %{nil}

Name:           virt-top
Version:        1.0.9
Release:        7%{?dist}
Summary:        Utility like top(1) for displaying virtualization stats
License:        GPLv2+

URL:            https://people.redhat.com/~rjones/virt-top/
Source0:        https://people.redhat.com/~rjones/virt-top/files/%{name}-%{version}.tar.gz

# Post-process output of CSV file (RHBZ#665817, RHBZ#912020).
Source1:        processcsv.py
Source2:        processcsv.py.pod

Patch0:         virt-top-1.0.4-processcsv-documentation.patch

# Upstream patch to fix FTBFS with ocaml libvirt 0.6.1.5.
Patch1:         0001-libvirt-Handle-VIR_DOMAIN_PMSUSPENDED-state.patch

BuildRequires:  ocaml >= 3.10.2
BuildRequires:  ocaml-ocamldoc
BuildRequires:  ocaml-findlib-devel
# Need the ncurses / ncursesw (--enable-widec) fix.
BuildRequires:  ocaml-curses-devel >= 1.0.3-7
BuildRequires:  ocaml-extlib-devel
BuildRequires:  ocaml-xml-light-devel
BuildRequires:  ocaml-csv-devel
BuildRequires:  ocaml-calendar-devel
BuildRequires:  ocaml-libvirt-devel >= 0.6.1.5

# Tortuous list of BRs for gettext.
BuildRequires:  ocaml-gettext-devel >= 0.3.3
BuildRequires:  ocaml-fileutils-devel
# For msgfmt:
BuildRequires:  gettext

# Non-OCaml BRs.
BuildRequires:  libvirt-devel
BuildRequires:  perl-interpreter
BuildRequires:  perl(Pod::Perldoc)
BuildRequires:  gawk


%description
virt-top is a 'top(1)'-like utility for showing stats of virtualized
domains.  Many keys and command line options are the same as for
ordinary 'top'.

It uses libvirt so it is capable of showing stats across a variety of
different virtualization systems.


%prep
%setup -q

%if 0%{?rhel} >= 6
%patch 0 -p1
%endif

%patch 1 -p1


%build
%configure
make all
%if %opt
make opt
strip src/virt-top.opt
%endif

# Build translations.
make -C po

# Force rebuild of man page.
rm -f src/virt-top.1
make -C src virt-top.1

%if 0%{?rhel} >= 6
# Build processcsv.py.1.
pod2man -c "Virtualization Support" --release "%{name}-%{version}" \
  %{SOURCE2} > processcsv.py.1
%endif


%install
make DESTDIR=$RPM_BUILD_ROOT install

# Install translations.
mkdir -p $RPM_BUILD_ROOT%{_datadir}/locale
make -C po install PODIR="$RPM_BUILD_ROOT%{_datadir}/locale"
%find_lang %{name}

# Install virt-top manpage by hand for now.
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
install -m 0644 src/virt-top.1 $RPM_BUILD_ROOT%{_mandir}/man1

%if 0%{?rhel} >= 6
# Install processcsv.py.
install -m 0755 %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}

# Install processcsv.py(1).
install -m 0644 processcsv.py.1 $RPM_BUILD_ROOT%{_mandir}/man1/
%endif


%files -f %{name}.lang
%doc COPYING README TODO ChangeLog
%{_bindir}/virt-top
%{_mandir}/man1/virt-top.1*
%if 0%{?rhel} >= 6
%{_bindir}/processcsv.py
%{_mandir}/man1/processcsv.py.1*
%endif


%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.9-7
- Switching to using full number for the 'Release' tag.
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Feb 28 2020 Richard W.M. Jones <rjones@redhat.com> - 1.0.9-6.1
- OCaml 4.10.0 final (Fedora 32).

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
- Upstream website is now https://libvirt.org/ocaml/

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
