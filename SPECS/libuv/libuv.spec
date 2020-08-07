Summary:        Cross-platform asynchronous I/O
Name:           libuv
Version:        1.38.0
Release:        1%{?dist}
License:        MIT and CC-BY
URL:            https://libuv.org/
Source0:        https://dist.libuv.org/dist/v%{version}/%{name}-v%{version}.tar.gz
Group:          Applications/System
Vendor:         Microsoft Corporation
Distribution:   Mariner
BuildRequires:  coreutils
BuildRequires:  build-essential

%description
libuv is a multi-platform support library with a focus on asynchronous I/O.
It was primarily developed for use by Node.js, but it's also used by Luvit, Julia, pyuv, and others.

%package devel
Summary:    %{name} development libraries
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
%description devel
%{summary}.

%package static
Summary:    %{name} static files
Group:      Development/Libraries
%description static
%{summary}.

%prep
%setup -qn %{name}-v%{version}

%build
./autogen.sh
%configure
%make_build

%install
%make_install
find %{buildroot} -name '*.la' -delete

%check
%make_build check

%files
%doc AUTHORS
%doc CONTRIBUTING.md
%doc MAINTAINERS.md
%doc README.md
%doc SUPPORTED_PLATFORMS.md
%license LICENSE
%license LICENSE-docs
%{_libdir}/%{name}.so.*

%files devel
%{_includedir}/uv.h
%{_includedir}/uv/
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/%{name}.so

%files static
%{_libdir}/%{name}.a

%changelog
*   Wed May 27 2020 Daniel McIlvaney <damcilva@microsoft.com> - 1.38.0-1
-   Original version for CBL-Mariner
