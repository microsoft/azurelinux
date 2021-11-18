Summary:        A SAT solver
Name:           picosat
Version:        965
Release:        13%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            http://fmv.jku.at/picosat/
Source0:        http://fmv.jku.at/picosat/%{name}-%{version}.tar.gz
# Thanks to David Wheeler for the man page.
Source1:        picosat.1
# Man page link for picosat.trace
Source2:        picosat.trace.1
# Man page for picomus
Source3:        picomus.1
# This patch has not been sent upstream.  It is specific to Fedora's build of
# two distinct binaries, one with trace support and one without.
Patch0:         %{name}-trace.patch
BuildRequires:  R-core-devel
BuildRequires:  gcc
BuildRequires:  make
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       bzip2
Requires:       gzip

# Temp: Do not build with x86_64 due to docker build issue
ExclusiveArch:  aarch64

%description
PicoSAT solves the SAT problem, which is the classical NP complete
problem of searching for a satisfying assignment of a propositional
formula in conjunctive normal form (CNF).  PicoSAT can generate proofs
and cores in memory by compressing the proof trace.  It supports the
proof format of TraceCheck.

%package R
Summary:        A SAT solver library for R

%description R
The PicoSAT library, which contains routines that solve the SAT problem.
The library has a simple API which is similar to that of previous
solvers by the same authors.  This version of the library is built for
use with R projects.

%package libs
Summary:        A SAT solver library

%description libs
The PicoSAT library, which contains routines that solve the SAT problem.
The library has a simple API which is similar to that of previous
solvers by the same authors.

%package devel
Summary:        Development files for PicoSAT
Requires:       %{name}-R%{?_isa} = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description devel
Headers and other development files for PicoSAT.

%prep
%autosetup

%build
# The configure script is NOT autoconf-generated and chooses its own CFLAGS,
# so we mimic its effects instead of using it.

# Build the version with R support
sed -e "s/@CC@/gcc/" \
    -e "s|@CFLAGS@|%{optflags} -D_GNU_SOURCE=1 -DNDEBUG -DRCODE -I/usr/lib64/R/include|" \
    -e "s|-Xlinker libpicosat.so|-Xlinker libpicosat.so.0 $RPM_LD_FLAGS -L/usr/lib64/R/lib |" \
    -e "s/libpicosat/libpicosat-R/g" \
    -e "s/-lpicosat/-lpicosat-R/g" \
    -e "s/@TARGETS@/libpicosat-R.so/" \
  makefile.in > makefile
%make_build

# Build the version with trace support
sed -e "s/@CC@/gcc/" \
    -e "s|@CFLAGS@|%{optflags} -D_GNU_SOURCE=1 -DNDEBUG -DTRACE|" \
    -e "s|-Xlinker libpicosat.so|-Xlinker libpicosat.so.0 $RPM_LD_FLAGS|" \
    -e "s/libpicosat/libpicosat-trace/g" \
    -e "s/-lpicosat/-lpicosat-trace/g" \
    -e "s/@TARGETS@/libpicosat-trace.so picosat picomus/" \
  makefile.in > makefile
%make_build
mv picosat picosat.trace

# Build the fast version.
# Note that picomus needs trace support, so we don't rebuild it.
rm -f *.o *.s config.h
sed -e "s/@CC@/gcc/" \
    -e "s|@CFLAGS@|%{optflags} -D_GNU_SOURCE=1 -DNDEBUG|" \
    -e "s|-Xlinker libpicosat.so|-Xlinker libpicosat.so.0 $RPM_LD_FLAGS|" \
    -e "s/@TARGETS@/libpicosat.so picosat picomcs picogcnf/" \
  makefile.in > makefile
%make_build

%install
# Install the header file
mkdir -p  %{buildroot}%{_includedir}
cp -p picosat.h  %{buildroot}%{_includedir}

# Install the libraries
mkdir -p  %{buildroot}%{_libdir}
install -m 0755 -p libpicosat-R.so \
   %{buildroot}%{_libdir}/libpicosat-R.so.0.0.%{version}
ln -s libpicosat-R.so.0.0.%{version}  %{buildroot}%{_libdir}/libpicosat-R.so.0
ln -s libpicosat-R.so.0  %{buildroot}%{_libdir}/libpicosat-R.so
install -m 0755 -p libpicosat-trace.so \
   %{buildroot}%{_libdir}/libpicosat-trace.so.0.0.%{version}
ln -s libpicosat-trace.so.0.0.%{version}  %{buildroot}%{_libdir}/libpicosat-trace.so.0
ln -s libpicosat-trace.so.0  %{buildroot}%{_libdir}/libpicosat-trace.so
install -m 0755 -p libpicosat.so \
   %{buildroot}%{_libdir}/libpicosat.so.0.0.%{version}
ln -s libpicosat.so.0.0.%{version}  %{buildroot}%{_libdir}/libpicosat.so.0
ln -s libpicosat.so.0  %{buildroot}%{_libdir}/libpicosat.so

# Install the binaries
mkdir -p  %{buildroot}%{_bindir}
install -m 0755 -p picosat picosat.trace picomus picomcs picogcnf \
   %{buildroot}%{_bindir}

# Install the man pages
mkdir -p  %{buildroot}%{_mandir}/man1
cp -p %{SOURCE1} %{SOURCE2} %{SOURCE3}  %{buildroot}%{_mandir}/man1

%ldconfig_scriptlets R
%ldconfig_scriptlets libs

%files
%{_bindir}/pico*
%{_mandir}/man1/picosat*
%{_mandir}/man1/picomus*

%files R
%doc NEWS
%license LICENSE
%{_libdir}/libpicosat-R.so.*

%files libs
%doc NEWS
%license LICENSE
%{_libdir}/libpicosat-trace.so.*
%{_libdir}/libpicosat.so.*

%files devel
%{_includedir}/picosat.h
%{_libdir}/libpicosat-R.so
%{_libdir}/libpicosat-trace.so
%{_libdir}/libpicosat.so

%changelog
* Mon Jun 21 2021 Rachel Menge <rachelmenge@microsoft.com> - 965-13
- Initial CBL-Mariner import from Fedora 34 (license: MIT)
- License verified

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 965-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 965-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 965-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 965-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 965-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 965-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 965-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 965-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 965-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 965-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 965-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 13 2016 Jerry James <loganjerry@gmail.com> - 965-1
- New upstream release
- Drop -proof-access patch now that csisat has been retired
- Add a library built for R support

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 960-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Nov  7 2014 Jerry James <loganjerry@gmail.com> - 960-1
- New upstream release
- Drop upstreamed -alias patch
- Fix license handling

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 957-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 957-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jul 31 2013 Jerry James <loganjerry@gmail.com> - 957-1
- New upstream release
- Remove comment that was being pulled into postun

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 951-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Aug 20 2012 Jerry James <loganjerry@gmail.com> - 951-1
- New upstream release

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 936-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan  6 2012 Jerry James <loganjerry@gmail.com> - 936-3
- Rebuild for GCC 4.7
- Minor spec file cleanups

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 936-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 27 2011 Jerry James <loganjerry@gmail.com> - 936-1
- Update to version 936.
- Drop picosat-sharedlib.patch, incorporated upstream.
- Add picosat-trace.patch, to support separate tracing and nontracing libs.

* Tue Jan 19 2010 Jerry James <loganjerry@gmail.com> - 913-2
- Spec file cleanups from review
- Man page courtesy of David Wheeler

* Wed Sep  2 2009 Jerry James <loganjerry@gmail.com> - 913-1
- Initial RPM
