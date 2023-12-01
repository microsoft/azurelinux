Summary:        Markdown to reStructuredText converter.
Name:           python-m2r
Version:        0.2.1
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://pypi.python.org/pypi/m2r
Source0:        https://github.com/miyakogi/m2r/archive/v%{version}/m2r-%{version}.tar.gz
BuildRequires:  python3-devel
BuildRequires:  python3-docutils
BuildRequires:  python3-mistune
BuildRequires:  python3-setuptools
%if %{with_check}
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
BuildRequires:  python3-pygments
%endif
BuildArch:      noarch

%description
M2R converts a markdown file including reST markups to a valid reST format.

%package -n     python3-m2r
Summary:        Markdown to reStructuredText converter.

Requires:       python3
Requires:       python3-docutils
Requires:       python3-mistune


%description -n python3-m2r
M2R converts a markdown file including reST markups to a valid reST format.

%prep
%autosetup -n m2r-%{version}

%build
%py3_build

%install
%py3_install
ln -s m2r %{buildroot}/%{_bindir}/m2r3

%check
pip3 install mock
%python3 setup.py test -s tests

%files -n python3-m2r
%defattr(-,root,root)
%license LICENSE
%{_bindir}/m2r
%{_bindir}/m2r3
%{python3_sitelib}/*

%changelog
* Mon Feb 07 2022 Olivia Crain <oliviacrain@microsoft.com> - 0.2.1-1
- Upgrade to latest upstream version

* Fri Dec 03 2021 Olivia Crain <oliviacrain@microsoft.com> - 0.2.0-7
- Replace easy_install usage with pip in %%check sections

* Wed Oct 20 2021 Olivia Crain <oliviacrain@microsoft.com> - 0.2.0-6
- Add license to python3 package
- Remove python2 package
- Lint spec
- License verified

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 0.2.0-5
- Added %%license line automatically

* Wed Apr 29 2020 Emre Girgin <mrgirgin@microsoft.com> - 0.2.0-4
- Renaming python-Pygments to python-pygments

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 0.2.0-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Mon Nov 26 2018 Tapas Kundu <tkundu@vmware.com> - 0.2.0-2
- Fix makecheck
- Removed buildrequires from subpackage

* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> - 0.2.0-1
- Update to version 0.2.0

* Fri Jul 21 2017 Divya Thaluru <dthaluru@vmware.com> - 0.1.7-1
- Updated version to 0.1.7
- Fixed make check errors

* Mon Jun 19 2017 Xiaolin Li <xiaolinl@vmware.com> - 0.1.5-3
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.

* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> - 0.1.5-2
- Separate the python2 and python3 scripts in the bin directory

* Mon Mar 20 2017 Xiaolin Li <xiaolinl@vmware.com> - 0.1.5-1
- Initial packaging for Photon
