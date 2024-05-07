%global srcname topkg

	
# OCaml packages not built on i686 since OCaml 5 / Fedora 39.
ExcludeArch: %{ix86}
 
%ifnarch %{ocaml_native_compiler}
%global debug_package %{nil}
%endif
 
# The topkg-care part has dependencies that themselves depend on the main
# package.  We do not build the care part for now.
%bcond_with care

Summary:        The transitory OCaml software packager
Name:           ocaml-%{srcname}
Version:        1.0.7
Release:        2%{?dist}
License:        ISC
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://erratique.ch/software/topkg/
Source0:        https://github.com/dbuenzli/topkg/archive/v%{version}/%{srcname}-%{version}.tar.gz

BuildRequires:  ocaml >= 5.1.1
BuildRequires:  ocaml-compiler-libs
BuildRequires:  ocaml-findlib >= 1.6.1
BuildRequires:  ocaml-ocamlbuild
BuildRequires:  ocaml-rpm-macros

	
%if %{with care}
BuildRequires:  ocaml-bos-devel >= 0.1.5
BuildRequires:  ocaml-cmdliner-devel >= 1.0.0
BuildRequires:  ocaml-fmt-devel
BuildRequires:  ocaml-logs-devel
BuildRequires:  ocaml-webbrowser-devel
BuildRequires:  ocaml-opam-format-devel >= 2.0.0
%endif

# This can be removed when F40 reaches EOL
Obsoletes:      ocaml-topkg-doc < 1.0.5-4
 
%global _desc %{expand:
Topkg is a packager for distributing OCaml software.  It provides an
API to describe the files a package installs in a given build
configuration and to specify information about the package's
distribution, creation and publication procedures.}
 
%description %_desc
%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
 
%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.
 
%if %{with care}
%package        care
Summary:        Command line tool for the transitory OCaml software packager
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ocaml-ocamlbuild%{?_isa}
 
%description    care %_desc
This package provides a command line tool which helps with various
aspects of a package's life cycle: creating and linting a distribution,
releasing it on the web, publishing its documentation, adding it to the
OCaml opam repository, etc.
 
%package        care-devel
Summary:        Development files for %{name}-care
Requires:       %{name}-care%{?_isa} = %{version}-%{release}
Requires:       ocaml-bos-devel%{?_isa}
Requires:       ocaml-cmdliner-devel%{?_isa}
Requires:       ocaml-fmt-devel%{?_isa}
Requires:       ocaml-logs-devel%{?_isa}
Requires:       ocaml-opam-format-devel%{?_isa}
Requires:       ocaml-webbrowser-devel%{?_isa}
 
%description    care-devel
The %{name}-care-devel package contains libraries and signature files
for developing applications that use %{name}-care.
%endif
 
%prep
%autosetup -n topkg-%{version} -p1
 
# This package can replace "watermarks" in software that it builds.  However,
# we are building from scratch, rather than using topkg to build itself, so we
# have to do the job manually.
for fil in $(find . -type f); do
  sed -e 's,%%%%NAME%%%%,topkg,' \
      -e 's,%%%%PKG_DOC%%%%,%{url}doc/,' \
      -e 's,%%%%PKG_HOMEPAGE%%%%,%{url},' \
      -e 's,%%%%VERSION%%%%,v%{version},' \
      -e 's,%%%%VERSION_NUM%%%%,%{version},' \
      -i.orig $fil
  touch -r $fil.orig $fil
  rm $fil.orig
done
 
%build
# Build the library and the tests
ocaml pkg/pkg.ml build --pkg-name topkg --tests true
 
%if %{with care}
# Build topkg-care
ocaml pkg/pkg.ml build --pkg-name topkg-care --tests true
%endif
 
%install
%ocaml_install -s
 
%if %{with care}
%check
ocaml pkg/pkg.ml test
%endif
 
%files -f .ofiles-topkg
%doc CHANGES.md README.md
%license LICENSE.md
 
%files devel -f .ofiles-topkg-devel
 
%if %{with care}
%files care -f .ofiles-care
 
%files care-devel -f .ofiles-care-devel
%endif

%changelog
* Mon May 06 2024 Mykhailo Bykhovtsev <mbykhovtsev@microsft.com> -  1.0.7-2
- Use ocaml 5.1.1 to build and update build process

* Thu Nov 02 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.0.7-1
- Auto-upgrade to 1.0.7 - Azure Linux 3.0 - package upgrades

* Thu Mar 31 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.3-4
- Cleaning-up spec. License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.3-3
- Initial CBL-Mariner import from Fedora 34 (license: MIT).

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Dec  1 2020 Jerry James <loganjerry@gmail.com> - 1.0.3-1
- Version 1.0.3

* Tue Sep 01 2020 Richard W.M. Jones <rjones@redhat.com> - 1.0.2-2
- OCaml 4.11.1 rebuild

* Tue Sep  1 2020 Jerry James <loganjerry@gmail.com> - 1.0.2-1
- Version 1.0.2

* Fri Aug 21 2020 Richard W.M. Jones <rjones@redhat.com> - 1.0.1-11
- OCaml 4.11.0 rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-10
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 05 2020 Richard W.M. Jones <rjones@redhat.com> - 1.0.1-8
- OCaml 4.11.0+dev2-2020-04-22 rebuild

* Tue Apr 21 2020 Richard W.M. Jones <rjones@redhat.com> - 1.0.1-7
- OCaml 4.11.0 pre-release attempt 2

* Fri Apr 17 2020 Richard W.M. Jones <rjones@redhat.com> - 1.0.1-6
- OCaml 4.11.0 pre-release

* Thu Apr 02 2020 Richard W.M. Jones <rjones@redhat.com> - 1.0.1-5
- Update all OCaml dependencies for RPM 4.16.

* Wed Feb 26 2020 Richard W.M. Jones <rjones@redhat.com> - 1.0.1-4
- OCaml 4.10.0 final.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jan 19 2020 Richard W.M. Jones <rjones@redhat.com> - 1.0.1-2
- OCaml 4.10.0+beta1 rebuild.

* Thu Jan  9 2020 Jerry James <loganjerry@gmail.com> - 1.0.1-1
- Initial RPM
