# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           python-typing-extensions
Version:        4.15.0
Release:        2%{?dist}
Summary:        Backported and Experimental Type Hints for Python

License:        PSF-2.0
URL:            https://pypi.org/project/typing-extensions/
Source:         %{pypi_source typing_extensions}

# fix test on 3.14
# https://github.com/python/typing_extensions/pull/683
Patch:          https://github.com/python/typing_extensions/pull/683.patch

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-test

%global _description %{expand:
The typing_extensions module serves two related purposes:

- Enable use of new type system features on older Python versions. For example,
  typing.TypeGuard is new in Python 3.10, but typing_extensions allows users on
  previous Python versions to use it too.

- Enable experimentation with new type system PEPs before they are accepted and
  added to the typing module.

typing_extensions is treated specially by static type checkers such as mypy and
pyright. Objects defined in typing_extensions are treated the same way as
equivalent forms in typing.}

%description %_description


%package -n python3-typing-extensions
Summary:       %{summary}

%description -n python3-typing-extensions %_description


%prep
%autosetup -p1 -n typing_extensions-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l typing_extensions


%check
cd src
%{py3_test_envvars} %{python3} -m unittest discover


%files -n python3-typing-extensions -f %{pyproject_files}
%doc CHANGELOG.md
%doc README.md


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 4.15.0-2
- Rebuilt for Python 3.14.0rc3 bytecode

* Mon Sep 01 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 4.15.0-1
- Update to 4.15.0 (close RHBZ#2390801)

* Tue Aug 19 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 4.15.0~rc1-1
- Update to 4.15.0~rc1 (close RHBZ#2389191; fixes RHBZ#2389399)

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 4.14.1-3
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.14.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jul 04 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 4.14.1-1
- Updated to version 4.14.1 (close RHBZ#2376358)

* Tue Jun 03 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 4.14.0-1
- Updated to version 4.14.0 (close RHBZ#2369847)

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 4.14.0~rc1-2
- Rebuilt for Python 3.14

* Sun May 25 2025 Jonny Heggheim <hegjon@gmail.com> - 4.14.0~rc1-1
- Updated to version 4.14.0rc1

* Thu Apr 10 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 4.13.2-1
- Update to 4.13.2

* Fri Apr 04 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 4.13.1-1
- Updated to version 4.13.1 (close RHBZ#2357244)

* Tue Apr 01 2025 Jonny Heggheim <hegjon@gmail.com> - 4.13.0-1
- Updated to version 4.13.0

* Tue Mar 18 2025 Jonny Heggheim <hegjon@gmail.com> - 4.13.0~rc1-1
- Updated to version 4.13.0rc1

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.12.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.12.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 10 2024 Python Maint <python-maint@redhat.com> - 4.12.2-2
- Rebuilt for Python 3.13

* Fri Jun 07 2024 Jonny Heggheim <hegjon@gmail.com> - 4.12.2-1
- Updated to version 4.12.2

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 4.12.1-2
- Rebuilt for Python 3.13

* Sun Jun 02 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 4.12.1-1
- Updated to version 4.12.1 (close RHBZ#2280883)

* Wed May 29 2024 Karolina Surma <ksurma@redhat.com> - 4.12.0-1
- Updated to version 4.12.0

* Tue Apr 09 2024 Jonny Heggheim <hegjon@gmail.com> - 4.11.0-1
- Updated to version 4.11.0

* Tue Feb 27 2024 Jonny Heggheim <hegjon@gmail.com> - 4.10.0-1
- Updated to version 4.10.0

* Sun Feb 18 2024 Jonny Heggheim <hegjon@gmail.com> - 4.10.0~rc1-1
- Updated to version 4.10.0rc1

* Fri Feb 16 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 4.9.0-4
- Fix test_generic_protocols_special_from_protocol with latest Python

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Dec 10 2023 Jonny Heggheim <hegjon@gmail.com> - 4.9.0-1
- Updated to version 4.9.0

* Mon Sep 18 2023 Jonny Heggheim <hegjon@gmail.com> - 4.8.0-1
- Updated to version 4.8.0

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Jul 02 2023 Jonny Heggheim <hegjon@gmail.com> - 4.7.1-1
- Updated to version 4.7.1

* Thu Jun 29 2023 Python Maint <python-maint@redhat.com> - 4.7.0-2
- Rebuilt for Python 3.12

* Wed Jun 28 2023 Jonny Heggheim <hegjon@gmail.com> - 4.7.0-1
- Updated to version 4.7.0

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 4.6.3-2
- Rebuilt for Python 3.12

* Sat Jun 03 2023 Jonny Heggheim <hegjon@gmail.com> - 4.6.3-1
- Updated to version 4.6.3

* Thu May 25 2023 Jonny Heggheim <hegjon@gmail.com> - 4.6.2-1
- Updated to version 4.6.2

* Wed May 24 2023 Jonny Heggheim <hegjon@gmail.com> - 4.6.1-1
- Updated to version 4.6.1

* Tue May 23 2023 Jonny Heggheim <hegjon@gmail.com> - 4.6.0-1
- Updated to version 4.6.0

* Wed Feb 15 2023 Jonny Heggheim <hegjon@gmail.com> - 4.5.0-1
- Updated to version 4.5.0

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Nov 29 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 4.4.0-2
- Update License to SPDX

* Thu Nov 24 2022 Jonny Heggheim <hegjon@gmail.com> - 4.4.0-1
- Updated to version 4.4.0

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 4.2.0-4
- Rebuilt for Python 3.11

* Mon May 23 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 4.2.0-3
- Stop using deprecated zero-argument pypi_source macro

* Sun May 22 2022 Jonny Heggheim <hegjon@gmail.com> - 4.2.0-2
- Removed unused build depenencies

* Sat Apr 30 2022 Jonny Heggheim <hegjon@gmail.com> - 4.2.0-1
- Updated to version 4.2.0

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Aug 31 2021 Fabian Affolter <mail@fabian-affolter.ch> - 3.10.0.2-1
- Update to latest upstream release 3.10.0.2 (closes rhbz#1955959)

* Thu Aug 26 2021 Fabian Affolter <mail@fabian-affolter.ch> - 3.10.0.0-1
- Update to latest upstream release 3.10.0.0 (closes rhbz#1955959)

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.4.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 3.7.4.3-3
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sun Aug 23 2020 Fabian Affolter <mail@fabian-affolter.ch> - 3.7.4.3-1
- Update to latest upstream release 3.7.4.3 (rhbz#1871451)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 3.7.4.2-2
- Rebuilt for Python 3.9

* Sat Apr 11 2020 Fabian Affolter <mail@fabian-affolter.ch> - 3.7.4.2-1
- Support for Python 3.9 (rhbz#1808663)
- Update to latest upstream release 3.7.4.2 (rhbz#1766182)

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 3.7.4-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 3.7.4-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jul 12 2019 Jonny Heggheim <hegjon@gmail.com> - 3.7.4-1
- Updated to 3.7.4

* Sun Mar 31 2019 Jonny Heggheim <hegjon@gmail.com> - 3.7.2-1
- Inital packaging
