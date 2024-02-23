# luajit does not have official releases, intead opting for a rolling release
# model. The upstream supports a couple branches/versions, the value of
# upstream_branch is the current production branch version.
# See: https://luajit.org/status.html

# Current production major & minor version:
%global luajit_version_major 2
%global luajit_version_minor 1

%global luajit_major_minor %{luajit_version_major}.%{luajit_version_minor}

# To support semantic versioning, luajit uses the posix timestamp of the last
# commit as the patch version.

# The following are filled in by generate-tarball.sh !
# Upstream commit snapshot (run update-release.sh to update)
%global upstream_commit 0d313b243194a0b8d2399d8b549ca5a0ff234db5
# Upstream commit posix timestamp (run update-release.sh to update)
%global upstream_commit_timestamp 1707061634

Summary:        Just-In-Time Compiler for Lua
Name:           luajit
Version:        %{luajit_major_minor}.%{upstream_commit_timestamp}
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://luajit.org/
# Note: github only cares about the commit ID, the name of the file name is anything we want.
Source0:        https://github.com/LuaJIT/LuaJIT/archive/%{upstream_commit}/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make

%description
LuaJIT implements the full set of language features defined by Lua 5.1.
The virtual machine (VM) is API- and ABI-compatible to the standard
Lua interpreter and can be deployed as a drop-in replacement.

%package devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description devel
This package contains development files for %{name}.

%prep
%autosetup -p1 -n LuaJIT-%{upstream_commit}

# Enable Lua 5.2 features
sed -i -e '/-DLUAJIT_ENABLE_LUA52COMPAT/s/^#//' src/Makefile

grep DLUAJIT_ENABLE_LUA52COMPAT src/Makefile

# preserve timestamps (cicku)
sed -i -e '/install -m/s/-m/-p -m/' Makefile

%build
# Q= - enable verbose output
# E= @: - disable @echo messages
# NOTE: we use amalgamated build as per documentation suggestion doc/install.html
make amalg Q= E=@: PREFIX=%{_prefix} TARGET_STRIP=: \
           CFLAGS="%{build_cflags}" LDFLAGS="%{build_ldflags}" \
           MULTILIB=%{_lib} \
           %{?_smp_mflags}

%install
# PREREL= - disable -betaX suffix
# INSTALL_TNAME - executable name
%make_install PREFIX=%{_prefix} \
              MULTILIB=%{_lib}

rm -rf _tmp_html ; mkdir _tmp_html
cp -a doc _tmp_html/html

# Remove static .a
find %{buildroot} -type f -name *.a -delete -print

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%check

# Don't fail the build on a check failure.
make check || true

%files
%license COPYRIGHT
%doc README
%{_bindir}/%{name}
%{_bindir}/%{name}-%{version}
%{_libdir}/lib%{name}-*.so.*
%{_mandir}/man1/%{name}.1*
%{_datadir}/%{name}-%{luajit_major_minor}/

%files devel
%doc _tmp_html/html/
%{_includedir}/%{name}-%{luajit_major_minor}/
%{_libdir}/lib%{name}-*.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Fri Feb 23 2024 Francisco Huelsz Prince <frhuelsz@microsoft.com> - 2.1.1707061634-1
- Update to latest rolling release.

* Fri Jan 27 2023 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 2.1.0-26
- Initial CBL-Mariner import from Fedora 38 (license: MIT).
- Verified license.
- Replaced ldconfig scriptlets with explicit calls to ldconfig.
- Removing rctag Release tag format should be in [number][dist].

* Sun Aug 21 2022 Andreas Schneider <asn@redhat.com> - 2.1.0-0.25beta3
- Update to latest luajit v2.1 git version

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-0.24beta3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-0.23beta3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Oct 26 2021 Siddhesh Poyarekar <siddhesh@gotplt.org> - 2.1.0-0.22beta3
- Bring back the earlier code to do ln -sf.

* Tue Oct 12 2021 Andreas Schneider <asn@redhat.com> - 2.1.0-0.21beta3
- Rebase onto https://github.com/LuaJIT/LuaJIT/tree/v2.1
- Dropped support for ppc64le
- Dropped support for s390x

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-0.20beta3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-0.19beta3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-0.18beta3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-0.17beta3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Sep 25 2019 Siddhesh Poyarekar <sid@reserved-bit.com> - 2.1.0-0.16beta3
- New API functions jit.prngstate and thread.exdata from OpenResty.
- Bug fixes in ppc64le and aarch64.
- Optimised string hash function for SSE4.2
- Miscellaneous bug fixes.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-0.16beta3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jun 25 2019 Siddhesh Poyarekar <sid@reserved-bit.com> - 2.1.0-0.15beta3
- Port JIT features and fixes from openresty/luajit2.

* Wed Jun 19 2019 Siddhesh Poyarekar <sid@reserved-bit.com> - 2.1.0-0.14beta3
- Patch for PPC64 support.

* Wed Jun 19 2019 Siddhesh Poyarekar <sid@reserved-bit.com> - 2.1.0-0.13beta3
- arm: Fix up condition codes for conditional arithmetic insn.
- bugfix: fixed a segfault when unsinking 64-bit pointers.
- Remove setrlimit on FreeBSD.
- test: Check for package.searchers only in compat5.2.

* Mon Jun 17 07:10:20 CEST 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.1.0-0.12beta3
- Enable Lua 5.2 compatibility

* Wed Apr 24 2019 Siddhesh Poyarekar <sid@reserved-bit.com> - 2.1.0-0.11beta3
- Add s390x support.

* Fri Apr 12 2019 Siddhesh Poyarekar <sid@reserved-bit.com> - 2.1.0-0.10beta3
- Add upstream bug fixes from the v2.1 branch.
- Add bug fixes from https://github.com/siddhesh/LuaJIT.git
- Incorporate tests and benchmarks from LuaJIT-test-cleanup.

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-0.9beta3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-0.8beta3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-0.7beta3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-0.6beta3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-0.5beta3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 15 2017 Tom Callaway <spot@fedoraproject.org> - 2.1.0-0.4beta3
- Update to 2.1.0-beta3

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-0.3beta2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Aug 29 2016 Igor Gnatenko <ignatenko@redhat.com> - 2.1.0-0.2beta2
- Add aarch64 to ExclusiveArch

* Mon Aug 29 2016 Igor Gnatenko <ignatenko@redhat.com> - 2.1.0-0.1beta2
- Update to 2.1.0-beta2 (RHBZ #1371158)

* Mon May 09 2016 Dan Horák <dan[at]danny.cz> - 2.0.4-5
- set ExclusiveArch also for Fedora

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Aug 07 2015 Oliver Haessler <oliver@redhat.com> - 2.0.4-3
- only build x86_64 on EPEL as luajit has no support for ppc64

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 21 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.4-1
- 2.0.4

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul 09 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.3-3
- rebuild against lua 5.2

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Mar 13 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.3-1
- 2.0.3 upstream release

* Sun Dec 15 2013 Clive Messer <clive.messer@communitysqueeze.org> - 2.0.2-9
- Apply luajit-path64.patch on x86_64.

* Mon Dec 09 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.2-8
- Fix strip (thanks Ville Skyttä)

* Fri Dec 06 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.2-7
- Fix executable binary

* Mon Dec 02 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.2-6
- Fix .pc

* Sun Dec 01 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.2-5
- Fixed short-circuit builds (schwendt)

* Sat Nov 30 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.2-4
- Preserve timestamps at install

* Fri Nov 29 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.2-3
- fixed some issues found by besser82
- Moved html-docs to -devel subpackage (besser82)
 
* Thu Nov 28 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.2-2
- Re-update

* Mon Sep 02 2013 Muayyad Alsadi <alsadi@gmail.com> - 2.0.2-1
- Update to new upstream version
- remove PREREL= option

* Mon Feb 06 2012 Andrei Lapshin - 2.0.0-0.4.beta9
- Update to new upstream version
- Rename main executable to luajit
- Remove BuildRoot tag and %%clean section

* Sun Oct 09 2011 Andrei Lapshin - 2.0.0-0.3.beta8
- Enable debug build
- Enable verbose build output
- Move libluajit-*.so to -devel
- Add link to upstream hotfix #1

* Tue Jul 05 2011 Andrei Lapshin <alapshin@gmx.com> - 2.0.0-0.2.beta8
- Append upstream hotfix #1

* Sun Jul 03 2011 Andrei Lapshin <alapshin@gmx.com> - 2.0.0-0.1.beta8
- Initial build
