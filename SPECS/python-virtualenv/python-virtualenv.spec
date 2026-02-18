Summary:        Virtual Python Environment builder
Name:           python-virtualenv
Version:        20.36.1
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://pypi.python.org/pypi/virtualenv
Source0:        https://files.pythonhosted.org/packages/aa/a3/4d310fa5f00863544e1d0f4de93bddec248499ccf97d4791bc3122c9d4f3/virtualenv-20.36.1.tar.gz
Patch0:         0001-replace-to-flit.patch
Patch1000:      CVE-2025-50181.patch
BuildArch:      noarch

%description
virtualenv is a tool to create isolated Python environment.

%package -n     python3-virtualenv
Summary:        Virtual Python Environment builder
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools_scm
BuildRequires:  python3-xml
BuildRequires:  python3-wheel
BuildRequires:  zip

%if 0%{?with_check}
BuildRequires:  python3-pip
%endif
BuildRequires:  python3-flit
BuildRequires:  python3-flit-core >= 3.8.0

Requires:       python3
Requires:       python3-filelock
Requires:       python3-platformdirs = 2.0.0
Requires:       python3-distlib < 1
Requires:       python3-six
Provides:       %{name}-doc = %{version}-%{release}

%description -n python3-virtualenv
virtualenv is a tool to create isolated Python environment.

%prep
# Adding -N to enable manual patching, needed for CVE-2025-50181 
%autosetup -p1 -n virtualenv-%{version} -N
%patch0 -p1

# Manual patching for CVE-2025-50181
# This patch is needed to fix the issue with urllib3 poolmanager.py
# The poolmanager.py file is located in 4 different places and each is of different version so the same patch cannot be applied to all of them.
# For the poolmanager.py under src, it is archived inside a .whl file, so we need to unpack it, apply the patch, and then re-zip it.
# For the poolmanager.py under tests, it is archived inside a .whl file, which in turn is archived inside another .whl file,
# so, we need to unpack the outer .whl, then unpack the inner .whl, apply the patch, and then re-zip both levels.

echo "Manually Patching virtualenv-20.36.1/src/virtualenv/seed/wheels/embed/pip-25.0.1-py3-none-any.whl/pip/_vendor/urllib3/poolmanager.py"
mkdir -p unpacked_pip-25.0.1-py3-none-any
unzip src/virtualenv/seed/wheels/embed/pip-25.0.1-py3-none-any.whl -d unpacked_pip-25.0.1-py3-none-any
patch -p1 -d unpacked_pip-25.0.1-py3-none-any < %{PATCH1000}
# Remove the original file
rm -f src/virtualenv/seed/wheels/embed/pip-25.0.1-py3-none-any.whl
# After patching, re-zip the contents back into a .whl
pushd unpacked_pip-25.0.1-py3-none-any
zip -r ../src/virtualenv/seed/wheels/embed/pip-25.0.1-py3-none-any.whl *
popd
rm -rf unpacked_pip-25.0.1-py3-none-any

echo "Manually Patching virtualenv-20.36.1/src/virtualenv/seed/wheels/embed/pip-25.3-py3-none-any.whl/pip/_vendor/urllib3/poolmanager.py"
mkdir -p unpacked_pip-25.3-py3-none-any
unzip src/virtualenv/seed/wheels/embed/pip-25.3-py3-none-any.whl -d unpacked_pip-25.3-py3-none-any
patch -p1 -d unpacked_pip-25.3-py3-none-any < %{PATCH1000}
# Remove the original file
rm -f src/virtualenv/seed/wheels/embed/pip-25.3-py3-none-any.whl
# After patching, re-zip the contents back into a .whl
pushd unpacked_pip-25.3-py3-none-any
zip -r ../src/virtualenv/seed/wheels/embed/pip-25.3-py3-none-any.whl *
popd
rm -rf unpacked_pip-25.3-py3-none-any

%generate_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install

%check
pip3 install 'tox>=3.27.1,<4.0.0'
# skip "test_can_build_c_extensions" tests since they fail on python3_version >= 3.12. See https://src.fedoraproject.org/rpms/python-virtualenv/blob/rawhide/f/python-virtualenv.spec#_153
export PYTEST_ADDOPTS='-k "not test_can_build_c_extensions"'
tox -e py

%files -n python3-virtualenv
%defattr(-,root,root,-)
%license LICENSE
%{python3_sitelib}/*
%{_bindir}/virtualenv

%changelog
* Thu Jan 15 2026 Archana Shettigar <v-shettigara@microsoft.com> - 20.36.1-1
- Upgrade to 20.36.1 for CVE-2026-22702

* Wed Jul 09 2025 Aninda Pradhan <v-anipradhan@microsoft.com> - 20.26.6-2
- Add patch to fix CVE-2025-50181 in urllib3 poolmanager.py

* Wed Feb 26 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 20.26.6-1
- Auto-upgrade to 20.26.6 - for CVE-2024-53899 [High]
- Remove previously applied patches
- Added patch to use python3-flit-core as build-backend rather than hatchling (which is not yet supported on Azure Linux) 

* Wed Feb 07 2024 corvus-callidus <108946721+corvus-callidus@users.noreply.github.com> - 20.14.0-6
- Fix pytest version to <8 for compatibility

* Thu Jan 25 2024 corvus-callidus <108946721+corvus-callidus@users.noreply.github.com> - 20.14.0-5
- Add missing runtime dependency on python-six

* Mon Dec 04 2023 Olivia Crain <oliviacrain@microsoft.com> - 20.14.0-4
- Add upstream patch to fix package tests with newer versions of pluggy

* Wed Dec 21 2022 Riken Maharjan <rmaharjan@microsoft.com> - 20.14.0-3
- Add missing runtime dependencies

* Fri Dec 16 2022 Sam Meluch <sammeluch@microsoft.com> - 20.14.0-2
- Update version of tox used for package tests

* Fri Mar 25 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 20.14.0-1
- Upgrade to 20.14.0

* Tue Feb 08 2022 Muhammad Falak <mwani@microsoft.com> - 16.0.0-8
- Add an explicit BR on `python3-pip` to enable ptest

* Wed Oct 20 2021 Olivia Crain <oliviacrain@microsoft.com> - 16.0.0-7
- Add license, virtualenv binary to python3 package
- Remove python2 package
- Lint spec

* Mon Feb 15 2021 Henry Li <lihl@microsoft.com> - 16.0.0-6
- Provides python-virtualenv-doc

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 16.0.0-5
- Added %%license line automatically

* Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> - 16.0.0-4
- Renaming python-pytest to pytest

* Thu Apr 23 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 16.0.0-3
- License verified.
- Fixed 'Source0' tag.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 16.0.0-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> - 16.0.0-1
- Update to version 16.0.0

* Fri Aug 25 2017 Vinay Kulkarni <kulkarniv@vmware.com> - 15.1.0-1
- Initial version of python-virtualenv package for Photon.
