%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        A tool to check your Python code
Name:           python-pycodestyle
Version:        2.5.0
Release:        4%{?dist}
Url:            https://pypi.org/project/pycodestyle/
License:        MIT
Group:          Development/Languages/Python
Vendor:         Microsoft Corporation
Distribution:   Mariner
#Source0:       https://files.pythonhosted.org/packages/1c/d1/41294da5915f4cae7f4b388cea6c2cd0d6cd53039788635f6875dfe8c72f/pycodestyle-2.5.0.tar.gz
Source0:        %{name}-%{version}.tar.gz
%define sha1    %{name}=8d25df191e57d6602bc8ccaf6f6d4f84181301d6

BuildArch:      noarch

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python2
Requires:       python2-libs

%description
pycodestyle is a tool to check your Python code against some of the style conventions in PEP 8.

%package -n     python3-pycodestyle
Summary:        python-pycodestyle
Requires:       python3
Requires:       python3-libs

%description -n python3-pycodestyle

Python 3 version.

%prep
%setup -q -n pycodestyle-%{version}
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
%defattr(-,root,root)
%license LICENSE
%{python2_sitelib}/*

%files -n python3-pycodestyle
%defattr(-,root,root,-)
%{python3_sitelib}/*
%{_bindir}/pycodestyle

%changelog
* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 2.5.0-4
- Added %%license line automatically
* Tue Apr 07 2020 Paul Monson <paulmon@microsoft.com> 2.5.0-3
- Add #Source0. License verified.
* Wed Sep 25 2019 Saravanan Somasundaram <sarsoma@microsoft.com> 2.5.0-2
- Initial CBL-Mariner import from Photon (license: Apache2).
* Tue Jun 04 2019 Ankit Jain <ankitja@vmware.com> 2.5.0-1
- Initial packaging for Photon