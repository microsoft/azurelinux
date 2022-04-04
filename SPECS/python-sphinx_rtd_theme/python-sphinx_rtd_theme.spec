%global srcname sphinx_rtd_theme
Summary:        Sphinx theme for readthedocs.org
Name:           python-%{srcname}
Version:        1.0.0
Release:        2%{?dist}
License:        MIT AND OFL
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/rtfd/%{srcname}
Source0:        https://github.com/rtfd/%{srcname}/archive/%{version}/%{srcname}-%{version}.tar.gz#/%{name}-%{version}.tar.gz
# The koji builders do not have network access, and this file is not included
# in any Fedora package, so we retrieve it for offline use.
Source1:        https://docs.readthedocs.io/en/latest/objects.inv#/%{name}-objects.inv
# Remove all traces of html5shiv.  We have no interest in supporting ancient
# versions of Internet Explorer.
Patch0:         %{name}-html5shiv.patch
# Unbundle fonts.  Refer to local fonts instead.
Patch1:         %{name}-unbundle-fonts.patch

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3dist(docutils)
BuildRequires:  python3dist(setuptools)
%if %{with_check}
BuildRequires:  python3-atomicwrites
BuildRequires:  python3-attrs
BuildRequires:  python3-pip
BuildRequires:  python3-six
BuildRequires:  python3dist(pytest)
%endif

%description
This is a prototype mobile-friendly sphinx theme for readthedocs.org.
It's currently in development and includes some rtd variable checks that
can be ignored if you're just trying to use it on your project outside
of that site.

%package -n python3-%{srcname}
%{?python_provide:%python_provide python3-%{srcname}}
Summary:        Sphinx theme for readthedocs.org
Requires:       font(fontawesome)
Requires:       font(lato)
Requires:       font(robotoslab)
Requires:       fontawesome-fonts-web

%description -n python3-%{srcname}
This is a prototype mobile-friendly sphinx theme for readthedocs.org.
It's currently in development and includes some rtd variable checks that
can be ignored if you're just trying to use it on your project outside
of that site.

%prep
%autosetup -p1 -n %{srcname}-%{version}

# Use local objects.inv for intersphinx
sed -e "s|\('https://docs\.readthedocs\.io/en/latest/', \)None|\1'%{SOURCE1}'|" \
    -e "s|\('http://www\.sphinx-doc\.org/en/stable/', \)None|\1'%{_docdir}/python-sphinx-doc/html/objects.inv'|" \
    -i docs/conf.py

# We cannot build the Javascript from source at this time, due to many missing
# dependencies.  Convince the build script to skip building the Javascript and
# go on to the python.
mkdir -p build/lib/%{srcname}/static/js
cp -p sphinx_rtd_theme/static/js/badge_only.js build/lib/%{srcname}/static/js
cp -p sphinx_rtd_theme/static/js/theme.js build/lib/%{srcname}/static/js
sed -i "/'build_py'/d" setup.py

%build
%py3_build

rst2html3 --no-datestamp README.rst README.html

%install
%py3_install

# Unbundle fonts
rm -fr %{buildroot}%{python3_sitelib}/%{srcname}/static/css/fonts

%check
pip3 install pluggy more-itertools Sphinx readthedocs-sphinx-ext
%pytest

%files -n python3-%{srcname}
%license LICENSE OFL-License.txt
%doc README.html
%{python3_sitelib}/%{srcname}*

%changelog
* Mon Apr 04 2022 Bala <balakumaran.kannan@microsoft.com> - 1.0.0-2
- pip install latest Sphinx for test

* Fri Mar 25 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.0-1
- Updating to 1.0.0 using Fedora 36 spec (license: MIT) for guidance.

* Mon Mar 07 2022 Bala <balakumaran.kannan@microsoft.com> - 0.4.3-13
- BR multiple python packages for when check enabled
- Pip install dependent packages during check

* Mon Dec 06 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.4.3-12
- Removed documentation build steps.
- License verified.

* Mon Feb 08 2021 Joe Schmitt <joschmit@microsoft.com> - 0.4.3-11
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Turn on bootstrap mode and explicitly use the python3 version of rst2html

* Tue Feb  4 2020 Jerry James <loganjerry@gmail.com> - 0.4.3-10
- BR readthedocs-sphinx-ext so the tests can be run

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 24 2020 Jerry James <loganjerry@gmail.com> - 0.4.3-8
- Add -doc subpackage

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.4.3-7
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 0.4.3-6
- Rebuilt for Python 3.8

* Thu Aug 15 2019 Miro Hrončok <mhroncok@redhat.com> - 0.4.3-5
- Bootstrap for Python 3.8

* Tue Aug  6 2019 Jerry James <loganjerry@gmail.com> - 0.4.3-4
- Add -script patch to silence deprecation warnings

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Mar 06 2019 Miro Hrončok <mhroncok@redhat.com> - 0.4.3-2
- Subpackage python2-sphinx_rtd_theme has been removed
  See https://fedoraproject.org/wiki/Changes/Sphinx2

* Tue Feb 12 2019 Jerry James <loganjerry@gmail.com> - 0.4.3-1
- New upstream version
- Use the github tarball, which has docs, instead of the pypi tarball
- Add %%check script

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Oct 22 2018 Jerry James <loganjerry@gmail.com> - 0.4.2-1
- New upstream version

* Tue Jul 31 2018 Jerry James <loganjerry@gmail.com> - 0.4.1-1
- New upstream version

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul  2 2018 Jerry James <loganjerry@gmail.com> - 0.4.0-1
- New upstream version

* Thu Jun 14 2018 Miro Hrončok <mhroncok@redhat.com> - 0.3.1-2
- Rebuilt for Python 3.7

* Wed May  2 2018 Jerry James <loganjerry@gmail.com> - 0.3.1-1
- New upstream version

* Sat Apr  7 2018 Jerry James <loganjerry@gmail.com> - 0.3.0-1
- New upstream version

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Mar  6 2017 Jerry James <loganjerry@gmail.com> - 0.2.4-1
- New upstream version

* Sat Mar  4 2017 Jerry James <loganjerry@gmail.com> - 0.2.2-1
- New upstream version

* Fri Mar  3 2017 Jerry James <loganjerry@gmail.com> - 0.2.0-1
- New upstream version
- Unbundle the roboto fonts

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 0.1.9-3
- Rebuild for Python 3.6

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Feb  1 2016 Jerry James <loganjerry@gmail.com> - 0.1.9-1
- Comply with latest python packaging guidelines

* Tue Nov 24 2015 Jerry James <loganjerry@gmail.com> - 0.1.9-1
- New upstream version

* Mon Nov 16 2015 Piotr Popieluch <piotr1212@gmail.com> - 0.1.8-4
- Add Requires: fontawesome-web (rhbz#1282297)

* Tue Oct 13 2015 Robert Kuska <rkuska@redhat.com> - 0.1.8-3
- Rebuilt for Python3.5 rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 13 2015 Jerry James <loganjerry@gmail.com> - 0.1.8-1
- New upstream version
- Unbundle the Lato fonts

* Wed Mar 11 2015 Jerry James <loganjerry@gmail.com> - 0.1.7-1
- New upstream version

* Sat Feb 21 2015 Jerry James <loganjerry@gmail.com> - 0.1.6-2
- Use license macro

* Thu Jul  3 2014 Jerry James <loganjerry@gmail.com> - 0.1.6-1
- Initial RPM
