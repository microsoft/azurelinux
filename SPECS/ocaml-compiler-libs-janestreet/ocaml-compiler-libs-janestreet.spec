%global srcname ocaml-compiler-libs

%ifarch %{ocaml_native_compiler}
%undefine _debugsource_packages
%else
%global debug_package %{nil}
%endif

Summary:        OCaml compiler libraries repackaged
Name:           %{srcname}-janestreet
Version:        0.12.4
Release:        2%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/janestreet/%{srcname}
Source0:        %{url}/archive/v%{version}/%{srcname}-%{version}.tar.gz

BuildRequires:  ocaml >= 5.1.1
BuildRequires:  ocaml-dune >= 2.8

%description
This package exposes the OCaml compiler libraries repackaged under
the toplevel names Ocaml_common, Ocaml_bytecomp, Ocaml_optcomp, etc.
 
%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
 
%description    devel
The %{name}-devel package contains libraries and
signature files for developing applications that use
%{name}.
 
%prep
%autosetup -n ocaml-compiler-libs-%{version}
 
%build
%dune_build
%install
%dune_install
%files -f .ofiles
%doc README.org
%license LICENSE.md
 
%files devel -f .ofiles-devel

%changelog
* Fri May 03 2024 Mykhailo Bykhovtsev <mbykhovtsev@microsft.com> - 0.12.4-2
- Rebuild for OCaml 5.1.1 and dune >= 2.8

* Mon Nov 06 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.12.4-1
- Auto-upgrade to 0.12.4 - Azure Linux 3.0 - package upgrades

* Thu Mar 31 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.12.3-4
- Cleaning-up spec. License verified.

* Mon Aug 09 2021 Thomas Crain <thcrain@microsoft.com> - 0.12.3-3
- Initial CBL-Mariner import from Fedora 34 (license: MIT).
- Remove test, docs circular dependencies

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Dec  7 2020 Jerry James <loganjerry@gmail.com> - 0.12.3-1
- Version 0.12.3

* Tue Sep 01 2020 Richard W.M. Jones <rjones@redhat.com> - 0.12.1-5
- OCaml 4.11.1 rebuild

* Fri Aug 21 2020 Richard W.M. Jones <rjones@redhat.com> - 0.12.1-4
- OCaml 4.11.0 rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.1-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu May  7 2020 Jerry James <loganjerry@gmail.com> - 0.12.1-1
- Initial RPM
