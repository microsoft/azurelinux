# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# TESTING NOTE: The testsuite requires numerous packages, many of which are
# built with dune.  Furthermore, the testsuite assumes it is running in a git
# checkout, and has access to the Internet.  We cannot satisfy any of these
# conditions on a koji builder, so we do not run the test suite.

# One of the dune libraries now depends on lwt.  We do not currently need that
# library in Fedora, so don't build it.
%bcond lwt 0

# docs are not needed in RHEL, and add unwanted build dependencies
%bcond docs %{undefined rhel}

%global giturl  https://github.com/ocaml/dune

Name:           ocaml-dune
Version:        3.20.2
Release: 2%{?dist}
Summary:        Composable build system for OCaml and Reason

# Dune itself is MIT.  Some bundled libraries have a different license:
# BSD-2-Clause:
# - vendor/ocaml-blake3-mini
# ISC:
# - vendor/cmdliner
# - vendor/notty
# - vendor/sha
# - vendor/uutf
# LGPL-2.1-only:
# - vendor/incremental-cycles
# LGPL-2.1-only WITH OCaml-LGPL-linking-exception
# - vendor/ocaml-inotify
# - vendor/opam
# - vendor/opam-file-format
# - vendor/re
# LGPL-2.1-or-later
# - src/dune_pkg/opam_solver.*
# - src/sat/hash_set.*
# - src/sat/sat.*
# MIT:
# - vendor/build_path_prefix_map
# - vendor/lwd
# - vendor/spawn
License:        MIT AND BSD-2-Clause AND ISC AND LGPL-2.1-only AND LGPL-2.1-only WITH OCaml-LGPL-linking-exception AND LGPL-2.1-or-later
URL:            https://dune.build
VCS:            git:%{giturl}.git
Source:         %{giturl}/archive/%{version}/dune-%{version}.tar.gz
# When building without lwt, remove libraries that need it
Patch0:         %{name}-no-lwt.patch
# Temporary workaround for broken debuginfo (rhbz#2168932)
# See https://github.com/ocaml/dune/issues/6929
Patch1:         %{name}-debuginfo.patch

# OCaml packages not built on i686 since OCaml 5 / Fedora 39.
ExcludeArch:    %{ix86}

BuildRequires:  emacs-nw
BuildRequires:  make
BuildRequires:  ocaml >= 4.08
BuildRequires:  ocaml-compiler-libs
%if !0%{?rhel}
BuildRequires:  ocaml-csexp-devel >= 1.5.0
BuildRequires:  ocaml-pp-devel >= 2.0.0
%endif
BuildRequires:  ocaml-rpm-macros

%if %{with docs}
BuildRequires:  %{py3_dist furo}
BuildRequires:  %{py3_dist myst-parser}
BuildRequires:  %{py3_dist sphinx}
BuildRequires:  %{py3_dist sphinx-copybutton}
BuildRequires:  %{py3_dist sphinx-design}
%endif

%if %{with lwt}
BuildRequires:  ocaml-lwt-devel >= 5.6.0
%endif

# Dune has vendored deps to avoid dependency cycles.  Upstream deliberately
# does not support unbundling these dependencies.
# See https://github.com/ocaml/dune/issues/220
Provides:       bundled(ocaml-build-path-prefix-map) = 0.3
Provides:       bundled(ocaml-cmdliner) = 1.2.0
Provides:       bundled(ocaml-incremental-cycles) = 1e2030a5d5183d84561cde142eecca40e03db2a3
Provides:       bundled(ocaml-inotify) = 2.3
Provides:       bundled(ocaml-lwd) = 0.3
Provides:       bundled(ocaml-notty) = 0.2.3
Provides:       bundled(ocaml-blake3-mini) = c6aa40e5f1973c2e6b736660ce2c8dcd3b3f9c9f
Provides:       bundled(ocaml-opam) = 2.2.0
Provides:       bundled(ocaml-opam-file-format) = 2.1.6
Provides:       bundled(ocaml-re) = 1.11.0
Provides:       bundled(ocaml-sha) = 1.15.4
Provides:       bundled(ocaml-spawn) = 0.15.1
Provides:       bundled(ocaml-uutf) = 1.0.3

Provides:       dune = %{version}-%{release}

# This is needed for the dune-related RPM macros
Requires:       ocaml-rpm-macros

# The dune rules module requires Toploop
Requires:       ocaml-compiler-libs%{?_isa}

# This can be removed when F42 reaches EOL
Obsoletes:      ocaml-fiber < 3.7.0
Obsoletes:      ocaml-fiber-devel < 3.7.0
Provides:       ocaml-fiber = %{version}-%{release}
Provides:       ocaml-fiber-devel = %{version}-%{release}

# Install documentation in the main package doc directory
%global _docdir_fmt %{name}

%description
Dune is a build system designed for OCaml/Reason projects only. It focuses
on providing the user with a consistent experience and takes care of most of
the low-level details of OCaml compilation. All you have to do is provide a
description of your project and Dune will do the rest.

The scheme it implements is inspired from the one used inside Jane Street and
adapted to the open source world. It has matured over a long time and is used
daily by hundred of developers, which means that it is highly tested and
productive.

%if %{with docs}
%package        doc
# The content is MIT.  Other licenses are due to files added by sphinx.
# BSD-2-Clause:
# - _static/basic.css
# - _static/doctools.js
# - _static/documentation_options.js
# - _static/file.png
# - _static/language_data.js
# - _static/minus.png
# - _static/plus.png
# - _static/searchtools.js
# - _static/sphinx_highlight.js
# MIT:
# - _static/check-solid.svg
# - _static/clipboard.min.js
# - _static/copy-button.svg
# - _static/copybutton.css
# - _static/copybutton.js
# - _static/copybutton_funcs.js
# - _static/design-style.*.min.css
# - _static/design-tabs.js
# - _static/css
# - _static/js
License:        MIT AND BSD-2-Clause
Summary:        HTML documentation for %{name}
BuildArch:      noarch

%description    doc
HTML documentation for dune, a composable build system for OCaml.
%endif

%package        emacs
Summary:        Emacs support for %{name}
License:        ISC
Requires:       %{name} = %{version}-%{release}
Requires:       emacs-filesystem >= %{?_emacs_version}%{!?_emacs_version:0}

BuildArch:      noarch

%description    emacs
The %{name}-devel package contains Emacs integration with the dune build
system, a mode to edit dune files, and flymake support for dune files.

## Dune libraries

%package        action-plugin
Summary:        API for writing dynamic dune actions
License:        MIT
Requires:       %{name}-glob%{?_isa} = %{version}-%{release}
Requires:       %{name}-rpc%{?_isa} = %{version}-%{release}
Requires:       ocaml-dyn%{?_isa} = %{version}-%{release}
Requires:       ocaml-ordering%{?_isa} = %{version}-%{release}
Requires:       ocaml-stdune%{?_isa} = %{version}-%{release}

%description    action-plugin
This experimental library provides an API for writing dynamic Dune
actions.  Dynamic dune actions do not need to declare their dependencies
upfront; they are instead discovered automatically during the execution
of the action.

%package        action-plugin-devel
Summary:        Development files for %{name}-action-plugin
License:        MIT
Requires:       %{name}-action-plugin%{?_isa} = %{version}-%{release}
Requires:       %{name}-glob-devel%{?_isa} = %{version}-%{release}
Requires:       %{name}-rpc-devel%{?_isa} = %{version}-%{release}
Requires:       ocaml-dyn-devel%{?_isa} = %{version}-%{release}
Requires:       ocaml-ordering-devel%{?_isa} = %{version}-%{release}
Requires:       ocaml-stdune-devel%{?_isa} = %{version}-%{release}
%if !0%{?rhel}
Requires:       ocaml-csexp-devel%{?_isa}
Requires:       ocaml-pp-devel%{?_isa}
%endif

%description    action-plugin-devel
The ocaml-dune-action-plugin-devel package contains libraries and
signature files for developing applications that use
ocaml-dune-action-plugin.

%package        build-info
Summary:        Embed build information in an executable
License:        MIT

%description    build-info
The build-info library allows access to information about how an
executable was built, such as the version of the project at which it was
built or the list of statically linked libraries with their versions.
It supports reporting the version from a version control system during
development to get a precise reference of when the executable was built.

%package        build-info-devel
Summary:        Development files for %{name}-build-info
License:        MIT
Requires:       %{name}-build-info%{?_isa} = %{version}-%{release}

%description    build-info-devel
The ocaml-dune-build-info-devel package contains libraries and signature
files for developing applications that use ocaml-dune-build-info.

%package        configurator
Summary:        Helper library for gathering system configuration
License:        MIT
Requires:       ocaml-stdune%{?_isa} = %{version}-%{release}

%description    configurator
Dune-configurator is a small library that helps write OCaml scripts that
test features available on the system, in order to generate config.h
files for instance.  Among other things, dune-configurator allows one
to:

- test if a C program compiles
- query pkg-config
- import a #define from OCaml header files
- generate a config.h file

%package        configurator-devel
Summary:        Development files for %{name}-configurator
License:        MIT
Requires:       %{name}-configurator%{?_isa} = %{version}-%{release}
Requires:       ocaml-stdune-devel%{?_isa} = %{version}-%{release}
%if !0%{?rhel}
Requires:       ocaml-csexp-devel%{?_isa}
%endif

%description    configurator-devel
The ocaml-dune-configurator-devel package contains libraries and
signature files for developing applications that use
ocaml-dune-configurator.

%package        glob
Summary:        Parser and interpreter for dune language globs
License:        MIT
Requires:       %{name}-private-libs%{?_isa} = %{version}-%{release}
Requires:       ocaml-dyn%{?_isa} = %{version}-%{release}
Requires:       ocaml-ordering%{?_isa} = %{version}-%{release}
Requires:       ocaml-stdune%{?_isa} = %{version}-%{release}

%description    glob
Dune-glob provides a parser and interpreter for globs as understood by
the dune language.

%package        glob-devel
Summary:        Development files for %{name}-glob
License:        MIT
Requires:       %{name}-glob%{?_isa} = %{version}-%{release}
Requires:       %{name}-private-libs-devel%{?_isa} = %{version}-%{release}
Requires:       ocaml-dyn-devel%{?_isa} = %{version}-%{release}
Requires:       ocaml-ordering-devel%{?_isa} = %{version}-%{release}
Requires:       ocaml-stdune-devel%{?_isa} = %{version}-%{release}
%if !0%{?rhel}
Requires:       ocaml-pp-devel%{?_isa}
%endif

%description    glob-devel
The ocaml-dune-glob-devel package contains libraries and signature files
for developing applications that use ocaml-dune-glob.

%package        private-libs
Summary:        Private dune libraries
License:        MIT

%description    private-libs
This package contains code that is shared between various dune-xxx
packages.  However, it is not meant for public consumption and provides
no stability guarantee.

%package        private-libs-devel
Summary:        Development files for %{name}-private-libs
License:        MIT
Requires:       %{name}-private-libs%{?_isa} = %{version}-%{release}

%description    private-libs-devel
The ocaml-dune-private-libs-devel package contains libraries and
signature files for other dune packages.  Do not use.

%package        rpc
Summary:        Communicate with dune using rpc
License:        MIT
Requires:       ocaml-dyn%{?_isa} = %{version}-%{release}
Requires:       ocaml-ordering%{?_isa} = %{version}-%{release}
Requires:       ocaml-stdune%{?_isa} = %{version}-%{release}
Requires:       ocaml-xdg%{?_isa} = %{version}-%{release}

%description    rpc
This package contains a library used to communicate with dune over rpc.

%package        rpc-devel
Summary:        Development files for %{name}-rpc
License:        MIT
Requires:       %{name}-rpc%{?_isa} = %{version}-%{release}
Requires:       ocaml-dyn-devel%{?_isa} = %{version}-%{release}
Requires:       ocaml-ordering-devel%{?_isa} = %{version}-%{release}
Requires:       ocaml-stdune-devel%{?_isa} = %{version}-%{release}
Requires:       ocaml-xdg-devel%{?_isa} = %{version}-%{release}
%if !0%{?rhel}
Requires:       ocaml-csexp-devel%{?_isa}
Requires:       ocaml-pp-devel%{?_isa}
%endif

%description    rpc-devel
The ocaml-dune-rpc-devel package contains libraries and signature files
for developing applications that use ocaml-rpc.

%if %{with lwt}
%package        rpc-lwt
Summary:        Communicate with dune using rpc and Lwt
License:        MIT
Requires:       %{name}-rpc%{?_isa} = %{version}-%{release}

%description    rpc-lwt
This package contains a library used to communicate with dune over rpc
using Lwt.

%package        rpc-lwt-devel
Summary:        Development files for %{name}-rpc-lwt
License:        MIT
Requires:       %{name}-rpc-lwt%{?_isa} = %{version}-%{release}
Requires:       %{name}-rpc-devel%{?_isa} = %{version}-%{release}
%if !0%{?rhel}
Requires:       ocaml-csexp-devel%{?_isa}
%endif
Requires:       ocaml-lwt-devel%{?_isa}

%description    rpc-lwt-devel
The ocaml-dune-rpc-lwt-devel package contains libraries and signature
files for developing applications that use ocaml-rpc-lwt.
%endif

%package        site
Summary:        Embed location information inside executables and libraries
License:        MIT
Requires:       %{name}-private-libs%{?_isa} = %{version}-%{release}

%description    site
This library enables embedding location information inside executables
and libraries.

%package        site-devel
Summary:        Development files for %{name}-site
License:        MIT
Requires:       %{name}-site%{?_isa} = %{version}-%{release}
Requires:       %{name}-private-libs-devel%{?_isa} = %{version}-%{release}

%description    site-devel
The ocaml-dune-site-devel package contains libraries and signature files
for developing applications that use ocaml-dune-site.

%package     -n ocaml-chrome-trace
Summary:        Chrome trace event generation library
License:        MIT

%description -n ocaml-chrome-trace
Library to output trace data to a file in Chrome's trace_event format.
This format is compatible with chrome trace viewer (chrome://tracing).
The trace viewer is part of the catapult project.

%package     -n ocaml-chrome-trace-devel
Summary:        Development files for ocaml-chrome-trace
License:        MIT
Requires:       ocaml-chrome-trace%{?_isa} = %{version}-%{release}

%description -n ocaml-chrome-trace-devel
The ocaml-dyn-devel package contains libraries and signature files for
developing applications that use ocaml-dyn.

%package     -n ocaml-dyn
Summary:        Dynamic types
License:        MIT
Requires:       ocaml-ordering%{?_isa} = %{version}-%{release}

%description -n ocaml-dyn
This library supports dynamic types in OCaml.

%package     -n ocaml-dyn-devel
Summary:        Development files for ocaml-dyn
License:        MIT
Requires:       ocaml-dyn%{?_isa} = %{version}-%{release}
Requires:       ocaml-ordering-devel%{?_isa} = %{version}-%{release}

%description -n ocaml-dyn-devel
The ocaml-dyn-devel package contains libraries and signature files for
developing applications that use ocaml-dyn.

%package     -n ocaml-ocamlc-loc
Summary:        Parse OCaml compiler output into structured form
License:        MIT
Requires:       ocaml-dyn%{?_isa} = %{version}-%{release}

%description -n ocaml-ocamlc-loc
Parse OCaml compiler output into structured form.

%package     -n ocaml-ocamlc-loc-devel
Summary:        Development files for ocaml-ocamlc-loc
License:        MIT
Requires:       ocaml-ocamlc-loc%{?_isa} = %{version}-%{release}
Requires:       ocaml-dyn-devel%{?_isa} = %{version}-%{release}

%description -n ocaml-ocamlc-loc-devel
The ocaml-ordering-devel package contains libraries and signature files
for developing applications that use ocaml-ocamlc-loc.

%package     -n ocaml-ordering
Summary:        Element ordering
License:        MIT

%description -n ocaml-ordering
Element ordering in OCaml.

%package     -n ocaml-ordering-devel
Summary:        Development files for ocaml-ordering
License:        MIT
Requires:       ocaml-ordering%{?_isa} = %{version}-%{release}

%description -n ocaml-ordering-devel
The ocaml-ordering-devel package contains libraries and signature files
for developing applications that use ocaml-ordering.

%package     -n ocaml-stdune
Summary:        Dune's unstable standard library
License:        MIT
Requires:       ocaml-dyn%{?_isa} = %{version}-%{release}
Requires:       ocaml-ordering%{?_isa} = %{version}-%{release}

%description -n ocaml-stdune
This package contains Dune's unstable standard library.

%package     -n ocaml-stdune-devel
Summary:        Development files for ocaml-stdune
License:        MIT
Requires:       ocaml-stdune%{?_isa} = %{version}-%{release}
Requires:       ocaml-dyn-devel%{?_isa} = %{version}-%{release}
Requires:       ocaml-ordering-devel%{?_isa} = %{version}-%{release}
%if !0%{?rhel}
Requires:       ocaml-csexp-devel%{?_isa}
Requires:       ocaml-pp-devel%{?_isa}
%endif

%description -n ocaml-stdune-devel
The ocaml-stdune-devel package contains libraries and signature files
for developing applications that use ocaml-stdune.

%package     -n ocaml-xdg
Summary:        XDG Base Directory Specification
License:        MIT

%description -n ocaml-xdg
This package contains the XDG Base Directory Specification.

%package     -n ocaml-xdg-devel
Summary:        Development files for ocaml-xdg
License:        MIT
Requires:       ocaml-xdg%{?_isa} = %{version}-%{release}

%description -n ocaml-xdg-devel
The ocaml-xdg-devel package contains libraries and signature files for
developing applications that use ocaml-xdg.

%prep
%autosetup -N -n dune-%{version}
%if %{without lwt}
%autopatch 0 -p1
rm -fr otherlibs/dune-rpc-lwt dune-rpc-lwt.opam
%endif
%autopatch -m1 -p1

%build
./configure \
  --prefix %{_prefix} \
  --bindir %{_bindir} \
  --datadir %{_datadir} \
  --docdir %{_prefix}/doc \
  --etcdir %{_sysconfdir} \
  --libdir %{ocamldir} \
  --libexecdir %{ocamldir} \
  --mandir %{_mandir} \
  --sbindir %{_sbindir}

%make_build release
%if %{with docs}
%make_build doc
%endif

# We also want the libraries
%if !0%{?rhel}
# Do not use the bundled csexp and pp when building them
rm -fr vendor/{csexp,pp}
%endif
./dune.exe build %{?_smp_mflags} --verbose --release @install

%install
%make_install

# Install the libraries
./dune.exe install --destdir=%{buildroot}

# We use %%doc below
rm -fr %{buildroot}%{_prefix}/doc

# Byte compile the Emacs files
cd %{buildroot}%{_emacs_sitelispdir}
%_emacs_bytecompile *.el
cd -

# Generate %%files lists
%ocaml_files -s

%files
%license LICENSE.md
%doc CHANGES.md README.md
%{_bindir}/dune
%{_mandir}/man*/dune*

%if %{with docs}
%files doc
%doc doc/_build/*
%endif

%files emacs
%{_emacs_sitelispdir}/dune*

%files action-plugin -f .ofiles-dune-action-plugin

%files action-plugin-devel -f .ofiles-dune-action-plugin-devel

%files build-info -f .ofiles-dune-build-info

%files build-info-devel -f .ofiles-dune-build-info-devel

%files configurator -f .ofiles-dune-configurator
%dir %{ocamldir}/dune/
%{ocamldir}/dune/META

%files configurator-devel -f .ofiles-dune-configurator-devel
%{ocamldir}/dune/dune-package
%{ocamldir}/dune/opam

%files glob -f .ofiles-dune-glob

%files glob-devel -f .ofiles-dune-glob-devel

%files private-libs -f .ofiles-dune-private-libs

%files private-libs-devel -f .ofiles-dune-private-libs-devel

%files rpc -f .ofiles-dune-rpc

%files rpc-devel -f .ofiles-dune-rpc-devel

%if %{with lwt}
%files rpc-lwt -f .ofiles-dune-rpc-lwt

%files rpc-lwt-devel -f .ofiles-dune-rpc-lwt-devel
%endif

%files site -f .ofiles-dune-site

%files site-devel -f .ofiles-dune-site-devel

%files -n ocaml-chrome-trace -f .ofiles-chrome-trace

%files -n ocaml-chrome-trace-devel -f .ofiles-chrome-trace-devel

%files -n ocaml-dyn -f .ofiles-dyn

%files -n ocaml-dyn-devel -f .ofiles-dyn-devel

%files -n ocaml-ocamlc-loc -f .ofiles-ocamlc-loc

%files -n ocaml-ocamlc-loc-devel -f .ofiles-ocamlc-loc-devel

%files -n ocaml-ordering -f .ofiles-ordering

%files -n ocaml-ordering-devel -f .ofiles-ordering-devel

%files -n ocaml-stdune -f .ofiles-stdune

%files -n ocaml-stdune-devel -f .ofiles-stdune-devel

%files -n ocaml-xdg -f .ofiles-xdg

%files -n ocaml-xdg-devel -f .ofiles-xdg-devel

%changelog
* Tue Sep 16 2025 Jerry James <loganjerry@gmail.com> - 3.20.2-1
- Version 3.20.2

* Mon Aug 25 2025 Jerry James <loganjerry@gmail.com> - 3.20.1-1
- Version 3.20.1

* Fri Aug 22 2025 Jerry James <loganjerry@gmail.com> - 3.20.0-1
- Version 3.20.0

* Wed Jul 23 2025 Jerry James <loganjerry@gmail.com> - 3.19.1-2
- Migrate tests from STI to TMT (rhbz#2382985)

* Wed Jun 11 2025 Jerry James <loganjerry@gmail.com> - 3.19.1-1
- Version 3.19.1

* Fri May 23 2025 Jerry James <loganjerry@gmail.com> - 3.19.0-1
- Version 3.19.0

* Fri May 02 2025 Jerry James <loganjerry@gmail.com> - 3.18.2-1
- Version 3.18.2

* Fri Apr 18 2025 Jerry James <loganjerry@gmail.com> - 3.18.1-1
- Version 3.18.1

* Thu Apr  3 2025 Jerry James <loganjerry@gmail.com> - 3.18.0-1
- Version 3.18.0

* Thu Jan 23 2025 Jerry James <loganjerry@gmail.com> - 3.17.2-1
- Version 3.17.2

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.17.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Dec 26 2024 Jerry James <loganjerry@gmail.com> - 3.17.1-1
- Version 3.17.1
- Update License field for changes in vendored dependencies
- Drop upstreamed furo theme patch

* Thu Oct 31 2024 Jerry James <loganjerry@gmail.com> - 3.16.1-1
- Version 3.16.1

* Thu Oct 10 2024 Charalampos Stratakis <cstratak@redhat.com> - 3.16.0-5
- Use the furo theme for docs build

* Tue Oct 08 2024 Richard W.M. Jones <rjones@redhat.com> - 3.16.0-4
- Rebuild for ocaml-lwt 5.8.0

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.16.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 19 2024 Richard W.M. Jones <rjones@redhat.com> - 3.16.0-2
- OCaml 5.2.0 ppc64le fix

* Mon Jun 17 2024 Jerry James <loganjerry@gmail.com> - 3.16.0-1
- Version 3.16.0

* Wed May 29 2024 Richard W.M. Jones <rjones@redhat.com> - 3.15.3-2
- OCaml 5.2.0 for Fedora 41

* Mon May 27 2024 Jerry James <loganjerry@gmail.com> - 3.15.3-1
- Version 3.15.3

* Wed May 15 2024 Richard W.M. Jones <rjones@redhat.com> - 3.15.2-2
- Use bundled ocaml-csexp and ocaml-pp (RHEL only)

* Wed Apr 24 2024 Jerry James <loganjerry@gmail.com> - 3.15.2-1
- Version 3.15.2

* Thu Apr 18 2024 Jerry James <loganjerry@gmail.com> - 3.15.1-1
- Version 3.15.1

* Mon Apr 08 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 3.15.0-2
- Disable docs in RHEL builds

* Fri Apr  5 2024 Jerry James <loganjerry@gmail.com> - 3.15.0-1
- Version 3.15.0

* Thu Mar 14 2024 Jerry James <loganjerry@gmail.com> - 3.14.2-1
- Version 3.14.2

* Wed Feb 14 2024 Jerry James <loganjerry@gmail.com> - 3.14.0-1
- Version 3.14.0

* Tue Feb  6 2024 Jerry James <loganjerry@gmail.com> - 3.13.1-1
- Version 3.13.1

* Fri Feb  2 2024 Jerry James <loganjerry@gmail.com> - 3.13.0-3
- Rebuild for changed ocamlx(Dynlink) hash

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.13.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Jerry James <loganjerry@gmail.com> - 3.13.0-1
- Version 3.13.0

* Tue Jan  9 2024 Jerry James <loganjerry@gmail.com> - 3.12.2-1
- Version 3.12.2

* Mon Dec 18 2023 Richard W.M. Jones <rjones@redhat.com> - 3.12.1-3
- OCaml 5.1.1 + s390x code gen fix for Fedora 40

* Tue Dec 12 2023 Richard W.M. Jones <rjones@redhat.com> - 3.12.1-2
- OCaml 5.1.1 rebuild for Fedora 40

* Thu Nov 30 2023 Jerry James <loganjerry@gmail.com> - 3.12.1-1
- Version 3.12.1

* Mon Oct  9 2023 Jerry James <loganjerry@gmail.com> - 3.11.1-1
- Version 3.11.1

* Thu Oct 05 2023 Richard W.M. Jones <rjones@redhat.com> - 3.11.0-3
- Bump release and rebuild

* Thu Oct 05 2023 Richard W.M. Jones <rjones@redhat.com> - 3.11.0-2
- OCaml 5.1 rebuild for Fedora 40

* Wed Oct  4 2023 Jerry James <loganjerry@gmail.com> - 3.11.0-1
- Version 3.11.0

* Tue Aug  1 2023 Jerry James <loganjerry@gmail.com> - 3.10.0-1
- Version 3.10.0

* Wed Jul 26 2023 Jerry James <loganjerry@gmail.com> - 3.9.2-1
- Version 3.9.2

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Richard W.M. Jones <rjones@redhat.com> - 3.9.1-3
- OCaml 5.0 rebuild for Fedora 39
- ExcludeArch i686

* Mon Jul 10 2023 Jerry James <loganjerry@gmail.com> - 3.9.1-1
- Version 3.9.1

* Fri Jun  9 2023 Jerry James <loganjerry@gmail.com> - 3.8.1-1
- Version 3.8.1
- Add LGPL-2.1-or-later to License tag due to bundled 0install-solver

* Tue Apr  4 2023 Jerry James <loganjerry@gmail.com> - 3.7.1-1
- Version 3.7.1

* Fri Mar 24 2023 Jerry James <loganjerry@gmail.com> - 3.7.0-2
- Rebuild for ocaml-csexp 1.5.2

* Tue Mar 21 2023 Jerry James <loganjerry@gmail.com> - 3.7.0-1
- Version 3.7.0
- The fiber subpackage has been removed
- Add debuginfo patch to produce good debuginfo again

* Tue Jan 24 2023 Richard W.M. Jones <rjones@redhat.com> - 3.6.1-3
- Rebuild OCaml packages for F38

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Nov 25 2022 Jerry James <loganjerry@gmail.com> - 3.6.1-1
- Version 3.6.1

* Thu Nov 17 2022 Jerry James <loganjerry@gmail.com> - 3.6.0-1
- Version 3.6.0
- Convert License tag to SPDX

* Thu Oct 20 2022 Jerry James <loganjerry@gmail.com> - 3.5.0-1
- Version 3.5.0

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 20 2022 Jerry James <loganjerry@gmail.com> - 3.4.0-1
- Version 3.4.0

* Tue Jul  5 2022 Jerry James <loganjerry@gmail.com> - 3.3.1-1
- Version 3.3.1
- Expose the libraries individually
- Explain why we do not run the test suite
- Use new OCaml macros
- Various spec file cleanups

* Sat Jun 18 2022 Richard W.M. Jones <rjones@redhat.com> - 2.9.3-3
- OCaml 4.14.0 rebuild

* Fri Feb 04 2022 Richard W.M. Jones <rjones@redhat.com> - 2.9.3-2
- OCaml 4.13.1 rebuild to remove package notes

* Thu Feb  3 2022 Jerry James <loganjerry@gmail.com> - 2.9.3-1
- Version 2.9.3
- Note the bundling of ocaml-incremental-cycles

* Wed Jan 26 2022 Richard W.M. Jones <rjones@redhat.com> - 2.9.1-5
- Rebuild to pick up new ocaml dependency

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Oct 04 2021 Richard W.M. Jones <rjones@redhat.com> - 2.9.1-3
- OCaml 4.13.1 build

* Wed Sep  8 2021 Jerry James <loganjerry@gmail.com> - 2.9.1-1
- Version 2.9.1

* Tue Jul 27 2021 Richard W.M. Jones <rjones@redhat.com> - 2.9.0-3
- Rebuild for changed ocamlx(Dynlink)

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Jul 17 2021 Jerry James <loganjerry@gmail.com> - 2.9.0-1
- Version 2.9.0

* Tue Mar 30 2021 Richard W.M. Jones <rjones@redhat.com> - 2.8.5-2
- Bump and rebuild for ELN.

* Mon Mar 29 2021 Jerry James <loganjerry@gmail.com> - 2.8.5-1
- Version 2.8.5

* Mon Mar  8 2021 Jerry James <loganjerry@gmail.com> - 2.8.4-1
- Version 2.8.4

* Mon Mar  8 2021 Jerry James <loganjerry@gmail.com> - 2.8.3-1
- Version 2.8.3

* Mon Mar  1 10:09:48 GMT 2021 Richard W.M. Jones <rjones@redhat.com> - 2.8.2-4
- OCaml 4.12.0 build

* Mon Feb  1 2021 Richard W.M. Jones <rjones@redhat.com> - 2.8.2-3
- Bump and rebuild for updated ocaml Dynlink dependency.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan 21 2021 Jerry James <loganjerry@gmail.com> - 2.8.2-1
- Version 2.8.2

* Thu Jan 14 2021 Jerry James <loganjerry@gmail.com> - 2.8.1-1
- Version 2.8.1

* Wed Jan 13 2021 Jerry James <loganjerry@gmail.com> - 2.8.0-1
- Version 2.8.0
- Drop upstreamed patch from pull request 3757

* Fri Sep 18 2020 Jerry James <loganjerry@gmail.com> - 2.7.1-2
- Add ocaml-csexp-devel R to the -devel subpackage

* Mon Sep 14 2020 Jerry James <loganjerry@gmail.com> - 2.7.1-1
- Version 2.7.1
- Csexp is no longer vendored in
- Drop upstreamed patches for issue 3736 and pull request 3739
- Fix configuration with patch from pull request 3757

* Tue Sep 01 2020 Richard W.M. Jones <rjones@redhat.com> - 2.7.0-6
- OCaml 4.11.1 rebuild

* Mon Aug 24 2020 Richard W.M. Jones <rjones@redhat.com> - 2.7.0-5
- Add fix for https://github.com/ocaml/dune/issues/3736

* Fri Aug 21 2020 Richard W.M. Jones <rjones@redhat.com> - 2.7.0-2
- OCaml 4.11.0 rebuild

* Fri Aug 14 2020 Jerry James <loganjerry@gmail.com> - 2.7.0-1
- Version 2.7.0
- Drop upstreamed patch for issue 3671

* Tue Aug  4 2020 Richard W.M. Jones <rjones@redhat.com> - 2.6.2-2
- Pass -g option when compiling ppx extensions.
  https://github.com/ocaml/dune/pull/3671

* Mon Aug  3 2020 Jerry James <loganjerry@gmail.com> - 2.6.2-1
- New version 2.6.2

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul  2 2020 Jerry James <loganjerry@gmail.com> - 2.6.1-1
- New version 2.6.1

* Sat Jun  6 2020 Jerry James <loganjerry@gmail.com> - 2.6.0-1
- New version 2.6.0

* Mon May 04 2020 Richard W.M. Jones <rjones@redhat.com> - 2.5.1-4
- OCaml 4.11.0+dev2-2020-04-22 rebuild

* Tue Apr 21 2020 Richard W.M. Jones <rjones@redhat.com> - 2.5.1-3
- OCaml 4.11.0 pre-release attempt 2
- Rename cond "bootstrap" as "menhir".

* Sun Apr 19 2020 Jerry James <loganjerry@gmail.com> - 2.5.1-1
- New version 2.5.1

* Sat Apr 18 2020 Richard W.M. Jones <rjones@redhat.com> - 2.5.0-5
- Bump release and rebuild.

* Sat Apr 18 2020 Richard W.M. Jones <rjones@redhat.com> - 2.5.0-4
- Bump release and rebuild.

* Fri Apr 17 2020 Richard W.M. Jones <rjones@redhat.com> - 2.5.0-3
- Bump release and rebuild.

* Fri Apr 17 2020 Richard W.M. Jones <rjones@redhat.com> - 2.5.0-2
- OCaml 4.11.0 pre-release

* Fri Apr 10 2020 Jerry James <loganjerry@gmail.com> - 2.5.0-1
- Version 2.5.0

* Thu Apr 02 2020 Richard W.M. Jones <rjones@redhat.com> - 2.4.0-2
- Update all OCaml dependencies for RPM 4.16.

* Fri Mar  6 2020 Jerry James <loganjerry@gmail.com> - 2.4.0-1
- New version 2.4.0
- Add bootstrap conditional for builds without ocaml-menhir

* Wed Feb 26 2020 Richard W.M. Jones <rjones@redhat.com> - 2.3.1-2
- OCaml 4.10.0 final.

* Thu Feb 20 2020 Jerry James <loganjerry@gmail.com> - 2.3.1-1
- New version 2.3.1 (bz 1805578)

* Tue Feb 18 2020 Jerry James <loganjerry@gmail.com> - 2.3.0-1
- New version 2.3.0 (bz 1803374)

* Fri Feb  7 2020 Jerry James <loganjerry@gmail.com> - 2.2.0-1
- New version 2.2.0 (bz 1742638)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jan 19 2020 Richard W.M. Jones <rjones@redhat.com> - 2.1.2-2
- OCaml 4.10.0+beta1 rebuild.

* Fri Jan 10 2020 Ben Rosser <rosser.bjr@gmail.com> - 2.1.2-1
- Update to latest upstream release, 2.1.2.
- Remove doc patches (as they were accepted upstream).

* Sat Jan  4 2020 Jerry James <loganjerry@gmail.com> - 2.1.0-1
- New version 2.1.0 (bz 1742638)
- Invoke the configure script (bz 1740196)
- Add LGPLv2 to License due to incremental-cycles
- Add -emacs subpackage and byte compile the Emacs Lisp files
- Drop upstreamed 15c04b09a8c06871635d5fd98c3a37089bbde6d9.patch
- Add -doc-emphasis and -doc-scheme patches
- Run the unit tests in %%check

* Fri Dec 06 2019 Richard W.M. Jones <rjones@redhat.com> - 1.11.0-4
- OCaml 4.09.0 (final) rebuild.

* Fri Aug 16 2019 Richard W.M. Jones <rjones@redhat.com> - 1.11.0-3
- OCaml 4.08.1 (final) rebuild.

* Fri Aug 09 2019 Richard W.M. Jones <rjones@redhat.com> - 1.11.0-2
- Work around nodynlink issue on armv7.
  https://github.com/ocaml/dune/issues/2527

* Thu Aug 08 2019 Richard W.M. Jones <rjones@redhat.com> - 1.11.0-1
- New version 1.11.0 (also required for camomile 1.0.2).

* Tue Aug 06 2019 Ben Rosser <rosser.bjr@gmail.com> - 1.10.0-5
- Install dune libraries. Add new ocaml-dune subpackage (rhbz#1737414).

* Wed Jul 31 2019 Richard W.M. Jones <rjones@redhat.com> - 1.10.0-4
- OCaml 4.08.1 (rc2) rebuild.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jun 27 2019 Richard W.M. Jones <rjones@redhat.com> - 1.10.0-2
- OCaml 4.08.0 (final) rebuild.

* Sun Jun 16 2019 Andy Li <andy@onthewings.net> - 1.10.0-1
- Updated to latest upstream release (#1715394).

* Thu May 16 2019 Andy Li <andy@onthewings.net> - 1.9.3-1
- Updated to latest upstream release (#1705660).

* Tue Apr 30 2019 Richard W.M. Jones <rjones@redhat.com> - 1.9.1-2
- OCaml 4.08.0 (beta 3) rebuild.

* Thu Apr 11 2019 Andy Li <andy@onthewings.net> - 1.9.1-1
- Updated to latest upstream release (#1698732).

* Wed Apr 10 2019 Andy Li <andy@onthewings.net> - 1.9.0-1
- Updated to latest upstream release (#1698022).

* Wed Mar 13 2019 Andy Li <andy@onthewings.net> - 1.8.2-1
- Updated to latest upstream release (#1686836).
- Add missing dependency on sphinx_rtd_theme.

* Fri Mar 08 2019 Andy Li <andy@onthewings.net> - 1.8.0-1
- Updated to latest upstream release (#1686466).

* Fri Mar 01 2019 Andy Li <andy@onthewings.net> - 1.7.3-1
- Renamed source package from jbuilder to ocaml-dune.
- Updated URLs and license according to upstream changes.
- Updated to latest upstream release (#1600105).
- Removed 1113.patch which has been applied upstream in eariler version.
- Removed rpm check section since the upstream tests depend on opam.

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Aug 07 2018 Ben Rosser <rosser.bjr@gmail.com> - 1.0.1-1
- Updated to latest upstream release.
- Manpages have been renamed to 'dune'. A 'dune' binary is now provided as well.

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.12.beta20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed May 02 2018 Ben Rosser <rosser.bjr@gmail.com> - 1.0-0.11.beta20
- Updated to latest upstream release (#1537836).

* Tue Mar 06 2018 Ben Rosser <rosser.bjr@gmail.com> - 1.0-0.10.beta18
- Updated to latest upstream release (#1537836).

* Mon Feb 12 2018 Ben Rosser <rosser.bjr@gmail.com> - 1.0-0.9.beta17
- Update to upstream re-release of beta 17.

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.8.beta17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 30 2018 Ben Rosser <rosser.bjr@gmail.com> - 1.0-0.7.beta18
- Fix build failure on ppc64 by always using bytecode ocaml compiler to bootstrap.

* Wed Jan 24 2018 Ben Rosser <rosser.bjr@gmail.com> 1.0-0.6.beta17
- Update to latest upstream release, beta17 (#1537836).
- Remove unit tests that require external deps (that themselves require jbuilder).

* Tue Nov 14 2017 Ben Rosser <rosser.bjr@gmail.com> 1.0-0.5.beta16
- Update to latest upstream release, beta16 (#1509749).
- Add pre_tag version suffix to source flie name to avoid confusion.

* Mon Oct 23 2017 Ben Rosser <rosser.bjr@gmail.com> 1.0-0.4.beta14
- Update to latest upstream release, beta14 (#1504414).

* Mon Aug 28 2017 Ben Rosser <rosser.bjr@gmail.com> 1.0-0.3.beta12
- Update to latest upstream release, beta12.
- Fix typo in description.
- Use simpler github source URL.
- Use make_build macros when compiling.

* Tue Aug 15 2017 Ben Rosser <rosser.bjr@gmail.com> 1.0-0.2.beta11
- Update to a git snapshot so opam can be built against.
- Modernize ocaml packaging.

* Tue Aug  1 2017 Ben Rosser <rosser.bjr@gmail.com> 1.0-0.1.beta11
- Initial package.
