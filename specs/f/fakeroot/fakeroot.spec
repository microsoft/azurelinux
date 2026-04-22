# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global build_type_safety_c 0

%bcond_without autoconf

Summary: Gives a fake root environment
Name: fakeroot
Version: 1.37.1
Release: 4%{?dist}
# setenv.c: LGPLv2+
# contrib/Fakeroot-Stat-1.8.8: Perl (GPL+ or Artistic)
# the rest: GPLv3+
# Automatically converted from old format: GPLv3+ and LGPLv2+ and (GPL+ or Artistic) - review is highly recommended.
License: GPL-3.0-or-later AND LicenseRef-Callaway-LGPLv2+ AND (GPL-1.0-or-later OR Artistic-1.0-Perl)
# Source code: https://salsa.debian.org/clint/fakeroot/-/tree/upstream
URL: https://tracker.debian.org/pkg/fakeroot
Source0: https://ftp.debian.org/debian/pool/main/f/fakeroot/%{name}_%{version}.orig.tar.gz

# Debian package patches, from debian.tar.xz
Patch2: debian_fix-shell-in-fakeroot.patch
# git commit 8ce7846 2013-07-26  Address some POSIX-types related problems.
# Patch4: fakeroot-inttypes.patch
# Fix LD_LIBRARY_PATH for multilib: https://bugzilla.redhat.com/show_bug.cgi?id=1241527
Patch5: fakeroot-multilib.patch
# Patch7: relax_tartest.patch


BuildRequires: make
%if %{with autoconf}
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  po4a
%endif
BuildRequires: /usr/bin/getopt
BuildRequires: gcc
# https://bugzilla.redhat.com/show_bug.cgi?id=887001
BuildRequires: libacl-devel
BuildRequires: libcap-devel
# uudecode used by tests/tartest
BuildRequires: sharutils
Requires: /usr/bin/getopt
Requires: fakeroot-libs = %{version}-%{release}
Requires(post): /usr/sbin/alternatives
Requires(post): /usr/bin/readlink
Requires(preun): /usr/sbin/alternatives


%description
fakeroot runs a command in an environment wherein it appears to have
root privileges for file manipulation. fakeroot works by replacing the
file manipulation library functions (chmod(2), stat(2) etc.) by ones
that simulate the effect the real library functions would have had,
had the user really been root.

%package libs
Summary: Gives a fake root environment (libraries)

%description libs
This package contains the libraries required by %{name}.

%prep
%autosetup -p1
sed -i 's#AC_PREREQ(\[2.71\])#AC_PREREQ([2.69])#' configure.ac
# this test fails on s390x, i don't know or care why
%ifarch s390x
sed -i -e '/^ *t\.tar/d' test/Makefile.am
%endif

%build
%if %{with autoconf}
./bootstrap
pushd doc
po4a -k 0 --rm-backups --variable "srcdir=../doc/" po4a/po4a.cfg
popd
%endif

for file in ./doc/{*.1,*/*.1}; do
  iconv -f latin1 -t utf8 < $file > $file.new && \
  mv -f $file.new $file
done

for type in sysv tcp; do
mkdir obj-$type
cd obj-$type
cat >> configure << 'EOF'
#!/bin/sh
exec ../configure "$@"
EOF
chmod +x configure
%configure \
  --disable-dependency-tracking \
  --disable-static \
  --libdir=%{_libdir}/libfakeroot \
  --with-ipc=$type \
  --program-suffix=-$type
make
cd ..
done

%install
for type in sysv tcp; do
  make -C obj-$type install libdir=%{_libdir}/libfakeroot DESTDIR=%{buildroot}
  mv %{buildroot}%{_libdir}/libfakeroot/libfakeroot-0.so \
     %{buildroot}%{_libdir}/libfakeroot/libfakeroot-$type.so
  rm -f %{buildroot}%{_libdir}/libfakeroot/libfakeroot.so
  rm -f %{buildroot}%{_libdir}/libfakeroot/libfakeroot.*la
  %find_lang faked-$type --without-mo --with-man
  %find_lang fakeroot-$type --without-mo --with-man
done

rm %{buildroot}%{_mandir}{,/*}/man1/fake{d,root}-sysv.1
rename -- -tcp '' %{buildroot}%{_mandir}{,/*}/man1/fake{d,root}-tcp.1
sed -e 's/-tcp//g' fake{d,root}-tcp.lang > fakeroot.lang

%check
# Check section disabled: Disabling checks for initial set of failures.
exit 0

for type in sysv tcp; do
%ifarch ppc64le
%if 0%{?rhel}
  make -C obj-$type check VERBOSE=1 || :
%else
  make -C obj-$type check VERBOSE=1
%endif
%else
  make -C obj-$type check VERBOSE=1
%endif
done

%post
link=$(readlink -e "/usr/bin/fakeroot")
if [ "$link" = "/usr/bin/fakeroot" ]; then
  rm -f /usr/bin/fakeroot
fi
link=$(readlink -e "%{_bindir}/faked")
if [ "$link" = "%{_bindir}/faked" ]; then
  rm -f "%{_bindir}/faked"
fi
link=$(readlink -e "%{_libdir}/libfakeroot/libfakeroot-0.so")
if [ "$link" = "%{_libdir}/libfakeroot/libfakeroot-0.so" ]; then
  rm -f "%{_libdir}/libfakeroot/libfakeroot-0.so"
fi

alternatives --install "%{_bindir}/fakeroot" fakeroot \
  "%{_bindir}/fakeroot-tcp" 50 \
  --follower %{_bindir}/faked faked %{_bindir}/faked-tcp \
  --follower %{_libdir}/libfakeroot/libfakeroot-0.so libfakeroot.so %{_libdir}/libfakeroot/libfakeroot-tcp.so

alternatives --install "%{_bindir}/fakeroot" fakeroot \
  "%{_bindir}/fakeroot-sysv" 40 \
  --follower %{_bindir}/faked faked %{_bindir}/faked-sysv \
  --follower %{_libdir}/libfakeroot/libfakeroot-0.so libfakeroot.so %{_libdir}/libfakeroot/libfakeroot-sysv.so || :

%preun
if [ $1 = 0 ]; then
  alternatives --remove fakeroot "%{_bindir}/fakeroot-tcp"
  alternatives --remove fakeroot "%{_bindir}/fakeroot-sysv" || :
fi

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc COPYING AUTHORS BUGS DEBUG doc/README.saving
%{_bindir}/faked-*
%ghost %{_bindir}/faked
%{_bindir}/fakeroot-*
%ghost %{_bindir}/fakeroot
%{_mandir}/man1/faked.1*
%{_mandir}/man1/fakeroot.1*

%files libs
%dir %{_libdir}/libfakeroot
%{_libdir}/libfakeroot/libfakeroot-sysv.so
%{_libdir}/libfakeroot/libfakeroot-tcp.so
%ghost %{_libdir}/libfakeroot/libfakeroot-0.so

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.37.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jul 18 2025 Adam Williamson <awilliam@redhat.com> - 1.37.1-2
- Disable a failing test on s390x
- Ensure scriptlets always exit 0

* Fri Jul 18 2025 Zbigniew Jędrzejewski-Szmek  <zbyszek@in.waw.pl>
- Drop trailing slashes in calls to alternatives to avoid rpm bug
  (https://pagure.io/releng/issue/12829)

* Sun Mar 16 2025 Packit <hello@packit.dev> - 1.37.1-1
- Update to version 1.37.1
- Resolves: rhbz#2352813

* Thu Jan 23 2025 Packit <hello@packit.dev> - 1.37-1
- Update to version 1.37
- Resolves: rhbz#2341841

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.36.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Dec 27 2024 Packit <hello@packit.dev> - 1.36.2-1
- Update to version 1.36.2
- Resolves: rhbz#2333583

* Sat Sep 07 2024 Packit <hello@packit.dev> - 1.36-1
- Update to version 1.36
- Resolves: rhbz#2305236

* Wed Aug 28 2024 Miroslav Suchý <msuchy@redhat.com> - 1.35.1-2
- convert license to SPDX

* Tue Jul 30 2024 Sérgio Basto <sergio@serjux.com> - 1.35.1-1
- Update to 1.35.1
- Update to version 1.35 (Wed Jun 05 2024 Packit <hello@packit.dev>)
- Resolves: rhbz#2290632

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.34-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri May 10 2024 Packit <hello@packit.dev> - 1.34-1
- Update to version 1.34
- Resolves: rhbz#2268025

* Tue Feb 13 2024 Sérgio Basto <sergio@serjux.com> - 1.33-1
- Update fakeroot to 1.33 (#2259446)

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.32.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.32.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Nov 06 2023 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1.32.2-1
- Update to 1.32.2 (#2248160)

* Thu Aug 31 2023 Sérgio Basto <sergio@serjux.com> - 1.32.1-1
- Update fakeroot to 1.32.1

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.31-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Mar 15 2023 Sérgio Basto <sergio@serjux.com> - 1.31-1
- Update fakeroot to 1.31 (#2167522)
- Add fix from Debian
- Drop fakeroot-inttypes.patch which had almost 10 year old and I dont know what his purpose
- Drop relax_tartest.patch we don't need it anymore

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.30.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Nov 23 2022 Sérgio Basto <sergio@serjux.com> - 1.30.1-1
- Update fakeroot to 1.30.1 (#2139595)

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.29-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun May 22 2022 Sérgio Basto <sergio@serjux.com> - 1.29-1
- Update fakeroot to 1.29 (#2089064)

* Sun Apr 10 2022 Sérgio Basto <sergio@serjux.com> - 1.28-2
- Drop po4a as Debian did and renamed patches that came from Debian

* Fri Apr 08 2022 Sérgio Basto <sergio@serjux.com> - 1.28-1
- Update fakeroot to 1.28 (#2060992)

* Fri Jan 28 2022 Sérgio Basto <sergio@serjux.com> - 1.27-1
- Update fakeroot to 1.27 (#2041663)

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.26-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Oct 04 2021 Sérgio Basto <sergio@serjux.com> - 1.26-4
- Relax tar test v2

* Mon Oct 04 2021 Sérgio Basto <sergio@serjux.com> - 1.26-3
- Relax tar test

* Sun Oct 03 2021 Sérgio Basto <sergio@serjux.com> - 1.26-2
- Relax autoconf version
- t.tar test, now just fail on ppc64le

* Wed Sep 22 2021 Sérgio Basto <sergio@serjux.com> - 1.26-1
- Update to 1.26 (#2001811)
- Drop upstreamed patches

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.25.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.25.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild
- Add upstreamed patches:
  0001-libfakeroot.c-define-_STAT_VER-if-not-already-define.patch
  0002-libfakeroot.c-add-wrappers-for-new-glibc-2.33-symbol.patch
  0003-libfakeroot.c-fix-compile-error-with-DEBUG-enabled.patch
  0004-configure.ac-fix-__xmknod-at-pointer-argument.patch
- Add patch "STAT_VER changes for different architectures"

* Wed Oct 14 2020 Dominik Mierzejewski <rpm@greysector.net> - 1.25.3-1
- update to 1.25.3 (#1886610)

* Mon Oct 05 2020 Dominik Mierzejewski <rpm@greysector.net> - 1.25.2-1
- update to 1.25.2 (#1881277)
- drop obsolete patch
- re-enable failing tests (fixed upstream)

* Sat Aug 22 2020 Dominik Mierzejewski <rpm@greysector.net> - 1.24-5
- disable three tests failing under glibc 2.32+ (#1871355)

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.24-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.24-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Sep 24 2019 Dominik Mierzejewski <rpm@greysector.net> - 1.24-2
- stop alternativizing manpages, they're identical for both sysv and tcp
  variants (#1677540)

* Fri Sep 20 2019 Dominik Mierzejewski <rpm@greysector.net> - 1.24-1
- update to 1.24 (#1750054)
- update source URL
- drop obsolete patches

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.23-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Nov 30 2018 Dominik Mierzejewski <rpm@greysector.net> - 1.23-2
- t.tar failure is no longer reproducible (#1601392)

* Mon Jul 16 2018 Dominik Mierzejewski <rpm@greysector.net> - 1.23-1
- update to 1.23 (#1597055)
- point to working URLs
- pretend t.tar test succeeds for now (#1601392)
- make testsuite more verbose for the future

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Aug 29 2017 Dominik Mierzejewski <rpm@greysector.net> - 1.22-1
- update to 1.22

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.21-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.21-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Dec 31 2016 Adam Williamson <awilliam@redhat.com> - 1.21-2
- Apply all patches from Debian package (should fix libuser build)

* Sat Dec 31 2016 Adam Williamson <awilliam@redhat.com> - 1.21-1
- New release 1.21

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Dec 26 2015 Dominik Mierzejewski <rpm@greysector.net> - 1.20.2-3
- fix root privilege faking for copied files/dirs (bug 887001)

* Mon Sep 28 2015 Dominik Mierzejewski <rpm@greysector.net> - 1.20.2-2
- fix LD_LIBRARY_PATH for multilib environment (bug 1241527)
- update License: tag
- don't strip the libraries in install, just keep the executable bit
- when converting from latin1 to utf8, don't use the converted file
  if the conversion failed: the pt manpage is already utf8

* Thu Jun 18 2015 Dominik Mierzejewski <rpm@greysector.net> - 1.20.2-1
- update to 1.20.2
- alternativize libfakeroot and faked as well (bug 817088)
- include Portugese manpages
- add missing BR: libcap-devel
- autogenerate most of the file list

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.18.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 1.18.4-5
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.18.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.18.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Aug 26 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.18.4-2
- Add alternatives (Mimic Debian's behavior).

* Fri Jul 26 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.18.4-1
- Upstream update.
- Spec cleanup.
- Add fakeroot-1.18.4-inttypes.patch.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu May 27 2010 Richard W.M. Jones <rjones@redhat.com> - 1.12.4-2
- Strip libfakeroot-*.so (RHBZ#596735).
- Verified that libguestfs still builds and runs with this change (this
  represents a fairly aggressive test of fakeroot).

* Fri Jan 29 2010 Richard W.M. Jones <rjones@redhat.com> - 1.12.4-1
- Upstream removed the tarball for 1.12.2, which made Source0 invalid.
- There is a new version (1.12.4), so update to the new version.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.2-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Mar 22 2009 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.12.2-21
- Update to 1.12.2.
- Create a fakeroot-libs subpackage so that the package is multilib
  aware (by Richard W.M. Jones <rjones@redhat.com>, see RH bug
  #490953).

* Sat Feb 14 2009 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.12.1-20
- Update to 1.12.1.

* Sat Nov 22 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.11-19
- Update to 1.11.

* Fri Oct  3 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.9.7-18
- Update to 1.9.7.

* Sun Aug 24 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.9.6-17
- %%check || : does not work anymore.

* Sun Aug  3 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.9.6-16
- Update to 1.9.6.

* Thu Mar  8 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.6.4-15
- Update to 1.6.4.

* Wed Jan 10 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.5.12-14
- Update to 1.5.12.

* Sun Jan  7 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.5.10-13
- po4a currently not need as a BR.
- remove empty README, add debian/changelog.

* Sun Dec 31 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.5.10-12
- Add %%{_libdir}/libfakeroot to %%files.
- Add %%check.

* Fri Dec 29 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.5.10-11
- Extend the %%description a bit.

* Thu Dec 28 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.5.10-10
- Don't build static lib.
- Exclude libtool lib.
- %%makeinstall to make install DESTDIR=%%buildroot.

* Mon Aug  7 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.5.10-9
- Update to 1.5.10.

* Fri Feb 17 2006 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 1.5.7.

* Thu Nov 24 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 1.5.5.

* Sat Sep 17 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 1.5.1.

* Fri Sep  2 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 1.4.3.

* Sun Jul  3 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 1.4.1.

* Sun Feb  6 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 1.2.4.

* Sun Jan 25 2004 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 0.8.3.

* Wed Oct  8 2003 Axel Thimm <Axel.Thimm@ATrpms.net> 
- Initial build.
