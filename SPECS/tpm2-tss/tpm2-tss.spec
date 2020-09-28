Summary:          OSS implementation of the TCG TPM2 Software Stack (TSS2)
Name:             tpm2-tss
Version:          2.2.0
Release:          4%{?dist}
License:          BSD
URL:              https://github.com/tpm2-software/tpm2-tss
Group:            System Environment/Security
Vendor:           Microsoft Corporation
Distribution:     Mariner
Source0:          https://github.com/tpm2-software/tpm2-tss/releases/download/%{version}/%{name}-%{version}.tar.gz
BuildRequires:    openssl-devel
Requires:         openssl
Requires(pre):    /usr/sbin/useradd /usr/sbin/groupadd
Requires(postun): /usr/sbin/userdel /usr/sbin/groupdel
%description
OSS implementation of the TCG TPM2 Software Stack (TSS2)

%package devel
Summary:    The libraries and header files needed for TSS2 development.
Requires:   %{name} = %{version}-%{release}
%description devel
The libraries and header files needed for TSS2 development.

%prep
%setup -q
%build
%configure \
    --disable-static \
    --disable-doxygen-doc \
    --with-udevrulesdir=/etc/udev/rules.d

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

%post
/sbin/ldconfig
mkdir -p /var/lib/tpm
if [ $1 -eq 1 ]; then
    # this is initial installation
    if ! getent group tss >/dev/null; then
        groupadd tss
    fi
    if ! getent passwd tss >/dev/null; then
        useradd -c "TCG Software Stack" -d /var/lib/tpm -g tss \
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
%{_libdir}/*.so.0.0.0

%files devel
%defattr(-,root,root)
%{_includedir}/tss2/*
%{_libdir}/pkgconfig/*
%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/*.so.0
%{_mandir}/man3
%{_mandir}/man7

%changelog
* Sat May 09 00:21:09 PST 2020 Nick Samson <nisamson@microsoft.com> - 2.2.0-4
- Added %%license line automatically

*   Fri Apr 10 2020 Nick Samson <nisamson@microsoft.com> 2.2.0-3
-   Updated Source0. Removed %%define sha1. Updated license abbreviation and validated license.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.2.0-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Thu Feb 21 2019 Alexey Makhalov <amakhalov@vmware.com> 2.2.0-1
-   Initial build. First version
