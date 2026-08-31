# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# The SDK tools have never had a versioned release, but they are updated
# frequently in the upstream repository.
%global         srcname         azure-sdk-tools
%global         commit          67d46b9c4292c267c14833b50bb313c077e63cd5
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})
%global         short_version   0.0.0

Name:           python-%{srcname}
Version:        %{short_version}~git.4.%{shortcommit}
Release:        16%{?dist}
Summary:        Specific tools for Azure SDK for Python testing
License:        MIT and Apache-2.0
URL:            https://github.com/Azure/azure-sdk-for-python/
# The azure-sdk-for-python repository is huge at > 160MB, but we only need ~
# 100KB of source for this package. Use this script to generate a tarball of the
# source code:
# ./generate-devtools-tarball.sh COMMIT_SHA
Source0:        azure-sdk-tools-%{commit}.tar.gz

BuildArch:      noarch


BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
BuildRequires:  pyproject-rpm-macros


%global _description %{expand:
Specific tools for Azure SDK for Python testing}

%description %{_description}


%package -n python3-%{srcname}
Summary:        %{summary}
Obsoletes:      python3-azure-sdk < 5.0.1
Provides:       python3dist(%{srcname}) == %{version}-%{release}
%description -n python3-%{srcname} %{_description}


%prep
%autosetup -p3 -c -n %{srcname}-%{commit}


%build
# Some tools are only used for the Azure SDK CI system and there's no need
# to package those.
rm -rf packaging_tools pypi_tools

# There's a dangling empty setup.py in the devtools_testutils directory.
rm -f devtools_testutils/setup.py

%pyproject_wheel


%install
%pyproject_install

# BZ 2048083: The package metadata causes a provides for version 0.0.0.
rm -rf %{buildroot}%{python3_sitelib}/azure_sdk_tools-0.0.0.dist-info

# Some provided executables are only used internally in Azure SDK's CI.
rm -f %{buildroot}/%{_bindir}/{auto_codegen,auto_package,generate_package,generate_sdk,sdk_generator,sdk_package}


%files -n python3-%{srcname}
%doc changelog_generics.md
%license LICENSE
%{python3_sitelib}/devtools_testutils
%{python3_sitelib}/testutils

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.0.0~git.4.67d46b9-16
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.0.0~git.4.67d46b9-15
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.0~git.4.67d46b9-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 0.0.0~git.4.67d46b9-13
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.0~git.4.67d46b9-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.0~git.4.67d46b9-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.0.0~git.4.67d46b9-10
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.0~git.4.67d46b9-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.0~git.4.67d46b9-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.0~git.4.67d46b9-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 0.0.0~git.4.67d46b9-6
- Rebuilt for Python 3.12

* Mon May 08 2023 Major Hayden <major@redhat.com> - 0.0.0~git.4.67d46b9-5
- Migrated to SPDX license

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.0~git.4.67d46b9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.0~git.4.67d46b9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.0.0~git.4.67d46b9-2
- Rebuilt for Python 3.11

* Tue May 24 2022 Major Hayden <major@mhtx.net> - 0.0.0~git.4.67d46b9-1
- Update to latest commit 67d46b9c4292c267c14833b50bb313c077e63cd5.

* Wed Apr 27 2022 Major Hayden <major@mhtx.net> - 0.0.0~git.3.6aabfa3-2
- Add provides for azure-sdk-tools.

* Tue Mar 01 2022 Major Hayden <major@mhtx.net> - 0.0.0~git.3.6aabfa3-1
- Update to 6aabfa36aab12fcdf5263281ccfed7e383c62663 (most recent tag on 2022-03-01)

* Fri Feb 04 2022 Major Hayden <major@mhtx.net> - 0.0.0~git.2.a5a4ef4-4
- Fixing bogus provides from BZ 2048083.

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.0~git.2.a5a4ef4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Sep 08 2021 Major Hayden <major@mhtx.net> - 0.0.0~git.2.a5a4ef4-2
- Move obsoletes into subpackage

* Wed Aug 11 2021 Major Hayden <major@mhtx.net> - 0.0.0~git.2.a5a4ef4
- Update to latest git checkout from 2021-08-11
- Reduce SRPM file size

* Tue Jun 01 2021 Major Hayden <major@mhtx.net> - 0.0.0~git.1.9d4f5a6
- First package.
