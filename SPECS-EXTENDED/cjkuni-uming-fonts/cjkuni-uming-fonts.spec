Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global fontname cjkuni-uming
%global fontconf 65-ttf-arphic-uming.conf
%global fontconf3 90-ttf-arphic-uming-embolden.conf

%global catalogue        %{_sysconfdir}/X11/fontpath.d

%global common_desc \
CJK Unifonts are Unicode TrueType fonts derived from original fonts made \
available by Arphic Technology under "Arphic Public License" and extended by \
the CJK Unifonts project.

%global umingbuilddir %{name}-%{version}

Name:           %{fontname}-fonts
Version:        0.2.20080216.1
Release:        65%{?dist}
Summary:        Chinese Unicode TrueType font in Ming face

License:        Arphic
URL:            https://www.freedesktop.org/wiki/Software/CJKUnifonts
Source0:        https://ftp.debian.org/debian/pool/main/t/ttf-arphic-uming/ttf-arphic-uming_%{version}.orig.tar.gz
Source1:        %{name}-fontconfig.conf
Source3:        %{fontconf3}

BuildArch:      noarch
BuildRequires:  fontpackages-devel
Requires:       fontpackages-filesystem
Obsoletes:      cjkuni-fonts-common < 0.2.20080216.1-42
Provides:       cjkuni-fonts-common = 0.2.20080216.1-42

%description
%common_desc

CJK Unifonts in Ming face.

%prep
%setup -q -c -n %{name}-%{version}


%build
%{nil}

%install
install -m 0755 -d %{buildroot}%{_fontdir}
install -m 0644 -p *.ttc %{buildroot}%{_fontdir}

install -m 0755 -d %{buildroot}%{_fontconfig_templatedir} \
                   %{buildroot}%{_fontconfig_confdir}

install -m 0644 -p %{SOURCE1} \
        %{buildroot}%{_fontconfig_templatedir}/%{fontconf}
ln -s %{_fontconfig_templatedir}/%{fontconf} \
      %{buildroot}%{_fontconfig_confdir}/%{fontconf}


install -m 0644 -p %{SOURCE3} \
        %{buildroot}%{_fontconfig_templatedir}/%{fontconf3}
ln -s %{_fontconfig_templatedir}/%{fontconf3} \
      %{buildroot}%{_fontconfig_confdir}/%{fontconf3}

# catalogue
install -m 0755 -d %{buildroot}%{catalogue}
ln -s %{_fontdir}/ %{buildroot}%{catalogue}/%{name}


%_font_pkg -f *.conf *.ttc

%defattr(-,root,root,-)
%doc ../%{umingbuilddir}/license
%doc ../%{umingbuilddir}/CONTRIBUTERS
%doc ../%{umingbuilddir}/FONTLOG
%doc ../%{umingbuilddir}/KNOWN_ISSUES
%doc ../%{umingbuilddir}/NEWS
%doc ../%{umingbuilddir}/README
%{catalogue}/%{name}

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.2.20080216.1-65
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.20080216.1-64
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.20080216.1-63
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.20080216.1-62
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.20080216.1-61
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.20080216.1-60
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.20080216.1-59
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.20080216.1-58
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.20080216.1-57
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.20080216.1-56
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May  4 2015 Peng Wu <pwu@redhat.com> - 0.2.20080216.1-55
- Lower font priority, as Adobe Source Han Sans are default Chinese fonts

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.20080216.1-54
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.20080216.1-53
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.20080216.1-52
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 13 2012  Peng Wu <pwu@redhat.com> - 0.2.20080216.1-51
- Improves spec file

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.20080216.1-50
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012  Peng Wu <pwu@redhat.com> - 0.2.20080216.1-49
- Fixes fontconf

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.20080216.1-48
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Mar 16 2011  Peng Wu <pwu@redhat.com> - 0.2.20080216.1-47
- Clean up spec.
  Remove fonts.dir, fonts.scale and 25-ttf-arphic-uming-render.conf.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.20080216.1-46
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jul 20 2010  Peng Wu <pwu@redhat.com> - 0.2.20080216.1-45
- Fixes font_pkg macro usage.

* Mon Jul 19 2010  Peng Wu <pwu@redhat.com> - 0.2.20080216.1-44
- Clean up the spec.

* Mon Jul 12 2010  Peng Wu <pwu@redhat.com> - 0.2.20080216.1-43
- The Initial Version.
  Split from cjkuni-fonts.
