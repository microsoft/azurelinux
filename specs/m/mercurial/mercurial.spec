# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# build Rust binary and extensions for non-Enterprise Linux systems
%if ! 0%{?rhel}
%ifarch %{rust_arches}
%bcond_with rust
%else
%bcond_with rust
%endif
%endif

Summary: A fast, lightweight Source Control Management system
Name: mercurial
Version: 7.1.2
Release: 2%{?dist}

# Release: 1.rc1%%{?dist}

#% define upstreamversion %%{version}-rc
%define upstreamversion %{version}

License: GPL-2.0-or-later
URL: https://mercurial-scm.org/
Source0: https://www.mercurial-scm.org/release/%{name}-%{upstreamversion}.tar.gz
Source1: mercurial-site-start.el
# Patch cargo metadata for dependency versions available in Fedora
Patch0:  mercurial-rust-metadata.patch

BuildRequires: make
BuildRequires: emacs-el
BuildRequires: emacs-nox
BuildRequires: gcc
BuildRequires: gettext
BuildRequires: pkgconfig
BuildRequires: python3-build
BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-setuptools_scm
BuildRequires: python3-docutils
%if %{with rust}
BuildRequires: rust-packaging
%endif

Provides: hg = %{version}-%{release}
Requires: emacs-filesystem
Provides: mercurial-rust = %{version}-%{release}
Obsoletes: mercurial-rust < %{version}-%{release}

%description
Mercurial is a fast, lightweight source control management system designed
for efficient handling of very large distributed projects.

Quick start: https://www.mercurial-scm.org/wiki/QuickStart
Tutorial: https://www.mercurial-scm.org/wiki/Tutorial
Extensions: https://www.mercurial-scm.org/wiki/UsingExtensions


%package hgk
Summary:    Hgk interface for mercurial
Requires:   hg = %{version}-%{release}
Requires:   tk8

%description hgk
A Mercurial extension for displaying the change history graphically
using Tcl/Tk.  Displays branches and merges in an easily
understandable way and shows diffs for each revision.  Based on
gitk for the git SCM.

Adds the "hg view" command.  See
https://www.mercurial-scm.org/wiki/HgkExtension for more
documentation.


%package chg
Summary:    A fast Mercurial command without slow Python startup
Requires:   hg = %{version}-%{release}

%description chg
chg is a C wrapper for the hg command. Typically, when you type hg, a new
Python process is created, Mercurial is loaded, and your requested command runs
and the process exits.

With chg, a Mercurial command server background process is created that runs
Mercurial. When you type chg, a C program connects to that background process
and executes Mercurial commands.


%if %{with rust}
%package rust
Summary:    Mercurial Rust binaries and extensions
# Effective license for the rust binaries, computed from statically linked dependencies:
# BSD
# GPLv2+
# MIT
# MIT or ASL 2.0
# MPLv2.0
# Python
# Unlicense or MIT
# zlib or ASL 2.0 or MIT
License:    GPL-2.0-or-later
Requires:   hg = %{version}-%{release}

%description rust
This subpackage provides following Mercurial components implemented in Rust:

The `rustext` extension speeds up some functionality of Mercurial, e.g.
ancestry computations in revision graphs, status or discovery of differences
between repositories.

The experimental `rhg` executable implements a subset of the functionality of
`hg` using only Rust, to avoid the startup cost of a Python interpreter. This
subset is initially small but grows over time as `rhg` is improved. When
fallback to the Python implementation is configured, `rhg` aims to be a drop-in
replacement for `hg` that should behave the same, except that some commands run
faster.

Warning: rhg is experimental and has some rough edges, in order of worse to
less bad:
  * A node/rev that is ambiguous with a name (tag, bookmark, topic, branch)
    will result in the command using the node/rev instead of the name, because
    names are not implemented yet. For example, `rhg cat -r abc` will resolve
    the `abc` node prefix and not look for the `abc` name.
  * some config options may be ignored entirely (this is a bug, please report)
  * pager support is not implemented yet
  * minor errors may be silenced
  * some error messages or error behavior may be slightly different
  * some warning and/or error output may do lossy encoding
  * other "terminal behavior" may be different, like color handling, etc.
  * rhg may be overly cautious in falling back
  * possibly other things we haven't caught yet

With this in mind, `rhg` has been used in production successfully for years now,
and is reasonably well tested, so feel free to use it with these warnings
in mind.
%endif


%prep
%autosetup -p1 -n %{name}-%{upstreamversion}

# Use tk8 with better handling of 8-bit encodings than the default tk9
sed -i.wish8 -e '1,1s/wish/\08/' contrib/hgk

%if %{with rust}
pushd rust
%cargo_prep
popd

%generate_buildrequires
for crate in rust/hg-core rust/hg-pyo3 rust/rhg rust/pyo3-sharedref; do
  cd $crate
  # Temporarily remove  hg-core = { path = "../hg-core"}  dependencies while generating buildrequires.
  # Also, handle another error: feature `full-tracing` includes `hg-core/full-tracing`, but `hg-core` is not a dependency
  sed -i.br -r -e '/=\s*\{[^}]+path\s*=/d' -e '/^full-tracing *=/d' Cargo.toml
  %cargo_generate_buildrequires
  mv -f Cargo.toml{.br,}
  cd - >/dev/null
done
%endif
# /with rust

# These are shipped as examples in /usr/share/docs and should not be executable
chmod -x hgweb.cgi contrib/hgweb.fcgi


%build
%py3_build

# chg will invoke the 'hg' command - no direct Python dependency
pushd contrib/chg
make
popd

%if %{with rust}
# Mercurial build system hardcodes too much. Instead, just build with Fedora macro.
pushd rust
%cargo_build
popd
%endif


%install
%py3_install
make install-doc DESTDIR=%{buildroot} MANDIR=%{_mandir}

# Overrule setup.py policy "c" for module usage: always allow rust extension (if available)
echo 'modulepolicy = b"rust+c-allow"' > %{buildroot}%{python3_sitearch}/mercurial/__modulepolicy__.py

%if %{with rust}
# We are not using the Mercurial build system to build rust, and must thus manually install relevant parts.
install -D -m 755 -pv rust/target/release/rhg %{buildroot}%{_bindir}
install -D -m 755 -pv rust/target/release/librusthg.so \
        %{buildroot}%{python3_sitearch}/mercurial/rustext%{python3_ext_suffix}
%endif

install -D -m 755 contrib/hgk       %{buildroot}%{_libexecdir}/mercurial/hgk
install -m 755 contrib/hg-ssh       %{buildroot}%{_bindir}

mkdir -p %{buildroot}%{_emacs_sitelispdir}/mercurial

pushd contrib
for file in mercurial.el mq.el; do
  #emacs -batch -l mercurial.el --no-site-file -f batch-byte-compile $file
  %{_emacs_bytecompile} $file
  install -p -m 644 $file ${file}c %{buildroot}%{_emacs_sitelispdir}/mercurial
  rm ${file}c
done
popd

pushd contrib/chg
make install DESTDIR=%{buildroot} PREFIX=%{_prefix} MANDIR=%{_mandir}/man1
popd


mkdir -p %{buildroot}%{_sysconfdir}/mercurial/hgrc.d

mkdir -p %{buildroot}%{_emacs_sitestartdir} && install -m644 %SOURCE1 %{buildroot}%{_emacs_sitestartdir}

cat >hgk.rc <<EOF
[extensions]
# enable hgk extension ('hg help' shows 'view' as a command)
hgk=

[hgk]
path=%{_libexecdir}/mercurial/hgk
EOF
install -m 644 hgk.rc %{buildroot}%{_sysconfdir}/mercurial/hgrc.d

mv %{buildroot}%{python3_sitearch}/mercurial/locale %{buildroot}%{_datadir}/locale
rm -rf %{buildroot}%{python3_sitearch}/mercurial/locale

%find_lang hg

%py3_shebang_fix %{buildroot}%{_bindir}/hg-ssh


%files -f hg.lang
%doc CONTRIBUTORS COPYING doc/README doc/hg*.html hgweb.cgi contrib/hgweb.fcgi contrib/hgweb.wsgi
%doc %attr(644,root,root) %{_mandir}/man?/hg*
%doc %attr(644,root,root) contrib/*.svg
%dir %{_sysconfdir}/mercurial
%dir %{_sysconfdir}/mercurial/hgrc.d
%{bash_completions_dir}/hg
%{zsh_completions_dir}/_hg
%pycached %exclude %{python3_sitearch}/hgext/hgk.py
%if %{with rust}
%exclude %{python3_sitearch}/mercurial/rustext%{python3_ext_suffix}
%endif
%{python3_sitearch}/mercurial-%{version}-py%{python3_version}.egg-info/
%{python3_sitearch}/mercurial/
%{python3_sitearch}/hgext/
%{python3_sitearch}/hgext3rd/
%{python3_sitearch}/hgdemandimport/
%{_emacs_sitelispdir}/mercurial
%{_emacs_sitestartdir}/*.el
%{_bindir}/hg
%{_bindir}/hg-ssh

%files hgk
%{_libexecdir}/mercurial/
%pycached %{python3_sitearch}/hgext/hgk.py
%config(noreplace) %{_sysconfdir}/mercurial/hgrc.d/hgk.rc

%files chg
%{_bindir}/chg
%doc %attr(644,root,root) %{_mandir}/man?/chg.*

%if %{with rust}
%files rust
%{_bindir}/rhg
%{python3_sitearch}/mercurial/rustext%{python3_ext_suffix}
%endif


#%%check
# The test suite is too slow and fragile to run here by default.
#cd tests && %%{python3} run-tests.py


%changelog
* Fri Nov 14 2025 Mads Kiilerich <mads@kiilerich.com> - 7.1.2-1
- mercurial 7.1.2

* Mon Oct 13 2025 Mads Kiilerich <mads@kiilerich.com> - 7.1.1-2
- Launch hgk with wish8 / tk8 to avoid regression with 8-bit encodings (#2384296)

* Fri Sep 19 2025 Mads Kiilerich <mads@kiilerich.com> - 7.1.1-1
- mercurial 7.1.1

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 7.1-2
- Rebuilt for Python 3.14.0rc2 bytecode

* Mon Aug 04 2025 Mads Kiilerich <mads@kiilerich.com> - 7.1-1
- mercurial 7.1

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 15 2025 Mads Kiilerich <mads@kiilerich.com> - 7.0.3-1
- mercurial 7.0.3

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 7.0.2-2
- Rebuilt for Python 3.14

* Wed May 07 2025 Mads Kiilerich <mads@kiilerich.com> - 7.0.2-1
- mercurial 7.0.2

* Mon Apr 07 2025 Mads Kiilerich <mads@kiilerich.com> - 7.0.1-1
- mercurial 7.0.1

* Tue Mar 25 2025 Mads Kiilerich <mads@kiilerich.com> - 7.0-1
- mercurial 7.0

* Thu Feb 20 2025 Mads Kiilerich <mads@kiilerich.com> - 6.9.2-1
- mercurial 6.9.2

* Mon Jan 20 2025 Mads Kiilerich <mads@kiilerich.com> - 6.9.1-2
- There is no need for TLS configuration with modern Python

* Thu Jan 16 2025 Mads Kiilerich <mads@kiilerich.com> - 6.9.1-1
- mercurial 6.9.1

* Sat Jan 11 2025 Mads Kiilerich <mads@kiilerich.com> - 6.9-2
- Backport ByteString fix from 6.9.1 (#2336977)

* Wed Nov 20 2024 Mads Kiilerich <mads@kiilerich.com> - 6.9-1
- mercurial 6.9

* Mon Oct 28 2024 Mads Kiilerich <mads@kiilerich.com> - 6.8.2-1
- mercurial 6.8.2

* Mon Oct 07 2024 Mads Kiilerich <mads@kiilerich.com> - 6.8.1-3
- Disable demandimport of collections.abc because Python 3.13 rc3 (#2316252)

* Thu Aug 01 2024 Mads Kiilerich <mads@kiilerich.com> - 6.8.1-2
- Drop upstreamed demandimport patch.

* Thu Aug 01 2024 Mads Kiilerich <mads@kiilerich.com> - 6.8.1-1
- mercurial 6.8.1

* Fri Jul 26 2024 Mads Kiilerich <mads@kiilerich.com> - 6.8-5
- Also exclude 'warnings' from demandimport.

* Fri Jul 26 2024 Mads Kiilerich <mads@kiilerich.com> - 6.8-4
- Exclude threading from demandimport. That became a problem with recent
  "stable" cpython changes. (#2299346)

* Fri Jul 26 2024 Miroslav Suchý <msuchy@redhat.com> - 6.8-3
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 09 2024 Mads Kiilerich <mads@kiilerich.com> - 6.8-1
- mercurial 6.8

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 6.7.3-2
- Rebuilt for Python 3.13

* Mon May 06 2024 Mads Kiilerich <mads@kiilerich.com> - 6.7.3-1
- mercurial 6.7.3

* Mon Apr 08 2024 Mads Kiilerich <mads@kiilerich.com> - 6.7.2-3
- Disable rust packaging - cpython create doesn't work with Python 3.12
  (#2249383)

* Mon Apr 08 2024 Mads Kiilerich <mads@kiilerich.com> - 6.7.2-2
- Drop python3-zombie-imp - it is no longer needed

* Mon Apr 08 2024 Mads Kiilerich <mads@kiilerich.com> - 6.7.2-1
- mercurial 6.7.2

* Mon Feb 12 2024 Mads Kiilerich <mads@kiilerich.com> - 6.6.3-1
- mercurial 6.6.3

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 11 2024 Mads Kiilerich <mads@kiilerich.com> - 6.6.2-1
- mercurial 6.6.2

* Wed Jan 10 2024 Mads Kiilerich <mads@kiilerich.com> - 6.6.1-2
- Fix sources file

* Mon Dec 11 2023 Mads Kiilerich <mads@kiilerich.com> - 6.6.1-1
- mercurial 6.6.1

* Tue Nov 21 2023 Mads Kiilerich <mads@kiilerich.com> - 6.6-1
- mercurial 6.6 and patch to use cargo toml 0.8

* Thu Nov 09 2023 Mads Kiilerich <mads@kiilerich.com> - 6.5.3-2
- Better support for custom _prefix

* Wed Nov 08 2023 Mads Kiilerich <mads@kiilerich.com> - 6.5.3-1
- mercurial 6.5.3

* Mon Aug 07 2023 Mads Kiilerich <mads@kiilerich.com> - 6.5.1-1
- mercurial 6.5.1

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jul 07 2023 Mads Kiilerich <mads@kiilerich.com> - 6.5-1
- mercurial 6.5

* Mon Jun 26 2023 Python Maint <python-maint@redhat.com> - 6.4.5-2
- Rebuilt for Python 3.12

* Thu Jun 22 2023 Mads Kiilerich <mads@kiilerich.com> - 6.4.5-1
- mercurial 6.4.5

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 6.4.4-2
- Rebuilt for Python 3.12

* Thu Jun 08 2023 Mads Kiilerich <mads@kiilerich.com> - 6.4.4-1
- mercurial 6.4.4

* Thu May 04 2023 Mads Kiilerich <mads@kiilerich.com> - 6.4.3-1
- mercurial 6.4.3

* Tue Apr 18 2023 Mads Kiilerich <mads@kiilerich.com> - 6.4.2-1
- mercurial 6.4.2

* Thu Apr 13 2023 Mads Kiilerich <mads@kiilerich.com> - 6.4.1-1
- mercurial 6.4.1

* Fri Mar 24 2023 Mads Kiilerich <mads@kiilerich.com> - 6.4-1
- mercurial 6.4

* Thu Mar 02 2023 Mads Kiilerich <mads@kiilerich.com> - 6.3.3-1
- mercurial 6.3.3

* Thu Feb 23 2023 Fabio Valentini <decathorpe@gmail.com> - 6.3.2-4
- Bump zstd crate dependency from 0.11 to 0.12.

* Sun Feb 05 2023 Fabio Valentini <decathorpe@gmail.com> - 6.3.2-3
- Rebuild for fixed frame pointer compiler flags in Rust RPM macros.

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan 04 2023 Mads Kiilerich <mads@kiilerich.com> - 6.3.2-1
- mercurial 6.3.2

* Sat Nov 19 2022 Mads Kiilerich <mads@kiilerich.com> - 6.3.1-1
- mercurial 6.3.1

* Mon Nov 14 2022 Mads Kiilerich <mads@kiilerich.com> - 6.3.0-1
- mercurial 6.3.0

* Tue Oct 04 2022 Mads Kiilerich <mads@kiilerich.com> - 6.2.3-1
- mercurial 6.2.3

* Sun Sep 04 2022 Mads Kiilerich <mads@kiilerich.com> - 6.2.2-1
- mercurial 6.2.2

* Sat Aug 06 2022 Fabio Valentini <decathorpe@gmail.com> - 6.2.1-3
- Bump zstd crate dependency from 0.10 to 0.11.

* Sat Aug 06 2022 Mads Kiilerich <mads@kiilerich.com> - 6.2.1-2
- Own .egg-info as directory, as introduced by setuptools 60 (#2115906)

* Thu Jul 28 2022 Mads Kiilerich <mads@kiilerich.com> - 6.2.1-1
- mercurial 6.2.1

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jul 11 2022 Mads Kiilerich <mads@kiilerich.com> - 6.2-2
- Update sources with mercurial-6.2.tar.gz

* Mon Jul 11 2022 Mads Kiilerich <mads@kiilerich.com> - 6.2-1
- mercurial 6.2

* Mon Jul 11 2022 Mads Kiilerich <mads@kiilerich.com> - 6.1.4-2
- Fix build after upstream applied patch

* Thu Jun 16 2022 Mads Kiilerich <mads@kiilerich.com> - 6.1.4-1
- mercurial 6.1.4

* Tue Jun 14 2022 Python Maint <python-maint@redhat.com> - 6.1.3-3
- Rebuilt for Python 3.11

* Fri Jun 03 2022 Mads Kiilerich <mads@kiilerich.com> - 6.1.3-2
- work around too narrow im-rc version constraint

* Thu Jun 02 2022 Mads Kiilerich <mads@kiilerich.com> - 6.1.3-1
- mercurial 6.1.3

* Mon May 23 2022 Stefan Bluhm <stefan.bluhm@clacee.eu> - 6.1.2-3
- Disable Rust components for Enterprise Linux.

* Fri May 13 2022 Mads Kiilerich <mads@kiilerich.com> - 6.1.2-2
- Rust dependency catch-up

* Thu May 05 2022 Mads Kiilerich <mads@kiilerich.com> - 6.1.2-1
- mercurial 6.1.2

* Tue May 03 2022 Mads Kiilerich <mads@kiilerich.com> - 6.1.1-4
- Address some rpmlint issues

* Thu Apr 14 2022 Aleksei Bavshin <alebastr@fedoraproject.org> - 6.1.1-3
- Build Rust components

* Wed Apr 06 2022 Mads Kiilerich <mads@kiilerich.com> - 6.1.1-2
- Undo accicental commit

* Wed Apr 06 2022 Mads Kiilerich <mads@kiilerich.com> - 6.1.1-1
- mercurial 6.1.1

* Tue Mar 01 2022 Mads Kiilerich <mads@kiilerich.com> - 6.1-1
- mercurial 6.1

* Fri Feb 18 2022 Mads Kiilerich <mads@kiilerich.com> - 6.0.3-1
- mercurial 6.0.3

* Wed Feb 02 2022 Mads Kiilerich <mads@kiilerich.com> - 6.0.2-1
- mercurial 6.0.2

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jan 05 2022 Mads Kiilerich <mads@kiilerich.com> - 6.0.1-1
- mercurial 6.0.1

* Wed Nov 24 2021 Mads Kiilerich <mads@kiilerich.com> - 6.0-1
- mercurial 6.0

* Thu Nov 18 2021 Mads Kiilerich <mads@kiilerich.com> - 5.9.3-2
- Drop old upgrade path
- Recommend python3-fb-re2 which will speed up some operations

* Wed Oct 27 2021 Mads Kiilerich <mads@kiilerich.com> - 5.9.3-1
- mercurial 5.9.3

* Wed Oct 06 2021 Mads Kiilerich <mads@kiilerich.com> - 5.9.2-1
- mercurial 5.9.2

* Wed Sep 01 2021 Mads Kiilerich <mads@kiilerich.com> - 5.9.1-1
- mercurial 5.9.1

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jul 12 2021 Mads Kiilerich <mads@kiilerich.com> - 5.8.1-1
- mercurial 5.8.1

* Thu Jun 03 2021 Python Maint <python-maint@redhat.com> - 5.8-2
- Rebuilt for Python 3.10

* Tue May 11 2021 Mads Kiilerich <mads@kiilerich.com> - 5.8-1
- mercurial 5.8

* Tue Mar 09 2021 Mads Kiilerich <mads@kiilerich.com> - 5.7.1-1
- mercurial 5.7.1

* Wed Feb 03 2021 Mads Kiilerich <mads@kiilerich.com> - 5.7-1
- mercurial 5.7

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.6.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan 20 2021 Petr Stodulka <pstodulk@redhat.com> - 5.6.1-6
- Set Provides for the obsoleted mercurial-py3 and mercurial-lang rpms
- Relates: #1917946

* Sun Jan  3 03:39:35 CET 2021 Mads Kiilerich <mads@kiilerich.com> - 5.6.1-5
- Stop providing hg3 - that is the only hg we have
- Drop alternatives - there is no alternative
- Move main package back to mercurial without py3 suffix
- Drop the -lang package

* Tue Dec  8 17:14:14 CET 2020 Mads Kiilerich <mads@kiilerich.com> - 5.6.1-4
- Change mercurial-hgk to use py3
- Use py3 for locales - py2 is going away
- Clarify in comment that chg has no py2/py3 concerns
- Drop comment left over from 53899096 when it introduced use of PYTHON=
- Let mercurial-py3 obsolete mercurial-py2 - it is going away soon
- Trivial removal of py2 package - no cleanup

* Sat Dec  5 14:50:30 CET 2020 Mads Kiilerich <mads@kiilerich.com> - 5.6.1-3
- Fix ownership of hgext3rd and hgdemandimport (#1897681)

* Thu Dec  3 21:24:26 CET 2020 Mads Kiilerich <mads@kiilerich.com> - 5.6.1-2
- Drop hgdemandimport_ast.patch - it has been fixed both in Mercurial 5.5.2 and
  Python 3.9.0rc2

* Thu Dec  3 20:39:41 CET 2020 Mads Kiilerich <mads@kiilerich.com> - 5.6.1-1
- mercurial 5.6.1

* Mon Nov 30 2020 Miro Hrončok <mhroncok@redhat.com> - 5.4-5
- Install Python 3 based mercurial by default

* Wed Sep 02 2020 Petr Viktorin <pviktori@redhat.com> - 5.4-4
- Add _ast to hgdemandimport ignore list
  Works around: BZ#1871992

* Mon Aug 10 2020 Petr Stodulka <pstodulk@redhat.com> - 5.4-3
- Fix upgrade from previous mercurial 4.9 causing broken alternatives for
  mercurial
- Resolves: #1831562

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jun  3 2020 Neal Becker <ndbecker2@gmail.com> - 5.4-1
- Update to 5.4

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 5.2-5
- Rebuilt for Python 3.9

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Dec 12 2019 Miro Hrončok <mhroncok@redhat.com> - 5.2-3
- Remove stray Python 2 files from the Python 3 package

* Tue Nov 26 2019 Miro Hrončok <mhroncok@redhat.com> - 5.2-2
- Use alternatives for /usr/bin/hg

* Mon Nov 25 2019 Petr Stodulka <pstodulk@redhat.com> - 5.2-1
- Update to 5.2
- Mercurial port is now much more stable on Python3 than before;
  still some issues can be discovered regarding the Python3
- Relates: #1737931

* Sat Oct 19 2019 Petr Stodulka <pstodulk@redhat.com> - 5.1.2-2
- first attempt to create builds for py2 & py3 version
- separate lang into the own subpackage as files are shared between
  mercurial for both pythons
- extensions are now prepared and working only under Python2
- the core mercurial is prepared in mercurial-python3 subpackage providing
  the hg3 executable
- Relates: #1737931

* Sat Oct 19 2019 Petr Stodulka <pstodulk@redhat.com> - 5.1.2-1
- Update to 5.1.2
- fix patching of Makefiles

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Apr  8 2019 Neal Becker <ndbecker2@gmail.com> - 4.9-1
- Update to 4.9

* Tue Mar  5 2019 Neal Becker <ndbecker2@gmail.com> - 4.7-3
- Fix shebang for python2

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Aug 20 2018 Petr Stodulka <pstodulk@redhat.com> - 4.7-1
- Update to 4.7

* Sat Aug 11 2018 Tom Prince <tom.prince@ualberta.net> - 4.5.3-1
- Package chg extension.

* Sat Aug 11 2018 Petr Stodulka <pstodulk@redhat.com> - 4.5.3-1
- Update to 4.5.3
- Resolves: CVE-2018-1000132

* Tue Jul 24 2018 Sebastian Kisela <skisela@redhat.com> - 4.4.2-6
- Stop using deprecated python macros: https://fedoraproject.org/wiki/Packaging:Python
- Add gcc build time dependency, as gcc was removed from default buildroot package set.

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.4.2-4
- Escape macros in %%changelog

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 09 2018 Iryna Shcherbina <ishcherb@redhat.com> - 4.4.2-2
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Dec 29 2017 Neal Becker <nbecker@nbecker2> - 4.4.2-1
- Update to 4.4.2

* Fri Aug 11 2017 Petr Stodulka <pstodulk@redhat.com> - 4.2.3-1
- Update to 4.2.3
- Resolves: CVE-2017-1000115 CVE-2017-1000116

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 12 2017 Neal Becker <nbecker@nbecker2> - 4.2.1-1
- Update to 4.2.1

* Mon Feb 27 2017 Neal Becker <nbecker@nbecker2> - 4.1-1
- Update to 4.1

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 23 2016 Neal Becker <nbecker@nbecker2> - 4.0.1-1
- Update to 4.0.1

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.1-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue May 03 2016 Neal Becker <ndbecker2@gmail.com> - 3.8.1-1
- Update to 3.8.1

* Tue Mar 29 2016 Neal Becker <ndbecker2@gmail.com> - 3.7.3-1
- Update to 3.7.3

* Thu Feb 25 2016 Neal Becker <ndbecker2@gmail.com> - 3.7.1-1
- Update to 3.7.1

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 22 2016 Neal Becker <ndbecker2@gmail.com> - 3.6.3-1
- Update to 3.6.3

* Thu Dec 24 2015 Neal Becker <ndbecker2@gmail.com> - 3.6.2-1
- Update to 3.6.2

* Fri Sep 11 2015 Neal Becker <ndbecker2@gmail.com> - 3.5.1-1
- Update to 3.5.1

* Wed Aug 12 2015 Neal Becker <ndbecker2@gmail.com> - 3.5-1
- Update to 3.5

* Tue Jun 23 2015 Neal Becker <ndbecker2@gmail.com> - 3.4.1-1
- Update to 3.4.1
- Obsolete emacs-mercurial{-el}
- own _emacs_sitelispdir/mercurial
- use standard emacs macros

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Apr  3 2015 Neal Becker <ndbecker2@gmail.com> - 3.3.3-1
- update to 3.3.3

* Mon Mar 16 2015 Neal Becker <ndbecker2@gmail.com> - 3.3.2-1
- Update to 3.3.2
- upstream dropped mergetools.rc

* Sat Jan 24 2015 Ville Skyttä <ville.skytta@iki.fi> - 3.2.3-2
- Install bash completion to %%{_datadir}/bash-completion/completions

* Sun Dec 21 2014 nbecker <ndbecker2@gmail.com> - 3.2.3-1
- Fixes CVE-2014-9390

* Tue Dec 16 2014 nbecker <ndbecker2@gmail.com> - 3.2-1
- Update to 3.2.2

* Sun Oct 19 2014 nbecker <ndbecker2@gmail.com> - 3.2-1.rc
- Patch0 no longer needed?
- Drop sample.hgrc (from upstream)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 30 2014 nbecker <ndbecker2@gmail.com> - 3.0-1
- fix Release

* Fri May 30 2014 nbecker <ndbecker2@gmail.com> - 3.0-
- Update to 3.0

* Wed Feb  5 2014 nbecker <ndbecker2@gmail.com> - 2.9-1
- Update to 2.9

* Fri Nov  8 2013 nbecker <ndbecker2@gmail.com> - 2.8-1
- Update to 2.8

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul  8 2013 nbecker <ndbecker2@gmail.com> - 2.6.3-1
- Update to 2.6.3


* Thu Jun 6 2013 nbecker <ndbecker2@gmail.com> - 2.6.2-1
- Update to 2.6.2

* Wed May  8 2013 nbecker <ndbecker2@gmail.com> - 2.6-1
- Update to 2.6

* Mon Mar 18 2013 nbecker <ndbecker2@gmail.com> - 2.5.2-2
- Add hgweb.wsgi

* Sat Mar  2 2013 nbecker <ndbecker2@gmail.com> - 2.5.2-1
- Update to 2.5.2

* Sat Feb  9 2013 Neal Becker <ndbecker2@gmail.com> - 2.5.1-1
- Update to 2.5.1

* Tue Feb  5 2013 Neal Becker <ndbecker2@gmail.com> - 2.5-1
- Update to 2.5

* Sun Dec 16 2012 Neal Becker <ndbecker2@gmail.com> - 2.4.1-1
- Update to 2.4.1

* Sun Nov  4 2012 Neal Becker <ndbecker2@gmail.com> - 2.4-1
- Update to 2.4

* Wed Sep  5 2012 Neal Becker <ndbecker2@gmail.com> - 2.3.1-1
- Update to 2.3.1

* Mon Aug 13 2012 Neal Becker <ndbecker2@gmail.com> - 2.3-1
- Update to 2.3

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul  9 2012 Neal Becker <ndbecker2@gmail.com> - 2.2.3-1
- Update to 2.2.3

* Sun Jun  3 2012 Neal Becker <ndbecker2@gmail.com> - 2.2.2-1
- Update to 2.2.2

* Fri May 25 2012 Neal Becker <ndbecker2@gmail.com> - 2.2.1-2
- Add certs.rc

* Fri May  4 2012 Neal Becker <ndbecker2@gmail.com> - 2.2.1-1
- update to 2.2.1

* Wed May  2 2012 Neal Becker <ndbecker2@gmail.com> - 2.2-1
- Update to 2.2

* Fri Apr  6 2012 Neal Becker <ndbecker2@gmail.com> - 2.1.2-1
- Update to 2.1.2

* Sat Mar 10 2012 Neal Becker <ndbecker2@gmail.com> - 2.1.1-1
- Update to 2.1.1

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jan  1 2012 Neal Becker <ndbecker2@gmail.com> - 2.0.2-1
- Update to 2.0.2

* Wed Nov 16 2011 Neal Becker <ndbecker2@gmail.com> - 2.0-1
- Update to 2.0

* Tue Oct 11 2011 Neal Becker <ndbecker2@gmail.com> - 1.9.3-2
- Fix br 744931 (unowned dir)

* Sun Oct  2 2011 Neal Becker <ndbecker2@gmail.com> - 1.9.3-1
- update to 1.9.3

* Sat Aug 27 2011 Neal Becker <ndbecker2@gmail.com> - 1.9.2-1
- Update to 1.9.2

* Wed Aug  3 2011 Neal Becker <ndbecker2@gmail.com> - 1.9.1-1
- Update to 1.9.1

* Fri Jul  1 2011 Neal Becker <ndbecker2@gmail.com> - 1.9-2
- Remove docutils patch

* Fri Jul  1 2011 Neal Becker <ndbecker2@gmail.com> - 1.9-1
- Update to 1.9

* Thu Jun  2 2011 Neal Becker <ndbecker2@gmail.com> - 1.8.4-2
- Add docutils-0.8 patch

* Wed Jun  1 2011 Neal Becker <ndbecker2@gmail.com> - 1.8.4-1
- Update to 1.8.4

* Sat Apr  2 2011 Neal Becker <ndbecker2@gmail.com> - 1.8.2-1
- update to 1.8.2

* Mon Mar 14 2011 Neal Becker <ndbecker2@gmail.com> - 1.8.1-2
- Try BR emacs-nox

* Mon Mar 14 2011 Neal Becker <ndbecker2@gmail.com> - 1.8.1-1
- Update to 1.8.1

* Wed Mar  2 2011 Neal Becker <ndbecker2@gmail.com> - 1.8-1
- Update to 1.8

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Feb  5 2011 Neal Becker <ndbecker2@gmail.com> - 1.7.5-1
- Update to 1.7.5

* Sun Jan  2 2011 Neal Becker <ndbecker2@gmail.com> - 1.7.3-1
- Update to 1.7.3

* Thu Dec  2 2010 Neal Becker <ndbecker2@gmail.com> - 1.7.2-1
- Update to 1.7.2

* Mon Nov 15 2010 Neal Becker <ndbecker2@gmail.com> - 1.7.1-1
- Update to 1.7.1

* Mon Nov  1 2010 Neal Becker <ndbecker2@gmail.com> - 1.7-3
- BR python-docutils

* Mon Nov  1 2010 Neal Becker <ndbecker2@gmail.com> - 1.7-2
- Make that 1.7

* Mon Nov  1 2010 Neal Becker <ndbecker2@gmail.com> - 1.7.0-1
- Update to 1.7.0

* Thu Oct 21 2010 Neal Becker <ndbecker2@gmail.com> - 1.6.4-4
- Try another way to own directories

* Wed Oct 20 2010 Neal Becker <ndbecker2@gmail.com> - 1.6.4-3
- Fixup unowned directories

* Wed Oct  6 2010 Neal Becker <ndbecker2@gmail.com> - 1.6.4-3
- patch i18n.py so hg will find moved locale files

* Fri Oct  1 2010 Neal Becker <ndbecker2@gmail.com> - 1.6.4-1
- Update to 1.6.4

* Fri Aug 27 2010 Neal Becker <ndbecker2@gmail.com> - 1.6.3-1
- Fix some rpmlint issues

* Thu Aug 26 2010 Neal Becker <ndbecker2@gmail.com> - 1.6.3-1
- Update to 1.6.3

* Mon Aug  2 2010 Neal Becker <ndbecker2@gmail.com> - 1.6.2-1
- Update to 1.6.2

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Jul  4 2010 Neal Becker <ndbecker2@gmail.com> - 1.6-2
- Remove hg-viz, git-rev-tree

* Sun Jul  4 2010 Neal Becker <ndbecker2@gmail.com> - 1.6-1
- Update to 1.6
- git-viz is removed

* Fri Jun 25 2010 Neal Becker <ndbecker2@gmail.com> - 1.5.4-1
- Don't install mercurial-convert-repo (use hg convert instead)

* Wed Jun  2 2010 Neal Becker <ndbecker2@gmail.com> - 1.5.4-1
- Update to 1.5.4

* Fri May 14 2010 Neal Becker <ndbecker2@gmail.com> - 1.5.3-1
- Update to 1.5.3

* Mon May  3 2010 Neal Becker <ndbecker2@gmail.com> - 1.5.2-1
- update to 1.5.2

* Mon Apr  5 2010 Neal Becker <ndbecker2@gmail.com> - 1.5.1-1
- Update to 1.5.1

* Sat Mar  6 2010 Neal Becker <ndbecker2@gmail.com> - 1.5-2
- doc/ja seems to be gone

* Sat Mar  6 2010 Neal Becker <ndbecker2@gmail.com> - 1.5-1
- Update to 1.5

* Fri Feb  5 2010 Neal Becker <ndbecker2@gmail.com> - 1.4.3-2
- License changed to gplv2+

* Mon Feb  1 2010 Neal Becker <ndbecker2@gmail.com> - 1.4.3-1
- Update to 1.4.3

* Sat Jan  2 2010 Neal Becker <ndbecker2@gmail.com> - 1.4.2-1
- Update to 1.4.2

* Wed Dec  2 2009 Neal Becker <ndbecker2@gmail.com> - 1.4.1-1
- Update to 1.4.1

* Mon Nov 16 2009 Neal Becker <ndbecker2@gmail.com> - 1.4-1.1
- Bump to 1.4-1.1

* Mon Nov 16 2009 Neal Becker <ndbecker2@gmail.com> - 1.4-1
- Update to 1.4

* Fri Jul 24 2009 Neal Becker <ndbecker2@gmail.com> - 1.3.1-3
- Disable self-tests

* Fri Jul 24 2009 Neal Becker <ndbecker2@gmail.com> - 1.3.1-2
- Update to 1.3.1

* Wed Jul  1 2009 Neal Becker <ndbecker2@gmail.com> - 1.3-2
- Re-enable tests since they now pass

* Wed Jul  1 2009 Neal Becker <ndbecker2@gmail.com> - 1.3-1
- Update to 1.3

* Sat Mar 21 2009 Neal Becker <ndbecker2@gmail.com> - 1.2.1-1
- Update to 1.2.1
- Tests remain disabled due to failures

* Wed Mar  4 2009 Neal Becker <ndbecker2@gmail.com> - 1.2-2
- patch0 for filemerge bug should not be needed

* Wed Mar  4 2009 Neal Becker <ndbecker2@gmail.com> - 1.2-1
- Update to 1.2

* Tue Feb 24 2009 Neal Becker <ndbecker2@gmail.com> - 1.1.2-7
- Use noreplace option on config

* Mon Feb 23 2009 Neal Becker <ndbecker2@gmail.com> - 1.1.2-6
- Fix typo

* Mon Feb 23 2009 Neal Becker <ndbecker2@gmail.com> - 1.1.2-5
- Own directories bash_completion.d and zsh/site-functions
  https://bugzilla.redhat.com/show_bug.cgi?id=487015

* Mon Feb  9 2009 Neal Becker <ndbecker2@gmail.com> - 1.1.2-4
- Mark mergetools.rc as config

* Sat Feb  7 2009 Neal Becker <ndbecker2@gmail.com> - 1.1.2-3
- Patch mergetools.rc to fix filemerge bug

* Thu Jan  1 2009 Neal Becker <ndbecker2@gmail.com> - 1.1.2-2
- Rename mergetools.rc -> mergetools.rc.sample

* Thu Jan  1 2009 Neal Becker <ndbecker2@gmail.com> - 1.1.2-1
- Update to 1.1.2

* Wed Dec 24 2008 Neal Becker <ndbecker2@gmail.com> - 1.1.1-3
- Install mergetools.rc as mergetools.rc.sample

* Sun Dec 21 2008 Neal Becker <ndbecker2@gmail.com> - 1.1.1-2
- Fix typo

* Sun Dec 21 2008 Neal Becker <ndbecker2@gmail.com> - 1.1.1-1
- Update to 1.1.1

* Thu Dec 04 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.1-2
- Rebuild for Python 2.6

* Tue Dec  2 2008 Neal Becker <ndbecker2@gmail.com> - 1.1-1
- Update to 1.1

* Mon Dec  1 2008 Neal Becker <ndbecker2@gmail.com> - 1.0.2-4
- Bump tag

* Mon Dec  1 2008 Neal Becker <ndbecker2@gmail.com> - 1.0.2-3
- Remove BR asciidoc
- Use macro for python executable

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.0.2-2
- Rebuild for Python 2.6

* Fri Aug 15 2008 Neal Becker <ndbecker2@gmail.com> - 1.0.2-1
- Update to 1.0.2

* Sun Jun 15 2008 Neal Becker <ndbecker2@gmail.com> - 1.0.1-4
- Bitten by expansion of commented out macro (again)

* Sun Jun 15 2008 Neal Becker <ndbecker2@gmail.com> - 1.0.1-3
- Add BR pkgconfig

* Sun Jun 15 2008 Neal Becker <ndbecker2@gmail.com> - 1.0.1-2
- Update to 1.0.1
- Fix emacs_version, etc macros (need expand)
- Remove patch0

* Mon Jun  2 2008 Neal Becker <ndbecker2@gmail.com> - 1.0-15
- Bump release tag

* Thu Apr 17 2008 Neal Becker <ndbecker2@gmail.com> - 1.0-14
- Oops, fix %%files due to last change

* Wed Apr 16 2008 Neal Becker <ndbecker2@gmail.com> - 1.0-13
- install mergetools.hgrc as mergetools.rc

* Sat Apr 12 2008 Neal Becker <ndbecker2@gmail.com> - 1.0-12
- Remove xemacs pkg - this is moved to xemacs-extras
- Own %%{python_sitearch}/{mercurial,hgext} dirs

* Thu Apr 10 2008 Neal Becker <ndbecker2@gmail.com> - 1.0-11
- Use install -p to install .el{c} files
- Don't (load mercurial) by default.

* Wed Apr  9 2008 Neal Becker <ndbecker2@gmail.com> - 1.0-10
- Patch to hgk from Mads Kiilerich <mads@kiilerich.com>

* Tue Apr  8 2008 Neal Becker <ndbecker2@gmail.com> - 1.0-9
- Add '-l mercurial.el' for emacs also

* Tue Apr  8 2008 Neal Becker <ndbecker2@gmail.com> - 1.0-8
- BR xemacs-packages-extra

* Tue Apr  8 2008 Neal Becker <ndbecker2@gmail.com> - 1.0-7
- Various fixes

* Tue Apr  8 2008 Neal Becker <ndbecker2@gmail.com> - 1.0-6
- fix to comply with emacs packaging guidelines

* Thu Mar 27 2008 Neal Becker <ndbecker2@gmail.com> - 1.0-5
- Move hgk-related py files to hgk
- Put mergetools.hgrc in /etc/mercurial/hgrc.d
- Add hgk.rc and put in /etc/mercurial/hgrc.d

* Wed Mar 26 2008 Neal Becker <ndbecker2@gmail.com> - 1.0-4
- Rename mercurial-site-start -> mercurial-site-start.el

* Wed Mar 26 2008 Neal Becker <ndbecker2@gmail.com> - 1.0-3
- Incorprate suggestions from hopper@omnifarious.org

* Wed Mar 26 2008 Neal Becker <ndbecker2@gmail.com> - 1.0-2
- Add site-start

* Tue Mar 25 2008 Neal Becker <ndbecker2@gmail.com> - 1.0-1
- Update to 1.0
- Disable check for now - 1 test fails
- Move emacs to separate package
- Add check

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.9.5-7
- Autorebuild for GCC 4.3

* Fri Nov  9 2007 Neal Becker <ndbecker2@gmail.com> - 0.9.5-6
- rpmlint fixes

* Fri Nov  9 2007 Neal Becker <ndbecker2@gmail.com> - 0.9.5-5
- /etc/mercurial/hgrc.d missing

* Fri Nov  9 2007 Neal Becker <ndbecker2@gmail.com> - 0.9.5-3
- Fix to last change

* Fri Nov  9 2007 Neal Becker <ndbecker2@gmail.com> - 0.9.5-2
- mkdir /etc/mercurial/hgrc.d for plugins

* Tue Oct 23 2007  <ndbecker2@gmail.com> - 0.9.5-2
- Bump tag to fix confusion

* Mon Oct 15 2007 Neal Becker <ndbecker2@gmail.com> - 0.9.5-1
- Sync with spec file from mercurial

* Sat Sep 22 2007 Neal Becker <ndbecker2@gmail.com> - 0.9.4-8
- Just cp contrib tree.
- Revert install -O2

* Thu Sep 20 2007 Neal Becker <ndbecker2@gmail.com> - 0.9.4-7
- Change setup.py install to -O2 to get bytecompile on EL-4

* Thu Sep 20 2007 Neal Becker <ndbecker2@gmail.com> - 0.9.4-6
- Revert last change.

* Thu Sep 20 2007 Neal Becker <ndbecker2@gmail.com> - 0.9.4-5
- Use {ghost} on contrib, otherwise EL-4 build fails

* Thu Sep 20 2007 Neal Becker <ndbecker2@gmail.com> - 0.9.4-4
- remove {_datadir}/contrib stuff for now

* Thu Sep 20 2007 Neal Becker <ndbecker2@gmail.com> - 0.9.4-3
- Fix mercurial-install-contrib.patch (/usr/share/mercurial->/usr/share/mercurial/contrib)

* Wed Aug 29 2007 Jonathan Shapiro <shap@eros-os.com> - 0.9.4-2
- update to 0.9.4-2
- install contrib directory
- set up required path for hgk
- install man5 man pages

* Thu Aug 23 2007 Neal Becker <ndbecker2@gmail.com> - 0.9.4-1
- update to 0.9.4

* Wed Jan  3 2007 Jeremy Katz <katzj@redhat.com> - 0.9.3-1
- update to 0.9.3
- remove asciidoc files now that we have them as manpages

* Mon Dec 11 2006 Jeremy Katz <katzj@redhat.com> - 0.9.2-1
- update to 0.9.2

* Mon Aug 28 2006 Jeremy Katz <katzj@redhat.com> - 0.9.1-2
- rebuild

* Tue Jul 25 2006 Jeremy Katz <katzj@redhat.com> - 0.9.1-1
- update to 0.9.1

* Fri May 12 2006 Mihai Ibanescu <misa@redhat.com> - 0.9-1
- update to 0.9

* Mon Apr 10 2006 Jeremy Katz <katzj@redhat.com> - 0.8.1-1
- update to 0.8.1
- add man pages (#188144)

* Fri Mar 17 2006 Jeremy Katz <katzj@redhat.com> - 0.8-3
- rebuild

* Fri Feb 17 2006 Jeremy Katz <katzj@redhat.com> - 0.8-2
- rebuild

* Mon Jan 30 2006 Jeremy Katz <katzj@redhat.com> - 0.8-1
- update to 0.8

* Thu Sep 22 2005 Jeremy Katz <katzj@redhat.com> 
- add contributors to %%doc

* Tue Sep 20 2005 Jeremy Katz <katzj@redhat.com> - 0.7
- update to 0.7

* Mon Aug 22 2005 Jeremy Katz <katzj@redhat.com> - 0.6c
- update to 0.6c

* Tue Jul 12 2005 Jeremy Katz <katzj@redhat.com> - 0.6b
- update to new upstream 0.6b

* Fri Jul  1 2005 Jeremy Katz <katzj@redhat.com> - 0.6-1
- Initial build.

