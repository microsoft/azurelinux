Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:		jbig2dec
Version:	0.19
Release:	3%{?dist}
Summary:	A decoder implementation of the JBIG2 image compression format 
License:	AGPLv3+
URL:		http://jbig2dec.sourceforge.net/
Source0:	https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs952/%{name}-%{version}.tar.gz
Requires:	%{name}-libs = %{version}-%{release}
BuildRequires:	libtool
BuildRequires:	libpng-devel

%description
jbig2dec is a decoder implementation of the JBIG2 image compression format.
JBIG2 is designed for lossy or lossless encoding of 'bilevel' (1-bit
monochrome) images at moderately high resolution, and in particular scanned
paper documents. In this domain it is very efficient, offering compression
ratios on the order of 100:1.

%package libs 
Summary:	A decoder implementation of the JBIG2 image compression format

%description libs 
jbig2dec is a decoder implementation of the JBIG2 image compression format.
JBIG2 is designed for lossy or lossless encoding of 'bilevel' (1-bit
monochrome) images at moderately high resolution, and in particular scanned
paper documents. In this domain it is very efficient, offering compression
ratios on the order of 100:1.

This package provides the shared jbig2dec library.

%package devel
Summary:	Static library and header files for development with jbig2dec
Requires:	%{name}-libs = %{version}-%{release}

%description devel
jbig2dec is a decoder implementation of the JBIG2 image compression format.
JBIG2 is designed for lossy or lossless encoding of 'bilevel' (1-bit
monochrome) images at moderately high resolution, and in particular scanned
paper documents. In this domain it is very efficient, offering compression
ratios on the order of 100:1.

This package is only needed if you plan to develop or compile applications
which requires the jbig2dec library.


%prep
%autosetup


%build
autoreconf -i
%configure
make %{?_smp_mflags}


%install
make DESTDIR=%{buildroot} install
rm -f %{buildroot}%{_libdir}/*.a
rm -f %{buildroot}%{_libdir}/*.la

%ldconfig_scriptlets libs


%files
%doc CHANGES COPYING LICENSE README
%{_bindir}/jbig2dec
%{_mandir}/man?/jbig2dec.1*

%files devel
%doc CHANGES COPYING LICENSE README
%{_includedir}/jbig2.h
%{_libdir}/libjbig2dec.so
%{_libdir}/pkgconfig/%{name}.pc

%files libs
%doc CHANGES COPYING LICENSE README
%{_libdir}/libjbig2dec.so.0
%{_libdir}/libjbig2dec.so.0.0.0



%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.19-3
- Initial CBL-Mariner import from Fedora 33 (license: MIT).

* Fri Sep 18 2020 Michael J Gruber <mjg@fedoraproject.org> - 0.19-2
- remove ABI patch (and coordinate builds)

* Thu Sep 17 2020 Anna Khaitovich <akhaitov@redhat.com> - 0.19-1
- Rebase to 0.19

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 08 2020 Michael J Gruber <mjg@fedoraproject.org> - 0.18-3
- build with libpng

* Wed Jul 08 2020 Nikola Forró <nforro@redhat.com> - 0.18-2
- fix License

* Mon May 11 2020 Michael J Gruber <mjg@fedoraproject.org> - 0.18-1
- rebase to 0.18 (bz #1818706)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Dec 14 2019 Michael J Gruber <mjg@fedoraproject.org> - 0.17-3
- require exact libs version
- clean up white space

* Sat Nov 09 2019 Michael J Gruber <mjg@fedoraproject.org> - 0.17-2
- restore ABI-compatibilty (#1770160)

* Thu Nov 07 2019 Michael J Gruber <mjg@fedoraproject.org> - 0.17-1
- bugfix release (bz #1761919)

* Thu Aug 15 2019 Michael J Gruber <mjg@fedoraproject.org> - 0.16-1
- rebase to 0.16 (bz #1741605)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Sep 18 2018 Owen Taylor <otaylor@redhat.com> - 0.14-4
- Handle both compressed and uncompressed man pages

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Nov 11 2017 Michael J Gruber <mjg@fedoraproject.org> - 0.14-1
- update to 0.14 (bugfix release)

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.13-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu May 11 2017 Pavel Zhukov <landgraf@fedoraproject.org> - 0.13.4
- Add fix for CVE-2017-7976 (#1443898)

* Wed May 03 2017 Pavel Zhukov <pzhukov@redhat.com> - 0.13-3
- Prevent segserv due to int overflow (#1443898)

* Tue Mar 07 2017 Pavel Zhukov <landgraf@fedoraproject.org> - 0.13-1
- New release 0.13

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Nov 27 2015 Pavel Zhukov <landgraf@fedoraproject.org> - 0.12-2
- New release (#1208076)
- Require autotools

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Mar 23 2013 Pavel Zhukov <landgraf@fedoraproject.org> - 0.11-7
- Add ARM64 patch

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 12 2011 Pavel Zhukov <landgraf@fedoraproject.org> - 0.11-2.fc14
- Fixed some spec errors

* Tue Jan 11 2011 Pavel Zhukov <landgraf@fedoraproject.org> - 0.11-1.fc14
- Initial package
