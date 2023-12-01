Summary:        libgpg-error
Name:           libgpg-error
Version:        1.47
Release:        1%{?dist}
License:        GPLv2+
URL:            https://gnupg.org/
Group:          Development/Libraries
Source0:        https://gnupg.org/ftp/gcrypt/%{name}/%{name}-%{version}.tar.bz2
Vendor:         Microsoft Corporation
Distribution:   Mariner

%description
This is a library that defines common error values for all GnuPG
components.  Among these are GPG, GPGSM, GPGME, GPG-Agent, libgcrypt,
pinentry, SmartCard Daemon and possibly more in the future.

%package devel
Summary:	Libraries and header files for libgpg-error
Requires:	%{name} = %{version}-%{release}

%description devel
Static libraries and header files for the support library for libgpg-error

%package lang
Summary: Additional language files for libgpg-error
Group:		Applications/System
Requires: %{name} = %{version}-%{release}
%description lang
These are the additional language files of libgpg-error.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -type f -name "*.la" -delete -print
rm -rf %{buildroot}/%{_infodir}
%find_lang %{name}
pwd
install -m 755 %{_builddir}/%{name}-%{version}/src/gpg-error-config %{buildroot}/%{_bindir}/gpg-error-config

%check
make %{?_smp_mflags} check

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/gpg-error
%{_bindir}/yat2m
%{_libdir}/libgpg-error.so.*

%files devel
%defattr(-,root,root)
%{_bindir}/gpg-error-config
%{_bindir}/gpgrt-config
%{_includedir}/*
%{_libdir}/*.so
%{_datadir}/libgpg-error
%{_datadir}/aclocal/*
%{_datadir}/common-lisp/source/gpg-error
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man1/gpgrt-config.1.gz

%files lang -f %{name}.lang
%defattr(-,root,root)

%changelog
* Fri Nov 10 2023 Andrew Phelps <anphel@microsoft.com> - 1.47-1
- Upgrade to version 1.47

* Fri Mar 03 2023 Bala <balakumaran.kannan@microsoft.com> - 1.46-1
- Upgrade to version 1.46 to support gnupg2

* Tue Feb 08 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.43-2
- Remove manual pkgconfig(*) provides in toolchain specs

* Fri Nov 05 2021 Andrew Phelps <anphel@microsoft.com> 1.43-1
- Update to version 1.43

* Fri Sep 10 2021 Olivia Crain <oliviacrain@microsoft.com> 1.32-6
- Remove libtool archive files from final packaging

* Mon Sep 28 2020 Joe Schmitt <joschmit@microsoft.com> 1.32-5
- Explicitly add Provides pkgconfig(gpg-error) to devel package.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 1.32-4
- Added %%license line automatically

* Thu Apr 23 2020 Nick Samson <nisamson@microsoft.com> 1.32-3
- Updated Source0, URL. License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.32-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Mon Sep 10 2018 Bo Gan <ganb@vmware.com> 1.32-1
- Update to 1.32

* Tue Apr 04 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.27-1
- Upgraded to new version 1.27

* Wed Nov 23 2016 Alexey Makhalov <amakhalov@vmware.com> 1.21-3
- Added -lang subpackage

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.21-2
- GA - Bump release of all rpms

* Fri Jan 15 2016 Xiaolin Li <xiaolinl@vmware.com> 1.21-1
- Updated to version 1.21

* Tue Nov 10 2015 Xiaolin Li <xiaolinl@vmware.com> 1.17-2
- Handled locale files with macro find_lang

* Tue Dec 30 2014 Priyesh Padmavilasom <ppadmavilasom@vmware.com>
- initial specfile.
