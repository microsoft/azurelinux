%global major_version 3
Summary:        Cmake
Name:           cmake
Version:        3.21.4
Release:        10%{?dist}
License:        BSD AND LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Tools
URL:            https://www.cmake.org/
Source0:        https://github.com/Kitware/CMake/releases/download/v%{version}/%{name}-%{version}.tar.gz
Source1:        macros.cmake
Patch0:         disableUnstableUT.patch
# We could use --system-curl instead of patching, but unfortuately curl isn't currently available in time during the toolchain build.
Patch1:         CVE-2022-43551.patch
Patch2:         CVE-2023-23914-0001-share-add-sharing-of-HSTS-cache-among-handles.patch
Patch3:         CVE-2023-23914-0002-hsts-handle-adding-the-same-host-name-again.patch
Patch4:         CVE-2023-28322-lib-unify-the-upload-method-handling.patch
Patch5:         CVE-2023-35945.patch
Patch6:         CVE-2023-38545.patch
Patch7:         CVE-2023-38546.patch
Patch8:         cve-2023-44487.patch
BuildRequires:  bzip2
BuildRequires:  bzip2-devel
BuildRequires:  curl
BuildRequires:  curl-devel
BuildRequires:  expat-devel
BuildRequires:  expat-libs
BuildRequires:  libarchive
BuildRequires:  libarchive-devel
BuildRequires:  ncurses-devel
BuildRequires:  xz
BuildRequires:  xz-devel
BuildRequires:  zlib
BuildRequires:  zlib-devel
Requires:       bzip2
Requires:       expat
Requires:       libarchive
Requires:       ncurses
Requires:       zlib
Provides:       %{name}%{major_version} = %{version}-%{release}
Provides:       %{name}-filesystem = %{version}-%{release}
Provides:       %{name}-filesystem%{?_isa} = %{version}-%{release}

%description
CMake is an extensible, open-source system that manages the build process in an
operating system and in a compiler-independent manner.

%prep
%autosetup -p1

%build
./bootstrap \
    --prefix=%{_prefix} \
    --system-expat \
    --system-zlib \
    --system-libarchive \
    --system-bzip2 \
    --parallel=$(nproc)
%make_build

%install
%make_install
find %{buildroot} -type f -name "*.la" -delete -print
install -Dpm0644 %{SOURCE1} %{buildroot}%{_libdir}/rpm/macros.d/macros.cmake
sed -i -e "s|@@CMAKE_VERSION@@|%{version}|" -e "s|@@CMAKE_MAJOR_VERSION@@|%{major_version}|" %{buildroot}%{_libdir}/rpm/macros.d/macros.cmake

%check
# Removing static libraries to fix issues with the "ParseImplicitLinkInfo" test runs for the "craype-C-Cray-8.7.input" and "craype-CXX-Cray-8.7.input" inputs.
# Should be removed once the issue is fixed upstream and we apply the fix: https://gitlab.kitware.com/cmake/cmake/-/issues/22470.
rm -f %{_lib64dir}/lib{stdc++,gfortran}.a

bin/ctest --force-new-ctest-process --rerun-failed --output-on-failure

%files
%defattr(-,root,root)
%license Licenses
%{_bindir}/*
%{_datadir}/%{name}-*/*
%{_datadir}/aclocal/*
%{_datadir}/bash-completion/completions/*
%{_datadir}/emacs/site-lisp/cmake-mode.el
%{_datadir}/vim/vimfiles/*
%{_libdir}/rpm/macros.d/macros.cmake
%{_prefix}/doc/%{name}-*/*

%changelog
* Thu Oct 19 2023 Dan Streetman <ddstreet@ieee.org> - 3.21.4-10
- Patch vendored nghttp2 for CVE-2023-44487

* Tue Oct 10 2023 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 3.21.4-9
- Patch vendored curl for CVE-2023-38545, CVE-2023-38546

* Wed Sep 06 2023 Brian Fjeldstad <bfjelds@microsoft.com> - 3.21.4-8
- Patch vendored nghttp2 for CVE-2023-35945

* Thu Jun 08 2023 Sam Meluch <sammeluch@microsoft.com> - 3.21.4-7
- Add source directory for when not building in source

* Thu Jun 08 2023 Sumedh Sharma <sumsharma@microsoft.com> - 3.21.4-6
- Patch vendored curl for CVE-2023-28322

* Tue Jun 06 2023 Dan Streetman <ddstreet@ieee.org> - 3.21.4-5
- Patch vendored curl for CVE-2023-23914

* Mon Apr 03 2023 Bala <balakumaran.kannan@microsoft.com> - 3.21.4-4
- Add build directory to %cmake macro to align with %cmake_build

* Mon Feb 06 2023 Daniel McIlvaney <damcilva@microsoft.com> - 3.21.4-3
- Patch CVE-2022-43551 in bundled curl

* Sun Dec 12 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.21.4-2
- Adding a workaround for two failing "ParseImplicitLinkInfo" test cases until a fix is available.
- Adjusted test command to re-run flaky tests.
- Bringing back generation of debug symbols.

* Mon Nov 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.21.4-1
- Update to version 3.21.4.
- License verified.

* Thu Dec 10 2020 Joe Schmitt <joschmit@microsoft.com> - 3.17.3-5
- Provide cmake-filesystem and isa version.

* Thu Nov 05 2020 Joe Schmitt <joschmit@microsoft.com> - 3.17.3-4
- Define additional cmake macros.

* Mon Sep 28 2020 Ruying Chen <v-ruyche@microsoft.com> - 3.17.3-3
- Update cmake version related macros
- Provide cmake3

* Mon Jul 06 2020 Eric Li <eli@microsoft.com> - 3.17.3-2
- Update Source0: to the new location

* Tue Jun 23 2020 Paul Monson <paulmon@microsoft.com> - 3.17.3-1
- Update to version 3.17.3

* Fri Jun 12 2020 Henry Beberman <henry.beberman@microsoft.com> - 3.12.1-7
- Temporarily disable generation of debug symbols.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 3.12.1-6
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 3.12.1-5
- Initial CBL-Mariner import from Photon (license: Apache2).

* Thu Jan 17 2019 Ankit Jain <ankitja@vmware.com> - 3.12.1-4
- Removed unnecessary libgcc-devel buildrequires

* Thu Dec 06 2018 <ashwinh@vmware.com> - 3.12.1-3
- Bug Fix 2243672. Add system provided libs.

* Sun Sep 30 2018 Bo Gan <ganb@vmware.com> - 3.12.1-2
- smp make (make -jN)
- specify /usr/lib as CMAKE_INSTALL_LIBDIR

* Fri Sep 07 2018 Ajay Kaher <akaher@vmware.com> - 3.12.1-1
- Upgrading version to 3.12.1
- Adding macros.cmake

* Fri Sep 29 2017 Kumar Kaushik <kaushikk@vmware.com> - 3.8.0-4
- Building using system expat libs.

* Thu Aug 17 2017 Kumar Kaushik <kaushikk@vmware.com> - 3.8.0-3
- Fixing make check bug # 1632102.

* Tue May 23 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> - 3.8.0-2
- bug 1448414: Updated to build in parallel

* Fri Apr 07 2017 Anish Swaminathan <anishs@vmware.com>  3.8.0-1
- Upgrade to 3.8.0

* Thu Oct 06 2016 ChangLee <changlee@vmware.com> - 3.4.3-3
- Modified %check

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 3.4.3-2
- GA - Bump release of all rpms

* Thu Feb 25 2016 Kumar Kaushik <kaushikk@vmware.com> - 3.4.3-1
- Updated version.

* Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> - 3.2.1.2
- Updated group.

* Mon Apr 6 2015 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 3.2.1-1
- Update to 3.2.1

* Tue Nov 25 2014 Divya Thaluru <dthaluru@vmware.com> - 3.0.2-1
- Initial build. First version
