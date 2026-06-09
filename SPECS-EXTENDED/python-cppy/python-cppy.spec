Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global srcname cppy

Name:           python-%{srcname}
Version:        1.3.1
Release:        1%{?dist}
Summary:        C++ headers for C extension development

License:        BSD-3-Clause
URL:            https://github.com/nucleic/cppy
Source0:        https://files.pythonhosted.org/packages/45/ed/b35645a1b285bce356f30cc0fe77a042375c385660ccd61e0cdc4c1f7c44/%{srcname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm
BuildRequires:  python3-wheel
BuildRequires:  pyproject-rpm-macros

%global _description %{expand:
cppy provides a set of C++ header files that make it easier to write Python C
extension modules. The headers provide thin wrappers around the CPython C API
to ease reference counting and error handling. It is a build-time dependency of
projects such as kiwisolver.}

%description %_description

%package -n python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname} %_description

%prep
%autosetup -n %{srcname}-%{version}

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
%doc README.rst

%changelog
* Wed Jun 03 2026 Andy Zaugg <azaugg@linkedin.com> - 1.3.1-1
- Initial Azure Linux import from the source project (license: same as "License" tag).
- License verified.
