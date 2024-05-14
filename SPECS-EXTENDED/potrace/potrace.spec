Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:		potrace
Version:	1.16
Release:	3%{?dist}
Summary:	Transform bitmaps into vector graphics
# README defines license as GPLv2+
License:	GPLv2+
URL:		https://potrace.sourceforge.net
Source0:	https://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
# Documentation
Source1:	https://potrace.sourceforge.net/potrace.pdf
Source2:	https://potrace.sourceforge.net/potracelib.pdf

BuildRequires:	gcc
BuildRequires:	zlib-devel

%description
Potrace is a utility for tracing a bitmap, which means, transforming a bitmap 
into a smooth, scalable image. The input is a bitmap (PBM, PGM, PPM, or BMP
format), and the default output is an encapsulated PostScript file (EPS).
A typical use is to create EPS files from scanned data, such as company or
university logos, handwritten notes, etc. The resulting image is not "jaggy"
like a bitmap, but smooth. It can then be rendered at any resolution.

Potrace can currently produce the following output formats: EPS, PostScript,
PDF, SVG (scalable vector graphics), Xfig, Gimppath, and PGM (for easy
antialiasing). Additional backends might be added in the future.

Mkbitmap is a program distributed with Potrace which can be used to pre-process
the input for better tracing behavior on greyscale and color images.


%package devel
Summary:	Potrace development library and headers
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the potrace development library and headers.


%package doc
Summary:	Documentation on how to use the potrace library

BuildArch:	noarch


%description doc
This package contains documentation for the potrace algorithm and the potrace
library.

%prep
%setup -q
cp -a %{SOURCE1} .
cp -a %{SOURCE2} .

%build
%configure --enable-shared --disable-static \
 --enable-metric --with-libpotrace --with-pic
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
find %{buildroot} -name *.la -exec rm -rf {} \;

# Get rid of installed copy of placement.pdf
rm -rf %{buildroot}%{_docdir}/%{name}

%files
%doc AUTHORS ChangeLog COPYING NEWS README doc/placement.pdf
%{_bindir}/potrace
%{_bindir}/mkbitmap
%{_libdir}/libpotrace.so.*
%{_mandir}/man1/potrace.1*
%{_mandir}/man1/mkbitmap.1*

%files devel
%{_libdir}/libpotrace.so
%{_includedir}/potracelib.h

%files doc
%doc potrace.pdf potracelib.pdf

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.16-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Sep 28 2019 Susi Lehtola <jussilehtola@fedoraproject.org> - 1.16-1
- Update to 1.16.

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.15-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.15-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 28 2018 Susi Lehtola <jussilehtola@fedoraproject.org> - 1.15-3
- Added gcc buildrequires.

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Aug 05 2017 Susi Lehtola <jussilehtola@fedoraproject.org> - 1.15-1
- Update to 1.15.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Feb 22 2017 Susi Lehtola <jussilehtola@fedoraproject.org> - 1.14-1
- Update to 1.14.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Nov 14 2015 Susi Lehtola <jussilehtola@fedoraproject.org> - 1.13-2
- Bump spec due to buildsystem problems.

* Fri Oct 23 2015 Susi Lehtola <jussilehtola@fedoraproject.org> - 1.13-1
- Update to 1.13.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Mar 24 2015 Susi Lehtola <jussilehtola@fedoraproject.org> - 1.12-1
- Update to 1.12.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed May 15 2013 Susi Lehtola <jussilehtola@fedoraproject.org> - 1.11-2
- Support for 64 bit ARM architecture (BZ #926364).

* Wed Feb 20 2013 Susi Lehtola <jussilehtola@fedoraproject.org> - 1.11-1
- Update to 1.11.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Aug 21 2011 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.10-1
- Update to 1.10.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 30 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.9-1
- Update to 1.9.

* Thu Aug 06 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.8-4
- Corrected license tag.

* Mon Aug 03 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.8-3
- Added missing BuildRequires.

* Mon Aug 03 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.8-2
- Adjusted descriptions as per review comments. 

* Mon Aug 03 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.8-1
- First release.
