Summary:        A powerful, sanity-friendly HTTP client for Python.
Name:           python-urllib3
Version:        1.26.9
Release:        2%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://pypi.python.org/pypi/urllib3
Source0:        https://github.com/urllib3/urllib3/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildArch:      noarch
Patch0:         CVE-2023-43804.patch

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
%endif
Requires:       python3

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
pip3 install --user --upgrade nox
PATH="$PATH:/root/.local/bin/"
nox --reuse-existing-virtualenvs --sessions test-%{python3_version}

%files -n python3-urllib3
%defattr(-,root,root,-)
%license LICENSE.txt
%{python3_sitelib}/*

%changelog
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
