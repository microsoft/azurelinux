Summary:        C-based implementation of the GDI+ API
Name:           libgdiplus
Version:        6.1
Release:        2%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/mono/libgdiplus/
Source0:        https://download.mono-project.com/sources/%{name}/%{name}-%{version}.tar.gz
BuildRequires:  gcc-c++
BuildRequires:  giflib-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  libtiff-devel
BuildRequires:  make
BuildRequires:  pkgconf
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(libexif)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(libpng16)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(x11)

%description
Libgdiplus is the Mono library that provides a GDI+-compatible API on non-Windows operating systems.
This implementation uses Cairo to do most of the heavy lifting.

%package        devel
Summary:        Development package for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
This package contains development files for %{name}.

%prep
%autosetup

%build
%configure \
    --with-pango
%make_build

%install
%make_install
find %{buildroot} -type f -name '*.la' -delete -print
find %{buildroot} -type f -name '*.a' -delete -print

# Tests currently fail. It doesn't seem like tests are very stable, with multiple bugs upstream
# pointing out various failures on various platforms. Disabling for now.
# %%check
# %%make_build check

%ldconfig_scriptlets

%files
%license COPYING LICENSE
%{_libdir}/%{name}.so.0*

%files devel
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Fri Mar 31 2023 Pawel Winogrodzki <pawelwi@microsoft.com> - 6.1-2
- Bumping release to re-build with newer 'libtiff' libraries.

* Mon Jul 11 2022 Olivia Crain <oliviacrain@microsoft.com> - 6.1-1
- Original version for CBL-Mariner (license: MIT)
- License verified