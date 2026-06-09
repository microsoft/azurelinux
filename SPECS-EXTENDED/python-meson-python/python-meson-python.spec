Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global srcname mesonpy
%global tarname meson_python

Name:           python-meson-python
Version:        0.19.0
Release:        1%{?dist}
Summary:        Meson PEP 517 build backend

License:        MIT
URL:            https://github.com/mesonbuild/meson-python
Source0:        https://files.pythonhosted.org/packages/32/98/7fe5d1bf741c03c6eea04b6245737dbd79657d4f9200e82fcbb4cc12637b/%{tarname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
BuildRequires:  pyproject-rpm-macros
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  python3-packaging
BuildRequires:  python3-pyproject-metadata

%global _description %{expand:
meson-python is a Python PEP 517 build backend that uses the Meson build
system. It enables Python packages with compiled extensions built by Meson to
be built into wheels and installed by pip, and is used by projects such as
matplotlib, contourpy, SciPy, and NumPy.}

%description %_description

%package -n python3-meson-python
Summary:        %{summary}
%{?python_provide:%python_provide python3-meson-python}
Requires:       meson
Requires:       ninja-build
Requires:       python3-packaging
Requires:       python3-pyproject-metadata

%description -n python3-meson-python %_description

%prep
%autosetup -n %{tarname}-%{version}

# Azure Linux's pyproject-metadata predates PEP 639, so rewrite the SPDX string
# license into the legacy table form and drop the license-files key it cannot
# parse (the source uses single-quoted TOML strings).
sed -i "s/^license = '\(.*\)'/license = {text = \"\1\"}/" pyproject.toml
sed -i '/^license-files/d' pyproject.toml

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{srcname}

%files -n python3-meson-python -f %{pyproject_files}
%license LICENSE
%doc README.rst

%changelog
* Wed Jun 03 2026 Andy Zaugg <azaugg@linkedin.com> - 0.19.0-1
- Initial Azure Linux import from the source project (license: same as "License" tag).
- License verified.
