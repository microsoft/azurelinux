Vendor:         Microsoft Corporation
Distribution:   Mariner
#%%global rc_ver 6
%global libomp_srcdir openmp-%{version}%{?rc_ver:rc%{rc_ver}}.src


%ifarch ppc64le
%global libomp_arch ppc64
%else
%global libomp_arch %{_arch}
%endif

Name: libomp
Version: 10.0.1
Release: 4%{?dist}
Summary: OpenMP runtime for clang

License: NCSA
URL: http://openmp.llvm.org	
%if 0%{?rc_ver:1}
Source0: https://prereleases.llvm.org/%{version}/rc%{rc_ver}/%{libomp_srcdir}.tar.xz
Source3: https://prereleases.llvm.org/%{version}/rc%{rc_ver}/%{libomp_srcdir}.tar.xz.sig
%else
Source0: https://github.com/llvm/llvm-project/releases/download/llvmorg-%{version}/%{libomp_srcdir}.tar.xz
Source3: https://github.com/llvm/llvm-project/releases/download/llvmorg-%{version}/%{libomp_srcdir}.tar.xz.sig
%endif
Source1: run-lit-tests
Source2: lit.fedora.cfg.py
Source4: https://prereleases.llvm.org/%{version}/hans-gpg-key.asc

Patch0: 0001-CMake-Make-LIBOMP_HEADERS_INSTALL_PATH-a-cache-varia.patch
Patch1: 99b03c1c18.patch

BuildRequires: cmake
BuildRequires: elfutils-libelf-devel
BuildRequires: perl
BuildRequires: perl-Data-Dumper
BuildRequires: perl-Encode
BuildRequires: libffi-devel

Requires: elfutils-libelf%{?isa}

# libomp does not support s390x.
ExcludeArch: s390x

%description
OpenMP runtime for clang.

%package devel
Summary: OpenMP header files
Requires: clang-devel%{?isa} = %{version}

%description devel
OpenMP header files.

%package test
Summary: OpenMP regression tests
Requires: %{name}%{?isa} = %{version}
Requires: %{name}-devel%{?isa} = %{version}
Requires: clang
Requires: llvm
Requires: gcc
Requires: gcc-c++
Requires: python3-lit

%description test
OpenMP regression tests

%prep
%autosetup -n %{libomp_srcdir} -p1

%build
mkdir -p _build
cd _build

%cmake .. \
	-DLIBOMP_INSTALL_ALIASES=OFF \
	-DLIBOMP_HEADERS_INSTALL_PATH:PATH=%{_libdir}/clang/%{version}/include \
	-DOPENMP_LIBDIR_SUFFIX= \

%make_build


%install
%make_install -C _build

# Test package setup
%global libomp_srcdir %{_datadir}/libomp/src/
%global libomp_testdir %{libomp_srcdir}/runtime/test/
%global lit_cfg %{libomp_testdir}/%{_arch}.site.cfg.py
%global lit_fedora_cfg %{_datadir}/libomp/lit.fedora.cfg.py

install -d %{buildroot}%{libomp_srcdir}/runtime
cp -R runtime/test  %{buildroot}%{libomp_srcdir}/runtime
cp -R runtime/src  %{buildroot}%{libomp_srcdir}/runtime

# Generate lit config files.  Strip off the last line that initiates the
# test run, so we can customize the configuration.
head -n -1 _build/runtime/test/lit.site.cfg >> %{buildroot}%{lit_cfg}

# Install custom fedora config file
cp %{SOURCE2} %{buildroot}%{lit_fedora_cfg}

# Patch lit config files to load custom fedora config
echo "lit_config.load_config(config, '%{lit_fedora_cfg}')" >> %{buildroot}%{lit_cfg}

# Install test script
install -d %{buildroot}%{_libexecdir}/tests/libomp
install -m 0755 %{SOURCE1} %{buildroot}%{_libexecdir}/tests/libomp

# Remove static libraries with equivalent shared libraries
rm -rf %{buildroot}%{_libdir}/libarcher_static.a


%files
%license LICENSE.txt
%{_libdir}/libomp.so
%{_libdir}/libomptarget.so
%ifnarch %{arm}
%{_libdir}/libarcher.so
%endif
%ifnarch %{arm} %{ix86}
%{_libdir}/libomptarget.rtl.%{libomp_arch}.so
%endif

%files devel
%{_libdir}/clang/%{version}/include/omp.h
%ifnarch %{arm}
%{_libdir}/clang/%{version}/include/omp-tools.h
%{_libdir}/clang/%{version}/include/ompt.h
%endif

%files test
%{_datadir}/libomp
%{_libexecdir}/tests/libomp/

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 10.0.1-4
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Fri May 28 2021 Thomas Crain <thcrain@microsoft.com> - 10.0.1-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Remove libdir suffix of 64 on 64-bit architectures

* Thu Sep 17 2020 sguelton@redhat.com - 10.0.1-2
- rebuilt with gating.yaml update

* Mon Jul 27 2020 sguelton@redhat.com - 10.0.1-1
- 10.0.1

* Fri Apr 3 2020 sguelton@redhat.com - 10.0.0-1
- 10.0.0 final

* Sun Mar 15 2020 sguelton@redhat.com - 10.0.0-0.2.rc4
- 10.0.0 rc4

* Fri Jan 31 2020 sguelton@redhat.com - 10.0.0-0.1.rc1
- 10.0.0 rc1

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 9.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Dec 19 2019 Tom Stellard <tstellar@redhat.com> - 9.0.1-1
- 9.0.1 Release

* Thu Sep 19 2019 Tom Stellard <tstellar@redhat.com> - 9.0.0-1
- 9.0.0 Release

* Thu Aug 22 2019 Tom Stellard <tstellar@redhat.com> - 9.0.0-0.1.rc3
- 9.0.0-rc3 Release

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.0-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Apr 25 2019 Tom Stellard <tstellar@redhat.com> - 8.0.0-2
- Simplify libomp-test package

* Wed Mar 20 2019 sguelton@redhat.com - 8.0.0-1
- 8.0.0 final

* Tue Mar 12 2019 sguelton@redhat.com - 8.0.0-0.3.rc4
- 8.0.0 Release candidate 4

* Mon Feb 11 2019 sguelton@redhat.com - 8.0.0-0.2.rc2
- 8.0.0 Release candidate 2

* Mon Feb 11 2019 sguelton@redhat.com - 8.0.0-0.1.rc1
- 8.0.0 Release candidate 1

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.1-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Dec 17 2018 sguelton@redhat.com - 7.0.1-1
- 7.0.1 Release

* Wed Sep 12 2018 Tom Stellard <tstellar@redhat.com> - 7.0.0-1
- 7.0.1 Release

* Wed Sep 12 2018 Tom Stellard <tstellar@redhat.com> - 7.0.0-0.2.rc3
- 7.0.0-rc3 Release

* Tue Aug 14 2018 Tom Stellard <tstellar@redhat.com> - 7.0.0-0.1.rc1
- 7.0.1-rc1 Release

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 02 2018 Tom Stellard <tstellar@redhat.com> - 6.0.1-2
- Add -threads option to runtest.sh

* Thu Jun 28 2018 Tom Stellard <tstellar@redhat.com> - 6.0.1-1
- 6.0.1 Release

* Fri May 11 2018 Tom Stellard <tstellar@redhat.com> - 6.0.0-0.1.rc1
- 6.0.1-rc1 Release

* Wed Mar 28 2018 Tom Stellard <tstellar@redhat.com> - 6.0.0-3
- Add test package

* Wed Mar 28 2018 Tom Stellard <tstellar@redhat.com> - 6.0.0-2
- Enable libomptarget plugins

* Fri Mar 09 2018 Tom Stellard <tstellar@redhat.com> - 6.0.0-1
- 6.0.0 Release

* Tue Feb 13 2018 Tom Stellard <tstellar@redhat.com> - 6.0.0-0.3.rc2
- 6.0.0-rc2 Release

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.0-0.2.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 25 2018 Tom Stellard <tstellar@redhat.com> - 6.0.0-0.1.rc1
- 6.0.0-rc1 Release

* Thu Dec 21 2017 Tom Stellard <tstellar@redhat.com> - 5.0.1-1
- 5.0.1 Release.

* Mon May 15 2017 Tom Stellard <tstellar@redhat.com> - 5.0.0-1
- Initial version.
