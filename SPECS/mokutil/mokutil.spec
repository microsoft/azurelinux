Name:           mokutil
Version:        0.3.0
Release:        17%{?dist}
Summary:        Tool to manage UEFI Secure Boot MoK Keys
License:        GPLv3+
URL:            https://github.com/lcp/mokutil
Vendor:         Microsoft Corporation
Distribution:   Mariner
#Source0:       https://github.com/lcp/mokutil/archive/%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz

ExclusiveArch:  x86_64

BuildRequires:  gcc
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gnu-efi
BuildRequires:  openssl-devel
BuildRequires:  openssl
BuildRequires:  which
BuildRequires:  efivar-devel >= 31-1

Conflicts:      shim < 0.8-1%{?dist}

Patch0001: 0001-Fix-the-potential-buffer-overflow.patch
Patch0002: 0002-Fix-the-32bit-signedness-comparison.patch
Patch0003: 0003-Build-with-fshort-wchar-so-toggle-passwords-work-rig.patch
Patch0004: 0004-Don-t-allow-sha1-on-the-mokutil-command-line.patch
Patch0005: 0005-Make-all-efi_guid_t-const.patch
Patch0006: 0006-mokutil-be-explicit-about-file-modes-in-all-cases.patch
Patch0007: 0007-Add-bash-completion-file.patch
Patch0008: 0008-generate_hash-generate_pw_hash-don-t-use-strlen-for-.patch
Patch0009: 0009-Avoid-taking-pointer-to-packed-struct.patch
Patch0010: 0010-Fix-a-integer-comparison-sign-issue.patch

%description
mokutil provides a tool to manage keys for Secure Boot through the MoK
("Machine's Own Keys") mechanism.

%prep
%setup -q -n %{name}-%{version}
%patch0001 -p1
%patch0002 -p1
%patch0003 -p1
%patch0004 -p1
%patch0005 -p1
%patch0006 -p1
%patch0007 -p1
%patch0008 -p1
%patch0009 -p1
%patch0010 -p1

%build
./autogen.sh
%configure
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make PREFIX=%{_prefix} LIBDIR=%{_libdir} DESTDIR=%{buildroot} install

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc README
%{_bindir}/mokutil
%{_mandir}/man1/*
%{_datadir}/bash-completion/completions/mokutil

%changelog
* Tue May 12 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.3.0-17
- Building only for x86_64.

* Thu May 07 2020 Chris Co <chrco@microsoft.com> - 0.3.0-16
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2:0.3.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 12 2019 Peter Jones <pjones@redhat.com> - 0.3.0-14
- Pull one more upstream patch to keep this in sync with the f31 build.

* Thu Oct 24 2019 Leigh Scott <leigh123linux@googlemail.com> - 1:0.3.0-14
- Apply upstream commits to fix FTBFS

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.3.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.3.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 14 2019 Björn Esser <besser82@fedoraproject.org> - 1:0.3.0-11
- Rebuilt for libcrypt.so.2 (#1666033)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.3.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.3.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 1:0.3.0-8
- Rebuilt for switch to libxcrypt

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.3.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.3.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jul 08 2017 Peter Jones <pjones@redhat.com> - 0.3.0-5
- Rebuild for efivar-31-1.fc26
  Related: rhbz#1468841

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Aug 17 2016 Peter Jones <pjones@redhat.com> - 0.3.0-3
- Rebuild for newer efivar again.

* Wed Aug 10 2016 Peter Jones <pjones@redhat.com> - 0.3.0-2
- Update for newer efivar.

* Tue Jun 14 2016 Peter Jones <pjones@redhat.com> - 0.3.0-1
- Update to 0.3.0 release.
  Resolves: rhbz#1334628

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 1:0.2.0-2
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Mon Oct 06 2014 Peter Jones <pjones@redhat.com> - 0.2.0-1
- First independent package.
