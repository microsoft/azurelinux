# We don't have support for mingw in azurelinux
%bcond_with mingw
 
Name:          tesseract
Version:       5.5.1
Release:       3%{?dist}
Summary:       Raw OCR Engine
Vendor:        Microsoft Corporation
Distribution:  Azure Linux 
License:       Apache-2.0
URL:           https://github.com/tesseract-ocr/%{name}
Source0:       https://github.com/tesseract-ocr/tesseract/archive/%{version}%{?pre:-%pre}/%{name}-%{version}%{?pre:-%pre}.tar.gz
 
# Fix library name case
# Build training libs statically
Patch1:        tesseract_cmake.patch
# Don't assume neon available on arm64/aarch64
Patch2:        tesseract_neon.patch
 
 
BuildRequires: cmake
BuildRequires: libcurl-devel
BuildRequires: gcc-c++
BuildRequires: giflib-devel
BuildRequires: leptonica-devel
BuildRequires: libicu-devel
BuildRequires: libjpeg-turbo-devel
BuildRequires: libtool
BuildRequires: libtiff-devel
BuildRequires: libwebp-devel
BuildRequires: pango-devel
BuildRequires: /usr/bin/asciidoc
BuildRequires: /usr/bin/xsltproc
 
%if %{with mingw}
BuildRequires: mingw32-curl
BuildRequires: mingw32-filesystem
BuildRequires: mingw32-gcc-c++
BuildRequires: mingw32-giflib
BuildRequires: mingw32-binutils
BuildRequires: mingw32-icu
BuildRequires: mingw32-leptonica
BuildRequires: mingw32-libgomp
BuildRequires: mingw32-libjpeg-turbo
BuildRequires: mingw32-libtiff
BuildRequires: mingw32-libwebp
BuildRequires: mingw32-pango
 
BuildRequires: mingw64-curl
BuildRequires: mingw64-filesystem
BuildRequires: mingw64-gcc-c++
BuildRequires: mingw64-giflib
BuildRequires: mingw64-binutils
BuildRequires: mingw64-icu
BuildRequires: mingw64-leptonica
BuildRequires: mingw64-libgomp
BuildRequires: mingw64-libjpeg-turbo
BuildRequires: mingw64-libtiff
BuildRequires: mingw64-libwebp
BuildRequires: mingw64-pango
%endif
 
Requires:      %{name}-libs%{?_isa} = %{version}-%{release}
 
 
%global _description %{expand:
A commercial quality OCR engine originally developed at HP between 1985 and
1995. In 1995, this engine was among the top 3 evaluated by UNLV. It was
open-sourced by HP and UNLV in 2005.}
 
%description %_description
 
%package devel
Summary:       Development files for %{name}
Requires:      %{name}-libs%{?_isa} = %{version}-%{release}
 
%description devel %_description
The %{name}-devel package contains header file for
developing applications that use %{name}.
 
 
%package libs
Summary:       Shared libraries for %{name}
Conflicts:     %{name} < 5.4.1-4
Requires:      %{name}-common = %{version}-%{release}
 
%description libs %_description
The %{name}-libs package contains shared libraries
for %{name}.
 
 
%package common
Summary:       Configuration files for ${name}
Conflicts:     %{name} < 5.5.0-5
BuildArch:     noarch
 
%description common %_description
The %{name}-common package contains configuration files for %{name}.
 
 
%package tools
Summary:       Training tools for %{name}
Requires:      %{name}%{?_isa} = %{version}-%{release}
 
%description tools %_description
The %{name}-tools package contains tools for training %{name}.
 
%if %{with mingw}

%package -n mingw32-%{name}
Summary:       MinGW Windows tesseract-ocr library
BuildArch:     noarch
 
%description -n mingw32-%{name}
MinGW Windows tesseract-ocr library.
 
 
%package -n mingw32-%{name}-tools
Summary:       MinGW Windows tesseract-ocr library tools
Requires:      mingw32-%{name} = %{version}-%{release}
BuildArch:     noarch
 
%description -n mingw32-%{name}-tools
MinGW Windows tesseract-ocr library tools.
 
 
%package -n mingw64-%{name}
Summary:       MinGW Windows tesseract-ocr library
BuildArch:     noarch
 
%description -n mingw64-%{name}
MinGW Windows tesseract-ocr library.
 
 
%package -n mingw64-%{name}-tools
Summary:       MinGW Windows tesseract-ocr library tools
Requires:      mingw64-%{name} = %{version}-%{release}
BuildArch:     noarch
 
%description -n mingw64-%{name}-tools
MinGW Windows tesseract-ocr library tools.
 
%endif
 
%{?mingw_debug_package}
 
 
%prep
%autosetup -p1 -n %{name}-%{version}%{?pre:-%pre}
 
 
%build
mkdir build
cd build
# Native build
%cmake .. -DCMAKE_INSTALL_LIBDIR=%{_lib} -DTESSDATA_PREFIX=%{_datadir}/%{name}
%cmake_build
# Manually build manfiles, cmake does not build them
man_xslt=http://docbook.sourceforge.net/release/xsl/current/manpages/docbook.xsl
for file in ../doc/*.asc; do
    asciidoc -b docbook -d manpage -o - $file | XML_CATALOG_FILES=%{_sysconfdir}/xml/catalog xsltproc --nonet -o ${file/.asc/} $man_xslt -
done
 
%if %{with mingw}
# MinGW build
MINGW32_CMAKE_ARGS=-DTESSDATA_PREFIX=%{mingw32_datadir}/%{name} \
MINGW64_CMAKE_ARGS=-DTESSDATA_PREFIX=%{mingw64_datadir}/%{name}
%mingw_cmake -DSW_BUILD=OFF -DLEPT_TIFF_RESULT=1
%mingw_make_build
%endif
 
 
%install
cd build
%cmake_install
mkdir -p %{buildroot}%{_mandir}/{man1,man5}/
cp -a ../doc/*.1 %{buildroot}%{_mandir}/man1/
cp -a ../doc/*.5 %{buildroot}%{_mandir}/man5/
 
%if %{with mingw}
%mingw_make_install
%mingw_debug_install_post
%endif
 
 
%files
%license LICENSE
%doc AUTHORS ChangeLog README.md
%{_bindir}/%{name}
%{_mandir}/man1/tesseract.1*
 
%files devel
%{_includedir}/%{name}
%{_libdir}/lib%{name}.so
%{_libdir}/libcommon_training.a
%{_libdir}/libunicharset_training.a
%{_libdir}/cmake/%{name}/
%{_libdir}/pkgconfig/%{name}.pc
 
%files libs
%{_libdir}/lib%{name}.so.5.5
%{_libdir}/lib%{name}.so.%{version}
 
%files common
%license LICENSE
%{_datadir}/%{name}/
 
%files tools
%{_bindir}/ambiguous_words
%{_bindir}/classifier_tester
%{_bindir}/cntraining
%{_bindir}/combine_lang_model
%{_bindir}/combine_tessdata
%{_bindir}/dawg2wordlist
%{_bindir}/lstmeval
%{_bindir}/lstmtraining
%{_bindir}/merge_unicharsets
%{_bindir}/mftraining
%{_bindir}/set_unicharset_properties
%{_bindir}/shapeclustering
%{_bindir}/text2image
%{_bindir}/unicharset_extractor
%{_bindir}/wordlist2dawg
%{_mandir}/man1/ambiguous_words.1*
%{_mandir}/man1/classifier_tester.1*
%{_mandir}/man1/cntraining.1*
%{_mandir}/man1/combine_lang_model.1*
%{_mandir}/man1/combine_tessdata.1*
%{_mandir}/man1/dawg2wordlist.1*
%{_mandir}/man1/lstmeval.1*
%{_mandir}/man1/lstmtraining.1*
%{_mandir}/man1/merge_unicharsets.1*
%{_mandir}/man1/mftraining.1*
%{_mandir}/man1/set_unicharset_properties.1*
%{_mandir}/man1/shapeclustering.1*
%{_mandir}/man1/text2image.1*
%{_mandir}/man1/unicharset_extractor.1*
%{_mandir}/man1/wordlist2dawg.1*
%{_mandir}/man5/unicharambigs.5.gz*
%{_mandir}/man5/unicharset.5.gz*
 
%if %{with mingw}
%files -n mingw32-%{name}
%license LICENSE
%{mingw32_bindir}/libtesseract-55.dll
%{mingw32_includedir}/tesseract/
%{mingw32_libdir}/libtesseract.dll.a
%{mingw32_libdir}/libcommon_training.a
%{mingw32_libdir}/libunicharset_training.a
%{mingw32_libdir}/pkgconfig/tesseract.pc
%{mingw32_libdir}/cmake/%{name}/
%{mingw32_datadir}/%{name}/
 
%files -n mingw32-%{name}-tools
%{mingw32_bindir}/*.exe
 
%files -n mingw64-%{name}
%license LICENSE
%{mingw64_bindir}/libtesseract-55.dll
%{mingw64_includedir}/tesseract/
%{mingw64_libdir}/libtesseract.dll.a
%{mingw64_libdir}/libcommon_training.a
%{mingw64_libdir}/libunicharset_training.a
%{mingw64_libdir}/pkgconfig/tesseract.pc
%{mingw64_libdir}/cmake/%{name}/
%{mingw64_datadir}/%{name}/
 
%files -n mingw64-%{name}-tools
%{mingw64_bindir}/*.exe
%endif
 
 
%changelog
* Tue Nov 11 2025 Sandeep Karambelkar <skarambelkar@microsoft.com> - 5.5.1-1
- Initial Azure Linux import from Fedora 42 (license: MIT).
- Modified for building in azurelinux and upgraded to 5.5.1 version
- License verified

* Wed Aug 06 2025 František Zatloukal <fzatlouk@redhat.com> - 5.5.1-3
- Rebuilt for icu 77.1
 
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild
 
* Thu May 29 2025 Sandro Mani <manisandro@gmail.com> - 5.5.1-1
- Update to 5.5.1
 
* Mon Apr 21 2025 Alessandro Astone <ales.astone@gmail.com>
- Split config files into common subpackage (rhbz#2350549).
 
* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild
 
* Fri Dec 06 2024 Sandro Mani <manisandro@gmail.com> - 5.5.0-3
- Rebuild (mingw-icu)
 
* Fri Dec 06 2024 Sandro Mani <manisandro@gmail.com> - 5.5.0-2
- Rebuild (mingw-icu)
 
* Mon Nov 11 2024 Sandro Mani <manisandro@gmail.com> - 5.5.0-1
- Update to 5.5.0
 
* Sat Oct 05 2024 Neal Gompa <ngompa@fedoraproject.org> - 5.4.1-5
- Fix upgrade path for package split
 
* Mon Sep 30 2024 Neal Gompa <ngompa@fedoraproject.org> - 5.4.1-4
- Rebuild for ffmpeg 7
 
* Mon Sep 23 2024 Michel Lind <salimma@fedoraproject.org> - 5.4.1-3
- Correctly set the soversion based on SemVer properties
  Backport of upstream PR#4319 from Neal Gompa (ngompa)
- Split shared libraries into their own -libs subpackage
 
* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild
 
* Thu Jun 13 2024 Sandro Mani <manisandro@gmail.com> - 5.4.1-1
- Update to 5.4.1
 
* Thu Jun 06 2024 Sandro Mani <manisandro@gmail.com> - 5.4.0-1
- Update to 5.4.0
 
* Mon Feb 05 2024 Sandro Mani <manisandro@gmail.com> - 5.3.4-4
- Rebuild (icu)
 
* Wed Jan 31 2024 Pete Walter <pwalter@fedoraproject.org> - 5.3.4-3
- Rebuild for ICU 74
 
* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild
 
* Sun Jan 21 2024 Sandro Mani <manisandro@gmail.com> - 5.3.4-1
- Update to 5.3.4
 
* Sat Oct 07 2023 Sandro Mani <manisandro@gmail.com> - 5.3.3-1
- Update to 5.3.3
 
* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild
 
* Tue Jul 18 2023 Sandro Mani <manisandro@gmail.com> - 5.3.2-2
- Rebuild (mingw-icu)
 
* Thu Jul 13 2023 Sandro Mani <manisandro@gmail.com> - 5.3.2-1
- Update to 5.3.2
 
* Tue Jul 11 2023 František Zatloukal <fzatlouk@redhat.com> - 5.3.1-2
- Rebuilt for ICU 73.2
 
* Mon Apr 03 2023 Sandro Mani <manisandro@gmail.com> - 5.3.1-1
- Update to 5.3.1
 
* Mon Mar 20 2023 Vitaly Zaitsev <vitaly@easycoding.org> - 5.3.0-6
- Backported GCC 13 build fix. Fixed FTBFS on Fedora 38+.
 
* Fri Feb 03 2023 FeRD (Frank Dana) <ferdnyc@gmail.com> - 5.3.0-5
- Add patch from upstream to fix pkg-config libdir value
 
* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild
 
* Tue Jan 03 2023 Sandro Mani <manisandro@gmail.com> - 5.3.0-3
- Rebuild (mingw-icu)
 
* Sat Dec 31 2022 Pete Walter <pwalter@fedoraproject.org> - 5.3.0-2
- Rebuild for ICU 72
 
* Fri Dec 23 2022 Sandro Mani <manisandro@gmail.com> - 5.3.0-1
- Update to 5.3.0
 
* Wed Dec 21 2022 Sandro Mani <manisandro@gmail.com> - 5.2.0-6
- Rebuild (leptonica)
 
* Fri Sep 23 2022 Sandro Mani <manisandro@gmail.com> - 5.2.0-5
- Backport patch to restore equality between cmake and autotools generated
  pkgconfig file
 
* Fri Aug 05 2022 Sandro Mani <manisandro@gmail.com> - 5.2.0-4
- Rebuild (icu)
 
* Mon Aug 01 2022 Frantisek Zatloukal <fzatlouk@redhat.com> - 5.2.0-3
- Rebuilt for ICU 71.1
 
* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild
 
* Thu Jul 07 2022 Sandro Mani <manisandro@gmail.com> - 5.2.0-1
- Update to 5.2.0
 
* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 5.1.0-3
- Rebuild with mingw-gcc-12
 
* Fri Mar 11 2022 Sandro Mani <manisandro@gmail.com> - 5.1.0-2
- Build training tool libraries statically
 
* Wed Mar 02 2022 Sandro Mani <manisandro@gmail.com> - 5.1.0-1
- Update to 5.1.0
 
* Fri Feb 25 2022 Sandro Mani <manisandro@gmail.com> - 5.0.1-5
- Bump as F36 needs another rebuild
 
* Thu Feb 24 2022 Sandro Mani <manisandro@gmail.com> - 5.0.1-4
- Make mingw subpackages noarch
 
* Sat Feb 19 2022 Sandro Mani <manisandro@gmail.com> - 5.0.1-3
- Add mingw subpackage
 
* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild
 
* Sat Jan 08 2022 Sandro Mani <manisandro@gmail.com> - 5.0.1-1
- Update to 5.0.1
 
* Fri Dec 17 2021 Sandro Mani <manisandro@gmail.com> - 5.0.0-3
- Switch back to autotools
 
* Wed Dec 15 2021 Sandro Mani <manisandro@gmail.com> - 5.0.0-2
- Also install training libraries
 
* Fri Dec 10 2021 Sandro Mani <manisandro@gmail.com> - 5.0.0-1
- Update to 5.0.0
 
* Wed Nov 17 2021 Sandro Mani <manisandro@gmail.com> - 4.1.3-1
- Update to 4.1.7
 
* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild
 
* Thu May 20 2021 Pete Walter <pwalter@fedoraproject.org> - 4.1.1-6
- Rebuild for ICU 69
 
* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild
 
* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild
 
* Sat May 16 2020 Pete Walter <pwalter@fedoraproject.org> - 4.1.1-3
- Rebuild for ICU 67
 
* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild
 
* Fri Dec 27 2019 Sandro Mani <manisandro@gmail.com> - 4.1.1-1
- Update to 4.1.1
 
* Fri Nov 01 2019 Pete Walter <pwalter@fedoraproject.org> - 4.1.0-2
- Rebuild for ICU 65
 
* Sun Jul 28 2019 Sandro Mani <manisandro@gmail.com> - 4.1.0-1
- Update to 4.1.0
 
* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild
 
* Tue Jul 23 2019 Sandro Mani <manisandro@gmail.com> - 4.0.0-6
- Add Requires: tesseract-langpack-eng
 
* Mon Jul 22 2019 Sandro Mani <manisandro@gmail.com> - 4.0.0-5
- Drop langpack and script subpackages, moved to separate tesseract-tessdata package
 
* Mon Jul 01 2019 Sandro Mani <manisandro@gmail.com> - 4.0.0-4
- Fix -frk subpackage description (#1721228)
 
* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild
 
* Wed Jan 23 2019 Pete Walter <pwalter@fedoraproject.org> - 4.0.0-2
- Rebuild for ICU 63
 
* Tue Nov 13 2018 Sandro Mani <manisandro@gmail.com> - 4.0.0-1
- Update to 4.0.0
 
* Tue Sep 25 2018 Sandro Mani <manisandro@gmail.com> - 4.0.0-0.3.beta.4
- Update to 4.0.0-beta.4
 
* Sat Aug 25 2018 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 3.05.02-1
- Update to latest version
- Fix descriptions of language packs
 
* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.05.01-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild
 
* Tue Jul 10 2018 Pete Walter <pwalter@fedoraproject.org> - 3.05.01-8
- Rebuild for ICU 62
 
* Mon Apr 30 2018 Pete Walter <pwalter@fedoraproject.org> - 3.05.01-7
- Rebuild for ICU 61.1
 
* Mon Feb 19 2018 Sandro Mani <manisandro@gmail.coM> - 3.05.01-6
- Add missing BR: gcc-c++, make
 
* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.05.01-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild
 
* Thu Nov 30 2017 Pete Walter <pwalter@fedoraproject.org> - 3.05.01-4
- Rebuild for ICU 60.1
 
* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.05.01-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild
 
* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.05.01-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild
 
* Sat Jun 03 2017 Sandro Mani <manisandro@gmail.com> - 3.05.01-1
- Update to 3.05.01
 
* Tue Feb 21 2017 Sandro Mani <manisandro@gmail.com> - 3.05.00-1
- Update to 3.05.00
 
* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.04.01-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild
 
* Tue Jan 03 2017 Adam Williamson <awilliam@redhat.com> - 3.04.01-3
- Rebuild (to fix behaviour on big-endian arches after leptonica endianness fix)
 
* Fri Apr 15 2016 David Tardon <dtardon@redhat.com> - 3.04.01-2
- rebuild for ICU 57.1
 
* Fri Feb 19 2016 Sandro Mani <manisandro@gmail.com> - 3.04.01-1
- Update to 3.04.01
 
* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.04.00-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild
 
* Tue Jan 26 2016 Sandro Mani <manisandro@gmail.com> - 3.04.00-5
- Rebuild (leptonica)
 
* Tue Jan 26 2016 Sandro Mani <manisandro@gmail.com> - 3.04.00-4
- Rebuild (leptonica)
 
* Mon Jan 25 2016 Parag Nemade <pnemade AT redhat DOT com> - 3.04.00-3
- Added virtual provides to follow langpacks naming guidelines
- Added Supplements tag for new way of langpacks installation
 
* Wed Oct 28 2015 David Tardon <dtardon@redhat.com> - 3.04.00-2
- rebuild for ICU 56.1
 
* Sat Sep 12 2015 Sandro Mani <manisandro@gmail.com> - 3.04.00-1
- Update to 3.04.00
 
* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.03-0.6.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild
 
* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 3.03-0.5.rc1
- Rebuilt for GCC 5 C++11 ABI change
 
* Mon Jan 26 2015 David Tardon <dtardon@redhat.com> - 3.03-0.4.rc1
- rebuild for ICU 54.1
 
* Tue Aug 26 2014 David Tardon <dtardon@redhat.com> - 3.03-0.3.rc1
- rebuild for ICU 53.1
 
* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.03-0.2.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild
 
* Tue Aug 12 2014 Sandro Mani <manisandro@gmail.com> - 3.03-0.1.rc1
- Update to v3.03-rc1
 
* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.02.02-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild
 
* Thu Mar 27 2014 Karol Trzcionka <karlik at fedoraproject.org> - 3.02.02-3
- Fix rhbz#1037350 (-Werror=format-security)
- Add OSD data
- Remove BuildRoot tag
 
* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.02.02-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild
 
* Sat Apr 27 2013 Karol Trzcionka <karlik at fedoraproject.org> - 3.02.02-1
- Update to v3.02.02
- Apply pkgconfig patch rhbz#904806
 
* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.01-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild
 
* Sat Oct 06 2012 Karol Trzcionka <karlik at fedoraproject.org> - 3.01-1
- Update to v3.01
- Add manual pages
- Add BRs leptonica, automake
 
* Tue Jul 31 2012 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.00-6
- Fix FTBFS with g++ 4.7
 
* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.00-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild
 
* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.00-4
- Rebuilt for c++ ABI breakage
 
* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.00-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild
 
* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.00-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild
 
* Tue Nov 16 2010 Karol Trzcionka <karlikt at gmail.com> - 3.00-1
- Update to v3.00
- Remove static libs and add dynamic
 
* Wed Oct 21 2009 Karol Trzcionka <karlikt at gmail.com> - 2.04-1
- Update to v2.04
- Add static libraries to -devel subpackage
 
* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.03-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild
 
* Wed Mar 04 2009 Caolán McNamara <caolanm@redhat.com> - 2.03-3
- include stdio.h for snprintf
 
* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.03-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild
 
* Sun May 04 2008 Karol Trzcionka <karlikt at gmail.com> - 2.03-1
- Update to v2.03
* Sat Feb 09 2008 Karol Trzcionka <karlikt at gmail.com> - 2.01-2
- Rebuild for gcc43
* Fri Sep 07 2007 Karol Trzcionka <karlikt at gmail.com> - 2.01-1
- Upgrade to v2.01
* Tue Aug 21 2007 Karol Trzcionka <karlikt at gmail.com> - 2.00-1
- Upgrade to v2.00
* Thu Mar 22 2007 Karol Trzcionka <karlikt at gmail.com> - 1.04-1
- Change url and source
- Update to v1.04
- Make patch bases on upstream's v1.04b
- Change compilefix patch
- Adding -devel subpackage
* Thu Mar 22 2007 Karol Trzcionka <karlikt at gmail.com> - 1.03-2
- Including patch bases on cvs
* Tue Feb 13 2007 Karol Trzcionka <karlikt at gmail.com> - 1.03-1
- Update to v1.03
* Sat Jan 27 2007 Karol Trzcionka <karlikt at gmail.com> - 1.02-3
- Update BRs
- Fix x86_64 compile
* Sat Dec 30 2006 Karol Trzcionka <karlikt at gmail.com> - 1.02-2
- Fixed rpmlint warning in SRPM
* Fri Dec 29 2006 Karol Trzcionka <karlikt at gmail.com> - 1.02-1
- Initial Release
