Summary:        RPM macros for PEP 517 Python packages
Name:           pyproject-rpm-macros

%bcond tests 0
# pytest-xdist and tox are not desired in RHEL
#%%bcond pytest_xdist %%{undefined rhel}
#%%bcond tox_tests %%{undefined rhel}

# The idea is to follow the spirit of semver
# Given version X.Y.Z:
#   Increment X and reset Y.Z when there is a *major* incompatibility
#   Increment Y and reset Z when new macros or features are added
#   Increment Z when this is a bugfix or a cosmetic change
# Dropping support for EOL Fedoras is *not* considered a breaking change
Version:        1.12.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://src.fedoraproject.org/rpms/pyproject-rpm-macros

BuildArch:      noarch

# Macro files
Source001:      macros.pyproject
Source002:      macros.aaa-pyproject-srpm

# Implementation files
Source101:      pyproject_buildrequires.py
Source102:      pyproject_save_files.py
Source103:      pyproject_convert.py
Source104:      pyproject_preprocess_record.py
Source105:      pyproject_construct_toxenv.py
Source106:      pyproject_requirements_txt.py
Source107:      pyproject_wheel.py

# Tests
Source201:      test_pyproject_buildrequires.py
Source202:      test_pyproject_save_files.py
Source203:      test_pyproject_requirements_txt.py
Source204:      compare_mandata.py

# Test data
Source301:      pyproject_buildrequires_testcases.yaml
Source302:      pyproject_save_files_test_data.yaml
Source303:      test_RECORD

# Metadata
Source901:      README.md
Source902:      LICENSE

%if %{with tests}
BuildRequires:  python3dist(pytest)
%if %{with pytest_xdist}
BuildRequires:  python3dist(pytest-xdist)
%endif
BuildRequires:  python3dist(pyyaml)
#BuildRequires:  python3dist(packaging)
BuildRequires:  python-packaging
BuildRequires:  python3dist(pip)
BuildRequires:  python3dist(setuptools)
%if %{with tox_tests}
BuildRequires:  python3dist(tox-current-env) >= 0.0.6
%endif
BuildRequires:  python3dist(wheel)
#BuildRequires:  (python3dist(tomli) if python3 < 3.11)
%endif

# We build on top of those:
BuildRequires:  python-rpm-macros
BuildRequires:  python-srpm-macros
BuildRequires:  python3-rpm-macros
Requires:       python-rpm-macros
Requires:       python-srpm-macros
Requires:       python3-rpm-macros
#Requires:       (pyproject-srpm-macros = %{?epoch:%{epoch}:}%{version}-%{release} if pyproject-srpm-macros)
Requires:       pyproject-srpm-macros

# We use the following tools outside of coreutils
Requires:       findutils
Requires:       sed

# This package requires the %%generate_buildrequires functionality.
# It has been introduced in RPM 4.15 (4.14.90 is the alpha of 4.15).
# What we need is rpmlib(DynamicBuildRequires), but that is impossible to (Build)Require.
Requires:       rpm-build >= 4.14.90
BuildRequires:  rpm-build >= 4.14.90

%description
These macros allow projects that follow the Python packaging specifications
to be packaged as RPMs.

They work for:

* traditional Setuptools-based projects that use the setup.py file,
* newer Setuptools-based projects that have a setup.cfg file,
* general Python projects that use the PEP 517 pyproject.toml file
  (which allows using any build system, such as setuptools, flit or poetry).

These macros replace %%py3_build and %%py3_install,
which only work with setup.py.


%package -n pyproject-srpm-macros
Summary:        Minimal implementation of %%pyproject_buildrequires
Requires:       pyproject-rpm-macros = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       rpm-build >= 4.14.90

%description -n pyproject-srpm-macros
This package contains a minimal implementation of %%pyproject_buildrequires.
When used in %%generate_buildrequires, it will generate BuildRequires
for pyproject-rpm-macros. When both packages are installed, the full version
takes precedence.


%prep
# Not strictly necessary but allows working on file names instead
# of source numbers in install section
%setup -c -T
cp -p %{sources} .

%generate_buildrequires
# nothing to do, this is here just to assert we have that functionality

%build
# nothing to do, sources are not buildable

%install
mkdir -p %{buildroot}%{_rpmmacrodir}
mkdir -p %{buildroot}%{_rpmconfigdir}/mariner
install -pm 644 macros.pyproject %{buildroot}%{_rpmmacrodir}/
install -pm 644 macros.aaa-pyproject-srpm %{buildroot}%{_rpmmacrodir}/
install -pm 644 pyproject_buildrequires.py %{buildroot}%{_rpmconfigdir}/mariner/
install -pm 644 pyproject_convert.py %{buildroot}%{_rpmconfigdir}/mariner/
install -pm 644 pyproject_save_files.py  %{buildroot}%{_rpmconfigdir}/mariner/
install -pm 644 pyproject_preprocess_record.py %{buildroot}%{_rpmconfigdir}/mariner/
install -pm 644 pyproject_construct_toxenv.py %{buildroot}%{_rpmconfigdir}/mariner/
install -pm 644 pyproject_requirements_txt.py %{buildroot}%{_rpmconfigdir}/mariner/
install -pm 644 pyproject_wheel.py %{buildroot}%{_rpmconfigdir}/mariner/

%check
# assert the two signatures of %%pyproject_buildrequires match exactly
signature1="$(grep '^%%pyproject_buildrequires' macros.pyproject | cut -d' ' -f1)"
signature2="$(grep '^%%pyproject_buildrequires' macros.aaa-pyproject-srpm | cut -d' ' -f1)"
test "$signature1" == "$signature2"
# but also assert we are not comparing empty strings
test "$signature1" != ""

%if %{with tests}
export HOSTNAME="rpmbuild"  # to speedup tox in network-less mock, see rhbz#1856356
%pytest -vv --doctest-modules %{?with_pytest_xdist:-n auto} %{!?with_tox_tests:-k "not tox"}

# brp-compress is provided as an argument to get the right directory macro expansion
%{python3} compare_mandata.py -f %{_rpmconfigdir}/brp-compress
%endif


%files
%{_rpmmacrodir}/macros.pyproject
%{_rpmconfigdir}/mariner/pyproject_buildrequires.py
%{_rpmconfigdir}/mariner/pyproject_convert.py
%{_rpmconfigdir}/mariner/pyproject_save_files.py
%{_rpmconfigdir}/mariner/pyproject_preprocess_record.py
%{_rpmconfigdir}/mariner/pyproject_construct_toxenv.py
%{_rpmconfigdir}/mariner/pyproject_requirements_txt.py
%{_rpmconfigdir}/mariner/pyproject_wheel.py

%doc README.md
%license LICENSE

%files -n pyproject-srpm-macros
%{_rpmmacrodir}/macros.aaa-pyproject-srpm
%license LICENSE


%changelog
* Fri Jan 26 2024 Miro Hrončok <miro@hroncok.cz> - 1.12.0-1
- Namespace pyproject-rpm-macros generated text files with %%{python3_pkgversion}
- That way, a single-spec can be used to build packages for multiple Python versions
- Fixes: rhbz#2209055
