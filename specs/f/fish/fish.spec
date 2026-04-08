## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 3;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global version_base 4.2.0
%dnl %global version_pre beta.1
%dnl %global gitnum 1
%dnl %global githash b82d0fcbcc44eb259cf2209b04f7a41c1f324e27
%dnl %global githashshort %{lua:print(string.sub(rpm.expand('%{githash}'), 1, 11))}

# For forked pcre2 crate that includes https://github.com/BurntSushi/rust-pcre2/pull/38
%global rust_pcre2_fish_tag 0.2.9-utf32

Name:           fish
Version:        %{version_base}%{?version_pre:~%{version_pre}}%{?gitnum:^git%{gitnum}.%{githashshort}}
Release:        %autorelease
Summary:        Friendly interactive shell
# Non-code licenses, see also doc_src/license.rst
# MIT
#   - share/completions/grunt.fish
#   - share/tools/web_config/js/angular-route.js
#   - share/tools/web_config/js/angular-sanitize.js
#   - share/tools/web_config/js/angular.js
# PSF-2.0
#   - doc_src/python_docs_theme/,
# Code licenses, see LICENSE.dependencies for a full license breakdown
# Apache-2.0 OR MIT
# GPL-2.0-only AND LGPL-2.0-or-later AND MIT AND PSF-2.0
# MIT
# MIT OR Apache-2.0
# Unlicense OR MIT
# WTFPL
# Zlib
License:        Apache-2.0 OR MIT and GPL-2.0-only AND LGPL-2.0-or-later AND MIT AND PSF-2.0 and Unlicense OR MIT and WTFPL and Zlib
URL:            https://fishshell.com
%if %{undefined gitnum}
Source0:        https://github.com/fish-shell/fish-shell/releases/download/%{version}/%{name}-%{version}.tar.xz
Source1:        https://github.com/fish-shell/fish-shell/releases/download/%{version}/%{name}-%{version}.tar.xz.asc
Source2:        https://github.com/krobelus.gpg
%else
Source0:        https://github.com/fish-shell/fish-shell/archive/%{githash}/%{name}-%{githash}.tar.gz
%endif

# For forked pcre2 crate that includes https://github.com/BurntSushi/rust-pcre2/pull/38
Source10:       https://github.com/fish-shell/rust-pcre2/archive/%{rust_pcre2_fish_tag}/rust-pcre2-%{rust_pcre2_fish_tag}.tar.gz

# Backports from upstream (0001~500)

# Proposed upstream (501~1000)
# https://github.com/fish-shell/fish-shell/pull/12222
Patch501:       0501-Update-phf-from-0.12-to-0.13.patch

# Downstream-only (1001+)
Patch1001:      1001-cargo-Use-internal-copy-of-rust-pcre2-instead-of-fet.patch
Patch1002:      1002-cmake-Use-rpm-profile-for-RelWithDebInfo.patch
Patch1003:      1003-cargo-Drop-unneeded-dependency-on-unix_path.patch

# Patches for bundled dependencies (10000+)
## For forked pcre2 crate that includes https://github.com/BurntSushi/rust-pcre2/pull/38
Patch10001:     10001-rust-pcre2-cargo-Drop-workspace-definition.patch
## For hopefully avoiding timeouts for tests on ppc64le and s390x
Patch10002:     10002-tests-Raise-the-default-timeout-for-pexpect-tests.patch


BuildRequires:  cargo
BuildRequires:  cargo-rpm-macros
BuildRequires:  cmake >= 3.5
BuildRequires:  ninja-build
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  git-core
BuildRequires:  ncurses-devel
BuildRequires:  pcre2-devel
BuildRequires:  gnupg2
BuildRequires:  python3-devel
BuildRequires:  python3-pexpect
BuildRequires:  procps-ng
BuildRequires:  rust
BuildRequires:  glibc-langpack-en
%global __python %{__python3}
BuildRequires:  /usr/bin/sphinx-build

# Needed to get terminfo
Requires:       ncurses-term

# tab completion wants man-db
Recommends:     man-db
Recommends:     man-pages
Recommends:     groff-base

# For the webconfig interface
Provides:       bundled(js-alpine)

# For forked pcre2 crate that includes https://github.com/BurntSushi/rust-pcre2/pull/38
Provides:       bundled(crate(pcre2)) = %{rust_pcre2_fish_tag}

%description
fish is a fully-equipped command line shell (like bash or zsh) that is
smart and user-friendly. fish supports powerful features like syntax
highlighting, autosuggestions, and tab completions that just work, with
nothing to learn or configure.

%prep
%if %{undefined gitnum}
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%endif
%autosetup -N %{?gitnum:-n fish-shell-%{githash}}

# For forked pcre2 crate that includes https://github.com/BurntSushi/rust-pcre2/pull/38
mkdir -p ./third-party-forks/rust-pcre2
tar -C ./third-party-forks/rust-pcre2 --strip-components=1 -xf %{SOURCE10}

%autopatch -p1

%if %{defined gitnum}
echo "%{version}" > version
%endif

# Change the bundled scripts to invoke the python binary directly.
for f in $(find share/tools -type f -name '*.py'); do
    sed -i -e '1{s@^#!.*@#!%{__python3}@}' "$f"
done
%cargo_prep


%generate_buildrequires
%cargo_generate_buildrequires -t


%conf
%cmake -GNinja -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DBUILD_DOCS=ON \
    -DCMAKE_INSTALL_SYSCONFDIR=%{_sysconfdir} \
    -Dextra_completionsdir=%{_datadir}/%{name}/vendor_completions.d \
    -Dextra_functionsdir=%{_datadir}/%{name}/vendor_functions.d \
    -Dextra_confdir=%{_datadir}/%{name}/vendor_conf.d


%build
export CARGO_NET_OFFLINE=true

# Cargo doesn't create this directory
mkdir -p %{_vpath_builddir}

%cmake_build -t all doc

# We still need to slightly manually adapt the pkgconfig file and remove
# some /usr/local/ references (RHBZ#1869376)
sed -i 's^/usr/local/^/usr/^g' %{_vpath_builddir}/*.pc

# Get Rust licensing data
%{cargo_license_summary}
%{cargo_license} > LICENSE.dependencies


%install
%cmake_install

# No more automagic Python bytecompilation phase 3
# * https://fedoraproject.org/wiki/Changes/No_more_automagic_Python_bytecompilation_phase_3
%py_byte_compile %{python3} %{buildroot}%{_datadir}/%{name}/tools/

# Install docs from tarball root
cp -a README.rst %{buildroot}%{_pkgdocdir}
cp -a CONTRIBUTING.rst %{buildroot}%{_pkgdocdir}


%check
# Skip all super-flaky tests because I have no patience anymore...
export CI=1
%cmake_build --target fish_run_tests


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


%files
%license COPYING
%license LICENSE.dependencies
%{_mandir}/man1/fish*.1*
%{_bindir}/fish*
%config(noreplace) %{_sysconfdir}/fish/
%{_datadir}/fish/
%{_datadir}/pkgconfig/fish.pc
%{_pkgdocdir}


%changelog
## START: Generated by rpmautospec
* Mon Apr 06 2026 azldev <> - 4.2.0-3
- Latest state for fish

* Sun Dec 28 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 4.2.0-2
- Update phf from 0.12 to 0.13

* Mon Nov 10 2025 Neal Gompa <ngompa@fedoraproject.org> - 4.2.0-1
- Update to version 4.2.0

* Sun Nov 09 2025 Neal Gompa <ngompa@fedoraproject.org> - 4.1.2-5
- Revert bump of timeout and export variable to disable flaky tests

* Sun Nov 09 2025 Neal Gompa <ngompa@fedoraproject.org> - 4.1.2-4
- Refresh pexpect timeout tests patch to increase the timeout again

* Sat Nov 08 2025 Neal Gompa <ngompa@fedoraproject.org> - 4.1.2-3
- Refresh pexpect timeout tests patch to increase timeout for ppc64le

* Sat Nov 08 2025 Neal Gompa <ngompa@fedoraproject.org> - 4.1.2-2
- Add patch to raise timeout for pexpect tests to avoid failures

* Fri Nov 07 2025 Neal Gompa <ngompa@fedoraproject.org> - 4.1.2-1
- Update to version 4.1.2

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 4.0.2-5
- Rebuilt for Python 3.14.0rc3 bytecode

* Tue Sep 02 2025 Neal Gompa <ngompa@fedoraproject.org> - 4.0.2-4
- Allow building on 32-bit architectures

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 4.0.2-3
- Rebuilt for Python 3.14.0rc2 bytecode

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Apr 21 2025 Neal Gompa <ngompa@fedoraproject.org> - 4.0.2-1
- Update to 4.0.2 upstream release
- Resolves: rhbz#2361232

* Fri Mar 21 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 4.0.1-2
- Update lru to 0.13.0 (proposed upstream)

* Wed Mar 19 2025 Neal Gompa <ngompa@fedoraproject.org> - 4.0.1-1
- Update to 4.0.1 upstream release

* Thu Feb 27 2025 Neal Gompa <ngompa@fedoraproject.org> - 4.0.0-3
- Disable building on 32-bit architectures

* Thu Feb 27 2025 Neal Gompa <ngompa@fedoraproject.org> - 4.0.0-2
- Fix bundled js dep provides

* Thu Feb 27 2025 Neal Gompa <ngompa@fedoraproject.org> - 4.0.0-1
- Rebase to new upstream release 4.0.0

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 27 2024 ErrorNoInternet <errornointernet@envs.net> - 3.7.1-1
- New upstream release 3.7.1 (fixes rhbz#2270247)

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Jan 02 2024 Neal Gompa <ngompa@fedoraproject.org> - 3.7.0-1
- New upstream release 3.7.0 (Resolves: rhbz#2256375)

* Mon Dec 11 2023 Dan Čermák <dan.cermak@cgc-instruments.com> - 3.6.4-2
- Remove duplicate AND from License tag

* Wed Dec 06 2023 Dan Čermák <dan.cermak@cgc-instruments.com> - 3.6.4-1
- New upstream release 3.6.4, fixes rhbz#2252773

* Wed Dec 06 2023 Dan Čermák <dan.cermak@cgc-instruments.com> - 3.6.1-4
- Switch license identifier to SPDX and add missing PSF-2.0

* Tue Dec 05 2023 Dan Čermák <dan.cermak@cgc-instruments.com> - 3.6.1-3
- Use proper rpm comments to prevent macro expansion

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Apr 10 2023 Siteshwar Vashisht <svashisht@redhat.com> - 3.6.1-1
- Update to 3.6.1

* Tue Jan 31 2023 Siteshwar Vashisht <svashisht@redhat.com> - 3.6.0-1
- Update to 3.6.0

* Mon Aug 15 2022 Siteshwar Vashisht <svashisht@redhat.com> - 3.5.1-1
- Update to 3.5.1

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 17 2022 Siteshwar Vashisht <svashisht@redhat.com> - 3.5.0-1
- Update to 3.5.0

* Sun Apr 03 2022 Igor Raits <igor.raits@gmail.com> - 3.4.1^120g1a0b1ae238e-1
- Update to 3.4.1-120-g1a0b1ae23

* Sun Apr 03 2022 Igor Raits <igor.raits@gmail.com> - 3.4.1-1
- Update to 3.4.1

* Sun Mar 13 2022 Igor Raits <igor.raits@gmail.com> - 3.4.0-1
- Update to 3.4.0

* Mon Feb 21 2022 Igor Raits <igor.raits@gmail.com> - 3.3.1^1075ge0bc944d5c5-1
- Update to 3.3.1-1075-ge0bc944d5

* Sun Feb 06 2022 Igor Raits <igor.raits@gmail.com> - 3.3.1^1034g964b7a729a7-1
- Update to 3.3.1-1034-g964b7a729

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1^803g76a336d647e-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Dec 29 2021 Igor Raits <igor.raits@gmail.com> - 3.3.1^803g76a336d647e-2
- Add missing BuildRequires for tests

* Wed Dec 29 2021 Igor Raits <igor.raits@gmail.com> - 3.3.1^803g76a336d647e-1
- Update to 3.3.1-803-g76a336d64

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 07 2021 Siteshwar Vashisht <svashisht@redhat.com> - 3.3.1-1
- Update to 3.3.1
  Resolves: #1979734

* Thu Jul 01 2021 Siteshwar Vashisht <svashisht@redhat.com> - 3.3.0-1
- Update to 3.3.0
  Resolves: #1947062

* Tue Mar 30 2021 Jonathan Wakely <jwakely@redhat.com> - 3.2.1-2
- Rebuilt for removed libstdc++ symbol (#1937698)

* Thu Mar 18 2021 Siteshwar Vashisht <svashisht@redhat.com> - 3.2.1-1
- Update to 3.2.1
  Resolves: #1940398

* Sat Mar 13 2021 Siteshwar Vashisht <svashisht@redhat.com> - 3.2.0-1
- Update to 3.2.0
  Resolves: #1933886

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Aug 25 2020 Oliver Falk <oliver@linux-kernel.at> - 3.1.2-5
- Correct pkgconfig references to /usr/local (RHBZ#1869376)

* Mon Aug 17 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 3.1.2-4
- Remove automagic Python bytecompilation | Fix FTBFS f33 | RH#1863559

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.2-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

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

## END: Generated by rpmautospec
