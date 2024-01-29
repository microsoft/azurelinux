Summary:        OSS implementation of the TCG TPM2 Software Stack (TSS2)
Name:           tpm2-tss
Version:        4.0.1
Release:        1%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Security
URL:            https://github.com/tpm2-software/tpm2-tss

Source0: https://github.com/tpm2-software/tpm2-tss/releases/download/%{version}/%{name}-%{version}.tar.gz
%define sha512 %{name}=cabb411f074dfa94919ba914849aac77a0ac2f50622e28a1406cf575369148774748e0e2b7a7c566ec83561a96d4b883bac5a3b1763f4cf48668a0c5d68c0a23
Source1: %{name}.sysusers
BuildRequires:  json-c-devel
BuildRequires:  openssl-devel
BuildRequires:  systemd-devel
BuildRequires:  shadow-utils

Requires: openssl
Requires: systemd-rpm-macros

%description
OSS implementation of the TCG TPM2 Software Stack (TSS2)

%package      devel
Summary:      The libraries and header files needed for TSS2 development.
Requires:     %{name} = %{version}-%{release}

%description    devel
The libraries and header files needed for TSS2 development.

%prep
%autosetup -p1

%build
%configure \
  --disable-static \
  --disable-doxygen-doc \
  --enable-fapi=no \
  --with-udevrulesdir=%{_sysconfdir}/udev/rules.d

%make_build

%install
%make_install %{?_smp_mflags}
install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_sysusersdir}/%{name}.sysusers

%post
%sysusers_create_compat %{SOURCE1}
mkdir -p /var/lib/tpm
chown -R tss:tss /var/lib/tpm
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_sysconfdir}/udev/rules.d/tpm-udev.rules
%{_libdir}/*.so.*
%{_sysusersdir}/%{name}.sysusers

%files devel
%defattr(-,root,root)
%{_includedir}/tss2/*
%{_libdir}/pkgconfig/*
%{_libdir}/*.so
%{_libdir}/*.la
%{_mandir}/man3
%{_mandir}/man7

%changelog
* Mon Jan 22 2024 Brian Fjeldstad <bfjelds@microsoft.com> - 4.0.1-1
- Updated to 4.0.1

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 2.4.6-3
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Wed Feb 08 2023 Rachel Menge <rachelmenge@microsoft.com> - 2.4.6-2
- Add patch to resolve CVE-2023-22745

* Tue Jan 18 2022 Daniel McIlvaney <damcilva@microsoft.com> - 2.4.6-1
- Update to version 2.4.6
- Verified license

* Fri Sep 10 2021 Thomas Crain <thcrain@microsoft.com> - 2.4.0-2
- Remove libtool archive files from final packaging

* Tue Aug 25 2020 Daniel McIlvaney <damcilva@microsoft.com> 2.4.0-1
- Update to 2.4.0.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.2.0-4
- Added %%license line automatically

* Fri Apr 10 2020 Nick Samson <nisamson@microsoft.com> 2.2.0-3
- Updated Source0. Removed %%define sha1. Updated license abbreviation and validated license.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.2.0-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Thu Feb 21 2019 Alexey Makhalov <amakhalov@vmware.com> 2.2.0-1
- Initial build. First version
