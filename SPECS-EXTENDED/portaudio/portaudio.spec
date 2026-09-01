Summary:        Free, cross-platform, open-source, audio I/O library
Name:           portaudio
Version:        19.7.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          System Environment/Libraries
URL:            https://www.portaudio.com
Source0:        https://files.portaudio.com/archives/pa_stable_v190700_20210406.tgz
BuildRequires:  alsa-lib-devel
BuildRequires:  gcc
BuildRequires:  make
Requires:       alsa-lib

%description
PortAudio is a free, cross-platform, open-source, audio I/O library. It lets
you write simple audio programs in C or C++ that will compile and run on many
platforms including Windows, Macintosh OS X, and Unix (OSS/ALSA). It is
intended to promote the exchange of audio software between developers on
different platforms.

%package        devel
Summary:        Header and development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
This package contains the libraries and header files needed to develop
applications that use %{name}.

%prep
%autosetup -n %{name}

%build
%configure \
    --enable-shared \
    --disable-static \
    --with-alsa \
    --without-jack \
    --without-oss
%make_build

%install
%make_install
find %{buildroot} -name '*.la' -delete

%files
%license LICENSE.txt
%{_libdir}/libportaudio.so.*

%files devel
%{_includedir}/portaudio.h
%{_includedir}/pa_linux_alsa.h
%{_libdir}/libportaudio.so
%{_libdir}/pkgconfig/portaudio-2.0.pc

%changelog
* Mon Jun 22 2026 Ankita Pareek <ankitapareekx@microsoft.com> - 19.7.0-1
- Original version for Azure Linux
- License verified
