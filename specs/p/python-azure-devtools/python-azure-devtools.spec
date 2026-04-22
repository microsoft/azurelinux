# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# The last versioned release of the devtools code is 1.2.1, but upstream
# continues to update it without bumping the version. 😞
%global         srcname         azure-devtools
%global         commit          67d46b9c4292c267c14833b50bb313c077e63cd5
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})
%global         short_version   1.2.1

Name:           python-%{srcname}
Version:        %{short_version}~git.4.%{shortcommit}
Release: 16%{?dist}
Summary:        Microsoft Azure Development Tools for SDK
License:        MIT and Apache-2.0
URL:            https://github.com/Azure/azure-sdk-for-python/
# The azure-sdk-for-python repository is huge at > 160MB, but we only need ~
# 100KB of source for this package. Use this script to generate a tarball of the
# source code:
# ./generate-devtools-tarball.sh COMMIT_SHA
Source0:        azure-devtools-%{commit}.tar.gz
# Asked upstream to update the vcrpy requirement. PR in progress.
# https://github.com/Azure/azure-sdk-for-python/pull/20032
Patch0:         python-azure-devtools-requirements-fix.patch

BuildArch:      noarch

BuildRequires:  python3-devel

%global _description %{expand:
Development tools for Python-based Azure tools
This package contains tools to aid in developing Python-based Azure code.}

%description %{_description}


%package -n python3-%{srcname}
Summary:        %{summary}

%description -n python3-%{srcname} %{_description}


%prep
%autosetup -v -p3 -c -n %{srcname}-%{commit}


%build
%pyproject_wheel


%generate_buildrequires
%pyproject_buildrequires -r


%install
%pyproject_install
%pyproject_save_files azure_devtools

# Some provided executables are only used internally in Azure SDK's CI.
rm -f %{buildroot}%{_bindir}/{perfstress,perfstressdebug,systemperf}


%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.rst
%license LICENSE


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.2.1~git.4.67d46b9-15
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.2.1~git.4.67d46b9-14
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1~git.4.67d46b9-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jun 06 2025 Python Maint <python-maint@redhat.com> - 1.2.1~git.4.67d46b9-12
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1~git.4.67d46b9-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1~git.4.67d46b9-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Jun 09 2024 Python Maint <python-maint@redhat.com> - 1.2.1~git.4.67d46b9-9
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1~git.4.67d46b9-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1~git.4.67d46b9-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1~git.4.67d46b9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jul 01 2023 Python Maint <python-maint@redhat.com> - 1.2.1~git.4.67d46b9-5
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1~git.4.67d46b9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1~git.4.67d46b9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.2.1~git.4.67d46b9-2
- Rebuilt for Python 3.11

* Tue May 24 2022 Major Hayden <major@mhtx.net> - 1.2.1~git.4.67d46b9-1
- Update to latest commit 67d46b9c4292c267c14833b50bb313c077e63cd5.

* Mon Apr 25 2022 Major Hayden <major@mhtx.net> - 1.2.1~git.3.a5a4ef4-5
- Updating dependencies.

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1~git.3.a5a4ef4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Sep 08 2021 Major Hayden <major@mhtx.net> - 1.2.1~git.3.a5a4ef4-3
- Move obsoletes into subpackage

* Wed Sep 08 2021 Major Hayden <major@mhtx.net> - 1.2.1~git.3.a5a4ef4-2
- Move obsoletes into subpackage

* Tue Aug 03 2021 Major Hayden <major@mhtx.net> - 1.2.1~git.3.a5a4ef4
- Updated to latest commit on 2021-08-11
- Generate a source tarball using a script to shrink size of source RPM

* Tue Aug 03 2021 Major Hayden <major@mhtx.net> - 1.2.1~git.2.19487ff
- Updated to latest commit on 2021-08-03

* Tue Jun 01 2021 Major Hayden <major@mhtx.net> - 1.2.1~git.1.a88809f
- Unretired package.
