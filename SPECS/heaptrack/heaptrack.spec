Vendor:         Microsoft Corporation
Distribution:   Azure Linux

Name:    heaptrack
Version: 1.5.0
Release: 12%{?dist}
Summary: A heap memory profiler for Linux

License: Apache-2.0 AND BSD-3-Clause AND BSL-1.0 AND GPL-2.0-or-later AND LGPL-2.1-only AND LGPL-2.1-or-later AND MIT
URL:     https://invent.kde.org/sdk/heaptrack/

Source0: https://download.kde.org/stable/heaptrack/%{version}/%{name}-%{version}.tar.xz

Patch0:  Support-KChart6-for-KF6.patch
Patch1:  Use-QString-for-KConfigGroup-names.patch

# Upstream Patch: https://invent.kde.org/sdk/heaptrack/-/commit/c6c45f3455a652c38aefa402aece5dafa492e8ab
# Will prolly be unneeded next release.
Patch2:  fix-gcc14-cmake-compat.patch

BuildRequires:  extra-cmake-modules
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  boost-devel
BuildRequires:  libunwind-devel
BuildRequires:  libdwarf-devel
BuildRequires:  elfutils-devel
BuildRequires:  libzstd-devel
BuildRequires:  zlib-devel

# no libunwind on s390(x)
ExcludeArch:    s390 s390x

%description
Heaptrack traces all memory allocations and annotates these events with stack
traces.Dedicated analysis tools then allow you to interpret the heap memory
profile to:
- find hotspots that need to be optimized to reduce the memory footprint of your
  application
- find memory leaks, i.e. locations that allocate memory which is never
  deallocated
- find allocation hotspots, i.e. code locations that trigger a lot of memory
  allocation calls
- find temporary allocations, which are allocations that are directly followed
  by their deallocation


%prep
%autosetup -n %{name}-%{version} -p1


%build
%cmake \
    -DHEAPTRACK_BUILD_GUI=OFF \
    -DHEAPTRACK_USE_LIBUNWIND=OFF

%cmake_build


%install
%cmake_install

#%find_lang heaptrack --with-qt --all-name

# binary not yet available
#%check
#desktop-file-validate %{buildroot}%{_datadir}/applications/org.kde.heaptrack.desktop


%files
%license LICENSES/GPL-2.0-or-later.txt
%{_bindir}/heaptrack
%{_bindir}/heaptrack_print
#%{_datadir}/applications/org.kde.heaptrack.desktop
%{_includedir}/heaptrack_api.h
#%{_datadir}/metainfo/org.kde.heaptrack.appdata.xml
%dir %{_libdir}/heaptrack/
%{_libdir}/heaptrack/libheaptrack_inject.so
%{_libdir}/heaptrack/libheaptrack_preload.so
%{_libdir}/heaptrack/libexec/heaptrack_interpret
%{_libdir}/heaptrack/libexec/heaptrack_env
#%{_datadir}/icons/hicolor/*/apps/heaptrack*


%changelog
* Tue Mar 10 2026 Kshitiz Godara <kgodara@microsoft.com> - 1.5.0-12
- Initial import from Fedora for Azure Linux

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Mon Jan 12 2026 Jonathan Wakely <jwakely@fedoraproject.org> - 1.5.0-10
- Rebuilt for Boost 1.90

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jan 20 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 18 2024 Steve Cossette <farchord@gmail.com> - 1.5.0-4
- Fix for building on GCC 14

* Wed Jan 17 2024 Jonathan Wakely <jwakely@redhat.com> - 1.5.0-3
- Rebuilt for Boost 1.83

* Tue Jan 16 2024 Alessandro Astone <ales.astone@gmail.com> - 1.5.0-2
- Backport Qt6 fixes

* Wed Dec 27 2023 Marie Loise Nolden <loise@kde.org> - 1.5.0-1
- Update to 1.5.0 using Qt6

* Fri Dec 15 2023 Florian Weimer <fweimer@redhat.com> - 1.4.0-3
- Fix C compatibility issues in CMake probes

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Mar 30 2023 Jan Grulich <jgrulich@redhat.com> - 1.4.0-1
- 1.4.0

* Mon Mar 06 2023 Jan Grulich <jgrulich@redhat.com> - 1.2.0-13
- Fix build failure against GCC13

* Mon Feb 20 2023 Jonathan Wakely <jwakely@redhat.com> - 1.2.0-12
- Rebuilt for Boost 1.81

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jan Grulich <jgrulich@redhat.com> - 1.2.0-9
- Add missing BR: elfutils-devel

* Wed May 04 2022 Thomas Rodgers <trodgers@redhat.com> - 1.2.0-8
- Rebuilt for Boost 1.78

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Aug 06 2021 Jonathan Wakely <jwakely@redhat.com> - 1.2.0-6
- Rebuilt for Boost 1.76

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Mar 30 2021 Jonathan Wakely <jwakely@redhat.com> - 1.2.0-4
- Rebuilt for removed libstdc++ symbol (#1937698)

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 22 2021 Jonathan Wakely <jwakely@redhat.com> - 1.2.0-2
- Rebuilt for Boost 1.75

* Tue Sep 01 2020 Jan Grulich <jgrulich@redhat.com> - 1.2.0-1
- 1.2.0

* Tue Sep 01 2020 Rex Dieter <rdieter@fedoraproject.org> - 1.1.0-10
- adapt to new cmake macros

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-9
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu May 28 2020 Jonathan Wakely <jwakely@redhat.com> - 1.1.0-7
- Rebuilt for Boost 1.73

* Thu Feb 27 2020 Jan Grulich <jgrulich@redhat.com> - 1.1.0-6
- BR: libzstd-devel

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 29 2019 Jonathan Wakely <jwakely@redhat.com> - 1.1.0-2
- Rebuilt for Boost 1.69

* Wed Jan 02 2019 Jan Grulich <jgrulich@redhat.com> - 1.1.0-1
- 1.1.0

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Sep 07 2017 Daniel Vrátil <dvratil@fedoraproject.org> - 1.0.0-8
- Fix build against glibc >= 2.26 (rawhide/f27)

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 24 2017 Björn Esser <besser82@fedoraproject.org> - 1.0.0-5
- Rebuilt for Boost 1.64

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Thu Mar 23 2017 Jan Grulich <jgrulich@redhat.com> - 1.0.0-3
- Add BR: qt5-qtsvg-devel

* Sat Mar 11 2017 Dan Horák <dan[at]danny.cz> - 1.0.0-2
- exclude s390(x), because libunwind is not there

* Fri Mar 10 2017 Jan Grulich <jgrulich@redhat.com> - 1.0.0-1
- Initial version
