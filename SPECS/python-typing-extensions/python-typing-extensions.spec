%global _description %{expand:
The `typing_extensions` module serves two related purposes:
- Enable use of new type system features on older Python versions. For example,
  `typing.TypeGuard` is new in Python 3.10, but `typing_extensions` allows
  users on Python 3.6 through 3.9 to use it too.
- Enable experimentation with new type system PEPs before they are accepted and
  added to the `typing` module.
New features may be added to `typing_extensions` as soon as they are specified
in a PEP that has been added to the [python/peps](https://github.com/python/peps)
repository. If the PEP is accepted, the feature will then be added to `typing`
for the next CPython release. No typing PEP has been rejected so far, so we
haven't yet figured out how to deal with that possibility.
Starting with version 4.0.0, `typing_extensions` uses
[Semantic Versioning](https://semver.org/). The
major version is incremented for all backwards-incompatible changes.
Therefore, it's safe to depend
on `typing_extensions` like this: `typing_extensions >=x.y, <(x+1)`,
where `x.y` is the first version that includes all features you need.
`typing_extensions` supports Python versions 3.7 and higher. In the future,
support for older Python versions will be dropped some time after that version
reaches end of life.}

Summary:        Python Typing Extensions
Name:           python-typing-extensions
Version:        4.9.0
Release:        1%{?dist}
License:        PSF-2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://pypi.org/project/typing-extensions/
Source0:        %{pypi_source typing_extensions}#/typing-extensions-%{version}.tar.gz
BuildRequires:  python3-devel
BuildRequires:  python3-test
BuildRequires:  python3-packaging
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-flit-core
BuildRequires:  python3-pip

BuildArch:      noarch

%description %{_description}

%package -n python3-typing-extensions
Summary:        %{summary}

%description -n python3-typing-extensions %{_description}

%prep
%autosetup -n typing_extensions-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files typing_extensions

%check
pip3 install pytest==7.1.3
%pytest

%files -n python3-typing-extensions -f %{pyproject_files}
%license LICENSE
%doc CHANGELOG
%doc README.rst

%changelog
* Tue Jan 23 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 4.9.0-1
- Auto-upgrade to 4.9.0 - Azure Linux 3.0 - package upgrades

* Mon Oct 24 2022 Riken Maharjan <rmaharjan@microsoft.com> - 4.2.0-6
- Initial CBL-Mariner import from Fedora 37 (license: MIT).
- License verified

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
