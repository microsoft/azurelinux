%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Summary:        Command Line XML Toolkit
Name:           xmlstarlet
Version:        1.6.1
Release:        16%{?dist}
License:        MIT
URL:            http://xmlstar.sourceforge.net/
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://downloads.sourceforge.net/project/xmlstar/%{name}/%{version}/%{name}-%{version}.tar.gz

# https://sourceforge.net/p/xmlstar/bugs/109/
Patch0:         xmlstarlet-1.6.1-nogit.patch
# http://sourceforge.net/tracker/?func=detail&aid=3266898&group_id=66612&atid=515106

BuildRequires:  gcc
BuildRequires:  xmlto
BuildRequires:  automake 
BuildRequires:  autoconf
BuildRequires:  libxslt-devel
BuildRequires:  libxml2-devel >= 2.6.23
BuildRequires:  docbook5-schemas


%description
XMLStarlet is a set of command line utilities which can be used
to transform, query, validate, and edit XML documents and files
using simple set of shell commands in similar way it is done for
plain text files using UNIX grep, sed, awk, diff, patch, join, etc
commands.

%prep
%setup -q
%patch0 -p1 -b .nogit


%build
autoreconf -i
%configure --disable-static-libs --with-libxml-include-prefix=%{_includedir}/libxml2 --docdir=%{_pkgdocdir} # --libdir=%{_libdir}
make %{?_smp_mflags}


%install
rm -fr %{buildroot}
make install DESTDIR=%{buildroot}
# Avoid name kludging in autotools
mv %{buildroot}%{_bindir}/xml %{buildroot}%{_bindir}/xmlstarlet


%check
make check


%files
%doc AUTHORS ChangeLog NEWS README Copyright TODO
%doc %{_pkgdocdir}/*
%{_mandir}/man1/xmlstarlet.1*
%{_bindir}/xmlstarlet


%changelog
* Fri Aug 21 2020 Olivia Crain <oliviacrain@microsoft.com> - 1.6.1-16
- Initial CBL-Mariner import from Fedora 33 (license: MIT)
- License verified

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Mar 01 2016 Yaakov Selkowitz <yselkowi@redhat.com> - 1.6.1-6
- Mark installed documentation as %%doc (#1308255)

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Dec  8 2014 Paul W. Frields <stickster@gmail.com> - 1.6.1-3
- Fix noisy git related spew (#1171864)

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Aug 13 2014 Paul W. Frields <stickster@gmail.com> - 1.6.1-1
- Update to upstream 1.6.1 (#1129106)

* Mon Jun 16 2014 Paul W. Frields <stickster@gmail.com> - 1.6.0-1
- Update to upstream 1.6.0 (#1037400, #1107292)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Jul 27 2013 Ville Skyttä <ville.skytta@iki.fi> - 1.5.0-2
- Install docs to %%{_pkgdocdir} where available.

* Wed Jul 10 2013 Paul W. Frields <stickster@gmail.com> - 1.5.0-1
- Update to upstream 1.5.0 (#983025)
- Fix man page rendering (#981050)
- Use standard docdir

* Mon Mar 25 2013 Paul W. Frields <stickster@gmail.com> - 1.4.2-1
- Update to upstream 1.4.2 (#851880)

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Feb 15 2012 Paul W. Frields <stickster@gmail.com> - 1.3.1-2
- Fix build with configure flag

* Wed Feb 15 2012 Paul W. Frields <stickster@gmail.com> - 1.3.1-1
- Update to upstream 1.3.1 (#782066)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct  3 2011 Paul W. Frields <stickster@gmail.com> - 1.3.0-1
- Update to upstream 1.3.0

* Fri Aug 26 2011 Paul W. Frields <stickster@gmail.com> - 1.2.1-1
- Update to upstream 1.2.1

* Sun Apr 10 2011 Paul W. Frields <stickster@gmail.com> - 1.1.0-1
- Update to upstream 1.1.0

* Thu Apr 07 2011 Dan Horák <dan[at]danny.cz> - 1.0.6-2
- fix build on 64-bit big-endians

* Sat Mar 26 2011 Paul W. Frields <stickster@gmail.com> - 1.0.6-1
- Update to upstream 1.0.6
- Drop obsolete patch

* Thu Feb 17 2011 Paul W. Frields <stickster@gmail.com> - 1.0.5-1
- Update to upstream 1.0.5
- Update libxml2 requirement
- Drop unnecessary patch, naming issue fixed upstream

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 19 2011 Paul W. Frields <stickster@gmail.com> - 1.0.4-1
- Update to new upstream 1.0.4
- Drop patches for fixed upstream issues

* Fri Dec 17 2010 Paul W. Frields <stickster@gmail.com> - 1.0.3-1
- Update to new upstream 1.0.3
- Add %%check section for validation testing

* Mon Nov  1 2010 Paul W. Frields <stickster@gmail.com> - 1.0.2-1
- Update to new upstream 1.0.2

* Sun Jan 10 2010 Paul W. Frields <stickster@gmail.com> - 1.0.1-9
- Correct source URL

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Mar 21 2008 Paul W. Frields <stickster@gmail.com> - 1.0.1-6
- Rebuild to use FORTIFY_SOURCE correctly

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.1-5
- Autorebuild for GCC 4.3

* Sat Sep  2 2006 Paul W. Frields <stickster@gmail.com> - 1.0.1-4
- Bump release for FC6 mass rebuild

* Fri Feb 17 2006 Paul W. Frields <stickster@gmail.com> - 1.0.1-3
- FESCo mandated rebuild

* Wed Nov 23 2005 Paul W. Frields <stickster@gmail.com> - 1.0.1-2
- Minor changes per review

* Tue Nov 22 2005 Paul W. Frields <stickster@gmail.com> - 1.0.1-1.2
- Improve patching to conquer inconsistent naming

* Tue Nov 22 2005 Paul W. Frields <stickster@gmail.com> - 1.0.1-1.1
- Initial RPM version

