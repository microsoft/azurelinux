Summary:        The GNU Database Manager
Name:           gdbm
Version:        1.23
Release:        1%{?dist}
License:        GPLv3+
URL:            http://www.gnu.org/software/gdbm
Group:          Applications/Databases
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://ftp.gnu.org/gnu/gdbm/%{name}-%{version}.tar.gz

%description
This is a disk file format database which stores key/data-pairs in
single files. The actual data of any record being stored is indexed
by a unique key, which can be retrieved in less time than if it was
stored in a text file.

%package lang
Summary:        Additional language files for gdbm
Group:          Applications/Databases
Requires:       %{name} = %{version}-%{release}
%description lang
These are the additional language files of gdbm

%package        devel
Summary:        Header and development files for gdbm
Requires:       %{name} = %{version}-%{release}
%description    devel
It contains the libraries and header files to create applications.

%prep
%setup -q

%build
./configure \
    --prefix=%{_prefix} \
    --enable-libgdbm-compat \
    --disable-silent-rules
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot}%{_libdir} -name '*.la' -delete
rm -rf %{buildroot}%{_infodir}
%find_lang %{name}

# create symlinks for compatibility
mkdir -p %{buildroot}/%{_includedir}/gdbm
ln -sf ../gdbm.h %{buildroot}/%{_includedir}/gdbm/gdbm.h
ln -sf ../ndbm.h %{buildroot}/%{_includedir}/gdbm/ndbm.h
ln -sf ../dbm.h %{buildroot}/%{_includedir}/gdbm/dbm.h

%check
make %{?_smp_mflags} check

%post   -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/*
%{_libdir}/*.so.*
%{_mandir}/man1/*

%files lang -f %{name}.lang
%defattr(-,root,root)

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/*.a
%{_includedir}/*
%{_mandir}/man3/*

%changelog
* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.23-1
- Auto-upgrade to 1.23 - Azure Linux 3.0 - package upgrades

* Fri Oct 22 2021 Andrew Phelps <anphel@microsoft.com> 1.21-1
- Update to version 1.21
- License verified

* Mon Oct 12 2020 Joe Schmitt <joschmit@microsoft.com> 1.18-4
- Symlink headers for compatibility.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.18-3
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.18-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Fri Sep 14 2018 Keerthana K <keerthanak@vmware.com> 1.18-1
- Update to version 1.18

* Fri Jun 23 2017 Xiaolin Li <xiaolinl@vmware.com> 1.13-3
- Add devel package.

* Tue May 02 2017 Anish Swaminathan <anishs@vmware.com> 1.13-2
- Add lang package.

* Wed Apr 05 2017 Danut Moraru <dmoraru@vmware.com> 1.13-1
- Upgrade gdbm to 1.13

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.11-2
- GA - Bump release of all rpms

* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 1.11-1
- Initial build.  First version
