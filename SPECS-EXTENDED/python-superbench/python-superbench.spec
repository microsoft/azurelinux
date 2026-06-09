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
Requires:       python3-knack
Requires:       python3-argcomplete
Requires:       python3-omegaconf
Requires:       python3-importlib-metadata
Requires:       python3-colorlog
Requires:       python3-networkx
Requires:       python3-jsonlines
Requires:       python3-jinja2
Requires:       python3-joblib
Requires:       python3-markdown
Requires:       python3-matplotlib
Requires:       python3-natsort
Requires:       python3-numpy
Requires:       python3-openpyxl
Requires:       python3-packaging
Requires:       python3-pandas
Requires:       python3-protobuf
Requires:       python3-pyyaml
Requires:       python3-requests
Requires:       python3-seaborn
Requires:       python3-tcping
Requires:       python3-types-requests
Requires:       python3-urllib3
Requires:       python3-xlrd
Requires:       python3-xlsxwriter
Requires:       python3-xmltodict

%description -n python3-%{srcname} %_description

%prep
%autosetup -n %{gitname}-%{version}

# Drop the remote/multi-node runner dependencies. The Ansible-based runner
# (superbench/runner) and the pssh-based topology-aware traffic helper are only
# used to orchestrate benchmarks across remote nodes; this package targets
# local execution, so these are removed to avoid pulling Ansible and an
# unresolvable git dependency.
sed -i '/pssh @ git+https/d' setup.py
sed -i '/ansible/d' setup.py

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
