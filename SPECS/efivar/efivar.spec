Summary:        Tools and libraries to manipulate EFI variables
Name:           efivar
Version:        37
Release:        6%{?dist}
License:        LGPL-2.1
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/System Utilities
URL:            https://github.com/rhboot/efivar
Source0:        https://github.com/rhboot/efivar/releases/download/%{version}/%{name}-%{version}.tar.bz2
BuildRequires:  popt-devel
Provides:       %{name}-libs = %{version}-%{release}

%description
efivar provides a simle CLI to the UEFI variable facility

%package        devel
Summary:        Header and development files for efivar
Requires:       %{name} = %{version}-%{release}

%description    devel
It contains the libraries and header files to create applications

%prep
%autosetup

%build
%make_build \
    PREFIX=%{_prefix} \
    libdir=%{_libdir} \
    bindir=%{_bindir} \
    CFLAGS="%{build_cflags} -Wno-error=address-of-packed-member -Wno-error=stringop-truncation"

%install
%make_install PREFIX=%{_prefix} LIBDIR=%{_libdir}

%check
%make_build test

%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/*
%{_libdir}/*.so.*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_mandir}/man3/*

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 37-6
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Tue Nov 09 2021 Andrew Phelps <anphel@microsoft.com> - 37-5
- Modify CFLAGS to build with gcc11
- License verified

* Fri Jul 23 2021 Thomas Crain <thcrain@microsoft.com> - 37-4
- Lint spec, using make macros throughout
- Package libraries in %%{_libdir}, not %%{_lib64dir}

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 37-3
- Added %%license line automatically

* Tue Mar 24 2020 Henry Beberman <henry.beberman@microsoft.com> - 37-2
- Add -Wno-error=address-of-packed-member to fix gcc9 compat.

* Tue Jan 14 2020 Henry Beberman <hebeberm@microsoft.com> - 37-1
- Update to efivar release 37.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 36-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue Sep 18 2018 Sujay G <gsujay@vmware.com> - 36-1
- Bump efivar version to 36

* Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> - 31-1
- Version update. Added -devel subpackage.

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 0.20-3
- GA - Bump release of all rpms

* Thu Apr 28 2016 Xiaolin Li <xiaolinl@vmware.com> - 0.20-2
- Fix build for linux 4.4.

* Mon Jul 6 2015 Sharath George <sharathg@vmware.com> - 0.20-1
- Initial build. First version
