Vendor:         Microsoft Corporation
Distribution:   Mariner
%global srcname podman
%global pkgsuf podman-api

# https://github.com/containers/python-podman
%global git https://github.com/containers/python-%{srcname}
%global commit d4b8263bf08b72082cfb45e7367ebf4309facc54
%global shortcommit %(c=%{commit}; echo ${c:0:7})

# Several tests require internet conection or journald to be running
# Let's disable checking for now
%global with_tests 0


# We name the package python-podman-api since there is an upstream intent to
# move to this namespace
Name: python-%{pkgsuf}
# See https://github.com/containers/python-podman/issues/27
Version: 0.0.0
Release: 2%{?dist}
Summary: Python bindings for using Varlink access to Podman Service

License: ASL 2.0
URL: %{git}
Source0: %{git}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz

BuildArch: noarch

%description 
%{summary}

%package -n python3-%{pkgsuf}
Summary: %{summary}
BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-pbr
%if 0%{?with_tests}
BuildRequires: podman
BuildRequires: python3-psutil
BuildRequires: python3-dateutil
BuildRequires: python3-varlink
%endif
%{?python_provide:%python_provide python3-%{pkgsuf}}

# See https://bugzilla.redhat.com/show_bug.cgi?id=1720577
Provides: python3-podman = %{version}-%{release}

%description -n python3-%{pkgsuf}
%{summary}

%prep
%setup -q -n python-%{srcname}-%{commit}

%if 0%{?with_tests}
# skip (am I root?) user check
sed -i 's/exit 2/echo/' test/test_runner.sh
%endif

# Fix example shebangs
sed -i '1 s|/usr/bin/env python3|/usr/bin/python3|' examples/*.py

%build
export PBR_VERSION="0.0.0"
%py3_build

%install
export PBR_VERSION="0.0.0"
%py3_install

%check
%if 0%{?with_tests}
/usr/bin/bash test/test_runner.sh
%endif

%files -n python3-%{pkgsuf}
%license LICENSE
%doc README.md examples CHANGES.txt
%{python3_sitelib}/%{srcname}/
%{python3_sitelib}/%{srcname}-*.egg-info/

%changelog
* Fri Feb 04 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.0.0-2
- Removing epoch.
- License verified.

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.0.0-1
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Sun Jun 14 2020 Athos Ribeiro <athoscr@fedoraproject.org> - 0.0.0-0.7.20200614gitd4b8263
- Update revision
- BZ1775437

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.0.0-0.6.20190613gitd0a45fe
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.0-0.5.20190613gitd0a45fe
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.0.0-0.4.20190613gitd0a45fe
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.0.0-0.3.20190613gitd0a45fe
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.0-0.2.20190613gitd0a45fe
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jun 13 2019 Athos Ribeiro <athoscr@fedoraproject.org> - 0.0.0-0.1.20190613gitd0a45fe
- Initial package

