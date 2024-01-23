%global pypi_name pytest-mock
%global file_name pytest_mock
Summary:        Thin-wrapper around the mock package for easier use with py.test
Name:           python-%{pypi_name}
Version:        3.12.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/pytest-dev/pytest-mock/
Source0:        https://files.pythonhosted.org/packages/96/e1/fb53b62056e6840a36d9a4beb4e42726155594c567b574103435a7131c60/%{pypi_name}-%{version}.tar.gz
# Can be removed once this bug is resolved: https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=1006736
Patch0:         skip_broken_tests_since_3.6.1.patch

BuildArch:      noarch

%description
This plugin installs a mocker fixture which is a thin-wrapper around the
patching API provided by the mock package, but with the benefit of not having
to worry about undoing patches at the end of a test.

%package -n     python3-%{pypi_name}
%{?python_provide:%python_provide python3-%{pypi_name}}
Summary:        %{summary}
BuildRequires:  python%{python3_pkgversion}-pytest-asyncio
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-setuptools_scm
BuildRequires:  python3-devel
%if %{with_check}
BuildRequires:  python3-pip
%endif

%description -n python3-%{pypi_name}
This plugin installs a mocker fixture which is a thin-wrapper around the
patching API provided by the mock package, but with the benefit of not having
to worry about undoing patches at the end of a test.

%prep
%autosetup -n %{pypi_name}-%{version} -p1
rm -rf *.egg-info
# Correct end of line encoding for README
sed -i 's/\r$//' README.rst

%build
%py3_build

%install
%py3_install

%check
pip3 install atomicwrites>=1.3.0 \
    attrs>=19.1.0 \
    more-itertools>=7.0.0 \
    pluggy>=0.11.0 \
    pytest==7.1.2 \
    pytest-cov>=2.7.1
PATH=%{buildroot}%{_bindir}:${PATH} \
PYTHONPATH=%{buildroot}%{python3_sitelib} \
    python%{python3_version} -m pytest -v tests \
    -k "not test_standalone_mock and not test_detailed_introspection and not test_detailed_introspection \
  and not test_assert_called_args_with_introspection and not test_assert_called_kwargs_with_introspection"

%files -n python3-%{pypi_name}
%doc CHANGELOG.rst README.rst
%license LICENSE
%{python3_sitelib}/%{file_name}/
%{python3_sitelib}/%{file_name}-%{version}-py%{python3_version}.egg-info/

%changelog
* Tue Jan 23 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.12.0-1
- Auto-upgrade to 3.12.0 - Azure Linux 3.0 - package upgrades

* Wed Oct 26 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.7.0-2
- Freezing 'pytest' test dependency to version 7.1.2.

* Fri Mar 25 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.7.0-1
- Updating to version 3.7.0.
- Added a patch skipping broken tests.

* Wed Jun 23 2021 Rachel Menge <rachelmenge@microsoft.com> - 3.5.1-3
- Initial CBL-Mariner import from Fedora 34 (license: MIT)
- License verified

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
