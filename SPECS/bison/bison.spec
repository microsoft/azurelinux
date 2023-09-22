Summary:        Contains a parser generator
Name:           bison
Version:        3.7.6
Release:        2%{?dist}
License:        GPLv3+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Base
URL:            https://www.gnu.org/software/bison
Source0:        https://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz

BuildRequires:  flex
BuildRequires:  m4

Requires:       m4

Provides:       %{name}-runtime = %{version}-%{release}

%description
This package contains a parser generator

%prep
%setup -q

%build
#make some fixes required by glibc-2.28:
#sed -i 's/IO_ftrylockfile/IO_EOF_SEEN/' lib/*.c
#echo "#define _IO_IN_BACKUP 0x100" >> lib/stdio-impl.h

./configure \
    --prefix=%{_prefix} \
    --disable-silent-rules
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
rm -rf %{buildroot}%{_infodir}
%find_lang %{name} --all-name

# Remove yacc binary/man pages where they conflict with byacc
rm -f %{buildroot}/%{_bindir}/yacc
rm -f %{buildroot}/%{_mandir}/man1/yacc*

%check
make %{?_smp_mflags} check

%files -f %{name}.lang
%defattr(-,root,root)
%license COPYING
%{_bindir}/*
%{_libdir}/*.a
%{_datarootdir}/%{name}/*
%{_datarootdir}/aclocal/*
%{_mandir}/*/*
%{_docdir}/bison/*

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 3.7.6-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Fri Nov 05 2021 Andrew Phelps <anphel@microsoft.com> 3.7.6-1
- Update to version 3.7.6

* Thu Sep 23 2021 Pawel Winogrodzki <pawelwi@microsoft.com> 3.1-5
- Adding 'Provides' for 'bison-runtime'.

* Fri Aug 21 2020 Thomas Crain <thcrain@microsoft.com> 3.1-4
- Remove yacc command for compatibility with byacc package
- Remove sha hash
- License verified

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 3.1-3
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 3.1-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue Sep 18 2018 Tapas Kundu <tkundu@vmware.com> 3.1-1
- Updated to release 3.1

* Sun Sep 09 2018 Alexey Makhalov <amakhalov@vmware.com> 3.0.4-4
- Fix compilation issue against glibc-2.28

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.0.4-3
- GA - Bump release of all rpms

* Thu Apr 28 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.0.4-2
- Removed requires for flex

* Tue Feb 23 2016 Xiaolin Li <xiaolinl@vmware.com> 3.0.4-1
- Updated to version 3.0.4

* Tue Nov 10 2015 Xiaolin Li <xiaolinl@vmware.com> 3.0.2-3
- Handled locale files with macro find_lang

* Fri Jun 5 2015 Divya Thaluru <dthaluru@vmware.com> 3.0.2-2
- Adding m4, flex package to build and run time required package

* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 3.0.2-1
- Initial build. First version.
