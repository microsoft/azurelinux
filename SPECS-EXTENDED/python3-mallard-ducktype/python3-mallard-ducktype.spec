Vendor:         Microsoft Corporation
Distribution:   Mariner
%global srcname mallard-ducktype

Name:    python3-mallard-ducktype
Version: 1.0.2
Release: 6%{?dist}
Summary: Parse Ducktype files and convert them to Mallard

License: MIT
URL:     https://pypi.python.org/pypi/%{srcname}
# The PyPI tarball does not have AUTHORS or COPYING.
Source0: https://github.com/projectmallard/%{srcname}/archive/%{version}/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildArch:     noarch
BuildRequires: python3-devel

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
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.2-6
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

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
