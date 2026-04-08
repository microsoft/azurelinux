# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%undefine __cmake_in_source_build
%global sover 0.5

Name:           lpcnetfreedv
Version:        0.5
Release:        9%{?dist}
Summary:        LPCNet for FreeDV

# Automatically converted from old format: BSD - review is highly recommended.
License:        LicenseRef-Callaway-BSD
URL:            https://github.com/drowe67/LPCNet
Source0:        https://github.com/drowe67/LPCNet/archive/v%{version}/LPCNet-%{version}.tar.gz
Source1:        http://rowetel.com/downloads/deep/lpcnet_191005_v1.0.tgz

Patch0:         lpcnetfreedv-libm.patch

BuildRequires:  cmake gcc

%description
Experimental version of LPCNet that has been used to develop FreeDV 2020 - a HF
radio Digial Voice mode for over the air experimentation with Neural Net speech
coding. Possibly the first use of Neural Net speech coding in real world
operation.

%package devel
Requires:       %{name}%{?_isa} = %{version}-%{release}
Summary:        Development files and tools for LPCNet

%description devel
%{summary}.


%prep
%autosetup -p1 -n LPCNet-%{version}


%build
# Add model data archive to the build directory so CMake finds it.
mkdir -p %{_vpath_builddir}
cp %{SOURCE1} %{__cmake_builddir}/

export CMAKE_POLICY_VERSION_MINIMUM=3.5
%cmake
%cmake_build


%install
%cmake_install


%check
# Test scripts incorrectly assume build directory name. Need to fix.
#ctest


%files
%license COPYING
%doc README.md
%{_libdir}/lib%{name}.so.%{sover}

%files devel
%{_bindir}/*
%{_includedir}/lpcnet/
%{_libdir}/cmake/lpcnetfreedv/
%{_libdir}/lib%{name}.so


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Sep 02 2024 Miroslav Suchý <msuchy@redhat.com> - 0.5-7
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Aug 14 2023 Richard Shaw <hobbes1069@gmail.com> - 0.5-3
- Add patch to link with math library.

* Fri Aug 11 2023 Than Ngo <than@redhat.com> - 0.5-2
- Rebuilt

* Sat Aug 05 2023 Richard Shaw <hobbes1069@gmail.com> - 0.5-1
- Update to 0.5.

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sun Dec 05 2021 Richard Shaw <hobbes1069@gmail.com> - 0.2-10
- Rebuild for codec2 1.0.1.

* Sun Aug 08 2021 Richard Shaw <hobbes1069@gmail.com> - 0.2-9
- Rebuild for codec2 1.0.0.

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sun Dec 20 2020 Richard Shaw <hobbes1069@gmail.com> - 0.2-6
- Bootstrap build for codec2.

* Sun Dec 20 2020 Richard Shaw <hobbes1069@gmail.com> - 0.2-5
- Change library install location to %%{_libdir}.

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.2-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed May 13 2020 Richard Shaw <hobbes1069@gmail.com> - 0.2-2
- Update per reviewer comments.
- Renamed package to lpcnetfreedv (same as library), repo will be renamed in
  the near future.
- Made library private as it is essentially a plugin for freedv.

* Mon Apr 20 2020 Richard Shaw <hobbes1069@gmail.com> - 0.2-1
- Initial packaging.
