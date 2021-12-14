Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           yelp-xsl
Version:        3.36.0
Release:        2%{?dist}
Summary:        XSL stylesheets for the yelp help browser

License:        LGPLv2+ and GPLv2+
URL:            https://download.gnome.org/sources/yelp-xsl
Source0:        https://download.gnome.org/sources/%{name}/3.36/%{name}-%{version}.tar.xz
BuildArch:      noarch

BuildRequires:  python3-libxml2
BuildRequires:  /usr/bin/ducktype
BuildRequires:  /usr/bin/xmllint
BuildRequires:  /usr/bin/xsltproc
BuildRequires:  gcc
BuildRequires:  itstool


%description
This package contains XSL stylesheets that are used by the yelp help browser.


%package devel
Summary: Developer documentation for yelp-xsl
Requires: %{name} = %{version}-%{release}

%description devel
The yelp-xsl-devel package contains developer documentation for the
XSL stylesheets in yelp-xsl.


%prep
%setup -q


%build
%configure --enable-doc
make %{?_smp_mflags}


%install
%make_install


%files
%doc README AUTHORS
%license COPYING COPYING.GPL COPYING.LGPL
%{_datadir}/yelp-xsl


%files devel
%{_datadir}/pkgconfig/yelp-xsl.pc


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.36.0-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Sat Mar 07 2020 Kalev Lember <klember@redhat.com> - 3.36.0-1
- Update to 3.36.0

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.34.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Nov 27 2019 Kalev Lember <klember@redhat.com> - 3.34.2-1
- Update to 3.34.2

* Mon Sep 09 2019 Kalev Lember <klember@redhat.com> - 3.34.0-1
- Update to 3.34.0

* Tue Sep 03 2019 Kalev Lember <klember@redhat.com> - 3.33.92-1
- Update to 3.33.92

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.33.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jul 18 2019 Kalev Lember <klember@redhat.com> - 3.33.4-1
- Update to 3.33.4

* Mon Mar 18 2019 Kalev Lember <klember@redhat.com> - 3.32.1-1
- Update to 3.32.1

* Mon Mar 11 2019 Kalev Lember <klember@redhat.com> - 3.32.0-1
- Update to 3.32.0

* Mon Feb 04 2019 Kalev Lember <klember@redhat.com> - 3.31.90-1
- Update to 3.31.90

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.30.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Sep 26 2018 Kalev Lember <klember@redhat.com> - 3.30.1-1
- Update to 3.30.1

* Thu Sep 06 2018 Kalev Lember <klember@redhat.com> - 3.30.0-1
- Update to 3.30.0

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.28.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Mar 18 2018 Iryna Shcherbina <ishcherb@redhat.com> - 3.28.0-2
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Mon Mar 12 2018 Kalev Lember <klember@redhat.com> - 3.28.0-1
- Update to 3.28.0

* Tue Mar 06 2018 Kalev Lember <klember@redhat.com> - 3.27.90-1
- Update to 3.27.90

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.27.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Nov 02 2017 Kalev Lember <klember@redhat.com> - 3.27.1-1
- Update to 3.27.1

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.20.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.20.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Apr 13 2016 Kalev Lember <klember@redhat.com> - 3.20.1-1
- Update to 3.20.1

* Tue Mar 22 2016 Kalev Lember <klember@redhat.com> - 3.20.0-1
- Update to 3.20.0

* Mon Feb 15 2016 David King <amigadave@amigadave.com> - 3.19.90-1
- Update to 3.19.90

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.18.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Oct 05 2015 Kalev Lember <klember@redhat.com> - 3.18.1-1
- Update to 3.18.1

* Mon Sep 21 2015 Kalev Lember <klember@redhat.com> - 3.18.0-1
- Update to 3.18.0

* Sun Aug 16 2015 Kalev Lember <klember@redhat.com> - 3.17.90-1
- Update to 3.17.90
- Use make_install macro

* Mon Jul 20 2015 David King <amigadave@amigadave.com> - 3.17.4-1
- Update to 3.17.4

* Mon Jun 29 2015 David King <amigadave@amigadave.com> - 3.17.3-1
- Update to 3.17.3

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.17.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 28 2015 David King <amigadave@amigadave.com> - 3.17.2-1
- Update to 3.17.2

* Tue Apr 14 2015 David King <amigadave@amigadave.com> - 3.16.1-1
- Update to 3.16.1
- Update licenses to include both GPLv2+ and LGPLv2+

* Tue Mar 24 2015 Kalev Lember <kalevlember@gmail.com> - 3.16.0-1
- Update to 3.16.0

* Tue Mar 17 2015 Kalev Lember <kalevlember@gmail.com> - 3.15.92-1
- Update to 3.15.92
- Use license macro for the COPYING file

* Mon Oct 27 2014 Kalev Lember <kalevlember@gmail.com> - 3.14.0-2
- Don't use the _isa macro as the package is noarch

* Tue Sep 23 2014 Kalev Lember <kalevlember@gmail.com> - 3.14.0-1
- Update to 3.14.0

* Tue Sep 16 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.92-1
- Update to 3.13.92
- Tighten subpackage deps

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 25 2014 Richard Hughes <rhughes@redhat.com> - 3.12.0-1
- Update to 3.12.0

* Tue Feb 18 2014 Richard Hughes <rhughes@redhat.com> - 3.11.90-1
- Update to 3.11.90

* Mon Feb 03 2014 Richard Hughes <rhughes@redhat.com> - 3.11.5-1
- Update to 3.11.5

* Mon Jan 13 2014 Richard Hughes <rhughes@redhat.com> - 3.11.4-1
- Update to 3.11.4

* Tue Nov 19 2013 Richard Hughes <rhughes@redhat.com> - 3.11.1-1
- Update to 3.11.1

* Tue Oct 29 2013 Richard Hughes <rhughes@redhat.com> - 3.10.1-1
- Update to 3.10.1

* Tue Sep 24 2013 Kalev Lember <kalevlember@gmail.com> - 3.10.0-1
- Update to 3.10.0

* Thu Aug 22 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.90-1
- Update to 3.9.90

* Fri Aug 09 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.1-1
- Update to 3.9.1

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 14 2013 Richard Hughes <rhughes@redhat.com> - 3.8.1-1
- Update to 3.8.1

* Tue Mar 26 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.0-1
- Update to 3.8.0

* Mon Mar 04 2013 Richard Hughes <rhughes@redhat.com> - 3.7.91-1
- Update to 3.7.91

* Wed Feb 20 2013 Richard Hughes <rhughes@redhat.com> - 3.7.90-1
- Update to 3.7.90

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 16 2013 Richard Hughes <hughsient@gmail.com> - 3.7.4-1
- Update to 3.7.4

* Wed Jan 09 2013 Richard Hughes <hughsient@gmail.com> - 3.7.3-1
- Update to 3.7.3

* Wed Nov 21 2012 Richard Hughes <hughsient@gmail.com> - 3.7.2-1
- Update to 3.7.2

* Tue Oct 16 2012 Kalev Lember <kalevlember@gmail.com> - 3.6.1-1
- Update to 3.6.1

* Tue Sep 25 2012 Kalev Lember <kalevlember@gmail.com> - 3.6.0-1
- Update to 3.6.0

* Tue Sep 18 2012 Kalev Lember <kalevlember@gmail.com> - 3.5.92-1
- Update to 3.5.92

* Tue Sep 04 2012 Richard Hughes <hughsient@gmail.com> - 3.5.91-1
- Update to 3.5.91

* Wed Aug 22 2012 Richard Hughes <hughsient@gmail.com> - 3.5.90-1
- Update to 3.5.90

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri May 18 2012 Richard Hughes <hughsient@gmail.com> - 3.4.2-1
- Update to 3.4.2

* Tue Apr 17 2012 Kalev Lember <kalevlember@gmail.com> - 3.4.1-1
- Update to 3.4.1

* Tue Mar 27 2012 Richard Hughes <hughsient@gmail.com> - 3.4.0-1
- Update to 3.4.0

* Tue Mar 20 2012 Kalev Lember <kalevlember@gmail.com> - 3.3.92-1
- Update to 3.3.92

* Sat Feb 25 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.3-1
- Update to 3.3.3

* Tue Jan 17 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.2-1
- Update to 3.3.2

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 21 2011 Matthias Clasen <mclasen@redhat.com> - 3.3.1-1
- Update to 3.3.1

* Tue Oct 18 2011 Matthias Clasen <mclasen@redhat.com> - 3.2.1-1
- Update to 3.2.1

* Tue Sep 27 2011 Ray <rstrode@redhat.com> - 3.2.0-1
- Update to 3.2.0

* Mon Sep 19 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.6-1
- Update to 3.1.6

* Wed Sep 07 2011 Kalev Lember <kalevlember@gmail.com> - 3.1.5-1
- Update to 3.1.5

* Thu Aug 18 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.4-1
- Update to 3.1.4

* Mon Jul 25 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.3-1
- Update to 3.1.3

* Wed Jul  6 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.2-1
- Update to 3.1.2

* Tue May 24 2011 Christopher Aillon <caillon@redhat.com> - 3.1.1-1
- Update to 3.1.1

* Tue May 24 2011 Christopher Aillon <caillon@redhat.com> - 3.0.2-1
- Update to 3.0.2

* Mon Apr 25 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.1-1
- Update to 3.0.1

* Mon Apr  4 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.0-1
- Update to 3.0.0

* Tue Mar 22 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.92-1
- Update to 2.91.92

* Mon Mar  7 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.91-1
- Update to 2.91.91

* Mon Feb 21 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.90-1
- Update to 2.91.90

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.91.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 10 2011 Matthias Clasen <mclasen@redhat.com> 2.91.9-1
- Update to 2.92.6

* Thu Nov 11 2010 Matthias Clasen <mclasen@redhat.com> 2.31.6-1
- Update to 2.31.6

* Mon Jul 12 2010 Matthias Clasen <mclasen@redhat.com> 2.31.5-1
- Update to 2.31.5

* Tue Jun 29 2010 Matthias Clasen <mclasen@redhat.com> 2.31.4-1
- Update to 2.31.4

* Tue Jun  8 2010 Matthias Clasen <mclasen@redhat.com> 2.31.3-1
- Update to 2.31.3

* Thu May 27 2010 Matthias Clasen <mclasen@redhat.com> 2.31.2-1
- Update to 2.31.2

* Thu May 27 2010 Matthias Clasen <mclasen@redhat.com> 2.31.1-2
- Some corrections

* Sat May 15 2010 Matthias Clasen <mclasen@redhat.com> 2.31.1-1
- Initial packaging
