Summary:        NTFS-3G plugin for reading "system compressed" files
Name:           ntfs-3g-system-compression
Version:        1.0
Release:        5%{?dist}
License:        GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/ebiggers/ntfs-3g-system-compression
Source0:        https://github.com/ebiggers/ntfs-3g-system-compression/archive/v%{version}/ntfs-3g-system-compression-%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  fuse-devel
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  pkg-config
BuildRequires:  pkgconfig(libntfs-3g) >= 2017.3.23

%description
System compression, also known as "Compact OS", is a Windows feature that
allows rarely modified files to be compressed using the XPRESS or LZX
compression formats. It is not built directly into NTFS but rather is
implemented using reparse points. This feature appeared in Windows 10 and it
appears that many Windows 10 systems have been using it by default.

This RPM contains a plugin which enables the NTFS-3G FUSE driver to
transparently read from system-compressed files. Currently, only reading is
supported. Compressing an existing file may be done by using the "compact"
utility on Windows.

%prep
%autosetup

%build
autoreconf -i
%configure
%make_build

%install
%make_install
find %{buildroot} -type f -name "*.la" -delete -print

%files
%doc README.md
%license COPYING
%dir %{_libdir}/ntfs-3g/
%{_libdir}/ntfs-3g/ntfs-plugin-80000017.so

%changelog
* Fri Apr 01 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0-5
- Cleaning-up spec. License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Feb 26 2019 Kamil Páral <kparal@redhat.com> - 1.0-1
- initial package
