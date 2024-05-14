%{!?python3_pkgversion: %global python3_pkgversion 3}
%{!?python3_version: %define python3_version %(python3 -c "import sys; sys.stdout.write(sys.version[:3])")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?__python3: %global __python3 /usr/bin/python3}
%{!?py3_build: %define py3_build CFLAGS="%{optflags}" %{__python3} setup.py build}
%{!?py3_install: %define py3_install %{__python3} setup.py install --skip-build --root %{buildroot}}

%global project_owner readthedocs
%global github_name recommonmark
%global sum docutils-compatibility bridge to CommonMark
%global desc A docutils-compatibility bridge to CommonMark.\
\
This allows you to write CommonMark inside of Docutils & Sphinx projects.\
\
Documentation is available on Read the Docs: https://recommonmark.readthedocs.org

Name:           python-%{github_name}
Version:        0.6.0
Release:        4%{?dist}
Summary:        %{sum}
License:        MIT
URL:            https://github.com/%{project_owner}/%{github_name}
Vendor:         Microsoft
Distribution:   Azure Linux
Source0:        https://github.com/%{project_owner}/%{github_name}/archive/%{version}/%{github_name}-%{version}.tar.gz
BuildArch:      noarch

%description
%{desc}

%package -n     python%{python3_pkgversion}-%{github_name}
Summary:        %{sum}
BuildArch:      noarch
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-docutils
BuildRequires:  python%{python3_pkgversion}-CommonMark
BuildRequires:  python%{python3_pkgversion}-pytest
BuildRequires:  python%{python3_pkgversion}-sphinx
Requires:       python%{python3_pkgversion}-docutils
Requires:       python%{python3_pkgversion}-CommonMark
Requires:       python%{python3_pkgversion}-sphinx
%{?python_provide:%python_provide python%{python3_pkgversion}-%{github_name}}
BuildRequires:  python%{python3_pkgversion}-sphinxcontrib-websupport 
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-xml
Requires:       python%{python3_pkgversion}-sphinxcontrib-websupport

%description -n python%{python3_pkgversion}-%{github_name}
%{desc}

%prep
%setup -qn %{github_name}-%{version}
# Remove upstream's egg-info
rm -rf %{github_name}.egg-info

sed -i '1{\@^#!/usr/bin/env python@d}' recommonmark/scripts.py

%build
%py3_build

%install
#  install python3 first to have unversioned binaries for python 3
%py3_install
pushd %{buildroot}%{_bindir}  # Enter buildroot bindir to ease symlink creation
for cm2bin in cm2*; do
    mv "${cm2bin}" "${cm2bin}-%{python3_version}"
    ln -s "${cm2bin}-%{python3_version}" "${cm2bin}-3"
done
popd  # Leave buildroot bindir

%check
# Skip some tests because of https://github.com/readthedocs/recommonmark/issues/164
# PYTHONPATH=$(pwd) py.test-%{python3_version} -k 'not test_lists and not test_integration' .

%files -n python%{python3_pkgversion}-%{github_name}
%license license.md
%doc README.md
%{python3_sitelib}/%{github_name}-%{version}*-py%{python3_version}.egg-info/
%{python3_sitelib}/%{github_name}/
%{_bindir}/cm2*-3
%{_bindir}/cm2*-%{python3_version}

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.6.0-4
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Wed Oct 21 2020 Steve Laughman <steve.laughman@microsoft.com> - 0.6.0-3
- Initial CBL-Mariner import from Fedora 33 (license: MIT)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-2.git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jul 18 2020 Julien Enselme <jujens@jujens.eu> - 0.6.0-1
- Update to 0.6.0

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.5.0-6.git
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-5.git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.5.0-4.git
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.5.0-3.git
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-2.git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Jul 13 2019 Julien Enselme <jujens@jujens.eu> - 0.5.0-1
- Update to 0.5.0
- Skip some broken tests.

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-19.gitdbed1c4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Oct 20 2018 Julien Enselme <jujens@jujens.eu> - 0.4.0-18.gitdbed1c4
- Bump version

* Sat Oct 20 2018 Julien Enselme <jujens@jujens.eu> - 0.4.0-17.gitdbed1c4
- Fix import of commonmark
- Remove Python 2 subpackage

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-16.gitdbed1c4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.4.0-15.gitdbed1c4
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-14.gitdbed1c4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 27 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.4.0-13.gitdbed1c4
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-12.gitdbed1c4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Feb 22 2017 Julien Enselme <jujens@jujens.eu> - 0.4.0-11.gitdbed1c4
- Fix requires

* Wed Feb 22 2017 Julien Enselme <jujens@jujens.eu> - 0.4.0-10.gitdbed1c4
- Add support for CommonMark 0.7.0

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-9.git7ca5247
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.4.0-8.git7ca5247
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-7.git7ca5247
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Mon Jul 11 2016 Julien Enselme - 0.4.0-6.git7ca5247
- Fix typo in comment

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-5.git7ca5247
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 18 2016 Julien Enselme <jujens@jujens.eu> - 0.4.0-4.git7ca5247
- Move unversionned binaries to python2 subpackage

* Sun Jan 17 2016 Julien Enselme <jujens@jujens.eu> - 0.4.0-3.git7ca5247
- Use tarball from github to have tests and LICENSE
- Add %%check section

* Sat Jan 16 2016 Julien Enselme <jujens@jujens.eu> - 0.4.0-2
- Remove separate source tag for license
- Add binary to python2 subpackage

* Sun Jan 10 2016 Julien Enselme <jujens@jujens.eu> - 0.4.0-1
- Update to 0.4.0

* Thu Dec 31 2015 Julien Enselme <jujens@jujens.eu> - 0.2.0-2
- Add missing dist tag

* Fri Dec 4 2015 Julien Enselme <jujens@jujens.eu> - 0.2.0-1
- Inital package
