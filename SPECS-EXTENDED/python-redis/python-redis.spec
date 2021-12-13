%{!?python3_pkgversion: %global python3_pkgversion 3}
%{!?python3_version: %define python3_version %(python3 -c "import sys; sys.stdout.write(sys.version[:3])")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?__python3: %global __python3 /usr/bin/python3}
%{!?py3_build: %define py3_build CFLAGS="%{optflags}" %{__python3} setup.py build}
%{!?py3_install: %define py3_install %{__python3} setup.py install --skip-build --root %{buildroot}}

%global upstream_name redis

Name:           python-%{upstream_name}
Version:        3.5.3
Release:        2%{?dist}
Summary:        Python interface to the Redis key-value store
License:        MIT
URL:            https://github.com/andymccurdy/redis-py
#Source0:       https://github.com/andymccurdy/redis-py/archive/%{version}.tar.gz
Source0:        https://github.com/andymccurdy/redis-py/archive/%{name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  redis

%global _description\
This is a Python interface to the Redis key-value store.

%description %_description

%package -n     python3-redis
Summary:        Python 3 interface to the Redis key-value store
%{?python_provide:%python_provide python3-redis}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-py
BuildRequires:  python3-pytest
BuildRequires:  python3-mock

%description -n python3-redis
This is a Python 3 interface to the Redis key-value store.

%prep
%setup -qn redis-py-%{version}
rm -frv %{upstream_name}.egg-info

# This test passes locally but fails in koji...
rm tests/test_commands.py*

%build
%py3_build

%install
%py3_install

%check
redis-server &
%{__python3} -m pytest
kill %1

%files -n python3-redis
%doc CHANGES LICENSE README.rst
%{python3_sitelib}/%{upstream_name}
%{python3_sitelib}/%{upstream_name}-%{version}-py%{python3_version}.egg-info

%changelog
* Wed Dec 09 2020 Steve Laughman <steve.laughman@microsoft.com> - 3.5.3-2
- Initial CBL-Mariner import from Fedora 33 (license: MIT)
* Tue Sep 15 2020 Joel Capitao <jcapitao@redhat.com> - 3.5.3-1
- Update to 3.5.3
* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild
* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 3.4.1-2
- Rebuilt for Python 3.9
* Mon Mar 16 2020 Clément Verna <cverna@fedoraproject.org> - 3.4.1-1
- Update to 3.4.1.
- Use pytest to run the unit tests.
* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild
* Sun Oct 06 2019 Kevin Fenzi <kevin@scrye.com> - 3.3.8-1
- Update to 3.3.8.
* Sun Sep 08 2019 Miro Hrončok <mhroncok@redhat.com> - 3.2.1-4
- Subpackage python2-redis has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal
* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 3.2.1-3
- Rebuilt for Python 3.8
* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild
* Sat Jun 22 2019 Kevin Fenzi <kevin@scrye.com> - 3.2.1-1
- Update to 3.2.1. Fixes bug #1670235
* Mon Feb 11 2019 Javier Peña <jpena@redhat.com> - 3.1.0-1
- Update to 3.1.0. Fixes bug #1670235
* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild
* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild
* Sat Jun 16 2018 Miro Hrončok <mhroncok@redhat.com> - 2.10.6-4
- Rebuilt for Python 3.7
* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild
* Sat Jan 27 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2.10.6-2
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)
* Sun Dec 17 2017 Kevin Fenzi <kevin@scrye.com> - 2.10.6-1
- Update to 2.10.6. Fixes bug #1482297
* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.10.5-6
- Python 2 binary package renamed to python2-redis
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3
* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild
* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild
* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 2.10.5-3
- Rebuild for Python 3.6
* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10.5-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages
* Mon Apr 04 2016 Ralph Bean <rbean@redhat.com> - 2.10.5-1
- new version
* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild
* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10.3-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5
* Fri Jul 10 2015 Ralph Bean <rbean@redhat.com> - 2.10.3-3
- Remove test that fails erroneously in koji.
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild
* Thu Aug 21 2014 Christopher Meng <rpm@cicku.me> - 2.10.3-1
- Update to 2.10.3
* Tue Aug 12 2014 Christopher Meng <rpm@cicku.me> - 2.10.2-1
- Update to 2.10.2
* Thu Jun 19 2014 Christopher Meng <rpm@cicku.me> - 2.10.1-1
- Update to 2.10.1
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild
* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 2.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4
* Fri Feb 14 2014 Christopher Meng <rpm@cicku.me> - 2.9.1-1
- Update to 2.9.1
- Use generated egg instead of bundled egg
- Cleanup again
* Sat Jul 27 2013 Luke Macken <lmacken@redhat.com> - 2.7.6-1
- Update to 2.7.6
- Run the test suite
- Add a python3 subpackage
- Remove obsolete buildroot tag and cleanup
* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild
* Thu Dec 27 2012 Silas Sewell <silas@sewell.org> - 2.7.2-1
- Update to 2.7.2
* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild
* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild
* Sun Jul 24 2011 Silas Sewell <silas@sewell.org> - 2.4.9-1
- Update to 2.4.9
* Sun Mar 27 2011 Silas Sewell <silas@sewell.ch> - 2.2.4-1
- Update to 2.2.4
* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild
* Sat Sep 04 2010 Silas Sewell <silas@sewell.ch> - 2.0.0-1
- Initial build