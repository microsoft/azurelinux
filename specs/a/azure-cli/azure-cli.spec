## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 3;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# The vast majority of azure-cli's tests require docker, networking, or both. 😢
%bcond_with     tests

# telemetry and testsdk don't follow azure-cli's versioning scheme.
# They have their own versions in the main repository.
%global         telemetry_version   1.1.0
# testsdk follows its own versioning scheme.
%global         testsdk_version     0.3.0

%global         srcname     azure-cli
%global         forgeurl    https://github.com/Azure/azure-cli
Version:        2.81.0
%global         tag         %{srcname}-%{version}
%global         distprefix  %{nil}
%forgemeta

Name:           %{srcname}
Release:        %autorelease
Summary:        Microsoft Azure Command-Line Tools
License:        MIT
URL:            %forgeurl
Source0:        %forgesource

# Offer azure-cli updates via dnf/rpm only.
# Avoid importing files from the local directory when running az.
# Source: https://github.com/Azure/azure-cli/pull/21261
Patch1:         az-fixes.patch

BuildArch:      noarch

%if 0%{?fedora}
# Only Fedora has antlr4 packages.
#
# Because antlr4 requires the JDK, it is not available on i686 in F37+. See:
#
# https://fedoraproject.org/wiki/Releases/37/ChangeSet#Drop_i686_builds_of_jdk8,11,17_and_latest_(18)_rpms_from_f37_onwards
# https://docs.fedoraproject.org/en-US/packaging-guidelines/#_arch_specific_runtime_and_build_time_dependencies
#
# Note that dropping i686 does not require a tracking bug due to:
#
# https://fedoraproject.org/wiki/Releases/37/ChangeSet#Encourage_Dropping_Unused_/_Leaf_Packages_on_i686
ExclusiveArch:  %{java_arches} noarch

BuildRequires:  antlr4
BuildRequires:  python3-antlr4-runtime
%endif

BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
BuildRequires:  pyproject-rpm-macros

%if %{with tests}
BuildRequires:  python3dist(azure-devtools)
BuildRequires:  python3dist(azure-mgmt-managedservices)
BuildRequires:  python3dist(decorator)
BuildRequires:  python3dist(pkginfo)
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(pytest-rerunfailures)
BuildRequires:  python3dist(pytest-xdist)
BuildRequires:  python3dist(vcrpy)
%endif

%description
Microsoft Azure Command-Line Tools

# python-azure-cli-core
%package -n python3-%{srcname}-core
Summary:        Microsoft Azure Command-Line Tools Core Module
Requires:       %{name} = %{version}-%{release}
%if 0%{?fedora}
Recommends:     python3-antlr4-runtime
%endif

%description -n python3-%{srcname}-core
Microsoft Azure Command-Line Tools Core Module

# python-azure-cli-telemetry
%package -n python3-%{srcname}-telemetry
Summary:        Microsoft Azure CLI Telemetry Package
Requires:       %{name} = %{version}-%{release}

%description -n python3-%{srcname}-telemetry
Microsoft Azure CLI Telemetry Package

# python-azure-cli-testsdk
%package -n python3-%{srcname}-testsdk
Summary:        Microsoft Azure CLI SDK testing tools
Requires:       %{name} = %{version}-%{release}

%description -n python3-%{srcname}-testsdk
Microsoft Azure CLI SDK testing tools


%prep
%forgeautosetup -p1

# This got bumped for a CVE but the CVE is only in 2.10.0 and F43 ships 2.8
sed -i 's/PyJWT==2.10.1/PyJWT>=2.1.0/' src/azure-cli/requirements.py3.Linux.txt

# Remove upper version boundaries on anything that isn't azure-related.
# Upstream has strict requirements on azure SDK packages, but many of the
# other requirements are set to versions too old for Fedora.
sed -i '/azure/!s/==/>=/' src/azure-cli/requirements.py3.Linux.txt
sed -i '/azure/!s/~=/>=/' src/azure-cli/setup.py
sed -i '/azure/!s/==/>=/' src/azure-cli/setup.py
sed -i '/azure/!s/~=/>=/' src/azure-cli-core/setup.py
sed -i '/azure/!s/==/>=/' src/azure-cli-core/setup.py

# This dependency is actually optional and used for telemetry anyway
sed -i '/py-deviceid/d' src/azure-cli-core/setup.py

# Temporary fix for azure-cli-2.64; upstream pinned to hdinsights 9.0b3 which should have been 9.1b1.
sed -i 's/azure-mgmt-hdinsight==9.0.0b3/azure-mgmt-hdinsight>=9,<10/' src/azure-cli/setup.py
sed -i 's/azure-mgmt-hdinsight==9.0.0b3/azure-mgmt-hdinsight>=9,<10/' src/azure-cli/requirements.py3.Linux.txt

sed -i 's/azure-monitor-query==1.2.0/azure-monitor-query>=1.2,<2/' src/azure-cli/setup.py
sed -i 's/azure-monitor-query==1.2.0/azure-monitor-query>=1.2,<2/' src/azure-cli/requirements.py3.Linux.txt

# Upstream broke themselves somehow since the pinned version conflicts with other packages
sed -i 's/azure-mgmt-resource==23.3/azure-mgmt-resource>=24.0/' src/azure-cli/setup.py
sed -i 's/azure-mgmt-resource==23.3/azure-mgmt-resource>=24.0/' src/azure-cli/requirements.py3.Linux.txt

# Rawhide has 1.7.1 at the moment
sed -i 's/azure-appconfiguration==1.7/azure-appconfiguration>=1.7,<2/' src/azure-cli/setup.py
sed -i 's/azure-appconfiguration==1.7/azure-appconfiguration>=1.7,<2/' src/azure-cli/requirements.py3.Linux.txt

# Namespace packages are no longer needed after Python 3.7, but upstream
# insists on carrying them.
sed -i '/nspkg/d' src/azure-cli/requirements.py3.Linux.txt

# portalocker 3 drops support for end-of-life Python versions
sed -i 's/portalocker>=1.6,<3/portalocker>=1.6,<4/' src/azure-cli-telemetry/setup.py
sed -i 's/portalocker==2.3.2/portalocker>=1.6,<4/' src/azure-cli/requirements.py3.Linux.txt

# The requirements file has requirements set for azure-cli-{core,telemetry,testsdk}
# but we can't install those until we actually build this package.
sed -i '/azure-cli.*/d' src/azure-cli/requirements.py3.Linux.txt

# certifi's version is irrelevant since the package is empty in Fedora.
sed -i 's/certifi.=.*$/certifi/' \
    src/azure-cli/requirements.py3.Linux.txt

# Remove the unnecessary secure extra from urllib3.
sed -i 's/urllib3\[secure\]/urllib3/' src/azure-cli/setup.py

# Remove the broker extra from msal because it would require the closed-source
# pymsalruntime.
sed -i 's/msal\[broker\]/msal/' src/azure-cli/setup.py
sed -i 's/msal\[broker\]/msal/' src/azure-cli/requirements.py3.Linux.txt
sed -i 's/msal\[broker\]/msal/' src/azure-cli-core/setup.py

# Be more flexible about the required azure-core
sed -i 's/^azure-core==.*$/azure-core>=1.28.0,<2/' src/azure-cli/requirements.py3.Linux.txt
sed -i 's/^azure-common==.*$/azure-common>=1.1.28,<2/' src/azure-cli/requirements.py3.Linux.txt
sed -i 's/azure-core~=1.35.0/azure-core>=1.35.0,<2/' src/azure-cli-core/setup.py

# Allow slightly older versions.
sed -i 's/^cryptography>=.*$/oauthlib>=37.0.2/' src/azure-cli/requirements.py3.Linux.txt
sed -i 's/^oauthlib>=.*$/oauthlib>=3.2.1/' src/azure-cli/requirements.py3.Linux.txt
sed -i 's/^packaging>=.*$/packaging>=21.3/' src/azure-cli/requirements.py3.Linux.txt
sed -i 's/^paramiko>=.*$/paramiko>=2.12.0/' src/azure-cli/requirements.py3.Linux.txt
sed -i 's/^pyOpenSSL>=.*$/pyOpenSSL>=21.0.0/' src/azure-cli/requirements.py3.Linux.txt
sed -i 's/^PyNaCl>=.*$/PyNaCl>=1.4.0/' src/azure-cli/requirements.py3.Linux.txt
sed -i 's/PyNaCl>=1.5.0/PyNaCl>=1.4.0/'  src/azure-cli/setup.py
sed -i 's/^requests\[socks\]>=.*$/requests[socks]>=2.28.2/' src/azure-cli/requirements.py3.Linux.txt

# Bring in the antlr4 python runtime manually to avoid a requires/provides mismatch.
sed -i '/antlr4-python3-runtime/d' src/azure-cli/requirements.py3.Linux.txt src/azure-cli/setup.py

# Allow an older argcomplete until we can get it updated in Fedora.
sed -i 's/argcomplete>=3.1.1/argcomplete>=2.0.0/' src/azure-cli-core/setup.py
sed -i 's/^argcomplete>=.*$/argcomplete>=2.0.0/' src/azure-cli/requirements.py3.Linux.txt

# Allow older versions for EPEL 9.
%if %{defined el9}
sed -i \
    -e 's/^argcomplete>=.*$/argcomplete>=1.12.0/' \
    -e 's/^cffi>=.*$/cffi>=1.12.0/' \
    -e 's/^distro>=.*$/distro>=1.5.0/' \
    -e 's/^Jinja2>=.*$/Jinja2>=2.11.3/' \
    -e 's/^jmespath>=.*$/jmespath>=0.9.4/' \
    -e 's/^MarkupSafe>=.*$/MarkupSafe>=1.1.1/' \
    -e 's/^oauthlib>=.*$/oauthlib>=3.1.1/' \
    -e 's/^packaging>=.*$/packaging>=20.9/' \
    -e 's/^psutil>=.*$/psutil>=5.8.0/' \
    -e 's/^requests\[socks\]>=.*$/requests[socks]>=2.25.1/' \
    -e 's/^six>=.*$/six>=1.15.0/' \
    -e 's/^urllib3>=.*$/urllib3>=1.26.5/' \
    -e 's/^websocket-client>=.*$/websocket-client>=1.2.3/' \
    src/azure-cli/requirements.py3.Linux.txt
sed -i \
    -e 's/websocket-client>=1.3.1/websocket-client>=1.2.3/' \
    src/azure-cli/setup.py
sed -i \
    -e 's/argcomplete>=3.1.1/argcomplete/' \
    -e 's/psutil>=5.9/psutil/' \
    src/azure-cli-core/setup.py
%endif


%generate_buildrequires
%pyproject_buildrequires -N src/azure-cli/requirements.py3.Linux.txt


%build

%if 0%{?fedora}
# Regenerate ANTLR files in Fedora only.
pushd src/azure-cli/azure/cli/command_modules/monitor/grammar/autoscale
antlr4 -Dlanguage=Python3 AutoscaleCondition.g4
cd ../metric_alert
antlr4 -Dlanguage=Python3 MetricAlertCondition.g4
popd
%endif

PROJECTS=("azure-cli azure-cli-core azure-cli-telemetry azure-cli-testsdk")
for PROJECT in ${PROJECTS[@]}; do
    pushd src/${PROJECT}
        %pyproject_wheel
    popd
done


%install
%pyproject_install

# Remove Windows/Powershell files.
rm -f %{buildroot}%{_bindir}/az.{bat,ps1}
rm -f %{buildroot}%{_bindir}/azps.ps1

# Install the az bash completion script properly.
install -Dp %{buildroot}%{_bindir}/az.completion.sh %{buildroot}%{_datadir}/bash-completion/completions/%{name}
rm -f %{buildroot}%{_bindir}/az.completion.sh


%if %{with tests}
%check
%pytest -n auto src/azure-cli-core
%pytest -n auto src/azure-cli-telemetry
%pytest -n auto src/azure-cli
%endif


%files
%doc README.md
%license LICENSE
# Executable-related files/directories.
%{_bindir}/az
# Bash completions.
%{_datadir}/bash-completion/completions/%{name}
%dir %{_datadir}/bash-completion
%dir %{_datadir}/bash-completion/completions
# Python sitelib files and directories.
%dir %{python3_sitelib}/azure
%{python3_sitelib}/azure/cli
%{python3_sitelib}/azure_cli-%{version}.dist-info/
# Prevent azure-cli from grabbing all of the files underneath azure/cli.
%exclude %{python3_sitelib}/azure/cli/core
%exclude %{python3_sitelib}/azure/cli/telemetry
%exclude %{python3_sitelib}/azure/cli/testsdk


%files -n python3-%{srcname}-core
%doc README.md
%{python3_sitelib}/azure/cli/core
%{python3_sitelib}/azure_cli_core-%{version}.dist-info/


%files -n python3-%{srcname}-testsdk
%doc README.md
%{python3_sitelib}/azure/cli/testsdk
%{python3_sitelib}/azure_cli_testsdk-%{testsdk_version}.dist-info/


%files -n python3-%{srcname}-telemetry
%doc README.md
%{python3_sitelib}/azure/cli/telemetry
%{python3_sitelib}/azure_cli_telemetry-%{telemetry_version}.dist-info/


%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 2.81.0-3
- test: add initial lock files

* Wed Feb 11 2026 Jeremy Cline <jeremycline@linux.microsoft.com> - 2.81.0-2
- Relax the dependency on azure-core

* Wed Dec 17 2025 Jeremy Cline <jeremycline@linux.microsoft.com> - 2.81.0-1
- Update to v2.81.0
- This differs from rawhide in that it drops the PyJWT requirement to 2.8
  which F43 ships, and is not vulnerable to the CVE in 2.10.0

* Tue Nov 04 2025 Jeremy Cline <jeremycline@linux.microsoft.com> - 2.79.0-1
- Update to v2.79.0

* Mon Nov 03 2025 Jeremy Cline <jeremycline@linux.microsoft.com> - 2.78.0-1
- Update to v2.78.0

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 2.74.0-6
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 2.74.0-5
- Rebuilt for Python 3.14.0rc2 bytecode

* Sun Jul 27 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 2.74.0-4
- Remove the broker extra from the msal dependency in azure-cli-core

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.74.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jul 23 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2.74.0-2
- Remove the broker extra from the msal dependency

* Wed Jun 25 2025 Jeremy Cline <jeremycline@linux.microsoft.com> - 2.74.0-1
- Update to v2.74

* Mon Jun 23 2025 Python Maint <python-maint@redhat.com> - 2.71.0-4
- Rebuilt for Python 3.14

* Mon May 19 2025 Matej Focko <mfocko@redhat.com> - 2.71.0-3
- Fix tag template for Packit

* Thu May 01 2025 Jeremy Cline <jeremycline@linux.microsoft.com> - 2.71.0-1
- Update to v2.71.0

* Tue Mar 18 2025 Jeremy Cline <jeremycline@linux.microsoft.com> - 2.70.0-1
- Update to v2.70.0

* Fri Feb 14 2025 Jeremy Cline <jeremycline@linux.microsoft.com> - 2.69.0-1
- Update to v2.69

* Wed Jan 29 2025 Jeremy Cline <jeremycline@linux.microsoft.com> - 2.68.0-1
- Update to v2.68

* Wed Jan 29 2025 Jeremy Cline <jeremycline@linux.microsoft.com> - 2.67.0-2
- Relax portalocker dependency

* Tue Jan 28 2025 Jeremy Cline <jeremycline@linux.microsoft.com> - 2.67.0-1
- Update to v2.67.0

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.65.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Oct 28 2024 Jeremy Cline <jeremycline@linux.microsoft.com> - 2.65.0-1
- Update to v2.65

* Mon Sep 16 2024 Jeremy Cline <jeremycline@linux.microsoft.com> - 2.64.0-1
- Update to v2.64.0

* Fri Aug 16 2024 Jeremy Cline <jeremycline@linux.microsoft.com> - 2.63.0-1
- Update to v2.63.0

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.62.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jul 11 2024 Jeremy Cline <jeremycline@microsoft.com> - 2.62.0-1
- Update to v2.62.0

* Thu Jul 11 2024 Jerry James <loganjerry@gmail.com> - 2.61.0-3
- Rebuild for antlr4-project 4.13.1

* Wed Jun 19 2024 Jeremy Cline <jeremycline@linux.microsoft.com> - 2.61.0-2
- Relax azure-core dependency requirement

* Wed May 29 2024 Jeremy Cline <jeremycline@microsoft.com> - 2.61.0-1
- Update to version 2.61.0

* Tue May 07 2024 Jeremy Cline <jeremycline@microsoft.com> - 2.60.0-1
- Update to version 2.60

* Fri Apr 05 2024 Jeremy Cline <jeremycline@microsoft.com> - 2.59.0-2
- Fix fails-to-install for azure-cli-2.59

* Wed Apr 03 2024 Jeremy Cline <jeremycline@microsoft.com> - 2.59.0-1
- Update to v2.59 (rhbz #2272746)

* Wed Mar 06 2024 Jeremy Cline <jeremycline@microsoft.com> - 2.58.0-1
- Bump to v2.58

* Tue Feb 06 2024 Major Hayden <major@redhat.com> - 2.57.0-1
- Update to 2.57.0 rhbz#2263011

* Tue Feb 06 2024 Jeremy Cline <jeremy@jcline.org> - 2.56.0-2
- Recommend python3-antlr4-runtime

* Thu Feb 01 2024 Major Hayden <major@redhat.com> - 2.56.0-1
- Update to 2.56.0 rhbz#2253123

* Tue Jan 23 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.54.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.54.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Nov 14 2023 Major Hayden <major@redhat.com> - 2.54.0-1
- Update to 2.54.0 rhbz#2249655

* Wed Oct 25 2023 Major Hayden <major@redhat.com> - 2.53.1-1
- Update to 2.53.1 rhbz#2240840

* Fri Sep 29 2023 Major Hayden <major@redhat.com> - 2.53.0-1
- Update to 2.53.0

* Tue Sep 12 2023 Major Hayden <major@redhat.com> - 2.52.0-3
- Allow older psutil/argcomplete for EL9

* Tue Sep 12 2023 Major Hayden <major@redhat.com> - 2.52.0-2
- Allow older websocket-client on EL9

* Tue Sep 05 2023 Major Hayden <major@redhat.com> - 2.52.0-1
- Update to 2.52.0

* Tue Aug 01 2023 Major Hayden <major@redhat.com> - 2.51.0-1
- Update to 2.51.0

* Mon Jul 31 2023 Major Hayden <major@redhat.com> - 2.50.0-9
- Allow an older version of PyNaCl to be installed

* Thu Jul 27 2023 Major Hayden <major@redhat.com> - 2.50.0-8
- Remove unused tests

* Wed Jul 19 2023 Major Hayden <major@redhat.com> - 2.50.0-7
- Fix FTI from rhbz#2223830

* Wed Jul 19 2023 Major Hayden <major@redhat.com> - 2.50.0-6
- Allow older versions of argcomplete

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.50.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jul 14 2023 Python Maint <python-maint@redhat.com> - 2.50.0-4
- Rebuilt for Python 3.12

* Fri Jul 14 2023 Major Hayden <major@redhat.com> - 2.50.0-3
- Allow newer azure-core

* Wed Jul 12 2023 Major Hayden <major@redhat.com> - 2.50.0-2
- Add packit config 🤖

* Thu Jul 06 2023 Major Hayden <major@redhat.com> - 2.50.0-1
- Update to 2.50.0 rhbz#2219715

* Wed May 24 2023 Major Hayden <major@redhat.com> - 2.49.0-2
- Update version limits for EPEL 9

* Tue May 23 2023 Major Hayden <major@redhat.com> - 2.49.0-1
- Update to 2.49.0 rhbz#2209184

* Wed May 17 2023 Major Hayden <major@redhat.com> - 2.48.1-3
- Migrated to SPDX license

* Tue Apr 25 2023 Major Hayden <major@redhat.com> - 2.48.1-2
- Allow older cryptography/pyOpenSSL

* Tue Apr 25 2023 Major Hayden <major@redhat.com> - 2.48.1-1
- Update to 2.48.1 rhbz#2189407

* Mon Apr 17 2023 Major Hayden <major@redhat.com> - 2.47.0-4
- Last 2 commits fix FTI in rhbz#2187227

* Mon Apr 17 2023 Major Hayden <major@redhat.com> - 2.47.0-3
- Remove some version constraints

* Mon Apr 17 2023 Major Hayden <major@redhat.com> - 2.47.0-2
- Allow newer versions of semver

* Thu Apr 06 2023 Major Hayden <major@redhat.com> - 2.47.0-1
- Update to 2.47.0 rhbz#2184352

* Tue Mar 07 2023 Major Hayden <major@redhat.com> - 2.46.0-1
- Update to 2.46.0 rhbz#2176124

* Tue Feb 14 2023 Major Hayden <major@redhat.com> - 2.45.0-2
- Allow newer version of packaging

* Fri Feb 10 2023 Major Hayden <major@redhat.com> - 2.45.0-1
- Update to 2.45.0 rhbz#2167994

* Tue Jan 24 2023 Major Hayden <major@redhat.com> - 2.44.1-4
- Allow newer paramiko rhbz#2163315

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.44.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 16 2023 Major Hayden <major@redhat.com> - 2.44.1-2
- Add in the PyNaCl version adjustment for F37

* Wed Jan 11 2023 Major Hayden <major@redhat.com> - 2.44.1-1
- Update to 2.44.1 rhbz#2159907

* Wed Dec 07 2022 Major Hayden <major@redhat.com> - 2.43.0-1
- Update to 2.43.0 rhbz#2151446

* Mon Nov 14 2022 Major Hayden <major@redhat.com> - 2.42.0-2
- Remove unnecessary azure-mgmt-core version adjustment

* Tue Nov 01 2022 Major Hayden <major@redhat.com> - 2.42.0-1
- Update to 2.32.0 rhbz#2139027

* Thu Oct 27 2022 Major Hayden <major@redhat.com> - 2.41.0-2
- Fix az local dir import bug rhbz#2053193

* Fri Oct 14 2022 Major Hayden <major@redhat.com> - 2.41.0-1
- Update to 2.41.0 rhbz#2134274

* Wed Oct 05 2022 Major Hayden <major@redhat.com> - 2.40.0-2
- Add subparser patch

* Wed Sep 07 2022 Major Hayden <major@redhat.com> - 2.40.0-1
- Update to 2.40.0 rhbz#2124590

* Tue Aug 02 2022 Major Hayden <major@redhat.com> - 2.39.0-2
- Skip one more flaky test

* Tue Aug 02 2022 Major Hayden <major@redhat.com> - 2.39.0-1
- Update to 2.39.0

* Wed Jul 20 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2.38.0-4
- Exclude i686 on F37+

* Fri Jul 08 2022 Major Hayden <major@redhat.com> - 2.38.0-3
- Add modifications for epel9

* Fri Jul 08 2022 Major Hayden <major@redhat.com> - 2.38.0-2
- Fix fedora check typo

* Tue Jul 05 2022 Major Hayden <major@redhat.com> - 2.38.0-1
- Update to 2.38.0

* Mon Jun 27 2022 Major Hayden <major@redhat.com> - 2.37.0-14
- Skip other flaky serviceconnector test

* Mon Jun 27 2022 Major Hayden <major@redhat.com> - 2.37.0-13
- Skip flaky serviceconnector test

* Mon Jun 27 2022 Major Hayden <major@redhat.com> - 2.37.0-12
- Skip flaky keyvault test

* Mon Jun 27 2022 Major Hayden <major@redhat.com> - 2.37.0-11
- Disable botservice tests

* Mon Jun 27 2022 Major Hayden <major@redhat.com> - 2.37.0-10
- Spec overhaul

* Thu Jun 23 2022 Major Hayden <major@redhat.com> - 2.37.0-9
- Disable tests temporarily

* Wed Jun 22 2022 Major Hayden <major@redhat.com> - 2.37.0-8
- Relax azure-mgmt-core requirement

* Wed Jun 22 2022 Major Hayden <major@redhat.com> - 2.37.0-7
- Relax azure-core requirement

* Tue Jun 21 2022 Jerry James <loganjerry@gmail.com> - 2.37.0-6
- Rebuild for ANTLR 4.10.1

* Fri Jun 10 2022 Jerry James <loganjerry@gmail.com> - 2.37.0-5
- Generate ANTLR parsers from source

* Wed May 25 2022 Major Hayden <major@mhtx.net> - 2.37.0-4
- Relax websocket-client requirement for F35/F36

* Tue May 24 2022 Major Hayden <major@mhtx.net> - 2.37.0-3
- Really disable the command module tests

* Tue May 24 2022 Major Hayden <major@mhtx.net> - 2.37.0-2
- Skip command module tests due to missing VCR cassettes

* Tue May 24 2022 Major Hayden <major@mhtx.net> - 2.37.0-1
- 🚀 Update to 2.37.0

* Wed May 11 2022 Major Hayden <major@mhtx.net> - 2.36.0-13
- Relax pynacl requirement

* Tue May 10 2022 Major Hayden <major@mhtx.net> - 2.36.0-12
- Skip cert test -- uses sha1 hash

* Tue May 10 2022 Major Hayden <major@mhtx.net> - 2.36.0-11
- Remove conditional includes for antlr4 in epel9

* Mon May 09 2022 Major Hayden <major@mhtx.net> - 2.36.0-10
- Relax certifi + bcrypt requirements

* Mon May 09 2022 Major Hayden <major@mhtx.net> - 2.36.0-9
- Relax jmespath requirement for EPEL 9

* Tue May 03 2022 Major Hayden <major@mhtx.net> - 2.36.0-8
- Relax certifi requirement

* Tue May 03 2022 Major Hayden <major@mhtx.net> - 2.36.0-7
- Relax websocket-client requirement for f36/epel9

* Tue May 03 2022 Major Hayden <major@mhtx.net> - 2.36.0-6
- Remove antlr4 dep in epel9

* Tue May 03 2022 Major Hayden <major@mhtx.net> - 2.36.0-5
- Relax requirements further for epel9

* Tue May 03 2022 Major Hayden <major@mhtx.net> - 2.36.0-4
- 🎉 Enable full command module tests

* Mon May 02 2022 Major Hayden <major@mhtx.net> - 2.36.0-3
- Revert "Get required Python packages from setup.py files"

* Mon May 02 2022 Major Hayden <major@mhtx.net> - 2.36.0-2
- Get required Python packages from setup.py files

* Tue Apr 26 2022 Major Hayden <major@mhtx.net> - 2.36.0-1
- Update to 2.36.0

* Wed Apr 13 2022 Major Hayden <major@redhat.com> - 2.35.0-2
- Allow newer jsondiff version

* Thu Apr 07 2022 Major Hayden <major@mhtx.net> - 2.35.0-1
- 🚀 Update to 2.35.0

* Thu Mar 03 2022 Major Hayden <major@redhat.com> - 2.34.1-1
- 💙 Update to 2.34.1

* Tue Mar 01 2022 Major Hayden <major@redhat.com> - 2.34.0-1
- Update to 2.34.0

* Thu Feb 17 2022 Major Hayden <major@redhat.com> - 2.33.1-2
- Relax cffi requirement

* Mon Feb 14 2022 Major Hayden <major@redhat.com> - 2.33.1-1
- Update to 2.33.1

* Tue Feb 08 2022 Major Hayden <major@redhat.com> - 2.33.0-2
- Allow older humanfriendly:

* Tue Feb 08 2022 Major Hayden <major@redhat.com> - 2.33.0-1
- Update to 2.33.0

* Wed Jan 19 2022 Major Hayden <major@redhat.com> - 2.32.0-7
- Disable azure-cli command modules tests

* Wed Jan 19 2022 Major Hayden <major@redhat.com> - 2.32.0-6
- Allow for newer argcomplete

* Mon Jan 17 2022 Major Hayden <major@redhat.com> - 2.32.0-5
- Align tests with upstream pytest arguments

* Mon Jan 17 2022 Major Hayden <major@redhat.com> - 2.32.0-4
- Update humanfriendly version for F35

* Thu Jan 06 2022 Major Hayden <major@redhat.com> - 2.32.0-3
- Synchronize versions for Fedora 35

* Wed Jan 05 2022 Major Hayden <major@redhat.com> - 2.32.0-2
- Allow newer requests

* Tue Jan 04 2022 Major Hayden <major@redhat.com> - 2.32.0-1
- 🚀 Update to 2.32.0

* Wed Dec 15 2021 Major Hayden <major@redhat.com> - 2.31.0-2
- Disable keyvault_hsm_security_domain test

* Wed Dec 15 2021 Major Hayden <major@redhat.com> - 2.31.0-1
- Update to 2.31.0

* Fri Nov 12 2021 Major Hayden <major@redhat.com> - 2.30.0-5
- Skip test_azconfig_import_export test

* Fri Nov 12 2021 Major Hayden <major@redhat.com> - 2.30.0-4
- Lower the humanfriendly requirement

* Fri Nov 12 2021 Major Hayden <major@redhat.com> - 2.30.0-3
- Update bash completion handling

* Wed Nov 10 2021 Major Hayden <major@redhat.com> - 2.30.0-2
- Disable a few more azure-cli tests

* Tue Nov 09 2021 Major Hayden <major@redhat.com> - 2.30.0-1
- Update to 2.30.0

* Mon Nov 01 2021 Major Hayden <major@mhtx.net> - 2.29.2-4
- Disable test_keyvault_hsm_security_domain test

* Mon Nov 01 2021 Major Hayden <major@mhtx.net> - 2.29.2-3
- Allow humanfriendly>=8.2 for F35

* Fri Oct 29 2021 Major Hayden <major@mhtx.net> - 2.29.2-2
- Switch to testing style used by azdev

* Fri Oct 29 2021 Major Hayden <major@mhtx.net> - 2.29.2-1
- Update to 2.29.2

* Fri Oct 22 2021 Major Hayden <major@mhtx.net> - 2.29.1-3
- Remove debug code

* Fri Oct 22 2021 Major Hayden <major@mhtx.net> - 2.29.1-2
- Enable testing for azure-cli components

* Thu Oct 21 2021 Major Hayden <major@mhtx.net> - 2.29.1-1
- Update to 2.29.1

* Tue Oct 12 2021 Major Hayden <major@mhtx.net> - 2.29.0-2
- Allow humanfriendly 8.2 or higher

* Tue Oct 12 2021 Major Hayden <major@mhtx.net> - 2.29.0-1
- Update to 2.29.0

* Mon Oct 04 2021 Major Hayden <major@mhtx.net> - 2.28.0-4
- Allow for newer versions of humanfriendly

* Mon Sep 13 2021 Major Hayden <major@mhtx.net> - 2.28.0-3
- Switch to rpmautospec

* Mon Sep 13 2021 Major Hayden <major@mhtx.net> - 2.28.0-2
- Allow newer versions of python3-scp

* Wed Sep 08 2021 Major Hayden <major@mhtx.net> - 2.28.0-1
- Update to 2.28.0

* Mon Aug 23 2021 Major Hayden <major@mhtx.net> - 2.27.2-1
- Update to azure-cli 2.27.2

* Wed Aug 11 2021 Major Hayden <major@mhtx.net> - 2.27.1-1
- Update to 2.27.1

* Mon Aug 09 2021 Major Hayden <major@mhtx.net> - 2.27.0-1
- Update to 2.27.0

* Sat Aug 07 2021 Major Hayden <major@mhtx.net> - 2.26.1-1
- Initial import (#1986602)
## END: Generated by rpmautospec
