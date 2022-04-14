%{!?__python3: %global __python3 /usr/bin/python3}
%{!?__python2: %global __python2 /usr/bin/python2}

%{!?python3_version: %define python3_version %(python3 -c "import sys; sys.stdout.write(sys.version[:3])")}
%{!?python2_version: %define python2_version %(python2 -c "import sys; sys.stdout.write(sys.version[:3])")}

%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

%global pypi_name junitxml

%global with_python2 1

%define py3dir %{_builddir}/python3-build
%define py2dir %{_builddir}/python2-build

Summary:        PyJUnitXML, a pyunit extension to output JUnit compatible XML
Name:           python-%{pypi_name}
Version:        0.7
Release:        24%{?dist}
License:        LGPLv3
Vendor:         Microsoft
Distribution:   Mariner
URL:            https://launchpad.net/pyjunitxml
Source0:        https://pypi.python.org/packages/source/j/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel

%global _description\
PyJUnitXML\
==========\
A Python unittest TestResult that outputs JUnit\
compatible XML.

%description %_description

%package -n python3-%{pypi_name}
Summary: PyJUnitXML, a pyunit extension to output JUnit compatible XML
BuildRequires: python3-devel

%description -n python3-%{pypi_name}
%_description

%if 0%{with_python2}
%package -n python2-%{pypi_name}
Summary: PyJUnitXML, a pyunit extension to output JUnit compatible XML 
BuildRequires: python2-devel
 
%description -n python2-%{pypi_name}
%_description
%endif

%prep
%setup -q -n %{pypi_name}-%{version}
rm -rf %{py3dir}
cp -a . %{py3dir}
%if 0%{with_python2}
rm -rf %{py2dir}
cp -a . %{py2dir}
%endif

%build
pushd %{py3dir}
%{__python3} setup.py build
popd

%if 0%{with_python2}
pushd %{py2dir}
%{__python2} setup.py build
popd
%endif

%install
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
mv %{buildroot}%{_bindir}/pyjunitxml %{buildroot}%{_bindir}/pyjunitxml-%{python3_version}
ln -s ./pyjunitxml-%{python3_version} %{buildroot}%{_bindir}/pyjunitxml-3

%if 0%{with_python2}
pushd %{py2dir}
%{__python2} setup.py install --skip-build --root %{buildroot}
popd
%endif
mv %{buildroot}%{_bindir}/pyjunitxml %{buildroot}%{_bindir}/pyjunitxml-%{python2_version}
ln -s ./pyjunitxml-%{python2_version} %{buildroot}%{_bindir}/pyjunitxml-2

%files -n python3-%{pypi_name}
%license COPYING
%{_bindir}/pyjunitxml-3
%{_bindir}/pyjunitxml-%{python3_version}
%{python3_sitelib}/*

%if 0%{with_python2}
%files -n python2-%{pypi_name}
%license COPYING
%{_bindir}/pyjunitxml-2
%{_bindir}/pyjunitxml-%{python2_version}
%{python2_sitelib}/*
%endif

%changelog
* Fri Oct 30 2020 Steve Laughman <steve.laughman@microsoft.com> - 0.7-24
- Initial CBL-Mariner import from Fedora 33 (license: MIT)
- Add back support for python2
* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild
* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.7-22
- Rebuilt for Python 3.9
* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild
* Mon Sep 23 2019 Gwyn Ciesla <gwync@protonmail.com> - 0.7-20
- Drop Python 2 support, no more consumers.
* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.7-19
- Rebuilt for Python 3.8
* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild
* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild
* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild
* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.7-15
- Rebuilt for Python 3.7
* Mon Feb 12 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.7-14
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)
* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild
* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.7-12
- Python 2 binary package renamed to python2-junitxml
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3
* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild
* Thu Feb 16 2017 Iryna Shcherbina <ishcherb@redhat.com> - 0.7-10
- Fix python-junitxml dragging in both Python 3 and Python 2 (RHBZ#1422933)
* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild
* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.7-8
- Rebuild for Python 3.6
* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-7
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages
* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild
* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild
* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4
* Tue Apr 29 2014 Steve Linabery <slinaber@redhat.com> - 0.7-1
- Initial package.
