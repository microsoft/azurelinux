%ifnarch %{ocaml_native_compiler}
%global debug_package %{nil}
%endif

Summary:        Build tool for OCaml libraries and programs
Name:           ocaml-ocamlbuild
Version:        0.14.2
Release:        1%{?dist}
License:        GPLv2 WITH exceptions
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/ocaml/ocamlbuild
Source0:        https://github.com/ocaml/ocamlbuild/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  ocaml >= 4.04.0

%description
OCamlbuild is a build tool for building OCaml libraries and programs.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains development files for %{name}.

%package doc
Summary:        Documentation for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description doc
This package contains the manual for %{name}.

%prep
%setup -q -n ocamlbuild-%{version}


%build
make configure \
  OCAMLBUILD_PREFIX=%{_prefix} \
  OCAMLBUILD_BINDIR=%{_bindir} \
  OCAMLBUILD_LIBDIR=%{_libdir}/ocaml \
%ifarch %{ocaml_native_compiler}
  OCAML_NATIVE=true
%else
  OCAML_NATIVE=false
%endif

# Parallel builds fail.
make \
%ifarch %{ocaml_native_compiler}
     OCAMLC="ocamlc.opt -g" \
     OCAMLOPT="ocamlopt.opt -g"
%else
     OCAMLC="ocamlc -g" \
     OCAMLOPT="ocamlopt -g"
%endif


%install
make install \
     DESTDIR=%{buildroot} \
     CHECK_IF_PREINSTALLED=false

# The install copies ocamlbuild & ocamlbuild.{byte or native}.
# Symlink them instead.
pushd %{buildroot}%{_bindir}
%ifarch %{ocaml_native_compiler}
ln -sf ocamlbuild.native ocamlbuild
%else
ln -sf ocamlbuild.byte ocamlbuild
%endif
popd

# Install the man page, which for some reason is not copied
# in by the make install rule above.
mkdir -p %{buildroot}%{_mandir}/man1/
install -p -m 0644 man/ocamlbuild.1 %{buildroot}%{_mandir}/man1/

# Remove the META file.  It will be replaced by ocaml-ocamlfind (findlib).
rm %{buildroot}%{_libdir}/ocaml/ocamlbuild/META

%files
%doc Changes Readme.md VERSION
%license LICENSE
%{_bindir}/ocamlbuild
%{_bindir}/ocamlbuild.byte
%ifarch %{ocaml_native_compiler}
%{_bindir}/ocamlbuild.native
%endif
%{_mandir}/man1/ocamlbuild.1*
%{_libdir}/ocaml/ocamlbuild
%ifarch %{ocaml_native_compiler}
%exclude %{_libdir}/ocaml/ocamlbuild/*.a
%exclude %{_libdir}/ocaml/ocamlbuild/*.o
%exclude %{_libdir}/ocaml/ocamlbuild/*.cmx
%exclude %{_libdir}/ocaml/ocamlbuild/*.cmxa
%endif
%exclude %{_libdir}/ocaml/ocamlbuild/*.mli

%files devel
%license LICENSE
%ifarch %{ocaml_native_compiler}
%{_libdir}/ocaml/ocamlbuild/*.a
%{_libdir}/ocaml/ocamlbuild/*.o
%{_libdir}/ocaml/ocamlbuild/*.cmx
%{_libdir}/ocaml/ocamlbuild/*.cmxa
%endif
%{_libdir}/ocaml/ocamlbuild/*.mli

%files doc
%license LICENSE
%doc manual/*

%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.14.2-1
- Auto-upgrade to 0.14.2 - Azure Linux 3.0 - package upgrades

* Tue Mar 29 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.14.0-15
- License verified.

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.14.0-14
- Switching to using full number for the 'Release' tag.
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Feb 27 2020 Richard W.M. Jones <rjones@redhat.com> - 0.14.0-13.1
- OCaml 4.10.0 final (Fedora 32).

* Wed Feb 26 2020 Richard W.M. Jones <rjones@redhat.com> - 0.14.0-13
- OCaml 4.10.0 final.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jan 18 2020 Richard W.M. Jones <rjones@redhat.com> - 0.14.0-11
- OCaml 4.10.0+beta1 rebuild.

* Thu Jan 09 2020 Richard W.M. Jones <rjones@redhat.com> - 0.14.0-10
- Bump release and rebuild.

* Wed Jan 08 2020 Richard W.M. Jones <rjones@redhat.com> - 0.14.0-9
- Bump and rebuild.

* Tue Jan 07 2020 Richard W.M. Jones <rjones@redhat.com> - 0.14.0-8
- OCaml 4.09.0 for riscv64

* Thu Dec 05 2019 Richard W.M. Jones <rjones@redhat.com> - 0.14.0-7
- Bump and rebuild for fixed ocaml(runtime) dependency.

* Thu Dec 05 2019 Richard W.M. Jones <rjones@redhat.com> - 0.14.0-6
- OCaml 4.09.0 (final) rebuild.

* Fri Aug 16 2019 Richard W.M. Jones <rjones@redhat.com> - 0.14.0-5
- OCaml 4.08.1 (final) rebuild.

* Wed Jul 31 2019 Richard W.M. Jones <rjones@redhat.com> - 0.14.0-4
- OCaml 4.08.1 (rc2) rebuild.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jun 27 2019 Richard W.M. Jones <rjones@redhat.com> - 0.14.0-2
- OCaml 4.08.0 (final) rebuild.

* Mon Apr 29 2019 Richard W.M. Jones <rjones@redhat.com> - 0.14.0-1
- New upstream version 0.14.0.
- OCaml 4.08.0 (beta 3) rebuild.
- Remove the source tarball which was accidentally added to git.

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Richard W.M. Jones <rjones@redhat.com> - 0.12.0-5
- OCaml 4.07.0 (final) rebuild.

* Tue Jun 19 2018 Richard W.M. Jones <rjones@redhat.com> - 0.12.0-4
- OCaml 4.07.0-rc1 rebuild.

* Thu Apr 26 2018 Richard W.M. Jones <rjones@redhat.com> - 0.12.0-3
- OCaml 4.07.0-beta2 rebuild.

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Dec 12 2017 Richard W.M. Jones <rjones@redhat.com> - 0.12.0-1
- New upstream version 0.12.0.

* Tue Nov 07 2017 Richard W.M. Jones <rjones@redhat.com> - 0.11.0-11
- Bump release and rebuild.

* Tue Nov 07 2017 Richard W.M. Jones <rjones@redhat.com> - 0.11.0-10
- OCaml 4.06.0 rebuild.

* Mon Aug 07 2017 Richard W.M. Jones <rjones@redhat.com> - 0.11.0-9
- Bump and rebuild.

* Mon Aug 07 2017 Richard W.M. Jones <rjones@redhat.com> - 0.11.0-8
- Bump and rebuild.

* Mon Aug 07 2017 Richard W.M. Jones <rjones@redhat.com> - 0.11.0-7
- OCaml 4.05.0 rebuild.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Mon Jul 31 2017 Richard W.M. Jones <rjones@redhat.com> - 0.11.0-5
- Enable debug symbols (-g).

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 26 2017 Richard W.M. Jones <rjones@redhat.com> - 0.11.0-3
- OCaml 4.04.2 rebuild.

* Thu May 11 2017 Richard W.M. Jones <rjones@redhat.com> - 0.11.0-2
- OCaml 4.04.1 rebuild.

* Wed May 10 2017 Richard W.M. Jones <rjones@redhat.com> - 0.11.0-1
- New upstream version 0.11.0.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Nov 04 2016 Richard W.M. Jones <rjones@redhat.com> - 0.9.3-5
- New package, ocamlbuild used to be part of ocaml.
