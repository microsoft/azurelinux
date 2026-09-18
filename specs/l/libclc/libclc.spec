# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# this stop us generating an empty debuginfo
%global debug_package %{nil}

%global shortname clc
%global libclc_version 21.1.8
#global rc_ver 3
%global libclc_srcdir libclc-%{libclc_version}%{?rc_ver:-rc%{rc_ver}}.src

Name:           libclc
Version:        %{libclc_version}%{?rc_ver:~rc%{rc_ver}}
Release:        1%{?dist}
Summary:        An open source implementation of the OpenCL 1.1 library requirements

License:        Apache-2.0 WITH LLVM-exception OR NCSA OR MIT
URL:            https://libclc.llvm.org
Source0:        https://github.com/llvm/llvm-project/releases/download/llvmorg-%{libclc_version}%{?rc_ver:-rc%{rc_ver}}/%{libclc_srcdir}.tar.xz
Source1:        https://github.com/llvm/llvm-project/releases/download/llvmorg-%{libclc_version}%{?rc_ver:-rc%{rc_ver}}/%{libclc_srcdir}.tar.xz.sig
Source2:        release-keys.asc

BuildRequires:  clang-devel >= %{version}
BuildRequires:  libedit-devel
BuildRequires:  llvm-devel >= %{version}
BuildRequires:  python-unversioned-command
BuildRequires:  zlib-devel
BuildRequires:  cmake
BuildRequires:  spirv-llvm-translator-tools

# For signature verification
BuildRequires:  gnupg2

Requires:       %{name}-spirv%{?_isa} = %{version}-%{release}

%description
libclc is an open source, BSD licensed implementation of the library
requirements of the OpenCL C programming language, as specified by the
OpenCL 1.1 Specification. The following sections of the specification
impose library requirements:

  * 6.1: Supported Data Types
  * 6.2.3: Explicit Conversions
  * 6.2.4.2: Reinterpreting Types Using as_type() and as_typen()
  * 6.9: Preprocessor Directives and Macros
  * 6.11: Built-in Functionsj
  * 9.3: Double Precision Floating-Point
  * 9.4: 64-bit Atomics
  * 9.5: Writing to 3D image memory objects
  * 9.6: Half Precision Floating-Point

libclc is intended to be used with the Clang compiler's OpenCL frontend.

libclc is designed to be portable and extensible. To this end, it provides
generic implementations of most library requirements, allowing the target
to override the generic implementation at the granularity of individual
functions.

libclc currently only supports the PTX target, but support for more
targets is welcome.


%package        spirv
Summary:        Spirv subset of %{name}

%description    spirv
The %{name}-spirv package contains the spirv*-mesa3d-.spv files only,
which are the subset required for upstream Mesa OpenCL support with RustiCL.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -n %{libclc_srcdir} -p2

%build
export CFLAGS="%{build_cflags} -D__extern_always_inline=inline"
%set_build_flags
%cmake -DCMAKE_INSTALL_DATADIR:PATH=%{_lib}

%cmake_build

%install
%cmake_install

%check
%cmake_build --target test

%files
%license LICENSE.TXT
%doc README.md CREDITS.TXT
%{_libdir}/%{shortname}/*.bc

%files spirv
%license LICENSE.TXT
%doc README.md CREDITS.TXT
%dir %{_libdir}/%{shortname}
%{_libdir}/%{shortname}/spirv-mesa3d-.spv
%{_libdir}/%{shortname}/spirv64-mesa3d-.spv

%files devel
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Tue Dec 16 2025 Packit <hello@packit.dev> - 21.1.8-1
- Update to version 21.1.8
- Resolves: rhbz#2422638

* Fri Dec 05 2025 Packit <hello@packit.dev> - 21.1.7-1
- Update to version 21.1.7
- Resolves: rhbz#2402496

* Tue Nov 18 2025 Packit <hello@packit.dev> - 21.1.6-1
- Update to version 21.1.6
- Resolves: rhbz#2402496

* Tue Nov 04 2025 Packit <hello@packit.dev> - 21.1.5-1
- Update to version 21.1.5
- Resolves: rhbz#2402496

* Tue Oct 21 2025 Packit <hello@packit.dev> - 21.1.4-1
- Update to version 21.1.4
- Resolves: rhbz#2402496

* Wed Oct 08 2025 Packit <hello@packit.dev> - 21.1.3-1
- Update to version 21.1.3
- Resolves: rhbz#2402496

* Thu Sep 25 2025 Tom Stellard <tstellar@redhat.com> - 21.1.2-1
- Update to LLVM 21.1.2

* Thu Sep 11 2025 Tom Stellard <tstellar@redhat.com> - 21.1.1-1
- Update to LLVM 21.1.1

* Sat Aug 09 2025 Tom Stellard <tstellar@redhat.com> - 21.1.0-1
- Update to LLVM 21.1.0

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 20.1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jul 10 2025 Nikita Popov <npopov@redhat.com> - 20.1.8-1
- Update to LLVM 20.1.8

* Fri Jun 20 2025 Nikita Popov <npopov@redhat.com> - 20.1.7-1
- Update to LLVM 20.1.7

* Mon Jun 02 2025 Nikita Popov <npopov@redhat.com> - 20.1.6-1
- Update to LLVM 20.1.6

* Mon May 26 2025 Nikita Popov <npopov@redhat.com> - 20.1.5-1
- Update to LLVM 20.1.5

* Wed May 07 2025 Nikita Popov <npopov@redhat.com> - 20.1.4-1
- Update to LLVM 20.1.4

* Tue Apr 22 2025 Nikita Popov <npopov@redhat.com> - 20.1.3-1
- Update to LLVM 20.1.3

* Thu Apr 03 2025 Nikita Popov <npopov@redhat.com> - 20.1.2-1
- Update to LLVM 20.1.2

* Thu Mar 20 2025 Nikita Popov <npopov@redhat.com> - 20.1.1-1
- Update to LLVM 20.1.1

* Wed Mar 05 2025 Nikita Popov <npopov@redhat.com> - 20.1.0-1
- Update to LLVM 20.1.0

* Wed Jan 22 2025 Timm Bäder <tbaeder@redhat.com> - 19.1.7-1
- Update to 19.1.7

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 19.1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jan 02 2025 Timm Bäder <tbaeder@redhat.com> - 19.1.6-1
- Update to 19.1.6

* Mon Dec 09 2024 Asahi Lina <lina@asahilina.net> - 19.1.5-2
- Split off spirv files into a subpackage

* Thu Dec 05 2024 Timm Bäder <tbaeder@redhat.com> - 19.1.5-1
- Update to 19.1.5

* Mon Nov 25 2024 Timm Bäder <tbaeder@redhat.com> - 19.1.4-1
- Update to 19.1.4

* Wed Nov 06 2024 Timm Bäder <tbaeder@redhat.com> - 19.1.3-1
- Update to 19.1.3

* Thu Sep 19 2024 Timm Bäder <tbaeder@redhat.com> - 19.1.0-1
- Update to 19.1.0

* Fri Sep 13 2024 Timm Bäder <tbaeder@redhat.com> - 19.1.0~rc4-1
- Update to 19.1.0-rc4

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 18.1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jul 12 2024 Jesus Checa Hidalgo <jchecahi@redhat.com> - 18.1.8-1
- 18.1.8 Release

* Thu Jun 13 2024 Tom Stellard <tstellar@redhat.com> - 18.1.7-1
- 18.1.7 Release

* Tue May 21 2024 Tom Stellard <tstellar@redhat.com> - 18.1.6-1
- 18.1.6 Release

* Fri May 03 2024 Tom Stellard <tstellar@redhat.com> - 18.1.4-1
- 18.1.4 Release

* Wed Apr 17 2024 Tom Stellard <tstellar@redhat.com> - 18.1.3-1
- 18.1.3 Release

* Fri Mar 22 2024 Tom Stellard <tstellar@redhat.com> - 18.1.2-1
- 18.1.2 Release

* Wed Mar 13 2024 Tom Stellard <tstellar@redhat.com> - 18.1.1-1
- 18.1.1 Release

* Thu Feb 29 2024 Tom Stellard <tstellar@redhat.com> - 18.1.0~rc4-1
- 18.1.0-rc4 Release

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 17.0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 17.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Nov 29 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 17.0.6-1
- Update to LLVM 17.0.6

* Wed Nov 01 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 17.0.4-1
- Update to LLVM 17.0.4

* Wed Oct 18 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 17.0.3-1
- Update to LLVM 17.0.3

* Thu Oct 05 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 17.0.2-1
- Update to LLVM 17.0.2

* Mon Sep 25 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 17.0.1-1
- Update to LLVM 17.0.1

* Mon Sep 11 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 17.0.0~rc4-1
- Update to LLVM 17.0.0 RC4

* Fri Aug 25 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 17.0.0~rc3-1
- Update to LLVM 17.0.0 RC3

* Mon Aug 07 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 17.0.0~rc1-1
- Update to LLVM 17.0.0 RC1

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 16.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jul 10 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 16.0.6-1
- Update to LLVM 16.0.6

* Tue Jun 06 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 16.0.5-1
- Update to LLVM 16.0.5

* Fri May 19 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 16.0.4-1
- Update to LLVM 16.0.4

* Wed May 10 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 16.0.3-1
- Update to LLVM 16.0.3

* Thu Apr 27 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 16.0.2-1
- Update to LLVM 16.0.2

* Thu Apr 13 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 16.0.1-1
- Update to LLVM 16.0.1

* Tue Mar 21 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 16.0.0-1
- Update to LLVM 16.0.0

* Wed Mar 15 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 16.0.0~rc4-1
- Update to LLVM 16.0.0 RC4

* Wed Mar 1 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 16.0.0~rc3-1
- Update to LLVM 16.0.0 RC3

* Thu Jan 19 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 15.0.7-3
- Update license to SPDX identifiers.
- Include the Apache license adopted in 2019.

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 15.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jan 13 2023 Nikita Popov <npopov@redhat.com> - 15.0.7-1
- Update to LLVM 15.0.7

* Tue Dec 06 2022 Nikita Popov <npopov@redhat.com> - 15.0.6-1
- Update to LLVM 15.0.6

* Mon Nov 07 2022 Nikita Popov <npopov@redhat.com> - 15.0.4-1
- Update to LLVM 15.0.4

* Tue Sep 06 2022 Nikita Popov <npopov@redhat.com> - 15.0.0-1
- Update to LLVM 15.0.0

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 14.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 20 2022 Timm Bäder <tbaeder@redhat.com> - 14.0.5-1
- Update to 14.0.5

* Wed Mar 30 2022 Timm Bäder <tbaeder@redhat.com> - 14.0.0-1
- Update to 14.0.0

* Thu Feb 03 2022 Nikita Popov <npopov@redhat.com> - 13.0.1-1
- Update to LLVM 13.0.1 final

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 13.0.1~rc2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jan 14 2022 Nikita Popov <npopov@redhat.com> - 13.0.1~rc1-1
- Update to LLVM 13.0.1rc2

* Fri Oct 01 2021 Tom Stellard <tstellar@redhat.com> - 13.0.0-1
- 13.0.0 Release

* Wed Sep 22 2021 Tom Stellard <tstellar@redhat.com> - 13.0.0~rc3-1
- 13.0.0-rc3 Release

* Wed Sep 15 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 13.0.0~rc1-2
- Fix library paths (rhbz 1960955)

* Mon Aug 09 2021 Tom Stellard <tstellar@redhat.com> - 13.0.0~rc1-1
- 13.0.0-rc1 Release

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 12.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 14 2021 Tom Stellard <tstellar@redhat.com> - 12.0.1-1
- 12.0.1 Release

* Wed Jun 30 2021 Tom Stellard <tstellar@redhat.com> - 12.0.1~rc3-1
- 12.0.1-rc3 Release

* Thu Jun 03 2021 Tom Stellard <tstellar@redhat.com> - 12.0.1~rc1-1
- 12.0.1-rc1 Release

* Mon May 17 2021 Dave Airlie <airlied@redhat.com> - 12.0.0-2
- build the spirv

* Fri Apr 16 2021 Tom Stellard <tstellar@redhat.com> - 12.0.0-1
- 12.0.0 Release

* Fri Feb 12 2021 Stephen Gallagher <sgallagh@redhat.com> - 11.0.0-1
- Latest upstream release that matches llvm 11.0.0

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-19.git9f6204e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-18.git9f6204e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-17.git9f6204e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-16.git9f6204e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Apr 03 2019 Dave Airlie <airlied@redhat.com> - 0.2.0-15.git9f6204e
- Update to latest upstream snapshot (prior to moving to cmake)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-14.git1ecb16d
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Dec 04 2018 Dave Airlie <airlied@redhat.com> - 0.2.0-13.git1ecb16d
- Update to latest libclc snapshot

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-12.gitc45b9df
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.2.0-11.gitc45b9df
- Update to latest git snapshot

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-10.git1cb3fbf
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Dan Horák <dan[at]danny.cz> - 0.2.0-9.git1cb3fbf
- Drop build workarounds

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-8.git1cb3fbf
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 24 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.2.0-7.git1cb3fbf
- Update to latest git snapshot

* Sat Mar 11 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.2.0-6.git520743b
- Update to latest snapshot which supports LLVM 3.9

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-5.20160207gitdc330a3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Aug 10 2016 Dan Horák <dan[at]danny.cz> - 0.2.0-4.20160207gitdc330a3
- Build on s390x

* Sun Apr 10 2016 Peter Robinson <pbrobinson@fedoraproject.org> 0.2.0-3.20160207gitdc330a3
- Build on ARMv7

* Tue Apr 05 2016 Than Ngo <than@redhat.com> - 0.2.0-2.20160207gitdc330a3
- temporary disable stack-protector on powe64 as workaround due to the bug in llvm
  which causes the build failure on power64

* Sun Feb 07 2016 Fabian Deutsch <fabiand@fedoraproject.org> - 0.2.0-1.20160207gitdc330a3
- Update to latest upstream
- Dorp llvm-static BR

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.1-14.20150918git4346c30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 21 2016 Peter Robinson <pbrobinson@fedoraproject.org> 0.0.1-13.20150918git4346c30
- Spell aarch64 correctly

* Thu Jan 21 2016 Peter Robinson <pbrobinson@fedoraproject.org> 0.0.1-12.20150918git4346c30
- Now supported on aarch64/Power64

* Fri Sep 18 2015 Dave Airlie <airlied@redhat.com> 0.0.1-11.20150918git4346c30
- latest snapshot - set build req to llvm 3.7

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.1-10.20140901gite822ae3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jan 08 2015 Adel Gadllah <adel.gadllah@gmail.com> - 0.0.1-9.20140901gite822ae3
- Rebuilt with newer llvm

* Tue Oct 28 2014 Peter Robinson <pbrobinson@fedoraproject.org> - 0.0.1-8.20140901gite822ae3
- Update to a newer snapshot

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.1-7.20140705git61127c5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul 25 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.0.1-6
- Rebuild now llvm bits are fixed for gcc-4.9
- Minor cleanups

* Sat Jul 05 2014 Fabian Deutsch <fabiand@fedoraproject.org> - 0.0.1-5
- Update to latest snapshot to support AMD Kaveri APUs
- Move bitcode files to an arch dependent dir, as they are arch dependent

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.1-4.20140429git4341094
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 29 2014 Fabian Deutsch <fabiand@fedoraproject.org> - 0.0.1-2.20140429git4341094
- Update to latest snapshot
- Support for AMD Kabini

* Mon Jan 13 2014 Fabian Deutsch <fabiand@fedoraproject.org> - 0.0.1-2.20140108gitc002f62
- Move headers to main package, needed by clover at runtime

* Wed Jan 08 2014 Fabian Deutsch <fabiand@fedoraproject.org> - 0.0.1-1.20140108gitc002f62
- Could not use latest master because it doesn't build
- Update to a fresher snapshot
- Limit to x86

* Sun Jul 14 2013 Fabian Deutsch <fabiand@fedoraproject.org> - 0.0.1-0.20130714git5217211
- Initial package
