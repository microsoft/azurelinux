%global srcname templated-dictionary
%global python3_pkgversion 3

%if 0%{?rhel} == 7
%global python3_pkgversion 36
%endif

Name:          python-%{srcname}
Version:       1.6
Release:       1%{?dist}
Vendor:        Microsoft Corporation
Distribution:  Azure Linux
Summary:       Dictionary with Jinja2 expansion

License:       GPL-2.0-or-later
URL:           https://github.com/xsuchy/templated-dictionary
Source0:       %{url}/archive/refs/tags/%{name}-%{version}-1.tar.gz#/%{name}-%{version}.tar.gz

BuildArch:     noarch

%if 0%{?rhel} > 10 || 0%{?fedora} > 42
BuildRequires: python%{python3_pkgversion}-devel
%else
BuildRequires: python%{python3_pkgversion}-devel
BuildRequires: python%{python3_pkgversion}-setuptools
%endif
Requires:      python%{python3_pkgversion}-jinja2

%global _description\
Dictionary where __getitem__() is run through Jinja2 template.

%description %_description


%package -n python3-%{srcname}
Summary: %{summary}
%{?py_provides:%py_provides python3-%{srcname}}
%description -n python3-%{srcname} %_description


%if 0%{?rhel} > 10 || 0%{?fedora} > 42
%generate_buildrequires
%pyproject_buildrequires
%endif

%prep
%setup -q -n %{srcname}-%{name}-%{version}-1


%build
%if 0%{?rhel} > 10 || 0%{?fedora} > 42
version="%version" %pyproject_wheel
%else
version="%version" %py3_build
%endif

%install
%if 0%{?rhel} > 10 || 0%{?fedora} > 42
version=%version %pyproject_install
%else
version=%version %py3_install
%endif


%files -n python3-%{srcname}
%license LICENSE
%{python3_sitelib}/templated_dictionary/
%if 0%{?rhel} > 10 || 0%{?fedora} > 42
%{python3_sitelib}/*.dist-info
%else
%{python3_sitelib}/templated_dictionary-*.egg-info/
%endif

%changelog
* Thu May 14 2026 Sandeep Karambelkar <skarambelkar@microsoft.com> - 1.6-1
- Upgraded to 1.6 and sync'd with Fedora spec.

* Wed Aug 28 2024 Reuben Olinsky <reubeno@microsoft.com> - 1.4-1
- Upgraded to 1.4 and sync'd with Fedora spec.

* Fri Apr 29 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1-6
- Fixing source URL.

* Tue Feb 08 2022 Cameron Baird <cameronbaird@microsoft.com> - 1.1-5
- Initial CBL-Mariner import from Fedora 33 (license: MIT).
- License verified

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.1-3
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Dec 09 2020 Miroslav Suchý <msuchy@redhat.com> 1.1-1
- require python3- variants and more specifis files section
- remove python2 support

* Wed Nov 18 2020 Miroslav Suchý <msuchy@redhat.com> 1.0-1
- new package
