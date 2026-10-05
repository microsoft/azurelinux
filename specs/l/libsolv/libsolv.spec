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
%bcond_without openssl
%if %{defined rhel}
%bcond_with zchunk
%else
%bcond_without zchunk
%endif
%bcond_without zstd

%define __cmake_switch(b:) %[%{expand:%%{?with_%{-b*}}} ? "ON" : "OFF"]

Name:           lib%{libname}
Version:        0.7.40
Release: 6%{?dist}
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
# Add "rpm" INSTALLER to Python metadata, not suitable for upstream.
# Replaces <https://src.fedoraproject.org/rpms/libsolv/pull-request/14>.
# Requires Python-Provide-dist-info-metadata.patch.
Patch:          0002-Add-INSTALLER-to-Python-metadata.patch
# Fix a buffer overflow when decompressing solv pages (CVE-2026-48864),
# rejected by upstream, <https://github.com/openSUSE/libsolv/pull/622>.
Patch:          0003-Fix-a-buffer-overflow-when-decompressing-solv-pages.patch
# Compute hashes with OpenSSL, proposed upstream,
# <https://github.com/openSUSE/libsolv/pull/627>.
Patch:          0004-Add-support-for-computing-hashes-using-OpenSSL-3.1.0.patch

BuildRequires:  cmake >= 3.5
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  pkgconfig(rpm)
BuildRequires:  zlib-devel
# -DWITH_LIBXML2=ON
BuildRequires:  libxml2-devel
%if %{with openssl}
# -DWITH_OPENSSL=ON
BuildRequires:  coreutils
BuildRequires:  openssl-devel >= 3.1.0
%endif
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

Patch4: 0002-Make-file-time-available-for-dnf-plugins.patch
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
%if %{with openssl}
# Unbundle private cryptography
rm src/chksum_impl.c src/md5.{c,h} src/sha1.{c,h} src/sha2.{c,h}
%endif

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
  -DWITH_OPENSSL=%{__cmake_switch -b openssl}             \
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

%check
%ctest

# Python smoke test (not tested in %%ctest):
export PYTHONPATH=%{buildroot}%{python3_sitearch}
export LD_LIBRARY_PATH=%{buildroot}%{_libdir}
%python3 -c 'import solv'

%files
%license LICENSE*
%doc NEWS README TODO
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
%{python3_sitearch}/%{libname}-*.dist-info/
%endif

%changelog
* Tue Sep 22 2026 Petr Pisar <ppisar@redhat.com> - 0.7.40-1
- 0.7.40 bump

* Fri Sep 18 2026 Petr Pisar <ppisar@redhat.com> - 0.7.39-3
- Move from automatic release numbering to manual one

* Fri Jun 19 2026 Petr Písař <ppisar@redhat.com> - 0.7.39-2
- Compute hashes with OpenSSL

* Thu May 28 2026 Petr Písař <ppisar@redhat.com> - 0.7.39-1
- Update to 0.7.39

* Wed May 27 2026 Petr Písař <ppisar@redhat.com> - 0.7.38-2
- Fix a buffer overflow when decompressing solv pages (CVE-2026-48864)

* Tue May 26 2026 Petr Písař <ppisar@redhat.com> - 0.7.38-1
- Update to 0.7.38

* Tue Apr 28 2026 Petr Písař <ppisar@redhat.com> - 0.7.37-2
- Cope with integer overflow in data size arithmetics in repo_add_solv()
  (upstream GH#617)

* Thu Apr 23 2026 Petr Písař <ppisar@redhat.com> - 0.7.37-1
- Update to 0.7.37

* Wed Apr 22 2026 Petr Písař <ppisar@redhat.com> - 0.7.36-3
- Fix a buffer overflow when copying SHA-384/512 checksum from a Debian
  repository (upstream GH#616)

* Thu Mar 12 2026 Petr Písař <ppisar@redhat.com> - 0.7.36-1
- Update to 0.7.36

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.35-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

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
