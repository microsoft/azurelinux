Summary:        OSS implementation of the TCG TPM2 Software Stack (TSS2)
Name:           tpm2-tss
Version:        2.4.6
Release:        3%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Security
URL:            https://github.com/tpm2-software/tpm2-tss
Source0:        https://github.com/tpm2-software/tpm2-tss/releases/download/%{version}/%{name}-%{version}.tar.gz
Patch0:         CVE-2023-22745.patch
BuildRequires:  json-c-devel
BuildRequires:  openssl-devel
Requires:       json-c
Requires:       openssl
Requires(postun): %{_sbindir}/groupdel
Requires(postun): %{_sbindir}/userdel
Requires(pre):  %{_sbindir}/groupadd
Requires(pre):  %{_sbindir}/useradd

%description
OSS implementation of the TCG TPM2 Software Stack (TSS2)

%package devel
Summary:        The libraries and header files needed for TSS2 development.
Requires:       %{name} = %{version}-%{release}

%description devel
The libraries and header files needed for TSS2 development.

%prep
%autosetup -p1

%build
%configure \
    --disable-static \
    --disable-doxygen-doc \
    --with-udevrulesdir=%{_sysconfdir}/udev/rules.d

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -type f -name "*.la" -delete -print

%post
/sbin/ldconfig
mkdir -p %{_sharedstatedir}/tpm
if [ $1 -eq 1 ]; then
    # this is initial installation
    if ! getent group tss >/dev/null; then
        groupadd tss
    fi
    if ! getent passwd tss >/dev/null; then
        useradd -c "TCG Software Stack" -d %{_sharedstatedir}/tpm -g tss \
            -s /bin/false tss
    fi
fi

%postun
/sbin/ldconfig
if [ $1 -eq 0 ]; then
    # this is delete operation
    if getent passwd tss >/dev/null; then
        userdel tss
    fi
    if getent group tss >/dev/null; then
        groupdel tss
    fi
fi

%files
%defattr(-,root,root)
%license LICENSE
%{_sysconfdir}/udev/rules.d/tpm-udev.rules
%{_sysconfdir}/tmpfiles.d/tpm2-tss-fapi.conf
%{_sysconfdir}/tpm2-tss/*
%{_libdir}/*.so.0.0.0
%exclude %{_sysconfdir}/sysusers.d/tpm2-tss.conf

%files devel
%defattr(-,root,root)
%{_includedir}/tss2/*
%{_libdir}/pkgconfig/*
%{_libdir}/*.so
%{_libdir}/*.so.0
%{_mandir}/man3/*
%{_mandir}/man5/*
%{_mandir}/man7/*

%changelog
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
