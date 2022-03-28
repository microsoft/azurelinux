Vendor:         Microsoft Corporation
Distribution:   Mariner
%global project_owner avakar
%global github_name pytoml
%global sum Parser for TOML
%global desc A parser for TOML-0.4.0

%bcond_with python2

# The support for TOML 4 in python-toml is not complete. I (Julien Enselme)
# tried to improve it (I contributed for inline object # support) but the
# upstream maintainer is slow to respond and still hasn't published a
# new version with this support. Furthermore, I find the code hard to read and
# modify. From what I looked at pytoml, it is better written, has a better
# support of toml including edge cases.

# I'd recommend python-pytoml but for some usage, python-toml will do the
# trick just fine (I find it a little easier to use). That's why I'll keep
# maintaining it for the foreseeable future.

Name:           python-%{github_name}
Version:        0.1.18
Release:        9%{?dist}
Summary:        %{sum}

License:        MIT
# Take source from github since the license file is not provided in pypi release.
URL:            https://github.com/%{project_owner}/%{github_name}
Source0:        https://github.com/%{project_owner}/%{github_name}/archive/v%{version}/%{github_name}-%{version}.tar.gz#/python-%{github_name}-%{version}.tar.gz
BuildArch:      noarch

%description
%{desc}


%if %{with python2}
%package -n     python2-%{github_name}
BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
Summary:        %{sum}
%{?python_provide:%python_provide python2-%{github_name}}

%description -n python2-%{github_name}
%{desc}
%endif # with python2


%package -n     python%{python3_pkgversion}-%{github_name}
Summary:        %{sum}
BuildArch:      noarch
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
%{?python_provide:%python_provide python%{python3_pkgversion}-%{github_name}}

%if %{without python2}
Obsoletes:      python-%{github_name} < %{version}-%{release}
Obsoletes:      python2-%{github_name} < %{version}-%{release}
%endif # without python2


%description -n python%{python3_pkgversion}-%{github_name}
%{desc}


%prep
%setup -qn %{github_name}-%{version}


%build
%if %{with python2}
%py2_build
%endif # with python2

%py3_build


%install
%py3_install

%if %{with python2}
%py2_install
%endif # with python2


# We cannot run check for now: the README ask to use git submodules, but we
# can't just use git submodules because it requires network access and pull code
# that is not from the package. The good way to do this would be to package the
# go program that include the tests file. It was done for python-toml that rely
# on golang-github-BurntSushi-toml-test. The problem is pytoml cannot pass this
# suite since it is outdated. The maintainer of pytoml uses his own fork of
# golang-github-BurntSushi-toml-test which has no release. So until improvement
# on that side, it's better not to run check within %%check and trust the
# upstream maintainer won't release broken stuff.


%if %{with python2}
%files -n python2-%{github_name}
%doc README.md
%license LICENSE
%{python2_sitelib}/%{github_name}-%{version}*-py%{python2_version}.egg-info/
%{python2_sitelib}/%{github_name}/
%endif # with python2


%files -n python%{python3_pkgversion}-%{github_name}
%doc README.md
%license LICENSE
%{python3_sitelib}/%{github_name}-%{version}*-py%{python3_version}.egg-info/
%{python3_sitelib}/%{github_name}/


%changelog
* Thu Feb 04 2021 Joe Schmitt <joschmit@microsoft.com> - 0.1.18-9
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Remove Fedora version check for python version

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.18-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.1.18-7
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Wed Aug 14 2019 Miro Hrončok <mhroncok@redhat.com> - 0.1.18-6
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Nov 04 2018 Julien Enselme <jujens@jujens.eu> - 0.1.18-2
- Disable Python 2 subpackage on epel 7

* Wed Aug 01 2018 Julien Enselme <jujens@jujens.eu> - 0.1.18-1
- Update to 0.1.18

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 0.1.17-2
- Rebuilt for Python 3.7

* Sat Jun 30 2018 Julien Enselme <jujens@jujens.eu> - 0.1.17-1
- Update to 0.1.17

* Mon Jun 18 2018 Miro Hrončok <mhroncok@redhat.com> - 0.1.16-2
- Rebuilt for Python 3.7

* Sat Jun 16 2018 Julien Enselme <jujens@jujens.eu> - 0.1.16-1
- Update to 0.1.16

* Fri Mar 16 2018 Tomas Orsava <torsava@redhat.com> - 0.1.14-5.git7dea353
- Conditionalize the Python 2 subpackage
- Don't build the Python 2 subpackage on EL > 7 and Fedora > 28

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.14-4.git7dea353
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 27 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.1.14-3.git7dea353
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.14-2.git7dea353
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jul 01 2017 Julien Enselme <jujens@jujens.eu> - 0.1.14-1.git7dea353
- Update to 0.1.14

* Mon May 22 2017 Julien Enselme <jujens@jujens.eu> - 0.1.13-1.git270397b
- Update ot 0.1.13

* Thu Apr 13 2017 Julien Enselme <jujens@jujens.eu> - 0.1.12-1.gite4ec5fb
- Update to 0.1.12

* Tue Mar 21 2017 Julien Enselme <jujens@jujens.eu> - 0.1.11-4.git01d900f
- Use %%{python3_pkgversion} to build for epel
- Add a BR to setuptools

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.11-3.git01d900f
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.1.11-2.git01d900f
- Rebuild for Python 3.6

* Mon Aug 22 2016 Julien Enselme <jujens@jujens.eu> - 0.1.11-1.git01d900f
- Update to 0.1.11

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.10-3.gitd883c7c
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Mon Jul 11 2016 Julien Enselme <jujens@jujens.eu> - 0.1.10-2.gitd883c7c
- Add comments to explain why python-toml and python-pytoml exist, why the
  source is taken from github and why the tests are not run for now.

* Thu Jul 07 2016 Julien Enselme <jujens@jujens.eu> - 0.1.10-1.gitd883c7c
- Inital package
