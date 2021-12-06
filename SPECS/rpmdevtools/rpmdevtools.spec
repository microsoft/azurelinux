%global spectool_version 1.0.10

Summary:        RPM Development Tools
Name:           rpmdevtools
Version:        8.10
Release:        13%{?dist}
# rpmdev-setuptree is GPLv2, everything else GPLv2+
License:        GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://pagure.io/rpmdevtools
Source0:        https://releases.pagure.org/rpmdevtools/%{name}-%{version}.tar.xz
# Backports from upstream
Patch0001:      0001-bumpspec-checksig-Avoid-python-3.6-regex-related-dep.patch
Patch0002:      0001-Limit-newVersion-s-re.sub-to-a-single-replacement.patch

BuildArch:      noarch

# help2man, pod2man, *python for creating man pages
BuildRequires:  %{_bindir}/pod2man
BuildRequires:  bash-completion
BuildRequires:  help2man
BuildRequires:  perl-generators
BuildRequires:  python3
BuildRequires:  python3-rpm

Requires:       curl
Requires:       diffutils
Requires:       fakeroot
Requires:       file
Requires:       findutils
Requires:       gawk
Requires:       grep
Requires:       python3-rpm
Requires:       rpm-build >= 4.4.2.3
Requires:       sed
Provides:       spectool = %{spectool_version}

%description
This package contains scripts and to aid in
development of RPM packages.
rpmdev-setuptree    Create RPM build tree within user's home directory
rpmdev-diff         Diff contents of two archives
rpmdev-newspec      Creates new .spec from template
rpmdev-rmdevelrpms  Find (and optionally remove) "development" RPMs
rpmdev-checksig     Check package signatures using alternate RPM keyring
rpminfo             Print information about executables and libraries
rpmdev-md5/sha*     Display checksums of all files in an archive file
rpmdev-vercmp       RPM version comparison checker
spectool            Expand and download sources and patches in specfiles
rpmdev-wipetree     Erase all files within dirs created by rpmdev-setuptree
rpmdev-extract      Extract various archives, "tar xvf" style
rpmdev-bumpspec     Bump revision in specfile
...and many more.

%prep
%autosetup -p1
grep -lF "%{_bindir}/python " * \
| xargs sed -i -e "s|%{_bindir}/python |%{_bindir}/python3 |"


%build
%configure --libdir=%{_libdir}
%make_build

%install
%make_install

echo %%{_datadir}/bash-completion > %{name}.files
[ -d %{buildroot}%{_sysconfdir}/bash_completion.d ] && \
echo %%{_sysconfdir}/bash_completion.d > %{name}.files


%files -f %{name}.files
%license COPYING
%doc NEWS
%config(noreplace) %{_sysconfdir}/rpmdevtools/
%{_datadir}/rpmdevtools/
%{_bindir}/*
%{_mandir}/man[18]/*.[18]*

%changelog
* Mon Dec 06 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 8.10-13
- License verified.

* Tue Jun 22 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 8.10-12
- Removing option to build with Python 2.
- Replacing dependency on 'rpm-python3' with 'python3-rpm'.

* Mon Nov 02 2020 Joe Schmitt <joschmit@microsoft.com> - 8.10-11
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Remove emacs dependency and support.
- Enable python3 option.

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 8.10-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 8.10-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 8.10-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Nov 28 2018 Neal Gompa <ngompa13@gmail.com> - 8.10-7
- Fix regex substitution issues with Python 3.7 (rhbz#1651954)

* Sun Sep 16 2018 Neal Gompa <ngompa13@gmail.com> - 8.10-6
- Fix regex related deprecation warnings (rhbz#1598089)

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 8.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 8.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 8.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 8.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Jan 14 2017 Ville Skyttä <ville.skytta@iki.fi> - 8.10-1
- Update to 8.10

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 8.9-2
- Rebuild for Python 3.6

* Sat Jun 25 2016 Ville Skyttä <ville.skytta@iki.fi> - 8.9-1
- Update to 8.9

* Sat Jun 25 2016 Ville Skyttä <ville.skytta@iki.fi> - 8.8-1
- Update to 8.8

* Fri Jun 24 2016 Petr Písař <ppisar@redhat.com>
- Add new mandatory perl build deps

* Thu Jun 23 2016 Ville Skyttä <ville.skytta@iki.fi> - 8.7-1
- Update to 8.7
- Specfile cleanups

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 8.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun  5 2015 Ville Skyttä <ville.skytta@iki.fi> - 8.6-2
- Use python3 on > F-22

* Sun May 10 2015 Ville Skyttä <ville.skytta@iki.fi> - 8.6-1
- Update to 8.6

* Mon Oct 20 2014 Ville Skyttä <ville.skytta@iki.fi> - 8.5-1
- Update to 8.5
- Mark COPYING as %%license where applicable

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Oct 17 2013 Ville Skyttä <ville.skytta@iki.fi> - 8.4-2
- Do not require devscripts in any scenario.

* Mon Oct  7 2013 Ville Skyttä <ville.skytta@iki.fi> - 8.4-1
- Update to 8.4.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 8.3-4
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 16 2012 Thomas Woerner <twoerner@redhat.com> - 8.3-2
- xemacs is not available on RHEL (RHBZ#866841)

* Sun Sep  2 2012 Ville Skyttä <ville.skytta@iki.fi> - 8.3-1
- Update to 8.3.
- Drop specfile constructs no longer needed with Fedora's rpm.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Nov 12 2011 Ville Skyttä <ville.skytta@iki.fi> - 8.2-1
- Update to 8.2.

* Tue Apr 26 2011 Ville Skyttä <ville.skytta@iki.fi> - 8.1-1
- Update to 8.1.

* Tue Mar  1 2011 Ville Skyttä <ville.skytta@iki.fi> - 8.0-3
- Require xemacs-filesystem on F-15+ (#672093).

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Feb  6 2011 Ville Skyttä <ville.skytta@iki.fi> - 8.0-1
- Update to 8.0, fixes #519061 and #657594.

* Mon Sep 27 2010 Ville Skyttä <ville.skytta@iki.fi> - 7.10-1
- Update to 7.10, fixes #595135 and #619867.
- Patch spectool to work with specfiles containing Icon or BuildArchitectures
  (#637000).

* Thu May 20 2010 Ville Skyttä <ville.skytta@iki.fi> - 7.9-1
- Update to 7.9, fixes #588313 and #589705.

* Fri Apr 16 2010 Ville Skyttä <ville.skytta@iki.fi> - 7.8-2
- Require %%{_bindir}/man instead of man (#582932).

* Tue Feb 16 2010 Ville Skyttä <ville.skytta@iki.fi> - 7.8-1
- Update to 7.8, fixes #562316.

* Tue Feb  2 2010 Ville Skyttä <ville.skytta@iki.fi> - 7.7-1
- Update to 7.7, fixes #558263.

* Mon Dec  7 2009 Ville Skyttä <ville.skytta@iki.fi> - 7.6-1
- Update to 7.6, fixes #528907.

* Thu Sep 17 2009 Ville Skyttä <ville.skytta@iki.fi> - 7.5-1
- Update to 7.5, fixes #502403.

* Fri Aug 21 2009 Ville Skyttä <ville.skytta@iki.fi> - 7.4-1
- Update to 7.4, fixes #215927 and #466353.
- Patch spectool to make -s and -p to work as documented (Todd Zullinger).

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon May 25 2009 Ville Skyttä <ville.skytta@iki.fi> - 7.3-1
- Release 7.3.

* Sat May 23 2009 Ville Skyttä <ville.skytta@iki.fi>
- Add rpmdev-packager - script for getting rpm packager info.
- Use rpmdev-packager in rpmdev-bumpspec and rpmdev-init.el.
- Fix rpmdev-extract MIME type comparisons with file(1) output containing
  parameters.

* Wed May 20 2009 Ville Skyttä <ville.skytta@iki.fi> - 7.2-1
- Release 7.2.

* Sun May  3 2009 Ville Skyttä <ville.skytta@iki.fi>
- Add dummy spec template for ad-hoc testing.

* Sat May  2 2009 Ville Skyttä <ville.skytta@iki.fi>
- Improve newspec/newinit when only "-o foo" argument is given (#498588,
  thanks to Edwin ten Brink).
- Try to get packager mail address for *Emacs rpm-spec-mode from ~/.fedora.cert
  if rpm-spec-user-mail-address is not set.
- Add xz support to rpmdev-extract.

* Sat Apr 18 2009 Ville Skyttä <ville.skytta@iki.fi>
- Make bumpspec's use of "head" POSIX compliant.

* Thu Apr 16 2009 Ville Skyttä <ville.skytta@iki.fi>
- Add rpmdev-newinit for easier access to the init script template, move the
  template to %%{_sysconfdir}/rpmdevtools, improve reload action example.

* Tue Apr  7 2009 Ville Skyttä <ville.skytta@iki.fi>
- Speed up rpmls bash completion.

* Sat Apr  4 2009 Ville Skyttä <ville.skytta@iki.fi> - 7.1-1
- 7.1.
- Make rpmdev-md5 and friends work on non-srpm package files too.

* Sun Mar 15 2009 Ville Skyttä <ville.skytta@iki.fi>
- Add bash completion.

* Mon Mar  9 2009 Ville Skyttä <ville.skytta@iki.fi>
- Add query format option to rmdevelrpms, sort output by NEVRA.

* Sun Feb 22 2009 Ville Skyttä <ville.skytta@iki.fi>
- Use %%global instead of %%define in spec templates.
- Handle %%global in addition to %%define in rpmdev-bumpspec.

* Mon Jan 26 2009 Ville Skyttä <ville.skytta@iki.fi>
- Add result dependent exit statuses to rpmdev-vercmp.

* Fri Dec 26 2008 Ville Skyttä <ville.skytta@iki.fi>
- Add minimum version to rpm-python dependency (for rpmdev-bumpspec).

* Fri Dec 26 2008 Ville Skyttä <ville.skytta@iki.fi> - 7.0-1
- 7.0.
- Drop fonts spec template, adapt to new ones from Fedora fonts SIG (#477055).
- Add man page for rpmdev-newspec.

* Tue Dec 16 2008 Ville Skyttä <ville.skytta@iki.fi>
- Add imake and intltool to internal list of devel packages in rmdevelrpms.

* Sat Dec 13 2008 Ville Skyttä <ville.skytta@iki.fi>
- Add rpmdev-sha*/*sum companions to rpmdev-md5 (ticket #7).

* Wed Nov 26 2008 Ville Skyttä <ville.skytta@iki.fi>
- Add vamp-plugin-sdk to internal list of non-devel packages in rmdevelrpms
  (#472641, Michael Schwendt).

* Thu Nov 20 2008 Ville Skyttä <ville.skytta@iki.fi>
- Drop "minimal buildroot" dependencies.
- Drop fedora-rpmdevtools Obsoletes.

* Mon Oct 13 2008 Ville Skyttä <ville.skytta@iki.fi>
- Show available types in rpmdev-newspec --help (ticket #6, Todd Zullinger).

* Fri Sep 26 2008 Ville Skyttä <ville.skytta@iki.fi>
- Add -r/--rightmost option to rpmdev-bumpspec (ticket #1, Thorsten Leemhuis).
- Add %%packager from rpm config to the set of defaults for rpmdev-bumpspec's
  user string.

* Thu Sep 25 2008 Ville Skyttä <ville.skytta@iki.fi>
- Bring rpmdev-bumpspec copyright holder closer to truth (Michael Schwendt).

* Mon Sep 22 2008 Ville Skyttä <ville.skytta@iki.fi>
- Switch to lzma compressed tarball.

* Sun Sep  7 2008 Ville Skyttä <ville.skytta@iki.fi>
- Improve arch specific %%files in perl spec template (#461177, Chris Weyl).

* Sun Aug  3 2008 Ville Skyttä <ville.skytta@iki.fi> - 6.7-1
- 6.7.
- Make rpmdev-diff, rpmdev-md5 and rpminfo honor TMPDIR.

* Sat Apr 26 2008 Ville Skyttä <ville.skytta@iki.fi>
- Make rpmls work with URLs.

* Sun Apr 20 2008 Ville Skyttä <ville.skytta@iki.fi>
- Include rpm arch in dir names created by rpmdev-extract (#443266).

* Fri Apr 18 2008 Ville Skyttä <ville.skytta@iki.fi>
- Remove duplicate "reload" from case block in init script template.
- Fix exit status of "reload" in case service is not running in init
  script template (#442993).

* Thu Mar 27 2008 Ville Skyttä <ville.skytta@iki.fi> - 6.6-1
- Fix man page generation.

* Wed Mar 26 2008 Ville Skyttä <ville.skytta@iki.fi> - 6.5-1
- 6.5.

* Sun Mar 23 2008 Ville Skyttä <ville.skytta@iki.fi>
- Generate man pages at build time.

* Sat Mar 22 2008 Ville Skyttä <ville.skytta@iki.fi>
- Remove libgcj-devel and zlib-devel from rmdevelrpms' internal exclusion
  list, they're not essential on non-devel systems any more.

* Mon Mar 17 2008 Ville Skyttä <ville.skytta@iki.fi>
- Include ocaml spec template.

* Tue Mar 11 2008 Ville Skyttä <ville.skytta@iki.fi>
- Include Michael Schwendt's bumpspecfile.py (as rpmdev-bumpspec).

* Tue Feb 12 2008 Ville Skyttä <ville.skytta@iki.fi>
- Sync with qa-robot upstream.
- Update spectool to 1.0.10.

* Sun Feb  3 2008 Ville Skyttä <ville.skytta@iki.fi>
- Add support for 7-zip, lzma and lzo in rpmdev-extract.

* Fri Feb  1 2008 Ville Skyttä <ville.skytta@iki.fi>
- Add ';;' to the init script template's reload action.

* Sat Dec  8 2007 Ville Skyttä <ville.skytta@iki.fi>
- Add fonts spec template from the Fedora Fonts SIG (#407781).
- Add option to use macro style instead of shell style variables to newspec.
- Prefer ~/.config/rpmdevtools/rmdevelrpms.conf over ~/.rmdevelrpmsrc in
  rmdevelrpms.

* Fri Oct 12 2007 Lubomir Kundrak <lkundrak@redhat.com> - 6.4-1
- Import the previous fix into CVS to resync, bump version

* Fri Oct 12 2007 Lubomir Kundrak <lkundrak@redhat.com> - 6.3-1
- Fix paths in qa-robot tools

* Sat Sep  8 2007 Ville Skyttä <ville.skytta@iki.fi> - 6.2-1
- Sync deps with Fedora's new "assumed present in buildroots" packages list.

* Thu Sep  6 2007 Ville Skyttä <ville.skytta@iki.fi>
- Init script template cleanups.

* Tue Aug 28 2007 Ville Skyttä <ville.skytta@iki.fi>
- Update rpminfo to version 2004-07-07-02.

* Fri Aug 10 2007 Ville Skyttä <ville.skytta@iki.fi> - 6.1-1
- Sync COPYING with http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

* Mon Aug  6 2007 Ville Skyttä <ville.skytta@iki.fi>
- Work around #250990 in rpmls and rpmdev-extract.
- Clarify copyright info of rpmdev-* and rpmls.

* Sat Jul  7 2007 Ville Skyttä <ville.skytta@iki.fi>
- Fix Epoch handling in the 2-arg form of rpmdev-vercmp with yum < 3.1.2.
- The long form of the list option in rmdevelrpms is --list-only, not --list.

* Thu Jul  5 2007 Ville Skyttä <ville.skytta@iki.fi> - 6.0-1
- Remove check-{buildroot,rpaths*}, now included in rpm-build >= 4.4.2.1.
- Drop explicit dependency on patch, pulled in by recent rpm-build.
- Add cmake and scons to default devel package list in rpmdev-rmdevelrpms.
- Add LSB comment block to init script template.

* Wed Jun 27 2007 Ville Skyttä <ville.skytta@iki.fi>
- Add 2-argument form for comparing EVR strings to rpmdev-vercmp
  (available only if rpmUtils.miscutils is available).

* Sat Jun 16 2007 Ville Skyttä <ville.skytta@iki.fi>
- Include rpmsodiff and dependencies (rpmargs, rpmelfsym, rpmfile, rpmpeek,
  rpmsoname) from ALT Linux's qa-robot package.
- Include rpmls (#213778).

* Fri Jun 15 2007 Ville Skyttä <ville.skytta@iki.fi>
- Update spectool to 1.0.9 (#243731).

* Wed Apr 11 2007 Ville Skyttä <ville.skytta@iki.fi>
- Add --list-only option to rmdevelrpms (Thorsten Leemhuis).

* Tue Mar 13 2007 Ville Skyttä <ville.skytta@iki.fi>
- BR perl(ExtUtils::MakeMaker) by default in perl spec template.
- Drop deprecated backwards compatibility with fedora-rpmdevtools.
- Update URL.

* Wed Nov  8 2006 Ville Skyttä <ville.skytta@iki.fi>
- Arch-qualify output of matched packages in rmdevelrpms and allow
  arch-qualified packages in the config file.

* Wed Oct 25 2006 Ville Skyttä <ville.skytta@iki.fi> - 5.3-1
- Update spectool to 1.0.8, fixes #212108.

* Mon Oct  2 2006 Ville Skyttä <ville.skytta@iki.fi> - 5.2-1
- Skip *.jar.so.debug in check-buildroot (#208903).
- Treat yasm and *-static as devel packages in rmdevelrpms.

* Sat Sep  9 2006 Ville Skyttä <ville.skytta@iki.fi> - 5.1-1
- Re-add PHP PEAR spec template, more improvements to it (#198706,
  Christopher Stone, Remi Collet).

* Tue Aug 22 2006 Ville Skyttä <ville.skytta@iki.fi> - 5.0-2
- Migrate rmdevelrpms config when upgrading from fedora-rpmdevtools.

* Sun Aug 20 2006 Ville Skyttä <ville.skytta@iki.fi> - 5.0-1
- Re-rename almost everything to rpmdev-*, with backwards compat symlinks.
- Don't encourage %%ghost'ing *.pyo in Python spec template, add some comments.
- Drop PHP PEAR spec template, it's not ready yet.

* Wed Aug  2 2006 Ville Skyttä <ville.skytta@iki.fi>
- Treat *-sdk as devel packages in rmdevelrpms (#199909).
- Don't assume compface is a devel package in rmdevelrpms.

* Thu Jul 20 2006 Ville Skyttä <ville.skytta@iki.fi>
- Mark things that are not needed for noarch module packages in the Perl
  spec template.

* Wed Jul 19 2006 Ville Skyttä <ville.skytta@iki.fi>
- Move option arguments to "find" before non-option ones in Perl spec template.
- Drop python-abi dependency from Python spec template (#189947).

* Tue Jul 18 2006 Ville Skyttä <ville.skytta@iki.fi>
- Add PHP PEAR spec template (#198706, Christopher Stone).

* Mon Jul 17 2006 Ville Skyttä <ville.skytta@iki.fi>
- Drop fedora- prefix everywhere, add backcompat symlinks for execubtables.
- Move %%{_sysconfdir}/fedora to %%{_sysconfdir}/rpmdevtools and
  %%{_datadir}/fedora to %%{_datadir}/rpmdevtools.
- Move spec templates to %%{_sysconfdir}/rpmdevtools, mark as config.
- Bump version to 5.0.

* Sun Jul 16 2006 Ville Skyttä <ville.skytta@iki.fi>
- Drop fedora-kmodhelper.
- Drop fedora-installdevkeys and GPG keys, modify rpmchecksig to use
  the system rpmdb.

* Sat Jul 15 2006 Ville Skyttä <ville.skytta@iki.fi>
- Sort rmdevelrpms' output.

* Fri Jul  7 2006 Ville Skyttä <ville.skytta@iki.fi>
- Improve ruby spec template (#180066, David Lutterkort).

* Mon Jun  5 2006 Ville Skyttä <ville.skytta@iki.fi>
- Add manual pages for rmdevelrpms, diffarchive and extract.
- Trim pre-2005 changelog entries.
- Autotoolize source tree.

* Tue May 16 2006 Ville Skyttä <ville.skytta@iki.fi> - 1.6-1
- Add spec template for library packages (#185606, Ignacio Vazquez-Abrams).

* Sun Feb 26 2006 Ville Skyttä <ville.skytta@iki.fi> - 1.5-1
- Improve diffarchive and extract error messages.

* Fri Feb 24 2006 Ville Skyttä <ville.skytta@iki.fi>
- Update spectool to 1.0.7 (#162253).

* Thu Feb  9 2006 Ville Skyttä <ville.skytta@iki.fi>
- Add file(1) based archive type detection to fedora-extract.

* Wed Feb  8 2006 Ville Skyttä <ville.skytta@iki.fi>
- Add "diff file lists only" option to diffarchive.

* Sun Feb  5 2006 Ville Skyttä <ville.skytta@iki.fi>
- Add Ruby spec template (#180066, Oliver Andrich) and make newrpmspec
  use it for ruby-*.

* Sat Feb  4 2006 Ville Skyttä <ville.skytta@iki.fi> - 1.4-2
- Fix rpath checker tests with bash 3.1 (#178636, Enrico Scholz).

* Fri Dec 30 2005 Ville Skyttä <ville.skytta@iki.fi> - 1.4-1
- Update spectool to 1.0.6 (#176521).

* Wed Dec 28 2005 Ville Skyttä <ville.skytta@iki.fi>
- Update spectool to 1.0.5 (#162253), require wget for it.
- Add disttags to spec templates.

* Thu Oct 27 2005 Ville Skyttä <ville.skytta@iki.fi> - 1.3-1
- check-rpaths-worker: detect when RPATH references the parent directory
  of an absolute path (#169298, Enrico Scholz).
- Add regression test for check-rpaths* (#169298, Enrico Scholz).
- Honor user's indent-tabs-mode setting in fedora-init.el (#170902).

* Fri Oct  7 2005 Ville Skyttä <ville.skytta@iki.fi> - 1.2-1
- check-buildroot: grep for buildroot as a fixed string, not a regexp.
- Update FSF's address in copyright notices.
- check-rpaths-worker: allow multiple $ORIGIN paths in an RPATH and allow
  RPATHs which are relative to $ORIGIN (#169298, Enrico Scholz).
- check-rpaths-worker: give out an hint about usage and the detected issues
  at the first detected error (Enrico Scholz).
- Remove some redundancy from the Perl spec template.
- Teach fedora-newrpmspec to detect and use different specfile variants.
- Use fedora-newrpmspec in fedora-init.el.

* Fri Jul  8 2005 Ville Skyttä <ville.skytta@iki.fi> - 1.1-1
- Drop more pre-FC2 compat stuff from Perl spec template.
- Treat gcc-gfortran as a devel package in rmdevelrpms.
- Drop fedora.us GPG key.

* Thu Mar 24 2005 Ville Skyttä <ville.skytta@iki.fi> - 1.0-1
- Make fedora-diffarchive work better with archives containing dirs without
  read/execute permissions.
- Sync "Epoch: 0" drops with Fedora Extras CVS.
- Include Nils Philippsen's spectool.
- Own (%%ghost'd) more dirs from the site-lisp dir hierarchies.
- Drop trigger support pre-FC2 Emacs and XEmacs packages.
- Drop rpm-spec-mode.el patch, no longer needed for FC2 Emacs and later.
- Update URLs.
- Drop developer GPG keys from the package, add Fedora Extras key.
- Drop fedora-pkgannfmt, it's no longer relevant.
- Remove pre-FC2 compatibility stuff from Perl spec template.
- Don't try to remove gcc-java and related packages by default in rmdevelrpms.
- Remove "full featured" spec template, convert newrpmspec to use -minimal.

* Sun Feb  6 2005 Ville Skyttä <ville.skytta@iki.fi> - 0:0.3.1-1
- Make buildrpmtree and wipebuildtree less dependent on a specific
  configuration (#147014, Ignacio Vazquez-Abrams).

* Tue Jan 18 2005 Ville Skyttä <ville.skytta@iki.fi> - 0:0.3.0-1
- Remove 0.fdr. prefixes and epoch 0's from all spec templates.
- Add try-restart action to init script template.
- Remove deprecated fedora-diffrpm and fedora-unrpm.
- Install check-* to %%{_prefix}/lib/rpm instead of %%{_libdir}/rpm (bug 2351).
- Check both %%{_prefix}/lib and %%{_prefix}/lib64 in the xemacs trigger.
- Update rpminfo to 2004-07-07-01 and include it in the tarball.
