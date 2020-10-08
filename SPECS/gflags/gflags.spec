Name:           gflags
Summary:        The gflags package contains a C++ library that implements commandline flags processing. 
Version:        2.2.2
Release:        3%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://gflags.github.io/gflags/
#Source0:       https://github.com/%{name}/%{name}/archive/v%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  build-essential

%description
The gflags package contains a C++ library that implements commandline flags processing.
It includes built-in support for standard types such as string and the ability to define
flags in the source file in which they are used.

%package devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}

%description devel
Development files for %{name}

%prep
%setup -q

%build
mkdir build
cd build
%cmake -DBUILD_SHARED_LIBS=ON ..
make %{?_smp_mflags}

%install
cd build
make install DESTDIR=%{buildroot}

# Remove unused files
rm %{buildroot}/root/.cmake/packages/gflags/*

%files
%doc README.md
%license COPYING.txt
%{_bindir}/*
%{_libdir}/*.so*

%files devel
%{_includedir}/*
%{_libdir}/cmake/%{name}
%{_libdir}/*.so
%{_libdir}/pkgconfig/gflags.pc

%changelog
*   Thu Oct 08 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 2.2.2-3
-   License verified.
-   Added %%license macro.
-   Added debug package.
-   Fixed extra file exclude.
-   Fixed 'Source0' URL.
*   Fri Jun 05 2020 Jonathan Chiu <jochi@microsoft.com> 2.2.2-2
-   Exclude extra files
*   Thu Apr 09 2020 Jonathan Chiu <jochi@microsoft.com> 2.2.2-1
-   Original version for CBL-Mariner.
