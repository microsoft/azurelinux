Summary:        Library for displaying tabular data in a visually appealing ASCII format
Name:           python-prettytable
Version:        3.2.0
Release:        2%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://github.com/jazzband/prettytable
Source0:        https://pypi.io/packages/source/p/prettytable/prettytable-%{version}.tar.gz
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm
%if %{with_check}
BuildRequires:  python3-pip
BuildRequires:  python3-wcwidth
%endif
BuildArch:      noarch

%description
Library for displaying tabular data in a visually appealing ASCII format

%package -n     python3-prettytable
Summary:        Library for displaying tabular data in a visually appealing ASCII format
Requires:       python3
Requires:       python3-wcwidth

%description -n python3-prettytable
PrettyTable is a simple Python library designed to make it quick and easy to
represent tabular data in visually appealing ASCII tables. It was inspired by
the ASCII tables used in the PostgreSQL shell psql. PrettyTable allows for
selection of which columns are to be printed, independent alignment of columns
(left or right justified or centred) and printing of "sub-tables" by
specifying a row range.

%prep
%autosetup -n prettytable-%{version}

%build
export SETUPTOOLS_SCM_PRETEND_VERSION=%{version}
%py3_build

%install
export SETUPTOOLS_SCM_PRETEND_VERSION=%{version}
%py3_install

%check
export SETUPTOOLS_SCM_PRETEND_VERSION=%{version}
pip3 install 'tox>=3.27.1,<4.0.0'
tox -e py%{python3_version_nodots} --sitepackages

%files -n python3-prettytable
%defattr(-,root,root,-)
%license COPYING
%{python3_sitelib}/*

%changelog
* Fri Dec 16 2022 Sam Meluch <sammeluch@microsoft.com> - 3.2.0-2
- Update version of tox used for package tests

* Thu Mar 31 2022 Olivia Crain <oliviacrain@microsoft.com> - 3.2.0-1
- Upgrade to latest upstream version
- Switch tests to tox runner
- Switch URL/Source0 links to new upstream location

* Wed Oct 20 2021 Olivia Crain <oliviacrain@microsoft.com> - 0.7.2-9
- Add license to python3 package
- Remove python2 package
- Lint spec
- License verified

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 0.7.2-8
- Added %%license line automatically

* Mon Apr 13 2020 Nick Samson <nisamson@microsoft.com> - 0.7.2-7
- Initial CBL-Mariner import from Photon (license: Apache2).
- Updated Source0, URL. Removed %%define sha1. Corrected release number. Confirmed license.

* Wed Jul 26 2017 Divya Thaluru <dthaluru@vmware.com> - 0.7.2-6
- Fixed rpm check errors

* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> - 0.7.2-5
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.

* Tue May 16 2017 Kumar Kaushik <kaushikk@vmware.com> - 0.7.2-4
- Adding python3 support.

* Mon Oct 04 2016 ChangLee <changlee@vmware.com> - 0.7.2-3
- Modified %check

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 0.7.2-2
- GA - Bump release of all rpms

* Wed Mar 04 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
- Initial packaging for Photon
