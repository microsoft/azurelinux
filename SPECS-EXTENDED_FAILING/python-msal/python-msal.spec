Vendor:         Microsoft Corporation
Distribution:   Mariner
%global srcname msal
%global _description %{expand:The Microsoft Authentication Library for Python enables applications to
integrate with the Microsoft identity platform. It allows you to sign in users
or apps with Microsoft identities (Azure AD, Microsoft Accounts and Azure AD B2C
accounts) and obtain tokens to call Microsoft APIs such as Microsoft Graph or
your own APIs registered with the Microsoft identity platform. It is built using
industry standard OAuth2 and OpenID Connect protocols.}

Name:           python-%{srcname}
Version:        1.4.3
Release:        3%{?dist}
Summary:        Microsoft Authentication Library (MSAL) for Python

License:        MIT
URL:            https://github.com/AzureAD/microsoft-authentication-library-for-python/
Source0:        %{url}/archive/%{version}/%{srcname}-%{version}.tar.gz

BuildRequires:  python3-devel
BuildRequires:  %{py3_dist setuptools}
# Required for tests
BuildRequires:  %{py3_dist pyjwt}
BuildRequires:  %{py3_dist pytest}
BuildRequires:  %{py3_dist requests}
# Required for documentation
BuildRequires:  fontpackages-devel
BuildRequires:  %{py3_dist sphinx}
BuildRequires:  %{py3_dist sphinx-rtd-theme}
BuildArch:      noarch

%description
%{_description}


%package -n python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
%{_description}


%package doc
Summary:        Documentation for %{name}
Requires:       google-roboto-slab-fonts
Requires:       lato-fonts
Requires:       fontawesome-fonts
Requires:       fontawesome-fonts-web

%description doc
This package provides documentation for %{name}.


%prep
%autosetup -n microsoft-authentication-library-for-python-%{version}

# Remove bundled egg-info
rm -rf *.egg-info


%build
%py3_build

%make_build -C docs/ html
rm docs/_build/html/{.buildinfo,.nojekyll}


%install
%py3_install

# Drop bundled web fonts in HTML documentation
pushd docs/_build/html/_static/fonts/
rm -f fontawesome-webfont.*
ln -s %{_fontbasedir}/fontawesome/fontawesome-webfont.* .

pushd Lato/
rm -f *.ttf
for i in Bold BoldItalic Italic Regular; do
    ln -s %{_fontbasedir}/lato/Lato-$i.ttf lato-${i,,}.ttf
done
popd

pushd RobotoSlab/
rm -f *.ttf
for i in Bold Regular; do
    ln -s %{_fontbasedir}/google-roboto-slab/RobotoSlab-$i.ttf roboto-slab-v7-${i,,}.ttf
done
popd
popd


%check
# Tests requiring an Internet connection are disabled
pytest-%{python3_version} \
    --deselect=tests/test_application.py::TestClientApplicationAcquireTokenSilentFociBehaviors \
    --deselect=tests/test_application.py::TestClientApplicationAcquireTokenSilentErrorBehaviors \
    --deselect=tests/test_application.py::TestClientApplicationForAuthorityMigration::test_acquire_token_silent \
    --deselect=tests/test_application.py::TestClientApplicationForAuthorityMigration::test_get_accounts \
    --deselect=tests/test_authority.py::TestAuthority::test_unknown_host_wont_pass_instance_discovery \
    --deselect=tests/test_authority.py::TestAuthority::test_wellknown_host_and_tenant \
    --deselect=tests/test_authority.py::TestAuthorityInternalHelperUserRealmDiscovery::test_memorize \
    --deselect=tests/test_authority_patch.py::TestAuthorityHonorsPatchedRequests::test_authority_honors_a_patched_requests


%files -n python3-%{srcname}
%doc README.md
%license LICENSE
%{python3_sitelib}/%{srcname}/
%{python3_sitelib}/%{srcname}-*.egg-info/


%files doc
%doc docs/_build/html/
%license LICENSE


%changelog
* Fri Feb 25 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.4.3-3
- Updating installation steps.
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.4.3-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Sat Jul 25 2020 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.4.3-1
- Update to 1.4.3

* Fri Jul 24 2020 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.4.2-1
- Update to 1.4.2

* Sat Jun 27 2020 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.4.1-1
- Update to 1.4.1
- Enable tests
- Add documentation subpackage

* Fri May 29 2020 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.3.0-1
- Initial RPM release
