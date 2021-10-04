%define debug_package %{nil}
Summary:        Distro - an OS platform information API
Name:           python-distro
Version:        1.4.0
Release:        5%{?dist}
License:        ASL
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://pypi.python.org/pypi/distro
#Source0:       https://github.com/nir0s/distro/archive/v%{version}.tar.gz
Source0:        distro-%{version}-github.tar.gz

%description
Distro provides information about the OS distribution it runs on, such as a reliable machine-readable ID, or version information.

%package -n     python3-distro
Summary:        Distro - an OS platform information API
BuildRequires:  python3
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       mariner-release
Requires:       python3
Requires:       python3-libs
%if %{with_check}
BuildRequires:  python3-pip
%endif

%description -n python3-distro
Distro provides information about the OS distribution it runs on, such as a reliable machine-readable ID, or version information.

%prep
%autosetup -n distro-%{version}

%build
%py3_build

%install
%py3_install

%check
pip3 install tox
tox

%files -n python3-distro
%defattr(-,root,root,-)
%doc CHANGELOG.md CONTRIBUTORS.md README.md
%license LICENSE
%{python3_sitelib}/*
%{bindir}/*

%changelog
* Fri Oct 01 2021 Thomas Crain <thcrain@microsoft.com> - 1.4.0-5
- Add license to python3 package
- Remove python2 package
- Lint spec

* Fri Feb 26 2021 Andrew Phelps <anphel@microsoft.com> - 1.4.0-4
- Use github source to fix check tests.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 1.4.0-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Thu Jul 11 2019 Tapas Kundu <tkundu@vmware.com> - 1.4.0-2
- Updated to build python2 distro pkg.
- Separated spec file for python3-distro.

* Tue Feb 12 2019 Tapas Kundu <tkundu@vmware.com> - 1.4.0-1
- Initial packaging for Photon
