# OCaml packages not built on i686 since OCaml 5 / Fedora 39.
ExcludeArch: %{ix86}

%global giturl  https://github.com/realworldocaml/mdx

Name:           ocaml-mdx
Version:        2.5.1
Release:        3%{?dist}
Summary:        Executable code blocks inside markdown files
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
License:        ISC
URL:            https://realworldocaml.github.io/mdx/
VCS:            git:%{giturl}.git
Source:         %{giturl}/releases/download/%{version}/mdx-%{version}.tbz#/%{name}-%{version}.tbz

BuildRequires:  ocaml >= 4.08.0
BuildRequires:  ocaml-alcotest-devel
BuildRequires:  ocaml-astring-devel
BuildRequires:  ocaml-camlp-streams-devel
BuildRequires:  ocaml-cmdliner-devel >= 1.1.0
BuildRequires:  ocaml-cppo >= 1.1.0
BuildRequires:  ocaml-csexp-devel >= 1.3.2
BuildRequires:  ocaml-dune >= 3.5
BuildRequires:  ocaml-findlib
BuildRequires:  ocaml-fmt-devel >= 0.8.7
BuildRequires:  ocaml-logs-devel >= 0.7.0
BuildRequires:  ocaml-lwt-devel
BuildRequires:  ocaml-re-devel >= 1.7.2
BuildRequires:  ocaml-result-devel >= 1.5
BuildRequires:  ocaml-version-devel >= 2.3.0

# odoc-parser has been merged back into odoc
# This package now vendors odoc-parser
Provides:       bundled(ocaml-odoc-parser) = 2.3.0

%description
mdx enables execution of code blocks inside markdown files.  There are
(currently) two sub-commands, corresponding to two modes of operation:
preprocessing (`ocaml-mdx pp`) and tests (`ocaml-mdx test`).

The preprocessor mode enables mixing documentation and code, and the
practice of "literate programming" using markdown and OCaml.

The test mode enables ensuring that shell scripts and OCaml fragments in
the documentation always stay up-to-date.

The blocks in markdown files can be parameterized by `mdx`-specific
labels, that will change the way `mdx` interprets the block.  The syntax
is: `<!-- $MDX labels -->`, where `labels` is a list of valid labels
separated by a comma.  This line must immediately precede the block it
is attached to.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ocaml-astring-devel%{?_isa}
Requires:       ocaml-camlp-streams-devel%{?_isa}
Requires:       ocaml-csexp-devel%{?_isa}
Requires:       ocaml-fmt-devel%{?_isa}
Requires:       ocaml-logs-devel%{?_isa}
Requires:       ocaml-re-devel%{?_isa}
Requires:       ocaml-result-devel%{?_isa}
Requires:       ocaml-version-devel%{?_isa}

%description    devel
The %{name}-devel package contains libraries and signature
files for developing applications that use %{name}.

%prep
%autosetup -n mdx-%{version} -p1

%build
%dune_build

%install
%dune_install

%check
%dune_check

%files -f .ofiles
%doc CHANGES.md README.md
%license LICENSE.md

%files devel -f .ofiles-devel

%changelog
* Fri Nov 28 2025 Aninda Pradhan <v-anipradhan@microsoft.com> - 2.5.1-3
- Initial Azure Linux import from Fedora 44 (license: MIT)
- License Verified

* Tue Oct 14 2025 Richard W.M. Jones <rjones@redhat.com> - 2.5.1-2
- OCaml 5.4.0 rebuild

* Mon Oct 13 2025 Richard W.M. Jones <rjones@redhat.com> - 2.5.1-1
- New upstream version 2.5.1 (RHBZ#2402582)

* Mon Aug 25 2025 Jerry James <loganjerry@gmail.com> - 2.5.0-7
- Rebuild for ocaml-fmt 0.11.0

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jul 12 2025 Jerry James  <loganjerry@gmail.com> - 2.5.0-5
- Rebuild to fix OCaml dependencies

* Tue Mar 18 2025 Jerry James <loganjerry@gmail.com> - 2.5.0-4
- Rebuild for ocaml-logs 0.8.0

* Mon Mar 10 2025 Jerry James <loganjerry@gmail.com> - 2.5.0-3
- Rebuild for ocaml-fmt 0.10.0

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jan  9 2025 Jerry James <loganjerry@gmail.com> - 2.5.0-1
- OCaml 5.3.0 rebuild for Fedora 42
- Version 2.5.0

* Tue Oct 08 2024 Richard W.M. Jones <rjones@redhat.com> - 2.4.1-7
- Rebuild for ocaml-lwt 5.8.0

* Sun Oct  6 2024 Jerry James <loganjerry@gmail.com> - 2.4.1-6
- Rebuild for ocaml-re 1.13.3 and ocaml-version 3.6.9

* Thu Sep 26 2024 Jerry James <loganjerry@gmail.com> - 2.4.1-5
- Rebuild for ocaml-version 3.6.8

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 19 2024 Richard W.M. Jones <rjones@redhat.com> - 2.4.1-3
- OCaml 5.2.0 ppc64le fix

* Thu May 30 2024 Richard W.M. Jones <rjones@redhat.com> - 2.4.1-2
- OCaml 5.2.0 for Fedora 41

* Thu Mar 14 2024 Jerry James <loganjerry@gmail.com> - 2.4.1-1
- Version 2.4.1

* Fri Feb 23 2024 Jerry James <loganjerry@gmail.com> - 2.4.0-1
- Version 2.4.0

* Fri Feb  2 2024 Jerry James <loganjerry@gmail.com> - 2.3.1-8
- Rebuild for changed ocamlx hashes

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 18 2023 Richard W.M. Jones <rjones@redhat.com> - 2.3.1-5
- Bump release and rebuild

* Mon Dec 18 2023 Richard W.M. Jones <rjones@redhat.com> - 2.3.1-4
- OCaml 5.1.1 + s390x code gen fix for Fedora 40

* Tue Dec 12 2023 Richard W.M. Jones <rjones@redhat.com> - 2.3.1-3
- OCaml 5.1.1 rebuild for Fedora 40

* Thu Oct 05 2023 Richard W.M. Jones <rjones@redhat.com> - 2.3.1-2
- OCaml 5.1 rebuild for Fedora 40

* Wed Oct  4 2023 Jerry James <loganjerry@gmail.com> - 2.3.1-1
- Version 2.3.1
- Drop dependency on ocaml-odoc-parser

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 12 2023 Richard W.M. Jones <rjones@redhat.com> - 2.3.0-3
- OCaml 5.0 rebuild for Fedora 39

* Mon Jul 10 2023 Jerry James <loganjerry@gmail.com> - 2.3.0-2
- OCaml 5.0.0 rebuild

* Fri Apr 28 2023 Jerry James <loganjerry@gmail.com> - 2.3.0-1
- Version 2.3.0

* Fri Mar 24 2023 Jerry James <loganjerry@gmail.com> - 2.2.1-3
- Rebuild for ocaml-csexp 1.5.2

* Tue Mar 21 2023 Jerry James <loganjerry@gmail.com> - 2.2.1-2
- Rebuild for ocaml-version 3.6.1
- Re-enable debuginfo now that dune is fixed

* Wed Jan 25 2023 Jerry James <loganjerry@gmail.com> - 2.2.1-1
- Version 2.2.1

* Tue Jan 24 2023 Richard W.M. Jones <rjones@redhat.com> - 2.2.0-4
- Rebuild OCaml packages for F38

* Fri Jan 20 2023 Jerry James <loganjerry@gmail.com> - 2.2.0-3
- Rebuild for ocaml-version 3.6.0

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan  9 2023 Jerry James <loganjerry@gmail.com> - 2.2.0-1
- Version 2.2.0
- Drop cmdliner patch

* Tue Sep 20 2022 Jerry James <loganjerry@gmail.com> - 2.1.0-7
- Add patch to adapt tests to cmdliner 1.1.0

* Tue Aug  2 2022 Jerry James <loganjerry@gmail.com> - 2.1.0-6
- Rebuild for ocaml-odoc-parser 2.0.0

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul  8 2022 Jerry James <loganjerry@gmail.com> - 2.1.0-4
- Rebuild for ocaml-version 3.5.0
- Use new OCaml macros

* Sun Jun 19 2022 Richard W.M. Jones <rjones@redhat.com> - 2.1.0-3
- OCaml 4.14.0 rebuild

* Fri Feb 04 2022 Richard W.M. Jones <rjones@redhat.com> - 2.1.0-2
- OCaml 4.13.1 rebuild to remove package notes

* Thu Feb  3 2022 Jerry James <loganjerry@gmail.com> - 2.1.0-1
- Version 2.1.0

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Dec 31 2021 Jerry James <loganjerry@gmail.com> - 2.0.0-1
- Initial RPM
