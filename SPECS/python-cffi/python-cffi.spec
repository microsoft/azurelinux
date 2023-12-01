Summary:        Interface for Python to call C code
Name:           python-cffi
Version:        1.15.0
Release:        3%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://pypi.python.org/pypi/cffi
Source0:        https://pypi.python.org/packages/source/c/cffi/cffi-%{version}.tar.gz

%description
Foreign Function Interface for Python.

%package -n     python3-cffi
Summary:        Interface for Python to call C code
BuildRequires:  libffi-devel
BuildRequires:  python3-devel
BuildRequires:  python3-pycparser
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
%if %{with_check}
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
BuildRequires:  python3-pip
%endif
Requires:       python3
Requires:       python3-libs
Requires:       python3-pycparser

%description -n python3-cffi
Foreign Function Interface for Python, providing a convenient and reliable way of calling existing C code from Python. The interface is based on LuaJIT’s FFI.

%prep
%autosetup -n cffi-%{version}

%build
%py3_build

%install
%py3_install

%check
pip3 install pytest==7.1.2
%python3 setup.py test

%files -n python3-cffi
%defattr(-,root,root,-)
%license LICENSE
%{python3_sitelib}/*

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 1.15.0-3
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Wed Oct 26 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.15.0-2
- Freezing 'pytest' test dependency to version 7.1.2.

* Thu Feb 10 2022 Nick Samson <nisamson@microsoft.com> - 1.15.0-1
- Upgraded to 1.15.0

* Fri Dec 03 2021 Olivia Crain <oliviacrain@microsoft.com> - 1.14.5-3
- Replace easy_install usage with pip in %%check sections

* Wed Oct 20 2021 Olivia Crain <oliviacrain@microsoft.com> - 1.14.5-2
- Add license to python3 package
- Remove python2 package
- Lint spec
- License verified

* Thu Feb 11 2021 Mateusz Malisz <mamalisz@microsoft.com> - 1.14.5-1
- Update to 1.14.5

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.11.5-4
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 1.11.5-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Thu Nov 15 2018 Tapas Kundu <tkundu@vmware.com> - 1.11.5-2
- Fixed make check errors.

* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> - 1.11.5-1
- Update to version 1.11.5

* Mon Jul 17 2017 Divya Thaluru <dthaluru@vmware.com> - 1.10.0-3
- Added build time dependecies required during check

* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> - 1.10.0-2
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.

* Mon Apr 03 2017 Rongrong Qiu <rqiu@vmware.com> - 1.10.0-1
- Update to 1.10.0

* Thu Mar 23 2017 Xiaolin Li <xiaolinl@vmware.com> - 1.9.1-1
- Updated to version 1.9.1.

* Thu Feb 02 2017 Xiaolin Li <xiaolinl@vmware.com> - 1.5.2-4
- Added python3 site-packages.

* Mon Oct 03 2016 ChangLee <changLee@vmware.com> - 1.5.2-3
- Modified %check

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 1.5.2-2
- GA - Bump release of all rpms

* Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> - 1.5.2-1
- Updated to version 1.5.2

* Thu Jan 21 2016 Anish Swaminathan <anishs@vmware.com> - 1.5.0-1
- Upgrade version

* Wed Nov 18 2015 Divya Thaluru <dthaluru@vmware.com> - 1.3.0-1
- nitial packaging for Photon
