Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global mod_name blinker

Name:           python-blinker
Version:        1.4
Release:        10%{?dist}
Summary:        Fast, simple object-to-object and broadcast signaling

License:        MIT
URL:            https://pythonhosted.org/blinker/
Source0:        https://pypi.python.org/packages/source/b/%{mod_name}/%{mod_name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%global _description\
Blinker provides a fast dispatching system that allows any number\
of interested parties to subscribe to events, or "signals".

%description %_description

%package -n python3-blinker
Summary:        Fast, simple object-to-object and broadcast signaling
%{?python_provide:%python_provide python3-blinker}

%description -n python3-blinker
Blinker provides a fast dispatching system that allows any number 
of interested parties to subscribe to events, or "signals".

%prep
%setup -q -n %{mod_name}-%{version}


%build
%py3_build

%install
%py3_install

 
%files -n python3-blinker
%doc docs/ CHANGES LICENSE README.md PKG-INFO
%{python3_sitelib}/*.egg-info
%{python3_sitelib}/%{mod_name}


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.4-10
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.4-8
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Fri Aug 30 2019 Miro Hrončok <mhroncok@redhat.com> - 1.4-7
- Subpackage python2-blinker has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Thu Aug 15 2019 Miro Hrončok <mhroncok@redhat.com> - 1.4-6
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 1.4-2
- Rebuilt for Python 3.7

* Sat Jun 16 2018 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 1.4-1
- new version

* Fri Jun 15 2018 Miro Hrončok <mhroncok@redhat.com> - 1.3-15
- Rebuilt for Python 3.7

* Sun Feb 11 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.3-14
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.3-12
- Python 2 binary package renamed to python2-blinker
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec 13 2016 Stratakis Charalampos <cstratak@redhat.com> - 1.3-9
- Rebuild for Python 3.6

* Tue Dec 13 2016 Stratakis Charalampos <cstratak@redhat.com> - 1.3-8
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-7
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Tue Sep 24 2013 Praveen Kumar <kumarpraveen.nitdgp@gmail.com> - 1.3-1
- Updated source and added python3 support

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jul 22 2011 Praveen Kumar <kumarpraveen.nitdgp@gmail.com> - 1.1-1
- Initial RPM
