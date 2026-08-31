# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond bootstrap 0

%global docs    %[%{without bootstrap} && 0%{?fedora}]
%global giturl  https://github.com/mongodb/mongo-python-driver

Name:           python-pymongo
Version:        4.13.2
Release:        3%{?dist}

License:        Apache-2.0
Summary:        Python driver for MongoDB
URL:            https://pymongo.readthedocs.io/en/stable/
VCS:            git:%{giturl}.git
Source0:        %{giturl}/archive/%{version}/pymongo-%{version}.tar.gz
# Don't fail tests on python 3.14 deprecation warnings
# Downstream patch
Patch0:         pymongo-nonfatal-warnings.patch

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  python3-devel
%if 0%{docs}
BuildRequires:  python3-furo
BuildRequires:  python3-sphinx
%endif

%description
The Python driver for MongoDB.


%package doc
# Apache-2.0: the content.  Other licenses are due to files copied in by Sphinx.
# _static/basic.css: BSD-2-Clause
# _static/debug.css: MIT
# _static/doctools.js: BSD-2-Clause
# _static/documentation_options.js: BSD-2-Clause
# _static/file.png: BSD-2-Clause
# _static/language_data.js: BSD-2-Clause
# _static/minus.png: BSD-2-Clause
# _static/plus.png: BSD-2-Clause
# _static/scripts: MIT
# _static/searchtools.js: BSD-2-Clause
# _static/skeleton.css: MIT
# _static/sphinx_highlight.js: BSD-2-Clause
# _static/styles: MIT
# genindex.html: BSD-2-Clause
# search.html: BSD-2-Clause
# searchindex.js: BSD-2-Clause
License:        Apache-2.0 AND BSD-2-Clause AND MIT
BuildArch:      noarch
Summary:        Documentation for python-pymongo

%description doc
Documentation for python-pymongo.


%package -n python3-bson
# All code is Apache-2.0 except bson/time64*.{c,h} which is MIT
License:        Apache-2.0 AND MIT
Summary:        Python bson library

%description -n python3-bson
BSON is a binary-encoded serialization of JSON-like documents. BSON is designed
to be lightweight, traversable, and efficient. BSON, like JSON, supports the
embedding of objects and arrays within other objects and arrays.  This package
contains the python3 version of this module.


%package -n python3-pymongo
Summary:        Python driver for MongoDB
Requires:       python3-bson%{?_isa} = %{version}-%{release}

%description -n python3-pymongo
The Python driver for MongoDB.  This package contains the python3 version of
this module.


%package -n python3-pymongo-gridfs
Summary:        Python GridFS driver for MongoDB
Requires:       python3-pymongo%{?_isa} = %{version}-%{release}

%description -n python3-pymongo-gridfs
GridFS is a storage specification for large objects in MongoDB.  This package
contains the python3 version of this module.


# Some extras cannot be supported due to missing dependencies:
# - pymongo-auth-aws: needed for aws and encryption extras
# - pymongocrypt: needed for encryption extra
# - pykerberos: needed for gssapi extra
# No snappy on i686
%ifarch %{ix86}
%pyproject_extras_subpkg -n python3-pymongo ocsp zstd
%else
%pyproject_extras_subpkg -n python3-pymongo ocsp snappy zstd
%endif


%prep
%autosetup -n mongo-python-driver-%{version} -p1

# Permit use of pytest-asyncio 0.23
sed -i '/pytest-asyncio/s/0\.24\.0/0.23.0/' requirements/test.txt


%generate_buildrequires
%ifarch %{ix86}
%pyproject_buildrequires -x ocsp,test,zstd
%else
%pyproject_buildrequires -x ocsp,snappy,test,zstd
%endif


%build
export PYMONGO_C_EXT_MUST_BUILD=1
%pyproject_wheel

%if 0%{docs}
export PYTHONPATH=$PWD
%make_build -C doc html
rm doc/_build/html/.buildinfo
%endif


%install
%pyproject_install
%pyproject_save_files -L pymongo


%check
# Skip tests that require network/nameservers
%pytest -v \
  --deselect=test/asynchronous/test_client.py::AsyncClientUnitTest::test_connection_timeout_ms_propagates_to_DNS_resolver \
  --deselect=test/asynchronous/test_client.py::AsyncClientUnitTest::test_detected_environment_logging \
  --deselect=test/asynchronous/test_client.py::AsyncClientUnitTest::test_detected_environment_warning \
  --deselect=test/test_client.py::ClientUnitTest::test_connection_timeout_ms_propagates_to_DNS_resolver \
  --deselect=test/test_client.py::ClientUnitTest::test_detected_environment_logging \
  --deselect=test/test_client.py::ClientUnitTest::test_detected_environment_warning \
  --deselect=test/test_srv_polling.py::TestSrvPolling::test_10_all_dns_selected \
  --deselect=test/test_srv_polling.py::TestSrvPolling::test_11_all_dns_selected \
  --deselect=test/test_srv_polling.py::TestSrvPolling::test_12_new_dns_randomly_selected \
  --deselect=test/test_srv_polling.py::TestSrvPolling::test_addition \
  --deselect=test/test_srv_polling.py::TestSrvPolling::test_dns_failures \
  --deselect=test/test_srv_polling.py::TestSrvPolling::test_dns_record_lookup_empty \
  --deselect=test/test_srv_polling.py::TestSrvPolling::test_does_not_flipflop \
  --deselect=test/test_srv_polling.py::TestSrvPolling::test_recover_from_initially_empty_seedlist \
  --deselect=test/test_srv_polling.py::TestSrvPolling::test_recover_from_initially_erroring_seedlist \
  --deselect=test/test_srv_polling.py::TestSrvPolling::test_removal \
  --deselect=test/test_srv_polling.py::TestSrvPolling::test_replace_both_with_one \
  --deselect=test/test_srv_polling.py::TestSrvPolling::test_replace_both_with_two \
  --deselect=test/test_srv_polling.py::TestSrvPolling::test_replace_one \
  --deselect=test/test_srv_polling.py::TestSrvPolling::test_srv_service_name \
  --deselect=test/test_srv_polling.py::TestSrvPolling::test_srv_waits_to_poll \
  --deselect=test/asynchronous/test_srv_polling.py::TestSrvPolling::test_10_all_dns_selected \
  --deselect=test/asynchronous/test_srv_polling.py::TestSrvPolling::test_11_all_dns_selected \
  --deselect=test/asynchronous/test_srv_polling.py::TestSrvPolling::test_12_new_dns_randomly_selected \
  --deselect=test/asynchronous/test_srv_polling.py::TestSrvPolling::test_addition \
  --deselect=test/asynchronous/test_srv_polling.py::TestSrvPolling::test_dns_failures \
  --deselect=test/asynchronous/test_srv_polling.py::TestSrvPolling::test_dns_record_lookup_empty \
  --deselect=test/asynchronous/test_srv_polling.py::TestSrvPolling::test_does_not_flipflop \
  --deselect=test/asynchronous/test_srv_polling.py::TestSrvPolling::test_recover_from_initially_empty_seedlist \
  --deselect=test/asynchronous/test_srv_polling.py::TestSrvPolling::test_recover_from_initially_erroring_seedlist \
  --deselect=test/asynchronous/test_srv_polling.py::TestSrvPolling::test_removal \
  --deselect=test/asynchronous/test_srv_polling.py::TestSrvPolling::test_replace_both_with_one \
  --deselect=test/asynchronous/test_srv_polling.py::TestSrvPolling::test_replace_both_with_two \
  --deselect=test/asynchronous/test_srv_polling.py::TestSrvPolling::test_replace_one \
  --deselect=test/asynchronous/test_srv_polling.py::TestSrvPolling::test_srv_service_name \
  --deselect=test/asynchronous/test_srv_polling.py::TestSrvPolling::test_srv_waits_to_poll \
  --deselect=test/test_uri_spec.py::TestAllScenarios::test_test_uri_options_srv-options_SRV_URI_with_custom_srvServiceName \
  --deselect=test/test_uri_spec.py::TestAllScenarios::test_test_uri_options_srv-options_SRV_URI_with_invalid_type_for_srvMaxHosts \
  --deselect=test/test_uri_spec.py::TestAllScenarios::test_test_uri_options_srv-options_SRV_URI_with_negative_integer_for_srvMaxHosts \
  --deselect=test/test_uri_spec.py::TestAllScenarios::test_test_uri_options_srv-options_SRV_URI_with_positive_srvMaxHosts_and_loadBalanced=false \
  --deselect=test/test_uri_spec.py::TestAllScenarios::test_test_uri_options_srv-options_SRV_URI_with_srvMaxHosts \
  --deselect=test/test_uri_spec.py::TestAllScenarios::test_test_uri_options_srv-options_SRV_URI_with_srvMaxHosts=0_and_loadBalanced=true \
  --deselect=test/test_uri_spec.py::TestAllScenarios::test_test_uri_options_srv-options_SRV_URI_with_srvMaxHosts=0_and_replicaSet \


%files doc
%license LICENSE
%if 0%{docs}
%doc doc/_build/html/*
%endif


%files -n python3-bson
%license LICENSE
%doc README.md
%{python3_sitearch}/bson


%files -n python3-pymongo -f %{pyproject_files}
%license LICENSE
%doc README.md


%files -n python3-pymongo-gridfs
%license LICENSE
%doc README.md
%{python3_sitearch}/gridfs


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 4.13.2-3
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 4.13.2-2
- Rebuilt for Python 3.14.0rc2 bytecode

* Tue Jul 29 2025 Gwyn Ciesla <gwync@protonmail.com> - 4.13.2-1
- 4.13.2

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jun 14 2025 Sandro Mani <manisandro@gmail.com> - 4.13.1-1
- Update to 4.13.1

* Fri Jun 13 2025 Sandro Mani <manisandro@gmail.com> - 4.9.1-5
- Add patch to fix build against python 3.14

* Wed Jun 04 2025 Python Maint <python-maint@redhat.com> - 4.9.1-4
- Rebuilt for Python 3.14

* Thu Feb 06 2025 Orion Poplawski <orion@nwra.com> - 4.9.1-3
- Use pytest for tests
- Drop snappy extra on i686

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Sep 20 2024 Jerry James <loganjerry@gmail.com> - 4.9.1-1
- Version 4.9.1
- Fixes CVE-2024-21506 (rhbz#2273860)
- Fixes CVE-2024-5629 (rhbz#2290587)
- Modernize the spec file
- Fix up the license information
- Add check script
- Package the ocsp, snappy, and zstd extras
- Build docs for Fedora only
- Permit use of pytest-asyncio 0.23 until Fedora can catch up

* Wed Sep 04 2024 Miroslav Suchý <msuchy@redhat.com> - 4.2.0-9
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 4.2.0-7
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 4.2.0-3
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Aug 27 2022 Orion Poplawski <orion@nwra.com> - 4.2.0-1
- Update to 4.2.0

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 3.10.1-9
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 3.10.1-6
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 3.10.1-3
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 21 2020 Randy Barlow <bowlofeggs@fedoraproject.org> - 3.10.1-1
- Update to 3.10.1 (#1782385).
- https://github.com/mongodb/mongo-python-driver/blob/3.10.1/doc/changelog.rst

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 3.8.0-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Sun Aug 18 2019 Miro Hrončok <mhroncok@redhat.com> - 3.8.0-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jun 04 2019 Randy Barlow <bowlofeggs@fedoraproject.org> - 3.8.0-1
- Update to 3.8.0 (#1686670).
- http://api.mongodb.com/python/3.8.0/changelog.html

* Tue Mar 26 2019 Randy Barlow <bowlofeggs@fedoraproject.org> - 3.7.2-2
- Drop build dependency on mongodb-server, since it is no longer shipped in Fedora.
- As a result of the above, we no longer run the tests.

* Thu Feb 28 2019 Yatin Karel <ykarel@redhat.com> - 3.7.2-1
- Update to 3.7.2
- http://api.mongodb.com/python/3.7.2/changelog.html

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 28 2019 Miro Hrončok <mhroncok@redhat.com> - 3.7.1-3
- Subpackages python2-bson, python2-pymongo, python2-pymongo-gridfs have been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Mon Dec 10 2018 Honza Horak <hhorak@redhat.com> - 3.7.1-3
- Add bootstrap macro and python2 condition

* Tue Jul 31 2018 Florian Weimer <fweimer@redhat.com> - 3.7.1-2
- Rebuild with fixed binutils

* Mon Jul 30 2018 Randy Barlow <bowlofeggs@fedoraproject.org> - 3.7.1-1
- Update to 3.7.1 (#1601651).
- http://api.mongodb.com/python/3.7.1/changelog.html

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 3.6.1-2
- Rebuilt for Python 3.7

* Sat Mar 10 2018 Randy Barlow <bowlofeggs@fedoraproject.org> - 3.6.1-1
- Update to 3.6.1 (#1550757).
- http://api.mongodb.com/python/3.6.1/changelog.html

* Tue Feb 27 2018 Iryna Shcherbina <ishcherb@redhat.com> - 3.6.0-2
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Mon Feb 19 2018 Marek Skalický <mskalick@redhat.com> - 3.6.0-1
- Rebase to latest release

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild
