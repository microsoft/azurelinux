%global _description %{expand:
A backwards/forwards-compatible fork of distutils.version.LooseVersion, for
times when PEP-440 isnt what you need.

The goal of this package is to be a drop-in replacement for the original
LooseVersion. It implements an identical interface and comparison logic to
LooseVersion. The only major change is that a looseversion.LooseVersion is
comparable to a distutils.version.LooseVersion, which means tools should not
need to worry whether all dependencies that use LooseVersion have migrated.

If you are simply comparing versions of Python packages, consider moving to
packaging.version.Version, which follows PEP-440. LooseVersion is better suited
to interacting with heterogeneous version schemes that do not follow PEP-440.}

Name:           python-looseversion
Version:        1.3.0
Release:        1%{?dist}
Summary:        Version numbering for anarchists and software realists

Vendor:         Microsoft Corporation
Distribution:   Azure Linux

License:        PSF-2.0
URL:            https://pypi.org/pypi/looseversion
Source0:        https://github.com/effigies/looseversion/archive/refs/tags/%{version}.tar.gz#/python-looseversion-%{version}.tar.gz

BuildArch:      noarch

%description %_description
%package -n python3-looseversion
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  python3-pytest

BuildRequires:  python-rpm-macros
BuildRequires:  python3-hatchling
BuildRequires:  python3-packaging
BuildRequires:  python3-pathspec
BuildRequires:  python3-pip
BuildRequires:  python3-trove-classifiers

%description -n python3-looseversion %_description

%prep
%autosetup -n looseversion-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files looseversion
# Removing unpackaged license file - we add it through the %%license macro.
find %{buildroot}%{python3_sitelib} -name LICENSE -delete

%check
pip3 install iniconfig
%pytest -v tests.py

%files -n python3-looseversion -f %{pyproject_files}
%license LICENSE
%doc README.md CHANGES.md

%changelog
* Mon Mar 11 2024 corvus-callidus <> - 1.3.0-1
- Initial import from Fedora 39 for Azure Linux
- License verified
