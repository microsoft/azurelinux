%global srcname dbus-signature-pyparsing

Name:           python-%{srcname}
Version:        0.4.1
Release:        10%{?dist}
Summary:        Parser for a D-Bus Signature

License:        Apache-2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/stratis-storage/dbus-signature-pyparsing
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/python-%{srcname}-%{version}.tar.gz
BuildArch:      noarch

%global _description \
%{summary}.

%description %{_description}

%package -n python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%description -n python3-%{srcname} %{_description}

Python 3 version.

%prep
%autosetup -n %{srcname}-%{version}

%build
%py3_build

%install
%py3_install

%files -n python3-%{srcname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/dbus_signature_pyparsing/
%{python3_sitelib}/dbus_signature_pyparsing-*.egg-info/

%changelog
* Mon Dec 23 2024 Akhila Guruju <v-guakhila@microsoft.com> - 0.4.1-10
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified.

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.4.1-8
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 0.4.1-4
- Rebuilt for Python 3.12

* Sun May 7 2023 mulhern<amulhern@redhat.com> - 0.4.3
- Fix up testing plan tag

* Sun May 7 2023 mulhern<amulhern@redhat.com> - 0.4.2
- Fix up testing plan

* Sun May 7 2023 mulhern<amulhern@redhat.com> - 0.4.1
- Update to 0.4.1

* Wed Apr 26 2023 mulhern<amulhern@redhat.com> - 0.04-15
- Checkout tests from HEAD revision

* Wed Apr 26 2023 mulhern<amulhern@redhat.com> - 0.04-14
- Include .fmf metadata

* Wed Apr 26 2023 mulhern<amulhern@redhat.com> - 0.04-13
- Use TMT instead of STI format gating tests; make license spec match upstream

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.04-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.04-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jul 19 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.04-10
- Rebuilt for pyparsing-3.0.9

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.04-9
- Rebuilt for Python 3.11

* Tue Feb 15 2022 mulhern <amulhern@redhat.com> - 0.04-8
- Remove %check

* Tue Feb 15 2022 mulhern <amulhern@redhat.com> - 0.04-7
- Add gating tests

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.04-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 28 2021 mulhern <amulhern@redhat.com> - 0.04-5
  Remove redundant requires

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.04-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.04-3
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.04-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Dec 03 2020 mulhern <amulhern@redhat.com> - 0.04-1
  Update to 0.04

* Tue Aug 04 2020 mulhern <amulhern@redhat.com> - 0.03-14
  Run check with deterministic tests only

* Tue Aug 04 2020 mulhern <amulhern@redhat.com> - 0.03-13
  Rebuild to pass non-deterministic tests on very slow machine

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.03-12
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.03-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.03-10
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.03-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.03-8
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.03-7
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.03-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.03-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.03-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.03-3
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.03-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 08 2018 Ilya Gradina <ilya.gradina@gmail.com> - 0.03-1
- Initial package
