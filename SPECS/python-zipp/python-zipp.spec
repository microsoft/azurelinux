%global pypi_name zipp

Summary:        Backport of pathlib-compatible object wrapper for zip files
Name:           python-%{pypi_name}
Version:        3.17.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/jaraco/zipp
Source0:        %{pypi_source}

BuildArch:      noarch

BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-wheel

%if 0%{?with_check}
BuildRequires:  python3-atomicwrites
BuildRequires:  python3-attrs
BuildRequires:  python3-docutils
BuildRequires:  python3-pluggy
BuildRequires:  python3-pygments
BuildRequires:  python3-six
BuildRequires:  python3dist(pytest)
%endif

%description
A pathlib-compatible Zipfile object wrapper. A backport of the Path object.

%package -n     python3-%{pypi_name}
Summary:        %{summary}

%description -n python3-%{pypi_name}
A pathlib-compatible Zipfile object wrapper. A backport of the Path object.

%prep
%autosetup -n %{pypi_name}-%{version}

%generate_buildrequires
%pyproject_buildrequires -r

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{pypi_name}

%check
pip3 install more-itertools iniconfig jaraco.itertools jaraco.functools
rm -rf .pyproject-builddir

%pytest

%files -n python3-%{pypi_name} -f %{pyproject_files}
%license LICENSE
%doc README.rst

%changelog
* Wed Feb 14 2024 Rohit Rawat <rohitrawat@microsoft.com> - 3.17.0-1
- Upgrade to 3.17.0

* Fri Apr 08 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.8.0-2
- Initial CBL-Mariner import from Fedora 35 (license: MIT).
- Cleaning-up spec. License verified.

* Mon Apr 04 2022 Lumír Balhar <lbalhar@redhat.com> - 3.8.0-1
- Update to 3.8.0
Resolves: rhbz#2071401

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Jan 03 2022 Lumír Balhar <lbalhar@redhat.com> - 3.7.0-1
- Update to 3.7.0
Resolves: rhbz#2036287

* Tue Oct 05 2021 Lumír Balhar <lbalhar@redhat.com> - 3.6.0-1
- Update to 3.6.0
Resolves: rhbz#2008627

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 07 2021 Lumír Balhar <lbalhar@redhat.com> - 3.5.0-1
- Update to 3.5.0
Resolves: rhbz#1978839

* Wed Jun 30 2021 Lumír Balhar <lbalhar@redhat.com> - 3.4.1-1
- Unretired package with new upstream version

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.5.1-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jun 26 2019 Miro Hrončok <mhroncok@redhat.com> - 0.5.1-1
- Initial package
