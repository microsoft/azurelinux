Vendor:         Microsoft Corporation
Distribution:   Mariner
%global _hardened_build 1

# https://github.com/varnishcache/varnish-cache/issues/2269
%global debug_package %{nil}

%if 0%{?rhel} == 6 || 0%{?rhel} == 7
%global _use_internal_dependency_generator 0
%global __find_provides %{_builddir}/%{name}-%{version}/find-provides %__find_provides
%global __python /usr/bin/python3.4
%else
%global __python %{__python3}
%endif

%global __provides_exclude_from ^%{_libdir}/varnish/vmods

%global abi 13f137934ec1cf14af66baf7896311115ee35598
%global vrt 11.0

# Package scripts are now external
# https://github.com/varnishcache/pkg-varnish-cache
%global commit1 ec7ad9e6c6dd7c9b4f4ba60c5b223376908c3ca6
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})

Summary: High-performance HTTP accelerator
Name: varnish
Version: 6.4.0
Release: 6%{?dist}
License: BSD
URL: https://www.varnish-cache.org/
Source0: http://varnish-cache.org/_downloads/%{name}-%{version}%{?vd_rc}.tgz
Source1: https://github.com/varnishcache/pkg-varnish-cache/archive/%{commit1}.tar.gz#/pkg-varnish-cache-%{shortcommit1}.tar.gz

# Patches:
# Patch  001: Because of Fedora's libtool no-rpath requirement, it is still
#             necessary to add LD_LIBRARY_PATH when building the documentation
#             (Fixed by using LT_SYS_LIBRARY_PATH)
#Patch1:  varnish-6.1.1_fix_ld_library_path_in_doc_build.patch

# Patch  004: varnish selinux support for el6
Patch4:  varnish-4.0.3_fix_varnish4_selinux.el6.patch

# Patch  009: Hard code older python support in configure for older el releases
#Patch9:  varnish-5.1.1.fix_python_version.patch

# Patch  012: Fix test for variants of ncurses, based on upstream commit 9bdc5f75, upstream issue #2668
#Patch12: varnish-6.0.1_fix_bug2668.patch

# Patch  013: Just a simple format error
#Patch13: varnish-6.1.0_fix_testu00008.patch

# Patch  014: Another formatting error fixed upstream, issue 2879
#Patch14: varnish-6.1.1_fix_upstrbug_2879.patch

# Patch  015: pcre-jit fixed upstream, issue #2912
#Patch15: varnish-6.1.1_fix_issue_2912.patch

# Patch  016: Fix some warnings that prohibited clean -Werror compilation
#             on el6. Will not be fixed upstream. Patch grows more stupid
#             for each iteration :-(
Patch16: varnish-6.4.0_el6_fix_warning_from_old_gcc.patch

# Patch  017: Fix stack size on ppc64 in test c_00057, upstream commit 88948d9
#Patch17: varnish-6.2.0_fix_ppc64_for_test_c00057.patch

# Patch 018: gcc-10.0.1/s390x compilation fix, upstream commit b0af060
#Patch18: varnish-6.3.2_fix_s390x.patch


Provides: varnish%{_isa} = %{version}-%{release}
Provides: varnishd(abi)%{_isa} = %{abi}
Provides: varnishd(vrt)%{_isa} = %{vrt}

Provides: vmod(blob)%{_isa} = %{version}-%{release}
Provides: vmod(directors)%{_isa} = %{version}-%{release}
Provides: vmod(proxy)%{_isa} = %{version}-%{release}
Provides: vmod(purge)%{_isa} = %{version}-%{release}
Provides: vmod(std)%{_isa} = %{version}-%{release}
Provides: vmod(unix)%{_isa} = %{version}-%{release}
Provides: vmod(vtc)%{_isa} = %{version}-%{release}


Obsoletes: varnish-libs < %{version}-%{release}

%if 0%{?rhel} == 6 || 0%{?rhel} == 7
BuildRequires: python34 python-sphinx python34-docutils
%else
BuildRequires: python3, python3-sphinx, python3-docutils
%endif
BuildRequires: jemalloc-devel
BuildRequires: libedit-devel
BuildRequires: ncurses-devel
BuildRequires: pcre-devel
BuildRequires: pkgconfig
BuildRequires: gcc
BuildRequires: make

# Extra requirements for the build suite
BuildRequires: nghttp2

# haproxy is broken in rawhide now
#if 0#{?fedora} || 0#{?rhel} >= 8
#BuildRequires: haproxy
#endif

%if 0%{?rhel} == 6
BuildRequires: selinux-policy
%endif
Requires: logrotate
Requires: ncurses
Requires: pcre
Requires: jemalloc
Requires: redhat-rpm-config
Requires(pre): shadow-utils
Requires(post): /usr/bin/uuidgen
# Varnish actually needs gcc installed to work. It uses the C compiler 
# at runtime to compile the VCL configuration files. This is by design.
Requires: gcc

Requires(post): systemd-units
Requires(post): systemd-sysv
Requires(preun): systemd-units
Requires(postun): systemd-units
BuildRequires: systemd-units


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

%description devel
Development files for %{name}
Varnish Cache is a high-performance HTTP accelerator
Requires: %{name} = %{version}-%{release}

%if 0%{?rhel} == 6
Requires: python34
%else
Requires: python3
%endif

%package docs
Summary: Documentation files for %name

%description docs
Documentation files for %name

%if 0%{?rhel} == 6
%package selinux
Summary: Minimal selinux policy for running varnish

%description selinux
Minimal selinux policy for running varnish4
%endif

%prep
%setup -q -n varnish-%{version}%{?vd_rc}
tar xzf %SOURCE1
ln -s pkg-varnish-cache-%{commit1}/redhat redhat
ln -s pkg-varnish-cache-%{commit1}/debian debian
cp redhat/find-provides .
%if 0%{?rhel} == 6
cp pkg-varnish-cache-%{commit1}/sysv/redhat/* redhat/
sed -i '8 i\RPM_BUILD_ROOT=%{buildroot}' find-provides
%endif

%if 0%{?rhel} == 6
%patch4 -p0
%patch16 -p1
%endif

%build
%if 0%{?rhel} == 6
export CFLAGS="%{optflags} -fPIC"
export LDFLAGS=" -pie"
%endif

# https://gcc.gnu.org/wiki/FAQ#PR323
%ifarch %ix86
export CFLAGS="%{optflags} -ffloat-store -fexcess-precision=standard"
%endif

%ifarch s390x
export CFLAGS="%{optflags} -Wno-error=free-nonheap-object"
%endif

# What gcc version is this?
gcc --version

# What is the page size
getconf PAGESIZE

# Man pages are prebuilt. No need to regenerate them.
export RST2MAN=/bin/true
export RST2HTML=/bin/true
# Explicit python, please
export PYTHON=%{__python}

%configure LT_SYS_LIBRARY_PATH=%_libdir \
 --disable-static \
%ifarch aarch64
%if 0%{?rhel} > 0
  --with-jemalloc=no \
%endif
%endif
%if 0%{?rhel} != 6
  --with-sphinx-build=sphinx-build-3.4 \
%endif
  --localstatedir=/var/lib  \
  --docdir=%{?_pkgdocdir}%{!?_pkgdocdir:%{_docdir}/%{name}-%{version}} \
#  --disable-pcre-jit \

make %{?_smp_mflags} V=1 

# One varnish user is enough
sed -i 's,User=varnishlog,User=varnish,g;' redhat/varnishncsa.service

# Clean up the html documentation
rm -rf doc/html/_sources

%check

# rhbz #1690796
%if 0%{?rhel} == 6
%ifarch ppc64 ppc64le aarch64
rm bin/varnishtest/tests/c00057.vtc
%endif
%endif

# Remove this for now. Hard to get the size and timing right
%ifarch s390 s390x
rm bin/varnishtest/tests/o00005.vtc
%endif

make %{?_smp_mflags} check VERBOSE=1


%install
rm -rf %{buildroot}

# mock el6 and el7 defaults to LANG=C, which makes python3 fail when parsing utf8 text
%if 0%{?rhel} == 6 || 0%{?rhel} == 7
export LANG=en_US.UTF-8
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

# systemd support

mkdir -p %{buildroot}%{_unitdir}
install -D -m 0644 redhat/varnish.service %{buildroot}%{_unitdir}/varnish.service
install -D -m 0644 redhat/varnishncsa.service %{buildroot}%{_unitdir}/varnishncsa.service


install -D -m 0755 redhat/varnishreload %{buildroot}%{_sbindir}/varnishreload

echo %{_libdir}/varnish > %{buildroot}%{_sysconfdir}/ld.so.conf.d/varnish-%{_arch}.conf

# No idea why these ends up with mode 600 in the debug package
chmod 644 lib/libvmod_*/*.c
chmod 644 lib/libvmod_*/*.h

# selinux module for el6
%if 0%{?rhel} == 6
cd selinux
make -f %{_datadir}/selinux/devel/Makefile
install -p -m 644 -D varnish4.pp %{buildroot}%{_datadir}/selinux/packages/%{name}/varnish4.pp
%endif

%files
%{_sbindir}/*
%{_bindir}/*
%{_libdir}/*.so.*
%{_libdir}/varnish
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
%config %{_sysconfdir}/ld.so.conf.d/varnish-%{_arch}.conf


# systemd from fedora 17 and rhel 7

%{_unitdir}/varnish.service
%{_unitdir}/varnishncsa.service


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

%if 0%{?rhel} == 6
%files selinux
%{_datadir}/selinux/packages/%{name}/varnish4.pp
%endif

%pre
getent group varnish >/dev/null || groupadd -r varnish
getent passwd varnish >/dev/null || \
       useradd -r -g varnish -d /var/lib/varnish -s /usr/sbin/nologin \
               -c "Varnish Cache" varnish
exit 0

%post

%systemd_post varnish varnishncsa

# Other distros: Use chkconfig





/sbin/ldconfig

# Previous versions had varnishlog and varnishncsa running as root
chown varnish:varnish /var/log/varnish/varnishncsa.log 2>/dev/null || true

test -f /etc/varnish/secret || (uuidgen > /etc/varnish/secret && chmod 0600 /etc/varnish/secret)

# selinux module for el6
%if 0%{?rhel} == 6
%post selinux
if [ "$1" -le "1" ] ; then # First install
semodule -i %{_datadir}/selinux/packages/%{name}/varnish4.pp 2>/dev/null || :
fi

%preun selinux
if [ "$1" -lt "1" ] ; then # Final removal
semodule -r varnish4 2>/dev/null || :
fi

%postun

%systemd_postun_with_restart varnish varnishncsa

/sbin/ldconfig


%postun selinux
if [ "$1" -ge "1" ] ; then # Upgrade
semodule -i %{_datadir}/selinux/packages/%{name}/varnish4.pp 2>/dev/null || :
fi

%endif

%preun
%systemd_preun varnish varnishncsa

%changelog
* Fri Jun 04 2021 Thomas Crain <thcrain@microsoft.com> - 6.4.0-6
- Provide dummy RST2HTML path in addition to the RST2MAN one already present.

* Fri Apr 30 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 6.4.0-5
- Initial CBL-Mariner import from Fedora 33 (license: MIT).
- Making binaries paths compatible with CBL-Mariner's paths.

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
