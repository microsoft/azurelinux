## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autochangelog
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# RPM conditionals so as to be able to dynamically produce
# slowdebug/release builds. See:
# http://rpm.org/user_doc/conditional_builds.html
#
# Examples:
#
# Produce release, fastdebug *and* slowdebug builds on x86_64 (default):
# $ rpmbuild -ba java-21-openjdk.spec
#
# Produce only release builds (no debug builds) on x86_64:
# $ rpmbuild -ba java-21-openjdk.spec --without slowdebug --without fastdebug
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

# Workaround for stripping of debug symbols from static libraries
%if %{with staticlibs}
%define __brp_strip_static_archive %{nil}
%global include_staticlibs 1
%else
%global include_staticlibs 0
%endif

# Disable automatic debuginfo/debugsource package.
# We create them manually ourselves for the release build.
# fastdebug/slowdebug have symbols in the binaries themselves.
%define debug_package %{nil}
# Don't strip any debug info symbols (in fastdebug/slowdebug builds).
# Keep the symbols internal, like the binaries in JMODs have
%define __brp_strip %{nil}
# The add-determinism build root helper might cause some jar files
# to change, breaking the run-time image link (for jrt-fs.jar). Disable
# the jar processor.
%define add_determinism_options --handler=-jar

#placeholder - used in regexes, otherwise for no use in portables
%global freetype_lib |libfreetype[.]so.*

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
%global is_system_jdk 1

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
# Set of architectures which support SystemTap tapsets
%global systemtap_arches %{jit_arches}
# Set of architectures with a Ahead-Of-Time (AOT) compiler
%global aot_arches      x86_64 %{aarch64}
# Set of architectures which support the serviceability agent
%global sa_arches       %{ix86} x86_64 sparcv9 sparc64 %{aarch64} %{power64} %{arm} riscv64
# As of JDK-8005165 in OpenJDK 10, class sharing is not arch-specific
# However, it does segfault on the Zero assembler port, so currently JIT only
%global share_arches    %{jit_arches}
# Set of architectures for which we build the Shenandoah garbage collector
%global shenandoah_arches x86_64 %{aarch64}
# Set of architectures for which we build the Z garbage collector
%global zgc_arches x86_64 riscv64
# Set of architectures for which alt-java has SSB mitigation
%global ssbd_arches x86_64
# Set of architectures for which java has short vector math library (libsvml.so)
%global svml_arches x86_64
# Set of architectures where we verify backtraces with gdb
# s390x fails on RHEL 7 so we exclude it there
%if (0%{?rhel} > 0 && 0%{?rhel} < 8)
%global gdb_arches %{arm} %{aarch64} %{ix86} %{power64} sparcv9 sparc64 x86_64 %{zero_arches}
%else
%global gdb_arches %{jit_arches} %{zero_arches}
%endif

# By default, we build a debug build during main build on JIT architectures
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

%if %{include_staticlibs}
# Extra target for producing the static-libraries. Separate from
# other targets since this target is configured to use in-tree
# AWT dependencies: lcms, libjpeg, libpng, libharfbuzz, giflib
# and possibly others
%global static_libs_target static-libs-image
%else
%global static_libs_target %{nil}
%endif

# VM variant being built
%ifarch %{zero_arches}
%global vm_variant zero
%else
%global vm_variant server
%endif

# debugedit tool for rewriting ELF file paths
%global debugedit %( if [ -f "%{_rpmconfigdir}/debugedit"  ]; then echo "%{_rpmconfigdir}/debugedit" ; else echo "/usr/bin/debugedit"; fi )

# With disabled nss is NSS deactivated, so NSS_LIBDIR can contain the wrong path
# the initialization must be here. Later the pkg-config have buggy behavior
# looks like openjdk RPM specific bug
# Always set this so the nss.cfg file is not broken
%global NSS_LIBDIR %(pkg-config --variable=libdir nss)

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
%global with_systemtap 1
%else
%global with_systemtap 0
%endif

# New Version-String scheme-style defines
%global featurever 21
%global interimver 0
%global updatever 8
%global patchver 0

# We don't add any LTS designator for STS packages (Fedora and EPEL).
# We need to explicitly exclude EPEL as it would have the %%{rhel} macro defined.
%if 0%{?rhel} && !0%{?epel}
  %global lts_designator "LTS"
  %global lts_designator_zip -%{lts_designator}
%else
  %global lts_designator ""
  %global lts_designator_zip ""
%endif

# Define vendor information used by OpenJDK
%global oj_vendor Red Hat, Inc.
%global oj_vendor_url https://www.redhat.com/
# Define what url should JVM offer in case of a crash report
# order may be important, epel may have rhel declared
%if 0%{?epel}
%global oj_vendor_bug_url  https://bugzilla.redhat.com/enter_bug.cgi?product=Fedora%20EPEL&component=%{name}&version=epel%{epel}
%else
%if 0%{?fedora}
# Does not work for rawhide, keeps the version field empty
%global oj_vendor_bug_url  https://bugzilla.redhat.com/enter_bug.cgi?product=Fedora&component=%{name}&version=%{fedora}
%else
%if 0%{?rhel}
%global oj_vendor_bug_url https://access.redhat.com/support/cases/
%else
%global oj_vendor_bug_url  https://bugzilla.redhat.com/enter_bug.cgi
%endif
%endif
%endif
%global oj_vendor_version (Red_Hat-%{version}-%{release})

# Define IcedTea version used for SystemTap tapsets and desktop file
%global icedteaver      6.0.0pre00-c848b93a8598
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
%global buildver        9
%global rpmrelease      1
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
%global is_ga           1
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
%define fullversion()     %{expand:%{compatiblename}%{?1}-%{version}-%{release}}
# images directories from upstream build
%global jdkimage                jdk
%global static_libs_image       static-libs
# installation directory for static libraries
%global static_libs_root        lib/static
%global static_libs_arch_dir    %{static_libs_root}/linux-%{archinstall}
%global static_libs_install_dir %{static_libs_arch_dir}/glibc

# we can copy the javadoc to not arched dir, or make it not noarch
%define uniquejavadocdir() %{expand:%{compatiblename}%{?1}}
# main id and dir of this jdk
%define uniquesuffix() %{expand:%{compatiblename}%{?1}}

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


%global etcjavasubdir     %{_sysconfdir}/java/java-%{javaver}-%{origin}
%define etcjavadir()      %{expand:%{etcjavasubdir}/%{uniquesuffix -- %{?1}}}
# Standard JPackage directories and symbolic links.
%define sdkdir()        %{expand:%{uniquesuffix -- %{?1}}}

%define sdkbindir()     %{expand:%{_jvmdir}/%{sdkdir -- %{?1}}/bin}
%define jrebindir()     %{expand:%{_jvmdir}/%{sdkdir -- %{?1}}/bin}

%global alt_java_name     alt-java
%global generated_sources_name     generated_sources

%global rpm_state_dir %{_localstatedir}/lib/rpm-state/
%global repack_file repack.info

# For flatpack builds hard-code dependency paths,
# otherwise use relative paths.
%if 0%{?flatpak}
%global alternatives_requires /usr/sbin/alternatives
%global javazidir /usr/share/javazi-1.8
%global portablejvmdir /usr/lib/jvm
%else
%global alternatives_requires %{_sbindir}/alternatives
%global javazidir %{_datadir}/javazi-1.8
%global portablejvmdir %{_jvmdir}
%endif

%global family %{name}.%{_arch}
%global family_noarch  %{name}

%if %{with_systemtap}
# Where to install systemtap tapset (links)
# We would like these to be in a package specific sub-dir,
# but currently systemtap doesn't support that, so we have to
# use the root tapset dir for now. To distinguish between 64
# and 32 bit architectures we place the tapsets under the arch
# specific dir (note that systemtap will only pickup the tapset
# for the primary arch for now). Systemtap uses the machine name
# aka target_cpu as architecture specific directory name.
%global tapsetroot /usr/share/systemtap
%global tapsetdirttapset %{tapsetroot}/tapset/
%global tapsetdir %{tapsetdirttapset}/%{stapinstall}
%endif

# x86 is no longer supported
%if 0%{?java_arches:1}
ExclusiveArch:  %{java_arches}
%else
ExcludeArch: %{ix86}
%endif

# not-duplicated scriptlets for normal/debug packages
%global update_desktop_icons /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%define post_script() %{expand:
update-desktop-database %{_datadir}/applications &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
}

# We want fastdebug and slowdebug alternatives to have a lower
# priority than the normal alternatives, so the normal alternatives
# are the default.
# If the argument to this macro is non-nil, that is either -fastdebug
# or -slowdebug, then priority_for will expand to a value one less
# than the priority global.  If the argument to this macro is nil,
# that is represents the non-debug or normal package, then the result
# is the normal priority macro value.
# This computation is done at RPM macro expansion time, rather than at
# runtime, to keep scriptlets as simple as possible.
%define priority_for() %{expand:%[%{?1:1}%{!?1:0} ? %{priority} - 1 : %{priority}]}

%global man_comp .gz

%define alternatives_java_install() %{expand:
if [ "x$debug"  == "xtrue" ] ; then
  set -x
fi
alternatives --install %{_bindir}/java java %{jrebindir -- %{?1}}/java %{priority_for -- %{?1}} \\
  --slave %{_jvmdir}/jre jre %{_jvmdir}/%{sdkdir -- %{?1}} \\
  --slave %{_bindir}/%{alt_java_name} %{alt_java_name} %{jrebindir -- %{?1}}/%{alt_java_name} \\
  --slave %{_bindir}/jcmd jcmd %{sdkbindir -- %{?1}}/jcmd \\
  --slave %{_bindir}/keytool keytool %{jrebindir -- %{?1}}/keytool \\
  --slave %{_bindir}/rmiregistry rmiregistry %{jrebindir -- %{?1}}/rmiregistry \\
  --slave %{_mandir}/man1/java.1%{man_comp} java.1%{man_comp} %{_jvmdir}/%{sdkdir -- %{?1}}/man/man1/java.1 \\
  --slave %{_mandir}/man1/%{alt_java_name}.1%{man_comp} %{alt_java_name}.1%{man_comp} %{_jvmdir}/%{sdkdir -- %{?1}}/man/man1/%{alt_java_name}.1 \\
  --slave %{_mandir}/man1/jcmd.1%{man_comp} jcmd.1%{man_comp} %{_jvmdir}/%{sdkdir -- %{?1}}/man/man1/jcmd.1 \\
  --slave %{_mandir}/man1/keytool.1%{man_comp} keytool.1%{man_comp} %{_jvmdir}/%{sdkdir -- %{?1}}/man/man1/keytool.1 \\
  --slave %{_mandir}/man1/rmiregistry.1%{man_comp} rmiregistry.1%{man_comp} %{_jvmdir}/%{sdkdir -- %{?1}}/man/man1/rmiregistry.1
alternatives --install %{_jvmdir}/jre-%{origin} jre_%{origin} %{_jvmdir}/%{sdkdir -- %{?1}} %{priority_for -- %{?1}}
alternatives --install %{_jvmdir}/jre-%{javaver} jre_%{javaver} %{_jvmdir}/%{sdkdir -- %{?1}} %{priority_for -- %{?1}}
alternatives --install %{_jvmdir}/jre-%{javaver}-%{origin} jre_%{javaver}_%{origin} %{_jvmdir}/%{sdkdir -- %{?1}} %{priority_for -- %{?1}}
}

%define post_headless() %{expand:
%{alternatives_java_install -- %{?1}}
update-desktop-database %{_datadir}/applications &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
}

%define postun_script() %{expand:
update-desktop-database %{_datadir}/applications &> /dev/null || :
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    %{update_desktop_icons}
fi
}

# Perform alternatives removals in preun instead of postun so that we
# are removing live symbolic links instead of dangling symbolic links,
# even though the alternatives command does not seem to care.  The
# documentation uses preun or postun without providing a rationale for
# using one over the other:
# https://docs.fedoraproject.org/en-US/packaging-guidelines/Alternatives/
#
# The [ $1 -eq 0 ] is an RPM scriptlet idiom meaning "only do the
# following if this scriptlet is being run during a straight package
# removal; in other words, do NOT do the following if this scriptlet
# is being run as part of an upgrade transaction".
# https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/#_syntax
%define preun_headless() %{expand:
if [ "x$debug"  == "xtrue" ] ; then
  set -x
fi
if [ $1 -eq 0 ]
then
  alternatives --remove java %{jrebindir -- %{?1}}/java
  alternatives --remove jre_%{origin} %{_jvmdir}/%{sdkdir -- %{?1}}
  alternatives --remove jre_%{javaver} %{_jvmdir}/%{sdkdir -- %{?1}}
  alternatives --remove jre_%{javaver}_%{origin} %{_jvmdir}/%{sdkdir -- %{?1}}
fi
}

# Invoke gtk-update-icon-cache in posttrans instead of post as an
# optimization.  If other packages in the transaction install icons
# and use this optimization, then invocations of gtk-update-icon-cache
# will all happen in succession, and invocations after the first one
# will notice that the cache is fresh and immediately succeed.  If
# this were instead done in each package's post, then the icon cache
# would be regenerated every time, rendering the whole transaction
# slower.
# See:
# https://lists.fedoraproject.org/archives/list/packaging\
# @lists.fedoraproject.org/thread/HXIIKIHBMT3HELPKWH2BAXRNIF7BPPJD/
# and:
# https://fedoraproject.org/wiki/Archive:PackagingDrafts/Icon_Cache
%define posttrans_script() %{expand:
%{update_desktop_icons}
}

%define alternatives_javac_install() %{expand:
if [ "x$debug"  == "xtrue" ] ; then
  set -x
fi
alternatives --install %{_bindir}/javac javac %{sdkbindir -- %{?1}}/javac %{priority_for -- %{?1}} \\
  --slave %{_jvmdir}/java java_sdk %{_jvmdir}/%{sdkdir -- %{?1}} \\
  --slave %{_bindir}/jlink jlink %{sdkbindir -- %{?1}}/jlink \\
  --slave %{_bindir}/jmod jmod %{sdkbindir -- %{?1}}/jmod \\
%ifarch %{sa_arches}
%ifnarch %{zero_arches}
  --slave %{_bindir}/jhsdb jhsdb %{sdkbindir -- %{?1}}/jhsdb \\
%endif
%endif
  --slave %{_bindir}/jar jar %{sdkbindir -- %{?1}}/jar \\
  --slave %{_bindir}/jarsigner jarsigner %{sdkbindir -- %{?1}}/jarsigner \\
  --slave %{_bindir}/javadoc javadoc %{sdkbindir -- %{?1}}/javadoc \\
  --slave %{_bindir}/javap javap %{sdkbindir -- %{?1}}/javap \\
  --slave %{_bindir}/jconsole jconsole %{sdkbindir -- %{?1}}/jconsole \\
  --slave %{_bindir}/jdb jdb %{sdkbindir -- %{?1}}/jdb \\
  --slave %{_bindir}/jdeps jdeps %{sdkbindir -- %{?1}}/jdeps \\
  --slave %{_bindir}/jdeprscan jdeprscan %{sdkbindir -- %{?1}}/jdeprscan \\
  --slave %{_bindir}/jfr jfr %{sdkbindir -- %{?1}}/jfr \\
  --slave %{_bindir}/jimage jimage %{sdkbindir -- %{?1}}/jimage \\
  --slave %{_bindir}/jinfo jinfo %{sdkbindir -- %{?1}}/jinfo \\
  --slave %{_bindir}/jmap jmap %{sdkbindir -- %{?1}}/jmap \\
  --slave %{_bindir}/jps jps %{sdkbindir -- %{?1}}/jps \\
  --slave %{_bindir}/jpackage jpackage %{sdkbindir -- %{?1}}/jpackage \\
  --slave %{_bindir}/jrunscript jrunscript %{sdkbindir -- %{?1}}/jrunscript \\
  --slave %{_bindir}/jshell jshell %{sdkbindir -- %{?1}}/jshell \\
  --slave %{_bindir}/jstack jstack %{sdkbindir -- %{?1}}/jstack \\
  --slave %{_bindir}/jstat jstat %{sdkbindir -- %{?1}}/jstat \\
  --slave %{_bindir}/jstatd jstatd %{sdkbindir -- %{?1}}/jstatd \\
  --slave %{_bindir}/jwebserver jwebserver %{sdkbindir -- %{?1}}/jwebserver \\
  --slave %{_bindir}/serialver serialver %{sdkbindir -- %{?1}}/serialver \\
  --slave %{_mandir}/man1/jar.1%{man_comp} jar.1%{man_comp} %{_jvmdir}/%{sdkdir -- %{?1}}/man/man1/jar.1 \\
  --slave %{_mandir}/man1/jarsigner.1%{man_comp} jarsigner.1%{man_comp} %{_jvmdir}/%{sdkdir -- %{?1}}/man/man1/jarsigner.1 \\
  --slave %{_mandir}/man1/javac.1%{man_comp} javac.1%{man_comp} %{_jvmdir}/%{sdkdir -- %{?1}}/man/man1/javac.1 \\
  --slave %{_mandir}/man1/javadoc.1%{man_comp} javadoc.1%{man_comp} %{_jvmdir}/%{sdkdir -- %{?1}}/man/man1/javadoc.1 \\
  --slave %{_mandir}/man1/javap.1%{man_comp} javap.1%{man_comp} %{_jvmdir}/%{sdkdir -- %{?1}}/man/man1/javap.1 \\
  --slave %{_mandir}/man1/jconsole.1%{man_comp} jconsole.1%{man_comp} %{_jvmdir}/%{sdkdir -- %{?1}}/man/man1/jconsole.1 \\
  --slave %{_mandir}/man1/jdb.1%{man_comp} jdb.1%{man_comp} %{_jvmdir}/%{sdkdir -- %{?1}}/man/man1/jdb.1 \\
  --slave %{_mandir}/man1/jdeps.1%{man_comp} jdeps.1%{man_comp} %{_jvmdir}/%{sdkdir -- %{?1}}/man/man1/jdeps.1 \\
  --slave %{_mandir}/man1/jinfo.1%{man_comp} jinfo.1%{man_comp} %{_jvmdir}/%{sdkdir -- %{?1}}/man/man1/jinfo.1 \\
  --slave %{_mandir}/man1/jmap.1%{man_comp} jmap.1%{man_comp} %{_jvmdir}/%{sdkdir -- %{?1}}/man/man1/jmap.1 \\
  --slave %{_mandir}/man1/jps.1%{man_comp} jps.1%{man_comp} %{_jvmdir}/%{sdkdir -- %{?1}}/man/man1/jps.1 \\
  --slave %{_mandir}/man1/jpackage.1%{man_comp} jpackage.1%{man_comp} %{_jvmdir}/%{sdkdir -- %{?1}}/man/man1/jpackage.1 \\
  --slave %{_mandir}/man1/jrunscript.1%{man_comp} jrunscript.1%{man_comp} %{_jvmdir}/%{sdkdir -- %{?1}}/man/man1/jrunscript.1 \\
  --slave %{_mandir}/man1/jstack.1%{man_comp} jstack.1%{man_comp} %{_jvmdir}/%{sdkdir -- %{?1}}/man/man1/jstack.1 \\
  --slave %{_mandir}/man1/jstat.1%{man_comp} jstat.1%{man_comp} %{_jvmdir}/%{sdkdir -- %{?1}}/man/man1/jstat.1 \\
  --slave %{_mandir}/man1/jwebserver.1%{man_comp} jwebserver.1%{man_comp} %{_jvmdir}/%{sdkdir -- %{?1}}/man/man1/jwebserver.1 \\
  --slave %{_mandir}/man1/jstatd.1%{man_comp} jstatd.1%{man_comp} %{_jvmdir}/%{sdkdir -- %{?1}}/man/man1/jstatd.1 \\
  --slave %{_mandir}/man1/serialver.1%{man_comp} serialver.1%{man_comp} %{_jvmdir}/%{sdkdir -- %{?1}}/man/man1/serialver.1
alternatives --install %{_jvmdir}/java-%{origin} java_sdk_%{origin} %{_jvmdir}/%{sdkdir -- %{?1}} %{priority_for -- %{?1}}
alternatives --install %{_jvmdir}/java-%{javaver} java_sdk_%{javaver} %{_jvmdir}/%{sdkdir -- %{?1}} %{priority_for -- %{?1}}
}

%define post_devel() %{expand:
%{alternatives_javac_install -- %{?1}}
update-desktop-database %{_datadir}/applications &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
}

%define preun_devel() %{expand:
if [ "x$debug"  == "xtrue" ] ; then
  set -x
fi
if [ $1 -eq 0 ]
then
  alternatives --remove javac %{sdkbindir -- %{?1}}/javac
  alternatives --remove java_sdk_%{origin} %{_jvmdir}/%{sdkdir -- %{?1}}
  alternatives --remove java_sdk_%{javaver} %{_jvmdir}/%{sdkdir -- %{?1}}
fi
}

%define postun_devel() %{expand:
if [ "x$debug"  == "xtrue" ] ; then
  set -x
fi
update-desktop-database %{_datadir}/applications &> /dev/null || :

if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    %{update_desktop_icons}
fi
}

%define posttrans_devel() %{expand:
%{update_desktop_icons}
}

%define alternatives_javadoc_install() %{expand:
if [ "x$debug"  == "xtrue" ] ; then
  set -x
fi
alternatives --install %{_javadocdir}/java-%{origin} javadocdir_%{origin} %{_javadocdir}/%{uniquejavadocdir -- %{?1}}/api %{priority_for -- %{?1}}
alternatives --install %{_javadocdir}/java-%{javaver} javadocdir_%{javaver} %{_javadocdir}/%{uniquejavadocdir -- %{?1}}/api %{priority_for -- %{?1}}
alternatives --install %{_javadocdir}/java javadocdir %{_javadocdir}/%{uniquejavadocdir -- %{?1}}/api %{priority_for -- %{?1}}
}

%define preun_javadoc() %{expand:
if [ "x$debug"  == "xtrue" ] ; then
  set -x
fi
if [ $1 -eq 0 ]
then
  alternatives --remove javadocdir %{_javadocdir}/%{uniquejavadocdir -- %{?1}}/api
  alternatives --remove javadocdir_%{origin} %{_javadocdir}/%{uniquejavadocdir -- %{?1}}/api
  alternatives --remove javadocdir_%{javaver} %{_javadocdir}/%{uniquejavadocdir -- %{?1}}/api
fi
}

%define alternatives_javadoczip_install() %{expand:
if [ "x$debug"  == "xtrue" ] ; then
  set -x
fi
alternatives --install %{_javadocdir}/java-%{origin}.zip javadoczip_%{origin} %{_javadocdir}/%{uniquejavadocdir -- %{?1}}.zip %{priority_for -- %{?1}}
alternatives --install %{_javadocdir}/java-%{javaver}.zip javadoczip_%{javaver} %{_javadocdir}/%{uniquejavadocdir -- %{?1}}.zip %{priority_for -- %{?1}}
# Weird legacy filename for backwards-compatibility
alternatives --install %{_javadocdir}/java-zip javadoczip %{_javadocdir}/%{uniquejavadocdir -- %{?1}}.zip %{priority_for -- %{?1}}
}

%define preun_javadoc_zip() %{expand:
if [ "x$debug"  == "xtrue" ] ; then
  set -x
fi
if [ $1 -eq 0 ]
then
  alternatives --remove javadoczip %{_javadocdir}/%{uniquejavadocdir -- %{?1}}.zip
  alternatives --remove javadoczip_%{origin} %{_javadocdir}/%{uniquejavadocdir -- %{?1}}.zip
  alternatives --remove javadoczip_%{javaver} %{_javadocdir}/%{uniquejavadocdir -- %{?1}}.zip
fi
}

%define files_jre() %{expand:
%{_datadir}/icons/hicolor/*x*/apps/java-%{javaver}-%{origin}.png
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/libsplashscreen.so
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/libawt_xawt.so
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/libjawt.so
}

%define files_jre_headless() %{expand:
%doc %{_defaultdocdir}/%{uniquejavadocdir --   %{?1}}/%{fullversion -- %{nil}}.specfile
%license %{_jvmdir}/%{sdkdir -- %{?1}}/legal
%doc %{_jvmdir}/%{sdkdir -- %{?1}}/NEWS	
%doc %{_defaultdocdir}/%{uniquejavadocdir -- %{?1}}/NEWS
%dir %{_defaultdocdir}/%{uniquejavadocdir -- %{?1}}
%dir %{_sysconfdir}/.java/.systemPrefs
%dir %{_sysconfdir}/.java
%dir %{_jvmdir}/%{sdkdir -- %{?1}}
%{_jvmdir}/%{sdkdir -- %{?1}}/release
%dir %{_jvmdir}/%{sdkdir -- %{?1}}/bin
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/java
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/%{alt_java_name}
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/jcmd
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/keytool
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/rmiregistry
%dir %{_jvmdir}/%{sdkdir -- %{?1}}/lib
%ifarch %{jit_arches}
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/classlist
%endif
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/jexec
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/jspawnhelper
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/jrt-fs.jar
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/modules
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/psfont.properties.ja
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/psfontj2d.properties
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/tzdb.dat
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/tzdb.dat.upstream
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/libjli.so
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/jvm.cfg
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/libattach.so
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/libawt.so
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/libextnet.so
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/libjsig.so
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/libawt_headless.so
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/libdt_socket.so
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/libfontmanager.so
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/libfreetype.so
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/libinstrument.so
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/libj2gss.so
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/libj2pcsc.so
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/libj2pkcs11.so
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/libjaas.so
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/libjava.so
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/libjavajpeg.so
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/libjdwp.so
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/libjimage.so
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/libjsound.so
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/liblcms.so
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/lible.so
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/libmanagement.so
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/libmanagement_agent.so
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/libmanagement_ext.so
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/libmlib_image.so
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/libnet.so
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/libnio.so
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/libprefs.so
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/librmi.so
# Some architectures don't have the serviceability agent
%ifarch %{sa_arches}
%ifnarch %{zero_arches}
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/libsaproc.so
%endif
%endif
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/libsctp.so
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/libsystemconf.so
%ifarch %{svml_arches}
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/libjsvml.so
%endif
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/libsyslookup.so
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/libverify.so
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/libzip.so
%dir %{_jvmdir}/%{sdkdir -- %{?1}}/lib/jfr
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/jfr/default.jfc
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/jfr/profile.jfc
%{_jvmdir}/%{sdkdir -- %{?1}}/man/man1/java.1
%{_jvmdir}/%{sdkdir -- %{?1}}/man/man1/%{alt_java_name}.1
%{_jvmdir}/%{sdkdir -- %{?1}}/man/man1/jcmd.1
%{_jvmdir}/%{sdkdir -- %{?1}}/man/man1/keytool.1
%{_jvmdir}/%{sdkdir -- %{?1}}/man/man1/rmiregistry.1
%dir %{_jvmdir}/%{sdkdir -- %{?1}}/lib/%{vm_variant}
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/%{vm_variant}/*.so
%ifarch %{share_arches}
%attr(444, root, root) %{_jvmdir}/%{sdkdir -- %{?1}}/lib/%{vm_variant}/classes.jsa
%ifnarch %{ix86} %{arm32}
%attr(444, root, root) %{_jvmdir}/%{sdkdir -- %{?1}}/lib/%{vm_variant}/classes_nocoops.jsa
%endif
%endif
%dir %{etcjavasubdir}
%dir %{etcjavadir -- %{?1}}
%dir %{etcjavadir -- %{?1}}/lib
%dir %{etcjavadir -- %{?1}}/lib/security
%{etcjavadir -- %{?1}}/lib/security/cacerts
%{etcjavadir -- %{?1}}/lib/security/cacerts.upstream
%dir %{etcjavadir -- %{?1}}/conf
%dir %{etcjavadir -- %{?1}}/conf/sdp
%dir %{etcjavadir -- %{?1}}/conf/management
%dir %{etcjavadir -- %{?1}}/conf/security
%dir %{etcjavadir -- %{?1}}/conf/security/policy
%dir %{etcjavadir -- %{?1}}/conf/security/policy/limited
%dir %{etcjavadir -- %{?1}}/conf/security/policy/unlimited
%config(noreplace) %{etcjavadir -- %{?1}}/lib/security/default.policy
%config(noreplace) %{etcjavadir -- %{?1}}/lib/security/blocked.certs
%config(noreplace) %{etcjavadir -- %{?1}}/lib/security/public_suffix_list.dat
%config(noreplace) %{etcjavadir -- %{?1}}/conf/security/policy/limited/exempt_local.policy
%config(noreplace) %{etcjavadir -- %{?1}}/conf/security/policy/limited/default_local.policy
%config(noreplace) %{etcjavadir -- %{?1}}/conf/security/policy/limited/default_US_export.policy
%config(noreplace) %{etcjavadir -- %{?1}}/conf/security/policy/unlimited/default_local.policy
%config(noreplace) %{etcjavadir -- %{?1}}/conf/security/policy/unlimited/default_US_export.policy
 %{etcjavadir -- %{?1}}/conf/security/policy/README.txt
%config(noreplace) %{etcjavadir -- %{?1}}/conf/security/java.policy
%config(noreplace) %{etcjavadir -- %{?1}}/conf/security/java.security
%config(noreplace) %{etcjavadir -- %{?1}}/conf/security/nss.fips.cfg
%config(noreplace) %{etcjavadir -- %{?1}}/conf/management/jmxremote.access
# This is a config template, thus not config-noreplace
%config  %{etcjavadir -- %{?1}}/conf/management/jmxremote.password.template
%config  %{etcjavadir -- %{?1}}/conf/sdp/sdp.conf.template
%config(noreplace) %{etcjavadir -- %{?1}}/conf/management/management.properties
%config(noreplace) %{etcjavadir -- %{?1}}/conf/jaxp.properties
%config(noreplace) %{etcjavadir -- %{?1}}/conf/logging.properties
%config(noreplace) %{etcjavadir -- %{?1}}/conf/net.properties
%config(noreplace) %{etcjavadir -- %{?1}}/conf/sound.properties
%{_jvmdir}/%{sdkdir -- %{?1}}/conf
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/security
%if %is_system_jdk
%if %{is_release_build -- %{?1}}
%ghost %{_bindir}/java
%ghost %{_jvmdir}/jre
%ghost %{_bindir}/%{alt_java_name}
%ghost %{_bindir}/jcmd
%ghost %{_bindir}/keytool
%ghost %{_bindir}/rmiregistry
%ghost %{_jvmdir}/jre-%{origin}
%ghost %{_jvmdir}/jre-%{javaver}
%ghost %{_jvmdir}/jre-%{javaver}-%{origin}
%endif
%endif
# https://bugzilla.redhat.com/show_bug.cgi?id=1820172
# https://docs.fedoraproject.org/en-US/packaging-guidelines/Directory_Replacement/
%ghost %{_jvmdir}/%{sdkdir -- %{?1}}/conf.rpmmoved
%ghost %{_jvmdir}/%{sdkdir -- %{?1}}/lib/security.rpmmoved
}

%define files_devel() %{expand:
%dir %{_jvmdir}/%{sdkdir -- %{?1}}/bin
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/jar
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/jarsigner
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/javac
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/javadoc
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/javap
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/jconsole
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/jdb
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/jdeps
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/jdeprscan
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/jfr
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/jimage
# Some architectures don't have the serviceability agent
%ifarch %{sa_arches}
%ifnarch %{zero_arches}
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/jhsdb
%{_jvmdir}/%{sdkdir -- %{?1}}/man/man1/jhsdb.1
%endif
%endif
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/jinfo
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/jlink
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/jmap
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/jmod
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/jps
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/jpackage
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/jrunscript
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/jshell
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/jstack
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/jstat
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/jstatd
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/jwebserver
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/serialver
%{_jvmdir}/%{sdkdir -- %{?1}}/include
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/ct.sym
%if %{with_systemtap}
%{_jvmdir}/%{sdkdir -- %{?1}}/tapset
%endif
%{_datadir}/applications/*jconsole%{?1}.desktop
%{_jvmdir}/%{sdkdir -- %{?1}}/man/man1/jar.1
%{_jvmdir}/%{sdkdir -- %{?1}}/man/man1/jarsigner.1
%{_jvmdir}/%{sdkdir -- %{?1}}/man/man1/javac.1
%{_jvmdir}/%{sdkdir -- %{?1}}/man/man1/javadoc.1
%{_jvmdir}/%{sdkdir -- %{?1}}/man/man1/javap.1
%{_jvmdir}/%{sdkdir -- %{?1}}/man/man1/jconsole.1
%{_jvmdir}/%{sdkdir -- %{?1}}/man/man1/jcmd.1
%{_jvmdir}/%{sdkdir -- %{?1}}/man/man1/jdb.1
%{_jvmdir}/%{sdkdir -- %{?1}}/man/man1/jdeprscan.1
%{_jvmdir}/%{sdkdir -- %{?1}}/man/man1/jdeps.1
%{_jvmdir}/%{sdkdir -- %{?1}}/man/man1/jfr.1
%{_jvmdir}/%{sdkdir -- %{?1}}/man/man1/jinfo.1
%{_jvmdir}/%{sdkdir -- %{?1}}/man/man1/jlink.1
%{_jvmdir}/%{sdkdir -- %{?1}}/man/man1/jmap.1
%{_jvmdir}/%{sdkdir -- %{?1}}/man/man1/jmod.1
%{_jvmdir}/%{sdkdir -- %{?1}}/man/man1/jps.1
%{_jvmdir}/%{sdkdir -- %{?1}}/man/man1/jpackage.1
%{_jvmdir}/%{sdkdir -- %{?1}}/man/man1/jrunscript.1
%{_jvmdir}/%{sdkdir -- %{?1}}/man/man1/jshell.1
%{_jvmdir}/%{sdkdir -- %{?1}}/man/man1/jstack.1
%{_jvmdir}/%{sdkdir -- %{?1}}/man/man1/jstat.1
%{_jvmdir}/%{sdkdir -- %{?1}}/man/man1/jstatd.1
%{_jvmdir}/%{sdkdir -- %{?1}}/man/man1/jwebserver.1
%{_jvmdir}/%{sdkdir -- %{?1}}/man/man1/serialver.1

%if %{with_systemtap}
%dir %{tapsetroot}
%dir %{tapsetdirttapset}
%dir %{tapsetdir}
%{tapsetdir}/*%{_arch}%{?1}.stp
%endif
%if %is_system_jdk
%if %{is_release_build -- %{?1}}
%ghost %{_bindir}/javac
%ghost %{_jvmdir}/java
%ghost %{_jvmdir}/%{alt_java_name}
%ghost %{_bindir}/jlink
%ghost %{_bindir}/jmod
%ghost %{_bindir}/jhsdb
%ghost %{_bindir}/jar
%ghost %{_bindir}/jarsigner
%ghost %{_bindir}/javadoc
%ghost %{_bindir}/javap
%ghost %{_bindir}/jconsole
%ghost %{_bindir}/jcmd
%ghost %{_bindir}/jdb
%ghost %{_bindir}/jdeps
%ghost %{_bindir}/jdeprscan
%ghost %{_bindir}/jfr
%ghost %{_bindir}/jimage
%ghost %{_bindir}/jinfo
%ghost %{_bindir}/jmap
%ghost %{_bindir}/jps
%ghost %{_bindir}/jpackage
%ghost %{_bindir}/jrunscript
%ghost %{_bindir}/jshell
%ghost %{_bindir}/jstack
%ghost %{_bindir}/jstat
%ghost %{_bindir}/jstatd
%ghost %{_bindir}/jwebserver
%ghost %{_bindir}/serialver
%ghost %{_jvmdir}/java-%{origin}
%ghost %{_jvmdir}/java-%{javaver}
%endif
%endif
}

%define files_jmods() %{expand:
%{_jvmdir}/%{sdkdir -- %{?1}}/jmods
}

%define files_demo() %{expand:
%license %{_jvmdir}/%{sdkdir -- %{?1}}/legal
%{_jvmdir}/%{sdkdir -- %{?1}}/demo
}

%define files_src() %{expand:
%license %{_jvmdir}/%{sdkdir -- %{?1}}/legal
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/src.zip
%{_jvmdir}/%{sdkdir -- %{?1}}/full_sources
%{_jvmdir}/%{sdkdir -- %{?1}}/%{generated_sources_name}
}

%define files_static_libs() %{expand:
%dir %{_jvmdir}/%{sdkdir -- %{?1}}/%{static_libs_root}
%dir %{_jvmdir}/%{sdkdir -- %{?1}}/%{static_libs_arch_dir}
%dir %{_jvmdir}/%{sdkdir -- %{?1}}/%{static_libs_install_dir}
%{_jvmdir}/%{sdkdir -- %{?1}}/%{static_libs_install_dir}/lib*.a
}

%define files_javadoc() %{expand:
%doc %{_javadocdir}/%{uniquejavadocdir -- %{?1}}
%license %{_jvmdir}/%{sdkdir -- %{?1}}/legal
%dir %{_jvmdir}/%{sdkdir -- %{?1}}
%if %is_system_jdk
%if %{is_release_build -- %{?1}}
%ghost %{_javadocdir}/java
%ghost %{_javadocdir}/java-%{origin}
%ghost %{_javadocdir}/java-%{javaver}
%endif
%endif
}

%define files_javadoc_zip() %{expand:
%doc %{_javadocdir}/%{uniquejavadocdir -- %{?1}}.zip
%doc %{_javadocdir}/%{uniquejavadocdir -- %{?1}}
%license %{_jvmdir}/%{sdkdir -- %{?1}}/legal
%dir %{_jvmdir}/%{sdkdir -- %{?1}}
%if %is_system_jdk
%if %{is_release_build -- %{?1}}
%ghost %{_javadocdir}/java-zip
%ghost %{_javadocdir}/java-%{origin}.zip
%ghost %{_javadocdir}/java-%{javaver}.zip
%endif
%endif
}

# not-duplicated requires/provides/obsoletes for normal/debug packages
%define java_rpo() %{expand:
Requires: fontconfig%{?_isa}
Requires: xorg-x11-fonts-Type1
# Require libXcomposite explicitly since it's only dynamically loaded
# at runtime. Fixes screenshot issues. See JDK-8150954.
Requires: libXcomposite%{?_isa}
# Requires rest of java
Requires: %{name}-headless%{?1}%{?_isa} = %{epoch}:%{version}-%{release}
OrderWithRequires: %{name}-headless%{?1}%{?_isa} = %{epoch}:%{version}-%{release}
# for java-X-openjdk package's desktop binding
# Where recommendations are available, recommend Gtk+ for the Swing look and feel
%if 0%{?rhel} >= 8 || 0%{?fedora} > 0
Recommends: gtk3%{?_isa}
%endif

Provides: java-%{javaver}-%{origin}%{?1} = %{epoch}:%{version}-%{release}

# Standard JPackage base provides
Provides: jre-%{javaver}%{?1} = %{epoch}:%{version}-%{release}
Provides: jre-%{javaver}-%{origin}%{?1} = %{epoch}:%{version}-%{release}
Provides: java-%{javaver}%{?1} = %{epoch}:%{version}-%{release}
%if %is_system_jdk
Provides: java-%{origin}%{?1} = %{epoch}:%{version}-%{release}
Provides: jre-%{origin}%{?1} = %{epoch}:%{version}-%{release}
Provides: java%{?1} = %{epoch}:%{version}-%{release}
Provides: jre%{?1} = %{epoch}:%{version}-%{release}
%endif
}

%define java_headless_rpo() %{expand:
# Require /etc/pki/java/cacerts
Requires: ca-certificates
# Require javapackages-filesystem for ownership of /usr/lib/jvm/ and macros
Requires: javapackages-filesystem
# Require zone-info data provided by tzdata-java sub-package
# 2024a required as of JDK-8325150
Requires: tzdata-java >= 2024a
# for support of kernel stream control
# libsctp.so.1 is being `dlopen`ed on demand
Requires: lksctp-tools%{?_isa}
# for printing support
Requires: cups-libs
# for system security properties
Requires: crypto-policies
# for FIPS PKCS11 provider
Requires: nss
# Post requires alternatives to install tool alternatives
Requires(post):   %{alternatives_requires}
# Postun requires alternatives to uninstall tool alternatives
Requires(postun): %{alternatives_requires}
# Where suggestions are available, recommend the sctp and pcsc libraries
# for optional support of kernel stream control and card reader
%if 0%{?rhel} >= 8 || 0%{?fedora} > 0
Suggests: lksctp-tools%{?_isa}, pcsc-lite-libs%{?_isa}
%endif

# Standard JPackage base provides
Provides: jre-%{javaver}-%{origin}-headless%{?1} = %{epoch}:%{version}-%{release}
Provides: jre-%{javaver}-headless%{?1} = %{epoch}:%{version}-%{release}
Provides: java-%{javaver}-%{origin}-headless%{?1} = %{epoch}:%{version}-%{release}
Provides: java-%{javaver}-headless%{?1} = %{epoch}:%{version}-%{release}
%if %is_system_jdk
Provides: java-%{origin}-headless%{?1} = %{epoch}:%{version}-%{release}
Provides: jre-%{origin}-headless%{?1} = %{epoch}:%{version}-%{release}
Provides: jre-headless%{?1} = %{epoch}:%{version}-%{release}
Provides: java-headless%{?1} = %{epoch}:%{version}-%{release}
%endif
}

%define java_devel_rpo() %{expand:
# Requires base package
Requires:         %{name}%{?1}%{?_isa} = %{epoch}:%{version}-%{release}
OrderWithRequires: %{name}-headless%{?1}%{?_isa} = %{epoch}:%{version}-%{release}
# Post requires alternatives to install tool alternatives
Requires(post):   %{alternatives_requires}
# Postun requires alternatives to uninstall tool alternatives
Requires(postun): %{alternatives_requires}

# Standard JPackage devel provides
Provides: java-sdk-%{javaver}-%{origin}%{?1} = %{epoch}:%{version}-%{release}
Provides: java-sdk-%{javaver}%{?1} = %{epoch}:%{version}-%{release}
Provides: java-%{javaver}-devel%{?1} = %{epoch}:%{version}-%{release}
Provides: java-%{javaver}-%{origin}-devel%{?1} = %{epoch}:%{version}-%{release}
%if %is_system_jdk
Provides: java-devel-%{origin}%{?1} = %{epoch}:%{version}-%{release}
Provides: java-sdk-%{origin}%{?1} = %{epoch}:%{version}-%{release}
Provides: java-devel%{?1} = %{epoch}:%{version}-%{release}
Provides: java-sdk%{?1} = %{epoch}:%{version}-%{release}
%endif
}

%define java_static_libs_rpo() %{expand:
Requires:         %{name}-devel%{?1}%{?_isa} = %{epoch}:%{version}-%{release}
OrderWithRequires: %{name}-headless%{?1}%{?_isa} = %{epoch}:%{version}-%{release}
}

%define java_jmods_rpo() %{expand:
# Requires devel package
# as jmods are bytecode, they should be OK without any _isa
Requires:         %{name}-devel%{?1} = %{epoch}:%{version}-%{release}
OrderWithRequires: %{name}-headless%{?1} = %{epoch}:%{version}-%{release}

Provides: java-%{javaver}-jmods%{?1} = %{epoch}:%{version}-%{release}
Provides: java-%{javaver}-%{origin}-jmods%{?1} = %{epoch}:%{version}-%{release}
%if %is_system_jdk
Provides: java-jmods%{?1} = %{epoch}:%{version}-%{release}
%endif
}

%define java_demo_rpo() %{expand:
Requires: %{name}%{?1}%{?_isa} = %{epoch}:%{version}-%{release}
OrderWithRequires: %{name}-headless%{?1}%{?_isa} = %{epoch}:%{version}-%{release}

Provides: java-%{javaver}-demo%{?1} = %{epoch}:%{version}-%{release}
Provides: java-%{javaver}-%{origin}-demo%{?1} = %{epoch}:%{version}-%{release}
%if %is_system_jdk
Provides: java-demo%{?1} = %{epoch}:%{version}-%{release}
Provides: java-%{origin}-demo%{?1} = %{epoch}:%{version}-%{release}
%endif
}

%define java_javadoc_rpo() %{expand:
OrderWithRequires: %{name}-headless%{?1}%{?_isa} = %{epoch}:%{version}-%{release}
# Post requires alternatives to install javadoc alternative
Requires(post):   %{alternatives_requires}
# Postun requires alternatives to uninstall javadoc alternative
Requires(postun): %{alternatives_requires}

# Standard JPackage javadoc provides
Provides: java-%{javaver}-javadoc%{?1}%{?2} = %{epoch}:%{version}-%{release}
Provides: java-%{javaver}-%{origin}-javadoc%{?1}%{?2} = %{epoch}:%{version}-%{release}
%if %is_system_jdk
Provides: java-javadoc%{?1}%{?2} = %{epoch}:%{version}-%{release}
%endif
}

%define java_src_rpo() %{expand:
Requires: %{name}-headless%{?1}%{?_isa} = %{epoch}:%{version}-%{release}

# Standard JPackage sources provides
Provides: java-%{javaver}-src%{?1} = %{epoch}:%{version}-%{release}
Provides: java-%{javaver}-%{origin}-src%{?1} = %{epoch}:%{version}-%{release}
%if %is_system_jdk
Provides: java-src%{?1} = %{epoch}:%{version}-%{release}
Provides: java-%{origin}-src%{?1} = %{epoch}:%{version}-%{release}
%endif
}

# Prevent brp-java-repack-jars from being run
%global __jar_repack 0

%global portable_name %{name}-portable
# the version must match, but sometmes we need to more precise, so including release
%global portable_version %{version}-1

Name:    java-%{javaver}-%{origin}
Version: %{newjavaver}.%{buildver}
Release: %{?eaprefix}%{rpmrelease}%{?extraver}%{?dist}.1
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
Summary: %{origin_nice} %{featurever} Runtime Environment
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

# Use 'icedtea_sync.sh' to update the following
# They are based on code contained in the IcedTea project (6.x).
# Systemtap tapsets. Zipped up to keep it small.
Source8: tapsets-icedtea-%{icedteaver}.tar.xz

# Desktop files. Adapted from IcedTea
Source9: jconsole.desktop.in

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

BuildRequires: %{portable_name}-sources >= %{portable_version}
BuildRequires: %{portable_name}-misc >= %{portable_version}
BuildRequires: %{portable_name}-docs >= %{portable_version}

%if %{include_normal_build}
BuildRequires: %{portable_name}-devel >= %{portable_version}
%if %{include_staticlibs}
BuildRequires: %{portable_name}-static-libs >= %{portable_version}
%endif
%endif
%if %{include_fastdebug_build}
BuildRequires: %{portable_name}-devel-fastdebug >= %{portable_version}
%if %{include_staticlibs}
BuildRequires: %{portable_name}-static-libs-fastdebug >= %{portable_version}
%endif
%endif
%if %{include_debug_build}
BuildRequires: %{portable_name}-devel-slowdebug >= %{portable_version}
%if %{include_staticlibs}
BuildRequires: %{portable_name}-static-libs-slowdebug >= %{portable_version}
%endif
%endif

BuildRequires: desktop-file-utils
# elfutils only are OK for build without AOT
BuildRequires: elfutils-devel
BuildRequires: gdb
# for modyfying build-id in clashing binaries
BuildRequires: /usr/bin/gcc
BuildRequires: /usr/bin/objcopy
BuildRequires: /usr/bin/readelf
# Requirement for setting and nss.fips.cfg
BuildRequires: nss-devel
# Requirement for system security property test
BuildRequires: crypto-policies
BuildRequires: pkgconfig
BuildRequires: zip
BuildRequires: unzip
BuildRequires: javapackages-filesystem
# ?
BuildRequires: tzdata-java >= 2022g

%if %{with_systemtap}
BuildRequires: systemtap-sdt-devel
%endif

# Version in src/java.desktop/share/legal/freetype.md
Provides: bundled(freetype) = 2.13.2
# Version in src/java.desktop/share/native/libsplashscreen/giflib/gif_lib.h
Provides: bundled(giflib) = 5.2.2
# Version in src/java.desktop/share/native/libharfbuzz/hb-version.h
Provides: bundled(harfbuzz) = 8.2.2
# Version in src/java.desktop/share/native/liblcms/lcms2.h
Provides: bundled(lcms2) = 2.16.0
# Version in src/java.desktop/share/native/libjavajpeg/jpeglib.h
Provides: bundled(libjpeg) = 6b
# Version in src/java.desktop/share/native/libsplashscreen/libpng/png.h
Provides: bundled(libpng) = 1.6.43
# Version in src/java.base/share/native/libzip/zlib/zlib.h
Provides: bundled(zlib) = 1.3.1

# this is always built, also during debug-only build
# when it is built in debug-only this package is just placeholder
%{java_rpo %{nil}}

%description
The %{origin_nice} %{featurever} runtime environment.

%if %{include_debug_build}
%package slowdebug
Summary: %{origin_nice} %{featurever} Runtime Environment %{debug_on}
%if (0%{?rhel} > 0 && 0%{?rhel} <= 8) || (0%{?fedora} >= 0 && 0%{?fedora} < 30)
Group:   Development/Languages
%endif

%{java_rpo -- %{debug_suffix_unquoted}}
%description slowdebug
The %{origin_nice} %{featurever} runtime environment.
%{debug_warning}
%endif

%if %{include_fastdebug_build}
%package fastdebug
Summary: %{origin_nice} %{featurever} Runtime Environment %{fastdebug_on}
%if (0%{?rhel} > 0 && 0%{?rhel} <= 8) || (0%{?fedora} >= 0 && 0%{?fedora} < 30)
Group:   Development/Languages
%endif

%{java_rpo -- %{fastdebug_suffix_unquoted}}
%description fastdebug
The %{origin_nice} %{featurever} runtime environment.
%{fastdebug_warning}
%endif

%if %{include_normal_build}
%package headless
Summary: %{origin_nice} %{featurever} Headless Runtime Environment
%if (0%{?rhel} > 0 && 0%{?rhel} <= 8) || (0%{?fedora} >= 0 && 0%{?fedora} < 30)
Group:   Development/Languages
%endif

%{java_headless_rpo %{nil}}

%description headless
The %{origin_nice} %{featurever} runtime environment without audio and video support.

%package headless-debuginfo
Summary: Debug information for package %{name}-headless
Group: Development/Debug
AutoReq: 0
AutoProv: 1
%description headless-debuginfo
This package provides debug information for package %{name}.
Debug information is useful when developing applications that use this
package or when debugging this package.
%files headless-debuginfo -f debugfiles.list

%package debugsource
Summary: Debug sources for package %{name}
Group: Development/Debug
AutoReqProv: 0
%description debugsource
This package provides debug sources for package %{name}.
Debug sources are useful when developing applications that use this
package or when debugging this package.
%files debugsource -f debugsourcefiles.list
%endif

%if %{include_debug_build}
%package headless-slowdebug
Summary: %{origin_nice} %{featurever} Runtime Environment %{debug_on}
%if (0%{?rhel} > 0 && 0%{?rhel} <= 8) || (0%{?fedora} >= 0 && 0%{?fedora} < 30)
Group:   Development/Languages
%endif

%{java_headless_rpo -- %{debug_suffix_unquoted}}

%description headless-slowdebug
The %{origin_nice} %{featurever} runtime environment without audio and video support.
%{debug_warning}
%endif

%if %{include_fastdebug_build}
%package headless-fastdebug
Summary: %{origin_nice} %{featurever} Runtime Environment %{fastdebug_on}
%if (0%{?rhel} > 0 && 0%{?rhel} <= 8) || (0%{?fedora} >= 0 && 0%{?fedora} < 30)
Group:   Development/Languages
%endif

%{java_headless_rpo -- %{fastdebug_suffix_unquoted}}

%description headless-fastdebug
The %{origin_nice} %{featurever} runtime environment without audio and video support.
%{fastdebug_warning}
%endif

%if %{include_normal_build}
%package devel
Summary: %{origin_nice} %{featurever} Development Environment
%if (0%{?rhel} > 0 && 0%{?rhel} <= 8) || (0%{?fedora} >= 0 && 0%{?fedora} < 30)
Group:   Development/Languages
%endif

%{java_devel_rpo %{nil}}

%description devel
The %{origin_nice} %{featurever} development tools.
%endif

%if %{include_debug_build}
%package devel-slowdebug
Summary: %{origin_nice} %{featurever} Development Environment %{debug_on}
%if (0%{?rhel} > 0 && 0%{?rhel} <= 8) || (0%{?fedora} >= 0 && 0%{?fedora} < 30)
Group:   Development/Languages
%endif

%{java_devel_rpo -- %{debug_suffix_unquoted}}

%description devel-slowdebug
The %{origin_nice} %{featurever} development tools.
%{debug_warning}
%endif

%if %{include_fastdebug_build}
%package devel-fastdebug
Summary: %{origin_nice} %{featurever} Development Environment %{fastdebug_on}
%if (0%{?rhel} > 0 && 0%{?rhel} <= 8) || (0%{?fedora} >= 0 && 0%{?fedora} < 30)
Group:   Development/Tools
%endif

%{java_devel_rpo -- %{fastdebug_suffix_unquoted}}

%description devel-fastdebug
The %{origin_nice} %{featurever} development tools.
%{fastdebug_warning}
%endif

%if %{include_staticlibs}

%if %{include_normal_build}
%package static-libs
Summary: %{origin_nice} %{featurever} libraries for static linking

%{java_static_libs_rpo %{nil}}

%description static-libs
The %{origin_nice} %{featurever} libraries for static linking.
%endif

%if %{include_debug_build}
%package static-libs-slowdebug
Summary: %{origin_nice} %{featurever} libraries for static linking %{debug_on}

%{java_static_libs_rpo -- %{debug_suffix_unquoted}}

%description static-libs-slowdebug
The %{origin_nice} %{featurever} libraries for static linking.
%{debug_warning}
%endif

%if %{include_fastdebug_build}
%package static-libs-fastdebug
Summary: %{origin_nice} %{featurever} libraries for static linking %{fastdebug_on}

%{java_static_libs_rpo -- %{fastdebug_suffix_unquoted}}

%description static-libs-fastdebug
The %{origin_nice} %{featurever} libraries for static linking.
%{fastdebug_warning}
%endif

# staticlibs
%endif

%if %{include_normal_build}
%package jmods
Summary: JMods for %{origin_nice} %{featurever}
%if (0%{?rhel} > 0 && 0%{?rhel} <= 8) || (0%{?fedora} >= 0 && 0%{?fedora} < 30)
Group:   Development/Languages
%endif

%{java_jmods_rpo %{nil}}

%description jmods
The JMods for %{origin_nice} %{featurever}.
%endif

%if %{include_debug_build}
%package jmods-slowdebug
Summary: JMods for %{origin_nice} %{featurever} %{debug_on}
%if (0%{?rhel} > 0 && 0%{?rhel} <= 8) || (0%{?fedora} >= 0 && 0%{?fedora} < 30)
Group:   Development/Languages
%endif

%{java_jmods_rpo -- %{debug_suffix_unquoted}}

%description jmods-slowdebug
The JMods for %{origin_nice} %{featurever}.
%{debug_warning}
%endif

%if %{include_fastdebug_build}
%package jmods-fastdebug
Summary: JMods for %{origin_nice} %{featurever} %{fastdebug_on}
%if (0%{?rhel} > 0 && 0%{?rhel} <= 8) || (0%{?fedora} >= 0 && 0%{?fedora} < 30)
Group:   Development/Tools
%endif

%{java_jmods_rpo -- %{fastdebug_suffix_unquoted}}

%description jmods-fastdebug
The JMods for %{origin_nice} %{featurever}.
%{fastdebug_warning}
%endif

%if %{include_normal_build}
%package demo
Summary: %{origin_nice} %{featurever} Demos
%if (0%{?rhel} > 0 && 0%{?rhel} <= 8) || (0%{?fedora} >= 0 && 0%{?fedora} < 30)
Group:   Development/Languages
%endif

%{java_demo_rpo %{nil}}

%description demo
The %{origin_nice} %{featurever} demos.
%endif

%if %{include_debug_build}
%package demo-slowdebug
Summary: %{origin_nice} %{featurever} Demos %{debug_on}
%if (0%{?rhel} > 0 && 0%{?rhel} <= 8) || (0%{?fedora} >= 0 && 0%{?fedora} < 30)
Group:   Development/Languages
%endif

%{java_demo_rpo -- %{debug_suffix_unquoted}}

%description demo-slowdebug
The %{origin_nice} %{featurever} demos.
%{debug_warning}
%endif

%if %{include_fastdebug_build}
%package demo-fastdebug
Summary: %{origin_nice} %{featurever} Demos %{fastdebug_on}
%if (0%{?rhel} > 0 && 0%{?rhel} <= 8) || (0%{?fedora} >= 0 && 0%{?fedora} < 30)
Group:   Development/Languages
%endif

%{java_demo_rpo -- %{fastdebug_suffix_unquoted}}

%description demo-fastdebug
The %{origin_nice} %{featurever} demos.
%{fastdebug_warning}
%endif

%if %{include_normal_build}
%package src
Summary: %{origin_nice} %{featurever} Source Bundle
%if (0%{?rhel} > 0 && 0%{?rhel} <= 8) || (0%{?fedora} >= 0 && 0%{?fedora} < 30)
Group:   Development/Languages
%endif

%{java_src_rpo %{nil}}

%description src
The %{compatiblename}-src sub-package contains the complete %{origin_nice} %{featurever}
class library source code for use by IDE indexers and debuggers.
%endif

%if %{include_debug_build}
%package src-slowdebug
Summary: %{origin_nice} %{featurever} Source Bundle %{for_debug}
%if (0%{?rhel} > 0 && 0%{?rhel} <= 8) || (0%{?fedora} >= 0 && 0%{?fedora} < 30)
Group:   Development/Languages
%endif

%{java_src_rpo -- %{debug_suffix_unquoted}}

%description src-slowdebug
The %{compatiblename}-src-slowdebug sub-package contains the complete %{origin_nice} %{featurever}
 class library source code for use by IDE indexers and debuggers, %{for_debug}.
%endif

%if %{include_fastdebug_build}
%package src-fastdebug
Summary: %{origin_nice} %{featurever} Source Bundle %{for_fastdebug}
%if (0%{?rhel} > 0 && 0%{?rhel} <= 8) || (0%{?fedora} >= 0 && 0%{?fedora} < 30)
Group:   Development/Languages
%endif

%{java_src_rpo -- %{fastdebug_suffix_unquoted}}

%description src-fastdebug
The %{compatiblename}-src-fastdebug sub-package contains the complete %{origin_nice} %{featurever}
 class library source code for use by IDE indexers and debuggers, %{for_fastdebug}.
%endif

%if %{include_normal_build}
%package javadoc
Summary: %{origin_nice} %{featurever} API documentation
%if (0%{?rhel} > 0 && 0%{?rhel} <= 8) || (0%{?fedora} >= 0 && 0%{?fedora} < 30)
Group:   Documentation
%endif
Requires: javapackages-filesystem
Obsoletes: javadoc-slowdebug < 1:13.0.0.33-1.rolling

%{java_javadoc_rpo -- %{nil} %{nil}}

%description javadoc
The %{origin_nice} %{featurever} API documentation.
%endif

%if %{include_normal_build}
%package javadoc-zip
Summary: %{origin_nice} %{featurever} API documentation compressed in a single archive
%if (0%{?rhel} > 0 && 0%{?rhel} <= 8) || (0%{?fedora} >= 0 && 0%{?fedora} < 30)
Group:   Documentation
%endif
Requires: javapackages-filesystem
Obsoletes: javadoc-zip-slowdebug < 1:13.0.0.33-1.rolling

%{java_javadoc_rpo -- %{nil} -zip}
%{java_javadoc_rpo -- %{nil} %{nil}}

%description javadoc-zip
The %{origin_nice} %{featurever} API documentation compressed in a single archive.
%endif

%prep
echo "Preparing %{oj_vendor_version}"

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

%setup -q -c -n %{uniquesuffix ""} -T
# https://bugzilla.redhat.com/show_bug.cgi?id=1189084
prioritylength=`expr length %{priority}`
if [ $prioritylength -ne 8 ] ; then
 echo "priority must be 8 digits in total, violated"
 exit 14
fi

tar -xf %{portablejvmdir}/%{compatiblename}*%{version}*portable.sources.noarch.tar.xz
tar -xf %{portablejvmdir}/%{compatiblename}*%{version}*portable*.misc.%{_arch}.tar.xz
tar -xf %{portablejvmdir}/%{compatiblename}*%{version}*portable*.docs.%{_arch}.tar.xz

%if %{include_normal_build}
tar -xf %{portablejvmdir}/%{compatiblename}*%{version}*portable.jdk.%{_arch}.tar.xz
tar -xf %{portablejvmdir}/%{compatiblename}*%{version}*portable.jmods.%{_arch}.tar.xz
# Extract debuginfo as well
tar -xf %{portablejvmdir}/%{compatiblename}*%{version}*portable.debuginfo.jdk.%{_arch}.tar.xz
%if %{include_staticlibs}
tar -xf %{portablejvmdir}/%{compatiblename}*%{version}*portable.static-libs.%{_arch}.tar.xz
%endif
%endif
%if %{include_fastdebug_build}
tar -xf %{portablejvmdir}/%{compatiblename}*%{version}*portable.fastdebug.jdk.%{_arch}.tar.xz
tar -xf %{portablejvmdir}/%{compatiblename}*%{version}*portable.fastdebug.jmods.%{_arch}.tar.xz
%if %{include_staticlibs}
tar -xf %{portablejvmdir}/%{compatiblename}*%{version}*portable.fastdebug.static-libs.%{_arch}.tar.xz
%endif
%endif
%if %{include_debug_build}
tar -xf %{portablejvmdir}/%{compatiblename}*%{version}*portable.slowdebug.jdk.%{_arch}.tar.xz
tar -xf %{portablejvmdir}/%{compatiblename}*%{version}*portable.slowdebug.jmods.%{_arch}.tar.xz
%if %{include_staticlibs}
tar -xf %{portablejvmdir}/%{compatiblename}*%{version}*portable.slowdebug.static-libs.%{_arch}.tar.xz
%endif
%endif

# print out info abot binaries used for repack. The version-less fallbacks are for development only, where can be cheated environment
echo "Those RPMs are just repacking portable tarballs extracted from portable RPMs" > %{repack_file}
echo "Usually this exact portable RPM can not be obtained via dnf install, but you can download it." >> %{repack_file}
echo "The exact info is at bottom." >> %{repack_file}
echo "All java- names and versions:" >> %{repack_file}
ls -l %{portablejvmdir} >> %{repack_file}
rpm -qa | grep "java-" >> %{repack_file}
echo "Used %{compatiblename}.*portable:" >> %{repack_file}
ls -l %{portablejvmdir} | grep "%{compatiblename}.*portable" >> %{repack_file} || echo "Not found!" >> %{repack_file}
echo "Used %{name}.*portable:" >> %{repack_file}
rpm -qa | grep "%{name}.*portable" >> %{repack_file} || echo "Not found!" >> %{repack_file}
echo "Used %{version}.*portable:" >> %{repack_file}
ls -l %{portablejvmdir} | grep "%{version}.*portable" >> %{repack_file} || echo "Not found!" >> %{repack_file}
echo "Used portable.*%{version}:" >> %{repack_file}
rpm -qa | grep "portable.*%{version}" >> %{repack_file} || echo "Not found!" >> %{repack_file}
echo "Where this is %{fullversion %{nil}}" >> %{repack_file}
portableNvr=`rpm -qa | grep %{name}-portable-misc-%{version} | sed "s/-misc-/-/" | sed "s/.%{_arch}.*//"`
if [ "x${portableNvr}" == x ] ; then
  portableNvr=`rpm -qa | grep %{name}-portable-misc- | sed "s/-misc-/-/" | sed "s/.%{_arch}.*//"`" #incorrect!"
fi
echo "Which repacked ${portableNvr}" >> %{repack_file}
echo "You can download the repacked portables from:" >> %{repack_file}
echo "https://koji.fedoraproject.org/koji/search?match=glob&type=build&terms=${portableNvr}" >> %{repack_file}
echo "`date`" >> %{repack_file}

# Extract systemtap tapsets
%if %{with_systemtap}
tar --strip-components=1 -x -I xz -f %{SOURCE8}
%if %{include_debug_build}
cp -r tapset tapset%{debug_suffix}
%endif
%if %{include_fastdebug_build}
cp -r tapset tapset%{fastdebug_suffix}
%endif

for suffix in %{build_loop} ; do
  for file in "tapset"$suffix/*.in; do
    OUTPUT_FILE=`echo $file | sed -e "s:\.stp\.in$:-%{version}-%{release}.%{_arch}.stp:g"`
    sed -e "s:@ABS_SERVER_LIBJVM_SO@:%{_jvmdir}/%{sdkdir -- $suffix}/lib/server/libjvm.so:g" $file > $file.1
    sed -e "s:@JAVA_SPEC_VER@:%{javaver}:g" $file.1 > $file.2
# TODO find out which architectures other than i686 have a client vm
%ifarch %{ix86}
    sed -e "s:@ABS_CLIENT_LIBJVM_SO@:%{_jvmdir}/%{sdkdir -- $suffix}/lib/client/libjvm.so:g" $file.2 > $OUTPUT_FILE
%else
    sed -e "/@ABS_CLIENT_LIBJVM_SO@/d" $file.2 > $OUTPUT_FILE
%endif
    sed -i -e "s:@ABS_JAVA_HOME_DIR@:%{_jvmdir}/%{sdkdir -- $suffix}:g" $OUTPUT_FILE
    sed -i -e "s:@INSTALL_ARCH_DIR@:%{archinstall}:g" $OUTPUT_FILE
    sed -i -e "s:@prefix@:%{_jvmdir}/%{sdkdir -- $suffix}/:g" $OUTPUT_FILE
  done
done
# systemtap tapsets ends
%endif

# Prepare desktop files
# The _X_ syntax indicates variables that are replaced by make upstream
# The @X@ syntax indicates variables that are replaced by configure upstream
for suffix in %{build_loop} ; do
for file in %{SOURCE9}; do
    FILE=`basename $file | sed -e s:\.in$::g`
    EXT="${FILE##*.}"
    NAME="${FILE%.*}"
    OUTPUT_FILE=$NAME$suffix.$EXT
    sed    -e  "s:_SDKBINDIR_:%{sdkbindir -- $suffix}:g" $file > $OUTPUT_FILE
    sed -i -e  "s:@target_cpu@:%{_arch}:g" $OUTPUT_FILE
    sed -i -e  "s:@OPENJDK_VER@:%{version}-%{release}.%{_arch}$suffix:g" $OUTPUT_FILE
    sed -i -e  "s:@JAVA_VER@:%{javaver}:g" $OUTPUT_FILE
    sed -i -e  "s:@JAVA_VENDOR@:%{origin}:g" $OUTPUT_FILE
done
done

%build
# we need to symlink sources to expected location, so debuginfo strip can locate debugsources
src_image=`ls -d %{compatiblename}*%{version}*portable.sources.noarch`
misc_image=`ls -d %{compatiblename}*%{version}*portable.misc.%{_arch}`
cp -rf $misc_image/%{generated_sources_name}/%{vcstag}/ $src_image # it would be nice to remove them once debugsources are generated:(
ln -s $src_image/%{vcstag} %{vcstag}
mkdir build
pushd build
  cp -r ../$misc_image/%{generated_sources_name}/jdk%{featurever}.build* .
popd
doc_image=`ls -d %{compatiblename}*%{version}*portable.docs.%{_arch}`

%install
function installjdk() {
    local imagepath=${1}

    if [ -d ${imagepath} ] ; then
        # the build (erroneously) removes read permissions from some jars
        # this is a regression in OpenJDK 7 (our compiler):
        # http://icedtea.classpath.org/bugzilla/show_bug.cgi?id=1437
        find ${imagepath} -iname '*.jar' -exec chmod ugo+r {} \;

        # Build screws up permissions on binaries
        # https://bugs.openjdk.java.net/browse/JDK-8173610
        find ${imagepath} -iname '*.so' -exec chmod +x {} \;
        find ${imagepath}/bin/ -exec chmod +x {} \;

        # Install nss.cfg right away as we will be using the JRE above
      	#is already there from portables
        # Install nss.fips.cfg: NSS configuration for global FIPS mode (crypto-policies)
      	#is already there from portables

        # Turn on system security properties
        sed -i -e "s:^security.useSystemPropertiesFile=.*:security.useSystemPropertiesFile=true:" \
            ${imagepath}/conf/security/java.security

        # Use system-wide tzdata
        mv ${imagepath}/lib/tzdb.dat{,.upstream}
        ln -sv %{javazidir}/tzdb.dat ${imagepath}/lib/tzdb.dat

        # Rename OpenJDK cacerts database
        mv ${imagepath}/lib/security/cacerts{,.upstream}
        # Install cacerts symlink needed by some apps which hard-code the path
        ln -sv /etc/pki/java/cacerts ${imagepath}/lib/security

        # add alt-java man page
	#  alt-java man and bianry are here from portables. Or not?
    fi
}

# Checks on debuginfo must be performed before the files are stripped
# by the RPM installation stage
function debugcheckjdk() {
    local imagepath=${1}
    local debug_suffix=${2}

    if [ -d ${imagepath} ] ; then

        # Check debug symbols are present and can identify code
        find "${imagepath}" -iname "*.$debug_suffix" -print0 | while read -d $'\0' lib
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
                if eu-readelf -S "$lib" | grep "\] .gnu_debuglink" | grep PROGBITS; then
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
        gdb -q "${imagepath}/bin/java" <<EOF | tee gdb.out
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

    fi
}

for suffix in %{build_loop} ; do
  if [ "x$suffix" = "x" ] ; then
      debugbuild=""
  else
      # change -something to .something
      debugbuild=`echo $suffix  | sed "s/-/./g"`
  fi
  # Final setup on the untarred images
  # TODO revisit. jre may be complety useless to unpack and process,
  # as all the files are taken from JDK tarball ans put to packages manually.
  # jre tarball may be usefull for  checking integrity of jre and jre headless subpackages
  #for jdkjre in jdk jre ; do
  for jdkjre in jdk ; do
    buildoutputdir=`ls -d %{compatiblename}*portable${debugbuild}.${jdkjre}*`
    top_dir_abs_main_build_path=$(pwd)/${buildoutputdir}
    installjdk ${top_dir_abs_main_build_path}
    # it may happen, that some library - in original case libjsvml build identically for two jdks
    # it is becasue of our ld/gcc flags - otherwise rpm build enhances each binarry by full path to it
    # if it is hit then this library needs to have build-id repalced - note, that it do not affect dbugability
    clashinglibs=""
%ifarch %{svml_arches}
    clashinglibs="$clashinglibs lib/libjsvml.so"
%endif
    for lib in $clashinglibs ; do
      libjsvmlgcchackdir=`mktemp -d`
      pushd $libjsvmlgcchackdir
        libjsvml=${top_dir_abs_main_build_path}/$lib
        ls -l $libjsvml
        echo "#include <stdio.h>" > a.c
        echo "int main(void) {  printf(\"$libjsvml\"); }" >> a.c
        gcc a.c -o exe
        readelf -n  exe | grep "Build ID"
        readelf -n  $libjsvml | grep "Build ID"
        objcopy --dump-section .note.gnu.build-id=id exe
        objcopy --update-section  .note.gnu.build-id=id $libjsvml
        readelf -n $libjsvml | grep -i "Build ID"
      popd
      rm -rf $libjsvmlgcchackdir
    done
    # Check debug symbols were built into the dynamic libraries
    if [ $jdkjre == jdk ] ; then
      if [ "x$suffix" = "x" ] ; then
        debugsuffix="debuginfo"
      else
        debugsuffix="so"
      fi
      #jdk only?
      debugcheckjdk ${top_dir_abs_main_build_path} $debugsuffix
    fi
    # Print release information
    cat ${top_dir_abs_main_build_path}/release
  done
# build cycles
done # end of release / debug cycle loop

STRIP_KEEP_SYMTAB=libjvm*

for suffix in %{build_loop} ; do
  if [ "x$suffix" = "x" ] ; then
      debugbuild=""
  else
      # change -something to .something
      debugbuild=`echo $suffix  | sed "s/-/./g"`
  fi
  buildoutputdir=`ls -d %{compatiblename}*portable${debugbuild}.jdk*`
  top_dir_abs_main_build_path=$(pwd)/${buildoutputdir}
%if %{include_staticlibs}
  top_dir_abs_staticlibs_build_path=`ls -d $top_dir_abs_main_build_path/lib/static/*/glibc/`
%endif
  jdk_image=${top_dir_abs_main_build_path}
  src_image=`echo ${top_dir_abs_main_build_path} | sed "s/portable.*.%{_arch}/portable.sources.noarch/"`
  misc_image=`echo ${top_dir_abs_main_build_path} | sed "s/portable.*.%{_arch}/portable.misc.%{_arch}/"`
  docs_image=`echo ${top_dir_abs_main_build_path} | sed "s/portable.*.%{_arch}/portable.docs.%{_arch}/"`

# Install the jdk
mkdir -p $RPM_BUILD_ROOT%{_jvmdir}

# Install icons
for s in 16 24 32 48 ; do
  install -D -p -m 644 \
     ${src_image}/%{vcstag}/src/java.desktop/unix/classes/sun/awt/X11/java-icon${s}.png \
     $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${s}x${s}/apps/java-%{javaver}-%{origin}.png
done


cp -a ${jdk_image} $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir -- $suffix}
cp -a ${src_image} $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir -- $suffix}/full_sources
cp -a ${misc_image}/%{generated_sources_name} $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir -- $suffix}
cp -a ${misc_image}/alt-java $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir -- $suffix}/bin
install -d -m 755 $RPM_BUILD_ROOT%{_defaultdocdir}/%{uniquejavadocdir -- $suffix}
cp %{repack_file} $RPM_BUILD_ROOT%{_defaultdocdir}/%{uniquejavadocdir --  $suffix}/%{fullversion -- %{nil}}.specfile

pushd ${jdk_image}

%if %{with_systemtap}
  # Install systemtap support files
  install -dm 755 $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir -- $suffix}/tapset
  # note, that uniquesuffix  is in BUILD dir in this case
  cp -a $RPM_BUILD_DIR/%{uniquesuffix ""}/tapset$suffix/*.stp $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir -- $suffix}/tapset/
  pushd  $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir -- $suffix}/tapset/
   tapsetFiles=`ls *.stp`
  popd
  install -d -m 755 $RPM_BUILD_ROOT%{tapsetdir}
  for name in $tapsetFiles ; do
    targetName=`echo $name | sed "s/.stp/$suffix.stp/"`
    ln -srvf $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir -- $suffix}/tapset/$name $RPM_BUILD_ROOT%{tapsetdir}/$targetName
  done
%endif

popd

# Install static libs artefacts
%if %{include_staticlibs}
mkdir -p $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir -- $suffix}/%{static_libs_install_dir}
cp -a ${top_dir_abs_staticlibs_build_path}/*.a $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir -- $suffix}/%{static_libs_install_dir}
%endif

if ! echo $suffix | grep -q "debug" ; then
  # Install Javadoc documentation
  install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}
  install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{uniquejavadocdir -- $suffix}
  built_doc_archive=$(basename $(ls ${docs_image}/jdk*docs.zip))
  cp -a ${docs_image}/${built_doc_archive} \
     $RPM_BUILD_ROOT%{_javadocdir}/%{uniquejavadocdir -- $suffix}.zip
  pushd $RPM_BUILD_ROOT%{_javadocdir}/%{uniquejavadocdir -- $suffix}
    unzip ${docs_image}/${built_doc_archive} 
  popd
fi

# Install release notes
commondocdir=${RPM_BUILD_ROOT}%{_defaultdocdir}/%{uniquejavadocdir -- $suffix}
install -d -m 755 ${commondocdir}
cp -a ${top_dir_abs_main_build_path}/NEWS ${commondocdir}

# Install desktop files
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/{applications,pixmaps}
for e in jconsole$suffix ; do
    desktop-file-install --vendor=%{uniquesuffix -- $suffix} --mode=644 \
        --dir=$RPM_BUILD_ROOT%{_datadir}/applications $e.desktop
done

# Install /etc/.java/.systemPrefs/ directory
# See https://bugzilla.redhat.com/show_bug.cgi?id=741821
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/.java/.systemPrefs

# moving config files to /etc
mkdir -p $RPM_BUILD_ROOT/%{etcjavadir -- $suffix}
mkdir -p $RPM_BUILD_ROOT/%{etcjavadir -- $suffix}/lib
mv $RPM_BUILD_ROOT/%{_jvmdir}/%{sdkdir -- $suffix}/conf/  $RPM_BUILD_ROOT/%{etcjavadir -- $suffix}
mv $RPM_BUILD_ROOT/%{_jvmdir}/%{sdkdir -- $suffix}/lib/security  $RPM_BUILD_ROOT/%{etcjavadir -- $suffix}/lib
pushd $RPM_BUILD_ROOT/%{_jvmdir}/%{sdkdir -- $suffix}
  ln -srv $RPM_BUILD_ROOT%{etcjavadir -- $suffix}/conf  ./conf
popd
pushd $RPM_BUILD_ROOT/%{_jvmdir}/%{sdkdir -- $suffix}/lib
  ln -srv $RPM_BUILD_ROOT%{etcjavadir -- $suffix}/lib/security  ./security
popd
# end moving files to /etc

#TODO this is done also i portables and in install jdk. But hard to say where the operation will hapen at the end
# stabilize permissions
find $RPM_BUILD_ROOT/%{_jvmdir}/%{sdkdir -- $suffix}/ -name "*.so" -exec chmod 755 {} \; ;
find $RPM_BUILD_ROOT/%{_jvmdir}/%{sdkdir -- $suffix}/ -type d -exec chmod 755 {} \; ;
find $RPM_BUILD_ROOT/%{_jvmdir}/%{sdkdir -- $suffix}/legal -type f -exec chmod 644 {} \; ;

# end, dual install
done

# Produce the debugsourcefiles.list manually from sources
%{__mkdir} -p $RPM_BUILD_ROOT/usr/src/debug
cp -a ${src_image} $RPM_BUILD_ROOT/usr/src/debug/%{name}-%{version}-%{release}
pushd $RPM_BUILD_ROOT/usr
find src/debug -mindepth 1 -maxdepth 1 | sed 's,^,/usr/,' >> %{_builddir}/%{compatiblename}/debugsourcefiles.list
popd

# Produce the debugfiles.list and debuginfo tree manually from existing debuginfo
%{__mkdir} -p $RPM_BUILD_ROOT/usr/lib/debug/%{_jvmdir}/%{sdkdir -- %{normal_suffix}}/lib/server
%{__mkdir} -p $RPM_BUILD_ROOT/usr/lib/debug/%{_jvmdir}/%{sdkdir -- %{normal_suffix}}/bin
pushd $RPM_BUILD_ROOT
for f in $(find .%{_jvmdir}/%{sdkdir -- %{normal_suffix}} -name \*.debuginfo); do
  %{__mv} $f "$RPM_BUILD_ROOT/usr/lib/debug/$(dirname $f)/$(basename $f)"
done
popd
pushd $RPM_BUILD_ROOT/usr/lib/debug%{_jvmdir}
find %{compatiblename} -name \*.debuginfo | sed 's,^,/usr/lib/debug%{_jvmdir}/,' >> %{_builddir}/%{compatiblename}/debugfiles.list
popd

%check

# We test debug first as it will give better diagnostics on a crash
for suffix in %{build_loop} ; do

# Tests in the check stage are performed on the installed image
# rpmbuild operates as follows: build -> install -> test
export JAVA_HOME=${RPM_BUILD_ROOT}%{_jvmdir}/%{sdkdir -- $suffix}

#check Shenandoah is enabled
%if %{use_shenandoah_hotspot}
$JAVA_HOME/bin/java -XX:+UseShenandoahGC -version
%endif

# Check unlimited policy has been used
$JAVA_HOME/bin/javac -d . %{SOURCE13}
$JAVA_HOME/bin/java --add-opens java.base/javax.crypto=ALL-UNNAMED TestCryptoLevel

# Check ECC is working
$JAVA_HOME/bin/javac -d . %{SOURCE14}
$JAVA_HOME/bin/java $(echo $(basename %{SOURCE14})|sed "s|\.java||")

# Check system crypto (policy) is active and can be disabled
# Test takes a single argument - true or false - to state whether system
# security properties are enabled or not.
$JAVA_HOME/bin/javac -d . %{SOURCE15}
export PROG=$(echo $(basename %{SOURCE15})|sed "s|\.java||")
export SEC_DEBUG="-Djava.security.debug=properties"
$JAVA_HOME/bin/java ${SEC_DEBUG} ${PROG} true
$JAVA_HOME/bin/java ${SEC_DEBUG} -Djava.security.disableSystemPropertiesFile=true ${PROG} false

# Check java launcher has no SSB mitigation
if ! nm $JAVA_HOME/bin/java | grep set_speculation ; then true ; else false; fi

# Check alt-java launcher has SSB mitigation on supported architectures
# set_speculation function exists in both cases, so check for prctl call
%ifarch %{ssbd_arches}
nm $JAVA_HOME/bin/%{alt_java_name} | grep prctl
%else
if ! nm $JAVA_HOME/bin/%{alt_java_name} | grep prctl ; then true ; else false; fi
%endif

# Check correct vendor values have been set
$JAVA_HOME/bin/javac -d . %{SOURCE16}
#TODO skipped vendor check. It now points to PORTABLE version of jdk.
#$JAVA_HOME/bin/java $(echo $(basename %{SOURCE16})|sed "s|\.java||") "%{oj_vendor}" "%{oj_vendor_url}" "%{oj_vendor_bug_url}" "%{oj_vendor_version}"

# Check translations are available for new timezones
$JAVA_HOME/bin/javac -d . %{SOURCE18}
#TODO doublecheck tzdata handling
$JAVA_HOME/bin/java $(echo $(basename %{SOURCE18})|sed "s|\.java||") JRE || echo "TZDATA no longer can be synced with system, because we repack"
$JAVA_HOME/bin/java -Djava.locale.providers=CLDR $(echo $(basename %{SOURCE18})|sed "s|\.java||") CLDR || echo "TZDATA no longer can be synced with system, because we repack"

%if %{include_staticlibs}
# Check debug symbols in static libraries (smoke test)
export STATIC_LIBS_HOME=${JAVA_HOME}/%{static_libs_install_dir}
readelf --debug-dump $STATIC_LIBS_HOME/libnet.a | grep Inet4AddressImpl.c
readelf --debug-dump $STATIC_LIBS_HOME/libnet.a | grep Inet6AddressImpl.c
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

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/
# recommends an explicit "exit 0" at the end of each scriptlet.  Keep
# them in this section instead of in the parameterized macro
# definitions, so that multiple macros can be called without worrying
# about which one ends with "exit 0".
%if %{include_normal_build}
%post
%{post_script %{nil}}
exit 0

# Allow upgrades from packages that have /usr/lib/jvm/java-21-openjdk
# as an alternatives symlink, without running into the known RPM
# limitation when changing to a directory a symlink to a directory.
# See also javadoc and javadoc-zip subpackages for
# /usr/share/javadoc/java-21-openjdk, which was a symlink before.
# /etc/java/java-21-openjdk is OK because it was always a directory.
# Reference:
# https://docs.fedoraproject.org/en-US/packaging-guidelines/Directory_Replacement/
%define lua_delete_old_link() %{expand:
path = "%{1}"
st = posix.stat(path)
if st and st.type == "link" then
  os.remove(path)
end
}

%pretrans headless -p <lua>
%{lua_delete_old_link -- %{_jvmdir}/%{sdkdir -- %{?1}}}

%post headless
%{post_headless %{nil}}
exit 0

%postun
%{postun_script %{nil}}
exit 0

%preun headless
%{preun_headless %{nil}}
exit 0

%posttrans
%{posttrans_script %{nil}}
exit 0

%post devel
%{post_devel %{nil}}
exit 0

%preun devel
%{preun_devel %{nil}}
exit 0

%postun devel
%{postun_devel %{nil}}
exit 0

%posttrans devel
%{posttrans_devel %{nil}}
exit 0

%pretrans javadoc -p <lua>
%{lua_delete_old_link -- %{_jvmdir}/%{sdkdir -- %{?1}}}
%{lua_delete_old_link -- %{_javadocdir}/%{uniquejavadocdir -- %{?1}}}

%post javadoc
%{alternatives_javadoc_install %{nil}}
exit 0

%preun javadoc
%{preun_javadoc %{nil}}
exit 0

%pretrans javadoc-zip -p <lua>
%{lua_delete_old_link -- %{_jvmdir}/%{sdkdir -- %{?1}}}
%{lua_delete_old_link -- %{_javadocdir}/%{uniquejavadocdir -- %{?1}}}

%post javadoc-zip
%{alternatives_javadoczip_install %{nil}}
exit 0

%preun javadoc-zip
%{preun_javadoc_zip %{nil}}
exit 0
%endif

%if %{include_debug_build}
%post slowdebug
%{post_script -- %{debug_suffix_unquoted}}
exit 0

%post headless-slowdebug
%{post_headless -- %{debug_suffix_unquoted}}
exit 0

%postun slowdebug
%{postun_script -- %{debug_suffix_unquoted}}
exit 0

%preun headless-slowdebug
%{preun_headless -- %{debug_suffix_unquoted}}
exit 0

%posttrans slowdebug
%{posttrans_script -- %{debug_suffix_unquoted}}
exit 0

%post devel-slowdebug
%{post_devel -- %{debug_suffix_unquoted}}
exit 0

%preun devel-slowdebug
%{preun_devel -- %{debug_suffix_unquoted}}
exit 0

%postun devel-slowdebug
%{postun_devel -- %{debug_suffix_unquoted}}
exit 0

%posttrans devel-slowdebug
%{posttrans_devel -- %{debug_suffix_unquoted}}
exit 0
%endif

%if %{include_fastdebug_build}
%post fastdebug
%{post_script -- %{fastdebug_suffix_unquoted}}
exit 0

%post headless-fastdebug
%{post_headless -- %{fastdebug_suffix_unquoted}}
exit 0

%postun fastdebug
%{postun_script -- %{fastdebug_suffix_unquoted}}
exit 0

%preun headless-fastdebug
%{preun_headless -- %{fastdebug_suffix_unquoted}}
exit 0

%posttrans fastdebug
%{posttrans_script -- %{fastdebug_suffix_unquoted}}
exit 0

%post devel-fastdebug
%{post_devel -- %{fastdebug_suffix_unquoted}}
exit 0

%preun devel-fastdebug
%{preun_devel -- %{fastdebug_suffix_unquoted}}
exit 0

%postun devel-fastdebug
%{postun_devel -- %{fastdebug_suffix_unquoted}}
exit 0

%posttrans devel-fastdebug
%{posttrans_devel -- %{fastdebug_suffix_unquoted}}
exit 0
%endif

%if %{include_normal_build}
%files
# main package builds always
%{files_jre %{nil}}
%else
%files
# placeholder
%endif

%if %{include_normal_build}
%files headless
%{files_jre_headless %{nil}}

%files devel
%{files_devel %{nil}}

%if %{include_staticlibs}
%files static-libs
%{files_static_libs %{nil}}
%endif

%files jmods
%{files_jmods %{nil}}

%files demo
%{files_demo %{nil}}

%files src
%{files_src %{nil}}

%files javadoc
%{files_javadoc %{nil}}

# This puts a huge documentation file in /usr/share
# It is now architecture-dependent, as eg. AOT and Graal are now x86_64 only
# same for debug variant
%files javadoc-zip
%{files_javadoc_zip %{nil}}
%endif

%if %{include_debug_build}
%files slowdebug
%{files_jre -- %{debug_suffix_unquoted}}

%files headless-slowdebug
%{files_jre_headless -- %{debug_suffix_unquoted}}

%files devel-slowdebug
%{files_devel -- %{debug_suffix_unquoted}}

%if %{include_staticlibs}
%files static-libs-slowdebug
%{files_static_libs -- %{debug_suffix_unquoted}}
%endif

%files jmods-slowdebug
%{files_jmods -- %{debug_suffix_unquoted}}

%files demo-slowdebug
%{files_demo -- %{debug_suffix_unquoted}}

%files src-slowdebug
%{files_src -- %{debug_suffix_unquoted}}
%endif

%if %{include_fastdebug_build}
%files fastdebug
%{files_jre -- %{fastdebug_suffix_unquoted}}

%files headless-fastdebug
%{files_jre_headless -- %{fastdebug_suffix_unquoted}}

%files devel-fastdebug
%{files_devel -- %{fastdebug_suffix_unquoted}}

%if %{include_staticlibs}
%files static-libs-fastdebug
%{files_static_libs -- %{fastdebug_suffix_unquoted}}
%endif

%files jmods-fastdebug
%{files_jmods -- %{fastdebug_suffix_unquoted}}

%files demo-fastdebug
%{files_demo -- %{fastdebug_suffix_unquoted}}

%files src-fastdebug
%{files_src -- %{fastdebug_suffix_unquoted}}

%endif

%changelog
## START: Generated by rpmautospec
* Mon Apr 06 2026 azldev <> - 1:21.0.8.0.9-4
- Latest state for java-21-openjdk

* Wed Jul 30 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 1:21.0.8.0.9-3
- Fix flatpak build of debuginfo

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:21.0.8.0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 22 2025 Jiri Vanek <jvanek@redhat.com> - 1:21.0.8.0.9-1
- July 2025 CPU

* Fri Jun 06 2025 Jiri <jvanek@redhat.com> - 1:21.0.7.0.6-2
- adapted to missing unstripped portable pkg

* Thu Apr 17 2025 Jiří Andrlík <jandrlik@redhat.com> - 1:21.0.7.0.6-1
- April CPU 2025

* Tue Feb 25 2025 Jiri Vanek <jvanek@redhat.com> - 1:21.0.6.0.7-11
- introduced NVRA.specfile in doc

* Wed Feb 12 2025 Jiri <jvanek@redhat.com> - 1:21.0.6.0.7-10
- adapted license to modern fomrats

* Wed Feb 12 2025 Jiri <jvanek@redhat.com> - 1:21.0.6.0.7-9
- Added jcmd ghost

* Sun Feb 02 2025 Jiri Vanek <jvanek@redhat.com> - 1:21.0.6.0.7-8
- Made fullversion() trully expandable, removed dangling quote

* Sun Feb 02 2025 Jiri Vanek <jvanek@redhat.com> - 1:21.0.6.0.7-7
- Minor cleanup

* Sun Feb 02 2025 Jiri Vanek <jvanek@redhat.com> - 1:21.0.6.0.7-6
- Moved fastdebug/slowdebug to proper place in full name

* Sun Feb 02 2025 Jiri Vanek <jvanek@redhat.com> - 1:21.0.6.0.7-5
- Returned autoprovides

* Sun Feb 02 2025 Jiri Vanek <jvanek@redhat.com> - 1:21.0.6.0.7-4
- Added NVRA symlink poinitng to main dir of java-21-openjdk

* Sun Feb 02 2025 Jiri Vanek <jvanek@redhat.com> - 1:21.0.6.0.7-3
- Removed release again. It miscalcualtes

* Sun Feb 02 2025 Jiri Vanek <jvanek@redhat.com> - 1:21.0.6.0.7-2
- Removed parallel installs support

* Tue Jan 28 2025 Jiri Vanek <jvanek@redhat.com> - 1:21.0.6.0.7-1
- January CPU 2025

* Tue Jan 28 2025 Jiri Vanek <jvanek@redhat.com> - 1:21.0.5.0.11-4
- Revert "Rebuilt for
  https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild"

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:21.0.5.0.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Oct 19 2024 Jiri <jvanek@redhat.com> - 1:21.0.5.0.11-2
- Removed hardcoded 21

* Sat Oct 19 2024 Jiri <jvanek@redhat.com> - 1:21.0.5.0.11-1
- October CPU repack

* Tue Sep 17 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 1:21.0.4.0.7-2
- Fix flatpak build

* Sat Jul 20 2024 Jiri <jvanek@redhat.com> - 1:21.0.4.0.7-1
- July CPU

* Sat Jul 20 2024 Jiri <jvanek@redhat.com> - 1:21.0.3.0.9-3
- Revert "Rebuilt for
  https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild"

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:21.0.3.0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed May 01 2024 Jiri <jvanek@redhat.com> - 1:21.0.3.0.9-1
- repacking april CPU portables

* Wed May 01 2024 Jiri <jvanek@redhat.com> - 1:21.0.2.0.13-6
- Added repack.info with information about original portables

* Thu Mar 14 2024 Jiri Vanek <jvanek@redhat.com> - 1:21.0.2.0.13-5
- bumped release

* Thu Mar 14 2024 Songsong Zhang <u2fsdgvkx1@gmail.com> - 1:21.0.2.0.13-4
- Add riscv64 support

* Thu Feb 15 2024 Petra Alice Mikova <petra.alice.mikova@gmail.com> - 1:21.0.2.0.13-3
- Make jdk21 system jdk

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:21.0.2.0.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Jiri Vanek <jvanek@redhat.com> - 1:21.0.2.0.13-1
- forked from java-latest-openjdk
## END: Generated by rpmautospec
