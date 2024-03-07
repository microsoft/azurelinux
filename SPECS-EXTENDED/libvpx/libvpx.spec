Vendor:         Microsoft Corporation
Distribution:   Mariner
%global somajor 8
%global sominor 0
%global sotiny  0
%global soversion %{somajor}.%{sominor}.%{sotiny}

Name:			libvpx
Summary:		VP8/VP9 Video Codec SDK
Version:		1.13.1
Release:		1%{?dist}
License:		BSD
Source0:		https://github.com/webmproject/libvpx/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:		vpx_config.h
# Thanks to debian.
Source2:		libvpx.ver
URL:			http://www.webmproject.org/code/
BuildRequires:		gcc
BuildRequires:		gcc-c++
%ifarch %{ix86} x86_64
BuildRequires:		yasm
%endif
BuildRequires:		doxygen, php-cli, perl(Getopt::Long)
# Do not disable FORTIFY_SOURCE=2
Patch0:			libvpx-1.7.0-leave-fortify-source-on.patch

%description
libvpx provides the VP8/VP9 SDK, which allows you to integrate your applications 
with the VP8 and VP9 video codecs, high quality, royalty free, open source codecs 
deployed on millions of computers and devices worldwide. 

%package devel
Summary:		Development files for libvpx
Requires:		%{name}%{?_isa} = %{version}-%{release}

%description devel
Development libraries and headers for developing software against 
libvpx.

%package utils
Summary:		VP8 utilities and tools
Requires:		%{name}%{?_isa} = %{version}-%{release}

%description utils
A selection of utilities and tools for VP8, including a sample encoder
and decoder.

%prep
%setup -q -n libvpx-%{version}
%patch0 -p1 -b .leave-fs-on

%build
%ifarch %{ix86}
%global vpxtarget x86-linux-gcc
%else
%ifarch	x86_64
%global	vpxtarget x86_64-linux-gcc
%else
%ifarch armv7hl
%global vpxtarget armv7-linux-gcc
%else
%ifarch aarch64
%global vpxtarget arm64-linux-gcc
%else
%global vpxtarget generic-gnu
%endif
%endif
%endif
%endif

# History: The configure script used to reject the shared flag on the generic target.
# This meant that we needed to fall back to manual shared lib creation.
# However, the modern configure script permits the shared flag and assumes ELF.
# Additionally, the libvpx.ver would need to be updated to work properly.
# As a result, we disable this universally, but keep it around in case we ever need to support
# something "special".
%if "%{vpxtarget}" == "generic-gnu"
%global generic_target 0
%else
%global	generic_target 0
%endif

%set_build_flags

%ifarch armv7hl
CROSS=armv7hl-redhat-linux-gnueabi- CHOST=armv7hl-redhat-linux-gnueabi-hardfloat ./configure \
%else
./configure --target=%{vpxtarget} \
%endif
%ifarch %{arm}
--disable-neon --disable-neon_asm \
%endif
--enable-pic --disable-install-srcs \
--enable-vp9-decoder --enable-vp9-encoder \
--enable-experimental \
--enable-vp9-highbitdepth \
%if ! %{generic_target}
--enable-shared \
%endif
--enable-install-srcs \
--prefix=%{_prefix} --libdir=%{_libdir} --size-limit=16384x16384

%ifarch armv7hl
#hackety hack hack
sed -i "s|AR=armv7hl-redhat-linux-gnueabi-ar|AR=ar|g" libs-%{vpxtarget}.mk
sed -i "s|AR=armv7hl-redhat-linux-gnueabi-ar|AR=ar|g" examples-%{vpxtarget}.mk
sed -i "s|AR=armv7hl-redhat-linux-gnueabi-ar|AR=ar|g" docs-%{vpxtarget}.mk

sed -i "s|AS=armv7hl-redhat-linux-gnueabi-as|AS=as|g" libs-%{vpxtarget}.mk
sed -i "s|AS=armv7hl-redhat-linux-gnueabi-as|AS=as|g" examples-%{vpxtarget}.mk
sed -i "s|AS=armv7hl-redhat-linux-gnueabi-as|AS=as|g" docs-%{vpxtarget}.mk

sed -i "s|NM=armv7hl-redhat-linux-gnueabi-nm|NM=nm|g" libs-%{vpxtarget}.mk
sed -i "s|NM=armv7hl-redhat-linux-gnueabi-nm|NM=nm|g" examples-%{vpxtarget}.mk
sed -i "s|NM=armv7hl-redhat-linux-gnueabi-nm|NM=nm|g" docs-%{vpxtarget}.mk
%endif

make %{?_smp_mflags} verbose=true

# Manual shared library creation
# We should never need to do this anymore, and if we do, we need to fix the version-script.
%if %{generic_target}
mkdir tmp
cd tmp
ar x ../libvpx_g.a
cd ..
gcc -fPIC -shared -pthread -lm -Wl,--no-undefined -Wl,-soname,libvpx.so.%{somajor} -Wl,--version-script,%{SOURCE2} -Wl,-z,noexecstack -o libvpx.so.%{soversion} tmp/*.o
rm -rf tmp
%endif

# Temporarily dance the static libs out of the way
# mv libvpx.a libNOTvpx.a
# mv libvpx_g.a libNOTvpx_g.a

# We need to do this so the examples can link against it.
# ln -sf libvpx.so.%{soversion} libvpx.so

# make %{?_smp_mflags} verbose=true target=examples CONFIG_SHARED=1
# make %{?_smp_mflags} verbose=true target=docs

# Put them back so the install doesn't fail
# mv libNOTvpx.a libvpx.a
# mv libNOTvpx_g.a libvpx_g.a

%install
%ifarch armv7hl
export CROSS=armv7hl-redhat-linux-gnueabi-
export CHOST=armv7hl-redhat-linux-gnueabi-hardfloat
%endif
make DIST_DIR=%{buildroot}%{_prefix} dist

# Simpler to label the dir as %%doc.
if [ -d %{buildroot}%{_prefix}/docs ]; then
   mv %{buildroot}%{_prefix}/docs doc/
fi

# Again, we should never need to do this anymore.
%if %{generic_target}
install -p libvpx.so.%{soversion} %{buildroot}%{_libdir}
pushd %{buildroot}%{_libdir}
ln -sf libvpx.so.%{soversion} libvpx.so
ln -sf libvpx.so.%{soversion} libvpx.so.%{somajor}
ln -sf libvpx.so.%{soversion} libvpx.so.%{somajor}.%{sominor}
popd
%endif

pushd %{buildroot}
# Stuff we don't need.
rm -rf .%{_prefix}/build/ .%{_prefix}/md5sums.txt .%{_libdir}*/*.a .%{_prefix}/CHANGELOG .%{_prefix}/README
# No, bad google. No treat.
mv .%{_bindir}/examples/* .%{_bindir}
rm -rf .%{_bindir}/examples

# Rename a few examples
mv .%{_bindir}/postproc .%{_bindir}/vp8_postproc
mv .%{_bindir}/simple_decoder .%{_bindir}/vp8_simple_decoder
mv .%{_bindir}/simple_encoder .%{_bindir}/vp8_simple_encoder
mv .%{_bindir}/twopass_encoder .%{_bindir}/vp8_twopass_encoder
# Fix the binary permissions
chmod 755 .%{_bindir}/*
popd

# Get the vpx_config.h file
%ifarch %{arm}
cp -a vpx_config.h %{buildroot}%{_includedir}/vpx/vpx_config-arm.h
%else
# Does ppc64le need its own?
%ifarch ppc64 ppc64le
cp -a vpx_config.h %{buildroot}%{_includedir}/vpx/vpx_config-ppc64.h
%else
%ifarch s390 s390x
cp -a vpx_config.h %{buildroot}%{_includedir}/vpx/vpx_config-s390.h
%else
%ifarch %{ix86}
cp -a vpx_config.h %{buildroot}%{_includedir}/vpx/vpx_config-x86.h
%else
cp -a vpx_config.h %{buildroot}%{_includedir}/vpx/vpx_config-%{_arch}.h
%endif
%endif
%endif
%endif
cp %{SOURCE1} %{buildroot}%{_includedir}/vpx/vpx_config.h
# for timestamp sync
touch -r AUTHORS %{buildroot}%{_includedir}/vpx/vpx_config.h

mv %{buildroot}%{_prefix}/src/vpx_dsp %{buildroot}%{_includedir}/
mv %{buildroot}%{_prefix}/src/vpx_mem %{buildroot}%{_includedir}/
mv %{buildroot}%{_prefix}/src/vpx_ports %{buildroot}%{_includedir}/
mv %{buildroot}%{_prefix}/src/vpx_scale %{buildroot}%{_includedir}/

rm -rf %{buildroot}%{_prefix}/src

%ldconfig_scriptlets

%check
# This symbolic linking is needed for the tests to execute successfully.
ln -sf %{buildroot}%{_libdir}/libvpx.so.%{somajor} /usr/lib/libvpx.so.%{somajor}
make test

%files
%license LICENSE
%doc AUTHORS CHANGELOG README
%{_libdir}/libvpx.so.%{somajor}*

%files devel
# These are SDK docs, not really useful to an end-user.
%doc docs/html/
%{_includedir}/vpx/
%{_includedir}/vpx_dsp/
%{_includedir}/vpx_mem/
%{_includedir}/vpx_ports/
%{_includedir}/vpx_scale/
%{_libdir}/pkgconfig/vpx.pc
%{_libdir}/libvpx.so

%files utils
%{_bindir}/*

%changelog
* Wed Oct 04 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.13.1-1
- Auto-upgrade to 1.13.1 - to fix CVE.
- Add %check section.

* Mon Apr 25 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.8.2-4
- Updating source URLs.
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.8.2-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Dec 20 2019 Tom Callaway <spot@fedoraproject.org> - 1.8.2-1
- update to 1.8.2

* Wed Jul 31 2019 Tom Callaway <spot@fedoraproject.org> - 1.8.1-1
- update to 1.8.1

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Feb 05 2019 Pete Walter <pwalter@fedoraproject.org> - 1.8.0-4
- Avoid setting optflags twice

* Tue Feb 05 2019 Pete Walter <pwalter@fedoraproject.org> - 1.8.0-3
- Tighten soname glob to avoid accidental soname bumps

* Tue Feb 05 2019 Björn Esser <besser82@fedoraproject.org> - 1.8.0-2
- rebuilt (libvpx)

* Tue Feb 05 2019 Pete Walter <pwalter@fedoraproject.org> - 1.8.0-1
- Update to 1.8.0

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Sep 18 2018 Owen Taylor <otaylor@redhat.com> - 1.7.0-8
- Avoid hardcoding prefix=/usr

* Fri Jul 20 2018 Wim Taymans <wtaymans@redhat.com> - 1.7.0-7
- Add compilers as buildrequires

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Feb 12 2018 Tom Callaway <spot@fedoraproject.org> - 1.7.0-5
- properly set build flags in rawhide (bz1543819)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb  3 2018 Tom Callaway <spot@fedoraproject.org> - 1.7.0-3
- package more files (for firefox)
- setup vpx_config.h for multilib

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.7.0-2
- Switch to %%ldconfig_scriptlets

* Fri Jan 26 2018 Tom Callaway <spot@fedoraproject.org> - 1.7.0-1
- update to 1.7.0 (ABI change)

* Wed Jan 17 2018 Wim Taymans <wtaymans@wredhat.com> - 1.6.1-5
- fix for CVE-2017-13194

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 16 2017 Tom Callaway <spot@fedoraproject.org> - 1.6.1-1
- update to 1.6.1

* Thu Jan 12 2017 Tom Callaway <spot@fedoraproject.org> - 1.6.0-2
- enable vp9-highbitdepth (thanks to mike@cchtml.com)

* Fri Jul 22 2016 Tom Callaway <spot@fedoraproject.org> - 1.6.0-1
- update to 1.6.0

* Wed Mar 16 2016 Tom Callaway <spot@fedoraproject.org> - 1.5.0-4
- disable generic_target conditional universally (bz1311125)

* Tue Mar  8 2016 Tom Callaway <spot@fedoraproject.org> - 1.5.0-3
- enable-experimental and enable-spatial-svc

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Dec  1 2015 Tom Callaway <spot@fedoraproject.org> - 1.5.0-1
- update to 1.5.0

* Mon Sep 21 2015 Tom Callaway <spot@fedoraproject.org> - 1.4.0-6
- remove exit 0

* Tue Sep 15 2015 Tom Callaway <spot@fedoraproject.org> - 1.4.0-5
- set --size-limit=16384x16384 to avoid CVE-2015-1258

* Mon Jul 27 2015 Kalev Lember <klember@redhat.com> - 1.4.0-4
- Package review fixes (#1225648)
- Update URL
- Use license macro
- Escape a commented out macro

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.4.0-2
- Rebuilt for GCC 5 C++11 ABI change

* Mon Apr  6 2015 Tom Callaway <spot@fedoraproject.org> - 1.4.0-1
- update to 1.4.0

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Mar 20 2014 Wim Taymans <wtaymans@redhat.com> - 1.3.0-4
- fix Illegal Instruction abort

* Thu Feb 13 2014 Dan Horák <dan[at]danny.cz> - 1.3.0-3
- update library symbol list for 1.3.0 from Debian

* Tue Feb 11 2014 Tom Callaway <spot@fedoraproject.org> - 1.3.0-2
- armv7hl specific target

* Tue Feb 11 2014 Tom Callaway <spot@fedoraproject.org> - 1.3.0-1
- update to 1.3.0

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 28 2013 Tom Callaway <spot@fedoraproject.org> - 1.2.0-1
- update to 1.2.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 29 2012 Tom Callaway <spot@fedoraproject.org> - 1.1.0-1
- update to 1.1.0

* Tue May 29 2012 Tom Callaway <spot@fedoraproject.org> - 1.0.0-3
- fix vpx.pc file to include -lm (bz825754)

* Fri May 11 2012 Tom Callaway <spot@fedoraproject.org> - 1.0.0-2
- use included vpx.pc file (drop local libvpx.pc)
- apply upstream fix to vpx.pc file (bz 814177)

* Mon Jan 30 2012 Tom Callaway <spot@fedoraproject.org> - 1.0.0-1
- update to 1.0.0

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 10 2011 Dan Horák <dan[at]danny.cz> - 0.9.7.1-3
- use macro instead of hard-coded version

* Mon Sep 12 2011 Dan Horák <dan[at]danny.cz> - 0.9.7.1-2
- fix build on generic targets

* Tue Aug 16 2011 Adam Jackson <ajax@redhat.com> 0.9.7.1-1
- libvpx 0.9.7-p1

* Tue Aug 09 2011 Adam Jackson <ajax@redhat.com> 0.9.7-1
- libvpx 0.9.7

* Mon Mar 21 2011 Dan Horák <dan[at]danny.cz> - 0.9.6-2
- add 2 symbols to the shared library for generic targets

* Thu Mar 10 2011 Tom Callaway <spot@fedoraproject.org> - 0.9.6-1
- update to 0.9.6

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 17 2010 Tom "spot" Callaway <tcallawa@redhat.com> 0.9.5-2
- apply patch from upstream git (Change I6266aba7), should resolve CVE-2010-4203

* Mon Nov  1 2010 Tom "spot" Callaway <tcallawa@redhat.com> 0.9.5-1
- update to 0.9.5

* Wed Sep  1 2010 Tom "spot" Callaway <tcallawa@redhat.com> 0.9.1-3
- only package html docs to avoid multilib conflict (bz 613185)

* Thu Jun 24 2010 Tom "spot" Callaway <tcallawa@redhat.com> 0.9.1-2
- build shared library the old way for generic arches

* Thu Jun 24 2010 Tom "spot" Callaway <tcallawa@redhat.com> 0.9.1-1
- update to 0.9.1

* Fri Jun 11 2010 Tom "spot" Callaway <tcallawa@redhat.com> 0.9.0-7
- update to git revision 8389f1967c5f8b3819cca80705b1b4ba04132b93
- upstream fix for bz 599147
- proper shared library support

* Wed Jun  2 2010 Tom "spot" Callaway <tcallawa@redhat.com> 0.9.0-6
- add hackish fix for bz 599147 
  (upstream will hopefully fix properly in future release)

* Fri May 21 2010 Tom "spot" Callaway <tcallawa@redhat.com> 0.9.0-5
- fix noexecstack flag

* Thu May 20 2010 Tom "spot" Callaway <tcallawa@redhat.com> 0.9.0-4
- BuildRequires: yasm (we're optimized again)

* Thu May 20 2010 Tom "spot" Callaway <tcallawa@redhat.com> 0.9.0-3
- add pkg-config file
- move headers into include/vpx/
- enable optimization

* Thu May 20 2010 Tom "spot" Callaway <tcallawa@redhat.com> 0.9.0-2
- fix permissions on binaries
- rename generic binaries to v8_*
- link shared library to -lm, -lpthread to resolve missing weak symbols

* Wed May 19 2010 Tom "spot" Callaway <tcallawa@redhat.com> 0.9.0-1
- Initial package for Fedora
