%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
Summary:        The PyPA recommended tool for installing Python packages.
Name:           python-pip
Version:        19.2
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://pypi.python.org/pypi/pip
Source0:        https://files.pythonhosted.org/packages/41/13/b6e68eae78405af6e4e9a93319ae5bb371057786f1590b157341f7542d7d/pip-19.2.tar.gz
# To get tests:
# git clone https://github.com/pypa/pip && cd pip
# git checkout 19.2 && tar -czvf ../pip-tests-19.2.tar.gz tests/
Source1:        pip-tests-%{version}.tar.gz
BuildRequires:  python-setuptools
BuildRequires:  python2
BuildRequires:  python2-libs
Requires:       python-setuptools
Requires:       python-xml
Requires:       python2
Requires:       python2-libs
BuildArch:      noarch
%if %{with_check}
BuildRequires:  PyYAML
BuildRequires:  curl-devel
BuildRequires:  mercurial
BuildRequires:  openssl-devel
BuildRequires:  python-xml
%endif

%description
The PyPA recommended tool for installing Python packages.

%prep
%setup -q -n pip-%{version}
tar -xf %{SOURCE1}

%build
python2 setup.py build

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
easy_install_2=$(ls %{_bindir} |grep easy_install |grep 2)
$easy_install_2 freezegun mock pretend virtualenv scripttest pytest pytest-capturelog

python setup.py test


%files
%defattr(-,root,root)
%license LICENSE.txt
%{python2_sitelib}/*
%{_bindir}/*

%changelog
*   Tue Dec 22 2020 Rachel Menge <rachelmenge@microsoft.com> - 19.2-1
-   Update to version 19.2 to fix CVE-2019-20916

*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 18.0-5
-   Added %%license line automatically

*   Wed Apr 08 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 18.0-4
-   Fixed "Source0" tag.
-   License verified.
-   Removed "%%define sha1".

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 18.0-3
-   Initial CBL-Mariner import from Photon (license: Apache2).

*   Mon Jan 14 2019 Tapas Kundu <tkundu@vmware.com> 18.0-2
-   Fix make check

*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 18.0-1
-   Update to version 18.0

*   Thu Jul 20 2017 Divya Thaluru <dthaluru@vmware.com> 9.0.1-6
-   Fixed make check errors

*   Thu Jun 15 2017 Dheeraj Shetty <dheerajs@vmware.com> 9.0.1-5
-   Use python2 explicitly

*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 9.0.1-4
-   Add python-xml to requires.

*   Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 9.0.1-3
-   Fix arch

*   Tue Apr 11 2017 Xiaolin Li <xiaolinl@vmware.com> 9.0.1-2
-   Added python-setuptools to requires.

*   Thu Mar 30 2017 Sarah Choi <sarahc@vmware.com> 9.0.1-1
-   Upgrade version to 9.0.1

*   Fri Sep 2 2016 Xiaolin Li <xiaolinl@vmware.com> 8.1.2-1
-   Initial packaging for Photon
