Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global srcname superbench
%global gitname superbenchmark

Name:           python-%{srcname}
Version:        0.12.0
Release:        1%{?dist}
Summary:        A validation and profiling tool for AI infrastructure

License:        MIT
URL:            https://github.com/microsoft/superbenchmark
Source0:        https://github.com/microsoft/%{gitname}/archive/refs/tags/v%{version}.tar.gz#/%{gitname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm
BuildRequires:  python3-wheel
BuildRequires:  pyproject-rpm-macros

%global _description %{expand:
SuperBench is a validation and profiling tool for AI infrastructure. It provides
a comprehensive set of micro-benchmarks and model benchmarks to evaluate the
performance and detect defects of hardware (GPU, CPU, network, etc.) at scale,
along with a distributed runner to orchestrate benchmarks across many nodes and
tooling to aggregate, analyze, and visualize the results.}

%description %_description

%package -n python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname} %_description

%prep
%autosetup -n %{gitname}-%{version}

# Drop the non-PyPI git dependency (pssh @ git+https://...) which cannot be
# resolved from the distro and is only needed for the multi-node SSH runner.
sed -i '/pssh @ git+https/d' setup.py

%generate_buildrequires
export SETUPTOOLS_SCM_PRETEND_VERSION=%{version}
%pyproject_buildrequires

%build
export SETUPTOOLS_SCM_PRETEND_VERSION=%{version}
%pyproject_wheel

%install
export SETUPTOOLS_SCM_PRETEND_VERSION=%{version}
%pyproject_install

# Upstream's find_packages(exclude=['tests']) does not exclude the tests.*
# subpackages, so an unowned top-level "tests" tree lands in site-packages.
# Drop it; only the superbench package is shipped.
rm -rf %{buildroot}%{python3_sitelib}/tests

%pyproject_save_files %{srcname}

%files -n python3-%{srcname} -f %{pyproject_files}
%license LICENSE
%doc README.md
%{_bindir}/sb

%changelog
* Wed Jun 03 2026 Andy Zaugg <azaugg@linkedin.com> - 0.12.0-1
- Original version for Azure Linux.
- License verified.
