Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global srcname jsonlines

Name:           python-%{srcname}
Version:        4.0.0
Release:        1%{?dist}
Summary:        Library with helpers for the jsonlines file format

License:        BSD-3-Clause
URL:            https://github.com/wbolster/jsonlines
Source0:        https://github.com/wbolster/%{srcname}/archive/refs/tags/%{version}.tar.gz#/%{srcname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
BuildRequires:  pyproject-rpm-macros

%global _description %{expand:
jsonlines is a Python library with helpers for reading and writing files in the
jsonlines (newline-delimited JSON) format, where each line is a separate JSON
value. It provides convenient Reader and Writer classes that transparently
handle encoding, decoding, type checking, and error reporting for streaming
JSON records.}

%description %_description

%package -n python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname} %_description

%prep
%autosetup -n %{srcname}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{srcname}

%files -n python3-%{srcname} -f %{pyproject_files}
%license LICENSE.rst
%doc README.rst

%changelog
* Wed Jun 03 2026 Andy Zaugg <azaugg@linkedin.com> - 4.0.0-1
- Initial Azure Linux import from the source project (license: same as "License" tag).
- License verified.
