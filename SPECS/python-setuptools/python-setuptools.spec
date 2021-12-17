%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
Summary:        Download, build, install, upgrade, and uninstall Python packages
Name:           python-setuptools
Version:        40.2.0
Release:        8%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://pypi.python.org/pypi/setuptools
Source0:        https://files.pythonhosted.org/packages/ef/1d/201c13e353956a1c840f5d0fbf0461bd45bbd678ea4843ebf25924e8984c/setuptools-%{version}.zip
BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  unzip
Requires:       python2
Requires:       python2-libs
Requires:       python-xml
Provides:       python2dist(setuptools) = %{version}-%{release}
Provides:       python2.7dist(setuptools) = %{version}-%{release}
BuildArch:      noarch

%description
setuptools is a collection of enhancements to the Python distutils that allow
you to more easily build and distribute Python packages, especially ones that
have dependencies on other packages.

%prep
%setup -q -n setuptools-%{version}

%build
python2 bootstrap.py
python2 setup.py build

%install
python2 setup.py install -O1 --skip-build \
    --root %{buildroot} \
    --single-version-externally-managed
find %{buildroot}%{python2_sitelib} -name '*.exe' | xargs rm -f
find %{buildroot}%{python2_sitelib} -name '*.txt' | xargs chmod -x
chmod +x %{buildroot}%{python2_sitelib}/setuptools/command/easy_install.py

%check
python2 setup.py test

%files
%defattr(-, root, root)
%license LICENSE
%{_bindir}/*
%{python2_sitelib}/*

%changelog
* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 40.2.0-8
- Removing the explicit %%clean stage.

* Fri Mar 26 2021 Thomas Crain <thcrain@microsoft.com> - 40.2.0-7
- Merge the following releases from 1.0 to dev branch
- pawelwi@microsoft.com, 40.2.0-6: Adding explicit runtime dependency on 'python-xml'.

* Fri Jan 15 2021 Ruying Chen <v-ruyche@microsoft.com> - 40.2.0-6
- Add dist provides.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 40.2.0-5
- Added %%license line automatically

*   Tue Apr 07 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 40.2.0-4
-   Fixed "Source0" tag.
-   License verified.

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 40.2.0-3
-   Initial CBL-Mariner import from Photon (license: Apache2).

*   Thu Sep 13 2018 Tapas Kundu <tkundu@vmware.com> 40.2.0-2
-   Updated the license

*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 40.2.0-1
-   Update to version 40.2.0

*       Tue Jun 20 2017 Dheeraj Shetty <dheerajs@vmware.com> 36.0.1-1
-       Upgrade to 36.0.1 and remove the BuildRequires

*       Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 34.3.3-2
-       Use python2 explicitly and add Vendor

*       Mon Apr 03 2017 Sarah Choi <sarahc@vmware.com> 34.3.3-1
-       Upgrade to 34.3.3

*       Mon Oct 10 2016 ChangLee <changlee@vmware.com> 21.0.0-3
-       Modified %check

*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 21.0.0-2
-	GA - Bump release of all rpms

*	Wed May 4 2016 Xiaolin Li <xiaolinl@vmware.com> 21.0.0-1
-	Update setuptools to version 21.0.0

* Wed Feb 11 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
- Initial packaging for Phoa
