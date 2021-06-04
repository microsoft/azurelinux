%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python-jsonpatch
Version:        1.23
Release:        4%{?dist}
Summary:        Applying JSON Patches in Python
License:        BSD
Group:          Development/Languages/Python
Url:		https://pypi.python.org/pypi/jsonpatch
#Source0:       https://github.com/stefankoegl/python-json-patch/archive/v%{version}.tar.gz
Source0:        https://files.pythonhosted.org/packages/9a/7d/bcf203d81939420e1aaf7478a3efce1efb8ccb4d047a33cb85d7f96d775e/jsonpatch-%{version}.tar.gz

BuildRequires: python2
BuildRequires: python2-libs
BuildRequires: python-setuptools
BuildRequires: python-jsonpointer
Requires: python-jsonpointer

BuildArch:      noarch

%description
Library to apply JSON Patches according to RFC 6902.

%package -n     python3-jsonpatch
Summary:        python-jsonpatch
BuildRequires:  python3-devel
BuildRequires:  python3-libs

Requires:       python3-jsonpointer

%description -n python3-jsonpatch

%prep
%setup -n jsonpatch-%{version}
rm -rf ../p3dir
cp -a . ../p3dir

%build
python2 setup.py build
pushd ../p3dir
python3 setup.py build
popd

%install
pushd ../p3dir
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
popd
mv %{buildroot}/%{_bindir}/jsondiff %{buildroot}/%{_bindir}/jsondiff3
mv %{buildroot}/%{_bindir}/jsonpatch %{buildroot}/%{_bindir}/jsonpatch3
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
python2 ext_tests.py && python2 tests.py
pushd ../p3dir
python3 ext_tests.py && python3 tests.py
popd

%files
%defattr(-,root,root,-)
%license COPYING
%{python2_sitelib}/*
%{_bindir}/jsondiff
%{_bindir}/jsonpatch

%files -n python3-jsonpatch
%defattr(-,root,root)
%{python3_sitelib}/*
%{_bindir}/jsondiff3
%{_bindir}/jsonpatch3

%changelog
* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.23-4
- Added %%license line automatically

*   Tue Apr 21 2020 Eric Li <eli@microsoft.com> 1.23-3
-   Fix Source0:, Add #Source0:, and delete sha1. License Verified.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.23-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 1.23-1
-   Update to version 1.23
*       Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.15-4
-       Separate python3 and python2 specific scripts in bin directory
*       Thu Apr 27 2017 Sarah Choi <sarahc@vmware.com> 1.15-3
-       Rename jsonpatch for python3
*       Thu Apr 06 2017 Sarah Choi <sarahc@vmware.com> 1.15-2
-       support python3
*       Mon Apr 03 2017 Sarah Choi <sarahc@vmware.com> 1.15-1
-       Update to 1.15
*       Tue Oct 04 2016 ChangLee <changlee@vmware.com> 1.9-3
-       Modified %check
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.9-2
-	GA - Bump release of all rpms
* Wed Mar 04 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
- Initial packaging for Photon
