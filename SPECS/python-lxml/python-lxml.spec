%global debug_package   %{nil}

Summary:        XML and HTML with Python
Name:           python-lxml
Version:        4.9.3
Release:        1%{?dist}
# Test suite (and only the test suite) is GPLv2+
License:        BSD and GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://lxml.de
Source0:        https://github.com/lxml/lxml/releases/download/lxml-%{version}/lxml-%{version}.tar.gz
BuildRequires:  libxslt-devel
BuildRequires:  libxml2-devel
BuildRequires:  python3-Cython
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%description
The lxml XML toolkit is a Pythonic binding for the C libraries libxml2 and libxslt.

%package -n     python3-lxml
Summary:        python-lxml
Requires:       libxslt
Requires:       libxml2
Requires:       python3

%description -n python3-lxml
The lxml XML toolkit is a Pythonic binding for the C libraries libxml2 and libxslt.
It is unique in that it combines the speed and XML feature completeness of these libraries
with the simplicity of a native Python API, mostly compatible but superior to the well-known
ElementTree API.


%prep
%autosetup -n lxml-%{version}
find -type f -name "*.c" -delete -print

%build
%{py3_build "--with-cython"}

%install
%py3_install

%check
export LC_ALL=en_US.UTF-8
export LANGUAGE=en_US.UTF-8
make test

%files -n python3-lxml
%defattr(-,root,root,-)
%license LICENSES.txt
%{python3_sitelib}/*

%changelog
* Fri Nov 10 2023 Andrew Phelps <anphel@microsoft.com> - 4.9.3-1
- Upgrade to version 4.9.3

* Mon Aug 22 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 4.9.1-1
- Upgrade to to fix CVE-2022-2309

* Wed Apr 20 2022 Olivia Crain <oliviacrain@microsoft.com> - 4.8.0-1
- Upgrade to latest upstream version
- Fixes CVE-2018-19787, CVE-2020-27783, CVE-2021-28957, CVE-2021-43818

* Thu Apr 14 2022 Daniel McIlvaney <damcilva@microsoft.com> - 4.2.4-11
- Disable the debuginfo package here since it is not being built in the toolchain

* Wed Feb 16 2022 Thomas Crain <thcrain@microsoft.com> - 4.2.4-10
- Remove %%files section for main package to avoid outputting an empty RPM

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.2.4-9
- Removing the explicit %%clean stage.

* Fri Dec 03 2021 Thomas Crain <thcrain@microsoft.com> - 4.2.4-8
- Regenerate C sources at build-time to fix build break with Python 3.9

* Wed Aug 26 2020 Thomas Crain <thcrain@microsoft.com> - 4.2.4-7
- Remove python2 support.
- License verified.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 4.2.4-6
- Added %%license line automatically

* Wed Apr 29 2020 Emre Girgin <mrgirgin@microsoft.com> - 4.2.4-5
- Renaming cython to Cython

* Mon Apr 13 2020 Nick Samson <nisamson@microsoft.com> - 4.2.4-4
- Updated Source0 and URL, removed %%define sha1, License verified

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 4.2.4-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Wed Nov 28 2018 Tapas Kundu <tkundu@vmware.com> - 4.2.4-2
- Fix make check
- moved build requires from subpackage

* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> - 4.2.4-1
- Update to version 4.2.4

* Mon Aug 07 2017 Dheeraj Shetty <dheerajs@vmware.com> - 3.7.3-3
- set LC_ALL and LANGUAGE for the tests to pass

* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> - 3.7.3-2
- Use python2_sitelib

* Mon Apr 03 2017 Sarah Choi <sarahc@vmware.com> - 3.7.3-1
- Update to 3.7.3

* Wed Feb 08 2017 Xiaolin Li <xiaolinl@vmware.com> - 3.5.0b1-4
- Added python3 site-packages.

* Tue Oct 04 2016 ChangLee <changlee@vmware.com> - 3.5.0b1-3
- Modified %check

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 3.5.0b1-2
- GA - Bump release of all rpms

* Wed Oct 28 2015 Divya Thaluru <dthaluru@vmware.com> - 3.5.0b1-1
- Initial build.
