Summary:        C11 Annex K functions
Name:           libsafec
Version:        3.7.1
Release:        2%{?dist}
License:        MIT
URL:            https://github.com/rurban/safeclib
Source0:        https://github.com/rurban/safeclib/releases/download/v%{version}/safeclib-%{version}.tar.xz
Patch0:         libsafec-3.7.1-issue119.patch
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  awk
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make
%if 0%{?with_check}
BuildRequires:  tzdata
%endif

%description
Extension library providing C11 Annex K functions

%package devel
Summary:        Development packages for libsafec
Requires:       libsafec = %{version}-%{release}

%description devel
Development files for libsafec

%package check
Summary:        Tools to detect use of unsafe libc APIs

%description check
Tools to detect use of unsafe libc APIs

%prep
%autosetup -n safeclib-%{version} -p1

%build
autoreconf -Wall --install
%configure --disable-static --enable-debug --enable-strmax=0x8000
%make_build

%check
export TZ=Europe/London
make check %{?_smp_mflags}

%install
%make_install
install -d %{buildroot}%{_mandir}/man1/ %{buildroot}%{_mandir}/man3/
install -D doc/man/man1/* %{buildroot}%{_mandir}/man1/
install -D doc/man/man3/* %{buildroot}%{_mandir}/man3/
find %{buildroot} -type f -name "*.la" -delete -print
find %{buildroot} -type f -name "*.pc" -delete -print

%files
%license COPYING
%{_libdir}/libsafec.so.*

%files devel
%license COPYING
%{_libdir}/libsafec.so
%{_includedir}/safeclib
%{_mandir}/man3/*

%files check
%license COPYING
%{_bindir}/check_for_unsafe_apis
%{_mandir}/man1/*

%changelog
* Wed Jul 13 2022 Andy Caldwell <andycaldwell@microsoft.com> - 3.7.1-2
- Don't emit runtime safety check when getenv fails to find variable.

* Wed Apr 20 2022 Andy Caldwell <andycaldwell@microsoft.com> - 3.7.1-1
- Original version for CBL-Mariner (license: MIT).
- License verified
