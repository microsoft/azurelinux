## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autochangelog
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%if (0%{?rhel} > 0 && 0%{?rhel} < 8)
# portable jdk 17 specific bug, _jvmdir being missing
%define _jvmdir /usr/lib/jvm
%endif

# debug_package %%{nil} is portable-jdks specific
%define  debug_package %{nil}

# RPM conditionals so as to be able to dynamically produce
# slowdebug/release builds. See:
# http://rpm.org/user_doc/conditional_builds.html
#
# Examples:
#
# Produce release, fastdebug *and* slowdebug builds on x86_64 (default):
# $ rpmbuild -ba java-25-openjdk.spec
#
# Produce only release builds (no debug builds) on x86_64:
# $ rpmbuild -ba java-25-openjdk.spec --without slowdebug --without fastdebug
#
# Only produce a release build on x86_64:
# $ fedpkg mockbuild --without slowdebug --without fastdebug

# Enable fastdebug builds by default on relevant arches.
%bcond_without fastdebug
# Enable slowdebug builds by default on relevant arches.
%bcond_without slowdebug
# Enable release builds by default on relevant arches.
%bcond_without release
# Enable static library builds by default.
%bcond_without staticlibs
# Remove build artifacts by default
%bcond_with artifacts
# Build a fresh libjvm.so for use in a copy of the bootstrap JDK
%bcond_without fresh_libjvm
# Build with system libraries
%bcond_with system_libs

# This is RHEL 7 specific as it doesn't seem to have the
# __brp_strip_static_archive macro.
%if 0%{?rhel} == 7
%define __os_install_post %{nil}
%endif

# Workaround for stripping of debug symbols from static libraries
%if %{with staticlibs}
%define __brp_strip_static_archive %{nil}
%global include_staticlibs 1
%else
%global include_staticlibs 0
%endif

%if %{with system_libs}
%global system_libs 1
%global link_type system
%global freetype_lib %{nil}
%else
%global system_libs 0
%global link_type bundled
%global freetype_lib |libfreetype[.]so.*
%endif

# The -g flag says to use strip -g instead of full strip on DSOs or EXEs.
# This fixes detailed NMT and other tools which need minimal debug info.
# See: https://bugzilla.redhat.com/show_bug.cgi?id=1520879
%global _find_debuginfo_opts -g

# note: parametrized macros are order-sensitive (unlike not-parametrized) even with normal macros
# also necessary when passing it as parameter to other macros. If not macro, then it is considered a switch
# see the difference between global and define:
# See https://github.com/rpm-software-management/rpm/issues/127 to comments at  "pmatilai commented on Aug 18, 2017"
# (initiated in https://bugzilla.redhat.com/show_bug.cgi?id=1482192)
%global debug_suffix_unquoted -slowdebug
%global fastdebug_suffix_unquoted -fastdebug
%global main_suffix_unquoted -main
%global staticlibs_suffix_unquoted -staticlibs
# quoted one for shell operations
%global debug_suffix "%{debug_suffix_unquoted}"
%global fastdebug_suffix "%{fastdebug_suffix_unquoted}"
%global normal_suffix ""
%global main_suffix "%{main_suffix_unquoted}"
%global staticlibs_suffix "%{staticlibs_suffix_unquoted}"

%global debug_warning This package is unoptimised with full debugging. Install only as needed and remove ASAP.
%global fastdebug_warning This package is optimised with full debugging. Install only as needed and remove ASAP.
%global debug_on unoptimised with full debugging on
%global fastdebug_on optimised with full debugging on
%global for_fastdebug for packages with debugging on and optimisation
%global for_debug for packages with debugging on and no optimisation

%if %{with release}
%global include_normal_build 1
%else
%global include_normal_build 0
%endif

%if %{include_normal_build}
%global normal_build %{normal_suffix}
%else
%global normal_build %{nil}
%endif

# We have hardcoded list of files, which  is appearing in alternatives, and in files
# in alternatives those are slaves and master, very often triplicated by man pages
# in files all masters and slaves are ghosted
# the ghosts are here to allow installation via query like `dnf install /usr/bin/java`
# you can list those files, with appropriate sections: cat *.spec | grep -e --install -e --slave -e post_ -e alternatives
# TODO - fix those hardcoded lists via single list
# Those files must *NOT* be ghosted for *slowdebug* packages
# FIXME - if you are moving jshell or jlink or similar, always modify all three sections
# you can check via headless and devels:
#    rpm -ql --noghost java-11-openjdk-headless-11.0.1.13-8.fc29.x86_64.rpm  | grep bin
# == rpm -ql           java-11-openjdk-headless-slowdebug-11.0.1.13-8.fc29.x86_64.rpm  | grep bin
# != rpm -ql           java-11-openjdk-headless-11.0.1.13-8.fc29.x86_64.rpm  | grep bin
# similarly for other %%{_jvmdir}/{jre,java} and %%{_javadocdir}/{java,java-zip}
%define is_release_build() %( if [ "%{?1}" == "%{debug_suffix_unquoted}" -o "%{?1}" == "%{fastdebug_suffix_unquoted}" ]; then echo "0" ; else echo "1"; fi )

# while JDK is a techpreview(is_system_jdk=0), some provides are turned off. Once jdk stops to be an techpreview, move it to 1
# as sytem JDK, we mean any JDK which can run whole system java stack without issues (like bytecode issues, module issues, dependencies...)
%global is_system_jdk 0

%global aarch64         aarch64 arm64 armv8
# we need to distinguish between big and little endian PPC64
%global ppc64le         ppc64le
%global ppc64be         ppc64 ppc64p7
# Set of architectures which support multiple ABIs
%global multilib_arches %{power64} sparc64 x86_64
# Set of architectures for which we build slowdebug builds
%global debug_arches    %{ix86} x86_64 sparcv9 sparc64 %{aarch64} %{power64} s390x
# Set of architectures for which we build fastdebug builds
%global fastdebug_arches x86_64 ppc64le aarch64
# Set of architectures with a Just-In-Time (JIT) compiler
%global jit_arches      %{arm} %{aarch64} %{ix86} %{power64} s390x sparcv9 sparc64 x86_64 riscv64
# Set of architectures which use the Zero assembler port (!jit_arches)
%global zero_arches ppc s390
# Set of architectures which run a full bootstrap cycle
%global bootstrap_arches %{jit_arches}
# Set of architectures which support SystemTap tapsets
%global systemtap_arches %{jit_arches}
# Set of architectures with a Ahead-Of-Time (AOT) compiler
%global aot_arches      x86_64 %{aarch64}
# Set of architectures which support the serviceability agent
%global sa_arches       %{ix86} x86_64 sparcv9 sparc64 %{aarch64} %{power64} %{arm} riscv64
# Set of architectures which support class data sharing
# As of JDK-8005165 in OpenJDK 10, class sharing is not arch-specific
# However, it does segfault on the Zero assembler port, so currently JIT only
%global share_arches    %{jit_arches}
# Set of architectures for which we build the Shenandoah garbage collector
%global shenandoah_arches x86_64 %{aarch64} riscv64
# Set of architectures for which we build the Z garbage collector
%global zgc_arches x86_64 riscv64
# Set of architectures for which alt-java has SSB mitigation
%global ssbd_arches x86_64
# Set of architectures for which java has short vector math library (libjsvml.so)
%global svml_arches x86_64
# Set of architectures where we verify backtraces with gdb
# s390x fails on RHEL 7 so we exclude it there
%if (0%{?rhel} > 0 && 0%{?rhel} < 8)
%global gdb_arches %{arm} %{aarch64} %{ix86} %{power64} sparcv9 sparc64 x86_64 %{zero_arches}
%else
%global gdb_arches %{jit_arches} %{zero_arches}
%endif

# By default, we build a slowdebug build during main build on JIT architectures
%if %{with slowdebug}
%ifarch %{debug_arches}
%global include_debug_build 1
%else
%global include_debug_build 0
%endif
%else
%global include_debug_build 0
%endif

# On certain architectures, we compile the Shenandoah GC
%ifarch %{shenandoah_arches}
%global use_shenandoah_hotspot 1
%else
%global use_shenandoah_hotspot 0
%endif

# By default, we build a fastdebug build during main build only on fastdebug architectures
%if %{with fastdebug}
%ifarch %{fastdebug_arches}
%global include_fastdebug_build 1
%else
%global include_fastdebug_build 0
%endif
%else
%global include_fastdebug_build 0
%endif

%if %{include_debug_build}
%global slowdebug_build %{debug_suffix}
%else
%global slowdebug_build %{nil}
%endif

%if %{include_fastdebug_build}
%global fastdebug_build %{fastdebug_suffix}
%else
%global fastdebug_build %{nil}
%endif

# If you disable all builds, then the build fails
# Build and test slowdebug first as it provides the best diagnostics
%global build_loop %{slowdebug_build} %{fastdebug_build} %{normal_build}

%if %{include_staticlibs}
%global staticlibs_loop %{staticlibs_suffix}
%else
%global staticlibs_loop %{nil}
%endif

%if 0%{?flatpak}
%global bootstrap_build false
%else
%ifarch %{bootstrap_arches}
%global bootstrap_build true
%else
%global bootstrap_build false
%endif
%endif

%if %{include_staticlibs}
# Extra target for producing the static-libraries. Separate from
# other targets since this target is configured to use in-tree
# AWT dependencies: lcms, libjpeg, libpng, libharfbuzz, giflib
# and possibly others
%global static_libs_target static-libs-image
%else
%global static_libs_target %{nil}
%endif

# The static libraries are produced under the same configuration as the main
# build for portables, as we expect in-tree libraries to be used throughout.
# If system libraries are enabled, the static libraries will also use them
# which may cause issues.
%global bootstrap_targets images %{static_libs_target} legacy-jre-image
%global release_targets images docs-zip %{static_libs_target} legacy-jre-image
# No docs nor bootcycle for debug builds
%global debug_targets images %{static_libs_target} legacy-jre-image
# Target to use to just build HotSpot
%global hotspot_target hotspot

# DTS toolset to use to provide gcc & binutils
%global dtsversion 10

# Disable LTO as this causes build failures at the moment.
# See RHBZ#1861401
%define _lto_cflags %{nil}

# Filter out flags from the optflags macro that cause problems with the OpenJDK build
# We filter out -O flags so that the optimization of HotSpot is not lowered from O3 to O2
# We filter out -Wall which will otherwise cause HotSpot to produce hundreds of thousands of warnings (100+mb logs)
# We replace it with -Wformat (required by -Werror=format-security) and -Wno-cpp to avoid FORTIFY_SOURCE warnings
# We filter out -fexceptions as the HotSpot build explicitly does -fno-exceptions and it's otherwise the default for C++
%global ourflags %(echo %optflags | sed -e 's|-Wall|-Wformat -Wno-cpp|' | sed -r -e 's|-O[0-9]*||')
%global ourcppflags %(echo %ourflags | sed -e 's|-fexceptions||')
%global ourldflags %{__global_ldflags}

# In some cases, the arch used by the JDK does
# not match _arch.
# Also, in some cases, the machine name used by SystemTap
# does not match that given by _target_cpu
%ifarch x86_64
%global archinstall amd64
%global stapinstall x86_64
%endif
%ifarch ppc
%global archinstall ppc
%global stapinstall powerpc
%endif
%ifarch %{ppc64be}
%global archinstall ppc64
%global stapinstall powerpc
%endif
%ifarch %{ppc64le}
%global archinstall ppc64le
%global stapinstall powerpc
%endif
%ifarch %{ix86}
%global archinstall i686
%global stapinstall i386
%endif
%ifarch ia64
%global archinstall ia64
%global stapinstall ia64
%endif
%ifarch s390
%global archinstall s390
%global stapinstall s390
%endif
%ifarch s390x
%global archinstall s390x
%global stapinstall s390
%endif
%ifarch %{arm}
%global archinstall arm
%global stapinstall arm
%endif
%ifarch %{aarch64}
%global archinstall aarch64
%global stapinstall arm64
%endif
%ifarch riscv64
%global archinstall riscv64
%global stapinstall %{_target_cpu}
%endif
# 32 bit sparc, optimized for v9
%ifarch sparcv9
%global archinstall sparc
%global stapinstall %{_target_cpu}
%endif
# 64 bit sparc
%ifarch sparc64
%global archinstall sparcv9
%global stapinstall %{_target_cpu}
%endif
# Need to support noarch for srpm build
%ifarch noarch
%global archinstall %{nil}
%global stapinstall %{nil}
%endif

%ifarch %{systemtap_arches}
%if (0%{?rhel} > 0 && !0%{?epel})
%global with_systemtap 1
%else
%global with_systemtap 0
%endif
%else
%global with_systemtap 0
%endif

# New Version-String scheme-style defines
%global featurever 25
%global interimver 0
%global updatever 0
%global patchver 0
# buildjdkver is usually same as %%{featurever},
# but in time of bootstrap of next jdk, it is featurever-1,
# and this it is better to change it here, on single place
%global buildjdkver 25
# We don't add any LTS designator for STS packages (Fedora and EPEL).
# We need to explicitly exclude EPEL as it would have the %%{rhel} macro defined.
%if 0%{?rhel} && !0%{?epel}
  %global lts_designator "LTS"
  %global lts_designator_zip -%{lts_designator}
%else
  %global lts_designator ""
  %global lts_designator_zip ""
%endif
# JDK to use for bootstrapping
%global bootjdk /usr/lib/jvm/java-%{buildjdkver}-openjdk
# Define whether to use the bootstrap JDK directly or with a fresh libjvm.so
# This will only work where the bootstrap JDK is the same major version
# as the JDK being built
%if %{with fresh_libjvm} && %{buildjdkver} == %{featurever}
%global build_hotspot_first 1
%else
%global build_hotspot_first 0
%endif

# Define vendor information used by OpenJDK
%global oj_vendor Red Hat, Inc.
%global oj_vendor_url https://www.redhat.com/
# Define what url should JVM offer in case of a crash report
# order may be important, epel may have rhel declared
%if 0%{?epel}
%global oj_vendor_bug_url  https://bugzilla.redhat.com/enter_bug.cgi?product=Fedora%20EPEL&component=%{component}&version=epel%{epel}
%else
%if 0%{?fedora}
# Does not work for rawhide, keeps the version field empty
%global oj_vendor_bug_url  https://bugzilla.redhat.com/enter_bug.cgi?product=Fedora&component=%{component}&version=%{fedora}
%else
%if 0%{?rhel}
%global oj_vendor_bug_url https://access.redhat.com/support/cases/
%else
%global oj_vendor_bug_url  https://bugzilla.redhat.com/enter_bug.cgi
%endif
%endif
%endif
%global oj_vendor_version (Red_Hat-%{version}-%{rpmrelease})

# Define IcedTea version used for SystemTap tapsets and desktop file
%global icedteaver      6.0.0pre00-c848b93a8598
# Define current Git revision for the FIPS support patches
# Define JDK versions
%global newjavaver %{featurever}.%{interimver}.%{updatever}.%{patchver}
%global javaver         %{featurever}
# Strip up to 6 trailing zeros in newjavaver, as the JDK does, to get the correct version used in filenames
%global filever %(svn=%{newjavaver}; for i in 1 2 3 4 5 6 ; do svn=${svn%%.0} ; done; echo ${svn})
# The tag used to create the OpenJDK tarball
%global vcstag jdk-%{filever}+%{buildver}%{?tagsuffix:-%{tagsuffix}}

# Standard JPackage naming and versioning defines
%global origin          openjdk
%global origin_nice     OpenJDK
%global top_level_dir_name   %{vcstag}
%global top_level_dir_name_backup %{top_level_dir_name}-backup
%global buildver        32
%global rpmrelease      1
#%%global tagsuffix     %%{nil}
# Priority must be 8 digits in total; up to openjdk 1.8, we were using 18..... so when we moved to 11, we had to add another digit
%if %is_system_jdk
# Using 10 digits may overflow the int used for priority, so we combine the patch and build versions
# It is very unlikely we will ever have a patch version > 4 or a build version > 20, so we combine as (patch * 20) + build.
# This means 11.0.9.0+11 would have had a priority of 11000911 as before
# A 11.0.9.1+1 would have had a priority of 11000921 (20 * 1 + 1), thus ensuring it is bigger than 11.0.9.0+11
%global combiver $( expr 20 '*' %{patchver} + %{buildver} )
%global priority %( printf '%02d%02d%02d%02d' %{featurever} %{interimver} %{updatever} %{combiver} )
%else
# for techpreview, using 1, so slowdebugs can have 0
%global priority %( printf '%08d' 1 )
%endif

# Define milestone (EA for pre-releases, GA for releases)
# Release will be (where N is usually a number starting at 1):
# - 0.N%%{?extraver}%%{?dist} for EA releases,
# - N%%{?extraver}{?dist} for GA releases
%global is_ga           0
%if %{is_ga}
%global build_type GA
%global ea_designator ""
%global ea_designator_zip %{nil}
%global extraver %{nil}
%global eaprefix %{nil}
%else
%global build_type EA
%global ea_designator ea
%global ea_designator_zip -%{ea_designator}
%global extraver .%{ea_designator}
%global eaprefix 0.
%endif

# parametrized macros are order-sensitive
%global compatiblename  java-%{featurever}-%{origin}
%global fullversion     %{compatiblename}-%{version}-%{release}
# images directories from upstream build
%global jdkimage                jdk
%global static_libs_image       static-libs
# output dir stub
%define buildoutputdir() %{expand:build/jdk%{featurever}.build%{?1}}
%define installoutputdir() %{expand:install/jdk%{featurever}.install%{?1}}
%global miscinstalloutputdir install
%global altjavaoutputdir %{miscinstalloutputdir}/altjava.install
%define packageoutputdir() %{expand:packages/jdk%{featurever}.packages%{?1}}
# we can copy the javadoc to not arched dir, or make it not noarch
%define uniquejavadocdir()    %{expand:%{fullversion}.%{_arch}%{?1}}
# main id and dir of this jdk
%define uniquesuffix()        %{expand:%{fullversion}.%{_arch}%{?1}}
# portable only declarations
%global jreimage                jre
%define jreportablenameimpl() %(echo %{uniquesuffix ""} | sed "s;%{version}-%{release};\\0.portable%{1}.jre;g" | sed "s;openjdkportable;el;g")
%define jdkportablenameimpl() %(echo %{uniquesuffix ""} | sed "s;%{version}-%{release};\\0.portable%{1}.jdk;g" | sed "s;openjdkportable;el;g")
%define jdkportablesourcesnameimpl() %(echo %{uniquesuffix ""} | sed "s;%{version}-%{release};\\0.portable%{1}.sources;g" | sed "s;openjdkportable;el;g" | sed "s;.%{_arch};.noarch;g")
%define staticlibsportablenameimpl() %(echo %{uniquesuffix ""} | sed "s;%{version}-%{release};\\0.portable%{1}.static-libs;g" | sed "s;openjdkportable;el;g")
%define jmodsportablenameimpl() %(echo %{uniquesuffix ""} | sed "s;%{version}-%{release};\\0.portable%{1}.jmods;g" | sed "s;openjdkportable;el;g")
%define jreportablearchive()  %{expand:%{jreportablenameimpl -- %%{1}}.tar.xz}
%define jdkportablearchive()  %{expand:%{jdkportablenameimpl -- %%{1}}.tar.xz}
%define jdkportablesourcesarchive()  %{expand:%{jdkportablesourcesnameimpl -- %%{1}}.tar.xz}
%define staticlibsportablearchive()  %{expand:%{staticlibsportablenameimpl -- %%{1}}.tar.xz}
%define jmodsportablearchive()  %{expand:%{jmodsportablenameimpl -- %%{1}}.tar.xz}
%define jreportablename()     %{expand:%{jreportablenameimpl -- %%{1}}}
%define jdkportablename()     %{expand:%{jdkportablenameimpl -- %%{1}}}
%define jdkportablesourcesname()     %{expand:%{jdkportablesourcesnameimpl -- %%{1}}}
# Intentionally use jdkportablenameimpl here since we want to have static-libs files overlayed on
# top of the JDK archive
%define staticlibsportablename()     %{expand:%{jdkportablenameimpl -- %%{1}}}
%define docportablename() %(echo %{uniquesuffix ""} | sed "s;%{version}-%{release};\\0.portable.docs;g" | sed "s;openjdkportable;el;g")
%define docportablearchive()  %{docportablename}.tar.xz
%define miscportablename() %(echo %{uniquesuffix ""} | sed "s;%{version}-%{release};\\0.portable.misc;g" | sed "s;openjdkportable;el;g")
%define miscportablearchive()  %{miscportablename}.tar.xz

# RPM 4.19 no longer accept our double percentaged %%{nil} passed to %%{1}
# so we have to pass in "" but evaluate it, otherwise files record will include it
%define jreportablearchiveForFiles()  %(echo %{jreportablearchive -- ""})
%define jdkportablearchiveForFiles()  %(echo %{jdkportablearchive -- ""})
%define jdkportablesourcesarchiveForFiles()  %(echo %{jdkportablesourcesarchive -- ""})
%define staticlibsportablearchiveForFiles()  %(echo %{staticlibsportablearchive -- ""})
%define jmodsportablearchiveForFiles()  %(echo %{jmodsportablearchive -- ""})

#################################################################
# fix for https://bugzilla.redhat.com/show_bug.cgi?id=1111349
#         https://bugzilla.redhat.com/show_bug.cgi?id=1590796#c14
#         https://bugzilla.redhat.com/show_bug.cgi?id=1655938
%global _privatelibs libsplashscreen[.]so.*|libawt_xawt[.]so.*|libjli[.]so.*|libattach[.]so.*|libawt[.]so.*|libextnet[.]so.*|libawt_headless[.]so.*|libdt_socket[.]so.*|libfontmanager[.]so.*|libinstrument[.]so.*|libj2gss[.]so.*|libj2pcsc[.]so.*|libj2pkcs11[.]so.*|libjaas[.]so.*|libjavajpeg[.]so.*|libjdwp[.]so.*|libjimage[.]so.*|libjsound[.]so.*|liblcms[.]so.*|libmanagement[.]so.*|libmanagement_agent[.]so.*|libmanagement_ext[.]so.*|libmlib_image[.]so.*|libnet[.]so.*|libnio[.]so.*|libprefs[.]so.*|librmi[.]so.*|libsaproc[.]so.*|libsctp[.]so.*|libsystemconf[.]so.*|libzip[.]so.*%{freetype_lib}
%global _publiclibs libjawt[.]so.*|libjava[.]so.*|libjvm[.]so.*|libverify[.]so.*|libjsig[.]so.*
%if %is_system_jdk
%global __provides_exclude ^(%{_privatelibs})$
%global __requires_exclude ^(%{_privatelibs})$
# Never generate lib-style provides/requires for any debug packages
%global __provides_exclude_from ^.*/%{uniquesuffix -- %{debug_suffix_unquoted}}/.*$
%global __requires_exclude_from ^.*/%{uniquesuffix -- %{debug_suffix_unquoted}}/.*$
%global __provides_exclude_from ^.*/%{uniquesuffix -- %{fastdebug_suffix_unquoted}}/.*$
%global __requires_exclude_from ^.*/%{uniquesuffix -- %{fastdebug_suffix_unquoted}}/.*$
%else
# Don't generate provides/requires for JDK provided shared libraries at all.
%global __provides_exclude ^(%{_privatelibs}|%{_publiclibs})$
%global __requires_exclude ^(%{_privatelibs}|%{_publiclibs})$
%endif

# VM variant being built
%ifarch %{zero_arches}
%global vm_variant zero
%else
%global vm_variant server
%endif

%global etcjavasubdir     %{_sysconfdir}/java/java-%{javaver}-%{origin}
%define etcjavadir()      %{expand:%{etcjavasubdir}/%{uniquesuffix -- %{?1}}}
# Standard JPackage directories and symbolic links.
%define sdkdir()        %{expand:%{uniquesuffix -- %{?1}}}
%define jrelnk()        %{expand:jre-%{javaver}-%{origin}-%{version}-%{release}.%{_arch}%{?1}}

%define sdkbindir()     %{expand:%{_jvmdir}/%{sdkdir -- %{?1}}/bin}
%define jrebindir()     %{expand:%{_jvmdir}/%{sdkdir -- %{?1}}/bin}

%global alt_java_name     alt-java
%global generated_sources_name     generated_sources

%global rpm_state_dir %{_localstatedir}/lib/rpm-state/

# For flatpack builds hard-code /usr/sbin/alternatives,
# otherwise use %%{_sbindir} relative path.
%if 0%{?flatpak}
%global alternatives_requires /usr/sbin/alternatives
%else
%global alternatives_requires %{_sbindir}/alternatives
%endif

# x86 is no longer supported
%if 0%{?java_arches:1}
ExclusiveArch:  %{java_arches}
%else
ExcludeArch: %{ix86}
%endif

# Portables have no repo (requires/provides), but these are awesome for orientation in spec
# Also scriptlets are happily missing and files are handled old fashion
# not-duplicated requires/provides/obsoletes for normal/debug packages
%define java_rpo() %{expand:
}

%define java_devel_rpo() %{expand:
}

%define java_static_libs_rpo() %{expand:
}

%define java_docs_rpo() %{expand:
}

%define java_misc_rpo() %{expand:
}

# Prevent brp-java-repack-jars from being run
%global __jar_repack 0

# portables have grown out of its component, moving back to java-x-vendor
# this expression, when declared as global, filled component with java-x-vendor portable
%define component %(echo %{name} | sed "s;-portable%{?pkgos:-%{pkgos}};;g")

Name:    java-25-%{origin}-portable%{?pkgos:-%{pkgos}}
Version: %{newjavaver}.%{buildver}
Release: %{?eaprefix}%{rpmrelease}%{?extraver}%{?dist}
# java-1.5.0-ibm from jpackage.org set Epoch to 1 for unknown reasons
# and this change was brought into RHEL-4. java-1.5.0-ibm packages
# also included the epoch in their virtual provides. This created a
# situation where in-the-wild java-1.5.0-ibm packages provided "java =
# 1:1.5.0". In RPM terms, "1.6.0 < 1:1.5.0" since 1.6.0 is
# interpreted as 0:1.6.0. So the "java >= 1.6.0" requirement would be
# satisfied by the 1:1.5.0 packages. Thus we need to set the epoch in
# JDK package >= 1.6.0 to 1, and packages referring to JDK virtual
# provides >= 1.6.0 must specify the epoch, "java >= 1:1.6.0".

Epoch:   1
Summary: %{origin_nice} %{featurever} Runtime Environment portable edition
# Groups are only used up to RHEL 8 and on Fedora versions prior to F30
%if (0%{?rhel} > 0 && 0%{?rhel} <= 8) || (0%{?fedora} >= 0 && 0%{?fedora} < 30)
Group:   Development/Languages
%endif

# HotSpot code is licensed under GPLv2
# JDK library code is licensed under GPLv2 with the Classpath exception
# The Apache license is used in code taken from Apache projects (primarily xalan & xerces)
# DOM levels 2 & 3 and the XML digital signature schemas are licensed under the W3C Software License
# The JSR166 concurrency code is in the public domain
# The BSD and MIT licenses are used for a number of third-party libraries (see ADDITIONAL_LICENSE_INFO)
# The OpenJDK source tree includes:
# - JPEG library (IJG), zlib & libpng (zlib), giflib (MIT), harfbuzz (ISC),
# - freetype (FTL), jline (BSD) and LCMS (MIT)
# - jquery (MIT), jdk.crypto.cryptoki PKCS 11 wrapper (RSA)
# - public_suffix_list.dat from publicsuffix.org (MPLv2.0)
# The test code includes copies of NSS under the Mozilla Public License v2.0
# The PCSClite headers are under a BSD with advertising license
# The elliptic curve cryptography (ECC) source code is licensed under the LGPLv2.1 or any later version
# Automatically converted from old format: ASL 1.1 and ASL 2.0 and BSD and BSD with advertising and GPL+ and GPLv2 and GPLv2 with exceptions and IJG and LGPLv2+ and MIT and MPLv2.0 and Public Domain and W3C and zlib and ISC and FTL and RSA - review is highly recommended.
License:  Apache-1.1 AND Apache-2.0 AND LicenseRef-Callaway-BSD AND LicenseRef-Callaway-BSD-with-advertising AND GPL-1.0-or-later AND GPL-2.0-only AND LicenseRef-Callaway-GPLv2-with-exceptions AND IJG AND LicenseRef-Callaway-LGPLv2+ AND LicenseRef-Callaway-MIT AND MPL-2.0 AND LicenseRef-Callaway-Public-Domain AND W3C AND Zlib AND ISC AND FTL AND LicenseRef-RSA
URL:      http://openjdk.java.net/

# The source tarball, generated using generate_source_tarball.sh
Source0: https://openjdk-sources.osci.io/openjdk%{featurever}/open%{vcstag}%{ea_designator_zip}.tar.xz

# Use 'icedtea_sync.sh' to update the following
# They are based on code contained in the IcedTea project (6.x).
# Systemtap tapsets. Zipped up to keep it small.
# Disabled in portables
#Source8: tapsets-icedtea-%%{icedteaver}.tar.xz

# Desktop files. Adapted from IcedTea
# Disabled in portables
#Source9: jconsole.desktop.in

# Release notes
Source10: NEWS

# Source code for alt-java
Source11: alt-java.c

# Removed libraries that we link instead
Source12: remove-intree-libraries.sh

# Ensure we aren't using the limited crypto policy
Source13: TestCryptoLevel.java

# Ensure ECDSA is working
Source14: TestECDSA.java

# Verify system crypto (policy) can be disabled via a property
Source15: TestSecurityProperties.java

# Ensure vendor settings are correct
Source16: CheckVendor.java

# Ensure translations are available for new timezones
Source18: TestTranslations.java

############################################
#
# RPM/distribution specific patches
#
############################################
# Crypto policy and FIPS support patches
# Patch is generated from the fips-21u tree at https://github.com/rh-openjdk/jdk/tree/fips-21u
# as follows: git diff %%{vcstag} src make test > fips-21u-$(git show -s --format=%h HEAD).patch
# Diff is limited to src and make subdirectories to exclude .github changes
# The following list is generated by:
# git log %%{vcstag}.. --no-merges --format=%s --reverse:
# Fixes currently included:
# PR3183, RH1340845: Follow system wide crypto policy
# PR3695: Allow use of system crypto policy to be disabled by the user
# RH1655466: Support RHEL FIPS mode using SunPKCS11 provider
# RH1818909: No ciphersuites availale for SSLSocket in FIPS mode
# RH1860986: Disable TLSv1.3 with the NSS-FIPS provider until PKCS#11 v3.0 support is available
# RH1915071: Always initialise JavaSecuritySystemConfiguratorAccess
# RH1929465: Improve system FIPS detection
# RH1995150: Disable non-FIPS crypto in SUN and SunEC security providers
# RH1996182: Login to the NSS software token in FIPS mode
# RH1991003: Allow plain key import unless com.redhat.fips.plainKeySupport is set to false
# RH2021263: Resolve outstanding FIPS issues
# RH2052819: Fix FIPS reliance on crypto policies
# RH2052829: Detect NSS at Runtime for FIPS detection
# RH2052070: Enable AlgorithmParameters and AlgorithmParameterGenerator services in FIPS mode
# RH2023467: Enable FIPS keys export
# RH2094027: SunEC runtime permission for FIPS
# RH2036462: sun.security.pkcs11.wrapper.PKCS11.getInstance breakage
# RH2090378: Revert to disabling system security properties and FIPS mode support together
# RH2104724: Avoid import/export of DH private keys
# RH2092507: P11Key.getEncoded does not work for DH keys in FIPS mode
# Build the systemconf library on all platforms
# RH2048582: Support PKCS#12 keystores [now part of JDK-8301553 upstream]
# RH2020290: Support TLS 1.3 in FIPS mode
# Add nss.fips.cfg support to OpenJDK tree
# RH2117972: Extend the support for NSS DBs (PKCS11) in FIPS mode
# Remove forgotten dead code from RH2020290 and RH2104724
# OJ1357: Fix issue on FIPS with a SecurityManager in place
# RH2134669: Add missing attributes when registering services in FIPS mode.
# test/jdk/sun/security/pkcs11/fips/VerifyMissingAttributes.java: fixed jtreg main class
# RH1940064: Enable XML Signature provider in FIPS mode
# RH2173781: Avoid calling C_GetInfo() too early, before cryptoki is initialized [now part of JDK-8301553 upstream]

#############################################
#
# OpenJDK patches in need of upstreaming
#
#############################################

# Currently empty

#############################################
#
# OpenJDK patches which missed last update
#
#############################################

# Currently empty

#############################################
#
# Portable build specific patches
#
#############################################

# Currently empty

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: alsa-lib-devel
BuildRequires: binutils
BuildRequires: cups-devel
BuildRequires: desktop-file-utils
# elfutils only are OK for build without AOT
BuildRequires: elfutils-devel
BuildRequires: file
BuildRequires: fontconfig-devel
%if (0%{?rhel} > 0 && 0%{?rhel} < 8)
BuildRequires: devtoolset-%{dtsversion}-gcc
BuildRequires: devtoolset-%{dtsversion}-gcc-c++
%else
BuildRequires: gcc
# gcc-c++ is already needed
%endif
BuildRequires: gcc-c++
BuildRequires: gdb
%if (0%{?rhel} > 0 && 0%{?rhel} < 8)
# rhel7 only, portables only. Rhel8 have gtk3, rpms have runtime recommends of gtk
BuildRequires: gtk2-devel
%endif
BuildRequires: libxslt
BuildRequires: libX11-devel
BuildRequires: libXi-devel
BuildRequires: libXinerama-devel
BuildRequires: libXrandr-devel
BuildRequires: libXrender-devel
BuildRequires: libXt-devel
BuildRequires: libXtst-devel
# Requirement for setting up nss.fips.cfg
BuildRequires: nss-devel
# Requirement for system security property test
# N/A for portable. RHEL7 doesn't provide them
#BuildRequires: crypto-policies
BuildRequires: pkgconfig
BuildRequires: xorg-x11-proto-devel
BuildRequires: zip
# to pack portable tarballs
BuildRequires: tar
BuildRequires: unzip
%if (0%{?rhel} > 0 && 0%{?rhel} < 8)
BuildRequires: javapackages-tools
BuildRequires: java-%{buildjdkver}-%{origin}%{?pkgos:-%{pkgos}}-devel
%else
BuildRequires: javapackages-filesystem
%endif
# Zero-assembler build requirement
%ifarch %{zero_arches}
BuildRequires: libffi-devel
%endif
# Full documentation build requirements
BuildRequires: graphviz
BuildRequires: pandoc
# 2023c required as of JDK-8305113
BuildRequires: tzdata-java >= 2023c
# cacerts build requirement in portable mode
BuildRequires: ca-certificates
# Earlier versions have a bug in tree vectorization on PPC
BuildRequires: gcc >= 4.8.3-8

%if %{with_systemtap}
BuildRequires: systemtap-sdt-devel
%endif
BuildRequires: make

%if %{system_libs}
BuildRequires: freetype-devel
BuildRequires: giflib-devel
BuildRequires: harfbuzz-devel
BuildRequires: lcms2-devel
BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: zlib-devel
%else
# Version in src/java.desktop/share/legal/freetype.md
Provides: bundled(freetype) = 2.13.3
# Version in src/java.desktop/share/native/libsplashscreen/giflib/gif_lib.h
Provides: bundled(giflib) = 5.2.2
# Version in src/java.desktop/share/native/libharfbuzz/hb-version.h
Provides: bundled(harfbuzz) = 10.4.0
# Version in src/java.desktop/share/native/liblcms/lcms2.h
Provides: bundled(lcms2) = 2.17.0
# Version in src/java.desktop/share/native/libjavajpeg/jpeglib.h
Provides: bundled(libjpeg) = 6b
# Version in src/java.desktop/share/native/libsplashscreen/libpng/png.h
Provides: bundled(libpng) = 1.6.47
# Version in src/java.base/share/native/libzip/zlib/zlib.h
Provides: bundled(zlib) = 1.3.1
# We link statically against libstdc++ to increase portability
BuildRequires: libstdc++-static
%endif

# this is always built, also during debug-only build
# when it is built in debug-only this package is just placeholder
%{java_rpo %{nil}}

BuildRequires: java-25-openjdk-devel
%description
The %{origin_nice} %{featurever} runtime environment - portable edition.

%if %{include_debug_build}
%package slowdebug
Summary: %{origin_nice} %{featurever} Runtime Environment portable edition %{debug_on}
%if (0%{?rhel} > 0 && 0%{?rhel} <= 8) || (0%{?fedora} >= 0 && 0%{?fedora} < 30)
Group:   Development/Languages
%endif

%{java_rpo -- %{debug_suffix_unquoted}}
%description slowdebug
The %{origin_nice} %{featurever} runtime environment - portable edition.
%{debug_warning}
%endif

%if %{include_fastdebug_build}
%package fastdebug
Summary: %{origin_nice} %{featurever} Runtime Environment portable edition %{fastdebug_on}
%if (0%{?rhel} > 0 && 0%{?rhel} <= 8) || (0%{?fedora} >= 0 && 0%{?fedora} < 30)
Group:   Development/Languages
%endif

%{java_rpo -- %{fastdebug_suffix_unquoted}}
%description fastdebug
The %{origin_nice} %{featurever} runtime environment - portable edition.
%{fastdebug_warning}
%endif

%if %{include_normal_build}
%package devel
Summary: %{origin_nice} %{featurever} Development Environment portable edition
%if (0%{?rhel} > 0 && 0%{?rhel} <= 8) || (0%{?fedora} >= 0 && 0%{?fedora} < 30)
Group:   Development/Languages
%endif

%{java_devel_rpo %{nil}}

%description devel
The %{origin_nice} %{featurever} development tools - portable edition.
%endif

%if %{include_debug_build}
%package devel-slowdebug
Summary: %{origin_nice} %{featurever} Runtime and Development Environment portable edition %{debug_on}
%if (0%{?rhel} > 0 && 0%{?rhel} <= 8) || (0%{?fedora} >= 0 && 0%{?fedora} < 30)
Group:   Development/Languages
%endif

%{java_devel_rpo -- %{debug_suffix_unquoted}}

%description devel-slowdebug
The %{origin_nice} %{featurever} development tools - portable edition.
%{debug_warning}
%endif

%if %{include_fastdebug_build}
%package devel-fastdebug
Summary: %{origin_nice} %{featurever} Runtime and Development Environment portable edition %{fastdebug_on}
%if (0%{?rhel} > 0 && 0%{?rhel} <= 8) || (0%{?fedora} >= 0 && 0%{?fedora} < 30)
Group:   Development/Tools
%endif

%{java_devel_rpo -- %{fastdebug_suffix_unquoted}}

%description devel-fastdebug
The %{origin_nice} %{featurever} runtime environment and development tools - portable edition
%{fastdebug_warning}
%endif

%if %{include_staticlibs}

%if %{include_normal_build}
%package static-libs
Summary: %{origin_nice} %{featurever} libraries for static linking - portable edition

%{java_static_libs_rpo %{nil}}

%description static-libs
The %{origin_nice} %{featurever} libraries for static linking - portable edition.
%endif

%if %{include_debug_build}
%package static-libs-slowdebug
Summary: %{origin_nice} %{featurever} libraries for static linking - portable edition %{debug_on}

%{java_static_libs_rpo -- %{debug_suffix_unquoted}}

%description static-libs-slowdebug
The %{origin_nice} %{featurever} libraries for static linking - portable edition
%{debug_warning}
%endif

%if %{include_fastdebug_build}
%package static-libs-fastdebug
Summary: %{origin_nice} %{featurever} libraries for static linking - portable edition %{fastdebug_on}

%{java_static_libs_rpo -- %{fastdebug_suffix_unquoted}}

%description static-libs-fastdebug
The %{origin_nice} %{featurever} libraries for static linking - portable edition
%{fastdebug_warning}
%endif

# staticlibs
%endif

%if %{include_normal_build}
%package docs
Summary: %{origin_nice} %{featurever} API documentation

%{java_docs_rpo %{nil}}

%description docs
The %{origin_nice} %{featurever} API documentation.

%package misc
Summary: %{origin_nice} %{featurever} miscellany

%{java_misc_rpo %{nil}}

%description misc
The %{origin_nice} %{featurever} miscellany.
%endif

%package sources
Summary: %{origin_nice} %{featurever} full patched sources of portable JDK

%description sources
The %{origin_nice} %{featurever} full patched sources of portable JDK to build, attach to debuggers or for debuginfo

%prep

echo "Preparing %{oj_vendor_version}"

# Using the echo macro breaks rpmdev-bumpspec, as it parses the first line of stdout :-(
%if 0%{?_build_cpu:1}
  echo "CPU: %{_target_cpu}, arch install directory: %{archinstall}, SystemTap install directory: %{_build_cpu}"
%else
  %{error:Unrecognised architecture %{_build_cpu}}
%endif

if [ %{include_normal_build} -eq 0 -o  %{include_normal_build} -eq 1 ] ; then
  echo "include_normal_build is %{include_normal_build}"
else
  echo "include_normal_build is %{include_normal_build}, that is invalid. Use 1 for yes or 0 for no"
  exit 11
fi
if [ %{include_debug_build} -eq 0 -o  %{include_debug_build} -eq 1 ] ; then
  echo "include_debug_build is %{include_debug_build}"
else
  echo "include_debug_build is %{include_debug_build}, that is invalid. Use 1 for yes or 0 for no"
  exit 12
fi
if [ %{include_fastdebug_build} -eq 0 -o  %{include_fastdebug_build} -eq 1 ] ; then
  echo "include_fastdebug_build is %{include_fastdebug_build}"
else
  echo "include_fastdebug_build is %{include_fastdebug_build}, that is invalid. Use 1 for yes or 0 for no"
  exit 13
fi
if [ %{include_debug_build} -eq 0 -a  %{include_normal_build} -eq 0 -a  %{include_fastdebug_build} -eq 0 ] ; then
  echo "You have disabled all builds (normal,fastdebug,slowdebug). That is a no go."
  exit 14
fi

%if %{with fresh_libjvm} && ! %{build_hotspot_first}
echo "WARNING: The build of a fresh libjvm has been disabled due to a JDK version mismatch"
echo "Build JDK version is %{buildjdkver}, feature JDK version is %{featurever}"
%endif

export XZ_OPT="-T0"
%setup -q -c -n %{uniquesuffix ""} -T -a 0
# https://bugzilla.redhat.com/show_bug.cgi?id=1189084
prioritylength=`expr length %{priority}`
if [ $prioritylength -ne 8 ] ; then
 echo "priority must be 8 digits in total, violated"
 exit 14
fi

# OpenJDK patches
%if %{system_libs}
# Remove libraries that are linked by both static and dynamic builds
sh %{SOURCE12} %{top_level_dir_name}
%endif

# Patch the JDK
pushd %{top_level_dir_name}
# Add crypto policy and FIPS support
# Skipping fips patch whil eit is not ready for jdk22 %%patch -P1001 -p1
# Patches in need of upstreaming
popd # openjdk


# The OpenJDK version file includes the current
# upstream version information. For some reason,
# configure does not automatically use the
# default pre-version supplied there (despite
# what the file claims), so we pass it manually
# to configure
VERSION_FILE=$(pwd)/%{top_level_dir_name}/make/conf/version-numbers.conf
if [ -f ${VERSION_FILE} ] ; then
    UPSTREAM_EA_DESIGNATOR=$(grep '^DEFAULT_PROMOTED_VERSION_PRE' ${VERSION_FILE} | cut -d '=' -f 2)
else
    echo "Could not find OpenJDK version file.";
    exit 16
fi
if [ "x${UPSTREAM_EA_DESIGNATOR}" != "x%{ea_designator}" ] ; then
    echo "WARNING: Designator mismatch";
    echo "Spec file is configured for a %{build_type} build with designator '%{ea_designator}'"
    echo "Upstream version-pre setting is '${UPSTREAM_EA_DESIGNATOR}'";
    #exit 17
fi

# Systemtap is processed in rpms

# Prepare desktop files
# Portables do not have desktop integration

%build

# How many CPU's do we have?
export NUM_PROC=%(/usr/bin/getconf _NPROCESSORS_ONLN 2> /dev/null || :)
export NUM_PROC=${NUM_PROC:-1}
%if 0%{?_smp_ncpus_max}
# Honor %%_smp_ncpus_max
[ ${NUM_PROC} -gt %{?_smp_ncpus_max} ] && export NUM_PROC=%{?_smp_ncpus_max}
%endif

%ifarch s390x sparc64 alpha %{power64} %{aarch64} riscv64
export ARCH_DATA_MODEL=64
%endif
%ifarch alpha
export CFLAGS="$CFLAGS -mieee"
%endif

# We use ourcppflags because the OpenJDK build seems to
# pass EXTRA_CFLAGS to the HotSpot C++ compiler...
# Explicitly set the C++ standard as the default has changed on GCC >= 6
EXTRA_CFLAGS="%ourcppflags"
EXTRA_CPP_FLAGS="%ourcppflags"

%ifarch %{power64} ppc
# fix rpmlint warnings
EXTRA_CFLAGS="$EXTRA_CFLAGS -fno-strict-aliasing"
%endif
%ifarch %{ix86}
# Align stack boundary on x86_32
EXTRA_CFLAGS="$(echo ${EXTRA_CFLAGS} | sed -e 's|-mstackrealign|-mincoming-stack-boundary=2 -mpreferred-stack-boundary=4|')"
EXTRA_CPP_FLAGS="$(echo ${EXTRA_CPP_FLAGS} | sed -e 's|-mstackrealign|-mincoming-stack-boundary=2 -mpreferred-stack-boundary=4|')"
%endif
export EXTRA_CFLAGS EXTRA_CPP_FLAGS

echo "Building %{SOURCE11}"
mkdir %{miscinstalloutputdir}
mkdir %{altjavaoutputdir}
gcc ${EXTRA_CFLAGS} -o %{altjavaoutputdir}/%{alt_java_name} %{SOURCE11}

echo "Building %{newjavaver}-%{buildver}, pre=%{ea_designator}, opt=%{lts_designator}"

function buildjdk() {
    local outputdir=${1}
    local buildjdk=${2}
    local maketargets="${3}"
    local debuglevel=${4}
    local link_opt=${5}
    local debug_symbols=${6}

    local top_dir_abs_src_path=$(pwd)/%{top_level_dir_name}
    local top_dir_abs_build_path=$(pwd)/${outputdir}

    # This must be set using the global, so that the
    # static libraries still use a dynamic stdc++lib
    if [ "x%{link_type}" = "xbundled" ] ; then
        libc_link_opt="static";
    else
        libc_link_opt="dynamic";
    fi

    echo "Using output directory: ${outputdir}";
    echo "Checking build JDK ${buildjdk} is operational..."
    ${buildjdk}/bin/java -version
    echo "Using make targets: ${maketargets}"
    echo "Using debuglevel: ${debuglevel}"
    echo "Using link_opt: ${link_opt}"
    echo "Using debug_symbols: ${debug_symbols}"
    echo "Building %{newjavaver}-%{buildver}, pre=%{ea_designator}, opt=%{lts_designator}"

    mkdir -p ${outputdir}
    pushd ${outputdir}

    # Note: zlib and freetype use %{link_type}
    # rather than ${link_opt} as the system versions
    # are always used in a system_libs build, even
    # for the static library build
%if (0%{?rhel} > 0 && 0%{?rhel} < 8)
    scl enable devtoolset-%{dtsversion} -- bash ${top_dir_abs_src_path}/configure \
%else
    bash ${top_dir_abs_src_path}/configure \
%endif
%ifarch %{zero_arches}
    --with-jvm-variants=zero \
%endif
%ifarch %{ppc64le}
    --with-jobs=1 \
%endif
    --with-version-build=%{buildver} \
    --with-version-pre="%{ea_designator}" \
    --with-version-opt="%{lts_designator}" \
    --with-vendor-version-string="%{oj_vendor_version}" \
    --with-vendor-name="%{oj_vendor}" \
    --with-vendor-url="%{oj_vendor_url}" \
    --with-vendor-bug-url="%{oj_vendor_bug_url}" \
    --with-vendor-vm-bug-url="%{oj_vendor_bug_url}" \
    --with-boot-jdk=${buildjdk} \
    --with-debug-level=${debuglevel} \
    --with-native-debug-symbols="${debug_symbols}" \
    --disable-absolute-paths-in-output \
    --enable-unlimited-crypto \
    --enable-linkable-runtime \
    --enable-keep-packaged-modules \
    --with-zlib=%{link_type} \
    --with-freetype=%{link_type} \
    --with-libjpeg=${link_opt} \
    --with-giflib=${link_opt} \
    --with-libpng=${link_opt} \
    --with-lcms=${link_opt} \
    --with-harfbuzz=${link_opt} \
    --with-stdc++lib=${libc_link_opt} \
    --with-extra-cxxflags="$EXTRA_CPP_FLAGS" \
    --with-extra-cflags="$EXTRA_CFLAGS" \
    --with-extra-ldflags="%{ourldflags}" \
    --with-num-cores="$NUM_PROC" \
    --with-source-date="${SOURCE_DATE_EPOCH}" \
    --disable-javac-server \
%ifarch %{zgc_arches}
    --with-jvm-features=zgc \
%endif
    --disable-warnings-as-errors

    cat spec.gmk
%if (0%{?rhel} > 0 && 0%{?rhel} < 8)
    scl enable devtoolset-%{dtsversion} -- make \
%else
    make \
%endif
      LOG=trace \
      WARNINGS_ARE_ERRORS="-Wno-error" \
      CFLAGS_WARNINGS_ARE_ERRORS="-Wno-error" \
      $maketargets || ( pwd; find ${top_dir_abs_src_path} ${top_dir_abs_build_path} -name "hs_err_pid*.log" | xargs cat && false )
    popd
}

function installjdk() {
    local outputdir=${1}
    local installdir=${2}
    local jdkimagepath=${installdir}/images/%{jdkimage}
    local jreimagepath=${installdir}/images/%{jreimage}

    echo "Installing build from ${outputdir} to ${installdir}..."
    mkdir -p ${installdir}
    echo "Installing images..."
    mv ${outputdir}/images ${installdir}
    if [ -d ${outputdir}/bundles ] ; then
        echo "Installing bundles...";
        mv ${outputdir}/bundles ${installdir} ;
    fi

%if !%{with artifacts}
    echo "Removing output directory...";
    rm -rf ${outputdir}
%endif

    # legacy-jre-image target does not install any man pages for the JRE
    # We copy the jdk man directory and then remove pages for binaries that
    # don't exist in the JRE
    cp -a ${jdkimagepath}/man ${jreimagepath}
    for manpage in $(find ${jreimagepath}/man -name '*.1'); do
        filename=$(basename ${manpage});
        binary=${filename/.1/};
        if [ ! -f ${jreimagepath}/bin/${binary} ] ; then
            echo "Removing ${manpage} from JRE for which no binary ${binary} exists";
            rm -f ${manpage};
        fi;
    done

    for imagepath in ${jdkimagepath} ${jreimagepath}; do

        if [ -d ${imagepath} ] ; then
            # the build (erroneously) removes read permissions from some jars
            # this is a regression in OpenJDK 7 (our compiler):
            # http://icedtea.classpath.org/bugzilla/show_bug.cgi?id=1437
            find ${imagepath} -iname '*.jar' -exec chmod ugo+r {} \;

            # Build screws up permissions on binaries
            # https://bugs.openjdk.java.net/browse/JDK-8173610
            find ${imagepath} -iname '*.so' -exec chmod +x {} \;
            find ${imagepath}/bin/ -exec chmod +x {} \;

            # Install local files which are distributed with the JDK
            install -m 644 %{SOURCE10} ${imagepath}

            # Create fake alt-java as a placeholder for future alt-java
            pushd ${imagepath}
            # add alt-java man page
            echo "Hardened java binary recommended for launching untrusted code from the Web e.g. javaws" > man/man1/%{alt_java_name}.1
            cat man/man1/java.1 >> man/man1/%{alt_java_name}.1
            popd

            # Print release information
            cat ${imagepath}/release
        fi
    done
}

function genchecksum() {
    local checkedfile=${1}

    checkdir=$(dirname ${1})
    checkfile=$(basename ${1})

    echo "Generating checksum for ${checkfile} in ${checkdir}..."
    pushd ${checkdir}
    sha256sum ${checkfile} > ${checkfile}.sha256sum
    sha256sum --check ${checkfile}.sha256sum
    popd
}

function packFullPatchedSources() {
  srcpackagesdir=`pwd`
  tar -cJf ${srcpackagesdir}/%{jdkportablesourcesarchive -- ""} --transform "s|^|%{jdkportablesourcesname -- ""}/|" %{top_level_dir_name}
  genchecksum ${srcpackagesdir}/%{jdkportablesourcesarchive -- ""}
}

function findgeneratedsources() {
  local targetDir=${1}
  local targetDirParent=$(dirname ${targetDir})
  local builtJdk=${2}
  local builtJdkName=$(basename ${builtJdk})
  local sources=${3}
  local sourcesName=$(basename ${sources})
  local sourcesParent=$(dirname ${sources})
  local target=${sourcesParent}/${targetDirParent}/%{generated_sources_name}
  local suffixes="cpp\|hpp\|h\|hh\|rl"
  suffixes=".*\.\($suffixes\)$"
  mkdir -p $target
  pushd ${builtJdk}
    mkdir -p ${target}/${builtJdkName}
    cp --parents $(find . | grep -e "$suffixes" -e "NONE$") ${target}/${builtJdkName}
  popd
  pushd ${sources}
    mkdir -p ${target}/${sourcesName}
    cp --parents $(find make | grep -e ".$suffixes" -e "NONE$") ${target}/${sourcesName}
  popd
}

function packagejdk() {
    local imagesdir=$(pwd)/${1}/images
    local docdir=$(pwd)/${1}/images/docs
    local bundledir=$(pwd)/${1}/bundles
    local packagesdir=$(pwd)/${2}
    local srcdir=$(pwd)/%{top_level_dir_name}
    local tapsetdir=$(pwd)/tapset
    local altjavadir=$(pwd)/${3}
    local gensources=$(pwd)/%{miscinstalloutputdir}/%{generated_sources_name}

    echo "Packaging build from ${imagesdir} to ${packagesdir}..."
    mkdir -p ${packagesdir}
    pushd ${imagesdir}

    if [ "x$suffix" = "x" ] ; then
        nameSuffix=""
    else
        nameSuffix=`echo "$suffix"| sed s/-/./`
    fi

    jdkname=%{jdkportablename -- "$nameSuffix"}
    jdkarchive=${packagesdir}/%{jdkportablearchive -- "$nameSuffix"}
    jmodsarchive=${packagesdir}/%{jmodsportablearchive -- "$nameSuffix"}
    jrename=%{jreportablename -- "$nameSuffix"}
    jrearchive=${packagesdir}/%{jreportablearchive -- "$nameSuffix"}
    staticname=%{staticlibsportablename -- "$nameSuffix"}
    staticarchive=${packagesdir}/%{staticlibsportablearchive -- "$nameSuffix"}
    debugarchive=${packagesdir}/%{jdkportablearchive -- "${nameSuffix}.debuginfo"}
    if [ "x$suffix" = "x" ] ; then
      docname=%{docportablename}
      docarchive=${packagesdir}/%{docportablearchive}
      built_doc_archive=jdk-%{filever}%{ea_designator_zip}+%{buildver}%{lts_designator_zip}-docs.zip
    fi
    # These are from the source tree so no debug variants
    miscname=%{miscportablename}
    miscarchive=${packagesdir}/%{miscportablearchive}

    # Rename directories for packaging
    mv %{jdkimage} ${jdkname}
    mv %{jreimage} ${jrename}

    # Release images have external debug symbols
    if [ "x$suffix" = "x" ] ; then
        tar -cJf ${debugarchive} $(find ${jdkname} -name \*.debuginfo)
        genchecksum ${debugarchive}

        mkdir ${docname}
        mv ${docdir} ${docname}
        mv ${bundledir}/${built_doc_archive} ${docname}
        tar -cJf ${docarchive} ${docname}
        genchecksum ${docarchive}

        mkdir ${miscname}
        for s in 16 24 32 48 ; do
            cp -av ${srcdir}/src/java.desktop/unix/classes/sun/awt/X11/java-icon${s}.png ${miscname}
        done
%if %{with_systemtap}
        cp -a ${tapsetdir}* ${miscname}
%endif
        cp -av ${altjavadir}/%{alt_java_name} ${miscname}
        cp -avr ${gensources} ${miscname}
        tar -cJf ${miscarchive} ${miscname}
        genchecksum ${miscarchive}
    fi

    tar -cJf ${jmodsarchive} --exclude='**.debuginfo' ${jdkname}/jmods
    genchecksum ${jmodsarchive}
    rm -rv ${jdkname}/jmods

    tar -cJf ${jdkarchive} --exclude='**.debuginfo' ${jdkname}
    genchecksum ${jdkarchive}

    tar -cJf ${jrearchive}  --exclude='**.debuginfo' ${jrename}
    genchecksum ${jrearchive}

%if %{include_staticlibs}
    # Static libraries (needed for building graal vm with native image)
    # Tar as overlay. Transform to the JDK name, since we just want to "add"
    # static libraries to that folder
    tar -cJf ${staticarchive} \
        --transform "s|^%{static_libs_image}/lib/*|${staticname}/lib/static/linux-%{archinstall}/glibc/|" "%{static_libs_image}/lib"
    genchecksum ${staticarchive}
%endif

    # Revert directory renaming so testing will run
    # TODO: testing should run on the packaged JDK
    mv ${jdkname} %{jdkimage}
    mv ${jrename} %{jreimage}

    popd #images

}

packFullPatchedSources

%if %{build_hotspot_first}
  # Build a fresh libjvm.so first and use it to bootstrap
  echo "Building HotSpot only for the latest libjvm.so"
  cp -LR --preserve=mode,timestamps %{bootjdk} newboot
  systemjdk=$(pwd)/newboot
  buildjdk build/newboot ${systemjdk} %{hotspot_target} "release" "bundled" "internal"
  mv build/newboot/jdk/lib/%{vm_variant}/libjvm.so newboot/lib/%{vm_variant}
%else
  systemjdk=%{bootjdk}
%endif

for suffix in %{build_loop} ; do
  if [ "x$suffix" = "x" ] ; then
      debugbuild=release
  else
      # change --something to something
      debugbuild=`echo $suffix  | sed "s/-//g"`
  fi
  # We build with 'external' debug symbols for the
  # release build and build with 'internal' for
  # slowdebug/fastdebug variants
  if [ "x$suffix" = "x" ] ; then
    debug_symbols=external
  else
    debug_symbols=internal
  fi

  builddir=%{buildoutputdir -- ${suffix}}
  bootbuilddir=boot${builddir}
  installdir=%{installoutputdir -- ${suffix}}
  bootinstalldir=boot${installdir}
  packagesdir=%{packageoutputdir -- ${suffix}}

  link_opt="%{link_type}"
%if %{system_libs}
  # Copy the source tree so we can remove all in-tree libraries
  cp -a %{top_level_dir_name} %{top_level_dir_name_backup}
  # Remove all libraries that are linked
  sh %{SOURCE12} %{top_level_dir_name} full
%endif
  # Debug builds don't need same targets as release for
  # build speed-up. We also avoid bootstrapping these
  # slower builds.
  if echo $debugbuild | grep -q "debug" ; then
      maketargets="%{debug_targets}"
      run_bootstrap=false
  else
      maketargets="%{release_targets}"
      run_bootstrap=%{bootstrap_build}
  fi
  if ${run_bootstrap} ; then
      buildjdk ${bootbuilddir} ${systemjdk} "%{bootstrap_targets}" ${debugbuild} ${link_opt} ${debug_symbols}
      installjdk ${bootbuilddir} ${bootinstalldir}
      buildjdk ${builddir} $(pwd)/${bootinstalldir}/images/%{jdkimage} "${maketargets}" ${debugbuild} ${link_opt} ${debug_symbols}
      findgeneratedsources ${installdir} ${builddir} $(pwd)/%{top_level_dir_name}
      installjdk ${builddir} ${installdir}
      %{!?with_artifacts:rm -rf ${bootinstalldir}}
  else
      buildjdk ${builddir} ${systemjdk} "${maketargets}" ${debugbuild} ${link_opt} ${debug_symbols}
      findgeneratedsources ${installdir} ${builddir} $(pwd)/%{top_level_dir_name}
      installjdk ${builddir} ${installdir}
  fi
  packagejdk ${installdir} ${packagesdir} %{altjavaoutputdir}

%if %{system_libs}
  # Restore original source tree we modified by removing full in-tree sources
  rm -rf %{top_level_dir_name}
  mv %{top_level_dir_name_backup} %{top_level_dir_name}
%endif

# build cycles
done # end of release / debug cycle loop

%check

# We test debug first as it will give better diagnostics on a crash
for suffix in %{build_loop} ; do

# portable builds have static_libs embedded, thus top_dir_abs_main_build_path is same as  top_dir_abs_staticlibs_build_path
top_dir_abs_main_build_path=$(pwd)/%{installoutputdir -- ${suffix}}
%if %{include_staticlibs}
top_dir_abs_staticlibs_build_path=${top_dir_abs_main_build_path}
%endif

export JAVA_HOME=${top_dir_abs_main_build_path}/images/%{jdkimage}

# Pre-test setup

# System security properties are disabled by default on portable.
# Turn on system security properties
#sed -i -e "s:^security.useSystemPropertiesFile=.*:security.useSystemPropertiesFile=true:" \
#${JAVA_HOME}/conf/security/java.security

# Check Shenandoah is enabled
%if %{use_shenandoah_hotspot}
$JAVA_HOME/bin/java -XX:+UseShenandoahGC -version
%endif

# Check unlimited policy has been used
$JAVA_HOME/bin/javac -d . %{SOURCE13}
$JAVA_HOME/bin/java --add-opens java.base/javax.crypto=ALL-UNNAMED TestCryptoLevel

# Check ECC is working
$JAVA_HOME/bin/javac -d . %{SOURCE14}
$JAVA_HOME/bin/java $(echo $(basename %{SOURCE14})|sed "s|\.java||")

# Check system crypto (policy) is deactive and can not be enabled
# Test takes a single argument - true or false - to state whether system
# security properties are enabled or not.
$JAVA_HOME/bin/javac -d . %{SOURCE15}
export PROG=$(echo $(basename %{SOURCE15})|sed "s|\.java||")
export SEC_DEBUG="-Djava.security.debug=properties"
# Specific to portable:System security properties to be off by default
$JAVA_HOME/bin/java ${SEC_DEBUG} ${PROG} false
$JAVA_HOME/bin/java ${SEC_DEBUG} -Djava.security.disableSystemPropertiesFile=false ${PROG} false

# Check correct vendor values have been set
$JAVA_HOME/bin/javac -d . %{SOURCE16}
$JAVA_HOME/bin/java $(echo $(basename %{SOURCE16})|sed "s|\.java||") "%{oj_vendor}" "%{oj_vendor_url}" "%{oj_vendor_bug_url}" "%{oj_vendor_version}"

# Check java launcher has no SSB mitigation
if ! nm $JAVA_HOME/bin/java | grep set_speculation ; then true ; else false; fi

# Check alt-java launcher has SSB mitigation on supported architectures
# set_speculation function exists in both cases, so check for prctl call
%ifarch %{ssbd_arches}
nm %{altjavaoutputdir}/%{alt_java_name} | grep prctl
%else
if ! nm %{altjavaoutputdir}/%{alt_java_name} | grep prctl ; then true ; else false; fi
%endif

%if ! 0%{?flatpak}
# Check translations are available for new timezones (during flatpak builds, the
# tzdb.dat used by this test is not where the test expects it, so this is
# disabled for flatpak builds)
$JAVA_HOME/bin/javac -d . %{SOURCE18}
$JAVA_HOME/bin/java $(echo $(basename %{SOURCE18})|sed "s|\.java||") JRE || echo "FIXME before release!"
$JAVA_HOME/bin/java -Djava.locale.providers=CLDR $(echo $(basename %{SOURCE18})|sed "s|\.java||") CLDR || echo "FIXME before release!"
%endif

%if %{include_staticlibs}
# Check debug symbols in static libraries (smoke test)
export STATIC_LIBS_HOME=${top_dir_abs_staticlibs_build_path}/images/%{static_libs_image}
ls -l $STATIC_LIBS_HOME
ls -l $STATIC_LIBS_HOME/lib
readelf --debug-dump $STATIC_LIBS_HOME/lib/libnet.a | grep Inet4AddressImpl.c
readelf --debug-dump $STATIC_LIBS_HOME/lib/libnet.a | grep Inet6AddressImpl.c
%endif

# Release builds strip the debug symbols into external .debuginfo files
if [ "x$suffix" = "x" ] ; then
  so_suffix="debuginfo"
else
  so_suffix="so"
fi
# Check debug symbols are present and can identify code
find "$JAVA_HOME" -iname "*.$so_suffix" -print0 | while read -d $'\0' lib
do
  if [ -f "$lib" ] ; then
    echo "Testing $lib for debug symbols"
    # All these tests rely on RPM failing the build if the exit code of any set
    # of piped commands is non-zero.

    # Test for .debug_* sections in the shared object. This is the main test
    # Stripped objects will not contain these
    eu-readelf -S "$lib" | grep "] .debug_"
    test $(eu-readelf -S "$lib" | grep -E "\]\ .debug_(info|abbrev)" | wc --lines) == 2

    # Test FILE symbols. These will most likely be removed by anything that
    # manipulates symbol tables because it's generally useless. So a nice test
    # that nothing has messed with symbols
    old_IFS="$IFS"
    IFS=$'\n'
    for line in $(eu-readelf -s "$lib" | grep "00000000      0 FILE    LOCAL  DEFAULT")
    do
     # We expect to see .cpp and .S files, except for architectures like aarch64 and
     # s390 where we expect .o and .oS files
      echo "$line" | grep -E "ABS ((.*/)?[-_a-zA-Z0-9]+\.(c|cc|cpp|cxx|o|S|oS))?$"
    done
    IFS="$old_IFS"

    # If this is the JVM, look for javaCalls.(cpp|o) in FILEs, for extra sanity checking
    if [ "`basename $lib`" = "libjvm.so" ]; then
      eu-readelf -s "$lib" | \
        grep -E "00000000      0 FILE    LOCAL  DEFAULT      ABS javaCalls.(cpp|o)$"
    fi

    # Test that there are no .gnu_debuglink sections pointing to another
    # debuginfo file. There shouldn't be any debuginfo files, so the link makes
    # no sense either
    eu-readelf -S "$lib" | grep 'gnu'
    if eu-readelf -S "$lib" | grep '] .gnu_debuglink' | grep PROGBITS; then
      echo "bad .gnu_debuglink section."
      eu-readelf -x .gnu_debuglink "$lib"
      false
    fi
  fi
done

# Make sure gdb can do a backtrace based on line numbers on libjvm.so
# javaCalls.cpp:58 should map to:
# http://hg.openjdk.java.net/jdk8u/jdk8u/hotspot/file/ff3b27e6bcc2/src/share/vm/runtime/javaCalls.cpp#l58
# Using line number 1 might cause build problems. See:
# https://bugzilla.redhat.com/show_bug.cgi?id=1539664
# https://bugzilla.redhat.com/show_bug.cgi?id=1538767
gdb -q "$JAVA_HOME/bin/java" <<EOF | tee gdb.out
handle SIGSEGV pass nostop noprint
handle SIGILL pass nostop noprint
set breakpoint pending on
break javaCalls.cpp:58
commands 1
backtrace
quit
end
run -version
EOF
%ifarch %{gdb_arches}
grep 'JavaCallWrapper::JavaCallWrapper' gdb.out
%endif

# Check src.zip has all sources. See RHBZ#1130490
$JAVA_HOME/bin/jar -tf $JAVA_HOME/lib/src.zip | grep 'sun.misc.Unsafe'

# Check class files include useful debugging information
$JAVA_HOME/bin/javap -l -c java.lang.Object | grep "Compiled from"
$JAVA_HOME/bin/javap -l -c java.lang.Object | grep LineNumberTable
$JAVA_HOME/bin/javap -l -c java.lang.Object | grep LocalVariableTable

# Check generated class files include useful debugging information
$JAVA_HOME/bin/javap -l -c java.nio.ByteBuffer | grep "Compiled from"
$JAVA_HOME/bin/javap -l -c java.nio.ByteBuffer | grep LineNumberTable
$JAVA_HOME/bin/javap -l -c java.nio.ByteBuffer | grep LocalVariableTable

# build cycles check
done

%install

 mkdir -p $RPM_BUILD_ROOT%{_jvmdir}
 mv %{jdkportablesourcesarchive -- ""} $RPM_BUILD_ROOT%{_jvmdir}/
 mv %{jdkportablesourcesarchive -- ""}.sha256sum $RPM_BUILD_ROOT%{_jvmdir}/

for suffix in %{build_loop} ; do

    packagesdir=%{packageoutputdir -- ${suffix}}

    if [ "x$suffix" == "x" ] ; then
        nameSuffix=""
    else
        nameSuffix=`echo "$suffix"| sed s/-/./`
    fi

    # These definitions should match those in installjdk
    jdkarchive=${packagesdir}/%{jdkportablearchive -- "$nameSuffix"}
    jmodsarchive=${packagesdir}/%{jmodsportablearchive -- "$nameSuffix"}
    jrearchive=${packagesdir}/%{jreportablearchive -- "$nameSuffix"}
    staticarchive=${packagesdir}/%{staticlibsportablearchive -- "$nameSuffix"}
    debugarchive=${packagesdir}/%{jdkportablearchive -- "${nameSuffix}.debuginfo"}

    mv ${jdkarchive} $RPM_BUILD_ROOT%{_jvmdir}/
    mv ${jdkarchive}.sha256sum $RPM_BUILD_ROOT%{_jvmdir}/
    mv ${jmodsarchive} $RPM_BUILD_ROOT%{_jvmdir}/
    mv ${jmodsarchive}.sha256sum $RPM_BUILD_ROOT%{_jvmdir}/
    mv ${jrearchive} $RPM_BUILD_ROOT%{_jvmdir}/
    mv ${jrearchive}.sha256sum $RPM_BUILD_ROOT%{_jvmdir}/

%if %{include_staticlibs}
    mv ${staticarchive} $RPM_BUILD_ROOT%{_jvmdir}/
    mv ${staticarchive}.sha256sum $RPM_BUILD_ROOT%{_jvmdir}/
%endif

    if [ "x$suffix" = "x" ] ; then
        mv ${debugarchive} $RPM_BUILD_ROOT%{_jvmdir}/
        mv ${debugarchive}.sha256sum $RPM_BUILD_ROOT%{_jvmdir}/
    fi
done

    if [ "x$suffix" = "x" ] ; then
        # These definitions should match those in installjdk
        # Install outside the loop as there are no debug variants
        docarchive=${packagesdir}/%{docportablearchive}
        miscarchive=${packagesdir}/%{miscportablearchive}
        mv ${docarchive} $RPM_BUILD_ROOT%{_jvmdir}/
        mv ${docarchive}.sha256sum $RPM_BUILD_ROOT%{_jvmdir}/
        mv ${miscarchive} $RPM_BUILD_ROOT%{_jvmdir}/
        mv ${miscarchive}.sha256sum $RPM_BUILD_ROOT%{_jvmdir}/
   fi

# To show sha in the build log
for file in `ls $RPM_BUILD_ROOT%{_jvmdir}/*.sha256sum` ; do
    ls -l $file ;
    cat $file ;
done

%if %{include_normal_build}
%files
# main package builds always
%{_jvmdir}/%{jreportablearchiveForFiles}
%{_jvmdir}/%{jreportablearchiveForFiles}.sha256sum
%else
%files
# placeholder
%endif

%if %{include_normal_build}
%files devel
%{_jvmdir}/%{jdkportablearchiveForFiles}
%{_jvmdir}/%{jdkportablearchive -- .debuginfo}
%{_jvmdir}/%{jdkportablearchiveForFiles}.sha256sum
%{_jvmdir}/%{jdkportablearchive -- .debuginfo}.sha256sum
%{_jvmdir}/%{jmodsportablearchiveForFiles}
%{_jvmdir}/%{jmodsportablearchiveForFiles}.sha256sum
%endif

%if %{include_normal_build}
%if %{include_staticlibs}
%files static-libs
%{_jvmdir}/%{staticlibsportablearchiveForFiles}
%{_jvmdir}/%{staticlibsportablearchiveForFiles}.sha256sum
%endif
%endif

%if %{include_debug_build}
%files slowdebug
%{_jvmdir}/%{jreportablearchive -- .slowdebug}
%{_jvmdir}/%{jreportablearchive -- .slowdebug}.sha256sum

%files devel-slowdebug
%{_jvmdir}/%{jdkportablearchive -- .slowdebug}
%{_jvmdir}/%{jdkportablearchive -- .slowdebug}.sha256sum
%{_jvmdir}/%{jmodsportablearchive -- .slowdebug}
%{_jvmdir}/%{jmodsportablearchive -- .slowdebug}.sha256sum

%if %{include_staticlibs}
%files static-libs-slowdebug
%{_jvmdir}/%{staticlibsportablearchive -- .slowdebug}
%{_jvmdir}/%{staticlibsportablearchive -- .slowdebug}.sha256sum
%endif
%endif

%if %{include_fastdebug_build}
%files fastdebug
%{_jvmdir}/%{jreportablearchive -- .fastdebug}
%{_jvmdir}/%{jreportablearchive -- .fastdebug}.sha256sum

%files devel-fastdebug
%{_jvmdir}/%{jdkportablearchive -- .fastdebug}
%{_jvmdir}/%{jdkportablearchive -- .fastdebug}.sha256sum
%{_jvmdir}/%{jmodsportablearchive -- .fastdebug}
%{_jvmdir}/%{jmodsportablearchive -- .fastdebug}.sha256sum

%if %{include_staticlibs}
%files static-libs-fastdebug
%{_jvmdir}/%{staticlibsportablearchive -- .fastdebug}
%{_jvmdir}/%{staticlibsportablearchive -- .fastdebug}.sha256sum
%endif
%endif

%files sources
%{_jvmdir}/%{jdkportablesourcesarchiveForFiles}
%{_jvmdir}/%{jdkportablesourcesarchiveForFiles}.sha256sum

%if %{include_normal_build}
%files docs
%{_jvmdir}/%{docportablearchive}
%{_jvmdir}/%{docportablearchive}.sha256sum

%files misc
%{_jvmdir}/%{miscportablearchive}
%{_jvmdir}/%{miscportablearchive}.sha256sum
%endif

%changelog
## START: Generated by rpmautospec
* Tue Apr 28 2026 azldev <azurelinux@microsoft.com> - 1:25.0.0.0.32-2
- Latest state for java-25-openjdk-portable

* Mon Jul 21 2025 Jiri Vanek <jvanek@redhat.com> - 1:25.0.0.0.32-1
- Updated to 25+32

* Mon Jun 09 2025 Jiri Vanek <jvanek@redhat.com> - 1:25.0.0.0.26-2
- Moved to produce external debuginfo instead of unstripped

* Mon Jun 09 2025 Jiri Vanek <jvanek@redhat.com> - 1:25.0.0.0.26-1
- Bumped to jdk25+26

* Wed Mar 12 2025 Jiri Vanek <jvanek@redhat.com> - 1:25.0.0.0.13-1
- Initial import
## END: Generated by rpmautospec
