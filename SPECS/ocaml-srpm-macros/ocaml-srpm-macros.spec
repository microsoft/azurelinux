# OCaml has a bytecode backend that works on anything with a C
# compiler, and a native code backend available on a subset of
# architectures.  A further subset of architectures support native
# dynamic linking.
#
# This package contains a file needed to define some RPM macros
# which are required before any SRPM is built.
#
# See also: https://bugzilla.redhat.com/show_bug.cgi?id=1087794
Summary:        OCaml architecture macros
Name:           ocaml-srpm-macros
Version:        9
Release:        3%{?dist}
License:        GPL-2.0-or-later
# NB. This package MUST NOT Require anything (except for dependencies
# that RPM itself generates).
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        macros.ocaml-srpm
BuildArch:      noarch

%description
This package contains macros needed by RPM in order to build
SRPMS.  It does not pull in any other OCaml dependencies.


%prep


%build


%install
mkdir -p %{buildroot}%{rpmmacrodir}
install -m 0644 %{SOURCE0} %{buildroot}%{rpmmacrodir}/macros.ocaml-srpm


%files
%{rpmmacrodir}/macros.ocaml-srpm

%changelog
* Tue May 14 2024 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 9-3
- Initial Azure Linux import from Fedora 41 (license: MIT)
- License verified

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Oct  4 2023 Jerry James <loganjerry@gmail.com> - 9-1
- Update OCaml native arches for OCaml 5.1
- Remove the Python file and some macros (now in ocaml-rpm-macros)
- Add %%ocaml_pkg macro for common declarations

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jul 10 2023 Richard W.M. Jones <rjones@redhat.com> - 8-1
- Update OCaml native archs for OCaml 5.0

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Feb 16 2022 Jerry James <loganjerry@gmail.com> - 7-1
- Add odoc and dune macros
- Add ocaml_files.py to support %%files automation
- Use %%rpmmacrodir instead of a custom macro

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Dec 06 2019 Richard W.M. Jones <rjones@redhat.com> - 6-1
- Remove support for native profiling, see:
  https://github.com/ocaml/ocaml/pull/2314

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Aug 08 2017 Richard W.M. Jones <rjones@redhat.com> - 5-2
- Bump and rebuild.

* Tue Aug  8 2017 Richard W.M. Jones <rjones@redhat.com> - 5-1
- Add new macro ocaml_native_profiling.

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Nov  8 2016 Richard W.M. Jones <rjones@redhat.com> - 4-1
- s390x is now a native architecture with OCaml 4.04 in Fedora >= 26.
- Add riscv64 as a native arch using out of tree backend.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May  2 2014 Richard W.M. Jones <rjones@redhat.com> - 2-1
- Move macros to _rpmconfigdir (RHBZ#1093528).

* Tue Apr 22 2014 Richard W.M. Jones <rjones@redhat.com> - 1-1
- New package.
