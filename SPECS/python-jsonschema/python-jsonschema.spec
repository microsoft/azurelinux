%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python-jsonschema
Version:        2.6.0
Release:        5%{?dist}
Summary:        An implementation of JSON Schema validation for Python
License:        MIT
Group:          Development/Languages/Python
Url:            https://pypi.python.org/pypi/jsonschema
Source0:        https://pypi.python.org/packages/source/j/jsonschema/jsonschema-%{version}.tar.gz
Vendor:         Microsoft Corporation
Distribution:   Mariner

BuildRequires: python2
BuildRequires: python2-libs
BuildRequires: python-setuptools
BuildRequires: python-vcversioner

BuildArch:      noarch

%description
jsonschema is JSON Schema validator currently based on
http://tools.ietf.org/html/draft-zyp-json-schema-03

%package -n     python3-jsonschema
Summary:        python-jsonschema
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  python3-vcversioner

%description -n python3-jsonschema

%prep
%setup -n jsonschema-%{version}
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
mv %{buildroot}/%{_bindir}/jsonschema %{buildroot}/%{_bindir}/jsonschema3
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
python2 setup.py test
pushd ../p3dir
python3 setup test
popd

%files
%defattr(-,root,root,-)
%license COPYING
%{python2_sitelib}/*
%{_bindir}/jsonschema

%files -n python3-jsonschema
%defattr(-,root,root)
%license COPYING
%{python3_sitelib}/*
%{_bindir}/jsonschema3

%changelog
*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.6.0-5
-   Added %%license line automatically
*   Wed May 06 2020 Paul Monson <paulmon@microsoft.com> 2.6.0-4
-   Restore python-vcversioner to enable build without internet access.
*   Mon Apr 13 2020 Nicolas Ontiveros <niontive@microsoft.com> 2.6.0-3
-   Don't use python-vcversioner in build.
*   Wed Apr 08 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 2.6.0-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
-   Switched "Source0" and "URL" tags to use https.
-   License verified.
*   Tue Oct 23 2018 Sujay G <gsujay@vmware.com> 2.6.0-1
-   Initial version
