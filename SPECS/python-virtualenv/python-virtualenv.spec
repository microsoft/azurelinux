Summary:        Virtual Python Environment builder
Name:           python-virtualenv
Version:        20.36.1
Release:        3%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Languages/Python
URL:            https://pypi.python.org/pypi/virtualenv
Source0:        https://files.pythonhosted.org/packages/aa/a3/4d310fa5f00863544e1d0f4de93bddec248499ccf97d4791bc3122c9d4f3/virtualenv-20.36.1.tar.gz
Patch0:         0001-replace-to-flit.patch
Patch1000:      CVE-2025-50181.patch
Patch1001:      CVE-2026-1703v0.patch
Patch1002:      CVE-2026-1703v1.patch
Patch1003:      CVE-2026-24049v0.patch
Patch1004:      CVE-2026-24049v1.patch
Patch1005:      CVE-2026-3219v0.patch
Patch1006:      CVE-2026-3219v1.patch
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
Requires:       python3-platformdirs
Requires:       python3-distlib < 1
Requires:       python3-filelock
Provides:       %{name}-doc = %{version}-%{release}

%description -n python3-virtualenv
virtualenv is a tool to create isolated Python environment.

%prep
# Adding -N to enable manual patching, needed for CVE-2025-50181
%autosetup -p1 -n virtualenv-%{version} -N
%patch -P 0 -p1

# Manual patching for CVE-2025-50181 and CVE-2026-1703v0
# For CVE-2025-50181, poolmanager.py file is located in 2 different places and each is of different version so the same patch cannot be applied to all of them.
# For CVE-2026-1703, unpacking.py file is located in 2 different places and each is of different version so the same patch cannot be applied to all of them.
# Affected files are under src and archived inside a .whl file, so we need to unpack it, apply the patch, and then re-zip it.

echo "Manually Patching virtualenv-20.36.1/src/virtualenv/seed/wheels/embed/pip-25.0.1-py3-none-any.whl/pip/_vendor/urllib3/poolmanager.py"
mkdir -p unpacked_pip-25.0.1-py3-none-any
unzip src/virtualenv/seed/wheels/embed/pip-25.0.1-py3-none-any.whl -d unpacked_pip-25.0.1-py3-none-any
patch -p1 -d unpacked_pip-25.0.1-py3-none-any < %{PATCH1000}
echo "Manually Patching virtualenv-20.36.1/src/virtualenv/seed/wheels/embed/pip-25.0.1-py3-none-any.whl/pip/_internal/utils/unpacking.py"
patch -p1 -d unpacked_pip-25.0.1-py3-none-any < %{PATCH1001}
# Remove the original file
rm -f src/virtualenv/seed/wheels/embed/pip-25.0.1-py3-none-any.whl
# After patching, re-zip the contents back into a .whl
pushd unpacked_pip-25.0.1-py3-none-any
zip -r ../src/virtualenv/seed/wheels/embed/pip-25.0.1-py3-none-any.whl *
popd
rm -rf unpacked_pip-25.0.1-py3-none-any

# Manual patching for CVE-2025-50181 and CVE-2026-1703v1
echo "Manually Patching virtualenv-20.36.1/src/virtualenv/seed/wheels/embed/pip-25.3-py3-none-any.whl/pip/_vendor/urllib3/poolmanager.py"
mkdir -p unpacked_pip-25.3-py3-none-any
unzip src/virtualenv/seed/wheels/embed/pip-25.3-py3-none-any.whl -d unpacked_pip-25.3-py3-none-any
patch -p1 -d unpacked_pip-25.3-py3-none-any < %{PATCH1000}
echo "Manually Patching virtualenv-20.36.1/src/virtualenv/seed/wheels/embed/pip-25.3-py3-none-any.whl/pip/_internal/utils/unpacking.py"
patch -p1 -d unpacked_pip-25.3-py3-none-any < %{PATCH1002}
rm -f src/virtualenv/seed/wheels/embed/pip-25.3-py3-none-any.whl
pushd unpacked_pip-25.3-py3-none-any
zip -r ../src/virtualenv/seed/wheels/embed/pip-25.3-py3-none-any.whl *
popd
rm -rf unpacked_pip-25.3-py3-none-any

# Manual patching for CVE-2026-24049v0
# For CVE-2026-24049, unpack.py file is located in 3 different places and each is of different version so the same patch cannot be applied to all of them.
# Affected files are under src and archived inside a .whl file, so we need to unpack it, apply the patch, and then re-zip it.
echo "Manually Patching virtualenv-20.36.1/src/virtualenv/seed/wheels/embed/setuptools-75.3.2-py3-none-any.whl/setuptools/_vendor/wheel/cli/unpack.py"
mkdir -p unpacked_setuptools-75.3.2-py3-none-any
unzip src/virtualenv/seed/wheels/embed/setuptools-75.3.2-py3-none-any.whl -d unpacked_setuptools-75.3.2-py3-none-any
patch -p1 -d unpacked_setuptools-75.3.2-py3-none-any < %{PATCH1003}
rm -f src/virtualenv/seed/wheels/embed/setuptools-75.3.2-py3-none-any.whl
pushd unpacked_setuptools-75.3.2-py3-none-any
zip -r ../src/virtualenv/seed/wheels/embed/setuptools-75.3.2-py3-none-any.whl *
popd
rm -rf unpacked_setuptools-75.3.2-py3-none-any

# Manual patching for CVE-2026-24049v0
echo "Manually Patching virtualenv-20.36.1/src/virtualenv/seed/wheels/embed/setuptools-80.9.0-py3-none-any.whl/setuptools/_vendor/wheel/cli/unpack.py"
mkdir -p unpacked_setuptools-80.9.0-py3-none-any
unzip src/virtualenv/seed/wheels/embed/setuptools-80.9.0-py3-none-any.whl -d unpacked_setuptools-80.9.0-py3-none-any
patch -p1 -d unpacked_setuptools-80.9.0-py3-none-any < %{PATCH1003}
rm -f src/virtualenv/seed/wheels/embed/setuptools-80.9.0-py3-none-any.whl
pushd unpacked_setuptools-80.9.0-py3-none-any
zip -r ../src/virtualenv/seed/wheels/embed/setuptools-80.9.0-py3-none-any.whl *
popd
rm -rf unpacked_setuptools-80.9.0-py3-none-any

# Manual patching for CVE-2026-24049v1
echo "Manually Patching virtualenv-20.36.1/src/virtualenv/seed/wheels/embed/unpacked_wheel-0.45.1-py3-none-any.whl/wheel/cli/unpack.py"
mkdir -p unpacked_wheel-0.45.1-py3-none-any
unzip src/virtualenv/seed/wheels/embed/wheel-0.45.1-py3-none-any.whl -d unpacked_wheel-0.45.1-py3-none-any
patch -p1 -d unpacked_wheel-0.45.1-py3-none-any < %{PATCH1004}
rm -f src/virtualenv/seed/wheels/embed/wheel-0.45.1-py3-none-any.whl
pushd unpacked_wheel-0.45.1-py3-none-any
zip -r ../src/virtualenv/seed/wheels/embed/unpacked_wheel-0.45.1-py3-none-any.whl *
popd
rm -rf unpacked_wheel-0.45.1-py3-none-any

# Manual patching for CVE-2026-3219v0
echo "Manually Patching virtualenv-20.36.1/src/virtualenv/seed/wheels/embed/pip-25.0.1-py3-none-any.whl/pip/_internal/utils/unpacking.py for CVE-2026-3219"
mkdir -p unpacked_pip-25.0.1-py3-none-any_3219
unzip src/virtualenv/seed/wheels/embed/pip-25.0.1-py3-none-any.whl -d unpacked_pip-25.0.1-py3-none-any_3219
patch -p1 -d unpacked_pip-25.0.1-py3-none-any_3219 < %{PATCH1005}
rm -f src/virtualenv/seed/wheels/embed/pip-25.0.1-py3-none-any.whl
pushd unpacked_pip-25.0.1-py3-none-any_3219
zip -r ../src/virtualenv/seed/wheels/embed/pip-25.0.1-py3-none-any.whl *
popd
rm -rf unpacked_pip-25.0.1-py3-none-any_3219

# Manual patching for CVE-2026-3219v1
echo "Manually Patching virtualenv-20.36.1/src/virtualenv/seed/wheels/embed/pip-25.3-py3-none-any.whl/pip/_internal/utils/unpacking.py for CVE-2026-3219"
mkdir -p unpacked_pip-25.3-py3-none-any_3219
unzip src/virtualenv/seed/wheels/embed/pip-25.3-py3-none-any.whl -d unpacked_pip-25.3-py3-none-any_3219
patch -p1 -d unpacked_pip-25.3-py3-none-any_3219 < %{PATCH1006}
rm -f src/virtualenv/seed/wheels/embed/pip-25.3-py3-none-any.whl
pushd unpacked_pip-25.3-py3-none-any_3219
zip -r ../src/virtualenv/seed/wheels/embed/pip-25.3-py3-none-any.whl *
popd
rm -rf unpacked_pip-25.3-py3-none-any_3219


%generate_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install

%check
pip3 install 'tox>=3.27.1,<4.0.0'
# skip "test_can_build_c_extensions" tests since they fail on python3_version >= 3.12. See https://src.fedoraproject.org/rpms/python-virtualenv/blob/rawhide/f/python-virtualenv.spec#_153
sed -i 's/coverage run -m pytest {posargs:--junitxml {toxworkdir}\/junit\.{envname}\.xml tests --int}/coverage run -m pytest {posargs:--junitxml {toxworkdir}\/junit\.{envname}\.xml tests -k "not test_can_build_c_extensions" --int}/g' tox.ini
tox -e py

%files -n python3-virtualenv
%defattr(-,root,root,-)
%license LICENSE
%{python3_sitelib}/*
%{_bindir}/virtualenv

%changelog
* Thu Apr 23 2026 Akarsh Chaudhary <v-akarshc@microsoft.com>- 20.36.1-3
- Patch for CVE-2026-3219

* Mon Feb 23 2026 BinduSri Adabala <v-badabala@microsoft.com> - 20.36.1-2
- Patch for CVE-2025-50181, CVE-2026-24049 and CVE-2026-1703

* Wed Jan 14 2026 Archana Shettigar <v-shettigara@microsoft.com> - 20.36.1-1
- Upgrade to 20.36.1 for CVE-2026-22702

* Wed Dec 11 2024 Sudipta Pandit <sudpandit@microsoft.com> - 20.25.0-3
- Backport fix for CVE-2024-53899

* Wed Apr 24 2024 Andrew Phelps <anphel@microsoft.com> - 20.25.0-2
- Add runtime requirement on python3-filelock

* Fri Mar 22 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 20.25.0-1
- Auto-upgrade to 20.25.0 - 3.0 package upgrade
- Added patch to use python3-flit-core as build-backend rather than hatchling (which is not yet supported on Azure Linux)

* Thu Mar 07 2024 Andrew Phelps <anphel@microsoft.com> - 20.14.0-4
- Remove version restriction on python3-platformdirs Requires

* Wed Dec 21 2022 Riken Maharjan <rmaharjan@microsoft.com> - 20.14.0-3
- Add missing runtime dependencies

* Fri Dec 16 2022 Sam Meluch <sammeluch@microsoft.com> - 20.14.0-2
- Update version of tox used for package tests

* Fri Mar 25 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 20.14.0-1
- Upgrade to 20.14.0

* Tue Feb 08 2022 Muhammad Falak <mwani@microsoft.com> - 16.0.0-8
- Add an explicit BR on `python3-pip` to enable ptest

* Wed Oct 20 2021 Thomas Crain <thcrain@microsoft.com> - 16.0.0-7
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
