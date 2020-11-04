Summary:        Programs for compressing and decompressing files
Name:           gzip
Version:        1.9
Release:        4%{?dist}
License:        GPLv3+
URL:            http://www.gnu.org/software/gzip
Group:          Applications/File
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:	    http://ftp.gnu.org/gnu/gzip/%{name}-%{version}.tar.xz
%define sha1 gzip=0249ad4c4ca1f144714e8e21b6d0db24651fc122
%description
The Gzip package contains programs for compressing and
decompressing files.
%prep
%setup -q
%build
#make some fixes required by glibc-2.28:
sed -i 's/IO_ftrylockfile/IO_EOF_SEEN/' lib/*.c
echo "#define _IO_IN_BACKUP 0x100" >> lib/stdio-impl.h

%configure --disable-silent-rules
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
install -vdm 755 %{buildroot}%{_bindir}
rm -rf %{buildroot}%{_infodir}

%check
make %{?_smp_mflags} check

%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/*
%{_mandir}/*/*
%changelog
* Sat May 09 00:21:13 PST 2020 Nick Samson <nisamson@microsoft.com> - 1.9-4
- Added %%license line automatically

* Fri Mar 03 2020 Jon Slobodzian <joslobo@microsoft.com> 1.9-3
- Fixed reference URL. Verified license.
* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.9-2
- Initial CBL-Mariner import from Photon (license: Apache2).
* Wed Sep 12 2018 Anish Swaminathan <anishs@vmware.com> 1.9-1
- Update to version 1.9
* Sat Sep 08 2018 Alexey Makhalov <amakhalov@vmware.com> 1.8-2
- Fix compilation issue against glibc-2.28
* Fri Mar 24 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.8-1
- Upgrading to version 1.8
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.6-2
- GA - Bump release of all rpms
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 1.6-1
- Initial build. First version