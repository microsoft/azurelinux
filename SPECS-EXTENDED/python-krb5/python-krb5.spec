Vendor:		Microsoft Corporation
Distribution:	Azure Linux

Name:           python-krb5
Version:        0.7.1
Release:        %3{?dist}
Summary:        Kerberos API bindings for Python
License:        MIT
URL:            https://github.com/jborean93/pykrb5
Source:         https://github.com/jborean93/pykrb5/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  krb5-devel
BuildRequires:  krb5
BuildRequires:	python3-pytest
BuildRequires:	python3-dist
BuildRequires:	python3-cython
BuildRequires:	python3-tomli
BuildRequires:	python3-packaging
BuildRequires:	python3-pip
BuildRequires:	python3-wheel



%global _description %{expand:
This library provides Python functions that wraps the Kerberos 5 C API.  Due to
the complex nature of this API it is highly recommended to use something like
python-gssapi which exposes the Kerberos authentication details through GSSAPI.}


%description %_description


%package -n python3-krb5
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  python3-pytest
BuildRequires:  python3-k5test


%description -n python3-krb5 %_description


%prep
%autosetup -p 1 -n krb5-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l krb5


%check
%pytest --verbose


%files -n python3-krb5 -f %{pyproject_files}
%doc README.md


%changelog
* Mon Sep 15 2025 Andy Zaugg <azaugg@linkedin.com> - 0.7.1-4
- Initial AzureLinux import from Fedora 41 (license: MIT).
- License verified.

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.7.1-3
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jul 17 2025 Jonathan Billings <jsbillings@fedoraproject.org> - 0.7.1-1
- Update to version 0.7.1 rhbz#2350223

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 0.7.0-3
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Oct 20 2024 Carl George <carlwgeorge@fedoraproject.org> - 0.7.0-1
- Update to version 0.7.0 rhbz#2320054

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.5.1-5
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Sep 28 2023 Carl George <carlwgeorge@fedoraproject.org> - 0.5.1-2
- Run test suite

* Wed Sep 13 2023 Carl George <carlwgeorge@fedoraproject.org> - 0.5.1-1
- Initial package, resolves rhbz#2238652
