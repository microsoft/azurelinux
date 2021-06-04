Summary:        Utilities for internationalization and localization
Name:           gettext
Version:        0.19.8.1
Release:        4%{?dist}
License:        GPLv3
URL:            http://www.gnu.org/software/gettext
Group:          Applications/System
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        http://ftp.gnu.org/gnu/gettext/%{name}-%{version}.tar.xz

%description
These allow programs to be compiled with NLS
(Native Language Support), enabling them to output
messages in the user's native language.

# Undefine _ld_as_needed to fix "test-thread_create" and "test-tls" test cases
%undefine _ld_as_needed

%prep
%setup -q

%build
export CFLAGS=" %{build_cflags} -Wno-error=format-security "
./configure \
    --prefix=%{_prefix} \
    --docdir=%{_defaultdocdir}/%{name}-%{version} \
    --disable-silent-rules
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot}%{_libdir} -name '*.la' -delete
rm -rf %{buildroot}/usr/share/doc/gettext-%{version}/examples
rm -rf %{buildroot}%{_infodir}
%find_lang %{name} --all-name

%check
make %{?_smp_mflags} check

%post   -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
%license COPYING
%{_bindir}/*
%{_includedir}/*
%{_libdir}/gettext/*
%{_libdir}/*.so.*
%{_libdir}/*.so
%{_libdir}/*.a
%{_datarootdir}/aclocal/*
%{_datadir}/*
%{_defaultdocdir}/%{name}-%{version}/*
%{_datarootdir}/%{name}/*
%{_mandir}/*

%changelog
*   Thu Jan 05 2021 Andrew Phelps <anphel@microsoft.com> 0.19.8.1-4
-   Undefine "_ld_as_needed" to fix tests "test-thread_create" and "test-tls".
-   Remove sha1. License verified.
*   Thu Jun 11 2020 Henry Beberman <henry.beberman@microsoft.com> 0.19.8.1-3
-   Disable -Wno-error=format-security to build with hardened cflags
*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 0.19.8.1-2
-   Added %%license line automatically
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 19.8.1-1
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Fri Sep 14 2018 Keerthana K <keerthanak@vmware.com> 0.19.8.1-1
-   Update to version 0.19.8.1
*   Wed Apr 05 2017 Danut Moraru <dmoraru@vmware.com> 0.19.8-1
-   Upgrade to 0.19.8
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.19.5.1-2
-   GA - Bump release of all rpms
*   Tue Jan 12 2016 Xiaolin Li <xiaolinl@vmware.com> 0.19.5.1-1
-   Updated to version 0.19.5.1
*   Tue Nov 10 2015 Xiaolin Li <xiaolinl@vmware.com> 0.18.3.2-2
-   Handled locale files with macro find_lang
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 0.18.3.2-1
-   Initial build. First version
