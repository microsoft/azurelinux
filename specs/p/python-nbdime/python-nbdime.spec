## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 2;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global giturl  https://github.com/jupyter/nbdime

Name:           python-nbdime
Version:        4.0.4
Release:        %autorelease
Summary:        Diff and merge of Jupyter notebooks

License:        BSD-3-Clause
URL:            https://nbdime.readthedocs.io/
VCS:            git:%{giturl}.git
Source0:        %{giturl}/archive/v%{version}/nbdime-%{version}.tar.gz
# Source1 and Source2 created with ./prepare_vendor.sh
# "nodejs-packaging-bundler nbdime" fails to include '@jupyterlab/buildutils'
Source1:        nbdime-%{version}-vendor.tar.xz
Source2:        nbdime-%{version}-vendor-licenses.txt
Source3:        prepare_vendor.sh
# Unbundle the fontawesome fonts
Patch:          %{name}-unbundle-fontawesome.patch
# Version 3.0.7 of @types/d3-dispatch is incompatible
Patch:          %{name}-d3-dispatch.patch
# Work around a typescript error with an object of type 'string | undefined'
Patch:          %{name}-undefined-string.patch
# Remove unused dependency on python-mock
# https://github.com/jupyter/nbdime/pull/808
Patch:          %{name}-rm-python-mock-usage.diff

# The build uses nx 16.10.0 (https://github.com/nrwl/nx), which has native
# components for x86_64 and aarch64 only.  Check later releases to see if
# the nx version has rolled forward to a version that supports more
# architectures
ExclusiveArch:  %{x86_64} %{arm64} noarch

BuildArch:      noarch
BuildSystem:    pyproject
BuildOption(generate_buildrequires): -x docs,test
BuildOption(install): -l nbdime

BuildRequires:  fdupes
BuildRequires:  fontawesome-fonts-web
BuildRequires:  gcc-c++
BuildRequires:  git-core
BuildRequires:  help2man
BuildRequires:  make
BuildRequires:  nodejs-devel
BuildRequires:  /usr/bin/node
BuildRequires:  /usr/bin/npm
BuildRequires:  python3-docs
BuildRequires:  yarnpkg

%global _desc %{expand:Nbdime provides tools for diffing and merging of Jupyter notebooks.

- nbdiff: compare notebooks in a terminal-friendly way
- nbmerge: three-way merge of notebooks with automatic conflict resolution
- nbdiff-web: shows you a rich rendered diff of notebooks
- nbmerge-web: gives you a web-based three-way merge tool for notebooks
- nbshow: present a single notebook in a terminal-friendly way}

%description
%_desc

%package -n python3-nbdime
# The nbdime project is released under the BSD-3-Clause license.
# Bundled JavaScript has the following licenses.
# Apache-2.0: mathjax-full, mhchemparser
# BSD-2-Clause: domelementtype, domhandler, domutils, entities
# BSD-3-Clause: @jupyter/ydoc, @jupyterlab/*, @lumino/*
# ISC: picocolors
# MIT: @codemirror/*, @fortawesome/*, @lezer/*, @marijn/find-cluster-break,
#   alertify.js, call-bind, call-bind-apply-helpers, call-bound, crelt,
#   css-loader, deepmerge, define-data-property, dom-serializer, dunder-proto,
#   es-define-property, es-errors, es-object-atoms, escape-string-regexp,
#   file-saver, function-bind, get-intrinsic, get-proto, gopd,
#   has-property-descriptors, has-symbols, hasown, htmlparser2, is-plain-object,
#   isarray, json-stable-stringify, lib0, lodash.escape, math-intrinsics,
#   minimist, nanoid, object-keys, parse-srcset, path-browserify, postcss,
#   process, querystringify, requires-port, sanitize-html, set-function-length,
#   style-loader, style-mod, url-parse, w3c-keyname, y-protocols, yjs
# Public Domain: jsonify
License:        %{shrink:
                  Apache-2.0 AND
                  BSD-2-Clause AND
                  BSD-3-Clause AND
                  ISC AND
                  MIT AND
                  LicenseRef-Fedora-Public-Domain
                }
Summary:        %{summary}
# Filesystem package for the standard Jupyter paths
Requires:       python-jupyter-filesystem
# Needed to replace the bundled fonts
Requires:       fontawesome-fonts-web

Provides:       npm(nbdime) = 7.0.4
Provides:       bundled(npm(@codemirror/autocomplete)) = 6.20.0
Provides:       bundled(npm(@codemirror/commands)) = 6.10.2
Provides:       bundled(npm(@codemirror/lang-cpp)) = 6.0.3
Provides:       bundled(npm(@codemirror/lang-css)) = 6.3.1
Provides:       bundled(npm(@codemirror/lang-html)) = 6.4.11
Provides:       bundled(npm(@codemirror/lang-java)) = 6.0.2
Provides:       bundled(npm(@codemirror/lang-javascript)) = 6.2.4
Provides:       bundled(npm(@codemirror/lang-json)) = 6.0.2
Provides:       bundled(npm(@codemirror/lang-markdown)) = 6.5.0
Provides:       bundled(npm(@codemirror/lang-php)) = 6.0.2
Provides:       bundled(npm(@codemirror/lang-python)) = 6.2.1
Provides:       bundled(npm(@codemirror/lang-rust)) = 6.0.2
Provides:       bundled(npm(@codemirror/lang-sql)) = 6.10.0
Provides:       bundled(npm(@codemirror/lang-wast)) = 6.0.2
Provides:       bundled(npm(@codemirror/lang-xml)) = 6.1.0
Provides:       bundled(npm(@codemirror/language)) = 6.12.1
Provides:       bundled(npm(@codemirror/legacy-modes)) = 6.5.2
Provides:       bundled(npm(@codemirror/search)) = 6.6.0
Provides:       bundled(npm(@codemirror/state)) = 6.5.4
Provides:       bundled(npm(@codemirror/view)) = 6.39.13
Provides:       bundled(npm(@jupyter/ydoc)) = 3.4.0
Provides:       bundled(npm(@jupyterlab/apputils)) = 4.6.4
Provides:       bundled(npm(@jupyterlab/cells)) = 4.5.4
Provides:       bundled(npm(@jupyterlab/codeeditor)) = 4.5.4
Provides:       bundled(npm(@jupyterlab/codemirror)) = 4.5.4
Provides:       bundled(npm(@jupyterlab/coreutils)) = 6.5.4
Provides:       bundled(npm(@jupyterlab/docregistry)) = 4.5.4
Provides:       bundled(npm(@jupyterlab/documentsearch)) = 4.5.4
Provides:       bundled(npm(@jupyterlab/filebrowser)) = 4.5.4
Provides:       bundled(npm(@jupyterlab/mathjax-extension)) = 4.5.4
Provides:       bundled(npm(@jupyterlab/nbformat)) = 4.5.4
Provides:       bundled(npm(@jupyterlab/notebook)) = 4.5.4
Provides:       bundled(npm(@jupyterlab/observables)) = 5.5.4
Provides:       bundled(npm(@jupyterlab/outputarea)) = 4.5.4
Provides:       bundled(npm(@jupyterlab/rendermime)) = 4.5.4
Provides:       bundled(npm(@jupyterlab/services)) = 7.5.4
Provides:       bundled(npm(@jupyterlab/statedb)) = 4.5.4
Provides:       bundled(npm(@jupyterlab/statusbar)) = 4.5.4
Provides:       bundled(npm(@jupyterlab/theme-light-extension)) = 4.5.4
Provides:       bundled(npm(@jupyterlab/toc)) = 6.5.4
Provides:       bundled(npm(@jupyterlab/translation)) = 4.5.4
Provides:       bundled(npm(@jupyterlab/ui-components)) = 4.5.4
Provides:       bundled(npm(@lezer/common)) = 1.5.1
Provides:       bundled(npm(@lezer/cpp)) = 1.1.5
Provides:       bundled(npm(@lezer/css)) = 1.3.0
Provides:       bundled(npm(@lezer/generator)) = 1.8.0
Provides:       bundled(npm(@lezer/highlight)) = 1.2.3
Provides:       bundled(npm(@lezer/html)) = 1.3.13
Provides:       bundled(npm(@lezer/java)) = 1.1.3
Provides:       bundled(npm(@lezer/javascript)) = 1.5.4
Provides:       bundled(npm(@lezer/json)) = 1.0.3
Provides:       bundled(npm(@lezer/lr)) = 1.4.8
Provides:       bundled(npm(@lezer/markdown)) = 1.6.3
Provides:       bundled(npm(@lezer/php)) = 1.0.5
Provides:       bundled(npm(@lezer/python)) = 1.1.18
Provides:       bundled(npm(@lezer/rust)) = 1.0.2
Provides:       bundled(npm(@lezer/xml)) = 1.0.6
Provides:       bundled(npm(@lumino/algorithm)) = 2.0.4
Provides:       bundled(npm(@lumino/collections)) = 2.0.4
Provides:       bundled(npm(@lumino/commands)) = 2.3.3
Provides:       bundled(npm(@lumino/coreutils)) = 2.2.2
Provides:       bundled(npm(@lumino/disposable)) = 2.1.5
Provides:       bundled(npm(@lumino/domutils)) = 2.0.4
Provides:       bundled(npm(@lumino/dragdrop)) = 2.1.8
Provides:       bundled(npm(@lumino/keyboard)) = 2.0.4
Provides:       bundled(npm(@lumino/messaging)) = 2.0.4
Provides:       bundled(npm(@lumino/polling)) = 2.1.5
Provides:       bundled(npm(@lumino/properties)) = 2.0.4
Provides:       bundled(npm(@lumino/signaling)) = 2.1.5
Provides:       bundled(npm(@lumino/virtualdom)) = 2.0.4
Provides:       bundled(npm(@lumino/widgets)) = 2.7.5
Provides:       bundled(npm(@marijn/find-cluster-break)) = 1.0.2
Provides:       bundled(npm(alertify.js)) = 1.0.12
Provides:       bundled(npm(call-bind)) = 1.0.8
Provides:       bundled(npm(call-bind-apply-helpers)) = 1.0.2
Provides:       bundled(npm(call-bound)) = 1.0.4
Provides:       bundled(npm(crelt)) = 1.0.6
Provides:       bundled(npm(css-loader)) = 6.11.0
Provides:       bundled(npm(deepmerge)) = 4.3.1
Provides:       bundled(npm(define-data-property)) = 1.1.4
Provides:       bundled(npm(dom-serializer)) = 2.0.0
Provides:       bundled(npm(domelementtype)) = 2.3.0
Provides:       bundled(npm(domhandler)) = 5.0.3
Provides:       bundled(npm(domutils)) = 3.2.2
Provides:       bundled(npm(dunder-proto)) = 1.0.1
Provides:       bundled(npm(entities)) = 6.0.1
Provides:       bundled(npm(es-define-property)) = 1.0.1
Provides:       bundled(npm(es-errors)) = 1.3.0
Provides:       bundled(npm(es-object-atoms)) = 1.1.1
Provides:       bundled(npm(escape-string-regexp)) = 4.0.0
Provides:       bundled(npm(file-saver)) = 2.0.5
Provides:       bundled(npm(function-bind)) = 1.1.2
Provides:       bundled(npm(get-intrinsic)) = 1.3.0
Provides:       bundled(npm(get-proto)) = 1.0.1
Provides:       bundled(npm(gopd)) = 1.2.0
Provides:       bundled(npm(has-property-descriptors)) = 1.0.2
Provides:       bundled(npm(has-symbols)) = 1.1.0
Provides:       bundled(npm(hasown)) = 2.0.2
Provides:       bundled(npm(htmlparser2)) = 8.0.2
Provides:       bundled(npm(is-plain-object)) = 5.0.0
Provides:       bundled(npm(isarray)) = 2.0.5
Provides:       bundled(npm(json-stable-stringify)) = 1.3.0
Provides:       bundled(npm(jsonify)) = 0.0.1
Provides:       bundled(npm(lib0)) = 0.2.117
Provides:       bundled(npm(lodash.escape)) = 4.0.1
Provides:       bundled(npm(math-intrinsics)) = 1.1.0
Provides:       bundled(npm(mathjax-full)) = 3.2.2
Provides:       bundled(npm(mhchemparser)) = 4.2.1
Provides:       bundled(npm(minimist)) = 1.2.8
Provides:       bundled(npm(nanoid)) = 3.3.11
Provides:       bundled(npm(object-keys)) = 1.1.1
Provides:       bundled(npm(parse-srcset)) = 1.0.2
Provides:       bundled(npm(path-browserify)) = 1.0.1
Provides:       bundled(npm(picocolors)) = 1.1.1
Provides:       bundled(npm(postcss)) = 8.5.6
Provides:       bundled(npm(process)) = 0.11.10
Provides:       bundled(npm(querystringify)) = 2.2.0
Provides:       bundled(npm(requires-port)) = 1.0.0
Provides:       bundled(npm(sanitize-html)) = 2.12.1
Provides:       bundled(npm(set-function-length)) = 1.2.2
Provides:       bundled(npm(style-loader)) = 3.3.4
Provides:       bundled(npm(style-mod)) = 4.1.3
Provides:       bundled(npm(url-parse)) = 1.5.10
Provides:       bundled(npm(w3c-keyname)) = 2.2.8
Provides:       bundled(npm(y-protocols)) = 1.0.7
Provides:       bundled(npm(yjs)) = 13.6.29

%description -n python3-nbdime
%_desc

%package        doc
# The content is BSD-3-Clause.  Other licenses are due to Sphinx files.
# _static/basic.css: BSD-2-Clause
# _static/css/badge_only.css: MIT
# _static/css/theme.css: MIT
# _static/doctools.js: BSD-2-Clause
# _static/documentation_options.js: BSD-2-Clause
# _static/file.png: BSD-2-Clause
# _static/js/badge_only.js: MIT
# _static/js/theme.js: MIT
# _static/language_data.js: BSD-2-Clause
# _static/minus.png: BSD-2-Clause
# _static/plus.png: BSD-2-Clause
# _static/pygments.css: BSD-3-Clause
# _static/searchtools.js: BSD-2-Clause
# _static/sphinx_highlight.js: BSD-2-Clause
# genindex.html: BSD-2-Clause
# search.html: BSD-2-Clause
# searchindex.js: BSD-2-Clause
License:        BSD-3-Clause AND BSD-2-Clause AND MIT
Summary:        Documentation for %{name}

%description    doc
Documentation for %{name}.

%prep
%autosetup -n nbdime-%{version} -a1 -p1
cp -p %{SOURCE2} .

# Do not depend on jupyter_server_mathjax; it doesn't work in jupyterlab 4.10+
# https://github.com/jupyter-server/jupyter_server_mathjax/issues/20
sed -i '/jupyter_server_mathjax/d' pyproject.toml

# Do not run code coverage tools
sed -i '/pytest-cov/d' pyproject.toml

%conf
# Remove useless shebangs
sed -i '\,#!/usr/bin/env,d' \
  nbdime/diffing/directorydiff.py \
  nbdime/gitfiles.py \
  nbdime/webapp/nb_server_extension.py \
  nbdime/webapp/webutil.py

# Fix the remaining shebangs
%py3_shebang_fix nbdime

# Use local objects.inv for intersphinx
sed -e "s|\('https://docs\.python\.org/3\.5', \)None|\1'%{_docdir}/python3-docs/html/objects.inv'|" \
    -i docs/source/conf.py

%build -p
export YARN_CACHE_FOLDER="$PWD/.package-cache"
export npm_config_nodedir=%{_includedir}/node
export CFLAGS='%{build_cflags} -I%{_includedir}/node'
export CXXFLAGS='%{build_cxxflags} -I%{_includedir}/node'
yarn install --offline

%build -a
# Build the documentation
PYTHONPATH=$PWD make -C docs html
rm docs/build/html/.buildinfo

%install -a
# Move the configuration files to the standard Jupyter directories
mv %{buildroot}%{_prefix}%{_sysconfdir} %{buildroot}%{_sysconfdir}

# Link identical files
%fdupes %{buildroot}%{python3_sitelib}/nbdime

# Add missing executable bits
chmod a+x \
  %{buildroot}%{python3_sitelib}/nbdime/tests/filters/add_helper.py \
  %{buildroot}%{python3_sitelib}/nbdime/tests/filters/noop.py \
  %{buildroot}%{python3_sitelib}/nbdime/tests/filters/strip_outputs.py \
  %{buildroot}%{python3_sitelib}/nbdime/vcs/git/diffdriver.py \
  %{buildroot}%{python3_sitelib}/nbdime/vcs/git/difftool.py \
  %{buildroot}%{python3_sitelib}/nbdime/vcs/git/mergedriver.py \
  %{buildroot}%{python3_sitelib}/nbdime/vcs/git/mergetool.py \
  %{buildroot}%{python3_sitelib}/nbdime/vcs/hg/diff.py \
  %{buildroot}%{python3_sitelib}/nbdime/vcs/hg/diffweb.py \
  %{buildroot}%{python3_sitelib}/nbdime/vcs/hg/merge.py \
  %{buildroot}%{python3_sitelib}/nbdime/vcs/hg/mergeweb.py \
  %{buildroot}%{python3_sitelib}/nbdime/webapp/nbdifftool.py \
  %{buildroot}%{python3_sitelib}/nbdime/webapp/nbdiffweb.py \
  %{buildroot}%{python3_sitelib}/nbdime/webapp/nbdimeserver.py \
  %{buildroot}%{python3_sitelib}/nbdime/webapp/nbmergetool.py \
  %{buildroot}%{python3_sitelib}/nbdime/webapp/nbmergeweb.py

# Generate man pages
mkdir -p %{buildroot}%{_mandir}/man1
export PYTHONPATH=%{buildroot}%{python3_sitelib}
makehelp() {
  help2man -N -n "$2" --version-string='%{version}' %{buildroot}%{_bindir}/$1 \
           --no-discard-stderr -o %{buildroot}%{_mandir}/man1/$1.1
}
makehelp git-nbdiffdriver 'A git diff driver for notebooks'
makehelp git-nbdifftool 'A git difftool plugin for notebooks'
makehelp git-nbmergedriver 'A git merge driver for notebooks'
makehelp git-nbmergetool 'A git mergetool plugin for notebooks'
makehelp hg-nbdiff 'A mercurial external differ for notebooks'
makehelp hg-nbdiffweb 'A mercurial web-based differ for notebooks'
makehelp hg-nbmerge 'A mercurial CLI merge tool for notebooks'
makehelp hg-nbmergeweb 'A mercurial web-based merge tool for notebooks'
makehelp nbdiff 'Compute the difference between two Jupyter notebooks'
makehelp nbdiff-web 'Compute the difference between two Jupyter notebooks'
makehelp nbdime 'Merge and diff tool for Jupyter notebooks'
makehelp nbmerge 'Merge two Jupyter notebooks'
makehelp nbmerge-web 'Merge two Jupyter notebooks'
makehelp nbshow 'Show a Jupyter notebook in a terminal'

%check
# Prepare for git tests
git config --global user.email "build@fedoraproject.org"
git config --global user.name "Fedora Builder"

# Skip tests that require a network
%pytest -v --ignore=nbdime/tests/test_cli_apps.py --ignore=nbdime/tests/test_web.py

%files -n python3-nbdime -f %{pyproject_files}
%doc CHANGELOG.md README.md
%license nbdime-%{version}-vendor-licenses.txt
%{_bindir}/git-nbdiffdriver
%{_bindir}/git-nbdifftool
%{_bindir}/git-nbmergedriver
%{_bindir}/git-nbmergetool
%{_bindir}/hg-nbdiff
%{_bindir}/hg-nbdiffweb
%{_bindir}/hg-nbmerge
%{_bindir}/hg-nbmergeweb
%{_bindir}/nbdiff
%{_bindir}/nbdiff-web
%{_bindir}/nbdime
%{_bindir}/nbmerge
%{_bindir}/nbmerge-web
%{_bindir}/nbshow
%{_mandir}/man1/git-nbdiffdriver.1*
%{_mandir}/man1/git-nbdifftool.1*
%{_mandir}/man1/git-nbmergedriver.1*
%{_mandir}/man1/git-nbmergetool.1*
%{_mandir}/man1/hg-nbdiff.1*
%{_mandir}/man1/hg-nbdiffweb.1*
%{_mandir}/man1/hg-nbmerge.1*
%{_mandir}/man1/hg-nbmergeweb.1*
%{_mandir}/man1/nbdiff.1*
%{_mandir}/man1/nbdiff-web.1*
%{_mandir}/man1/nbdime.1*
%{_mandir}/man1/nbmerge.1*
%{_mandir}/man1/nbmerge-web.1*
%{_mandir}/man1/nbshow.1*
%{_datadir}/jupyter/labextensions/nbdime-jupyterlab/
%{_datadir}/jupyter/nbextensions/nbdime/
%config(noreplace) %{_sysconfdir}/jupyter/jupyter_notebook_config.d/nbdime.json
%config(noreplace) %{_sysconfdir}/jupyter/jupyter_server_config.d/nbdime.json
%config(noreplace) %{_sysconfdir}/jupyter/nbconfig/notebook.d/nbdime.json
%exclude %{_datadir}/jupyter/labextensions/nbdime-jupyterlab/schemas/nbdime-jupyterlab/package.json.orig
%exclude %{python3_sitelib}/nbdime/labextension/schemas/nbdime-jupyterlab/package.json.orig

%files doc
%doc docs/build/html
%license LICENSE.md

%changelog
## START: Generated by rpmautospec
* Wed Apr 22 2026 azldev <azurelinux@microsoft.com> - 4.0.4-2
- Latest state for python-nbdime

* Wed Feb 11 2026 Jerry James <loganjerry@gmail.com> - 4.0.4-1
- Version 4.0.4

* Wed Feb 11 2026 Michel Lind <salimma@fedoraproject.org> - 4.0.3-3
- Rebuilt without python-mock

* Thu Jan 29 2026 Jerry James <loganjerry@gmail.com> - 4.0.3-2
- Adapt to nodejs changes in Rawhide

* Fri Jan 16 2026 Jerry James <loganjerry@gmail.com> - 4.0.3-1
- Version 4.0.3
- Add patch to avoid incompatible version of @types/d3-dispatch
- Add patch to work around a typescript error

* Mon Nov 03 2025 Jerry James <loganjerry@gmail.com> - 4.0.2-9
- Do not run code coverage tools

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 4.0.2-8
- Rebuilt for Python 3.14.0rc3 bytecode

* Wed Aug 27 2025 Jerry James <loganjerry@gmail.com> - 4.0.2-7
- Add noarch to ExclusiveArch
- Use the pyproject declarative buildsystem

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 4.0.2-6
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jun 06 2025 Python Maint <python-maint@redhat.com> - 4.0.2-4
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Dec 09 2024 Jerry James <loganjerry@gmail.com> - 4.0.2-2
- CVE-2024-55565: update vendored nanoid

* Thu Sep 05 2024 Jerry James <loganjerry@gmail.com> - 4.0.2-1
- Version 4.0.2
- Setting LC_ALL is no longer needed
- Test more verbosely

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jul 17 2024 Jerry James <loganjerry@gmail.com> - 4.0.1-2
- Simplify linking of duplicate files
- Fix the VCS field

* Thu Jun 20 2024 Jerry James <loganjerry@gmail.com> - 4.0.1-1
- Initial RPM
## END: Generated by rpmautospec
