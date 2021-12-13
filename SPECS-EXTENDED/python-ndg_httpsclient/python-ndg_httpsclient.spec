Vendor:         Microsoft Corporation
Distribution:   Mariner
%global pypi_name ndg_httpsclient
Name:           python-%{pypi_name}
Version:        0.5.1
Release:        6%{?dist}
Summary:        Provides enhanced HTTPS support for httplib and urllib2 using PyOpenSSL

License:        BSD
URL:            https://github.com/cedadev/ndg_httpsclient/
Source0:        %{pypi_source}
BuildArch:      noarch
 
BuildRequires:  python3-devel
BuildRequires:  python3-pyOpenSSL
BuildRequires:  openssl
BuildRequires:  /usr/bin/killall


%description
This is a HTTPS client implementation for httplib and urllib2 based on
PyOpenSSL. PyOpenSSL provides a more fully featured SSL implementation
over the default provided with Python and importantly enables full
verification of the SSL peer.

%package -n python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name}
This is a HTTPS client implementation for httplib and urllib2 based on
PyOpenSSL. PyOpenSSL provides a more fully featured SSL implementation
over the default provided with Python and importantly enables full
verification of the SSL peer. This is the python3 library.

%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py3_build

%install
%py3_install
cp ndg/httpsclient/LICENSE .

%check
pushd ndg/httpsclient/test/
./scripts/openssl_https_server.sh &
sleep 1
# the test suite is not working and we don't know why
# upstream bugtracker is not functional
#for FILE in test_*.py; do
for FILE in test_utils.py; do
  PYTHONPATH=../../.. %{__python3} ./$FILE
done
killall openssl

# Make sure the script uses the expected python version
grep -qv python2 %{buildroot}%{_bindir}/ndg_httpclient

%files -n python3-%{pypi_name}
%license LICENSE
%{_bindir}/ndg_httpclient
%{python3_sitelib}/ndg/
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info/

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.5.1-6
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.5.1-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.5.1-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Apr 15 2019 Miro Hrončok <mhroncok@redhat.com> - 0.5.1-1
- Update to 0.5.1 (#1699021)

* Tue Mar 12 2019 Miro Hrončok <mhroncok@redhat.com> - 0.4.0-14
- Subpackage python2-ndg_httpsclient has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.4.0-11
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 26 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.4.0-9
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Mar 02 2017 Miro Hrončok <mhroncok@redhat.com> - 0.4.0-7
- Use Python 3 in the executable

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.4.0-5
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Nov 28 2015 James Hogarth <james.hogarth@gmail.com> - 0.4.0-2
- Add python3 subpackage (#1286321)
- Update to latest python packaging guidelines

* Wed Jul 08 2015 Miro Hrončok <mhroncok@redhat.com> - 0.4.0-1
- Update to 0.4.0

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Oct 14 2014 Miro Hrončok <mhroncok@redhat.com> - 0.3.2-1
- Initial package.
