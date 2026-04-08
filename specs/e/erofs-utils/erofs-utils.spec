# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond curl     1
%bcond deflate  %[ 0%{?fedora} >= 34 || 0%{?rhel} >=  8 ]
%bcond fuse     1
%bcond jsonc    1
%bcond libnl3   1
%bcond libxml2  1
%bcond lz4      %[ 0%{?fedora} >= 34 || 0%{?rhel} >=  9 ]
%bcond lzma     %[ 0%{?fedora} >= 36 || 0%{?rhel} >= 10 ]
%bcond oci      %[ %{with curl} && %{with jsonc} ]
%bcond openssl  1
%bcond qpl      %[ 0%{?fedora} >= 41 && "%{_arch}" == "x86_64" ]
%bcond s3       %[ %{with curl} && %{with libxml2} && %{with openssl} ]
%bcond selinux  1
%bcond uuid     1
%bcond xxhash   1
%bcond zlib     1
%bcond zstd     1

Name:           erofs-utils
Version:        1.9
Release:        1%{?dist}

Summary:        Utilities for working with EROFS
License:        GPL-2.0-only AND GPL-2.0-or-later AND (GPL-2.0-only OR Apache-2.0) AND (GPL-2.0-or-later OR Apache-2.0) AND (GPL-2.0-only OR BSD-2-Clause) AND (GPL-2.0-or-later OR BSD-2-Clause) AND MIT AND Unlicense
URL:            https://erofs.docs.kernel.org/

Source:         https://git.kernel.org/pub/scm/linux/kernel/git/xiang/erofs-utils.git/snapshot/%{name}-%{version}.tar.gz
Patch:          https://git.kernel.org/pub/scm/linux/kernel/git/xiang/erofs-utils.git/patch?id=bb4d440337258ea8a047779c9ca4875c73806ee7#/%{name}-%{version}-fix-manpages.patch

BuildRequires:  %[ "%{toolchain}" == "clang" ? "clang compiler-rt" : "gcc" ]
BuildRequires:  libtool
BuildRequires:  make
%{?with_curl:BuildRequires:  pkgconfig(libcurl)}
%{?with_deflate:BuildRequires:  pkgconfig(libdeflate)}
%{?with_fuse:BuildRequires:  pkgconfig(fuse3) >= 3.2}
%{?with_jsonc:BuildRequires:  pkgconfig(json-c)}
%{?with_libnl3:BuildRequires:  pkgconfig(libnl-genl-3.0) >= 3.1}
%{?with_libxml2:BuildRequires:  pkgconfig(libxml-2.0)}
%{?with_lz4:BuildRequires:  pkgconfig(liblz4) >= 1.9.3}
%{?with_lzma:BuildRequires:  pkgconfig(liblzma) >= 5.4}
%{?with_openssl:BuildRequires:  pkgconfig(openssl)}
%{?with_qpl:BuildRequires:  pkgconfig(qpl) >= 1.5.0}
%{?with_selinux:BuildRequires:  pkgconfig(libselinux)}
%{?with_uuid:BuildRequires:  pkgconfig(uuid)}
%{?with_xxhash:BuildRequires:  pkgconfig(libxxhash)}
%{?with_zlib:BuildRequires:  pkgconfig(zlib)}
%{?with_zstd:BuildRequires:  pkgconfig(libzstd) >= 1.4.0}

Recommends:     erofs-fuse%{?_isa} = %{version}-%{release}

%description
EROFS stands for Enhanced Read-Only File System.  It aims to be a general
read-only file system solution for various use cases instead of just focusing
on saving storage space without considering runtime performance.

This package includes tools to create, check, and extract EROFS images.

%if %{with fuse}
%package -n erofs-fuse
Summary:        FUSE support for mounting EROFS images
Requires:       fuse3

%description -n erofs-fuse
EROFS stands for Enhanced Read-Only File System.  It aims to be a general
read-only file system solution for various use cases instead of just focusing
on saving storage space without considering runtime performance.

This package includes erofsfuse to mount EROFS images.
%endif


%prep
%autosetup -p1

%build
autoreconf -fi
%configure \
    --enable-multithreading \
    --%{?with_curl:with}%{!?with_curl:without}-libcurl \
    --%{?with_deflate:with}%{!?with_deflate:without}-libdeflate \
    --%{?with_fuse:enable}%{!?with_fuse:disable}-fuse \
    --%{?with_jsonc:with}%{!?with_jsonc:without}-json-c \
    --%{?with_libnl3:with}%{!?with_libnl3:without}-libnl3 \
    --%{?with_libxml2:with}%{!?with_libxml2:without}-libxml2 \
    --%{?with_lz4:enable}%{!?with_lz4:disable}-lz4 \
    --%{?with_lzma:enable}%{!?with_lzma:disable}-lzma \
    --%{?with_oci:enable}%{!?with_oci:disable}-oci \
    --%{?with_openssl:with}%{!?with_openssl:without}-openssl \
    --%{?with_qpl:with}%{!?with_qpl:without}-qpl \
    --%{?with_s3:enable}%{!?with_s3:disable}-s3 \
    --%{?with_selinux:with}%{!?with_selinux:without}-selinux \
    --%{?with_uuid:with}%{!?with_uuid:without}-uuid \
    --%{?with_xxhash:with}%{!?with_xxhash:without}-xxhash \
    --%{?with_zlib:with}%{!?with_zlib:without}-zlib \
    --%{?with_zstd:with}%{!?with_zstd:without}-libzstd
%make_build

%install
%make_install


%files
%{_bindir}/dump.erofs
%{_bindir}/fsck.erofs
%{_bindir}/mkfs.erofs
%{_sbindir}/mount.erofs
%{_mandir}/man1/dump.erofs.1*
%{_mandir}/man1/fsck.erofs.1*
%{_mandir}/man1/mkfs.erofs.1*
%{_mandir}/man8/mount.erofs.8*
%doc AUTHORS ChangeLog README docs/PERFORMANCE.md docs/compress-hints.example
%license LICENSES/Apache-2.0 LICENSES/GPL-2.0 LICENSES/MIT

%if %{with fuse}
%files -n erofs-fuse
%{_bindir}/erofsfuse
%{_mandir}/man1/erofsfuse.1*
%doc AUTHORS ChangeLog README
%license LICENSES/Apache-2.0 LICENSES/GPL-2.0 LICENSES/MIT
%endif


%changelog
* Wed Feb 18 2026 David Michael <fedora.dm0@gmail.com> - 1.9-1
- Update to the 1.9 release.

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Tue Nov  4 2025 Tom Callaway <spot@fedoraproject.org> - 1.8.10-3
- rebuild for new fuse3

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 15 2025 David Michael <fedora.dm0@gmail.com> - 1.8.10-1
- Update to the 1.8.10 release.

* Thu Jun 26 2025 David Michael <fedora.dm0@gmail.com> - 1.8.9-1
- Update to the 1.8.9 release.

* Wed Jun 25 2025 David Michael <fedora.dm0@gmail.com> - 1.8.8-1
- Update to the 1.8.8 release.

* Sat Jun 21 2025 Neal Gompa <ngompa@fedoraproject.org> - 1.8.7-1
- Update to the 1.8.7 release.

* Sun Apr 06 2025 David Michael <fedora.dm0@gmail.com> - 1.8.6-1
- Update to the 1.8.6 release.

* Sun Feb 16 2025 Neal Gompa <ngompa@fedoraproject.org> - 1.8.5-2
- Backport fixes to handle low memory environments

* Mon Feb 10 2025 David Michael <fedora.dm0@gmail.com> - 1.8.5-1
- Update to the 1.8.5 release.

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jan 03 2025 Neal Gompa <ngompa@fedoraproject.org> - 1.8.4-2
- Backport support for -Efragdedupe=inode mkfs option

* Thu Jan 02 2025 Neal Gompa <ngompa@fedoraproject.org> - 1.8.4-1
- Update to the 1.8.4 release.

* Sat Dec 14 2024 David Michael <fedora.dm0@gmail.com> - 1.8.3-1
- Update to the 1.8.3 release.

* Sat Oct 12 2024 David Michael <fedora.dm0@gmail.com> - 1.8.2-2
- Backport a fix for multithreaded -Eall-fragments crashes.

* Tue Sep 24 2024 David Michael <fedora.dm0@gmail.com> - 1.8.2-1
- Update to the 1.8.2 release.

* Fri Aug 09 2024 David Michael <fedora.dm0@gmail.com> - 1.8.1-1
- Update to the 1.8.1 release.

* Thu Aug 08 2024 David Michael <fedora.dm0@gmail.com> - 1.8-1
- Update to the 1.8 release.

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Oct 20 2023 David Michael <fedora.dm0@gmail.com> - 1.7.1-1
- Update to the 1.7.1 release.

* Thu Sep 21 2023 David Michael <fedora.dm0@gmail.com> - 1.7-1
- Update to the 1.7 release.

* Tue Aug 29 2023 David Michael <fedora.dm0@gmail.com> - 1.6-3
- Backport patches for CVE-2023-33551 and CVE-2023-33552.
- Change conditional build feature defaults for supporting EPEL 9.

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Mar 11 2023 David Michael <fedora.dm0@gmail.com> - 1.6-1
- Update to the 1.6 release.

* Wed Jan 25 2023 David Michael <fedora.dm0@gmail.com> - 1.5-4
- Enable MicroLZMA support.
- Switch the License tag to SPDX, and ship matching noneffective license files.

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 David Michael <fedora.dm0@gmail.com> - 1.5-1
- Update to the 1.5 release.

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Nov 25 2021 David Michael <fedora.dm0@gmail.com> - 1.4-2
- Backport the patch to install a man page for fsck.
- Backport the patch to fix dump output.

* Sun Nov 21 2021 David Michael <fedora.dm0@gmail.com> - 1.4-1
- Update to the 1.4 release.

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 31 2021 David Michael <fedora.dm0@gmail.com> - 1.3-1
- Update to the 1.3 release.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Jan 09 2021 David Michael <fedora.dm0@gmail.com> - 1.2.1-1
- Update to the 1.2.1 release.

* Thu Dec 10 2020 David Michael <fedora.dm0@gmail.com> - 1.2-1
- Update to the 1.2 release.
- Split FUSE support into an independent subpackage.

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Apr 13 2020 David Michael <fedora.dm0@gmail.com> - 1.1-1
- Update to the 1.1 release.

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Nov 25 2019 David Michael <fedora.dm0@gmail.com> - 1.0-1
- Initial package.
