%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python-pyasn1
Version:        0.4.4
Release:        3%{?dist}
Summary:        Implementation of ASN.1 types and codecs in Python programming language
License:        BSD
Group:          Development/Languages/Python
Vendor:         Microsoft Corporation
Distribution:   Mariner
Url:            https://pypi.python.org/pypi/pyasn1
Source0:        https://files.pythonhosted.org/packages/10/46/059775dc8e50f722d205452bced4b3cc965d27e8c3389156acd3b1123ae3/pyasn1-%{version}.tar.gz

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools

Requires:       python2
Requires:       python2-libs

BuildArch:      noarch

%description
This is an implementation of ASN.1 types and codecs in Python programming language. It has been first written to support particular protocol (SNMP) but then generalized to be suitable for a wide range of protocols based on ASN.1 specification.

%package -n     python3-pyasn1
Summary:        python-pyasn1
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs

Requires:       python3
Requires:       python3-libs

%description -n python3-pyasn1

Python 3 version.

%prep
%setup -n pyasn1-%{version}
rm -rf ../p3dir
cp -a . ../p3dir

%build
python2 setup.py build
pushd ../p3dir
python3 setup.py build
popd

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}
pushd ../p3dir
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
popd

%check
python2 setup.py test
pushd ../p3dir
python3 setup.py test
popd

%files
%defattr(-,root,root,-)
%license LICENSE.rst
%{python2_sitelib}/*

%files -n python3-pyasn1
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 0.4.4-3
-   Added %%license line automatically.
*   Tue Apr 07 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 0.4.4-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
-   Added 'Distribution' and 'Vendor' tags.
-   Fixed "Source0" tag.
-   License verified.
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 0.4.4-1
-   Update to version 0.4.4
*   Thu Mar 23 2017 Xiaolin Li <xiaolinl@vmware.com> 0.2.3-1
-   Updated to version 0.2.3.
*   Mon Oct 04 2016 ChangLee <changlee@vmware.com> 0.1.9-3
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.1.9-2
-   GA - Bump release of all rpms
*   Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 0.1.9-1
-   Upgraded to version 0.1.9
*   Thu Aug 6 2015 Anish Swaminathan <anishs@vmware.com>
-   Added sha1sum
*   Fri Mar 13 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
-   Initial packaging for Photon
