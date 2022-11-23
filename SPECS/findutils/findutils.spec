Summary:        This package contains programs to find files
Name:           findutils
Version:        4.8.0
Release:        4%{?dist}
License:        GPLv3+
URL:            http://www.gnu.org/software/findutils
Group:          Applications/File
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://ftp.gnu.org/gnu/findutils/%{name}-%{version}.tar.xz
Requires:       libselinux
BuildRequires:  libselinux-devel
Conflicts:      toybox

# Required to unblock automatic BR resolution for some Python packages.
Provides:       /usr/bin/find

%description
These programs are provided to recursively search through a
directory tree and to create, maintain, and search a database
(often faster than the recursive find, but unreliable if the
database has not been recently updated).

%package lang
Summary: Additional language files for findutils
Group:   Applications/File
Requires: %{name} = %{version}-%{release}
%description lang
These are the additional language files of findutils

%prep
%setup -q

%build
./configure \
    --prefix=%{_prefix} \
    --localstatedir=%{_sharedstatedir}/locate \
    --disable-silent-rules
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
install -vdm 755 %{buildroot}/bin
mv -v %{buildroot}%{_bindir}/find %{buildroot}/bin
sed -i 's/find:=${BINDIR}/find:=\/bin/' %{buildroot}%{_bindir}/updatedb
rm -rf %{buildroot}%{_infodir}
%find_lang %{name}

%check
make %{?_smp_mflags} check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
/bin/find
%{_bindir}/*
%{_libexecdir}/*
%{_mandir}/*/*

%files lang -f %{name}.lang
%defattr(-,root,root)

%changelog
* Wed Nov 23 2022 Chris PeBenito <chpebeni@microsoft.com> 4.8.0-4
- Force rebuild to address missing SELinux features.
* Wed Mar 23 2022 Chris PeBenito <chpebeni@microsoft.com> 4.8.0-3
- Add missing (Build)Requires needed to enable SELinux support.
* Mon Feb 14 2022 Pawel Winogrodzki <pawelwi@microsoft.com> 4.8.0-2
- Adding "Provides: /usr/bin/find".
* Fri Oct 22 2021 Andrew Phelps <anphel@microsoft.com> 4.8.0-1
- Update to version 4.8.0
- License verified
* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 4.6.0-7
- Added %%license line automatically
* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 4.6.0-6
- Initial CBL-Mariner import from Photon (license: Apache2).
* Sun Sep 09 2018 Alexey Makhalov <amakhalov@vmware.com> 4.6.0-5
- Fix compilation issue against glibc-2.28
* Mon Oct 02 2017 Alexey Makhalov <amakhalov@vmware.com> 4.6.0-4
- Added conflicts toybox
* Tue May 02 2017 Anish Swaminathan <anishs@vmware.com> 4.6.0-3
- Add lang package.
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.6.0-2
- GA - Bump release of all rpms
* Tue Apr 26 2016 Anish Swaminathan <anishs@vmware.com> 4.6.0-1
- Updated to version 4.6.0
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 4.4.2-1
- Initial build. First version
