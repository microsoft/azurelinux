%global common_description %{expand:
This repository is a collection of Python library code for building Python
applications. The code is collected from Google’s own Python code base, and has
been extensively tested and used in production.

Features:

  • Simple application startup
  • Distributed commandline flags system
  • Custom logging module with additional features
  • Testing utilities}

Summary:        Abseil Python Common Libraries
Name:           python-absl-py
Version:        1.4.0
Release:        1%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/abseil/abseil-py
Source0:        %{url}/archive/v%{version}/abseil-py-%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-wheel

%description %{common_description}

%package -n     python3-absl-py
Summary:        %{summary}
%py_provides python3-absl

%description -n python3-absl-py %{common_description}

%prep
%autosetup -n abseil-py-%{version}
%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files absl


%check
# Since we cannot run the full upstream test suite (see comments below), we
# start with an import “smoke test”:
%pyproject_check_import

# Upstream provides some “smoke tests” that we can run, too. We cannot use the
# wrapper smoke_tests/smoke_test.sh because it downloads things from the
# Internet, but we can run the Python scripts manually.
PYTHONPATH='%{buildroot}/%{python3_sitelib}'; export PYTHONPATH
%{python3} smoke_tests/sample_app.py --echo smoke 2>&1 |
  grep -F 'echo is smoke.'
%{python3} smoke_tests/sample_test.py | grep -Fq 'msg_for_test'

# Running the actual test suite requires bazel, which will almost certainly
# never be packaged for Fedora due to its Byzantine mass of bundled
# dependencies. It is possible to invoke the tests with another runner, such as
# pytest, but there are many spurious failures due to the incorrect
# environment, so it is useless to do so.


%files -n python3-absl-py -f %{pyproject_files}
%doc AUTHORS
%doc CHANGELOG.md
%doc CONTRIBUTING.md
%doc README.md
%doc smoke_tests
%license LICENSE

%changelog
* Thu Nov 02 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.4.0-1
- Auto-upgrade to 1.4.0 - Azure Linux 3.0 - package upgrades

* Wed Oct 05 2022 Riken Maharjan <rmaharjan@microsoft.com> - 1.2.0-1
- License verified
- Initial CBL-Mariner import from Fedora 37 (license: MIT).

* Tue Jun 15 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 0.13.0-1
- Update to 0.13.0; closes RHBZ#1972146

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.12.0-5
- Rebuilt for Python 3.10

* Tue Mar 30 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 0.12.0-4
- Use pyproject-rpm-macros for build and install, too

* Tue Mar 16 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 0.12.0-3
- Drop python3dist(setuptools) BR, redundant with %%pyproject_buildrequires

* Wed Mar 10 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 0.12.0-2
- Add CHANGELOG.md, from absl/, to documentation

* Wed Mar 10 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 0.12.0-1
- Update to 0.12.0
- Drop python-absl-py-0.11.0-python-3.10.patch, now upstreamed

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Dec 11 2020 Benjamin A. Beasley <code@musicinmybrain.net> - 1.1.0-4
- Fix Python 3.10 incompatibility due to incorrect string-based version
  detection (RHBZ#1906811, https://github.com/abseil/abseil-py/issues/161)

* Tue Dec  1 2020 Benjamin A. Beasley <code@musicinmybrain.net> - 1.1.0-3
- Remove conditionals for Fedora 32 and older

* Wed Nov 25 2020 Benjamin A. Beasley <code@musicinmybrain.net> - 1.1.0-2
- Remove EPEL conditionals from Fedora spec file

* Wed Nov 25 2020 Benjamin A. Beasley <code@musicinmybrain.net> - 1.1.0-1
- Initial package
