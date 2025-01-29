Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global srcname mallard-ducktype

Name:    python3-mallard-ducktype
Version: 1.0.2
Release: 22%{?dist}
Summary: Parse Ducktype files and convert them to Mallard

License: MIT
URL:     https://pypi.python.org/pypi/%{srcname}
# The PyPI tarball does not have AUTHORS or COPYING.
Source0: https://github.com/projectmallard/%{srcname}/archive/%{version}/%{version}.tar.gz

BuildArch:     noarch
BuildRequires: python3-devel
BuildRequires: python3-setuptools

%description
Parse Ducktype files and convert them to Mallard.


%prep
%setup -q -n %{srcname}-%{version}


%build
%py3_build


%install
%py3_install


%check
%{__python3} setup.py test


%files
%doc AUTHORS README.md
%license COPYING
%{_bindir}/ducktype
%{python3_sitelib}/*



%changelog
* Thu Jan 16 2025 Archana Shettigar <v-shettigara@microsoft.com> - 1.0.2-22
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License Verified

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.0.2-20
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 1.0.2-16
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.0.2-13
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.0.2-10
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jun 24 2020 David King <amigadave@amigadave.com> - 1.0.2-7
- BuildRequire python3-setuptools explicitly

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.0.2-6
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.0.2-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.0.2-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jul 21 2019 David King <amigadave@amigadave.com> - 1.0.2-1
- Update to 1.0.2

* Sun Apr 28 2019 David King <amigadave@amigadave.com> - 1.0.1-1
- Update to 1.0.1 (#1703831)

* Mon Apr 08 2019 David King <amigadave@amigadave.com> - 1.0-1
- Update to 1.0 (#1697490)

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 23 2019 David King <amigadave@amigadave.com> - 0.4-1
- Update to 0.4

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.3-3
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Oct 10 2017 David King <amigadave@amigadave.com> - 0.3-1
- Update to 0.3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.2-6
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-5
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Wed Sep 09 2015 David King <amigadave@amigadave.com> - 0.2-2
- Add backported UTF-8 encoding patch

* Tue Sep 08 2015 David King <amigadave@amigadave.com> - 0.2-1
- Update to 0.2

* Fri Sep 04 2015 David King <amigadave@amigadave.com> - 0.1-1
- Initial Fedora packaging (#1260219)
