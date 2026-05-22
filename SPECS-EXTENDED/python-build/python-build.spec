# not all test dependencies are included in RHEL: filelock, pytest-mock
%bcond tests %{undefined rhel}
# uv has many build dependencies which are not included in RHEL;
# virtualenv is not included in RHEL
%bcond extras %{undefined rhel}
 
%global pypi_name build
 
Name:           python-%{pypi_name}
Version:        1.4.2
Release:        1%{?dist}
Summary:        A simple, correct PEP517 package builder
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
 
License:        MIT
URL:            https://github.com/pypa/build
Source0:        %{url}/archive/%{version}/%{pypi_name}-%{version}.tar.gz
 
# downstream-only
#Patch:          0001-fedora-disable-some-build-requirements.patch
 
BuildArch:      noarch
 
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-flit-core
BuildRequires:  python3-wheel
BuildRequires:  python3-pyproject-hooks
BuildRequires:  pyproject-rpm-macros >= 0-41
%if %{with tests}
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(pytest-mock)
BuildRequires:  python3dist(filelock)
%endif
 
%description
A simple, correct PEP517 package builder.
 
 
%package -n     python3-%{pypi_name}
Summary:        %{summary}
 
%description -n python3-%{pypi_name}
A simple, correct PEP517 package builder.
 
 
# Even --without extras, we still build the extras in ELN
# to make it available in ELN Extras (e.g. tox).
# Note that due to technical limitations,
# we must *not* generate their runtime deps as BuildRequires
# or else they are pulled into ELN proper (not ELN Extras).
# https://github.com/fedora-eln/eln/issues/309
%if %{with extras} || %{defined eln}
%pyproject_extras_subpkg -n python3-%{pypi_name} virtualenv uv
%endif
 
%prep
%autosetup -p1 -n %{pypi_name}-%{version}

# flit-core in this buildroot expects PEP 621 license as a table.
if grep -qE '^license *= *"[^"]+"' pyproject.toml; then
	sed -E -i 's/^license *= *"([^"]+)"/license = {text = "\1"}/' pyproject.toml
fi

# Add the 'flaky' marker used in upstream tests but not declared in pyproject.toml.
sed -i '/^markers = \[/a\  "flaky",' pyproject.toml

# When building as root, file-permission checks are bypassed; skip the
# PermissionError branch of test_init to avoid a spurious DID NOT RAISE failure.
sed -i "s/if not sys.platform.startswith('win'):/if not sys.platform.startswith('win') and os.getuid() != 0:/" \
    tests/test_projectbuilder.py

%generate_buildrequires
%if %{with tests}
%pyproject_buildrequires -R
%else
%pyproject_buildrequires
%endif

%build
%pyproject_wheel
%install
%pyproject_install
%pyproject_save_files %{pypi_name}
 
%check
%pyproject_check_import
%if %{with tests}
# Upstream has integration tests that can be run with the --run-integration
# flag, but currently that only includes one network test and one test that is
# xfail when flit-core is installed (which it will be during our package
# build), so including that flag doesn't run any additional tests.
%pytest -v -m "not network"
%endif
 
%files -n python3-%{pypi_name} -f %{pyproject_files}
%license LICENSE
%doc README.md
%{_bindir}/pyproject-build
 
%changelog
* Sat Apr 4 2026 Akarsh Chaudhary <v-akarshc@microsoft.com> - 1.4.2-1
- Initial CBL-Mariner import from Fedora 44 (license: MIT).
- License verified