Summary:        Check is a unit testing framework for C
Name:           check
Version:        0.15.2
Release:        1%{?dist}
License:        LGPLv2+
URL:            https://libcheck.github.io/check/
Source0:        https://github.com/libcheck/check/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Provides:       %{name}-devel = %{version}-%{release}
Group:          Development/Tools
Vendor:         Microsoft Corporation
Distribution:   Mariner

%description
Check is a unit testing framework for C. It features a simple interface for defining unit tests,
putting little in the way of the developer. Tests are run in a separate address space,
so both assertion failures and code errors that cause segmentation faults or other signals can be caught.

%prep
%setup -q

%build
autoreconf --install
./configure --prefix=%{_prefix}
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete
rm %{buildroot}%{_infodir}/dir

%check
make %{?_smp_mflags} check

%files
%defattr(-,root,root)
%license COPYING.LESSER
%{_bindir}/*
%{_includedir}/*
%{_libdir}/*so*
%{_libdir}/*.a
%{_libdir}/pkgconfig/*
%{_mandir}/man1/*
%{_infodir}/*
/usr/share/doc/%{name}/*
/usr/share/aclocal/*

%changelog
* Tue Nov 23 2021 Nicolas Guibourge <nicolasg@microsoft.com> 0.15.2-1
- Upgrade to version 0.15.2

* Mon Sep 28 2020 Ruying Chen <v-ruyche@microsoft.com> 0.12.0-5
- Provide check-devel

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 0.12.0-4
- Added %%license line automatically

* Thu Apr 23 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 0.12.0-3
- License verified.
- Updated 'Url' and 'Source0' tags.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 0.12.0-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Wed Sep 19 2018 Ajay Kaher <akaher@vmware.com> 0.12.0-1
- Upgraded to version 0.12.0

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.10.0-2
- GA - Bump release of all rpms

* Tue Feb 23 2016 Xiaolin Li <xiaolinl@vmware.com> 0.10.0-1
- Updated to version 0.10.0

* Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> 0.9.14-2
- Updated group.

* Tue Nov 25 2014 Divya Thaluru <dthaluru@vmware.com> 0.9.14-1
- Initial build. First version
