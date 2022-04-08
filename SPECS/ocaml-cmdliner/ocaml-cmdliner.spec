%define libname %(echo %{name} | sed -e 's/^ocaml-//')

Summary:        Declarative definition of command line interfaces for OCaml
Name:           ocaml-cmdliner
Version:        1.0.4
Release:        20%{?dist}
License:        ISC
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/dbuenzli/cmdliner/
Source0:        https://github.com/dbuenzli/%{libname}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  make
BuildRequires:  ocaml
BuildRequires:  ocaml-findlib-devel
BuildRequires:  ocaml-ocamlbuild
BuildRequires:  ocaml-result-devel

%description
Cmdliner allows the declarative definition of command line
interfaces for OCaml.

It provides a simple and compositional mechanism to convert
command line arguments to OCaml values and pass them to your
functions. The module automatically handles syntax errors,
help messages and UNIX man page generation. It supports
programs with single or multiple commands and respects
most of the POSIX and GNU conventions.

Cmdliner has no dependencies and is distributed under
the ISC license.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%prep
%autosetup -n %{libname}-%{version}

# The makefile requires some cleanup to put things in correct place.
sed 's,/lib/,/%{_lib}/,g' -i Makefile

# Enable debuginfo generation.
sed 's/, package(result)/, package(result), debug/g' -i _tags
sed 's/ocamlbuild/ocamlbuild -lflag -g/g' -i Makefile

# Use install -p.
sed 's/INSTALL=install/INSTALL=install -p/g' -i Makefile

%build
make build-byte %{?_smp_mflags}
%ifarch %{ocaml_native_compiler}
make build-native %{?_smp_mflags}
%endif

%ifarch %{ocaml_natdynlink}
make build-native-dynlink %{?_smp_mflags}
%endif

%install
make install-common DESTDIR=%{buildroot}
make install-byte DESTDIR=%{buildroot}
%ifarch %{ocaml_native_compiler}
make install-native DESTDIR=%{buildroot}
%endif

%ifarch %{ocaml_natdynlink}
make install-native-dynlink DESTDIR=%{buildroot}
%endif

# Fix some spurious executable perms?
chmod -x %{buildroot}%{_libdir}/ocaml/%{libname}/*.cmx
chmod -x %{buildroot}%{_libdir}/ocaml/%{libname}/*.cmxa
chmod -x %{buildroot}%{_libdir}/ocaml/%{libname}/*.mli
chmod -x %{buildroot}%{_libdir}/ocaml/%{libname}/*.a
chmod -x %{buildroot}%{_libdir}/ocaml/%{libname}/META
chmod -x %{buildroot}%{_libdir}/ocaml/%{libname}/opam

%files
%license LICENSE.md
%doc README.md CHANGES.md
%{_libdir}/ocaml/%{libname}
%ifarch %{ocaml_native_compiler}
%exclude %{_libdir}/ocaml/%{libname}/*.a
%exclude %{_libdir}/ocaml/%{libname}/*.cmxa
%exclude %{_libdir}/ocaml/%{libname}/*.cmx
%endif
%exclude %{_libdir}/ocaml/%{libname}/*.mli

%files devel
%doc README.md CHANGES.md
%license LICENSE.md
%ifarch %{ocaml_native_compiler}
%{_libdir}/ocaml/%{libname}/*.a
%{_libdir}/ocaml/%{libname}/*.cmxa
%{_libdir}/ocaml/%{libname}/*.cmx
%endif
%{_libdir}/ocaml/%{libname}/*.mli

%changelog
* Thu Mar 31 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.4-20
- Cleaning-up spec. License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.4-19
- Initial CBL-Mariner import from Fedora 34 (license: MIT).

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Sep 01 2020 Richard W.M. Jones <rjones@redhat.com> - 1.0.4-17
- OCaml 4.11.1 rebuild

* Fri Aug 21 2020 Richard W.M. Jones <rjones@redhat.com> - 1.0.4-16
- OCaml 4.11.0 rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-15
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 05 2020 Richard W.M. Jones <rjones@redhat.com> - 1.0.4-13
- OCaml 4.11.0+dev2-2020-04-22 rebuild

* Tue Apr 21 2020 Richard W.M. Jones <rjones@redhat.com> - 1.0.4-12
- OCaml 4.11.0 pre-release attempt 2

* Fri Apr 17 2020 Richard W.M. Jones <rjones@redhat.com> - 1.0.4-11
- OCaml 4.11.0 pre-release

* Thu Apr 02 2020 Richard W.M. Jones <rjones@redhat.com> - 1.0.4-10
- Update all OCaml dependencies for RPM 4.16.

* Wed Feb 26 2020 Richard W.M. Jones <rjones@redhat.com> - 1.0.4-9
- OCaml 4.10.0 final.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jan 19 2020 Richard W.M. Jones <rjones@redhat.com> - 1.0.4-7
- OCaml 4.10.0+beta1 rebuild.

* Thu Jan 09 2020 Richard W.M. Jones <rjones@redhat.com> - 1.0.4-6
- OCaml 4.09.0 for riscv64

* Fri Dec 06 2019 Richard W.M. Jones <rjones@redhat.com> - 1.0.4-5
- OCaml 4.09.0 (final) rebuild.

* Fri Aug 16 2019 Richard W.M. Jones <rjones@redhat.com> - 1.0.4-4
- OCaml 4.08.1 (final) rebuild.

* Wed Jul 31 2019 Richard W.M. Jones <rjones@redhat.com> - 1.0.4-3
- OCaml 4.08.1 (rc2) rebuild.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jul 18 2019 Ben Rosser <rosser.bjr@gmail.com> - 1.0.4-1
- Update to latest upstream release, 1.0.4. (rhbz#1720606).

* Thu Jun 27 2019 Richard W.M. Jones <rjones@redhat.com> - 1.0.2-13
- OCaml 4.08.0 (final) rebuild.

* Mon Apr 29 2019 Richard W.M. Jones <rjones@redhat.com> - 1.0.2-12
- OCaml 4.08.0 (beta 3) rebuild.

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Richard W.M. Jones <rjones@redhat.com> - 1.0.2-9
- OCaml 4.07.0 (final) rebuild.

* Wed Jun 20 2018 Richard W.M. Jones <rjones@redhat.com> - 1.0.2-8
- OCaml 4.07.0-rc1 rebuild.

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Dec 02 2017 Richard W.M. Jones <rjones@redhat.com> - 1.0.2-6
- OCaml 4.06.0 rebuild.

* Sat Nov 25 2017 Ben Rosser <rosser.bjr@gmail.com> 1.0.2-5
- Added archful dependency (isa) on main package to devel package.
- Added documentation line to devel package.

* Sat Sep 02 2017 Ben Rosser <rosser.bjr@gmail.com> 1.0.2-4
- Add result dependency, now that ocaml-result is packaged.

* Tue Aug 15 2017 Ben Rosser <rosser.bjr@gmail.com> 1.0.2-3
- Fix debuginfo generation by not blindly chmod -x all the files.
- Pass -g to the link step of ocamlbuild as well as the compilation step.
- Use ocaml_natdynlink macro to determine when to compile the *.cmxs files.
- Modify the makefile to use install -p instead of just install.
- Switch License tag to the more correct ISC license.
- Added parallel build macro to make invocation.
- Made libname macro a global rather than a define.

* Fri Aug 11 2017 Ben Rosser <rosser.bjr@gmail.com> 1.0.2-2
- Attempt debuginfo generation by setting true : debug in tags file.
- Modernize ocaml packaging: use ocaml_native_compiler macro.
- Also remove old ocaml dependency generator scripts.

* Fri Aug 11 2017 Ben Rosser <rosser.bjr@gmail.com> 1.0.2-1
- Update to latest upstream release.

* Tue Aug  1 2017 Ben Rosser <rosser.bjr@gmail.com> 1.0.0-1.20170801git8c4bc23
- Initial package.
