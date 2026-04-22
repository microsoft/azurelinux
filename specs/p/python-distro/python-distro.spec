# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pypi_name distro

Name:           python-%{pypi_name}
Version:        1.9.0
Release: 11%{?dist}
Summary:        Linux Distribution - a Linux OS platform information API

License:        Apache-2.0
URL:            https://github.com/python-distro/distro
Source0:        %{url}/archive/v%{version}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pytest
 
%global _description \
The distro (for: Linux Distribution) package provides information about the\
Linux distribution it runs on, such as a reliable machine-readable ID, or\
version information.\
\
It is a renewed alternative implementation for Python's original\
platform.linux_distribution function, but it also provides much more\
functionality. An alternative implementation became necessary because\
Python 3.5 deprecated this function, and Python 3.7 is expected to remove it\
altogether. Its predecessor function platform.dist was already deprecated since\
Python 2.6 and is also expected to be removed in Python 3.7. Still, there are\
many cases in which access to that information is needed. See Python issue 1322\
for more information.

%description %{_description}

%package -n     python3-%{pypi_name}
Summary:        %{summary}
%if 0%{?fedora}
Suggests:       /usr/bin/lsb_release
%endif

%description -n python3-%{pypi_name} %{_description}

%prep
%autosetup -n %{pypi_name}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install

%files -n python3-%{pypi_name}
%doc CHANGELOG.md CONTRIBUTORS.md README.md
%license LICENSE
%{python3_sitelib}/%{pypi_name}/
%{python3_sitelib}/%{pypi_name}-%{version}.dist-info/

%{_bindir}/distro

%check
%pytest

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.9.0-10
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.9.0-9
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 1.9.0-7
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.9.0-4
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Dec 24 2023 Packit <hello@packit.dev> - 1.9.0-1
- Optimize some repo metastuff and prepare v1.9.0 (#364) (nir0s)
- Actions(deps): Bump actions/setup-python from 4 to 5 (#363) (dependabot[bot])
- Test on modern versions of CPython and PyPy and macOS (#362) (Christian Clauss)
- Actions(deps): Bump actions/checkout from 3 to 4 (#361) (dependabot[bot])
- Refactor `distro.info()` method to return an `InfoDict` (#360) (SCC/楊志璿)
- Ignore the file '/etc/ec2_version' (Pritam Kulkarni)
- Add Debian Testing to the tests (#356) (Harshula Jayasuriya)
- Ignore the file '/etc/board-release' (#353) (Pedro Lamas)
- Add support for ALT Linux Server 10.1 distribution (#354) (Alexander Stepchenko)
- Run Python 3.6 on Ubuntu 20.04 for CI and bump isort (#355) (Samuel FORESTIER)
- Update archlinux resource for tests (Saltaformajo)
- Resolves rhbz#2255740

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 1.8.0-5
- Rebuilt for Python 3.12

* Tue May 23 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 1.8.0-4
- Migrate from tox to pytest

* Sat Feb 11 2023 msuchy <msuchy@redhat.com> - 1.8.0-3
- migrate license to SPDX

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Oct 14 2022 Marek Blaha <mblaha@redhat.com> - 1.8.0-1
- Update to 1.8.0

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.7.0-2
- Rebuilt for Python 3.11

* Wed Feb 16 2022 Marek Blaha <mblaha@redhat.com> - 1.7.0-1
- Update to 1.7.0 (#2054810)
- Drop Python 2 support in the spec
- Run tests using tox

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Aug 05 2021 Marek Blaha <mblaha@redhat.com> - 1.6.0-1
- Update to 1.6.0 (#1988492)

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 03 2021 Python Maint <python-maint@redhat.com> - 1.5.0-6
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 1.5.0-3
- Rebuilt for Python 3.9

* Mon May 11 2020 Stephen Gallagher <sgallagh@redhat.com> - 1.5.0-2
- Fix Python configuration for ELN/RHEL 9
- Rework bconds for Python now that there are no Fedoras left that should
  use Python2

* Tue Mar 31 2020 Marek Blaha <mblaha@redhat.com> - 1.5.0-1
- rebase to distro 1.5.0

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.4.0-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 1.4.0-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Feb 04 2019 Marek Blaha <mblaha@redhat.com> - 1.4.0-1
- rebase to distro 1.4.0

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Aug 30 2018 Marek Blaha <mblaha@redhat.com> - 1.3.0-5
- do not build python2 version for Fedora 30+

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jun 17 2018 Miro Hrončok <mhroncok@redhat.com> - 1.3.0-3
- Rebuilt for Python 3.7

* Tue May 29 2018 Miro Hrončok <mhroncok@redhat.com> - 1.3.0-2
- run tests by pytest, not by tox, there is no tox.ini

* Thu May 10 2018 Miroslav Suchý <msuchy@redhat.com> 1.3.0-1
- rebase to distro 1.3.0

* Tue Jan 02 2018 Miroslav Suchý <msuchy@redhat.com> 1.2.0-1
- run tests
- rebase to distro 1.2.0

* Mon Mar 20 2017 Miroslav Suchý <msuchy@redhat.com> 1.0.3-1
- rebase to 1.0.3

* Tue Jan 24 2017 Miroslav Suchý <msuchy@redhat.com> 1.0.2-3
- typo in license macro

* Tue Jan 24 2017 Miroslav Suchý <msuchy@redhat.com> 1.0.2-2
- add license macro for el6

* Tue Jan 24 2017 Miroslav Suchý <msuchy@redhat.com> 1.0.2-1
- update to 1.0.2
- 1415667 - require python-argparse on EL6

* Tue Jan 03 2017 Miroslav Suchý <msuchy@redhat.com> 1.0.1-2
- soft deps on lsb_release

* Sun Jan 01 2017 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1.0.1-1
- Update to 1.0.1
- Provide only one copy of $bindir/distro
- Cleanups in spec

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.0.0-7
- Rebuild for Python 3.6

* Thu Oct 06 2016 Miroslav Suchý <msuchy@redhat.com> 1.0.0-6
- polish spec according the package review

* Wed Oct 05 2016 Miroslav Suchý 1.0.0-5
- use python3 in /usr/bin/distro on Fedoras

* Wed Oct 05 2016 Miroslav Suchý 1.0.0-4
- use python3 in /usr/bin/distro on Fedoras

* Wed Oct 05 2016 Miroslav Suchý 1.0.0-3
- python2 subpackages only on rhel
- correct description

* Wed Oct 05 2016 Miroslav Suchý 1.0.0-2
- require lsb_release

* Wed Oct 05 2016 Miroslav Suchý 1.0.0-1
- initial packaging

