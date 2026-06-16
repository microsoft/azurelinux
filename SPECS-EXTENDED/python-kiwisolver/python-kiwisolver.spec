Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global srcname kiwisolver

Name:           python-%{srcname}
Version:        1.5.0
Release:        1%{?dist}
Summary:        Fast implementation of the Cassowary constraint solver

License:        BSD-3-Clause
URL:            https://github.com/nucleic/kiwi
Source0:        https://files.pythonhosted.org/packages/d0/67/9c61eccb13f0bdca9307614e782fec49ffdde0f7a2314935d489fa93cd9c/%{srcname}-%{version}.tar.gz

# Compiled (C++) package. %%pyproject_buildrequires pulls the cppy and
# setuptools_scm build requirements; the C/C++ toolchain is required too.
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm
BuildRequires:  python3-cppy

%global _description %{expand:
Kiwi is an efficient C++ implementation of the Cassowary constraint solving
algorithm, exposed to Python as the kiwisolver module. It is used by matplotlib
for constraint-based layout.}

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
%doc README.md

%changelog
* Wed Jun 03 2026 Andy Zaugg <azaugg@linkedin.com> - 1.5.0-1
- Initial Azure Linux import from the source project (license: same as "License" tag).
- License verified.
