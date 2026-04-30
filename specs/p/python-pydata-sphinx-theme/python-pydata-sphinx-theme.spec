## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 11;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Documentation can no longer be built in Fedora due to missing python modules:
# ablog and sphinx-togglebutton
# This also means that doctests cannot be run.
%bcond docs 0

%global giturl  https://github.com/pydata/pydata-sphinx-theme

Name:           python-pydata-sphinx-theme
Version:        0.16.1
Release:        %autorelease
Summary:        Bootstrap-based Sphinx theme from the PyData community

# This project is BSD-3-Clause.
# The bundled bootstrap JavaScript library is MIT.
License:        BSD-3-Clause AND MIT
URL:            https://pydata-sphinx-theme.readthedocs.io/
VCS:            git:%{giturl}.git
Source0:        %{giturl}/archive/v%{version}/pydata-sphinx-theme-%{version}.tar.gz
# Source1 and Source2 created with ./prepare_vendor.sh
Source1:        pydata-sphinx-theme-%{version}-vendor.tar.xz
Source2:        pydata-sphinx-theme-%{version}-vendor-licenses.txt

# Compatibility with Pygments 2.19+
Patch:          https://github.com/pydata/pydata-sphinx-theme/pull/2091.patch

%if %{with docs}
# Generating image files requires network access.  Instead, we scrape these from
# https://pydata-sphinx-theme.readthedocs.io/en/latest/_images.  See
# docs/_static/gallery.yaml for a list of images to download.
Source3:        pydata-gallery.tar.xz
%endif
# Fedora-only patch: unbundle the fontawesome fonts
Patch:          %{name}-fontawesome.patch

BuildArch:      noarch
BuildSystem:    pyproject
BuildOption(install): -L pydata_sphinx_theme
BuildOption(generate_buildrequires): -x test%{?with_docs:,doc}

BuildRequires:  babel
BuildRequires:  fontawesome-fonts-all
BuildRequires:  fontawesome-fonts-web
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  nodejs-devel
BuildRequires:  nodejs-npm
BuildRequires:  yarnpkg

Provides:       bundled(js-bootstrap) = 5.3.8

%if %{without docs}
Obsoletes:      %{name}-doc < 0.13.0-1
%endif

%global _description %{expand:This package contains a Sphinx extension for creating document components
optimized for HTML+CSS.

- The panels directive creates panels of content in a grid layout, utilizing
  both the Bootstrap 5 grid system, and cards layout.

- The link-button directive creates a clickable button, linking to a URL or
  reference, and can also be used to make an entire panel clickable.

- The dropdown directive creates content that can be toggled.

- The tabbed directive creates tabbed content.

- opticon and fa (fontawesome) roles allow for inline icons to be added.

See https://pydata-sphinx-theme.readthedocs.io/ for documentation.}

%description
%_description

%package     -n python3-pydata-sphinx-theme
Summary:        Bootstrap-based Sphinx theme from the PyData community
Requires:       fontawesome-fonts-all
Requires:       fontawesome-fonts-web
Provides:       bundled(js-bootstrap) = 5.3.7

%if %{without docs}
Obsoletes:      %{name}-doc < 0.13.0-1
%endif

%description -n python3-pydata-sphinx-theme
%_description

%if %{with docs}
%package        doc
Summary:        Documentation for pydata-sphinx-theme

%description    doc
Documentation for pydata-sphinx-theme.
%endif

%prep
%autosetup -n pydata-sphinx-theme-%{version} -p1 -a1

%conf
cp -p %{SOURCE2} .

%if %{with docs}
%setup -n pydata-sphinx-theme-%{version} -q -T -D -a 3

# Point to the local switcher instead of the inaccessible one on the web
sed -i 's,https://pydata-sphinx-theme\.readthedocs\.io/en/latest/,,' docs/conf.py
%endif

# Substitute the installed nodejs version for the requested version
%global nodejs_version %(%{_bindir}/node -v | sed s/v//)
sed -i 's,^\(node-version = \)".*",\1"%{nodejs_version}",' pyproject.toml

%generate_buildrequires -p
# The Fedora sphinx package does not provide sphinx[test]
sed -i 's/\(sphinx\)\[test\]/\1/' pyproject.toml
# Do not run code coverage tools
sed -i 's/, "pytest-cov"//' pyproject.toml

%build -p
export YARN_CACHE_FOLDER="$PWD/.package-cache"
yarn install --offline
nodeenv --node=system --prebuilt --clean-src $PWD/.nodeenv

%install -a
%define instdir %{buildroot}%{python3_sitelib}/pydata_sphinx_theme
%define themedir %{instdir}/theme/pydata_sphinx_theme/static
sed -i '/\.gitignore/d' %{pyproject_files}
rm %{themedir}/.gitignore

# More work is required to fully unbundle the fontawesome fonts
sed -i 's,pydata_sphinx_theme/\.\./\.\./\.\./\.\./\.\.,,g' \
    %{themedir}/scripts/fontawesome.js.map \
    %{themedir}/styles/pydata-sphinx-theme.css.map
sed -e 's,url.*fa-solid-900\.woff2.*format("truetype"),local("fontawesome-free-fonts/Font Awesome 6 Free-Solid-900") format("opentype"),g' \
    -e 's,url.*fa-regular-400\.woff2.*format("truetype"),local("fontawesome-free-fonts/Font Awesome 6 Free-Regular-400") format("opentype"),g' \
    -e 's,url.*fa-brands-400\.woff2.*format("truetype"),local("fontawesome-brands-fonts/Font Awesome 6 Brands-Regular-400") format("opentype"),g' \
    -i %{themedir}/styles/pydata-sphinx-theme.css
sed -i '/vendor/d' %{pyproject_files}
rm -fr %{themedir}/vendor

%if %{with docs}
# We need an installed tree before documentation building works properly
cd docs
%{py3_test_envvars} sphinx-build -a . _build
rm _build/.buildinfo
cd -
%endif

%check
%pytest -v

%files -n python3-pydata-sphinx-theme -f %{pyproject_files}
%doc README.md
%license LICENSE

%if %{with docs}
%files doc
%doc docs/_build/*
%license LICENSE
%endif

%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 0.16.1-11
- test: add initial lock files

* Tue Dec 09 2025 Jerry James <loganjerry@gmail.com> - 0.16.1-10
- Adapt to removal of %%{nodejs_version}
- Update the nodejs packages

* Tue Nov 04 2025 Jerry James <loganjerry@gmail.com> - 0.16.1-9
- Do not run code coverage tools

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.16.1-8
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.16.1-7
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jul 19 2025 Jerry James <loganjerry@gmail.com> - 0.16.1-5
- Update bundled bootstrap to version 5.3.7
- Use the pyproject declarative buildsystem

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 0.16.1-4
- Rebuilt for Python 3.14

* Wed Mar 05 2025 Karolina Surma <ksurma@redhat.com> - 0.16.1-3
- Enable compatibility with Pygments 2.19+

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Dec 17 2024 Jerry James <loganjerry@gmail.com> - 0.16.1-1
- Version 0.16.1
- Fix building and testing translations

* Wed Oct 30 2024 Jerry James <loganjerry@gmail.com> - 0.16.0-1
- Version 0.16.0
- Rework method of unbundling fontawesome-fonts
- Run tests verbosely

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jul 17 2024 Jerry James <loganjerry@gmail.com> - 0.15.4-2
- Fix the VCS field

* Tue Jun 25 2024 Jerry James <loganjerry@gmail.com> - 0.15.4-1
- Version 0.15.4

* Wed Jun 12 2024 Jerry James <loganjerry@gmail.com> - 0.15.3-1
- Version 0.15.3

* Sun Jun 09 2024 Python Maint <python-maint@redhat.com> - 0.15.2-5
- Rebuilt for Python 3.13

* Tue Feb 20 2024 Jerry James <loganjerry@gmail.com> - 0.15.2-4
- Fix the SPDX expression

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 18 2024 Jerry James <loganjerry@gmail.com> - 0.15.2-1
- Version 0.15.2

* Tue Jan  9 2024 Jerry James <loganjerry@gmail.com> - 0.15.1-1
- Version 0.15.1

* Mon Nov 27 2023 Jerry James <loganjerry@gmail.com> - 0.14.4-1
- Version 0.14.4

* Mon Oct 30 2023 Jerry James <loganjerry@gmail.com> - 0.14.3-1
- Version 0.14.3

* Wed Oct 25 2023 Jerry James <loganjerry@gmail.com> - 0.14.2-1
- Version 0.14.2

* Wed Sep 20 2023 Jerry James <loganjerry@gmail.com> - 0.14.1-1
- Version 0.14.1

* Fri Sep 15 2023 Jerry James <loganjerry@gmail.com> - 0.14.0-1
- Version 0.14.0

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 29 2023 Python Maint <python-maint@redhat.com> - 0.13.3-2
- Rebuilt for Python 3.12

* Thu Mar 30 2023 Jerry James <loganjerry@gmail.com> - 0.13.3-1
- Version 0.13.3
- Stop building documentation due to missing dependencies
- Dynamically generate python BuildRequires
- The node header tarball is no longer needed

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jan  6 2023 Jerry James <loganjerry@gmail.com> - 0.9.0-2
- Fix unexpanded macros in the doc subpackage
- Convert License tag to SPDX

* Tue Aug  2 2022 Jerry James <loganjerry@gmail.com> - 0.9.0-1
- Version 0.9.0 (fixes rhbz#2105307)

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 21 2022 Python Maint <python-maint@redhat.com> - 0.8.1-3
- Rebuilt for Python 3.11

* Fri May 13 2022 Jerry James <loganjerry@gmail.com> - 0.8.1-2
- Bring back the doc subpackage

* Tue Apr 12 2022 Jerry James <loganjerry@gmail.com> - 0.8.1-1
- Version 0.8.1
- Drop the doc subpackage due to missing dependencies
- Use yarn to install vendored JavaScript

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Nov 11 2021 Jerry James <loganjerry@gmail.com> - 0.7.2-1
- Version 0.7.2

* Sat Oct  2 2021 Jerry James <loganjerry@gmail.com> - 0.7.1-1
- Version 0.7.1
- Drop upstreamed -sphinx4.1 and -docutils patches

* Wed Sep 22 2021 Jerry James <loganjerry@gmail.com> - 0.6.3-2
- Add upstream -docutils patch to fix FTI (bz 2006934)

* Tue Jul 13 2021 Jerry James <loganjerry@gmail.com> - 0.6.3-1
- Initial RPM

## END: Generated by rpmautospec
