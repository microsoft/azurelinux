Summary:        A high-performance implementation of MPI
Name:           mpich
Version:        3.3.2
Release:        7%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.mpich.org/

Source0:        https://www.mpich.org/static/downloads/%{version}/%{name}-%{version}.tar.gz
Source1:        mpich.macros
Source2:        mpich.pth.py3
Patch0:         mpich-modules.patch
Patch1:         0001-Drop-real128.patch
# fix for #1793563 and #1799473
Patch2:         https://github.com/pmodels/mpich/pull/4320.patch

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gcc-gfortran
BuildRequires:  hwloc-devel >= 2.0
%ifnarch s390 %{mips}
BuildRequires:  valgrind-devel
%endif
# For %%{python3_sitearch}
BuildRequires:  python3-devel
BuildRequires:  rpm-mpi-hooks
BuildRequires:  automake
Provides:       mpi
Provides:       mpich2 = %{version}
Obsoletes:      mpich2 < 3.0
Requires:       environment(modules)

# Make sure this package is rebuilt with correct Python version when updating
# Otherwise mpi.req from rpm-mpi-hooks doesn't work
# https://bugzilla.redhat.com/show_bug.cgi?id=1705296
Requires:       python3

%description
MPICH is a high-performance and widely portable implementation of the Message
Passing Interface (MPI) standard (MPI-1, MPI-2 and MPI-3). The goals of MPICH
are: (1) to provide an MPI implementation that efficiently supports different
computation and communication platforms including commodity clusters (desktop
systems, shared-memory systems, multicore architectures), high-speed networks
(10 Gigabit Ethernet, InfiniBand, Myrinet, Quadrics) and proprietary high-end
computing systems (Blue Gene, Cray) and (2) to enable cutting-edge research in
MPI through an easy-to-extend modular framework for other derived
implementations.

The mpich binaries in this RPM packages were configured to use the default
process manager (Hydra) using the default device (ch3). The ch3 device
was configured with support for the nemesis channel that allows for
shared-memory and TCP/IP sockets based communication.

This build also include support for using the 'module environment' to select
which MPI implementation to use when multiple implementations are installed.
If you want MPICH support to be automatically loaded, you need to install the
mpich-autoload package.

%package autoload
Summary:        Load mpich automatically into profile
Requires:       mpich = %{version}-%{release}
Provides:       mpich2-autoload = 3.0.1
Obsoletes:      mpich2-autoload < 3.0

%description autoload
This package contains profile files that make mpich automatically loaded.

%package devel
Summary:        Development files for mpich
Provides:       %{name}-devel-static = %{version}-%{release}
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig
Requires:       gcc-gfortran
Requires:       rpm-mpi-hooks
Provides:       mpich2-devel = 3.0.1
Obsoletes:      mpich2-devel < 3.0

%description devel
Contains development headers and libraries for mpich

%package doc
Summary:        Documentations and examples for mpich
BuildArch:      noarch
Requires:       %{name}-devel = %{version}-%{release}
Provides:       mpich2-doc = 3.0.1
Obsoletes:      mpich2-doc < 3.0

%description doc
Contains documentations, examples and man-pages for mpich

%package -n python3-mpich
Summary:        mpich support for Python 3
Requires:       %{name} = %{version}-%{release}
Requires:       python3

%description -n python3-mpich
mpich support for Python 3.

%prep
%setup

%patch0 -p1

%ifarch %{arm}
%patch1 -p1
%endif
%patch2 -p1

%build
CONFIGURE_OPTS=(
        --enable-sharedlibs=gcc
        --enable-shared
        --enable-static=no
        --enable-lib-depend
        --disable-rpath
        --disable-silent-rules
        --enable-fc
        --with-device=ch3:nemesis
        --with-pm=hydra:gforker
        --includedir=%{_includedir}/%{name}-%{_arch}
        --bindir=%{_libdir}/%{name}/bin
        --libdir=%{_libdir}/%{name}/lib
        --datadir=%{_datadir}/%{name}
        --mandir=%{_mandir}/%{name}-%{_arch}
        --docdir=%{_datadir}/%{name}/doc
        --htmldir=%{_datadir}/%{name}/doc
        --with-hwloc-prefix=system
        --disable-fortran
)

# Set -fallow-argument-mismatch for #1795817
%configure "${CONFIGURE_OPTS[@]}" FFLAGS="$FFLAGS -fallow-argument-mismatch"

# Remove rpath
sed -r -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -r -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

#Try and work around 'unused-direct-shlib-dependency' rpmlint warnning
sed -i -e 's| -shared | -Wl,--as-needed\0|g' libtool

# work-around libtool error: cannot determine absolute directory name of 'system/lib'
mkdir -p system/lib

%make_build VERBOSE=1

%install
%make_install


# Install the module file
mkdir -p %{buildroot}%{_datadir}/modulefiles/mpi
sed -r 's|%{_bindir}|%{_libdir}/%{name}/bin|;
        s|@LIBDIR@|%{_libdir}/%{name}|;
        s|@MPINAME@|%{name}|;
        s|@py2sitearch@|%{python2_sitearch}|;
        s|@py3sitearch@|%{python3_sitearch}|;
        s|@ARCH@|%{_arch}|;
     ' \
     <src/packaging/envmods/mpich.module \
     >%{buildroot}%{_datadir}/modulefiles/mpi/%{name}-%{_arch}

mkdir -p %{buildroot}%{_sysconfdir}/profile.d
cat >%{buildroot}%{_sysconfdir}/profile.d/mpich-%{_arch}.sh <<EOF
# Load mpich environment module
module load mpi/%{name}-%{_arch}
EOF
cp -p %{buildroot}%{_sysconfdir}/profile.d/mpich-%{_arch}.{sh,csh}

# Install the RPM macros
install -pDm0644 %{SOURCE1} %{buildroot}%{_rpmconfigdir}/macros.d/macros.%{name}

# Install the .pth file
mkdir -p %{buildroot}%{python3_sitearch}/%{name}
install -pDm0644 %{SOURCE2} %{buildroot}%{python3_sitearch}/%{name}.pth

find %{buildroot} -type f -name "*.la" -delete


%check
make check VERBOSE=1

%ldconfig_scriptlets

%files
%license COPYRIGHT
%doc CHANGES README README.envvar RELEASE_NOTES
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/lib
%dir %{_libdir}/%{name}/bin
%{_libdir}/%{name}/lib/*.so.*
%{_libdir}/%{name}/bin/hydra*
%{_libdir}/%{name}/bin/mpichversion
%{_libdir}/%{name}/bin/mpiexec*
%{_libdir}/%{name}/bin/mpirun
%{_libdir}/%{name}/bin/mpivars
%{_libdir}/%{name}/bin/parkill
%dir %{_mandir}/%{name}-%{_arch}
%doc %{_mandir}/%{name}-%{_arch}/man1/
%{_datadir}/modulefiles/mpi/

%files autoload
%{_sysconfdir}/profile.d/mpich-%{_arch}.*

%files devel
%{_includedir}/%{name}-%{_arch}/
%{_libdir}/%{name}/lib/pkgconfig/
%{_libdir}/%{name}/lib/*.so
%{_libdir}/%{name}/bin/mpicc
%{_libdir}/%{name}/bin/mpic++
%{_libdir}/%{name}/bin/mpicxx
%{_rpmconfigdir}/macros.d/macros.%{name}
%{_mandir}/%{name}-%{_arch}/man3/

%files doc
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/doc/

%files -n python3-mpich
%dir %{python3_sitearch}/%{name}
%{python3_sitearch}/%{name}.pth

%changelog
* Fri May 28 2021 Thomas Crain <thcrain@microsoft.com> - 3.3.2-7
- Remove mpich.pth.py2 file from sources/installation steps

* Wed Jan 20 2021 Joe Schmitt <joschmit@microsoft.com> - 3.3.2-6
- Remove python(abi) requirement

* Fri Jan 08 2021 Ruying Chen <v-ruyche@microsoft.com> - 3.3.2-5
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Remove redhat-rpm-config build requirement.
- Disable fortran support.
- Remove python2 site-packages.

* Fri Feb 14 2020 Christoph Junghans <junghans@votca.org> - 3.3.2-4
- Add 4320.patch to fix #1793563 and #1799473

* Thu Jan 30 2020 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.3.2-3
- Add requirement for redhat-rpm-config (#1795674)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Nov 17 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.3.2-1
- Subpackage python2-mpich has been removed (#1773126)

* Sun Nov 17 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.3.2-1
- Update to latest version (#1772152). This is a bugfix release:
  https://github.com/pmodels/mpich/blob/v3.3.2/CHANGES.

* Wed Aug 28 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.3.1-1
- Really upgrade to 3.3.1 (#1745252)

* Sat Aug 24 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.2.1-1
- "Upgrade" back to 3.2.1 (#1745252)
  (I made a typo, and instead of *upgrading* to 3.3.1, I made a downgrade
   to 3.1.1. Too bad that we don't have *any* automatic check that would
   warn about this in Fedora. Version 3.3.1 requires a newer hwloc, but
   some of the dependencies are not ready to switch. So let's "upgrade"
   back to 3.2.1, and plan to 3.3.1 next week.)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 3.1.1-2
- Rebuilt for Python 3.8

* Tue Jul 30 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.1.1-1
- Update to latest version (#1718376)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed May  8 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.2.1-12
- Require main package and appropriate python version from python subpackages

* Tue May  7 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.2.1-11
- Add a guard for python3 version (#1705296)
- Module files are moved to /usr/share/modulefiles/mpi/

* Tue May  7 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.2.1-10
- Drop all custom compilation and link flags (#1573088)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 3.2.1-7
- Rebuilt for Python 3.7

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 3.2.1-6
- Rebuilt for Python 3.7

* Wed Apr  4 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.2.1-5
- Update MANPATH so that normal man pages can still be found (#1533717)

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Feb 01 2018 Ralf Corsépius <corsepiu@fedoraproject.org> - 3.2.1-3
- Rebuilt for GCC-8.0.1.

* Sun Nov 12 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.2.1-2
- Update $modincdir in mpifort after moving .mod files (#1301533)
- Move compiler wrappers to mpich-devel (#1353621)
- Remove bogus rpath (#1361586)

* Sun Nov 12 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.2.1-1
- Update to latest bugfix release (#1512188)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 3.2-7
- Rebuild for Python 3.6

* Wed Nov 2 2016 Orion Poplawski <orion@cora.nwra.com> - 3.2-7
- Split python support into sub-packages

* Wed Mar 30 2016 Michal Toman <mtoman@fedoraproject.org> - 3.2-6
- Fix build on MIPS

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 22 2016 Orion Poplawski <orion@cora.nwra.com> - 3.2-4
- Add patch to allow -host localhost to work on builders

* Wed Jan 20 2016 Orion Poplawski <orion@cora.nwra.com> - 3.2-3
- Use nemesis channel on all platforms

* Wed Dec  9 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.2-2
- Soften version check (#1289779)

* Tue Dec  1 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.2-1
- Update to latest version

* Mon Nov 16 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.1.4-9
- Update requires and fix MPI_FORTRAN_MOD_DIR var

* Mon Nov 16 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.1.4-8
- Move fortran .mod files to %%{_fmoddir}/mpich (#1154991)
- Move man pages to arch-specific dir (#1264359)

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.4-7
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Aug 27 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.1.4-6
- Use .pth files to set the python path (https://fedorahosted.org/fpc/ticket/563)
- Cleanups to the spec file

* Sun Jul 26 2015 Sandro Mani <manisandro@gmail.com> - 3.1.4-5
- Require, BuildRequire: rpm-mpi-hooks

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May  9 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.1.4-3
- Change MPI_SYCONFIG to /etc/mpich-x86_64 (#1196728)

* Fri Mar 13 2015 Orion Poplawski <orion@cora.nwra.com> - 3.1.4-2
- Set PKG_CONFIG_DIR (bug #1113627)
- Fix modulefile names and python paths (bug#1201343)

* Wed Mar 11 2015 Orion Poplawski <orion@cora.nwra.com> - 3.1.4-1
- Update to 3.1.4
- Own and set PKG_CONFIG_DIR (bug #1113627)
- Do not ship old modulefile location (bug #921534)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Feb 21 2014 Ville Skyttä <ville.skytta@iki.fi> - 3.1-2
- Install rpm macros to %%{_rpmconfigdir}/macros.d as non-%%config.

* Fri Feb 21 2014 Deji Akingunola <dakingun@gmail.com> - 3.1-1
- Update to 3.1

* Mon Jan  6 2014 Peter Robinson <pbrobinson@fedoraproject.org> 3.0.4-7
- Set the aarch64 compiler options

* Fri Dec 13 2013 Peter Robinson <pbrobinson@fedoraproject.org> 3.0.4-6
- Now have valgrind on ARMv7
- No valgrind on aarch64

* Fri Aug 23 2013 Orion Poplawski <orion@cora.nwra.com> - 3.0.4-5
- Add %%check

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 20 2013 Deji Akingunola <dakingun@gmail.com> - 3.0.4-3
- Add proper Provides and Obsoletes for the sub-packages

* Thu Jul 18 2013 Deji Akingunola <dakingun@gmail.com> - 3.0.4-2
- Fix some of the rpmlint warnings from package review (BZ #973493)

* Wed Jun 12 2013 Deji Akingunola <dakingun@gmail.com> - 3.0.4-1
- Update to 3.0.4

* Thu Feb 21 2013 Deji Akingunola <dakingun@gmail.com> - 3.0.2-1
- Update to 3.0.2
- Rename to mpich.
- Drop check for old alternatives' installation

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 1 2012 Orion Poplawski <orion@cora.nwra.com> - 1.5-1
- Update to 1.5
- Drop destdir-fix and mpicxx-und patches
- Update rpm macros to use the new module location

* Wed Oct 31 2012 Orion Poplawski <orion@cora.nwra.com> - 1.4.1p1-9
- Install module file in mpi subdirectory and conflict with other mpi modules
- Leave existing module file location for backwards compatibility for a while

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1p1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Feb 15 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.4.1p1-7
- Rebuild for new hwloc

* Wed Feb 15 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.4.1p1-6
- Update ARM build configuration

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1p1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jan  2 2012 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.4.1p1-4
- Bump spec.

* Wed Nov 16 2011 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.4.1p1-3
- Comply to MPI guidelines by separating autoloading into separate package
  (BZ #647147).

* Tue Oct 18 2011 Deji Akingunola <dakingun@gmail.com> - 1.4.1p1-2
- Rebuild for hwloc soname bump.

* Sun Sep 11 2011 Deji Akingunola <dakingun@gmail.com> - 1.4.1p1-1
- Update to 1.4.1p1 patch update
- Add enable-lib-depend to configure flags

* Sat Aug 27 2011 Deji Akingunola <dakingun@gmail.com> - 1.4.1-1
- Update to 1.4.1 final
- Drop the mpd subpackage, the PM is no longer supported upstream
- Fix undefined symbols in libmpichcxx (again) (#732926)

* Wed Aug 03 2011 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.4-2
- Respect environment module guidelines wrt placement of module file.

* Fri Jun 17 2011 Deji Akingunola <dakingun@gmail.com> - 1.4-1
- Update to 1.4 final
