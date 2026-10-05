# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Enables additional tests in tests/test_pydantic.py
%bcond pydantic 1

Name:           python-yarl
Version:        1.25.1
Release: 5%{?dist}
Summary:        Python module to handle URLs

License:        Apache-2.0
URL:            https://yarl.readthedocs.io
Source:         https://github.com/aio-libs/yarl/archive/v%{version}/yarl-%{version}.tar.gz
# Allow downstream packagers to opt out of release build flags
# https://github.com/aio-libs/yarl/pull/1675
#
# Fixes:
#
# Cannot build distribution-friendly wheels
# https://github.com/aio-libs/yarl/issues/1592
#
# Rebased on v1.25.1.
Patch:          yarl-1.25.1-system-flags.patch

BuildRequires:  gcc
BuildRequires:  python3dist(cython)

# See requirements/test-cibuildwheel.txt and requirements/test.txt, which also
# contain coverage-analysis tools and some other unnecessary or unwanted
# dependencies.
BuildRequires:  python3dist(hypothesis)
%if %{with pydantic}
BuildRequires:  python3dist(pydantic)
%endif
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(pytest-xdist)

%description
The module provides handy URL class for URL parsing and changing.

%package -n python3-yarl
Summary:        %{summary}

%description -n python3-yarl
The module provides handy URL class for URL parsing and changing.

%prep
%autosetup -n yarl-%{version} -p1
# Disable coverage
sed --regexp-extended --in-place 's/(-.*cov.*$)/#\1/g' pytest.ini

%generate_buildrequires
export YARL_NO_BUILD_OPTIMIZATION_FLAGS=1
# Imitates upstream, and doesn’t interfere with respecting distro flags
export CFLAGS="${CFLAGS} -DNDEBUG"
%pyproject_buildrequires

%build
export YARL_NO_BUILD_OPTIMIZATION_FLAGS=1
# Imitates upstream, and doesn’t interfere with respecting distro flags
export CFLAGS="${CFLAGS} -DNDEBUG"
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files --assert-license yarl

%check
# Ignore the benchmark tests which require pytest_codspeed which is not
# packaged in Fedora.
%pytest --ignore-glob='tests/test_*_benchmarks.py' --verbose -rs tests

%files -n python3-yarl -f %{pyproject_files}
%doc CHANGES.rst README.rst

%changelog
* Wed Sep 16 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 1.25.1-1
- Update to 1.25.1 (close RHBZ#2422940)
- Fix compiling with distribution compiler flags and generating debuginfo

* Wed Jul 22 2026 Python Maint <python-maint@redhat.com> - 1.22.0-5
- Rebuilt for Python 3.15.0b4 ABI change

* Thu Jul 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_45_Mass_Rebuild

* Thu Jun 04 2026 Python Maint <python-maint@redhat.com> - 1.22.0-3
- Rebuilt for Python 3.15

* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Fri Oct 10 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1.22.0-1
- Update to 1.22.0 (close RHBZ#2357666)

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.18.3-6
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.18.3-5
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 07 2025 Charalampos Stratakis <cstratak@redhat.com> - 1.18.3-3
- Remove cython upper version pin

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 1.18.3-2
- Rebuilt for Python 3.14

* Fri Feb 14 2025 Romain Geissler <romain.geissler@amadeus.com> - 1.18.3-1
- Update to 1.18.3

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Sep 28 2024 Fabian Affolter <mail@fabian-affolter.ch> - 1.13.1-1
- Update to latest upstream release (closes rhbz#2315385)

* Tue Sep 24 2024 Fabian Affolter <mail@fabian-affolter.ch> - 1.12.1-1
- Update to latest upstream release (closes rhbz#2314377)

* Mon Sep 16 2024 Fabian Affolter <mail@fabian-affolter.ch> - 1.11.1-1
- Update to latest upstream release 1.11.1 (closes rhbz#2309712)

* Wed Jul 24 2024 Miroslav Suchý <msuchy@redhat.com> - 1.9.4-3
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Sandro <devel@penguinpee.nl> - 1.9.4-1
- Update to 1.9.4 (RHBZ#2251098)

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.9.2-6
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 1.9.2-2
- Rebuilt for Python 3.12

* Mon May 15 2023 Tomáš Hrnčiar <thrnciar@redhat.com> - 1.9.2-1
- Update to 1.9.2
- Fixes: rhbz#2161299
- Fixes: rhbz#2188511

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Dec 04 2022 Fabian Affolter <mail@fabian-affolter.ch> - 1.8.2-1
- Update to latest upstream release 1.8.2 (closes rhbz#2150499)

* Fri Aug 19 2022 Fabian Affolter <mail@fabian-affolter.ch> - 1.8.1-1
- Update to latest upstream release 1.8.1 (closes rhbz#2112722)

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.8.0-2
- Rebuilt for Python 3.11

* Wed Feb 23 2022 Fabian Affolter <mail@fabian-affolter.ch> - 1.8.0-1
- Update to latest upstream release 1.8.0 (closes rhbz#2054415)

* Thu Jan 27 2022 Carl George <carl@george.computer> - 1.7.2-3
- Remove unnecessary buildrequirements

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Nov 25 2021 Fabian Affolter <mail@fabian-affolter.ch> - 1.7.2-1
- Update to latest upstream release 1.7.2 (closes rhbz#2019303)

* Wed Oct 13 2021 Fabian Affolter <mail@fabian-affolter.ch> - 1.7.0-1
- Update to latest upstream release 1.7.0 (closes rhbz#2010811)

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.6.3-4
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 25 2021 Miro Hrončok <mhroncok@redhat.com> - 1.6.3-2
- Build the extension module and install it
- Run the tests
- Fixes: rhbz#1919977

* Tue Nov 17 2020 Fabian Affolter <mail@fabian-affolter.ch> - 1.6.3-1
- Tests are disaabled for now (approx. 10 % failures)
- Update to latest upstream release 1.6.3 (#1887712)

* Tue Oct 13 2020 Fabian Affolter <mail@fabian-affolter.ch> - 1.6.2-1
- Update to latest upstream release 1.6.2 (#1887712)

* Thu Sep 24 2020 Fabian Affolter <mail@fabian-affolter.ch> - 1.6.0-1
- Update to latest upstream release 1.6.0 (#1882235)

* Sun Aug 09 2020 Fabian Affolter <mail@fabian-affolter.ch> - 1.5.1-1
- Update to latest upstream release 1.5.1 (#1860699)

* Thu Aug 06 2020 Fabian Affolter <mail@fabian-affolter.ch> - 1.5.0-1
- Update to latest upstream release 1.5.0 (#1860699)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 1.4.2-3
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Dec 08 2019 Fabian Affolter <mail@fabian-affolter.ch> - 1.4.2-1
- Update to latest upstream release 1.4.2 (#1758088)

* Thu Dec 05 2019 Fabian Affolter <mail@fabian-affolter.ch> - 1.4.1-1
- Update to latest upstream release 1.4.1 (#1758088)

* Mon Dec 02 2019 Fabian Affolter <mail@fabian-affolter.ch> - 1.4.0-1
- Update to latest upstream release 1.4.0

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.3.0-6
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 1.3.0-5
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Jun 01 2019 Fabian Affolter <mail@fabian-affolter.ch> - 1.3.0-3
- Remove dep generator

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 10 2019 Fabian Affolter <mail@fabian-affolter.ch> - 1.3.0-1
- Update to latest upstream release 1.3.0

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.2.6-2
- Rebuilt for Python 3.7

* Thu Jun 14 2018 Fabian Affolter <mail@fabian-affolter.ch> - 1.2.6-1
- Update to latest upstream release 1.2.6 (#1588495)

* Thu May 24 2018 Fabian Affolter <mail@fabian-affolter.ch> - 1.2.5-1
- Update to latest upstream release 1.2.5 (#1582015)

* Tue May 08 2018 Fabian Affolter <mail@fabian-affolter.ch> - 1.2.4-1
- Update to latest upstream release 1.2.4 (#1575970)

* Mon May 07 2018 Fabian Affolter <mail@fabian-affolter.ch> - 1.2.3-1
- Update to latest upstream release 1.2.3 (#1574065)

* Sat May 05 2018 Fabian Affolter <mail@fabian-affolter.ch> - 1.2.2-1
- Update to latest upstream release 1.2.2 (#1574065)

* Fri May 04 2018 Fabian Affolter <mail@fabian-affolter.ch> - 1.2.1-1
- Update to latest upstream release 1.2.1 (#1574065)

* Mon Feb 19 2018 Fabian Affolter <mail@fabian-affolter.ch> - 1.1.1-1
- Update to latest upstream release 1.1.1

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Jan 21 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.1.0-1
- Update to 1.1.0

* Fri Jan 19 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.0.0-2
- Enable usage of dependency generator

* Mon Jan 15 2018 Fabian Affolter <mail@fabian-affolter.ch> - 1.0.0-1
- Update to latest upstream release 1.0.0

* Thu Jan 11 2018 Fabian Affolter <mail@fabian-affolter.ch> - 0.18.0-1
- Update to latest upstream release 0.18.0

* Sun Dec 31 2017 Fabian Affolter <mail@fabian-affolter.ch> - 0.17.0-1
- Update to latest upstream release 0.17.0 (#1523436)

* Fri Dec 08 2017 Fabian Affolter <mail@fabian-affolter.ch> - 0.16.0-1
- Update to latest upstream release 0.16.0 (#1523436)

* Fri Nov 24 2017 Fabian Affolter <mail@fabian-affolter.ch> - 0.15.0-1
- Update to latest upstream release 0.15.0

* Tue Nov 14 2017 Fabian Affolter <mail@fabian-affolter.ch> - 0.14.2-1
- Update to latest upstream release 0.14.2

* Tue Nov 14 2017 Fabian Affolter <mail@fabian-affolter.ch> - 0.14.1-1
- Update to latest upstream release 0.14.1

* Sat Nov 11 2017 Fabian Affolter <mail@fabian-affolter.ch> - 0.14.0-1
- Update to latest upstream release 0.14.0 (#1512195)

* Sun Oct 01 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.13.0-2
- Fixes and cleanups in spec file

* Sun Oct 01 2017 Fabian Affolter <mail@fabian-affolter.ch> - 0.13.0-1
- Update to latest upstream release 0.13.0 (#1497531)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jul 15 2017 Fabian Affolter <mail@fabian-affolter.ch> - 0.12.0-1
- Update to latest upstream release 0.12.0 (#1471102)

* Wed Jun 28 2017 Fabian Affolter <mail@fabian-affolter.ch> - 0.11.0-1
- Update to latest upstream release 0.11.0 (#1465202)

* Wed Jun 14 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.10.3-1
- Update to 0.10.3 (#1461225)

* Tue May 09 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.10.2-1
- Update to 0.10.2

* Wed Mar 15 2017 Fabian Affolter <mail@fabian-affolter.ch> - 0.10.0-1
- Update to latest upstream release 0.10.0 (#1432279)

* Mon Feb 20 2017 Fabian Affolter <mail@fabian-affolter.ch> - 0.9.8-1
- Update to latest upstream release 0.9.8 (#1423061)

* Thu Feb 16 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.9.6-1
- Update to 0.9.6

* Thu Feb 09 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.9.2-1
- Update to 0.9.2

* Wed Feb 08 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.9.1-1
- Update to 0.9.1

* Tue Feb 07 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.8.1-4
- Fix BRs

* Tue Feb 07 2017 Fabian Affolter <mail@fabian-affolter.ch> - 0.8.1-3
- Update BR

* Fri Jan 27 2017 Fabian Affolter <mail@fabian-affolter.ch> - 0.8.1-2
- Don't remove _quoting.c

* Sat Jan 21 2017 Fabian Affolter <mail@fabian-affolter.ch> - 0.8.1-1
- Update to latest upstream release 0.8.1
- Remove _quoting.c

* Mon Nov 21 2016 Fabian Affolter <mail@fabian-affolter.ch> - 0.7.1-2
- Update Source0, summary

* Fri Nov 18 2016 Fabian Affolter <mail@fabian-affolter.ch> - 0.7.1-1
- Initial package
