Summary:        A powerful, sanity-friendly HTTP client for Python.
Name:           python-urllib3
Version:        1.26.19
Release:        3%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://pypi.python.org/pypi/urllib3
Source0:        https://github.com/urllib3/urllib3/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildArch:      noarch

%description
A powerful, sanity-friendly HTTP client for Python.

%package -n     python3-urllib3
Summary:        python-urllib3
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
%if %{with_check}
BuildRequires:  python3-pip
BuildRequires:  python3-pytest
BuildRequires:  python3-mock
%endif
Requires:       python3

Patch0:         CVE-2025-50181.patch
Patch1:         CVE-2025-66418.patch
Patch2:         CVE-2026-21441.patch

%description -n python3-urllib3
urllib3 is a powerful, sanity-friendly HTTP client for Python. Much of the Python ecosystem already uses urllib3 and you should too.

%prep
%autosetup -p 1 -n urllib3-%{version}
# remove tests that are failing when running in chroot.
rm -rf test/with_dummyserver/
rm -rf test/contrib/

%build
%py3_build

%install
%py3_install

%check
# Install nox to handle test environment setup
pip3 install nox

# Patch dev-requirements.txt to use compatible versions with setuptools 69.x:
# - pytest 7.x+ is compatible with newer setuptools
# - flaky 3.8.0+ is compatible with pytest 7.x+
sed -i 's/pytest==4.6.9.*/pytest>=7.0.0/' dev-requirements.txt
sed -i 's/pytest==6.2.4.*/pytest>=7.0.0/' dev-requirements.txt
sed -i 's/flaky==3.7.0/flaky>=3.8.0/' dev-requirements.txt

# Run the test session for Python 3.9
# Skip test_recent_date which uses hardcoded date that is now in the past
# Note: test/with_dummyserver and test/contrib are removed in %prep
nox -s test-3.9 -- -k "not test_recent_date"

%files -n python3-urllib3
%defattr(-,root,root,-)
%license LICENSE.txt
%{python3_sitelib}/*

%changelog
* Fri Jan 09 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 1.26.19-3
- Patch for CVE-2025-66418, CVE-2026-21441

* Thu Jun 26 2025 Durga Jagadeesh Palli <v-dpalli@microsoft.com> - 1.26.19-2
- Patch CVE-2025-50181

* Thu Jun 20 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.26.19-1
- Auto-upgrade to 1.26.19 - patch CVE-2024-37891

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
