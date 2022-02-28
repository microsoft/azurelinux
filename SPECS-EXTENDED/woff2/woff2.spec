Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           woff2
Version:        1.0.2
Release:        9%{?dist}
Summary:        Web Open Font Format 2.0 library

License:        MIT
URL:            https://github.com/google/woff2
Source0:        https://github.com/google/woff2/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  brotli-devel >= 1.0

%description
Web Open Font Format (WOFF) 2.0 is an update to the existing WOFF 1.0 with
improved compression that is achieved by using the Brotli algorithm. The primary
purpose of the WOFF2 format is to efficiently package fonts linked to Web
documents by means of CSS @font-face rules.

%package        tools
Summary:        Web Open Font Format 2.0 tools
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    tools
Tools for compressing TTF files to WOFF2 format, decompressing WOFF2
files back to TTF files and dumping WOFF2 file information.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
Development files and utils for %{name}

%prep
%autosetup -n %{name}-%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%cmake .. \
    -DCMAKE_INSTALL_PREFIX="%{_prefix}" \
    -DCMAKE_INSTALL_LIBDIR="%{_libdir}"
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
%make_install -C %{_target_platform}
pushd %{_target_platform}
mkdir -p  %{buildroot}%{_bindir}/
install -m 755 woff2_decompress %{buildroot}%{_bindir}/
install -m 755 woff2_compress %{buildroot}%{_bindir}/
install -m 755 woff2_info %{buildroot}%{_bindir}/
popd

%files
%license LICENSE
%{_libdir}/libwoff2common.so.*
%{_libdir}/libwoff2dec.so.*
%{_libdir}/libwoff2enc.so.*

%files tools
%attr(755, root, root) %{_bindir}/woff2_compress
%attr(755, root, root) %{_bindir}/woff2_decompress
%attr(755, root, root) %{_bindir}/woff2_info

%files devel
%{_includedir}/woff2
%{_libdir}/libwoff2common.so
%{_libdir}/libwoff2dec.so
%{_libdir}/libwoff2enc.so
%{_libdir}/pkgconfig/libwoff2common.pc
%{_libdir}/pkgconfig/libwoff2dec.pc
%{_libdir}/pkgconfig/libwoff2enc.pc

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.2-9
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Mon Apr 06 2020 Tomas Popela <tpopela@redhat.com> - 1.0.2-8
- Package woff2_decompress, woff2_compress and woff2_info in a tools subpackage.
  Thanks to Tomasz Gąsior <kontakt@tomaszgasior.pl>

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Mar 05 2018 Tomas Popela <tpopela@redhat.com> - 1.0.2-3
- Rebuild for brotli update

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Nov 14 2017 Tomas Popela <tpopela@redhat.com> 1.0.2-1
- Update to 1.0.2

* Mon Oct 09 2017 Tomas Popela <tpopela@redhat.com> 1.0.1-1
- Initial import (rhbz#1499676)
