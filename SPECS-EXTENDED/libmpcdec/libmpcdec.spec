Vendor:         Microsoft Corporation
Distribution:   Azure Linux

Summary: Musepack audio decoding library
Name:	 libmpcdec
Version: 1.2.6
Release: 26%{?dist}

License: BSD 
URL: 	 https://www.musepack.net/
Source0: https://files.musepack.net/source/libmpcdec-%{version}.tar.bz2

BuildRequires:  gcc-c++
BuildRequires: gcc
BuildRequires: sed

%description
Musepack is an audio compression format with a strong emphasis on high quality.
It's not lossless, but it is designed for transparency, so that you won't be
able to hear differences between the original wave file and the much smaller
MPC file.
It is based on the MPEG-1 Layer-2 / MP2 algorithms, but has rapidly developed
and vastly improved and is now at an advanced stage in which it contains
heavily optimized and patentless code.

%package devel
Summary: Development files for the Musepack audio decoding library
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
%{summary}.


%prep
%setup -q

#hack out hard-coded undesirable compiler flags
sed -i.cflags -e 's|-O3 -fomit-frame-pointer||g' configure


%build
%configure --disable-static

%make_build


%install
%make_install

#Unpackaged files
rm -fv $RPM_BUILD_ROOT%{_libdir}/lib*.la


%ldconfig_scriptlets

%files
%doc AUTHORS ChangeLog README
%license COPYING
%{_libdir}/libmpcdec.so.5*

%files devel
%{_includedir}/mpcdec/
%{_libdir}/libmpcdec.so


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.2.6-26
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.6-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.6-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.6-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.6-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Mar 07 2018 Rex Dieter <rdieter@fedoraproject.org> - 1.2.6-21
- .spec cleanup
- BR: gcc
- use %%ldconfig_scriptlets %%license %%make_build %%make_install
- drop undesirable cflags

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.6-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.6-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.6-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.6-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.6-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.6-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.6-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.6-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.6-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 04 2013 Rex Dieter <rdieter@fedoraproject.org> 1.2.6-11
- -devel: tighten dep using %%{?_isa}
- %%files: tighten file lists

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 08 2008 Rex Dieter <rdieter@fedoraproject.org> 1.2.6-4
- respin (gcc43)

* Sat Aug 25 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.2.6-3
- respin (BuildID)

* Wed Jun 06 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.2.6-2
- fix %%files (docs/html is no more)

* Wed Jun 06 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.2.6-1
- libmpcdec-1.2.6

* Tue Aug 29 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.2.2-4
- fc6 respin

* Wed Aug 09 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.2.2-3
- fc6 respin

* Sat Apr 01 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.2.2-2
- License: BSD

* Thu Jan 19 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.2.2-1
- libmpcdec-1.2.2

* Thu Jan 19 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.1-2
- cleanup

* Fri Jun 17 2005 Mihai Maties <mihai@xcyb.org> 1.1-1
- update to 1.1
- changed license to BSD
- updated the spec to use autotools

* Fri Nov 26 2004 Matthias Saou <https://freshrpms.net/> 1.0.2-1
- Initial RPM release.
- Include the mandatory copy of the LGPL (there is none in the sources...).

