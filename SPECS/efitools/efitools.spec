Name:           efitools
Version:        1.9.2
Release:        14%{?dist}
Summary:        Tools to manipulate EFI secure boot keys and signatures
License:        GPLv2 and LGPLv2 and BSD

# call-to-mktemp: 
# https://github.com/vathpela/efitools/issues/2
URL:            https://git.kernel.org/pub/scm/linux/kernel/git/jejb/efitools.git
Source0:        %{url}/snapshot/%{name}-%{version}.tar.gz
Patch1:         efitools-c99-1.patch
Patch2:         efitools-c99-2.patch
Patch3:         fix_make_dep.patch

# same as gnu-efi
ExclusiveArch:  x86_64

BuildRequires:  pkgconfig(openssl)

BuildRequires:  gcc
BuildRequires:  gnu-efi-devel
BuildRequires:  help2man
BuildRequires:  openssl
BuildRequires:  perl-File-Slurp
BuildRequires:  sbsigntools

Requires:       coreutils%{_isa}
Requires:       mtools%{_isa}
Requires:       parted%{_isa}
Requires:       util-linux%{_isa}
Recommends:     sbsigntools%{_isa}

%description
This package installs a variety of tools for manipulating keys and binary
signatures on UEFI secure boot platforms.
The tools provide access to the keys and certificates stored in the
secure variables of the UEFI firmware, usually in the NVRAM area.

%prep
%autosetup -p1

%build
%set_build_flags
%make_build

%install
%make_install DOCDIR=%{buildroot}%{_docdir}/%{name}/ CFLAGS="%{optflags}"

rm -v %{buildroot}%{_docdir}/%{name}/COPYING

%files
%doc README
%license COPYING

%{_datadir}/%{name}/
%{_mandir}/man1/*.1.*

%{_bindir}/cert-to-efi-hash-list
%{_bindir}/cert-to-efi-sig-list
%{_bindir}/efi-readvar
%{_bindir}/efi-updatevar
%{_bindir}/efitool-mkusb
%{_bindir}/flash-var
%{_bindir}/hash-to-efi-sig-list
%{_bindir}/sig-list-to-certs
%{_bindir}/sign-efi-sig-list

%changelog
* Fri Jun 14 2024 Dan Streetman <ddstreet@microsoft.com> - 1.9.2-14
- initial import from fedora 40

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Dec 14 2022 Florian Weimer <fweimer@redhat.com> - 1.9.2-9
- C99 port

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 1.9.2-6
- Rebuilt with OpenSSL 3.0.0

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun Mar 07 2021 Vladislav Kazakov <vpackager@gmail.com> - 1.9.2-4 
- Fix incorrect build.

* Sat Feb 06 2021 Vladislav Kazakov <vpackager@gmail.com> - 1.9.2-3
- Add system flags to CFLAGS.
- Remove i686 support.

* Sun Jan 31 2021 Vladislav Kazakov <vpackager@gmail.com> - 1.9.2-2
- Add BSD license.
- Rename LGPLv2.1 to LGPLv2. 
- Add reference to issue about mktemp usage.

* Sun Jan 17 2021 Vladislav Kazakov <vpackager@gmail.com> - 1.9.2-1
- Initial SPEC release.
