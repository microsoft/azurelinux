# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           libmpeg2
Version:        0.5.1
Release: 33%{?dist}
Summary:        MPEG-2 decoder libraries

License:        GPL-2.0-or-later
URL:            http://libmpeg2.sourceforge.net
Source0:        %{url}/files/libmpeg2-%{version}.tar.gz
# https://github.com/videolan/vlc/blob/master/contrib/src/libmpeg2/libmpeg2-inline.patch
Patch0:         libmpeg2-inline.patch

BuildRequires:  gcc
BuildRequires:  SDL-devel
BuildRequires:  libXt-devel
BuildRequires:  libXv-devel
# bootstrap deps
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires: make


%description
libmpeg2 is a free library for decoding mpeg-2 and mpeg-1 video
streams. It is released under the terms of the GPL license.

%package -n     mpeg2dec
Summary:        MPEG-2 decoder program
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n mpeg2dec
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}


%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q
%patch -P0 -p1
autoreconf -fiv

iconv -f ISO-8859-1 -t UTF-8 AUTHORS > AUTHORS.tmp
touch -r AUTHORS AUTHORS.tmp 
cp -p -f AUTHORS.tmp AUTHORS
rm AUTHORS.tmp

#Disable ppc altivec case
sed -i -e 's/ppc-/noppc64-/' configure.ac configure
sed -i -e 's/powerpc-/nopowerpc64-/' configure.ac configure

%build
%configure --disable-static \
%ifarch %{ix86} ppc
  --disable-accel-detect \
%endif

# mpeg2dec have rpath
# remove rpath from libtool
sed -i.rpath 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i.rpath 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%{make_build} \
%ifarch %{ix86}
  OPT_CFLAGS="-fPIC -DPIC" \
%else
  OPT_CFLAGS="" \
%endif


%install
%{make_install}
find %{buildroot} -name '*.la' -exec rm -f {} ';'


#Fix datatype internal definitions
install -pm 0644 libmpeg2/mpeg2_internal.h \
  %{buildroot}%{_includedir}/mpeg2dec/

%ldconfig_scriptlets

%files
%doc AUTHORS ChangeLog NEWS README TODO
%license COPYING
%{_libdir}/*.so.*

%files -n mpeg2dec
%{_bindir}/corrupt_mpeg2
%{_bindir}/extract_mpeg2
%{_bindir}/mpeg2dec
%{_mandir}/man1/*.1*

%files devel
%doc CodingStyle doc/libmpeg2.txt doc/sample*.c
%{_includedir}/mpeg2dec/
%{_libdir}/*.so
%{_libdir}/pkgconfig/libmpeg2.pc
%{_libdir}/pkgconfig/libmpeg2convert.pc


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jan 20 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed May 08 2019 Yaakov Selkowitz <yselkowi@redhat.com> - 0.5.1-18
- Rebuilt for inclusion in Fedora

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.5.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 26 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.5.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Apr 29 2018 Leigh Scott <leigh123linux@googlemail.com> - 0.5.1-15
- Add patch to fix inline warnings
- Spec file clean up

* Thu Mar 01 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 0.5.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.5.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Mar 19 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.5.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Aug 31 2014 Sérgio Basto <sergio@serjux.com> - 0.5.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Mar 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.5.1-10
- Mass rebuilt for Fedora 19 Features

* Wed Jan 25 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.5.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Oct 17 2009 kwizart < kwizart at gmail.com > - 0.5.1-8
- Rebuild for F-12

* Wed Apr  8 2009 kwizart < kwizart at gmail.com > - 0.5.1-7
- New attempt

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.5.1-6
- rebuild for new F11 features

* Fri Mar 27 2009 kwizart < kwizart at gmail.com > - 0.5.1-5
- Rebuild
- Fix target_arch conditionals
- Provides internal definitions mpeg2_internal.h
- Disable ppc altivec optim (TODO improve asm optim later)
 
* Sat Oct  4 2008 kwizart < kwizart at gmail.com > - 0.5.1-3
- Fix CFLAGS on x86 producing selinux denials.

* Wed Jul 30 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 0.5.1-2
- rebuild for buildsys cflags issue

* Fri Jul 18 2008 kwizart < kwizart at gmail.com > - 0.5.1-1
- Update to 0.5.1

* Tue Jul 15 2008 kwizart < kwizart at gmail.com > - 0.5.0-1
- Initial package (based on mpeg2dec)

