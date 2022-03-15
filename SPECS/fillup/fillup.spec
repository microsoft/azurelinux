#
# spec file for package fillup
#
# Copyright (c) 2020 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#

Summary:        Tool for Merging Config Files
Name:           fillup
Version:        1.42
Release:        278%{?dist}
License:        GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System/Base
URL:            https://github.com/openSUSE/fillup
#Source0:       https://github.com/openSUSE/%{name}/archive/refs/tags/%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
Patch0:         %{name}-optflags.patch
Patch1:         %{name}-warnings.dif
Patch2:         %{name}-%{version}.dif
Patch3:         %{name}-retval.dif
Patch4:         %{name}-nodate.patch
Patch5:         %{name}-1.42-cloexec.patch
Patch6:         %{name}-fno-common.patch
Patch7:         %{name}-test-create-DIFFERENCE-dir-before-testing.patch
Provides:       /bin/%{name}
BuildRequires:  diffutils

%description
fillup merges files that hold variables.  A variable is defined by an
entity composed of a preceding comment, a variable name, an assignment
delimiter, and a related variable value.  A variable is determined by
its variable name.

%prep
%setup -q
%patch0
%patch1 -p1
%patch2
%patch3
%patch4
%patch5
%patch6 -p1
%patch7 -p1

%build
mkdir -p OBJ
mkdir -p BIN
make %{?_smp_mflags} compile COMPILE_OPTION=OPTIMIZE OPTISPLUS="%{optflags}"

%install
mkdir -p %{buildroot}%{_fillupdir}
install -d -m 755 %{buildroot}/%{_bindir}
install -m 755 BIN/fillup %{buildroot}/%{_bindir}
install -d %{buildroot}/%{_mandir}/man8
install -m 644 SGML/fillup.8.gz %{buildroot}/%{_mandir}/man8

%check
make %{?_smp_mflags} test    OPTISPLUS="%{optflags}"

%files
%defattr(-,root,root)
%{_bindir}/fillup
%{_mandir}/man8/fillup*

%changelog
* Mon Mar 07 2022 Muhammad Falak <mwani@microsoft.com> - 1.42.278
- Introduce patch to fix ptest

* Tue Aug 17 2021 Henry Li <lihl@microsoft.com> - 1.42-277
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- License Verified
- Update Source0 URL path
- Manually create BIN and OBJ folder to build the project
- Remove symbolic link on fillup
- Remove _fillupdir macro definition

* Fri Oct 16 2020 Ludwig Nussel <lnussel@suse.de>
- prepare usrmerge (boo#1029961)

* Wed Jan 15 2020 Adam Majer <adam.majer@suse.de>
- fillup-fno-common.patch: fix compilation on Tumbleweed
  (boo#1160871)

* Thu Nov 23 2017 rbrown@suse.com
- Replace references to /var/adm/fillup-templates with new
  %%_fillupdir macro (boo#1069468)

* Mon Nov  3 2014 tchvatal@suse.com
- Also return back the /bin/fillup provides line

* Fri Oct 31 2014 dimstar@opensuse.org
- Keep /bin/fillup as a symlink in the package: there are hundreds
  of RPMs out there referencing it in the %%post scriptlets, when
  any of the %%*fillup* macros was used. Even updating the macro
  will not make the existing RPMs magically be fixed.

* Sun Oct 26 2014 tchvatal@suse.com
- Cleanup the mess in spec with spec-cleaner

* Wed Feb  8 2012 rschweikert@suse.com
- place binary into /usr tree (UsrMerge project)

* Fri Sep 30 2011 uli@suse.com
- cross-build workarounds: disable %%build section testing, use fake
  gcc script to work around build system deficiencies

* Sun Sep 18 2011 jengelh@medozas.de
- Apply packaging guidelines (remove redundant/obsolete
  tags/sections from specfile, etc.)

* Sat May 21 2011 crrodriguez@opensuse.org
- Open all file descriptors with O_CLOEXEC
- handle out-of-disk-space situations somewhat better.

* Mon Jun 28 2010 jengelh@medozas.de
- use %%_smp_mflags

* Sun Dec 13 2009 aj@suse.de
- Do not compile in date into binary to create reproduceable binaries.

* Sun Dec 13 2009 jengelh@medozas.de
- enable parallel building

* Wed Aug 26 2009 mls@suse.de
- make patch0 usage consistent

* Tue Sep 19 2006 rguenther@suse.de
- Do not install info or plaintext documentation (same as manpage).
- Remove sgmltool BuildRequires.

* Mon May 22 2006 schwab@suse.de
- Don't strip binaries.

* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires

* Wed Jan 11 2006 ro@suse.de
- fix missing return value in test-code (#139594)

* Fri Sep  2 2005 werner@suse.de
- Fix segv on big endian (bug #114066)
  * Correct usage of EOF macro, this is and was never a character
  * Make it handle missing newline at EOF
- Make it strict alias safe
- Compare the correct debug output in test suite (bug #95371)

* Wed Jul 27 2005 ro@suse.de
- silence some compiler warnings (#95370)

* Mon Jun 27 2005 ro@suse.de
- removed -fsigned-char (#93875)

* Wed Jun 15 2005 meissner@suse.de
- Use RPM_OPT_FLAGS -fno-strict-aliasing.
- compile OPTIMIZE, drop some no longer applying -f flags.

* Mon Mar  1 2004 ro@suse.de
- fix install_info stuff in postun

* Sun Oct 19 2003 ro@suse.de
- use defattr
- don't build as root

* Thu Sep 11 2003 ro@suse.de
- update to 1.42 (#30279)

* Mon Aug 25 2003 ro@suse.de
- update to 1.41
- additional Keyword: PreSaveCommand

* Thu Aug 14 2003 ro@suse.de
- update to 1.38 with additional MetaData keywords

* Mon Jun 16 2003 kukuk@suse.de
- Remove /var/adm/fillup-templates, already in filesystem package

* Wed Mar 12 2003 ro@suse.de
- update to 1.24 including the last two patches and
  more testcases for "make check"

* Wed Mar 12 2003 ro@suse.de
- switch behaviour to "fixed sequence of metadata" (#25119)

* Sun Mar  9 2003 ro@suse.de
- fix watchdog for removal part (factor 2 needed)
  (fix for reopened #24648)

* Thu Mar  6 2003 ro@suse.de
- update to 1.22 (avoid possible infinite loop on failure) (#24648)

* Thu Mar  6 2003 ro@suse.de
- fix for stale comment when removing variable (#24540)

* Wed Feb 19 2003 ro@suse.de
- update to 1.21
- works around problem with comments wrongly typed as metadata

* Thu Feb  6 2003 ro@suse.de
- added install-info macros

* Thu Nov 28 2002 ro@suse.de
- update to 1.20 beta (aka prototype)

* Mon Nov 11 2002 ro@suse.de
- changed neededforbuild <sp> to <opensp>

* Mon Aug 12 2002 ro@suse.de
- split off aaa_base
