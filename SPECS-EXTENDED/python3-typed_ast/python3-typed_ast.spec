Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global modname typed_ast

Name:               python3-%{modname}
Version:            1.5.4
Release:            1%{?dist}
Summary:            A fork of the ast module with type annotations

License:            ASL 2.0
URL:                https://github.com/python/typed_ast
Source0:            %{url}/archive/%{version}/%{modname}-%{version}.tar.gz

%{?python_provide:%python_provide python3-%{modname}}

BuildRequires:      gcc
BuildRequires:      python3-devel
BuildRequires:      python3-setuptools
BuildRequires:      python3-pytest

%description
%summary. This package is based on the ast modules from Python 2 and 3,
and has been extended with support for type comments and type annotations
as supported in Python 3.6.

%prep
%autosetup -p1 -n %{modname}-%{version}

%build
%py3_build

%install
%py3_install

%check
%py3_check_import typed_ast.ast3 typed_ast.ast27 typed_ast.conversions
%{__python3} setup.py test

%files
%doc *.md
%license LICENSE
%{python3_sitearch}/%{modname}/
%{python3_sitearch}/%{modname}-*.egg-info

%changelog
* Fri Mar 07 2025 Jyoti Kanase <v-jykanase@microsoft.com> - 1.5.4-1 
- Upgrade to 1.5.4
- License Verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.4.2-2
- Initial CBL-Mariner import from Fedora 33 (license: MIT).

* Thu Dec 31 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.4.2-1
- 1.4.2

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 1.4.1-3
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 14 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.4.1-1
- 1.4.1

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.4.0-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Sat Aug 17 2019 Miro Hrončok <mhroncok@redhat.com> - 1.4.0-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jun 11 2019 Gwyn Ciesla <gwync@protonmail.com> - 1.4.0-1
- 1.4.0.

* Wed May 15 2019 Gwyn Ciesla <gwync@protonmail.com> - 1.3.5-1
- 1.3.5.

* Tue May 14 2019 Gwyn Ciesla <gwync@protonmail.com> - 1.3.1-2
- Fix 3.8 FTBFS.

* Sat Feb 23 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.3.1-1
- Update to 1.3.1

* Thu Jan 31 2019 Gwyn Ciesla <limburgher@gmail.com> - 1.3.0-1
- 1.3.0

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-3
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Nov 07 2017 Gwyn Ciesla <limburgher@gmail.com> - 1.1.0-1
- 1.1.0

* Mon Jul 31 2017 Gwyn Ciesla <limburgher@gmail.com> - 1.0.4-1
- 1.0.4

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 11 2017 Gwyn Ciesla <limburgher@gmail.com> - 1.0.3-1
- Initial package.
