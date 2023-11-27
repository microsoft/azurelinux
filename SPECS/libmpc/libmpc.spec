Summary:        Library for the arithmetic of complex numbers
Name:           libmpc
Version:        1.3.1
Release:        1%{?dist}
License:        LGPLv3+
URL:            http://www.multiprecision.org
Group:          Applications/System
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://ftp.gnu.org/gnu/mpc/mpc-%{version}.tar.gz
Requires:       gmp
Provides:       %{name}-devel = %{version}-%{release}

%description
The MPC package contains a library for the arithmetic of complex
numbers with arbitrarily high precision and correct rounding of
the result.

%prep
%setup -q -n mpc-%{version}

%build
./configure \
        --prefix=%{_prefix} \
        --disable-silent-rules
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot}%{_libdir} -name '*.la' -delete
rm -rf %{buildroot}%{_infodir}

%check
make %{?_smp_mflags} check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING.LESSER
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/*.so.*

%changelog
* Tue Nov 21 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.3.1-1
- Auto-upgrade to 1.3.1 - Azure Linux 3.0 - package upgrades

* Mon Oct 11 2021 Andrew Phelps <anphel@microsoft.com> 1.2.1-1
- Update to version 1.2.1

* Mon Sep 28 2020 Ruying Chen <v-ruyche@microsoft.com> 1.1.0-6
- Provide libmpc-devel

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 1.1.0-5
- Added %%license line automatically

* Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> 1.1.0-4
- Renaming mpc to libmpc

* Tue Apr 07 2020 Paul Monson <paulmon@microsoft.com> 1.1.0-3
- Add #Source0. License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.1.0-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Mon Sep 10 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 1.1.0-1
- Update to version 1.1.0

* Mon Oct 03 2016 ChangLee <changLee@vmware.com> 1.0.3-3
- Modified check

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.3-2
- GA - Bump release of all rpms

* Tue Jan 12 2016 Anish Swaminathan <anishs@vmware.com>  1.0.3-1
- Update version.

* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 1.0.2-1
- Initial build. First version
