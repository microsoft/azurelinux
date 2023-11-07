Summary:        Reading, writing, and converting info pages
Name:           texinfo
Version:        7.0.3
Release:        1%{?dist}
License:        GPLv3+
URL:            https://www.gnu.org/software/texinfo/
Group:          Applications/System
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        http://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz
Provides:       info = %{version}-%{release}
Provides:       %{name}-tex = %{version}-%{release}
BuildRequires:  perl

Requires:       perl-libintl-perl

%description
The Texinfo package contains programs for reading, writing,
and converting info pages.

%prep
%setup -q

%build
# fix issue building with glibc 2.34:
sed -e 's/__attribute_nonnull__/__nonnull/' \
    -i gnulib/lib/malloc/dynarray-skeleton.c
%configure --disable-silent-rules
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
make DESTDIR=%{buildroot} TEXMF=%{_datarootdir}/texmf install-tex
rm -rf %{buildroot}%{_infodir}

%find_lang %{name} --all-name

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
%license COPYING
%exclude %{_bindir}/pdftexi2dvi
%exclude %{_bindir}/texi2dvi
%exclude %{_bindir}/texi2pdf
%{_bindir}/info
%{_bindir}/install-info
%{_bindir}/makeinfo
%{_bindir}/pod2texi
%{_bindir}/texi2any
%{_bindir}/texindex
%{_libdir}/texinfo/*
%{_mandir}/*/*
%dir %{_datarootdir}/texinfo
%{_datarootdir}/texinfo/*
%dir %{_datarootdir}/texmf
%{_datarootdir}/texmf/*

%changelog
* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 7.0.3-1
- Auto-upgrade to 7.0.3 - Azure Linux 3.0 - package upgrades

* Fri Oct 08 2021 Andrew Phelps <anphel@microsoft.com> 6.8-1
- Update to version 6.8
- Fix issue building with glibc 2.34
- Remove texinfo-perl-fix.patch

* Mon Sep 28 2020 Ruying Chen <v-ruyche@microsoft.com> 6.5-8
- Provide info and texinfo-tex

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 6.5-7
- Added %%license line automatically

* Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> 6.5-6
- Renaming perl-libintl to perl-libintl-perl
* Mon Apr 20 2020 Eric Li <eli@microsoft.com> 6.5-5
- Fix URL and Source0:, delete sha1. License verified.
* Wed Jan 22 2020 Henry Beberman <hebeberm@microsoft.com> 6.5-4
- Add missing Requires for perl-libintl to ensure the package exists for iso installs.
* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 6.5-3
- Initial CBL-Mariner import from Photon (license: Apache2).
* Fri Nov 02 2018 Anish Swaminathan <anishs@vmware.com> 6.5-2
- Fix texinfo issue with locales
- http://lists.gnu.org/archive/html/bug-texinfo/2018-06/msg00029.html
* Fri Sep 07 2018 Michelle Wang <michellew@vmware.com> 6.5-1
- Update version to 6.5.
* Fri May 05 2017 Xiaolin Li <xiaolinl@vmware.com> 6.3-3
- Excluded pdftexi2dvi, texi2dvi, texi2pdf from package,
- because these commands depend on installation of tex.
* Tue Apr 18 2017 Robert Qi <qij@vmware.com> 6.3-2
- Updated to version 6.3-2 due to perl build requires.
* Tue Mar 28 2017 Xiaolin Li <xiaolinl@vmware.com> 6.3-1
- Updated to version 6.3.
* Tue Oct 04 2016 ChangLee <changlee@vmware.com> 6.1-4
- Modified %check
* Mon Jun 27 2016 Divya Thaluru <dthaluru@vmware.com> 6.1-3
- Removed packaging of debug files
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 6.1-2
- GA - Bump release of all rpms
* Mon Feb 22 2016 Xiaolin Li <xiaolinl@vmware.com> 6.1-1
- Updated to version 6.1
* Tue Nov 10 2015 Xiaolin Li <xiaolinl@vmware.com> 5.2-3
- Handled locale files with macro find_lang
* Wed Jun 3 2015 Divya Thaluru <dthaluru@vmware.com> 5.2-2
- Removing perl-libintl package from run-time required packages
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 5.2-1
- Upgrade version
