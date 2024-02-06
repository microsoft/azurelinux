Summary:        Sample rate conversion library for audio data
Name:           libsamplerate
Version:        0.2.2
Release:        4%{?dist}
License:        BSD-2-Clause
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://libsndfile.github.io/libsamplerate/
Source0:        https://github.com/libsndfile/%{name}/releases/download/%{version}/%{name}-%{version}.tar.xz
BuildRequires:  alsa-lib-devel
BuildRequires:  fftw-devel >= 0.15.0
BuildRequires:  gcc
BuildRequires:  libsndfile-devel >= 1.0.6
BuildRequires:  make
BuildRequires:  pkg-config

%description
Secret Rabbit Code is a sample rate converter for audio. It is capable
of arbitrary and time varying conversions. It can downsample by a
factor of 12 and upsample by the same factor. The ratio of input and
output sample rates can be a real number. The conversion ratio can
also vary with time for speeding up and slowing down effects.

%package devel
Summary:        Development related files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       pkg-config

%description devel
Secret Rabbit Code is a sample rate converter for audio. It is capable
of arbitrary and time varying conversions. It can downsample by a
factor of 12 and upsample by the same factor. The ratio of input and
output sample rates can be a real number. The conversion ratio can
also vary with time for speeding up and slowing down effects.
This package contains development files for %{name}

%prep
%autosetup

%build
%configure --disable-dependency-tracking --disable-static
# Don't use rpath!
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
%make_build

%install
%make_install
rm %{buildroot}%{_libdir}/%{name}.la

%check
%{set_build_flags}
export LD_LIBRARY_PATH=`pwd`/src/.libs
%make_build check
unset LD_LIBRARY_PATH

%files
%doc AUTHORS README.md
%license COPYING
%{_libdir}/%{name}.so.0*

%files devel
%{_includedir}/samplerate.h
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/samplerate.pc
%{_pkgdocdir}/*
%exclude %{_pkgdocdir}/AUTHORS
%exclude %{_pkgdocdir}/README.md

%changelog
* Thu Nov 24 2022 Sumedh Sharma <sumsharma@microsoft.com> - 0.2.2-4
- Initial CBL-Mariner import from Fedora 37 (license: MIT)
- Enable check section
- License verified

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Nov 11 2021 Guido Aulisi <guido.aulisi@gmail.com> - 0.2.2-1
- Version 0.2.2

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Apr 26 2021 Guido Aulisi <guido.aulisi@gmail.com> - 0.2.1-1
- Version 0.2.1
- New upstream URL
- Some spec cleanup

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.9-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.9-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 13 2020 Tom Stellard <tstellar@redhat.com> - 0.1.9-6
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Feb 20 2018 Nils Philippsen <nils@tiptoe.de> - 0.1.9-1
- version 0.1.9
- change license to BSD (2-clause)
- require gcc, alsa-lib-devel, fftw-devel for building

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.8-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.8-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.8-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.8-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.8-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 0.1.8-8
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Oct 16 2011 Hans de Goede <hdegoede@redhat.com> - 0.1.8-1
- New upstream release 0.1.8 (rhbz#730939)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri May 08 2009 Lubomir Rintel <lkundrak@v3.sk> - 0.1.7-1
- New upstream release

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 27 2009 Hans de Goede <hdegoede@redhat.com> 0.1.6-1
- New upstream release 0.1.6

* Tue Jul 15 2008 Lubomir Rintel <lkundrak@v3.sk> 0.1.4-1
- New upstream release

* Mon Apr 14 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.1.3-1
- New upstream release 0.1.3

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.1.2-8
- Autorebuild for GCC 4.3

* Mon Aug 13 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.1.2-7
- Update License tag for new Licensing Guidelines compliance

* Mon Aug 28 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 0.1.2-6
- Drop static lib from -devel package
- FE6 Rebuild

* Sun Jul 23 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 0.1.2-5
- Taking over as maintainer since Anvil has other priorities
- Long long due rebuild with new gcc for FC-5, it seems this may have already
  been done, since the last rebuild was of March 16 and the Rebuild Request
  bug of March 19? Rebuilding anyway to be sure (bug 185876)
- Fix (remove) use of rpath

* Thu Mar 16 2006 Dams <anvil[AT]livna.org> - 0.1.2-4.fc5
- rebuild

* Thu May 12 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.1.2-3
- rebuilt

* Mon Oct 18 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.1.2-0.fdr.1
- Update to 0.1.2.
- Use "make install DESTDIR=...", disable dependency tracking.
- Run tests during build.
- Drop fftw-devel build dep, it's only for an optional part of the test suite.

* Tue Jul 13 2004 Michael Schwendt <mschwendt[AT]users.sf.net> 0:0.0.15-0.fdr.5
- Fix %%postun (#1665).

* Sat Jun 28 2003 Dams <anvil[AT]livna.org> 0:0.0.15-0.fdr.4
- Applied changes about doc from Michael Schwendt

* Sat Jun 28 2003 Dams <anvil[AT]livna.org> 0:0.0.15-0.fdr.3
- Modified doc inclusion way

* Wed Jun 25 2003 Dams <anvil[AT]livna.org> 0:0.0.15-0.fdr.2
- Added some more doc

* Thu May 22 2003 Dams <anvil[AT]livna.org>
- Initial build.
