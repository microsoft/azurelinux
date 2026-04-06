# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global srcname gitdb

Name:           python-%{srcname}
Version:        4.0.11
Release:        6%{?dist}
Summary:        Git Object Database

License:        BSD-3-Clause
URL:            https://github.com/gitpython-developers/gitdb
Source0:        %{pypi_source %{srcname}}

BuildArch:      noarch

BuildRequires:  git-core

%global _description %{expand:
GitDB allows you to access bare git repositories for reading and writing.
It aims at allowing full access to loose objects as well as packs with
performance and scalability in mind. It operates exclusively on streams,
allowing to handle large objects with a small memory footprint.}

%description %{_description}

%package -n python3-%{srcname}
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  %{py3_dist pytest}

%description -n python3-%{srcname} %{_description}

%prep
%autosetup -n %{srcname}-%{version} -p 1

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l %{srcname}

%check
# The tests require a git repo with a substantial number of objects.
# https://github.com/gitpython-developers/gitdb/issues/16
mkdir testrepo
pushd testrepo
git init -q
git config user.email "%{name}-owner@fedoraproject.org"
git config user.name "%{name} maintainer"
for i in {1..400}; do echo $i > $i; git add $i; git commit -q -m "$i"; done
git gc
popd

export GITDB_TEST_GIT_REPO_BASE=testrepo/.git
%pytest --verbose

%files -n python3-%{srcname} -f %{pyproject_files}
%doc AUTHORS

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 4.0.11-6
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 4.0.11-5
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 4.0.11-3
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Sep 11 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 4.0.11-1
- Update to 4.0.11 (close RHBZ#2245314)

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 4.0.10-6
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 4.0.10-2
- Rebuilt for Python 3.12

* Tue May 23 2023 Lubomír Sedlář <lsedlar@redhat.com> - 4.0.10-1
- New upstream release 4.0.10 (#2148339)

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 4.0.9-3
- Rebuilt for Python 3.11

* Thu Feb 10 2022 Carl George <carl@george.computer> - 4.0.9-2
- Convert to pyproject macros
- Fix test suite

* Wed Feb 09 2022 Joel Capitao <jcapitao@redhat.com> - 4.0.9-1
- New upstream release 4.0.9 (#1943332)

* Wed Feb 09 2022 Troy Dawson <tdawson@redhat.com> - 4.0.5-6
- Switch from python3-nose to python3-pytest for testing

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 4.0.5-3
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan 07 2021 Joel Capitao <jcapitao@redhat.com> - 4.0.5-1
- New upstream release 4.0.5 (#1806853)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 4.0.1-2
- Rebuilt for Python 3.9

* Mon Feb 24 2020 Lubomír Sedlář <lsedlar@redhat.com> - 4.0.1-1
- New upstream release 4.0.1

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jan 08 2020 Lubomír Sedlář <lsedlar@redhat.com> - 2.0.3-10
- Fix build with Python 3.9

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 2.0.3-9
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 2.0.3-8
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jun 26 2019 Petr Viktorin <pviktori@redhat.com> - 2.0.3-6
- Remove Python 2 subpackage
  https://bugzilla.redhat.com/show_bug.cgi?id=1723967
- Run tests using a specific Python interpreter, rather than rely on command name
- Re-enable passing tests

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jun 17 2018 Miro Hrončok <mhroncok@redhat.com> - 2.0.3-3
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Sep 30 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.0.3-1
- Update to 2.0.3

* Tue Aug 08 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.0.2-1
- Update to 2.0.2

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Dec 28 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.0-1
- Update to 2.0.0
- Modernize spec

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.6.4-6
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.4-5
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.4-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 26 2015 Dennis Gilmore <dennis@ausil.us> - 0.6.4-1
- update to 0.6.4
- enable python3 support

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 17 2011 Jesse Keating <jkeating@redhat.com> - 0.5.4-2
- Require python-smmap

* Mon Jul 18 2011 Jesse Keating <jkeating@redhat.com> - 0.5.4-1
- Upstream release to fix licensing issues
- Use real upstream release instead of git checkout
- No tests shipped in release, remove %%check

* Tue Jun 14 2011 Jesse Keating <jkeating@redhat.com> - 0.5.2-3.20110613git17d9d13
- Add a br on python-async

* Mon Jun 13 2011 Jesse Keating <jkeating@redhat.com> - 0.5.2-2.20110613git17d9d13
- Fix perms and add a date to the release field.

* Sat May 28 2011 Jesse Keating <jkeating@redhat.com> - 0.5.2-1.git17d9d13
- Initial package

