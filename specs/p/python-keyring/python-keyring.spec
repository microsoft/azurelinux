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

%bcond tests 1
%bcond desktop_tests 1

Name:           python-keyring
Version:        25.7.0
Release:        %autorelease
Summary:        Store and access your passwords safely

# SPDX
License:        MIT
URL:            https://github.com/jaraco/keyring
Source:         %{pypi_source keyring}

BuildSystem:            pyproject
BuildOption(generate_buildrequires): -x %{?with_tests:test,}completion
BuildOption(install):   -l keyring
# - keyring.backends.macOS does not import on this platform
# - keyring.devpi_client and keyring.testing are test hooks that require pluggy
#   and/or pytest; we can import them only if the test dependencies are present
BuildOption(check):     %{shrink:
                        -e 'keyring.backends.macOS*'
                        %{?!with_tests:-e 'keyring.devpi_client'}
                        %{?!with_tests:-e 'keyring.testing*'}
                        }

BuildArch:      noarch

BuildRequires:  help2man
BuildRequires:  tomcli

%if %{with tests}
%if %{with desktop_tests}
# Run graphical tests in non-graphical build environment.
BuildRequires:  xwayland-run
# Enable libsecret backend
BuildRequires:  python3-gobject
BuildRequires:  libsecret
BuildRequires:  gnome-keyring
BuildRequires:  /usr/bin/dbus-launch
%endif
%endif

%global desc %{expand:
The Python keyring library provides an easy way to access the system keyring
service from python. It can be used in any application that needs safe password
storage.

These recommended keyring backends are supported:

  • macOS Keychain
  • Freedesktop Secret Service supports many DE including GNOME (requires
    secretstorage)
  • KDE4 & KDE5 KWallet (requires dbus)
  • Windows Credential Locker

Other keyring implementations are available through third-party backends.}


%description %desc


%package -n     python3-keyring
Summary:        Python 3 library to access the system keyring service

Recommends:     python3-keyring+completion = %{version}-%{release}

%description -n python3-keyring %desc


# We don’t use “%%pyproject_extras_subpkg -n python3-keyring completion”
# because we want to add the completion scripts to the files list and provide a
# custom summary and description.
%package -n     python3-keyring+completion
Summary:        Shell completion support for the keyring command

Requires:       python3-keyring = %{version}-%{release}

%description -n python3-keyring+completion
This package:

• Makes sure the “completion” extra dependencies are installed
• Installs the actual shell completion scripts

There may be additional requirements to enable completion support *in general*
for a particular shell. For example, bash needs the bash-completion package to
be installed.


%prep -a
# This will be installed in site-packages without the executable bit set, so
# the shebang should be removed.
sed -r -i '1{/^#!/d}' keyring/cli.py

# The coherent.licensed build dependency copies a license file from outside the
# repository; see https://github.com/jaraco/skeleton/issues/174 for an overview
# of how this is supposed to work. This would need some sort of workaround if
# we were building from a GitHub source archive, since its normal operation
# requires network access. Fortunately, we’re using the PyPI sdist, so the
# LICENSE file is already copied in, and we can simply omit the dependency.
tomcli set pyproject.toml lists delitem build-system.requires \
    'coherent\.licensed\b.*'


%install -a
# Generate both completions and man pages in %%install rather than in %%build
# so we can use the actual generated entry point. For completions in
# particular, this is very important; see RHBZ#2408842.

install -d '%{buildroot}%{bash_completions_dir}'
%{py3_test_envvars} keyring --print-completion bash |
    tee '%{buildroot}%{bash_completions_dir}/keyring'
install -d '%{buildroot}%{zsh_completions_dir}'
%{py3_test_envvars} keyring --print-completion zsh |
    tee '%{buildroot}%{zsh_completions_dir}/_keyring'
install -d '%{buildroot}%{_sysconfdir}/profile.d'
%{py3_test_envvars} keyring --print-completion tcsh |
    tee '%{buildroot}%{_sysconfdir}/profile.d/keyring.csh'

install -d '%{buildroot}%{_mandir}/man1'
%{py3_test_envvars} help2man --no-info --version-string='%{version}' \
    --output='%{buildroot}%{_mandir}/man1/keyring.1' keyring


%check -a
%if %{with tests}

%if %{with desktop_tests}
%global __pytest xwfb-run -- pytest
%endif

%pytest -k "${k-}" ${ignore-} -rs
%endif


%files -n python3-keyring -f %{pyproject_files}
%doc NEWS.rst
%doc README.rst

%{_bindir}/keyring
%{_mandir}/man1/keyring.1*


%files -n python3-keyring+completion
%{bash_completions_dir}/keyring
%{zsh_completions_dir}/_keyring
%config(noreplace) %{_sysconfdir}/profile.d/keyring.csh

%ghost %dir %{python3_sitelib}/*.dist-info


%changelog
## START: Generated by rpmautospec
* Wed Apr 22 2026 azldev <azurelinux@microsoft.com> - 25.7.0-3
- Latest state for python-keyring

* Mon Nov 17 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 25.7.0-2
- Avoid build-time dependency on python3-coherent-licensed

* Mon Nov 17 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 25.7.0-1
- Update to 25.7.0 (close RHBZ#2415263)

* Fri Oct 31 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 25.6.0-13
- Generate completions with the correct entry-point name
- Fixes RHBZ#2408842

* Fri Oct 31 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 25.6.0-12
- Simplify man-page generation

* Wed Oct 22 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 25.6.0-11
- Improve completion extra metapackage

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 25.6.0-9
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 25.6.0-8
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 25.6.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 25.6.0-6
- Rebuilt for Python 3.14

* Mon May 05 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 25.6.0-5
- F41+: Use the provisional pyproject declarative buildsystem

* Sat Apr 05 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 25.6.0-4
- Skip multiprocessing tests on EPEL10

* Sat Apr 05 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 25.6.0-3
- De-conditionalize pyfakefs test dependency

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 25.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Dec 26 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 25.6.0-1
- Update to 25.6.0 (close RHBZ#2334086)

* Thu Nov 07 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 25.5.0-1
- Update to 25.5.0 (close RHBZ#2321932)

* Fri Oct 18 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 25.4.1-6
- Allow testing without pyfakefs, e.g. in EPEL10

* Fri Oct 18 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 25.4.1-5
- Use generated BuildRequires for tests

* Mon Sep 23 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 25.4.1-4
- Try enabling the “desktop” tests by default

* Mon Sep 23 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 25.4.1-3
- Replace xvfb-run with xwfb-run, from xwayland-run

* Sun Sep 22 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 25.4.1-2
- Print reasons for skipped tests

* Sun Sep 22 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 25.4.1-1
- Update to 25.4.1 (close RHBZ#2313823)

* Tue Sep 17 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 25.4.0-1
- Update to 25.4.0 (close RHBZ#2312884)

* Sun Aug 04 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 25.3.0-1
- Update to 25.3.0 (close RHBZ#2302573)

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 25.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 25.2.0-2
- Rebuilt for Python 3.13

* Fri Apr 26 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 25.2.0-1
- Update to 25.2.0 (close RHBZ#2277383)

* Fri Apr 05 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 25.1.0-1
- Update to 25.1.0 (close RHBZ#2271201)

* Fri Apr 05 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 25.0.1-1
- Update to 25.0.1

* Sat Mar 30 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 25.0.0-1
- Update to 25.0.0 (close RHBZ#2271201)

* Tue Feb 27 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 24.3.1-1
- Update to 24.3.1 (close RHBZ#2266385)

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 24.3.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 24.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 18 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 24.3.0-4
- Assert that %%pyproject_files contains a license file

* Mon Nov 13 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 24.3.0-1
- Update to 24.3.0 (close RHBZ#2249415)

* Mon Nov 13 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 24.2.0-11
- Add a generated man page

* Mon Nov 13 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 24.2.0-10
- F40+: Drop “keyring-python3” compat executable

* Mon Nov 13 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 24.2.0-8
- Confirm License is SPDX MIT

* Mon Sep 25 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 24.2.0-2
- Bump release after python-keyring-24.2.0-1.fc40 was untagged

* Fri Sep 01 2023 Tomáš Hrnčiar <thrnciar@redhat.com> - 24.2.0-1
- Update to 24.2.0
- Fixes: rhbz#2154699
- Upstream removed Python-2.0.1 license option; now only MIT
- Add subpackage for “completions” extra
- Replace deprecated pyproject_build_lib macro
- Drop unwanted shebang in keyring/cli.py

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 23.11.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jul 01 2023 Python Maint <python-maint@redhat.com> - 23.11.0-4
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 23.11.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Dec 08 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 23.11.0-2
- Correct dual license expression from AND to OR

* Mon Nov 21 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 23.11.0-1
- Update to 23.11.0 (close RHBZ#2140241)

* Fri Nov 18 2022 Christopher Tubbs <ctubbsii@fedoraproject.org> - 23.9.3-2
- Convert license to SPDX

* Sat Sep 24 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 23.9.3-1
- Update to 23.9.3 (close RHBZ#2127652)

* Mon Sep 05 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 23.9.1-1
- Update to 23.9.1 (close RHBZ#2123348)

* Fri Aug 12 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 23.8.2-1
- Update to 23.8.2 (close RHBZ#2107061)

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 23.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 14 2022 Python Maint <python-maint@redhat.com> - 23.6.0-2
- Rebuilt for Python 3.11

* Tue May 24 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 23.5.1-1
- Update to 23.5.1 (close RHBZ#2089081)

* Wed Apr 06 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 23.5.0-3
- Switch to pyproject-rpm-macros

* Wed Apr 06 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 23.5.0-2
- Fix rather than skipping test_entry_point

* Thu Mar 24 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 23.5.0-1
- Update to 23.5.0 (close RHBZ#1920125)
- Drop EPEL8 compatibility in the Fedora spec file: this upstream release
  requires setuptools features not available in EPEL8
- Allow using xvfb to run the tests for the libsecret backend; disable by
  default because tests occasionally hang in koji when doing so

* Tue Mar 22 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 21.8.0-6
- Drop workarounds for EPEL7 and for EOL Fedoras
- Update description text from upstream
- Stop using deprecated nose package for tests

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 21.8.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 21.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 21.8.0-3
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 21.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan 13 2021 Joel Capitao <jcapitao@redhat.com> - 21.8.0-1
- Update to 21.8.0 (rhbz#1910110)

* Mon Nov 09 2020 Joel Capitao <jcapitao@redhat.com> - 21.5.0-1
- Update to 21.5.0 (rhbz#1873845)

* Mon Aug 24 2020 Christopher Tubbs <ctubbsii@fedoraproject.org> - 21.3.1-1
- new version 21.3.1 (rhbz#1871352)

* Wed Aug 12 2020 Merlin Mathesius <mmathesi@redhat.com> - 21.3.0-2
- Drop manual (Build)Requires on python3-importlib-metadata for RHEL9+ and ELN.

* Mon Aug 03 2020 Christopher Tubbs <ctubbsii@fedoraproject.org> - 21.3.0-1
- new version 21.3.0 (rhbz#1810846)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 21.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 21.2.0-2
- Rebuilt for Python 3.9

* Fri Apr 17 2020 Christopher Tubbs <ctubbsii@fedoraproject.org> - 21.2.0-1
- new version (rhbz#1810846)

* Tue Feb 11 2020 Christopher Tubbs <ctubbsii@fedoraproject.org> - 21.1.0-1
- new version 21.1.0 (rhbz#1790114)

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 21.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 10 2020 Christopher Tubbs <ctubbsii@fedoraproject.org> - 21.0.0-1
- new version 21.0.0 (rhbz#1782317)

* Wed Dec 04 2019 Fabio Valentini <decathorpe@gmail.com> - 19.3.0-2
- Drop manual (Build)Requires on python3-importlib-metadata in rawhide/f32.

* Tue Dec 03 2019 Christopher Tubbs <ctubbsii@fedoraproject.org> - 19.3.0-1
- new version 19.3.0 (rhbz#1778416)

* Fri Sep 20 2019 Christopher Tubbs <ctubbsii@fedoraproject.org> - 19.2.0-1
- new version 19.2.0 (rhbz#1751298)

* Thu Aug 22 2019 Christopher Tubbs <ctubbsii@fedoraproject.org> - 19.1.0-1
- new version 19.1.0 (rhbz#1744382)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 19.0.2-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 19.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue May 21 2019 Christopher Tubbs <ctubbsii@fedoraproject.org> - 19.0.2-1
- new version 19.0.2 (rhbz#1711472)

* Thu May 09 2019 Orion Poplawski <orion@nwra.com> - 19.0.1-2
- Drop BR on pytest-cache

* Thu Mar 28 2019 Christopher Tubbs <ctubbsii@fedoraproject.org> - 19.0.1-1
- Update to 19.0.1 (rhbz#1691871)

* Fri Feb 08 2019 Yatin Karel <ykarel@redhat.com> - 17.1.1-1
- Update to 17.1.1

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 15.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Dec 11 2018 David King <amigadave@amigadave.com> - 15.2.0-1
- Update to 15.2.0

* Thu Oct 18 2018 Miro Hrončok <mhroncok@redhat.com> - 13.2.1-4
- Remove python2 subpackage from Fedora 30+

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 13.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jul 07 2018 Miro Hrončok <mhroncok@redhat.com> - 13.2.1-2
- Add missing dependency on entrypoints (#1598998)

* Fri Jul 06 2018 Christopher Tubbs <ctubbsii@fedoraproject.org> - 13.2.1-1
- Update to 13.2.1

* Thu Jul 05 2018 Christopher Tubbs <ctubbsii@fedoraproject.org> - 13.2.0-1
- Update to 13.2.0

* Mon Jun 18 2018 Miro Hrončok <mhroncok@redhat.com> - 11.0.0-4
- Rebuilt for Python 3.7

* Fri Mar 09 2018 Iryna Shcherbina <ishcherb@redhat.com> - 11.0.0-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Mar 08 2018 Christopher Tubbs <ctubbsii@fedoraproject.org> - 11.0.0-2
- Remove unused BR pycryptopp (rhbz#1552676)

* Mon Mar  5 2018 Haïkel Guémar <hguemar@fedoraproject.org> - 11.0.0-1
- Upstream 11.0.0 (RHBZ#1539962)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 10.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 12 2018 Christopher Tubbs <ctubbsii@fedoraproject.org> - 10.6.0-1
- Update to 10.6.0 (rhbz#1532092)

* Thu Dec 21 2017 Christopher Tubbs <ctubbsii@fedoraproject.org> - 10.5.1-1
- Update to 10.5.1; fix AttributeError with kwallet backend (bz#1526653)

* Thu Nov 16 2017 Christopher Tubbs <ctubbsii@fedoraproject.org> - 10.5.0-1
- Update to 10.5.0; bz#1512519

* Mon Aug 28 2017 Christopher Tubbs <ctubbsii@fedoraproject.org> - 10.4.0-2
- Use python2-* naming conventions for *Requires

* Mon Aug 28 2017 Christopher Tubbs <ctubbsii@fedoraproject.org> - 10.4.0-1
- Update to python-keyring 10.4.0 (bz#1464676)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 10.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Apr 11 2017 Christopher Tubbs <ctubbsii@fedoraproject.org> - 10.3.2-2
- Fix dependency on setuptools_scm for f25

* Mon Apr 10 2017 Christopher Tubbs <ctubbsii@fedoraproject.org> - 10.3.2-1
- Update to python-keyring 10.3.2

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 9.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 22 2016 Miro Hrončok <mhroncok@redhat.com> - 9.0-6
- Rebuild for Python 3.6

* Wed Dec 21 2016 Christopher Tubbs <ctubbsii@fedoraproject.org> - 9.0-5
- Add dependency on python-SecretStorage (bz#1328218,bz#1398710)

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 9.0-4
- Rebuild for Python 3.6

* Mon Nov 21 2016 Orion Poplawski <orion@cora.nwra.com> - 9.0-3
- Enable python 3 build for EPEL
- Ship python2-keyring
- Modernize spec

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.0-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Mon May 02 2016 Matthias Runge <mrunge@redhat.com> - 9.0-1
- update to 9.0, resolves rhbz#1271641, rhbz#1195985

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Oct 13 2015 Robert Kuska <rkuska@redhat.com> - 5.0-3
- Rebuilt for Python3.5 rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Feb 04 2015 Christopher Meng <rpm@cicku.me> - 5.0-1
- Update to 5.0
- Revise license tag to match upstream.

* Sat Aug 02 2014 Christopher Meng <rpm@cicku.me> - 4.0-1
- Update to 4.0

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 3.8-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Tue May 13 2014 Christopher Meng <rpm@cicku.me> - 3.8-1
- Update to 3.8

* Sat Mar 08 2014 Christopher Meng <rpm@cicku.me> - 3.6-1
- Update to 3.6

* Thu Feb 13 2014 Christopher Meng <rpm@cicku.me> - 3.4-1
- Update to 3.4(BZ#1064256)
- Ensure the obsolete line works for the old packages really.

* Mon Dec 02 2013 Christopher Meng <rpm@cicku.me> - 3.3-1
- Update to 3.3(BZ#1007354,BZ#872262)
- Cleanup dependencies mess(BZ#1030944).
- Optimize the %%changelog section of the spec.

* Tue Oct 22 2013 Ratnadeep Debnath <rtnpro@gmail.com> - 3.1-1
- Bump to version 3.1

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Ratnadeep Debnath <rtnpro@gmail.com> 0.7-1
- Python 3 is now supported. All tests now pass under Python 3.2 on Windows and
Linux (although Linux backend support is limited). Fixes #28.
- Extension modules on Mac and Windows replaced by pure-Python ctypes
implementations. Thanks to Jérôme Laheurte.
- WinVaultKeyring now supports multiple passwords for the same service.
Fixes #47.
- Most of the tests don't require user interaction anymore.
- Entries stored in Gnome Keyring appears now with a meaningful name if you try
to browser your keyring (for ex. with Seahorse)
- Tests from Gnome Keyring no longer pollute the user own keyring.
- keyring.util.escape now accepts only unicode strings. Don't try to encode
strings passed to it.

* Tue Nov 08 2011 Ratnadeep Debnath <rtnpro@gmail.com> 0.6.2-1
- fix compiling on OSX with XCode 4.0
- Gnome keyring should not be used if there is no DISPLAY or if the dbus is not around
    (https://bugs.launchpad.net/launchpadlib/+bug/752282).
- Added keyring.http for facilitating HTTP Auth using keyring.
- Add a utility to access the keyring from the command line.

* Mon Jan 10 2011 Ratnadeep Debnath <rtnpro@gmail.com> 0.5.1-1
- Remove a spurious KDE debug message when using KWallet
- Fix a bug that caused an exception if the user canceled the KWallet dialog

* Sun Nov 28 2010 Ratnadeep Debnath <rtnpro@gmail.com> 0.5-2
- Removed sub-packages: gnome and kwallet; removed "Requires: PyKDE4 PyQt4"

* Mon Nov 22 2010 Ratnadeep Debnath <rtnpro@gmail.com> 0.5-1
- RPM for keyring-0.5

* Mon Nov 01 2010 Ratnadeep Debnath <rtnpro@gmail.com> 0.4-1
- Updated rpm to python-keyring version 0.4

* Sat Oct 30 2010 Ratnadeep Debnath <rtnpro@gmail.com> 0.2-4
- Filtered gnome_keyring.so from the provides list, removed kdelibs-devel

* Sat Oct 02 2010 Ratnadeep Debnath <rtnpro@gmail.com> 0.2-3
- Updated dependencies to kdelibs4-devel, some cleanup

* Tue Aug 24 2010 Ratnadeep Debnath <rtnpro@gmail.com> 0.2-2
- Some updates according to bugzilla reviews

* Sat Jun 26 2010 Ratnadeep Debnath <rtnpro@gmail.com> 0.2-1.3
- Some cleanup

* Sat Jun 26 2010 Felix Schwarz <felix.schwarz@oss.schwarz.eu> 0.2-1.2
- add KWallet subpackage

* Mon Jun 21 2010 Felix Schwarz <felix.schwarz@oss.schwarz.eu> 0.2-1.1
- add build dependencies
- create subpackage for gnome, disable KWallet for now
- look for files in arch-dependend site-packages

* Tue May 25 2010 Ratnadeep Debnath <rtnpro@gmail.com> 0.2-1
- Incorporated some changes with reference to http://vcrhonek.fedorapeople.org/python-keyring/python-keyring.spec
- Fixed some rpmlint errors

* Wed May 19 2010 Ratnadeep Debnath <rtnpro@gmail.com> 0.2
- Initial RPM package

## END: Generated by rpmautospec
