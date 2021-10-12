Summary:        A network address manipulation library for Python
Name:           python-netaddr
Version:        0.7.19
Release:        9%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://github.com/netaddr/netaddr
Source0:        https://github.com/netaddr/netaddr/archive/netaddr-%{version}.tar.gz
Patch0:         0001-fixed-broken-tests-in-issue-149-python-3-regression.patch
BuildArch:      noarch

%description
A network address manipulation library for Python

%package -n python3-netaddr
Summary:        A network address manipulation library for Python
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
%if %{with_check}
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
%endif

%description -n python3-netaddr
A network address manipulation library for Python

%prep
%autosetup -p 1 -n netaddr-%{version}

%build
%py3_build

%install
%py3_install
ln -s netaddr %{buildroot}/%{_bindir}/netaddr3

%check
easy_install_3=$(ls %{_bindir} |grep easy_install |grep 3)
$easy_install_3 pytest
LANG=en_US.UTF-8 PYTHONPATH=./ %{python3} setup.py test

%files -n python3-netaddr
%defattr(-,root,root,-)
%license LICENSE
%{_bindir}/netaddr
%{_bindir}/netaddr3
%{python3_sitelib}/*

%changelog
* Fri Oct 01 2021 Thomas Crain <thcrain@microsoft.com> - 0.7.19-9
- Add license to python3 package
- Remove python2 package
- Lint spec

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 0.7.19-8
- Added %%license line automatically

* Tue Apr 07 2020 Joe Schmitt <joschmit@microsoft.com> - 0.7.19-7
- Initial CBL-Mariner import from Photon (license: Apache2).
- Update URL.
- Update Source0 with valid URL.
- Remove sha1 macro.
- License verified.

* Mon Dec 03 2018 Tapas Kundu <tkundu@vmware.com> - 0.7.19-6
- Fixed make check.

* Tue Jul 25 2017 Divya Thaluru <dthaluru@vmware.com> - 0.7.19-5
- Fixed test command and added patch to fix test issues.

* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> - 0.7.19-4
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.

* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> - 0.7.19-3
- Separate python2 and python3 bindings

* Mon Mar 27 2017 Xiaolin Li <xiaolinl@vmware.com> - 0.7.19-2
- Added python3 package.

* Fri Feb 03 2017 Vinay Kulkarni <kulkarniv@vmware.com> - 0.7.19-1
- Initial version of python-netaddr package for Photon.
