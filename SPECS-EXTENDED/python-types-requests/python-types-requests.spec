Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global srcname types-requests
%global tarname types_requests

Name:           python-%{srcname}
Version:        2.33.0.20260518
Release:        1%{?dist}
Summary:        Typing stubs for requests

License:        Apache-2.0
URL:            https://github.com/python/typeshed
Source0:        https://files.pythonhosted.org/packages/e0/01/c5a19253fe1ac159159ddf9a3a07cec8bb5e486ec4d9002ad2821da0e5d2/%{tarname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
BuildRequires:  pyproject-rpm-macros

%global _description %{expand:
This package provides external type annotations (PEP 561 stubs) for the
requests HTTP library, taken from the typeshed project. It contains no runtime
code; it exists so that static type checkers such as mypy and pyright can check
code that uses requests.}

%description %_description

%package -n python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname} %_description

%prep
%autosetup -n %{tarname}-%{version}

# Azure Linux's setuptools predates PEP 639, so rewrite the SPDX string license
# into the legacy table form and drop the license-files key it cannot parse.
sed -i 's/^license = "\(.*\)"/license = {text = "\1"}/' pyproject.toml
sed -i '/^license-files/d' pyproject.toml
# setuptools 69 only allows a valid module name or '*' as a package-data key;
# the stub package's hyphenated 'requests-stubs' key is rejected. There is a
# single package here, so apply its data globs to the '*' wildcard instead.
sed -i "s/^'requests-stubs' =/'*' =/" pyproject.toml

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files '*'

%files -n python3-%{srcname} -f %{pyproject_files}
%license LICENSE
%doc README.md

%changelog
* Wed Jun 03 2026 Andy Zaugg <azaugg@linkedin.com> - 2.33.0.20260518-1
- Initial Azure Linux import from the source project (license: same as "License" tag).
- License verified.
