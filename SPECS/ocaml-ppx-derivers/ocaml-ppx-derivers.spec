Summary:        Deriving plugin registry
Name:           ocaml-ppx-derivers
Version:        1.2.1
Release:        20%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/ocaml-ppx/ppx_derivers
Source0:        https://github.com/ocaml-ppx/ppx_derivers/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  ocaml
BuildRequires:  ocaml-dune

%description
Ppx_derivers is a tiny package whose sole purpose is to allow
ppx_deriving and ppx_type_conv to inter-operate gracefully when
linked as part of the same ocaml-migrate-parsetree driver.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}


%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.


%prep
%autosetup -n ppx_derivers-%{version}


%build
%dune_build


%install
%dune_install


%check
%dune_check


%files -f .ofiles
%doc README.md CHANGES.md
%license LICENSE.md


%files devel -f .ofiles-devel
%doc README.md CHANGES.md
%license LICENSE.md

%changelog
* Wed May 01 2024 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 1.2.1-20
- Removing not needed build requirement and updating the build process

* Thu Mar 31 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.2.1-19
- Cleaning-up spec. License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.2.1-18
- Initial CBL-Mariner import from Fedora 34 (license: MIT).

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Sep 01 2020 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-16
- OCaml 4.11.1 rebuild

* Fri Aug 21 2020 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-15
- OCaml 4.11.0 rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-14
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon May 04 2020 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-12
- OCaml 4.11.0+dev2-2020-04-22 rebuild

* Tue Apr 21 2020 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-11
- OCaml 4.11.0 pre-release attempt 2

* Fri Apr 03 2020 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-10
- Update all OCaml dependencies for RPM 4.16.

* Wed Feb 26 2020 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-9
- OCaml 4.10.0 final.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jan 19 2020 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-7
- OCaml 4.10.0+beta1 rebuild.

* Thu Dec 19 2019 Andy Li <andy@onthewings.net> - 1.2.1-6
- Rebuild against the latest OCaml.
- Remove unneeded BuildRequires on opam-installer.

* Fri Aug 16 2019 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-5
- OCaml 4.08.1 (final) rebuild.

* Thu Aug 01 2019 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-4
- OCaml 4.08.1 (rc2) rebuild.

* Sat Jul 27 2019 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-3
- Bump and rebuild.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 16 2019 Andy Li <andy@onthewings.net> - 1.2.1-1
- Initial RPM release.
