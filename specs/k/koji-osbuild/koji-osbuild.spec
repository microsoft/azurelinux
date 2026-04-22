# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Do not build with tests by default
# Pass --with tests to rpmbuild to override
%bcond_with tests

%global         forgeurl https://github.com/osbuild/koji-osbuild

Name:           koji-osbuild
Version:        12
Release: 7%{?dist}
Summary:        Koji integration for osbuild composer

%forgemeta

License:        Apache-2.0
URL:            %{forgeurl}
Source0:        %{forgesource}

BuildArch:      noarch
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}dist(setuptools)

%description
Koji integration for osbuild composer.

%package        hub
Summary:        Koji hub plugin for osbuild composer integration
Requires:       %{name} = %{version}-%{release}
Requires:       koji-hub
Requires:       python3-jsonschema

%description    hub
Koji hub plugin for osbuild composer integration.

%package        builder
Summary:        Koji hub plugin for osbuild composer integration
Requires:       %{name} = %{version}-%{release}
Requires:       koji-builder
Requires:       python3-requests

%description    builder
Koji builder plugin for osbuild composer integration.

%package        cli
Summary:        Koji client plugin for osbuild composer integration
Requires:       %{name} = %{version}-%{release}
Requires:       koji

%description    cli
Koji client plugin for osbuild composer integration.

%prep
%forgesetup

%build
# no op

%install
install -d %{buildroot}/%{_prefix}/lib/koji-hub-plugins
install -p -m 0755 plugins/hub/osbuild.py %{buildroot}/%{_prefix}/lib/koji-hub-plugins/
%py_byte_compile %{__python3} %{buildroot}/%{_prefix}/lib/koji-hub-plugins/osbuild.py

install -d %{buildroot}/%{_prefix}/lib/koji-builder-plugins
install -p -m 0755 plugins/builder/osbuild.py %{buildroot}/%{_prefix}/lib/koji-builder-plugins/
%py_byte_compile %{__python3} %{buildroot}/%{_prefix}/lib/koji-builder-plugins/osbuild.py

install -d %{buildroot}%{python3_sitelib}/koji_cli_plugins
install -p -m 0644 plugins/cli/osbuild.py %{buildroot}%{python3_sitelib}/koji_cli_plugins/osbuild.py
%py_byte_compile %{__python3} %{buildroot}%{python3_sitelib}/koji_cli_plugins/osbuild.py


%if %{with tests}
# Tests
install -m 0755 -vd                                             %{buildroot}/%{_libexecdir}/tests/%{name}
install -m 0755 -vp test/integration.sh                         %{buildroot}/%{_libexecdir}/tests/%{name}/

install -m 0755 -vd                                             %{buildroot}/%{_libexecdir}/%{name}-tests
install -m 0755 -vp test/make-certs.sh                          %{buildroot}/%{_libexecdir}/%{name}-tests/
install -m 0755 -vp test/build-container.sh                     %{buildroot}/%{_libexecdir}/%{name}-tests/
install -m 0755 -vp test/run-koji-container.sh                  %{buildroot}/%{_libexecdir}/%{name}-tests/
install -m 0755 -vp test/run-openid.sh                          %{buildroot}/%{_libexecdir}/%{name}-tests/
install -m 0755 -vp test/copy-creds.sh                          %{buildroot}/%{_libexecdir}/%{name}-tests/
install -m 0755 -vp test/run-builder.sh                         %{buildroot}/%{_libexecdir}/%{name}-tests/
install -m 0755 -vp test/make-tags.sh                           %{buildroot}/%{_libexecdir}/%{name}-tests/

install -m 0755 -vd                                             %{buildroot}/%{_libexecdir}/%{name}-tests/integration
install -m 0755 -vp test/integration/*                          %{buildroot}/%{_libexecdir}/%{name}-tests/integration/

install -m 0755 -vd                                             %{buildroot}/%{_datadir}/%{name}-tests

install -m 0755 -vd                                             %{buildroot}/%{_datadir}/%{name}-tests/data
install -m 0755 -vp test/data/*                                 %{buildroot}/%{_datadir}/%{name}-tests/data/

install -m 0755 -vd                                             %{buildroot}/%{_datadir}/%{name}-tests/container
install -m 0755 -vp test/container/brew.repo                    %{buildroot}/%{_datadir}/%{name}-tests/container/

install -m 0755 -vd                                             %{buildroot}/%{_datadir}/%{name}-tests/container/builder
install -m 0755 -vp test/container/builder/Dockerfile.fedora    %{buildroot}/%{_datadir}/%{name}-tests/container/builder/
install -m 0755 -vp test/container/builder/Dockerfile.rhel      %{buildroot}/%{_datadir}/%{name}-tests/container/builder/
install -m 0755 -vp test/container/builder/kojid.conf           %{buildroot}/%{_datadir}/%{name}-tests/container/builder/
install -m 0755 -vp test/container/builder/osbuild-koji.conf    %{buildroot}/%{_datadir}/%{name}-tests/container/builder/
install -m 0755 -vp test/container/builder/osbuild.krb5.conf    %{buildroot}/%{_datadir}/%{name}-tests/container/builder/
install -m 0755 -vp test/container/builder/run-kojid.sh         %{buildroot}/%{_datadir}/%{name}-tests/container/builder/

install -m 0755 -vd                                             %{buildroot}/%{_datadir}/%{name}-tests/container/hub
install -m 0755 -vp test/container/hub/Dockerfile.fedora        %{buildroot}/%{_datadir}/%{name}-tests/container/hub/
install -m 0755 -vp test/container/hub/Dockerfile.rhel          %{buildroot}/%{_datadir}/%{name}-tests/container/hub/
install -m 0755 -vp test/container/hub/hub.conf                 %{buildroot}/%{_datadir}/%{name}-tests/container/hub/
install -m 0755 -vp test/container/hub/kojiweb.conf             %{buildroot}/%{_datadir}/%{name}-tests/container/hub/
install -m 0755 -vp test/container/hub/run-hub.sh               %{buildroot}/%{_datadir}/%{name}-tests/container/hub/
install -m 0755 -vp test/container/hub/ssl.conf                 %{buildroot}/%{_datadir}/%{name}-tests/container/hub/
install -m 0755 -vp test/container/hub/web.conf                 %{buildroot}/%{_datadir}/%{name}-tests/container/hub/

install -m 0755 -vd                                             %{buildroot}/%{_datadir}/%{name}-tests/container/hub/plugin
install -m 0755 -vp test/container/hub/plugin/osbuild.py        %{buildroot}/%{_datadir}/%{name}-tests/container/hub/

%endif

%files
%license LICENSE
%doc README.md

%files hub
%{_prefix}/lib/koji-hub-plugins/osbuild.py
%{_prefix}/lib/koji-hub-plugins/__pycache__/osbuild.*

%files builder
%{_prefix}/lib/koji-builder-plugins/osbuild.py
%{_prefix}/lib/koji-builder-plugins/__pycache__/osbuild.*

%files cli
%{python3_sitelib}/koji_cli_plugins/osbuild.py
%{python3_sitelib}/koji_cli_plugins/__pycache__/osbuild.*

%if %{with tests}

%package tests
Summary:        Integration tests for koji-osbuild
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-cli
Requires:       container-selinux
Requires:       dnsmasq
Requires:       jq
Requires:       koji
Requires:       krb5-workstation
Requires:       openssl
Requires:       osbuild-composer >= 58
Requires:       osbuild-composer-tests
Requires:       podman
Requires:       python3-boto3

%description tests
Integration tests for koji-osbuild. To be run on a dedicated system.

%files tests
%{_libexecdir}/tests/%{name}
%{_libexecdir}/%{name}-tests
%{_datadir}/%{name}-tests

%endif


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 12-6
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 12-5
- Rebuilt for Python 3.14.0rc2 bytecode

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 12-3
- Rebuilt for Python 3.14

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Nov 14 2024 Packit <hello@packit.dev> - 12-1
Changes with 12
----------------
  * Actions: add workflow for marking and closing stale issues and PRs (#124)
    * Author: Tomáš Hozza, Reviewers: Achilleas Koutsou
  * build(deps): bump ludeeus/action-shellcheck from 1.1.0 to 2.0.0 (#115)
    * Author: dependabot[bot], Reviewers: Ondřej Budai
  * ci: add Fedora 37 (#111)
    * Author: Ondřej Budai, Reviewers: Tomáš Hozza
  * docs: Update architecture diagram (#114)
    * Author: Simon Steinbeiß, Reviewers: Tomáš Hozza
  * hub: mark baseurl as required in repo schema (#112)
    * Author: Tomáš Hozza, Reviewers: Ondřej Budai
  * koji-osbuild.spec: migrate the license field to SPDX (#113)
    * Author: Ondřej Budai, Reviewers: Tomáš Hozza
  * plugin/builder: increase retries for requests to composer (#128)
    * Author: Sanne Raymaekers, Reviewers: Simon de Vlieger

— Somewhere on the Internet, 2024-11-14


* Wed Jul 24 2024 Miroslav Suchý <msuchy@redhat.com> - 11-9
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 11-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 11-7
- Rebuilt for Python 3.13

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 11-3
- Rebuilt for Python 3.12

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Nov 21 2022 Packit <hello@packit.dev> - 11-1
Changes with 11
----------------
  * Print more log messages to enable tracking of SLIs (#110)
  * Various fixes (#108)

Contributions from: Simon Steinbeiss, Thomas Lavocat, Tomáš Hozza

— Somewhere on the Internet, 2022-11-21



* Fri Sep 02 2022 Packit <hello@packit.dev> - 10-1
Changes with 10
----------------
  * Hub: support `image_type` being an array for backwards compatibility (#107)
  * packit: Enable Bodhi updates workflow (#106)
Contributions from: Tomas Hozza
— Somewhere on the Internet, 2022-09-02





* Wed Aug 31 2022 Packit <hello@packit.dev> - 9-1
Changes with 9
----------------
  * Support specifying upload options for image builds (#104)
  * Various enhancements (#105)
  * builder: add retries to composer API calls (#103)
Contributions from: Ondřej Budai, Tomas Hozza
— Somewhere on the Internet, 2022-08-31





* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jun 30 2022 Packit <hello@packit.dev> - 8-1
Changes with 8
----------------
  * builder: always refresh OAuth token after getting 401 (#102)
Contributions from: Ondřej Budai
— Somewhere on the Internet, 2022-06-30





* Wed Jun 29 2022 Packit <hello@packit.dev> - 7-1
Changes with 7
----------------
  * builder: set OAuth token creation time before we fetch it (#101)
  * packit: Enable Koji build integration (#99)
  * spec: set the default release to 1 (#98)
Contributions from: Jakub Rusz, Ondřej Budai, Simon Steinbeiss
— Somewhere on the Internet, 2022-06-29





* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 6-1
- Rebuilt for Python 3.11

* Tue May 03 2022 Packit <hello@packit.dev> - 6-0
Changes with 6
----------------
  * builder: add support for proxying requests to composer  (#96)
  * devcontainer: remove trailing comma from JSON (#95)
  * plugins: add support for customizations (#97)
  * workflows/trigger-gitlab: run Gitlab CI in new image-builder project (#94)
Contributions from: Christian Kellner, Jakub Rusz, Ondřej Budai
— Somewhere on the Internet, 2022-05-03





* Mon Mar 28 2022 Packit Service <user-cont-team+packit-service@redhat.com> - 5-0
CHANGES WITH 5:
----------------
  * builder: rename gpg_key field to gpgkey for repos (#91)
  * builder: fix type annotations (#92)
  * Add GitHub Action to create upstream tag (#90)
  * docs: fix error in hacking.md (#85)
  * build(deps): bump actions/checkout from 2 to 3 (#86)
  * spec: don't push tests into Fedora (#89)
  * test/builder: drop misleading quotes from config (#88)
  * builder: use correct secret when fetching token (#87)
  * packit: Push directly to dist-git (#84)
Contributions from: Christian Kellner, Ondřej Budai, Simon Steinbeiss, Stephen Coady, dependabot[bot]
— Somewhere on the Internet, 2022-03-28





* Tue Feb 15 2022 Packit Service <user-cont-team+packit-service@redhat.com> - 4-0
CHANGES WITH 4:
----------------
  * plugins: support for repo package sets (#82)
  * Lower task weight (#60)
  * Add upstream release bot and enable packit (#81)
  * plugins: support for ostree specific options (#80)
  * builder: use cloud api (#73)
  * README: contributing (#74)
  * README.md,HACKING.md: update for SSO/OAuth2 (#79)
  * Support for oauth2 authentication (#69)
  * ci: switch from rhel 8.4 to 8.5 (#78)
  * ci: integration tests now adapt to the host (#77)
  * schutzbot: update osbuild to 46 (#75)
  * cli: do not use translation helper (#72)
  * `builder`: fixes for the command line argument parsing (#71)
  * Fix command line argument names (#70)
  * devcontainer: add initial support (#68)
  * schutzbot: remove ssh keys of team member that left us (#67)
  * CI: Fix failure in Coverity Scan (#66)
  * ci: Enable Coverity Scan (#65)
  * Adjust variable names (#64)
  * build(deps): bump ludeeus/action-shellcheck from 0.5.0 to 1.1.0 (#63)
  * test: use importlib instead of imp (#62)
  * Enable Dependabot (#61)
  * plugin/cli: remove type annotation (#59)
  * Migrate to GitLab CI (#58)
  * Test and CI maintenance (#57)
  * Fetch and attach the manifests (#56)
  * Test housekeeping (#55)
  * assorted CI fixes/improvements (#54)
  * Add Fedora 33 to Schutzbot & fix the name of repo (#52)
  * test/integration.sh: bump nightly (#53)
  * test: replace docker.io with fedora's registry (#50)
  * mockbuild: make more consistent with other osbuild projects (#49)
  * Update osbuild-composer dependency to 25 (#48)
Contributions from: Alexander Todorov, Chloe Kaubisch, Christian Kellner, Lars Karlitski, Ondřej Budai, Simon Steinbeiss, Tomas Kopecek
— Vöcklabruck, 2022-02-15





* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2-2
- Rebuilt for Python 3.10

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Nov  3 2020 Christian Kellner <ckellner@redhat.com> - 2-0
- Upstream release 2
- Add python3-jsonschema dependency for builder sub-package.

* Wed Sep 30 2020 Christian Kellner <ckellner@redhat.com> - 1-0
- Initial import.
