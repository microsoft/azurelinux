Name:           python-soupsieve
Version:        2.6
Release:        3%{?dist}
Summary:        CSS selector library
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%bcond_with tests

License:        MIT
URL:            https://github.com/facelessuser/soupsieve
Source0:        https://github.com/facelessuser/soupsieve/archive/%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel           
BuildRequires:  python3dist(wheel)
BuildRequires:  python3-pytest
BuildRequires:  python3-lxml
BuildRequires:  python3-html5lib
BuildRequires:  python3-pip
BuildRequires:  python3-hatchling
BuildRequires:  python3-pathspec
BuildRequires:  python3-trove-classifiers


%global _description %{expand:
Soup Sieve is a CSS selector library designed to be used with Beautiful Soup 4.
It aims to provide selecting, matching, and filtering using modern CSS
selectors. Soup Sieve currently provides selectors from the CSS level 1
specifications up through the latest CSS level 4 drafts and beyond (though some
are not yet implemented).

Soup Sieve was written with the intent to replace Beautiful Soup's builtin
select feature, and as of Beautiful Soup version 4.7.0, it now is. Soup Sieve
can also be imported in order to use its API directly for more controlled,
specialized parsing.

Soup Sieve has implemented most of the CSS selectors up through the latest CSS
draft specifications, though there are a number that don't make sense in a
non-browser environment. Selectors that cannot provide meaningful functionality
simply do not match anything.}

%description %_description

%package -n python3-soupsieve
Summary:        %{summary}

%description -n python3-soupsieve %_description

%prep
%autosetup -n soupsieve-%{version}

# Do not run coverage report during check
sed -i -e '/coverage/d' -e '/pytest-cov/d' requirements/tests.txt

%generate_buildrequires
%pyproject_buildrequires -w %{?with_tests:-r requirements/tests.txt}

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files soupsieve

%if %{with tests}
%check
%pytest -v
%endif

%files -n python3-soupsieve -f %{pyproject_files}
%license LICENSE.md
%doc README.md
/usr/lib/python3.12/site-packages/soupsieve-2.6.dist-info/licenses/LICENSE.md

%changelog
* Fri Feb 21 2025 Akarsh Chaudhary <v-akarshc@microsoft.com> - 2.6-3
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified

* Tue Aug 13 2024 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.6-2
- Reenable tests that were failing with Python 3.10

* Tue Aug 13 2024 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.6-1
- Version 2.6 (rhbz#2304326)

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 2.5-5
- Rebuilt for Python 3.13

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 2.5-4
- Bootstrap for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Sep 06 2023 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.5-1
- Version 2.5 (rhbz#2236980)

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 29 2023 Python Maint <python-maint@redhat.com> - 2.4.1-6
- Rebuilt for Python 3.12

* Mon Jun 26 2023 Python Maint <python-maint@redhat.com> - 2.4.1-5
- Bootstrap for Python 3.12

* Fri Jun 16 2023 Python Maint <python-maint@redhat.com> - 2.4.1-4
- Rebuilt for Python 3.12

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 2.4.1-3
- Bootstrap for Python 3.12

* Mon May 29 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 2.4.1-2
- Avoid tox dependency

* Sat May 20 2023 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.4.1-1
- Version 2.4.1 (rhbz#2187123)

* Wed Feb 22 2023 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.4-1
- Version 2.4 (rhbz#2169774)

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2.post1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2.post1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jul 11 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2.3.2.post1-6
- Explicitly list the license file

* Mon Jul 11 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2.3.2.post1-5
- Fix pyproject_buildrequires invocation for hatchling backend

* Mon Jul 11 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2.3.2.post1-4
- Remove obsolete workaround for rhbz#1985340

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 2.3.2.post1-3
- Rebuilt for Python 3.11

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 2.3.2.post1-2
- Bootstrap for Python 3.11

* Fri Apr 22 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.3.2.post1-1
- Version 2.3.2.post1 (rhbz#2072609)

* Tue Feb 08 2022 Miro Hrončok <miro@hroncok.cz> - 2.3.1-4
- Remove deprecated and redundant %%python_provide call

* Tue Feb 08 2022 Steve Traylen <steve.traylen@cern.ch> - 2.3.1-3
- Convert to pyproject macros

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Nov 13 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.3.1-1
- Version 2.3.1 (fixes #2022380)

* Sun Nov 07 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.3-1
- Version 2.3 (fixes #2019960)

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun  9 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.2.1-1
- Update to latest bugfix version

* Thu Jun 03 2021 Python Maint <python-maint@redhat.com> - 2.2-3
- Rebuilt for Python 3.10

* Thu Jun 03 2021 Python Maint <python-maint@redhat.com> - 2.2-2
- Bootstrap for Python 3.10

* Sat Feb 13 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.2-1
- Latest version (#1927002)

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan 07 2021 Joel Capitao <jcapitao@redhat.com> - 2.1.0-1
- Update to 2.1.0 (#1906625)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 26 2020 Charalampos Stratakis <cstratak@redhat.com> - 2.0.1-1
- Update to 2.0.1 (#1814999)

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 1.9.2-6
- Rebuilt for Python 3.9

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 1.9.2-5
- Bootstrap for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Sep 03 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.9.2-3
- Subpackage python2-soupsieve has been removed (#1748298)

* Mon Aug 19 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.9.2-2
- Rebuilt for Python 3.8

* Mon Jun 10 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.9.2-1
- Initial packaging
