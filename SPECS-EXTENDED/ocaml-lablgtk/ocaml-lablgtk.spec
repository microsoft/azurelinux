# OCaml packages not built on i686 since OCaml 5 / Fedora 39.
ExcludeArch: %{ix86}

%global giturl  https://github.com/garrigue/lablgtk

Name:           ocaml-lablgtk
Version:        2.18.14
Release:        5%{?dist}

Summary:        Objective Caml interface to gtk+
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
# The project as a whole is LGPL-2.0-only.  LGPL-2.1-or-later files:
# - src/gtkSourceView2_types.mli
# - src/introspection/xml-light/* (not included in the binary RPM)
License:        LGPL-2.0-only WITH OCaml-LGPL-linking-exception AND LGPL-2.1-or-later WITH OCaml-LGPL-linking-exception

URL:            https://garrigue.github.io/lablgtk/
VCS:            git:%{giturl}.git
Source:         %{giturl}/archive/%{version}/lablgtk-%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Provide a definition of ml_rsvg_handle_new_gz for newer versions of librsvg
# which do not explicitly expose an SVGZ interface.
Patch:          %{name}-svgz.patch
# Adapt to new paths to Unix library in OCaml 5.1.0
Patch:          %{name}-unix.patch

BuildRequires:  help2man
BuildRequires:  make
BuildRequires:  ocaml >= 4.06
BuildRequires:  ocaml-camlp-streams-devel
BuildRequires:  ocaml-findlib >= 1.2.1
BuildRequires:  ocaml-ocamldoc
BuildRequires:  ocaml-rpm-macros
BuildRequires:  pkgconfig(gtk+-2.0)
BuildRequires:  pkgconfig(gtksourceview-2.0)
BuildRequires:  pkgconfig(gtkspell-2.0)
BuildRequires:  pkgconfig(libglade-2.0)
BuildRequires:  pkgconfig(libgnomecanvas-2.0)
BuildRequires:  pkgconfig(librsvg-2.0)
BuildRequires:  pkgconfig(ncurses)
BuildRequires:  pkgconfig(xmu)
BuildRequires:  pkgconfig(zlib)

%global __ocaml_requires_opts -i GtkSourceView2_types


%description
LablGTK is an Objective Caml interface to gtk+.

It uses the rich type system of Objective Caml to provide a strongly
typed, yet very comfortable, object-oriented interface to gtk+. This
is not that easy if you know the dynamic typing approach taken by
gtk+.


%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       gtk2-devel%{?_isa}

%description devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.


%prep
%autosetup -n lablgtk-%{version} -p1

# Remove spurious executable bits
chmod a-x README*

%build
# Parallel builds don't work.
unset MAKEFLAGS
%configure --without-gnomeui
sed -e "s|-O|%{build_cflags}|" \
    -e "s|-shared|& -ccopt '%{build_ldflags}'|" \
    -e "s|(CAMLMKLIB)|& -ldopt '%{build_ldflags}'|" \
    -e "s|-warn-error [-A-Za-z0-9]\+||" \
    -i src/Makefile
%ifarch %{ocaml_native_compiler}
make world CAMLOPT="ocamlopt.opt -g" CAMLC="ocamlc.opt -g"
%else
make world CAMLC="ocamlc -g"
%endif


%install
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{ocamldir}
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{ocamldir}/lablgtk2
mkdir -p $RPM_BUILD_ROOT%{ocamldir}/stublibs
make install \
     RANLIB=true \
     BINDIR=$RPM_BUILD_ROOT%{_bindir} \
     LIBDIR=$RPM_BUILD_ROOT%{_libdir} \
     INSTALLDIR=$RPM_BUILD_ROOT%{ocamldir}/lablgtk2 \
     DLLDIR=$RPM_BUILD_ROOT%{ocamldir}/stublibs
%ifarch %{ocaml_native_compiler}
cp -p META $RPM_BUILD_ROOT%{ocamldir}/lablgtk2
%else
# Do not require the native artifacts
sed -e '/native/d' \
    -e '/exists_if/s/,[[:alnum:]]*\.cmxa,[[:alnum:]]*\.cmxs//' \
    -e '/exists_if/s/,[[:alnum:]]*\.cmx//' \
    META > $RPM_BUILD_ROOT%{ocamldir}/lablgtk2/META
touch -r META $RPM_BUILD_ROOT%{ocamldir}/lablgtk2/META
%endif

# Remove ld.conf (part of main OCaml dist).
rm $RPM_BUILD_ROOT%{ocamldir}/ld.conf

# Remove unnecessary *.ml files (ones which have a *.mli).
pushd $RPM_BUILD_ROOT%{ocamldir}/lablgtk2
for f in *.ml; do \
  b=`basename $f .ml`; \
  if [ -f "$b.mli" ]; then \
    rm $f; \
  fi; \
done
popd

# Remove .cvsignore files from examples directory.
find examples -name .cvsignore -delete

# Generate man pages
export LD_LIBRARY_PATH=$PWD/src
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
cp -p src/lablgladecc src/lablgladecc2
for bin in gdk_pixbuf_mlsource lablgladecc2 lablgtk2; do
  help2man -N --version-string=%{version} src/$bin > \
    $RPM_BUILD_ROOT%{_mandir}/man1/$bin.1
done

%ocaml_files

# Move two files from the main package to the devel package
sed -i '/propcc/d;/varcc/d' .ofiles


%files -f .ofiles


%files devel -f .ofiles-devel
%doc CHANGES.API
%{ocamldir}/lablgtk2/propcc
%{ocamldir}/lablgtk2/varcc


%changelog
* Fri Nov 28 2025 Aninda Pradhan <v-anipradhan@microsoft.com> - 2.18.14-5
- Initial Azure Linux import from Fedora 44 (license: MIT)
- License Verified

* Mon Oct 13 2025 Richard W.M. Jones <rjones@redhat.com> - 2.18.14-4
- OCaml 5.4.0 rebuild

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jul 11 2025 Jerry James  <loganjerry@gmail.com> - 2.18.14-2
- Rebuild to fix OCaml dependencies

* Mon Feb  3 2025 Jerry James <loganjerry@gmail.com> - 2.18.14-1
- Version 2.18.14
- Drop upstreamed precious and ocaml5 patches

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.13-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jan  9 2025 Jerry James <loganjerry@gmail.com> - 2.18.13-15
- OCaml 5.3.0 rebuild for Fedora 42

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.13-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 19 2024 Richard W.M. Jones <rjones@redhat.com> - 2.18.13-13
- OCaml 5.2.0 ppc64le fix

* Wed May 29 2024 Richard W.M. Jones <rjones@redhat.com> - 2.18.13-12
- OCaml 5.2.0 for Fedora 41

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.13-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.13-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 18 2023 Richard W.M. Jones <rjones@redhat.com> - 2.18.13-9
- OCaml 5.1.1 + s390x code gen fix for Fedora 40

* Tue Dec 12 2023 Richard W.M. Jones <rjones@redhat.com> - 2.18.13-8
- OCaml 5.1.1 rebuild for Fedora 40

* Thu Oct 05 2023 Richard W.M. Jones <rjones@redhat.com> - 2.18.13-7
- OCaml 5.1 rebuild for Fedora 40

* Wed Oct  4 2023 Jerry James <loganjerry@gmail.com> - 2.18.13-6
- Add patch for new Unix library name in OCaml 5.1.0

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.13-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Richard W.M. Jones <rjones@redhat.com> - 2.18.13-5
- OCaml 5.0 rebuild for Fedora 39

* Mon Jul 10 2023 Jerry James <loganjerry@gmail.com> - 2.18.13-4
- Add patch for OCaml 5.0 compatibility

* Tue Jan 24 2023 Richard W.M. Jones <rjones@redhat.com> - 2.18.13-3
- Rebuild OCaml packages for F38

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Oct 12 2022 Jerry James <loganjerry@gmail.com> - 2.18.13-1
- Version 2.18.13
- Convert License tag to SPDX
- Provide a working definition of ml_rsvg_handle_new_gz
- BR ocaml-camlp-streams-devel for OCaml 5 compatibility
- Stop building in debug mode

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 20 2022 Jerry James <loganjerry@gmail.com> - 2.18.12-4
- Use new OCaml macros

* Sat Jun 18 2022 Richard W.M. Jones <rjones@redhat.com> - 2.18.12-4
- OCaml 4.14.0 rebuild

* Fri Feb 04 2022 Richard W.M. Jones <rjones@redhat.com> - 2.18.12-3
- OCaml 4.13.1 rebuild to remove package notes

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Dec 27 2021 Jerry James <loganjerry@gmail.com> - 2.18.12-1
- Version 2.18.12
- Drop upstreamed -vadjustment patch

* Mon Oct 04 2021 Richard W.M. Jones <rjones@redhat.com> - 2.18.11-9
- OCaml 4.13.1 build

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.11-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jul 19 2021 Jerry James <loganjerry@gmail.com> - 2.18.11-7
- Move META to the main package

* Tue Jun 22 2021 Jerry James <loganjerry@gmail.com> - 2.18.11-7
- Drop gnomeui support due to upcoming retirement
- Add -vadjustment patch to fix layout issue

* Mon Mar  1 10:09:47 GMT 2021 Richard W.M. Jones <rjones@redhat.com> - 2.18.11-6
- OCaml 4.12.0 build

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Sep 01 2020 Richard W.M. Jones <rjones@redhat.com> - 2.18.11-4
- OCaml 4.11.1 rebuild

* Fri Aug 21 2020 Richard W.M. Jones <rjones@redhat.com> - 2.18.11-3
- OCaml 4.11.0 rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 29 2020 Jerry James <loganjerry@gmail.com> - 2.18.11-1
- New upstream version 2.18.11
- Drop upstreamed -fno-common patch

* Mon May 04 2020 Richard W.M. Jones <rjones@redhat.com> - 2.18.10-7
- OCaml 4.11.0+dev2-2020-04-22 rebuild

* Tue Apr 21 2020 Richard W.M. Jones <rjones@redhat.com> - 2.18.10-6
- OCaml 4.11.0 pre-release attempt 2

* Fri Apr 17 2020 Richard W.M. Jones <rjones@redhat.com> - 2.18.10-5
- OCaml 4.11.0 pre-release

* Thu Apr 02 2020 Richard W.M. Jones <rjones@redhat.com> - 2.18.10-4
- Update all OCaml dependencies for RPM 4.16.

* Wed Feb 26 2020 Richard W.M. Jones <rjones@redhat.com> - 2.18.10-3
- OCaml 4.10.0 final.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 24 2020 Jerry James <loganjerry@gmail.com> - 2.18.10-1
- New upstream version 2.18.10
- Add -fno-common patch to fix build with gcc 10
- Link shared objects with RPM_OPT_FLAGS
- Use %%license macro
- Drop ancient Obsoletes/Provides; package was obsoleting itself
- Add man pages

* Mon Jan 20 2020 Richard W.M. Jones <rjones@redhat.com> - 2.18.9-1
- New upstream version 2.18.9.
- Remove patch which has equivalent fix upstream.

* Sun Jan 19 2020 Richard W.M. Jones <rjones@redhat.com> - 2.18.8-8
- OCaml 4.10.0+beta1 rebuild.

* Thu Jan 09 2020 Richard W.M. Jones <rjones@redhat.com> - 2.18.8-7
- OCaml 4.09.0 for riscv64

* Thu Dec 05 2019 Richard W.M. Jones <rjones@redhat.com> - 2.18.8-6
- OCaml 4.09.0 (final) rebuild.

* Thu Aug 29 2019 Jerry James <loganjerry@gmail.com> - 2.18.8-5
- Bring the gtksourceview2 dependency back.

* Fri Aug 16 2019 Richard W.M. Jones <rjones@redhat.com> - 2.18.8-4
- OCaml 4.08.1 (final) rebuild.

* Sat Aug 10 2019 Richard W.M. Jones <rjones@redhat.com> - 2.18.8-3
- Drop dependency on gtksourceview2.

* Wed Jul 31 2019 Richard W.M. Jones <rjones@redhat.com> - 2.18.8-2
- OCaml 4.08.1 (rc2) rebuild.

* Sat Jul 27 2019 Richard W.M. Jones <rjones@redhat.com> - 2.18.8-1
- New version 2.18.8.
- Remove BRs on camlp4 and lablgl.
- Drop HTML documentation.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Richard W.M. Jones <rjones@redhat.com> - 2.18.6-7
- OCaml 4.07.0 (final) rebuild.

* Tue Jun 19 2018 Richard W.M. Jones <rjones@redhat.com> - 2.18.6-6
- OCaml 4.07.0-rc1 rebuild.

* Tue Feb 13 2018 Richard W.M. Jones <rjones@redhat.com> - 2.18.6-5
- Remove support for GL.

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.18.6-4
- Escape macros in %%changelog

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Nov 07 2017 Richard W.M. Jones <rjones@redhat.com> - 2.18.6-2
- OCaml 4.06.0 rebuild.

* Tue Nov 07 2017 Richard W.M. Jones <rjones@redhat.com> - 2.18.6-1
- New upstream version 2.18.6.

* Mon Aug 07 2017 Richard W.M. Jones <rjones@redhat.com> - 2.18.5-9
- OCaml 4.05.0 rebuild.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 26 2017 Richard W.M. Jones <rjones@redhat.com> - 2.18.5-6
- Bump release and rebuild.

* Mon Jun 26 2017 Richard W.M. Jones <rjones@redhat.com> - 2.18.5-5
- OCaml 4.04.2 rebuild.

* Thu May 11 2017 Richard W.M. Jones <rjones@redhat.com> - 2.18.5-4
- OCaml 4.04.1 rebuild.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Nov 09 2016 Dan Horák <dan@danny.cz> - 2.18.5-2
- rebuild for s390x codegen bug

* Fri Nov 04 2016 Richard W.M. Jones <rjones@redhat.com> - 2.18.5-1
- New version 2.18.5.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jul 28 2015 Richard W.M. Jones <rjones@redhat.com> - 2.18.3-7
- OCaml 4.02.3 rebuild.

* Wed Jul 22 2015 Richard W.M. Jones <rjones@redhat.com> - 2.18.3-6
- Enable bytecode builds (patch supplied by Rafael Fonseca).

* Tue Jul 07 2015 Richard W.M. Jones <rjones@redhat.com> - 2.18.3-5
- Drop dependency on gtksourceview-devel.  See:
  https://lists.fedoraproject.org/pipermail/devel/2015-July/thread.html#212049

* Wed Jun 24 2015 Richard W.M. Jones <rjones@redhat.com> - 2.18.3-4
- ocaml-4.02.2 final rebuild.

* Wed Jun 17 2015 Richard W.M. Jones <rjones@redhat.com> - 2.18.3-3
- ocaml-4.02.2 rebuild.

* Mon Feb 16 2015 Richard W.M. Jones <rjones@redhat.com> - 2.18.3-2
- ocaml-4.02.1 rebuild.

* Wed Oct 29 2014 Richard W.M. Jones <rjones@redhat.com> - 2.18.3-1
- New upstream version 2.18.3, which corrects a bindings problem
  with OCaml 4.02.

* Sat Aug 30 2014 Richard W.M. Jones <rjones@redhat.com> - 2.18.0-8
- ocaml-4.02.0 final rebuild.

* Fri Aug 22 2014 Richard W.M. Jones <rjones@redhat.com> - 2.18.0-7
- ocaml-4.02.0+rc1 rebuild.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.18.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 01 2014 Richard W.M. Jones <rjones@redhat.com> - 2.18.0-5
- ocaml-4.02.0-0.8.git10e45753.fc22 rebuild.

* Tue Jul 22 2014 Richard W.M. Jones <rjones@redhat.com> - 2.18.0-4
- OCaml 4.02.0 beta rebuild.

* Mon Jul 14 2014 Orion Poplawski <orion@cora.nwra.com> - 2.18.0-3
- Rebuild for OCaml 4.02

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.18.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Oct  1 2013 Richard W.M. Jones <rjones@redhat.com> - 2.18.0-1
- New upstream version 2.18.0.

* Sat Sep 14 2013 Richard W.M. Jones <rjones@redhat.com> - 2.16.0-5
- Rebuild for OCaml 4.01.0.
- Enable debuginfo.
- Remove bogus (and not accepted upstream) patch.

* Sun Aug  4 2013 Richard W.M. Jones <rjones@redhat.com> - 2.16.0-4
- gnome-panel is dead, apparently.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.16.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.16.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Oct 17 2012 Richard W.M. Jones <rjones@redhat.com> - 2.16.0-2
- Clean up the spec file.
- Set OCAMLFIND_DESTDIR so the ocamlfind install works.

* Wed Oct 17 2012 Orion Poplawski <orion@cora.nwra.com> - 2.16.0-1
- Update to 2.16.0
- Rebase avoid-queue-empty-in-gtkThread patch
- Drop ocaml 4.00 patch fixed upstream, and drop autoconf rebuild
- Drop META version fix no longer needed
- Add BR ocaml-findlib

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.14.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun  8 2012 Richard W.M. Jones <rjones@redhat.com> - 2.14.2-11
- Patch for changes in ocamldoc in OCaml 4.00.0.

* Fri Jun 8 2012 Orion Poplawski <orion@cora.nwra.com> - 2.14.2-10
- Rebuild for OCaml 4.00.0.
- Updated URL.

* Sat Apr 28 2012 Richard W.M. Jones <rjones@redhat.com> - 2.14.2-9
- Bump and rebuild against new OCaml compiler in ARM.

* Fri Jan 06 2012 Richard W.M. Jones <rjones@redhat.com> - 2.14.2-8
- Rebuild for OCaml 3.12.1.

* Mon Nov  7 2011 Richard W.M. Jones <rjones@redhat.com> - 2.14.2-7
- Bump and rebuild for updated libpng 1.5.

* Wed Jul 27 2011 Richard W.M. Jones <rjones@redhat.com> - 2.14.2-6
- Add patch (sent upstream) to fix gtkThread async callbacks throwing
  Queue.Empty.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.14.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb  4 2011 Richard W.M. Jones <rjones@redhat.com> - 2.14.2-3
- Rebuild against rpm-4.9.0-0.beta1.6.fc15.  See discussion:
  http://lists.fedoraproject.org/pipermail/devel/2011-February/148398.html

* Fri Feb  4 2011 Richard W.M. Jones <rjones@redhat.com> - 2.14.2-2
- Rebuild for libpanel-applet soname bump.

* Wed Jan  5 2011 Richard W.M. Jones <rjones@redhat.com> - 2.14.2-1
- New upstream version 2.14.2.
- Remove get/set patch, fixed upstream.

* Tue Aug 24 2010 Adam Tkac <atkac redhat com> - 2.14.0-6
- fix building against new glib (#626765)

* Tue Jul 27 2010 David A. Wheeler <dwheeler@dwheeler.com> - 2.14.0-5
- Add support for gtksourceview2 (in addition to gtksourceview 1.0).

* Tue Jan  5 2010 Richard W.M. Jones <rjones@redhat.com> - 2.14.0-4
- Use upstream RPM 4.8 dependency generator.
- -devel package should depend on gtk2-devel, otherwise lablgtk programs
  cannot find libgtk-x11-2.0.so.0 when they are being built.

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 2.14.0-3
- Rebuild for OCaml 3.11.2.

* Mon Sep 28 2009 Richard W.M. Jones <rjones@redhat.com> - 2.14.0-2
- Ignore GtkSourceView2_types dependency (pure type-only *.cmi file).

* Mon Sep 28 2009 Richard W.M. Jones <rjones@redhat.com> - 2.14.0-1
- New upstream version 2.14.0.
- Patch to fix ml_panel.c is now upstream, so removed.
- New *.cmxs files (dynamically linked OCaml native code) added to
  the base package.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.12.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 2.12.0-3
- Rebuild for OCaml 3.11.1

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb  6 2009 Richard W.M. Jones <rjones@redhat.com> - 2.12.0-1
- New upstream version 2.12.0.
- Patch to include gnome-ui-init.h.
- gdk-pixbuf-mlsource was renamed gdk_pixbuf_mlsource (this will
  probably break things).

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 2.10.1-7
- Rebuild for OCaml 3.11.0+rc1.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 2.10.1-6
- Rebuild for OCaml 3.11.0

* Mon Sep 22 2008 Richard W.M. Jones <rjones@redhat.com> - 2.10.1-5
- Ignore bogus requires GtkSourceView_types.

* Thu Sep 18 2008 Richard W.M. Jones <rjones@redhat.com> - 2.10.1-4
- Add missing BR for gtksourceview-devel (rhbz#462651).

* Mon Aug 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.10.1-3
- fix license tag

* Wed Apr 23 2008 Richard W.M. Jones <rjones@redhat.com> - 2.10.1-2
- Rebuild for OCaml 3.10.2

* Mon Apr 21 2008 Richard W.M. Jones <rjones@redhat.com> - 2.10.1-0
- New upstream release 2.10.1.

* Sat Mar  1 2008 Richard W.M. Jones <rjones@redhat.com> - 2.10.0-3
- Rebuild for ppc64.

* Tue Feb 12 2008 Richard W.M. Jones <rjones@redhat.com> - 2.10.0-2
- Rebuild for OCaml 3.10.1.

* Wed Nov  7 2007 Richard W.M. Jones <rjones@redhat.com> - 2.10.0-1
- New upstream release 2.10.0.
- Fix path to Camlp4Parsers in 'make doc' rule.

* Fri Sep  7 2007 Gerard Milmeister <gemi@bluewin.ch> - 2.6.0-10.20060908cvs
- rebuild

* Thu Aug 30 2007 Gerard Milmeister <gemi@bluewin.ch> - 2.6.0-9.20060908cvs
- rebuild

* Sat Jul  7 2007 Gerard Milmeister <gemi@bluewin.ch> - 2.6.0-8.20060908cvs
- update to cvs version
- renamed package from lablgtk to ocaml-lablgtk

* Sat Dec  2 2006 Gerard Milmeister <gemi@bluewin.ch> - 2.6.0-7
- Rebuild for ocaml 3.09.3

* Tue Aug 29 2006 Gerard Milmeister <gemi@bluewin.ch> - 2.6.0-6
- added BR: ncurses-devel

* Tue Aug 29 2006 Gerard Milmeister <gemi@bluewin.ch> - 2.6.0-5
- Rebuild for FE6

* Wed May 10 2006 Gerard Milmeister <gemi@bluewin.ch> - 2.6.0-4
- rebuilt for ocaml 3.09.2
- removed unnecessary ldconfig

* Sun Feb 26 2006 Gerard Milmeister <gemi@bluewin.ch> - 2.6.0-3
- Rebuild for Fedora Extras 5

* Sun Jan  1 2006 Gerard Milmeister <gemi@bluewin.ch> - 2.6.0-1
- new version 2.6.0

* Sat Sep 10 2005 Gerard Milmeister <gemi@bluewin.ch> - 2.4.0-6
- include META file

* Sun May 22 2005 Toshio Kuratomi <toshio-iki-lounge.com> - 2.4.0-5
- Removed gnome-1.x BuildRequires
- Removed BuildRequires not explicitly mentioned in the configure script
  (These are dragged in through dependencies.)
- Fix a gcc4 error about lvalue casting.

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 2.4.0-4
- rebuild on all arches

* Fri Apr  8 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sat Feb 12 2005 Gerard Milmeister <gemi@bluewin.ch> - 0:2.4.0-2
- Remove %%{_smp_mflags} as it breaks the build

* Sat Feb 12 2005 Gerard Milmeister <gemi@bluewin.ch> - 0:2.4.0-1
- New Version 2.4.0

* Sat Nov 13 2004 Michael Schwendt <mschwendt[AT]users.sf.net> - 0:2.2.0-5
- BR gnome-panel-devel instead of gnome-panel (since FC2!)

* Wed Apr 28 2004 Gerard Milmeister <gemi@bluewin.ch> - 0:2.2.0-0.fdr.4
- Compile with debug

* Tue Dec  2 2003 Gerard Milmeister <gemi@bluewin.ch> - 0:2.2.0-0.fdr.3
- Make GL support optional using --with gl switch

* Fri Nov 28 2003 Gerard Milmeister <gemi@bluewin.ch> - 0:2.2.0-0.fdr.2
- Added dependency on libcroco
- Honor RPM_OPT_FLAGS

* Fri Oct 31 2003 Gerard Milmeister <milmei@ifi.unizh.ch> - 0:2.2.0-0.fdr.1
- First Fedora release

* Mon Oct 13 2003 Axel Thimm <Axel.Thimm@physik.fu-berlin.de>
- Update to 2.2.0.

* Sun Aug 17 2003 Axel Thimm <Axel.Thimm@physik.fu-berlin.de>
- Provide ocaml-lablgtk (reported by bishop@platypus.bc.ca).

* Wed Apr  9 2003 Axel Thimm <Axel.Thimm@physik.fu-berlin.de>
- Rebuilt for Red Hat 9.

* Tue Nov 26 2002 Axel Thimm <Axel.Thimm@physik.fu-berlin.de>
- Initial build
