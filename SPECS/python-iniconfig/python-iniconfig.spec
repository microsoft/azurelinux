%bcond_with tests
%global base_name iniconfig
%global _description %{expand:
iniconfig is a small and simple INI-file parser module
having a unique set of features:
 
* tested against Python2.4 across to Python3.2, Jython, PyPy
* maintains order of sections and entries
* supports multi-line values with or without line-continuations
* supports "#" comments everywhere
* raises errors with proper line-numbers
* no bells and whistles like automatic substitutions
* iniconfig raises an Error if two sections have the same name.}

Name:           python-%{base_name}
Version:        2.1.0
Release:        1%{?dist}
Summary:        Brain-dead simple parsing of ini files
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Languages/Python
URL:            https://github.com/pytest-dev/%{base_name}
Source0:        https://files.pythonhosted.org/packages/23/a2/97899f6bd0e873fed3a7e67ae8d3a08b21799430fb4da15cfedf10d6e2c2/%{base_name}-%{version}.tar.gz
# XXX: When a version of 'pyproject-rpm-macros' is released for Azure Linux
# that incorporates the 'pypi_source' macro, we should uncomment the following
# line and use that macro instead of spelling out the source URI.
# Source0:        %%{pypi_source iniconfig}
BuildArch:      noarch

# BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm
BuildRequires:  python3-hatch-vcs
BuildRequires:  python3-hatchling
BuildRequires:  python3-wheel

# pytest 6+ needs this and this uses pytest for tests
%if %{with tests}
# There's a "circular" dependency between 'pytest' and this package.  'pytest'
# depends on this package at runtime, and this package depends on 'pytest' to
# run tests.  It's not a *strictly* circular dependency - you could imagine
# building this package, running the "%install" stage, installing this package
# in a chroot, installing 'pytest' in the chroot, and running the "%check"
# stage thereafter.  Unfortunately, it's not currently possible to define these
# specific dependency relationships in RPM spec files.
#
# XXX: What we really want here is something like 'BuildRequires(check)', but
# that can't be specified in RPM specs.  If a tag like that is ever implemented
# in spec files, then this issue:
#
#     https://github.com/rpm-software-management/rpm/issues/2631
#
# ... will likely be updated with details.
BuildRequires:  python3-pytest
%endif

%description %_description


%package -n python3-%{base_name}
Summary:        %{summary}
%description -n python3-%{base_name} %_description


%prep
%autosetup -n %{base_name}-%{version}

%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files %{base_name}


%if %{with tests}
%check
%pytest -v
%endif


%files -n python3-%{base_name} -f %{pyproject_files}
%doc README.rst
%license %{python3_sitelib}/iniconfig-%{version}.dist-info/licenses/LICENSE


%changelog
* Wed Apr 16 2025 Riken Maharjan <rmaharjan@microsoft.com> - 2.1.0-1
- Upgrade to 2.1.0

* Mon Oct 07 2024 Devin Anderson <danderson@microsoft.com> - 1.1.1-17
- Initial Azure Linux import from Fedora 40 (license: MIT).
- License verified.
- Use explicit name macro to reduce potential of naming errors.
- Add explicit build dependencies on 'python3-setuptools',
  'python3-setuptools_scm', and 'python3-wheel'.
