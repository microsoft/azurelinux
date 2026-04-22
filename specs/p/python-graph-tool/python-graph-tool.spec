## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 3;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# This needs about 15 gigs per thread, otherwise OOMs.
%constrain_build -m 15360

Name:           python-graph-tool
Version:        2.98
Release:        %autorelease
Summary:        Efficient network analysis tool written in Python

# The entire source is LGPL-3.0-or-later, except:
#   - BSL-1.0: src/boost-workaround/
#              src/graph/graphml.cpp
#              src/graph/read_graphviz_new.cpp
#   - LGPL-3.0-or-later AND BSD-3-Clause: src/graph_tool/collection/small.py
# Additionally, the following libraries are header-only and are therefore
# treated as static libraries; their licenses do contribute to that of the
# binary RPMs:
#   - CGAL is: LGPL-3.0-or-later AND GPL-3.0-or-later AND BSL-1.0 AND MIT
#     (and possibly a few tiny bits of other things – this package could use a
#     good license audit – but it is a sprawling package, and the preceding
#     expression is slightly better than the one it currently carries)
#   - pcg-cpp is: MIT OR Apache-2.0
# Additionally, the following are under other licenses but do not contribute to
# the licenses of the binary RPMs:
#   - FSFULLR: aclocal.m4
#   - FSFUL (or perhaps FSFUL AND LGPL-3.0-or-later): configure
#   - GPL-2.0-or-later: build-aux/compile
#                       build-aux/depcomp
#                       build-aux/ltmain.sh
#                       build-aux/py-compile
#                       m4/ax_boost_python.m4
#   - GPL-3.0-or-later: build-aux/config.guess
#                       build-aux/config.sub
#                       m4/ax_create_pkgconfig_info.m4
#                       m4/ax_openmp.m4
#                       m4/ax_python_devel.m4
#   - X11: build-aux/install-sh
#   - FSFAP: m4/ax_boost_base.m4
#            m4/ax_boost_context.m4
#            m4/ax_boost_coroutine.m4
#            m4/ax_boost_graph.m4
#            m4/ax_boost_iostreams.m4
#            m4/ax_boost_regex.m4
#            m4/ax_boost_thread.m4
#            m4/ax_cxx_compile_stdcxx.m4,
#            m4/ax_cxx_compile_stdcxx_17.m4
#            m4/ax_lib_cgal_core.m4
#            m4/ax_python_module.m4
License:        %{shrink:
                LGPL-3.0-or-later AND
                BSL-1.0 AND
                BSD-3-Clause AND
                GPL-3.0-or-later AND
                MIT AND
                (MIT OR Apache-2.0)
                }
URL:            https://graph-tool.skewed.de/
Source:         https://downloads.skewed.de/graph-tool/graph-tool-%{version}.tar.bz2

# Note that upstream sets the optimization flag -O3. Per
# https://docs.fedoraproject.org/en-US/packaging-guidelines/#_compiler_flags,
# we should normally patch this out in order to fully respect the system
# default compiler flags. However, upstream writes in
# https://git.skewed.de/count0/graph-tool/-/blob/release-2.86/configure.ac#L67-L69:
#
#   Enforce -O3. It makes a substantial difference, e.g. 12x speed improvement
#   over -O2 in benchmarks.
#
# It’s not obvious how we should validate upstream’s claim with downstream
# benchmarking; nevertheless, we consider it adequate justification for
# allowing -O3.

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}

BuildRequires:  make
BuildRequires:  git-core
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  gawk

%global _description %{expand:
Graph-tool is an efficient Python module for manipulation and statistical
analysis of graphs (a.k.a. networks). Contrary to most other python modules
with similar functionality, the core data structures and algorithms are
implemented in C++, making extensive use of template metaprogramming, based
heavily on the Boost Graph Library. This confers it a level of performance that
is comparable (both in memory usage and computation time) to that of a pure
C/C++ library.

Please refer to https://graph-tool.skewed.de/static/doc/index.html for
documentation.}

%description %_description


%package -n python3-graph-tool
Summary:        %{summary}

BuildRequires:  python3-devel
BuildRequires:  boost-devel
BuildRequires:  boost-python3-devel
BuildRequires:  CGAL-devel
# CGAL is header-only since version 5.4.0, so we must BR the virtual -static
# subpackage for tracking, per Fedora guidelines
BuildRequires:  CGAL-static
BuildRequires:  pkgconfig(cairomm-1.16)
BuildRequires:  expat-devel
BuildRequires:  gcc-c++
BuildRequires:  gmp-devel
BuildRequires:  gtk3-devel
BuildRequires:  python3-devel
BuildRequires:  %{py3_dist scipy}
BuildRequires:  %{py3_dist numpy}
BuildRequires:  %{py3_dist pycairo}
BuildRequires:  python3-cairo-devel
BuildRequires:  %{py3_dist matplotlib}
BuildRequires:  sparsehash-devel
# BR -static package of header-only libraries for tracking per guidelines
BuildRequires:  pcg-cpp-devel
BuildRequires:  pcg-cpp-static

Recommends:     %{py3_dist pycairo}
Recommends:     %{py3_dist matplotlib}

Provides:       graph-tool%{?_isa} = %{version}-%{release}

%description -n python3-graph-tool %_description


%package -n python3-graph-tool-devel
Summary:        %{summary}

# This package does not contain compiled binaries, so its license does not
# include the licenses of header-only “static” dependencies. The headers of
# pcg-cpp are “re-exposed” in this package, but it uses symbolic links rather
# than installing additional copies. Additionally, no .py source files are
# included.
License:        LGPL-3.0-or-later AND BSL-1.0

Requires:       python3-graph-tool%{?_isa} = %{version}-%{release}
# Since this header-only package is re-exposed as part of the extension API,
# dependent packages should ideally also BuildRequire pcg-cpp-static for
# tracking, per guidelines.
Requires:       pcg-cpp-devel

Provides:       graph-tool-devel%{?_isa} = %{version}-%{release}

%description -n python3-graph-tool-devel %_description


%prep
%autosetup -S git -n graph-tool-%{version}
# Remove shebangs from non-script sources
#
# The pattern of selecting files before modifying them with sed keeps us from
# unnecessarily discarding the original mtimes on unmodified files.
find 'src' -type f -name '*.py' \
    -exec gawk '/^#!/ { print FILENAME }; { nextfile }' '{}' '+' |
  xargs -r sed -r -i '1{/^#!/d}'

# Unbundle pcg-cpp. To avoid having to patch the Makefiles, we use symbolic
# links from the original locations. Note that these are followed when the
# extension API headers are installed, so we need to re-create them afterwards.
rm -vf src/pcg-cpp/include/*
ln -sv \
    '%{_includedir}/pcg_extras.hpp' \
    '%{_includedir}/pcg_random.hpp' \
    '%{_includedir}/pcg_uint128.hpp' \
    'src/pcg-cpp/include/'

# Remove assets for HTML documentation to prove that they are not installed. We
# are most particularly concerned with fonts (in WOFF2 format). To avoid having
# to patch build-system files that explicitly list these assets and expect them
# to exist, we truncate the files to zero length rather than deleting them.
find doc/_static -type f -print -execdir truncate --size=0 '{}' '+'


%conf
./autogen.sh

# We get a few thousand warnings like:
#   warning: 'always_inline' attribute does not apply to types [-Wattributes]
# and since each is very verbose, with a lot of context, the build log explodes
# to many gigabytes, which ends up failing the build. Disable this class of
# warnings as a pragmatic matter.
export CXXFLAGS="${CXXFLAGS-} -Wno-attributes"

# Keeping track of full debugging symbols causes us to run out of *disk space*
# (not memory!) on some koji builders. Reduce the debuginfo level to -g1.
export CXXFLAGS="$(echo "${CXXFLAGS-}" | sed -r 's/(^| )-g($| )/\1-g1\2/')"

%configure \
    --with-python-module-path=%{python3_sitearch} \
    --with-boost-libdir=%{_libdir} \
    --enable-debug


%build
%make_build

# Provide Python metadata
%global graph_tool_distinfo graph_tool-%{version}.dist-info
mkdir %{graph_tool_distinfo}
cat > %{graph_tool_distinfo}/METADATA << EOF
Metadata-Version: 2.1
Name: graph-tool
Version: %{version}
Requires-dist: numpy
Requires-dist: scipy
EOF
echo rpm > %{graph_tool_distinfo}/INSTALLER


%install
%make_install

# Remove installed doc sources
rm -r %{buildroot}/%{_datadir}/doc/graph-tool

# Remove static objects
find %{buildroot} -name '*.la' -print -delete

# Restore symbolic links that were followed in “wheelification”
ln -svf \
    '%{_includedir}/pcg_extras.hpp' \
    '%{_includedir}/pcg_random.hpp' \
    '%{_includedir}/pcg_uint128.hpp' \
    '%{buildroot}%{python3_sitearch}/graph_tool/include/pcg-cpp/'

# Install Python metadata
cp -a %{graph_tool_distinfo} %{buildroot}%{python3_sitearch}


%files -n python3-graph-tool
%license COPYING src/boost-workaround/LICENSE_1_0.txt
%doc README.md ChangeLog AUTHORS
%{python3_sitearch}/graph_tool/
%{python3_sitearch}/%{graph_tool_distinfo}/
%exclude %{python3_sitearch}/graph_tool/include/


%files -n python3-graph-tool-devel
%{python3_sitearch}/graph_tool/include/
%{_libdir}/pkgconfig/graph-tool-py%{python3_version}.pc
%{_libdir}/pkgconfig/graph-tool-py.pc


%changelog
## START: Generated by rpmautospec
* Wed Apr 22 2026 azldev <azurelinux@microsoft.com> - 2.98-3
- Latest state for python-graph-tool

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 2.98-2
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 22 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2.98-1
- Update to 2.98 (close RHBZ#2390176)

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 2.97-9
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.97-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 2.97-7
- Rebuilt for Python 3.14

* Sat Apr 19 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2.97-6
- Lower the debuginfo level
- Needed to avoid running out of disk space on koji builders

* Sat Apr 19 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2.97-4
- Move configuration steps to a %%conf section

* Sat Apr 19 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2.97-3
- Revert "Allow even more memory per compiler process, for more reliable
  builds"

* Sat Apr 19 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2.97-2
- Allow even more memory per compiler process, for more reliable builds

* Thu Apr 17 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2.97-1
- Update to 2.97 (close RHBZ#2360422)

* Thu Apr 17 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2.96-2
- Stop patching/fixing doc files that we will not install anyway

* Fri Apr 04 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2.96-1
- Update to 2.96 (close RHBZ#2356124)

* Tue Mar 04 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2.92-1
- Update to 2.92 (close RHBZ#2349183)

* Mon Feb 10 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2.90-1
- Update to 2.90 (close RHBZ#2344590)

* Mon Feb 10 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2.89-1
- Update to 2.89 (close RHBZ#2344590)

* Mon Jan 20 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2.88-1
- Update to 2.88 (close RHBZ#2335593)

* Sun Jan 19 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2.80-6
- Allow upstream to set -O3

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.80-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Dec 17 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2.80-4
- Move numpy/scipy dependencies to patched-in metadata

* Tue Dec 17 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2.80-3
- Add weak dependencies on pycairo and matplotlib

* Tue Dec 17 2024 Sandro <devel@penguinpee.nl> - 2.80-2
- Add missing runtime dependencies

* Tue Dec 03 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2.80-1
- Update to 2.80 (close RHBZ#2329743)

* Sat Oct 26 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2.79-1
- Update to 2.79 (close RHBZ#2321918)

* Fri Oct 25 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2.78-1
- Update to 2.78 (close RHBZ#2321539)

* Sat Oct 19 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2.77-3
- Rebuilt with CGAL-6.0 in Fedora 42

* Sat Sep 28 2024 Sandro <devel@penguinpee.nl> - 2.77-2
- Provide dist-info metadata (RHBZ#2315149)

* Sat Aug 10 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2.77-1
- Update to 2.77 (close RHBZ#2303673)

* Thu Aug 01 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2.75-1
- Update to 2.75 (close RHBZ#2301744)

* Wed Jul 24 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2.74-1
- Update to 2.74 (close RHBZ#2297839)

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.71-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jul 05 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2.71-1
- Update to 2.71 (close RHBZ#2295496)

* Mon Jun 17 2024 Ankur Sinha (Ankur Sinha Gmail) <sanjay.ankur@gmail.com> - 2.70-1
- feat: update to 2.70 (fixes rh#2292416)

* Tue Jun 11 2024 Ankur Sinha (Ankur Sinha Gmail) <sanjay.ankur@gmail.com> - 2.69-1
- feat: update to 2.69 (fixes rh#2291158)

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 2.68-2
- Rebuilt for Python 3.13

* Mon May 27 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2.68-1
- Update to 2.68 (close RHBZ#2283159)

* Mon May 06 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2.63-1
- Update to 2.63 (close RHBZ#2279141)

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.59-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.59-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 18 2024 Jonathan Wakely <jwakely@redhat.com> - 2.59-2
- Rebuilt for Boost 1.83

* Sat Jan 06 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2.59-1
- Update to 2.59 (close RHBZ#2256970)

* Mon Oct 30 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2.58-3
- Break a long line in the spec file

* Fri Aug 18 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2.58-1
- Update to 2.58 (close RHBZ#2232687)

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.57-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 29 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2.57-1
- Update to 2.57 (close RHBZ#2218665)

* Tue Jun 27 2023 Python Maint <python-maint@redhat.com> - 2.56-4
- Rebuilt for Python 3.12

* Fri Jun 09 2023 Ankur Sinha (Ankur Sinha Gmail) <sanjay.ankur@gmail.com> - 2.56-1
- feat: update to 2.56 (fixes rhbz#2213671)

* Mon May 01 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2.55-1
- Update to 2.55 (close RHBZ#2192313)

* Fri Apr 21 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2.54-1
- Update to 2.54 (close RHBZ#2188413)

* Mon Apr 10 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2.53-1
- Update to 2.53 (close RHBZ#2185454)

* Fri Apr 07 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2.52-1
- Update to 2.52 (close RHBZ#2184845)

* Tue Apr 04 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2.50-1
- Update to 2.50 (close RHBZ#2184345)

* Sun Apr 02 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2.49-1
- Update to 2.49 (close RHBZ#2183768)

* Sun Mar 19 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2.48-1
- Update to 2.48 (close RHBZ#2179683)

* Sat Mar 18 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2.47-1
- Update to 2.47 (close RHBZ#2179447)

* Tue Feb 28 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2.46-2
- Update License for 2.46
- The python3-graph-tool-devel subpackage now has its own License without
  the terms for header-only dependencies, etc.
- Link cairomm1.16 instead of cairomm1.0, now that it is supported

* Tue Feb 28 2023 Ankur Sinha (Ankur Sinha Gmail) <sanjay.ankur@gmail.com> - 2.46-1
- feat: update to 2.46 (fixes rhbz#2173447)

* Mon Feb 20 2023 Jonathan Wakely <jwakely@redhat.com> - 2.45-7
- Rebuilt for Boost 1.81

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.45-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan 11 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 2.45-5
- Update License to include header-only dependencies

* Wed Dec 21 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2.45-4
- Simplify constraining the build

* Tue Dec 20 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2.45-3
- No longer need to exclude armv7hl on F37+
- Additionally, we no longer need to justify excluding i686

* Thu Nov 24 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2.45-2
- Drop -fpermissive workaround

* Sun Nov 20 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2.45-1
- Update to 2.45

* Sun Nov 20 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2.43-24
- Re-enable LTO

* Sun Nov 20 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2.43-23
- Drop workarounds for armv7hl, which is already excluded

* Sat Nov 19 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2.43-22
- Patch out fewer upstream compiler flags

* Sat Nov 19 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2.43-21
- Make the file lists clearer
- Use trailing slashes to indicate directory paths

* Sat Nov 19 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2.43-20
- Reduce macro indirection in the spec file

* Sat Nov 19 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2.43-19
- Include license file for BSL-1.0

* Sat Nov 19 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2.43-18
- Convert License field to SPDX

* Sat Nov 19 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2.43-17
- Work around 2144197

* Sat Nov 19 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2.43-16
- Break a long line in the spec file

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.43-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 15 2022 Python Maint <python-maint@redhat.com> - 2.43-14
- Rebuilt for Python 3.11

* Wed May 04 2022 Thomas Rodgers <trodgers@redhat.com> - 2.43-13
- Rebuilt for Boost 1.78

* Fri Feb 04 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2.43-12
- No longer reduce debug level for ppc64le/s390x

* Tue Feb 01 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2.43-11
- Re-enable ppc64le (fix RHBZ#1771031)

* Tue Feb 01 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2.43-10
- BR CGAL-static since CGAL is now header-only

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.43-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jan 07 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2.43-8
- Drop intersphinx mappings

* Fri Dec 17 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 2.43-4
- Remove arch from -devel dependency on pcg-cpp-devel; the pcg-cpp-devel
  subpackage will become noarch

* Mon Sep 20 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 2.43-3
- Unbundle pcg-cpp
- Split out headers for C++ extension development into a -devel package

* Fri Aug 27 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 2.43-2
- Work around resource limits to re-enable s390x, and get closer to the root
  causes on the remaining excluded architectures

* Tue Aug 10 2021 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 2.43-1
- Update to latest release
- Remove unneeded patches

* Sat Aug 07 2021 Jonathan Wakely <jwakely@redhat.com> - 2.33-7
- Rebuilt for Boost 1.76

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.33-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.33-5
- Rebuilt for Python 3.10

* Fri Feb 12 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 2.33-4
- Use pkgconfig to BR the required cairomm API/ABI version 1.0 (vs. 1.16)

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.33-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 22 2021 Jonathan Wakely <jwakely@redhat.com> - 2.33-2
- Rebuilt for Boost 1.75

* Fri Sep 04 2020 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 2.33-1
- Update to latest release
- Disable LTO
- update COPYING file name
- Update license

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.29-7
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.29-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat May 30 2020 Jonathan Wakely <jwakely@redhat.com> - 2.29-5
- Rebuilt for Boost 1.73
- Simplify shell command to determine number of threads to use

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 2.29-4
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.29-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Nov 09 2019 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 2.29-2
- Exclude builds on arches: usually falls short of resources

* Fri Nov 01 2019 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 2.29-1
- Remove unneeded shebangs

* Tue Oct 22 2019 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 2.29-1
- Improve conditional to handle cases where _smp_build_ncpus is not defined
- Correct conditional hack

* Tue Oct 15 2019 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 2.29-1
- Initial build

## END: Generated by rpmautospec
