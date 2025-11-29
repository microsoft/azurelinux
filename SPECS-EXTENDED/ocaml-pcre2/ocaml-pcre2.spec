Name:           ocaml-pcre2
Version:        8.0.3
Release:        2%{?dist}
Summary:        OCaml bindings to the pcre2 library
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
License:        LGPL-2.1-or-later WITH OCaml-LGPL-linking-exception
URL:            https://github.com/camlp5/pcre2-ocaml
VCS:            git:%{url}.git
Source:         %{url}/archive/%{version}/pcre2-%{version}.tar.gz#/%{name}-%{version}.tar.gz

# OCaml packages not built on i686 since OCaml 5 / Fedora 39.
ExcludeArch:    %{ix86}

BuildRequires:  ocaml >= 4.08
BuildRequires:  ocaml-dune >= 2.7
BuildRequires:  ocaml-dune-configurator-devel
BuildRequires:  ocaml-ounit-devel
BuildRequires:  pkgconfig(libpcre2-8)

%description
This packages offers library functions for string pattern matching and
substitution, similar to the functionality offered by the Perl language.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pcre2-devel%{?_isa}

%description    devel
The %{name}-devel package contains libraries and signature
files for developing applications that use %{name}.

%prep
%autosetup -n pcre2-ocaml-%{version}

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

%changelog
* Fri Nov 28 2025 Aninda Pradhan <v-anipradhan@microsoft.com> - 8.0.3-2
- Initial Azure Linux import from Fedora 44 (license: MIT)
- License Verified

* Sat Feb 15 2025 Jerry James <loganjerry@gmail.com> - 8.0.3-1
- Version 8.0.3

* Wed Jan 29 2025 Jerry James <loganjerry@gmail.com> - 8.0.2-1
- OCaml 5.2.1 rebuild for Fedora 41
- Version 8.0.2

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.5.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jul 17 2024 Jerry James <loganjerry@gmail.com> - 7.5.2-9
- Add VCS field

* Wed Jun 19 2024 Richard W.M. Jones <rjones@redhat.com> - 7.5.2-8
- OCaml 5.2.0 ppc64le fix

* Wed May 29 2024 Richard W.M. Jones <rjones@redhat.com> - 7.5.2-7
- OCaml 5.2.0 for Fedora 41

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.5.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.5.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 18 2023 Richard W.M. Jones <rjones@redhat.com> - 7.5.2-4
- OCaml 5.1.1 + s390x code gen fix for Fedora 40

* Tue Dec 12 2023 Richard W.M. Jones <rjones@redhat.com> - 7.5.2-3
- OCaml 5.1.1 rebuild for Fedora 40

* Thu Oct 05 2023 Richard W.M. Jones <rjones@redhat.com> - 7.5.2-2
- OCaml 5.1 rebuild for Fedora 40

* Thu Oct 05 2023 Jerry James <loganjerry@gmail.com> - 7.5.2-1
- Initial RPM

