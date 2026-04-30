## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 2;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond tests 1

Name:           python-google-api-core
Version:        2.27.0
Epoch:          1
Release:        %autorelease
Summary:        Google API client core library

License:        Apache-2.0
URL:            https://github.com/googleapis/python-api-core
Source0:        %{url}/archive/v%{version}/python-api-core-%{version}.tar.gz

BuildRequires:  python3-devel
BuildRequires:  tomcli

%if %{with tests}
# See noxfile.py:
BuildRequires:  %{py3_dist pytest}
BuildRequires:  %{py3_dist pytest-asyncio}
%endif

BuildArch:      noarch

%global _description %{expand:
This library is not meant to stand alone. Instead it defines common helpers
used by all Google API clients.}

%description %{_description}


%package -n python3-google-api-core
Summary:        %{summary}

%if %[ %{defined fc43} || %{defined fc42} || %{defined fc41} || %{defined el10} ]
# Historically, we added manual dependencies corresponding to the “grpc” extra.
# There’s no good reason to do that, since packages that need grpcio should be
# depending on google-api-core[grpc], so we stopped doing it as of Fedora 44.
Requires:       python3-google-api-core+grpc = %{epoch}:%{version}-%{release}
%endif

%description -n python3-google-api-core %{_description}


%pyproject_extras_subpkg -n python3-google-api-core async_rest grpc grpcgcp grpcio-gcp


%prep
%autosetup -n python-api-core-%{version} -p1

# Remove lower bounds on the versions of protobuf, proto-plus, and grpcio.  The
# protobuf and grpc packages have proven very difficult to update, and they are
# languishing at old and increasingly-broken versions, but we must work with
# what is available.
for dep in protobuf proto-plus
do
  # Don’t use “lists replace” since there may be multiple copies for different
  # Python versions. Replace the dependency entirely with an unversioned one.
  tomcli set pyproject.toml lists delitem --no-first \
      project.dependencies "^${dep}\b.*"
  tomcli set pyproject.toml append project.dependencies "${dep}"
done
# NOTE(mhayden): All of the tests pass fine with 1.48.3
# which is in rawhide/f38 as of 2023-02-20.
for dep in grpcio grpcio-status
do
  tomcli set pyproject.toml lists delitem --no-first \
      project.optional-dependencies.grpc "^${dep}\b.*"
  tomcli set pyproject.toml append project.optional-dependencies.grpc "${dep}"
done


%generate_buildrequires
%pyproject_buildrequires -x async_rest,grpc,grpcgcp,grpcio-gcp


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l google


%check
%pyproject_check_import
%if %{with tests}
# TODO: Try to determine whether the root cause is within this package and
# report these upstream.
# E           RuntimeError: There is no current event loop in thread 'MainThread'.
k="${k-}${k+ and }not test_from_gapic"
k="${k-}${k+ and }not test_metadata"

# Since 2.15.0:
#
# /usr/lib/python3.14/site-packages/google/protobuf/internal/well_known_types.py:92:
#         in <module>
#     _EPOCH_DATETIME = datetime.utcfromtimestamp(0)
# E   DeprecationWarning: datetime.datetime.utcfromtimestamp() is deprecated
#         and scheduled for removal in a future version. Use timezone-aware
#         objects to represent datetimes in UTC:
#         datetime.datetime.fromtimestamp(timestamp, datetime.UTC).
#
# ----
#
# /usr/lib/python3.14/site-packages/google/protobuf/descriptor.py:97: in
#         _Deprecated
#     warnings.warn(
# E   DeprecationWarning: Call to deprecated create function FileDescriptor().
#         Note: Create unlinked descriptors is going to go away. Please use
#         get/find descriptors from generated code or query the
#         descriptor_pool.
#
# ----
#
# We are stuck with both of the above until someone can actually update the
# protobuf package.
#
# Additionally, since 2.17.0:
#
# /usr/lib/python3.14/site-packages/proto/datetime_helpers.py:24: in <module>
#     _UTC_EPOCH = datetime.datetime.utcfromtimestamp(0).replace(
#         tzinfo=datetime.timezone.utc)
# E   DeprecationWarning: datetime.datetime.utcfromtimestamp() is deprecated
#         and scheduled for removal in a future version. Use timezone-aware
#         objects to represent datetimes in UTC:
#         datetime.datetime.fromtimestamp(timestamp, datetime.UTC).
#
# We are stuck with this until someone can actually update the proto-plus
# package.
warningsfilter="${warningsfilter-} -W ignore:datetime:DeprecationWarning"
warningsfilter="${warningsfilter-} -W ignore:Call:DeprecationWarning"

%pytest ${warningsfilter-} -k "${k-}" tests
%endif


%files -n python3-google-api-core -f %{pyproject_files}
%doc CHANGELOG.md
%doc README.rst
%doc SECURITY.md


%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 1:2.27.0-2
- test: add initial lock files

* Mon Oct 27 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1:2.27.0-1
- Update to 2.27.0 (close RHBZ#2261626)

* Sun Oct 26 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1:2.26.0-2
- Package the async_rest feature

* Sun Oct 19 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1:2.26.0-1
- Update to 2.26.0 (close RHBZ#2261626)

* Sun Oct 19 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1:2.25.2-2
- In Fedora 44+, don’t add manual deps. corresponding to grpc extra

* Sun Oct 19 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1:2.25.2-1
- Update to 2.25.2

* Sun Oct 19 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1:2.25.1-1
- Update to 2.25.1

* Sun Oct 19 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1:2.25.0-1
- Update to 2.25.0

* Sun Oct 19 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1:2.24.2-1
- Update to 2.24.2

* Sun Oct 19 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1:2.24.1-1
- Update to 2.24.1

* Sun Oct 19 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1:2.24.0-1
- Update to 2.24.0

* Sun Oct 19 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1:2.23.0-1
- Update to 2.23.0

* Sun Oct 19 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1:2.22.0-1
- Update to 2.22.0

* Sun Oct 19 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1:2.21.0-1
- Update to 2.21.0
- Omit the async_rest extra until python-google-auth provides the “aiohttp”
  extra

* Sun Oct 19 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1:2.20.0-1
- Update to 2.20.0

* Sun Oct 19 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1:2.19.2-1
- Update to 2.19.2

* Sun Oct 19 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1:2.19.1-1
- Update to 2.19.1

* Sun Oct 19 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1:2.19.0-1
- Update to 2.19.0

* Sun Oct 19 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1:2.18.0-1
- Update to 2.18.0
- There is now a hard dependency on python-proto-plus

* Sun Oct 19 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1:2.17.1-1
- Update to 2.17.1

* Sun Oct 19 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1:2.17.0-1
- Update to 2.17.0

* Sun Oct 19 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1:2.16.2-3
- Improved Summary/description

* Sun Oct 19 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1:2.16.2-1
- Update to 2.16.2

* Sun Oct 19 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1:2.16.1-1
- Update to 2.16.1

* Sun Oct 19 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1:2.16.0-1
- Update to 2.16.0

* Sun Oct 19 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1:2.15.0-2
- Do a “smoke test” even if tests are disabled

* Sun Oct 19 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1:2.15.0-1
- Update to 2.15.0
- The package no longer includes a .pth file

* Sun Oct 19 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1:2.14.0-1
- Update to 2.14.0

* Sun Oct 19 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1:2.13.1-1
- Update to 2.13.1

* Sun Oct 19 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1:2.13.0-1
- Update to 2.13.0

* Sun Oct 19 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1:2.12.0-1
- Update to 2.12.0

* Sun Oct 19 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1:2.11.1-24
- Drop some no-longer-necessary test skips

* Sun Oct 19 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1:2.11.1-23
- Also run asyncio tests

* Sun Oct 19 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1:2.11.1-22
- Package missing grpcgcp/grpcio-gcp extras
- Don’t use so many unecessary manual BuildRequires

* Sun Oct 19 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1:2.11.1-21
- Skip a couple of new test regressions (close RHBZ#2374299)

* Sun Oct 19 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1:2.11.1-20
- Assert that the .dist-info directory contains a license file

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1:2.11.1-17
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1:2.11.1-16
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.11.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jun 19 2025 Python Maint <python-maint@redhat.com> - 1:2.11.1-14
- Rebuilt for Python 3.14

* Wed Jun 18 2025 Python Maint <python-maint@redhat.com> - 1:2.11.1-13
- Bootstrap for Python 3.14.0b3 bytecode

* Tue Jun 17 2025 Python Maint <python-maint@redhat.com> - 1:2.11.1-12
- Bootstrap for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.11.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.11.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 1:2.11.1-9
- Rebuilt for Python 3.13

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 1:2.11.1-8
- Bootstrap for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.11.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.11.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.11.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jul 06 2023 Major Hayden <major@redhat.com> - 1:2.11.1-4
- Bump revision number

* Sat Jun 17 2023 Python Maint <python-maint@redhat.com> - 1:2.11.1-3
- Rebuilt for Python 3.12

* Fri Jun 16 2023 Major Hayden <major@redhat.com> - 1:2.11.1-2
- Bump revision number

* Fri Jun 16 2023 Major Hayden <major@redhat.com> - 1:2.11.1-1
- Update to 2.11.1 rhbz#2215121

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 1:2.11.0-3
- Bootstrap for Python 3.12

* Wed Feb 22 2023 Major Hayden <major@redhat.com> - 1:2.11.0-2
- Set SPDX license

* Tue Feb 21 2023 Major Hayden <major@redhat.com> - 1:2.11.0-1
- Update to 2.11.0

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.10.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Dec 08 2022 Major Hayden <major@redhat.com> - 1:2.10.2-2
- Bump revision number after adjusting epoch

* Thu Dec 08 2022 Major Hayden <major@redhat.com> - 1:2.10.2-1
- Bump epoch number to downgrade

* Thu Dec 08 2022 Major Hayden <major@redhat.com> - 2.10.2-1
- Revert "Update to 2.11.0 rhbz#2150012"

* Wed Dec 07 2022 Major Hayden <major@redhat.com> - 2.11.0-1
- Update to 2.11.0 rhbz#2150012

* Mon Nov 14 2022 Major Hayden <major@redhat.com> - 2.10.2-1
- Update to 2.10.2 rhbz#2123558

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 28 2022 Python Maint <python-maint@redhat.com> - 2.8.2-3
- Rebuilt for Python 3.11

* Thu Jun 16 2022 Python Maint <python-maint@redhat.com> - 2.8.2-2
- Bootstrap for Python 3.11

* Wed Jun 15 2022 Major Hayden <major@redhat.com> - 2.8.2-1
- Update to 2.8.2

* Wed Jun 15 2022 Python Maint <python-maint@redhat.com> - 2.8.1-2
- Bootstrap for Python 3.11

* Fri May 27 2022 Major Hayden <major@mhtx.net> - 2.8.1-1
- Update to 2.8.1

* Thu May 19 2022 Major Hayden <major@mhtx.net> - 2.8.0-1
- 🚀 Update to 2.8.0

* Mon May 02 2022 Major Hayden <major@mhtx.net> - 2.7.3-1
- Update to 2.7.3

* Wed Apr 13 2022 Major Hayden <major@mhtx.net> - 2.7.2-1
- Update to 2.7.2

* Thu Mar 10 2022 Major Hayden <major@redhat.com> - 2.7.1-1
- Update to 2.7.1

* Wed Mar 09 2022 Major Hayden <major@redhat.com> - 2.7.0-1
- Update to 2.7.0

* Tue Mar 08 2022 Major Hayden <major@redhat.com> - 2.6.1-1
- Update to 2.6.1

* Fri Mar 04 2022 Major Hayden <major@redhat.com> - 2.6.0-1
- Update to 2.6.0

* Fri Feb 04 2022 Major Hayden <major@redhat.com> - 2.5.0-1
- Update to 2.5.0

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jan 13 2022 Major Hayden <major@redhat.com> - 2.4.0-4
- Restore other skipped tests

* Thu Jan 13 2022 Major Hayden <major@redhat.com> - 2.4.0-3
- Skip broken tests in rest streaming

* Thu Jan 13 2022 Major Hayden <major@redhat.com> - 2.4.0-2
- Run all tests

* Wed Jan 12 2022 Major Hayden <major@redhat.com> - 2.4.0-1
- Update to 2.4.0

* Thu Dec 16 2021 Major Hayden <major@redhat.com> - 2.3.2-1
- Update to 2.3.2

* Wed Dec 15 2021 Major Hayden <major@redhat.com> - 2.3.1-1
- Update to 2.3.1

* Wed Dec 08 2021 Major Hayden <major@redhat.com> - 2.3.0-1
- Update to 2.3.0

* Wed Nov 03 2021 Major Hayden <major@redhat.com> - 2.2.2-1
- Update to 2.2.2

* Thu Oct 28 2021 Major Hayden <major@redhat.com> - 2.2.1-1
- Update to 2.2.1

* Tue Oct 26 2021 Major Hayden <major@mhtx.net> - 2.2.0-1
- Update to 2.2.0

* Mon Oct 25 2021 Major Hayden <major@mhtx.net> - 2.1.1-2
- Use python3-devel as BuildRequires

* Thu Oct 14 2021 Major Hayden <major@mhtx.net> - 2.1.1-1
- Update to 2.1.0

* Wed Oct 06 2021 Major Hayden <major@mhtx.net> - 2.1.0-1
- Update to 2.1.0

* Fri Sep 17 2021 Major Hayden <major@mhtx.net> - 2.0.1-3
- Fix tests with PEP 420 workaround

* Thu Sep 09 2021 Major Hayden <major@mhtx.net> - 2.0.1-2
- Move to rpmautospec

* Wed Sep 01 2021 Major Hayden <major@mhtx.net> - 2.0.1-1
- Update to 2.0.1

* Mon Aug 23 2021 Major Hayden <major@mhtx.net> - 2.0.0-2
- Add proto-plus dependency for tests

* Mon Aug 23 2021 Major Hayden <major@mhtx.net> - 2.0.0-1
- Update to 2.0.0

* Tue Jul 27 2021 Major Hayden <major@mhtx.net> - 1.31.1-2
- Use correct path for extracted sources

* Tue Jul 27 2021 Major Hayden <major@mhtx.net> - 1.31.1-1
- Update to 1.31.1

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.31.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jul 15 2021 Major Hayden <major@mhtx.net> - 1.31.0-2
- Add grpc, grpcgcp, and grpcio-gcp extras packages

* Fri Jul 09 2021 Major Hayden <major@mhtx.net> - 1.31.0-1
- Update to 1.31.0

* Tue Jun 15 2021 Major Hayden <major@mhtx.net> - 1.30.0-3
- Get the right sources this time

* Tue Jun 15 2021 Major Hayden <major@mhtx.net> - 1.30.0-2
- Include patch in new sources

* Tue Jun 15 2021 Major Hayden <major@mhtx.net> - 1.30.0-1
- Update to v1.3.0

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.29.0-2
- Rebuilt for Python 3.10

* Thu Jun 03 2021 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.29.0-1
- Update to 1.29.0

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Aug 17 2020 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.17.0-2
- Temporarily disable tests

* Thu Aug 13 2020 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.17.0-1
- Rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.21.0-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.21.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 19 2020 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.21.0-1
- Update to 1.21.0

* Fri Jun 05 2020 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.17.0-2
- Update sources file

* Fri Jun 05 2020 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.17.0-1
- Revert to 1.17.0 until grpc is updated

* Fri Jun 05 2020 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.19.0-1
- First import
## END: Generated by rpmautospec
