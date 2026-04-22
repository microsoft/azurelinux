# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global         srcname         diskcache
%global         forgeurl        https://github.com/grantjenks/python-diskcache
Version:        5.6.3
%global         tag             v%{version}
%forgemeta

Name:           python-%{srcname}
Release: 12%{?dist}
Summary:        Python disk-backed cache

License:        Apache-2.0
URL:            https://grantjenks.com/docs/diskcache/
# Pypi version does not have tests
Source0:        %{forgesource}


BuildRequires:  python3-devel
BuildRequires:  python3-tox

BuildArch: noarch

%global _description %{expand:
DiskCache is an Apache2 licensed disk and file backed cache library,
written in pure-Python, and compatible with Django.}

%description %_description

%package -n python3-%{srcname}
Summary:        %{summary}

%description -n python3-%{srcname} %_description


%prep
%forgesetup
# Relax test version requirement
sed -i 's/==4.2.*//g' requirements-dev.txt
sed -i 's/==4.2.*//g' tox.ini

%generate_buildrequires
%pyproject_buildrequires -e %{toxenv}

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{srcname}

%check
%tox -e py

%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.rst
 
%changelog
* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 5.6.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 5.6.3-10
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 5.6.3-9
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.6.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jun 26 2025 Python Maint <python-maint@redhat.com> - 5.6.3-7
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.6.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.6.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 5.6.3-4
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.6.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Sep 08 2023 Benson Muite <benson_muite@emailplus.org> - 5.6.3-1
- Update to new release 5.6.3

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jun 30 2023 Python Maint <python-maint@redhat.com> - 5.6.1-2
- Rebuilt for Python 3.12

* Thu Jun 29 2023 Benson Muite <benson_muite@emailplus.org> - 5.6.1-1
- Unretire package

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Jan 23 2021 Fabian Affolter <mail@fabian-affolter.ch> - 5.2.1-1
- Update to latest upstream release 5.2.1

* Sun Dec 06 2020 Fabian Affolter <mail@fabian-affolter.ch> - 5.1.0-1
- Update to latest upstream release 5.1.0

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro HronÄ¨ok <mhroncok@redhat.com> - 4.1.0-3
- Rebuilt for Python 3.9

* Sun Jan 26 2020 Fabian Affolter <mail@fabian-affolter.ch> - 4.1.0-2
- Address issues (#1795068)

* Sun Jan 26 2020 Fabian Affolter <mail@fabian-affolter.ch> - 4.1.0-1
- Initial package
