# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pypi_name pytest_mock
%global package_name pytest-mock
%global file_name pytest_mock

Name:           python-%{package_name}
Version:        3.14.1
Release: 5%{?dist}
Summary:        Thin-wrapper around the mock package for easier use with py.test

License:        MIT
URL:            https://github.com/pytest-dev/pytest-mock/
Source0:        %{pypi_source}

BuildArch:      noarch

%description
This plugin installs a mocker fixture which is a thin-wrapper around the
patching API provided by the mock package, but with the benefit of not having
to worry about undoing patches at the end of a test.

%package -n     python3-%{package_name}
Summary:        %{summary}

BuildRequires:  python3-devel
BuildRequires:  %py3_dist setuptools
BuildRequires:  %py3_dist pytest
BuildRequires:  %py3_dist setuptools_scm
%if %{undefined rhel}
BuildRequires:  %py3_dist pytest-asyncio
%endif

%description -n python3-%{package_name}
This plugin installs a mocker fixture which is a thin-wrapper around the
patching API provided by the mock package, but with the benefit of not having
to worry about undoing patches at the end of a test.

%prep
%autosetup -n %{file_name}-%{version} -p1
# Correct end of line encoding for README
sed -i 's/\r$//' README.rst

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l %{file_name}

%check
%pyproject_check_import

%pytest -v tests \
  -k "not test_standalone_mock and not test_detailed_introspection and not test_detailed_introspection \
  and not test_assert_called_args_with_introspection and not test_assert_called_kwargs_with_introspection \
  and not test_plain_stopall and not test_used_with_class_scope and not est_used_with_module_scope \
  and not test_used_with_package_scope and not test_used_with_session_scope \
  %{?rhel:and not test_instance_async_method_spy}"

%files -n python3-%{package_name} -f %{pyproject_files}
%doc CHANGELOG.rst README.rst
%license LICENSE

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 3.14.1-4
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 3.14.1-3
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.14.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jul 11 2025 Julien Enselme <jujens@jujens.eu> - 3.14.1-1
- Update to 3.14.1
- Add support for Python 3.14

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 3.14.0-4
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.14.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.14.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 15 2024 Julien Enselme - 3.14.0-1
- Update to 3.14.0

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 3.12.0-5
- Rebuilt for Python 3.13

* Thu Feb 08 2024 Julien Enselme <jujens@jujens.eu> - 3.12.0-4
- Bump version after adding patch to fix tests.

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Oct 21 2023 Julien Enselme <jujens@jujens.eu> - 3.12.0-1
- Update to 3.12.0

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.11.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 04 2023 Python Maint <python-maint@redhat.com> - 3.11.1-2
- Rebuilt for Python 3.12

* Tue Jul 04 2023 Julien Enselme <jujens@jujens.eu> - 3.11.1
- Update to 3.11.1

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 3.10.0-3
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Nov 01 2022 Lumír Balhar <lbalhar@redhat.com> - 3.10.0-1
- Update to 3.10.0
Resolves: rhbz#2132453

* Wed Sep 28 2022 Fabian Affolter <mail@fabian-affolter.ch> - 3.9.0-1
- Update to latest upstream release 3.9.0 (closes rhbz#2130519)

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 06 2022 Julien Enselme <jujens@jujens.eu> - 3.8.2-1
- Update to 3.8.2

* Wed Jun 29 2022 Julien Enselme <jujens@jujens.eu> - 3.8.1-1
- Update to 3.8.1

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 3.7.0-2
- Rebuilt for Python 3.11

* Wed Feb 23 2022 Fabian Affolter <mail@fabian-affolter.ch> - 3.7.0-1
- Update to latest upstream release 3.7.0 (closes rhbz#2047739)

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Jul 26 2021 Carl George <carl@george.computer> - 3.6.1-1
- Latest upstream
- Resolves: rhbz#1953232

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 03 2021 Python Maint <python-maint@redhat.com> - 3.5.1-3
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 11 2021 Fabian Affolter <mail@fabian-affolter.ch> - 3.5.1-1
- Update to new upstream release 3.5.1 (#1912592)

* Tue Jan 05 2021 Fabian Affolter <mail@fabian-affolter.ch> - 3.5.0-1
- Update to new upstream release 3.5.0 (#1912592)

* Wed Dec 16 2020 Fabian Affolter <mail@fabian-affolter.ch> - 3.4.0-1
- Update macros
- Update to new upstream release 3.4.0 (#1907878)

* Fri Aug 21 2020 Fabian Affolter <mail@fabian-affolter.ch> - 3.3.0-1
- Update to latest upstream release 3.3.0 (rhbz#1871290)

* Fri Aug 21 2020 Fabian Affolter <mail@fabian-affolter.ch> - 3.2.0-1
- Update to latest upstream release 3.2.0 (rhbz#1756646)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri May 29 2020 Miro Hrončok <mhroncok@redhat.com> - 1.10.4-9
- Drop manual requires on python3-pytest to support usage with pytest4 compat package

* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 1.10.4-8
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Oct 01 2019 Miro Hrončok <mhroncok@redhat.com> - 1.10.4-6
- Subpackage python2-pytest-mock has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Aug 17 2019 Miro Hrončok <mhroncok@redhat.com> - 1.10.4-5
- Rebuilt for Python 3.8

* Thu Aug 01 2019 Julien Enselme <jujens@jujens.eu> - 1.10.4-4
- Fix build issues with python 3.8 and mock 3.0

* Tue Jul 30 2019 Julien Enselme <jujens@jujens.eu> - 1.10.4-3
- Fix build issues with pytest 4.6.3

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Jul 13 2019 Julien Enselme <jujens@jujens.eu> - 1.10.4-1
- Update to 1.10.4

* Thu Apr 04 2019 Miro Hrončok <mhroncok@redhat.com> - 1.10.3-1
- Update to 1.10.3

* Sat Feb 23 2019 Julien Enselme <jujens@jujens.eu> - 1.10.1-1
- Update to 1.10.1

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 18 2018 Miro Hrončok <mhroncok@redhat.com> - 1.10.0-2
- Rebuilt for Python 3.7

* Mon May 07 2018 Julien Enselme <jujens@jujens.eu> - 1.10.0-1
- Update to 1.10.0

* Sun Apr 15 2018 Julien Enselme <jujens@jujens.eu> - 1.9.0-1
- Update to 1.9.0

* Thu Mar 01 2018 Julien Enselme <jujens@jujens.eu> - 1.7.1-1
- Update to 1.7.1

* Mon Feb 19 2018 Julien Enselme <jujens@jujesn.eu> - 1.7.0-1
- Update to 1.7.0

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Sep 16 2017 Julien Enselme <jujens@jujens.eu> - 1.6.3-1
- Update to 1.6.3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jul 23 2017 Julien Enselme <jujens@jujens.eu> - 1.6.2-1
- Update to 1.6.2

* Wed Apr 05 2017 Julien Enselme <jujens@jujens.eu> - 1.6.0-2
- Add missing BR

* Wed Apr 05 2017 Julien Enselme <jujens@jujens.eu> - 1.6.0-1
- Update to 1.6.0

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.2-3
- Rebuild for Python 3.6

* Sat Oct 01 2016 Julien Enselme <jujens@jujens.eu> - 1.2-2
- Add patch to fix tests with pytest3

* Sun Sep 18 2016 Julien Enselme <jujens@jujens.eu> - 1.2-1
- Update to 1.2

* Wed Aug 31 2016 Julien Enselme <jujens@jujens.eu> - 1.1-3
- Use %%summary instead of custom %%sum macro

* Mon Aug 29 2016 Julien Enselme <jujens@jujens.eu> - 1.1-2
- Add python2-mock to BR so %%check passes correctly.

* Tue Jul 26 2016 Julien Enselme <jujens@jujens.eu> - 1.1-1
- Inital package
