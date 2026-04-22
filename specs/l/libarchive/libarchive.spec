# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond_without check

Name:           libarchive
Version:        3.8.4
Release: 2%{?dist}
Summary:        A library for handling streaming archive formats

# Licenses:
# ./configure: FSFUL
# ./build/autoconf/lib-ld.m4: FSFULLR
# ./configure: FSFUL
# ./unzip/la_queue.h: BSD-3-Clause
# ./aclocal.m4: (FSFULLR and/or GPL-2) with Libtool-exception exception
License:        BSD-2-Clause AND FSFULLR AND GPL-2.0-or-later WITH Libtool-exception AND BSD-3-Clause AND FSFUL
URL:            https://www.libarchive.org/
Source0:        https://libarchive.org/downloads/%{name}-%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  bison
BuildRequires:  bzip2-devel
BuildRequires:  e2fsprogs-devel
BuildRequires:  gcc
BuildRequires:  libacl-devel
BuildRequires:  libattr-devel
BuildRequires:  libtool
BuildRequires:  libxml2-devel
BuildRequires:  libzstd-devel
BuildRequires:  lz4-devel
# According to libarchive maintainer, linking against liblzo violates
# LZO license.
# See https://github.com/libarchive/libarchive/releases/tag/v3.3.0
#BuildRequires:  lzo-devel
BuildRequires:  openssl-devel
BuildRequires:  xz-devel
BuildRequires:  zlib-devel
BuildRequires: make

# When configured against OpenSSL 1.1, the RIPEMD-160 support was not detected,
# so it was not compiled in previously. With OpenSSL 3.0, it's now detected as
# being available, but it only actually works when the legacy provider is
# loaded, which breaks the RIPEMD-160 test. This patch disables the RIPEMD-160
# support explicitly.
Patch0001: 0001-Drop-rmd160-from-OpenSSL.patch

%description
Libarchive is a programming library that can create and read several different
streaming archive formats, including most popular tar variants, several cpio
formats, and both BSD and GNU ar variants. It can also write shar archives and
read ISO9660 CDROM images and ZIP archives.


%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package -n bsdtar
Summary:        Manipulate tape archives
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n bsdtar
The bsdtar package contains standalone bsdtar utility split off regular
libarchive packages.


%package -n bsdcpio
Summary:        Copy files to and from archives
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n bsdcpio
The bsdcpio package contains standalone bsdcpio utility split off regular
libarchive packages.


%package -n bsdcat
Summary:        Expand files to standard output
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n bsdcat
The bsdcat program typically takes a filename as an argument or reads standard
input when used in a pipe.  In both cases decompressed data it written to
standard output.

%package -n bsdunzip
Summary:        Extract files from a ZIP archive
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n bsdunzip
The bsdunzip package contains standalone bsdunzip utility split off regular
libarchive packages. It is designed to provide an interface compatible with Info-ZIP's.


%prep
%autosetup -p1


%build
autoreconf -ifv
%configure --disable-static LT_SYS_LIBRARY_PATH=%_libdir
%make_build


%install
%make_install
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# rhbz#1294252
replace ()
{
    filename=$1
    file=`basename "$filename"`
    binary=${file%%.*}
    pattern=${binary##bsd}

    awk "
        # replace the topic
        /^.Dt ${pattern^^} 1/ {
            print \".Dt ${binary^^} 1\";
            next;
        }
        # replace the first occurence of \"$pattern\" by \"$binary\"
        !stop && /^.Nm $pattern/ {
            print \".Nm $binary\" ;
            stop = 1 ;
            next;
        }
        # print remaining lines
        1;
    " "$filename" > "$filename.new"
    mv "$filename".new "$filename"
}

for manpage in bsdtar.1 bsdcpio.1
do
    installed_manpage=`find "$RPM_BUILD_ROOT" -name "$manpage"`
    replace "$installed_manpage"
done


%check
%if %{with check}
logfiles ()
{
    find -name '*_test.log' -or -name test-suite.log
}

tempdirs ()
{
    cat `logfiles` \
        | awk "match(\$0, /[^[:space:]]*`date -I`[^[:space:]]*/) { print substr(\$0, RSTART, RLENGTH); }" \
        | sort | uniq
}

cat_logs ()
{
    for i in `logfiles`
    do
        echo "=== $i ==="
        cat "$i"
    done
}

run_testsuite ()
{
    rc=0
    %make_build check -j1 || {
        # error happened - try to extract in koji as much info as possible
        cat_logs

        for i in `tempdirs`; do
            if test -d "$i" ; then
                find $i -printf "%p\n    ~> a: %a\n    ~> c: %c\n    ~> t: %t\n    ~> %s B\n"
                cat $i/*.log
            fi
        done
        return 1
    }
    cat_logs
}

# On a ppc/ppc64 is some race condition causing 'make check' fail on ppc
# when both 32 and 64 builds are done in parallel on the same machine in
# koji.  Try to run once again if failed.
%ifarch ppc
run_testsuite || run_testsuite
%else
run_testsuite
%endif
%endif


%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc NEWS README.md
%{_libdir}/libarchive.so.13*
%{_mandir}/*/cpio.*
%{_mandir}/*/mtree.*
%{_mandir}/*/tar.*

%files devel
%{_includedir}/*.h
%{_mandir}/*/archive*
%{_mandir}/*/libarchive*
%{_libdir}/libarchive.so
%{_libdir}/pkgconfig/libarchive.pc

%files -n bsdtar
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc NEWS README.md
%{_bindir}/bsdtar
%{_mandir}/*/bsdtar*

%files -n bsdcpio
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc NEWS README.md
%{_bindir}/bsdcpio
%{_mandir}/*/bsdcpio*

%files -n bsdcat
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc NEWS README.md
%{_bindir}/bsdcat
%{_mandir}/*/bsdcat*

%files -n bsdunzip
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc NEWS README.md
%{_bindir}/bsdunzip
%{_mandir}/*/bsdunzip*


%changelog
* Fri Dec 05 2025 Packit <hello@packit.dev> - 3.8.4-1
- Update to version 3.8.4
- Resolves: rhbz#2419348

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jul 23 2025 Lukas Javorsky <ljavorsk@redhat.com> - 3.8.1-2
- Remove sharutils dependency, as it's not needed anymore

* Mon Jun 02 2025 Lukas Javorsky <ljavorsk@redhat.com> - 3.8.1-1
- Rebase to version 3.8.1

* Tue Mar 25 2025 Lukas Javorsky <ljavorsk@redhat.com> - 3.7.9-1
- Rebase to version 3.7.9

* Mon Mar 10 2025 Lukas Javorsky <ljavorsk@redhat.com> - 3.7.7-4
- Fix for CVE-2025-25724
- Fix for CVE-2025-1632

* Tue Feb 18 2025 Lukas Javorsky <ljavorsk@redhat.com> - 3.7.7-3
- Fix for CVE-2024-57970

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Nov 05 2024 Lukas Javorsky <ljavorsk@redhat.com> - 3.7.7-1
- Rebase to 3.7.7

* Tue Sep 24 2024 Lukas Javorsky <ljavorsk@redhat.com> - 3.7.6-1
- Rebase to 3.7.6

* Mon Sep 23 2024 Lukas Javorsky <ljavorsk@redhat.com> - 3.7.5-2
- Add Patch0002 to fix the failing tar test and the bug that it identified

* Mon Sep 16 2024 Lukas Javorsky <ljavorsk@redhat.com> - 3.7.5-1
- Rebase to version 3.7.5
- Patch 0002 upstreamed

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jun 06 2024 Lukas Javorsky <ljavorsk@redhat.com> - 3.7.4-2
- Fix CVE-2024-20696
- Resolves: rhbz#2290449

* Mon Apr 29 2024 Lukas Javorsky <ljavorsk@redhat.com> - 3.7.4-1
- Rebase to version 3.7.4

* Mon Apr 08 2024 Lukas Javorsky <ljavorsk@redhat.com> - 3.7.3-1
- Rebase to version 3.7.3

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Sep 12 2023 Lukas Javorsky <ljavorsk@redhat.com> - 3.7.2-1
- Rebase to version 3.7.2

* Mon Jul 31 2023 Lukas Javorsky <ljavorsk@redhat.com> - 3.7.1-1
- Rebase to version 3.7.1

* Tue Jul 25 2023 Lukas Javorsky <ljavorsk@redhat.com> - 3.7.0-1
- Rebase to version 3.7.0
- Add new bsdunzip subpackage

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Feb 08 2023 Davide Cavalca <dcavalca@fedoraproject.org> - 3.6.1-5
- Backport upstream PR#1772 for better pathname portability across OS
  Resolves: #2136961

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Dec 02 2022 Lukas Javorsky <ljavorsk@redhat.com> - 3.6.1-3
- Resolves: CVE-2022-36227

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Apr 08 2022 Lukas Javorsky <ljavorsk@redhat.com> - 3.6.1-1
- Rebase to version 3.6.1
- Resolves: #2071934

* Tue Feb 22 2022 Matej Mužila <mmuzila@redhat.com> - 3.6.0-1
- Rebase to version 3.6.0
- Resolves: #2051860

* Mon Feb 14 2022 Lukas Javorsky <ljavorsk@redhat.com> - 3.5.3-1
- Rebase to version 3.5.3

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Dec 03 2021 Stephen Gallagher <sgallagh@redhat.com> - 3.5.2-5
- Drop RIPEMD-160 support for OpenSSL 3.0

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 3.5.2-3
- Rebuilt with OpenSSL 3.0.0

* Mon Aug 30 2021 Ondrej Dubaj <odubaj@redhat.com> - 3.5.2-2
- Fixed symlink handling

* Mon Aug 23 2021 Ondrej Dubaj <odubaj@redhat.com> - 3.5.2-1
- Rebased to version 3.5.2

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 04 2021 Ondrej Dubaj <odubaj@redhat.com> - 3.5.1-1
- Rebased to version 3.5.1

* Wed Dec 02 2020 Ondrej Dubaj <odubaj@redhat.com> - 3.5.0-1
- Rebased to version 3.5.0

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 13 2020 Tom Stellard <tstellar@redhat.com> - 3.4.3-2
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Fri May 22 2020 Ondrej Dubaj <odubaj@redhat.com> - 3.4.3-1
- Rebased to version 3.4.3

* Wed Feb 12 2020 Ondrej Dubaj <odubaj@redhat.com> - 3.4.2-1
- Rebased to version 3.4.2

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Aug 30 2019 FeRD (Frank Dana) <ferdnyc@gmail.com> - 3.4.0-1
- New upstream release, adds RAR5 and ZIPX support (readonly)
- Drop upstreamed patches
- Add upstreamed patch to fix test failure with libzstd-1.4.2

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Mar 28 2019 Pavel Raiskup <praiskup@redhat.com> - 3.3.3-7
- simplify libtool hacks

* Tue Mar 19 2019 Ondrej Dubaj <odubaj@redhat.com> - 3.3.3-6
- applied various flaws (#1663893)

* Tue Mar 19 2019 Ondrej Dubaj <odubaj@redhat.com> - 3.3.3-5
- applied CVE patches (#1690071)

* Thu Mar 14 2019 Ondrej Dubaj <odubaj@redhat.com> - 3.3.3-4
- applied various flaws (#1672900)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Nov 26 2018 Pavel Raiskup <praiskup@redhat.com> - 3.3.3-2
- fix some covscan issues (rhbz#1602575)
- build-requires libzstd-devel (rhbz#1653046)

* Tue Oct 23 2018 Pavel Raiskup <praiskup@redhat.com> - 3.3.3-1
- the latest upstream release

* Wed Jul 18 2018 Pavel Raiskup <praiskup@redhat.com> - 3.3.2-3
- drop use of %%ldconfig_scriptlets

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Pavel Raiskup <praiskup@redhat.com> - 3.3.2-1
- rebase to latest upstream release

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.3.1-4
- Switch to %%ldconfig_scriptlets

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Apr 18 2017 Pavel Raiskup <praiskup@redhat.com> - 3.3.1-1
- the latest release, per release notes:
  https://groups.google.com/forum/#!topic/libarchive-discuss/jfc7lBfrvVg

* Mon Feb 20 2017 Pavel Raiskup <praiskup@redhat.com> - 3.2.2-3
- temporary work-around for FTBFS (rhbz#1423839)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Nov 11 2016 Pavel Raiskup <praiskup@redhat.com> - 3.2.2-2
- enable lz4 support, rhbz#1394038

* Tue Oct 25 2016 Pavel Raiskup <praiskup@redhat.com> - 3.2.2-1
- minor rebase to 3.2.2

* Tue Oct 11 2016 Tomáš Mráz <tmraz@redhat.com> - 3.2.1-5
- rebuild with OpenSSL 1.1.0

* Mon Sep 26 2016 Tomas Repik <trepik@redhat.com> - 3.2.1-4
- fix some stack and heap overflows
- resolves (rhbz#1378669, rhbz#1378668, rhbz#1378666)

* Mon Aug 08 2016 Tomas Repik <trepik@redhat.com> - 3.2.1-3
- bump release for upgradepath

* Mon Jul 18 2016 Pavel Raiskup <praiskup@redhat.com> - 3.2.1-2
- print more detailed logs for testsuite, even if testsuite succeeded

* Mon Jun 20 2016 Pavel Raiskup <praiskup@redhat.com> - 3.2.1-1
- rebase, several security issues fixed (rhbz#1348194)

* Mon May 16 2016 Pavel Raiskup <praiskup@redhat.com> - 3.2.0-3
- fix the manual pages for remaining issue (rhbz#1294252)

* Thu May 12 2016 Pavel Raiskup <praiskup@redhat.com> - 3.2.0-2
- fix manual pages to mention correctly spelled binary names (rhbz#1294252)

* Tue May 03 2016 Pavel Raiskup <praiskup@redhat.com> - 3.2.0-1
- new upstream release 3.2.0 (rhbz#1330345), per release notes:
  https://groups.google.com/d/msg/libarchive-discuss/qIzW7doKzxA/MVbUkjlNAAAJ

* Mon Mar 07 2016 Björn Esser <fedora@besser82.io> - 3.1.2-16
- removed %%defattr, BuildRoot and other ancient bits
- added arch'ed bits to all Requires

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.2-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Dec 21 2015 Pavel Raiskup <praiskup@redhat.com> - 3.1.2-14
- fix 'Out of memory when creating mtree files' error (rhbz#1284162)
- use %%autosetup macro

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 29 2015 Pavel Raiskup <praiskup@redhat.com> - 3.1.2-12
- fix libarchive segfault for intentionally broken cpio archives (rhbz#1216892)

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 3.1.2-11
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 17 2014 Tom Callaway <spot@fedoraproject.org> - 3.1.2-9
- fix license handling

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Aug 08 2013 Jaromir Koncicky <jkoncick@redhat.com> - 3.1.2-7
- Fixed Bug 993048 - added #ifdef ACL_TYPE_NFS4 to code which requires
  NFS4 ACL support

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 22 2013 Pavel Raiskup <praiskup@redhat.com> - 3.1.2-5
- try to workaround racy testsuite fail

* Sun Jun 30 2013 Pavel Raiskup <praiskup@redhat.com> - 3.1.2-4
- enable testsuite in the %%check phase

* Mon Jun 24 2013 Pavel Raiskup <praiskup@redhat.com> - 3.1.2-3
- bsdtar/bsdcpio should require versioned libarchive

* Wed Apr  3 2013 Tomas Bzatek <tbzatek@redhat.com> - 3.1.2-2
- Remove libunistring-devel build require

* Thu Mar 28 2013 Tomas Bzatek <tbzatek@redhat.com> - 3.1.2-1
- Update to 3.1.2
- Fix CVE-2013-0211: read buffer overflow on 64-bit systems (#927105)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 14 2013 Tomas Bzatek <tbzatek@redhat.com> - 3.1.1-1
- Update to 3.1.1
- NEWS seems to be valid UTF-8 nowadays

* Wed Oct 03 2012 Pavel Raiskup <praiskup@redhat.com> - 3.0.4-3
- better install manual pages for libarchive/bsdtar/bsdcpio (# ... )
- several fedora-review fixes ...:
- Source0 has moved to github.com
- remove trailing white spaces
- repair summary to better describe bsdtar/cpiotar utilities

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon May  7 2012 Tomas Bzatek <tbzatek@redhat.com> - 3.0.4-1
- Update to 3.0.4

* Wed Feb  1 2012 Tomas Bzatek <tbzatek@redhat.com> - 3.0.3-2
- Enable bsdtar and bsdcpio in separate subpackages (#786400)

* Fri Jan 13 2012 Tomas Bzatek <tbzatek@redhat.com> - 3.0.3-1
- Update to 3.0.3

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.0-0.3.a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 15 2011 Rex Dieter <rdieter@fedoraproject.org> 3.0.0-0.2.a
- track files/sonames closer, so abi bumps aren't a surprise
- tighten subpkg deps via %%_isa

* Mon Nov 14 2011 Tomas Bzatek <tbzatek@redhat.com> - 3.0.0-0.1.a
- Update to 3.0.0a (alpha release)

* Mon Sep  5 2011 Tomas Bzatek <tbzatek@redhat.com> - 2.8.5-1
- Update to 2.8.5

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 13 2011 Tomas Bzatek <tbzatek@redhat.com> - 2.8.4-2
- Rebuild for new xz-libs

* Wed Jun 30 2010 Tomas Bzatek <tbzatek@redhat.com> - 2.8.4-1
- Update to 2.8.4

* Fri Jun 25 2010 Tomas Bzatek <tbzatek@redhat.com> - 2.8.3-2
- Fix ISO9660 reader data type mismatches (#597243)

* Tue Mar 16 2010 Tomas Bzatek <tbzatek@redhat.com> - 2.8.3-1
- Update to 2.8.3

* Mon Mar  8 2010 Tomas Bzatek <tbzatek@redhat.com> - 2.8.1-1
- Update to 2.8.1

* Fri Feb  5 2010 Tomas Bzatek <tbzatek@redhat.com> - 2.8.0-1
- Update to 2.8.0

* Wed Jan  6 2010 Tomas Bzatek <tbzatek@redhat.com> - 2.7.902a-1
- Update to 2.7.902a

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 2.7.1-2
- rebuilt with new openssl

* Fri Aug  7 2009 Tomas Bzatek <tbzatek@redhat.com> 2.7.1-1
- Update to 2.7.1
- Drop deprecated lzma dependency, libxz handles both formats

* Mon Jul 27 2009 Tomas Bzatek <tbzatek@redhat.com> 2.7.0-3
- Enable XZ compression format

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue May 12 2009 Tomas Bzatek <tbzatek@redhat.com> 2.7.0-1
- Update to 2.7.0

* Fri Mar  6 2009 Tomas Bzatek <tbzatek@redhat.com> 2.6.2-1
- Update to 2.6.2

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 16 2009 Tomas Bzatek <tbzatek@redhat.com> 2.6.1-1
- Update to 2.6.1

* Thu Jan  8 2009 Tomas Bzatek <tbzatek@redhat.com> 2.6.0-1
- Update to 2.6.0

* Mon Dec 15 2008 Tomas Bzatek <tbzatek@redhat.com> 2.5.904a-1
- Update to 2.5.904a

* Tue Dec  9 2008 Tomas Bzatek <tbzatek@redhat.com> 2.5.903a-2
- Add LZMA support

* Mon Dec  8 2008 Tomas Bzatek <tbzatek@redhat.com> 2.5.903a-1
- Update to 2.5.903a

* Tue Jul 22 2008 Tomas Bzatek <tbzatek@redhat.com> 2.5.5-1
- Update to 2.5.5

* Wed Apr  2 2008 Tomas Bzatek <tbzatek@redhat.com> 2.4.17-1
- Update to 2.4.17

* Wed Mar 19 2008 Tomas Bzatek <tbzatek@redhat.com> 2.4.14-1
- Initial packaging
