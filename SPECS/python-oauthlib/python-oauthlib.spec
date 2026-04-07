# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# RHEL does not include pyjwt, blinker needed for extras
%bcond extras %{undefined rhel}

Name:               python-oauthlib
Version:            3.2.2
Release:            10%{?dist}
Summary:            An implementation of the OAuth request-signing logic

License:            BSD-3-Clause
URL:                https://github.com/oauthlib/oauthlib

Source0:            https://github.com/oauthlib/oauthlib/archive/v%{version}/%{name}-%{version}.tar.gz

# Make UtilsTests.test_filter_params Python 3.13+ compatible
Patch:              https://github.com/oauthlib/oauthlib/pull/866.patch

BuildArch:          noarch

%description
OAuthLib is a generic utility which implements the logic of OAuth without
assuming a specific HTTP request object or web framework. Use it to graft
OAuth client support onto your favorite HTTP library, or provider support
onto your favourite web framework. If you're a maintainer of such a
library, write a thin veneer on top of OAuthLib and get OAuth support for
very little effort.

%package -n python3-oauthlib
Summary:            %{summary}

BuildRequires:      python3-devel
BuildRequires:      python3-pytest

%description -n python3-oauthlib
OAuthLib is a generic utility which implements the logic of OAuth without
assuming a specific HTTP request object or web framework. Use it to graft
OAuth client support onto your favorite HTTP library, or provider support
onto your favourite web framework. If you're a maintainer of such a
library, write a thin veneer on top of OAuthLib and get OAuth support for
very little effort.

%if %{with extras}
%pyproject_extras_subpkg -n python3-oauthlib rsa,signedtoken,signals
%endif

%prep
%autosetup -n oauthlib-%{version} -p1

%generate_buildrequires
%pyproject_buildrequires %{?with_extras:-x rsa,signedtoken,signals}

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files oauthlib

%check
# enable SHA-1 signatures for RSA tests
# also see https://github.com/pyca/cryptography/pull/6931 and rhbz#2060343
export OPENSSL_ENABLE_SHA1_SIGNATURES=yes
%if %{without extras}
echo 'import pytest; __getattr__ = lambda _: pytest.skip("this test needs jwt")' > jwt.py
%endif
%{pytest} \
%if %{without extras}
  --ignore tests/oauth2/rfc6749/clients/test_service_application.py \
  --ignore tests/oauth2/rfc6749/clients/test_web_application.py \
  --ignore tests/oauth2/rfc6749/clients/test_mobile_application.py \
  --ignore tests/oauth2/rfc6749/clients/test_legacy_application.py \
  --ignore tests/oauth2/rfc6749/clients/test_backend_application.py \
  --ignore tests/oauth2/rfc6749/test_parameters.py \
%endif
  %{nil}

%files -n python3-oauthlib -f %{pyproject_files}
%doc README.rst

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 3.2.2-10
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 3.2.2-9
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 3.2.2-7
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 3.2.2-4
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Sep 19 2023 Michel Lind <salimma@fedoraproject.org> - 3.2.2-1
- Update to 3.2.2 for CVE-2022-36087
- Fix FTBFS with Python 3.12 (rhbz#2192914)

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 3.2.1-5
- Rebuilt for Python 3.12

* Mon May 08 2023 Major Hayden <major@redhat.com> - 3.2.1-4
- Migrated to SPDX license

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Dec 13 2022 Major Hayden <major@redhat.com> - 3.2.1-2
- Add SHA1 signature fix for ELN from yselkowitz. 👏

* Mon Sep 12 2022 Dariusz Smigiel <dsmigiel@redhat.com) - 3.2.1-1
- Update spec file and sources for 3.2.1
- Fixes CVE-2022-36087

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 14 2022 Python Maint <python-maint@redhat.com> - 3.2.0-2
- Rebuilt for Python 3.11

* Thu Mar 24 2022 Michael Kelly <mkelly@arista.com> - 3.2.0-1
- Remove python-mock patches (not required in 3.2.0)
- Update spec file and sources for 3.2.0

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 03 2021 Python Maint <python-maint@redhat.com> - 3.0.2-10
- Rebuilt for Python 3.10

* Mon May 10 2021 Jakub Hrozek <jhrozek@redhat.com> - 3.1.0-2
- Don't use python-mock
- Use an actual URL as Source0 (thanks, churchyard)

* Mon Feb  8 2021 Jakub Hrozek <jhrozek@redhat.com> - 3.1.0-1
- Update to upstream 3.1.0
- Gets rid of obsolete python-nose dependency
- Nuke the python2/python3 conditionals, let's only support python3

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 10 2020 Miro Hrončok <mhroncok@redhat.com> - 3.0.2-7
- Add oauthlib[signedtoken] subpackage

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 3.0.2-6
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 3.0.2-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 3.0.2-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 15 2019  <jdennis@redhat.com> - 3.0.2-1
- Update to upstream 3.0.2
- Resolves: rhbz#1730033

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Aug  3 2018  <jdennis@redhat.com> - 2.1.0-1
- upgrade to latest upstream 2.1.0

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018  <jdennis@redhat.com> - 2.0.1-10
- Restore use of bcond for python conditionals

* Tue Jul 10 2018  <jdennis@redhat.com> - 2.0.1-9
- Unify spec file between Fedora and RHEL

* Fri Jun 15 2018 Miro Hrončok <mhroncok@redhat.com> - 2.0.1-8
- Rebuilt for Python 3.7

* Mon Feb 12 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2.0.1-7
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Sep 29 2017 Troy Dawson <tdawson@redhat.com> - 0.7.19-5
- Cleanup spec file conditionals

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Apr 17 2017 John Dennis <jdennis@redhat.com> - 2.0.1-3
- fix dependency on python2-jwt, should be python-jwt

* Thu Apr 13 2017 Dennis Gilmore <dennis@ausil.us> - 2.0.1-2
- add spaces around the >= for Requires

* Thu Mar 16 2017 John Dennis <jdennis@redhat.com> - 2.0.1-1
- Upgrade to upstream 2.0.1
- port from jwt to jwcrypto (conditional build)
- bring into alignment with rhel spec file

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec 13 2016 Stratakis Charalampos <cstratak@redhat.com> - 1.0.3-4
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue Jun 28 2016 Ralph Bean <rbean@redhat.com> - 1.0.3-2
- Modernize python macros.

* Sun Apr 10 2016 Kevin Fenzi <kevin@scrye.com> - 1.0.3-1
- Update to 1.0.3
- Add python2 provides (fixes bug #1313235 and #1314349)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.2-5.20150520git514cad7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2-4.20150520git514cad7
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2-3.20150520git514cad7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Feb 18 2015 Ralph Bean <rbean@redhat.com> - 0.7.2-2.20150520git514cad7
- new version, from a git checkout
- Replace our patch with a sed statement.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Fri Apr 11 2014 Ralph Bean <rbean@redhat.com> - 0.6.0-4
- Use forward-compat python-crypto2.6 package for el6.

* Tue Jan 21 2014 Ralph Bean <rbean@redhat.com> - 0.6.0-3
- Compat macros for el6.

* Fri Nov 01 2013 Ralph Bean <rbean@redhat.com> - 0.6.0-2
- Modernized python2 rpmmacros.

* Thu Oct 31 2013 Ralph Bean <rbean@redhat.com> - 0.6.0-1
- Initial package for Fedora
