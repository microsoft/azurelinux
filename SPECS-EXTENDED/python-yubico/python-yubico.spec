Vendor:         Microsoft Corporation
Distribution:   Mariner
%{?python_enable_dependency_generator}
%global srcname yubico

Name:           python-%{srcname}
Version:        1.3.3
Release:        2%{?dist}
Summary:        Pure-python library for interacting with Yubikeys

License:        BSD
URL:            https://github.com/Yubico/%{name}
Source0:        https://github.com/Yubico/%{name}/archive/%{name}-%{version}.tar.gz

BuildArch:      noarch

%description
Pure-python library for interacting with Yubikeys


%package -n python3-%{srcname}
Summary:        Pure-python library for interacting with Yubikeys
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-nose
BuildRequires:  python3-pyusb

%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
Pure-python library for interacting with Yubikeys. For Python 3.


%prep
%autosetup -n %{name}-%{name}-%{version} -p1


%build
%py3_build


%install
%py3_install


%check
nosetests-%{python3_version} -e test_challenge_response -e test_serial -e test_status


%files -n python3-%{srcname}
%license COPYING
%doc NEWS README
%{python3_sitelib}/*


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.3.3-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Mar 05 2020 Mohan Boddu <mboddu@bhujji.com> - 1.3.3-1
- Update to 1.3.3
- Removing py3 patches

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Oct 21 2019 Miro Hrončok <mhroncok@redhat.com> - 1.3.2-17
- Drop forgotten build dependency on python2-pyusb

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.3.2-16
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Sun Aug 18 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.3.2-15
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jan 11 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.3.2-12
- Enable python dependency generator

* Wed Jan 09 2019 Miro Hrončok <mhroncok@redhat.com> - 1.3.2-11
- Subpackage python2-yubico has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.3.2-9
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 24 2017 Nathaniel McCallum <npmccallum@redhat.com> - 1.3.2-7
- Backport an upstream python3 fix (#1484862)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.3.2-4
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed May 11 2016 Nathaniel McCallum <npmccallum@redhat.com> - 1.3.2-2
- Add missing provide for python-yubico
- Add missing obsoletes for python-yubico

* Tue May 10 2016 Nathaniel McCallum <npmccallum@redhat.com> - 1.3.2-1
- Cleanup obsolete conditions (like RHEL 6)
- Update to v1.3.2

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 11 2016 Will Thompson <will@willthompson.co.uk> - 1.2.3-5
- Add python3-pyusb dependency to python3 subpackage (#1278210)

* Mon Jan 11 2016 Ville Skyttä <ville.skytta@iki.fi>
- Ship COPYING as %%license where applicable

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Mon Jul 20 2015 Miro Hrončok <mhroncok@redhat.com> - 1.2.3-3
- Add Python 3 subpackage (#1244237)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Mar 23 2015 Nathaniel McCallum <npmccallum@redhat.com> - 1.2.3-1
- Upstream 1.2.3
- Require pyusb during building when running tests

* Mon Jun 23 2014 Nathaniel McCallum <npmccallum@redhat.com> - 1.2.1-3
- Enable build on EL6.

* Sat Jun 21 2014 Nathaniel McCallum <npmccallum@redhat.com> - 1.2.1-2
- Run upstream tests during build.

* Thu Jun 19 2014 Nathaniel McCallum <npmccallum@redhat.com> - 1.2.1-1
- Initial release.
