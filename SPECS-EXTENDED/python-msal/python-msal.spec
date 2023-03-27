%global         srcname         msal
%global         forgeurl        https://github.com/AzureAD/microsoft-authentication-library-for-python/
%global         pypi_version    1.18.0b1
%global         tag             %{pypi_version}

# Most of the tests require network access, so they are disabled by default.
%bcond_with     tests

Vendor:         Microsoft Corporation
Distribution:   Mariner
Version:        1.18.0~b1
Name:           python-%{srcname}
Release:        3%{?dist}
Summary:        Microsoft Authentication Library (MSAL) for Python

License:        MIT
URL:            %forgeurl
Source0:        https://github.com/AzureAD/microsoft-authentication-library-for-python/archive/%{pypi_version}/microsoft-authentication-library-for-python-%{pypi_version}.tar.gz#/%{name}-%{pypi_version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-packaging
BuildRequires:  python3-requests
BuildRequires:  python3-wheel

%if %{with_check}
BuildRequires:  python3dist(pytest)
%endif

%global _description %{expand:
The Microsoft Authentication Library for Python
enables applications to integrate with the Microsoft identity platform. It
allows you to sign in users or apps with Microsoft identities (Azure AD,
Microsoft Accounts and Azure AD B2Caccounts) and obtain tokens to call Microsoft
APIs such as Microsoft Graph or your own APIs registered with the Microsoft
identity platform. It is built using industry standard OAuth2 and OpenID Connect
protocols.}

%description %{_description}


%package -n python3-%{srcname}
Summary:        %{summary}
%description -n python3-%{srcname} %{_description}


%prep
%autosetup -p1 -n microsoft-authentication-library-for-python-%{pypi_version}


%generate_buildrequires
%pyproject_buildrequires -r


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files msal


%check
%pytest --disable-warnings tests


%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.md


%changelog
* Wed Mar 15 2023 Muhammad Falak <mwani@microsoft.com> - 1.18.0~b1-3
- Rename Source0 to `%{name}-%{version}.extension

* Fri Mar 03 2023 Muhammad Falak <mwani@microsoft.com> - 1.18.0~b1-2
- Convert 'Release' tag to '[number].[distribution]' format
- Initial CBL-Mariner import from Fedora 36 (license: MIT).
- License verified

* Tue May 24 2022 Major Hayden <major@mhtx.net> 1.18.0~b1-1
- Update to 1.18.0~b1

* Fri Feb 11 2022 Major Hayden <major@mhtx.net> 1.17.0-1
- Update to 1.17.0

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> 1.16.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Dec 15 2021 Major Hayden <major@mhtx.net> 1.16.0-1
- Update to 1.16.0

* Fri Nov 12 2021 Major Hayden <major@mhtx.net> 1.15.0-2
- Remove docs

* Mon Oct 04 2021 Major Hayden <major@mhtx.net> 1.15.0-1
- 🚀 Update to 1.15.0

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> 1.13.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 21 2021 Major Hayden <major@mhtx.net> 1.13.0-1
- Update to 1.13.0

* Tue Jul 06 2021 Major Hayden <major@mhtx.net> 1.12.0-4
- Fix lato font requirement

* Thu Jun 10 2021 Stephen Gallagher <sgallagh@redhat.com> 1.12.0-3
- Fix conditional to work when %%fedora is not defined

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> 1.12.0-2
- Rebuilt for Python 3.10

* Fri Jun 04 2021 Mohamed El Morabity <melmorabity@fedoraproject.org> 1.12.0-1
- Update to 1.12.0

* Sun Mar 21 2021 Mohamed El Morabity <melmorabity@fedoraproject.org> 1.10.0-2
- Fix doc. build + disable online unit tests

* Sun Mar 21 2021 Mohamed El Morabity <melmorabity@fedoraproject.org> 1.10.0-1
- Update to 1.10.0

* Mon Feb 15 2021 Mohamed El Morabity <melmorabity@fedoraproject.org> 1.8.0-1
- Update to 1.8.0

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> 1.4.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 08 2021 Tom Stellard <tstellar@redhat.com> 1.4.3-3
- Add BuildRequires: make

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> 1.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jul 25 2020 Mohamed El Morabity <melmorabity@fedoraproject.org> 1.4.3-1
- Update to 1.4 3

* Fri Jul 24 2020 Mohamed El Morabity <melmorabity@fedoraproject.org> 1.4.2-1
- Update to 1.4.2

* Sat Jun 27 2020 Mohamed El Morabity <melmorabity@fedoraproject.org> 1.4.1-1
- Update to 1.4.1

* Sun May 31 2020 Mohamed El Morabity <melmorabity@fedoraproject.org> 1.3.0-2
- Rebuild for Python 3.9

* Fri May 29 2020 Mohamed El Morabity <melmorabity@fedoraproject.org> 1.3.0-1
- First import
