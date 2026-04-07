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
# $ rpmbuild -ba java-latest-openjdk.spec
#
# Produce only release builds (no debug builds) on x86_64:
# $ rpmbuild -ba java-latest-openjdk.spec --without slowdebug --without fastdebug
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
# Build with system libraries
%bcond_with system_libs

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
# Set of architectures for which java has intrinsics for Arrays.sort (libsimdsort.so)
%global simdsort_arches x86_64
# Set of architectures for which SLEEF is used for vector math operations
%global sleef_arches aarch64 riscv64
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
%global featurever 26
%global interimver 0
%global updatever 0
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
# Define current Git revision for the crypto policy & FIPS support patches
%global fipsver df044414ef4
# Define nssadapter version
%global nssadapter_version 0.1.0
%global nssadapter_name nssadapter-%{nssadapter_version}
# Define whether the crypto policy is expected to be active when testing
%global crypto_policy_active true
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
%global top_level_dir_name   %{vcstag}-
%global top_level_dir_name_backup %{top_level_dir_name}-backup
%global buildver        32
%global rpmrelease      3
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
%global compatiblename  %{name}
# TODO think about renaming  tarball in portables so it matches and compatiblename and drop portable_compatiblename
# It may be better to keep portables tarball as it is, as it nicely points out what is going from portables to rpms
%global portable_compatiblename java-%{featurever}-%{origin}
%define fullversion()     %{expand:%{compatiblename}%{?1}-%{version}-%{release}}
# output dir stub for nssadapter and proeprties
%define installoutputdir() %{expand:jdk%{featurever}.install-nsscp%{?1}}
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
%global _privatelibs libsplashscreen[.]so.*|libawt_xawt[.]so.*|libjli[.]so.*|libattach[.]so.*|libawt[.]so.*|libextnet[.]so.*|libawt_headless[.]so.*|libdt_socket[.]so.*|libfontmanager[.]so.*|libinstrument[.]so.*|libj2gss[.]so.*|libj2pcsc[.]so.*|libj2pkcs11[.]so.*|libjaas[.]so.*|libjavajpeg[.]so.*|libjdwp[.]so.*|libjimage[.]so.*|libjsound[.]so.*|libjsvml[.]so.*|liblcms[.]so.*|libmanagement[.]so.*|libmanagement_agent[.]so.*|libmanagement_ext[.]so.*|libmlib_image[.]so.*|libnet[.]so.*|libnio[.]so.*|libprefs[.]so.*|librmi[.]so.*|libsaproc[.]so.*|libsctp[.]so.*|libsimdsort[.]so.*|libsleef[.]so.*|libsyslookup[.]so.*|libzip[.]so.*%{freetype_lib}
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
  --slave %{_bindir}/jnativescan jnativescan %{sdkbindir -- %{?1}}/jmap \\
  --slave %{_bindir}/jps jps %{sdkbindir -- %{?1}}/jps \\
  --slave %{_bindir}/jpackage jpackage %{sdkbindir -- %{?1}}/jpackage \\
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
  --slave %{_mandir}/man1/jnativescan.1%{man_comp} jnativescan.1%{man_comp} %{_jvmdir}/%{sdkdir -- %{?1}}/man/man1/jnativescan.1 \\
  --slave %{_mandir}/man1/jps.1%{man_comp} jps.1%{man_comp} %{_jvmdir}/%{sdkdir -- %{?1}}/man/man1/jps.1 \\
  --slave %{_mandir}/man1/jpackage.1%{man_comp} jpackage.1%{man_comp} %{_jvmdir}/%{sdkdir -- %{?1}}/man/man1/jpackage.1 \\
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
%dir %{_jvmdir}/%{sdkdir -- %{?1}}/
%dir %{_jvmdir}/%{sdkdir -- %{?1}}/lib/
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
%if ! %{system_libs}
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/libfreetype.so
%endif
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
%ifarch %{svml_arches}
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/libjsvml.so
%endif
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/liblcms.so
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
%ifarch %{simdsort_arches}
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/libsimdsort.so
%endif
%ifarch %{sleef_arches}
%{_jvmdir}/%{sdkdir -- %{?1}}/lib/libsleef.so
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
%attr(444, root, root) %{_jvmdir}/%{sdkdir -- %{?1}}/lib/%{vm_variant}/classes_coh.jsa
%ifnarch %{ix86} %{arm32}
%attr(444, root, root) %{_jvmdir}/%{sdkdir -- %{?1}}/lib/%{vm_variant}/classes_nocoops.jsa
%attr(444, root, root) %{_jvmdir}/%{sdkdir -- %{?1}}/lib/%{vm_variant}/classes_nocoops_coh.jsa
%endif
%endif
%dir %{etcjavasubdir}
%dir %{etcjavadir -- %{?1}}
%dir %{etcjavadir -- %{?1}}/lib
%dir %{etcjavadir -- %{?1}}/lib/security
%{etcjavadir -- %{?1}}/lib/security/cacerts
%{etcjavadir -- %{?1}}/lib/security/cacerts.upstream
%dir %{etcjavadir -- %{?1}}/conf
%dir %{etcjavadir -- %{?1}}/conf/management
%dir %{etcjavadir -- %{?1}}/conf/security
%dir %{etcjavadir -- %{?1}}/conf/security/policy
%dir %{etcjavadir -- %{?1}}/conf/security/policy/limited
%dir %{etcjavadir -- %{?1}}/conf/security/policy/unlimited
%config(noreplace) %{etcjavadir -- %{?1}}/lib/security/blocked.certs
%config(noreplace) %{etcjavadir -- %{?1}}/lib/security/public_suffix_list.dat
%config(noreplace) %{etcjavadir -- %{?1}}/conf/security/policy/limited/exempt_local.policy
%config(noreplace) %{etcjavadir -- %{?1}}/conf/security/policy/limited/default_local.policy
%config(noreplace) %{etcjavadir -- %{?1}}/conf/security/policy/limited/default_US_export.policy
%config(noreplace) %{etcjavadir -- %{?1}}/conf/security/policy/unlimited/default_local.policy
%config(noreplace) %{etcjavadir -- %{?1}}/conf/security/policy/unlimited/default_US_export.policy
 %{etcjavadir -- %{?1}}/conf/security/policy/README.txt
%config(noreplace) %{etcjavadir -- %{?1}}/conf/security/java.security
%config(noreplace) %{etcjavadir -- %{?1}}/conf/security/java.security.upstream
%dir %{etcjavadir -- %{?1}}/conf/security/redhat
%dir %{etcjavadir -- %{?1}}/conf/security/redhat/false
%dir %{etcjavadir -- %{?1}}/conf/security/redhat/true
# config-noreplace in case the system administrator wants to adjust
# the FIPS configuration
%config(noreplace) %{etcjavadir -- %{?1}}/conf/security/redhat/SunPKCS11-FIPS.cfg
# config-noreplace in case the system administrator wants to change
# the default for crypto-policies usage
%config(noreplace) %{etcjavadir -- %{?1}}/conf/security/redhat/crypto-policies.properties
# The system administrator is never expected to change these files -- they
# are implementation details -- so leave them as not config-noreplace
%config %{etcjavadir -- %{?1}}/conf/security/redhat/false/crypto-policies.properties
%config %{etcjavadir -- %{?1}}/conf/security/redhat/true/crypto-policies.properties
%config %{etcjavadir -- %{?1}}/conf/security/redhat/false/fips.properties
%config %{etcjavadir -- %{?1}}/conf/security/redhat/true/fips.properties
%config(noreplace) %{etcjavadir -- %{?1}}/conf/management/jmxremote.access
# This is a config template, thus not config-noreplace
%config  %{etcjavadir -- %{?1}}/conf/management/jmxremote.password.template
%config(noreplace) %{etcjavadir -- %{?1}}/conf/management/management.properties
%config(noreplace) %{etcjavadir -- %{?1}}/conf/jaxp.properties
%config(noreplace) %{etcjavadir -- %{?1}}/conf/jaxp-strict.properties.template
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
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/jnativescan
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/jps
%{_jvmdir}/%{sdkdir -- %{?1}}/bin/jpackage
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
%{_jvmdir}/%{sdkdir -- %{?1}}/man/man1/jnativescan.1
%{_jvmdir}/%{sdkdir -- %{?1}}/man/man1/jps.1
%{_jvmdir}/%{sdkdir -- %{?1}}/man/man1/jpackage.1
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

%define files_crypto_adapter() %{expand:
%dir %{_libdir}/%{sdkdir -- %{?1}}
%{_libdir}/%{sdkdir -- %{?1}}/libnssadapter.so
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
# for libnssadapter.so
Requires: %{name}-crypto-adapter%{?1}%{?_isa} = %{epoch}:%{version}-%{release}

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

Name:    java-latest-%{origin}
Version: %{newjavaver}.%{buildver}
# This package needs `.0` as prefix of Release so as to not conflict on install with
# java-X-openjdk. I.e. when latest rolling release is also an LTS release packaged as
# java-X-openjdk. See: https://bugzilla.redhat.com/show_bug.cgi?id=1647298
Release: %{?eaprefix}0.%{rpmrelease}%{?extraver}%{?dist}
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

# FIPS support sources.
# For libnssadapter.so (RHEL-128413)
Source31: https://github.com/rh-openjdk/nss-native-fips-key-import-export-adapter/releases/download/%{nssadapter_version}/%{nssadapter_name}.tar.xz
# Create OpenJDK's crypto-policies hierarchy (RHEL-128409)
Source32: create-redhat-properties-files.bash


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
# 2025a required as of JDK-8347965
BuildRequires: tzdata-java >= 2025a
# Earlier versions have a bug in tree vectorization on PPC
BuildRequires: gcc >= 4.8.3-8

%if %{with_systemtap}
BuildRequires: systemtap-sdt-devel
%endif
BuildRequires: make

# libnssadapter.so build requirements
BuildRequires: nss-devel
BuildRequires: nss-softokn-devel

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
Provides: bundled(libpng) = 1.6.51
# Version in src/java.base/share/native/libzip/zlib/zlib.h
Provides: bundled(zlib) = 1.3.1
%endif
%ifarch %{sleef_arches}
# SLEEF is always bundled
# Version in src/jdk.incubator.vector/linux/native/libsleef/generated/sleefinline_advsimd.h
Provides: bundled(sleef) = 3.6.1
%endif

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

# crypto-adapter
%if %{include_normal_build}
%package crypto-adapter
Summary: %{origin_nice} %{featurever} Cryptography Adapter Library
%if (0%{?rhel} > 0 && 0%{?rhel} <= 8) || (0%{?fedora} >= 0 && 0%{?fedora} < 30)
Group:   Development/Languages
%endif

# crypto-adapter does not need an "rpo" function since
# its specific nss and nss-softokn library requirements are
# automatically generated by RPM.

%description crypto-adapter
The %{origin_nice} %{featurever} cryptography adapter library.
%endif

%if %{include_debug_build}
%package crypto-adapter-slowdebug
Summary: %{origin_nice} %{featurever} Cryptography Adapter Library %{debug_on}
%if (0%{?rhel} > 0 && 0%{?rhel} <= 8) || (0%{?fedora} >= 0 && 0%{?fedora} < 30)
Group:   Development/Languages
%endif

%description crypto-adapter-slowdebug
The %{origin_nice} %{featurever} cryptography adapter library.
%{debug_warning}
%endif

%if %{include_fastdebug_build}
%package crypto-adapter-fastdebug
Summary: %{origin_nice} %{featurever} Cryptography Adapter Library %{fastdebug_on}
%if (0%{?rhel} > 0 && 0%{?rhel} <= 8) || (0%{?fedora} >= 0 && 0%{?fedora} < 30)
Group:   Development/Languages
%endif

%description crypto-adapter-fastdebug
The %{origin_nice} %{featurever} cryptography adapter library.
%{fastdebug_warning}
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

export XZ_OPT="-T0"
# do not add -a 0; will break build dirs
%setup -q -c -n %{uniquesuffix ""} -T
# Prepare libnssadapter.so source code
tar -xJf %{SOURCE31}
# https://bugzilla.redhat.com/show_bug.cgi?id=1189084
prioritylength=`expr length %{priority}`
if [ $prioritylength -ne 8 ] ; then
 echo "priority must be 8 digits in total, violated"
 exit 14
fi

tar -xf %{portablejvmdir}/%{portable_compatiblename}*%{version}*portable.sources.noarch.tar.xz
tar -xf %{portablejvmdir}/%{portable_compatiblename}*%{version}*portable*.misc.%{_arch}.tar.xz
tar -xf %{portablejvmdir}/%{portable_compatiblename}*%{version}*portable*.docs.%{_arch}.tar.xz

%if %{include_normal_build}
tar -xf %{portablejvmdir}/%{portable_compatiblename}*%{version}*portable.jdk.%{_arch}.tar.xz
tar -xf %{portablejvmdir}/%{portable_compatiblename}*%{version}*portable.jmods.%{_arch}.tar.xz
# Extract debuginfo as well
tar -xf %{portablejvmdir}/%{portable_compatiblename}*%{version}*portable.debuginfo.jdk.%{_arch}.tar.xz
%if %{include_staticlibs}
tar -xf %{portablejvmdir}/%{portable_compatiblename}*%{version}*portable.static-libs.%{_arch}.tar.xz
%endif
%endif
%if %{include_fastdebug_build}
tar -xf %{portablejvmdir}/%{portable_compatiblename}*%{version}*portable.fastdebug.jdk.%{_arch}.tar.xz
tar -xf %{portablejvmdir}/%{portable_compatiblename}*%{version}*portable.fastdebug.jmods.%{_arch}.tar.xz
%if %{include_staticlibs}
tar -xf %{portablejvmdir}/%{portable_compatiblename}*%{version}*portable.fastdebug.static-libs.%{_arch}.tar.xz
%endif
%endif
%if %{include_debug_build}
tar -xf %{portablejvmdir}/%{portable_compatiblename}*%{version}*portable.slowdebug.jdk.%{_arch}.tar.xz
tar -xf %{portablejvmdir}/%{portable_compatiblename}*%{version}*portable.slowdebug.jmods.%{_arch}.tar.xz
%if %{include_staticlibs}
tar -xf %{portablejvmdir}/%{portable_compatiblename}*%{version}*portable.slowdebug.static-libs.%{_arch}.tar.xz
%endif
%endif

# print out info abot binaries used for repack. The version-less fallbacks are for development only, where can be cheated environment
echo "Those RPMs are just repacking portable tarballs extracted from portable RPMs" > %{repack_file}
echo "Usually this exact portable RPM can not be obtained via dnf install, but you can download it." >> %{repack_file}
echo "The exact info is at bottom." >> %{repack_file}
echo "All java- names and versions:" >> %{repack_file}
ls -l %{portablejvmdir} >> %{repack_file}
rpm -qa | grep "java-" >> %{repack_file}
echo "Used %{portable_compatiblename}.*portable:" >> %{repack_file}
ls -l %{portablejvmdir} | grep "%{portable_compatiblename}.*portable" >> %{repack_file} || echo "Not found!" >> %{repack_file}
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
src_image=`ls -d %{portable_compatiblename}*%{version}*portable.sources.noarch`
misc_image=`ls -d %{portable_compatiblename}*%{version}*portable.misc.%{_arch}`
cp -rf $misc_image/%{generated_sources_name}/%{vcstag}/ $src_image # it would be nice to remove them once debugsources are generated:(
ln -s $src_image/%{vcstag} %{vcstag}
mkdir build
pushd build
  cp -r ../$misc_image/%{generated_sources_name}/jdk%{featurever}.build* .
popd
doc_image=`ls -d %{portable_compatiblename}*%{version}*portable.docs.%{_arch}`

# it is used differently on fedora
for suffix in %{build_loop} ; do
  mkdir %{installoutputdir -- ${suffix}}
  if [ "x$suffix" = "x" ] ; then
      make -C %{nssadapter_name} CFLAGS="%{build_cflags}" LDFLAGS="%{build_ldflags}"
  elif [ "x$suffix" = "x%{fastdebug_suffix_unquoted}" ] ; then
      make -C %{nssadapter_name} CFLAGS="%{build_cflags}" LDFLAGS="%{build_ldflags}"
  else # slowdebug
      # Disable _FORTIFY_SOURCE to allow for no optimization
      # -Wno-error<=error: -D_FORTIFY_SOURCE defined but value is too low [-Werror]
      make -C %{nssadapter_name} CFLAGS="%{build_cflags} -O0 -Wp,-U_FORTIFY_SOURCE -Wno-error" LDFLAGS="%{build_ldflags}"
  fi

  installdir=%{installoutputdir -- ${suffix}}

  # Install and clean libnssadapter.so
  mkdir ${installdir}/lib
  install -m 755 %{nssadapter_name}/bin/libnssadapter.so ${installdir}/lib
  make -C %{nssadapter_name} clean

# build cycles of nss adapter
done # end of release / debug cycle loop


%install
function customisejdkProperties() {
    local imagepath=${1}
    local suffix=${2}
    if [ -d ${imagepath} ] ; then
        # Install crypto-policies FIPS configuration files and append
        # include line to java.security
        bash -ex %{SOURCE32} ${imagepath}/conf/security %{_libdir}/%{sdkdir -- ${suffix}}/libnssadapter.so
    fi
}

function customisejdkTzdata() {
    local imagepath=${1}
    local suffix=${2}
    if [ -d ${imagepath} ] ; then
        # Use system-wide tzdata
        mv ${imagepath}/lib/tzdb.dat{,.upstream}
        ln -s %{javazidir}/tzdb.dat ${imagepath}/lib/tzdb.dat
    fi
}

function installjdk() {
    local imagepath=${1}
    local suffix=${2}

    if [ -d ${imagepath} ] ; then
        # the build (erroneously) removes read permissions from some jars
        # this is a regression in OpenJDK 7 (our compiler):
        # http://icedtea.classpath.org/bugzilla/show_bug.cgi?id=1437
        find ${imagepath} -iname '*.jar' -exec chmod ugo+r {} \;

        # Build screws up permissions on binaries
        # https://bugs.openjdk.java.net/browse/JDK-8173610
        find ${imagepath} -iname '*.so' -exec chmod +x {} \;
        find ${imagepath}/bin/ -exec chmod +x {} \;

        customisejdkTzdata ${imagepath} ${suffix}
        # Final setup on the main image
        customisejdkProperties ${imagepath} ${suffix}

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
    buildoutputdir=`ls -d %{portable_compatiblename}*portable${debugbuild}.${jdkjre}*`
    top_dir_abs_main_build_path=$(pwd)/${buildoutputdir}
    installjdk  ${top_dir_abs_main_build_path} ${suffix}
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
  buildoutputdir=`ls -d %{portable_compatiblename}*portable${debugbuild}.jdk*`
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
    ln -sf %{_jvmdir}/%{sdkdir -- $suffix}/tapset/$name $RPM_BUILD_ROOT%{tapsetdir}/$targetName
  done
%endif

popd

  install -d -m 755 $RPM_BUILD_ROOT%{_libdir}/%{sdkdir -- ${suffix}}
# RPM 4.20 (F41+) uses rpm-controlled per-package build directories
%if 0%{?fedora} || 0%{?rhel} >= 11
  mv $RPM_BUILD_ROOT/../%{name}/%{installoutputdir -- $suffix}/lib/libnssadapter.so          $RPM_BUILD_ROOT%{_libdir}/%{sdkdir -- ${suffix}}
%else
  mv $RPM_BUILD_ROOT/../../BUILD/%{name}/%{installoutputdir -- $suffix}/lib/libnssadapter.so $RPM_BUILD_ROOT%{_libdir}/%{sdkdir -- ${suffix}}
%endif

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
# TODO: provide desktop files via portable
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
  ln -s %{etcjavadir -- $suffix}/conf  ./conf
popd
pushd $RPM_BUILD_ROOT/%{_jvmdir}/%{sdkdir -- $suffix}/lib
  ln -s %{etcjavadir -- $suffix}/lib/security  ./security
popd
# end moving files to /etc

#TODO this is done also in portables and in install jdk. But hard to say where the operation will hapen at the end
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
 if [ "x$suffix" = "x" ] ; then
      debugbuild=""
  else
      # change -something to .something
      debugbuild=`echo $suffix  | sed "s/-/./g"`
  fi
  buildoutputdir=`ls -d %{portable_compatiblename}*portable${debugbuild}.jdk*`
  top_dir_abs_main_build_path=$(pwd)/${buildoutputdir}
export JAVA_HOME_INTERNAL=${top_dir_abs_main_build_path}  # have in-tree setup before move of configs to /etc
export JAVA_HOME=${RPM_BUILD_ROOT}%{_jvmdir}/%{sdkdir -- $suffix} # have systems setup with links to /etc


#check Shenandoah is enabled
%if %{use_shenandoah_hotspot}
$JAVA_HOME/bin/java -XX:+UseShenandoahGC -version
%endif

# Check unlimited policy has been used
$JAVA_HOME/bin/javac -d . %{SOURCE13}
$JAVA_HOME_INTERNAL/bin/java --add-opens java.base/javax.crypto=ALL-UNNAMED TestCryptoLevel 

# Check ECC is working
$JAVA_HOME/bin/javac -d . %{SOURCE14}
$JAVA_HOME_INTERNAL/bin/java $(echo $(basename %{SOURCE14})|sed "s|\.java||")

# Check system crypto (policy) is active and can be disabled
# Test takes a single argument - true or false - to state whether system
# security properties are enabled or not.
$JAVA_HOME/bin/javac -d . %{SOURCE15}
export PROG=$(echo $(basename %{SOURCE15})|sed "s|\.java||")
export SEC_DEBUG="-Djava.security.debug=properties"
$JAVA_HOME_INTERNAL/bin/java ${SEC_DEBUG} ${PROG} true
$JAVA_HOME_INTERNAL/bin/java ${SEC_DEBUG} -Dredhat.crypto-policies=false ${PROG} false

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
%files crypto-adapter
%{files_crypto_adapter %{nil}}

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
%files crypto-adapter-slowdebug
%{files_crypto_adapter -- %{debug_suffix_unquoted}}

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
%files crypto-adapter-fastdebug
%{files_crypto_adapter --  %{fastdebug_suffix_unquoted}}

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
* Mon Apr 06 2026 azldev <> - 1:26.0.0.0.32-4
- Latest state for java-latest-openjdk

* Thu Feb 12 2026 Jiri Vanek <jvanek@redhat.com> - 1:26.0.0.0.32-3
- Keeping also original version of java.security

* Sun Feb 08 2026 Yaakov Selkowitz <yselkowi@redhat.com> - 1:26.0.0.0.32-2
- Fix javazidir regression

* Tue Jan 27 2026 Jiri Vanek <jvanek@redhat.com> - 1:26.0.0.0.32-1
- Updated to jdk26+32

* Tue Jan 27 2026 Jiri Vanek <jvanek@redhat.com> - 1:26.0.0.0.29-4
- Revert "Rebuilt for
  https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild"

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1:26.0.0.0.29-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Wed Dec 24 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 1:26.0.0.0.29-2
- Fix ELN build

* Wed Dec 24 2025 Jiri Vanek <jvanek@redhat.com> - 1:26.0.0.0.29-1
- Annual christmas update to jdk26

* Fri Dec 19 2025 Jiri Vanek <jvanek@redhat.com> - 1:25.0.1.0.8-4
- Make different path for built libnssadapter.so on el x fedora

* Fri Dec 19 2025 Jiri Vanek <jvanek@redhat.com> - 1:25.0.1.0.8-3
- Release bump

* Fri Dec 19 2025 Jiri Vanek <jvanek@redhat.com> - 1:25.0.1.0.8-2
- Migrated to universal fipsver df044414ef4

* Thu Oct 23 2025 Jiri Vanek <jvanek@redhat.com> - 1:25.0.1.0.8-1
- Updated to October 2025 cpu

* Tue Sep 30 2025 Jiri Vanek <jvanek@redhat.com> - 1:25.0.0.0.36-4
- Bumped release

* Fri Sep 26 2025 Jiri Vanek <jvanek@redhat.com> - 1:25.0.0.0.36-3
- Renamed the top level directoy to java-latest-openjdk

* Fri Sep 26 2025 Jiri Vanek <jvanek@redhat.com> - 1:25.0.0.0.36-2
- Fixed bug with duplicated javadoc

* Tue Sep 23 2025 Jiri Vanek <jvanek@redhat.com> - 1:25.0.0.0.36-1
- Moved to jdk 25 ga

* Wed Jul 30 2025 Jiri Vanek <jvanek@redhat.com> - 1:24.0.2.0.12-6
- Revert "Rebuilt for
  https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild"

* Wed Jul 30 2025 Jiri Vanek <jvanek@redhat.com> - 1:24.0.2.0.12-5
- bumped release

* Wed Jul 30 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 1:24.0.2.0.12-4
- Fix flatpak build of debuginfo

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:24.0.2.0.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jul 23 2025 Jiri Vanek <jvanek@redhat.com> - 1:24.0.2.0.12-2
- riscv64 has libsleef.so

* Tue Jul 22 2025 Jiri Vanek <jvanek@redhat.com> - 1:24.0.2.0.12-1
- July 2025  CPU

* Wed Jun 04 2025 Jiri Vanek <jvanek@redhat.com> - 1:24.0.1.0.9-13
- Bumped release

* Wed Jun 04 2025 Severin Gehwolf <sgehwolf@redhat.com> - 1:24.0.1.0.9-12
- Work around debuginfo package issue on RPM < 4.20

* Tue May 13 2025 Severin Gehwolf <sgehwolf@redhat.com> - 1:24.0.1.0.9-11
- Disable jar processor of add-determinism

* Mon May 12 2025 Severin Gehwolf <sgehwolf@redhat.com> - 1:24.0.1.0.9-10
- Use the separate JMODs tarball throughout

* Mon Apr 28 2025 Severin Gehwolf <sgehwolf@redhat.com> - 1:24.0.1.0.9-9
- Don't perform debugedit on binaries and libraries

* Mon Apr 28 2025 Severin Gehwolf <sgehwolf@redhat.com> - 1:24.0.1.0.9-8
- Make fastdebug/slowdebug packages build

* Fri Apr 25 2025 Severin Gehwolf <sgehwolf@redhat.com> - 1:24.0.1.0.9-7
- Bump release

* Fri Apr 25 2025 Severin Gehwolf <sgehwolf@redhat.com> - 1:24.0.1.0.9-6
- Clean-up and don't strip fastdebug/slowdebug builds

* Thu Apr 24 2025 Severin Gehwolf <sgehwolf@redhat.com> - 1:24.0.1.0.9-5
- Remove work-around for JDK-8350137

* Thu Apr 24 2025 Severin Gehwolf <sgehwolf@redhat.com> - 1:24.0.1.0.9-4
- First cut at creating the debuginfo package manually

* Thu Apr 24 2025 Severin Gehwolf <sgehwolf@redhat.com> - 1:24.0.1.0.9-3
- Switch to using -devel from portable

* Wed Apr 23 2025 Severin Gehwolf <sgehwolf@redhat.com> - 1:24.0.1.0.9-2
- Revert JEP 493 jlink gymnastics

* Thu Apr 17 2025 Jiri Vanek <jvanek@redhat.com> - 1:24.0.1.0.9-1
- Updated to repack April 2025 CPU

* Tue Apr 15 2025 Jiri Vanek <jvanek@redhat.com> - 1:24.0.0.0.36-7
- In devel posttrans, regenrating all jlink hashsums

* Thu Apr 10 2025 Jiri <jvanek@redhat.com> - 1:24.0.0.0.36-6
- Added unpack of jmods, they are now in separate tarball

* Thu Apr 10 2025 Jiri Vanek <jvanek@redhat.com> - 1:24.0.0.0.36-5
- Bumping release and building against newest portables

* Thu Apr 03 2025 Jiri Vanek <jvanek@redhat.com> - 1:24.0.0.0.36-4
- Regenerating jmods file after repack

* Thu Mar 13 2025 Jiri Vanek <jvanek@redhat.com> - 1:24.0.0.0.36-3
- Moved man pages to JAVA_HOME

* Mon Feb 24 2025 Jiri <jvanek@redhat.com> - 1:24.0.0.0.36-2
- introduced NVRA.specfile in doc

* Tue Feb 18 2025 Jiri Vanek <jvanek@redhat.com> - 1:24.0.0.0.36-1
- Updated to 24+36, GA final candidate

* Wed Feb 12 2025 Jiri <jvanek@redhat.com> - 1:24.0.0.0.34-5
- One more jcmd

* Wed Feb 12 2025 Jiri <jvanek@redhat.com> - 1:24.0.0.0.34-4
- Added forgotten jcmd

* Tue Feb 04 2025 Jiri Vanek <jvanek@redhat.com> - 1:24.0.0.0.34-3
- Added aarch64 specific libsleef.so

* Mon Feb 03 2025 Jiri Vanek <jvanek@redhat.com> - 1:24.0.0.0.34-2
- Temporarily disabled debug_package

* Mon Feb 03 2025 Jiri Vanek <jvanek@redhat.com> - 1:24.0.0.0.34-1
- Updated to jdk-24+34-ea

* Sun Feb 02 2025 Jiri Vanek <jvanek@redhat.com> - 1:23.0.2.0.7-2
- Removed parallel installs support

* Tue Jan 28 2025 Jiri Vanek <jvanek@redhat.com> - 1:23.0.2.0.7-1
- January CPU 2025

* Tue Jan 28 2025 Jiri Vanek <jvanek@redhat.com> - 1:23.0.1.0.11-4
- Revert "Rebuilt for
  https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild"

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:23.0.1.0.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Oct 29 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 1:23.0.1.0.11-2
- Fix flatpak build

* Mon Oct 21 2024 Jiri Vanek <jvanek@redhat.com> - 1:23.0.1.0.11-1
- October CPU repack

* Fri Sep 27 2024 Jiri Vanek <jvanek@redhat.com> - 1:23.0.0.0.37-1
- Bumped to jdk23

* Mon Sep 02 2024 Miroslav Suchý <msuchy@redhat.com> - 1:22.0.2.0.9-2
- convert license to SPDX

* Mon Jul 22 2024 Jiri <jvanek@redhat.com> - 1:22.0.2.0.9-1
- April CPU

* Mon Jul 22 2024 Jiri <jvanek@redhat.com> - 1:22.0.1.0.8-3
- Revert "Rebuilt for
  https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild"

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:22.0.1.0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed May 01 2024 Jiri <jvanek@redhat.com> - 1:22.0.1.0.8-1
- repacking april CPU portables

* Wed May 01 2024 Jiri <jvanek@redhat.com> - 1:22.0.0.0.36-3
- Added repack.info with information about original portables

* Wed Feb 21 2024 Songsong Zhang <u2fsdgvkx1@gmail.com> - 1:22.0.0.0.36-2
- Add riscv64 support

* Sun Feb 18 2024 Jiri <jvanek@redhat.com> - 1:22.0.0.0.36-1
- Update to jdk-22.0.0.0.36

* Mon Jan 29 2024 Jiri <jvanek@redhat.com> - 1:22.0.0.0.32-2
- libsimdsort.so built only on simdsort_arches x86_64

* Mon Jan 29 2024 Jiri <jvanek@redhat.com> - 1:22.0.0.0.32-1
- Update to jdk-22.0.0.0.32-0.2
- removed libsystemconf.so; not present in jdk?
- removed nss.fips.cfg; fisp disabled in portables for now
- disabled java ${SEC_DEBUG} ${PROG} true; fisp disabled in portables for
  now
- added lib/libsimdsort.so
- added server/libjvm.a

* Mon Jan 29 2024 Jiri <jvanek@redhat.com> - 1:21.0.2.0.13-6
- Revert "Rebuilt for
  https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild"

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:21.0.2.0.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Jiri Vanek <jvanek@redhat.com> - 1:21.0.2.0.13-4
- removing incorrect  dsit verzion

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:21.0.2.0.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Jiri <jvanek@redhat.com> - 1:21.0.2.0.13-2
- Fixed year in changelog

* Fri Jan 19 2024 Jiri Vanek <jvanek@redhat.com> - 1:21.0.2.0.13-1
- Update to jdk-21.0.2+13 (GA)

* Mon Dec 18 2023 Jiri <jvanek@redhat.com> - 1:21.0.1.0.12-7
- using generated sources from portables for final debuginfo

* Sat Dec 09 2023 Jiri <jvanek@redhat.com> - 1:21.0.1.0.12-6
- fixed date in changelog

* Fri Dec 08 2023 Jiri Vanek <jvanek@redhat.com> - 1:21.0.1.0.12-5
- fix build paths in ELF files so it looks like we built them

* Thu Dec 07 2023 Jiri Vanek <jvanek@redhat.com> - 1:21.0.1.0.12-4
- proeprly filing debugsources pkg  by addedd symlinks restructuring the
  structure for original build sources

* Thu Dec 07 2023 Jiri Vanek <jvanek@redhat.com> - 1:21.0.1.0.12-3
- added setup and thus enabled debuginfo strip
- note, that debugsources are now empty. Symlink from full sourcess to
  build/jdk21.build or build/vcstag is needed

* Sun Nov 26 2023 Jiri <jvanek@redhat.com> - 1:21.0.1.0.12-2
- Minor cosmetic changes

* Sun Nov 26 2023 Jiri <jvanek@redhat.com> - 1:21.0.1.0.12-1
- updated to OpenJDK 21.0.1 (2023-10-17)

* Sat Sep 30 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 1:21.0.0.0.35-6
- Fix flatpak build

* Fri Sep 29 2023 Jiri Vanek <jvanek@redhat.com> - 1:21.0.0.0.35-5
- Removed no longer used {1} in misc subpkg

* Mon Sep 25 2023 Jiri Vanek <jvanek@redhat.com> - 1:21.0.0.0.35-4
- adapted ssbd alt-java test to run on all arches

* Wed Sep 20 2023 Jiri Vanek <jvanek@redhat.com> - 1:21.0.0.0.35-3
- repacked alt-java from misc subpkg

* Wed Sep 20 2023 Jiri Vanek <jvanek@redhat.com> - 1:21.0.0.0.35-2
- adapted to new path in sources

* Tue Aug 29 2023 Jiri Vanek <jvanek@redhat.com> - 1:21.0.0.0.35-1
- updated jdk 21

* Mon Aug 07 2023 Jiri <jvanek@redhat.com> - 1:20.0.2.0.9-1
- updated to July security update  20.0.2.9 portables

* Tue Aug 01 2023 Petra Alice Mikova <petra.alice.mikova@gmail.com> - 1:20.0.1.0.9-12
- Remove excessive .1 string in release

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:20.0.1.0.9-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon May 15 2023 Jiri <jvanek@redhat.com> - 1:20.0.1.0.9-10
- excluding classes_nocoops.jsa on i686 and arm32

* Thu May 11 2023 Jiri Vanek <jvanek@redhat.com> - 1:20.0.1.0.9-9
- Following JDK-8005165, class data sharing can be enabled on all JIT
  architectures

* Wed May 10 2023 Jiri Vanek <jvanek@redhat.com> - 1:20.0.1.0.9-8
- Enable CDS on power64

* Wed May 10 2023 Jiri Vanek <jvanek@redhat.com> - 1:20.0.1.0.9-7
- Fix packaging of CDS archives

* Fri May 05 2023 Jiri <jvanek@redhat.com> - 1:20.0.1.0.9-6
- lib/libjsvml.so now have fake build id only on svml arches

* Thu May 04 2023 Jiri Vanek <jvanek@redhat.com> - 1:20.0.1.0.9-5
- faking build-id in libjsvml.so

* Sat Apr 29 2023 Jiri <jvanek@redhat.com> - 1:20.0.1.0.9-4
- returned news

* Sat Apr 29 2023 Jiri <jvanek@redhat.com> - 1:20.0.1.0.9-3
- added unzip

* Fri Apr 28 2023 Jiri <jvanek@redhat.com> - 1:20.0.1.0.9-2
- now expecting the exact version in portbale filename

* Fri Apr 28 2023 Jiri <jvanek@redhat.com> - 1:20.0.1.0.9-1
- updated to 20.0.1.0.9 underlying portables

* Thu Apr 20 2023 Jiri Vanek <jvanek@redhat.com> - 1:20.0.0.0.36-10
- enabled system crypto tests

* Thu Apr 20 2023 Jiri Vanek <jvanek@redhat.com> - 1:20.0.0.0.36-9
- Added comment about nss-devel dep

* Thu Apr 20 2023 Jiri Vanek <jvanek@redhat.com> - 1:20.0.0.0.36-8
- Removed trailing spaces

* Thu Apr 20 2023 Jiri Vanek <jvanek@redhat.com> - 1:20.0.0.0.36-7
- Fixed typo

* Thu Apr 20 2023 Jiri Vanek <jvanek@redhat.com> - 1:20.0.0.0.36-6
- Added missing url

* Thu Apr 20 2023 Jiri Vanek <jvanek@redhat.com> - 1:20.0.0.0.36-5
- removed empty line

* Wed Apr 19 2023 Jiri Vanek <jvanek@redhat.com> - 1:20.0.0.0.36-4
- returned libsystemconf.so

* Wed Apr 19 2023 Jiri Vanek <jvanek@redhat.com> - 1:20.0.0.0.36-3
- repacking full sources tarball and using icons from it

* Wed Apr 19 2023 Jiri Vanek <jvanek@redhat.com> - 1:20.0.0.0.36-2
- Now requiring full version.release portables

* Mon Apr 03 2023 Jiri Vanek <jvanek@redhat.com> - 1:20.0.0.0.36-1
- bumed to jdk20
- removed no loger existing libsystemconf.so
- commented out usage if Source15 TestSecurityProperties.java test, as
  honoring of
- - system crypto policies comes from fips aptch which is not yet adapted

* Fri Mar 24 2023 Jiri Vanek <jvanek@redhat.com> - 1:19.0.2.0.7-7
- Using proepr icons from repacked portables

* Tue Jan 31 2023 Jiri <jvanek@redhat.com> - 1:19.0.2.0.7-6
- Added changelog and bumped release for versioned requires

* Tue Jan 31 2023 Jiri <jvanek@redhat.com> - 1:19.0.2.0.7-5
- Repacked portable now requires CPU patched portbales

* Tue Jan 31 2023 Jiri <jvanek@redhat.com> - 1:19.0.2.0.7-4
- Removed unnecessary comments

* Mon Jan 30 2023 Petra Mikova <pmikova@redhat.com> - 1:19.0.2.0.7-3
- Return libfreetype.so to resoluve requires during install

* Fri Jan 27 2023 Jiri <jvanek@redhat.com> - 1:19.0.2.0.7-2
- inital repacking

* Thu Jan 26 2023 Andrew Hughes <gnu.andrew@redhat.com> - 1:19.0.2.0.7-1
- Update to jdk-19.0.2 release

* Thu Jan 26 2023 Andrew Hughes <gnu.andrew@redhat.com> - 1:19.0.1.0.10-8
- Revert "Revert "Rebuilt for
  https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild""

* Fri Jan 20 2023 Jiri <jvanek@redhat.com> - 1:19.0.1.0.10-7
- Revert "Rebuilt for
  https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild"

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:19.0.1.0.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Dec 16 2022 Andrew Hughes <gnu.andrew@redhat.com> - 1:19.0.1.0.10-5
- Update in-tree tzdata & CLDR to 2022g with JDK-8296108, JDK-8296715 &
  JDK-8297804

* Fri Dec 16 2022 Stephan Bergmann <sbergman@redhat.com> - 1:19.0.1.0.10-4
- Fix flatpak builds after <https://src.fedoraproject.org/rpms/java-11-
  openjdk/c/6eee73b250484d6c740ce27eb03f36afe0526775> "Update to
  jdk-11.0.16.1+1" added the TestTranslations.java "test to ensure
  timezones can be translated":  Similar to the previous <https://src.fedor
  aproject.org/rpms/java-11-
  openjdk/c/1ac4052b443719e5c582eff9ce30691e043be01f> "Fix flatpak builds",
  during a flatpak build of java-11-openjdk its .../images/jdk/lib/tzdb.dat
  is a dangling symlink to /app/share/javazi-1.8/tzdb.dat (but which will
  be a working symlink in at least the assembled LibreOffice flatpak).
  That causes execution of TestTranslations.java during the build to fail
  due to a java.io.FileNotFoundException when trying to access that
  tzdb.dat.  The easiest fix appears to be to just not run that specific
  test for a flatpak build.

* Wed Dec 07 2022 Jiri Vanek <jvanek@redhat.com> - 1:19.0.1.0.10-3
- Bumped release to rebuild

* Wed Oct 26 2022 Andrew Hughes <gnu.andrew@redhat.com> - 1:19.0.1.0.10-2
- Update in-tree tzdata to 2022e with JDK-8294357 & JDK-8295173

* Thu Oct 20 2022 Andrew Hughes <gnu.andrew@redhat.com> - 1:19.0.1.0.10-1
- Update to jdk-19.0.1 release

* Mon Oct 03 2022 Andrew Hughes <gnu.andrew@redhat.com> - 1:19.0.0.0.36-4
- The stdc++lib, zlib & freetype options should always be set from the
  global, so they are not altered for staticlibs builds

* Tue Aug 30 2022 Andrew Hughes <gnu.andrew@redhat.com> - 1:19.0.0.0.36-3
- Switch buildjdkver back to being featurever, now java-19-openjdk is
  available in the buildroot

* Mon Aug 29 2022 Andrew John Hughes <gnu_andrew@member.fsf.org> - 1:19.0.0.0.36-2
- Switch to static builds, reducing system dependencies and making build
  more portable

* Mon Aug 29 2022 Andrew Hughes <gnu.andrew@redhat.com> - 1:19.0.0.0.36-1
- Update to RC version of OpenJDK 19

* Fri Jul 22 2022 Andrew Hughes <gnu.andrew@redhat.com> - 1:18.0.2.0.9-1
- Update to jdk-18.0.2 release

* Fri Jul 22 2022 Jiri <jvanek@redhat.com> - 1:18.0.1.1.2-9
- moved to build only on %%%%{java_arches}
- - https://fedoraproject.org/wiki/Changes/Drop_i686_JDKs
- reverted :
- - Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild
  (always mess up release)
- - Try to build on x86 again by creating a husk of a JDK which does not
  depend on itself
- - Exclude x86 from builds as the bootstrap JDK is now completely broken
  and unusable
- - Replaced binaries and .so files with bash-stubs on i686
- added ExclusiveArch:  %%%%{java_arches}
- - this now excludes i686
- - this is safely backport-able to older fedoras, as the macro was
  backported proeprly (with i686 included)
- https://bugzilla.redhat.com/show_bug.cgi?id=2104125

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:18.0.1.1.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jul 19 2022 Andrew Hughes <gnu.andrew@redhat.com> - 1:18.0.1.1.2-7
- Try to build on x86 again by creating a husk of a JDK which does not
  depend on itself

* Sun Jul 17 2022 Andrew Hughes <gnu.andrew@redhat.com> - 1:18.0.1.1.2-6
- Exclude x86 from builds as the bootstrap JDK is now completely broken and
  unusable

* Thu Jul 14 2022 Andrew Hughes <gnu.andrew@redhat.com> - 1:18.0.1.1.2-5
- Explicitly require crypto-policies during build and runtime for system
  security properties

* Wed Jul 13 2022 Jiri <jvanek@redhat.com> - 1:18.0.1.1.2-4
- Replaced binaries and .so files with bash-stubs on i686

* Wed Jul 13 2022 Andrew Hughes <gnu.andrew@redhat.com> - 1:18.0.1.1.2-3
- Make use of the vendor version string to store our version & release
  rather than an upstream release date

* Tue Jul 12 2022 FeRD (Frank Dana) <ferdnyc@gmail.com> - 1:18.0.1.1.2-2
- Add additional javadoc & javadoczip alternatives

* Mon Jul 11 2022 Andrew Hughes <gnu.andrew@redhat.com> - 1:18.0.1.1.2-1
- Update to jdk-18.0.1.1 interim release

* Sat Jul 09 2022 Andrew Hughes <gnu.andrew@redhat.com> - 1:18.0.1.0.10-10
- Include a test in the RPM to check the build has the correct vendor
  information.

* Fri Jul 08 2022 Andrew Hughes <gnu.andrew@redhat.com> - 1:18.0.1.0.10-9
- Fix whitespace in spec file

* Fri Jul 08 2022 Andrew Hughes <gnu.andrew@redhat.com> - 1:18.0.1.0.10-8
- Sequence spec file sections as they are run by rpmbuild (build, install
  then test)

* Fri Jul 08 2022 Andrew Hughes <gnu.andrew@redhat.com> - 1:18.0.1.0.10-7
- Turn on system security properties as part of the build's install section

* Thu Jul 07 2022 Stephan Bergmann <sbergman@redhat.com> - 1:18.0.1.0.10-6
- Fix flatpak builds after 19065a8b01585a1aa5f22e38e99fc0c47c597074
  "Temporarily move x86 to use Zero in order to get a working build":

* Fri Jul 01 2022 Francisco Ferrari Bihurriet <fferrari@redhat.com> - 1:18.0.1.0.10-5
- RH2007331: SecretKey generate/import operations don't add the CKA_SIGN
  attribute in FIPS mode

* Thu Jun 30 2022 Stephan Bergmann <sbergman@redhat.com> - 1:18.0.1.0.10-4
- Fix flatpak builds (catering for their uncompressed manual pages) see
  <https://docs.fedoraproject.org/en-
  US/flatpak/troubleshooting/#_uncompressed_manual_pages> for details

* Fri Jun 24 2022 Andrew John Hughes <gnu_andrew@member.fsf.org> - 1:18.0.1.0.10-3
- Update FIPS support to bring in latest changes

* Wed May 25 2022 Andrew John Hughes <gnu_andrew@member.fsf.org> - 1:18.0.1.0.10-2
- Exclude s390x from the gdb test on RHEL 7 where we see failures with the
  portable build

* Thu Apr 28 2022 Jiri Vanek <jvanek@redhat.com> - 1:18.0.1.0.10-1
- updated to CPU jdk-18.0.1+10 sources

* Wed Apr 27 2022 Jiri Vanek <jvanek@redhat.com> - 1:18.0.1.0.0-1
- updated to CPU jdk-18.0.1 sources

* Sun Apr 10 2022 Andrew John Hughes <gnu_andrew@member.fsf.org> - 1:18.0.0.0.37-8
- Add missing ChangeLog entry for previous commit

* Tue Apr 05 2022 Jiri Vanek <jvanek@redhat.com> - 1:18.0.0.0.37-7
- removed hardcoded /usr/lib/jvm by %%{_jvmdir} to make rpmlint happy

* Mon Mar 28 2022 Andrew John Hughes <gnu_andrew@member.fsf.org> - 1:18.0.0.0.37-6
- Automatically turn off building a fresh HotSpot first, if the bootstrap
  JDK is not the same major version as that being built

* Thu Mar 24 2022 Jiri <jvanek@redhat.com> - 1:18.0.0.0.37-5
- Updated generate_source_tarball.sh to match current sources

* Thu Mar 24 2022 Jiri <jvanek@redhat.com> - 1:18.0.0.0.37-4
- Removed ages unused update_package.sh

* Mon Mar 21 2022 Jiri Vanek <jvanek@redhat.com> - 1:18.0.0.0.37-3
- set build jdk to 18

* Mon Mar 21 2022 Jiri Vanek <jvanek@redhat.com> - 1:18.0.0.0.37-2
- replaced tabs by sets of spaces to make rpmlint happy

* Wed Mar 16 2022 Andrew John Hughes <gnu_andrew@member.fsf.org> - 1:18.0.0.0.37-1
- Update to RC version of OpenJDK 18

* Thu Feb 17 2022 Andrew John Hughes <gnu_andrew@member.fsf.org> - 1:17.0.2.0.8-5
- Reinstate JIT builds on x86_32.

* Tue Feb 08 2022 Severin Gehwolf <sgehwolf@redhat.com> - 1:17.0.2.0.8-4
- Re-enable gdb backtrace check on formerly disabled arches.

* Sat Feb 05 2022 Andrew John Hughes <gnu_andrew@member.fsf.org> - 1:17.0.2.0.8-3
- Temporarily move x86 to use Zero in order to get a working build

* Mon Jan 24 2022 Andrew John Hughes <gnu_andrew@member.fsf.org> - 1:17.0.2.0.8-2
- Introduce stapinstall variable to set SystemTap arch directory correctly
  (e.g. arm64 on aarch64)

* Mon Jan 24 2022 Andrew John Hughes <gnu_andrew@member.fsf.org> - 1:17.0.2.0.8-1
- January 2022 security update to jdk 17.0.2+8

* Mon Jan 24 2022 Andrew John Hughes <gnu_andrew@member.fsf.org> - 1:17.0.1.0.12-17
- Separate crypto policy initialisation from FIPS initialisation, now they
  are no longer interdependent

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:17.0.1.0.12-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jan 19 2022 Andrew John Hughes <gnu_andrew@member.fsf.org> - 1:17.0.1.0.12-15
- Sync gdb test with java-1.8.0-openjdk and improve architecture
  restrictions.

* Thu Jan 13 2022 Andrew John Hughes <gnu_andrew@member.fsf.org> - 1:17.0.1.0.12-14
- Fix FIPS issues in native code and with initialisation of
  java.security.Security

* Mon Dec 13 2021 Jiri Vanek <jvanek@redhat.com> - 1:17.0.1.0.12-13
- Storing and restoring alterntives during update manually

* Mon Dec 13 2021 Jiri Vanek <jvanek@redhat.com> - 1:17.0.1.0.12-12
- family extracted to globals

* Thu Dec 09 2021 Jiri Vanek <jvanek@redhat.com> - 1:17.0.1.0.12-11
- Providing proper provides for javadoc-zip subpk

* Thu Dec 09 2021 Jiri Vanek <jvanek@redhat.com> - 1:17.0.1.0.12-10
- Removing tabs in whitespaced specfile for rpmlint

* Mon Nov 29 2021 Andrew John Hughes <gnu_andrew@member.fsf.org> - 1:17.0.1.0.12-9
- Handle Fedora in distro conditionals that currently only pertain to RHEL.

* Mon Nov 08 2021 Jiri Vanek <jvanek@redhat.com> - 1:17.0.1.0.12-8
- Patch syslookup.c so it actually has some code to be compiled into
  libsyslookup

* Fri Nov 05 2021 Severin Gehwolf <sgehwolf@redhat.com> - 1:17.0.1.0.12-7
- Use 'sql:' prefix in nss.fips.cfg

* Wed Nov 03 2021 Andrew John Hughes <gnu_andrew@member.fsf.org> - 1:17.0.1.0.12-6
- Turn off bootstrapping for slow debug builds, which are particularly slow
  on ppc64le.

* Mon Nov 01 2021 Andrew John Hughes <gnu_andrew@member.fsf.org> - 1:17.0.1.0.12-5
- Sync desktop files with upstream IcedTea release 3.15.0 using new script

* Tue Oct 26 2021 Andrew John Hughes <gnu_andrew@member.fsf.org> - 1:17.0.1.0.12-4
- Restructure the build so a minimal initial build is then used for the
  final build (with docs)

* Tue Oct 26 2021 Andrew John Hughes <gnu_andrew@member.fsf.org> - 1:17.0.1.0.12-3
- Minor cosmetic improvements to make spec more comparable between variants

* Thu Oct 21 2021 Andrew John Hughes <gnu_andrew@member.fsf.org> - 1:17.0.1.0.12-2
- Update tapsets from IcedTea 6.x repository with fix for JDK-8015774
  changes (_heap->_heaps) and @JAVA_SPEC_VER@

* Thu Oct 21 2021 Petra Mikova <pmikova@redhat.com> - 1:17.0.1.0.12-1
- October CPU 2021 update

* Sun Oct 10 2021 Andrew John Hughes <gnu_andrew@member.fsf.org> - 1:17.0.0.0.35-5
- Add FIPS patch to allow plain key import.

* Fri Oct 01 2021 Andrew John Hughes <gnu_andrew@member.fsf.org> - 1:17.0.0.0.35-4
- Add patch to login to the NSS software token when in FIPS mode.

* Mon Sep 27 2021 Andrew John Hughes <gnu_andrew@member.fsf.org> - 1:17.0.0.0.35-3
- Update release notes to document the major changes between OpenJDK 11 &
  17.

* Thu Sep 16 2021 Andrew John Hughes <gnu_andrew@member.fsf.org> - 1:17.0.0.0.35-2
- Add patch to disable non-FIPS crypto in the SUN and SunEC security
  providers.

* Tue Sep 14 2021 Andrew John Hughes <gnu_andrew@member.fsf.org> - 1:17.0.0.0.35-1
- Update to jdk-17+35, also known as jdk-17-ga.

* Wed Sep 08 2021 Andrew John Hughes <gnu_andrew@member.fsf.org> - 1:17.0.0.0.33-4
- Detect FIPS using SECMOD_GetSystemFIPSEnabled in the new libsystemconf
  JDK library.

* Mon Sep 06 2021 Andrew John Hughes <gnu_andrew@member.fsf.org> - 1:17.0.0.0.33-3
- Support the FIPS mode crypto policy (RH1655466)

* Tue Aug 31 2021 Jiri Vanek <jvanek@redhat.com> - 1:17.0.0.0.33-2
- alternatives creation moved to posttrans
- Thus fixing the old reisntall issue:
- https://bugzilla.redhat.com/show_bug.cgi?id=1200302
- https://bugzilla.redhat.com/show_bug.cgi?id=1976053

* Fri Jul 30 2021 Andrew John Hughes <gnu_andrew@member.fsf.org> - 1:17.0.0.0.33-1
- Update to jdk-17+33, including JDWP fix and July 2021 CPU

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:17.0.0.0.26-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 07 2021 Andrew John Hughes <gnu_andrew@member.fsf.org> - 1:17.0.0.0.26-6
- Use the "reverse" build loop (debug first) as the main and only build
  loop to get more diagnostics.

* Mon Jun 28 2021 Petra Mikova <pmikova@redhat.com> - 1:17.0.0.0.26-5
- Fix patch
  rh1648249-add_commented_out_nss_cfg_provider_to_java_security.patch

* Thu Jun 24 2021 Severin Gehwolf <sgehwolf@redhat.com> - 1:17.0.0.0.26-4
- Add PR3695 to allow the system crypto policy to be turned off.
- Adds patch from java-11-openjdk so as to be able to properly toggle the
  system crypto policy
- Fixes test TestSecurityProperties.java which was failing

* Thu Jun 24 2021 Severin Gehwolf <sgehwolf@redhat.com> - 1:17.0.0.0.26-3
- Update buildjdkver to 17

* Mon Jun 21 2021 Petra Mikova <pmikova@redhat.com> - 1:17.0.0.0.26-2
- Fix bogus date in changelog to get rid of the warning

* Fri Jun 18 2021 Petra Mikova <pmikova@redhat.com> - 1:17.0.0.0.26-1
- Update to JDK 17

* Fri May 07 2021 Jiri Vanek <jvanek@redhat.com> - 1:16.0.1.0.9-5
- removed cjc backward comaptiblity, to fix when both rpm 4.16 and 4.17 are
  in transaction

* Fri Apr 30 2021 Jiri <jvanek@redhat.com> - 1:16.0.1.0.9-4
- Disable copy-jdk-configs for Flatpak builds

* Fri Apr 30 2021 Jiri <jvanek@redhat.com> - 1:16.0.1.0.9-3
- Adapted to rpm 4.17 and cjc 4.0

* Mon Apr 26 2021 Petra Mikova <pmikova@redhat.com> - 1:16.0.1.0.9-2
- Add forgotten changelog

* Wed Apr 21 2021 Petra Mikova <pmikova@redhat.com> - 1:16.0.1.0.9-1
- April CPU update

* Thu Mar 11 2021 Severin Gehwolf <sgehwolf@redhat.com> - 1:16.0.0.0.36-4
- Perform static library build on a separate source tree with bundled image
  libraries

* Tue Mar 09 2021 Jiri <jvanek@redhat.com> - 1:16.0.0.0.36-3
- bumped buildjdkver to build by itself - 16

* Tue Mar 09 2021 Jiri <jvanek@redhat.com> - 1:16.0.0.0.36-2
- fixed suggests of wrong pcsc-lite-devel%%{?_isa} to correct pcsc-lite-
  libs%%{?_isa}

* Tue Feb 23 2021 Andrew John Hughes <gnu_andrew@member.fsf.org> - 1:16.0.0.0.36-1
- Update to jdk-16.0.0.0+36

* Fri Feb 19 2021 Andrew John Hughes <gnu_andrew@member.fsf.org> - 1:15.0.2.0.7-3
- Hardcode /usr/sbin/alternatives for Flatpak builds

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:15.0.2.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 22 2021 Andrew John Hughes <gnu_andrew@member.fsf.org> - 1:15.0.2.0.7-1
- Update to jdk-15.0.2.0+7

* Tue Jan 19 2021 Andrew John Hughes <gnu_andrew@member.fsf.org> - 1:15.0.1.9-15
- Use -march=i686 for x86 builds if -fcf-protection is detected (needs
  CMOV)

* Tue Jan 05 2021 Tom Stellard <tstellar@redhat.com> - 1:15.0.1.9-14
- Add BuildRequires: make

* Mon Jan 04 2021 Jiri Vanek <jvanek@redhat.com> - 1:15.0.1.9-13
- Fixed typo in variable

* Tue Dec 22 2020 Jiri <jvanek@redhat.com> - 1:15.0.1.9-12
- fixed missing condition for fastdebug packages being counted as debug
  ones

* Sun Dec 20 2020 Jiri <jvanek@redhat.com> - 1:15.0.1.9-11
- removed lib-style provides for fastdebug_suffix_unquoted

* Sun Dec 20 2020 Jiri <jvanek@redhat.com> - 1:15.0.1.9-10
- Added few missing majorver into descriptions

* Sun Dec 20 2020 Jiri <jvanek@redhat.com> - 1:15.0.1.9-9
- many cosmetic changes taken from more maintained jdk11 - introduced
  debug_arches, bootstrap_arches, systemtap_arches, fastdebug_arches,
  sa_arches, share_arches, shenandoah_arches, zgc_arches instead of various
  hardcoded ifarches - updated systemtap - added requires excludes for
  debug pkgs - removed redundant logic around jsa files - added runtime
  requires of lksctp-tools and libXcomposite%% - added and used Source15
  TestSecurityProperties.java, but is made always positive as jdk15 now
  does not honor system policies - s390x excluded form fastdebug build

* Thu Dec 17 2020 Jiri Vanek <jvanek@redhat.com> - 1:15.0.1.9-8
- Added checks and restrictions around alt-java

* Thu Dec 10 2020 Jiri Vanek <jvanek@redhat.com> - 1:15.0.1.9-7
- Fixed not-including fastdebugbuild in case of --without fastdebug

* Thu Dec 10 2020 Jiri Vanek <jvanek@redhat.com> - 1:15.0.1.9-6
- moved wrongly placed icenses to acompany other ones

* Thu Dec 10 2020 Jiri <jvanek@redhat.com> - 1:15.0.1.9-5
- Redeffined linux -> __linux__ and __x86_64 -> __x86_64__; should be
  backported to jdk11 and jdk8

* Mon Dec 07 2020 Jiri <jvanek@redhat.com> - 1:15.0.1.9-4
- Fixes comment for speculative store bypass patch

* Mon Dec 07 2020 Jiri <jvanek@redhat.com> - 1:15.0.1.9-3
- Replaced alt-java palceholder by real pathced alt-java - added patch600,
  rh1750419-redhat_alt_java.patch, suprassing removed patch - no longer
  copying of java->alt-java as it is created by  patch600

* Mon Nov 23 2020 Jiri <jvanek@redhat.com> - 1:15.0.1.9-2
- Create a copy of java as alt-java with alternatives and man pages
- java-11-openjdk doesn't have a JRE tree, so don't try and copy alt-java
  there...

* Thu Oct 29 2020 Petra Mikova <pmikova@redhat.com> - 1:15.0.1.9-1
- October CPU 2020 update

* Thu Oct 22 2020 Severin Gehwolf <sgehwolf@redhat.com> - 1:15.0.0.36-5
- Fix directory ownership of static-libs sub-package

* Tue Oct 13 2020 Jiri Vanek <jvanek@redhat.com> - 1:15.0.0.36-4
- Build static-libs-image and add resulting files via -static-libs sub-
  package.

* Wed Sep 23 2020 Petra Mikova <pmikova@redhat.com> - 1:15.0.0.36-3
- Add support for fastdebug builds on 64 bit architectures

* Tue Sep 15 2020 Severin Gehwolf <sgehwolf@redhat.com> - 1:15.0.0.36-2
- Update for JDK 15 GA

* Thu Sep 03 2020 Petra Mikova <pmikova@redhat.com> - 1:15.0.0.36-1
- Update to OpenJDK 15
- Update to jdk 15.0.0.36 tag
- Modify
  rh1648249-add_commented_out_nss_cfg_provider_to_java_security.patch
- Update vendor version string to 20.9
- Remove jjs binaries from files after JEP 372: Nashorn removal
- Remove rmic binaries from files after JDK-8225319

* Mon Jul 27 2020 Severin Gehwolf <sgehwolf@redhat.com> - 1:14.0.2.12-2
- Disable LTO for passing debuginfo check

* Wed Jul 22 2020 Petra Mikova <pmikova@redhat.com> - 1:14.0.2.12-1
- July 2020 CPU

* Thu Jul 09 2020 Petra Mikova <pmikova@redhat.com> - 1:14.0.1.7-6
- Fix changes in Provides from system_jdk support.

* Tue May 26 2020 Petra Mikova <pmikova@redhat.com> - 1:14.0.1.7-5
- Update generate_source_tarball script to new icedtea patch

* Wed May 20 2020 Petra Mikova <pmikova@redhat.com> - 1:14.0.1.7-4
- Add patch for jdk8235833 to fix build issues in rawhide

* Thu Apr 23 2020 Jiri <jvanek@redhat.com> - 1:14.0.1.7-3
- Moved vendor_version_string to better place

* Thu Apr 23 2020 Severin Gehwolf <sgehwolf@redhat.com> - 1:14.0.1.7-2
- Fix vendor version string

* Mon Apr 20 2020 Petra Mikova <pmikova@redhat.com> - 1:14.0.1.7-1
- CPU update to OpenJDK 14.0.1+7

* Fri Apr 17 2020 Jiri <jvanek@redhat.com> - 1:14.0.0.36-7
- Fxing build failure caused by "," in  value of vendor property

* Wed Apr 08 2020 Jiri <jvanek@redhat.com> - 1:14.0.0.36-6
- Added --with-vendor  id and url family of switches

* Wed Apr 08 2020 Petra Mikova <pmikova@redhat.com> - 1:14.0.0.36-5
- Uploaded new src tarball

* Tue Mar 31 2020 Petra Mikova <pmikova@redhat.com> - 1:14.0.0.36-4
- Bump buildjdkver to 14

* Fri Mar 27 2020 Petra Mikova <pmikova@redhat.com> - 1:14.0.0.36-3
- Remove s390x workaround

* Tue Mar 24 2020 Petra Mikova <pmikova@redhat.com> - 1:14.0.0.36-2
- Fix devel postinstall script

* Thu Mar 19 2020 Petra Mikova <pmikova@redhat.com> - 1:14.0.0.36-1
- Update to OpenJDK 14 - update to jdk 14+36 ea build - remove JDK-8224851
  patch, as OpenJDK 14 already contains it - removed pack200 and unpack200
  binaries, slaves, manpages and libunpack.so library - added listings for
  jpackage binary, manpages and added slave records to alternatives

* Fri Mar 13 2020 Petra Mikova <pmikova@redhat.com> - 1:13.0.2.8-5
- Fix make 4.3 build issues

* Mon Mar 02 2020 Petra Mikova <pmikova@redhat.com> - 1:13.0.2.8-4
- Fix build issues with GCC10

* Tue Feb 04 2020 Petra Mikova <pmikova@redhat.com> - 1:13.0.2.8-3
- Fix release broken by last rpmdev-specbump

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:13.0.2.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jan 18 2020 Petra Mikova <pmikova@redhat.com> - 1:13.0.2.8-1
- CPU sources update to 13.0.2+8 tag

* Fri Oct 25 2019 Petra Mikova <pmikova@redhat.com> - 1:13.0.1.9-4
- Renamed patches according to the convention

* Fri Oct 25 2019 Petra Mikova <pmikova@redhat.com> - 1:13.0.1.9-3
- Create new section for the patches that will be upstreamed in 13.0.2

* Fri Oct 25 2019 Petra Mikova <pmikova@redhat.com> - 1:13.0.1.9-2
- Add shenandoah patches that did not make it to 13.0.1.9

* Tue Oct 22 2019 Petra Mikova <pmikova@redhat.com> - 1:13.0.1.9-1
- Updated to October 2019 CPU sources

* Mon Oct 21 2019 Petra Mikova <pmikova@redhat.com> - 1:13.0.0.33-8
- Changed rpmrelease to 3, replaced previously missed occurences of PR3681
  with PR3755

* Wed Oct 16 2019 Petra Mikova <pmikova@redhat.com> - 1:13.0.0.33-7
- Synced up patches and generate tarball script

* Wed Oct 16 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:13.0.0.33-6
- Switch to in-tree SunEC code, dropping NSS runtime dependencies and
  patches to link against it.

* Wed Oct 16 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:13.0.0.33-5
- Drop unnecessary build requirement on gtk3-devel, as OpenJDK searches for
  Gtk+ at runtime.

* Wed Oct 16 2019 Andrew Hughes <gnu.andrew@redhat.com> - 1:13.0.0.33-4
- Obsolete javadoc-slowdebug and javadoc-slowdebug-zip packages via javadoc
  and javadoc-zip respectively.

* Wed Oct 16 2019 Severin Gehwolf <sgehwolf@redhat.com> - 1:13.0.0.33-3
- Don't produce unnecessary things for the debug variant

* Mon Sep 30 2019 Severin Gehwolf <sgehwolf@redhat.com> - 1:13.0.0.33-2
- Fix vendor version for JDK 13

* Wed Aug 14 2019 Petra Mikova <pmikova@redhat.com> - 1:13.0.0.33-1
- Updated to 13+33 sources

* Fri Jul 26 2019 Severin Gehwolf <sgehwolf@redhat.com> - 1:13.0.0.28-4
- Fix bootjdkver macro

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:13.0.0.28-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jul 12 2019 Petra Mikova <pmikova@redhat.com> - 1:13.0.0.28-2
- Removed jhsdb manpage for s390x arch

* Thu Jul 11 2019 Petra Mikova <pmikova@redhat.com> - 1:13.0.0.28-1
- Update to 13+28 sources

* Thu Jul 11 2019 Petra Mikova <pmikova@redhat.com> - 1:13.0.0.27-2
- Backported patch related to ea designator from ojdk11

* Tue Jul 09 2019 Petra Mikova <pmikova@redhat.com> - 1:13.0.0.27-1
- Update of the package to OpenJDK 13

* Wed May 22 2019 Petra Mikova <pmikova@redhat.com> - 1:12.0.1.12-2
- Fixed requires/provides for non-system jdk (backport of RHBZ#1702324)

* Thu Apr 18 2019 pmikova <pmikova@redhat.com> - 1:12.0.1.12-1
- Updated sources to the latest CPU

* Fri Apr 05 2019 pmikova <pmikova@redhat.com> - 1:12.0.0.33-5
- Added comments to explain removal of chkconfig

* Thu Apr 04 2019 pmikova <pmikova@redhat.com> - 1:12.0.0.33-4
- Deleted unused patch jdk8210416-rh1632174-
  compile_fdlibm_with_o2_ffp_contract_off_on_gcc_clang_arches.patch

* Thu Apr 04 2019 pmikova <pmikova@redhat.com> - 1:12.0.0.33-3
- Added slave for jfr in devel

* Thu Apr 04 2019 pmikova <pmikova@redhat.com> - 1:12.0.0.33-2
- Added patches that I did not somehow pack to srpm

* Tue Apr 02 2019 pmikova <pmikova@redhat.com> - 1:12.0.0.33-1
- Initial commit
## END: Generated by rpmautospec
