%{!?python3_pkgversion: %global python3_pkgversion 3}
%{!?python3_version: %define python3_version %(python3 -c "import sys; sys.stdout.write(sys.version[:3])")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?__python3: %global __python3 /usr/bin/python3}
%{!?py3_build: %define py3_build CFLAGS="%{optflags}" %{__python3} setup.py build}
%{!?py3_install: %define py3_install %{__python3} setup.py install --skip-build --root %{buildroot}}

Summary:        Specification-style output for python-nose
Name:           python-spec
Version:        1.4.1
Release:        6%{?dist}
License:        MIT
URL:            https://github.com/bitprophet/spec
#Source0:       https://files.pythonhosted.org/packages/source/s/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
Source0:        https://files.pythonhosted.org/packages/source/s/%{pypi_name}/%{name}-%{version}.tar.gz
#Source1:       https://files.pythonhosted.org/packages/source/s/%{pypi_name}/%{pypi_name}-%{version}.tar.gz.asc
Source1:        https://files.pythonhosted.org/packages/source/s/%{pypi_name}/%{name}-%{version}.tar.gz.asc
# The following keyring is made from the public key shown on: http://bitprophet.org/bio/
# It has fingerprint 0C8AFED2B8FDD7AF40F809BA9C29BC560041E930
# Keyring created by importing that key and using the output of:
# gpg2 --export --export-options export-minimal 0C8AFED2B8FDD7AF40F809BA9C29BC560041E930
Source2:        gpgkey-0C8AFED2B8FDD7AF40F809BA9C29BC560041E930.gpg
Source3:        https://raw.githubusercontent.com/bitprophet/spec/master/LICENSE
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  gnupg2
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%description
A Python testing tool that provides:

* Colorized, specification style output
* Colorized tracebacks and summary
* Test-running CLI tool that enables useful non-default options and implements
  relaxed test discovery for less test_annoying.py:TestBoilerplate.test_code
  and more readable.py:Classes.and_methods.

%package -n python3-spec
Summary:        Specification-style output for python3-nose
BuildRequires:  python3-nose >= 1.3
BuildRequires:  python3-six
%{?python_provide:%python_provide python3-spec}

%description -n python3-spec
A Python testing tool that provides:

* Colorized, specification style output
* Colorized tracebacks and summary
* Test-running CLI tool that enables useful non-default options and implements
  relaxed test discovery for less test_annoying.py:TestBoilerplate.test_code
  and more readable.py:Classes.and_methods.

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'

%setup -q -n spec-%{version}

# LICENSE file
cp -p %{SOURCE3} .

# Remove bundled egg-info
rm -rf spec.egg-info

%build
%py3_build

%install
%py3_install

%files -n python3-spec
%license LICENSE
%{_bindir}/spec
%{python3_sitelib}/spec/
%{python3_sitelib}/spec-*.egg-info/

%changelog
* Wed Dec 09 2020 Steve Laughman <steve.laughman@microsoft.com> - 1.4.1-6
- Initial CBL-Mariner import from Fedora 33 (license: MIT)
* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild
* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 1.4.1-4
- Rebuilt for Python 3.9
* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild
* Fri Dec 20 2019 Paul Howarth <paul@city-fan.org> - 1.4.1-2
- Incorporate feedback from package review (#1785391)
  - Use %%pypi_source macro
  - Use %%python_provide macro
  - Runtime python dependencies detected automatically since F-30, EL-8
  - Fix egg-info globbing in %%files list
  - Add GPG source verification in %%prep section
  - Update LICENSE file (updated copyright date)
* Wed Dec 11 2019 Paul Howarth <paul@city-fan.org> - 1.4.1-1
- Update to 1.4.1
- Strip out Python 2 support
* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild
* Sun Dec  6 2015 Toshio Kuratomi <toshio@fedoraproject.org> - - 1.0.0-5
- Add provides for python2-spec
* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5
* Thu Nov  5 2015 Toshio Kuratomi <toshio@fedoraproject.org> - 1.0.0-3
- Fix the python2 and python3 scripts to coexist according to the
  Packaging:Python guidelines
- Fix dist tag
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild
* Sat Mar 28 2015 Eduardo Mayorga Téllez <mayorga@fedoraproject.org> - 1.0.0-1
- Update to 1.0.0
* Sun Aug 03 2014 Eduardo Mayorga Téllez <mayorga@fedoraproject.org> - 0.11.1-2
- Changing Requires from python2- to python-
* Tue Jul 29 2014 Eduardo Mayorga Téllez <mayorga@fedoraproject.org> - 0.11.1-1
- Initial packaging