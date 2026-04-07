# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global sname urllib-gssapi
%global s_name urllib_gssapi

Name:           python-%{sname}
Version:        1.0.2
Release:        19%{?dist}
Summary:        A GSSAPI/SPNEGO authentication handler for urllib/urllib2

License:        Apache-2.0
URL:            https://github.com/pythongssapi/%{sname}
Source0:        https://github.com/pythongssapi/%{sname}/releases/download/v%{version}/%{s_name}-%{version}.tar.gz
BuildArch:      noarch

# Patches

BuildRequires:  git-core

BuildRequires:  python3-devel
BuildRequires:  python3-gssapi
BuildRequires:  python3-setuptools

%global _description\
urllib_gssapi is a backend for urllib.  It provides GSSAPI/SPNEGO\
authentication to HTTP servers.  urllib_gssapi replaces urllib_kerberos and\
behaves in the same ways.

%description %_description

%package -n python3-%{sname}
Summary:        %summary
Requires:       python3-gssapi
%{?python_provide:%python_provide python3-%{sname}}
%description -n python3-%{sname} %_description

%prep
%autosetup -S git -n %{s_name}-%{version}

%build
%py3_build


%install
%py3_install

%check
%py3_check_import %{s_name}

%files -n python3-%{sname}
%doc README.md
%license COPYING
%{python3_sitelib}/%{s_name}*

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.0.2-19
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.0.2-18
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 1.0.2-16
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.0.2-13
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 1.0.2-9
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.0.2-6
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.0.2-3
- Rebuilt for Python 3.10

* Fri Mar 19 2021 Robbie Harwood <rharwood@redhat.com> - 1.0.2-2
- Drop dependency on python-nose

* Fri Mar 19 2021 Robbie Harwood <rharwood@redhat.com> - 1.0.2-1
- New upstream release (1.0.2)

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.0.1-11
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.0.1-9
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.0.1-8
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Dec 04 2018 Robbie Harwood <rharwood@redhat.com> - 1.0.1-5
- Drop python2 subpackage
- Resolves: #1655258

* Mon Sep 24 2018 Robbie Harwood <rharwood@redhat.com> - 1.0.1-4
- Drop requirement on python-requests
- Resolves: #1631938

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.0.1-2
- Rebuilt for Python 3.7

* Fri Feb 23 2018 Robbie Harwood <rharwood@redhat.com> - 1.0.1-1
- New upstream release (v1.0.0)
- Adds COPYING and removes shebang
- Resolves: #1546835

* Mon Feb 19 2018 Robbie Harwood <rharwood@redhat.com> - 1.0.0-1
- New upstream release (v1.0.0)
