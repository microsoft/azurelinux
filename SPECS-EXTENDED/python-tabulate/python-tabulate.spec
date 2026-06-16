Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global srcname tabulate
%global gitname python-tabulate

Name:           python-%{srcname}
Version:        0.10.0
Release:        1%{?dist}
Summary:        Pretty-print tabular data

License:        MIT
URL:            https://github.com/astanin/python-tabulate
Source0:        https://github.com/astanin/%{gitname}/archive/refs/tags/v%{version}.tar.gz#/%{gitname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm
BuildRequires:  python3-wheel
BuildRequires:  pyproject-rpm-macros

%global _description %{expand:
Tabulate is a library and command-line utility to pretty-print tabular data in
Python. It supports many output formats (plain, simple, grid, GitHub-flavored
Markdown, reStructuredText, HTML, LaTeX, and more), numeric/text alignment,
floating-point formatting, and rendering of common Python data structures such
as lists of lists, dictionaries, and NumPy arrays.}

%description %_description

%package -n python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname} %_description

%prep
%autosetup -n %{gitname}-%{version}

# Azure Linux's setuptools predates PEP 639, so the SPDX string form of the
# license metadata fails validation. Rewrite `license = "MIT"` into the legacy
# table form and drop the `license-files` key the older validator rejects; the
# LICENSE file is still shipped via the %%license entry below.
sed -i 's/^license = "MIT"/license = {text = "MIT"}/' pyproject.toml
sed -i '/^license-files = /d' pyproject.toml

%generate_buildrequires
export SETUPTOOLS_SCM_PRETEND_VERSION=%{version}
%pyproject_buildrequires

%build
export SETUPTOOLS_SCM_PRETEND_VERSION=%{version}
%pyproject_wheel

%install
export SETUPTOOLS_SCM_PRETEND_VERSION=%{version}
%pyproject_install
%pyproject_save_files %{srcname}

%files -n python3-%{srcname} -f %{pyproject_files}
%license LICENSE
%doc README.md
%{_bindir}/tabulate

%changelog
* Wed Jun 03 2026 Andy Zaugg <azaugg@linkedin.com> - 0.10.0-1
- Initial Azure Linux import from the source project (license: same as "License" tag).
- License verified.
