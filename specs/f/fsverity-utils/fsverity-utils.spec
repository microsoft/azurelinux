# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name: fsverity-utils
Version: 1.6
Release: 3%{?dist}
Summary: fsverity utilities

# Automatically converted from old format: BSD - review is highly recommended.
License: LicenseRef-Callaway-BSD
URL:     https://github.com/ebiggers/fsverity-utils
Source0: %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires: gcc make
BuildRequires: kernel-headers glibc-headers
BuildRequires: openssl-devel
BuildRequires: openssl-devel-engine
Requires:      libfsverity = %{version}-%{release}

%description
This is fsverity, a userspace utility for fs-verity.
fs-verity is a Linux kernel feature that does transparent on-demand
integrity/authenticity verification of the contents of read-only files,
using a hidden Merkle tree (hash tree) associated with the file.
The mechanism is similar to dm-verity, but implemented at the file level
rather than at the block device level. The fsverity utility allows you
to set up fs-verity protected files.

%package -n libfsverity
Summary:          Development package for fsverity-utils
%description -n libfsverity
Library for fsverity-utils.

%package devel
Summary:          Development package for fsverity-utils
Requires:         libfsverity = %{version}-%{release}
Requires:         %{name} = %{version}-%{release}
%description devel
Development package for fsverity-utils. This package includes the
libfsverity header and library files.

%prep
%autosetup -p1

%build
%set_build_flags
%make_build CFLAGS="$CFLAGS -g" USE_SHARED_LIB=1

%install
%set_build_flags
%make_install PREFIX=/usr LIBDIR=%{_libdir}  CFLAGS="$CFLAGS -g" USE_SHARED_LIB=1
find %{buildroot} -type f -name "*.a" -delete

%files
%doc README.md
%{_bindir}/fsverity
%{_mandir}/man1/fsverity.1.gz

%files -n libfsverity
%license LICENSE
%{_libdir}/libfsverity.so.0

%files devel
%{_includedir}/libfsverity.h
%{_libdir}/libfsverity.so
%{_libdir}/pkgconfig/libfsverity.pc

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Aug 28 2024 Peter Robinson <pbrobinson@fedoraproject.org> - 1.6-1
- Update to 1.6
- Update upstream URL

* Wed Aug 28 2024 Miroslav Suchý <msuchy@redhat.com> - 1.4-14
- convert license to SPDX

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Sep 17 2021 Timm Bäder <tbaeder@redhat.com> - 1.4-6
- Make sure to pass all build flags in both %%build and %%install

* Thu Sep 16 2021 Sahana Prasad <sahana@redhat.com> - 1.4-5
- Rebuilt with OpenSSL 3.0.0

* Wed Sep 15 2021 Filipe Brandenburger <filbranden@gmail.com> - 1.4-4
- Include patch to implement PKCS#11 opaque keys support through
  OpenSSL pkcs11 engine (rhbz #2000411)

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 1.4-3
- Rebuilt with OpenSSL 3.0.0

* Mon Aug 09 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 1.4-2
- Fix libfsverity package naming (rhbz #1991175)

* Fri Aug 06 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 1.4-1
- Update to 1.4
- Split libs out to subpackage

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 22 21:53:29 UTC 2021 Colin Walters <walters@verbum.org> - 1.3-2
- Update to 1.3

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 15 2020 Colin Walters <walters@verbum.org> - 1.1-2
- Move .so to -devel, hardcode soname

* Mon Jun 15 2020 Jes Sorensen <Jes.Sorensen@gmail.com> - 1.1-1
- Update to version 1.1, split into fsverity-utils and fsverity-utils-devel

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Dec 04 2019 Colin Walters <walters@verbum.org> - 1.0-1
- Initial version
