Summary:        Portable C Audio Library
Name:           pcaudiolib
Version:        1.2
Release:        1%{?dist}
License:        GPLv3+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/espeak-ng/pcaudiolib
#Source0:       https://github.com/espeak-ng/%{name}/archive/%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
BuildRequires:  alsa-lib-devel
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  pkg-config
BuildRequires:  which
Requires:       alsa-lib

%description
The Portable C Audio Library (pcaudiolib) provides a C API to different audio devices.

%package devel
Summary:        Libraries and header files for pcaudiolib
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Libraries and header files for %{name}

%prep
%autosetup -p1

%build
./autogen.sh
%configure \
    --with-alsa \
    --without-pulseaudio \
    --without-qsa \
    --without-coreaudio \
    --without-oss
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -type f -name "*.la" -delete -print

# %check
# This library does not have a testing suite as of version 1.2

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
%doc AUTHORS CHANGELOG.md README.md
%{_libdir}/libpcaudio.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}/audio.h
%{_libdir}/libpcaudio.a
%{_libdir}/libpcaudio.so

%changelog
* Mon Feb 14 2022 Minghe Ren <mingheren@microsoft.com> - 1.2-1
- Update to version 1.2

* Fri Feb 05 2021 Olivia Crain <oliviacrain@microsoft.com> - 1.1-1
- Original version for CBL-Mariner (license: MIT)
- License verified
