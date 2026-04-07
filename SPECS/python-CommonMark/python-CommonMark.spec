# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pypi_name CommonMark
%global desc Pure Python port of jgm’s stmd.js, a Markdown parser and renderer for the\
CommonMark specification, using only native modules. Once both this project and\
the CommonMark specification are stable we will release the first 1.0 version\
and attempt to keep up to date with changes in stmd.js.\
\
We are currently at the same development stage (actually a bit ahead because we\
have implemented HTML entity conversion and href URL escaping) as stmd.js. Since\
Python versions pre-3.4 use outdated (i.e. not HTML5 spec) entity conversion,\
I’ve converted the 3.4 implementation into a single file, entitytrans.py which\
so far seems to work (all tests pass on 2.7, 3.3, and 3.4).

Name:           python-%{pypi_name}
Version:        0.9.1
Release:        24%{?dist}
Summary:        Python parser for the CommonMark Markdown spec

# Automatically converted from old format: BSD - review is highly recommended.
License:        LicenseRef-Callaway-BSD
URL:            https://pypi.python.org/pypi/%{pypi_name}
Source0:        https://files.pythonhosted.org/packages/60/48/a60f593447e8f0894ebb7f6e6c1f25dafc5e89c5879fdc9360ae93ff83f0/commonmark-0.9.1.tar.gz

Patch0:         0001-Rename-cmark-entrypoint.patch

BuildArch:      noarch

%description
%{desc}

%package utils
Summary:        Command-line tools built using %{name}

%description utils
%{desc}

This package contains the 'commonmark' command.


%package doc
Summary:        Documentation for python-%{pypi_name}

%description doc
%{desc}

Documentation package.


%package -n     python%{python3_pkgversion}-%{pypi_name}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-hypothesis
Suggests:       python-CommonMark-doc
Suggests:       %{name}-utils == %{version}-%{release}
Summary:        %{summary}

%description -n python%{python3_pkgversion}-%{pypi_name}
%{desc}


%prep
%autosetup -p1 -n commonmark-%{version}

# Fix non executable scripts
sed -i '1{\@^#!/usr/bin/env python@d}' commonmark/tests/run_spec_tests.py
sed -i '1{\@^#!/usr/bin/env python@d}' commonmark/cmark.py



%generate_buildrequires
%pyproject_buildrequires



%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l commonmark


%check
%pyproject_check_import

export PYTHONIOENCODING=UTF-8
PYTHONPATH=$(pwd) %{__python3} setup.py test


%files -n python%{python3_pkgversion}-%{pypi_name} -f %{pyproject_files}
%license LICENSE

%files utils
%license LICENSE
%{_bindir}/commonmark

%files doc
%license LICENSE
%doc README.rst spec.txt


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.9.1-24
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.9.1-23
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jul 11 2025 Julien Enselme <jujens@jujens.eu> - 0.9.1-21
- Correct Python macro usages

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 0.9.1-20
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Sep 04 2024 Miroslav Suchý <msuchy@redhat.com> - 0.9.1-18
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.9.1-16
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 0.9.1-12
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.9.1-9
- Rebuilt for Python 3.11

* Tue May 31 2022 FeRD (Frank Dana) <ferdnyc@gmail.com> - 0.9.1-8
- Remove python-future requirement (only required in Python2)

* Sat May 28 2022 FeRD (Frank Dana) <ferdnyc@gmail.com> - 0.9.1-7
- Split out command-line tool to -utils subpackage, rename 'commonmark'
  (bug 1958762)

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.9.1-4
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jul 18 2020 Julien Enselme <jujens@jujens.eu> - 0.9.1-1
- Update to 0.9.1

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.9.0-6
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.9.0-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.9.0-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Jul 13 2019 Julien Enselme <jujens@jujens.eu> - 0.9.0-1
- Update to 0.9.0
- Fix build on Python 3.8

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Nov 18 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.8.1-2
- Drop explicit locale setting
  See https://fedoraproject.org/wiki/Changes/Remove_glibc-langpacks-all_from_buildroot

* Tue Oct 02 2018 Julien Enselme <jujens@jujens.eu> - 0.8.1-1
- Update to 0.8.1
- Remove Python 2 subpackage

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.7.5-2
- Rebuilt for Python 3.7

* Wed Mar 14 2018 Julien Enselme <jujens@jujens.eu> - 0.7.5-1
- Update to 0.7.5

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.7.2-3
- Rebuild for Python 3.6

* Sun Sep 18 2016 Julien Enselme <jujens@jujens.eu> - 0.7.2-2
- Correct encodings in tests

* Sun Sep 18 2016 Julien Enselme <jujens@jujens.eu> - 0.7.2-1
- Update to 0.7.2

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.4-5
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Dec 5 2015 Julien Enselme <jujens@jujens.eu> - 0.5.4-3
- Use only one doc package.
- Use %%summary to avoid summary repetition.
- Use %%__python3 macro to fix shebang.

* Fri Dec 4 2015 Julien Enselme <jujens@jujens.eu> - 0.5.4-2
- Correct shebang of cmark.py (/usr/bin/python2 -> /usr/bin/python3)
- Add doc packages.

* Fri Dec 4 2015 Julien Enselme <jujens@jujens.eu> - 0.5.4-1
- Inital package
