## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 12;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# When bootstrapping sphinx in Fedora, we don't yet have sphinxcontrib-*
# Without the packages, we have warnings in docs, but it's not a hard dependency
# We don't want to support sphinxcontrib-* in RHEL, hence disabling the dependencies
%bcond sphinxcontrib %{undefined rhel}
# RHEL does not include python3-snowballstemmer (SRPM: snowball)
%bcond snowballstemmer %{undefined rhel}
# Also, we don't have all the tests requirements
%bcond tests 1

# Unset -s on python shebang to allow RPM-installed sphinx to be used
# with user-installed modules (#1903763)
%undefine _py3_shebang_s

# No internet in Koji
%bcond internet 0

# Build without BuildRequires ImageMagick, to skip imgconverter tests
%bcond imagemagick_tests %{undefined rhel}

# During texlive updates, sometimes the latex environment is unstable
%bcond latex_tests 1

Name:       python-sphinx
%global     general_version 8.2.3
#global     prerel ...
%global     upstream_version %{general_version}%{?prerel}
Version:    %{general_version}%{?prerel:~%{prerel}}
Release:    %autorelease
Epoch:      1
Summary:    Python documentation generator

# Unless otherwise noted, the license for code is BSD-2-Clause
# sphinx/themes/haiku/static/haiku.css_t has bits licensed with MIT
License:    BSD-2-Clause AND MIT

URL:        https://www.sphinx-doc.org/
Source:     %{pypi_source sphinx %{upstream_version}}

# Allow extra themes to exist. We pull in python3-sphinx-theme-alabaster
# which causes that test to fail.
Patch:      sphinx-test_theming.patch

# Make the first party extensions optional
# This removes the runtime dependencies on:
#  - sphinxcontrib.applehelp
#  - sphinxcontrib.devhelp
#  - sphinxcontrib.jsmath
#  - sphinxcontrib.htmlhelp
#  - sphinxcontrib.serializinghtml
#  - sphinxcontrib.qthelp
# The majority of Fedora RPM packages does not need any of those.
# By removing the dependencies, we minimize the stuff that's pulled into
# the buildroots of 700+ of packages.
#
# This is a downstream-only change - rejected upstream.
# https://github.com/sphinx-doc/sphinx/pull/11747
Patch:      Make-the-first-party-extensions-optional.patch

# Compatibility with Python 3.14
Patch:      https://github.com/sphinx-doc/sphinx/commit/8962398b761c3d85a.patch
Patch:      https://github.com/sphinx-doc/sphinx/commit/e01e42f5fc738815b.patch
Patch:      https://github.com/sphinx-doc/sphinx/pull/13527.patch

BuildArch:     noarch

BuildRequires: make
BuildRequires: python%{python3_pkgversion}-devel
BuildRequires: pyproject-rpm-macros

%if %{with sphinxcontrib}
# applehelp and jsmath have been orphaned, we cannot use the [docs] extra directly
BuildRequires: python%{python3_pkgversion}-sphinxcontrib-devhelp
BuildRequires: python%{python3_pkgversion}-sphinxcontrib-htmlhelp
BuildRequires: python%{python3_pkgversion}-sphinxcontrib-serializinghtml
BuildRequires: python%{python3_pkgversion}-sphinxcontrib-qthelp
BuildRequires: python%{python3_pkgversion}-sphinxcontrib-websupport
%endif

%if %{with tests}
# tests import _testcapi
BuildRequires: python%{python3_pkgversion}-test

BuildRequires: gcc
BuildRequires: gettext
BuildRequires: graphviz
BuildRequires: texinfo

%if %{with imagemagick_tests}
BuildRequires: ImageMagick
%endif

%if %{with latex_tests}
BuildRequires: texlive-collection-fontsrecommended
BuildRequires: texlive-collection-latex
BuildRequires: texlive-dvipng
BuildRequires: texlive-dvisvgm
BuildRequires: tex(amsmath.sty)
BuildRequires: tex(amsthm.sty)
BuildRequires: tex(anyfontsize.sty)
BuildRequires: tex(article.cls)
BuildRequires: tex(capt-of.sty)
BuildRequires: tex(cmap.sty)
BuildRequires: tex(color.sty)
BuildRequires: tex(ctablestack.sty)
BuildRequires: tex(fancyhdr.sty)
BuildRequires: tex(fancyvrb.sty)
BuildRequires: tex(fncychap.sty)
BuildRequires: tex(framed.sty)
BuildRequires: tex(FreeSerif.otf)
BuildRequires: tex(geometry.sty)
BuildRequires: tex(hyperref.sty)
BuildRequires: tex(kvoptions.sty)
BuildRequires: tex(luatex85.sty)
BuildRequires: tex(needspace.sty)
BuildRequires: tex(parskip.sty)
BuildRequires: tex(polyglossia.sty)
BuildRequires: tex(tabulary.sty)
BuildRequires: tex(titlesec.sty)
BuildRequires: tex(upquote.sty)
BuildRequires: tex(utf8x.def)
BuildRequires: tex(wrapfig.sty)
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
Summary:       Python documentation generator

Recommends:    graphviz
Recommends:    ImageMagick

# Upstream Requires those, but we have a patch to remove the dependency.
# We keep them Recommended to preserve the default user experience.
%if %{with sphinxcontrib}
# applehelp and jsmath have been orphaned
Recommends:    python%{python3_pkgversion}-sphinxcontrib-devhelp
Recommends:    python%{python3_pkgversion}-sphinxcontrib-htmlhelp
Recommends:    python%{python3_pkgversion}-sphinxcontrib-serializinghtml
Recommends:    python%{python3_pkgversion}-sphinxcontrib-qthelp
%endif

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


%package -n python%{python3_pkgversion}-sphinx-latex
Summary:       LaTeX builder dependencies for python%{python3_pkgversion}-sphinx

Requires:      python%{python3_pkgversion}-sphinx = %{epoch}:%{version}-%{release}
Requires:      texlive-collection-fontsrecommended
Requires:      texlive-collection-latex
Requires:      texlive-dvipng
Requires:      texlive-dvisvgm
Requires:      tex(amsmath.sty)
Requires:      tex(amsthm.sty)
Requires:      tex(anyfontsize.sty)
Requires:      tex(article.cls)
Requires:      tex(capt-of.sty)
Requires:      tex(cmap.sty)
Requires:      tex(color.sty)
Requires:      tex(ctablestack.sty)
Requires:      tex(fancyhdr.sty)
Requires:      tex(fancyvrb.sty)
Requires:      tex(fncychap.sty)
Requires:      tex(framed.sty)
Requires:      tex(FreeSerif.otf)
Requires:      tex(geometry.sty)
Requires:      tex(hyperref.sty)
Requires:      tex(kvoptions.sty)
Requires:      tex(luatex85.sty)
Requires:      tex(needspace.sty)
Requires:      tex(parskip.sty)
Requires:      tex(polyglossia.sty)
Requires:      tex(tabulary.sty)
Requires:      tex(titlesec.sty)
Requires:      tex(upquote.sty)
Requires:      tex(utf8x.def)
Requires:      tex(wrapfig.sty)

# No files in this package, automatic provides don't work:
%py_provides   python%{python3_pkgversion}-sphinx-latex

%description  -n python%{python3_pkgversion}-sphinx-latex
Sphinx is a tool that makes it easy to create intelligent and
beautiful documentation for Python projects (or other documents
consisting of multiple reStructuredText sources), written by Georg
Brandl. It was originally created to translate the new Python
documentation, but has now been cleaned up in the hope that it will be
useful to many other projects.

This package pulls in the TeX dependencies needed by Sphinx's LaTeX
builder.


%package doc
Summary:       Documentation for %{name}
License:       BSD-2-Clause
Recommends:    python%{python3_pkgversion}-sphinx = %{epoch}:%{version}-%{release}

%description doc
Sphinx is a tool that makes it easy to create intelligent and
beautiful documentation for Python projects (or other documents
consisting of multiple reStructuredText sources), written by Georg
Brandl. It was originally created to translate the new Python
documentation, but has now been cleaned up in the hope that it will be
useful to many other projects.

This package contains documentation in the HTML format.


%prep
%autosetup -n sphinx-%{upstream_version} -p1

# Drop test-dependency on pytest-xdist
# This allows for parallel testing, but has a lot of dependencies.
# We want to avoid the dependency in RHEL, where it is not available.
%if 0%{?rhel}
sed -i -e '/pytest-xdist/d' pyproject.toml
%endif

# Drop test-dependency on defusedxml,
# use xml from the standard library instead.
# defusedxml is safer but this is only used in tests.
# Upstream uses defusedxml to be "safer for future contributors when they
# create/open branches and pull requests" -- that does not concern us.
# https://github.com/sphinx-doc/sphinx/pull/12168#discussion_r1535383868
# We want to avoid the dependency in RHEL, but no harm in doing so unconditionally.
sed -i '/"defusedxml/d' pyproject.toml
sed -i 's/from defusedxml./from xml.etree./' sphinx/testing/util.py tests/test_theming/test_theming.py

%if %{without snowballstemmer}
# Drop dependency on snowballstemmer for RHEL, implement dummy method instead
sed -i -e '/snowballstemmer/d' pyproject.toml
sed -i -e 's/^import \(snowballstemmer\)/from . import dummystemmer as \1/' sphinx/search/*.py
cat > sphinx/search/dummystemmer.py <<_EOF
class stemmer:
    def __init__(self, *args, **kwargs): pass
    def stemWord(self, word): return word
_EOF
%endif

%if %{without imagemagick_tests}
rm tests/test_extensions/test_ext_imgconverter.py
%endif


%generate_buildrequires
%pyproject_buildrequires -r %{?with_tests:-x test}


%build
%pyproject_wheel

export PYTHONPATH=$PWD
pushd doc
export SPHINXBUILD="%{python3} ../sphinx/cmd/build.py"
make html SPHINXBUILD="$SPHINXBUILD"
make man SPHINXBUILD="$SPHINXBUILD"
rm -rf _build/html/.buildinfo
# Those files are copied to _build/html/_images and loaded to the
# html pages from there - we can safely remove the duplicated and unused files
rm -rf _build/html/_static/themes _build/html/_static/tutorial
rm -f _build/html/_static/more.png _build/html/_static/translation.svg
mv _build/html ..
popd


%install
%pyproject_install

# For backwards compatibility. Remove with care, if at all
for i in sphinx-{apidoc,autogen,build,quickstart}; do
    ln -s %{_bindir}/$i %{buildroot}%{_bindir}/$i-%{python3_version}
    ln -s %{_bindir}/$i %{buildroot}%{_bindir}/$i-3
done

# Clean up non-python files
rm -f %{buildroot}%{python3_sitelib}/sphinx/locale/.DS_Store
rm -rf %{buildroot}%{python3_sitelib}/sphinx/locale/.tx

pushd doc
# Deliver man pages
install -d %{buildroot}%{_mandir}/man1
for f in _build/man/sphinx-*.1;
do
    cp -p $f %{buildroot}%{_mandir}/man1/$(basename $f)
done
popd

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


%if %{with tests}
%check
# Currently, all linkcheck tests and test_latex_images need internet
# test_build_latex_doc needs internet to download pictures,
# but fails also with it enabled, we decided to skip it entirely
# test_autodoc_type_aliases fails with Python 3.12.4, 3.13.0b3
# skip temporarily until resolved:
# https://github.com/sphinx-doc/sphinx/issues/12430
k="not test_autodoc_type_aliases"
%if %{without internet}
k="${k} and not linkcheck and not test_latex_images and not test_build_latex_doc"
%endif

%if %{without snowballstemmer}
# Without snowballstemmer, some tests have to be skipped as well,
# as the results with dummystemmer do not exactly match the testcases
k="${k} and not test_meta_keys_are_handled_for_language_en and not test_stemmer"
k="${k} and not test_term_in_heading_and_section and not test_IndexBuilder"
k="${k} and not test_check_js_search_indexes"
%endif

%pytest -k "${k}"
%endif

%files -n python%{python3_pkgversion}-sphinx -f sphinx.lang
%license LICENSE.rst
%doc README.rst
%{_bindir}/sphinx-*
%{python3_sitelib}/sphinx/
%dir %{python3_sitelib}/sphinxcontrib/
%{python3_sitelib}/sphinx-%{upstream_version}.dist-info/
%dir %{_datadir}/sphinx/
%dir %{_datadir}/sphinx/locale
%dir %{_datadir}/sphinx/locale/*
%{_mandir}/man1/sphinx-*


%files -n python%{python3_pkgversion}-sphinx-latex
# empty, this is a metapackage


%files doc
%license LICENSE.rst
%doc html


%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 1:8.2.3-12
- test: add initial lock files

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1:8.2.3-11
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1:8.2.3-10
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:8.2.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jun 05 2025 Python Maint <python-maint@redhat.com> - 1:8.2.3-8
- Rebuilt for Python 3.14

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 1:8.2.3-7
- Bootstrap for Python 3.14

* Fri May 30 2025 Karolina Surma <ksurma@redhat.com> - 1:8.2.3-6
- Fix tests with Python 3.14.0a7+

* Fri May 09 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 1:8.2.3-5
- Disable snowballstemmer dependency on RHEL

* Thu Apr 10 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 1:8.2.3-4
- Avoid pytest-xdist dependency on RHEL

* Wed Apr 09 2025 Miro Hrončok <miro@hroncok.cz> - 1:8.2.3-3
- Drop test-dependency on defusedxml

* Thu Mar 27 2025 Karolina Surma <ksurma@redhat.com> - 1:8.2.3-2
- Add compatibility with Python 3.14

* Thu Mar 06 2025 Karolina Surma <ksurma@redhat.com> - 1:8.2.3-1
- Update to 8.2.3

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:8.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jan 09 2025 Tomáš Hrnčiar <thrnciar@redhat.com> - 1:8.1.3-1
- Update to 8.1.3
- Fixes: rhbz#2275375

* Fri Sep 20 2024 Karolina Surma <ksurma@redhat.com> - 1:7.3.7-4
- Tests sphinx extensions with the package

* Thu Aug 22 2024 Karolina Surma <ksurma@redhat.com> - 1:7.3.7-3
- Add a smoke test

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:7.3.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 16 2024 Karolina Surma <ksurma@redhat.com> - 1:7.3.7-1
- Update to 7.3.7

* Sun Jun 09 2024 Python Maint <python-maint@redhat.com> - 1:7.2.6-9
- Rebuilt for Python 3.13

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1:7.2.6-8
- Bootstrap for Python 3.13

* Wed Jan 24 2024 Karolina Surma <ksurma@redhat.com> - 1:7.2.6-6
- Suppress traceback when importing the weakened sphinxcontrib* dependencies

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:7.2.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Dec 12 2023 Karolina Surma <ksurma@redhat.com> - 1:7.2.6-4
- Fix the tests run when building with Python 3.11.7, 3.12.1 and later

* Thu Nov 16 2023 Miro Hrončok <mhroncok@redhat.com> - 1:7.2.6-3
- On Fedora, BuildRequire the sphinxcontrib packages to build the documentation

* Wed Nov 08 2023 Miro Hrončok <mhroncok@redhat.com> - 1:7.2.6-2
- Weaken the runtime dependency on:
  - python3-sphinxcontrib-applehelp
  - python3-sphinxcontrib-devhelp
  - python3-sphinxcontrib-jsmath
  - python3-sphinxcontrib-htmlhelp
  - python3-sphinxcontrib-serializinghtml
  - python3-sphinxcontrib-qthelp
- Packages that want to use them during build need to BuildRequire them explicitly

* Thu Oct 26 2023 Karolina Surma <ksurma@redhat.com> - 1:7.2.6-1
- Update to 7.2.6
- Fixes rhbz#2232469

* Thu Sep 21 2023 Karolina Surma <ksurma@redhat.com> - 1:7.1.2-2
- Fix FTBFS with Pygments 2.16+

* Mon Aug 14 2023 Karolina Surma <ksurma@redhat.com> - 1:7.1.2-1
- Update to 7.1.2
- Fixes rhbz#2225274

* Mon Aug 07 2023 Karolina Surma <ksurma@redhat.com> - 1:7.0.1-1
- Update to 7.0.1

* Thu Jul 27 2023 Miro Hrončok <mhroncok@redhat.com> - 1:6.2.1-4
- Don't use filelock to test this package on RHEL

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jul 13 2023 Karolina Surma <ksurma@redhat.com> - 1:6.2.1-2
- Don't use websupport to build documentation on RHEL

* Mon Jun 26 2023 Karolina Surma <ksurma@redhat.com> - 1:6.2.1-1
- Update to 6.2.1
- Fixes rhbz#2188968

* Fri Jun 16 2023 Python Maint <python-maint@redhat.com> - 1:6.1.3-4
- Rebuilt for Python 3.12

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 1:6.1.3-3
- Bootstrap for Python 3.12

* Wed May 31 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 1:6.1.3-2
- Avoid html5lib test dependency in RHEL builds

* Fri Mar 10 2023 Karolina Surma <ksurma@redhat.com> - 1:6.1.3-1
- Update to 6.1.3
- Fixes rhbz#2135122

* Thu Mar 09 2023 Karolina Surma <ksurma@redhat.com> - 1:5.3.0-4
- Fix tests related to missing setuptools and Babel 2.12
- Fixes rhbz#2176685

* Tue Jan 31 2023 Karolina Surma <ksurma@redhat.com> - 1:5.3.0-3
- Fix tests with python-pygments 2.14+

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Nov 08 2022 Karolina Surma <ksurma@redhat.com> - 1:5.3.0-1
- Update to 5.3.0
- Fixes rhbz#2129546

* Mon Aug 15 2022 Karolina Surma <ksurma@redhat.com> - 1:5.1.1-1
- Update to 5.1.1
- Fixes rhbz#2110473
- Remove reST documentation from the -doc package, ship only HTML

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 21 2022 Karolina Surma <ksurma@redhat.com> - 1:5.0.2-1
- Update to 5.0.2

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1:4.5.0-3
- Rebuilt for Python 3.11

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1:4.5.0-2
- Bootstrap for Python 3.11

* Fri Apr 01 2022 Karolina Surma <ksurma@redhat.com> - 1:4.5.0-1
- Update to 4.5.0
- Fixes rhbz#2068924

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

## END: Generated by rpmautospec
