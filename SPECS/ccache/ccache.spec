Name:           ccache
Summary:        Compiler Cache
Version:        4.6
Release:        1%{?dist}
License:        BeOpen and BSD and GPLv3+ and (Patrick Powell's and Holger Weiss' license) and Public Domain and Python and zlib
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://ccache.dev
Source0:        https://github.com/%{name}/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake

%description
Ccache (or “ccache”) is a compiler cache. It speeds up recompilation by caching previous
compilations and detecting when the same compilation is being done again.

%prep
%setup -q

%build
mkdir build
pushd build
%cmake .. -DREDIS_STORAGE_BACKEND=OFF -DENABLE_TESTING=ON
make %{?_smp_mflags}
popd

%install
pushd build
%make_install
popd

%check
pushd build
make check
popd

%files
%license LICENSE.adoc
%doc README.md
%{_bindir}/ccache

%changelog
*   Mon Mar 07 2022 Andrew Phelps <anphel@microsoft.com> 4.6-1
-   Upgrade to version 4.6
-   Enable check tests
*   Mon Oct 19 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 3.6-2
-   License verified.
-   Added 'Vendor' and 'Distribution' tags.
*   Mon Mar 30 2020 Jonathan Chiu <jochi@microsoft.com> 3.6-1
-   Original version for CBL-Mariner.
