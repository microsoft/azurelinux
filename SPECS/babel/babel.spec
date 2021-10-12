Summary:        An integrated collection of utilities that assist in internationalizing and localizing Python applications
Name:           babel
Version:        2.6.0
Release:        9%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://babel.pocoo.org
Source0:        https://files.pythonhosted.org/packages/be/cc/9c981b249a455fa0c76338966325fc70b7265521bad641bf2932f77712f4/Babel-%{version}.tar.gz
BuildArch:      noarch

%description
Babel is an integrated collection of utilities that assist in internationalizing and localizing Python applications,
with an emphasis on web-based applications.

%package -n     python3-babel
Summary:        An integrated collection of utilities that assist in internationalizing and localizing Python applications
BuildRequires:  python3-devel
BuildRequires:  python3-pytest
BuildRequires:  python3-pytz
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
%if %{with_check}
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
BuildRequires:  python3-attrs
BuildRequires:  python3-six
%endif
Requires:       python3
Requires:       python3-pytz

%description -n python3-babel
Babel is an integrated collection of utilities that assist in internationalizing and localizing Python applications,
with an emphasis on web-based applications.

The functionality Babel provides for internationalization (I18n) and localization (L10N) can be separated into two different aspects:
1.Tools to build and work with gettext message catalogs.
2.A Python interface to the CLDR (Common Locale Data Repository), providing access to various locale display names, localized number and date formatting, etc.

%prep
%autosetup -n Babel-%{version}

%build
%py3_build

%install
%py3_install
ln -sfv pybabel %{buildroot}/%{_bindir}/pybabel3

%check
easy_install_3=$(ls %{_bindir} |grep easy_install |grep 3)
$easy_install_3 pytest freezegun funcsigs pathlib2 pluggy utils
%{python3} setup.py test

%files -n python3-babel
%defattr(-,root,root,-)
%license LICENSE
%{_bindir}/pybabel
%{_bindir}/pybabel3
%{python3_sitelib}/*

%changelog
* Fri Oct 01 2021 Thomas Crain <thcrain@microsoft.com> - 2.6.0-9
- Add license to python3 package
- Remove python2 package
- Lint spec

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.6.0-8
- Added %%license line automatically

* Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> - 2.6.0-7
- Renaming python-pytest to pytest

* Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> - 2.6.0-6
- Renaming python-pytz to pytz

* Wed Apr 29 2020 Emre Girgin <mrgirgin@microsoft.com> - 2.6.0-5
- Renaming python-babel to babel

* Fri Apr 24 2020 Nick Samson <nisamson@microsoft.com> - 2.6.0-4
- Updated Source0, URL. Removed %%define sha1. License updated. License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 2.6.0-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue Nov 13 2018 Tapas Kundu <tkundu@vmware.com> - 2.6.0-2
- Fixed make check errors.

* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> - 2.6.0-1
- Update to version 2.6.0

* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> - 2.4.0-3
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.

* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> - 2.4.0-2
- Change python to python2 and add python2 scripts to bin directory

* Tue Apr 25 2017 Dheeraj Shetty <dheerajs@vmware.com> - 2.4.0-1
- Initial
