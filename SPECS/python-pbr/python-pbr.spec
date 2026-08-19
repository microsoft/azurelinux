Summary:        Python Build Reasonableness
Name:           python-pbr
Version:        6.0.0
Release:        2%{?dist}
License:        Apache-2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Languages/Python
URL:            https://docs.openstack.org/developer/pbr/
Source0:        https://pypi.io/packages/source/p/pbr/pbr-%{version}.tar.gz
Patch0:         disable-test-wsgi.patch
Patch1:         test-pin-sphinx.patch
BuildArch:      noarch

%description
A library for managing setuptools packaging needs in a consistent manner.

%package -n     python3-pbr
Summary:        Python Build Reasonableness
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
%if 0%{?with_check}
BuildRequires:  git
BuildRequires:  gnupg2
BuildRequires:  python3-pip
BuildRequires:  python3-virtualenv
BuildRequires:  python3-wheel
%endif

%description -n python3-pbr
A library for managing setuptools packaging needs in a consistent manner.

%prep
%autosetup -p 1 -n pbr-%{version}

%build
export SKIP_PIP_INSTALL=1
%py3_build

%install
%py3_install
ln -s pbr %{buildroot}/%{_bindir}/pbr3

%check
# tox 3.x + virtualenv 21.x fails to editable-install due to setuptools isolation.
# Run tests directly with stestr instead.
#
# Skip 5 tests that exercise pbr's pip-bootstrap path: they create a fresh
# virtualenv and run 'pip install -U pip wheel build <pbr-source>'. Because
# pbr 6.0.0 ships no pyproject.toml, pip falls back to a PEP 517 isolated
# build env containing only setuptools+wheel. pbr's own setup.py starts with
# 'from pbr import util', which fails inside that isolated env
# (ModuleNotFoundError: No module named 'pbr'). PYTHONPATH cannot reach in
# either, because pip strips it from the build subprocess. tox 'usedevelop'
# papered over this historically by injecting an editable pbr install before
# the tests spawned the inner venv, but that workflow is broken with current
# setuptools. The self-bootstrap is fixed upstream in pbr 6.1+.
pip3 install stestr testscenarios testresources six
python3 -m stestr run --suppress-attachments \
    --exclude-regex '(test_freeze_command|test_console_script_develop|test_console_script_install|test_pep_517_support|test_requirement_parsing)'

%files -n python3-pbr
%defattr(-,root,root)
%license LICENSE
%doc README.rst
%{_bindir}/pbr
%{_bindir}/pbr3
%{python3_sitelib}/pbr-%{version}-*.egg-info
%{python3_sitelib}/pbr

%changelog
* Wed Jun 17 2026 Kshitiz Godara <kgodara@microsoft.com> - 6.0.0-2
- Replace tox-based testing with a direct stestr invocation; tox 3.x +
  virtualenv 21.x fails to editable-install due to setuptools isolation.
- Add python3-virtualenv and python3-wheel BRs so test discovery can
  import pbr.tests.test_packaging / test_integration.
- Exclude 5 tests (test_freeze_command, test_console_script_{develop,install},
  test_pep_517_support, test_requirement_parsing) -- they create an isolated
  virtualenv, pip-install pbr-from-source, then import a fixture
  ('pbr_testpackage') whose __init__.py does 'import pbr.version', which
  fails since the isolated venv has no system pbr.

* Fri Feb 09 2024 Ameya Usgaonkar <ausgaonkar@microsoft.com> - 6.0.0-1
- Upgrade to version 6.0.0

* Fri May 19 2023 Olivia Crain <oliviacrain@microsoft.com> - 5.8.1-4
- Add patch to pin version of sphinx used in tests to a known compatible version
- Remove check-time install of packages that should be handled by tox
- Use SPDX license expression in license tag

* Fri Dec 16 2022 Sam Meluch <sammeluch@microsoft.com> - 5.8.1-3
- Update version of tox used for package tests

* Tue Mar 15 2022 Muhammad Falak <mwani@microsoft.com> - 5.8.1-2
- Use `py%{python3_version_nodots}` instead of harcoding `py39`

* Thu Feb 10 2022 Muhammad Falak <mwani@microsoft.com> - 5.8.1-1
- Bump version to 5.8.1
- Use `tox` instead of `setup.py test` to enable ptest

* Fri Dec 03 2021 Thomas Crain <thcrain@microsoft.com> - 5.1.2-4
- Replace easy_install usage with pip in %%check sections

* Wed Oct 20 2021 Thomas Crain <thcrain@microsoft.com> - 5.1.2-3
- Remove python2 package
- Lint spec

* Thu Apr 16 2020 Nicolas Ontiveros <niontive@microsoft.com> - 5.1.2-2
- Use gnupg2 in BR.

* Wed Mar 18 2020 Paul Monson <paulmon@microsoft.com> - 5.1.2-1
- Update to version 5.1.2.  License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 4.2.0-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Wed Jan 16 2019 Tapas Kundu <tkundu@vmware.com> - 4.2.0-2
- Disabled the make check as the requirements can not be fulfilled

* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> - 4.2.0-1
- Update to version 4.2.0

* Wed Jul 19 2017 Divya Thaluru <dthaluru@vmware.com> - 2.1.0-5
- Fixed make check failure

* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> - 2.1.0-4
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.

* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> - 2.1.0-3
- Create pbr3 script

* Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 2.1.0-2
- Fix arch

* Fri Apr 14 2017 Dheeraj Shetty <dheerajs@vmware.com> - 2.1.0-1
- Initial packaging for Photon
