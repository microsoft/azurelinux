# Unset -s on python shebang to allow RPM-installed sphinx to be used
# with user-installed modules (#1903763)
%undefine py3_shebang_flags

# Disabled until we bring "ImageMagick" to Mariner.
%bcond_with imagemagick_tests

# Disabled until we have the required LaTeX dependencies in Mariner.
%bcond_with latex_tests

Summary:        Python documentation generator
Name:           python-sphinx
Version:        4.4.0
Release:        2%{?dist}
# Unless otherwise noted, the license for code is BSD
# sphinx/util/inspect.py has bits licensed with PSF license v2 (Python)
# sphinx/themes/haiku/static/haiku.css_t has bits licensed with MIT
License:        BSD AND Python AND MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.sphinx-doc.org/
Source0:        https://files.pythonhosted.org/packages/c9/08/c2932e66460cfbc8973928d276dc82ccde2d24b365055eeda9f0afc1951e/Sphinx-%{version}.tar.gz

BuildArch:      noarch

# for fixes
BuildRequires:  dos2unix
BuildRequires:  make
BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3dist(wheel)

%if %{with_check}
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  graphviz
BuildRequires:  python3-atomicwrites
BuildRequires:  python3-attrs
BuildRequires:  python3-docutils
BuildRequires:  python3-pluggy
BuildRequires:  python3-pytest
BuildRequires:  python3-six
BuildRequires:  python3-test
BuildRequires:  texinfo

%if %{with imagemagick_tests}
BuildRequires:  ImageMagick
%endif

%if %{with latex_tests}
BuildRequires:  texlive-collection-fontsrecommended
BuildRequires:  texlive-collection-latex
BuildRequires:  texlive-dvipng
BuildRequires:  texlive-dvisvgm
BuildRequires:  tex(FreeSerif.otf)
BuildRequires:  tex(amsmath.sty)
BuildRequires:  tex(amsthm.sty)
BuildRequires:  tex(anyfontsize.sty)
BuildRequires:  tex(article.cls)
BuildRequires:  tex(capt-of.sty)
BuildRequires:  tex(cmap.sty)
BuildRequires:  tex(color.sty)
BuildRequires:  tex(ctablestack.sty)
BuildRequires:  tex(fancyhdr.sty)
BuildRequires:  tex(fancyvrb.sty)
BuildRequires:  tex(fncychap.sty)
BuildRequires:  tex(framed.sty)
BuildRequires:  tex(geometry.sty)
BuildRequires:  tex(hyperref.sty)
BuildRequires:  tex(kvoptions.sty)
BuildRequires:  tex(luatex85.sty)
BuildRequires:  tex(needspace.sty)
BuildRequires:  tex(parskip.sty)
BuildRequires:  tex(polyglossia.sty)
BuildRequires:  tex(tabulary.sty)
BuildRequires:  tex(titlesec.sty)
BuildRequires:  tex(upquote.sty)
BuildRequires:  tex(utf8x.def)
BuildRequires:  tex(wrapfig.sty)
%endif

%endif

%description
Sphinx is a tool that makes it easy to create intelligent and
beautiful documentation for Python projects (or other documents
consisting of multiple reStructuredText sources), written by Georg
Brandl. It was originally created to translate the new Python
documentation, but has now been cleaned up in the hope that it will be
useful to many other projects.

Sphinx uses reStructuredText as its markup language, and many of its
strengths come from the power and straightforwardness of
reStructuredText and its parsing and translating suite, the Docutils.

Although it is still under constant development, the following
features are already present, work fine and can be seen "in action" in
the Python docs:

    * Output formats: HTML (including Windows HTML Help) and LaTeX,
      for printable PDF versions
    * Extensive cross-references: semantic markup and automatic links
      for functions, classes, glossary terms and similar pieces of
      information
    * Hierarchical structure: easy definition of a document tree, with
      automatic links to siblings, parents and children
    * Automatic indices: general index as well as a module index
    * Code handling: automatic highlighting using the Pygments highlighter
    * Various extensions are available, e.g. for automatic testing of
      snippets and inclusion of appropriately formatted docstrings.

%package -n python%{python3_pkgversion}-sphinx
Summary:        Python documentation generator
License:        BSD AND Python AND MIT

Requires:       python3-babel
Requires:       python3-docutils
Requires:       python3-imagesize
# Required until we update to at least Python 3.10 due to Sphinx calling into "importlib_metadata.entry_points(group=...)".
# Pre-Python 3.10 versions provide the "importlib.metadata.entry_points" function WITHOUT the "group" argument.
# Without "python3-importlib-metadata" Sphinx attempts to use that Python's function and crashes for Python < 3.10.
# This package provides the newer version of "entry_points", which accepts the "group" argument.
Requires:       python3-importlib-metadata
Requires:       python3-jinja2
Requires:       python3-packaging
Requires:       python3-pygments
Requires:       python3-requests
Requires:       python3-six
Requires:       python3-snowballstemmer
Requires:       python3-sphinx-theme-alabaster
Requires:       python3-sphinxcontrib-applehelp
Requires:       python3-sphinxcontrib-devhelp
Requires:       python3-sphinxcontrib-htmlhelp
Requires:       python3-sphinxcontrib-jsmath
Requires:       python3-sphinxcontrib-qthelp
Requires:       python3-sphinxcontrib-serializinghtml

Recommends:     ImageMagick
Recommends:     graphviz

Provides:       bundled(css3-mediaqueries) = 1.0

%description -n python%{python3_pkgversion}-sphinx
Sphinx is a tool that makes it easy to create intelligent and
beautiful documentation for Python projects (or other documents
consisting of multiple reStructuredText sources), written by Georg
Brandl. It was originally created to translate the new Python
documentation, but has now been cleaned up in the hope that it will be
useful to many other projects.

Sphinx uses reStructuredText as its markup language, and many of its
strengths come from the power and straightforwardness of
reStructuredText and its parsing and translating suite, the Docutils.

Although it is still under constant development, the following
features are already present, work fine and can be seen "in action" in
the Python docs:

    * Output formats: HTML (including Windows HTML Help) and LaTeX,
      for printable PDF versions
    * Extensive cross-references: semantic markup and automatic links
      for functions, classes, glossary terms and similar pieces of
      information
    * Hierarchical structure: easy definition of a document tree, with
      automatic links to siblings, parents and children
    * Automatic indices: general index as well as a module index
    * Code handling: automatic highlighting using the Pygments highlighter
    * Various extensions are available, e.g. for automatic testing of
      snippets and inclusion of appropriately formatted docstrings.

%prep
%autosetup -n Sphinx-%{version} -p1

# Remove bundled JS components.
rm ./sphinx/themes/basic/static/{jquery,underscore}*.js
rm ./sphinx/themes/bizstyle/static/css3-mediaqueries*.js

%if %{without imagemagick_tests}
rm tests/test_ext_imgconverter.py
%endif

# Don't measure coverage:
sed -i '/pytest-cov/d' setup.py
# Not needed on recent Pythons, https://github.com/sphinx-doc/sphinx/pull/8483
sed -i '/typed_ast/d' setup.py


%generate_buildrequires
%pyproject_buildrequires -r %{?with_check:-x test}

%build
%pyproject_wheel

%install
%pyproject_install

# For backwards compatibility. Remove with care, if at all
for i in sphinx-{apidoc,autogen,build,quickstart}; do
    ln -s %{_bindir}/$i %{buildroot}%{_bindir}/${i}%{python3_pkgversion}
    ln -s %{_bindir}/$i %{buildroot}%{_bindir}/$i-%{python3_version}
    ln -s %{_bindir}/$i %{buildroot}%{_bindir}/$i-%{python3_pkgversion}
done

# Clean up non-python files
rm -f %{buildroot}%{python3_sitelib}/sphinx/locale/.DS_Store
rm -rf %{buildroot}%{python3_sitelib}/sphinx/locale/.tx

# Move language files to /usr/share;
# patch to support this incorporated in 0.6.6
pushd %{buildroot}%{python3_sitelib}

for lang in `find sphinx/locale -maxdepth 1 -mindepth 1 -type d -not -path '*/\.*' -printf "%f "`;
do
  test $lang == __pycache__ && continue
  install -d %{buildroot}%{_datadir}/sphinx/locale/$lang
  install -d %{buildroot}%{_datadir}/locale/$lang/LC_MESSAGES
  mv sphinx/locale/$lang/LC_MESSAGES/sphinx.js \
     %{buildroot}%{_datadir}/sphinx/locale/$lang/
  mv sphinx/locale/$lang/LC_MESSAGES/sphinx.mo \
    %{buildroot}%{_datadir}/locale/$lang/LC_MESSAGES/
  rm -rf sphinx/locale/$lang
done

popd

# Create the sphinxcontrib directory, so we can own it
# See https://bugzilla.redhat.com/show_bug.cgi?id=1669790 for rationale
mkdir %{buildroot}%{python3_sitelib}/sphinxcontrib

%find_lang sphinx

# Language files; Since these are javascript, it's not immediately obvious to
# find_lang that they need to be marked with a language.
(cd %{buildroot} && find . -name 'sphinx.js') | sed -e 's|^.||' | sed -e \
  's:\(.*/locale/\)\([^/_]\+\)\(.*\.js$\):%lang(\2) \1\2\3:' \
  >> sphinx.lang

%check
pip3 install more-itertools
%pytest

%files -n python%{python3_pkgversion}-sphinx -f sphinx.lang
%license LICENSE
%doc AUTHORS CHANGES EXAMPLES README.rst
%{_bindir}/sphinx-*
%{python3_sitelib}/sphinx/
%dir %{python3_sitelib}/sphinxcontrib/
%{python3_sitelib}/Sphinx-%{version}.dist-info/
%dir %{_datadir}/sphinx/
%dir %{_datadir}/sphinx/locale
%dir %{_datadir}/sphinx/locale/*

%changelog
* Fri Mar 25 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.4.0-2
- Initial CBL-Mariner import from Fedora 36 (license: MIT).
- Removing epoch.
- License verified.
- Removed the "*-sphinx-latex" subpackage and thus support for LaTeX due to missing dependencies.
- Removed bundled JS components.
- Removed docs subpackage due to missing BRs.

* Tue Feb 01 2022 Karolina Surma <ksurma@redhat.com> - 1:4.4.0-1
- Update to 4.4.0
- Fixes rhbz#2033955

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Nov 29 2021 Karolina Surma <ksurma@redhat.com> - 1:4.3.1-1
- Update to 4.3.1
- Fixes rhbz#2027059

* Fri Nov 19 2021 Karolina Surma <ksurma@redhat.com> - 1:4.3.0-1
- Update to 4.3.0
- Fixes rhbz#2022111

* Fri Sep 17 2021 Karolina Surma <ksurma@redhat.com> - 1:4.2.0-1
- Update to 4.2.0
- Fixes rhbz#2003427

* Thu Sep 16 2021 Karolina Surma <ksurma@redhat.com> - 1:4.1.2-3
- Display typing objects correctly with Python 3.10 (fix FTBFS)
- Generate correct reference to parent class if class has `_name` attribute
- Enable previously deselected test

* Wed Aug 18 2021 Karolina Surma <ksurma@redhat.com> - 1:4.1.2-2
- Patch python-sphinx to work with python-pygments >=2.10

* Mon Aug 02 2021 Karolina Surma <ksurma@redhat.com> - 1:4.1.2-1
- Update to 4.1.2
- Fixes rhbz#1979326
- Backport commit to fix python-sphinx with Python 3.10-rc1

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 11 2021 Karolina Surma <ksurma@redhat.com> - 1:4.0.2-1
- Update to 4.0.2
- Fixes rhbz#1948279

* Thu Jun 03 2021 Python Maint <python-maint@redhat.com> - 1:3.5.4-3
- Rebuilt for Python 3.10

* Wed Jun 02 2021 Python Maint <python-maint@redhat.com> - 1:3.5.4-2
- Bootstrap for Python 3.10

* Mon May 10 2021 Karolina Surma <ksurma@redhat.com> - 1:3.5.4-1
- Update to 3.5.4
- Fixes rhbz#1949477

* Thu Apr 01 2021 Karolina Surma <ksurma@redhat.com> - 1:3.5.3-1
- Update to 3.5.3
- Fixes rhbz#1941161

* Wed Mar 10 2021 Charalampos Stratakis <cstratak@redhat.com> - 1:3.5.2-1
- Update 3.5.2
- Fixes rhbz#1928459

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jan 19 2021 Charalampos Stratakis <cstratak@redhat.com> - 1:3.4.3-1
- Update to 3.4.3
- Fixes rhbz#1909494

* Sat Dec 05 2020 Mattia Verga <mattia.verga@protonmail.com> - 1:3.3.1-2
- Unset -s from python shebang
- Fixes: rhbz#1903763

* Mon Nov 23 2020 Miro Hrončok <mhroncok@redhat.com> - 1:3.3.1-1
- Update to 3.3.1
- Fixes: rhbz#1893752

* Wed Oct 14 2020 Tomas Hrnciar <thrnciar@redhat.com> - 1:3.2.1-2
- Backport commit to fix python-sphinx with python-pygments v2.7.1

* Tue Aug 18 2020 Miro Hrončok <mhroncok@redhat.com> - 1:3.2.1-1
- Update to 3.2.1
- Remove compatibility symbolic links from /usr/libexec/
- Fixes rhbz#1867294

* Fri Aug 07 2020 Miro Hrončok <mhroncok@redhat.com> - 1:3.1.2-1
- Update to 3.1.2
- Fixes rhbz#1853901

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 30 2020 Charalampos Stratakis <cstratak@redhat.com> - 1:3.1.1-1
- Update to 3.1.1 (#1783776)

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 1:2.2.2-4
- Rebuilt for Python 3.9

* Fri May 22 2020 Miro Hrončok <mhroncok@redhat.com> - 1:2.2.2-3
- Bootstrap for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Dec 10 2019 Miro Hrončok <mhroncok@redhat.com> - 1:2.2.2-1
- Update to 2.2.2 (rhbz#1743018)

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1:2.1.2-6
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 1:2.1.2-5
- Rebuilt for Python 3.8

* Thu Aug 15 2019 Miro Hrončok <mhroncok@redhat.com> - 1:2.1.2-4
- Bootstrap for Python 3.8

* Thu Aug 15 2019 Richard Shaw <hobbes1069@gmail.com> - 1:2.1.2-3
- Rebuild for Python 3.8.

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 23 2019 Miro Hrončok <mhroncok@redhat.com> - 1:2.1.2-1
- Update to 2.1.2 (#1716158)

* Wed Apr 10 2019 Miro Hrončok <mhroncok@redhat.com> - 1:2.0.1-1
- Update to 2.0.1 (#1697544)
- Own the sphinxcontrib directory (#1669790)

* Wed Mar 27 2019 Charalampos Stratakis <cstratak@redhat.com> - 1:2.0.0~b2-1
- Update to 2.0.0b2

* Wed Feb 27 2019 Miro Hrončok <mhroncok@redhat.com> - 1:2.0.0~b1-1
- Update to 2.0.0b1
- Drop Python 2 package
- https://fedoraproject.org/wiki/Changes/Sphinx2

* Thu Feb 07 2019 Alfredo Moralejo <amoralej@redhat.com> - 1:1.8.4-1
- Update to 1.8.4.

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.7.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Nov 18 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1:1.7.6-2
- Drop explicit locale setting for python3, use C.UTF-8 for python2
  See https://fedoraproject.org/wiki/Changes/Remove_glibc-langpacks-all_from_buildroot

* Mon Jul 23 2018 Marcel Plch <mplch@redhat.com> - 1:1.7.6-1
- Update to 1.7.6

* Fri Jul 13 2018 Miro Hrončok <mhroncok@redhat.com> - 1:1.7.5-6
- Remove unused dependencies on xapian and simplejson

* Thu Jul  5 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1:1.7.5-5
- Add patch to fix build if alabaster theme is installed
- Add patch for #1589868

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 1:1.7.5-4
- Enable tests

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 1:1.7.5-3
- Enable websupport

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 1:1.7.5-2
- Rebuilt for Python 3.7

* Tue Jun 19 2018 Charalampos Stratakis <cstratak@redhat.com> - 1:1.7.5-1
- Update to 1.7.5 (bz#1570451)

* Mon Jun 18 2018 Miro Hrončok <mhroncok@redhat.com> - 1:1.7.2-5
- Rebuilt for Python 3.7

* Fri Jun 15 2018 Miro Hrončok <mhroncok@redhat.com> - 1:1.7.2-4
- Bootstrap for Python 3.7

* Thu Jun 14 2018 Miro Hrončok <mhroncok@redhat.com> - 1:1.7.2-3
- Bootstrap for Python 3.7

* Wed Apr 11 2018 Petr Viktorin <pviktori@redhat.com> - 1:1.7.2-2
- Conditionalize the ImageMagick build dependency & tests

* Wed Apr 11 2018 Petr Viktorin <pviktori@redhat.com> - 1:1.7.2-1
- Update to 1.7.2 (bz#1558968)

* Tue Mar 13 2018 Charalampos Stratakis <cstratak@redhat.com> - 1:1.7.1-1
- Update to 1.7.1 (bz#1534802)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.6.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 09 2018 Charalampos Stratakis <cstratak@redhat.com> - 1:1.6.6-1
- Update to 1.6.6 (bz#1532435)

* Mon Dec 11 2017 Iryna Shcherbina <ishcherb@redhat.com> - 1:1.6.5-2
- Fix ambiguous Python 2 dependency declarations
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Mon Nov 06 2017 Charalampos Stratakis <cstratak@redhat.com> - 1:1.6.5-1
- Update to 1.6.5 (bz#1508237)

* Mon Oct 09 2017 Troy Dawson <tdawson@redhat.com> - 1:1.6.4-2
- Cleanup spec file conditionals

* Tue Sep 26 2017 Charalampos Stratakis <cstratak@redhat.com> - 1:1.6.4-1
- Update to 1.6.4 (bz#1426928)

* Wed Sep 20 2017 Charalampos Stratakis <cstratak@redhat.com> - 1:1.6.3-3
- Provide the epoch tag in order to keep the upgrade path clean.

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 20 2017 Charalampos Stratakis <cstratak@redhat.com> - - 1.6.3-1
- Update to 1.6.3 (bz#1426928)

* Sat Feb 18 2017 Toshio Kuratomi <toshio@fedoraproject.org> - - 1.5.2-2
- Cleanup source files that should not be installed
- Fix the __init__.pyc that was byte compiled for the wrong python

* Fri Feb 17 2017 Toshio Kuratomi <toshio@fedoraproject.org> - - 1.5.2-1
- Update to 1.5.2
- Remove a few latex dependencies that are no longer needed
- Remove xapian patch; now in upstream tarball

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 31 2017 Toshio Kuratomi <toshio@fedoraproject.org> - - 1.5.1-5
- environment-modules is less featureful than Lmod.
  - Select the default version in a different way since environment-modules
    didn't understand the symlink
  - Ignore error messsages in the shell startup script as environment-modules
    prints an error message if a module has already been loaded.  The command
    is doing the right thing for this case except that it's also printing an
    error message.

* Thu Jan 26 2017 Toshio Kuratomi <toshio@fedoraproject.org> - - 1.5.1-4
- Add recipe for setting the system default to the README.fedora

* Wed Jan 18 2017 Toshio Kuratomi <toshio@fedoraproject.org> - - 1.5.1-3
- Move the unversioned executables into the python2 package as they are now
  using python2 to run

* Wed Jan 18 2017 Toshio Kuratomi <toshio@fedoraproject.org> - - 1.5.1-2
- Add README.fedora so people know how to use environment-modules to switch.
- Change the default to be the python2 version to match with the guidelines
- Switch to generic environment(modules) instead of Lmod specifically.

* Fri Dec 30 2016 Orion Poplawski <orion@cora.nwra.com> - 1.5.1-1
- Update to 1.5.1

* Fri Dec 30 2016 Toshio Kuratomi <toshio@fedoraproject.org> - 1.4.9-2
- Remove alternatives.  Alternatives should only be used for a very small
  number of packages (system daemons which also have a compatible command line
  interface).
- Use environment-modules to switch between the python2 and python3 packages
  *but* be aware that no amount of manual switching can get this 100% right.
  The code has to be fixed upstream, not in packaging.

* Tue Dec 13 2016 Charalampos Stratakis <cstratak@redhat.com> - 1.4.9-1
- Update to 1.4.9
- Enable python3 tests

* Mon Dec 12 2016 Charalampos Stratakis <cstratak@redhat.com> - 1.4.8-3
- Rebuild for Python 3.6
- Disable python3 tests for now

* Thu Oct 6 2016 Avram Lubkin <aviso@fedoraproject.org> - 1.4.8-2
- Added tex(luatex85.sty) dependency to support TexLive 2016

* Thu Oct 6 2016 Avram Lubkin <aviso@fedoraproject.org> - 1.4.8-1
- Update to 1.4.8
- Alternatives fails for scripts sometimes (bz#1382405)

* Sun Sep 4 2016 Avram Lubkin <aviso@fedoraproject.org> - 1.4.6-2
- Alternatives fails for man pages due to existing files

* Fri Sep 2 2016 Avram Lubkin <aviso@fedoraproject.org> - 1.4.6-1
- Update to 1.4.6 (bz#1370810)
- Fix unversioned Obsoletes
- Add alternatives slaves for man pages

* Fri Aug 12 2016 Avram Lubkin <aviso@fedoraproject.org> - 1.4.5-1
- Update to 1.4.5 (bz#1356336)
- Remove Recommends for latex, locale, and doc subpackages (bz#1366624)
- Remove Requires from locale subpackage (bz#1366624)
- Set executable scripts via alternatives  (bz#1321413)
- Change graphviz Requires to Recommends (bz#1366706)

* Sun Jul 03 2016 Avram Lubkin <aviso@fedoraproject.org> - 1.4.4-2
- doc and locale no longer specifically require python2-sphinx
- Colapsed python3-sphinx-latex into python-latex

* Sun Jun 12 2016 Avram Lubkin <aviso@fedoraproject.org> - 1.4.4-1
- Updated to 1.4.4
- Added python-sphinx-locale for common locale files

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Nov 27 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.3.1-4
- Obsolete napoleon extension, it is now packaged with sphinx (#1286275)
- Rename python2-Sphinx to python2-sphinx
- Add conflicts to disallow parallel installation of different versions,
  which causes file conflicts because of the shared documentation files.

* Wed Nov 25 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.3.1-3
- Restore using python2 scripts by default (#1285535)

* Wed Nov 25 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.3.1-2
- Fix requirements of python2- subpackage
- Provide sphinx-*-{3.5,3} symlinks for each script

* Tue Nov 24 2015 Julien Enselme <jujens@jujens.eu> - 1.3.1-1
- Update to 1.3.1 (#1136284)
- Update to new guidelines
- Make the default executable use python3

* Tue Oct 13 2015 Robert Kuska <rkuska@redhat.com> - 1.2.3-5
- Rebuilt for Python3.5 rebuild
- add patch to reflect that Python3.5 dropped HTMLParserError

* Mon Jul 20 2015 Michel Alexandre Salim <salimma@fedoraproject.org> - 1.2.3-4
- Fix line encoding of bundled jquery.js

* Mon Jul 20 2015 Michel Alexandre Salim <salimma@fedoraproject.org> - 1.2.3-3
- Re-introduce LaTeX subpackage, solely for pulling in LaTeX dependencies

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Feb  5 2015 Michel Alexandre Salim <salimma@fedoraproject.org> - 1.2.3-1
- Update to 1.2.3
- Mark license file with %%license instead of %%doc

* Thu Feb  5 2015 Michel Alexandre Salim <salimma@fedoraproject.org> - 1.2.2-10
- Complete LaTeX builder deps (fixes bz#882166)
- Make test output verbose
- Add BRs needed to enable all tests

* Tue Feb  3 2015 Michel Alexandre Salim <salimma@fedoraproject.org> - 1.2.2-9
- python3-sphinx package also Provides: python3-sphinx-latex

* Tue Feb  3 2015 Michel Alexandre Salim <salimma@fedoraproject.org> - 1.2.2-8
- If a separate LaTeX subpackage is not generated, the main package should have
  a virtual Provides: for it (bz#1187989)

* Tue Jan 27 2015 Michel Alexandre Salim <salimma@fedoraproject.org> - 1.2.2-7
- Disable separate LaTeX builder for now (bz#1185574)

* Thu Jan 22 2015 Michel Alexandre Salim <salimma@fedoraproject.org> - 1.2.2-6
- Split off LaTeX builder into its own subpackages, to remove TeXLive
  dependencies from the main package.
  Thanks to Robert Kuska <rkuska@redhat.com> for feedback
- Clean up python3-sphinx's locale files, they ended up in the python2 package.
  Share the locale files in /usr/share instead

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 1.2.2-4
- Don't own the -3 scripts by python 2 package

* Thu May 22 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 1.2.2-3
- Add sphinx-*-3 links to scripts
Resolves: #1098109

* Fri May  9 2014 Orion Poplawski <orion@cora.nwra.com> - 1.2.2-2
- Rebuild for Python 3.4

* Fri May  9 2014 Orion Poplawski <orion@cora.nwra.com> - 1.2.2-1
- Update to 1.2.2

* Thu Feb 13 2014 Michel Salim <salimma@fedoraproject.org> - 1.2.1-1
- Update to 1.2.1

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Mar  9 2013 Michel Salim <salimma@fedoraproject.org> - 1.1.3-7
- Fix inheritance_diagram quoting bug, exposed by the newer, stricter dot

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Aug 21 2012 Toshio Kuratomi <toshio@fedoraproject.org> - 1.1.3-5
- Fix for use of sphinx's manpage writer with docutils-0.10

* Mon Aug  6 2012 Michel Salim <salimma@fedoraproject.org> - 1.1.3-4
- Rebuild for Python 3.3

* Fri Aug  3 2012 David Malcolm <dmalcolm@redhat.com> - 1.1.3-3
- remove rhel logic from with_python3 conditional

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr  5 2012 Michel Salim <salimma@fedoraproject.org> - 1.1.3-1
- Update to 1.1.3

* Sun Feb  5 2012 Michel Salim <salimma@fedoraproject.org> - 1.1.2-5
- Move python3 runtime dependencies to the right subpackage
- Properly exclude python3 binaries

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Dec 17 2011 Michel Salim <salimma@fedoraproject.org> - 1.1.2-3
- BR on texlive-latex for LaTeX tests

* Thu Dec  8 2011 Michel Salim <salimma@fedoraproject.org> - 1.1.2-2
- Enable python3 subpackage

* Mon Nov 28 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 1.1.2-1
- Update to upstream 1.1.2

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 18 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 1.0.7-1
- Update to upstream 1.0.7

* Mon Jan 17 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 1.0.6-1
- Update to upstream 1.0.6

* Mon Nov  1 2010 Michel Salim <salimma@fedoraproject.org> - 1.0.4-3
- Fix -doc Makefile to allow regeneration of .rst files

* Mon Nov  1 2010 Michel Salim <salimma@fedoraproject.org> - 1.0.4-2
- Actually include *.js locale files
- Generate manpages

* Fri Sep 17 2010 Michel Salim <salimma@fedoraproject.org> - 1.0.4-1
- Update to 1.0.4
- Remove BuildRoot and %%clean declarations

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1.0-0.1.b2.1
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon May 31 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 1.0-0.2.b2
- Update to 1.0 beta 2
- Fixes problem building html documentation in non-English locales

* Wed May 26 2010 Michel Salim <salimma@fedoraproject.org> - 1.0-0.1.b1
- Update to 1.0 beta 1

* Tue May 25 2010 Michel Salim <salimma@fedoraproject.org> - 0.6.6-1
- Update to 0.6.6

* Fri May 21 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.5-2
- Few minor tweaks to Gareth's spec file update

* Mon May 10 2010 Gareth Armstrong <gareth.armstrong@hp.com> - 0.6.5-1.hp
- Update to 0.6.5
- Initial import of python-sphinx from Fedora Rawhide for use in HP CMS
- Enforce that Sphinx requires Python 2.4 or later via an explicit BR
- Minor tweaks to spec file
- Move language files to %%{_datadir}, idea borrowed from Debian's sphinx
  package
- Deliver man pages for sphinx-build & sphinx-quickstart
- Deliver rst documentation files to reST directory in doc sub-package
- Add %%check section for Python2 and add BR on python-nose

* Wed Jan 13 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.4-1
- Update to 0.6.4
- Fixes a problem using autodoc with pylons projects.

* Fri Sep  4 2009 Michel Salim <salimma@fedoraproject.org> - 0.6.3-1
- Update to 0.6.3

* Mon Aug 17 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 0.6.2-1
- Update to 0.6.2 -- upstream bugfix requested inside bz#512438

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 05 2009 Luke Macken <lmacken@redhat.com> - 0.6.1-2
- Add a patch to use our own setuptools package

* Fri Apr 17 2009 Michel Salim <salimma@fedoraproject.org> - 0.6.1-1
- Update to 0.6.1

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan  2 2009 Michel Salim <salimma@fedoraproject.org> - 0.5.1-1
- Update to 0.5.1

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.5-2
- Rebuild for Python 2.6

* Mon Nov 24 2008 Michel Salim <salimma@fedoraproject.org> - 0.5-1
- Update to 0.5

* Fri Oct 10 2008 Michel Salim <salimma@fedoraproject.org> - 0.4.3-1
- Update to 0.4.3

* Wed Aug 27 2008 Toshio Kuratomi <toshio@fedoraproject.org> - 0.4.2-1.1
- Fix for EL-5 build.

* Mon Aug 25 2008 Michel Salim <salimma@fedoraproject.org> - 0.4.2-1
- Update to 0.4.2

* Mon May 26 2008 Michel Salim <salimma@fedoraproject.org> - 0.3-1
- Update to 0.3

* Fri May  2 2008 Michel Salim <salimma@fedoraproject.org> - 0.1.61950-3
- Split documentation into subpackage
- Exclude C files (not built by default anyway)

* Wed Apr 16 2008 José Matos <jamatos@fc.up.pt> - 0.1.61950-2
- Build html documentation, include it and include the rst
  documentation.

* Thu Mar 27 2008 Michel Salim <michel.sylvan@gmail.com> 0.1.61950-1
- Initial package
