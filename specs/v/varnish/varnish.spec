# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global _hardened_build 0
# https://github.com/varnishcache/varnish-cache/issues/2269
%global debug_package %{nil}

%global __provides_exclude_from ^%{_libdir}/varnish/vmods

%global abi 2e8180f788715e5bc44df08479d60c9435d79bdd
%global vrt 21.0

# Package scripts are now external
# https://github.com/varnishcache/pkg-varnish-cache
%global commit1 7d90347be31891b338dededb318594cebb668ba7
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})

# Default: Use jemalloc, as adviced by upstream project
# Change to 1 to use system allocator (ie. glibc)
#
# for rhel >= 10, use bundled jemalloc
# for rhel < 10, use system allocator
%bcond system_allocator %[0%{?rhel} && 0%{?rhel} < 10]
%bcond bundled_jemalloc %[0%{?rhel} >= 10]

%define jemalloc_version 5.3.0
%define jemalloc_prefix varnish_

%if %{with system_allocator}
# use _lto_cflags if present
%else
%global _lto_cflags %{nil}
%endif

Summary: High-performance HTTP accelerator
Name: varnish
Version: 7.7.1
Release: 4%{?dist}
License: BSD-2-Clause AND (BSD-2-Clause-FreeBSD AND BSD-3-Clause AND LicenseRef-Fedora-Public-Domain AND Zlib)
URL: https://www.varnish-cache.org/
Source0: http://varnish-cache.org/_downloads/%{name}-%{version}.tgz
Source1: https://github.com/varnishcache/pkg-varnish-cache/archive/%{commit1}.tar.gz#/pkg-varnish-cache-%{shortcommit1}.tar.gz
Source2: varnish.sysusers
Source3: https://github.com/jemalloc/jemalloc/releases/download/%{jemalloc_version}/jemalloc-%{jemalloc_version}.tar.bz2

# Fix for h2 switch in varnishtest
# https://github.com/varnishcache/varnish-cache/issues/4298
Patch0:   varnish-7.7.0_fix_4298.patch

%if %{with bundled_jemalloc}
# bundled jemalloc patch
Patch100: jemalloc-5.3.0_fno-builtin.patch
Patch101: jemalloc-5.3.0-aarch64-ts-segfault.patch
%endif

Provides: varnish%{_isa} = %{version}-%{release}
Provides: varnishd(abi)%{_isa} = %{abi}
Provides: varnishd(vrt)%{_isa} = %{vrt}

Provides: vmod(blob)%{_isa} = %{version}-%{release}
Provides: vmod(cookie)%{_isa} = %{version}-%{release}
Provides: vmod(debug)%{_isa} = %{version}-%{release}
Provides: vmod(directors)%{_isa} = %{version}-%{release}
Provides: vmod(h2)%{_isa} = %{version}-%{release}
Provides: vmod(proxy)%{_isa} = %{version}-%{release}
Provides: vmod(purge)%{_isa} = %{version}-%{release}
Provides: vmod(std)%{_isa} = %{version}-%{release}
Provides: vmod(unix)%{_isa} = %{version}-%{release}
Provides: vmod(vtc)%{_isa} = %{version}-%{release}

%if %{with bundled_jemalloc}
Provides: bundled(jemalloc)
%endif

BuildRequires: systemd-rpm-macros
%{?systemd_requires}
%{?sysusers_requires_compat}

BuildRequires: python3, python3-sphinx, python3-docutils
BuildRequires: gcc
%if %{without bundled_jemalloc}
%if %{with system_allocator}
# use glibc
%else
%ifnarch aarch64
BuildRequires: jemalloc-devel
%endif
%endif
%endif

BuildRequires: libedit-devel
BuildRequires: make
BuildRequires: ncurses-devel
BuildRequires: pcre2-devel
BuildRequires: pkgconfig

%if %{with bundled_jemalloc}
BuildRequires:  /usr/bin/xsltproc
BuildRequires:  perl-generators
%endif

# Extra requirements for the build suite
#   needs haproxy2
%if 0%{?fedora} > 30 || 0%{?rhel} > 8
BuildRequires: haproxy
%endif
BuildRequires: nghttp2

# Varnish actually needs gcc installed to work. It uses the C compiler
# at runtime to compile the VCL configuration files. This is by design.
Requires: gcc
Requires: logrotate
Requires: ncurses
Requires: pcre2
Requires: redhat-rpm-config
Requires(post): /usr/bin/uuidgen

%if %{with system_allocator}
# use glibc
%else
%if %{without bundled_jemalloc}
Requires: jemalloc
%endif
%endif

%description
This is Varnish Cache, a high-performance HTTP accelerator.

Varnish Cache stores web pages in memory so web servers don’t have to
create the same web page over and over again. Varnish Cache serves
pages much faster than any application server; giving the website a
significant speed up.

Documentation wiki and additional information about Varnish Cache is
available on: https://www.varnish-cache.org/

%package devel
Summary: Development files for %{name}
#BuildRequires: ncurses-devel
Provides: varnish-libs-devel%{?isa} = %{version}-%{release}
Provides: varnish-libs-devel = %{version}-%{release}
Obsoletes: varnish-libs-devel < %{version}-%{release}
Requires: %{name} = %{version}-%{release}
Requires: python3

%description devel
Development files for %{name}
Varnish Cache is a high-performance HTTP accelerator

%package docs
Summary: Documentation files for %name

%description docs
Documentation files for %name

%prep
%setup -q
%patch 0 -p1
tar xzf %SOURCE1
ln -s pkg-varnish-cache-%{commit1}/redhat redhat
ln -s pkg-varnish-cache-%{commit1}/debian debian
cp redhat/find-provides .
sed -i 's,rst2man-3.6,rst2man-3.4,g; s,rst2html-3.6,rst2html-3.4,g; s,phinx-build-3.6,phinx-build-3.4,g' configure

# jemalloc
%if %{with bundled_jemalloc}
tar xjf %SOURCE3
sed -i '/^LIBPREFIX/s/@libprefix@/@libprefix@%{jemalloc_prefix}/' jemalloc*/Makefile.in
pushd jemalloc*
%patch 100 -p1 -b .jemalloc
%patch 101 -p1 -b .ts-segfault
popd

# Override PAGESIZE, bz #1545539
%ifarch %ix86 %arm x86_64 s390x riscv64
%define lg_page --with-lg-page=12
%endif

%ifarch ppc64 ppc64le aarch64
%define lg_page --with-lg-page=16
%endif

# Disable thp on systems not supporting this for now
%ifarch %ix86 %arm aarch64 s390x
%define disable_thp --disable-thp
%endif
%endif

%build
%if %{with bundled_jemalloc}
# build bundled jemalloc first
pushd jemalloc*

echo "For debugging package builders"
echo "What is the pagesize?"
getconf PAGESIZE

echo "What mm features are available?"
ls /sys/kernel/mm
ls /sys/kernel/mm/transparent_hugepage || true
cat /sys/kernel/mm/transparent_hugepage/enabled || true

echo "What kernel version and config is this?"
uname -a

%configure %{?disable_thp} %{?lg_page} --enable-prof
make %{?_smp_mflags}
popd
%endif


# varnish
%if %{with system_allocator}
export CFLAGS="%{optflags}"
%else
# nilled _lto_cflags above because they remove the deps on jemalloc.
# On the fedoras, _lto_cflags is -flto=auto and -ffat-lto-objects. The latter is OK.
export CFLAGS="%{optflags} -ffat-lto-objects"
%endif

# https://gcc.gnu.org/wiki/FAQ#PR323
%ifarch %ix86
%if 0%{?fedora} > 21
export CFLAGS="$CFLAGS -ffloat-store -fexcess-precision=standard"
%endif
%endif

%if 0%{?fedora} > 41 || 0%{?rhel} > 10
export CFLAGS="$CFLAGS -std=gnu17"
%endif

%ifarch s390x
export CFLAGS="$CFLAGS -Wno-error=free-nonheap-object"
%endif

# What platform is this
uname -a

# What gcc version is this?
gcc --version

# What is the page size
getconf PAGESIZE

# Man pages are prebuilt. No need to regenerate them.
export RST2MAN=/bin/true
# Explicit python, please
export PYTHON=python3

for f in configure configure.ac; do
  sed -i 's|ljemalloc|l%{jemalloc_prefix}jemalloc|g' $f
done

%if %{with bundled_jemalloc}
export LDFLAGS="$LDFLAGS -L%{_builddir}/%{name}-%{version}/jemalloc-%{jemalloc_version}/lib"
%endif

%configure LT_SYS_LIBRARY_PATH=%_libdir \
 --disable-static \
  --localstatedir=/var/lib  \
  --with-contrib \
  --docdir=%{?_pkgdocdir}%{!?_pkgdocdir:%{_docdir}/%{name}-%{version}} \
%ifarch %ix86
%if 0%{?fedora} <= 37
  --enable-pcre2-jit=no \
%endif
%endif
%if %{with system_allocator} || %{without bundled_jemalloc}
  --with-jemalloc=no \
%endif

%if %{with bundled_jemalloc}
export LD_LIBRARY_PATH=%{_builddir}/%{name}-%{version}/jemalloc-%{jemalloc_version}/lib
%endif

%make_build

# One varnish user is enough
sed -i 's,User=varnishlog,User=varnish,g;' redhat/varnishncsa.service

# Clean up the html documentation
rm -rf doc/html/_sources

%check
# check jemalloc first
%if %{with bundled_jemalloc}
pushd jemalloc*
make %{?_smp_mflags} check
popd
%endif

# Up the stack size in tests, necessary on secondary arches
sed -i 's/thread_pool_stack 80k/thread_pool_stack 128k/g;' bin/varnishtest/tests/*.vtc
sed -i 's/file,2M/file,8M/' bin/varnishtest/tests/r04036.vtc

# This is a bug in varnishtest making it incompatible with nghttp2 >= 1.65
#if 0#{?fedora} > 41 || 0#{?rhel} > 10
#rm bin/varnishtest/tests/a02022.vtc
#endif

%if %{with bundled_jemalloc}
export LD_LIBRARY_PATH=%{_builddir}/%{name}-%{version}/jemalloc-%{jemalloc_version}/lib
%endif

# Just a hack to avoid too high load on secondary arch builders
%ifarch s390x ppc64le
# This works when ran alone, but not in the whole suite. Load and/or timing issues
rm bin/varnishtest/tests/t02014.vtc
make -j2 check
%else
%make_build check
%endif

%install
rm -rf %{buildroot}

# jemalloc
%if %{with bundled_jemalloc}
pushd jemalloc*
make DESTDIR=%{buildroot} install_lib %{?_smp_mflags}

find %{buildroot}%{_libdir}/ -name '*.a' -exec rm -vf {} ';'

# we don't need .pc file
rm  %{buildroot}%{_libdir}/pkgconfig/jemalloc.pc
popd
%endif

%{make_install}

# None of these for fedora
find %{buildroot}/%{_libdir}/ -name '*.la' -exec rm -f {} ';'

mkdir -p %{buildroot}/var/lib/varnish
mkdir -p %{buildroot}/var/log/varnish
mkdir -p %{buildroot}/var/run/varnish
mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d/
install -D -m 0644 etc/example.vcl %{buildroot}%{_sysconfdir}/varnish/default.vcl
install -D -m 0644 redhat/varnish.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/varnish
install -D -m 0644 include/vcs_version.h %{buildroot}%{_includedir}/varnish
install -D -m 0644 include/vrt.h %{buildroot}%{_includedir}/varnish

mkdir -p %{buildroot}%{_unitdir}
install -D -m 0644 redhat/varnish.service %{buildroot}%{_unitdir}/varnish.service
install -D -m 0644 redhat/varnishncsa.service %{buildroot}%{_unitdir}/varnishncsa.service
install -D -m 0755 redhat/varnishreload %{buildroot}%{_sbindir}/varnishreload
install -p -D -m 0644 %{SOURCE2} %{buildroot}%{_sysusersdir}/varnish.conf

echo %{_libdir}/varnish > %{buildroot}%{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf

# No idea why these ends up with mode 600 in the debug package
%if 0%{debug_package}
chmod 644 lib/libvmod_*/*.c
chmod 644 lib/libvmod_*/*.h
%endif

%pre
%sysusers_create_compat %{SOURCE2}

%files
%if "%{_sbindir}" != "%{_bindir}"
%{_sbindir}/*
%endif
%{_bindir}/*
%{_libdir}/*.so.*
%{_libdir}/%{name}
%{_var}/lib/varnish
%attr(0700,varnish,varnish) %dir %{_var}/log/varnish
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3*
%{_mandir}/man7/*.7*
%license LICENSE
%doc README.rst ChangeLog
%doc etc/builtin.vcl etc/example.vcl
%dir %{_sysconfdir}/varnish/
%config(noreplace) %{_sysconfdir}/varnish/default.vcl
%config(noreplace) %{_sysconfdir}/logrotate.d/varnish
%config %{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf

%{_unitdir}/varnish.service
%{_unitdir}/varnishncsa.service
%{_sysusersdir}/varnish.conf

%files devel
%license LICENSE
%doc README.rst
%{_libdir}/lib*.so
%{_includedir}/%{name}
%{_libdir}/pkgconfig/varnishapi.pc
%{_datadir}/%{name}
%{_datadir}/aclocal/*.m4

%files docs
%license LICENSE
%doc doc/html
%doc doc/changes*.html

%post
%systemd_post varnish varnishncsa
/sbin/ldconfig
test -f /etc/varnish/secret || (uuidgen > /etc/varnish/secret && chmod 0600 /etc/varnish/secret)

%postun
%systemd_postun_with_restart varnish varnishncsa
/sbin/ldconfig


%preun
%systemd_preun varnish varnishncsa


%changelog
* Fri Jun 31 2025 Luboš Uhliarik <luhliari@redhat.com> - 7.7.1-4
- bundle jemalloc in RHEL

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 7.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu May 22 2025 Ingvar Hagelund <ingvar@redpill-linpro.com> - 7.7.1-2
- Correct ABI and VRT versions
- Pulled el7 support
- Use systemd setup for users

* Tue May 20 2025 Luboš Uhliarik <luhliari@redhat.com> - 7.7.1-1
- new version 7.7.1

* Thu Mar 27 2025 Ingvar Hagelund <ingvar@redpill-linpro.com> - 7.7.0-2
- Fix for eln build (merged from yselkowitz)
- Fix for failing h2 switch check. Enabling full test suite again

* Mon Mar 24 2025 Ingvar Hagelund <ingvar@redpill-linpro.com> - 7.7.0-1
- New upstream release
- fedora now has completed the bin/sbin merge

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 7.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Dec 02 2024 Ingvar Hagelund <ingvar@redpill-linpro.com> - 7.6.1-1
- New upstream release

* Mon Sep 16 2024 Ingvar Hagelund <ingvar@redpill-linpro.com> - 7.6.0-1
- New upstream release
- Updated checkout of pkg-varnish

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Mar 19 2024 Ingvar Hagelund <ingvar@redpill-linpro.com> - 7.5.0-1
- New upstream release
- Moved somethings around to make the diff from the upstream spec less
- Upped some memory requirements in some of the tests. Necessary on aarch64 and ppc64le (and ppc32)
- Reduced number of parallel jobs on s390x builders as builds tend to fail when stressed
- Retired armv7hl

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Nov 08 2023 Ingvar Hagelund <ingvar@redpill-linpro.com> - 7.4.2-1
- New upstream release. A security release
- Includes fix for CVE-2023-44487 aka VSV00013, rhbz#2243328, HTTP/2 Rapid Reset Attack

* Thu Oct 12 2023 Ingvar Hagelund <ingvar@redpill-linpro.com> - 7.4.1-1
- New upstream release. A bugfix release

* Wed Oct 11 2023 Ingvar Hagelund <ingvar@redpill-linpro.com> - 7.4.0-0
- New upstream release

* Thu Sep 14 2023 Luboš Uhliarik <luhliari@redhat.com> - 7.3.0-5
- SPDX migration

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 7.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jun 23 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 7.3.0-3
- Enable system_allocator in RHEL/ELN builds

* Mon Mar 20 2023 Ingvar Hagelund <ingvar@redpill-linpro.com> - 7.3.0-2
- Switched from bcond to bcond_with for compatibility with el8 and el9
- haproxy builddep on systems with haproxy2
- Disable pcre2-jit only for fedora <= 37 on 32bit x86

* Thu Mar 16 2023 Ingvar Hagelund <ingvar@redpill-linpro.com> - 7.3.0-1
- New upstream release
- Added a bcond system_allocator for skipping jemalloc, bz#1917697
- nil _lto_cflags macro to link to jemalloc again
- disable pcre2-jit on 32bit x86 for now

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 7.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Nov 09 2022 Ingvar Hagelund <ingvar@redpill-linpro.com> - 7.2.1-1
- New upstream release: A security release
- Includes fix for VSV00011

* Fri Sep 16 2022 Ingvar Hagelund <ingvar@redpill-linpro.com> - 7.2.0-1
- New upstream release. The regular bi-annual "fresh" release
- Removed list of patches from comments
- Cosmetical changes to specfile from upstream
- Now build with --with-contrib

* Fri Aug 12 2022 Ingvar Hagelund <ingvar@redpill-linpro.com> - 7.1.1-1
- New upstream release. A security release
- Includes fix for VSV00009 aka CVE-2022-38150

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Mar 29 2022 Ingvar Hagelund <ingvar@redpill-linpro.com> - 7.1.0-1
- New upstream release
- Includes updated snapshot of pkg-varnish

* Mon Feb 21 2022 Luboš Uhliarik <luhliari@redhat.com> - 7.0.2-2
- Fix Provides directive for varnish-devel package

* Wed Jan 26 2022 Ingvar Hagelund <ingvar@redpill-linpro.com> - 7.0.2-1
- New upstream release. A security release
- Includes fix for CVE-2022-23959 aka VSV00008, rhbz#2045033

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jan 13 2022 Ingvar Hagelund <ingvar@redpill-linpro.com> - 7.0.1-2
- Update ABI string

* Thu Jan 13 2022 Ingvar Hagelund <ingvar@redpill-linpro.com> - 7.0.1-1
- New upstream release. A maintenance and stability release

* Tue Nov 02 2021 Ingvar Hagelund <ingvar@redpill-linpro.com> - 7.0.0-2
- upstream switched to pcre2 a while ago

* Thu Sep 16 2021 Ingvar Hagelund <ingvar@redpill-linpro.com> - 7.0.0-1
- New upstream release
- Updated pkg-varnish checkout from the 7.0 branch

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Jul 17 2021 Ingvar Hagelund <ingvar@redpill-linpro.com> 6.6.1-2
- Bumped abi and vrt versions

* Sat Jul 17 2021 Ingvar Hagelund <ingvar@redpill-linpro.com> 6.6.1-1
- New upstream release
- Includes fix for CVE-2021-36740 aka VSV00007, bz#1982413

* Tue May 18 2021 Timm Bäder <tbaeder@redhat.com> - 6.6.0-2
- Use make macros

* Mon Mar 15 2021 Ingvar Hagelund <ingvar@redpill-linpro.com> - 6.6.0-1
- New upstream release
- Now provides vmod_purge
- Uses haproxy in the test suite on el8
- Skipped obsoleting varnish-libs. That was many years ago now.

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 6.5.1-4
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan 21 2021 Ingvar Hagelund <ingvar@redpill-linpro.com> 6.5.1-2
- Pulled support for el6
- Pulled support for sysvinit
- aarch64 builds now with jemalloc again on el7

* Fri Sep 25 2020 Ingvar Hagelund <ingvar@redpill-linpro.com> 6.5.1-1
- New upstream release varnish-6.5.1

* Wed Sep 16 2020 Ingvar Hagelund <ingvar@redpill-linpro.com> 6.5.0-1
- New upstream release varnish-6.5.0
- Respun silly patch to get rid of compiler warnings on el6

* Tue Aug 04 2020 Ingvar Hagelund <ingvar@redpill-linpro.com> 6.4.0-4
- Added -Wno-error=free-nonheap-object to CFLAGS to build on s390x

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.4.0-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Mar 16 2020 Ingvar Hagelund <ingvar@redpill-linpro.com> - 6.4.0-1
- New upstream release
- Respin patches for 6.4.0
- Removed patches merged upstream
- Deactivated a test on s390*. Too hard to get size and timing right

* Wed Feb 12 2020 Ingvar Hagelund <ingvar@redpill-linpro.com> - 6.3.2-3
- Got corrected compilation fix patch from upstream

* Tue Feb 11 2020 Ingvar Hagelund <ingvar@redpill-linpro.com> - 6.3.2-2
- Added simple compilation fix for gcc-10.0.1/s390x

* Tue Feb 11 2020 Ingvar Hagelund <ingvar@redpill-linpro.com> - 6.3.2-1
- New upstream release, a security release. Includes fix for VSV00005
- Added new checkout of pkg-varnish
- Temporarily disable haproxy unit tests, as haproxy seems broken in rawhide

* Mon Feb 10 2020 Joe Orton <jorton@redhat.com> - 6.3.1-3
- drop buildreq on (retired) vttest (#1800232)

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Oct 22 2019 Ingvar Hagelund <ingvar@redpill-linpro.com> - 6.3.1-1
- New upstream release. A security release. Includes fix for VSV00004

* Fri Sep 20 2019 Ingvar Hagelund <ingvar@redpill-linpro.com> - 6.3.0-2
- Respin patch for el6

* Mon Sep 16 2019 Ingvar Hagelund <ingvar@redpill-linpro.com> - 6.3.0-1
- New upstream release

* Wed Sep 04 2019 Ingvar Hagelund <ingvar@redpill-linpro.com> - 6.2.1-4
- New upstream release. A security release. Includes fix for CVE-2019-15892

* Thu Aug 08 2019 Ingvar Hagelund <ingvar@redpill-linpro.com> - 6.2.0-4
- Pull in extra requirements to the build requirements to run more
  tests (on fedora: haproxy, vttest)

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Apr 04 2019 Ingvar Hagelund <ingvar@redpill-linpro.com> - 6.2.0-2
- Run configure with LT_SYS_LIBRARY_PATH, removing the need for
  killing RPATH in libtool with sed and scattering LD_LIBRARY_PATH around
  with patches
- Some explicit python version fixes needed for el7 python34 vs python36
- aarch64 now builds with jemalloc again on fedora

* Fri Mar 15 2019 Ingvar Hagelund <ingvar@redpill-linpro.com> - 6.2.0-1
- New upstream release varnish-6.2
- Removed patches merged upstream
- Remove misc sed hacks for bugs that are fixed upstream
- Added a patch for gcc-4.4 -Werror support on el6
- Added a patch from upstream to fix too small thread pool stack in a test
- Override macro __python to make brp-python-bytecompile choose python3
- Explicitly use python-3.4
- Switch to make_install macro
- Better documentation of patches
- Updated checkout of pkg-varnish-cache

* Thu Mar 07 2019 Ingvar Hagelund <ingvar@redpill-linpro.com> - 6.1.1-5
- Adding a patch based on upstream commits, fixing pcre-jit, see 
  upstream bug 2912

* Thu Feb 14 2019 Ingvar Hagelund <ingvar@redpill-linpro.com> - 6.1.1-4
- Adding a patch from upstream fixing a simple formatting bug on gcc-9

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Nov 07 2018 Ingvar Hagelund <ingvar@redpill-linpro.com> - 6.1.1-2
- Respun ld_library_path patch for varnish-6.1.1

* Wed Nov 07 2018 Ingvar Hagelund <ingvar@redpill-linpro.com> - 6.1.1-1
- New upstream release

* Tue Nov 06 2018 Ingvar Hagelund <ingvar@redpill-linpro.com> - 6.1.0-3
- Dropped the depricated external dependency generator in Fedora
- Hard coded vmod, abi and vrt provides

* Fri Nov 02 2018 Ingvar Hagelund <ingvar@redpill-linpro.com> - 6.1.0-2
- Added a patch to fix a failing test in the testsuite

* Fri Nov 02 2018 Ingvar Hagelund <ingvar@redpill-linpro.com> - 6.1.0-1
- New upstream release
- Respin patches for 6.1.0
- Disable pcre-jit for now, ref upstream bug #2817

* Tue Oct 09 2018 Ingvar Hagelund <ingvar@redpill-linpro.com> - 6.0.1-3
- Explicitly using utf8 under install on el6 and el7 for python quirks

* Tue Oct 09 2018 Ingvar Hagelund <ingvar@redpill-linpro.com> - 6.0.1-2
- Explicitly using python3 on all targets

* Thu Sep 27 2018 Ingvar Hagelund <ingvar@redpill-linpro.com> - 6.0.1-1
- New upstream release
- Removed graphciz from BuildRequires. It is not used
- Removed patch for fortify_source on el6. It is merged upstream
- Small workaround for test suite problem with old readline/curses on el6
- Supports bcond_with python3, for simpler future deprication of python2
- Added -fno-exceptions to CFLAGS on el6, see upstream issue #2793

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Apr 25 2018 Ingvar Hagelund <ingvar@redpill-linpro.com> - 6.0.0-1
- New upstream release
- Added a patch that fixes _FORTIFY_SOURCE=2 on copr/el6
- Added a patch fixing compilation on epel6
- Fresh checkout of pkg-varnish-cache
- Updated find-requires sed fix to update variant and moved it to prep
- Removed -libs subpackage
- varnish_reload_vcl changed name to varnishreload, as in upstream
- varnish.params is gone. To override startup configuration,
  use /etc/systemd/system/varnish.service
- Dropped patch and sed fixes for find-provides, as it is fixed upstream
- Dropped patch for test vsv00002, as it is fixed upstream
- Droppet patch for python3, as it is included upstream
- Dropped buildreq on groff, as tarball includes prebuilt manpages
- Dropped systemv to systemd helpers
- Updated project url
- Use prebuilt html files for docs subpackage
- Dropped unnecessary explicit require of initscripts, closes #1592398

* Wed Mar 28 2018 Joe Orton <jorton@redhat.com> - 5.2.1-5
- add conditional build support for Python 3

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.1-4.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Dec 21 2017 Ingvar Hagelund <ingvar@redpill-linpro.com> - 5.2.1-4
- Disabled pcre-jit on x86_64 and arm in rawhide for now. It does not
  work, and makes other varnish dependant packages crash
  (upstream bug #2521)

* Thu Nov 16 2017 Ingvar Hagelund <ingvar@redpill-linpro.com> - 5.2.1-3
- Disabled running make check again. Too many timing issues. All tests run
  successfully on all arches from time to time, but seldom in a single
  run while all redhat builders are loaded.

* Thu Nov 16 2017 Ingvar Hagelund <ingvar@redpill-linpro.com> - 5.2.1-2
- Added patch for vsv00002 on ppc64[le]
- Added buildreq on nghttp2 for the test suite

* Wed Nov 15 2017 Ingvar Hagelund <ingvar@redpill-linpro.com> - 5.2.1-1
- New upstream release. A security release
  Includes fix for CVE-2017-8807, closes 1512798, 1513523, 1513524

* Mon Oct 23 2017 Ingvar Hagelund <ingvar@redpill-linpro.com> - 5.2.0-2
- Use ix86 macro for all ifarch matches of 32bit x86 hardware
- Added Makefile hack for el6 also to libvarnishapi

* Thu Oct 12 2017 Ingvar Hagelund <ingvar@redpill-linpro.com> - 5.2.0-1
- New upstream release

* Fri Aug 04 2017 Ingvar Hagelund <ingvar@redpill-linpro.com> - 5.1.3-2
- Disabled jemalloc on aarch64, as it fails reproducably
- Disabled running make check. Too many timing issues. All tests run
  successfully on all arches from time to time, but not in a single
  run.

* Thu Aug 03 2017 Ingvar Hagelund <ingvar@redpill-linpro.com> - 5.1.3-1
- New upstream release, including fix for VSV00001

* Wed Aug 02 2017 Patrick Uiterwijk <patrick@puiterwijk.org> - 5.1.2-3
- Added patch for vsv00001

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.2-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Apr 07 2017 Ingvar Hagelund <ingvar@redpill-linpro.com> 5.1.2-1
- New upstream release
- Updated pkg-varnish checkout to 5b97619, setting systemd memlock limit
  to actual 82MB, as it says in the comment
- Disabled stripping and building of debug packages, upstream issue #2269

* Thu Mar 16 2017 Ingvar Hagelund <ingvar@redpill-linpro.com> 5.1.1-1
- New upstream release
- Rebased patches for 5.1.1
- Removed patches merged upstream
- Pulled support for rhel5 and clones
- Updated pkg-varnish checkout to 92373fe

* Mon Feb 13 2017 Ingvar Hagelund <ingvar@redpill-linpro.com> 5.0.0-2
- Updated snapshot of pgk-varnish
- Added a patch for varnish_reload_vcl, fixes stricter vcl names 

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Sep 14 2016 Ingvar Hagelund <ingvar@redpill-linpro.com> 5.0.0-1
- New upstream release: 5.0.0
- Rebased patches for 5.0.0
- Added patch from upstream fixing a h/2 bug visible on secondary arches
- New snapshot of pkg-varnish
- Some cosmetic changes to reduce the diff to the upstream specfile
- Renamed subpackage varnish-libs-devel to just varnish-devel
  (as in upstream)
- Removed varnishlog initrc and systemd start scripts, as in upstream
  (Nobody should run varnishlog as a daemon continously)

* Thu Sep 01 2016 Ingvar Hagelund <ingvar@redpill-linpro.com> 4.1.3-5
- Changed ownership of varnishlog and varnishncsa logs, as previous
  versions have had them run as root
- Removed old outcommented config that is no longer in use

* Mon Aug 29 2016 Ingvar Hagelund <ingvar@redpill-linpro.com> 4.1.3-4
- Removed out-commented stuff about building from git
- Removed out-commented sub package -libs-static
- Use user varnish also for varnishlog and varnishncsa (#1371181)
- Changed owner of /var/log/varnish, so varnishlog/ncsa can start (#1371181)
- Reduced the number of parallell checks, to not overflow the builders

* Fri Aug 05 2016 Ingvar Hagelund <ingvar@redpill-linpro.com> 4.1.3-3
- Reduced the number of parallell checks ran by make, to reduce 
  stress on the builders

* Fri Aug 05 2016 Ingvar Hagelund <ingvar@redpill-linpro.com> 4.1.3-2
- Added python2.4 fix for el5 to the fedora tree

* Thu Aug 04 2016 Ingvar Hagelund <ingvar@redpill-linpro.com> 4.1.3-1
- New upstream release
- New snapshot of pkg-varnish, commit 4e27994
- README is now named README.rst
- Rebased Werror patch for el6
- vmod vcc files readable for all users
- set explicit python version in vmodtool.py
- Remove superflous Makefile.in.orig generated by patch

* Thu Mar 31 2016 Ingvar Hagelund <ingvar@redpill-linpro.com> 4.1.2-2
- Added missing tarball for pkg-varnish

* Tue Mar 29 2016 Ingvar Hagelund <ingvar@redpill-linpro.com> 4.1.2-1
- New upstream realease
- New checkout of pkg-varnish-cache from github
- Removed systemd patches now merged upstream
- Updated fix_python_24 patch for el5
- General i386 floating point precision fix (was fix for gcc6) now for more
  fedoras/el variants

* Mon Feb 29 2016 Ingvar Hagelund <ingvar@redpill-linpro.com> 4.1.1-4
- Rebuilt against jemalloc-4.1.0-1
- fix for gcc6 now for fedora >23

* Thu Feb 04 2016 Ingvar Hagelund <ingvar@redpill-linpro.com> 4.1.1-3
- Added "-ffloat-store -fexcess-precision=standard" to CFLAGS on i386
  to work around a bug in gcc6, see
  https://github.com/dhobsd/Varnish-Cache/commit/9f1035d 
- Quieted unpacking of distro package source

* Wed Feb 03 2016 Ingvar Hagelund <ingvar@redpill-linpro.com> 4.1.1-2
- Added patch from upstream, daemonizing varnishd in systemd, as
  it handles SIGHUP otherwice when running foregrounded under systemd

* Fri Jan 29 2016 Ingvar Hagelund <ingvar@redpill-linpro.com> 4.1.1-1
- New upstream release
- Rebased sphinx build patch
- Removed patch for dns corner case, it has been fixed upstream
- Removed patch for pcre madness test. It has been removed
- Added new source pkg-varnish-cache from github, replacing varnish-cache-redhat
- Also stop varnishlog and varnishncsa on package removal
- Removed redhat/README.rst. It is no longer included upstream

* Wed Oct 21 2015 Ingvar Hagelund <ingvar@redpill-linpro.com> 4.1.0-2
- Moved LICENSE to license catalog for fedora and el7

* Fri Oct 09 2015 Ingvar Hagelund <ingvar@redpill-linpro.com> 4.1.0-1
- New upstream release 4.1.0
- Changed buildreqs list to be one per line
- Skipped patches included upstream
- Rebased sphinx build patch
- Changed description to match upstream
- Added basic buildreqs gcc and make
- Included vcs_version.h and vrt.h to produce correct provides, even 
  when building in a non-standard buildroot
- Patched local find_provides similarily
- Added a couple of patches that adjusts test values for the koji 
  i686 and ppc64 build servers
- Added -fPIC and -pie for el6 rebuilds
- redhat subdir is now fetched from new upstream gitrepo

* Tue Sep 01 2015 Ingvar Hagelund <ingvar@redpill-linpro.com> 4.0.3-6
- Rebuilt for jemalloc-4.0.0

* Wed Aug 26 2015 Ingvar Hagelund <ingvar@redpill-linpro.com> 4.1.0-0.1.tp1
- Added patch for varnish unix-jail, instead of old-style -u user

* Fri Aug 21 2015 Ingvar Hagelund <ingvar@redpill-linpro.com> 4.1.0-0.0.tp1
- New upstream tech preview release
- Removed patches included upstream
- Prebuild html docs now placed in doc dir already

* Fri Aug 21 2015 Ingvar Hagelund <ingvar@redpill-linpro.com> 4.0.3-5
- Added example vcl files explicitly. They are installed by make, but
  have been removed by the cleaning of docroot in older rpmbuild. This makes
  varnish build again in rawhide

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.3-4.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 27 2015 Ingvar Hagelund <ingvar@redpill-linpro.com> 4.0.3-4
- libs-devel package now requires python, closing #1225243

* Fri Mar 13 2015 Ingvar Hagelund <ingvar@redpill-linpro.com> 4.0.3-3
- Added a patch fixing a crash on bogus content-length header,
  closing #1200034

* Fri Mar 06 2015 Ingvar Hagelund <ingvar@redpill-linpro.com> 4.0.3-2
- Added selinux module for varnish4 on el6

* Thu Mar 05 2015 Ingvar Hagelund <ingvar@redpill-linpro.com> 4.0.3-1
- New upstream release
- Removed systemd patch included upstream
- Rebased trivial Werr-patch for varnish-4.0.3
- Added patch to build on el5

* Tue Nov 25 2014 Ingvar Hagelund <ingvar@redpill-linpro.com> 4.0.2-1
- New upstream release
- Rebased sphinx makefile patch
- Added systemd services patch from Federico Schwindt

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.1-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul 30 2014 Ingvar Hagelund <ingvar@redpill-linpro.com> 4.0.1-2
- Rebased patch for el6

* Wed Jul 30 2014 Ingvar Hagelund <ingvar@redpill-linpro.com> 4.0.1-1 
- New upstream release 
- systemd support for rhel7 
- Dropped patches included upstream 

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.0-3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 23 2014 Ingvar Hagelund <ingvar@redpill-linpro.com> 4.0.0-3
- Added a patch that fixes broken find_provides and hard coded provides
  from upstream
- Added _isa macro to the libs dependency and updated Group definitions to
  more modern tags, closes bz 1090196
- Added aclocal macros to libs-devel sub package

* Tue Apr 22 2014 Ingvar Hagelund <ingvar@redpill-linpro.com> 4.0.0-2
- Use _pkgdocdir macro on fedora

* Fri Apr 11 2014 Ingvar Hagelund <ingvar@redpill-linpro.com> 4.0.0-1
- New upstream release
- Updated patches to match new release
- Dropped patches included upstream

* Tue Apr 01 2014 Ingvar Hagelund <ingvar@redpill-linpro.com> 4.0.0-0.4.beta1
- New upstream beta release
- Added a few patches from upstream git for building on ppc

* Wed Mar 12 2014 Ingvar Hagelund <ingvar@redpill-linpro.com> 4.0.0-0.3.tp2+20140327
- Daily snapshot build

* Wed Mar 12 2014 Ingvar Hagelund <ingvar@redpill-linpro.com> 4.0.0-0.2.tp2+20140306
- First try on wrapping 4.0.0-tp2+ daily snapshot series
- Added the rc and __find_provides macros from upstream
- Added LD_LIBRARY_PATH fix for varnishd-to-sphinx doc thing
- Changed LD_LIBRARY_PATH for make check to something more readable
- etc/zope-plone.vcl is gone. example.vcl replaces default.vcl as example vcl doc
- Now using example.vcl for /etc/varnish/default.vcl
- Added docdir to configure call, to get example docs in the right place
- Systemd scripts are now upstream
- Added some explicit provides not found automatically

* Tue Dec 03 2013 Ingvar Hagelund <ingvar@redpill-linpro.com> 3.0.5-1
- New upstream release
- Dropped patch for CVE-2013-4484, as it's in upstream

* Thu Nov 21 2013 Ingvar Hagelund <ingvar@redpill-linpro.com> 3.0.4-2
- Changed default mask for varnish log dir to 700, closing #915413 
- Added a patch for CVE-2013-4484 from upstream, closing #1025128

* Mon Aug 12 2013 Ingvar Hagelund <ingvar@redpill-linpro.com> 3.0.4-1
- New upstream release
- Added libedit-devel to the build reqs
- Changed the old-style initrc sed patching to a blacklist as in upstream
- Some tab vs space cleanup to make rpmlint more happy
- Added requirement of redhat-rpm-config, which provides redhat-hardened-cc1,
  needed for _hardened_build, closes #975147
- Removed no-pcre patch, as pcre is now switched off by default upstream

* Sun Jul 28 2013 Dennis Gilmore <dennis@ausil.us> - 3.0.3-6
- no pcre jit on arm arches

* Wed May 15 2013 Ingvar Hagelund <ingvar@redpill-linpro.com> 3.0.3-5
- Added macro _hardened_build to enforce compiling with PIE, closes #955156
- moved ldconfig in postun script to a shell line, since the following lines
  may expand to more shell commands on fedora >=18
- Corrected some bogus dates in the changelog

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 09 2012 Ingvar Hagelund <ingvar@redpill-linpro.com> - 3.0.3-3
- Upped the minimum number of threads from 1 to 5, closes #861493

* Tue Sep 18 2012 Ingvar Hagelund <ingvar@redpill-linpro.com> - 3.0.3-2
- Added a patch from phk, fixing upstream ppc64 bug #1194

* Tue Aug 21 2012 Ingvar Hagelund <ingvar@redpill-linpro.com> - 3.0.3-1
- New upstream release
- Remove unneeded hacks for ppc
- Remove hacks for rhel4, we no longer support that
- Remove unneeded hacks for docs, since we use the pregenerated docs
- Add new systemd scriptlets from f18+
- Added a patch switching off pcre jit on i386 and ppc to avoid upstream bug #1191 

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Mar 12 2012 Ingvar Hagelund <ingvar@redpill-linpro.com> - 3.0.2-2
- Added PrivateTmp=true to varnishd unit file, closing #782539
- Fixed comment typos in varnish unit file

* Tue Mar 06 2012 Ingvar Hagelund <ingvar@redpill-linpro.com> - 3.0.2-1
- New upstream version 3.0.2
- Removed INSTALL as requested by rpmlint
- Added a ld.so.conf.d fragment file listing libdir/varnish 
- Removed redundant doc/html/_sources
- systemd support from fedora 17
- Stopped using macros for make and install, according to 
  Fedora's packaging guidelines
- Changes merged from upstream:
  - Added suse_version macro
  - Added comments on building from a git checkout
  - mkpasswd -> uuidgen for fewer dependencies
  - Fixed missing quotes around cflags for pcre
  - Removed unnecessary 32/64 bit parallell build hack as this is fixed upstream
  - Fixed typo in configure call, disable -> without
  - Added lib/libvgz/.libs to LD_LIBRARY_PATH in make check
  - Added section 3 manpages
  - Configure with --without-rst2man --without-rst2html
  - changelog entries
- Removed unnecessary patch for system jemalloc, upstream now supports this

* Fri Feb 10 2012 Petr Pisar <ppisar@redhat.com> - 2.1.5-4
- Rebuild against PCRE 8.30

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb 01 2011 Ingvar Hagelund <ingvar@redpill-linpro.com> - 2.1.5-1
- New upstream release
- New download location
- Moved varnish_reload_vcl to sbin
- Removed patches included upstream
- Use jemalloc as system installed library

* Mon Nov 15 2010 Ingvar Hagelund <ingvar@redpill-linpro.com> - 3.0.0-0.svn20101115r5543
- Merged some changes from fedora
- Upped general version to 3.0 prerelease in trunk

* Thu Nov 04 2010 Ingvar Hagelund <ingvar@redpill-linpro.com> - 2.1.4-4
- Added a patch fixing a missing echo in the init script that
  masked failure output from the script
- Added a patch from upstream, fixing a problem with Content-Length
  headers (upstream r5461, upstream bug #801)
- Added a patch from upstream, adding empty Default-Start and Default-Stop
  to initscripts for better lsb compliance
- Added varnish_reload_vcl from trunk
- Synced descriptions from release spec

* Thu Oct 28 2010 Ingvar Hagelund <ingvar@redpill-linpro.com> - 2.1.4-3
- Fixed missing manpages because of no rst2man in rhel4 and 5

* Mon Oct 25 2010 Ingvar Hagelund <ingvar@redpill-linpro.com> - 2.1.4-2
- Removed RHEL6/ppc64 specific patch that has been included upstream

* Mon Oct 25 2010 Ingvar Hagelund <ingvar@redpill-linpro.com> - 2.1.4-1
- New upstream release
- New URL for source tarball and main website
- Prebuilt html docs now included, use that instead of running sphinx
- Putting sphinx generated doc in a separate subpackage
- Replaced specific include files with a wildcard glob
- Needs python-sphinx and deps to build sphinx documentation

* Tue Aug 24 2010 Ingvar Hagelund <ingvar@redpill-linpro.com> - 2.1.3-2
- Added a RHEL6/ppc64 specific patch that changes the hard coded
  stack size in tests/c00031.vtc

* Thu Jul 29 2010 Ingvar Hagelund <ingvar@redpill-linpro.com> - 2.1.4-0.svn20100824r5117
- Replaced specific include files with a wildcard glob
- Needs python-sphinx and deps to build sphinx documentation
- Builds html and latex documentation. Put that in a subpackage varnish-docs

* Thu Jul 29 2010 Ingvar Hagelund <ingvar@redpill-linpro.com> - 2.1.3-1
- New upstream release
- Add a patch for jemalloc on s390 that lacks upstream

* Wed May 05 2010 Ingvar Hagelund <ingvar@redpill-linpro.com> - 2.1.2-1
- New upstream release
- Remove patches merged upstream

* Tue Apr 27 2010 Ingvar Hagelund <ingvar@linpro.no> - 2.1.1-1
- New upstream release
- Added a fix for missing pkgconfig/libpcre.pc on rhel4
- Added a patch from trunk making the rpm buildable on lowspec
  build hosts (like Red Hat's ppc build farm nodes)
- Removed patches that are merged upstream

* Wed Apr 14 2010 Ingvar Hagelund <ingvar@linpro.no> - 2.1.0-2
- Added a patch from svn that fixes changes-2.0.6-2.1.0.xml

* Tue Apr 06 2010 Ingvar Hagelund <ingvar@linpro.no> - 2.1.0-1
- New upstream release; note: Configuration changes, see the README
- Removed unneeded patches 
- CVE-2009-2936: Added a patch from Debian that adds the -S option 
  to the varnisdh(1) manpage and to the sysconfig defaults, thus
  password-protecting the admin interface port (#579536,#579533)
- Generates that password in the post script, requires mkpasswd
- Added a patch from Robert Scheck for explicit linking to libm
- Requires pcre

* Wed Dec 23 2009 Ingvar Hagelund <ingvar@linpro.no> - 2.0.6-2
- Added a test that enables jemalloc on ppc if the kernel is
  not a rhel5 kernel (as on redhat builders)
- Removed tests c00031.vtc and r00387on rhel4/ppc as they fail
  on the Red Hat ppc builders (but works on my rhel4 ppc instance)
- Added a patch that fixes broken changes-2.0.6.html in doc

* Mon Dec 14 2009 Ingvar Hagelund <ingvar@linpro.no> - 2.0.6-1
- New upstream release
- Removed patches for libjemalloc, as they are added upstream

* Mon Nov 09 2009 Ingvar Hagelund <ingvar@linpro.no> - 2.0.5-1
- New upstream release

* Thu Aug 13 2009 Ingvar Hagelund <ingvar@linpro.no> - 2.0.4-4
- Added a sparc specific patch to libjemalloc.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 04 2009 Ingvar Hagelund <ingvar@linpro.no> - 2.0.4-2
- Added a s390 specific patch to libjemalloc.

* Fri Mar 27 2009 Ingvar Hagelund <ingvar@linpro.no> - 2.0.4-1
  New upstream release 2.0.4 

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 11 2009 Ingvar Hagelund <ingvar@linpro.no> - 2.0.3-1
  New upstream release 2.0.3. A bugfix and feature enhancement release

* Fri Dec 12 2008 Ingvar Hagelund <ingvar@linpro.no> - 2.0.2-2
  Added a fix for a timeout bug, backported from trunk

* Mon Nov 10 2008 Ingvar Hagelund <ingvar@linpro.no> - 2.0.2-1
  New upstream release 2.0.2. A bugfix release

* Sun Nov 02 2008 Ingvar Hagelund <ingvar@linpro.no> - 2.0.1-2
- Removed the requirement for kernel => 2.6.0. All supported
  platforms meets this, and it generates strange errors in EPEL

* Fri Oct 17 2008 Ingvar Hagelund <ingvar@linpro.no> - 2.0.1-1
- 2.0.1 released, a bugfix release. New upstream sources
- Package now also available in EPEL

* Thu Oct 16 2008 Ingvar Hagelund <ingvar@linpro.no> - 2.0-2
- Readded the debugflag patch. It's so practical
- Added a strange workaround for make check on ppc64

* Wed Oct 15 2008 Ingvar Hagelund <ingvar@linpro.no> - 2.0-1
- 2.0 released. New upstream sources
- Disabled jemalloc on ppc and ppc64. Added a note in README.redhat
- Synced to upstream again. No more patches needed

* Wed Oct 08 2008 Ingvar Hagelund <ingvar@linpro.no> - 2.0-0.11.rc1
- 2.0-rc1 released. New upstream sources
- Added a patch for pagesize to match redhat's rhel5 ppc64 koji build boxes
- Added a patch for test a00008, from r3269
- Removed condrestart in postscript at upgrade. We don't want that

* Fri Sep 26 2008 Ingvar Hagelund <ingvar@linpro.no> - 2.0-0.10.beta2
- 2.0-beta2 released. New upstream sources
- Whitespace changes to make rpmlint more happy

* Fri Sep 12 2008 Ingvar Hagelund <ingvar@linpro.no> - 2.0-0.9.20080912svn3184
- Added varnisncsa init script (Colin Hill)
- Corrected varnishlog init script (Colin Hill)

* Tue Sep 09 2008 Ingvar Hagelund <ingvar@linpro.no> - 2.0-0.8.beta1
- Added a patch from r3171 that fixes an endian bug on ppc and ppc64
- Added a hack that changes the varnishtest ports for 64bits builds,
  so they can run in parallell with 32bits build on same build host

* Tue Sep 02 2008 Ingvar Hagelund <ingvar@linpro.no> - 2.0-0.7.beta1
- Added a patch from r3156 and r3157, hiding a legit errno in make check

* Tue Sep 02 2008 Ingvar Hagelund <ingvar@linpro.no> - 2.0-0.6.beta1
- Added a commented option for max coresize in the sysconfig script
- Added a comment in README.redhat about upgrading from 1.x to 2.0

* Fri Aug 29 2008 Ingvar Hagelund <ingvar@linpro.no> - 2.0-0.5.beta1
- Bumped version numbers and source url for first beta release \o/
- Added a missing directory to the libs-devel package (Michael Schwendt)
- Added the LICENSE file to the libs-devel package
- Moved make check to its proper place
- Removed superfluous definition of lockfile in initscripts

* Wed Aug 27 2008 Ingvar Hagelund <ingvar@linpro.no> - 2.0-0.4.20080827svn3136
- Fixed up init script for varnishlog too

* Mon Aug 25 2008 Ingvar Hagelund <ingvar@linpro.no> - 2.0-0.3.20080825svn3125
- Fixing up init script according to newer Fedora standards
- The build now runs the test suite after compiling
- Requires initscripts
- Change default.vcl from nothing but comments to point to localhost:80,

* Mon Aug 18 2008 Ingvar Hagelund <ingvar@linpro.no> - 2.0-0.2.tp2
- Changed source, version and release to match 2.0-tp2

* Thu Aug 14 2008 Ingvar Hagelund <ingvar@linpro.no> - 2.0-0.1.20080814svn
- default.vcl has moved
- Added groff to build requirements

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.1.2-6
- Autorebuild for GCC 4.3

* Sat Dec 29 2007 Ingvar Hagelund <ingvar@linpro.no> - 1.1.2-5
- Added missing configuration examples
- Corrected the license to "BSD"

* Fri Dec 28 2007 Ingvar Hagelund <ingvar@linpro.no> - 1.1.2-4
- Build for fedora update

* Fri Dec 28 2007 Ingvar Hagelund <ingvar@linpro.no> - 1.1.2-2
- Added missing changelog items

* Thu Dec 20 2007 Stig Sandbeck Mathisen <ssm@linpro.no> - 1.1.2-1
- Bumped the version number to 1.1.2.
- Addeed build dependency on libxslt

* Fri Sep 07 2007 Ingvar Hagelund <ingvar@linpro.no> - 1.1.1-3
- Added a patch, changeset 1913 from svn trunk. This makes varnish
  more stable under specific loads. 

* Thu Sep 06 2007 Ingvar Hagelund <ingvar@linpro.no> - 1.1.1-2
- Removed autogen call (only diff from relase tarball)

* Mon Aug 20 2007 Ingvar Hagelund <ingvar@linpro.no> - 1.1.1-1
- Bumped the version number to 1.1.1.

* Tue Aug 14 2007 Ingvar Hagelund <ingvar@linpro.no> - 1.1.svn
- Update for 1.1 branch
- Added the devel package for the header files and static library files
- Added a varnish user, and fixed the init script accordingly

* Thu Jul 05 2007 Dag-Erling Smørgrav <des@des.no> - 1.1-1
- Bump Version and Release for 1.1

* Mon May 28 2007 Ingvar Hagelund <ingvar@linpro.no> - 1.0.4-3
- Fixed initrc-script bug only visible on el4 (fixes #107)

* Sun May 20 2007 Ingvar Hagelund <ingvar@linpro.no> - 1.0.4-2
- Repack from unchanged 1.0.4 tarball
- Final review request and CVS request for Fedora Extras
- Repack with extra obsoletes for upgrading from older sf.net package

* Fri May 18 2007 Dag-Erling Smørgrav <des@des.no> - 1.0.4-1
- Bump Version and Release for 1.0.4

* Wed May 16 2007 Ingvar Hagelund <ingvar@linpro.no> - 1.0.svn-20070517
- Wrapping up for 1.0.4
- Changes in sysconfig and init scripts. Syncing with files in
  trunk/debian

* Fri May 11 2007 Ingvar Hagelund <ingvar@linpro.no> - 1.0.svn-20070511
- Threw latest changes into svn trunk
- Removed the conversion of manpages into utf8. They are all utf8 in trunk

* Wed May 09 2007 Ingvar Hagelund <ingvar@linpro.no> - 1.0.3-7
- Simplified the references to the subpackage names
- Added init and logrotate scripts for varnishlog

* Mon Apr 23 2007 Ingvar Hagelund <ingvar@linpro.no> - 1.0.3-6
- Removed unnecessary macro lib_name
- Fixed inconsistently use of brackets in macros
- Added a condrestart to the initscript
- All manfiles included, not just the compressed ones
- Removed explicit requirement for ncurses. rpmbuild figures out the 
  correct deps by itself.
- Added ulimit value to initskript and sysconfig file
- Many thanks to Matthias Saou for valuable input

* Mon Apr 16 2007 Ingvar Hagelund <ingvar@linpro.no> - 1.0.3-5
- Added the dist tag
- Exchanged  RPM_BUILD_ROOT variable for buildroot macro
- Removed stripping of binaries to create a meaningful debug package
- Removed BuildRoot and URL from subpackages, they are picked from the
  main package
- Removed duplication of documentation files in the subpackages
- 'chkconfig --list' removed from post script
- Package now includes _sysconfdir/varnish/
- Trimmed package information
- Removed static libs and .so-symlinks. They can be added to a -devel package
  later if anybody misses them

* Wed Feb 28 2007 Ingvar Hagelund <ingvar@linpro.no> - 1.0.3-4
- More small specfile fixes for Fedora Extras Package
  Review Request, see bugzilla ticket 230275
- Removed rpath (only visible on x86_64 and probably ppc64)

* Tue Feb 27 2007 Ingvar Hagelund <ingvar@linpro.no> - 1.0.3-3
- Made post-1.0.3 changes into a patch to the upstream tarball
- First Fedora Extras Package Review Request

* Fri Feb 23 2007 Ingvar Hagelund <ingvar@linpro.no> - 1.0.3-2
- A few other small changes to make rpmlint happy

* Thu Feb 22 2007 Ingvar Hagelund <ingvar@linpro.no> - 1.0.3-1
- New release 1.0.3. See the general ChangeLog
- Splitted the package into varnish, libvarnish1 and
  libvarnish1-devel

* Thu Oct 19 2006 Ingvar Hagelund <ingvar@linpro.no> - 1.0.2-7
- Added a Vendor tag

* Thu Oct 19 2006 Ingvar Hagelund <ingvar@linpro.no> - 1.0.2-6
- Added redhat subdir to svn
- Removed default vcl config file. Used the new upstream variant instead.
- Based build on svn. Running autogen.sh as start of build. Also added
  libtool, autoconf and automake to BuildRequires.
- Removed rule to move varnishd to sbin. This is now fixed in upstream
- Changed the sysconfig script to include a lot more nice features.
  Most of these were ripped from the Debian package. Updated initscript
  to reflect this.

* Tue Oct 10 2006 Ingvar Hagelund <ingvar@linpro.no> - 1.0.1-3
- Moved Red Hat specific files to its own subdirectory

* Tue Sep 26 2006 Ingvar Hagelund <ingvar@linpro.no> - 1.0.1-2
- Added gcc requirement.
- Changed to an even simpler example vcl in to /etc/varnish (thanks, perbu)
- Added a sysconfig entry

* Fri Sep 22 2006 Ingvar Hagelund <ingvar@linpro.no> - 1.0.1-1
- Initial build.
