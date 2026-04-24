# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Not packaged: python-pyjwt
%bcond pyjwt 0
# Not packaged: python-pyu2f
%bcond reauth 0
# Since grpc is a challenging package, it’s helpful to maintain the ability to
# break this dependency.

%if 0%{?rhel}
%bcond grpcio 0
%bcond tests 0
%else
%bcond grpcio 1
%bcond tests 1
%endif

%bcond pytest_localserver %[ %{undefined el10} && %{undefined el9} ]

Name:           python-google-auth
Version:        2.45.0
Release: 2%{?dist}
Epoch:          1
Summary:        Google Authentication Library

License:        Apache-2.0
URL:            https://github.com/googleapis/google-auth-library-python
Source:         %{url}/archive/v%{version}/google-auth-library-python-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel

%if %{with grpcio}
# For import-checking google.auth.transport.grpc; see also
# https://github.com/googleapis/google-auth-library-python/issues/1735.
BuildRequires:  %{py3_dist grpcio}
%endif

%if %{with tests}
# Some tests in tests/transport/test_requests.py and
# tests/transport/test_urllib3.py require this.
BuildRequires:  %{py3_dist certifi}
%endif

%global common_description %{expand:
This library simplifies using Google’s various server-to-server authentication
mechanisms to access Google APIs.}

%description %{common_description}


%package -n python3-google-auth
Summary:       %{summary}

%description -n python3-google-auth %{common_description}


%pyproject_extras_subpkg -n python3-google-auth aiohttp
%pyproject_extras_subpkg -n python3-google-auth enterprise_cert
%pyproject_extras_subpkg -n python3-google-auth pyopenssl
%if %{with pyjwt}
%pyproject_extras_subpkg -n python3-google-auth pyjwt
%endif
%if %{with reauth}
%pyproject_extras_subpkg -n python3-google-auth reauth
%endif
%pyproject_extras_subpkg -n python3-google-auth requests
%pyproject_extras_subpkg -n python3-google-auth urllib3


%prep
%autosetup -n google-auth-library-python-%{version}

# use unittest.mock instead of mock
# https://github.com/googleapis/google-auth-library-python/issues/1055
#
# Needed for https://fedoraproject.org/wiki/Changes/DeprecatePythonMock.
#
# See also https://github.com/googleapis/google-auth-library-python/pull/1786,
# https://github.com/googleapis/google-auth-library-python/pull/1361, but these
# are out of date and upstream has failed to act for months, so we use a more
# “dynamic” sed-patch to avoid constant rebasing
find tests* system_tests -type f -name '*.py' -exec \
    sed -r -i -e 's/^(from )(mock)\b/\1unittest\.\2/' \
        -e 's/^(import mock)/from unittest \1/' '{}' '+'
sed -r -i 's/^([[:blank:]]*)("mock",)$/\1# \2/' setup.py

# Upstream expands dependencies for extras into the testing extra. Omit any
# missing extras from the testing extra.
%if %{without pyjwt}
sed -r -i 's/^([[:blank:]]*)(\*pyjwt_extra_require,)$/\1# \2/' setup.py
%endif
%if %{without reauth}
sed -r -i 's/^([[:blank:]]*)(\*reauth_extra_require,)$/\1# \2/' setup.py
%endif

%if %{without pytest_localserver}
sed -r -i 's/^([[:blank:]]*)("pytest-localserver\b[^"]*",)$/\1# \2/' setup.py
%endif

# We cannot respect version upper bounds that were added for testing:
#   "pyopenssl < 24.3.0",
#   "aiohttp < 3.10.0",
sed -r -i 's/^([[:blank:]]*"(pyopenssl|aiohttp))\b[^"]+(",)$/\1\3/' setup.py

%if %{defined el9}
# We must loosen the lower bound on the cryptography version.
sed -r -i 's/^([[:blank:]]*"cryptography) >= [^"]+(",)$/\1\2/' setup.py
%endif


%generate_buildrequires
%{pyproject_buildrequires \
  -x aiohttp \
  -x enterprise_cert \
  -x pyopenssl \
%if %{with pyjwt}
  -x pyjwt \
%endif
%if %{with reauth}
  -x reauth \
%endif
  -x requests \
%if %{with tests}
  -x testing \
%endif
  -x urllib3}


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l google


%check
%if %{with grpcio}
%pyproject_check_import
%else
%pyproject_check_import -e google.auth.transport.grpc
%endif

%if %{with tests}
# Requires python-google-cloud-storage, which we don’t really want to add as a
# build dependency.
ignore="${ignore-} --ignore=samples/cloud-client/snippets/snippets_test.py"

# Require additional test data files not in the repository:
ignore="${ignore-} --ignore=system_tests"

%if %{without pyjwt}
k="${k-}${k+ and }not test_verify_token_jwk"
%endif

%if %{without reauth}
ignore="${ignore-} --ignore=tests/oauth2/test_challenges.py"
%endif

%if %{without pytest_localserver}
ignore="${ignore-} --ignore=tests/transport/compliance.py"
ignore="${ignore-} --ignore=tests/transport/test__http_client.py"
ignore="${ignore-} --ignore=tests/transport/test_requests.py"
ignore="${ignore-} --ignore=tests/transport/test_urllib3.py"
ignore="${ignore-} --ignore=tests_async/transport/async_compliance.py"
ignore="${ignore-} --ignore=tests_async/transport/test_aiohttp_requests.py"
%endif

# TODO: What would it take to fix these?
#   >       loop = loop or asyncio.get_running_loop()
#   E       RuntimeError: no running event loop
k="${k-}${k+ and }not (TestRequestResponse and test_unsupported_session)"
k="${k-}${k+ and }not (TestAuthorizedSession and test_constructor)"
k="${k-}${k+ and }not (TestAuthorizedSession and test_constructor_with_auth_request)"

# TestDecryptPrivateKey::test_success fails with pyOpenSSL 24.3.0+ #1665
# https://github.com/googleapis/google-auth-library-python/issues/1665
k="${k-}${k+ and }not (TestDecryptPrivateKey and test_success)"

%if %{defined el9}
# TODO: We have not tried to investigate these EPEL9-specific failures.

#   ERROR at teardown of TestAsyncAuthorizedSession.test_request_provided_auth_request_success _
#   […]
#   E           ValueError: Async generator fixture didn't stop.Yield only once.
k="${k-}${k+ and }not (TestAsyncAuthorizedSession and test_request_provided_auth_request_success)"

# E           TypeError: object bool can't be used in 'await' expression
k="${k-}${k+ and }not (TestTimeoutGuard and test_timeout_with_simple_async_task_within_bounds)"
# E           TypeError: object Mock can't be used in 'await' expression
k="${k-}${k+ and }not (TestAsyncAuthorizedSession and test_http_delete_method_success)"
k="${k-}${k+ and }not (TestAsyncAuthorizedSession and test_http_get_method_success)"
k="${k-}${k+ and }not (TestAsyncAuthorizedSession and test_http_patch_method_success)"
k="${k-}${k+ and }not (TestAsyncAuthorizedSession and test_http_post_method_success)"
k="${k-}${k+ and }not (TestAsyncAuthorizedSession and test_http_put_method_success)"
k="${k-}${k+ and }not (TestAsyncAuthorizedSession and test_request_default_auth_request_success)"
# E       TypeError: 'async for' requires an object with __aiter__ method, got bytes
k="${k-}${k+ and }not (TestAsyncAuthorizedSession and test_request_provided_auth_request_success)"
%endif

%pytest ${ignore-} -k "${k-}" -v
%endif


%files -n python3-google-auth -f %{pyproject_files}


%changelog
* Tue Dec 16 2025 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:2.45.0-1
- Update to 2.45.0 (#2422343)

* Tue Nov 11 2025 Jason Montleon <jmontleo@redhat.com> - 1:2.43.0-1
- Update to 2.43.0 (#2413000)

* Thu Oct 30 2025 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:2.42.1-1
- Update to 2.42.1 (#2406878)

* Sun Oct 19 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1:2.41.1-2
- Migrate to pyproject-rpm-macros (fix RHBZ#2377753)
- Add missing extras metapackages
- Run the tests

* Wed Oct 01 2025 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:2.41.1-1
- Update to 2.41.1 (#2400572)

* Mon Sep 29 2025 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:2.41.0-1
- Update to 2.41.0 (#2400375)

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1:2.40.3-6
- Rebuilt for Python 3.14.0rc3 bytecode

* Sat Aug 30 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1:2.40.3-5
- Patch to allow cachetools 6; fixes RHBZ#2390999, fixes RHBZ#2391729

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1:2.40.3-4
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.40.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jun 06 2025 Python Maint <python-maint@redhat.com> - 1:2.40.3-2
- Rebuilt for Python 3.14

* Wed Jun 04 2025 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:2.40.3-1
- Update to 2.40.3 (#2359565)

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 1:2.38.0-2
- Rebuilt for Python 3.14

* Thu Jan 23 2025 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:2.38.0-1
- Update to 2.38.0 (#2341662)

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.37.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Dec 11 2024 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:2.37.0-1
- Update to 2.37.0 (#2331785)

* Sat Nov 09 2024 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:2.36.1-1
- Update to 2.36.1 (#2324956)

* Sat Nov 02 2024 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:2.36.0-1
- Update to 2.36.0 (#2323339)

* Sat Sep 21 2024 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:2.35.0-1
- Update to 2.35.0 (#2313466)

* Fri Aug 16 2024 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:2.34.0-1
- Update to 2.34.0 (#2305283)

* Wed Aug 07 2024 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:2.33.0-1
- Update to 2.33.0 (#2303290)

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.32.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 09 2024 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:2.32.0-1
- Update to 2.32.0 (#2296475)

* Wed Jul 03 2024 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:2.31.0-1
- Update to 2.31.0 (#2295490)

* Mon Jun 10 2024 Python Maint <python-maint@redhat.com> - 1:2.30.0-2
- Rebuilt for Python 3.13

* Fri Jun 07 2024 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:2.30.0-1
- Update to 2.30.0 (#2290820)

* Fri May 31 2024 Jason Montleon <jmontleo@redhat.com> - 1:2.29.0-2
- Add directory to files (#2284084)

* Sat Apr 13 2024 Jason Montleon <jmontleo@redhat.com> - 1:2.29.0-1
- Update to 2.29.0 (#2270854)

* Sat Mar 09 2024 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:2.28.2-1
- Update to 2.28.2 (#2265467)

* Thu Feb 15 2024 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:2.28.0-1
- Update to 2.28.0 (#2264481)

* Wed Jan 24 2024 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:2.27.0-1
- Update to 2.27.0 (#2260260)

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.26.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 11 2024 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:2.26.2-1
- Update to 2.26.2 (#2256863)

* Wed Jan 03 2024 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:2.26.0-1
- Update to 2.26.0 (#2256622)

* Sat Dec 09 2023 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:2.25.2-1
- Update to 2.25.2 (#2253755)

* Wed Dec 06 2023 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:2.25.1-1
- Update to 2.25.1 (#2252361)

* Wed Nov 01 2023 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:2.23.4-1
- Update to 2.23.4 (#2247351)

* Tue Oct 10 2023 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:2.23.3-1
- Update to 2.23.3 (#2243020)

* Fri Sep 29 2023 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:2.23.2-1
- Update to 2.23.2 (#2240965)

* Wed Sep 13 2023 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:2.23.0-1
- Update to 2.23.0 (#2238835)

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.22.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 12 2023 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:2.22.0-1
- Update to 2.22.0 (#2218188)

* Tue Jun 27 2023 Python Maint <python-maint@redhat.com> - 1:2.21.0-2
- Rebuilt for Python 3.12

* Mon Jun 26 2023 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:2.21.0-1
- Update to 2.21.0 (#2214891)

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 1:2.19.1-3
- Rebuilt for Python 3.12

* Thu Jun 08 2023 Jan Friesse <jfriesse@redhat.com> - 1:2.19.1-2
- migrated to SPDX license

* Fri Jun 02 2023 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:2.19.1-1
- Update to 2.19.1 (#2212001)

* Fri May 26 2023 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:2.19.0-1
- Update to 2.19.0 (#2208101)

* Wed May 10 2023 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:2.18.0-1
- Update to 2.18.0 (#2198978)

* Wed Apr 12 2023 Jason Montleon <jmontleo@redhat.com> - 1:2.17.3-1
- Update to 2.17.3

* Fri Mar 31 2023 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:2.17.1-1
- Update to 2.17.1 (#2183612)

* Wed Mar 29 2023 Jason Montleon <jmontleo@redhat.com> - 1:2.17.0-1
- Update to 2.17.0

* Fri Mar 24 2023 Jason Montleon <jmontleo@redhat.com> - 1:2.16.3-1
- Update to 2.16.3

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.16.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jan 10 2023 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:2.16.0-1
- Update to 2.16.0 (#2159576)

* Fri Dec 02 2022 Jason Montleon <jmontleo@redhat.com> - 1:2.15.0-1
- Update to 2.15.0

* Tue Nov 01 2022 Jason Montleon <jmontleo@redhat.com> - 1:2.14.0-1
- Update to 2.14.0

* Thu Oct 20 2022 Jason Montleon <jmontleo@redhat.com> - 1:2.13.0-1
- Update to 2.13.0

* Fri Sep 30 2022 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:2.12.0-1
- Update to 2.12.0 (#2128641)

* Tue Sep 20 2022 Jason Montleon <jmontleo@redhat.com> - 1:2.11.1-1
- Update to 2.11.1

* Mon Aug 08 2022 Jason Montleon <jmontleo@redhat.com> - 1:2.10.0-1
- Update to 2.10.0

* Wed Jul 13 2022 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:2.9.1-1
- Update to 2.9.1 (#2106564)

* Wed Jun 29 2022 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:2.9.0-1
- Update to 2.9.0 (#2102235)

* Thu Jun 16 2022 Python Maint <python-maint@redhat.com> - 1:2.8.0-2
- Rebuilt for Python 3.11

* Wed Jun 15 2022 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:2.8.0-1
- Update to 2.8.0 (#2095056)

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1:2.6.6-2
- Rebuilt for Python 3.11

* Fri Apr 22 2022 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:2.6.6-1
- Update to 2.6.6 (#2077788)

* Sat Apr 16 2022 Jason Montleon <jmontleo@redhat.com> - 1:2.6.5-1
- Update to 2.6.5

* Thu Apr 07 2022 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:2.6.3-1
- Update to 2.6.3 (#2064496)

* Tue Feb 01 2022 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:2.6.0-1
- Update to 2.6.0 (#2048870)

* Wed Jan 26 2022 Jason Montleon <jmontleo@redhat.com> - 1:2.5.0-1
- Update to 2.5.0

* Fri Jan 21 2022 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:2.4.0-1
- Update to 2.4.0 (#2043482)

* Wed Jan 12 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1:2.3.3-2
- Apply upstream PR#937 (fix RHBZ#2037828); this simply loosens the version
  specification to allow cachetools 5.x

* Tue Nov 02 2021 Jason Montleon <jmontleo@redhat.com> - 1:2.3.3-1
- Update to 2.3.3 (#2019277)

* Wed Oct 27 2021 Jason Montleon <jmontleo@redhat.com> - 1:2.3.2-1
- Update to 2.3.2 (#2017662)

* Tue Oct 26 2021 Jason Montleon <jmontleo@redhat.com> - 1:2.3.1-1
- Update to 2.3.1 (#2012136)

* Wed Sep 29 2021 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:2.2.1-1
- Update to 2.2.1 (#2008543)

* Wed Sep 15 2021 Jason Montleon <jmontleo@redhat.com> - 1:2.1.0-1
- Update to 2.1.0.

* Wed Sep 01 2021 Jason Montleon <jmontleo@redhat.com> - 1:2.0.2-1
- Update to 2.0.2.

* Fri Aug 20 2021 Jason Montleon <jmontleo@redhat.com> - 1:2.0.1-1
- Update to 2.0.1. Drops support for Python 2.

* Tue Jul 27 2021 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:1.34.0-1
- Update to 1.34.0 (#1986566)

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.33.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:1.33.1-1
- Update to 1.33.1 (#1978114)

* Mon Jun 21 2021 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:1.32.0-1
- Update to 1.32.0 (#1970848)

* Wed Jun 09 2021 Jason Montleon <jmontleo@redhat.com> - 1:1.30.2-1
- Update to 1.30.2

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1:1.30.0-2
- Rebuilt for Python 3.10

* Tue Apr 27 2021 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:1.30.0-1
- Update to 1.30.0 (#1953843)

* Fri Apr 16 2021 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:1.29.0-1
- Update to 1.29.0 (#1950299)

* Fri Apr 09 2021 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:1.28.1-1
- Update to 1.28.1 (#1933900)

* Wed Feb 17 2021 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:1.27.0-1
- Update to 1.27.0 (#1927595)

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.24.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Dec 15 2020 Jason Montleon <jmontleo@redhat.com> - 1:1.24.0-1
- Update to 1.24.0

* Fri Dec 11 2020 Jason Montleon <jmontleo@redhat.com> - 1:1.23.0-1
- Update to 1.23.0

* Thu Sep 24 2020 Jason Montleon <jmontleo@redhat.com> - 1:1.21.3-1
- Update to 1.21.3 (#1879308)

* Fri Sep 04 2020 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:1.21.1-1
- Update to 1.21.1 (#1875665)

* Fri Aug 28 2020 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:1.21.0-1
- Update to 1.21.0 (#1866978)

* Wed Jul 29 2020 Jason Montleon <jmontleo@redhat.com> - 1:1.20.0-1
- Update to 1.20.0 (#1858426)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.19.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul 16 2020 Jason Montleon <jmontleo@redhat.com> - 1:1.19.1-1
- Update to 1.19.1 (#1856662)

* Fri Jun 19 2020 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:1.18.0-1
- Update to 1.18.0 (#1846258)

* Thu Jun 04 2020 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:1.16.1-1
- Update to 1.16.1 (#1841468)

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1:1.14.3-2
- Rebuilt for Python 3.9

* Tue May 12 2020 Jason Montleon <jmontleo@redhat.com> - 1:1.14.3-1
- Update to 1.14.3

* Thu May 07 2020 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:1.14.2-1
- Update to 1.14.2 (#1832794)

* Wed Apr 22 2020 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:1.14.1-1
- Update to 1.14.1 (#1824032)

* Thu Apr 02 2020 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:1.13.1-1
- Update to 1.13.1 (#1817303)

* Mon Mar 16 2020 Jason Montleon <jmontleo@redhat.com> - 1:1.11.3-1
- Update to 1.11.3

* Wed Feb 19 2020 Jason Montleon <jmontleo@redhat.com> - 1:1.11.2-1
- Update to 1.11.2

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 24 2020 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:1.11.0-1
- Update to 1.11.0 (#1794771)

* Thu Jan 23 2020 Jason Montleon <jmontleo@redhat.com> - 1:1.10.2-2
- Update to 1.10.2 (#1793920)

* Wed Jan 15 2020 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:1.10.1-1
- Update to 1.10.1 (#1779733)

* Fri Dec 20 2019 Jason Montleon <jmontleo@redhat.com> - 1:1.10.0-1
- Update to 1.10.0

* Wed Dec 11 2019 Jason Montleon <jmontleo@redhat.com> - 1:1.9.0-2
- Allow newer cachetools

* Wed Dec 11 2019 Jason Montleon <jmontleo@redhat.com> - 1:1.9.0-1
- Update to 1.9.0

* Wed Dec 11 2019 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1:1.8.2-1
- Update to 1.8.2 (#1779733)

* Thu Nov 19 2019 Jason Montleon <jmontleo@redhat.com> - 1:1.7.1-1
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1:1.1.1-10
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1:1.1.1-9
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 15 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1:1.1.1-6
- Enable python dependency generator

* Mon Jan 14 2019 Jason Montleon <jmontleo@redhat.com> - 1:1.1.1-5
- Fix cachetools dependency for python2

* Thu Dec 13 2018 Jason Montleon <jmontleo@redhat.com> - 1:1.1.1-4
- Use python3_pkgversion for EPEL

* Mon Dec 3 2018 Jason Montleon <jmontleo@redhat.com> - 1:1.1.1-3
- Use GitHub instead of PyPI source tarball to build

* Tue Oct 23 2018 Alfredo Moralejo <amoralej@redhat.com> - 1:1.1.1-2
- Removed python2 subpackages in Fedora (rhbz#1636936).

* Mon Aug 13 2018 Alfredo Moralejo <amoralej@redhat.com> - 1:1.1.1-1
- Revert to version 1.1.1. Version 1.3.0 requires pyasn1-modules newer that in Fedora (rhbz#1577286).

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.3.0-4
- Rebuilt for Python 3.7

* Wed Feb 21 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.3.0-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 24 2018 Alfredo Moralejo <amoralej@redhat.com> 1.3.0-1
- Update to 1.3.0

* Fri Oct 13 2017 Jason Montleon <jmontleo@redhat.com> 1.1.1-1
- Initial Build
