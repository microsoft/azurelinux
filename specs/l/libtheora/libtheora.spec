# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# enable bootstrap mode (e.g. disables doc generation)
%bcond bootstrap 0
# enable devel-docs (transfig is unavailable in RHEL)
%bcond devel_docs %[%{without bootstrap} && %{undefined rhel}]

Name:           libtheora
Epoch:          1
Version:        1.1.1
Release:        40%{?dist}
Summary:        Theora Video Compression Codec
License:        BSD-3-Clause
URL:            http://www.theora.org
Source0:        http://downloads.xiph.org/releases/theora/%{name}-%{version}.tar.xz
Patch0:         libtheora-1.1.1-fix-pp_sharp_mod-calc.patch
# https://bugs.archlinux.org/task/35985
Patch1:         libtheora-1.1.1-libpng16.patch
Patch2:         libtheora-1.1.1-libm.patch

BuildRequires: make
BuildRequires:  autoconf automake libtool
BuildRequires:  libogg-devel >= 2:1.1
BuildRequires:  libvorbis-devel
BuildRequires:  SDL-devel libpng-devel
%if %{without devel_docs}
Obsoletes: %{name}-devel-docs < %{epoch}:%{version}-%{release}
%else
BuildRequires:  doxygen
BuildRequires:  tetex-latex transfig
%endif

%description
Theora is Xiph.Org's first publicly released video codec, intended
for use within the Ogg's project's Ogg multimedia streaming system.
Theora is derived directly from On2's VP3 codec; Currently the two are
nearly identical, varying only in encapsulating decoder tables in the
bitstream headers, but Theora will make use of this extra freedom
in the future to improve over what is possible with VP3.


%package devel
Summary:        Development tools for Theora applications
Requires:       libogg-devel >= 2:1.1
Requires:       %{name}%{?_isa} = %{epoch}:%{version}-%{release}

%description devel
The libtheora-devel package contains the header files needed to develop
applications with libtheora.


%package devel-docs
Summary:        Documentation for developing Theora applications
BuildArch:      noarch

%description devel-docs
The libtheora-devel-docs package contains the documentation needed
to develop applications with libtheora.


%package -n theora-tools
Summary:        Command line tools for Theora videos
Requires:       %{name}%{?_isa} = %{epoch}:%{version}-%{release}

%description -n theora-tools
The theora-tools package contains simple command line tools for use
with theora bitstreams.


%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p0 -b .libpng16
%patch -P2 -p1

# Update config.guess/sub to fix builds on new architectures (aarch64/ppc64le)
cp /usr/lib/rpm/redhat/config.* .

%build
./autogen.sh
# no custom CFLAGS please
sed -i 's/CFLAGS="$CFLAGS $cflags_save"/CFLAGS="$cflags_save"/g' configure
%configure --enable-shared --disable-static
# Don't use rpath!
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
%{make_build}

%if %{with devel_docs}
make -C doc/spec %{?_smp_mflags}
%endif


%install
%{make_install}

find %{buildroot} -type f -name "*.la" -delete
rm -r %{buildroot}/%{_docdir}/*

mkdir -p %{buildroot}/%{_bindir}
install -m 755 examples/.libs/dump_video $RPM_BUILD_ROOT/%{_bindir}/theora_dump_video
install -m 755 examples/.libs/encoder_example $RPM_BUILD_ROOT/%{_bindir}/theora_encode
install -m 755 examples/.libs/player_example $RPM_BUILD_ROOT/%{_bindir}/theora_player
install -m 755 examples/.libs/png2theora $RPM_BUILD_ROOT/%{_bindir}/png2theora


%ldconfig_scriptlets


%files
%doc README COPYING
%{_libdir}/*.so.*

%files devel
%{_includedir}/theora
%{_libdir}/*.so
%{_libdir}/pkgconfig/theora*.pc

%if %{with devel_docs}
%files devel-docs
%doc doc/libtheora/html doc/vp3-format.txt doc/spec/Theora.pdf
%doc doc/color.html doc/draft-ietf-avt-rtp-theora-00.txt
%endif

%files -n theora-tools
%{_bindir}/*


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1.1-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1.1-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1.1-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri May 10 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 1:1.1.1-37
- Do not build devel-docs in RHEL/ELN builds

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1.1-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1.1-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1.1-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1.1-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1.1-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1.1-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1.1-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1.1-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Aug 03 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 1:1.1.1-28
- Use new macros, update config.\* locations

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1.1-27
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1.1-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1.1-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1.1-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1.1-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1.1-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1:1.1.1-20
- Switch to %%ldconfig_scriptlets

* Mon Aug 07 2017 Rex Dieter <rdieter@fedoraproject.org> - 1:1.1.1-19
- disable bootstrap

* Mon Aug 07 2017 Rex Dieter <rdieter@fedoraproject.org> - 1:1.1.1-18
- support and enable bootstrap mode (ie, no docs)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.1.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.1.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jun 10 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.1.1-11
- Update config.guess/sub for new architecture support

* Mon Jun 09 2014 Adam Jackson <ajax@redhat.com> 1.1.1-10
- Fix FTBFS due to underlinked examples

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.1.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug  3 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1:1.1.1-9
- Add patch to fix FTBFS with libpng-1.6

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.1.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri May 10 2013 Hans de Goede <hdegoede@redhat.com> - 1:1.1.1-7
- Remove no longer needed autoreconf call, %%configure from redhat-rpm-config
  >= 9.1.0-42 updates config.guess and config.sub for new architecture support

* Fri May  3 2013 Hans de Goede <hdegoede@redhat.com> - 1:1.1.1-6
- run autoreconf for aarch64 support (#925898)
- add a patch from upstream fixing a crash when compiled with gcc-4.8 (#959001)
- cleanup spec-file

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 1:1.1.1-2
- Rebuild for new libpng

* Thu Feb 17 2011 Adam Jackson <ajax@redhat.com> 1.1.1-1
- libtheora 1.1.1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Sep 25 2009 Adam Jackson <ajax@redhat.com> 1.1.0-1
- libtheora 1.1.0

* Mon Aug 24 2009 Matthias Clasen <mclasen@redhat.com> - 1.1beta3
- 1.1beta3

* Thu Aug 13 2009 Matthias Clasen <mclasen@redhat.com> - 1.1beta2
- 1.1beta2

* Wed Aug 12 2009 Ville Skyttä <ville.skytta@iki.fi> - 1:1.1beta1-2
- Use xz compressed upstream tarball.

* Wed Aug  5 2009 Matthias Clasen <mclasen@redhat.com> - 1.1beta1
- 1.1beta1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.1alpha2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 03 2009 Adam Jackson <ajax@redhat.com> 1.1alpha2-1
- 1.1alpha2

* Tue Jun 02 2009 Adam Jackson <ajax@redhat.com> 1:1.1alpha1-1
- libtheora 1.1alpha1.  Woo Thusnelda!

* Tue Feb 24 2009 Matthias Clasen <mclasen@redhat.com> 1:1.0-3
- Make -devel-docs noarch

* Sat Dec 20 2008 Hans de Goede <hdegoede@redhat.com> 1:1.0-2
- Put development documentation in its own subpackage to fix multilib
  conflicts (rh 477290)

* Tue Dec 16 2008 Hans de Goede <hdegoede@redhat.com> 1:1.0-1
- 1.0 final release
- need epoch because we were not using the special pre-release
  version-release scheme used now a days in Fedora :(

* Fri Oct  3 2008 Matthias Clasen <mclasen@redhat.com> 1.0rc1-2
- Fix build on x86_64

* Fri Oct  3 2008 Matthias Clasen <mclasen@redhat.com> 1.0rc1-1
- Update to 1.0rc1

* Wed May 14 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0:1.0beta3-2
- Fix libtheoraenc getting build but not installed

* Thu Apr 17 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 1.0beta3-1
- New upstream release 1.0beta3

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:1.0beta2-4
- Autorebuild for GCC 4.3

* Thu Nov 29 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.0beta2-3
- Update png2theora to latest svn version (bz 401681)

* Wed Oct 24 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.0beta2-2
- Put Obsoletes/Provides theora-exp-devel in the -devel package instead of in
  the -tools package (oops)
- Install png2theora (bz 349951)

* Thu Oct 18 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.0beta2-1
- New upstream bugfix release 1.0beta2

* Thu Oct 11 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.0beta1-1
- New upstream release 1.0beta1 (bz 307571)

* Fri Sep 14 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.0alpha8-0.3.svn13393
- Fix textrelocations on i386 (bz 253591)

* Wed Aug 22 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.0alpha8-0.2.svn13393
- Fix Source0 URL

* Sun Jul 29 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.0alpha8-0.1.svn13393
- Update to 1.0alpha8 svn (revision 13393) snapshot

* Wed Apr 11 2007 Matthias Clasen <mclasen@redhat.com> - 0:1.0alpha7-3
- Add api docs to the -devel package

* Sun Mar 25 2007 Matthias Clasen <mclasen@redhat.com> - 0:1.0alpha7-2
- Fix a directory ownership issue (#233872)
- Small spec cleanups

* Wed Aug 02 2006 Monty <cmontgom@redhat.com> - 0:1.0alpha7-1
- Update to 1.0alpha7

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0:1.0alpha5-1.2.2
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0:1.0alpha5-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0:1.0alpha5-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov 09 2005 John (J5) Palmieri <johnp@redhar.com> - 1.0alpha5-1
- Update to 1.0alpha5

* Wed Mar 02 2005 John (J5) Palmieri <johnp@redhar.com> - 1.0alpha4-2
- rebuild with gcc 4.0

* Mon Jan 03 2005 Colin Walters <walters@redhat.com> - 1.0alpha4-1
- New upstream version 1.0alpha4 
- Remove upstreamed patch libtheora-1.0alpha3-include.patch 
- Use Theora_I_spec.pdf for spec
- Add in .pc file (yay! another library sees the light)

* Tue Oct 05 2004 Colin Walters <walters@redhat.com> - 1.0alpha3-5
- Add BuildRequires on libvorbis-devel (134664)

* Sat Jul 17 2004 Warren Togami <wtogami@redhat.com> - 1.0alpha3-4
- Add Epoch dependencies for future Epoch increment safety measure

* Thu Jul 15 2004 Colin Walters <walters@redhat.com> - 1.0alpha3-3
- Apply patch to fix include path, thanks to Thomas Vander Stichele

* Tue Jul 13 2004 Jeremy Katz <katzj@redhat.com> - 1.0alpha3-2
- rebuild

* Mon Jun 21 2004 Jeremy Katz <katzj@redhat.com> - 1.0alpha3-1
- Initial build
