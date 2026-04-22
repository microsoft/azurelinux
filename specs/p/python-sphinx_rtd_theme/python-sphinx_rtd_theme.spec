## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 7;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global srcname sphinx_rtd_theme

# Disables tests and docs
%bcond_with bootstrap

Name:           python-%{srcname}
Version:        3.0.2
Release:        %autorelease
Summary:        Sphinx theme for readthedocs.org

# SPDX
License:        MIT
URL:            https://github.com/readthedocs/%{srcname}/
Source:         %{url}/archive/%{version}/%{srcname}-%{version}.tar.gz
# The koji builders do not have network access, and this file is not included
# in any Fedora package, so we retrieve it for offline use.
Source:         https://docs.readthedocs.io/en/latest/objects.inv

BuildArch:      noarch

BuildRequires:  font(fontawesome)
BuildRequires:  font(lato)
BuildRequires:  font(robotoslab)
BuildRequires:  make
BuildRequires:  python%{python3_pkgversion}-devel
%if %{without bootstrap}
BuildRequires:  %{py3_dist pytest}
BuildRequires:  %{py3_dist sphinx}
BuildRequires:  python-sphinx-doc
%endif

%description
This is a prototype mobile-friendly sphinx theme for readthedocs.org.
It's currently in development and includes some rtd variable checks that
can be ignored if you're just trying to use it on your project outside
of that site.

%package -n python%{python3_pkgversion}-%{srcname}
Summary:        Sphinx theme for readthedocs.org
Requires:       font(fontawesome)
Requires:       font(lato)
Requires:       font(robotoslab)

%description -n python%{python3_pkgversion}-%{srcname}
This is a prototype mobile-friendly sphinx theme for readthedocs.org.
It's currently in development and includes some rtd variable checks that
can be ignored if you're just trying to use it on your project outside
of that site.

%if %{without bootstrap}
%package doc
Summary:        Documentation for the Sphinx theme for readthedocs.org
Requires:       font(fontawesome)
Requires:       font(lato)
Requires:       font(robotoslab)

%description doc
This package contains documentation for the Sphinx theme for
readthedocs.org.
%endif

%prep
%autosetup -p1 -n %{srcname}-%{version}

# Unpin docutils
sed -i "s/docutils <0\.21/docutils <0\.22/" setup.cfg

# Use local objects.inv for intersphinx
sed -e "s|\('https://docs\.readthedocs\.io/en/stable/', \)None|\1'%{SOURCE1}'|" \
    -e "s|\('https://www\.sphinx-doc\.org/en/master/', \)None|\1'%{_docdir}/python-sphinx-doc/html/objects.inv'|" \
    -i docs/conf.py

# We modify the tests to avoid dependency on readthedocs-sphinx-ext.
# According to upstream, the test dependency is only used to test integration with that dependency.
# See https://github.com/readthedocs/readthedocs-sphinx-ext/pull/105#pullrequestreview-928253285
sed -Ei -e "/extensions\.append\('readthedocs_ext\.readthedocs'\)/d" \
        -e "s/'readthedocs[^']*'(, ?)?//g" \
        tests/util.py

# We patch the theme css files to unbundle fonts (they are required from Fedora)
# Using Web Assets shall support the use case when documentation is
# exported via web server
# See: https://docs.fedoraproject.org/en-US/packaging-guidelines/Web_Assets/
pushd sphinx_rtd_theme/static/css

rm -r fonts

# Edit the fonts references in theme.css and badge.css
for FONT in lato-normal=lato/Lato-Regular.ttf \
            lato-bold=lato/Lato-Bold.ttf \
            lato-normal-italic=lato/Lato-Italic.ttf \
            lato-bold-italic=lato/Lato-BoldItalic.ttf \
            Roboto-Slab-Regular=google-roboto-slab-fonts/RobotoSlab-Regular.ttf \
            Roboto-Slab-Bold=google-roboto-slab-fonts/RobotoSlab-Bold.ttf;
do
  L="${FONT%=*}"
  R="${FONT#*=}"
  # Get the font basename from the path
  F="${R#*/}"
  F_BASENAME="${F/.ttf}"
  sed \
    -e "s|src:\(url(fonts/$L\.[^)]*) format([^)]*),\?\)\+|src:local('$F_BASENAME'),url('/.sysassets/fonts/$R') format(\"truetype\")|g" \
    -i theme.css
done

sed -e "s|src:url(fonts/fontawesome-webfont\.[^)]*);||" \
    -e "s|src:\(url(fonts/fontawesome-webfont\.[^)]*) format([^)]*),\?\)\+|src:local(\"FontAwesome\"),url('/.sysassets/fonts/fontawesome/fontawesome-webfont.ttf') format(\"truetype\")|" \
    -i badge_only.css theme.css

popd

# We cannot build the Javascript from source at this time, due to many missing
# dependencies.  Convince the build script to skip building the Javascript and
# go on to the python.
mkdir -p build/lib/%{srcname}/static/js
cp -p sphinx_rtd_theme/static/js/badge_only.js build/lib/%{srcname}/static/js
cp -p sphinx_rtd_theme/static/js/theme.js build/lib/%{srcname}/static/js

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%if %{without bootstrap}
# Build the documentation
make -C docs html
%endif

rst2html --no-datestamp README.rst README.html

%install
%pyproject_install

%if %{without bootstrap}
rm docs/build/html/.buildinfo
%endif

%check
%if %{without bootstrap}
%pytest
%endif

# Test that the forbidden fonts were successfully removed from the css files
grep 'format("woff2\?")' \
  %{buildroot}%{python3_sitelib}/%{srcname}/static/css/badge_only.css \
  %{buildroot}%{python3_sitelib}/%{srcname}/static/css/theme.css \
&& exit 1 || true

%files -n python%{python3_pkgversion}-%{srcname}
%doc README.html
%license LICENSE
%{python3_sitelib}/%{srcname}-%{version}.dist-info/
%dir %{python3_sitelib}/%{srcname}/
%{python3_sitelib}/%{srcname}/__pycache__/
%{python3_sitelib}/%{srcname}/static/
%{python3_sitelib}/%{srcname}/*.html
%{python3_sitelib}/%{srcname}/*.py
%{python3_sitelib}/%{srcname}/theme.conf
%dir %{python3_sitelib}/%{srcname}/locale/
%{python3_sitelib}/%{srcname}/locale/sphinx.pot
%lang(da) %{python3_sitelib}/%{srcname}/locale/da/
%lang(de) %{python3_sitelib}/%{srcname}/locale/de/
%lang(en) %{python3_sitelib}/%{srcname}/locale/en/
%lang(es) %{python3_sitelib}/%{srcname}/locale/es/
%lang(et) %{python3_sitelib}/%{srcname}/locale/et/
%lang(fa_IR) %{python3_sitelib}/%{srcname}/locale/fa_IR/
%lang(fr) %{python3_sitelib}/%{srcname}/locale/fr/
%lang(hr) %{python3_sitelib}/%{srcname}/locale/hr/
%lang(hu) %{python3_sitelib}/%{srcname}/locale/hu/
%lang(it) %{python3_sitelib}/%{srcname}/locale/it/
%lang(lt) %{python3_sitelib}/%{srcname}/locale/lt/
%lang(nl) %{python3_sitelib}/%{srcname}/locale/nl/
%lang(pl) %{python3_sitelib}/%{srcname}/locale/pl/
%lang(pt) %{python3_sitelib}/%{srcname}/locale/pt/
%lang(pt_BR) %{python3_sitelib}/%{srcname}/locale/pt_BR/
%lang(ru) %{python3_sitelib}/%{srcname}/locale/ru/
%lang(sv) %{python3_sitelib}/%{srcname}/locale/sv/
%lang(tr) %{python3_sitelib}/%{srcname}/locale/tr/
%lang(zh_CN) %{python3_sitelib}/%{srcname}/locale/zh_CN/
%lang(zh_TW) %{python3_sitelib}/%{srcname}/locale/zh_TW/

%if %{without bootstrap}
%files doc
%doc docs/build/html
%license LICENSE
%endif

%changelog
## START: Generated by rpmautospec
* Wed Apr 22 2026 azldev <azurelinux@microsoft.com> - 3.0.2-7
- Latest state for python-sphinx_rtd_theme

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 3.0.2-6
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 3.0.2-5
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 3.0.2-3
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Nov 19 2024 Charalampos Stratakis <cstratak@redhat.com> - 3.0.2-1
- Update to 3.0.2
- Fixes: rhbz#2317615

* Tue Oct 01 2024 Karolina Surma <releng@fedoraproject.org> - 2.0.0-7
- Fix compatibility with docutils 0.21.2

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jul 15 2024 Karolina Surma <ksurma@redhat.com> - 2.0.0-5
- Fix compatibility with Sphinx 7.3+

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 2.0.0-4
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 04 2023 Karolina Surma <ksurma@redhat.com> - 2.0.0-1
- Update to 2.0.0
Fixes rhbz#2233302

* Mon Oct 16 2023 Miro Hrončok <mhroncok@redhat.com> - 1.2.2-2
- Do not BuildRequire python3-sphinxcontrib-httpdomain, it was not needed

* Mon Aug 07 2023 Karolina Surma <ksurma@redhat.com> - 1.2.2-1
- Update to 1.2.2
Fixes rhbz#2213220
- Make the package compatible with docutils 0.20+ and Sphinx 7

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 1.2.1-2
- Rebuilt for Python 3.12

* Wed May 24 2023 Karolina Surma <ksurma@redhat.com> - 1.2.1-1
- Update to 1.2.1
Fixes rhbz#2209270

* Tue Feb 21 2023 Karolina Surma <ksurma@redhat.com> - 1.2.0-1
- Update to 1.2.0
Fixes rhbz#2154374

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Nov 09 2022 Karolina Surma <ksurma@redhat.com> - 1.1.1-1
- Update to the new upstream version
- Relax the python-docutils version requirement to <0.20

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 01 2022 Karolina Surma <ksurma@redhat.com> - 1.0.0-7
- Relax the python-docutils version requirement to <0.19
- Improve references to system fonts (needed by Firefox)

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.0.0-6
- Rebuilt for Python 3.11

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.0.0-5
- Bootstrap for Python 3.11

* Wed Apr 13 2022 Miro Hrončok <mhroncok@redhat.com> - 1.0.0-4
- Avoid build dependency on readthedocs-sphinx-ext

* Fri Mar 25 2022 Karolina Surma <ksurma@redhat.com> - 1.0.0-3
- Unbundle fonts properly, improve referencing them in css files

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Sep 14 2021 Jerry James <loganjerry@gmail.com> - 1.0.0-1
- Version 1.0.0
- Drop upstreamed patch for Sphinx 4.1+
- Use the pyproject macros

* Wed Aug 04 2021 Miro Hrončok <mhroncok@redhat.com> - 0.5.2-5
- Fix for Sphinx 4.1+

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.5.2-3
- Rebuilt for Python 3.10

* Wed Jun 02 2021 Python Maint <python-maint@redhat.com> - 0.5.2-2
- Bootstrap for Python 3.10

* Tue Apr  6 2021 Jerry James <loganjerry@gmail.com> - 0.5.2-1
- Version 0.5.2

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan  4 2021 Jerry James <loganjerry@gmail.com> - 0.5.1-1
- Version 0.5.1
- Do not list language files twice

* Thu Dec 10 2020 Jerry James <loganjerry@gmail.com> - 0.5.0-1
- Version 0.5.0
- Drop upstreamed -script patch
- Do not even link to fonts; modify the CSS to point to system fonts
- Remove all traces of html5shiv

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 0.4.3-13
- Rebuilt for Python 3.9

* Fri May 22 2020 Miro Hrončok <mhroncok@redhat.com> - 0.4.3-12
- Bootstrap for Python 3.9

* Wed Mar 18 2020 Jerry James <loganjerry@gmail.com> - 0.4.3-11
- Fix symlinks to the Roboto fonts

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

## END: Generated by rpmautospec
