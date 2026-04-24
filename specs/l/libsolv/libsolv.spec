## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 4;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global libname solv

%bcond_without python_bindings
%bcond_without perl_bindings
%bcond_without ruby_bindings
# Creates special prefixed pseudo-packages from appdata metadata
%bcond_without appdata
# Creates special prefixed "group:", "category:" pseudo-packages
%bcond_without comps
%bcond_without conda
# For rich dependencies
%bcond_without complex_deps
%bcond_without helix_repo
%bcond_without suse_repo
%bcond_without debian_repo
%bcond_without arch_repo
%bcond_without apk_repo
# For handling deb + rpm at the same time
%bcond_without multi_semantics
%if %{defined rhel}
%bcond_with zchunk
%else
%bcond_without zchunk
%endif
%bcond_without zstd

%define __cmake_switch(b:) %[%{expand:%%{?with_%{-b*}}} ? "ON" : "OFF"]

Name:           lib%{libname}
Version:        0.7.35
Release:        %autorelease
Summary:        Package dependency solver

# LICENSE.BSD:      BSD-3-Clause text
# other files:      "read LICENSE.BSD"
# src/sha2.c:       BSD-3-Clause
# src/sha2.h:       BSD-3-Clause
## Used at build time but not in any binary package
# cmake/modules/_CMakeParseArguments.cmake:             BSD-3-Clause
# cmake/modules/FindPackageHandleStandardArgs.cmake:    BSD-3-Clause
# cmake/modules/FindRuby.cmake:                         BSD-3-Clause
# package/libsolv.spec.in:  (project's license IF open-source) XOR (MIT IF not in open-source project)
## Not used at build time and not in any binary package
# src/qsort_r.c:    BSD-3-Clause
# win32/LICENSE:    MIT text AND BSD-2-Clause text
# win32/regcomp.c:  BSD-2-Clause
# win32/regexec.c:  BSD-2-Clause
# win32/tre.h:      BSD-2-Clause
# win32/tre-mem.c:  BSD-2-Clause
License:        BSD-3-Clause
SourceLicense:  %{license} AND BSD-2-Clause AND MIT
URL:            https://github.com/openSUSE/libsolv
Source:         %{url}/archive/%{version}/%{name}-%{version}.tar.gz
# Provides: python3dist(solv) in python3-solv
# https://github.com/openSUSE/libsolv/pull/602
# https://bugzilla.redhat.com/show_bug.cgi?id=2252743
Patch:          0001-Python-Provide-dist-info-metadata.patch

BuildRequires:  cmake >= 3.5
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  pkgconfig(rpm)
BuildRequires:  zlib-devel
# -DWITH_LIBXML2=ON
BuildRequires:  libxml2-devel
# -DENABLE_LZMA_COMPRESSION=ON
BuildRequires:  xz-devel
# -DENABLE_BZIP2_COMPRESSION=ON
BuildRequires:  bzip2-devel
%if %{with zchunk} || %{with zstd} || %{with apk}
# -DENABLE_ZSTD_COMPRESSION=ON
BuildRequires:  libzstd-devel
%endif
%if %{with zchunk}
# -DENABLE_ZCHUNK_COMPRESSION=ON
BuildRequires:  pkgconfig(zck)
%endif

%description
A free package dependency solver using a satisfiability algorithm. The
library is based on two major, but independent, blocks:

- Using a dictionary approach to store and retrieve package
  and dependency information.

- Using satisfiability, a well known and researched topic, for
  resolving package dependencies.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       rpm-devel%{?_isa}

%description devel
Development files for %{name}.

%package tools-base
Summary:        Utilities used by libzypp to manage .solv files
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       libsolv-tools:%{_bindir}/repo2solv
Conflicts:      libsolv-tools < %{version}

%description tools-base
This subpackage contains utilities used by libzypp to manage solv files.

%package tools
Summary:        Package dependency solver tools
Requires:       %{name}%{?_isa} = %{version}-%{release}
# repo2solv dependencies. Used as execl()
Requires:       libsolv-tools-base = %{version}-%{release}

%description tools
Package dependency solver tools.

%package demo
Summary:        Applications demoing the %{name} library
Requires:       %{name}%{?_isa} = %{version}-%{release}
# solv dependencies. Used as execlp() and system()
Requires:       /usr/bin/curl
Requires:       /usr/bin/gpg2

%description demo
Applications demoing the %{name} library.

%if %{with perl_bindings}
%package -n perl-%{libname}
Summary:        Perl bindings for the %{name} library
BuildRequires:  swig
BuildRequires:  perl-devel
BuildRequires:  perl-generators
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n perl-%{libname}
Perl bindings for the %{name} library.
%endif

%if %{with ruby_bindings}
%package -n ruby-%{libname}
Summary:        Ruby bindings for the %{name} library
BuildRequires:  swig
BuildRequires:  ruby-devel
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n ruby-%{libname}
Ruby bindings for the %{name} library.
%endif

%if %{with python_bindings}
%package -n python3-%{libname}
Summary:        Python bindings for the %{name} library
%{?python_provide:%python_provide python3-%{libname}}
BuildRequires:  swig
BuildRequires:  python3-devel
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n python3-%{libname}
Python bindings for the %{name} library.

Python 3 version.
%endif

%prep
%autosetup -p1

%build
%cmake -GNinja                                            \
  -DFEDORA=1                                              \
  -DENABLE_RPMDB=ON                                       \
  -DENABLE_RPMDB_BYRPMHEADER=ON                           \
  -DENABLE_RPMDB_LIBRPM=ON                                \
  -DENABLE_RPMPKG_LIBRPM=ON                               \
  -DENABLE_RPMMD=ON                                       \
  -DENABLE_STATIC_BINDINGS=OFF                            \
  -DENABLE_STATIC_TOOLS=OFF                               \
  -DENABLE_COMPS=%{__cmake_switch -b comps}               \
  -DENABLE_APPDATA=%{__cmake_switch -b appdata}           \
  -DUSE_VENDORDIRS=ON                                     \
  -DWITH_LIBXML2=ON                                       \
  -DENABLE_LZMA_COMPRESSION=ON                            \
  -DENABLE_BZIP2_COMPRESSION=ON                           \
  -DENABLE_ZSTD_COMPRESSION=%{__cmake_switch -b zstd}     \
  -DENABLE_ZCHUNK_COMPRESSION=%{__cmake_switch -b zchunk} \
%if %{with zchunk}
  -DWITH_SYSTEM_ZCHUNK=ON                                 \
%endif
  -DENABLE_HELIXREPO=%{__cmake_switch -b helix_repo}      \
  -DENABLE_SUSEREPO=%{__cmake_switch -b suse_repo}        \
  -DENABLE_DEBIAN=%{__cmake_switch -b debian_repo}        \
  -DENABLE_ARCHREPO=%{__cmake_switch -b arch_repo}        \
  -DENABLE_APK=%{__cmake_switch -b apk_repo}              \
  -DMULTI_SEMANTICS=%{__cmake_switch -b multi_semantics}  \
  -DENABLE_COMPLEX_DEPS=%{__cmake_switch -b complex_deps} \
  -DENABLE_CONDA=%{__cmake_switch -b conda}               \
  -DENABLE_PERL=%{__cmake_switch -b perl_bindings}        \
  -DENABLE_RUBY=%{__cmake_switch -b ruby_bindings}        \
  -DENABLE_PYTHON=%{__cmake_switch -b python_bindings}    \
%if %{with python_bindings}
  -DPYTHON_EXECUTABLE=%{python3}                          \
%endif
  %{nil}
%cmake_build

%install
%cmake_install

%if %{with python_bindings}
echo "rpm" > %{buildroot}%{python3_sitearch}/%{libname}-%{version}.dist-info/INSTALLER
%endif

%check
%ctest

# Python smoke test (not tested in %%ctest):
export PYTHONPATH=%{buildroot}%{python3_sitearch}
export LD_LIBRARY_PATH=%{buildroot}%{_libdir}
%python3 -c 'import solv'

%files
%license LICENSE*
%doc NEWS README
%{_libdir}/%{name}.so.*
%{_libdir}/%{name}ext.so.*

%files devel
%{_libdir}/%{name}.so
%{_libdir}/%{name}ext.so
%{_includedir}/%{libname}/
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/pkgconfig/%{name}ext.pc
# Own directory because we don't want to depend on cmake
%dir %{_datadir}/cmake/Modules/
%{_datadir}/cmake/Modules/FindLibSolv.cmake
%{_mandir}/man3/%{name}*.3*

# Some small macro to list tools with mans
%global solv_tool() \
%{_bindir}/%{1}\
%{_mandir}/man1/%{1}.1*

%files tools-base
%solv_tool repo2solv
%solv_tool rpmdb2solv

%files tools
%solv_tool deltainfoxml2solv
%solv_tool dumpsolv
%solv_tool installcheck
%solv_tool mergesolv
%solv_tool repomdxml2solv
%solv_tool rpmmd2solv
%solv_tool rpms2solv
%solv_tool testsolv
%solv_tool updateinfoxml2solv
%if %{with comps}
  %solv_tool comps2solv
%endif
%if %{with appdata}
  %solv_tool appdata2solv
%endif
%if %{with debian_repo}
  %solv_tool deb2solv
%endif
%if %{with arch_repo}
  %solv_tool archpkgs2solv
  %solv_tool archrepo2solv
%endif
%if %{with apk_repo}
  %solv_tool apk2solv
%endif
%if %{with helix_repo}
  %solv_tool helix2solv
%endif
%if %{with suse_repo}
  %solv_tool susetags2solv
%endif
%if %{with conda}
  %{_bindir}/conda2solv
%endif

%files demo
%solv_tool solv

%if %{with perl_bindings}
%files -n perl-%{libname}
%{perl_vendorarch}/%{libname}.pm
%{perl_vendorarch}/%{libname}.so
%endif

%if %{with ruby_bindings}
%files -n ruby-%{libname}
%{ruby_vendorarchdir}/%{libname}.so
%endif

%if %{with python_bindings}
%files -n python3-%{libname}
%{python3_sitearch}/_%{libname}.so
%{python3_sitearch}/%{libname}.py
%{python3_sitearch}/__pycache__/%{libname}.*
%{python3_sitearch}/%{libname}-%{version}.dist-info/
%endif

%changelog
## START: Generated by rpmautospec
* Wed Apr 22 2026 azldev <azurelinux@microsoft.com> - 0.7.35-4
- Latest state for libsolv

* Mon Jan 05 2026 Yaakov Selkowitz <yselkowi@redhat.com> - 0.7.35-3
- Add INSTALLER to Python metadata

* Wed Dec 10 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 0.7.35-2
- Provide Python metadata

* Thu Oct 30 2025 Petr Písař <ppisar@redhat.com> - 0.7.35-1
- Update to 0.7.35

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.7.34-5
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.7.34-4
- Rebuilt for Python 3.14.0rc2 bytecode

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.34-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jul 09 2025 Jitka Plesnikova <jplesnik@redhat.com> - 0.7.34-2
- Perl 5.42 re-rebuild updated packages

* Tue Jul 08 2025 Petr Písař <ppisar@redhat.com> - 0.7.34-1
- Update to 0.7.34

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 0.7.33-2
- Perl 5.42 rebuild

* Wed Jun 04 2025 Petr Písař <ppisar@redhat.com> - 0.7.33-1
- Update to 0.7.33

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 0.7.32-5
- Rebuilt for Python 3.14

* Fri Apr 04 2025 Petr Písař <ppisar@redhat.com> - 0.7.32-2
- Package NEWS file and declare a source license

* Thu Apr 03 2025 Neal Gompa <ngompa@fedoraproject.org> - 0.7.32-1
- Update to 0.7.32

* Mon Feb 17 2025 Petr Písař <ppisar@redhat.com> - 0.7.31-5
- Teach rpmlint

* Mon Feb 17 2025 Petr Písař <ppisar@redhat.com> - 0.7.31-4
- Fix building with GCC 15

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.31-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jan 08 2025 Vít Ondruch <vondruch@redhat.com> - 0.7.31-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_3.4

* Tue Nov 12 2024 Evan Goode <mail@evangoo.de> - 0.7.31-1
- Update to 0.7.31

* Thu Aug 01 2024 Evan Goode <mail@evangoo.de> - 0.7.30-1
- Update to 0.7.30

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.29-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 12 2024 Jitka Plesnikova <jplesnik@redhat.com> - 0.7.29-4
- Perl 5.40 rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.7.29-3
- Rebuilt for Python 3.13

* Fri May 31 2024 Petr Písař <ppisar@redhat.com> - 0.7.29-2
- Stricten dependencies between libsolv subpackages

* Mon May 06 2024 Evan Goode <mail@evangoo.de> - 0.7.29-1
- Update to 0.7.29

* Fri Feb 09 2024 Jan Kolarik <jkolarik@redhat.com> - 0.7.28-1
- Update to 0.7.28

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.27-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.27-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 03 2024 Vít Ondruch <vondruch@redhat.com> - 0.7.27-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_3.3

* Tue Dec 05 2023 Jan Kolarik <jkolarik@redhat.com> - 0.7.27-1
- Update to 0.7.27

* Tue Oct 03 2023 Jan Kolarik <jkolarik@redhat.com> - 0.7.25-1
- Update to 0.7.25

* Mon Aug 28 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 0.7.24-9
- Disable zchunk in RHEL builds

* Fri Jul 21 2023 Neal Gompa <ngompa@fedoraproject.org> - 0.7.24-8
- Backport fix to lower memory usage of updateinfo processing
  (rhbz#2214520)

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.24-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 0.7.24-6
- Perl 5.38 rebuild

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 0.7.24-5
- Rebuilt for Python 3.12

* Wed May 17 2023 Jan Kolarik <jkolarik@redhat.com> - 0.7.24-4
- Rebuild for rpm-4.18.90-4

* Tue May 16 2023 Jan Kolarik <jkolarik@redhat.com> - 0.7.24-3
- Rebuild for rpm-4.18.90

* Mon May 15 2023 Igor Raits <igor.raits@gmail.com> - 0.7.24-2
- Upload sources

* Mon May 15 2023 Igor Raits <igor.raits@gmail.com> - 0.7.24-1
- Update to 0.7.24

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.22-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.7.22-2
- Rebuilt for Python 3.11

* Sun Apr 17 2022 Igor Raits <igor.raits@gmail.com> - 0.7.22-1
- Update to 0.7.22

* Fri Feb 25 2022 Igor Raits <igor.raits@gmail.com> - 0.7.21-1
- Update to 0.7.21

* Thu Jan 27 2022 Vít Ondruch <vondruch@redhat.com> - 0.7.20-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_3.1

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Oct 01 2021 Igor Raits <ignatenkobrain@fedoraproject.org> - 0.7.20-1
- Update to 0.7.20

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun Jul 18 2021 Igor Raits <ignatenkobrain@fedoraproject.org> - 0.7.19-2
- Fix compatibility with Python 3.10

* Sun Jul 18 2021 Igor Raits <ignatenkobrain@fedoraproject.org> - 0.7.19-1
- Update to 0.7.19

* Wed Jun 16 2021 Orion Poplawski <orion@nwra.com> - 0.7.17-5
- Enable conda support

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.7.17-4
- Rebuilt for Python 3.10

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Jan 23 2021 Igor Raits <ignatenkobrain@fedoraproject.org> - 0.7.17-2
- Drop unneeded explicit dependency on RPM

* Thu Jan 21 2021 Igor Raits <ignatenkobrain@fedoraproject.org> - 0.7.17-1
- Update to 0.7.17

* Thu Jan 07 2021 Vít Ondruch <vondruch@redhat.com> - 0.7.15-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_3.0

* Mon Nov 16 2020 Miro Hrončok <miro@hroncok.cz> - 0.7.15-2
- Backport upstream fix for Python 3.10 compatibility

* Mon Oct 19 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 0.7.15-1
- Update to 0.7.15

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.14-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 03 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 0.7.14-4
- Switch to %%cmake_build/%%cmake_install + Drop Python 2 support

* Sat Jun 13 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 0.7.14-3
- Remove unused patch

* Wed Jun 03 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 0.7.14-2
- Raise lowest compatible RPM version

* Wed May 27 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 0.7.14-1
- Update to 0.7.14

* Tue May 26 2020 Miro Hrončok <miro@hroncok.cz> - 0.7.12-4
- Rebuilt for Python 3.9

* Mon May 25 2020 Colin Walters <walters@verbum.org> - 0.7.12-3
- Apply https://github.com/openSUSE/libsolv/pull/386

* Mon May 25 2020 Miro Hrončok <miro@hroncok.cz> - 0.7.12-2
- Rebuilt for Python 3.9

* Tue Apr 21 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 0.7.12-1
- Update to 0.7.12

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 23 2020 Neal Gompa <ngompa13@gmail.com> - 0.7.11-1
- Update to 0.7.11

* Tue Dec 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.7.10-1
- Update to 0.7.10

* Tue Nov 12 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.7.8-1
- Update to 0.7.8

* Sat Oct 19 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.7.7-1
- Update to 0.7.7

* Mon Oct 14 2019 Jaroslav Mracek <jmracek@redhat.com> - 0.7.6-3
- Backport support of POOL_FLAG_WHATPROVIDESWITHDISABLED

* Thu Oct 03 2019 Miro Hrončok <miro@hroncok.cz> - 0.7.6-2
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Fri Aug 30 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.7.6-1
- Update to 0.7.6

* Sun Aug 18 2019 Miro Hrončok <miro@hroncok.cz> - 0.7.5-5
- Rebuilt for Python 3.8

* Sun Aug 04 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.7.5-4
- Fix queries with src.rpm with DynamicBuildRequires

* Sun Aug 04 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.7.5-3
- Drop obsolete conditionals

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jun 12 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.7.5-1
- Update to 0.7.5

* Mon Jun 10 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.7.4-7
- Rebuild for RPM 4.15

* Mon Jun 10 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.7.4-6
- Rebuild for RPM 4.15

* Tue May 21 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.7.4-5
- Fixed build for SWIG 4.0.0 (#1707367)

* Tue Apr 02 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.7.4-4
- Backport patch to fix solver_solve() running multiple times with
  SOLVER_FAVOR

* Mon Apr 01 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.7.4-3
- Revert "Change time stamp to compatible format"

* Mon Apr 01 2019 Jaroslav Mracek <jmracek@redhat.com> - 0.7.4-2
- Change time stamp to compatible format

* Fri Mar 29 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.7.4-1
- Update to 0.7.4

* Tue Feb 26 2019 Pavla Kratochvilova <pkratoch@redhat.com> - 0.7.3-6
- Backport: Add support for modular updateinfo.xml data

* Wed Feb 13 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.7.3-5
- bindings: Add best_solvables/whatmatchessolvable

* Wed Feb 13 2019 Marek Blaha <mblaha@redhat.com> - 0.7.3-4
- Conditionalize %%ldconfig_scriptlets for plain RHEL

* Wed Feb 13 2019 Marek Blaha <mblaha@redhat.com> - 0.7.3-3
- Disable zstd on RHEL

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 30 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.7.3-1
- Update to 0.7.3

* Tue Jan 15 2019 Jaroslav Mracek <jmracek@redhat.com> - 0.7.2-4
- Backport patch from upstream

* Sat Jan 12 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.7.2-3
- remove leftovers from commit

* Sat Jan 12 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.7.2-2
- Fix small security issues

* Mon Dec 10 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.7.2-1
- Update to 0.7.2

* Fri Nov 30 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.7.1-3
- Backport fixes for autouninstall

* Wed Nov 28 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.7.1-2
- remove SCM leftovers

* Wed Oct 31 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.7.1-1
- Update to 0.7.1

* Sun Oct 28 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.7.0-1
- Update to 0.7.0

* Mon Oct 01 2018 Jaroslav Rohel <jrohel@redhat.com> - 0.6.35-4
- Bacport patch: Make sure that targeted updates don't do reinstalls

* Mon Oct 01 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.6.35-3
- disable python2 subpackage

* Thu Aug 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.6.35-2
- commit sources

* Thu Aug 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.6.35-1
- Update to 0.6.35

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.34-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 02 2018 Miro Hrončok <miro@hroncok.cz> - 0.6.34-5
- Rebuilt for Python 3.7

* Mon Jul 02 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.6.34-4
- Rebuilt for Python 3.7

* Thu Jun 28 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.6.34-3
- Backport few fixes and enhancements from upstream

* Tue Jun 19 2018 Miro Hrončok <miro@hroncok.cz> - 0.6.34-2
- Rebuilt for Python 3.7

* Mon Mar 26 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.6.34-1
- Update to 0.6.34

* Wed Feb 28 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.6.33-1
- Update to 0.6.33

* Tue Feb 13 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.6.32-1
- Update to 0.6.32

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.31-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 31 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.6.31-1
- Update to 0.6.31

* Tue Jan 30 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.6.30-10
- Use librpm to access rpm headers

* Tue Jan 30 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.6.30-9
- Use librpm to access DB

* Tue Jan 30 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.6.30-8
- Switch to %%ldconfig_scriptlets

* Mon Jan 29 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.6.30-7
- Disable librpm from accessing DB

* Mon Jan 29 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.6.30-6
- Allow disabling python2 bindings

* Mon Jan 29 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.6.30-5
- Switch to ninja-build

* Mon Jan 29 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.6.30-4
- Update to latest git version

* Mon Nov 20 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.6.30-3
- Update to latest snapshot

* Mon Nov 06 2017 Panu Matilainen <pmatilai@redhat.com> - 0.6.30-2
- Better error message on DB_VERSION_MISMATCH errors

* Tue Oct 24 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.6.30-1
- Update to 0.6.30

* Tue Sep 19 2017 Panu Matilainen <pmatilai@redhat.com> - 0.6.29-2
- Band-aid for DB_VERSION_MISMATCH errors on glibc updates

* Thu Sep 07 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.6.29-1
- Update to 0.6.29

* Fri Aug 11 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.6.28-8
- Rebuilt after RPM update (№ 3)

* Thu Aug 10 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.6.28-7
- Rebuilt for RPM soname bump

* Thu Aug 10 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.6.28-6
- Rebuilt for RPM soname bump

* Thu Aug 03 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.6.28-5
- Add support for REL_WITHOUT

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.28-4
- Rebuilt for
  https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.28-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 21 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.6.28-2
- Backport patch for fixing yumobs

* Sat Jul 01 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.6.28-1
- Update to 0.6.28

* Mon May 29 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.6.27-3
- Backport few fixes for bindings

* Thu May 04 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.6.27-2
- don't set PYTHON3_EXECUTABLE

* Thu May 04 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.6.27-1
- Update to 0.6.27

* Mon Mar 27 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.6.26-9
- Update to latest snapshot

* Mon Mar 27 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.6.26-8
- update to latest snapshot

* Sat Mar 18 2017 Neal Gompa <ngompa13@gmail.com> - 0.6.26-7
- Enable AppData support (#1427171)

* Thu Mar 16 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.6.26-6
- D'oh, finally

* Thu Mar 16 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.6.26-5
- make it build on RPM less than 4.14

* Thu Mar 16 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.6.26-4
- remove unused patch

* Thu Mar 16 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.6.26-3
- Update to latest git; Switch to libxml2

* Mon Mar 06 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.6.26-2
- Use %%{__python3} as PYTHON3_EXECUTABLE

* Wed Feb 15 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.6.26-1
- Update to 0.6.26

* Tue Feb 07 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.6.25-2
- don't pollute spec with useless macro

* Tue Feb 07 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.6.25-1
- Update to 0.6.25

* Fri Jan 13 2017 Vít Ondruch <vondruch@redhat.com> - 0.6.24-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.4

* Mon Dec 12 2016 Charalampos Stratakis <cstratak@redhat.com> - 0.6.24-4
- Rebuild for Python 3.6

* Fri Dec 09 2016 Orion Poplawski <orion@cora.nwra.com> - 0.6.24-3
- Use upstream python build options

* Fri Nov 11 2016 Igor Gnatenko <ignatenko@redhat.com> - 0.6.24-2
- remove unused patch

* Thu Nov 10 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.6.24-1
- Update to 0.6.24

* Mon Oct 31 2016 Denis Ollier <larchunix@gmail.com> - 0.6.23-6
- Typo fixes in spec: s/MULTI_SYMANTICS/MULTI_SEMANTICS/

* Tue Sep 13 2016 Igor Gnatenko <ignatenko@redhat.com> - 0.6.23-5
- Trivial fixes in spec

* Sat Sep 03 2016 Neal Gompa <ngompa13@gmail.com> - 0.6.23-4
- Enable suserepo on Fedora to enable making openSUSE containers with
  Zypper

* Fri Aug 12 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.6.23-3
- enable helixrepo on Fedora

* Wed Aug 03 2016 Igor Gnatenko <ignatenko@redhat.com> - 0.6.23-2
- Backport patch to fix dnf --debugsolver crash (RHBZ #1361831)

* Wed Jul 27 2016 Igor Gnatenko <ignatenko@redhat.com> - 0.6.23-1
- Update to 0.6.23

* Wed Jul 20 2016 Igor Gnatenko <ignatenko@redhat.com> - 0.6.22-5
- fix typo

* Wed Jul 20 2016 Igor Gnatenko <ignatenko@redhat.com>
- Backport couple of patches from upstream

* Tue Jul 19 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.22-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_
  Packages

* Fri Jun 24 2016 Petr Písař <ppisar@redhat.com> - 0.6.22-2
- Mandatory Perl build-requires added
  <https://fedoraproject.org/wiki/Changes/Build_Root_Without_Perl>

* Tue Jun 14 2016 Igor Gnatenko <ignatenko@redhat.com> - 0.6.22-1
- Update to 0.6.22

* Mon Jun 06 2016 Igor Gnatenko <ignatenko@redhat.com> - 0.6.21-3
- Enable deb/arch support for non-rhel distros

* Mon May 30 2016 Igor Gnatenko <ignatenko@redhat.com> - 0.6.21-2
- Modify enabled/disabled features

* Wed May 18 2016 Igor Gnatenko <ignatenko@redhat.com> - 0.6.21-1
- Update to 0.6.21

* Tue May 17 2016 Igor Gnatenko <ignatenko@redhat.com> - 0.6.20-2
- backport some bugfixes (RHBZ #1318662, RHBZ #1325471)

* Sat Apr 09 2016 Igor Gnatenko <ignatenko@redhat.com> - 0.6.20-1
- Update to 0.6.20

* Tue Apr 05 2016 Igor Gnatenko <ignatenko@redhat.com> - 0.6.19-3
- re-organize spec file

* Tue Mar 08 2016 Jaroslav Mracek <jmracek@redhat.com> - 0.6.19-2
- Apply 9 patches from upstream

* Sat Feb 27 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.6.19-1
- Update to 0.6.19

* Tue Feb 02 2016 Peter Robinson <pbrobinson@gmail.com> - 0.6.15-6
- Explicitly add rubypick and ruubygems build dependencies

* Tue Jan 12 2016 Vít Ondruch <vondruch@redhat.com> - 0.6.15-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.3

* Sun Jan 10 2016 Dan Horák <dan@danny.cz> - 0.6.15-4
- fix build on non-Fedora with python3

* Tue Jan 05 2016 Jaroslav Mracek <jmracek@redhat.com> - 0.6.15-3
- Fix bzip2 support for python3 build (RhBug:1293652)

* Fri Dec 18 2015 Michal Luscon <mluscon@redhat.com> - 0.6.15-2
- Revert reworked multiversion orphaned handling

* Thu Dec 17 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.6.15-1
- Update to 0.6.15

* Thu Dec 10 2015 Jaroslav Mracek <jmracek@redhat.com> - 0.6.14-8
- Enable bzip2 support

* Thu Nov 26 2015 Adam Williamson <awilliam@redhat.com> - 0.6.14-7
- revert obsolete, as %%python_provide does it (undocumented)

* Wed Nov 18 2015 Adam Williamson <awilliam@redhat.com> - 0.6.14-6
- adjust obsolete for stupid packaging

* Wed Nov 18 2015 Adam Williamson <awilliam@redhat.com> - 0.6.14-5
- python2-solv obsoletes python-solv (#1263230)

* Tue Nov 10 2015 Peter Robinson <pbrobinson@fedoraproject.org> - 0.6.14-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Wed Oct 14 2015 Michal Luscon <mluscon@redhat.com> - 0.6.14-3
- Backport upstream patches

* Mon Oct 12 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.6.14-2
- fix examples in docs

* Mon Oct 12 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.6.14-1
- Update to 0.6.14; Backport patches from upstream

* Thu Sep 10 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.6.12-2
- include pkgconfig file to devel subpkg

* Thu Sep 10 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.6.12-1
- Update to 0.6.12

* Thu Aug 06 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.6.11-11
- drop unused patch

* Wed Aug 05 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.6.11-10
- really upload sources + spec cleanup from patch

* Wed Aug 05 2015 Colin Walters <walters@verbum.org> - 0.6.11-9
- Drop all bindings on EL7, as well as arch/deb solv support

* Wed Aug 05 2015 Colin Walters <walters@verbum.org> - 0.6.11-8
- Use make and not make_build macro, as it's not in EL7

* Wed Aug 05 2015 Colin Walters <walters@verbum.org> - 0.6.11-7
- Add missing leading 0 in conditional

* Wed Aug 05 2015 Jan Silhan <jsilhan@redhat.com> - 0.6.11-6
- uploaded new source for 1f9abfb

* Wed Aug 05 2015 Jan Silhan <jsilhan@redhat.com> - 0.6.11-5
- uploaded new source for 1f9abfb

* Wed Aug 05 2015 Jan Silhan <jsilhan@redhat.com> - 0.6.11-4
- uploaded new source for 1f9abfb

* Wed Aug 05 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.6.11-3
- New version: 1f9abfb

* Tue Aug 04 2015 Adam Williamson <awilliam@redhat.com> - 0.6.11-2
- bindings require the exact matching version of the lib (#1243737)

* Mon Jun 22 2015 Jan Silhan <jsilhan@redhat.com> - 0.6.11-1
- New version: 2db517f

* Wed Jun 17 2015 Dennis Gilmore <dennis@ausil.us> - 0.6.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Mar 27 2015 Jan Silhan <jsilhan@redhat.com> - 0.6.10-4
- New version: 99edb54

* Wed Mar 25 2015 Jan Silhan <jsilhan@redhat.com> - 0.6.10-3
- new tar

* Wed Mar 25 2015 Jan Silhan <jsilhan@redhat.com> - 0.6.10-2
- added source

* Wed Mar 25 2015 Jan Silhan <jsilhan@redhat.com> - 0.6.10-1
- New version: 0.6.10

* Fri Mar 06 2015 Jan Silhan <jsilhan@redhat.com> - 0.6.8-8
- building python2-solv subpkg finally

* Mon Mar 02 2015 Jan Silhan <jsilhan@redhat.com> - 0.6.8-7
- fixed source

* Mon Mar 02 2015 Jan Silhan <jsilhan@redhat.com> - 0.6.8-6
- adds python3 requirement

* Thu Feb 26 2015 Jan Silhan <jsilhan@redhat.com> - 0.6.8-5
- tmp

* Tue Feb 24 2015 Jan Silhan <jsilhan@redhat.com> - 0.6.8-4
- generating python3-solv subpackage

* Tue Feb 24 2015 Jan Silhan <jsilhan@redhat.com> - 0.6.8-3
- rebase to 78c8a55

* Mon Jan 19 2015 Vít Ondruch <vondruch@redhat.com> - 0.6.8-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.2

* Fri Jan 16 2015 Richard Hughes <richard@hughsie.com> - 0.6.8-1
- Update to latest upstream release to fix a crash in PackageKit

* Sun Aug 17 2014 Peter Robinson <pbrobinson@fedoraproject.org> - 0.6.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Aug 11 2014 Jan Silhan <jsilhan@redhat.com> - 0.6.4-4
- rebase to 12af31a

* Mon Jul 28 2014 Ales Kozumplik <ales@redhat.com> - 0.6.4-3
- rebase to 5bd9589

* Mon Jul 14 2014 Jan Silhan <jsilhan@redhat.com> - 0.6.4-2
- changed gitrev for 2a5c1c4 rebase

* Mon Jul 14 2014 Jan Silhan <jsilhan@redhat.com> - 0.6.4-1
- rebase to 3a5c1c4

* Sat Jun 07 2014 Dennis Gilmore <dennis@ausil.us> - 0.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Ales Kozumplik <ales@redhat.com> - 0.6.1-2
- rebase to 6d968f1

* Fri Apr 25 2014 Jan Silhan <jsilhan@redhat.com> - 0.6.1-1
- rebase to f78f5de

* Thu Apr 24 2014 Vít Ondruch <vondruch@redhat.com> - 0.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.1

* Wed Apr 09 2014 Jan Silhan <jsilhan@redhat.com> - 0.6.0-3
- file compressed is called only libsolv

* Wed Apr 09 2014 Jan Silhan <jsilhan@redhat.com> - 0.6.0-2
- added right tarball extension

* Wed Apr 09 2014 Jan Silhan <jsilhan@redhat.com> - 0.6.0-1
- rebase to 05baf54

* Thu Jan 23 2014 Ales Kozumplik <ales@redhat.com> - 0.4.1-2
- rebase

* Mon Dec 16 2013 Ales Kozumplik <ales@redhat.com> - 0.4.1-1
- rebase to a8e47f1

* Fri Nov 22 2013 Zdenek Pavlas <zpavlas@redhat.com> - 0.4.0-2
- Rebase to 0.4.0, upstream commit 4442b7f.
- support DELTA_LOCATION_BASE for completeness

* Tue Oct 29 2013 Ales Kozumplik <ales@redhat.com> - 0.4.0-1
- rebase to d49d319.

* Sat Aug 03 2013 Petr Písař <ppisar@redhat.com> - 0.3.0-12
- Perl 5.18 rebuild

* Wed Jul 31 2013 Ales Kozumplik <ales@redhat.com> - 0.3.0-11
- Rebase to upstream a59d11d

* Mon Jul 22 2013 Ales Kozumplik <ales@redhat.com> - 0.3.0-10
- missing requires

* Mon Jul 22 2013 Ales Kozumplik <ales@redhat.com> - 0.3.0-9
- forgot to bump the release.

* Fri Jul 19 2013 Ales Kozumplik <ales@redhat.com> - 0.3.0-8
- add build flags.

* Wed Jul 17 2013 Petr Písař <ppisar@redhat.com> - 0.3.0-7
- Perl 5.18 rebuild

* Mon Jun 24 2013 Ales Kozumplik <ales@redhat.com> - 0.3.0-6
- rebased to upstream 228d412

* Thu Jun 20 2013 Ales Kozumplik <ales@redhat.com> - 0.3.0-5
- fix: bogus date in changelog

* Thu Jun 20 2013 Ales Kozumplik <ales@redhat.com> - 0.3.0-4
- rebase to upstream 209e9cb

* Thu May 16 2013 Ales Kozumplik <ales@redhat.com> - 0.3.0-3
- run make test

* Thu May 16 2013 Ales Kozumplik <ales@redhat.com> - 0.3.0-2
- rebase to 7399ad1.

* Mon Apr 08 2013 Ales Kozumplik <ales@redhat.com> - 0.3.0-1
- rebase to upstream e372b78

* Thu Feb 14 2013 Dennis Gilmore <dennis@ausil.us> - 0.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Dec 21 2012 Ales Kozumplik <ales@redhat.com> - 0.2.3-2
- Add missing sources.

* Fri Dec 21 2012 Ales Kozumplik <ales@redhat.com> - 0.2.3-1
- wip

* Thu Aug 23 2012 Ales Kozumplik <ales@redhat.com> - 0.0.0-15
- Rebase to 6c9d3eb.

* Mon Jul 23 2012 Ales Kozumplik <ales@redhat.com> - 0.0.0-14
- Fix Perl build.

* Mon Jul 23 2012 Ales Kozumplik <ales@redhat.com> - 0.0.0-13
- Rebuild.

* Thu Jul 19 2012 Dennis Gilmore <dennis@ausil.us> - 0.0.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Ales Kozumplik <ales@redhat.com> - 0.0.0-11
- preliminary fix for JOB resons in solver_describe_decision().

* Sun Jul 01 2012 Ales Kozumplik <ales@redhat.com> - 0.0.0-10
- rebuild

* Thu Jun 07 2012 Ales Kozumplik <ales@redhat.com> - 0.0.0-9
- Rebase to the latest upstream.

* Fri May 18 2012 Ales Kozumplik <akozumpl@redhat.com>
- Rebase to upstream 8cf7650.

* Thu Apr 12 2012 Ales Kozumplik <akozumpl@redhat.com> - 0.0.0-7
- rebase to af1465a2.

* Thu Apr 05 2012 Karel Klic <kklic@redhat.com> - 0.0.0-6
- rebuild

* Mon Apr 02 2012 Karel Klic <kklic@redhat.com> - 0.0.0-5
- rebuild

* Wed Mar 21 2012 Ales Kozumplik <akozumpl@redhat.com> - 0.0.0-4
- the previous build had a wrong relase number in spec.

* Wed Mar 21 2012 Ales Kozumplik <akozumpl@redhat.com> - 0.0.0-3
- Update to upstream libsolv HEAD 857fe28.

* Tue Feb 07 2012 Karel Klic <kklic@redhat.com> - 0.0.0-2
- Adapted to Ruby 1.9.3

* Mon Feb 06 2012 Karel Klic <kklic@redhat.com> - 0.0.0-1
- Initial commit
## END: Generated by rpmautospec
