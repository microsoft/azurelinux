Vendor:         Microsoft Corporation
Distribution:   Mariner
%bcond_with tests

Name:           python-soupsieve
Version:        1.9.2
Release:        5%{?dist}
Summary:        CSS selector library

License:        MIT
URL:            https://github.com/facelessuser/soupsieve
Source0:        https://github.com/facelessuser/soupsieve/archive/%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel
%if %{with tests}
BuildRequires:  python3-pytest
BuildRequires:  python3dist(lxml)
BuildRequires:  python3dist(html5lib)
BuildRequires:  python3dist(beautifulsoup4)
%endif

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
%{?python_provide:%python_provide python3-soupsieve}

%description -n python3-soupsieve %_description

%prep
%autosetup -n soupsieve-%{version}

%build
%py3_build

%install
%py3_install

%if %{with tests}
%check
pytest-3 -v tests -k 'not test_namespace_xml_with_namespace'
%endif

%files -n python3-soupsieve
%{python3_sitelib}/soupsieve/
%{python3_sitelib}/soupsieve-%{version}-py%{python3_version}.egg-info/
%doc README.md
%license LICENSE.md

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.9.2-5
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Sep 03 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.9.2-3
- Subpackage python2-soupsieve has been removed (#1748298)

* Mon Aug 19 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.9.2-2
- Rebuilt for Python 3.8

* Mon Jun 10 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.9.2-1
- Initial packaging
