# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global         srcname  aioresponses
%global         desc     Aioresponses is a helper to mock/fake web requests in the python\
aiohttp package. The purpose of this package is to provide an\
easy way  to test asynchronous HTTP requests.

Name:           python-%{srcname}
Version:        0.7.8
Release:        5%{?dist}
Summary:        Mock out requests made by ClientSession from aiohttp package

License:        MIT
URL:            https://github.com/pnuckowski/aioresponses
Source0:        %pypi_source

BuildArch:      noarch
# Since python-aiohttp excludes s390x we have to exclude it, as well
# See also:
# https://src.fedoraproject.org/rpms/python-aiohttp/blob/67855c61bee706fcd99305d1715aad02d898cbfc/f/python-aiohttp.spec#_22
# https://fedoraproject.org/wiki/EPEL/FAQ#RHEL_8.2B_has_binaries_in_the_release.2C_but_is_missing_some_corresponding_-devel_package._How_do_I_build_a_package_that_needs_that_missing_-devel_package.3F
%if %{defined el8}
ExcludeArch:    s390x
%endif


# required for py3_build macro
BuildRequires:  python3-devel

# from setup.py
BuildRequires: python3-pbr
BuildRequires: python3-aiohttp

## for tests
BuildRequires: python3-pytest
BuildRequires: python3-pytest-cov
BuildRequires: python3-ddt

%{?python_enable_dependency_generator}

%description
%{desc}

%package -n python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
%{desc}

%prep
%autosetup -p1 -n %{srcname}-%{version}


%build
%py3_build


%install
%py3_install


%check
# disable tests that connect to httpbin.org
%pytest -v -k 'not test_address_as_instance_of_url_combined_with_pass_through and not test_pass_through_with_origin_params and not test_pass_through_unmatched_requests'


%files -n python3-%{srcname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{srcname}/
%{python3_sitelib}/%{srcname}-*-py*.egg-info/


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.7.8-5
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.7.8-4
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 0.7.8-2
- Rebuilt for Python 3.14

* Sun May 11 2025 Georg Sauthoff <mail@gms.tf> - 0.7.8-1
- bump version (fixes fedora#2338886)

* Sun Jan 19 2025 Georg Sauthoff <mail@gms.tf> - 0.7.7-1
- bump version (fixes fedora#2326558)

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Oct 22 2024 Tomáš Hrnčiar <thrnciar@redhat.com> - 0.7.6-6
- Add compatibility to setuptools 74+
- Fixes: rhbz#2319639

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.7.6-4
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Nov 25 2023 Georg Sauthoff <mail@gms.tf> - 0.7.6-1
- bump version (fixes fedora#2249536)

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 29 2023 Python Maint <python-maint@redhat.com> - 0.7.4-2
- Rebuilt for Python 3.12

* Sun Jan 29 2023 Georg Sauthoff <mail@gms.tf> - 0.7.4-1
- bump version (fixes fedora#2153091)

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 14 2022 Python Maint <python-maint@redhat.com> - 0.7.3-2
- Rebuilt for Python 3.11

* Sat Feb 05 2022 Georg Sauthoff <mail@gms.tf> - 0.7.3-1
- bump version (fixes fedora#2039096)

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Dec 14 2021 Georg Sauthoff <mail@gms.tf> - 0.7.2-5
- Fix dependency issue in rawhide -> rollback (cf. #2026630)

* Tue Dec 14 2021 Georg Sauthoff <mail@gms.tf> - 0.7.2-4
- Fix dependency issue in rawhide

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.7.2-2
- Rebuilt for Python 3.10

* Sat Mar 20 2021 Georg Sauthoff <mail@gms.tf> - 0.7.2-1
- bump version (fixes fedora#1936797 - python-aioresponses-0.7.2 is available)

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Dec 05 2020 Georg Sauthoff <mail@gms.tf> - 0.7.1-1
- bump version

* Thu Sep 10 2020 Georg Sauthoff <mail@gms.tf> - 0.6.4-3
- EPEL8: exclude s390x because of aiohttp

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun Jun 21 2020 Georg Sauthoff <mail@gms.tf> - 0.6.4-1
- Skip asynctest dependency for Python 3.9
- bump to latest upstream

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.6.3-2
- Rebuilt for Python 3.9

* Fri May 01 2020  Georg Sauthoff <mail@gms.tf> - 0.6.3-1
- bump to latest upstream

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Dec 08 2019  Georg Sauthoff <mail@gms.tf> - 0.6.1-2
- bump to latest upstream

* Sun Dec 08 2019  Georg Sauthoff <mail@gms.tf> - 0.6.1-1
- bump to latest upstream

* Fri Dec 06 2019 Georg Sauthoff <mail@gms.tf> - 0.6.0-4
- remove superfluous watchdog dependency

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.6.0-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Mar 26 2019 Georg Sauthoff <mail@gms.tf> - 0.6.0-1
- initial packaging
