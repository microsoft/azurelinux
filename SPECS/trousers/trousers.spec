Summary:        TCG Software Stack (TSS)
Name:           trousers
Version:        0.3.14
Release:        7%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Security
URL:            https://sourceforge.net/projects/trousers
Source0:        %{url}/files/%{name}/%{version}/%{name}-%{version}.tar.gz
# CVE-2020-24330.patch also fixes CVE-2020-24331 and CVE-2020-24332.
Patch0:         CVE-2020-24330.patch
Patch1:         CVE-2020-24331.nopatch
Patch2:         CVE-2020-24332.nopatch
Requires:       libtspi = %{version}-%{release}

%description
Trousers is an open-source TCG Software Stack (TSS), released under
the BSD License. Trousers aims to be compliant with the
1.1b and 1.2 TSS specifications available from the Trusted Computing

%package devel
Summary:        The libraries and header files needed for TSS development.
Requires:       libtspi = %{version}-%{release}

%description devel
The libraries and header files needed for TSS development.

%package -n libtspi
Summary:        TSPI library

%description -n libtspi
TSPI library

%prep
%autosetup -c %{name}-%{version} -p1

%build
%configure \
    --disable-static

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

%post
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
if [ $1 -eq 0 ]; then
    # this is delete operation
    if getent passwd tss >/dev/null; then
        userdel tss
    fi
    if getent group tss >/dev/null; then
        groupdel tss
    fi
fi

%post -n libtspi -p /sbin/ldconfig
%postun -n libtspi -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license LICENSE
%{_sysconfdir}/*
%{_sbindir}/*
%{_mandir}/man5
%{_mandir}/man8
%exclude %{_var}

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/libtspi.la
%{_libdir}/libtspi.so
%{_libdir}/libtspi.so.1
%{_mandir}/man3

%files -n libtspi
%defattr(-,root,root)
%{_libdir}/libtspi.so.1.2.0
%exclude %{_libdir}/debug
%exclude %{_libdir}/libtddl.a

%changelog
* Tue Oct 27 2020 Olivia Crain <oliviacrain@microsoft.com> - 0.3.14-7
- Added nopatch file for CVE-2020-24332.

* Thu Aug 20 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.3.14-6
- Applying a patch for CVE-2020-24330 and CVE-2020-24331.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 0.3.14-5
- Added %%license line automatically

* Thu Apr 09 2020 Joe Schmitt <joschmit@microsoft.com> - 0.3.14-4
- Update Source0 with valid URL.
- Update License.
- Remove sha1 macro.
- License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 0.3.14-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> - 0.3.14-2
- Use standard configure macros

* Thu Mar 2 2017 Alexey Makhalov <amakhalov@vmware.com> - 0.3.14-1
- Initial build. First version
