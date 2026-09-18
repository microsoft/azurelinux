# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%undefine __cmake_in_source_build

Summary: A PDF file viewer for the X Window System
Name: xpdf
Version: 4.06
Release: 1%{?dist}
License: (GPL-2.0-only OR GPL-3.0-only) AND BSD-3-Clause
Epoch: 1
Url: https://www.xpdfreader.com/

Source0: https://dl.xpdfreader.com/%{name}-%{version}.tar.gz
Source1: https://dl.xpdfreader.com/%{name}-%{version}.tar.gz.sig
Source2: https://www.xpdfreader.com/gpg-key.txt
%if 0%{?fedora}
# We have to pull the following CMap files out due to non-free license.
# CMap/Adobe-GB1-UCS2
# CMap/GBK-EUC-UCS2
# CMap/GBpc-EUC-UCS2
# CMap/GBpc-EUC-UCS2C
# Source3: http://www.xpdfreader.com/dl/xpdf-chinese-simplified.tar.gz
Source3: xpdf-chinese-simplified-2023-dec-05-NOCMAP.tar.gz
# CMap/Adobe-CNS1-UCS2
# CMap/B5pc-UCS2
# CMap/B5pc-UCS2C
# CMap/ETen-B5-UCS2
# Source4: http://www.xpdfreader.com/dl/xpdf-chinese-traditional.tar.gz
Source4: xpdf-chinese-traditional-2020-dec-22-NOCMAP.tar.gz
# CMap/90ms-RKSJ-UCS2
# CMap/90pv-RKSJ-UCS2
# CMap/90pv-RKSJ-UCS2C
# CMap/Adobe-Japan1-UCS2
# Source5: http://www.xpdfreader.com/dl/xpdf-japanese.tar.gz
Source5: xpdf-japanese-2020-dec-22-NOCMAP.tar.gz
# CMap/Adobe-Korea1-UCS2
# CMap/KSCms-UHC-UCS2
# CMap/KSCpc-EUC-UCS2
# CMap/KSCpc-EUC-UCS2C
# Source6: http://www.xpdfreader.com/dl/xpdf-korean.tar.gz
Source6: xpdf-korean-2023-dec-05-NOCMAP.tar.gz
# cyrillic and thai don't have CMap files to worry about.
Source7: ftp://ftp.foolabs.com/pub/xpdf/xpdf-cyrillic-2011-aug-15.tar.gz
# thai: 2025-08-13
Source8: https://dl.xpdfreader.com/xpdf-thai.tar.gz
Source10: xpdf.desktop
Source11: xpdf.png
Source12: ftp://ftp.foolabs.com/pub/xpdf/xpdf-arabic-2011-aug-15.tar.gz
Source13: ftp://ftp.foolabs.com/pub/xpdf/xpdf-greek-2011-aug-15.tar.gz
Source14: ftp://ftp.foolabs.com/pub/xpdf/xpdf-hebrew-2011-aug-15.tar.gz
Source15: ftp://ftp.foolabs.com/pub/xpdf/xpdf-latin2-2011-aug-15.tar.gz
Source16: ftp://ftp.foolabs.com/pub/xpdf/xpdf-turkish-2011-aug-15.tar.gz
%endif

Patch3: xpdf-4.01-ext.patch
Patch9: xpdf-3.00-papersize.patch
Patch11: xpdf-4.01-crash.patch
Patch12: xpdf-4.01-64bit.patch
Patch15: xpdf-3.04-nocmap.patch
Patch25: xpdf-4.00-versionedlib.patch
Patch26: xpdf-4.06-urw-base35-fonts.patch
Patch28: xpdf-4.04-GlobalParams-null-fix.patch
# https://forum.xpdfreader.com/viewtopic.php?t=42521
Patch29: xpdf-4.04-shared-xpdf-lib.patch

# Security patches
# Based on
# https://gitlab.freedesktop.org/poppler/poppler/commit/cdb7ad95f7c8fbf63ade040d8a07ec96467042fc
# https://gitlab.freedesktop.org/poppler/poppler/commit/bf4aae25a244b1033a2479b9a8f633224f7d5de5
Patch101: xpdf-4.02-CVE-2019-12360.patch
# merged in 4.06
# Patch102: xpdf-4.05-CVE-2024-4141.patch

# Debian patches
Patch200: xpdf-4.06-permissions.patch
# Proper stream encoding on 64bit platforms
Patch203: fix-444648.dpatch

Requires: urw-fonts
Requires: xdg-utils
Requires: poppler-utils
Requires: xorg-x11-fonts-ISO8859-1-75dpi
Requires: xorg-x11-fonts-ISO8859-1-100dpi
Requires: qt5-qtsvg

%if 0%{?fedora}
BuildRequires: qt5-qtbase-devel, cmake
BuildRequires: freetype-devel >= 2.1.7
BuildRequires: fontconfig-devel
BuildRequires: desktop-file-utils
BuildRequires: libpaper-devel
BuildRequires: libpng-devel
BuildRequires: libXpm-devel
BuildRequires: cups-devel
%else
BuildRequires: gcc-c++
BuildRequires: cmake
BuildRequires: freetype-devel >= 2.1.7
BuildRequires: fontconfig-devel
BuildRequires: libpng-devel
%endif
# for %%gpgverify
BuildRequires: gnupg2

Provides:  %{name}-chinese-simplified = %{version}-%{release}
Obsoletes: %{name}-chinese-simplified
Provides:  %{name}-chinese-traditional = %{version}-%{release}
Obsoletes: %{name}-chinese-traditional
Provides:  %{name}-korean = %{version}-%{release}
Obsoletes: %{name}-korean
Provides:  %{name}-japanese = %{version}-%{release}
Obsoletes: %{name}-japanese

Requires: %{name}-libs%{_isa} = %{epoch}:%{version}-%{release}

%description
Xpdf is an X Window System based viewer for Portable Document Format
(PDF) files. Xpdf is a small and efficient program which uses
standard X fonts.

%package devel
%if 0%{?fedora}
Requires: %{name}%{_isa} = %{epoch}:%{version}-%{release}
Requires: libpaper-devel
%endif
Requires: fontconfig-devel, freetype-devel
Requires: libpng-devel
Summary: Development files for xpdf libraries

%description devel
Development files for xpdf libraries.

%package libs
Summary: Libraries from xpdf

%description libs
Libraries from xpdf.

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%if 0%{?fedora} 
%setup -q -a 3 -a 4 -a 5 -a 6 -a 7 -a 8 -a 12 -a 13 -a 14 -a 15 -a 16
%else
%setup -q
%endif
%patch -P3 -p1 -b .ext
%patch -P9 -p1 -b .papersize
%patch -P11 -p1 -b .crash
%patch -P12 -p1 -b .alloc
%patch -P25 -p1 -b .versionedlib
%patch -P26 -p1 -b .urw-font-fix
%patch -P28 -p1 -b .GlobalParams-null-fix
%patch -P29 -p1 -b .shared-xpdf-lib

# security patches
%patch -P101 -p1 -b .CVE-2019-12360
# %%patch -P102 -p1 -b .CVE-2024-4141

# debian patches
%patch -P200 -p1 -b .permissions
%patch -P203 -p1 -b .64bit-stream

# Comment out unused urlCommand option
sed -i 's|urlCommand|#urlCommand|g' doc/sample-xpdfrc

%build
find -name "*orig" | xargs rm -f

%if 0%{?fedora}
# This may seem pointless, but in the unlikely event that _sysconfdir != /etc ...
for file in doc/*.1 doc/*.5 xpdf-*/README; do
  sed -i -e 's:/etc/xpdfrc:%{_sysconfdir}/xpdfrc:g' $file
done
# Same action for _datadir.
for file in xpdf-*/README xpdf-*/add-to-xpdfrc; do
  sed -i -e 's:/usr/share/:%{_datadir}/:g' $file
  sed -i -e 's:/usr/local/share/:%{_datadir}/:g' $file
done
%endif

export CFLAGS="%{optflags} -fPIC"
export CXXFLAGS="%{optflags} -Wno-deprecated -fPIC"
%cmake -DMULTITHREADED=ON -DOPI_SUPPORT=ON -DXPDFWIDGET_PRINTING=1 -DSYSTEM_XPDFRC="%{_sysconfdir}/xpdfrc" -DCMAKE_POLICY_VERSION_MINIMUM=3.5

%cmake_build
%if 0%{?fedora}
%cmake_build --target xpdf
%endif

%install
%if 0%{?fedora}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/xpdf/arabic \
         $RPM_BUILD_ROOT%{_datadir}/xpdf/chinese-simplified \
         $RPM_BUILD_ROOT%{_datadir}/xpdf/chinese-traditional \
         $RPM_BUILD_ROOT%{_datadir}/xpdf/cyrillic \
         $RPM_BUILD_ROOT%{_datadir}/xpdf/greek \
         $RPM_BUILD_ROOT%{_datadir}/xpdf/hebrew \
         $RPM_BUILD_ROOT%{_datadir}/xpdf/japanese \
         $RPM_BUILD_ROOT%{_datadir}/xpdf/korean \
         $RPM_BUILD_ROOT%{_datadir}/xpdf/latin2 \
         $RPM_BUILD_ROOT%{_datadir}/xpdf/thai \
         $RPM_BUILD_ROOT%{_datadir}/xpdf/turkish \
         $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps

%cmake_install
%endif

# Y U NO INSTALL LIBS?!?
mkdir -p $RPM_BUILD_ROOT%{_libdir}
cp -a %{_vpath_builddir}/fofi/libfofi.so* $RPM_BUILD_ROOT%{_libdir}
cp -a %{_vpath_builddir}/goo/libgoo.so* $RPM_BUILD_ROOT%{_libdir}
cp -a %{_vpath_builddir}/splash/libsplash.so* $RPM_BUILD_ROOT%{_libdir}
cp -a %{_vpath_builddir}/xpdf/libxpdfcore.so* $RPM_BUILD_ROOT%{_libdir}

# headers
mkdir -p $RPM_BUILD_ROOT%{_includedir}/xpdf/fofi
mkdir -p $RPM_BUILD_ROOT%{_includedir}/xpdf/goo
mkdir -p $RPM_BUILD_ROOT%{_includedir}/xpdf/splash
cp -a fofi/*.h $RPM_BUILD_ROOT%{_includedir}/xpdf/fofi/
cp -a goo/*.h $RPM_BUILD_ROOT%{_includedir}/xpdf/goo/
cp -a splash/*.h $RPM_BUILD_ROOT%{_includedir}/xpdf/splash/
cp -a xpdf/*.h $RPM_BUILD_ROOT%{_includedir}/xpdf/
cp -a %{__cmake_builddir}/aconf.h $RPM_BUILD_ROOT%{_includedir}/xpdf/

%if 0%{?fedora}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications/
%if 0%{?rhel} > 5 || 0%{?fedora}
desktop-file-install            \
%else
desktop-file-install --vendor "fedora"                  \
%endif
        --dir $RPM_BUILD_ROOT%{_datadir}/applications   \
        --add-category X-Fedora                         \
        %{SOURCE10}
install -m 0644 %{SOURCE11} $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps/xpdf.png

cp -pr xpdf-arabic/* $RPM_BUILD_ROOT%{_datadir}/xpdf/arabic/
cp -pr xpdf-chinese-simplified/* $RPM_BUILD_ROOT%{_datadir}/xpdf/chinese-simplified/
cp -pr xpdf-chinese-traditional/* $RPM_BUILD_ROOT%{_datadir}/xpdf/chinese-traditional/
cp -pr xpdf-cyrillic/* $RPM_BUILD_ROOT%{_datadir}/xpdf/cyrillic/
cp -pr xpdf-greek/* $RPM_BUILD_ROOT%{_datadir}/xpdf/greek/
cp -pr xpdf-hebrew/* $RPM_BUILD_ROOT%{_datadir}/xpdf/hebrew/
cp -pr xpdf-japanese/* $RPM_BUILD_ROOT%{_datadir}/xpdf/japanese/
cp -pr xpdf-korean/* $RPM_BUILD_ROOT%{_datadir}/xpdf/korean/
cp -pr xpdf-latin2/* $RPM_BUILD_ROOT%{_datadir}/xpdf/latin2/
cp -pr xpdf-thai/* $RPM_BUILD_ROOT%{_datadir}/xpdf/thai/
cp -pr xpdf-turkish/* $RPM_BUILD_ROOT%{_datadir}/xpdf/turkish/

# poppler provides all utilities now
# http://bugzilla.redhat.com/bugzillA/SHow_bug.cgi?id=177446
# https://bugzilla.redhat.com/bugzilla/show_bug.cgi?id=219032
%if 0%{?rhel} > 6 || 0%{?fedora}
rm $RPM_BUILD_ROOT%{_bindir}/pdfdetach
%endif
rm $RPM_BUILD_ROOT%{_bindir}/pdffonts
rm $RPM_BUILD_ROOT%{_bindir}/pdfimages
rm $RPM_BUILD_ROOT%{_bindir}/pdfinfo
rm $RPM_BUILD_ROOT%{_bindir}/pdftohtml
rm $RPM_BUILD_ROOT%{_bindir}/pdftops
rm $RPM_BUILD_ROOT%{_bindir}/pdftotext
%if 0%{?rhel} > 5 || 0%{?fedora} > 6
rm $RPM_BUILD_ROOT%{_bindir}/pdftoppm
rm $RPM_BUILD_ROOT%{_mandir}/man1/pdftoppm.1*
%endif
%if 0%{?rhel} > 6 || 0%{?fedora}
rm $RPM_BUILD_ROOT%{_mandir}/man1/pdfdetach.1*
%endif
rm $RPM_BUILD_ROOT%{_mandir}/man1/pdffonts.1*
rm $RPM_BUILD_ROOT%{_mandir}/man1/pdfimages.1*
rm $RPM_BUILD_ROOT%{_mandir}/man1/pdfinfo.1*
rm $RPM_BUILD_ROOT%{_mandir}/man1/pdftohtml.1*
rm $RPM_BUILD_ROOT%{_mandir}/man1/pdftops.1*
rm $RPM_BUILD_ROOT%{_mandir}/man1/pdftotext.1*

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/xpdf/
for i in arabic chinese-simplified chinese-traditional cyrillic greek hebrew japanese korean latin2 thai turkish; do
     mv $RPM_BUILD_ROOT%{_datadir}/%{name}/$i/README README.$i
     mv $RPM_BUILD_ROOT%{_datadir}/%{name}/$i/add-to-xpdfrc $RPM_BUILD_ROOT%{_sysconfdir}/xpdf/add-to-xpdfrc.$i
done

# xpdfrc cleanup
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/
cp -a doc/sample-xpdfrc $RPM_BUILD_ROOT%{_sysconfdir}/xpdfrc
sed -i -e 's:/usr/local/share/:%{_datadir}/:g' $RPM_BUILD_ROOT%{_sysconfdir}/xpdfrc
%endif

%ldconfig_scriptlets

%if 0%{?fedora}
%files
%license COPYING COPYING3
%doc CHANGES README README.*
%{_bindir}/xpdf
%{_bindir}/pdftopng
%{_libdir}/lib*.so.*
%{_mandir}/man?/pdftopng*
%{_mandir}/man?/xpdf*
%if 0%{?rhel} > 5 || 0%{?fedora} > 6
# Do Nothing.
%else
%{_bindir}/pdftoppm
%{_mandir}/man?/pdftoppm*
%endif
%if 0%{?rhel}
%if 0%{?rhel} < 7
%{_bindir}/pdfdetach
%{_mandir}/man?/pdfdetach*
%endif
%endif
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/xpdfrc
%dir %{_sysconfdir}/xpdf
%lang(ar) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/xpdf/add-to-xpdfrc.arabic
%lang(zh_CN) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/xpdf/add-to-xpdfrc.chinese-simplified
%lang(zh_TW) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/xpdf/add-to-xpdfrc.chinese-traditional
%lang(el) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/xpdf/add-to-xpdfrc.greek
%lang(iw) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/xpdf/add-to-xpdfrc.hebrew
%lang(ja) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/xpdf/add-to-xpdfrc.japanese
%lang(ko) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/xpdf/add-to-xpdfrc.korean
%lang(th) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/xpdf/add-to-xpdfrc.thai
%lang(tr) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/xpdf/add-to-xpdfrc.turkish
# cyrillic and latin2 are not langs, many languages are cyrillic/latin2
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/xpdf/add-to-xpdfrc.cyrillic
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/xpdf/add-to-xpdfrc.latin2
%{_datadir}/icons/hicolor/48x48/apps/xpdf.png
%dir %{_datadir}/xpdf
%{_datadir}/applications/*
%lang(ar) %{_datadir}/xpdf/arabic
%lang(zh_CN) %{_datadir}/xpdf/chinese-simplified
%lang(zh_TW) %{_datadir}/xpdf/chinese-traditional
%lang(el) %{_datadir}/xpdf/greek
%lang(iw) %{_datadir}/xpdf/hebrew
%lang(ja) %{_datadir}/xpdf/japanese
%lang(ko) %{_datadir}/xpdf/korean
%lang(th) %{_datadir}/xpdf/thai
%lang(tr) %{_datadir}/xpdf/turkish
%{_datadir}/xpdf/cyrillic
%{_datadir}/xpdf/latin2
%endif

%files devel
%{_includedir}/xpdf/
%{_libdir}/lib*.so

%files libs
%{_libdir}/lib*.so.*

%changelog
* Tue Nov 18 2025 Tom Callaway <spot@fedoraproject.org> - 1:4.06-1
- update to 4.06

* Thu Jul 31 2025 Tom Callaway <spot@fedoraproject.org> - 1:4.05-8
- passing -DCMAKE_POLICY_VERSION_MINIMUM=3.5 to fix FTBFS with CMake4 (bz2381643)

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.05-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.05-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.05-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed May 29 2024 Tom Callaway <spot@fedoraproject.org> - 4.05-4
- apply fix for CVE-2024-4141, thanks to Petr Gajdos and Derek Noonburg

* Fri Apr  5 2024 Peter Lemenkov <lemenkov@gmail.com> - 4.05-3
- Verify GPG signature

* Thu Feb 29 2024 Tom Callaway <spot@fedoraproject.org> - 4.05-2
- update langpacks

* Tue Feb 27 2024 Than Ngo <than@redhat.com> - 4.05-1
- fixed bz#2263444, update to 4.05

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.04-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.04-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jun 16 2023 Than Ngo <than@redhat.com> - 1:4.04-9
- added ELN/RHEL conditions

* Fri Apr 28 2023 Tom Callaway <spot@fedoraproject.org> 1:4.04-8
- move libs to -libs subpackage to minimize dep footprint of texlive-pdftex (bz2188328)

* Tue Feb 21 2023 Than Ngo <than@redhat.com> - 4.04-7
- migrated to SPDX license

* Thu Feb 16 2023 Tom Callaway <spot@fedoraproject.org> - 1:4.04-6
- drop now unnecessary libpaper2 patch

* Mon Jan 30 2023 Tom Callaway <spot@fedoraproject.org> - 1:4.04-5
- pull in all the headers
- apply null fix for default var in GlobalParams()
- make a libxpdfcore for texlive-base to use

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.04-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Jan  8 2023 Tom Callaway <spot@fedoraproject.org> - 1:4.04-3
- fix build with libpaper2, rebuild for it

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.04-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Apr 22 2022 Tom Callaway <spot@fedoraproject.org> - 1:4.04-1
- update to 4.04

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.03-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.03-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Feb  2 2021 Tom Callaway <spot@fedoraproject.org> - 1:4.03-1
- update to 4.03

* Thu Jan 28 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.02-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.02-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 26 2020 Tom Callaway <spot@fedoraproject.org> - 1:4.02-4
- generate and apply fix based on poppler fix for CVE-2019-12360

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.02-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Dec  2 2019 Tom Callaway <spot@fedoraproject.org> - 1:4.02-2
- apply upstream fix for CVE-2019-17064

* Wed Oct 16 2019 Tom Callaway <spot@fedoraproject.org> - 1:4.02-1
- update to 4.02

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.01-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 22 2019 Tom Callaway <spot@fedoraproject.org> 1:4.01-1
- update to 4.01

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.00-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.00-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Apr 30 2018 Tom Callaway <spot@fedoraproject.org> - 1:4.00-7
- add Requires: qt5-qtsvg to ensure icons are shown

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.00-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Nov 27 2017 Tom Callaway <spot@fedoraproject.org> - 1:4.00-5
- enable printing support. I hate cmake. thanks to Henrique Martins.

* Mon Nov 13 2017 Tom Callaway <spot@fedoraproject.org> - 1:4.00-4
- tell xpdf where to find the system copy of xpdfrc
- comment out unused urlCommand option from xpdfrc

* Tue Nov  7 2017 Tom Callaway <spot@fedoraproject.org> - 1:4.00-3
- fix URW font handling (thanks to Yaakov Selkowitz)

* Wed Aug 23 2017 Tom Callaway <spot@fedoraproject.org> 1:4.00-2
- fix macro typo

* Wed Aug 16 2017 Tom Callaway <spot@fedoraproject.org> 1:4.00-1
- update to 4.00

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.04-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.04-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.04-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.04-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jul 27 2015 Tom Callaway <spot@fedoraproject.org> - 1:3.04-11
- fix output resolution of png file output (thanks to Kevin Farshaw, bz1246666)

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.04-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 11 2015 Tom Callaway <spot@fedoraproject.org> - 1:3.04-9
- RHEL 7 does not need pdfdetach

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1:3.04-8
- Rebuilt for GCC 5 C++11 ABI change

* Mon Jan 12 2015 Tom Callaway <spot@fedoraproject.org> - 1:3.04-7
- add BR: libXpm-devel, drop --with-gzip (no longer exists)

* Tue Dec  2 2014 Tom Callaway <spot@fedoraproject.org> - 1:3.04-6
- fix proper display of international strings in the title (bz 1169301)

* Fri Sep 12 2014 Tom Callaway <spot@fedoraproject.org> - 1:3.04-5
- fix .desktop file

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.04-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.04-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jun  3 2014 Tom Callaway <spot@fedoraproject.org> - 1:3.04-2
- fix "sharexpdf" typo in lang configs

* Thu May 29 2014 Tom Callaway <spot@fedoraproject.org> - 1:3.04-1
- update to 3.04
- update all patches, langpacks
- use motif instead of lesstif where possible
- fix pdftopng to install (not in poppler right now)

* Sun Sep 22 2013 Tom Callaway <spot@fedoraproject.org> - 1:3.03-8.1
- rhel still needs pdfdetach in xpdf

* Sun Sep 22 2013 Tom Callaway <spot@fedoraproject.org> - 1:3.03-8
- fix CVE-2012-2142
- fix issue with icon name in .desktop file (except on el5)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.03-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Feb 10 2013 Parag Nemade <paragn AT fedoraproject DOT org> - 1:3.03-6
- Remove vendor tag from desktop file as per https://fedorahosted.org/fesco/ticket/1077

* Wed Nov 14 2012 Tom Callaway <spot@fedoraproject.org> - 1:3.03-5
- fix desktop file to invoke xpdf with a file param (bz874644)

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.03-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri May 25 2012 Tom Callaway <spot@fedoraproject.org> - 1:3.03-3
- drop pdfdetach, poppler-utils has it now

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.03-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Aug 22 2011 Tom Callaway <spot@fedoraproject.org> - 1:3.03-1
- update to 3.03

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.02-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 21 2011 Tom Callaway <spot@fedoraproject.org> - 1:3.02-17
- Added pdftoppm for el5 or older, since it is not included in poppler-utils on el5
- Thanks to Ingvar Hagelund.

* Fri Oct 22 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 1:3.02-16
- apply xpdf-3.02pl5 security patch to fix:
  CVE-2010-3702, CVS-2010-3704

* Fri Oct 16 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1:3.02-15
- apply xpdf-3.02pl4 security patch to fix:
  CVE-2009-3603, CVE-2009-3604, CVE-2009-3605, CVE-2009-3606
  CVE-2009-3608, CVE-2009-3609

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.02-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Apr 16 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1:3.02-13
- apply xpdf-3.02pl3 security patch to fix:
  CVE-2009-0799, CVE-2009-0800, CVE-2009-1179, CVE-2009-1180
  CVE-2009-1181, CVE-2009-1182, CVE-2009-1183

* Wed Mar  4 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1:3.02-12
- add Requires: xorg-x11-fonts-ISO8859-1-100dpi (bz 485404)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.02-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 11 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1:3.02-10
- cleanup crash patch a bit (bz 483664)
- improve support for more mouse buttons (bz 483669)

* Wed Dec 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1:3.02-9
- apply debian patches

* Sun Sep 21 2008 Ville Skyttä <ville.skytta at iki.fi> - 1:3.02-8
- Fix Patch0:/%%patch mismatch.

* Thu Jun 19 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1:3.02-7
- add missing Requires: xorg-x11-fonts-ISO8859-1-75dpi

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1:3.02-6
- Autorebuild for GCC 4.3

* Wed Jan  2 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1:3.02-5
- use xdg-utils instead of htmlview (bz 313311)

* Fri Nov  9 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1:3.02-4
- resolve 372461, 372471, 372481

* Tue Aug 28 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1:3.02-3
- fix PDF printing on x86_64 (bz 253601)
- add mouse buttons 8 and 9 (bz 255401)
- add extra zoom types (bz 251855)
- rebuild for BuildID

* Mon Aug  6 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1:3.02-2
- fix font list parsing to squelch noise (bz 250709)
- cleanup add-to-xpdfrc files, update xpdfrc to include them by default

* Wed Aug  1 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1:3.02-1
- bump to 3.02
- patch in security fix
- add arabic, greek, hebrew, latin2, turkish lang support

* Mon Dec 18 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1:3.01-28
- Requires: poppler-utils

* Thu Dec 14 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1:3.01-27
- drop the xpdf-utils subpackage, poppler-utils ate it all

* Mon Sep 25 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1:3.01-26
- get rid of goo/vms_* since they have questionable licensing

* Mon Sep 25 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1:3.01-25
- patch thai/cyrillic files for proper pathing

* Mon Sep 25 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1:3.01-24
- get rid of non-free CMap files
- actually use thai/cyrillic sources
- patch out the references to using CMap files

* Mon Sep 25 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1:3.01-23
- new patch missed README files, fixed

* Mon Sep 25 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1:3.01-22
- use latest localized files
- fix redhat patch to work with new localized files

* Mon Sep 25 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1:3.01-21
- use sane cp flags
- remove hardcoded X-Red-Hat-Base from .desktop
- mark the extra config files with their lang
- get rid of unnecessary Requires post,postun

* Sun Sep 24 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1:3.01-20
- use the proper icon

* Sat Sep 23 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1:3.01-19
- get rid of unnecessary BR fileutils, findutils
- get rid of duplicate R poppler-utils on main package
- use _sysconfdir/xpdf hierarchy, own add-to-xpdfrc as config files
- README files for each lang should be doc files, rename with lang ext
- ensure that files reflect macro settings
- use _sysconfdir macro
- remove files without -rf
- no need for /etc/X11/applnk/Graphics
- update xpdf-3.01-redhat.patch accordingly

* Sat Sep 23 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1:3.01-18
- use t1lib
- remove non-utf8 character from old changelog
- put png icon in hicolor/48x48/apps
- use appropriate desktop scriptlets
- set vendor="fedora"
- move R:poppler-utils to xpdf-utils
- remove period from xpdf-utils summary
- add provides for everything we obsolete
- get rid of autoconf, Xprint patch, just pass --without-Xp-library
- add libpaper as BR

* Fri Sep 22 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1:3.01-17
- move to Fedora Extras, use desktop-file-install

* Wed Aug 09 2006 Than Ngo <than@redhat.com> 1:3.01-16
- fix #200608, install icon in the wrong dir

* Fri Jul 14 2006 Than Ngo <than@redhat.com> 1:3.01-15
- fix build problem with new freetype

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1:3.01-14.1
- rebuild

* Wed Jun 28 2006 Than Ngo <than@redhat.com> 1:3.01-14
- fix #197090, BR: autoconf

* Fri May  5 2006 Adam Jackson <ajackson@redhat.com> 1:3.01-13
- Remove spurious libXp dependency

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1:3.01-12.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Than Ngo <than@redhat.com> 3.01-12
- apply patch to fix buffer overflow issue in the xpdf codebase
  when handling splash images CVE-2006-0301 (#179423)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1:3.01-11.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Jan 23 2006 Than Ngo <than@redhat.com> 3.01-11
- add correct app-defaults directory #178545

* Wed Jan 18 2006 Ray Strode <rstrode@redhat.de> 3.01-10
- remove requires line in utils subpackage

* Wed Jan 18 2006 Ray Strode <rstrode@redhat.de> 3.01-9
- remove pdf command-line utilities and require poppler ones
  instead (bug 177446).

* Wed Jan 18 2006 Than Ngo <than@redhat.com> 3.01-8
- add new subpackage xpdf-utils

* Tue Jan 10 2006 Karsten Hopp <karsten@redhat.de> 3.01-7
- add patches to fix CVE-2005-3191 and CAN-2005-3193

* Mon Dec 12 2005 Than Ngo <than@redhat.com> 3.01-6 
- rebuilt against new openmotif-2.3

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov 09 2005 Than Ngo <than@redhat.com> 3.01-5
- add correct Simplified/Traditional Chinese fonts #170989

* Tue Nov 08 2005 Than Ngo <than@redhat.com> 3.01-4
- get rid of XFree86-devel

* Thu Oct 13 2005 Matthias Clasen <mclasen@redhat.com> 3.01-3
- don't use freetype internals

* Fri Oct 07 2005 Than Ngo <than@redhat.com> 3.01-2 
- apply upstream patch to fix resize/redraw bug #166569

* Thu Aug 18 2005 Than Ngo <than@redhat.com> 3.01-1
- update to 3.01

* Thu Aug 11 2005 Than Ngo <than@redhat.com> 3.00-24
- change Kochi fonts to Sazanami fonts #165678

* Tue Aug 09 2005 Than Ngo <than@redhat.com> 3.00-23
- apply patch to fix xpdf DoS, CAN-2005-2097 #163918

* Mon Jul 25 2005 Than Ngo <than@redhat.com> 3.00-22
- fix allocation size 64bit architectures

* Mon Jul 25 2005 Than Ngo <than@redhat.com> 3.00-21
- fix xpdf crash #163807 

* Mon Jun 13 2005 Than Ngo <than@redhat.com> 3.00-20
- urlCommand launches htmlview #160176
- fix gcc4 build problem

* Mon May 23 2005 Than Ngo <than@redhat.com> 3.00-19
- apply patch to fix texts in non-embedded cjk font disappear, (#158509)

* Sat Mar 05 2005 Than Ngo <than@redhat.com> 1:3.00-18
- rebuilt

* Thu Feb 10 2005 Than Ngo <than@redhat.com> 1:3.00-17
- More fixing of CAN-2004-0888 patch (bug #135393)

* Wed Jan 26 2005 Than Ngo <than@redhat.com> 1:3.00-16
- Add patch to fix handling CID font encodings in freetype version >= 2.1.8 (bug #135066)

* Thu Jan 20 2005 Than Ngo <than@redhat.com> 1:3.00-15
- Applied patch to fix CAN-2005-0064 (bug #145050)

* Wed Dec 22 2004 Tim Waugh <twaugh@redhat.com> 1:3.00-14
- Applied patch to fix CAN-2004-1125 (bug #143500).

* Mon Nov 29 2004 Than Ngo <than@redhat.com> 1:3.00-13
- set match as default psPaperSize #141131

* Tue Oct 26 2004 Than Ngo <than@redhat.com> 1:3.00-12
- bump release

* Tue Oct 26 2004 Than Ngo <than@redhat.com> 1:3.00-11
- don't link against t1lib, use freetype2 for rendering

* Thu Oct 21 2004 Than Ngo <than@redhat.com> 1:3.00-10
- apply patch to fix CAN-2004-0888

* Thu Oct 21 2004 Than Ngo <than@redhat.com> 1:3.00-9
- fix xpdf crash #136633

* Tue Oct 12 2004 Than Ngo <than@redhat.com> 1:3.00-8
- fix default fonts setting

* Mon Oct 11 2004 Than Ngo <than@redhat.com> 3.00-7
- fix locale issue #133911

* Thu Oct 07 2004 Than Ngo <than@redhat.com> 1:3.00-6
- Fix xpdf crash when selecting outline without page reference,
  thanks Ulrich Drepper, bz #134993

* Thu Jun 24 2004 Than Ngo <than@redhat.com> 1:3.00-5
- update t1lib upstream
- add cjk font patch, thanks to Yukihiro Nakai, bug #123540
- fix a bug in font rasterizer, bug #125559
- improve menue entry, bug #125850

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 20 2004 Than Ngo <than@redhat.com> 3.00-3
- better fix for building with freetype 2.1.7

* Tue Feb 17 2004 Than Ngo <than@redhat.com> 3.00-2 
- t1lib-5.0.1

* Tue Jan 27 2004 Than Ngo <than@redhat.com> 3.00-1
- 3.00 release
- add patch file to built with new freetype-2.1.7

* Mon Oct 13 2003 Than Ngo <than@redhat.com> 1:2.03-1
- 2.03
- remove xpdf-2.02pl1.patch, which is included in 2.03
- fix warning issue (bug #106313)
- fix huge memory leak, (bug #89552)

* Tue Jul 29 2003 Than Ngo <than@redhat.com> 1:2.02-9
- rebuild

* Tue Jul 29 2003 Than Ngo <than@redhat.com> 1:2.02-8
- add missing icon (bug #100780) 
- fix a bug xpdf resource

* Tue Jun 17 2003 Than Ngo <than@redhat.com> 2.02-7
- fixes a security hole

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon May  5 2003 Than Ngo <than@redhat.com> 2.02-4.1
- merge sub packages to main package (bug #87750)

* Fri May  2 2003 Than Ngo <than@redhat.com> 2.02-3.1
- don't install backup files

* Mon Mar 31 2003 Than Ngo <than@redhat.com> 2.02-2
- build with freetype in RHL, #79680
- unsafe temporary files, #79682
- add Xfree86-devel in buildprereq
- build with -O0 on ppc, gcc bug

* Tue Mar 25 2003 Than Ngo <than@redhat.com> 2.02-1
- 2.02
- adjust some patch files for 2.02

* Tue Feb 18 2003 Than Ngo <than@redhat.com> 2.01-8
- own /usr/share/xpdf,  #73983
- remove debug unused infos, #84197

* Tue Feb  4 2003 Than Ngo <than@redhat.com> 2.01-7
- fix #82634

* Mon Feb  3 2003 Than Ngo <than@redhat.com> 2.01-6
- fix #82633

* Mon Jan 27 2003 Than Ngo <than@redhat.com> 2.01-5
- added locale patch from ynakai@redhat.com, bug #82638

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Jan 20 2003 Than Ngo <than@redhat.com> 2.01-3
- Security fixes.

* Sun Dec  8 2002 Than Ngo <than@redhat.com> 2.01-2
- urlCommand launches htmlview (bug #76694)

* Fri Dec  6 2002 Than Ngo <than@redhat.com> 2.01-1
- update to 2.01

* Wed Nov  6 2002 Than Ngo <than@redhat.com> 2.00-1
- update to 2.00
- adapt a patch file for 2.00
- build against openmotif

* Fri Sep 20 2002 Than Ngo <than@redhat.com> 1.01-9
- Build against new freetype

* Mon Aug 26 2002 Than Ngo <than@redhat.com> 1.01-8
- add descriptive name (bug #71673)

* Sat Aug 10 2002 Elliot Lee <sopwith@redhat.com>
- rebuilt with gcc-3.2 (we hope)

* Wed Jul 24 2002 Than Ngo <than@redhat.com> 1.01-6
- desktop file issue (bug #69554)

* Tue Jul 23 2002 Tim Powers <timp@redhat.com> 1.01-5
- build using gcc-3.2-0.1

* Fri Jun 21 2002 Tim Powers <timp@redhat.com> 1.01-4
- automated rebuild

* Sun Jun 2 2002 Than Ngo <than@redhat.com> 1.01-3
- fix a bug in open file dialog (bug #39844)
- 1.01 handles Type 3 fonts (bug #48843)

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Harald Hoyer <harald@redhat.de> 1.01-1
- xpdf-1.01, freetype-2.0.9

* Sun Mar 17 2002 Than Ngo <than@redhat.com> 1.00-3
- rebuild

* Thu Feb 21 2002 Than Ngo <than@redhat.com> 1.00-2
- fix Bad 'urlCommand' (bug #59730)

* Tue Feb 05 2002 Than Ngo <than@redhat.com> 1.00-1
- update to 1.00 (bug #59239, #48904)
- remove some patch files, which are included in 1.00
- sub packages for chinese-simplified, chinese-traditional, japanese and korean

* Fri Jan 25 2002 Than Ngo <than@redhat.com> 0.93-4
- rebuild in rawhide

* Mon Nov 12 2001 Than Ngo <than@redhat.com> 0.93-2
- enable Chinese GB font support
- enable Chinese CNS font support
- enable use of FreeType 2

* Mon Oct 29 2001 Than Ngo <than@redhat.com> 0.93-1
- update to 0.93

* Wed Sep 12 2001 Tim Powers <timp@redhat.com>
- rebuild with new gcc and binutils

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Fri Apr 27 2001 Bill Nottingham <notting@redhat.com>
- rebuild for C++ exception handling on ia64

* Wed Mar 28 2001 Than Ngo <than@redhat.com>
- add german translation into desktop file
- move desktop file to /etc/X11/applnk/Graphics (Bug #32720)

* Tue Jan 02 2001 Than Ngo <than@redhat.com>
- added a default URL handler script with a corresponding definition
  in Xpdf, thanks to Michal Jaegermann <michal@harddata.com> (Bug #23112)

* Mon Dec 04 2000 Than Ngo <than@redhat.com>
- updated to 0.92 (Bug #16646)
- remove some patches, which included in xpdf-0.92

* Mon Oct 16 2000 Than Ngo <than@redhat.com>
- rebuild for 7.1

* Wed Oct 11 2000 Than Ngo <than@redhat.com>
- fix update problem (Bug #17924)

* Thu Aug 17 2000 Than Ngo <than@redhat.com>
- update to 0.91 (Bug #9961 and many major bugs) 

* Sun Aug 06 2000 Than Ngo <than@redhat.de>
- added swedish translation (Bug 15312)

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sun Jul  2 2000 Jakub Jelinek <jakub@redhat.com>
- Rebuild with new C++

* Fri Jun 16 2000 Than Ngo <than@redhat.de>
- enable Japanese font support

* Fri Jun 16 2000 Preston Brown <pbrown@redhat.com>
- FHS paths
- better .desktop entry file

* Tue Jun 06 2000 Than Ngo <than@redhat.de>
- fix xpdf crashes on some data streams (Bug# 10154) (thanks Derek)
- add %%defattr
- use rpm macros

* Tue May 23 2000 Ngo Than <than@redhat.de>
- fix problem with loading fonts

* Sun May 21 2000 Ngo Than <than@redhat.de>
- put man pages in /usr/share/man/*
- update t1lib-1.0.1

* Mon May 08 2000 Trond Eivind Glomsrod <teg@redhat.com>
- fixed URL

* Fri Feb 11 2000 Preston Brown <pbrown@redhat.com>
- build for inclusion in 6.2.

* Wed Feb 09 2000 Jakub Jelinek <jakub@redhat.com>
- include decryption patches

* Mon Feb 07 2000 Presto Brown <pbrown@redhat.com>
- rebuild to gzip man pages

* Mon Aug 30 1999 Preston Brown <pbrown@redhat.com>
- upgrade to xpdf 0.90, include t1lib Type1 rasterizer
- fix zapfdingbats font mapping issue

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 4)

* Wed Mar 17 1999 Preston Brown <pbrown@redhat.com>
- converted wmconfig to desktop entry

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Mon Nov 30 1998 Preston Brown <pbrown@redhat.com>
- updated to 0.80

* Fri Nov 06 1998 Preston Brown <pbrown@redhat.com>
- patched to compile with new, stricter egcs

* Tue May 05 1998 Cristian Gafton <gafton@redhat.com>
- updated to 0.7a

* Thu Nov 20 1997 Otto Hammersmith <otto@redhat.com>
- added changelog
- added wmconfig
