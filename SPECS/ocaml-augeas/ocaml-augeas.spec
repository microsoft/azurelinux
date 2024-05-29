# OCaml packages not built on i686 since OCaml 5 / Fedora 39.
ExcludeArch: %{ix86}
%global srcname augeas

Summary:        OCaml bindings for Augeas configuration API
Name:           ocaml-%{srcname}
Version:        0.6
Release:        33%{?dist}
License:        LGPL-2.1-or-later WITH OCaml-LGPL-linking-exception
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://people.redhat.com/~rjones/augeas/files/
Source0:        https://people.redhat.com/~rjones/%{srcname}/files/%{name}-%{version}.tar.gz
# Upstream patch to enable debuginfo.
Patch1:         0001-Use-ocamlopt-g-option.patch
# Const-correctness fix for OCaml 4.09+
Patch2:         0002-caml_named_value-returns-const-value-pointer-in-OCam.patch

BuildRequires:  make
BuildRequires:  ocaml >= 5.1.1
BuildRequires:  ocaml-findlib
BuildRequires:  ocaml-ocamldoc
BuildRequires:  ocaml-rpm-macros
BuildRequires:  augeas-devel >= 0.1.0

%description
Augeas is a unified system for editing arbitrary configuration
files. This provides complete OCaml bindings for Augeas.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%prep
%autosetup -p1

# Pass -g to ocamlmklib
sed -i 's/ocamlmklib/& -g/' Makefile.in

%build
%configure
%ifarch %{ocaml_native_compiler}
make
%else
make mlaugeas.cma test_augeas
%endif
make doc

%check
make check

%install
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs

# The upstream 'make install' rule is missing '*.so' and distributes
# '*.cmi' instead of just the augeas.cmi file.  Temporary fix:
#make install
%ifarch %{ocaml_native_compiler}
ocamlfind install augeas META *.mli *.cmx *.cma *.cmxa *.a augeas.cmi *.so
%else
ocamlfind install augeas META *.mli *.cma *.a augeas.cmi *.so
%endif

%ocaml_files


%files -f .ofiles
%license COPYING.LIB


%files devel -f .ofiles-devel
%doc html

%changelog
* Wed May 01 2024 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 0.6-33
- Converted spec file to match with Fedora 41.
- Removing embedded macros file in favor of using one provided by the ocaml-rpm-macros package.

* Fri Mar 29 2024 Betty Lakes <bettylakes@microsoft.com> - 0.6-32
- Cleaning-up spec. License verified.
- Initial Azure Linux import from Fedora 40 (license: MIT).

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.6-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild
