%bcond_with testcoverage

# Only generate buildrequires or use PEP 518 style building on Fedora and new EPEL releases because
# Poetry is missing elsewhere. Fall back to using setuptools instead.
%if ((! 0%{?azl}) && (! 0%{?rhel} || 0%{?epel} >= 10))
%bcond_without genbrs
%bcond_without pyproject_build
%else
%bcond_with genbrs
%bcond_with pyproject_build
%endif

%if 0%{undefined pyproject_files}
%global pyproject_files %{_builddir}/%{name}-%{version}-%{release}.%{_arch}-pyproject-files
%endif

%global srcname rpmautospec_core
%global canonicalname rpmautospec-core

Name: python-%{canonicalname}
Version: 0.1.5
Release: 1%{?dist}
Vendor:  Microsoft Corporation
Distribution: Azure Linux
Summary: Minimum functionality for rpmautospec

License: MIT
URL: https://github.com/fedora-infra/%{canonicalname}
Source0: %{url}/releases/download/%{version}/rpmautospec_core-%{version}.tar.gz#/%{canonicalname}-%{version}.tar.gz
BuildArch: noarch
BuildRequires: python3-devel >= 3.6.0
# The dependencies needed for testing donâ€™t get auto-generated.
BuildRequires: python3dist(pytest)
%if %{with testcoverage}
BuildRequires: python3dist(pytest-cov)
%endif
BuildRequires: sed

%if %{with genbrs}
%generate_buildrequires
%{pyproject_buildrequires}
%else
BuildRequires: python3dist(pip)
BuildRequires: python3dist(setuptools)
%endif

%global _description %{expand:
This package contains minimum functionality to determine if an RPM spec file
uses rpmautospec features.}

%description %_description

%package -n python3-%{canonicalname}
Summary: %{summary}
%if %{without pyproject_build}
%py_provides python3-%{canonicalname}
%endif

%description -n python3-%{canonicalname} %_description

%prep
%autosetup -n %{srcname}-%{version}

%if %{without testcoverage}
cat << PYTESTINI > pytest.ini
[pytest]
addopts =
PYTESTINI
%endif

%build
%if %{with pyproject_build}
%pyproject_wheel
%else
%py3_build
%endif

%install
%if %{with pyproject_build}
%pyproject_install
%pyproject_save_files %{srcname}
# Work around poetry not listing license files as such in package metadata.
sed -i -e 's|^\(.*/LICENSE\)|%%license \1|g' %{pyproject_files}
%else
%py3_install
echo '%{python3_sitelib}/%{srcname}*' > %{pyproject_files}
%endif

%check
%pytest

%files -n python3-%{canonicalname} -f %{pyproject_files}
%doc README.md
%if %{without pyproject_build}
%license LICENSE
%endif

%changelog
* Wed Aug 28 2028 Reuben Olinsky <reubeno@microsoft.com> - 0.1.5-1
- Initial Azure Linux import from Fedora 41 (license: MIT)
- License verified
