# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           python-sphinxcontrib-jquery
Version:        4.1
Release: 15%{?dist}
Summary:        Extension to include jQuery on newer Sphinx releases

# The project is 0BSD
# _sphinx_javascript_frameworks_compat.js is BSD-2-Clause
# jquery-3.6.0.js and jquery.js are MIT
License:        0BSD AND BSD-2-Clause AND MIT
URL:            https://github.com/sphinx-contrib/jquery/
Source:         %{url}/archive/v%{version}/sphinxcontrib-jquery-%{version}.tar.gz

# Make the tests pass with Sphinx 7.1+
# Based on the original work in https://github.com/sphinx-contrib/jquery/pull/26
Patch:          Fix-tests-failures-with-Sphinx-7.2.patch

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pytest

%global _description %{expand:
sphinxcontrib-jquery is a Sphinx extension that ensures that jQuery
is always installed for use in Sphinx themes or extensions.}


%description %_description

%package -n     python3-sphinxcontrib-jquery
Summary:        %{summary}

%description -n python3-sphinxcontrib-jquery %_description


%prep
%autosetup -p1 -n jquery-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files 'sphinxcontrib*'


%check
%pytest


%files -n python3-sphinxcontrib-jquery -f %{pyproject_files}
%doc README.rst
%license LICENCE


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 4.1-14
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 4.1-13
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 4.1-11
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 4.1-8
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Oct 30 2023 Karolina Surma <ksurma@redhat.com> - 4.1-5
- Fix tests with Sphinx 7.2+

* Tue Aug 15 2023 Karolina Surma <ksurma@redhat.com> - 4.1-4
- Fix tests with Sphinx 7.1+

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 4.1-2
- Rebuilt for Python 3.12

* Wed Mar 29 2023 Karolina Surma <ksurma@redhat.com> - 4.1-1
- Update to 4.1
Resolves rhbz#2178260

* Mon Feb 27 2023 Karolina Surma <ksurma@redhat.com> - 3.0.0-1
- Initial package
