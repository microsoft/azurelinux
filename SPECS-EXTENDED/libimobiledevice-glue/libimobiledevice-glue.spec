Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           libimobiledevice-glue
Version:        1.3.1
Release:        1%{?dist}
Summary:        Library used by the libimobiledevice tools and libraries.

License:        LGPLv2.1+
URL:            http://www.libimobiledevice.org/
Source0:        https://github.com/libimobiledevice/%{name}/releases/download/%{version}/%{name}-%{version}.tar.bz2

BuildRequires:  gcc
BuildRequires:  libplist-devel

%description
%{name} is a library with common code used by the libraries and tools around the
libimobiledevice project.

%package devel
Summary: Development package for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Files for development with %{name}.

%prep
%autosetup -p1

%build
%configure --disable-static

make %{?_smp_mflags} V=1


%install
make install DESTDIR=%{buildroot} INSTALL='install -p'

#Remove libtool archives.
find %{buildroot} -type f -name "*.la" -delete

%check
make check

%ldconfig_scriptlets

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc README.md
%{_libdir}/libimobiledevice-glue-1.0.so.*

%files devel
%dir %{_includedir}/libimobiledevice-glue/
%{_includedir}/libimobiledevice-glue*
%{_libdir}/pkgconfig/libimobiledevice-glue-1.0.pc
%{_libdir}/libimobiledevice-glue-1.0.so

%changelog
* Wed Oct 30 2024 Kevin Lockwood <v-klockwood@microsoft.com> - 1.3.1-1
- Original version for Azure Linux
- License verified
