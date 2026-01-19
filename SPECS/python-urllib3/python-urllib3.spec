Summary:        A powerful, sanity-friendly HTTP client for Python.
Name:           python-urllib3
Version:        2.0.7
Release:        4%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Languages/Python
URL:            https://pypi.python.org/pypi/urllib3
Source0:        https://github.com/urllib3/urllib3/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildArch:      noarch
Patch0:         urllib3_test_recent_date.patch
Patch1:         change-backend-to-flit_core.patch
Patch2:         CVE-2024-37891.patch
Patch3:         CVE-2025-50181.patch
Patch4:         CVE-2025-66418.patch
Patch5:         CVE-2025-66471.patch
Patch6:         CVE-2026-21441.patch

%description
A powerful, sanity-friendly HTTP client for Python.

%package -n     python3-urllib3
Summary:        python-urllib3
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
BuildRequires:  python-flit-core
Requires:       python3

%description -n python3-urllib3
urllib3 is a powerful, sanity-friendly HTTP client for Python. Much of the Python ecosystem already uses urllib3 and you should too.

%prep
%autosetup -p 1 -n urllib3-%{version}
# remove tests that are failing when running in chroot.
rm -rf test/with_dummyserver/
rm -rf test/contrib/

%build
%pyproject_wheel

%install
%pyproject_install

%check
pip3 install --upgrade pip
pip3 install tornado>=6.2 \
    trustme>=0.9.0 \
    pytest>=7.4.0 \
    pytest-cov>=2.7.1 \
    Brotli>=1.0.9 \
    PySocks>=1.7.1 \
    certifi \
    cryptography>=1.9 \
    flaky \
    idna>=3.4 \
    psutil \
    pytest>=7.4.0 \
    pytest-timeout>=2.1.0 \
    pytest-xdist \
    urllib3>=%{version}

# gh#urllib3/urllib3#2109
export CI="true"
# skip some randomly failing tests (mostly on i586, but sometimes they fail on other architectures)
skiplist="test_ssl_read_timeout or test_ssl_failed_fingerprint_verification or test_ssl_custom_validation_failure_terminates"
# gh#urllib3/urllib3#1752 and others: upstream's way of checking that the build
# system has a correct system time breaks (re-)building the package after too
# many months have passed since the last release.
skiplist+=" or test_recent_date"
# too slow to run in obs (checks 2GiB of data)
skiplist+=" or test_requesting_large_resources_via_ssl"
# Try to access external evil.com
skiplist+=" or test_deprecated_no_scheme"
# Skip timezone test
skiplist+=" or test_respect_retry_after_header_sleep"
%pytest -k "not (${skiplist})" --ignore test/with_dummyserver/test_socketlevel.py

%files -n python3-urllib3
%defattr(-,root,root,-)
%license LICENSE.txt
%{python3_sitelib}/*

%changelog
* Fri Jan 09 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 2.0.7-4
- Patch for CVE-2026-21441

* Wed Dec 10 2025 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 2.0.7-3
- Patch for CVE-2025-66418, CVE-2025-66471

* Tue Jun 24 2025 Durga Jagadeesh Palli <v-dpalli@microsoft.com> - 2.0.7-2
- add patch for CVE-2025-50181

* Wed Jul 10 2024 Sumedh Sharma <sumsharma@microsoft.com> - 2.0.7-1
- Bump version to fix CVE-2023-43804 & CVE-2023-45803.
- Add patch file to fix CVE-2024-37891.

* Fri Feb 02 2024 Henry Li <lihl@microsoft.com> - 2.0.4-1
- Upgrade to version 2.0.4
- Add patch to change backend build system to python-flit-core
- Add python-flit-core as BR
- Fix test section

* Wed Jan 17 2024 Mandeep Plaha <mandeepplaha@microsoft.com> - 1.26.18-2
- Fix test_recent_date test by updating the hard-coded date used for test

* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.26.18-1
- Auto-upgrade to 1.26.18 - fix CVE-2023-45803

* Thu Oct 12 2023 Amrita Kohli <amritakohli@microsoft.com> - 1.26.9-2
- Patch CVE-2023-43804

* Fri Mar 25 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 1.26.9-1
- Upgrade to 1.26.9

* Wed Oct 20 2021 Thomas Crain <thcrain@microsoft.com> - 1.25.9-3
- Add license to python3 package
- Move python3-pip to check-time build requirements
- Remove python2 package
- Lint spec

* Fri Jul 09 2021 Henry Li <lihl@microsoft.com> - 1.25.9-2
- Resolve CVE-2021-33503

* Wed Dec 23 2020 Rachel Menge <rachelmenge@microsoft.com> - 1.25.9-1
- Updated to version 1.25.9

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.24.2-2
- Added %%license line automatically

* Thu Mar 19 2020 Paul Monson <paulmon@microsoft.com> - 1.24.2-1
- Update to version 1.24.2. Updated Source0 URL. License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 1.23-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Mon Jan 14 2019 Tapas Kundu <tkundu@vmware.com> - 1.23-2
- Fix make check

* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> - 1.23-1
- Update to version 1.23

* Tue Aug 15 2017 Xiaolin Li <xiaolinl@vmware.com> - 1.20-5
- Increased number of open files per process to 5000 before run make check.

* Wed Jul 26 2017 Divya Thaluru <dthaluru@vmware.com> - 1.20-4
- Fixed rpm check errors

* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> - 1.20-3
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.

* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> - 1.20-2
- Use python2 explicitly

* Thu Feb 02 2017 Xiaolin Li <xiaolinl@vmware.com> - 1.20-1
- Initial packaging for Photon
