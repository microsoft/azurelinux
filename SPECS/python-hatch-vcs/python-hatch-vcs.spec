Vendor:         Microsoft Corporation
Distribution:   Azure Linux

%undefine distro_module_ldflags

# Let’s try to build this as early as we can, since it’s a dependency for
# some important libraries, such as python-platformdirs.
%bcond bootstrap 0
%bcond tests %{without bootstrap}

Name:           python-hatch-vcs
Version:        0.4.0
Release:        4%{?dist}
Summary:        Hatch plugin for versioning with your preferred VCS

# SPDX
License:        MIT
URL:            https://github.com/ofek/hatch-vcs
Source:         %{pypi_source hatch_vcs}

BuildArch:      noarch

BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-six
BuildRequires:  python3-wheel
BuildRequires:  python3-hatchling
BuildRequires:  python3-pathspec
BuildRequires:  python3-packaging
BuildRequires:  python3-trove-classifiers

%if %{with tests}
BuildRequires:  python3dist(pytest)
BuildRequires:  git-core
BuildRequires:  python3-setuptools_scm
%endif

%global common_description %{expand:
This provides a plugin for Hatch that uses your preferred version control
system (like Git) to determine project versions.}

%description %{common_description}


%package -n python3-hatch-vcs
Summary:        %{summary}

%description -n python3-hatch-vcs %{common_description}


%prep
%autosetup -n hatch_vcs-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files hatch_vcs


%check
%if %{with tests}
pip3 install iniconfig
%pytest
%else
%pyproject_check_import
%endif


%files -n python3-hatch-vcs -f %{pyproject_files}
%license %{python3_sitearch}/hatch_vcs-%{version}.dist-info/licenses/LICENSE.txt
%doc HISTORY.md
%doc README.md


%changelog
* Tue Mar 12 2024 corvus-callidus <108946721+corvus-callidus@users.noreply.github.com> - 0.4.0-4
- Improve check section and dependencies

* Fri Mar 01 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.4.0-3
- Updating naming for 3.0 version of Azure Linux.

* Mon Feb 26 2024 Bala <balakumaran.kannan@microsoft.com> - 0.4.0-2
- Initial CBL-Mariner import from Fedora 39 (license: MIT)
- License verified.

* Mon Nov 06 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 0.4.0-1
- Update to 0.4.0 (close RHBZ#2248106)

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jul 07 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 0.3.0-6
- Use new (rpm 4.17.1+) bcond style

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 0.3.0-5
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Dec 20 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 0.3.0-2
- Work with setuptools_scm 7.1

* Sat Dec 10 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 0.3.0-1
- Update to 0.3.0 (close RHBZ#2152320)
- We can now rely on pyproject-rpm-macros >= 1.2.0
- The LICENSE.txt file is now handled in pyproject_files
- The setuptools_scm 7 patch is now merged upstream

* Sat Oct 22 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 0.2.0-10
- Confirm License is SPDX MIT

* Sun Sep 11 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 0.2.0-9
- Use hatchling’s new “prepare_metadata_…” hook support for BR’s

* Thu Jul 21 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 0.2.0-8
- Updated setuptools_scm 7 patch again

* Thu Jul 07 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 0.2.0-7
- Fix extra newline in description

* Thu Jun 30 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 0.2.0-6
- Updated setuptools_scm 7 patch

* Thu Jun 30 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 0.2.0-5
- Fix test compatibility with setuptools_scm 7

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.2.0-4
- Rebuilt for Python 3.11

* Fri May 06 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 0.2.0-3
- Use wheel-building support to generate BR’s

* Sun May 01 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 0.2.0-2
- Adjust for pyproject-rpm-macros >= 1.1.0

* Fri Apr 22 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 0.2.0-1
- Initial package (close RHBZ#2077832)
