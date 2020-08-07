%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%define LICENSE_PATH COPYING

Name:           python-vcversioner
Version:        2.16.0.0
Release:        4%{?dist}
Summary:        Python version extractor
License:        ISC
Group:          Development/Languages/Python
Url:            https://github.com/habnabit/vcversioner

# Using the pypi tarball because building this rpm doesn't work with tarball from github.
#Source0:       https://pypi.python.org/packages/source/v/vcversioner/vcversioner-2.16.0.0.tar.gz
Source0:        vcversioner-%{version}.tar.gz
Source1:        https://raw.githubusercontent.com/habnabit/vcversioner/%{version}/%{LICENSE_PATH}

BuildRequires:  python2
BuildRequires:  python-setuptools

BuildArch:      noarch

%description
Elevator pitch: you can write a setup.py with no version information specified, and vcversioner will find a recent, properly-formatted VCS tag and extract a version from it.

%package -n     python3-vcversioner
Summary:        python3-vcversioner
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml

%description -n python3-vcversioner
Python 3 version.

%prep
%setup -q -n vcversioner-%{version}
rm -rf ../p3dir
cp -a . ../p3dir
cp %{SOURCE1} .

%build
python2 setup.py build
pushd ../p3dir
python3 setup.py build
popd

%install
pushd ../p3dir
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
popd
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
python2 setup.py test
pushd ../p3dir
python3 setup test
popd

%files
%license %{LICENSE_PATH}
%defattr(-,root,root,-)
%{python2_sitelib}/*

%files -n python3-vcversioner
%license %{LICENSE_PATH}
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
*   Fri May 29 2020 Mateusz Malisz <mamalisz@microsoft.com> 2.16.0.0-4
-   Add quiet option to setup.
-   Add %%license macro.
-   Add COPYING file.

*   Wed May 06 2020 Paul Monson <paulmon@microsoft.com> 2.16.0.0-3
-   Restore vcversioner
-   Url verified.
-   License verified.
-   Fix Source0.

*   Thu Aug 08 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.16.0.0-2
-   Initial CBL-Mariner import from Photon (license: Apache2).

*   Tue Oct 23 2018 Sujay G <gsujay@vmware.com> 2.16.0.0-1
-   Initial version
