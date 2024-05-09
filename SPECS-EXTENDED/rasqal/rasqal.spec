Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           rasqal
Version:        0.9.33
Release:        13%{?dist}
Summary:        RDF Query Library

License:        LGPLv2+ or ASL 2.0
URL:            https://librdf.org/rasqal/
Source:         https://download.librdf.org/source/%{name}-%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  libxml2-devel
BuildRequires:  mpfr-devel
BuildRequires:  pcre-devel
BuildRequires:  raptor2-devel
# for the testsuite
BuildRequires:  perl(Pod::Usage)
BuildRequires:  perl(XML::DOM)
#BuildRequires:  %{_bindir}/rapper

%description
Rasqal is a library providing full support for querying Resource
Description Framework (RDF) including parsing query syntaxes, constructing
the queries, executing them and returning result formats.  It currently
handles the RDF Data Query Language (RDQL) and SPARQL Query language.

%package        devel
Summary:        Development files for the Rasqal RDF libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description    devel
Libraries, includes etc to develop with the Rasqal RDF query language library.


%prep
%setup -q

# hack to nuke rpaths
%if "%{_libdir}" != "/usr/lib"
sed -i -e 's|"/lib /usr/lib|"/%{_lib} %{_libdir}|' configure
%endif


%build
%configure \
  --disable-static\
  --enable-release

%make_build


%install
%make_install

# unpackaged files
rm -fv $RPM_BUILD_ROOT%{_libdir}/lib*.la


%check
export PKG_CONFIG_PATH=%{buildroot}%{_datadir}/pkgconfig:%{buildroot}%{_libdir}/pkgconfig
test "$(pkg-config --modversion rasqal)" = "%{version}"
if [ -x %{_bindir}/rapper ]; then
%ifarch ppc64 s390x
make -k check ||:
%else
make -k check
%endif
else
echo "WARNING: %{_bindir}/rapper not present in buildroot, 'make check' skipped"
fi


%ldconfig_scriptlets

%files
%license COPYING COPYING.LIB
%license LICENSE.txt LICENSE-2.0.txt
%doc AUTHORS ChangeLog NEWS NOTICE README
%doc RELEASE.html
%{_bindir}/roqet
%{_libdir}/librasqal.so.3*
%{_mandir}/man1/roqet.1*

%files devel
%doc docs/README.html
%{_bindir}/rasqal-config
%{_includedir}/rasqal/
%{_libdir}/librasqal.so
%{_libdir}/pkgconfig/rasqal.pc
%{_mandir}/man1/rasqal-config.1*
%{_mandir}/man3/librasqal.3*
%{_datadir}/gtk-doc/


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.9.33-13
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.33-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Oct  9 2019 Jerry James <loganjerry@gmail.com> - 0.9.33-11
- Rebuild for mpfr 4

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.33-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.33-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.33-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Mar 07 2018 Rex Dieter <rdieter@fedoraproject.org> - 0.9.33-7
- BR: gcc-c++, use %%make_build %%make_insall %%ldconfig_scriptlets

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.33-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.33-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.33-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.33-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.33-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Dec 21 2015 Rex Dieter <rdieter@fedoraproject.org> 0.9.33-1
- 0.9.33, .spec cosmetics, use %%license

* Mon Dec 21 2015 Rex Dieter <rdieter@fedoraproject.org> 0.9.33-1
- 0.9.33

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.32-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Feb 18 2015 Rex Dieter <rdieter@fedoraproject.org> 0.9.32-4
- rebuild (gcc5)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.32-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.32-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Rex Dieter <rdieter@fedoraproject.org> 0.9.32-1
- 0.9.32

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.30-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Feb 19 2013 Rex Dieter <rdieter@fedoraproject.org> 0.9.30-1
- 0.9.30

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.29-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.29-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May 23 2012 Rex Dieter <rdieter@fedoraproject.org> 0.9.29-1
- rasqal-0.9.29

* Mon Mar 05 2012 Rex Dieter <rdieter@fedoraproject.org> 0.9.28-1
- 0.9.28

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Sep 06 2011 Rex Dieter <rdieter@fedoraproject.org> 0.9.27-1
- 0.9.27

* Sun Jul 31 2011 Rex Dieter <rdieter@fedoraproject.org> 0.9.26-1
- 0.9.26
- %%check: make /usr/bin/rapper not present non-fatal

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 0.9.21-1
- Update to 0.9.21

* Tue Nov 30 2010 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 0.9.20-2
- Rebuild against new mpfr-3.0

* Thu Sep 09 2010 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 0.9.20-1
- Update to 0.9.20
- Drop gtk-doc dependency RHBZ#604413
- Drop upstreamed DSO linking patch

* Sun Jul 11 2010 Dan Horák <dan[at]danny.cz> - 0.9.17-3
- don't fail the whole build due failed checks on s390(x)

* Sat Feb 13 2010 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 0.9.17-2
- Fix DSO linking error RHBZ#564859

* Sun Jan 03 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.9.17-1
- rasqal-0.9.17

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.15-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri May 01 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.9.15-5
- slightly less ugly rpath hacks
- cleanup %%files

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 17 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.9.15-3
- disable testsuite so this builds
- rebuild for pkg-config Provides

* Sun Nov 23 2008 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.15-2
- update summary
- not rebuilt yet

* Sat Feb 09 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.9.15-1
- Update to 0.9.15 (for redland 1.0.7, also lots of bugfixes)
- Update minimum raptor version
- BR perl(XML::DOM) (needed by the testsuite)

* Mon Oct 15 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.9.14-2
- Update minimum raptor version

* Mon Oct 15 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.9.14-1
- Update to 0.9.14 (for redland 1.0.6, also lots of bugfixes)
- Specify LGPL version in License tag

* Mon Dec 18 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.12-5
- added pcre-devel and libxml2-devel buildrequires

* Wed Dec 13 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.12-4
- Requires: pkgconfig in -devel package (Kevin Fenzi)

* Fri Nov 17 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.12-3
- rpmlint cleanup

* Thu Oct 26 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.12-2
- Surrender and use DESTDIR install

* Sat Jun 17 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.12-2
- fixed x86_64 rpath issue with an ugly hack
- removed OPTIMIZE from make invocation
- added smp flags
- added make check
- updated license

* Sun May 14 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.12-1
- new upstream release

* Fri Apr 07 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.11-1: packaged for Fedora Extras

* Thu Aug 11 2005  Dave Beckett <dave.beckett@bristol.ac.uk>
- Update Source:
- Use makeinstall macro

* Wed Aug 10 2005  Dave Beckett <dave.beckett@bristol.ac.uk>
- Use configure macro.

* Thu Jul 28 2005  Dave Beckett <dave.beckett@bristol.ac.uk>
- Updated for gtk-doc locations

* Fri Oct 22 2004 <Dave.Beckett@bristol.ac.uk>
- License now LGPL/Apache 2
- Added LICENSE-2.0.txt and NOTICE

* Wed May 5 2004 <Dave.Beckett@bristol.ac.uk>
- Ship roqet and roqet.1

* Sat May 1 2004 <Dave.Beckett@bristol.ac.uk>
- Requires raptor 1.3.0

* Tue Feb 24 2004 <Dave.Beckett@bristol.ac.uk>
- Requires raptor

* Mon Aug 11 2003 <Dave.Beckett@bristol.ac.uk>
- Initial packaging
