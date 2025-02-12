Name:           python-PyMySQL
Version:        1.1.1
Release:        3%{?dist}
Summary:        Pure-Python MySQL client library

License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://pypi.org/project/pymysql/
Source0:        https://files.pythonhosted.org/packages/b3/8f/ce59b5e5ed4ce8512f879ff1fa5ab699d211ae2495f1adaa5fbba2a1eada/pymysql-%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildArch:      noarch

%description
This package contains a pure-Python MySQL client library. The goal of PyMySQL is
to be a drop-in replacement for MySQLdb and work on CPython, PyPy, IronPython
and Jython.

%package -n     python3-PyMySQL
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires: 	python3-pip
BuildRequires: 	python3-wheel

%description -n python3-PyMySQL
This package contains a pure-Python MySQL client library. The goal of PyMySQL is
to be a drop-in replacement for MySQLdb and work on CPython, PyPy, IronPython
and Jython.

%pyproject_extras_subpkg -n python3-PyMySQL rsa %{!?rhel:ed25519}

%prep
%autosetup -n pymysql-%{version}

%generate_buildrequires
%pyproject_buildrequires -x rsa %{!?rhel:-x ed25519}

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files pymysql

%check
# Tests cannot be launch on koji, they require a mysqldb running.
%pyproject_check_import

%files -n python3-PyMySQL -f %{pyproject_files}
%license LICENSE
%doc README.md

%changelog
* Tue Feb 11 2025 Akhila Guruju <v-guakhila@microsoft.com> - 1.1.1-3
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified.
- Added 'BuildRequires: python3-pip python3-wheel'

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 15 2024 Julien Enselme <jujens@jujens.eu> - 1.1.1-1
- Update to 1.1.1

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 1.1.0-7
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Jan 16 2024 Carl George <carlwgeorge@fedoraproject.org> - 1.1.0-4
- Convert to pyproject macros

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 04 2023 Python Maint <python-maint@redhat.com> - 1.1.0-2
- Rebuilt for Python 3.12

* Tue Jul 04 2023 Julien Enselme <jujens@jujens.eu> - 1.1.0-1
- Update to 1.1.0

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 1.0.3-3
- Rebuilt for Python 3.12

* Thu May 11 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 1.0.3-2
- Disable ed25519 in RHEL builds

* Tue Apr 25 2023 Julien Enselme <jujens@jujens.eu> - 1.0.3-1
- Update to 1.0.3

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Aug 11 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.0.2-3
- Add metapackages for “rsa” and “ed25519” extras
- Drop hard dependency on python3-cryptography

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 29 2022 Julien Enselme <jujens@jujens.eu> - 1.0.2-1
- Update to 1.0.2

* Tue Jun 14 2022 Python Maint <python-maint@redhat.com> - 0.10.1-6
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.10.1-3
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Sep 10 2020 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 0.10.1-1
- Update to 0.10.1 (#1877703)

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jul 18 2020 Julien Enselme <jujens@jujens.eu> - 0.10.0-1
- Update to 0.10.0

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.9.3-3
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Nov 18 2019 Lumír Balhar <lbalhar@redhat.com> - 0.9.3-1
- New upstream version 0.9.3

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.9.2-7
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.9.2-6
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Dec 02 2018 Julien Enselme <jujens@jujens.eu> - 0.9.2-3
- Remove Python 2 subpackage.

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jul 06 2018 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 0.9.2-1
- Update to 0.9.2

* Tue Jul 03 2018 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 0.9.1-1
- Update to 0.9.1

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 0.9.0-2
- Rebuilt for Python 3.7

* Sat Jun 30 2018 Julien Enselme <jujens@jujens.eu> - 0.9.0-1
- Update to 0.9.0

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.8.1-2
- Rebuilt for Python 3.7

* Mon May 07 2018 Julien Enselme <jujens@jujens.eu> - 0.8.1-1
- Update to 0.8.1

* Mon Mar 19 2018 Carl George <carl@george.computer> - 0.8.0-5
- Rename python3 subpackage to python34

* Thu Feb 15 2018 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 0.8.0-4
- make spec file compatible with epel7
- remove conditionals and always build for Python 3

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 15 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.8.0-2
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Wed Dec 27 2017 Julien Enselme <jujens@jujens.eu> - 0.8.0-1
- Update to 0.8.0

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Apr 07 2017 Julien Enselme <jujens@jujens.eu> - 0.7.11-1
- Update to 0.7.11

* Wed Feb 15 2017 Julien Enselme <jujens@jujens.eu> - 0.7.10-1
- Update to 0.7.10

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.7.9-3
- Rebuild for Python 3.6

* Wed Nov 23 2016 Damien Ciabrini <dciabrin@redhat.com> - 0.7.9-2
- cherrypick commit 755dfdc upstream to allow bind before connect
  Related: rhbz#1378008

* Sun Sep 18 2016 Julien Enselme <jujens@jujens.eu> - 0.7.9-1
- Update to 0.7.9

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.7-6
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 4 2016 Julien Enselme <jujens@jujens.eu> - 0.6.7-4
- Correct installation problems due to Requires: mariadb

* Thu Nov 5 2015 Julien Enselme <jujens@jujens.eu> - 0.6.7-3
- Rebuilt for python 3.5

* Wed Nov  4 2015 Haïkel Guémar <hguemar@fedoraproject.org> - 0.6.7-2
- Drop unnecessary mariadb requirement
- Add python3 conditionals in order to rebuild it in EL7

* Thu Oct 1 2015 Julien Enselme <jujens@jujens.eu> - 0.6.7-1
- Update to 0.6.7

* Thu Aug 6 2015 Julien Enselme <jujens@jujens.eu> - 0.6.6-4
- Use %%license in %%files

* Wed Aug 5 2015 Julien Enselme <jujens@jujens.eu> - 0.6.6-3
- Move python2 package in its own subpackage
- Add provides

* Fri Jul 31 2015 Julien Enselme <jujens@jujens.eu> - 0.6.6-2
- Add Provides: python2-PyMySQL
- Remove usage of %%py3dir

* Sun May 31 2015 Julien Enselme <jujens@jujens.eu> - 0.6.6-1
- Update to 0.6.6

* Wed Nov 26 2014 Julien Enselme <jujens@jujens.eu> - 0.6.2-1
- Initial packaging
