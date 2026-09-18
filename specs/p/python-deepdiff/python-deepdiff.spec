# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Don't have sphinx-sitemaps for now...
%bcond_with docs
%bcond_without tests

Name:           python-deepdiff
Version:        8.6.1
Release:        2%{?dist}
Summary:        Deep Difference and search of any Python object/data

License:        MIT
URL:            https://github.com/seperman/deepdiff/
Source:         https://github.com/seperman/deepdiff/archive/%{version}/%{name}-v%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  python3-devel

# For tests
# Cherry picked test reqs from pyproject.toml
%if %{with tests}
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(numpy)
BuildRequires:  python3dist(tomli-w)
BuildRequires:  python3dist(python-dateutil)
BuildRequires:  python3dist(jsonpickle)
BuildRequires:  python3dist(pydantic)
BuildRequires:  python3-pandas
BuildRequires:  python3-pytest-benchmark
%endif

# For docs
%if %{with docs}
BuildRequires:  python3dist(sphinx)
BuildRequires:  python3-dotenv
BuildRequires:  python3-sphinx-sitemap
%endif

%global _description %{expand:
Deep Difference of dictionaries, iterables, strings, and ANY other object.
Includes additional modules with related functionality:
DeepSearch: Search for objects within other objects.
DeepHash: Hash any object based on their content.
Delta: Store the difference of objects and apply them to other objects.
Extract: Extract an item from a nested Python object using its path.
commandline: Use DeepDiff from commandline.}

%description %{_description}

%package     -n python3-deepdiff
Summary:        %{summary}
Recommends:     python3-deepdiff+cli

%description -n python3-deepdiff %{_description}


# Add the cli as a extras subpackage which provides the deep executable.
# Including the cli extra as the deep command doesnt function without it.
%pyproject_extras_subpkg -n python3-deepdiff cli
%{_bindir}/deep


%prep
%autosetup -p1 -n deepdiff-%{version}

find deepdiff/ -name \*.py -exec sed -i '/#!\/usr\/bin\/env /d' {} \;

# Upstream pins the dependencies to explicit versions
# This leads to downstream problems like:
#  https://bugzilla.redhat.com/2246614
# We replace all the version matching clauses with compatible release clauses:
sed -i 's/==/~=/' pyproject.toml
# Relax a bit the flit-core version for EPEL 10.
sed -i '/flit_core/{s/>=3.11/>=3.9/}' pyproject.toml
# Remove click's upper version bound
sed -i 's/click~=8.1.0/click>=8.1.0/' pyproject.toml


%generate_buildrequires
%pyproject_buildrequires -x cli,optimize


%build
%pyproject_wheel

%if %{with docs}
# Build docs
make -C docs html
# remove the sphinx-build leftovers
rm -rf docs/_build/html/.{doctrees,buildinfo}
%endif


%install
%pyproject_install

%pyproject_save_files deepdiff


%check
%if %{with tests}
# uuid6 package is not available on Fedora at the moment, so remove test_hash.py
%pytest --ignore=tests/test_hash.py tests/
%endif
%pyproject_check_import


%files -n python3-deepdiff -f %{pyproject_files}

%doc AUTHORS.md README.md

%if %{with docs}
%doc docs/_build/html
%endif



%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 8.6.1-2
- Rebuilt for Python 3.14.0rc3 bytecode

* Sun Sep 14 2025 Romain Geissler <romain.geissler@amadeus.com> - 8.6.1-1
- Update to 8.6.1 (rhbz#2393085).

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 8.5.0-7
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 8.5.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 08 2025 Charalampos Stratakis <cstratak@redhat.com> - 8.5.0-5
- Remove click's upper version bound

* Sun Jun 29 2025 Romain Geissler <romain.geissler@amadeus.com> - 8.5.0-4
- Fix tests with python 3.14 (rhbz#2374300).

* Wed Jun 18 2025 Python Maint <python-maint@redhat.com> - 8.5.0-3
- Bootstrap for Python 3.14.0b3 bytecode

* Thu Jun 05 2025 Python Maint <python-maint@redhat.com> - 8.5.0-2
- Bootstrap for Python 3.14

* Sat May 10 2025 Romain Geissler <romain.geissler@amadeus.com> - 8.5.0-1
- Update to 8.5.0 (rhbz#2365409).

* Wed Apr 16 2025 Romain Geissler <romain.geissler@amadeus.com> - 8.4.1-2
- Relax a bit the pyyaml version for EPEL 10

* Mon Mar 31 2025 Romain Geissler <romain.geissler@amadeus.com> - 8.4.1-1
- Update to 8.4.1 (rhbz#2332738).

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Oct 30 2024 Karolina Surma <ksurma@redhat.com> - 8.0.1-1
- Update to 8.0.1.

* Wed Sep 04 2024 Susi Lehtola <jussilehtola@fedoraproject.org> - 8.0.0-1
- Update to 8.0.0.

* Tue Jul 30 2024 Susi Lehtola <jussilehtola@fedoraproject.org> - 7.0.1-1
- Update to 7.0.1.

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.3.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 29 2024 Python Maint <python-maint@redhat.com> - 6.3.1-7
- Rebuilt for Python 3.13

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 6.3.1-6
- Bootstrap for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Nov 06 2023 Miro Hrončok <mhroncok@redhat.com> - 6.3.1-3
- Relax the required versions of some of the dependencies
- Fixes: rhbz#2246614

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jul 14 2023 Susi Lehtola <jussilehtola@fedoraproject.org> - 6.3.1-1
- Update to 6.3.1.

* Wed Apr 05 2023 Ryan Erickson <rerickso@redhat.com> - 6.3.0-1
- Update to 6.3.0.
- Surface cli extra as subpackage to fix cli if python3-deepdiff+cli installed.
Resolves: rhbz#2171664
Resolves: rhbz#2138689

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Sep 01 2022 Susi Lehtola <jussilehtola@fedoraproject.org> - 6.1.0-1
- Update to 6.1.0.

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 22 2022 Adam Williamson <awilliam@redhat.com> - 5.8.2-1
- Update to 5.8.2
- Drop all Python 2 bits from spec
- Actually run the test suite
- Backport PR #327 to fix tests with Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.2-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 5.0.2-3
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Aug 11 2020 Susi Lehtola <jussilehtola@fedoraproject.org> - 5.0.2-1
- Update to 5.0.2.

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 4.3.1-2
- Rebuilt for Python 3.9

* Fri Mar 13 2020 Susi Lehtola <jussilehtola@fedoraproject.org> - 4.3.1-1
- Update to 4.3.1.

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 4.0.7-3
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 4.0.7-2
- Rebuilt for Python 3.8

* Wed Jul 24 2019 Susi Lehtola <jussilehtola@fedoraproject.org> - 4.0.7-1
- Update to 4.0.7.

* Wed May 15 2019 Susi Lehtola <jussilehtola@fedoraproject.org> - 4.0.6-1
- Update to 4.0.6.

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Sep 24 2018 Susi Lehtola <jussilehtola@fedoraproject.org> - 3.3.0-3
- Further review fixes.

* Mon Sep 24 2018 Susi Lehtola <jussilehtola@fedoraproject.org> - 3.3.0-2
- Review fixes.

* Sat Sep 22 2018 Susi Lehtola <jussilehtola@fedoraproject.org> - 3.3.0-1
- First release.
