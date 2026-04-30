## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 2;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           nauty
Version:        2.9.3
Release:        %autorelease
Summary:        Graph canonical labeling and automorphism group computation

%global nautytarver %(tr . _ <<< %{version})

# The projects as a whole is Apache-2.0.
# The bundled cliquer code in nautycliquer.c is GPL-2.0-or-later, but we patch
# it out.
# The SHA256 code in nausha.{c,h} is in the public domain.
# Other licenses are due to embedded fonts in the PDF manual.
# CM: Knuth-CTAN
# CM-Super: GPL-1.0-or-later
License:        Apache-2.0 AND LicenseRef-Fedora-Public-Domain AND Knuth-CTAN AND GPL-1.0-or-later
URL:            https://pallini.di.uniroma1.it/
Source:         https://pallini.di.uniroma1.it/%{name}%{nautytarver}.tar.gz

# Debian patch to fix the gt_numorbits declaration
Patch:          %{name}-fix-gt_numorbits.patch
# Use zlib-ng instead of invoking zcat through a pipe
Patch:          %{name}-zlib-dimacs2g.patch
# Debian patch to improve usage and help information
Patch:          %{name}-help2man.patch
# Link binaries with shared libraries instead of static libraries
Patch:          %{name}-shared.patch
# Detect availability of the popcnt instruction at runtime
Patch:          %{name}-popcnt.patch
# Unbundle cliquer
Patch:          %{name}-unbundle-cliquer.patch
# Fix uninitialized variable warnings
Patch:          %{name}-uninitialized.patch

BuildRequires:  gcc
BuildRequires:  gmp-devel
BuildRequires:  help2man
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  pkgconfig(libcliquer)
BuildRequires:  pkgconfig(zlib-ng)

# Some version of planarity is bundled.  I do not know which version it is,
# but the interface is completely different from the one provided by Fedora's
# planarity package.
Provides:       bundled(planarity)

# The shortg program invokes sort.
Requires:       coreutils
Requires:       lib%{name}%{?_isa} = %{version}-%{release}

%description
Nauty and Traces are programs for computing automorphism groups of graphs and
digraphs.  (At present, Traces does not accept digraphs.)  They can also
produce a canonical label.  They are written in a portable subset of C, and
run on a considerable number of different systems.

There is a small suite of programs called gtools included in the package.  For
example, geng can generate non-isomorphic graphs very quickly.  There are also
generators for bipartite graphs, digraphs, and multigraphs, and programs for
manipulating files of graphs in a compact format.

%package     -n libnauty
License:        Apache-2.0
Summary:        Library for graph automorphism

%description -n libnauty
Nauty (No AUTomorphisms, Yes?) is a set of procedures for computing
automorphism groups of graphs and digraphs.  This package contains a library
of nauty procedures.

%package     -n libnauty-devel
License:        Apache-2.0
Summary:        Development files for libnauty
Requires:       lib%{name}%{?_isa} = %{version}-%{release}

%description -n libnauty-devel
This package contains files needed to develop programs that use libnauty.

%prep
%autosetup -p1 -n %{name}%{nautytarver}

%conf
# Remove the pregenerated makefile
rm -f makefile

# Regenerate the configure script due to the patches
aclocal
autoreconf -fi

# Fix the pkgconfig file
sed -i 's,/usr/local,%{_prefix},' nauty.pc
if [ '%{_lib}' != 'lib' ]; then
    sed -i 's,/lib,/lib64,' nauty.pc
fi

%build
export CFLAGS='%{build_cflags} -fwrapv -I%{_includedir}/cliquer'
export LIBS='-lz-ng'
%configure \
    --enable-ansi \
    --enable-generic \
%ifarch %{ix86} %{x86_64}
    --disable-popcnt \
    --enable-runtime-popcnt \
%endif
    --disable-static \
    --enable-tls

# Get rid of undesirable hardcoded rpaths; workaround libtool reordering
# -Wl,--as-needed after all the libraries.
sed -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
    -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' \
    -e 's|CC="\(.*g..\)"|CC="\1 -Wl,--as-needed"|' \
    -i libtool

# FIXME: parallel building was broken in version 2.8.9
make

%install
%make_install

# Generate the man pages
export LD_LIBRARY_PATH=%{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_mandir}/man1
for f in %{buildroot}%{_bindir}/*; do
  help2man -N -o %{buildroot}%{_mandir}/man1/$(basename $f).1 \
    --version-string=%{version} $f
done

# Link identical executables
rm %{buildroot}%{_bindir}/pickg
ln countg %{buildroot}%{_bindir}/pickg

# Move the headers
mkdir -p %{buildroot}%{_includedir}/nauty
mv %{buildroot}%{_includedir}/*.h %{buildroot}%{_includedir}/nauty

%check
chmod a+x runalltests
LD_LIBRARY_PATH=$PWD/.libs PATH=$PWD:$PATH make check

%files
%doc README nug29.pdf
%{_bindir}/*g
%{_bindir}/*gL
%{_bindir}/dreadnaut
%{_bindir}/dretodot
%{_bindir}/hamheuristic
%{_bindir}/watercluster2
%{_mandir}/man1/*g.1*
%{_mandir}/man1/*gL.1*
%{_mandir}/man1/dreadnaut.1*
%{_mandir}/man1/dretodot.1*
%{_mandir}/man1/hamheuristic.1*
%{_mandir}/man1/watercluster2.1*

%files -n libnauty
%doc changes24-29.txt formats.txt
%license COPYRIGHT LICENSE-2.0.txt
%{_libdir}/libnauty-2.9.3.so
%{_libdir}/libnautyS-2.9.3.so
%{_libdir}/libnautyW-2.9.3.so
%{_libdir}/libnautyL-2.9.3.so
%{_libdir}/libnauty1-2.9.3.so
%{_libdir}/libnautyS1-2.9.3.so
%{_libdir}/libnautyW1-2.9.3.so
%{_libdir}/libnautyL1-2.9.3.so
%if 0%{?__isa_bits} == 64
%{_libdir}/libnautyQ-2.9.3.so
%{_libdir}/libnautyQ1-2.9.3.so
%endif

%files -n libnauty-devel
%doc schreier.txt
%{_includedir}/nauty/
%{_libdir}/pkgconfig/lib%{name}*.pc
%{_libdir}/libnauty.so
%{_libdir}/libnautyS.so
%{_libdir}/libnautyW.so
%{_libdir}/libnautyL.so
%{_libdir}/libnauty1.so
%{_libdir}/libnautyS1.so
%{_libdir}/libnautyW1.so
%{_libdir}/libnautyL1.so
%if 0%{?__isa_bits} == 64
%{_libdir}/libnautyQ.so
%{_libdir}/libnautyQ1.so
%endif

%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 2.9.3-2
- test: add initial lock files

* Thu Jan 08 2026 Jerry James <loganjerry@gmail.com> - 2.9.3-1
- Version 2.9.3

* Wed Sep 17 2025 Jerry James <loganjerry@gmail.com> - 2.9.1-1
- Version 2.9.1
- Drop upstreamed patches: big-endian, fall-off, memory-overrun

* Sat Aug 23 2025 Jerry James <loganjerry@gmail.com> - 2.9.0-4
- Make the buffer overrun patch even more correct

* Sat Aug 23 2025 Jerry James <loganjerry@gmail.com> - 2.9.0-3
- Add patch to fix buffer overruns

* Wed Jul 30 2025 Jerry James <loganjerry@gmail.com> - 2.9.0-2
- Fix SHA256 computation on big-endian architectures

* Wed Jul 30 2025 Jerry James <loganjerry@gmail.com> - 2.9.0-1
- Version 2.9.0
- Drop upstreamed format patch
- Modify License for public domain SHA256 code

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Jan 14 2025 Jerry James <loganjerry@gmail.com> - 2.8.9-2
- Move configuration steps to %%conf

* Mon Sep 23 2024 Jerry James <loganjerry@gmail.com> - 2.8.9-1
- Version 2.8.9
- Drop upstreamed or irrelevant patches: autoconf, autotoolization,
  includes, noreturn
- Drop tool-prefix patch; ship binaries with upstream names
- Add shared patch to link shared libraries with Fedora linker flags
- Use zlib-ng directly instead of via the compatibility interface
- Minor spec file simplifications

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Apr 12 2024 Jerry James <loganjerry@gmail.com> - 2.8.8-4
- Fix FTBFS with autoconf 2.72

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Nov 28 2023 Jerry James <loganjerry@gmail.com> - 2.8.8-1
- Version 2.8.8
- Drop upstreamed gentreeg patch

* Sat Sep 30 2023 Jerry James <loganjerry@gmail.com> - 2.8.6-5
- Add patch to fix gentreeg bug (bz 2241471)

* Thu Aug 10 2023 Jerry James <loganjerry@gmail.com> - 2.8.6-4
- Use a more reliable way of detecting CPU features

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Nov 16 2022 Jerry James <loganjerry@gmail.com> - 2.8.6-1
- Version 2_8_6
- Convert License tag to SPDX

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul  1 2022 Jerry James <loganjerry@gmail.com> - 2.7.4-1
- Version 2.7r4
- Add -fall-off and -noreturn patches

* Thu Jan 27 2022 Jerry James <loganjerry@gmail.com> - 2.7.3-2
- Disable popcnt support on i386 due to test failures
- Add -format and -uninitialized patches

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Sep  6 2021 Jerry James <loganjerry@gmail.com> - 2.7.3-1
- Version 2.7.3

* Thu Sep  2 2021 Jerry James <loganjerry@gmail.com> - 2.7.2-1
- Version 2.7.2

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jan 05 2021 Timm Bäder <tbaeder@redhat.com> - 2.7.1-3
- Enable runtime popcount support on clang

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun  2 2020 Jerry James <loganjerry@gmail.com> - 2.7.1-1
- Version 2.7.1

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Oct 15 2019 Jerry James <loganjerry@gmail.com> - 2.6.12-1
- New upstream version

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Oct  6 2018 Jerry James <loganjerry@gmail.com> - 2.6.11-1
- New upstream version

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Oct 23 2017 Jerry James <loganjerry@gmail.com> - 2.6.10-1
- New upstream version

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Sep 10 2016 Jerry James <loganjerry@gmail.com> - 2.6.7-1
- New upstream version

* Thu Apr 21 2016 Jerry James <loganjerry@gmail.com> - 2.6.5-1
- New upstream version

* Fri Apr 15 2016 Jerry James <loganjerry@gmail.com> - 2.6.4-1
- Initial RPM

## END: Generated by rpmautospec
