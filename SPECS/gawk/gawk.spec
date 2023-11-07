Summary:        Contains programs for manipulating text files
Name:           gawk
Version:        5.2.2
Release:        1%{?dist}
License:        GPLv3
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/File
URL:            https://www.gnu.org/software/gawk
Source0:        https://ftp.gnu.org/gnu/gawk/%{name}-%{version}.tar.xz
Requires:       gmp
Requires:       mpfr
Requires:       readline >= 7.0
Provides:       /bin/awk
Provides:       /bin/gawk
Provides:       awk

%description
The Gawk package contains programs for manipulating text files.

%prep
%setup -q

%build
%configure \
    --prefix=%{_prefix} \
    --sysconfdir=%{_sysconfdir } \
    --disable-silent-rules
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
install -vdm 755 %{buildroot}%{_defaultdocdir}/%{name}-%{version}
cp -v doc/{awkforai.txt,*.{eps,pdf,jpg}} %{buildroot}%{_defaultdocdir}/%{name}-%{version}
rm -rf %{buildroot}%{_infodir}
find %{buildroot} -type f -name "*.la" -delete -print
%find_lang %{name}

%check
# Skip the timeout test, which is unreliable on our (vm) build machines
sed -i 's/ timeout / /' test/Makefile
sed -i 's/ pty1 / /' test/Makefile

# Generate locale for `en_US.iso88591` which is required for ptest
# Ideally it should have been present. Investigate if its a `chroot` only issue
%{_sbindir}/locale-gen.sh
make %{?_smp_mflags} check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
%license COPYING
%{_bindir}/*
%{_libdir}/%{name}/*
%{_includedir}/*
%{_libexecdir}/*
%{_datarootdir}/awk/*
%{_defaultdocdir}/%{name}-%{version}/*
%{_mandir}/*/*
%{_sysconfdir}/profile.d/gawk.csh
%{_sysconfdir}/profile.d/gawk.sh

%changelog
* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.2.2-1
- Auto-upgrade to 5.2.2 - Azure Linux 3.0 - package upgrades

* Mon Oct 16 2023 Neha Agarwal <nehaagarwal@microsoft.com> - 5.1.1-1
- Update to v5.1.1 to fix CVE-2023-4156

* Tue Feb 15 2022 Muhammad Falak <mwani@microsoft.com> - 5.1.0-2
- Generate locale `en_US.iso88591` in `%check` section to enable ptest
- Lint spec

* Fri Nov 05 2021 Andrew Phelps <anphel@microsoft.com> - 5.1.0-1
- Update to version 5.1.0
- License verified

* Tue Jan 05 2021 Andrew Phelps <anphel@microsoft.com> - 4.2.1-4
- Skip timeout test

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 4.2.1-3
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 4.2.1-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Mon Sep 17 2018 Sujay G <gsujay@vmware.com> - 4.2.1-1
- Bump version to 4.2.1

* Wed Apr 05 2017 Danut Moraru <dmoraru@vmware.com> - 4.1.4-1
- Upgrade to version 4.1.4

* Wed Jan 18 2017 Dheeraj Shetty <dheerajs@vmware.com> - 4.1.3-4
- Bump up for depending on readline 7.0

* Sun Dec 18 2016 Alexey Makhalov <amakhalov@vmware.com> - 4.1.3-3
- Provides /bin/awk

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 4.1.3-2
- GA - Bump release of all rpms

* Tue Jan 12 2016 Xiaolin Li <xiaolinl@vmware.com> - 4.1.3-1
- Updated to version 4.1.3

* Fri Jun 19 2015 Alexey Makhalov <amakhalov@vmware.com> - 4.1.0-2
- Provide /bin/gawk.

* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> - 4.1.0-1
- Initial build. First version
