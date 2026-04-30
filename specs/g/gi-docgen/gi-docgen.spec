## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 4;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# The Source Code Pro fonts are not packaged in RHEL/ELN.
%bcond source_code_pro %[ %{undefined rhel} || %{defined epel} ]

Name:           gi-docgen
Version:        2026.1
Release:        %autorelease
Summary:        Documentation tool for GObject-based libraries

# Based on the “Copyright and Licensing terms” in README.md, on the contents of
# .reuse/dep5, and on inspection of SPDX headers or other file contents with
# assistance from licensecheck.
#
# The entire source is (Apache-2.0 OR GPL-3.0-or-later) except the following files that are
# packaged or are used to generate packaged files:
#
# (Apache-2.0 OR GPL-3.0-or-later) AND BSD-2-Clause:
#   - gidocgen/mdext.py
#
# MIT:
#   - gidocgen/templates/basic/fzy.js
#   - gidocgen/templates/basic/solarized-{dark,light}.js
#
# CC0-1.0:
#   - gi-docgen.pc.in (from which gi-docgen.pc is generated)
#   - gidocgen/templates/basic/*.png
#   - docs/CODEOWNERS (-doc subpackage)
#   - examples/*.toml (-doc subpackage)
#
# Note that CC0-1.0 is allowed in Fedora for content only; all of the above
# files may reasonably be called content.
#
# Additionally, CC0-1.0 appears in certain sample configuration snippets within
# the following files, which are otherwise (Apache-2.0 OR GPL-3.0-or-later):
#   - docs/project-configuration.rst
#   - docs/tutorial.rst
# On one hand, these are copied from real projects; on the other hand, they are
# very trivial. It’s not obvious whether they should be considered “real”
# CC0-1.0 content or not.
#
# The identifier LGPL-2.1-or-later also appears in a sample configuration
# template in docs/tutorial.rst, but the configuration in question is filled
# with placeholder values and is not copied from a real project, so it’s
# reasonable to consider LGPL-2.1-or-later a placeholder rather than a real
# license as well.
License:        %{shrink:
                (Apache-2.0 OR GPL-3.0-or-later) AND
                BSD-2-Clause AND
                MIT AND
                CC0-1.0
                }
# Additionally, the following sources are under licenses other than (Apache-2.0
# OR GPL-3.0-or-later), but are not packaged in any of the binary RPMs:
#
# CC0-1.0:
#   - .editorconfig (not installed)
#   - .gitlab-ci.yml (not installed)
#   - gi-docgen.doap (not installed)
#   - MANIFEST.in (not installed)
#   - pytest.ini (not installed; test only)
#   - tests/data/config/*.toml (not installed; test only)
#
# CC-BY-SA-3.0:
#   - docs/gi-docgen.{png,svg} (for HTML docs; not currently packaged)
#   - code-of-conduct.md (not installed)
#
# OFL-1.1:
#   - gidocgen/templates/basic/*.{woff,woff2} (removed in prep)
#
# GPL-2.0-or-later:
#   - tests/data/gir/{Utility-1.0,Regress-1.0}.gir (not installed; test only)
#
# LGPL-2.0-or-later:
#   - tests/data/gir/{GLib,GObject,Gio}-2.0.gir (not installed; test only)
#
# LGPL-2.0-or-later OR MPL-1.1:
#   - tests/data/gir/cairo-1.0.gir (not installed; test only)
SourceLicense:  %{shrink:
                %{license} AND
                CC-BY-SA-3.0 AND
                GPL-2.0-or-later AND
                LGPL-2.0-or-later AND
                (LGPL-2.0-or-later OR MPL-1.1) AND
                OFL-1.1
                }
URL:            https://gitlab.gnome.org/GNOME/gi-docgen
Source:         %{url}/-/archive/%{version}/gi-docgen-%{version}.tar.bz2

# We are prohibited from bundling fonts, and we are prohibited from shipping
# fonts in web font formats; see
# https://docs.fedoraproject.org/en-US/packaging-guidelines/FontsPolicy/#_web_fonts.
#
# Since upstream uses *only* web fonts, we need a patch. We haven’t offered it
# upstream since upstream has no reason NOT to use web fonts.
#
# This patch removes all references to WOFF/WOFF2 font files (which we still
# must remove in %%prep) and ensures the CSS correctly references corresponding
# or stand-in local system fonts.
Patch:          0001-Downstream-only-use-local-packaged-fonts-instead-of-.patch

BuildSystem:            pyproject
BuildOption(install):   gidocgen

BuildArch:      noarch

BuildRequires:  python3dist(pytest)

# Documentation
BuildRequires:  make
BuildRequires:  python3dist(sphinx)
BuildRequires:  python3dist(sphinx-rtd-theme)

# Unbundle fonts.
# Fonts we expect to be in redhat-display-fonts:
BuildRequires:  font(redhatdisplay)
BuildRequires:  font(redhatdisplayitalic)
BuildRequires:  font(redhatdisplayblack)
BuildRequires:  font(redhatdisplaymedium)
BuildRequires:  font(redhatdisplaymediumitalic)
BuildRequires:  font(redhatdisplayblack)
BuildRequires:  font(redhatdisplayblackitalic)
# These auto-Provides are not present, but it is safe enough to believe that
# the corresponding font files will be present in the same package as the other
# BuildRequires:  font(redhatdisplaybold)
# BuildRequires:  font(redhatdisplaybolditalic)
# Fonts we expect to be in redhat-text-fonts:
BuildRequires:  font(redhattext)
BuildRequires:  font(redhattextitalic)
BuildRequires:  font(redhattextmedium)
BuildRequires:  font(redhattextmediumitalic)
# These auto-Provides are not present, but it is safe enough to believe that
# the corresponding font files will be present in the same package as the other
# BuildRequires:  font(redhattextbold)
# BuildRequires:  font(redhattextbolditalic)
%if %{with source_code_pro}
# Fonts we expect to be in adobe-source-code-pro-fonts
BuildRequires:  font(sourcecodepro)
# These auto-Provides are not present, but it is safe enough to believe that
# the corresponding font files will be present in the same package as the other
# BuildRequires:  font(sourcecodeproitalic)
BuildRequires:  font(sourcecodeprosemibold)
%else
# At least depend on a good monospace alternative.
BuildRequires:  redhat-mono-vf-fonts
%endif

# The “dot” tool is required for e.g. rendering class hierarchy diagrams. We
# choose to make it a hard dependency so that package users never have to deal
# with missing features.
BuildRequires:  graphviz
Requires:       graphviz

# Unbundling fonts:
Requires:       gi-docgen-fonts = %{version}-%{release}

# Trivial fork of https://github.com/jhawthorn/fzy.js (looks like it was
# basically just wrapped in an IIFE). Given that modification, it’s not clear
# how we could unbundle it, either downstream or with some kind of upstream
# support.
#
# It’s not clear what version was used for the fork.
Provides:       bundled(js-fzy)

%description
GI-DocGen is a document generator for GObject-based libraries. GObject is the
base type system of the GNOME project. GI-Docgen reuses the introspection data
generated by GObject-based libraries to generate the API reference of these
libraries, as well as other ancillary documentation.

GI-DocGen is not a general purpose documentation tool for C libraries.

While GI-DocGen can be used to generate API references for most GObject/C
libraries that expose introspection data, its main goal is to generate the
reference for GTK and its immediate dependencies. Any and all attempts at
making this tool more generic, or to cover more use cases, will be weighted
heavily against its primary goal.

GI-DocGen is still in development. The recommended use of GI-DocGen is to add
it as a sub-project to your Meson build system, and vendor it when releasing
dist archives.

You should not depend on a system-wide installation until GI-DocGen is declared
stable.


%package fonts
Summary:        Metapackage providing fonts for gi-docgen output
# Really, there is nothing copyrightable in this metapackage, so we give it the
# overall license of the project.
License:        Apache-2.0 OR GPL-3.0-or-later

Requires:       font(redhatdisplay)
Requires:       font(redhatdisplayitalic)
Requires:       font(redhatdisplayblack)
Requires:       font(redhatdisplaymedium)
Requires:       font(redhatdisplaymediumitalic)
Requires:       font(redhatdisplayblack)
Requires:       font(redhatdisplayblackitalic)
Requires:       font(redhattext)
Requires:       font(redhattextitalic)
Requires:       font(redhattextmedium)
Requires:       font(redhattextmediumitalic)
%if %{with source_code_pro}
Requires:       font(sourcecodepro)
Requires:       font(sourcecodeprosemibold)
%else
Requires:       redhat-mono-vf-fonts
%endif

%description fonts
Because web fonts from upstream are not bundled in the gi-docgen package,
documentation packages generated with gi-docgen must depend on this metapackage
to ensure the proper system fonts are present.


%package doc
Summary:        Documentation for gi-docgen
License:        (Apache-2.0 OR GPL-3.0-or-later) AND CC0-1.0

%description doc
Documentation for gi-docgen.


%prep -a
# Remove all bundled fonts.
# See 0001-Downstream-only-use-local-packaged-fonts-instead-of-.patch.
find . -type f \( -name '*.woff' -o -name '*.woff2' \) -print -delete


%build -a
sphinx-build -b html -j%{?_smp_build_ncpus} docs %{_vpath_builddir}/_html
# Do not ship hashes and caches for incremental rebuilds.
rm -rv %{_vpath_builddir}/_html/{.buildinfo,.doctrees}


%install -a
install -t '%{buildroot}%{_pkgdocdir}' -D -m 0644 -p \
    CHANGES.md \
    CONTRIBUTING.md \
    docs/CODEOWNERS \
    README.md
cp -rp '%{_vpath_builddir}/_html' '%{buildroot}%{_pkgdocdir}/html'
cp -rp examples '%{buildroot}%{_pkgdocdir}/'


%check -a
%pytest


%files -f %{pyproject_files}
%license LICENSES/ REUSE.toml

%{_bindir}/gi-docgen
%{_mandir}/man1/gi-docgen.1*
# Normally, this would go in a -devel package, but there is little point in
# providing a -devel package for *just* the .pc file when there are no
# libraries or headers.
%{_datadir}/pkgconfig/gi-docgen.pc


%files fonts
# Empty; this is a metapackage


%files doc
%license LICENSES/ REUSE.toml
%doc %{_pkgdocdir}/


%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 2026.1-4
- test: add initial lock files

* Sat Jan 24 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 2026.1-3
- F43+: Remove F42 conditionals; allow the F42 branch to diverge

* Sat Jan 24 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 2026.1-2
- Improve RHEL/EPEL build conditionals

* Sat Jan 24 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 2026.1-1
- Update to 2026.1 (close RHBZ#2432459)
- Improve font dependencies
- Depend on graphviz to ensure we can render class hierarchies, etc.

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 2025.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Thu Nov 06 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2025.5-2
- Drop conditionals for F41, soon to be EOL

* Sat Oct 11 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2025.5-1
- Update to 2025.5 (close RHBZ#2403282)

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 2025.4-5
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 2025.4-4
- Rebuilt for Python 3.14.0rc2 bytecode

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2025.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 14 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2025.4-2
- Beginning with Fedora 43, build HTML documentation (with unbundled
  assets)

* Mon Jul 14 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2025.4-1
- Update to 2025.4 (close RHBZ#2375892)

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 2025.3-4
- Rebuilt for Python 3.14

* Sat Apr 26 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2025.3-2
- Update .rpmlintrc file for current rpmlint

* Fri Feb 28 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2025.3-1
- Update to 2025.3 (close RHBZ#2349030)

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2024.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Dec 12 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2024.1-7
- Add a SourceLicense field

* Fri Nov 01 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2024.1-4
- F41+: Use the provisional declarative buildsystem

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2024.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 2024.1-2
- Rebuilt for Python 3.13

* Fri May 24 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2024.1-1
- Update to 2024.1 (close RHBZ#2281806)

* Thu May 23 2024 Ray Strode <rstrode@redhat.com> - 2023.3-6
- Drop Source Code Pro dependency on RHEL

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2023.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2023.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 18 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 2023.3-2
- Add patch to fix broken Since/Obsoletes

* Sun Nov 26 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2023.3-1
- Update to 2023.3 (close RHBZ#2251397)

* Sun Nov 26 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2023.1-10
- Package LICENSES/ as a directory

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2023.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jul 07 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2023.1-8
- Use new (rpm 4.17.1+) bcond style

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 2023.1-7
- Rebuilt for Python 3.12

* Fri Mar 17 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2023.1-3
- Don’t assume %%_smp_mflags is -j%%_smp_build_ncpus

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2023.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jan 07 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2023.1-1
- Update to 2023.1 (close RHBZ#2158850)

* Fri Dec 30 2022 Miro Hrončok <miro@hroncok.cz> - 2022.2-3
- Use tomllib (tomli) instated of deprecated python3-toml

* Fri Nov 11 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2022.2-2
- Update License to SPDX

* Fri Nov 11 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2022.2-1
- Update to 2022.2 (close RHBZ#2140725)

* Thu Nov 10 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2022.1-9
- Drop explicit -r for pyproject_buildrequires; no longer needed

* Thu Nov 10 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2022.1-8
- Drop code-of-conduct.md from the -doc subpackage

* Tue Aug 23 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2022.1-7
- Parallelize sphinx-build

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2022.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 2022.1-5
- Rebuilt for Python 3.11

* Wed Apr 20 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2022.1-4
- Drop “forge” macros, which are not doing much here

* Sat Apr 16 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2022.1-3
- Update spec file comment

* Sat Apr 16 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2022.1-2
- Stop numbering patches

* Wed Feb 16 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2022.1-1
- Update to 2022.1 (close RHBZ#2053858)

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2021.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Nov 27 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 2021.8-2
- Reduce LaTeX PDF build verbosity

* Thu Oct 21 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 2021.8-1
- Update to 2021.8 (close RHBZ#2016447)

* Thu Oct 21 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 2021.7-5
- Reduce macro indirection in the spec file

* Wed Sep 29 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 2021.7-4
- Improve comments about test availability

* Mon Sep 27 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 2021.7-3
- Build PDF docs instead of HTML

* Sun Sep 12 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 2021.7-2
- Drop BR on pyproject-rpm-macros, now implied by python3-devel

* Mon Aug 16 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 2021.7-1
- Update to 2021.7

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2021.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 25 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 2021.6-1
- Initial package

## END: Generated by rpmautospec
