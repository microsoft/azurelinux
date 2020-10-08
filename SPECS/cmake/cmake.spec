%global major_version 3

Summary:        Cmake
Name:           cmake
Version:        3.17.3
Release:        3%{?dist}
License:        BSD and LGPLv2+
URL:            https://www.cmake.org/
Source0:        https://github.com/Kitware/CMake/releases/download/v%{version}/%{name}-%{version}.tar.gz
Source1:        macros.cmake
Patch0:         disableUnstableUT.patch
Group:          Development/Tools
Vendor:         Microsoft Corporation
Distribution:   Mariner
Provides:       %{name}%{major_version} = %{version}-%{release}
BuildRequires:  ncurses-devel
BuildRequires:  xz
BuildRequires:  xz-devel
BuildRequires:  curl
BuildRequires:  curl-devel
BuildRequires:  expat-libs
BuildRequires:  expat-devel
BuildRequires:  zlib
BuildRequires:  zlib-devel
BuildRequires:  libarchive
BuildRequires:  libarchive-devel
BuildRequires:  bzip2
BuildRequires:  bzip2-devel
Requires:       ncurses
Requires:       expat
Requires:       zlib
Requires:       libarchive
Requires:       bzip2

%description
CMake is an extensible, open-source system that manages the build process in an
operating system and in a compiler-independent manner.
%prep
%setup -q
%patch0 -p1
%build
# Disable symbol generation
export CFLAGS="`echo " %{build_cflags} " | sed 's/ -g//'`"
export CXXFLAGS="`echo " %{build_cxxflags} " | sed 's/ -g//'`"

ncores="$(/usr/bin/getconf _NPROCESSORS_ONLN)"
./bootstrap --prefix=%{_prefix} --system-expat --system-zlib --system-libarchive --system-bzip2 --parallel=$ncores
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete
install -Dpm0644 %{SOURCE1} %{buildroot}%{_libdir}/rpm/macros.d/macros.cmake
sed -i -e "s|@@CMAKE_VERSION@@|%{version}|" -e "s|@@CMAKE_MAJOR_VERSION@@|%{major_version}|" %{buildroot}%{_libdir}/rpm/macros.d/macros.cmake

%check
make  %{?_smp_mflags} test

%files
%defattr(-,root,root)
%license Licenses
/usr/share/%{name}-*/*
%{_bindir}/*
/usr/doc/%{name}-*/*
/usr/share/aclocal/*
%{_libdir}/rpm/macros.d/macros.cmake

%changelog
*   Mon Sep 28 2020 Ruying Chen <v-ruyche@microsoft.com> 3.17.3-3
-   Update cmake version related macros
-   Provide cmake3
*   Mon Jul 06 2020 Eric Li <eli@microsoft.com> 3.17.3-2
-   Update Source0: to the new location
*   Tue Jun 23 2020 Paul Monson <paulmon@microsoft.com> 3.17.3-1
-   Update to version 3.17.3
*   Fri Jun 12 2020 Henry Beberman <henry.beberman@microsoft.com> 3.12.1-7
-   Temporarily disable generation of debug symbols.
*   Sat May 09 00:20:40 PST 2020 Nick Samson <nisamson@microsoft.com> - 3.12.1-6
-   Added %%license line automatically
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 3.12.1-5
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Thu Jan 17 2019 Ankit Jain <ankitja@vmware.com> 3.12.1-4
-   Removed unnecessary libgcc-devel buildrequires
*   Thu Dec 06 2018 <ashwinh@vmware.com> 3.12.1-3
-   Bug Fix 2243672. Add system provided libs.
*   Sun Sep 30 2018 Bo Gan <ganb@vmware.com> 3.12.1-2
-   smp make (make -jN)
-   specify /usr/lib as CMAKE_INSTALL_LIBDIR
*   Fri Sep 07 2018 Ajay Kaher <akaher@vmware.com> 3.12.1-1
-   Upgrading version to 3.12.1
-   Adding macros.cmake
*   Fri Sep 29 2017 Kumar Kaushik <kaushikk@vmware.com> 3.8.0-4
-   Building using system expat libs.
*   Thu Aug 17 2017 Kumar Kaushik <kaushikk@vmware.com> 3.8.0-3
-   Fixing make check bug # 1632102.
*   Tue May 23 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.8.0-2
-   bug 1448414: Updated to build in parallel
*   Fri Apr 07 2017 Anish Swaminathan <anishs@vmware.com>  3.8.0-1
-   Upgrade to 3.8.0
*   Thu Oct 06 2016 ChangLee <changlee@vmware.com> 3.4.3-3
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.4.3-2
-   GA - Bump release of all rpms
*   Thu Feb 25 2016 Kumar Kaushik <kaushikk@vmware.com> 3.4.3-1
-   Updated version.
*   Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> 3.2.1.2
-   Updated group.
*   Mon Apr 6 2015 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.2.1-1
-   Update to 3.2.1
*   Tue Nov 25 2014 Divya Thaluru <dthaluru@vmware.com> 3.0.2-1
-   Initial build. First version
