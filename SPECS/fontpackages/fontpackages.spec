%global spectemplatedir %{_sysconfdir}/rpmdevtools/
%global ftcgtemplatedir %{_datadir}/fontconfig/templates/
%global rpmmacrodir     %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d/)

# Use the same directory of the main package for subpackage licence and docs
%global _docdir_fmt %{name}

Summary:        Common directory and macro definitions used by font packages
Name:           fontpackages
Version:        1.44
Release:        29%{?dist}
# Mostly means the scriptlets inserted via this package do not change the
# license of the packages they're inserted in.
License:        LGPLv3+
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/pnemade/fontpackages
Source0:        https://github.com/pnemade/fontpackages/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         dnf.patch
Patch1:         %{name}-drop-fccache.patch
Patch2:         %{name}-add-ghost-uuid.patch

BuildArch:      noarch

BuildRequires:  perl-generators

%description
This package contains the basic directory layout, spec templates, rpm macros
and other materials used to create font packages.

%package filesystem
Summary:        Directories used by font packages
License:        Public Domain

%description filesystem
This package contains the basic directory layout used by font packages,
including the correct permissions for the directories.

%package devel
Summary:        Templates and macros used to create font packages
License:        LGPLv3+

Requires:       %{name}-filesystem = %{version}-%{release}
Requires:       fontconfig
Requires:       rpmdevtools

%description devel
This package contains spec templates, rpm macros and other materials used to
create font packages.

%prep
%autosetup -p1

sed -i 's|%{_bindir}/fedoradev-pkgowners|""|g' bin/repo-font-audit

# Drop obosolete %defattr (#1047031)
sed -i '/^%%defattr/d' rpm/macros.fonts

%build
sed -i "s|^DATADIR\([[:space:]]*\)\?=\(.*\)$|DATADIR=%{_datadir}/%{name}|g" \
  bin/repo-font-audit bin/compare-repo-font-audit

%install
# Pull macros out of macros.fonts and emulate them during install
for dir in fontbasedir        fontconfig_masterdir \
           fontconfig_confdir fontconfig_templatedir ; do
  export _${dir}=$(rpm --eval $(grep -E "^%{_}${dir}\b" \
    rpm/macros.fonts | gawk '{ print $2 }'))
done

install -m 0755 -d %{buildroot}${_fontbasedir} \
                   %{buildroot}${_fontconfig_masterdir} \
                   %{buildroot}${_fontconfig_confdir} \
                   %{buildroot}${_fontconfig_templatedir} \
                   %{buildroot}%{spectemplatedir} \
                   %{buildroot}%{rpmmacrodir} \
                   %{buildroot}%{_datadir}/fontconfig/templates \
                   %{buildroot}%{_datadir}/%{name}
install -m 0644 -p spec-templates/*.spec       %{buildroot}%{spectemplatedir}
install -m 0644 -p fontconfig-templates/*      %{buildroot}%{ftcgtemplatedir}
install -m 0644 -p rpm/macros*                 %{buildroot}%{rpmmacrodir}

cat <<EOF > %{name}-%{version}.files
%dir ${_fontbasedir}
%dir ${_fontconfig_masterdir}
%dir ${_fontconfig_confdir}
%dir ${_fontconfig_templatedir}
%ghost ${_fontbasedir}/.uuid
EOF

%files filesystem -f %{name}-%{version}.files
%dir %{_datadir}/fontconfig

%files devel
%license license.txt
%doc readme.txt
%config(noreplace) %{spectemplatedir}/*.spec
%{rpmmacrodir}/macros*
%dir %{ftcgtemplatedir}
%{ftcgtemplatedir}/*conf
%{ftcgtemplatedir}/*txt

%changelog
* Mon Feb 12 2024 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 1.44-29
- Added compatibility flag to createrepo command in the patch.

* Thu Dec 02 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.44-28
- Removing the "*-tools" subpackage.
- License verified.

* Mon Nov 22 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.44-27
- Removing dependency on "fedora-packager".

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.44-26
- Initial CBL-Mariner import from Fedora 31 (license: MIT).
- Remove 'fontforge' from run-time dependencies for the 'tools' subpackage.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.44-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Feb 06 2019 Akira TAGOH <tagoh@redhat.com> - 1.44-24
- Fix a typo.

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.44-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Oct 23 2018 Akira TAGOH <tagoh@redhat.com>
- Add .uuid as ghost file.

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.44-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Apr 14 2018 Parag Nemade <pnemade AT fedoraproject DOT org> - 1.44-21
- Drop yum-utils conditionals as we don't need it anymore
- use %%autosetup
- Drop Group: tag

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.44-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.44-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.44-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.44-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 21 2016 Dan Horák <dan[at]danny.cz> - 1.44-16
- fix conditional

* Mon Sep  7 2015 Akira TAGOH <tagoh@redhat.com> - 1.44-15
- Drop fc-cache from %%post/un in rpm macro.

* Tue Aug 18 2015 Parag Nemade <pnemade AT fedoraproject DOT org> - 1.44-14
- Port yum to dnf patch by Michael Mráka (rh#1156554)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.44-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri May 29 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.44-12
- Drop obsolete defattr stanzas (#1047031)

* Wed Mar  4 2015 Ville Skyttä <ville.skytta@iki.fi> - 1.44-11
- Install macros to %%{_rpmconfigdir}/macros.d where available (#1074274)
- Fix bogus date in %%changelog

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.44-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.44-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 1.44-8
- Perl 5.18 rebuild

* Sat Mar 09 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.44-7
- Remove %%config from %%{_sysconfdir}/rpm/macros.*
  (https://fedorahosted.org/fpc/ticket/259).

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.44-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.44-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 22 2012 Parag <panemade AT fedoraproject DOT org> - 1.44-4
- Resolves:rh#761409:remove fedora-packager dependency from -tools in RHEL

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.44-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.44-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jun 13 2010 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.44-1
— Cleanup release

* Fri May 28 2010 Akira TAGOH <tagoh@redhat.com>
- 1.42-2
— Get rid of binding="same" from l10n-font-template.conf (#578015)

* Sat Feb 13 2010 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.42-1
— Update mailing list references

* Tue Dec 01 2009 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.41-1
— Bugfix release

* Sat Nov 28 2009 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.40-1
— Bugfix release

* Mon Nov 23 2009 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.35-1

* Sun Nov 22 2009 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.34-1
— compare-repo-font-audit: make output more comprehensive

* Sat Nov 21 2009 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.33-1
— repo-font-audit: add ancilliary script to compare the results of two
  different runs
- 1.32-1
— repo-font-audit: add test for core fonts direct use
— repo-font-audit: replace font naming tests by a more comprehensive one
  (in a separate utility)
— repo-font-audit: add fedora packager detection
— repo-font-audit: parallelize (at the cost of more filesystem space use)
— repo-font-audit: misc output and reliability fixes

* Sun Nov 1 2009 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.31-2
— add yum-utils to deps
- 1.31-1
— Rework repo-font-audit messages based on packager feedback

* Thu Oct 29 2009 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.30-1
— Bugfix release

* Tue Oct 27 2009 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.29-1
— Split out tools as repo-font-audit requirements grow

* Mon Oct 19 2009 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.28-1
— Rework repo-font-audit to also generate individual packager nagmails

* Mon Sep 28 2009 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.27-1
— Brownpaper bag release ×2

* Sun Sep 27 2009 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.26-1
— Brownpaper bag release
- 1.25-1
– Add short test summary to repo-font-audit

* Sat Sep 26 2009 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.24-1
– improve repo-font-audit (make WWS check more accurate, support file://
  local repositories…)

* Sun Sep 13 2009 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.23-1
— cleanups + add merging/remapping templates

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- 1.22-2
— Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jun 20 2009 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.22-1
– workaround rpm eating end-of-line after %%_font_pkg calls
– add script to audit font sanity of yum repositories

* Tue Jun 2 2009 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.21-1
— try to handle more corner naming cases in lua macro – expect some fallout
  if your spec uses weird naming

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- 1.20-2
— Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.20-1
— global-ization

* Mon Feb 16 2009 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.19-3
— remove workaround and explicit version checks
- 1.19-2
— workaround the fact koji is not ready yet
- 1.19-1
— Add a fontconfig dep to -devel so font autoprovides work (bz#485702)
— Drop duplicated group declarations, rpm has been fixed (bz#470714)
— Add partial templates for fonts subpackages of non-font source packages
— Make them noarch (https://fedoraproject.org/wiki/Features/NoarchSubpackages)

* Thu Feb 5 2009 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.18-1
✓ Panu wants autoprovides in rpm proper, drop it
✓ Guidelines people are ok with multiple ownership of directories, make the
  fonts macro auto-own the directory font files are put into

* Sat Jan 31 2009 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.17-1
⁇ Tweak and complete documentation
☤ Merge the autoprovides stuff and try to make it actually work

* Tue Jan 27 2009 Richard Hughes <rhughes@redhat.com>
- 1.16-2
- Add fontconfig.prov and macros.fontconfig so that we can automatically
  generate font provides for packages at build time.
  This lets us do some cool things with PackageKit in the future.

* Wed Jan 21 2009 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.16-1

* Thu Jan 15 2009 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.15-1
➜ lua-ize the main macro

* Wed Jan 14 2009 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.14-1
➽ Update for subpackage naming changes requested by FPC

* Mon Dec 22 2008 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.13-1
⟃ Add another directory to avoid depending on unowned stuff
❤ use it to put the fontconfig examples in a better place

* Sun Dec 21 2008 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.12-2
⌂ Change homepage

* Fri Dec 19 2008 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.12-1
☺ Add another macro to allow building fontconfig without cycling

* Wed Dec 10 2008 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.11-1
☺ Add actual fedorahosted references

* Sun Nov 23 2008 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.10-1
☺ renamed to “fontpackages”

* Fri Nov 14 2008 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.9-1
☺ fix and complete fontconfig doc
- 1.8-1
☺ simplify multi spec template: codify general case
- 1.7-1
☺ split fontconfig template documentation is separate files
- 1.6-1
☺ simplify spec templates
- 1.5-1
☺ use ".conf" extension for fontconfig templates
- 1.4-1
☺ small multi spec template fix

* Wed Nov 12 2008 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.3-1
☺ remove trailing slashes in directory macros

* Tue Nov 11 2008 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.2-1
☺ add fontconfig templates
☺ fix a few typos

* Mon Nov 10 2008 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.0-1
☺ initial release
