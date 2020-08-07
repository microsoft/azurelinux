%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%define debug_package %{nil}

Summary:        Distro - an OS platform information API
Name:           python-distro
Version:        1.4.0
Release:        3%{?dist}
License:        ASL
Group:          Development/Languages/Python
Vendor:         Microsoft Corporation
Distribution:   Mariner
Url:            https://pypi.python.org/pypi/distro
Source0:        https://files.pythonhosted.org/packages/ca/e3/78443d739d7efeea86cbbe0216511d29b2f5ca8dbf51a6f2898432738987/distro-%{version}.tar.gz
%define sha1    distro=d72ac60844b2b472fc815441afe60fc1da728926

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python-setuptools
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
%if %{with_check}
BuildRequires:  python-pip
%endif
Requires:       mariner-release
Requires:       python2
Requires:       python2-libs
BuildArch:      noarch

%description
Distro provides information about the OS distribution it runs on, such as a reliable machine-readable ID, or version information.

%package -n     python3-distro
Summary:        python-distro
Requires:       python3
Requires:       python3-libs
Requires:       mariner-release

%description -n python3-distro
Python 3 version.

%prep
%setup -q -n distro-%{version}

%build
python2 setup.py build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
pip install tox
tox

%files
%defattr(-,root,root,-)
%{python2_sitelib}/*
%doc CHANGELOG.md CONTRIBUTORS.md README.md
%license LICENSE
/usr/bin/*

%files -n python3-distro
%defattr(-,root,root,-)
%{python3_sitelib}/*
/usr/bin/*
%doc CHANGELOG.md CONTRIBUTORS.md README.md
%license LICENSE

%changelog
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.4.0-3
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Thu Jul 11 2019 Tapas Kundu <tkundu@vmware.com> 1.4.0-2
-   Updated to build python2 distro pkg.
-   Separated spec file for python3-distro.
*   Tue Feb 12 2019 Tapas Kundu <tkundu@vmware.com> 1.4.0-1
-   Initial packaging for Photon
