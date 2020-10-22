Name:           ccache
Summary:        Compiler Cache
Version:        3.6
Release:        2%{?dist}
License:        BeOpen and BSD and GPLv3+ and (Patrick Powell's and Holger Weiss' license) and Public Domain and Python and zlib
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://ccache.dev
Source0:        https://github.com/%{name}/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  make

%description
Ccache (or “ccache”) is a compiler cache. It speeds up recompilation by caching previous
compilations and detecting when the same compilation is being done again.

%prep
%setup -q 

%build
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

%files
%license LICENSE.adoc
%doc README.md
%{_mandir}/*
%{_bindir}/ccache

%changelog
*   Mon Oct 19 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 3.6-2
-   License verified.
-   Added 'Vendor' and 'Distribution' tags.
*   Mon Mar 30 2020 Jonathan Chiu <jochi@microsoft.com> 3.6-1
-   Original version for CBL-Mariner.
