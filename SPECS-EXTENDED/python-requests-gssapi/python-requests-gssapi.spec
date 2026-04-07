%bcond_with tests

%global sname requests-gssapi
%global s_name requests_gssapi

Name:           python-%{sname}
Version:        1.4.0
Release:        1%{?dist}
Summary:        A GSSAPI/SPNEGO authentication handler for python-requests
Vendor:         Microsoft Corporation
Distribution:   Azure Linux

# SPDX
License:        ISC
URL:            https://github.com/pythongssapi/%{sname}
Source0:        https://github.com/pythongssapi/%{sname}/archive/v%{version}/%{sname}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-pip  
BuildRequires:  python3-wheel
BuildRequires:  python3-gssapi
BuildRequires:  python3-decorator
BuildRequires:  python3-requests
BuildRequires:  pyproject-rpm-macros
BuildRequires:  git-core
%if %{with tests}
BuildRequires:  python3dist(pytest)
%endif

%generate_buildrequires
%if %{with tests}
%pyproject_buildrequires -t
%else
%pyproject_buildrequires
%endif

%global _description %{expand:
Requests is an HTTP library, written in Python, for human beings. This
library adds optional GSSAPI authentication support and supports
mutual authentication. It includes a fully backward-compatible shim
for requests-kerberos.
}

%description %{_description}

%package -n python3-%{sname}
Summary:        %{summary}
Requires:       python3-gssapi
Requires:       python3-requests

%description -n python3-%{sname} %{_description}

%prep
%autosetup -S git_am -n %{sname}-%{version}
# Fix pyproject.toml license field: PEP 639 bare SPDX string fails older setuptools schema validation
# (JSON Schema oneOf vacuously matches both {file} and {text} sub-schemas for a plain string)
sed -i 's/^license = "ISC"/license = {text = "ISC"}/' pyproject.toml

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{s_name}

%check
%pyproject_check_import
%if %{with tests}
%pytest
%endif

%files -n python3-%{sname} -f %{pyproject_files}
%doc README.rst AUTHORS HISTORY.rst
%license LICENSE

%changelog
* Sat Apr 4 2026 Akarsh Chaudhary <v-akarshc@microsoft.com> - 1.4.0-1
- Initial CBL-Mariner import from Fedora 45 (license: ISC).
- License verified
