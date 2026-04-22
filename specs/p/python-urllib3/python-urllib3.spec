## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 2;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# When bootstrapping Python, we cannot test this yet
# RHEL does not include the test dependencies and the dependencies for extras
%bcond tests %{undefined rhel}
%bcond extras %[%{undefined rhel} || %{defined eln}]
%bcond extradeps %{undefined rhel}

Name:           python-urllib3
Version:        2.6.3
Release:        %autorelease
Summary:        HTTP library with thread-safe connection pooling, file post, and more

# SPDX
License:        MIT
URL:            https://github.com/urllib3/urllib3
Source0:        %{url}/archive/%{version}/urllib3-%{version}.tar.gz
# A special forked copy of Hypercorn is required for testing. We asked about
# the possiblility of using a released version in the future in:
#   Path toward testing with a released version of hypercorn?
#   https://github.com/urllib3/urllib3/3334
# Upstream would like to get the necessary changes merged into Hypercorn, but
# explained clearly why the forked copy is needed for now.
#
# Note that tool.uv.sources.hypercorn in pyproject.toml references the
# urllib3-changes branch of https://github.com/urllib3/hypercorn/, and we
# should use the latest commit from that branch, but we package using a commit
# hash for reproducibility.
#
# We do not need to treat this as a bundled dependency because it is not
# installed in the buildroot or otherwise included in any of the binary RPMs.
%global hypercorn_url https://github.com/urllib3/hypercorn
%global hypercorn_commit d1719f8c1570cbd8e6a3719ffdb14a4d72880abb
Source1:        %{hypercorn_url}/archive/%{hypercorn_commit}/hypercorn-%{hypercorn_commit}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel
# The conditional is important: we benefit from tomcli for editing dependency
# groups, but we do not want it when bootstrapping or in RHEL.
%if %{with tests}
BuildRequires:  tomcli
%endif

%global _description %{expand:
urllib3 is a powerful, user-friendly HTTP client for Python. urllib3 brings
many critical features that are missing from the Python standard libraries:

  • Thread safety.
  • Connection pooling.
  • Client-side SSL/TLS verification.
  • File uploads with multipart encoding.
  • Helpers for retrying requests and dealing with HTTP redirects.
  • Support for gzip, deflate, brotli, and zstd encoding.
  • Proxy support for HTTP and SOCKS.
  • 100% test coverage.}

%description %{_description}


%package -n python3-urllib3
Summary:        %{summary}

BuildRequires:  ca-certificates
Requires:       ca-certificates

# There has historically been a manual hard dependency on python3-idna.
BuildRequires:  %{py3_dist idna}
Requires:       %{py3_dist idna}

%if %{with extradeps}
# There has historically been a manual hard dependency on python3-pysocks;
# since bringing it in is the sole function of python3-urllib3+socks,
# we recommend it, so it is installed by default.
Recommends:     python3-urllib3+socks
%endif

%description -n python3-urllib3 %{_description}


%if %{with extras}
%pyproject_extras_subpkg -n python3-urllib3 brotli zstd socks h2
%endif


%prep
%autosetup -n urllib3-%{version}
%setup -q -n urllib3-%{version} -T -D -b 1

# Make sure that the RECENT_DATE value doesn't get too far behind what the current date is.
# RECENT_DATE must not be older that 2 years from the build time, or else test_recent_date
# (from test/test_connection.py) would fail. However, it shouldn't be to close to the build time either,
# since a user's system time could be set to a little in the past from what build time is (because of timezones,
# corner cases, etc). As stated in the comment in src/urllib3/connection.py:
#   When updating RECENT_DATE, move it to within two years of the current date,
#   and not less than 6 months ago.
#   Example: if Today is 2018-01-01, then RECENT_DATE should be any date on or
#   after 2016-01-01 (today - 2 years) AND before 2017-07-01 (today - 6 months)
# There is also a test_ssl_wrong_system_time test (from test/with_dummyserver/test_https.py) that tests if
# user's system time isn't set as too far in the past, because it could lead to SSL verification errors.
# That is why we need RECENT_DATE to be set at most 2 years ago (or else test_ssl_wrong_system_time would
# result in false positive), but before at least 6 month ago (so this test could tolerate user's system time being
# set to some time in the past, but not to far away from the present).
# Next few lines update RECENT_DATE dynamically.
recent_date=$(date --date "7 month ago" +"%Y, %_m, %_d")
sed -i "s/^RECENT_DATE = datetime.date(.*)/RECENT_DATE = datetime.date($recent_date)/" src/urllib3/connection.py

%if %{with tests}
# Possible improvements to dependency groups
# https://github.com/urllib3/urllib3/issues/3594
# Adjust the contents of the "dev" dependency group by removing:
remove_from_dev() {
  tomcli set pyproject.toml lists delitem 'dependency-groups.dev' "($1)\b.*"
}
#   - Linters, coverage tools, profilers, etc.:
#     https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/#_linters
remove_from_dev 'coverage|pytest-memray'
#   - Dependencies for maintainer tasks
remove_from_dev 'build|towncrier'
#   - Dependencies that are not packaged and not strictly required
remove_from_dev 'pytest-socket'
#   - Hypercorn, because we have a special forked version we must use for
#     testing instead, so we do not want to generate a dependency on the system
#     copy. Note that the system copy is still an indirect dependency via quart
#     and quart-trio.
remove_from_dev 'hypercorn'

# Remove all version bounds for test dependencies. We must attempt to make do
# with what we have. (This also removes any python version or platform
# constraints, which is currently fine, but could theoretically cause trouble
# in the future. We’ll cross that bridge if we ever arrive at it.)
tomcli set pyproject.toml lists replace --type regex_search \
    'dependency-groups.dev' '[>=]=.*' ''
%endif


%generate_buildrequires
export SETUPTOOLS_SCM_PRETEND_VERSION='%{version}'
# Generate BR’s from packaged extras even when tests are disabled, to ensure
# the extras metapackages are installable if the build succeeds.
%pyproject_buildrequires %{?with_extradeps:-x brotli,zstd,socks,h2} %{?with_tests:-g dev}


%build
export SETUPTOOLS_SCM_PRETEND_VERSION='%{version}'
%pyproject_wheel


%install
%pyproject_install

%pyproject_save_files -l urllib3


%check
# urllib3.contrib.socks requires urllib3[socks]
#
# urllib3.contrib.emscripten is “special” (import js will fail)
# urllib3.contrib.ntlmpool is deprecated and requires ntlm
# urllib3.contrib.securetransport is macOS only
# urllib3.contrib.pyopenssl requires pyOpenSSL
%{pyproject_check_import %{!?with_extradeps:-e urllib3.contrib.socks -e urllib3.http2*}
                         -e urllib3.contrib.emscripten*
                         -e urllib3.contrib.ntlmpool
                         -e urllib3.contrib.securetransport
                         -e urllib3.contrib.pyopenssl}

# Increase the “long timeout” for slower environments; as of this writing, it
# is increased from 0.1 to 0.5 second.
export CI=1
# Interpose the special forked copy of Hypercorn.
hypercorndir="${PWD}/../hypercorn-%{hypercorn_commit}/src"
export PYTHONPATH="${hypercorndir}:%{buildroot}%{python3_sitelib}"

%if %{with tests}
# This test still times out sometimes, especially on certain architectures,
# even when we export the CI environment variable to increase timeouts.
k="${k-}${k+ and }not (TestHTTPProxyManager and test_tunneling_proxy_request_timeout[https-https])"

%pytest -v -rs ${ignore-} -k "${k-}"
%pytest -v -rs ${ignore-} -k "${k-}" --integration
%endif


%files -n python3-urllib3 -f %{pyproject_files}
%doc CHANGES.rst README.md


%changelog
## START: Generated by rpmautospec
* Wed Apr 22 2026 azldev <azurelinux@microsoft.com> - 2.6.3-2
- Latest state for python-urllib3

* Wed Jan 07 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 2.6.3-1
- Update to 2.6.3 (close RHBZ#2427603)

* Fri Dec 12 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2.6.2-1
- Update to 2.6.2 (close RHBZ#2421420)

* Mon Dec 08 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2.6.1-1
- Update to 2.6.1 (close RHBZ#2419408)
- Fixes CVE-2025-66471 / GHSA-2xpw-w6gg-jr37
- Fixes CVE-2025-66418 / GHSA-gm62-xv2j-4w53

* Mon Dec 08 2025 Miro Hrončok <miro@hroncok.cz> - 2.5.0-4
- Allow building with setuptools_scm 9

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 2.5.0-3
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 2.5.0-2
- Rebuilt for Python 3.14.0rc2 bytecode

* Thu Aug 07 2025 Karolina Surma <ksurma@redhat.com> - 2.5.0-1
- Update to 2.5.0 (rhbz#2375401)

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jun 13 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2.4.0-4
- Non-bootstrap build for Python 3.14

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 2.4.0-3
- Bootstrap for Python 3.14

* Thu May 29 2025 Miro Hrončok <miro@hroncok.cz> - 2.4.0-2
- Unpin hatch-vcs version

* Tue Apr 15 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2.4.0-1
- Update to 2.4.0 (close RHBZ#2358892)

* Tue Apr 15 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2.3.0-3
- In the CI smoke test, do not check for a ‘server’ header

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Dec 22 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2.3.0-1
- Update to 2.3.0 (close RHBZ#2333724)

* Tue Sep 17 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 2.2.3-5
- Add extras to ELN builds

* Mon Sep 16 2024 Karolina Surma <ksurma@redhat.com> - 2.2.3-4
- Add a smoke test

* Thu Sep 12 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2.2.3-3
- Remove a 32-bit workaround (since noarch packages no longer build on
  i686)

* Thu Sep 12 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2.2.3-2
- Stop skipping one test that now passes

* Thu Sep 12 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2.2.3-1
- Update to 2.2.3 (close RHBZ#2311902)

* Mon Aug 05 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2.2.2-1
- Update to 2.2.2 (close RHBZ#2143021)

* Mon Aug 05 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2.2.1-1
- Update to 2.2.1

* Mon Aug 05 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2.2.0-1
- Update to 2.2.0

* Mon Aug 05 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2.1.0-1
- Update to 2.1.0

* Mon Aug 05 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2.0.7-1
- Update to 2.0.7
- Add metapackage for new zstd extra
- Upstream no longer vendors six, so we no longer need to bundle it
- Assert that there is a license file in the .dist-info directory
- Greatly reduce the number of skipped tests
- Stop explicitly bounding versions of build dependencies for testing

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.26.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 26 2024 Lumir Balhar <lbalhar@redhat.com> - 1.26.19-1
- Update to 1.26.19 to fix CVE-2024-37891 (rhbz#2292790)

* Sun Jun 09 2024 Python Maint <python-maint@redhat.com> - 1.26.18-6
- Rebuilt for Python 3.13

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.26.18-5
- Bootstrap for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.26.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.26.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Oct 17 2023 Maxwell G <maxwell@gtmx.me> - 1.26.18-1
- Update to 1.26.18.
- Mitigates CVE-2023-45803 / GHSA-g4mx-q9vg-27p4.

* Mon Oct 09 2023 Miro Hrončok <mhroncok@redhat.com> - 1.26.17-2
- Switch the hardcoded dependency on urllib3[socks] to a weak one

* Mon Oct 02 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.26.17-1
- Update to 1.26.17: fix CVE-2023-43804 (GHSA-v845-jxx5-vc9f)

* Wed Aug 30 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 1.26.16-3
- Use bundled six

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.26.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jul 01 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.26.16-1
- Update to 1.26.16

* Sat Jul 01 2023 Python Maint <python-maint@redhat.com> - 1.26.15-3
- Rebuilt for Python 3.12

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 1.26.15-2
- Bootstrap for Python 3.12

* Thu May 18 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.26.15-1
- Update to 1.26.15

* Thu May 18 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.26.12-5
- Confirm the License is SPDX MIT
- Update Summary and description based on upstream
- Add metapackages for brotli and socks extras
- Port to pyproject-rpm-macros

* Tue May 16 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 1.26.12-4
- Disable tests by default in RHEL builds

* Tue May 16 2023 Tomáš Hrnčiar <thrnciar@redhat.com> - 1.26.12-3
- Accomodate the test to the changed behavior of SSLContext.shared_ciphers() in CPython
- Fixes: rhbz#2203773

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.26.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Sep 15 2022 Kevin Fenzi <kevin@scrye.com> - 1.26.12-1
- Update to 1.26.12. Fixes rhbz#2104964

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.26.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 14 2022 Python Maint <python-maint@redhat.com> - 1.26.9-3
- Rebuilt for Python 3.11

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.26.9-2
- Bootstrap for Python 3.11

* Mon May 30 2022 Kevin Fenzi <kevin@scrye.com> - 1.26.9-1
- Update to 1.26.9. fixes rhbz#2064777

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.26.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Jan 08 2022 Kevin Fenzi <kevin@scrye.com> - 1.26.8-1
- Update to 1.26.8. Fixes rhbz#2038246

* Tue Jan 04 2022 Adam Williamson <awilliam@redhat.com> - 1.26.7-2
- Stop unbundling ssl.match_hostname, it's deprecated upstream (#2009550)

* Sun Sep 26 2021 Kevin Fenzi <kevin@scrye.com> - 1.26.7-1
- Update to 1.26.7. Fixes rhbz#2006973

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.26.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun Jul 11 2021 Kevin Fenzi <kevin@scrye.com> - 1.26.6-1
- Update to 1.26.1. Fixes rhbz#1976190
- Fix FTBFS. Fixes rhbz#1966120

* Wed Jun 30 2021 Yatin Karel <ykarel@redhat.com> - 1.26.5-2
- Update minimal requirement of six to >= 1.16.0

* Wed Jun 16 2021 Karolina Surma <ksurma@redhat.com> - 1.26.5-1
- Update to 1.26.5
- Fixes rhbz#1965056

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.26.4-3
- Rebuilt for Python 3.10

* Wed Jun 02 2021 Python Maint <python-maint@redhat.com> - 1.26.4-2
- Bootstrap for Python 3.10

* Tue May 18 2021 Miro Hrončok <mhroncok@redhat.com> - 1.26.4-1
- Update to 1.26.4
- Fixes rhbz#1889391

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.25.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 15 2021 Miro Hrončok <mhroncok@redhat.com> - 1.25.10-3
- Drop redundant BuildRequires for nose
- Instead of the mock backport, use unittest.mock from the standard library

* Tue Jan 05 2021 Anna Khaitovich <akhaitov@redhat.com> - 1.25.10-2
- Update RECENT_DATE dynamically

* Sun Sep 27 2020 Kevin Fenzi <kevin@scrye.com> - 1.25.10-1
- Update to 1.25.10. Fixed bug #1824900

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.25.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 1.25.8-3
- Rebuilt for Python 3.9

* Fri May 22 2020 Miro Hrončok <mhroncok@redhat.com> - 1.25.8-2
- Bootstrap for Python 3.9

* Sun Mar 22 2020 Carl George <carl@george.computer> - 1.25.8-1
- Latest upstream rhbz#1771186

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.25.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Nov 18 2019 Miro Hrončok <mhroncok@redhat.com> - 1.25.7-2
- Subpackage python2-urllib3 has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Tue Oct 15 2019 Jeremy Cline <jcline@redhat.com> - 1.25.6-1
- Update to v1.25.6

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.25.3-7
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Sun Aug 18 2019 Miro Hrončok <mhroncok@redhat.com> - 1.25.3-6
- Rebuilt for Python 3.8

* Thu Aug 15 2019 Miro Hrončok <mhroncok@redhat.com> - 1.25.3-5
- Bootstrap for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.25.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 08 2019 Miro Hrončok <mhroncok@redhat.com> - 1.25.3-3
- Set RECENT_DATE not to be older than 2 years (#1727796)

* Tue May 28 2019 Jeremy Cline <jcline@redhat.com> - 1.25.3-2
- Drop the Python 2 tests since Tornado is going away

* Tue May 28 2019 Jeremy Cline <jcline@redhat.com> - 1.25.3-1
- Update to 1.25.3

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.24.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Nov 13 2018 Jeremy Cline <jeremy@jcline.org> - 1.24.1-2
- Adjust unbundling of ssl_match_hostname

* Mon Oct 29 2018 Jeremy Cline <jeremy@jcline.org> - 1.24.1-1
- Update to v1.24.1

* Wed Jun 20 2018 Lumír Balhar <lbalhar@redhat.com> - 1.23-4
- Removed unneeded dependency python[23]-psutil

* Mon Jun 18 2018 Miro Hrončok <mhroncok@redhat.com> - 1.23-3
- Rebuilt for Python 3.7

* Thu Jun 14 2018 Miro Hrončok <mhroncok@redhat.com> - 1.23-2
- Bootstrap for Python 3.7

* Tue Jun 05 2018 Jeremy Cline <jeremy@jcline.org> - 1.23-1
- Update to the latest upstream release (rhbz 1586072)

* Wed May 30 2018 Jeremy Cline <jeremy@jcline.org> - 1.22-10
- Backport patch to support Python 3.7 (rhbz 1584112)

* Thu May 03 2018 Lukas Slebodnik <lslebodn@fedoraproject.org> - 1.22-9
- Do not lowercase hostnames with custom-protocol (rhbz 1567862)
- upstream: https://github.com/urllib3/urllib3/issues/1267

* Wed Apr 18 2018 Jeremy Cline <jeremy@jcline.org> - 1.22-8
- Drop the dependency on idna and cryptography (rhbz 1567862)

* Mon Apr 16 2018 Jeremy Cline <jeremy@jcline.org> - 1.22-7
- Drop the dependency on PyOpenSSL, it's not needed (rhbz 1567862)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.22-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 31 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.22-5
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Jan 25 2018 Tomas Hoger <thoger@redhat.com> - 1.22-4
- Fix FTBFS - Move RECENT_DATE to 2017-06-30

* Fri Dec 01 2017 Jeremy Cline <jeremy@jcline.org> - 1.22-3
- Symlink the Python 3 bytecode for six (rbhz 1519147)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 21 2017 Jeremy Cline <jeremy@jcline.org> - 1.22-1
- Update to 1.22 (#1473293)

* Wed May 17 2017 Jeremy Cline <jeremy@jcline.org> - 1.21.1-1
- Update to 1.21.1 (#1445280)

* Thu Feb 09 2017 Jeremy Cline <jeremy@jcline.org> - 1.20-1
- Update to 1.20 (#1414775)

* Tue Dec 13 2016 Stratakis Charalampos <cstratak@redhat.com> - 1.19.1-2
- Rebuild for Python 3.6

* Thu Nov 17 2016 Jeremy Cline <jeremy@jcline.org> 1.19.1-1
- Update to 1.19.1
- Clean up the specfile to only support Fedora 26

* Wed Aug 10 2016 Kevin Fenzi <kevin@scrye.com> - 1.16-3
- Rebuild now that python-requests is ready to update.

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.16-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Jun 15 2016 Kevin Fenzi <kevin@scrye.com> - 1.16-1
- Update to 1.16

* Thu Jun 02 2016 Ralph Bean <rbean@redhat.com> - 1.15.1-3
- Create python2 subpackage to comply with guidelines.

* Wed Jun 01 2016 Ralph Bean <rbean@redhat.com> - 1.15.1-2
- Remove broken symlinks to unbundled python3-six files
  https://bugzilla.redhat.com/show_bug.cgi?id=1295015

* Fri Apr 29 2016 Ralph Bean <rbean@redhat.com> - 1.15.1-1
- Removed patch for ipv6 support, now applied upstream.
- Latest version.
- New dep on pysocks.

* Fri Feb 26 2016 Ralph Bean <rbean@redhat.com> - 1.13.1-3
- Apply patch from upstream to fix ipv6.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Dec 21 2015 Ralph Bean <rbean@redhat.com> - 1.13.1-1
- new version

* Fri Dec 18 2015 Ralph Bean <rbean@redhat.com> - 1.13-1
- new version

* Mon Dec 14 2015 Ralph Bean <rbean@redhat.com> - 1.12-1
- new version

* Thu Oct 15 2015 Robert Kuska <rkuska@redhat.com> - 1.10.4-7
- Rebuilt for Python3.5 rebuild

* Sat Oct 10 2015 Ralph Bean <rbean@redhat.com> - 1.10.4-6
- Sync from PyPI instead of a git checkout.

* Tue Sep 08 2015 Ralph Bean <rbean@redhat.com> - 1.10.4-5.20150503gita91975b
- Drop requirement on python-backports-ssl_match_hostname on F22 and newer.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.4-4.20150503gita91975b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 08 2015 Ralph Bean <rbean@redhat.com> - 1.10.4-3.20150503gita91975b
- Apply pyopenssl injection for an outdated cpython as per upstream advice
  https://urllib3.readthedocs.org/en/latest/security.html#insecureplatformwarning
  https://urllib3.readthedocs.org/en/latest/security.html#pyopenssl

* Tue May 19 2015 Ralph Bean <rbean@redhat.com> - 1.10.4-2.20150503gita91975b
- Specify symlinks for six.py{c,o}, fixing rhbz #1222142.

* Sun May 03 2015 Ralph Bean <rbean@redhat.com> - 1.10.4-1.20150503gita91975b
- Latest release for python-requests-2.7.0

* Wed Apr 29 2015 Ralph Bean <rbean@redhat.com> - 1.10.3-2.20150429git585983a
- Grab a git snapshot to get around this chunked encoding failure.

* Wed Apr 22 2015 Ralph Bean <rbean@redhat.com> - 1.10.3-1
- new version

* Thu Feb 26 2015 Ralph Bean <rbean@redhat.com> - 1.10.2-1
- new version

* Wed Feb 18 2015 Ralph Bean <rbean@redhat.com> - 1.10.1-1
- new version

* Wed Feb 18 2015 Ralph Bean <rbean@redhat.com> - 1.10.1-1
- new version

* Mon Jan 05 2015 Ralph Bean <rbean@redhat.com> - 1.10-2
- Copy in a shim for ssl_match_hostname on python3.

* Sun Dec 14 2014 Ralph Bean <rbean@redhat.com> - 1.10-1
- Latest upstream 1.10, for python-requests-2.5.0.
- Re-do unbundling without patch, with symlinks.
- Modernize python2 macros.
- Remove the with_dummyserver tests which fail only sometimes.

* Wed Nov 05 2014 Ralph Bean <rbean@redhat.com> - 1.9.1-1
- Latest upstream, 1.9.1 for latest python-requests.

* Mon Aug  4 2014 Tom Callaway <spot@fedoraproject.org> - 1.8.2-4
- fix license handling

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 1.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Mon Apr 21 2014 Arun S A G <sagarun@gmail.com> - 1.8.2-1
- Update to latest upstream version

* Mon Oct 28 2013 Ralph Bean <rbean@redhat.com> - 1.7.1-2
- Update patch to find ca_certs in the correct location.

* Wed Sep 25 2013 Ralph Bean <rbean@redhat.com> - 1.7.1-1
- Latest upstream with support for a new timeout class and py3.4.

* Wed Aug 28 2013 Ralph Bean <rbean@redhat.com> - 1.7-3
- Bump release again, just to push an unpaired update.

* Mon Aug 26 2013 Ralph Bean <rbean@redhat.com> - 1.7-2
- Bump release to pair an update with python-requests.

* Thu Aug 22 2013 Ralph Bean <rbean@redhat.com> - 1.7-1
- Update to latest upstream.
- Removed the accept-header proxy patch which is included in upstream now.
- Removed py2.6 compat patch which is included in upstream now.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 11 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 1.5-6
- Fix Requires of python-ordereddict to only apply to RHEL

* Fri Mar  1 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 1.5-5
- Unbundling finished!

* Fri Mar 01 2013 Ralph Bean <rbean@redhat.com> - 1.5-4
- Upstream patch to fix Accept header when behind a proxy.
- Reorganize patch numbers to more clearly distinguish them.

* Wed Feb 27 2013 Ralph Bean <rbean@redhat.com> - 1.5-3
- Renamed patches to python-urllib3-*
- Fixed ssl check patch to use the correct cert path for Fedora.
- Included dependency on ca-certificates
- Cosmetic indentation changes to the .spec file.

* Tue Feb  5 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 1.5-2
- python3-tornado BR and run all unittests on python3

* Mon Feb 04 2013 Toshio Kuratomi <toshio@fedoraproject.org> 1.5-1
- Initial fedora build.

## END: Generated by rpmautospec
