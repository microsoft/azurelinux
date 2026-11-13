# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global libname toml

%global commit 03e8a3ab1d4d014e63a2befe8a48e74783a81521
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           lib%{libname}
Version:        0
Release:        37.20161213git%{shortcommit}%{?dist}
Summary:        Fast C parser using Ragel to generate the state machine.

# Automatically converted from old format: BSD - review is highly recommended.
License:        LicenseRef-Callaway-BSD
URL:            https://github.com/ajwans/libtoml
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz

# https://github.com/ajwans/libtoml/pull/15
Patch0001:      0001-add-meson-buildsystem-as-experiment.patch

BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  %{_bindir}/ragel
BuildRequires:  pkgconfig(icu-uc)
BuildRequires:  pkgconfig(cunit)

%description
%{summary}.

%package devel
Summary:        Development libraries and header files for %{name}
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
%{summary}.

%prep
%autosetup -n %{name}-%{commit} -p1

%build
%set_build_flags
# Provide a declaration of asprintf in <stdio.h>.
CFLAGS="$CFLAGS -D__STDC_WANT_LIB_EXT2__"
%meson
%meson_build

%install
%meson_install

%check
%meson_test

%ldconfig_scriptlets

%files
%license LICENSE
%{_bindir}/%{libname}
%{_libdir}/%{name}.so.*

%files devel
%{_includedir}/%{libname}.h
%{_libdir}/%{name}.so

%changelog
* Wed Aug 06 2025 František Zatloukal <fzatlouk@redhat.com> - 0-37.20161213git03e8a3a
- Rebuilt for icu 77.1

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0-36.20161213git03e8a3a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jan 20 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0-35.20161213git03e8a3a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Dec 08 2024 Pete Walter <pwalter@fedoraproject.org> - 0-34.20161213git03e8a3a
- Rebuild for ICU 76

* Mon Sep 02 2024 Miroslav Suchý <msuchy@redhat.com> - 0-33.20161213git03e8a3a
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0-32.20161213git03e8a3a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 31 2024 Pete Walter <pwalter@fedoraproject.org> - 0-31.20161213git03e8a3a
- Rebuild for ICU 74

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0-30.20161213git03e8a3a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0-29.20161213git03e8a3a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0-28.20161213git03e8a3a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 František Zatloukal <fzatlouk@redhat.com> - 0-27.20161213git03e8a3a
- Rebuilt for ICU 73.2

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0-26.20161213git03e8a3a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Dec 31 2022 Pete Walter <pwalter@fedoraproject.org> - 0-25.20161213git03e8a3a
- Rebuild for ICU 72

* Wed Dec 07 2022 Florian Weimer <fweimer@redhat.com> - 0-24.20161213git03e8a3a
- Arrange for asprintf declaration in <stdio.h> for C99 compatibility

* Mon Aug 01 2022 Frantisek Zatloukal <fzatlouk@redhat.com> - 0-23.20161213git03e8a3a
- Rebuilt for ICU 71.1

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0-22.20161213git03e8a3a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0-21.20161213git03e8a3a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0-20.20161213git03e8a3a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu May 20 2021 Pete Walter <pwalter@fedoraproject.org> - 0-19.20161213git03e8a3a
- Rebuild for ICU 69

* Wed May 19 2021 Pete Walter <pwalter@fedoraproject.org> - 0-18.20161213git03e8a3a
- Rebuild for ICU 69

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0-17.20161213git03e8a3a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0-16.20161213git03e8a3a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri May 15 2020 Pete Walter <pwalter@fedoraproject.org> - 0-15.20161213git03e8a3a
- Rebuild for ICU 67

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0-14.20161213git03e8a3a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Nov 01 2019 Pete Walter <pwalter@fedoraproject.org> - 0-13.20161213git03e8a3a
- Rebuild for ICU 65

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0-12.20161213git03e8a3a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0-11.20161213git03e8a3a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 23 2019 Pete Walter <pwalter@fedoraproject.org> - 0-10.20161213git03e8a3a
- Rebuild for ICU 63

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0-9.20161213git03e8a3a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Pete Walter <pwalter@fedoraproject.org> - 0-8.20161213git03e8a3a
- Rebuild for ICU 62

* Mon Apr 30 2018 Pete Walter <pwalter@fedoraproject.org> - 0-7.20161213git03e8a3a
- Rebuild for ICU 61.1

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0-6.20161213git03e8a3a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Nov 30 2017 Pete Walter <pwalter@fedoraproject.org> - 0-5.20161213git03e8a3a
- Rebuild for ICU 60.1

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0-4.20161213git03e8a3a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0-3.20161213git03e8a3a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0-2.20161213git03e8a3a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec 13 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0-1.20161213git03e8a3a
- Initial package
