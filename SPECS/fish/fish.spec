# This package depends on automagic byte compilation
# https://fedoraproject.org/wiki/Changes/No_more_automagic_Python_bytecompilation_phase_2
%global _python_bytecompile_extra 1
Name:           fish
Version:        3.6.2
Release:        1%{?dist}
Summary:        Friendly interactive shell
Vendor:         Microsoft Corporation
Distribution:   Mariner
# GPLv2
#   - src/fish.cpp
#   and rest..
# GPLv2+
#   - src/builtin_printf.cpp
# BSD
#   - share/tools/create_manpage_completions.py
# ISC
#   - src/utf8.cpp
#   - src/utf8.h
# LGPLv2+
#   - src/wgetopt.c
#   - src/wgetopt.h
# MIT
#   - share/completions/grunt.fish
#   - share/tools/web_config/js/angular-sanitize.js
#   - share/tools/web_config/js/angular.js
#   - user_doc/html/_static/jquery.js
#   - user_doc/html/_static/underscore.js
License:        GPLv2 and BSD and ISC and LGPLv2+ and MIT
URL:            https://fishshell.com
Source0:        https://github.com/fish-shell/fish-shell/releases/download/%{version}/%{name}-%{version}.tar.xz

BuildRequires:  cmake >= 3.2
BuildRequires:  ninja-build
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gettext
BuildRequires:  ncurses-devel
BuildRequires:  pcre2-devel
BuildRequires:  gnupg2
BuildRequires:  python3-devel
%global __python %{__python3}

# tab completion wants man-db
Recommends:     man-db
Recommends:     man-pages
Recommends:     groff-base

# Expects the `kill` command to be available
Requires:       util-linux

Provides:       bundled(js-angular) = 1.0.8
Provides:       bundled(js-jquery) = 3.3.1
Provides:       bundled(js-underscore) = 1.9.1

%description
fish is a fully-equipped command line shell (like bash or zsh) that is
smart and user-friendly. fish supports powerful features like syntax
highlighting, autosuggestions, and tab completions that just work, with
nothing to learn or configure.

%prep
%autosetup -p1
rm -vrf pcre2-*

# Change the bundled scripts to invoke the python binary directly.
for f in $(find share/tools -type f -name '*.py'); do
    sed -i -e '1{s@^#!.*@#!%{__python3}@}' "$f"
done

%build
# Removing linker scripts to fix component existance checks.
LDFLAGS="$(echo " $LDFLAGS " | sed 's#-Wl,-dT,%{_topdir}/BUILD/module_info.ld##')"

%cmake . -B%{_vpath_builddir} -GNinja \
    -DCMAKE_INSTALL_SYSCONFDIR=%{_sysconfdir} \
    -Dextra_completionsdir=%{_datadir}/%{name}/vendor_completions.d \
    -Dextra_functionsdir=%{_datadir}/%{name}/vendor_functions.d \
    -Dextra_confdir=%{_datadir}/%{name}/vendor_conf.d

%ninja_build -C %{_vpath_builddir} all fish_tests

# We still need to slightly manually adapt the pkgconfig file and remove
# some /usr/local/ references (RHBZ#1869376)
sed -i 's^/usr/local/^/usr/^g' %{_vpath_builddir}/*.pc

%install
%ninja_install -C %{_vpath_builddir}

# Install docs from tarball root
cp -a README.rst %{buildroot}%{_pkgdocdir}
cp -a CONTRIBUTING.rst %{buildroot}%{_pkgdocdir}

%find_lang %{name}

%check
%{_vpath_builddir}/fish_tests

%post
if [ "$1" = 1 ]; then
  if [ ! -f %{_sysconfdir}/shells ] ; then
    echo "%{_bindir}/fish" > %{_sysconfdir}/shells
    echo "/bin/fish" >> %{_sysconfdir}/shells
  else
    grep -q "^%{_bindir}/fish$" %{_sysconfdir}/shells || echo "%{_bindir}/fish" >> %{_sysconfdir}/shells
    grep -q "^/bin/fish$" %{_sysconfdir}/shells || echo "/bin/fish" >> %{_sysconfdir}/shells
  fi
fi

%postun
if [ "$1" = 0 ] && [ -f %{_sysconfdir}/shells ] ; then
  sed -i '\!^%{_bindir}/fish$!d' %{_sysconfdir}/shells
  sed -i '\!^/bin/fish$!d' %{_sysconfdir}/shells
fi

%files -f %{name}.lang
%license COPYING
%{_mandir}/man1/fish*.1*
%{_bindir}/fish*
%config(noreplace) %{_sysconfdir}/fish/
%{_datadir}/applications/fish.desktop
%{_datadir}/fish/
%{_datadir}/pixmaps/fish.png
%{_datadir}/pkgconfig/fish.pc
%{_pkgdocdir}

%changelog
* Mon Dec 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.6.2-1
- Auto-upgrade to 3.6.2 - CVE-2023-49284

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 3.5.0-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Fri Jul 01 2022 Daniel McIlvaney <damcilva@microsft.com> - 3.5.0-1
- Update to 3.5.0 to reslove CVE-2022-20001

* Thu Jun 30 2022 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 3.1.2-5
- Mariner has sha256 check so remove not required gpg and asc files.
- Align vendor and distribution entries

* Thu Feb 17 2022 Andrew Phelps <anphel@microsoft.com> - 3.1.2-4
- Use _topdir instead of hard-coded value /usr/src/mariner
- License verified

* Thu Sep 23 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.1.2-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Removed linker scripts to fix the build.

* Fri Aug 28 2020 Oliver Falk <oliver@linux-kernel.at> - 3.1.2-2
- Correct pkgconfig references to /usr/local (RHBZ#1869376)

* Wed May 06 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 3.1.2-1
- Update to 3.1.2

* Sat Feb 15 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 3.1.0-1
- Update to 3.1.0

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 24 2019 luto@kernel.org - 3.0.2-1
- Update to 3.0.2

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jan 05 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.0.0-4
- Fix crash in 'string match' subcommand

* Sun Dec 30 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.0.0-3
- Switch to CMake/Ninja

* Sat Dec 29 2018 David Adam <zanchey@ucc.gu.uwa.edu.au> - 3.0.0-2
- Move to CMake builds
- Drop unneeded dependencies

* Fri Dec 28 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.0.0-1
- Update to 3.0.0

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 2.7.1-3
- Rebuilt for Python 3.7

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Jan 14 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.7.1-1
- Update to 2.7.1

* Wed Oct 04 2017 Andy Lutomirski <luto@kernel.org> - 2.6.0-1
- Update to 2.6.0
- Stop using bundled pcre2
- Add some missing dependencies (rhbz #1478779)

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Mar 12 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2.3.1-4
- Drop ExcludeArch as ppc64le's tests now pass

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 2.3.1-2
- Rebuild for Python 3.6

* Thu Jul 07 2016 Oliver Haessler <oliver@redhat.com> - 2.3.1-1
- Bump to 2.3.1

* Sun Jun 26 2016 luto@kernel.org - 2.3.0-2
- Require bc (rhbz 1349714)
- Improve Fedora vs EPEL compatibility in the specfile

* Sun May 22 2016 luto@kernel.org - 2.3.0-1
- Bump to 2.3.0
- Drop most Fedora patches

* Fri Feb 26 2016 luto@kernel.org - 2.2.0-11
- Add function/snippet hierarchy (backported from upstream)

* Thu Feb 04 2016 luto@kernel.org - 2.2.0-10
- Fix build on GCC 6

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 04 2016 Andy Lutomirski <luto@mit.edu> - 2.2.0-8
- Tidy up EL compat

* Sat Jan 02 2016 Oliver Haessler <oliver@redhat.com> - 2.2.0-7
- included patch directly into the spec file
- added new patch for using python3.4 on EPEL 7
- excluded ppc64le as the fish_tests fail for this arch

* Mon Dec 21 2015 Oliver Haessler <oliver@redhat.com> - 2.2.0-6
- added new patch for EL7 build

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Sep 24 2015 Andy Lutomirski <luto@mit.edu> - 2.2.0-4
- Hopefully fix rhbz #1263052 / upstream #2393

* Thu Aug 20 2015 Andy Lutomirski <luto@mit.edu> - 2.2.0-3
- Re-enable tests

* Wed Aug 19 2015 Andy Lutomirski <luto@mit.edu> - 2.2.0-2
- Fix docs on newer RPM

* Wed Aug 19 2015 Andy Lutomirski <luto@mit.edu> - 2.0.0-1
- Bump to 2.2.0
- Drop most Fedora patches
- Disable tests (broken upstream)
- Adapt to new tarball contents
- Drop Python 2 support (we will only target F22 and newer)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 2.1.1-4
- Rebuilt for GCC 5 C++11 ABI change

* Wed Dec 17 2014 Andy Lutomirski <luto@mit.edu> - 2.1.1-3
- For Fedora 22+, use Python 3

* Sun Dec 14 2014 Andy Lutomirski <luto@mit.edu> - 2.1.1-2
- Backport grep.fish fixes (rhbz #1173924)

* Mon Sep 29 2014 Andy Lutomirski <luto@mit.edu> - 2.1.1-1
- Update to 2.1.1

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Aug 12 2014 Andy Lutomirski <luto@mit.edu> - 2.1.0-11
- Improve fixes for CVE-2014-2905 and CVE-2014-2914

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Apr 28 2014 Andy Lutomirski <luto@mit.edu> - 2.1.0-9
- Fix CVE-2014-2914

* Mon Apr 28 2014 Andy Lutomirski <luto@mit.edu> - 2.1.0-8
- Fix build failure

* Mon Apr 28 2014 Andy Lutomirski <luto@mit.edu> - 2.1.0-7
- Fix CVE-2014-2905
- Fix CVE-2014-2906

* Fri Dec 20 2013 Andy Lutomirski <luto@mit.edu> - 2.1.0-6
- Switch back to Python 2

* Fri Dec 20 2013 Andy Lutomirski <luto@mit.edu> - 2.1.0-5
- Add BR: python3 (for __pycache__)
- Remove --without-xsel: fish dropped it in favor of a runtime check

* Fri Dec 13 2013 Andy Lutomirski <luto@mit.edu> - 2.1.0-4
- Stop looking in /usr/local (#1185 upstream)
- Link with CXXFLAGS (#1062 upstream)
- Use /usr/bin/python3 in scripts intead of /usr/bin/env
- Add fish_tests to the build process
- Split up the %%doc lines

* Wed Dec 11 2013 Andy Lutomirski <luto@mit.edu> - 2.1.0-3
- Use %%make_install instead of make install DESTDIR=...
- Removed rm -rf %%{buildroot}
- Added Requires: python

* Tue Dec 10 2013 Andy Lutomirski <luto@mit.edu> - 2.1.0-2
- Drop 'help' patch
- Misc cleanups

* Mon Dec 9 2013 Andy Lutomirski <luto@mit.edu> - 2.1.0-1
- Update to 2.1.0 and update a lot of the specfile
- Fix bogus changelog dates
- Add a patch to make 'help' work on F19 (upstream #1065)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.23.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 03 2009 Lorenzo Villani <lvillani@binaryhelix.net> - 1.23.1-3
- Pass --without-xsel to configure, if you want xsel install its package instead
- Fix file list
- Drop unneeded BuildRequires

* Fri Jul 03 2009 Lorenzo Villani <lvillani@binaryhelix.net> - 1.23.1-2
- rebuilt

* Fri Jul 03 2009 Lorenzo Villani <lvillani@binaryhelix.net> - 1.23.1-1
- 1.23.1
- Fix bz #472613

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.23.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Sep 15 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.23.0-6
- cleanups
- define ARG_MAX properly so it compiles

* Mon Jul 07 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.23.0-5
- fix conditional comparison

* Sun Jul 06 2008 Oliver Falk <oliver@linux-kernel.at> - 1.23.0-4
- Rebuild

* Wed May 21 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.23.0-3
- fix license tag

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.23.0-2
- Autorebuild for GCC 4.3

* Mon Jan 14 2008 Oliver Falk <oliver@linux-kernel.at> - 1.23.0-1
- Update to fix #208780
- Remove openfix patch, included upstream now

* Wed Oct 31 2007 Oliver Falk <oliver@linux-kernel.at> - 1.22.3-5
- Fix glibc's open check, by providing mode, instead of working
  around...

* Wed Oct 31 2007 Oliver Falk <oliver@linux-kernel.at> - 1.22.3-4
- Update URL; Fixes bz#359451

* Thu Aug 16 2007 Oliver Falk <oliver@linux-kernel.at> - 1.22.3-3
- Workaround glibc's open check
- Problem reported upstream; Should be fixed there

* Tue Aug 07 2007 Oliver Falk <oliver@linux-kernel.at> - 1.22.3-2
- Fix BR autoconf

* Tue Aug 07 2007 Oliver Falk <oliver@linux-kernel.at> - 1.22.3-1
- Update; Bug #236868
- Add missing doxygen BR

* Fri Aug 4 2006 Axel Liljencrantz<axel@liljencrantz.se> 1.21.10-4
- Add better translation finding code from fedora spec to main spec. Thank you to Michael Schwendt.
- Add missing dependency libXext-devel.
- Remove one nesting level from dependency checking code.

* Tue Aug 1 2006 Axel Liljencrantz<axel@liljencrantz.se> 1.21.10-1
- Improved the dependency check for X headers. Thank you to Michael Schwendt for pointers on how to do this

* Mon Jul 31 2006 Axel Liljencrantz<axel@liljencrantz.se> 1.21.10-1
- Fixed spelling and punctuation as a per patch from Paul Howarth
- Fixed dependencies as per patch from Paul Howarth

* Tue Nov 29 2005 Axel Liljencrantz <axel@liljencrantz.se> 1.17.0-0
- 1.17.0

* Sat Sep 24 2005 Axel Liljencrantz <axel@liljencrantz.se> 1.14.0-0
- 1.14.0

* Mon Sep 12 2005 Axel Liljencrantz <axel@liljencrantz.se> 1.13.4-0
- 1.13.4

* Wed Sep 07 2005 Axel Liljencrantz <axel@liljencrantz.se> 1.13.3-0
- 1.13.3

* Tue Sep 06 2005 Axel Liljencrantz <axel@liljencrantz.se> 1.13.2-0
- 1.13.2

* Tue Aug 30 2005 Axel Liljencrantz <axel@liljencrantz.se> 1.13.1-0
- 1.13.1

* Sun Aug 28 2005 Axel Liljencrantz <axel@liljencrantz.se> 1.13.0-0
- 1.13.0

* Sat Aug 13 2005 Axel Liljencrantz <axel@liljencrantz.se> 1.13.0-0
- Add completions subdirectory

* Thu Jul 28 2005 Axel Liljencrantz <axel@liljencrantz.se> 1.12.1-0
- 1.12.1

* Fri Jul 15 2005 Axel Liljencrantz <axel@liljencrantz.se> 1.12.0-1
- 1.12.0

* Thu Jun 30 2005 Michael Schwendt <mschwendt@users.sf.net> 1.11.1-9
- Set CFLAGS the proper way

* Thu Jun 30 2005 Axel Liljencrantz <axel@liljencrantz.se> 1.11.1-8
- Fix revision number in changelog

* Wed Jun 29 2005 Axel Liljencrantz <axel@liljencrantz.se> 1.11.1-7
- Send post-script output to /dev/null

* Wed Jun 29 2005 Axel Liljencrantz <axel@liljencrantz.se> 1.11.1-6
- Add changelog section to spec file
- Add macros to source tags
- Add smp_mflags to 'make all'
- Fix typo in post install scriptlet test
- Set CFLAGS from spec file
