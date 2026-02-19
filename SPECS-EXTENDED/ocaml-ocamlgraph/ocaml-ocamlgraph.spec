# OCaml packages not built on i686 since OCaml 5 / Fedora 39.
ExcludeArch: %{ix86}

%global giturl  https://github.com/backtracking/ocamlgraph

Name:           ocaml-ocamlgraph
Version:        2.2.0
Release:        5%{?dist}
Summary:        OCaml library for arc and node graphs
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
License:        LGPL-2.1-only WITH OCaml-LGPL-linking-exception
URL:            https://backtracking.github.io/ocamlgraph/
VCS:            git:%{giturl}.git
Source:         %{giturl}/releases/download/%{version}/ocamlgraph-%{version}.tbz#/%{name}-%{version}.tbz

BuildRequires:  ocaml >= 4.08.0
BuildRequires:  ocaml-dune >= 2.0
BuildRequires:  ocaml-graphics-devel
BuildRequires:  ocaml-lablgtk-devel
BuildRequires:  pkgconfig(libgnomecanvas-2.0)

%description
Ocamlgraph provides several different implementations of graph data
structures. It also provides implementations for a number of classical
graph algorithms like Kruskal's algorithm for MSTs, topological
ordering of DAGs, Dijkstra's shortest paths algorithm, and
Ford-Fulkerson's maximal-flow algorithm to name a few. The algorithms
and data structures are written functorially for maximal
reusability. Also has input and output capability for Graph Modeling
Language file format and Dot and Neato graphviz (graph visualization)
tools.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and signature files
for developing applications that use %{name}.

%package        gtk
Summary:        Display graphs using OCamlGraph and GTK2
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    gtk
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%package        gtk-devel
Summary:        Development files for %{name}-gtk
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}
Requires:       %{name}-gtk%{?_isa} = %{version}-%{release}
Requires:       ocaml-lablgtk-devel%{?_isa}
Requires:       libgnomecanvas-devel%{?_isa}

%description    gtk-devel
The %{name}-gtk-devel package contains libraries and signature
files for developing applications that use %{name}-gtk.

%package        tools
Summary:        Graph editing tools for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    tools
The %{name}-tools package contains graph editing tools for use with
%{name}.

%prep
%autosetup -n ocamlgraph-%{version}

%conf
# Fix encoding
for fil in COPYING TODO.md; do
  iconv -f latin1 -t utf-8 $fil > $fil.utf8
  touch -r $fil $fil.utf8
  mv -f $fil.utf8 $fil
done

%build
%dune_build @default editor

%install
%dune_install -s

# Install the graph editing tools
mkdir -p %{buildroot}%{_bindir}
install -m 0755 -p _build/default/editor/editor.exe \
        %{buildroot}/%{_bindir}/ocamlgraph-editor
install -m 0755 -p _build/default/editor/ed_main.exe \
        %{buildroot}/%{_bindir}/ocamlgraph-ed_main
install -m 0755 -p _build/default/editor/graphEdGTK.exe \
        %{buildroot}/%{_bindir}/graphEdGTK
install -m 0755 -p _build/default/dgraph/dGraphViewer.exe \
        %{buildroot}%{_bindir}/dGraphViewer
install -m 0755 -p _build/default/view_graph/viewGraph_test.exe \
        %{buildroot}%{_bindir}/ocamlgraph-viewgraph

%check
%dune_check

%files -f .ofiles-ocamlgraph
%doc CREDITS FAQ
%license COPYING LICENSE

%files devel -f .ofiles-ocamlgraph-devel
%doc examples CHANGES.md README.md

%files gtk -f .ofiles-ocamlgraph_gtk

%files gtk-devel -f .ofiles-ocamlgraph_gtk-devel

%files tools
%{_bindir}/dGraphViewer
%{_bindir}/graphEdGTK
%{_bindir}/ocamlgraph*

%changelog
* Fri Nov 28 2025 Aninda Pradhan <v-anipradhan@microsoft.com> - 2.2.0-5
- Initial Azure Linux import from Fedora 44 (license: MIT)
- License Verified

* Mon Oct 13 2025 Richard W.M. Jones <rjones@redhat.com> - 2.2.0-4
- OCaml 5.4.0 rebuild

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jul 12 2025 Jerry James <loganjerry@gmail.com> - 2.2.0-2
- Rebuild to fix OCaml dependencies

* Tue Apr 15 2025 Jerry James <loganjerry@gmail.com> - 2.2.0-1
- Version 2.2.0

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jan  9 2025 Jerry James <loganjerry@gmail.com> - 2.1.0-10
- OCaml 5.3.0 rebuild for Fedora 42

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 19 2024 Richard W.M. Jones <rjones@redhat.com> - 2.1.0-8
- OCaml 5.2.0 ppc64le fix

* Wed May 29 2024 Richard W.M. Jones <rjones@redhat.com> - 2.1.0-7
- OCaml 5.2.0 for Fedora 41

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 18 2023 Richard W.M. Jones <rjones@redhat.com> - 2.1.0-4
- OCaml 5.1.1 + s390x code gen fix for Fedora 40

* Tue Dec 12 2023 Richard W.M. Jones <rjones@redhat.com> - 2.1.0-3
- OCaml 5.1.1 rebuild for Fedora 40

* Thu Oct 05 2023 Richard W.M. Jones <rjones@redhat.com> - 2.1.0-2
- OCaml 5.1 rebuild for Fedora 40

* Sat Sep  9 2023 Jerry James <loganjerry@gmail.com> - 2.1.0-1
- Version 2.1.0

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Richard W.M. Jones <rjones@redhat.com> - 2.0.0-13
- OCaml 5.0 rebuild for Fedora 39

* Mon Jul 10 2023 Jerry James <loganjerry@gmail.com> - 2.0.0-12
- OCaml 5.0.0 rebuild

* Tue Jan 24 2023 Richard W.M. Jones <rjones@redhat.com> - 2.0.0-11
- Rebuild OCaml packages for F38

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Dec 12 2022 Jerry James <loganjerry@gmail.com> - 2.0.0-9
- Convert License tag to SPDX

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 20 2022 Jerry James <loganjerry@gmail.com> - 2.0.0-8
- Use new OCaml macros

* Sun Jun 19 2022 Richard W.M. Jones <rjones@redhat.com> - 2.0.0-8
- OCaml 4.14.0 rebuild

* Fri Feb 04 2022 Richard W.M. Jones <rjones@redhat.com> - 2.0.0-7
- OCaml 4.13.1 rebuild to remove package notes

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Dec 27 2021 Jerry James <loganjerry@gmail.com> - 2.0.0-5
- Rebuild for ocaml-lablgtk 2.18.12

* Mon Oct 04 2021 Richard W.M. Jones <rjones@redhat.com> - 2.0.0-4
- OCaml 4.13.1 build

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 22 2021 Jerry James <loganjerry@gmail.com> - 2.0.0-2
- Rebuild for ocaml-lablgtk with gnomeui removed

* Tue Jun  8 2021 Jerry James <loganjerry@gmail.com> - 2.0.0-1
- Version 2.0.0
- Drop all patches
- New URLs

* Mon Mar  1 16:57:43 GMT 2021 Richard W.M. Jones <rjones@redhat.com> - 1.8.8-25
- OCaml 4.12.0 build

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.8-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Sep 01 2020 Richard W.M. Jones <rjones@redhat.com> - 1.8.8-23
- OCaml 4.11.1 rebuild

* Fri Aug 21 2020 Richard W.M. Jones <rjones@redhat.com> - 1.8.8-22
- OCaml 4.11.0 rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.8-21
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.8-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon May 04 2020 Richard W.M. Jones <rjones@redhat.com> - 1.8.8-19
- OCaml 4.11.0+dev2-2020-04-22 rebuild

* Tue Apr 21 2020 Richard W.M. Jones <rjones@redhat.com> - 1.8.8-18
- OCaml 4.11.0 pre-release attempt 2

* Fri Apr 17 2020 Richard W.M. Jones <rjones@redhat.com> - 1.8.8-17
- OCaml 4.11.0 pre-release

* Thu Apr 02 2020 Richard W.M. Jones <rjones@redhat.com> - 1.8.8-16
- Update all OCaml dependencies for RPM 4.16.

* Wed Feb 26 2020 Richard W.M. Jones <rjones@redhat.com> - 1.8.8-15
- OCaml 4.10.0 final.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.8-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jan 19 2020 Richard W.M. Jones <rjones@redhat.com> - 1.8.8-13
- OCaml 4.10.0+beta1 rebuild.

* Thu Jan 09 2020 Richard W.M. Jones <rjones@redhat.com> - 1.8.8-12
- OCaml 4.09.0 for riscv64

* Fri Dec 06 2019 Richard W.M. Jones <rjones@redhat.com> - 1.8.8-11
- OCaml 4.09.0 (final) rebuild.

* Fri Aug 16 2019 Richard W.M. Jones <rjones@redhat.com> - 1.8.8-10
- OCaml 4.08.1 (final) rebuild.

* Sat Aug 10 2019 Richard W.M. Jones <rjones@redhat.com> - 1.8.8-9
- Rebuild against new ocaml-lablgtk.

* Wed Jul 31 2019 Richard W.M. Jones <rjones@redhat.com> - 1.8.8-8
- OCaml 4.08.1 (rc2) rebuild.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Richard W.M. Jones <rjones@redhat.com> - 1.8.8-4
- OCaml 4.07.0 (final) rebuild.

* Tue Jun 19 2018 Richard W.M. Jones <rjones@redhat.com> - 1.8.8-3
- OCaml 4.07.0-rc1 rebuild.

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Nov 08 2017 Richard W.M. Jones <rjones@redhat.com> - 1.8.8-1
- New upstream version 1.8.8.

* Tue Nov 07 2017 Richard W.M. Jones <rjones@redhat.com> - 1.8.7-11
- OCaml 4.06.0 rebuild.

* Mon Aug 07 2017 Richard W.M. Jones <rjones@redhat.com> - 1.8.7-10
- OCaml 4.05.0 rebuild.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.7-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 26 2017 Richard W.M. Jones <rjones@redhat.com> - 1.8.7-7
- OCaml 4.04.2 rebuild.

* Fri May 12 2017 Richard W.M. Jones <rjones@redhat.com> - 1.8.7-6
- Bump release and rebuild.

* Thu May 11 2017 Richard W.M. Jones <rjones@redhat.com> - 1.8.7-5
- OCaml 4.04.1 rebuild.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Nov 09 2016 Dan Horák <dan@danny.cz> - 1.8.7-3
- rebuild for s390x codegen bug

* Sun Nov 06 2016 Richard W.M. Jones <rjones@redhat.com> - 1.8.7-2
- Rebuild for OCaml 4.04.0.

* Sat Apr 16 2016 Jerry James <loganjerry@gmail.com> - 1.8.7-1
- New upstream release

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jul 28 2015 Richard W.M. Jones <rjones@redhat.com> - 1.8.6-5
- OCaml 4.02.3 rebuild.

* Wed Jul 22 2015 Richard W.M. Jones <rjones@redhat.com> - 1.8.6-4
- Enable bytecode builds.

* Wed Jun 24 2015 Richard W.M. Jones <rjones@redhat.com> - 1.8.6-3
- ocaml-4.02.2 final rebuild.

* Wed Jun 17 2015 Richard W.M. Jones <rjones@redhat.com> - 1.8.6-2
- ocaml-4.02.2 rebuild.

* Wed Mar 18 2015 Jerry James <loganjerry@gmail.com> - 1.8.6-1
- New upstream release
- Reenable documentation generation

* Mon Feb 16 2015 Richard W.M. Jones <rjones@redhat.com> - 1.8.5-10
- ocaml-4.02.1 rebuild.

* Thu Oct 30 2014 Jerry James <loganjerry@gmail.com> - 1.8.5-9
- Rebuild for new ocaml-lablgtk
- Fix license handling

* Sat Aug 30 2014 Richard W.M. Jones <rjones@redhat.com> - 1.8.5-8
- ocaml-4.02.0 final rebuild.

* Sat Aug 23 2014 Richard W.M. Jones <rjones@redhat.com> - 1.8.5-7
- ocaml-4.02.0+rc1 rebuild.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 01 2014 Richard W.M. Jones <rjones@redhat.com> - 1.8.5-5
- ocaml-4.02.0-0.8.git10e45753.fc22 rebuild.

* Wed Jul 23 2014 Richard W.M. Jones <rjones@redhat.com> - 1.8.5-4
- OCaml 4.02.0 beta rebuild.
- Disable documentation generation.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Apr 21 2014 Jerry James <loganjerry@gmail.com> - 1.8.5-1
- New upstream release

* Tue Apr 15 2014 Richard W.M. Jones <rjones@redhat.com> - 1.8.4-2
- Remove ocaml_arches macro (RHBZ#1087794).

* Wed Feb 26 2014 Jerry James <loganjerry@gmail.com> - 1.8.4-1
- New upstream release, 1.8.4+dev, where the "+dev" refers to a bug fix
  that was applied immediately after the 1.8.4 release
- Drop upstreamed patch
- Install graph.cmxs and enable the -debuginfo subpackage
- Update expected test results
- BR ocaml-findlib only, not ocaml-findlib-devel
- Install graph editing tools into -tools subpackage
- Fix the bytecode build

* Wed Oct 02 2013 Richard W.M. Jones <rjones@redhat.com> - 1.8.3-5
- Rebuild for ocaml-lablgtk 2.18.

* Sat Sep 14 2013 Richard W.M. Jones <rjones@redhat.com> - 1.8.3-4
- Rebuild for OCaml 4.01.0.

* Tue Aug  6 2013 Jerry James <loganjerry@gmail.com> - 1.8.3-3
- Adapt to Rawhide unversioned docdir change (bz 994002)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 14 2013 Jerry James <loganjerry@gmail.com> - 1.8.3-1
- New upstream release

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Oct 17 2012 Jerry James <loganjerry@gmail.com> - 1.8.2-2
- Rebuild for OCaml 4.00.1.

* Mon Jul 30 2012 Jerry James <loganjerry@gmail.com> - 1.8.2-1
- New upstream release

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Richard W.M. Jones <rjones@redhat.com> - 1.8.1-3
- Rebuild for OCaml 4.00.0.

* Sat Jan  7 2012 Jerry James <loganjerry@gmail.com> - 1.8.1-2
- Rebuild for OCaml 3.12.1

* Tue Oct 25 2011 Jerry James <loganjerry@gmail.com> - 1.8.1-1
- New upstream release

* Mon Jul 11 2011 Jerry James <loganjerry@gmail.com> - 1.7-1
- New upstream release
- Drop unnecessary spec file elements (BuildRoot, etc.)
- Drop dependency generation workaround for Fedora 12 and earlier
- Remove spurious executable bits on source files
- Replace the definition of __ocaml_requires_opts to "-i Sig", which removes
  the legitimate Requires: ocaml(GtkSignal), with __requires_exclude.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 21 2011 Richard W.M. Jones <rjones@redhat.com> - 1.6-2
- Ignore ocaml(Sig) symbol.

* Mon Jan 10 2011 Richard W.M. Jones <rjones@redhat.com> - 1.6-1
- New upstream version 1.6.
- Rebuild for OCaml 3.12.
- Remove obsolete patches and add patch to fix install-findlib rule.

* Wed Feb 10 2010 Alan Dunn <amdunn@gmail.com> - 1.3-3
- Include files (including .cmo files) and install more files that are
  needed by other applications (eg: Frama-C) that depend on
  ocaml-ocamlgraph
- define -> global
- Update for new dependency generator in F13

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 1.3-2
- Rebuild for OCaml 3.11.2.

* Thu Oct  8 2009 Richard W.M. Jones <rjones@redhat.com> - 1.3-1
- New upstream release 1.3.
- A slightly different viewGraph-related patch is required for this release.

* Fri Aug 07 2009 Alan Dunn <amdunn@gmail.com> - 1.1-1
- New upstream release 1.1.
- Makefile patch updated (still not incorporated upstream).

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0-5
- Rebuild for OCaml 3.11.1

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Dec  5 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0-3
- Rebuild for OCaml 3.11.0.
- Requires lablgtk2.
- Pull in gtk / libgnomecanvas too.

* Thu Nov 20 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0-1
- New upstream release 1.0.
- Patch0 removed - now upstream.
- Added a patch to fix documentation problem.
- Run tests with 'make --no-print-directory'.

* Wed Aug 13 2008 Alan Dunn <amdunn@gmail.com> 0.99c-2
- Incorporates changes suggested during review:
- License information was incorrect
- rpmlint error now properly justified

* Thu Aug 07 2008 Alan Dunn <amdunn@gmail.com> 0.99c-1
- Initial Fedora RPM release.

