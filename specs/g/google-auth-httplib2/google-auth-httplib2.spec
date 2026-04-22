# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global sum An httplib2 transport for google-auth
%global srcname google-auth-httplib2

Name:           google-auth-httplib2
Summary:        %{sum}
Version:        0.2.1
Release: 2%{?dist}

License:        Apache-2.0
URL:            https://github.com/googleapis/google-auth-library-python-httplib2
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
BuildArch:      noarch

%description 
httplib has lots of problems such as lack of threadsafety and insecure usage
of TLS. Using it is highly discouraged. This library is intended to help
existing users of oauth2client migrate to google-auth.

%package -n python3-%{srcname}
Summary:        %{sum}

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros

%description -n python3-%{srcname}
Written by Google, this library provides a small, flexible, and powerful 
Python 3 client library for accessing Google APIs.

%prep
%autosetup -n google-auth-library-python-httplib2-%{version}

%generate_buildrequires
%pyproject_buildrequires -r

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files google_auth_httplib2

%files -n python3-%{srcname} -f %{pyproject_files}
%license LICENSE 
%doc README.rst

%changelog
* Fri Oct 31 2025 Gwyn Ciesla <gwync@protonmail.com> - 0.2.1-1
- 0.2.1

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.2.0-10
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.2.0-9
- Rebuilt for Python 3.14.0rc2 bytecode

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 0.2.0-7
- Rebuilt for Python 3.14

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.2.0-4
- Rebuilt for Python 3.13

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Dec 12 2023 Gwyn Ciesla <gwync@protonmail.com> - 0.2.0-1
- 0.2.0

* Mon Sep 11 2023 Gwyn Ciesla <gwync@protonmail.com> - 0.1.1-1
- 0.1.1

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 0.1.0-7
- Rebuilt for Python 3.12

* Sun Mar 05 2023 Gwyn Ciesla <gwync@protonmail.com> - 0.1.0-6
- migrated to SPDX license

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jun 16 2022 Python Maint <python-maint@redhat.com> - 0.1.0-3
- Rebuilt for Python 3.11

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Oct 25 2021 Mikel Olasagasti Uranga <mikel@olasagasti.info> - 0.1.0-1
- Version bump and switch to pyproject-rpm-macros

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.0.3-4
- Rebuilt for Python 3.10

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon May 04 2020 Gwyn Ciesla <gwync@protonmail.com> - 0.0.3-1
- Initial build

