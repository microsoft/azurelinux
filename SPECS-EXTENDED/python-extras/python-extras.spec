%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?__python3: %global __python3 /usr/bin/python3}
%{!?py3_build: %define py3_build CFLAGS="%{optflags}" %{__python3} setup.py build}
%{!?py3_install: %define py3_install %{__python3} setup.py install --skip-build --root %{buildroot}}

%bcond_with check

# NOTE(hguemar): discussed with maintainer to allow rebuild on RHEL/CentOS
# No impact on Fedora/EPEL!

Summary:        Useful extra bits for Python
Name:           python-extras
Version:        1.0.0
Release:        15%{?dist}
License:        MIT
URL:            https://github.com/testing-cabal/extras
Vendor:         Microsoft
Distribution:   Mariner
Source0:        https://pypi.io/packages/source/e/extras/extras-%{version}.tar.gz
BuildArch:      noarch

%global _description\
extras is a set of extensions to the Python standard library, originally\
written to make the code within testtools cleaner, but now split out for\
general use outside of a testing context.\

%description %_description

%package -n python3-extras
Summary:        %summary
%{?python_provide:%python_provide python3-extras}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
#%if %{with check}
#BuildRequires:  python3-testtools
#%endif

%description -n python3-extras %_description

%prep
%setup -q -n extras-%{version}
# Remove bundled egg-info
rm -vrf *.egg-info

%build
%py3_build

%install
%py3_install

#%if %{with check}
#%check
#%{__python3} setup.py test
#%endif

%files -n python3-extras
%license LICENSE
%doc NEWS
%doc README.rst
%{python3_sitelib}/extras/
%{python3_sitelib}/extras-*.egg-info/

%changelog
* Tue Oct 13 2020 Steve Laughman <steve.laughman@microsoft.com> - 1.6.0-15
- Initial CBL-Mariner import from Fedora 33 (license: MIT)
- Disable circular dependency check

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 1.0.0-13
- Rebuilt for Python 3.9

* Fri May 22 2020 Miro Hrončok <mhroncok@redhat.com> - 1.0.0-12
- Bootstrap for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.0.0-10
- Subpackage python2-extras has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Aug 17 2019 Miro Hrončok <mhroncok@redhat.com> - 1.0.0-9
- Rebuilt for Python 3.8

* Wed Aug 14 2019 Miro Hrončok <mhroncok@redhat.com> - 1.0.0-8
- Bootstrap for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 18 2018 Miro Hrončok <mhroncok@redhat.com> - 1.0.0-4
- Rebuilt for Python 3.7

* Thu Jun 14 2018 Miro Hrončok <mhroncok@redhat.com> - 1.0.0-3
- Bootstrap for Python 3.7

* Tue Feb  6 2018 Haïkel Guémar <hguemar@fedoraproject.org> - 1.0.0-2
- Fix build on EL7

* Sat Sep  2 2017 Jan Beran <jberan@redhat.com> - 1.0.0-1
- New version

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.0.3-17
- Python 2 binary package renamed to python2-extras
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.3-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.3-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec 13 2016 Stratakis Charalampos <cstratak@redhat.com> - 0.0.3-14
- Enable tests

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 0.0.3-13
- Rebuild for Python 3.6
- Disable tests

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.3-12
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Nov 14 2015 Toshio Kuratomi <toshio@fedoraproject.org> - - 0.0.3-10
- And now re-enable

* Sat Nov 14 2015 Toshio Kuratomi <toshio@fedoraproject.org> - - 0.0.3-9
- Temporarily disable tests to bootstrap past a dep loop

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.3-8
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 16 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.0.3-5
- Enable tests again.

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4
- Bootstrap tests to break circular dependency with python-testtools

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed May 29 2013 Matthias Runge <mrunge@redhat.com> - 0.0.3-2
- spec cleanup and enable tests

* Wed May  1 2013 Michel Salim <salimma@fedoraproject.org> - 0.0.3-1
- Initial package
