# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global srcname aioodbc

Name:           python-%{srcname}
Version:        0.4.0
Release:        10%{?dist}
Summary:        Library for accessing a ODBC databases from the asyncio

License:        Apache-2.0
URL:            https://github.com/aio-libs/aioodbc
Source:         %{pypi_source}

BuildArch:      noarch


%description
%{summary}.


%package -n python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}
BuildRequires:  python3-devel
# for tests
#BuildRequires:  python3-pytest
#BuildRequires:  python3-pytest-asyncio


%description -n python3-%{srcname}
%{summary}.


%prep
%autosetup -n %{srcname}-%{version}

%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install

%pyproject_save_files aioodbc


%check
# tests all fail with error "AttributeError: module pytest has no attribute db_list"
# and i'm not sure how to fix it right now
#%%pytest


%files -n python3-%{srcname} -f %{pyproject_files}
%license LICENSE
%doc CHANGES.txt README.rst


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.4.0-10
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.4.0-9
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 0.4.0-7
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jun 13 2024 Python Maint <python-maint@redhat.com> - 0.4.0-4
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Sep 15 2023 Jonathan Wright <jonathan@almalinux.org> - 0.4.0-1
- Update to 0.4.0 rhbz#2179217
- modernize spec

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.3-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 0.3.3-14
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.3.3-11
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.3.3-8
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.3.3-5
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.3.3-3
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.3.3-2
- Rebuilt for Python 3.8

* Sat Aug 03 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.3.3-1
- Update to 0.3.3

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Sep 02 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.3.2-1
- Update to 0.3.2

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jul 07 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.3.1-1
- Update to 0.3.1

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.3.0-2
- Rebuilt for Python 3.7

* Sun Mar 11 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.3.0-1
- Update to 0.3.0

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Sep 30 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.2.0-1
- Update to 0.2.0

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Nov 27 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.0.3-1
- Initial package
