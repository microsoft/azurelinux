Vendor:         Microsoft Corporation
Distribution:   Mariner
## START: Set by rpmautospec
## (rpmautospec version 0.3.1)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 1;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

%global sum Google APIs Client Library for Python
%global srcname google-api-client

Name:           google-api-python-client
Summary:        %{sum}
Epoch:          2
Version:        2.73.0
Release:        %autorelease

License:        ASL 2.0
URL:            https://github.com/googleapis/google-api-python-client
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-packaging
BuildRequires:  python3-requests
BuildRequires:  python3-wheel

%description 
Written by Google, this library provides a small, flexible, and powerful
Python client library for accessing Google APIs.

%package -n python3-%{srcname}
Summary:        %{sum}

%description -n python3-%{srcname}
Written by Google, this library provides a small, flexible, and powerful 
Python 3 client library for accessing Google APIs.

%prep
%autosetup

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files googleapiclient apiclient

%files -n python3-%{srcname} -f %{pyproject_files}
%license LICENSE
%doc README.md

%changelog
* Thu Jan 19 2023 Mikel Olasagasti Uranga <mikel@olasagasti.info> - 2:2.73.0-1
- Update to 2.73.0 - Closes rhbz#2160094

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.71.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jan 05 2023 Mikel Olasagasti Uranga <mikel@olasagasti.info> - 2:2.71.0-1
- Update to 2.71.0 - Closes rhbz#2158313

* Sat Dec 17 2022 Mikel Olasagasti Uranga <mikel@olasagasti.info> - 2:2.70.0-1
- Update to 2.70.0 - Closes rhbz#2153632

* Fri Dec 09 2022 Mikel Olasagasti Uranga <mikel@olasagasti.info> - 2:2.69.0-1
- Update to 2.69.0 - Closes rhbz#2152093

* Thu Dec 01 2022 Mikel Olasagasti Uranga <mikel@olasagasti.info> - 2:2.68.0-1
- Update to 2.68.0 - Closes rhbz#2149793

* Fri Nov 18 2022 Mikel Olasagasti Uranga <mikel@olasagasti.info> - 2:2.67.0-1
- Update to 2.67.0 - Closes rhbz#2143475

* Sat Oct 22 2022 Mikel Olasagasti Uranga <mikel@olasagasti.info> - 2:2.65.0-1
- Update to 2.65.0 - Closes rhbz#2132200

* Fri Sep 30 2022 Mikel Olasagasti Uranga <mikel@olasagasti.info> - 2:2.63.0-1
- Update to 2.63.0 - Closes rhbz#2130929

* Wed Sep 21 2022 Mikel Olasagasti Uranga <mikel@olasagasti.info> - 2:2.62.0-1
- Update to 2.62.0 - Closes rhbz#2126570

* Thu Sep 08 2022 Mikel Olasagasti Uranga <mikel@olasagasti.info> - 2:2.60.0-1
- Update to 2.60.0 - Closes rhbz#2124908

* Sun Sep 04 2022 Mikel Olasagasti Uranga <mikel@olasagasti.info> - 2:2.59.0-1
- Update to 2.59.0 - Closes rhbz#2123800

* Wed Aug 24 2022 Mikel Olasagasti Uranga <mikel@olasagasti.info> - 2:2.58.0-1
- Update to 2.58.0 - Closes rhbz#2120893

* Thu Aug 11 2022 Mikel Olasagasti Uranga <mikel@olasagasti.info> - 2:2.56.0-1
- Update to 2.56.0 - Closes rhbz#2117336

* Tue Jul 26 2022 Mikel Olasagasti Uranga <mikel@olasagasti.info> - 2:2.55.0-1
- Update to 2.55.0 - Closes rhbz#2102236

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.51.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jun 16 2022 Python Maint <python-maint@redhat.com> - 2:2.51.0-2
- Rebuilt for Python 3.11

* Wed Jun 15 2022 Mikel Olasagasti Uranga <mikel@olasagasti.info> - 2:2.51.0-1
- Update to 2.51.0 - Closes rhbz#2097445

* Tue Jun 07 2022 Mikel Olasagasti Uranga <mikel@olasagasti.info> - 2:2.50.0-1
- Update to 2.50.0 - Closes rhbz#2094498

* Thu May 26 2022 Mikel Olasagasti Uranga <mikel@olasagasti.info> - 2:2.49.0-1
- Update to 2.49.0 - Closes rhbz#2090697

* Wed May 18 2022 Mikel Olasagasti Uranga <mikel@olasagasti.info> - 2:2.48.0-1
- Update to 2.48.0 - Closes rhbz#2087691

* Wed May 04 2022 Mikel Olasagasti Uranga <mikel@olasagasti.info> - 2:2.47.0-1
- Update to 2.47.0 - Closes rhbz#2079128

* Tue Apr 19 2022 Mikel Olasagasti Uranga <mikel@olasagasti.info> - 2:2.45.0-1
- Update to 2.45.0 - Closes rhbz#2076797

* Wed Apr 13 2022 Mikel Olasagasti Uranga <mikel@olasagasti.info> - 2:2.44.0-1
- Update to 2.44.0 - Closes rhbz#2075142

* Wed Apr 06 2022 Mikel Olasagasti Uranga <mikel@olasagasti.info> - 2:2.43.0-1
- Update to 2.43.0 - Closes rhbz#2066982

* Wed Mar 16 2022 Mikel Olasagasti Uranga <mikel@olasagasti.info> - 2:2.41.0-1
- Update to 2.41.0 - Closes rhbz#2064497

* Fri Mar 11 2022 Mikel Olasagasti Uranga <mikel@olasagasti.info> - 2:2.40.0-1
- Update to 2.40.0 - Closes rhbz#2063202

* Wed Mar 02 2022 Mikel Olasagasti Uranga <mikel@olasagasti.info> - 2:2.39.0-1
- Update to 2.39.0 - Closes rhbz#2059798

* Thu Feb 24 2022 Mikel Olasagasti Uranga <mikel@olasagasti.info> - 2:2.38.0-1
- Update to 2.38.0 - Closes rhbz#2057892

* Wed Feb 09 2022 Mikel Olasagasti Uranga <mikel@olasagasti.info> - 2:2.37.0-1
- Update to 2.37.0

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.36.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jan 19 2022 Mikel Olasagasti Uranga <mikel@olasagasti.info> - 2:2.36.0-1
- Update to 2.36.0 - Closes rhbz#2042177

* Fri Jan 14 2022 Mikel Olasagasti Uranga <mikel@olasagasti.info> - 2:2.35.0-1
- Update to 2.35.0 - Closes rhbz#2040568

* Thu Jan 06 2022 Mikel Olasagasti Uranga <mikel@olasagasti.info> - 2:2.34.0-1
- Update to 2.34.0 - Closes rhbz#2037573

* Wed Dec 08 2021 Mikel Olasagasti Uranga <mikel@olasagasti.info> - 2:2.33.0-1
- Update to 2.33.0 - Fixes rhbz#2030093

* Fri Dec 03 2021 Mikel Olasagasti Uranga <mikel@olasagasti.info> - 2:2.32.0-1
- Update to 2.32.0 BZ#2028797

* Wed Nov 10 2021 Gwyn Ciesla <gwync@protonmail.com> - 2:2.30.0-1
- 2.30.0

* Wed Nov 03 2021 Gwyn Ciesla <gwync@protonmail.com> - 2:2.29.0-1
- 2.29.0

* Wed Oct 27 2021 Mikel Olasagasti Uranga <mikel@olasagasti.info> - 2:2.28.0-1
- Version bump to 2.28

* Mon Oct 25 2021 Mikel Olasagasti Uranga <mikel@olasagasti.info> - 2:2.27.0-1
- Version bump and switch to pyproject-rpm-macros

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.6.7-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2:1.6.7-15
- Rebuilt for Python 3.10

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.6.7-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Sep 16 2020 Gwyn Ciesla <gwync@protonmail.com> - 2:1.6.7-13
- Revert to 1.6.7

* Tue Sep 15 2020 Gwyn Ciesla <gwync@protonmail.com> - 1:1.12.1-1
- 1.12.1

* Fri Aug 28 2020 Gwyn Ciesla <gwync@protonmail.com> - 1:1.11.0-1
- 1.11.0

* Wed Aug 26 2020 Gwyn Ciesla <gwync@protonmail.com> - 1:1.10.1-1
- 1.10.1

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul 16 2020 Gwyn Ciesla <gwync@protonmail.com> - 1:1.10.0-1
- 1.10.0

* Tue Jun 30 2020 Gwyn Ciesla <gwync@protonmail.com> - 1:1.9.3-2
- Requires fix.

* Thu Jun 11 2020 Gwyn Ciesla <gwync@protonmail.com> - 1:1.9.3-1
- Update to 1.9.3

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1:1.6.7-12
- Rebuilt for Python 3.9

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.6.7-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1:1.6.7-10
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1:1.6.7-9
- Rebuilt for Python 3.8

* Wed Jul 31 2019 Miro Hrončok <mhroncok@redhat.com> - 1:1.6.7-8
- Subpackage python2-google-api-client has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.6.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.6.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 28 2019 Michele Baldessari <michele@acksyn.org> - 1.6.7-5
- Add an epoch and downgrade to 1.6.7 while we get python-google-auth-httplib2

* Mon Jan 21 2019 Michele Baldessari <michele@acksyn.org> - 1.7.7-1
- New upstream

* Fri Jul 20 2018 Alfredo Moralejo <amoralej@redhat.com> - 1.6.7-4
- Fix build when disabling python3.

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.6.7-2
- Rebuilt for Python 3.7

* Sat May 05 2018 Michele Baldessari <michele@acksyn.org> - 1.6.7-1
- New upstream

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 19 2018 Michele Baldessari <michele@acksyn.org> - 1.6.5-1
- New upstream

* Mon Oct 23 2017 Michele Baldessari <michele@acksyn.org> - 1.6.4-1
- New upstream

* Sun Sep 10 2017 Nick Bebout <nb@fedoraproject.org> - 1.6.3-2
- Fix BuildRequires/Requires to use python2-* for Fedora

* Thu Aug 31 2017 Michele Baldessari <michele@acksyn.org> - 1.6.3-1
- New upstream

* Fri Aug 4 2017 Nick Bebout <nb@fedoraproject.org> - 1.6.2-2
- Fix conditionals for epel

* Tue Aug 1 2017 Nick Bebout <nb@fedoraproject.org> - 1.6.2-1
- Update to 1.6.2

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.5.5-2
- Rebuild for Python 3.6

* Thu Nov 10 2016 Michele Baldessari <michele@acksyn.org> - 1.5.5-1
New upstream

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Sun May 22 2016 Michele Baldessari <michele@acksyn.org> - 1.5.1-1
- New upstream

* Thu Mar 10 2016 Michele Baldessari <michele@acksyn.org> - 1.5.0-1
- New upstream

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Jan 31 2016 Michele Baldessari <michele@acksyn.org> - 1.4.2-4
- Make spec more epel friendly

* Mon Nov 02 2015 Michele Baldessari <michele@acksyn.org> - 1.4.2-3
- Cleanup spec according to newest python policy
- Drop python3 conditional, we'll build this for Fedora only for now anyways

* Wed Oct 21 2015 Michele Baldessari <michele@acksyn.org> - 1.4.2-2
- Address some comments from BZ 1272187

* Thu Oct 15 2015 Michele Baldessari <michele@acksyn.org> - 1.4.2-1
- Update to 1.4.2

* Tue Jun 23 2015 Michele Baldessari <michele@acksyn.org> - 1.4.1-1
- Update to 1.4.1

* Sun Jun 07 2015 Michele Baldessari <michele@acksyn.org> - 1.4.0-1
- Update to latest version
- Add python3 package
- Tag LICENSE with appropriate macro
- Generate {python,python3}-google-api-client packages to be more consistent
  within Fedora
- Add python-oauthclient dependency

* Sat Feb 14 2015 Ankur Sinha <ankursinha AT fedoraproject DOT org> 1.3.1-1
- Update to latest version

* Sat Jul 27 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 1.1-1
- Initial rpm package


