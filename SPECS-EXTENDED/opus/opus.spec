Vendor:         Microsoft Corporation
Distribution:   Azure Linux
#global candidate rc2

Name:     opus
Version:  1.3.1
Release:  4%{?dist}
Summary:  An audio codec for use in low-delay speech and audio communication
License:  BSD
URL:      https://www.opus-codec.org/

Source0:  https://downloads.xiph.org/releases/%{name}/%{name}-%{version}%{?candidate:-%{candidate}}.tar.gz
# This is the final IETF Working Group RFC
Source1:  https://tools.ietf.org/rfc/rfc6716.txt 
Source2:  https://tools.ietf.org/rfc/rfc8251.txt

BuildRequires: gcc
BuildRequires: doxygen

%description
The Opus codec is designed for interactive speech and audio transmission over 
the Internet. It is designed by the IETF Codec Working Group and incorporates 
technology from Skype's SILK codec and Xiph.Org's CELT codec.

%package  devel
Summary:  Development package for opus
Requires: libogg-devel
Requires: opus = %{version}-%{release}

%description devel
Files for development with opus.

%prep
%setup -q %{?candidate:-n %{name}-%{version}-%{candidate}}
cp %{SOURCE1} .
cp %{SOURCE2} .

%build
%configure --enable-custom-modes --disable-static \
           --enable-hardening --enable-ambisonics

%make_build

%install
%make_install

# Remove libtool archives
find %{buildroot} -type f -name "*.la" -delete
rm -rf %{buildroot}%{_datadir}/doc/opus/html

%check
make check %{?_smp_mflags} V=1

%ldconfig_scriptlets

%files
%license COPYING
%{_libdir}/libopus.so.*

%files devel
%doc README doc/html rfc6716.txt rfc8251.txt
%{_includedir}/opus
%{_libdir}/libopus.so
%{_libdir}/pkgconfig/opus.pc
%{_datadir}/aclocal/opus.m4
%{_datadir}/man/man3/opus_*.3.gz

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.3.1-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Apr 14 2019 Peter Robinson <pbrobinson@fedoraproject.org> 1.3.1-1
- Update to 1.3.1

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Oct 18 2018 Peter Robinson <pbrobinson@fedoraproject.org> 1.3-1
- Update to 1.3

* Wed Sep 19 2018 Peter Robinson <pbrobinson@fedoraproject.org> 1.3-0.7.rc2
- Update to 1.3 rc2

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-0.6.rc
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun  2 2018 Peter Robinson <pbrobinson@fedoraproject.org> 1.3-0.5.rc
- Update to 1.3 rc

* Fri Mar  9 2018 Peter Robinson <pbrobinson@fedoraproject.org> 1.3-0.4.beta
- Add gcc BR

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-0.3.beta
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.3-0.2.beta
- Switch to %%ldconfig_scriptlets

* Fri Dec 22 2017 Peter Robinson <pbrobinson@fedoraproject.org> 1.3-0.1.beta
- Update to 1.3 beta

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 28 2017 Peter Robinson <pbrobinson@fedoraproject.org> 1.2.1-1
- Update to 1.2.1

* Tue Jun 20 2017 Peter Robinson <pbrobinson@fedoraproject.org> 1.2-1
- Update to 1.2

* Fri Jun  9 2017 Peter Robinson <pbrobinson@fedoraproject.org> 1.2-0.4
- Update to 1.2.0 RC1

* Wed May 24 2017 Peter Robinson <pbrobinson@fedoraproject.org> 1.2-0.3
- Update to 1.2.0 Beta

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-0.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Nov  4 2016 Peter Robinson <pbrobinson@fedoraproject.org> 1.2-0.1
- Update to 1.2.0 Alpha

* Mon Jul 18 2016 Peter Robinson <pbrobinson@fedoraproject.org> 1.1.3-1
- Update 1.1.3 GA

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 12 2016 Peter Robinson <pbrobinson@fedoraproject.org> 1.1.2-1
- Update 1.1.2 GA

* Thu Nov 26 2015 Peter Robinson <pbrobinson@fedoraproject.org> 1.1.1-1
- Update 1.1.1 GA

* Wed Oct 28 2015 Peter Robinson <pbrobinson@fedoraproject.org> 1.1.1-0.4.rc
- Update to 1.1.1 RC (further ARM optimisations)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-0.3.beta
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Feb  3 2015 Peter Robinson <pbrobinson@fedoraproject.org> 1.1.1-0.2.beta
- Use %%license

* Wed Oct 15 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.1.1-0.1.beta
- Update to 1.1.1 beta (SSE, ARM, MIPS optimisations)

* Sun Oct  5 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.1-5
- Install html docs in devel package

* Fri Oct  3 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.1-4
- Build developer docs

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Dec  6 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.1-1
- 1.1 release

* Tue Dec  3 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.1-0.3rc3
- Update to 1.1-rc3

* Thu Nov 28 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.1-0.2rc2
- Update to 1.1-rc2

* Tue Nov 26 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.1-0.1rc
- Update to 1.1-rc

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 14 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.3-1
- 1.0.3 release

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan 10 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.2-2
- Enable extra custom modes API

* Thu Dec  6 2012 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.2-1
- Official 1.0.2 release

* Wed Sep 12 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.0.1-1
- Official 1.0.1 release now rfc6716 is stable

* Tue Sep  4 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.0.1rc3-0.1
- Update to 1.0.1rc3

* Thu Aug  9 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.0.0rc1-0.1
- Update to 1.0.0rc1

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun May 27 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.9.14-1
- Update to 0.9.14

* Sat May 12 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.9.10-2
- Add make check - fixes RHBZ # 821128

* Fri Apr 27 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.9.10-1
- Update to 0.9.10

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov  8 2011 Peter Robinson <pbrobinson@fedoraproject.org> 0.9.8-1
- Update to 0.9.8

* Mon Oct 10 2011 Peter Robinson <pbrobinson@fedoraproject.org> 0.9.6-1
- Initial packaging
