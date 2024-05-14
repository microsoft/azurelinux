# TESTING NOTE: The ppx_jane module is needed to run the tests.  However,
# ppx_jane transitively requires this module.  Therefore, we cannot run the
# tests at all until we are able to add ppx_jane.
%global srcname base

Summary:        Jane Street standard library for OCaml
Name:           ocaml-%{srcname}
Version:        0.16.3
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://opensource.janestreet.com/base/
Source0:        https://github.com/janestreet/%{srcname}/archive/v%{version}/%{srcname}-%{version}.tar.gz
# Expose a dependency on the math library so RPM can see it
Patch0:         %{name}-mathlib.patch

BuildRequires:  ocaml >= 5.1.1
BuildRequires:  ocaml-dune >= 2.0.0
BuildRequires:  ocaml-dune-configurator-devel
BuildRequires:  ocaml-sexplib0-devel >= 0.16

%if %{with_check}
BuildRequires:  ocaml-num-devel
BuildRequires:  ocaml-ppx-jane-devel
BuildRequires:  ocaml-sexplib-devel
BuildRequires:  ocaml-stdio-devel
BuildRequires:  ocaml-uutf-devel
%endif

%description
Base is a standard library for OCaml.  It provides a standard set of
general purpose modules that are well-tested, performant, and
fully-portable across any environment that can run OCaml code.  Unlike
other standard library projects, Base is meant to be used as a wholesale
replacement of the standard library distributed with the OCaml compiler.
In particular it makes different choices and doesn't re-export features
that are not fully portable such as I/O, which are left to other
libraries.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ocaml-sexplib0-devel%{?_isa}

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%prep
%autosetup -n %{srcname}-%{version} -p1

%build
%dune_build

%install
%dune_install

%if %{with_check}
%check
%dune_check
%endif

%files -f .ofiles
%doc CHANGES.md README.org ROADMAP.md
%license LICENSE.md

%files devel -f .ofiles-devel

%changelog
* Wed May 01 2024 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 0.16.3-1
- Converted spec file to match with Fedora 41.
- Upgrade to 0.16.3

* Thu Mar 31 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.15.0-2
- Cleaning-up spec. License verified.

* Tue Jan 18 2022 Thomas Crain <thcrain@microsoft.com> - 0.15.0-1
- Upgrade to latest upstream version
- Add patch for OCaml 4.13.0 compatibility
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.14.1-2
- Initial CBL-Mariner import from Fedora 34 (license: MIT).

* Sat Feb 20 2021 Jerry James <loganjerry@gmail.com> - 0.14.1-1
- Version 0.14.1

* Tue Feb  2 2021 Richard W.M. Jones <rjones@redhat.com> - 0.14.0-6
- Bump and rebuild for updated ocaml-camomile dep (RHBZ#1923853).

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Sep 01 2020 Richard W.M. Jones <rjones@redhat.com> - 0.14.0-4
- OCaml 4.11.1 rebuild

* Fri Aug 21 2020 Richard W.M. Jones <rjones@redhat.com> - 0.14.0-3
- OCaml 4.11.0 rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jun 17 2020 Jerry James <loganjerry@gmail.com> - 0.14.0-1
- Version 0.14.0

* Tue May 12 2020 Jerry James <loganjerry@gmail.com> - 0.13.2-1
- Version 0.13.2

* Mon May 04 2020 Richard W.M. Jones <rjones@redhat.com> - 0.13.1-5
- OCaml 4.11.0+dev2-2020-04-22 rebuild

* Tue Apr 21 2020 Richard W.M. Jones <rjones@redhat.com> - 0.13.1-4
- OCaml 4.11.0 pre-release attempt 2

* Fri Apr 03 2020 Richard W.M. Jones <rjones@redhat.com> - 0.13.1-3
- Update all OCaml dependencies for RPM 4.16.

* Wed Feb 26 2020 Richard W.M. Jones <rjones@redhat.com> - 0.13.1-2
- OCaml 4.10.0 final.

* Tue Feb 18 2020 Jerry James <loganjerry@gmail.com> - 0.13.1-1
- Version 0.13.1
- Drop upstreamed -gc patch

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jan 22 2020 Jerry James <loganjerry@gmail.com> - 0.13.0-3
- Add -gc patch to fix FTBFS with OCaml 4.10

* Sun Jan 19 2020 Richard W.M. Jones <rjones@redhat.com> - 0.13.0-3
- OCaml 4.10.0+beta1 rebuild.

* Wed Jan 15 2020 Jerry James <loganjerry@gmail.com> - 0.13.0-2
- Add R on ocaml-sexplib0-devel to the -devel subpackage
- Pass smp_mflags to dune build

* Thu Jan  2 2020 Jerry James <loganjerry@gmail.com> - 0.13.0-1
- Initial RPM
