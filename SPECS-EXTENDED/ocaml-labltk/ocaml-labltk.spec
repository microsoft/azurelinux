%ifarch %{ocaml_native_compiler}
%global native_compiler 1
%else
%global native_compiler 0
%endif

Name:          ocaml-labltk
Version:       8.06.5
Release:       14%{?dist}

Summary:       Tcl/Tk interface for OCaml

License:       LGPLv2+ with exceptions

Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:           https://forge.ocamlcore.org/projects/labltk/
Source0:       https://forge.ocamlcore.org/frs/download.php/1727/labltk-%{version}.tar.gz

# This adds debugging (-g) everywhere.
Patch1:        labltk-8.06.0-enable-debugging.patch
Patch2:        labltk-8.06.4-enable-more-debugging.patch

BuildRequires: ocaml
BuildRequires: tcl-devel, tk-devel


%description
labltk or mlTk is a library for interfacing OCaml with the scripting
language Tcl/Tk (all versions since 8.0.3, but no betas).


%package devel
Summary:       Tcl/Tk interface for OCaml

Requires:      %{name}%{?_isa} = %{version}-%{release}


%description devel
labltk or mlTk is a library for interfacing OCaml with the scripting
language Tcl/Tk (all versions since 8.0.3, but no betas).

This package contains the development files.


%prep
%setup -q -n labltk-%{version}

%patch1 -p1
%patch2 -p1

# Remove version control files which might get copied into documentation.
find -name .gitignore -delete

# Kill -warn-error.
find -type f | xargs sed -i -e 's/-warn-error/-w/g'

# Don't build ocamlbrowser.
mv browser browser.old
mkdir browser
echo -e 'all:\ninstall:\n' > browser/Makefile


%build
./configure

# Build does not work in parallel.
unset MAKEFLAGS

%if !%{native_compiler}
make byte
%else
make all opt \
     SHAREDCCCOMPOPTS="%{optflags} -fPIC" \
     TK_LINK="%{__global_ldflags} -ltk8.6 -ltcl8.6"
%endif


%install
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_libdir}/ocaml/labltk
mkdir -p $RPM_BUILD_ROOT%{_libdir}/ocaml/stublibs
make install \
    BINDIR=$RPM_BUILD_ROOT%{_bindir} \
    INSTALLDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml/labltk \
    STUBLIBDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml/stublibs
%if %{native_compiler}
# The *.o files are not installed by the Makefile.  AIUI
# that prevents linking with native code programs.
install -m 0644 camltk/*.o $RPM_BUILD_ROOT%{_libdir}/ocaml/labltk
%endif


%files
%doc Changes README.mlTk
%dir %{_libdir}/ocaml/labltk
%{_libdir}/ocaml/labltk/*.cmi
%{_libdir}/ocaml/labltk/*.cma
%{_libdir}/ocaml/labltk/*.cmo
%{_libdir}/ocaml/stublibs/dlllabltk.so


%files devel
%doc README.mlTk
%doc examples_camltk
%doc examples_labltk
%{_bindir}/labltk
%{_libdir}/ocaml/labltk/labltktop
%{_libdir}/ocaml/labltk/pp
%{_libdir}/ocaml/labltk/tkcompiler
%{_libdir}/ocaml/labltk/*.a
%if %{native_compiler}
%{_libdir}/ocaml/labltk/*.cmxa
%{_libdir}/ocaml/labltk/*.cmx
%{_libdir}/ocaml/labltk/*.o
%endif
%{_libdir}/ocaml/labltk/*.mli


%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 8.06.5-14
- Switching to using full number for the 'Release' tag.
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Feb 27 2020 Richard W.M. Jones <rjones@redhat.com> - 8.06.5-13.1
- OCaml 4.10.0 final (Fedora 32).

* Wed Feb 26 2020 Richard W.M. Jones <rjones@redhat.com> - 8.06.5-13
- OCaml 4.10.0 final.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 8.06.5-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jan 18 2020 Richard W.M. Jones <rjones@redhat.com> - 8.06.5-11
- OCaml 4.10.0+beta1 rebuild.

* Thu Jan 09 2020 Richard W.M. Jones <rjones@redhat.com> - 8.06.5-10
- Bump release and rebuild.

* Tue Jan 07 2020 Richard W.M. Jones <rjones@redhat.com> - 8.06.5-9
- OCaml 4.09.0 for riscv64

* Thu Dec 05 2019 Richard W.M. Jones <rjones@redhat.com> - 8.06.5-8
- Bump and rebuild for fixed ocaml(runtime) dependency.

* Thu Dec 05 2019 Richard W.M. Jones <rjones@redhat.com> - 8.06.5-7
- Bump release and rebuild.

* Thu Dec 05 2019 Richard W.M. Jones <rjones@redhat.com> - 8.06.5-6
- OCaml 4.09.0 (final) rebuild.

* Fri Aug 16 2019 Richard W.M. Jones <rjones@redhat.com> - 8.06.5-5
- OCaml 4.08.1 (final) rebuild.

* Wed Jul 31 2019 Richard W.M. Jones <rjones@redhat.com> - 8.06.5-4
- OCaml 4.08.1 (rc2) rebuild.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 8.06.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jun 27 2019 Richard W.M. Jones <rjones@redhat.com> - 8.06.5-2
- OCaml 4.08.0 (final) rebuild.

* Mon Apr 29 2019 Richard W.M. Jones <rjones@redhat.com> - 8.06.5-1
- New upstream version 8.06.5.
- Try harder to set CFLAGS and LDFLAGS.
- Don't build ocamlbrowser.
- OCaml 4.08.0 (beta 3) rebuild.

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 8.06.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 8.06.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Richard W.M. Jones <rjones@redhat.com> - 8.06.4-6
- OCaml 4.07.0 (final) rebuild.

* Tue Jun 19 2018 Richard W.M. Jones <rjones@redhat.com> - 8.06.4-5
- OCaml 4.07.0-rc1 rebuild.

* Thu Apr 26 2018 Richard W.M. Jones <rjones@redhat.com> - 8.06.4-4
- OCaml 4.07.0-beta2 rebuild.
- Kill -warn-error.

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 8.06.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Nov 07 2017 Richard W.M. Jones <rjones@redhat.com> - 8.06.4-2
- OCaml 4.06.0 rebuild.
- Add -g flag to all calls to gcc as well.

* Tue Nov 07 2017 Richard W.M. Jones <rjones@redhat.com> - 8.06.4-1
- New upstream version 8.06.4.

* Mon Aug 07 2017 Richard W.M. Jones <rjones@redhat.com> - 8.06.3-1
- New upstream version 8.06.3 (including fixes for OCaml 4.05).
- OCaml 4.05.0 rebuild.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 8.06.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 8.06.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 26 2017 Richard W.M. Jones <rjones@redhat.com> - 8.06.2-4
- OCaml 4.04.2 rebuild.

* Wed May 10 2017 Richard W.M. Jones <rjones@redhat.com> - 8.06.2-3
- Rebuild for OCaml 4.04.1.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 8.06.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Nov 04 2016 Richard W.M. Jones <rjones@redhat.com> - 8.06.2-1
- New upstream version 8.06.2.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 8.06.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jul 28 2015 Richard W.M. Jones <rjones@redhat.com> - 8.06.0-5
- OCaml 4.02.3 rebuild.

* Wed Jul 22 2015 Richard W.M. Jones <rjones@redhat.com> - 8.06.0-4
- s390x: Don't copy *.o files when building bytecode.

* Wed Jun 24 2015 Richard W.M. Jones <rjones@redhat.com> - 8.06.0-3
- ocaml-4.02.2 final rebuild.

* Wed Jun 17 2015 Richard W.M. Jones <rjones@redhat.com> - 8.06.0-2
- ocaml-4.02.2 rebuild.

* Mon Feb 16 2015 Richard W.M. Jones <rjones@redhat.com> - 8.06.0-1
- New upstream version 8.06.0.
- Big jump in upstream version numbers to match Tk versions.
- ocaml-4.02.1 rebuild.

* Sat Aug 30 2014 Richard W.M. Jones <rjones@redhat.com> - 4.02-0.7.beta1
- ocaml-4.02.0 final rebuild.

* Fri Aug 22 2014 Richard W.M. Jones <rjones@redhat.com> - 4.02-0.6.beta1
- ocaml-4.02.0+rc1 rebuild.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.02-0.5.beta1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 01 2014 Richard W.M. Jones <rjones@redhat.com> - 4.02-0.4.beta1
- ocaml-4.02.0-0.8.git10e45753.fc22 rebuild.

* Tue Jul 22 2014 Richard W.M. Jones <rjones@redhat.com> - 4.02-0.3.beta1
- OCaml 4.02.0 beta rebuild.

* Tue Jul 22 2014 Richard W.M. Jones <rjones@redhat.com> - 4.02-0.2.beta1
- Enable debugging.
- Move labltk to -devel package.
- Enable _smp_flags.

* Tue Jul 22 2014 Richard W.M. Jones <rjones@redhat.com> - 4.02-0.1.beta1
- Initial packaging of new out-of-tree ocaml-labltk.
