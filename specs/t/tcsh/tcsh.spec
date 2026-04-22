# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# === GLOBAL MACROS ===========================================================

# According to Fedora Package Guidelines, it is advised that packages that can
# process untrusted input are build with position-independent code (PIC).
#
# Koji should override the compilation flags and add the -fPIC or -fPIE flags by
# default. This is here just in case this wouldn't happen for some reason.
# For more info: https://fedoraproject.org/wiki/Packaging:Guidelines#PIE
%global _hardened_build 1

# =============================================================================

Name:             tcsh
Summary:          An enhanced version of csh, the C shell
Version:          6.24.14
Release: 5%{?dist}
License:          BSD-3-Clause

URL:              http://www.tcsh.org/
Source:           https://astron.com/pub/tcsh/%{name}-%{version}.tar.gz

Provides:         csh = %{version}
Provides:         /bin/csh
Provides:         /bin/tcsh

Requires(post):   coreutils
Requires(post):   grep
Requires(postun): sed

BuildRequires:    make
BuildRequires:    gcc
BuildRequires:    git
BuildRequires:    autoconf
BuildRequires:    gettext-devel
BuildRequires:    libxcrypt-devel
BuildRequires:    ncurses-devel

# =============================================================================

# NOTE: 'autosetup' macro (below) uses 'git' for applying the patches:
#       ->> All the patches should be provided in 'git format-patch' format.
#       ->> Auxiliary repository will be created during 'fedpkg prep', you
#           can see all the applied patches there via 'git log'.

# Upstream patches -- official upstream patches released by upstream since the
# ----------------    last rebase that are necessary for any reason:
Patch001: tcsh-6.24.14-Fix-defined-name-It-is-UTF16_STRINGS-not-UTF16_STRIN.patch


# Downstream patches -- these should be always included when doing rebase:
# ------------------
Patch100: tcsh-6.24.07-manpage-memoryuse.patch


# Downstream patches for RHEL -- patches that we keep only in RHEL for various
# ---------------------------    reasons, but are not enabled in Fedora:
%if %{defined rhel} || %{defined centos}
Patch200: tcsh-6.20.00-tcsh-posix-status.patch
%endif


# Patches to be removed -- deprecated functionality which shall be removed at
# ---------------------    some point in the future:


%description
Tcsh is an enhanced but completely compatible version of csh, the C shell. Tcsh
is a command language interpreter which can be used both as an interactive login
shell and as a shell script command processor. Tcsh includes a command line
editor, programmable word completion, spelling correction, a history mechanism,
job control and a C language like syntax.

# === BUILD INSTRUCTIONS ======================================================

# Call the 'autosetup' macro to prepare the environment, but do not patch the
# source code yet -- we need to convert the 'Fixes' file first:
%prep
%autosetup -N -S git

# NOTE: If more files needs to be converted, add them here:
for file in Fixes; do
  iconv -f iso-8859-1 -t utf-8 "$file" > "${file}.converted" && \
  touch -r "$file" "${file}.converted" && \
  mv "${file}.converted" "$file"
done

# Also, rename the Copyright so we comply with more generally accepted name:
mv Copyright COPYING

# Amend the converted files to the initial commit, and patch the source code:
git add --all --force
git commit --all --amend --no-edit > /dev/null
%autopatch -p1

# ---------------

%build
%configure
%make_build all

# ---------------

%check
%make_build check

# ---------------

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}/man1
install -p -m 755 tcsh     %{buildroot}%{_bindir}/tcsh
install -p -m 644 tcsh.man %{buildroot}%{_mandir}/man1/tcsh.1
ln -sf tcsh                %{buildroot}%{_bindir}/csh
ln -sf tcsh.1              %{buildroot}%{_mandir}/man1/csh.1

# NOTE: We have to construct tcsh.lang by ourselves, since upstream does not use
#       standard naming/placing of localization files for the gettext...
while read lang language; do
  dest="%{buildroot}%{_datadir}/locale/$lang/LC_MESSAGES"
  if [[ -f "nls/$language.cat" ]]; then
    mkdir -p "$dest"
    install -p -m 644 "nls/$language.cat" "$dest/tcsh"
    echo "%lang($lang) %{_datadir}/locale/$lang/LC_MESSAGES/tcsh"
  fi
done > %{name}.lang << _EOF
de german
el greek
en C
es spanish
et et
fi finnish
fr french
it italian
ja ja
pl pl
ru russian
uk ukrainian
_EOF

# ---------------

%post
# Add login shell entries to /etc/shells only when installing the package
# for the first time (see 'man 5 SHELLS' for more info):
if [[ "$1" -eq 1 ]]; then
  if [[ ! -f %{_sysconfdir}/shells ]]; then
    echo "/bin/csh"        >> %{_sysconfdir}/shells
    echo "/bin/tcsh"       >> %{_sysconfdir}/shells
    echo "%{_bindir}/csh"  >> %{_sysconfdir}/shells
    echo "%{_bindir}/tcsh" >> %{_sysconfdir}/shells
  else
    grep -q "^/bin/csh$"        %{_sysconfdir}/shells || echo "/bin/csh"        >> %{_sysconfdir}/shells
    grep -q "^/bin/tcsh$"       %{_sysconfdir}/shells || echo "/bin/tcsh"       >> %{_sysconfdir}/shells
    grep -q "^%{_bindir}/csh$"  %{_sysconfdir}/shells || echo "%{_bindir}/csh"  >> %{_sysconfdir}/shells
    grep -q "^%{_bindir}/tcsh$" %{_sysconfdir}/shells || echo "%{_bindir}/tcsh" >> %{_sysconfdir}/shells
  fi
fi

# ---------------

%postun
# Remove the login shell lines from /etc/shells only when uninstalling:
if [[ "$1" -eq 0 && -f %{_sysconfdir}/shells ]]; then
  sed -i -e '\!^/bin/csh$!d'        %{_sysconfdir}/shells
  sed -i -e '\!^/bin/tcsh$!d'       %{_sysconfdir}/shells
  sed -i -e '\!^%{_bindir}/csh$!d'  %{_sysconfdir}/shells
  sed -i -e '\!^%{_bindir}/tcsh$!d' %{_sysconfdir}/shells
fi

# === PACKAGING INSTRUCTIONS ==================================================

%files -f %{name}.lang
%doc FAQ Fixes README.md complete.tcsh
%license COPYING
%{_bindir}/tcsh
%{_bindir}/csh
%{_mandir}/man1/*.1*

# =============================================================================

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.24.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Feb 01 2025 Björn Esser <besser82@fedoraproject.org> - 6.24.14-3
- Add explicit BR: libxcrypt-devel

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.24.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Nov 29 2024 Jan Macku <jamacku@redhat.com> - 6.24.14-1
- Update to new version

* Thu Aug 01 2024 Jan Macku <jamacku@redhat.com> - 6.24.13-1
- Update to new version

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.24.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue May 14 2024 Jan Macku <jamacku@redhat.com> - 6.24.12-1
- Update to tcsh-6.24.12 (#2269465)

* Thu Mar 14 2024 Jan Macku <jamacku@redhat.com> - 6.24.10-4
- Fix Source URL

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.24.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.24.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri May 05 2023 Jan Macku <jamacku@redhat.com> - 6.24.10-1
- Update to tcsh-6.24.10 (#2185572)

* Mon Apr 24 2023 Lukáš Zaoral <lzaoral@redhat.com> - 6.24.07-3
- migrate to SPDX license format

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.24.07-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jan 13 2023 Jan Macku <jamacku@redhat.com> - 6.24.07-1
- Update to tcsh-6.24.07 (#2147466)

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.24.01-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 16 2022 Jan Macku <jamacku@redhat.com> - 6.24.01-1
- Update to tcsh-6.24.01 (#2084638)

* Thu Feb 03 2022 Jan Macku <jamacku@redhat.com> - 6.24.00-1
- Update to tcsh-6.24.00 (#2049530)

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.23.02-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Jan 03 2022 Jan Macku <jamacku@redhat.com> - 6.23.02-1
- Update to tcsh-6.23.02 (#2036566)

* Tue Dec 14 2021 Jan Macku <jamacku@redhat.com> - 6.23.01-1
- Update to tcsh-6.23.01 (#2030781)

* Mon Nov 15 2021 Jan Macku <jamacku@redhat.com> - 6.23.00-1
- Update to tcsh-6.23.00 (#2022337)
- Drop tcsh-6.22.04-expose-HIST_PURGE.patch                   - applied by upstream
- Drop tcsh-6.22.04-modifiers-no-longer-breaks-history.patch  - applied by upstream

* Tue Aug 24 2021 Jan Macku <jamacku@redhat.com> - 6.22.04-3
- Fix issue when modifiers breaks history

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.22.04-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Apr 27 2021 Jan Macku <jamacku@redhat.com> - 6.22.04-1
- Update to tcsh-6.22.04 (#1953702)

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.22.03-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Nov 19 2020 Jan Macku <jamacku@redhat.com> - 6.22.03-1
- Update to tcsh-6.22.03
- Drop tcsh-6.22.02-avoid-gcc-to-fail.patch                              - applied by upstream
- Drop tcsh-6.22.02-call-seterror-consistently-and-abort-quickly.patch   - applied by upstream
- Drop tcsh-6.22.02-avoid-crashing-when-loading-corrupted-history.patch  - applied by upstream

* Wed Oct 14 2020 Jan Macku <jamacku@redhat.com> - 6.22.02-5
- Switch to stderror() when parsing history so that we stop processing immediately to avoid crashes

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.22.02-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Feb 07 2020 Jan Macku <jamacku@redhat.com> - 6.22.02-3
- Avoid gcc 10 to fail during build on "multiple definition of handle_interrupt"

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.22.02-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Dec 12 2019 Jan Macku <jamacku@redhat.com> - 6.22.02-1
- Update to tcsh-6.22.02

* Fri Nov 29 2019 Jan Macku <jamacku@redhat.com> - 6.22.00-1
- Update to tcsh-6.22.00
- Drop tcsh-6.21.00-000-failing-exit-command-causes-infinite-loop.patch     - applied by upstream

* Fri Oct 25 2019 Jan Macku <jamacku@redhat.com> - 6.21.00-3
- Added upstream patch to fix infinite loop caused by exit command

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.21.00-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 16 2019 Jan Macku <jamacku@redhat.com> - 6.21.00-01
- Update to tcsh-6.21.00
- Drop tcsh-6.20.00-000-add-all-flags-for-gethost-build.patch       - applied by upstream
- Drop tcsh-6.20.00-001-delay-arginp-interpreting.Patches           - applied by upstream
- Drop tcsh-6.20.00-002-type-of-read-in-prompt-confirm.patch        - applied by upstream
- Drop tcsh-6.20.00-003-fix-out-of-bounds-read.patch                - applied by upstream
- Drop tcsh-6.20.00-004-do-not-use-old-pointer-tricks.patch         - applied by upstream
- Drop tcsh-6.20.00-005-reset-fixes-numbering.patch                 - applied by upstream
- Drop tcsh-6.20.00-006-cleanup-in-readme-files.patch               - applied by upstream
- Drop tcsh-6.20.00-007-look-for-tgetent-in-libtinfo.patch          - applied by upstream
- Drop tcsh-6.20.00-008-guard-ascii-only-reversion.patch            - applied by upstream
- Drop tcsh-6.20.00-009-fix-regexp-for-backlash-quoting-tests.patch - applied by upstream

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.20.00-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 14 2019 Björn Esser <besser82@fedoraproject.org> - 6.20.00-11
- Rebuilt for libcrypt.so.2 (#1666033)

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.20.00-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.20.00-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 6.20.00-8
- Rebuilt for switch to libxcrypt

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.20.00-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.20.00-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Feb 28 2017 David Kaspar [Dee'Kej] <dkaspar@redhat.com> - 6.20.00-5
- Added multiple upstream patches:
    tcsh-6.20.00-004-do-not-use-old-pointer-tricks.patch
    tcsh-6.20.00-005-reset-fixes-numbering.patch
    tcsh-6.20.00-006-cleanup-in-readme-files.patch
    tcsh-6.20.00-007-look-for-tgetent-in-libtinfo.patch
    tcsh-6.20.00-008-guard-ascii-only-reversion.patch
    tcsh-6.20.00-009-fix-regexp-for-backlash-quoting-tests.patch (bug #1424082)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.20.00-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec  5 2016 David Kaspar [Dee'Kej] <dkaspar@redhat.com> - 6.20.00-3
- Added tcsh-6.20.00-003-fix-out-of-bounds-read.patch

* Mon Nov 28 2016 David Kaspar [Dee'Kej] <dkaspar@redhat.com> - 6.20.00-2
- Added multiple upstream patches:
    tcsh-6.20.00-000-add-all-flags-for-gethost-build.patch
    tcsh-6.20.00-001-delay-arginp-interpreting.patch
    tcsh-6.20.00-002-type-of-read-in-prompt-confirm.patch (bug #1386129)

* Mon Nov 28 2016 David Kaspar [Dee'Kej] <dkaspar@redhat.com> - 6.20.00-1
- Rebase to tcsh-6.20.00

* Tue Sep  6 2016 David Kaspar [Dee'Kej] <dkaspar@redhat.com> - 6.19.00-15
- Add a safeguard for installation on UsrMove enabled filesystem only

* Fri Aug 12 2016 David Kaspar [Dee'Kej] <dkaspar@redhat.com> - 6.19.00-14
- Move the COPYING file to correct location

* Mon Jul 18 2016 David Kaspar [Dee'Kej] <dkaspar@redhat.com> - 6.19.00-13
- Added tcsh-6.19.00-032-fix-multiline-prompt.patch (bug #1351056)

* Mon Jul 18 2016 David Kaspar [Dee'Kej] <dkaspar@redhat.com> - 6.19.00-12
- Added tcsh-6.19.00-031-always-send-prusage-to-stdout.patch,
  to fix regression in: tcsh-6.19.00-026-quote-backslashes-properly.patch
  See <http://mx.gw.com/pipermail/tcsh-bugs/2016-June/001067.html> for more info.

* Tue May 31 2016 David Kaspar [Dee'Kej] <dkaspar@redhat.com> - 6.19.00-11
- Deprecated tcsh-6.19.00-tcsh_posix_status-deprecated.patch removed

* Sun May 29 2016 David Kaspar [Dee'Kej] <dkaspar@redhat.com> - 6.19.00-10
- Added 3 new testcases into testsuite.

* Fri May 27 2016 David Kaspar [Dee'Kej] <dkaspar@redhat.com> - 6.19.00-9
- Another regression in tcsh-6.19.00-026-quote-backslashes-properly.patch fixed, see:
  <https://bugzilla.redhat.com/show_bug.cgi?id=1334751#c9>
- tcsh-6.19.00-029-do-not-print-jobs-to-stderr.patch added

* Mon May 16 2016 David Kaspar [Dee'Kej] <dkaspar@redhat.com> - 6.19.00-8
- Regression in tcsh-6.19.00-026-quote-backslashes-properly.patch fixed (#1333523)

* Tue May  3 2016 David Kaspar [Dee'Kej] <dkaspar@redhat.com> - 6.19.00-7
- Adding multiple upstream patches to stay closer with upstream:
    tcsh-6.19.00-000-announcement.patch
    tcsh-6.19.00-001-remove-CFLAGS-for-gethost.patch
    tcsh-6.19.00-002-fix-error-messages.patch
    tcsh-6.19.00-003-avoid-gcc5-calloc-optimization.patch (replaces tcsh-6.19.00-gcc5-calloc.patch)
    tcsh-6.19.00-004-remove-unused-variable.patch
    tcsh-6.19.00-005-ge0-is-always-true-for-unsigned.patch
    tcsh-6.19.00-006-_SIGWINCH-added.patch
    tcsh-6.19.00-007-fix-handling-of-invalid-unicode-characters.patch
    tcsh-6.19.00-008-fix-ln-1-completion.patch
    tcsh-6.19.00-009-fix-parsing-of-if-statement.patch
    tcsh-6.19.00-010-fix-editor-and-visual-variables-and-its-behaviour.patch
    tcsh-6.19.00-011-man-page-spelling-fixes.patch
    tcsh-6.19.00-012-display-default-in-editor.patch
    tcsh-6.19.00-013-VImode-variable-provided.patch
    tcsh-6.19.00-014-do-not-use-union-wait.patch
    tcsh-6.19.00-015-set-LC_COLLATE-to-C-and-add-HTML-makefile.patch
    tcsh-6.19.00-016-do-not-quote-name-expanded-by-completion.patch
    tcsh-6.19.00-017-fix-for-finnish-translations.patch
    tcsh-6.19.00-018-add-noclobber-and-ask-options.patch
    tcsh-6.19.00-019-fix-uninitialized-estr.patch
    tcsh-6.19.00-020-make-heredoc-interruptible-again.patch
    tcsh-6.19.00-021-remove-extra-semicolon.patch
    tcsh-6.19.00-022-fix-source-command-memory-leak.patch
    tcsh-6.19.00-023-fix-debugging-code.patch
    tcsh-6.19.00-024-use-sysmalloc.patch
    tcsh-6.19.00-025-more-generous-ROUNDUP-_LP64.patch
    tcsh-6.19.00-026-quote-backslashes-properly.patch
    tcsh-6.19.00-027-fix-memory-leak-when-cdpath-fails.patch
    tcsh-6.19.00-028-fix-wrong-ifdef.patch

* Thu Apr 21 2016 David Kaspar [Dee'Kej] <dkaspar@redhat.com> - 6.19.00-6
- Drop tcsh-6.15.00-closem.patch - issue not reproducible, patch not accepted by upstream
- Drop tcsh-6.14.00-unprintable.patch - issue not reproducible with 6.19.00 upstream version
- Drop tcsh-6.14.00-syntax.patch - patch not accepted by upstream, breaks other things
- Drop tcsh-6.18.01-skip-tty-tests.patch - has been fixed in 6.18.05 upstream version
- Drop tcsh-6.18.01-elf-interpreter.patch - patch not working anymore, not accepted by upstream
- Drop tcsh-6.18.01-introduce-tcsh_posix_status.patch - not accepted by upstream,
                                                        upstream introduced $anyerror instead
- Add  tcsh-6.19.00-tcsh_posix_status-deprecated.patch - temporary patch with warning,
                                                         should be removed in F25
- Drop tcsh-6.14.00-order.patch - misleading man page change not reflecting correct behaviour
- Fix  tcsh-6.13.00-memoryuse.patch -> tcsh-6.19.00-manpage-memoryuse.patch
- Drop tcsh-6.15.00-hist-sub.patch - misleading man page change

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 6.19.00-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 13 2016 Lubomir Rintel <lkundrak@v3.sk> - 6.19.00-04
- Fix build

* Tue Jun 16 2015 Fridolin Pokorny <fpokorny@redhat.com> - 6.19.00-03
- Add /bin/tcsh and /bin/csh to /etc/shells (#1229032)

* Thu May 28 2015 Fridolin Pokorny <fpokorny@redhat.com> - 6.19.00-02
- Add tcsh-6.19.00-gcc5-calloc.patch to avoid crashes and infinite loops due to
  gcc-5 malloc+memset optimization.

* Wed May 27 2015 Fridolin Pokorny <fpokorny@redhat.com> - 6.19.00-01
- Update to tcsh-6.19.00
- Drop tcsh-6.14.00-tinfo.patch, not used anymore
- Drop tcsh-6.17.00-manpage-spelling.patch, accepted by upstream
- Drop tcsh-6.18.00-history-file-locking.patch, upstream introduced own history
  file locking
- Drop tcsh-6.18.00-history-merge.patch to respect upstream history handling
- Drop tcsh-6.18.01-repeated-words-man.patch, accepted by upstream
- Adjust tcsh-6.15.00-hist-sub.patch to merge new release
- Adjust tcsh-6.18.01-elf-interpreter.patch to merge new release
- Adjust tcsh-6.18.01-introduce-tcsh_posix_status.patch to merge new release
- Remove tcsh-6.18.01-reverse-history-handling-in-loops.patch, issue does not
  occur anymore
- Adjust tcsh-6.18.01-skip-tty-tests.patch to merge new release
- Remove tcsh-6.18.01-wait-hang.patch, accepted by upstream

* Tue Jan 27 2015 Pavel Raiskup <praiskup@redhat.com> - 6.18.01-13
- fix 'wait' built-in hang (#1181685)
- call %%autosetup after iconv, this avoids having uncommitted changes in
  srcdir after patches are applied

* Wed Aug 27 2014 Pavel Raiskup <praiskup@redhat.com> - 6.18.01-12
- use the %%autosetup macro
- enable testsuite in %%check
- skip tests which are not able to be run without tty
- support both $anyerror & $tcsh_posix_status (#1129703)

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.18.01-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.18.01-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Dec 19 2013 Pavel Raiskup <praiskup@redhat.com> - 6.18.01-9
- provide binaries in /bin for compatibility

* Thu Dec 19 2013 Jaromir Koncicky <jkoncick@redhat.com> - 6.18.01-8
- Move binaries from /bin to /usr/bin

* Thu Dec 19 2013 Jaromir Koncicky <jkoncick@redhat.com> - 6.18.01-7
- Revert history handling in loops
  (Backported resolution of RHEL bug #814069)

* Wed Dec 18 2013 Jaromir Koncicky <jkoncick@redhat.com> - 6.18.01-6
- Changed 'anyerror' variable to 'tcsh_posix_status' with opposite meaning
  (Backported resolution of RHEL bug #759132)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.18.01-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 26 2013 Pavel Raiskup <praiskup@redhat.com> - 6.18.01-4
- fix rpmlint warnings

* Wed May 22 2013 Fridolin Pokorny <fpokorny@redhat.com> 6.18.01-3
- Added tcsh-6.18.01-elf-interpreter.patch to report missing ELF interpreter
  Resolves: #711066

* Mon Apr 08 2013 Fridolin Pokorny <fpokorny@redhat.com> 6.18.01-2
- Removed repeated words in man
  Resolves: #948884

* Fri Apr 05 2013 Fridolin Pokorny <fpokorny@redhat.com> 6.18.01-1
- Update to tcsh-6.18.01
- Removed tcsh-6.18.00-history-savehist.patch, not accepted by upstream
  http://mx.gw.com/pipermail/tcsh-bugs/2013-March/000824.html

* Thu Mar 28 2013 Fridolin Pokorny <fpokorny@redhat.com> 6.18.00-7
- File locking patch modified to reflect HIST_MERGE flag (#879371)
- Drop tcsh-6.18.00-sigint-while-waiting-for-child.patch, accepted by upstream
- Add tcsh-6.18.00-history-merge.patch to merge histlist properly (#919452)
- Add tcsh-6.18.00-history-savehist.patch to store history with length
  $savehist, not only $history.

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.18.00-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Dec 12 2012 Roman Kollar <rkollar@redhat.com> 6.18.00-5
- Fix tcsh being interruptible while waiting for child process (#884937)

* Mon Oct 29 2012 Roman Kollar <rkollar@redhat.com> - 6.18.00-4
- Add Copyright file in %%doc
- Readd tcsh-6.18.00-history-file-locking.patch
- Fix casting in lseek calls in the history file locking patch (#821796)
- Fix dosource calls in the history file locking patch (#847102)
  Resolves: #842851
- Fix upstream source tarball location

* Fri Aug 3 2012 Orion Poplawski <orion@nwra.com> - 6.18.00-3
- Drop tcsh-6.18.00-history-file-locking.patch for now (bug 842851)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.18.00-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Mar 15 2012 Vojtech Vitek (V-Teq) <vvitek@redhat.com> - 6.18.00-1
- Update to tcsh-6.18.00
- Remove obsolete patches: tcsh-6.15.00-ca-color.patch,
  tcsh-6.17.00-tc-color.patch, tcsh-6.17.00-mh-color.patch,
  tcsh-6.17.00-history.patch, tcsh-6.17.00-printexitvalue.patch,
  tcsh-6.17.00-testsuite.patch, tcsh-6.17.00-negative_jobs.patch,
  tcsh-6.17.00-wait-intr.patch, tcsh-6.17.00-dont-set-empty-remotehost.patch,
  tcsh-6.17.00-dont-print-history-on-verbose.patch, tcsh-6.14.00-set.patch,
  tcsh-6.17.00-extrafork.patch, tcsh-6.17.00-avoid-null-cwd.patch,
  tcsh-6.17.00-avoid-infinite-loop-pendjob-xprintf.patch,
  tcsh-6.17.00-variable-names.patch,
  tcsh-6.17.00-handle-signals-before-flush.patch
  tcsh-6.17.00-status-pipeline-backquote-list-of-cmds.patch (reverted!)
- Modify and adapt the existing patches to the new source code:
  tcsh-6.13.00-memoryuse.patch, tcsh-6.14.00-tinfo.patch,
  tcsh-6.18.00-history-file-locking.patch

* Thu Feb 16 2012 Vojtech Vitek (V-Teq) <vvitek@redhat.com> - 6.17-19
- Handle pending signals before flush so that the the .history file
  does not get truncated (#653054)
- Implement file locking using shared readers, exclusive writer
  to prevent any .history file data corruption (#653054)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.17-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 31 2011 Vojtech Vitek (V-Teq) <vvitek@redhat.com> - 6.17-17
- Fix minor man page spelling mistakes (#675137)

* Thu Oct 27 2011 Vojtech Vitek (V-Teq) <vvitek@redhat.com> - 6.17-16
- Fix status of pipelined/backquoted/list of commands (RHEL-6 #658190)
- Do not dereference null pointer in cwd (RHEL-6 #700309)
- Fix negative number of jobs with %%j formatting parameter in prompt
- Clean-up patches numbers & order (prepare space for missing RHEL-6 patches)
- Disable obsolete glob-automount.patch; The issue should have been
  (and is now) fixed in glibc (posix/glob.c)

* Thu Mar 24 2011 Vojtech Vitek (V-Teq) <vvitek@redhat.com> - 6.17-15
- Avoid infinite loop pendjob()-xprintf() when stdout is closed
  Resolves: #690356

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.17-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 28 2011 Vojtech Vitek (V-Teq) <vvitek@redhat.com> - 6.17-13
- Modify verbose patch to match with upstream (don't print on history -S)
  Resolves: #672810

* Wed Jan 26 2011 Vojtech Vitek (V-Teq) <vvitek@redhat.com> - 6.17-12
- Fix error message on exit
  Resolves: #672810

* Mon Jan 24 2011 Vojtech Vitek (V-Teq) <vvitek@redhat.com> - 6.17-11
- Don't set $REMOTEHOST on the local machine
  Resolves: #669176
- Don't print history in verbose mode
  Resolves: #583075, #658171
- Don't allow illegal variable names to be set
  Resolves: #436901
- Revert "Fix incorrect $status value of pipelined commands"

* Tue Dec 21 2010 Vojtech Vitek (V-Teq) <vvitek@redhat.com> - 6.17-10
- Make wait builtin command interruptible
  Resolves: #440465
- Fix incorrect $status value of pipelined commands
  Resolves: #638955 (Patch by Tomas Smetana <tsmetana@redhat.com>)

* Wed Oct  6 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 6.17-9
- Remove fork when tcsh processes backquotes

* Wed Apr 14 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 6.17-8
- Fix testsuite

* Mon Mar  1 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 6.17-7
- Ship README file

* Tue Dec 15 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 6.17-6
- Fix tcsh obeys printexitvalue for back-ticks

* Wed Nov  4 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 6.17-5
- Fix few globbing problems

* Mon Oct 19 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 6.17-4
- Fix tcsh globbing causing bad automount
- Fix truncated history file after network crash

* Wed Aug 26 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 6.17-3
- Add new colorls variable
  Resolves: #518808

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 20 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 6.17-1
- Update to tcsh-6.17.00

* Thu Apr 30 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 6.16-1
- Update to tcsh-6.16.00
- Merge Review (fix License, add BUGS and WishList to documentation, convert Fixes and
  WishList to UTF-8, remove root checking from buildroot cleaning, preserve timestamps,
  use smp_flags, remove unused patches, improve postun script and minor fix to %%files)
  Resolves: #226483

* Mon Mar  2 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 6.15-8
- Fix tcsh needs to know about new colorls variables
  Resolves: #487783

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.15-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Sep  3 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 6.15-6
- Fix UTF-8 Japanese character is garbled in tcsh script in
  a certain situation
  Related: #453785
- Fix calculation order of operators description in tcsh manpage
  Related: #442536
- Fix strings which begin with '0' are not recognized as octal numbers
  Related: #438109
- Fix memoryuse description in tcsh manpage
  Related: #437095
- Fix tcsh scripts with multiple case statement with end keywords
  break with error
  Related: #436956
- Fix description of builtin command 'set' in tcsh manpage
  Related: #430459

* Fri Aug 29 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 6.15-5
- Rediffed all patches to work with patch --fuzz=0
- Let tcsh know 'ca' colorls variable
  Resolves: #458716

* Fri Feb 29 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 6.15-4
- Fix '\' can not be used to quote all delimiters
  Related: #435421
- Fix $name[selector] should fail when any number of 'selector' is out of range
  Related: #435398

* Mon Feb 11 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 6.15-3
- Fix Buildroot

* Fri Jan 18 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 6.15-2
- Rebuild

* Mon Aug 27 2007 Vitezslav Crhonek <vcrhonek@redhat.com> - 6.15-1
- Update to tcsh-6.15.00
- Fix license
- Add gettext-devel to BuildRequires (AM_ICONV)

* Wed Apr 25 2007 Vitezslav Crhonek <vcrhonek@redhat.com> - 6.14-16
- Fix floating exception in print_by_column() with unprintable characters
  (#233525)

* Mon Feb 26 2007 Miloslav Trmac <mitr@redhat.com> - 6.14-15
- Fix License:
  Related: #226483.

* Mon Feb 12 2007 Miloslav Trmac <mitr@redhat.com> - 6.14-14
- Link to libtinfo instead of libncurses

* Thu Nov 30 2006 Miloslav Trmac <mitr@redhat.com> - 6.14-13
- Link to ncurses instead of libtermcap
- Fix some rpmlint warnings

* Tue Sep 26 2006 Miloslav Trmac <mitr@redhat.com> - 6.14-12
- Fix error handling in tcsh-6.14.00-wide-seeks.patch

* Sat Sep  9 2006 Miloslav Trmac <mitr@redhat.com> - 6.14-11
- Fix an unlikely crash on startup (#188279)

* Wed Aug 16 2006 Miloslav Trmac <mitr@redhat.com> - 6.14-10
- Fix an uninitialized variable causing stack corruption (#197968)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 6.14-9.1
- rebuild

* Mon Jul 10 2006 Miloslav Trmac <mitr@redhat.com> - 6.14-9
- Fix seeking over multibyte characters (#195972)
- Don't ship obsolete eight-bit.txt

* Thu Mar 23 2006 Miloslav Trmac <mitr@redhat.com> - 6.14-8
- Backport a patch to ignore LS_COLOR codes introduced in newer coreutils
  (#186037)

* Sat Mar 18 2006 Miloslav Trmac <mitr@redhat.com> - 6.14-7
- Fix a crash when reading scripts with multibyte characters (#183267)
- Block SIGINT while waiting for children (#177366)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 6.14-5.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 6.14-5.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Aug  5 2005 Miloslav Trmac <mitr@redhat.com> - 6.14-5
- Fix EOF handling in $< (#165095, patch by s_h_o_@hotmail.co.jp)

* Thu Jul  7 2005 Miloslav Trmac <mitr@redhat.com> - 6.14-3
- Fix -n (#162187)

* Mon Jun 20 2005 Miloslav Trmac <mitr@redhat.com> - 6.14-2
- Backport a column width calculation bugfix (#160760)

* Fri Mar 25 2005 Miloslav Trmac <mitr@redhat.com> - 6.14-1
- Update to tcsh-6.14.00

* Sat Mar  5 2005 Miloslav Trmac <mitr@redhat.com> - 6.13-13
- Rebuild with gcc 4

* Fri Feb 25 2005 Miloslav Trmac <mitr@redhat.com> - 6.13-12
- Don't ship the HTML documentation (generated from the man page, contains
  also a copy of the man page)

* Sun Jan 30 2005 Miloslav Trmac <mitr@redhat.com> - 6.13-11
- Fix the previous patch, handle a missed case (#146330)

* Sat Jan 15 2005 Miloslav Trmac <mitr@redhat.com> - 6.13-10
- Avoid reusing iconv_catgets' static buffer (#145177, #145195)

* Tue Sep 21 2004 Miloslav Trmac <mitr@redhat.com> - 6.13-9
- Fix invalid argument to xprintf () (#133129)

* Wed Sep 15 2004 Miloslav Trmac <mitr@redhat.com> - 6.13-8
- Fix $HOSTTYPE and $MACHTYPE for ppc64 and s390x, this time for sure

* Wed Sep 15 2004 Miloslav Trmac <mitr@redhat.com> - 6.13-7
- Define $HOSTTYPE and $MACHTYPE for ppc64 and s390 (#115531),
  I hope that finally covers all architectures.

* Wed Sep 15 2004 Miloslav Trmac <mitr@redhat.com> - 6.13-6
- Define $HOSTTYPE and $MACHTYPE also on IA-64 and s390x (#115531)
- Don't close sockets to avoid file descriptor conflits with nss_ldap (#112453)

* Tue Sep 14 2004 Miloslav Trmac <mitr@redhat.com> - 6.13-5
- Fix HTML documentation generation, second attempt (#60664)
- Set dspmbyte using nl_langinfo(CODESET) if possible, should cover all
  cases where lang.csh was correctly setting dspmbyte (#89549)

* Wed Sep  8 2004 Miloslav Trmac <mitr@redhat.com> - 6.13-4
- Remove unneeded patches

* Thu Aug 26 2004 Miloslav Trmac <mitr@redhat.com> - 6.13-3
- Check for SIGWINCH more often (from tcsh-6.13.01, #130941)

* Wed Aug 18 2004 Miloslav Trmac <mitr@redhat.com> - 6.13-2
- Make comparisons for ranges in bracket expressions symmetric (#59493)
- Run perl2html with LC_ALL=C to workaround what seems to be a perl bug
  (#60664)
- Define $HOSTTYPE and $MACHTYPE on x86_64 (#115531)
- Fix setting of O_LARGEFILE (#122558)

* Tue Aug 17 2004 Miloslav Trmac <mitr@redhat.com> - 6.13-1
- Update to tcsh-6.13.00
- Fix charset headers in some of the translations
- Convert translated messages to LC_CTYPE locale
- Fix automatic dspmbyte setting

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Feb 10 2004 Nalin Dahyabhai <nalin@redhat.com> 6.12-7
- remove declaration of setpgrp() which conflicts with libc's (#115185)

* Fri Nov 21 2003 Nalin Dahyabhai <nalin@redhat.com> 6.12-6
- add missing buildprereqs on groff, libtermcap-devel (#110599)

* Tue Jul  8 2003 Nalin Dahyabhai <nalin@redhat.com>
- update URL

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Dec 05 2002 Elliot Lee <sopwith@redhat.com> 6.12-3
- Merge changes from 8.0-hammer

* Tue Nov 19 2002 Nalin Dahyabhai <nalin@redhat.com> 6.12-3
- rebuild

* Thu Aug 08 2002 Phil Knirsch <pknirsch@redhat.com> 6.12-2
- Added csh.1 symlink to manpages.

* Tue Jun  4 2002 Nalin Dahyabhai <nalin@redhat.com> 6.11-1
- update to 6.11

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Jan 31 2002 Bill Nottingham <notting@redhat.com>
- rebuild in new env

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Wed Mar 28 2001 Akira TAGOH <tagoh@redhat.com> 6.10-5
- Fixed check locale.

* Tue Feb  6 2001 Adrian Havill <havill@redhat.com>
- use <time.h> instead of <sys/time.h> for pickier lib (#25935)
- allow arguments for login shells (#19926)

* Thu Nov 30 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 6.10.00 to fix here-script vulnerability

* Mon Sep 18 2000 Adrian Havill <havill@redhat.com>
- fix catalog locale dirname for Japanese

* Thu Jun 15 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging.
- add locale support (#10345).

* Tue Mar  7 2000 Jeff Johnson <jbj@redhat.com>
- rebuild for sparc baud rates > 38400.

* Mon Jan 31 2000 Cristian Gafton <gafton@redhat.com>
- rebuild to fix dependencies

* Thu Jan 27 2000 Jeff Johnson <jbj@redhat.com>
- append entries to spanking new /etc/shells.

* Mon Jan 10 2000 Jeff Johnson <jbj@redhat.com>
- update to 6.09.
- fix strcoll oddness (#6000, #6244, #6398).

* Sat Sep 25 1999 Michael K. Johnson <johnsonm@redhat.com>
- fix $shell by using --bindir

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 5)

* Wed Feb 24 1999 Cristian Gafton <gafton@redhat.com>
- patch for using PATH_MAX instead of some silly internal #defines for
  variables that handle filenames.

* Fri Nov  6 1998 Jeff Johnson <jbj@redhat.com>
- update to 6.08.00.

* Fri Oct 02 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to 6.07.09 from the freebsd
- security fix

* Wed Aug  5 1998 Jeff Johnson <jbj@redhat.com>
- use -ltermcap so that /bin/tcsh can be used in single user mode w/o /usr.
- update url's

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Tue Oct 21 1997 Cristian Gafton <gafton@redhat.com>
- updated to 6.07; added BuildRoot
- cleaned up the spec file; fixed source url

* Wed Sep 03 1997 Erik Troan <ewt@redhat.com>
- added termios hacks for new glibc
- added /bin/csh to file list

* Fri Jun 13 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Fri Feb 07 1997 Erik Troan <ewt@redhat.com>
- Provides csh, adds and removes /bin/csh from /etc/shells if csh package
isn't installed.
