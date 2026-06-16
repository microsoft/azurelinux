Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global srcname joblib

Name:           python-%{srcname}
Version:        1.5.3
Release:        1%{?dist}
Summary:        Lightweight pipelining with Python functions

License:        BSD-3-Clause
URL:            https://github.com/joblib/joblib
Source0:        https://files.pythonhosted.org/packages/41/f2/d34e8b3a08a9cc79a50b2208a93dce981fe615b64d5a4d4abee421d898df/%{srcname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
BuildRequires:  pyproject-rpm-macros

%global _description %{expand:
Joblib is a set of tools to provide lightweight pipelining in Python. It
provides transparent disk caching of functions, lazy re-evaluation
(memoize pattern), and easy simple parallel computing. Joblib is optimized to
be fast and robust on large data and has specific optimizations for numpy
arrays.}

%description %_description

%package -n python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname} %_description

%prep
%autosetup -n %{srcname}-%{version}

# Azure Linux's setuptools predates PEP 639, so rewrite the SPDX string license
# into the legacy table form and drop the license-files key it cannot parse.
sed -i 's/^license = "\(.*\)"/license = {text = "\1"}/' pyproject.toml
sed -i '/^license-files/d' pyproject.toml

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{srcname}

%files -n python3-%{srcname} -f %{pyproject_files}
%license LICENSE.txt
%doc README.rst

%changelog
* Wed Jun 03 2026 Andy Zaugg <azaugg@linkedin.com> - 1.5.3-1
- Initial Azure Linux import from the source project (license: same as "License" tag).
- License verified.
