Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Summary:    Small test program for liba52
Name:       a52dec
Version:    0.7.4
Release:    38%{?dist}
License:    GPLv2
URL:        https://liba52.sourceforge.net
Source0:    %{url}/files/%{name}-%{version}.tar.gz
Patch0:     a52dec-configure-optflags.patch
Patch1:     a52dec-0.7.4-rpath64.patch
Patch2:     liba52-silence.patch

BuildRequires: gcc

Requires:   liba52%{?_isa} = %{version}-%{release}
#Multilib transition
#Introduced in Fedora 26, can be dropped in Fedora 28
Obsoletes:  %{name} < 0.7.4-25


%package -n liba52
Summary:    A free ATSC A/52 stream decoder, also known as AC-3 or AC3
#Fix multilibs transition - introduced in f26
Obsoletes:  a52dec < 0.7.4-25
#Fix others 3rd part repos transition
Obsoletes:  a52dec-libs < 0.7.4-25
Provides:   a52dec-libs = %{version}-%{release}

%package -n liba52-devel
Summary:    Development files for liba52
Requires:   liba52%{?_isa} = %{version}-%{release}
Provides:   %{name}-devel = %{version}-%{release}
Obsoletes:  %{name}-devel < 0.7.4-25

%description
Small test program for liba52.

%description -n liba52
liba52 is a free library for decoding ATSC A/52 streams. The A/52
standard is used in a variety of applications, including digital
television and DVD. It is also known as AC-3 or AC3

%description -n liba52-devel
The liba52-devel package contains libraries and header files for
developing applications that use liba52-devel.


%prep
%autosetup -p1

sed -i -e 's/-prefer-non-pic/-prefer-pic/' \
  configure liba52/configure.incl

# Convert to utf-8
for file in AUTHORS; do
    iconv -f ISO-8859-1 -t UTF-8 -o $file.new $file && \
    touch -r $file $file.new && \
    mv $file.new $file
done


%build
%configure --enable-shared --disable-static
%make_build


%install
%make_install


%ldconfig_scriptlets -n liba52


%files
%exclude %{_libdir}/liba52.la
%doc AUTHORS ChangeLog HISTORY NEWS TODO
%{_bindir}/%{name}
%{_bindir}/extract_a52
%{_mandir}/man1/a52dec.1*
%{_mandir}/man1/extract_a52.1*

%files -n liba52
%license COPYING
%{_libdir}/liba52.so.*

%files -n liba52-devel
%doc doc/liba52.txt
%{_includedir}/%{name}
%{_libdir}/liba52.so


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.7.4-38
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.4-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.4-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.4-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jul 17 2018 Nicolas Chauvet <kwizart@gmail.com> - 0.7.4-34
- Add missng cc

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.4-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.4-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.7.4-31
- Switch to %%ldconfig_scriptlets

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.4-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.4-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Apr 07 2017 Nicolas Chauvet <kwizart@gmail.com> - 0.7.4-28
- Obsoletes at the same version see rhbz#1439690#c16

* Tue Apr 04 2017 Nicolas Chauvet <kwizart@gmail.com> - 0.7.4-27
- Fix others 3rd part repos

* Thu Mar 30 2017 Nicolas Chauvet <kwizart@gmail.com> - 0.7.4-26
- Fix multilibs transition

* Tue Mar 21 2017 Nicolas Chauvet <kwizart@gmail.com> - 0.7.4-25
- Fixup Obsoletes/Provides for the devel
- Use sed instead of perl to avoid a build dependency

* Mon Mar 20 2017 Nicolas Chauvet <kwizart@gmail.com> - 0.7.4-24
- Multilibs support - rhbz#1433758
- Simplify description
- Convert AUTHORS to UTF-8
- Drop Groups
- Add Obsoletes/Provides for a52dec-devel

* Sat Mar 18 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.7.4-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Aug 23 2016 Nicolas Chauvet <nicolas.chauvet@kwizart.fr> - 0.7.4-21
- Fix macro in comment

* Tue Aug 16 2016 Sérgio Basto <sergio@serjux.com> - 0.7.4-20
- Clean spec, with Vascom, rfbz #4193, add license tag

* Sat Aug 30 2014 Sérgio Basto <sergio@serjux.com> - 0.7.4-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Mar 10 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.7.4-18
- Add silence patch as we don't built with DJBFFT enabled

* Sun Mar 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.7.4-17
- Mass rebuilt for Fedora 19 Features

* Wed Jan 25 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.7.4-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Apr 28 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.7.4-15
- rebuild

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.7.4-14
- rebuild for new F11 features

* Sun Aug 03 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.7.4-12
- integrate a fix from livna that got lost

* Thu Jul 24 2008 David Juran <david@juran.se> - 0.7.4-12
- Bump Release for RpmFusion

* Sun Nov 11 2007 Dominik Mierzejewski <dominik [AT] greysector [DOT] net> 0.7.4-11.1
- Really drop djbfft

* Mon Oct  1 2007 David Juran <david@juran.se> - 0.7.4-11
- Fix Licence tag to be GPLv2
- Drop %%makeinstall macro
- Drop static archive
- Drop djbfft

* Fri Oct 06 2006 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 0.7.4-10
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Mon Mar 13 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 0.7.4-9
- Drop epoch in devel dep, too

* Thu Mar 09 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- switch to new release field
- drop epoch

* Tue Feb 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- add dist

* Thu Feb 16 2006 Ville Skyttä <ville.skytta at iki.fi> - 0:0.7.4-0.lvn.8
- Avoid standard rpaths on lib64 archs.

* Tue Jul 27 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.7.4-0.lvn.7
- Prefer PIC.
- (Build)Require djbfft-devel.
- Include more docs.

* Sun Sep 28 2003 Dams <anvil[AT]livna.org> 0:0.7.4-0.fdr.6
- Removed comment after scriptlets
- buildroot -> RPM_BUILD_ROOT

* Mon Apr 14 2003 Dams <anvil[AT]livna.org> 0:0.7.4-0.fdr.5
- devel package require djbfft (not djbfft-devel)

* Sun Apr 13 2003 Dams <anvil[AT]livna.org> 0:0.7.4-0.fdr.4
- Enabled support for djbfft

* Sun Apr 13 2003 Dams <anvil[AT]livna.org> 0:0.7.4-0.fdr.3
- Added post and postun scriplet
- moved man pages from devel to main package

* Sun Apr 13 2003 Dams <anvil[AT]livna.org> 0:0.7.4-0.fdr.2
- make configure honor optflags
- devel package
- shared library added

* Thu Apr 10 2003 Dams <anvil[AT]livna.org> 
- Initial build.
