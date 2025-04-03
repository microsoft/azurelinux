Summary:        Combinators for binding to C libraries without writing any C
Name:           ocaml-ctypes
Version:        0.21.1
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/ocamllabs/ocaml-ctypes
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  ocaml >= 4.03.0
BuildRequires:  ocaml-bigarray-compat-devel
BuildRequires:  ocaml-dune >= 2.9
BuildRequires:  ocaml-dune-configurator-devel
BuildRequires:  ocaml-integers-devel >= 0.2.2
BuildRequires:  pkgconfig(libffi)

%if 0%{?with_check}
BuildRequires:  ocaml-bisect-ppx-devel
BuildRequires:  ocaml-lwt-devel >= 2.4.7
BuildRequires:  ocaml-ounit-devel
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(ncurses)
%endif

# This can be removed when F42 reaches EOL
Obsoletes:      %{name}-doc < 0.21.0
Provides:       %{name}-doc = %{version}-%{release}

# Do not require ocaml-compiler-libs at runtime
%global __ocaml_requires_opts -i Asttypes -i Build_path_prefix_map -i Cmi_format -i Env -i Ident -i Identifiable -i Load_path -i Location -i Longident -i Misc -i Outcometree -i Parsetree -i Path -i Primitive -i Shape -i Subst -i Toploop -i Type_immediacy -i Types -i Warnings

%description
Ctypes is a library for binding to C libraries using pure OCaml.  The
primary aim is to make writing C extensions as straightforward as
possible.

The core of ctypes is a set of combinators for describing the structure
of C types -- numeric types, arrays, pointers, structs, unions and
functions.  You can use these combinators to describe the types of the
functions that you want to call, then bind directly to those functions --
all without writing or generating any C!

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ocaml-bigarray-compat-devel%{?_isa}
Requires:       ocaml-integers-devel%{?_isa}

%description    devel
The %{name}-devel package contains libraries and signature
files for developing applications that use %{name}.

%prep
%autosetup
# Use Mariner flags
sed -i 's/ "-cclib"; "-Wl,--no-as-needed";//' src/ctypes-foreign/config/discover.ml

%build
%dune_build

%install
%dune_install

%check
%dune_check

%files -f .ofiles
%license LICENSE
%doc CHANGES.md README.md

%files devel -f .ofiles-devel

%changelog
* Tue Jun 04 2024 Andrew Phelps <anphel@microsoft.com> - 0.21.1-1
- Upgrade to version 0.21.1 based on Fedora 40 package (license: MIT)
- Remove doc subpackage

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 0.18.0-6
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Wed Jun 01 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.18.0-5
- Fixing ptests.

* Thu Mar 31 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.18.0-4
- Cleaning-up spec. License verified.

* Tue Jan 18 2022 Thomas Crain <thcrain@microsoft.com> - 0.18.0-3
- Use direct libffi-devel BR instead of pkgconfig(libffi) due to improper provides
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.18.0-2
- Initial CBL-Mariner import from Fedora 34 (license: MIT).

* Tue Feb 09 2021 Jerry James <loganjerry@gmail.com> - 0.18.0-1
- Initial package
