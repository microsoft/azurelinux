%define debug_package %{nil}
Summary:        Distro - an OS platform information API
Name:           python-distro
Version:        1.9.0
Release:        1%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Languages/Python
URL:            https://distro.readthedocs.io/en/latest/
Source0:        https://github.com/python-distro/distro/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if %{with_check}
BuildRequires:  python3-pip
%endif
BuildArch:      noarch

%description
Distro provides information about the OS distribution it runs on, such as a reliable machine-readable ID, or version information.

%package -n     python3-distro
Summary:        Distro - an OS platform information API
Requires:       azurelinux-release
Requires:       python3

%description -n python3-distro
Distro provides information about the OS distribution it runs on, such as a reliable machine-readable ID, or version information.

%prep
%autosetup -n distro-%{version}

%build
make build

%install
make install

%check
make test
# pip3 install pytest
# export LANG=C.UTF-8
# %pytest

%files -n python3-distro
%defattr(-,root,root,-)
%doc CHANGELOG.md CONTRIBUTORS.md README.md
%license LICENSE
%{python3_sitelib}/*
%{_bindir}/*

%changelog
* Mon Feb 12 2024 Osama Esmail <osamaesmail@microsoft.com> - 1.9.0-1
- Update versions for 3.0 release
- Update source URL

* Wed Feb 07 2024 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 1.6.0-3
- Update the runtime dependency from mariner-release to azurelinux-release

* Wed Feb 09 2022 Muhammad Falak <mwani@microsoft.com> - 1.6.0-2
- Use `%pytest` instead of `tox` to enable ptest

* Mon Jan 24 2022 Thomas Crain <thcrain@microsoft.com> - 1.6.0-1
- Upgrade to latest upstream version

* Wed Oct 20 2021 Thomas Crain <thcrain@microsoft.com> - 1.4.0-5
- Add license to python3 package
- Remove python2 package
- Lint spec
- License verified (clarified ASL version in tag)

* Fri Feb 26 2021 Andrew Phelps <anphel@microsoft.com> - 1.4.0-4
- Use github source to fix check tests.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 1.4.0-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Thu Jul 11 2019 Tapas Kundu <tkundu@vmware.com> - 1.4.0-2
- Updated to build python2 distro pkg.
- Separated spec file for python3-distro.

* Tue Feb 12 2019 Tapas Kundu <tkundu@vmware.com> - 1.4.0-1
- Initial packaging for Photon
