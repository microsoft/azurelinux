%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%define debug_package %{nil}

Summary:        Distro - an OS platform information API
Name:           python-distro
Version:        1.6.0
Release:        2%{?dist}
License:        ASL
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://pypi.python.org/pypi/distro
Source0:        https://github.com/nir0s/distro/archive/v%{version}.tar.gz#/distro-%{version}-github.tar.gz

BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
%if %{with_check}
BuildRequires:  python3-pip
%endif

BuildArch:      noarch

%description
Distro provides information about the OS distribution it runs on, such as a reliable machine-readable ID, or version information.

%package -n     python3-distro
Summary:        python-distro

Requires:       mariner-release
Requires:       python3
Requires:       python3-libs

Obsoletes:      %{name} <= 1.4.0-4
Provides:       %{name} = %{version}-%{release}

%description -n python3-distro
Python 3 version.

%prep
%setup -q -n distro-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
# Disabled tests:
# - 'py27' - depends on Python 2, CBL-Mariner doesn't support that anymore.
# - 'lint' - new test added in version 1.6.0, depends on 'pre-commit', which is not provided by CBL-Mariner.
sed -i -E "s/(lint|py27), //g" tox.ini
sed -i -E "/.*testenv:lint/Q" tox.ini

pip3 install tox
tox

%files -n python3-distro
%defattr(-,root,root,-)
%{python3_sitelib}/*
%{_bindir}/*
%doc CHANGELOG.md CONTRIBUTORS.md README.md
%license LICENSE

%changelog
* Mon Oct 25 2021 Pawel Winogrodzki <pawel.winogrodzki@microsoft.com> - 1.6.0-2
- Disabling tests we cannot run from the '%%check' section.

* Mon Oct 25 2021 Pawel Winogrodzki <pawel.winogrodzki@microsoft.com> - 1.6.0-1
- Updated to version 1.6.0 to make tests work with Python 3.7.
- Removing Python 2 version.

* Fri Feb 26 2021 Andrew Phelps <anphel@microsoft.com> - 1.4.0-4
- Use github source to fix check tests.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 1.4.0-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Thu Jul 11 2019 Tapas Kundu <tkundu@vmware.com> - 1.4.0-2
- Updated to build python2 distro pkg.
- Separated spec file for python3-distro.

* Tue Feb 12 2019 Tapas Kundu <tkundu@vmware.com> - 1.4.0-1
- Initial packaging for Photon
