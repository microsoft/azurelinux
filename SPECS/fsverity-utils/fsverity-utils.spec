Summary:        fsverity utilities
Name:           fsverity-utils
Version:        1.5
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://git.kernel.org/pub/scm/fs/fsverity/fsverity-utils.git/
Source0:        https://git.kernel.org/pub/scm/fs/fsverity/fsverity-utils.git/snapshot/%{name}-%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  glibc-headers
BuildRequires:  kernel-headers
BuildRequires:  make
BuildRequires:  openssl-devel
Requires:       libfsverity = %{version}-%{release}

%description
This is fsverity, a userspace utility for fs-verity.
fs-verity is a Linux kernel feature that does transparent on-demand
integrity/authenticity verification of the contents of read-only files,
using a hidden Merkle tree (hash tree) associated with the file.
The mechanism is similar to dm-verity, but implemented at the file level
rather than at the block device level. The fsverity utility allows you
to set up fs-verity protected files.

%package -n libfsverity
Summary:        Library files for fsverity-utils

%description -n libfsverity
Library for fsverity-utils.

%package devel
Summary:        Development package for fsverity-utils
Requires:       %{name} = %{version}-%{release}
Requires:       libfsverity = %{version}-%{release}

%description devel
Development package for fsverity-utils. This package includes the
libfsverity header and library files.

%prep
%autosetup -p1

%build
%make_build USE_SHARED_LIB=1

%install
%make_install PREFIX=%{_prefix} LIBDIR=%{_libdir} USE_SHARED_LIB=1
find %{buildroot} -type f -name "*.a" -delete

%check
make check

%files
%doc README.md
%{_bindir}/fsverity

%files -n libfsverity
%license LICENSE
%{_libdir}/libfsverity.so.0

%files devel
%{_includedir}/libfsverity.h
%{_libdir}/libfsverity.so
%{_libdir}/pkgconfig/libfsverity.pc

%changelog
* Thu Jun 22 2023 Zhichun Wan <zhichunwan@microsoft.com> - 1.5-1
- Initial CBL-Mariner import from Fedora 36 (license: MIT).
- Update to 1.5
- License verified

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
