%bcond_with po4a

Summary:        Gives a fake root environment
Name:           fakeroot
Version:        1.32.1
Release:        1%{?dist}
# setenv.c: LGPLv2+
# contrib/Fakeroot-Stat-1.8.8: Perl (GPL+ or Artistic)
# the rest: GPLv3+
License:        GPLv3+ AND LGPLv2+ AND (GPL+ OR Artistic)
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://tracker.debian.org/pkg/fakeroot
Source0:        https://cdn-aws.deb.debian.org/debian/pool/main/f/fakeroot/%{name}_%{version}.orig.tar.gz
# Debian package patches, from debian.tar.xz
Patch2:         debian_fix-shell-in-fakeroot.patch
# Address some POSIX-types related problems.
Patch4:         fakeroot-inttypes.patch
# Fix LD_LIBRARY_PATH for multilib: https://bugzilla.redhat.com/show_bug.cgi?id=1241527
Patch5:         fakeroot-multilib.patch
Patch7:         relax_tartest.patch
#Patch8:         also-wrap-stat-library-call.patch
#Patch10:        po4a.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
# https://bugzilla.redhat.com/show_bug.cgi?id=887001
BuildRequires:  libacl-devel
BuildRequires:  libcap-devel
BuildRequires:  libtool
BuildRequires:  make

%if %{with po4a}
BuildRequires:  po4a
%endif

%if %{with_check}
# uudecode used by tests/tartest
BuildRequires:  sharutils
%endif

Requires:       %{_bindir}/getopt
Requires:       fakeroot-libs = %{version}-%{release}
Requires(post): %{_bindir}/readlink
Requires(post): %{_sbindir}/alternatives
Requires(preun): %{_sbindir}/alternatives

%description
fakeroot runs a command in an environment wherein it appears to have
root privileges for file manipulation. fakeroot works by replacing the
file manipulation library functions (chmod(2), stat(2) etc.) by ones
that simulate the effect the real library functions would have had,
had the user really been root.

%package libs
Summary:        Gives a fake root environment (libraries)

%description libs
This package contains the libraries required by %{name}.

%prep
%autosetup -p1

%build
%if !%{with po4a}
  # Disabling docs generation.
  sed -i "s/SUBDIRS=doc /SUBDIRS=/" Makefile.am
  sed -i "/doc\/.*Makefile/d" configure.ac
%endif

./bootstrap

%if %{with po4a}
  pushd doc
  po4a -k 0 --rm-backups --variable "srcdir=../doc/" po4a/po4a.cfg
  popd

  for file in ./doc/{*.1,*/*.1}; do
    iconv -f latin1 -t utf8 < $file > $file.new && \
    mv -f $file.new $file
  done
%endif

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
  rm -f %{buildroot}%{_libdir}/libfakeroot/libfakeroot.a
  rm -f %{buildroot}%{_libdir}/libfakeroot/libfakeroot.so
  rm -f %{buildroot}%{_libdir}/libfakeroot/libfakeroot.*la
%if %{with po4a}
  %find_lang faked-$type --without-mo --with-man
  %find_lang fakeroot-$type --without-mo --with-man
%endif
done

%if %{with po4a}
  rm %{buildroot}%{_mandir}{,/*}/man1/fake{d,root}-sysv.1
  rename -- -tcp '' %{buildroot}%{_mandir}{,/*}/man1/fake{d,root}-tcp.1
  sed -e 's/-tcp//g' fake{d,root}-tcp.lang > fakeroot.lang
%endif

%check
for type in sysv tcp; do
  make -C obj-$type check VERBOSE=1
done

%post
link=$(readlink -e "%{_bindir}/fakeroot")
if [ "$link" = "%{_bindir}/fakeroot" ]; then
  rm -f %{_bindir}/fakeroot
fi
link=$(readlink -e "%{_bindir}/faked")
if [ "$link" = "%{_bindir}/faked" ]; then
  rm -f "%{_bindir}/faked"
fi
link=$(readlink -e "%{_libdir}/libfakeroot/libfakeroot-0.so")
if [ "$link" = "%{_libdir}/libfakeroot/libfakeroot-0.so" ]; then
  rm -f "%{_libdir}/libfakeroot/libfakeroot-0.so"
fi

%{_sbindir}/alternatives --install "%{_bindir}/fakeroot" fakeroot \
  "%{_bindir}/fakeroot-tcp" 50 \
  --slave %{_bindir}/faked faked %{_bindir}/faked-tcp \
  --slave %{_libdir}/libfakeroot/libfakeroot-0.so libfakeroot.so %{_libdir}/libfakeroot/libfakeroot-tcp.so \

%{_sbindir}/alternatives --install "%{_bindir}/fakeroot" fakeroot \
  "%{_bindir}/fakeroot-sysv" 40 \
  --slave %{_bindir}/faked faked %{_bindir}/faked-sysv \
  --slave %{_libdir}/libfakeroot/libfakeroot-0.so libfakeroot.so %{_libdir}/libfakeroot/libfakeroot-sysv.so \

%preun
if [ $1 = 0 ]; then
  %{_sbindir}/alternatives --remove fakeroot "%{_bindir}/fakeroot-tcp"
  %{_sbindir}/alternatives --remove fakeroot "%{_bindir}/fakeroot-sysv"
fi

%if %{with po4a}
%files -f %{name}.lang
%else
%files
%endif
%defattr(-,root,root,-)
%doc COPYING AUTHORS BUGS DEBUG doc/README.saving
%{_bindir}/faked-*
%ghost %{_bindir}/faked
%{_bindir}/fakeroot-*
%ghost %{_bindir}/fakeroot

%if %{with po4a}
%{_mandir}/man1/faked.1*
%{_mandir}/man1/fakeroot.1*
%endif

%files libs
%dir %{_libdir}/libfakeroot
%{_libdir}/libfakeroot/libfakeroot-sysv.so
%{_libdir}/libfakeroot/libfakeroot-tcp.so
%ghost %{_libdir}/libfakeroot/libfakeroot-0.so

%changelog
* Mon Jun 27 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.29-1
- Updating to 1.29 to fix a test.

* Fri Mar 18 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.28-1
- Updating to version 1.28 using Fedora 36 spec (license: MIT) for guidance.
- Switching to using upstream fix for tartest.

* Mon Mar 14 2022 Muhammad Falak <mwani@microsoft.com> - 1.25.3-2
- Update `relax_tartest.patch` to enable ptest

* Thu Dec 02 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.25.3-1
- Update to version 1.25.3.
- Apply fix to build with 'glibc' 2.33+.
- Disabled generation and translation of docs to remove BR on "po4a".
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.25.2-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Mon Oct 05 2020 Dominik Mierzejewski <rpm@greysector.net> - 1.25.2-1
- update to 1.25.2 (#1881277)
- drop obsolete patch

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
