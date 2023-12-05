Summary:        Cross-platform asynchronous I/O
Name:           libuv
Version:        1.46.0
Release:        1%{?dist}
License:        MIT AND CC-BY
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://libuv.org/
Source0:        https://dist.libuv.org/dist/v%{version}/%{name}-v%{version}.tar.gz
BuildRequires:  build-essential
BuildRequires:  coreutils
%if %{with_check}
BuildRequires:  shadow-utils
BuildRequires:  sudo
%endif

%description
libuv is a multi-platform support library with a focus on asynchronous I/O.
It was primarily developed for use by Node.js, but it's also used by Luvit, Julia, pyuv, and others.

%package devel
Summary:        %{name} development libraries
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
%{summary}.

%package static
Summary:        %{name} static files
Group:          Development/Libraries

%description static
%{summary}.

%prep
%setup -q -n %{name}-v%{version}

%build
./autogen.sh
%configure
%make_build

%install
%make_install
find %{buildroot} -type f -name "*.la" -delete -print

%check
# The libuv test suite cannot be run as root
chmod g+w . -R
useradd test -G root -m
# skip known failing tests
sed -i '/tty/d' test/test-list.h
sed -i '/queue_foreach_delete/d' test/test-list.h
sudo -u test make -k check

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
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.46.0-1
- Auto-upgrade to 1.46.0 - Azure Linux 3.0 - package upgrades

* Tue Jan 25 2022 Henry Li <lihl@microsoft.com> - 1.43.0-1
- Upgrade to version 1.43.0
- License Verified

*   Fri Dec 04 2020 Andrew Phelps <anphel@microsoft.com> - 1.38.0-2
-   Fix check tests.

*   Wed May 27 2020 Daniel McIlvaney <damcilva@microsoft.com> - 1.38.0-1
-   Original version for CBL-Mariner
