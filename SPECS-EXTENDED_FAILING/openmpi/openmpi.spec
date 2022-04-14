Vendor:         Microsoft Corporation
Distribution:   Mariner
%global _hardened_build 1
# We only compile with gcc, but other people may want other compilers.
# Set the compiler here.
%global opt_cc gcc
# Optional CFLAGS to use with the specific compiler...gcc doesn't need any,
# so uncomment and define to use
#global opt_cflags
%global opt_cxx g++
#global opt_cxxflags
%global opt_f77 gfortran
#global opt_fflags
%global opt_fc gfortran
#global opt_fcflags

# Optional name suffix to use...we leave it off when compiling with gcc, but
# for other compiled versions to install side by side, it will need a
# suffix in order to keep the names from conflicting.
#global _cc_name_suffix -gcc

%global macrosdir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)


%bcond_with python2
%bcond_with ucx

# ARM 32-bit is not supported by rdma
# https://bugzilla.redhat.com/show_bug.cgi?id=1780584
%ifarch %{arm}
%bcond_with rdma
%else
%bcond_without rdma
%endif

Name:            openmpi%{?_cc_name_suffix}
Version:         4.0.3x
Release:         5%{?dist}
Summary:         Open Message Passing Interface
License:         BSD and MIT and Romio
URL:             http://www.open-mpi.org/

# We can't use %%{name} here because of _cc_name_suffix
#Source0:         https://www.open-mpi.org/software/ompi/v4.0/downloads/openmpi-%{version}.tar.bz2
Source0:         https://www.open-mpi.org/software/ompi/v4.0/downloads/openmpi-4.0.3.tar.bz2
Source1:         openmpi.module.in
Source2:         openmpi.pth.py2
Source3:         openmpi.pth.py3
Source4:         macros.openmpi

BuildRequires:   gcc-c++
BuildRequires:   gcc-gfortran
BuildRequires:   valgrind-devel
%if %{with rdma}
BuildRequires:   opensm-devel > 3.3.0
BuildRequires:   rdma-core-devel
%endif
# Doesn't compile:
# vt_dyn.cc:958:28: error: 'class BPatch_basicBlockLoop' has no member named 'getLoopHead'
#                      loop->getLoopHead()->getStartAddress(), loop_stmts );
#BuildRequires:   dyninst-devel
BuildRequires:   hwloc-devel
# So configure can find lstopo
BuildRequires:   java-devel
# Old libevent causes issues
%if !0%{?el7}
BuildRequires:   libevent-devel
%endif
BuildRequires:   libfabric-devel
%ifnarch s390 s390x
BuildRequires:   papi-devel
%endif
BuildRequires:   orangefs-devel
BuildRequires:   perl-generators
BuildRequires:   perl-interpreter
BuildRequires:   perl(Getopt::Long)
BuildRequires:   pmix-devel
BuildRequires:   python%{python3_pkgversion}-devel
%ifarch x86_64
BuildRequires:   infinipath-psm-devel
BuildRequires:   libpsm2-devel
%endif
%if %{with ucx}
BuildRequires:   ucx-devel
%endif
BuildRequires:   zlib-devel
%if !0%{?el7}
BuildRequires:   rpm-mpi-hooks
%endif

Provides:        mpi
%if 0%{?rhel}
# Need this for /etc/profile.d/modules.sh
Requires:        environment-modules
%endif
Requires:        environment(modules)
# openmpi currently requires ssh to run
# https://svn.open-mpi.org/trac/ompi/ticket/4228
Requires:        openssh-clients

# Private openmpi libraries
%global __provides_exclude_from %{_libdir}/openmpi/lib/(lib(mca|ompi|open-(pal|rte|trace))|openmpi/).*.so
%global __requires_exclude lib(mca|ompi|open-(pal|rte|trace)|vt).*

%description
Open MPI is an open source, freely available implementation of both the
MPI-1 and MPI-2 standards, combining technologies and resources from
several other projects (FT-MPI, LA-MPI, LAM/MPI, and PACX-MPI) in
order to build the best MPI library available.  A completely new MPI-2
compliant implementation, Open MPI offers advantages for system and
software vendors, application developers, and computer science
researchers. For more information, see http://www.open-mpi.org/ .

%package devel
Summary:	Development files for openmpi
Requires:	%{name} = %{version}-%{release}, gcc-gfortran
Provides:	mpi-devel
Requires:	rpm-mpi-hooks
# Make sure this package is rebuilt with correct Python version when updating
# Otherwise mpi.req from rpm-mpi-hooks doesn't work
# https://bugzilla.redhat.com/show_bug.cgi?id=1705296
Requires:	python3

%description devel
Contains development headers and libraries for openmpi.

%package java
Summary:    Java library
Requires:   %{name} = %{version}-%{release}

Requires:   java




%description java
Java library.

%package java-devel
Summary:    Java development files for openmpi
Requires:   %{name}-java = %{version}-%{release}
Requires:   java-devel

%description java-devel
Contains development wrapper for compiling Java with openmpi.

# We set this to for convenience, since this is the unique dir we use for this
# particular package, version, compiler
%global namearch openmpi-%{_arch}%{?_cc_name_suffix}

%if %{with python2}
%package -n python2-openmpi
Summary:    OpenMPI support for Python 2
BuildRequires: python2-devel
Requires:   %{name} = %{version}-%{release}
Requires:   python2

%description -n python2-openmpi
OpenMPI support for Python 2.
%endif

%package -n python%{python3_pkgversion}-openmpi
Summary:    OpenMPI support for Python 3
Requires:   %{name} = %{version}-%{release}
Requires:   python3

%description -n python%{python3_pkgversion}-openmpi
OpenMPI support for Python 3.


%prep
%autosetup -p1 -n openmpi-4.0.3


%build
./configure --prefix=%{_libdir}/%{name} \
	--mandir=%{_mandir}/%{namearch} \
	--includedir=%{_includedir}/%{namearch} \
	--sysconfdir=%{_sysconfdir}/%{namearch} \
	--disable-silent-rules \
	--enable-builtin-atomics \
	--enable-mpi-cxx \
	--enable-mpi-java \
  --with-jdk-dir="/usr/lib/jvm/OpenJDK-1.8.0.292" \
	--enable-mpi1-compatibility \
	--with-sge \
	--with-valgrind \
	--enable-memchecker \
	--with-hwloc=/usr \
%if !0%{?el7}
	--with-libevent=external \
	--with-pmix=external \
%endif
	CC=%{opt_cc} CXX=%{opt_cxx} \
	LDFLAGS='%{__global_ldflags}' \
	CFLAGS="%{?opt_cflags} %{!?opt_cflags:$RPM_OPT_FLAGS}" \
	CXXFLAGS="%{?opt_cxxflags} %{!?opt_cxxflags:$RPM_OPT_FLAGS}" \
	FC=%{opt_fc} FCFLAGS="%{?opt_fcflags} %{!?opt_fcflags:$RPM_OPT_FLAGS}"
#        --with-contrib-vt-flags='CXXFLAGS="-I%{_includedir}/dyninst -L%{_libdir}/dyninst"' \

%make_build V=1

%install
%make_install
find %{buildroot}%{_libdir}/%{name}/lib -name \*.la | xargs rm
find %{buildroot}%{_mandir}/%{namearch} -type f | xargs gzip -9
ln -s mpicc.1.gz %{buildroot}%{_mandir}/%{namearch}/man1/mpiCC.1.gz
# Remove dangling symlink
rm %{buildroot}%{_mandir}/%{namearch}/man1/mpiCC.1
mkdir %{buildroot}%{_mandir}/%{namearch}/man{2,4,5,6,8,9,n}

# Make the environment-modules file
mkdir -p %{buildroot}%{_datadir}/modulefiles/mpi
# Since we're doing our own substitution here, use our own definitions.
sed 's#@LIBDIR@#%{_libdir}/%{name}#;
     s#@ETCDIR@#%{_sysconfdir}/%{namearch}#;
     s#@FMODDIR@#%{_fmoddir}/%{name}#;
     s#@INCDIR@#%{_includedir}/%{namearch}#;
     s#@MANDIR@#%{_mandir}/%{namearch}#;
%if %{with python2}
     s#@PY2SITEARCH@#%{python2_sitearch}/%{name}#;
%else
     /@PY2SITEARCH@/d;
%endif
     s#@PY3SITEARCH@#%{python3_sitearch}/%{name}#;
     s#@COMPILER@#openmpi-%{_arch}%{?_cc_name_suffix}#;
     s#@SUFFIX@#%{?_cc_name_suffix}_openmpi#' \
     <%{SOURCE1} \
     >%{buildroot}%{_datadir}/modulefiles/mpi/%{namearch}

# make the rpm config file
install -Dpm 644 %{SOURCE4} %{buildroot}/%{macrosdir}/macros.%{namearch}

# Link the fortran module to proper location
mkdir -p %{buildroot}%{_fmoddir}/%{name}
for mod in %{buildroot}%{_libdir}/%{name}/lib/*.mod
do
  modname=$(basename $mod)
  ln -s ../../../%{name}/lib/${modname} %{buildroot}/%{_fmoddir}/%{name}/
done

# Link the pkgconfig files into the main namespace as well
mkdir -p %{buildroot}%{_libdir}/pkgconfig
cd %{buildroot}%{_libdir}/pkgconfig
ln -s ../%{name}/lib/pkgconfig/*.pc .
cd -

# Remove extraneous wrapper link libraries (bug 814798)
sed -i -e s/-ldl// -e s/-lhwloc// \
  %{buildroot}%{_libdir}/%{name}/share/openmpi/*-wrapper-data.txt

# install .pth files
%if %{with python2}
mkdir -p %{buildroot}/%{python2_sitearch}/%{name}
install -pDm0644 %{SOURCE2} %{buildroot}/%{python2_sitearch}/openmpi.pth
%endif
mkdir -p %{buildroot}/%{python3_sitearch}/%{name}
install -pDm0644 %{SOURCE3} %{buildroot}/%{python3_sitearch}/openmpi.pth

%check
make check

%files
%license LICENSE
%dir %{_libdir}/%{name}
%dir %{_sysconfdir}/%{namearch}
%dir %{_libdir}/%{name}/bin
%dir %{_libdir}/%{name}/lib
%dir %{_libdir}/%{name}/lib/openmpi
%dir %{_mandir}/%{namearch}
%dir %{_mandir}/%{namearch}/man*
%config(noreplace) %{_sysconfdir}/%{namearch}/*
%{_libdir}/%{name}/bin/mpi[er]*
%{_libdir}/%{name}/bin/ompi*
%{_libdir}/%{name}/bin/orte[-dr_]*
%if %{with ucx}
%{_libdir}/%{name}/bin/oshmem_info
%{_libdir}/%{name}/bin/oshrun
%{_libdir}/%{name}/bin/shmemrun
%endif
%{_libdir}/%{name}/lib/*.so.40*
%{_libdir}/%{name}/lib/libmca*.so.41*
%{_libdir}/%{name}/lib/libmca*.so.50*
%if 0%{?el7}
%{_libdir}/%{name}/lib/pmix/
%endif
%{_mandir}/%{namearch}/man1/mpi[er]*
%{_mandir}/%{namearch}/man1/ompi*
%{_mandir}/%{namearch}/man1/orte[-dr_]*
%if %{with ucx}
%{_mandir}/%{namearch}/man1/oshmem_info*
%{_mandir}/%{namearch}/man1/oshrun*
%{_mandir}/%{namearch}/man1/shmemrun*
%endif
%{_mandir}/%{namearch}/man7/ompi_*
%{_mandir}/%{namearch}/man7/opal_*
%{_mandir}/%{namearch}/man7/orte*
%{_libdir}/%{name}/lib/openmpi/*
%{_datadir}/modulefiles/mpi/
%dir %{_libdir}/%{name}/share
%dir %{_libdir}/%{name}/share/openmpi
%{_libdir}/%{name}/share/openmpi/amca-param-sets
%{_libdir}/%{name}/share/openmpi/help*.txt
%if %{with rdma}
%{_libdir}/%{name}/share/openmpi/mca-btl-openib-device-params.ini
%endif
%if 0%{?el7}
%{_libdir}/%{name}/share/pmix/
%endif

%files devel
%dir %{_includedir}/%{namearch}
%{_libdir}/%{name}/bin/aggregate_profile.pl
%{_libdir}/%{name}/bin/mpi[cCf]*
%{_libdir}/%{name}/bin/opal_*
%{_libdir}/%{name}/bin/orte[cCf]*
%if %{with ucx}
%{_libdir}/%{name}/bin/osh[cCf]*
%endif
%{_libdir}/%{name}/bin/profile2mat.pl
%if %{with ucx}
%{_libdir}/%{name}/bin/shmem[cCf]*
%endif
%{_includedir}/%{namearch}/*
%{_fmoddir}/%{name}/
%{_libdir}/%{name}/lib/*.so
%{_libdir}/%{name}/lib/*.mod
%{_libdir}/%{name}/lib/pkgconfig/
%{_libdir}/pkgconfig/*.pc
%{_mandir}/%{namearch}/man1/mpi[cCf]*
%if %{with ucx}
%{_mandir}/%{namearch}/man1/osh[cCf]*
%{_mandir}/%{namearch}/man1/shmem[cCf]*
%endif
%{_mandir}/%{namearch}/man1/opal_*
%{_mandir}/%{namearch}/man3/*
%{_libdir}/%{name}/share/openmpi/openmpi-valgrind.supp
%{_libdir}/%{name}/share/openmpi/*-wrapper-data.txt
%{macrosdir}/macros.%{namearch}

%files java
%{_libdir}/%{name}/lib/mpi.jar

%files java-devel
%{_libdir}/%{name}/bin/mpijavac
%{_libdir}/%{name}/bin/mpijavac.pl
# Currently this only contaings openmpi/javadoc
%{_libdir}/%{name}/share/doc/
%{_mandir}/%{namearch}/man1/mpijavac.1.gz

%if %{with python2}
%files -n python2-openmpi
%dir %{python2_sitearch}/%{name}
%{python2_sitearch}/openmpi.pth
%endif

%files -n python%{python3_pkgversion}-openmpi
%dir %{python3_sitearch}/%{name}
%{python3_sitearch}/openmpi.pth


%changelog
* Wed Jan 05 2022 Thomas Crain <thcrain@microsoft.com> - 4.0.3x-5
- Rename java-headless dependency to java
- License verified

* Mon May 17 2021 Thomas Crain <thcrain@microsoft.com> - 4.0.3x-4
- Change JDK dir to match JDK version

* Wed Jan 20 2021 Joe Schmitt <joschmit@microsoft.com> - 4.0.3x-3
- Remove python(abi) requirement

* Fri Jan 08 2021 Ruying Chen <v-ruyche@microsoft.com> - 4.0.3x-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Build without ucx support
- Build without python2 support
- Remove hwloc-gui build requirement
- Specify jdk-dir

* Thu Mar 05 2020 Orion Poplawski <orion@nwra.com> - 4.0.3x-1
- Update to 4.0.3 (use x to avoid epoch)

* Sun Mar 01 2020 Orion Poplawski <orion@nwra.com> - 4.0.3rc4-1
- Update to 4.0.3rc4

* Sat Feb 1 2020 Orion Poplawski <orion@nwra.com> - 4.0.3rc3-1
- Update to 4.0.3rc3

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Dec 10 2019 Dominik Mierzejewski <rpm@greysector.net> - 4.0.2-4
- disable rdma on ARM 32-bit (bz#1780584)

* Sun Nov 24 2019 Orion Poplawski <orion@nwra.com> - 4.0.2-3
- Add upstream fix for error in calculating aggregators in 32bit mode

* Fri Nov 15 2019 Orion Poplawski <orion@nwra.com> - 4.0.2-2
- Drop python2 for Fedora 32+ (bz#1773125)

* Mon Oct 7 2019 Philip Kovacs <pkfed@fedoraproject.org> - 4.0.2-1
- Update to 4.0.2

* Sat Sep 14 2019 Orion Poplawski <orion@nwra.com> - 4.0.2-0.4.rc2
- Update to 4.0.2rc2
- Re-enable C++ bindings on power64

* Fri Sep 6 2019 Philip Kovacs <pkfed@fedoraproject.org> - 4.0.2-0.3.rc1
- Rebuild for annobin update to correct aarch64 build (bug #1748529)

* Fri Aug 30 2019 Philip Kovacs <pkfed@fedoraproject.org> - 4.0.2-0.2.rc1
- Apply upstream PR 6946 to avoid linking to __mmap
- Add build deps to run upstream autogen.pl
- Remove embedded tabs in the spec

* Thu Aug 29 2019 Philip Kovacs <pkfed@fedoraproject.org> - 4.0.2-0.1.rc1
- Update to 4.0.2rc1
- Closes bug #1746564

* Thu Aug 29 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 4.0.1-11
- Fix MANPATH so normal modules can still be loaded (#1564899)

* Sun Aug 25 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 4.0.1-10
- Rebuilt for hwloc-2.0

* Sun Aug 18 2019 Miro Hrončok <mhroncok@redhat.com> - 4.0.1-9
- Rebuilt for Python 3.8

* Fri Aug 9 2019 Philip Kovacs <pkfed@fedoraproject.org> - 4.0.1-8
- Remove torque support (torque retired: bug #1676147)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jun 21 2019 Orion Poplawski <orion@nwra.com> - 4.0.1-6
- Rebuild for libfabric 1.8
- Re-enable UCX, hopefully issue fixed in 1.5.2

* Mon May 27 2019 Orion Poplawski <orion@nwra.com> - 4.0.1-5
- Drop UCX support for now

* Wed May 15 2019 Orion Poplawski <orion@nwra.com> - 4.0.1-4
- Add upstream patch OSC/UCX: use correct rkey for atomic_fadd in rget/rput

* Wed May 15 2019 Orion Poplawski <orion@nwra.com> - 4.0.1-3
- Add upstream patch to fix issue with UCX usage in BTL/UCT

* Tue May  7 2019 Orion Poplawski <orion@nwra.com> - 4.0.1-2
- Add a guard for python3 version (#1705296)
- Add requires on python(abi) to python packages

* Sun Apr 28 2019 Orion Poplawski <orion@nwra.com> - 4.0.1-1
- Update to 4.0.1

* Sun Apr 28 2019 Orion Poplawski <orion@nwra.com> - 3.1.4-1
- Update to 3.1.4

* Mon Apr 22 2019 Björn Esser <besser82@fedoraproject.org> - 3.1.3-5
- rebuilt(opensm)

* Wed Apr 17 2019 Christoph Junghans <junghans@votca.org> - 3.1.3-4
- Rebuild to fix ibosmcomp linkage

* Sat Mar  2 2019 Orion Poplawski <orion@nwra.com> - 3.1.3-3
- Enable valgrind on s390x
- Cleanup arch conditionals

* Tue Feb 19 2019 Orion Poplawski <orion@nwra.com> - 3.1.3-2
- Enable PVFS2/OrangeFS MPI-IO support (bug #1655010)

* Wed Feb 13 2019 Orion Poplawski <orion@nwra.com> - 3.1.3-1
- Update to 3.1.3
- Drop ppc64le patch fixed upstream
- Use external libevent and pmix, except on EL7
- Fix EPEL7 builds

* Sat Feb 2 2019 Orion Poplawski <orion@nwra.com> - 2.1.6-1
- Update to 2.1.6

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.6-0.2.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Nov 28 2018 Orion Poplawski <orion@nwra.com> - 2.1.6-0.1.rc1
- Update to 2.1.6rc1

* Thu Oct 11 2018 Orion Poplawski <orion@nwra.com> - 2.1.5-1
- Update to 2.1.5

* Sun Jul 22 2018 Orion Poplawski <orion@nwra.com> - 2.1.1-14
- Add BR gcc-c++ (fix FTBFS bug #1605323)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 2.1.1-12
- Rebuilt for Python 3.7

* Thu May 10 2018 Troy Dawson <tdawson@redhat.com> - 2.1.1-11
- Build with rdma-core-devel instead of libibcm-devel

* Mon Apr 30 2018 Florian Weimer <fweimer@redhat.com> - 2.1.1-10
- Rebuild with new flags from redhat-rpm-config

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.1.1-9
- Escape macros in %%changelog

* Mon Feb 05 2018 Orion Poplawski <orion@cora.nwra.com> - 2.1.1-8
- Rebuild for rdma-core 16.2

* Wed Jan 31 2018 Christoph Junghans <junghans@votca.org> - 2.1.1-7
- Rebuild for gfortran-8

* Fri Jan 12 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2.1.1-6
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Wed Aug 23 2017 Adam Williamson <awilliam@redhat.com> - 2.1.1-5
- Disable RDMA support on 32-bit ARM (#1484155)
- Disable hanging opal_fifo test on ppc64le (gh #2526 / #2966)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 19 2017 Orion Poplawski <orion@cora.nwra.com> - 2.1.1-2
- Provide pkgconfig files in the main namespace as well (1471512)

* Fri May 12 2017 Orion Poplawski <orion@cora.nwra.com> - 2.1.1-1
- Update to 2.1.1

* Thu May 4 2017 Orion Poplawski <orion@cora.nwra.com> - 2.1.0-1
- Update to 2.1.0

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 2 2017 Orion Poplawski <orion@cora.nwra.com> - 2.0.2-1
- Update to 2.0.2

* Sat Jan 28 2017 Björn Esser <besser82@fedoraproject.org> - 2.0.1-7
- Rebuilt for GCC-7

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 2.0.1-6
- Rebuild for Python 3.6

* Wed Nov 2 2016 Orion Poplawski <orion@cora.nwra.com> - 2.0.1-5
- Split python support into sub-packages (bug #1391157)

* Thu Oct 27 2016 Dan Horák <dan[at]danny.cz> - 2.0.1-4
- Temporarily disable C++ bindings on ppc64/ppc64le (#1388561)

* Mon Oct 24 2016 Orion Poplawski <orion@cora.nwra.com> - 2.0.1-3
- Fix License tag format
- Use /usr/share/modulefiles for modulefile install location

* Mon Oct 24 2016 Orion Poplawski <orion@cora.nwra.com> - 2.0.1-2
- Add upstream patch for thread wait issue with mpi4py

* Fri Oct 21 2016 Orion Poplawski <orion@cora.nwra.com> - 2.0.1-1
- Update to 2.0.1

* Thu Oct 20 2016 Orion Poplawski <orion@cora.nwra.com> - 1.10.4-4
- Support s390(x) (bug #1358701)

* Thu Oct 20 2016 Orion Poplawski <orion@cora.nwra.com> - 1.10.4-3
- Enable psm/psm2 support on x86_64 (bug #1263655)

* Wed Oct 19 2016 Orion Poplawski <orion@cora.nwra.com> - 1.10.4-2
- Enable MPI_THREAD_MULTIPLE support (bug #1369989)

* Wed Oct 19 2016 Orion Poplawski <orion@cora.nwra.com> - 1.10.4-1
- Update to 1.10.4

* Thu Sep 15 2016 Orion Poplawski <orion@cora.nwra.com> - 1.10.3-3
- Rebuild for papi 5.5.0

* Fri Jun 24 2016 Orion Poplawski <orion@cora.nwra.com> - 1.10.3-2
- Use bundled libevent, system version causes issues (bug #1235044)

* Wed Jun 15 2016 Orion Poplawski <orion@cora.nwra.com> - 1.10.3-1
- Update to 1.10.3
- New javadoc location

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 26 2016 Orion Poplawski <orion@cora.nwra.com> - 1.10.2-2
- Rebuild for papi 5.4.3

* Thu Jan 21 2016 Orion Poplawski <orion@cora.nwra.com> - 1.10.2-1
- Update to 1.10.2
- Drop upsream nbc_copy patch

* Tue Nov 10 2015 Orion Poplawski <orion@cora.nwra.com> - 1.10.1-3
- Add upstream patch to fix zero size message

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Nov 5 2015 Orion Poplawski <orion@cora.nwra.com> - 1.10.1-1
- Update to 1.10.1
- Require environment(modules)
- Fixup fortran module install (bug #1154982)

* Tue Oct 6 2015 Orion Poplawski <orion@cora.nwra.com> - 1.10.0-3
- Do not set CFLAGS in %%_openmpi_load

* Wed Sep 16 2015 Orion Poplawski <orion@cora.nwra.com> - 1.10.0-2
- Add patch to add needed opal/util/argv.h includes

* Tue Sep 15 2015 Orion Poplawski <orion@cora.nwra.com> - 1.10.0-1
- Update to 1.10.0

* Thu Aug 27 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.8.8-5
- Use .pth files to set the python path (https://fedorahosted.org/fpc/ticket/563)

* Mon Aug 24 2015 Orion Poplawski <orion@cora.nwra.com> 1.8.8-4
- Disable valgrind only on s390

* Mon Aug 17 2015 Orion Poplawski <orion@cora.nwra.com> 1.8.8-3
- Do not filter libvt* provides as some dependencies link to it

* Mon Aug 10 2015 Sandro Mani <manisandro@gmail.com> - 1.8.8-2
- Require, BuildRequire: rpm-mpi-hooks

* Mon Aug 10 2015 Orion Poplawski <orion@cora.nwra.com> 1.8.8-1
- Update to 1.8.8
- Drop atomic patch applied upstream

* Wed Jul 15 2015 Orion Poplawski <orion@cora.nwra.com> 1.8.7-1
- Update to 1.8.7

* Tue Jun 23 2015 Orion Poplawski <orion@cora.nwra.com> 1.8.6-1
- Update to 1.8.6

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 5 2015 Orion Poplawski <orion@cora.nwra.com> 1.8.5-1
- Update to 1.8.5

* Fri May 1 2015 Orion Poplawski <orion@cora.nwra.com> 1.8.5-0.2.rc3
- Update to 1.8.5rc3

* Sun Apr 5 2015 Orion Poplawski <orion@cora.nwra.com> 1.8.5-0.1.rc1
- Update to 1.8.5rc1

* Mon Mar 30 2015 Orion Poplawski <orion@cora.nwra.com> 1.8.4-7.20150324gitg9ad2aa8
- Add upstream patch to fix race/hang on 32bit machines

* Fri Mar 27 2015 Orion Poplawski <orion@cora.nwra.com> 1.8.4-6.20150324gitg9ad2aa8
- Update to latest 1.8.4 snapshot
- Add upstream patch to fix atomics on 32bit

* Mon Mar 23 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.8.4-5.20150228gitgd83fb30
- Rebuild for fortran update (#1204420)

* Mon Mar 16 2015 Orion Poplawski <orion@cora.nwra.com> 1.8.4-4.99.20150228gitgd83fb30
- Own and ship pkgconfig files, set PKG_CONFIG_PATH in modulefile (bug #1113626)
- Drop old configure settings

* Wed Mar 4 2015 Orion Poplawski <orion@cora.nwra.com> 1.8.4-3.99.20150228gitgd83fb30
- Update to 1.8.4.99 snapshot

* Fri Feb 13 2015 Orion Poplawski <orion@cora.nwra.com> 1.8.4-2
- Fix MPI_FORTRAN_MOD_DIR (bug #1154982)

* Tue Dec 23 2014 Orion Poplawski <orion@cora.nwra.com> 1.8.4-1
- Update to 1.8.4

* Mon Nov 17 2014 Orion Poplawski <orion@cora.nwra.com> 1.8.3-3
- Rebuild for papi soname change

* Fri Oct 3 2014 Orion Poplawski <orion@cora.nwra.com> 1.8.3-2
- Fix typo in oshmem library name

* Sat Sep 27 2014 Orion Poplawski <orion@cora.nwra.com> 1.8.3-1
- Update to 1.8.3

* Tue Sep 16 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.8.2-2
- ppc64le now has valgrind

* Tue Aug 26 2014 Orion Poplawski <orion@cora.nwra.com> 1.8.2-1
- Update to 1.8.2

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Aug  6 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.8.1-6
- Rebuild (papi)

* Mon Aug  4 2014 Dan Horák <dan[at]danny.cz> 1.8.1-5
- no valgrind on ppc64le yet

* Sat Aug  2 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.8.1-4
- aarch64 now has valgrind

* Thu Jul 17 2014 Orion Poplawski <orion@cora.nwra.com> 1.8.1-3
- Add patch to prevent shmem wrappers from adding extra libs

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 23 2014 Orion Poplawski <orion@cora.nwra.com> 1.8.1-1
- Update to 1.8.1, fixes bug #1089044

* Tue Apr 1 2014 Orion Poplawski <orion@cora.nwra.com> 1.8-1
- Update to 1.8

* Tue Mar 25 2014 Orion Poplawski <orion@cora.nwra.com> 1.7.5-2
- Update provides filter

* Mon Mar 24 2014 Orion Poplawski <orion@cora.nwra.com> 1.7.5-1
- Update to 1.7.5

* Fri Feb 21 2014 Orion Poplawski <orion@cora.nwra.com> - 1.7.4-3
- Require java-headless

* Sat Feb  8 2014 Ville Skyttä <ville.skytta@iki.fi> - 1.7.4-2
- Install macros to %%{_rpmconfdir}/macros.d where available.

* Wed Feb 5 2014 Orion Poplawski <orion@cora.nwra.com> 1.7.4-1
- Update to 1.7.4
- Drop format patch fixed upstream
- Build against system libevent
- Build Java mpi bindings, ship in -java sub-package
- Add requires openssh-clients

* Tue Jan 28 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.7.3-5
- Drop mode/modeflag. mode no longer used, modeflag obsolete as set in CFLAGS
- Use distro LDFLAGS for hardened build
- Drop armv5tel options
- General spec cleanups

* Thu Jan 16 2014 Orion Poplawski <orion@cora.nwra.com> 1.7.3-4
- Rebuild with papi 5.3.0

* Wed Dec  4 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.7.3-3
- valgrind not currently supported on aarch64

* Tue Dec 3 2013 Orion Poplawski <orion@cora.nwra.com> 1.7.3-2
- Fix compilation with -Werror=format-security (bug #1037231)

* Sun Oct 20 2013 Orion Poplawski <orion@cora.nwra.com> 1.7.3-1
- Update to 1.7.3
- Upstream no longer ships license incompatible files

* Fri Aug 16 2013 Orion Poplawski <orion@cora.nwra.com> 1.7.2-7
- Move orte* compiler wrappers to devel sub-package (bug #997330)

* Thu Aug 08 2013 Dennis Gilmore <dennis@ausil.us> - 1.7.2-6
- rebuild for papi soname bump bz#995092

* Sat Aug 03 2013 Petr Pisar <ppisar@redhat.com> - 1.7.2-5
- Perl 5.18 rebuild

* Fri Jul 26 2013 Orion Poplawski <orion@cora.nwra.com> 1.7.2-4
- Fix build issue with _cc_name_suffix (bug #986664)

* Mon Jul 22 2013 Deji Akingunola <dakingun@gmail.com> - 1.7.2-3
- Rebuild for papi's shared lib fix

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.7.2-2
- Perl 5.18 rebuild

* Thu Jun 27 2013 Orion Poplawski <orion@cora.nwra.com> 1.7.2-1
- Update to 1.7.2

* Wed Apr 17 2013 Orion Poplawski <orion@cora.nwra.com> 1.7.1-1
- Update to 1.7.1
- Add BR on hwloc
- Add BR on papi-devel

* Tue Apr 16 2013 Orion Poplawski <orion@cora.nwra.com> 1.7-1
- Update to 1.7
- Rebase patch to handle removed components
- Drop esmtp - no longer used

* Sat Feb 23 2013 Orion Poplawski <orion@cora.nwra.com> 1.6.4-2
- Exclude libopen-trace.* from requires

* Fri Feb 22 2013 Orion Poplawski <orion@cora.nwra.com> 1.6.4-1
- Update to 1.6.4
- Drop f90sover and arm-atomics patch fixed upstream

* Mon Jan 28 2013 Orion Poplawski <orion@cora.nwra.com> 1.6.3-7
- Make __requires_exclude more specific so we don't exclude needed libs
  (bug #905263)

* Sun Nov 18 2012 Peter Robinson <pbrobinson@fedoraproject.org> 1.6.3-6
- Update atomics patch for ARM (thanks to Jon Masters)

* Sun Nov 11 2012 Peter Robinson <pbrobinson@fedoraproject.org> 1.6.3-5
- Atomics patch to fix building on ARM (thanks to Jon Masters)

* Mon Nov 5 2012 Orion Poplawski <orion@cora.nwra.com> 1.6.3-4
- Add patch to fix libmpi_f90.so version
- Add patch to link tests with system libltdl
- Run make check

* Fri Nov 2 2012 Orion Poplawski <orion@cora.nwra.com> 1.6.3-3
- Set enable-opal-multi-threads for IB support

* Thu Nov 1 2012 Orion Poplawski <orion@cora.nwra.com> 1.6.3-2
- Update rpm macros to use the new module location

* Wed Oct 31 2012 Orion Poplawski <orion@cora.nwra.com> 1.6.3-1
- Update to 1.6.3

* Sat Oct 13 2012 Orion Poplawski <orion@cora.nwra.com> 1.6.2-1
- Update to 1.6.2
- Add BR torque-devel to enable torque support
- Drop old module file location (bug #838467)

* Thu Sep 13 2012 Orion Poplawski <orion@cora.nwra.com> 1.6.1-2
- Drop adding -fPIC, no longer needed
- Set --disable-silent-rules for more verbose build logs
- Don't add opt_*flags to the wrappers
- Only use $RPM_OPT_FLAGS if not using the opt_*flags

* Thu Aug 23 2012 Orion Poplawski <orion@cora.nwra.com> 1.6.1-1
- Update to 1.6.1
- Drop hostfile patch applied upstream

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 15 2012 Orion Poplawski <orion@cora.nwra.com> 1.6-2
- Add patch from upstream to fix default hostfile location

* Tue May 15 2012 Orion Poplawski <orion@cora.nwra.com> 1.6-1
- Update to 1.6
- Drop arm patch, appears to be addressed upstream
- Remove extraneous wrapper link libraries (bug 814798)

* Tue Apr  3 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.5.5-1
- Update to 1.5.5

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.4-5.1
- Rebuilt for c++ ABI breakage

* Wed Feb 22 2012 Orion Poplawski <orion@cora.nwra.com> 1.5.4-4.1
- Rebuild with hwloc 1.4

* Wed Feb 15 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.5.4-4
- Rebuild for hwloc soname bump

* Fri Jan 20 2012 Doug Ledford <dledford@redhat.com> - 1.5.4-3
- Move modules file to mpi directory and make it conflict with any other
  mpi module (bug #651074)

* Sun Jan 8 2012 Orion Poplawski <orion@cora.nwra.com> 1.5.4-2
- Rebuild with gcc 4.7 (bug #772443)

* Thu Nov 17 2011 Orion Poplawski <orion@cora.nwra.com> 1.5.4-1
- Update to 1.5.4
- Drop dt-textrel patch fixed upstream
- Fixup handling removed files (bug #722534)
- Uses hwloc instead of plpa
- Exclude private libraries from provides/requires (bug #741104)
- Drop --enable-mpi-threads & --enable-openib-ibcm, no longer recognized

* Sat Jun 18 2011 Peter Robinson <pbrobinson@gmail.com> 1.5-4
- Exclude ARM platforms due to current lack of "atomic primitives" on the platform

* Thu Mar 17 2011 Jay Fenlason <fenlason@redhat.com> 1.5-3
- Add dt-textrel patch to close
  Resolves: bz679489
- Add memchecker and esmtp support
  Resolves: bz647011

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Oct 18 2010 Jay Fenlason <fenlason@redhat.com> 1.5-1
- set MANPATH in openmpi module file
- Upgrade to 1.5
- Workaround for rhbz#617766 appears to no longer be needed for 1.5
- remove pkgconfig files in instal
- Remove orteCC.1 dangling symlink
- Adjust the files entries for share/openmpi/help* and share/openmpi/mca*
- Adjust the files entries for share/openmpi/mpi*
- Add files entry for share/openmpi/orte*.txt

* Sun Sep 05 2010 Dennis Gilmore <dennis@ausil.us> - 1.4.1-7
- disable valgrind support on sparc arches

* Sat Jul 24 2010 David Malcolm <dmalcolm@redhat.com> - 1.4.1-6
- workaround for rhbz#617766

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 1.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Mar 29 2010 Jay Fenlason <fenlason@redhat.com> - 1.4.1-4
- Update to fix licencing and packaging issues:
  Use the system plpa and ltdl librarires rather than the ones in the tarball
  Remove licence incompatible files from the tarball.
- update module.in to prepend-path PYTHONPATH

* Tue Mar 9 2010 Jay Fenlason <fenlason@redhat.com> - 1.4.1-3
- remove the pkgconfig file completely like we did in RHEL.

* Tue Jan 26 2010 Jay Fenlason <fenlason@redhat.com> - 1.4.1-2
- BuildRequires: python

* Tue Jan 26 2010 Jay Fenlason <fenlason@redhat.com> - 1.4.1-1
- New upstream version, which includes the changeset_r22324 patch.
- Correct a typo in the Source0 line in this spec file.

* Fri Jan 15 2010 Doug Ledford <dledford@redhat.com> - 1.4-4
- Fix an issue with usage of _cc_name_suffix that cause a broken define in
  our module file

* Fri Jan 15 2010 Doug Ledford <dledford@redhat.com> - 1.4-3
- Fix pkgconfig file substitution
- Bump version so we are later than the equivalent version from Red Hat
  Enterprise Linux

* Wed Jan 13 2010 Doug Ledford <dledford@redhat.com> - 1.4-1
- Update to latest upstream stable version
- Add support for libibcm usage
- Enable sge support via configure options since it's no longer on by default
- Add patch to resolve allreduce issue (bz538199)
- Remove no longer needed patch for Chelsio cards

* Tue Sep 22 2009 Jay Fenlason <fenlason@redhat.com> - 1.3.3-6
- Create and own man* directories for use by dependent packages.

* Wed Sep 16 2009 Jay Fenlason <fenlason@redhat.com> - 1.3.3-5
- Move the module file from %%{_datadir}/Modules/modulefiles/%%{namearch} to
  %%{_sysconfdir}/modulefiles/%%{namearch} where it belongs.
- Have the -devel subpackage own the man1 and man7 directories for completeness.
- Add a blank line before the clean section.
- Remove --enable-mpirun-prefix-by-default from configure.

* Wed Sep 9 2009 Jay Fenlason <fenlason@redhat.com> - 1.3.3-4
- Modify packaging to conform to
  https://fedoraproject.org/wiki/PackagingDrafts/MPI (bz521334).
- remove --with-ft=cr from configure, as it was apparently causing problems
  for some people.
- Add librdmacm-devel and librdmacm to BuildRequires (related bz515565).
- Add openmpi-bz515567.patch to add support for the latest Chelsio device IDs
  (related bz515567).
- Add exclude-arch (s390 s390x) because we don't have required -devel packages
  there.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 21 2009 Doug Ledford <dledford@redhat.com> - 1.3.3-2
- Add MPI_BIN and MPI_LIB to the modules file (related bz511099)

* Tue Jul 21 2009 Doug Ledford <dledford@redhat.com> - 1.3.3-1
- Make sure all created dirs are owned (bz474677)
- Fix loading of pkgconfig file (bz476844)
- Resolve file conflict between us and libotf (bz496131)
- Resolve dangling symlinks issue (bz496909)
- Resolve unexpanded %%{mode} issues (bz496911)
- Restore -devel subpackage (bz499851)
- Make getting the default openmpi devel environment easier (bz504357)
- Make the -devel package pull in the base package (bz459458)
- Make it easier to use alternative compilers to build package (bz246484)

* Sat Jul 18 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.3.1-4
- Add Provides: openmpi-devel to fix other package builds in rawhide.

* Fri May 08 2009 Lubomir Rintel <lkundrak@v3.sk> - 1.3.1-3
- Treat i586 the same way as i386

* Wed Apr 22 2009 Doug Ledford <dledford@redhat.com> - 1.3.1-2
- fixed broken update
- Resolves: bz496909, bz496131, bz496911

* Tue Apr 14 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1.3.1-1
- update to 1.3.1, cleanup alternatives, spec, make new vt subpackage

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.2.4-2
- Autorebuild for GCC 4.3

* Wed Oct 17 2007 Doug Ledford <dledford@redhat.com> - 1.2.4-1
- Update to 1.2.4 upstream version
- Build against libtorque
- Pass a valid mode to open
- Resolves: bz189441, bz265141

* Tue Aug 28 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 1.2.3-5
- Rebuild for selinux ppc32 issue.

* Mon Jul 16 2007 Doug Ledford <dledford@redhat.com> - 1.2.3-4
- Fix a directory permission problem on the base openmpi directories

* Thu Jul 12 2007 Florian La Roche <laroche@redhat.com> - 1.2.3-3
- requires alternatives for various sub-rpms

* Mon Jul 02 2007 Doug Ledford <dledford@redhat.com> - 1.2.3-2
- Fix dangling symlink issue caused by a bad macro usage
- Resolves: bz246450

* Wed Jun 27 2007 Doug Ledford <dledford@redhat.com> - 1.2.3-1
- Update to latest upstream version
- Fix file ownership on -libs package
- Take a swing at solving the multi-install compatibility issues

* Mon Feb 19 2007 Doug Ledford <dledford@redhat.com> - 1.1.1-7
- Bump version to be at least as high as the RHEL4U5 openmpi
- Integrate fixes made in RHEL4 openmpi into RHEL5 (fix a multilib conflict
  for the openmpi.module file by moving from _datadir to _libdir, make sure
  all sed replacements have the g flag so they replace all instances of
  the marker per line, not just the first, and add a %%defattr tag to the
  files section of the -libs package to avoid install errors about
  brewbuilder not being a user or group)
- Resolves: bz229298

* Wed Jan 17 2007 Doug Ledford <dledford@redhat.com> - 1.1.1-5
- Remove the FORTIFY_SOURCE and stack protect options
- Related: bz213075

* Fri Oct 20 2006 Doug Ledford <dledford@redhat.com> - 1.1.1-4
- Bump and build against the final openib-1.1 package

* Wed Oct 18 2006 Doug Ledford <dledford@redhat.com> - 1.1.1-3
- Fix an snprintf length bug in opal/util/cmd_line.c
- RESOLVES: rhbz#210714

* Wed Oct 18 2006 Doug Ledford <dledford@redhat.com> - 1.1.1-2
- Bump and build against openib-1.1-0.pre1.1 instead of 1.0

* Tue Oct 17 2006 Doug Ledford <dledford@redhat.com> - 1.1.1-1
- Update to upstream 1.1.1 version

* Fri Oct 13 2006 Doug Ledford <dledford@redhat.com> - 1.1-7
- ia64 can't take -m64 on the gcc command line, so don't set it there

* Wed Oct 11 2006 Doug Ledford <dledford@redhat.com> - 1.1-6
- Bump rev to match fc6 rev
- Fixup some issue with alternatives support
- Split the 32bit and 64bit libs ld.so.conf.d files into two files so
  multilib or single lib installs both work properly
- Put libs into their own package
- Add symlinks to /usr/share/openmpi/bin%%{mode} so that opal_wrapper-%%{mode}
  can be called even if it isn't the currently selected default method in
  the alternatives setup (opal_wrapper needs to be called by mpicc, mpic++,
  etc. in order to determine compile mode from argv[0]).

* Sun Aug 27 2006 Doug Ledford <dledford@redhat.com> - 1.1-4
- Make sure the post/preun scripts only add/remove alternatives on initial
  install and final removal, otherwise don't touch.

* Fri Aug 25 2006 Doug Ledford <dledford@redhat.com> - 1.1-3
- Don't ghost the mpi.conf file as that means it will get removed when
  you remove 1 out of a number of alternatives based packages
- Put the .mod file in -devel

* Mon Aug  7 2006 Doug Ledford <dledford@redhat.com> - 1.1-2
- Various lint cleanups
- Switch to using the standard alternatives mechanism instead of a home
  grown one

* Wed Aug  2 2006 Doug Ledford <dledford@redhat.com> - 1.1-1
- Upgrade to 1.1
- Build with Infiniband support via openib

* Mon Jun 12 2006 Jason Vas Dias <jvdias@redhat.com> - 1.0.2-1
- Upgrade to 1.0.2

* Wed Feb 15 2006 Jason Vas Dias <jvdias@redhat.com> - 1.0.1-1
- Import into Fedora Core
- Resolve LAM clashes

* Wed Jan 25 2006 Orion Poplawski <orion@cora.nwra.com> - 1.0.1-2
- Use configure options to install includes and libraries
- Add ld.so.conf.d file to find libraries
- Add -fPIC for x86_64

* Tue Jan 24 2006 Orion Poplawski <orion@cora.nwra.com> - 1.0.1-1
- 1.0.1
- Use alternatives

* Sat Nov 19 2005 Ed Hill <ed@eh3.com> - 1.0-2
- fix lam conflicts

* Fri Nov 18 2005 Ed Hill <ed@eh3.com> - 1.0-1
- initial specfile created

