Name:           ocaml-stdlib-random
Version:        1.2.0
Release:        2%{?dist}
Summary:        Versioned Random module from the OCaml standard library
License:        LGPL-2.1-or-later WITH OCaml-LGPL-linking-exception
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/ocaml/stdlib-random
Source0:        %{url}/archive/%{version}/stdlib-random-%{version}.tar.gz

# OCaml packages not built on i686 since OCaml 5 / Fedora 39.
ExcludeArch:    %{ix86}

BuildRequires:  ocaml >= 5.1.1
BuildRequires:  ocaml-cppo >= 1.1.0
BuildRequires:  ocaml-dune >= 2.7

%description
The stdlib-random package provides a stable and compiler-independent
implementation of all the PRNGs used in the Random module.  Those PRNGs
are available in the various libraries:
- stdlib-random.v3: OCaml 3.07 to 3.11 PRNG
- stdlib-random.v4: OCaml 3.12 to 4.14 PRNG
- stdlib-random.v5: current OCaml 5.0 PRNG
- stdlib-random.v5o: pure OCaml version of the OCaml 5 PRNG
All those libraries can be used together and the signature of their
Random$n module has been extended to the latest signature whenever
possible.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and signature
files for developing applications that use %{name}.

%prep
%autosetup -n stdlib-random-%{version}

%build
%dune_build

%install
%dune_install

%check
%dune_check

%files -f .ofiles
%doc Changelog.md README.md
%license LICENSE

%files devel -f .ofiles-devel

%changelog
* Fri May 03 2024 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 1.2.0-2
- Initial Azure Linux import from Fedora 41 (license: MIT)
- License verified

* Sat Mar 30 2024 Jerry James <loganjerry@gmail.com> - 1.2.0-1
- Version 1.2.0

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 18 2023 Richard W.M. Jones <rjones@redhat.com> - 1.1.0-3
- OCaml 5.1.1 + s390x code gen fix for Fedora 40

* Tue Dec 12 2023 Richard W.M. Jones <rjones@redhat.com> - 1.1.0-2
- OCaml 5.1.1 rebuild for Fedora 40

* Wed Nov 22 2023 Jerry James <loganjerry@gmail.com> - 1.1.0-1
- Initial RPM (rhbz#2242905)
