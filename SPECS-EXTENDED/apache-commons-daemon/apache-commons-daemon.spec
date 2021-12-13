Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package apache-commons-daemon
#
# Copyright (c) 2020 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


%define short_name commons-daemon
Name:           apache-%{short_name}
Version:        1.2.3
Release:        2%{?dist}
Summary:        Commons Daemon - Controlling of Java Daemons
License:        Apache-2.0
Group:          System/Daemons
URL:            https://commons.apache.org/daemon/
Source0:        https://archive.apache.org/dist/commons/daemon/source/%{short_name}-%{version}-src.tar.gz
Source1:        https://archive.apache.org/dist/commons/daemon/source/%{short_name}-%{version}-src.tar.gz.asc
Source2:        apache-commons-daemon.keyring
Source10:       apache-commons-daemon-build.xml
Patch0:         apache-commons-daemon-JAVA_OS.patch
Patch1:         apache-commons-daemon-riscv64.patch
BuildRequires:  ant
BuildRequires:  autoconf
BuildRequires:  fdupes
BuildRequires:  gcc
BuildRequires:  java-devel >= 1.8
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  libcap-devel
BuildRequires:  make
BuildRequires:  xmlto
BuildRequires:  docbook-dtd-xml
Provides:       jakarta-%{short_name} = %{version}
Obsoletes:      jakarta-%{short_name} < %{version}
Provides:       jakarta-%{short_name}-java = %{version}
Obsoletes:      jakarta-%{short_name}-java < %{version}

%description
The Daemon Component contains a set of Java and native code, including
a set of Java interfaces applications must implement and Unix native
code to control a Java daemon from a Unix operating system.

%package        jsvc
Summary:        Java daemon launcher
Group:          System/Daemons
Provides:       jsvc = %{version}-%{release}
Obsoletes:      jsvc < %{version}
Provides:       jakarta-%{short_name}:%{_sbindir}/jsvc

%description    jsvc
Jsvc is a set of libraries and applications for making Java applications run on
UNIX more easily. It allows the application (e.g. Tomcat) to perform some
privileged operations as root (e.g. bind to a port < 1024), and then switch
identity to a non-privileged user.

%package javadoc
Summary:        Commons Daemon Javadoc
Group:          Documentation/Other
Provides:       jakarta-%{short_name}-javadoc = %{version}
Obsoletes:      jakarta-%{short_name}-javadoc < %{version}
BuildArch:      noarch

%description javadoc
The Javadoc Documentation for Commons Daemon.

%prep
%setup -q -n %{short_name}-%{version}-src
cp %{SOURCE10} build.xml
%patch0 -p1
%patch1 -p1

# remove java binaries from sources
rm -rf src/samples/build/

# remove files for different OS
rm -rf src/samples/*.cmd

# mark example files as non-executable
chmod -R 0644 src/samples/*

%pom_remove_parent .

# build manpage for jsvc
pushd src/native/unix
xmlto man man/jsvc.1.xml

%build
# build native jsvc
pushd src/native/unix
sh support/buildconf.sh

%configure --with-java=%{java_home}
%make_build
popd

# build jar
%{ant}

%install
# native jsvc
install -Dpm 0755 src/native/unix/jsvc %{buildroot}%{_bindir}/jsvc
install -Dpm 0644 src/native/unix/jsvc.1 %{buildroot}%{_mandir}/man1/jsvc.1

# jar
install -Dpm 0644 target/%{short_name}-%{version}.jar %{buildroot}%{_jnidir}/%{short_name}.jar
ln -sf %{_jnidir}/%{short_name}.jar %{buildroot}%{_jnidir}/%{name}.jar

# pom
install -Dpm 0644 pom.xml %{buildroot}%{_mavenpomdir}/%{short_name}.pom
%add_maven_depmap %{short_name}.pom %{short_name}.jar -a "org.apache.commons:%{short_name}"

# javadoc
install -dm 0755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}
%fdupes -s %{buildroot}%{_javadocdir}/%{name}

%files -f .mfiles
%license LICENSE.txt NOTICE.txt
%doc PROPOSAL.html RELEASE-NOTES.txt src/samples
%doc src/docs/*
%{_jnidir}/%{name}.jar

%files jsvc
%license LICENSE.txt NOTICE.txt
%{_bindir}/jsvc
%{_mandir}/man1/jsvc.1*

%files javadoc
%license LICENSE.txt NOTICE.txt
%{_javadocdir}/%{name}

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.2.3-2
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Thu Nov 19 2020 Joe Schmitt <joschmit@microsoft.com> - 1.2.3-1.3
- Add understated build requires on docbook-dtd-xml for offline xmlto conversion.
- Set java location in %%configure.
- Remove openSUSE specific macro %%ext_man.

* Tue Nov 17 2020 Ruying Chen <v-ruyche@microsoft.com> - 1.2.3-1.2
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Tue Oct 27 2020 Pedro Monreal <pmonreal@suse.com>
- Update to 1.2.3
  * Fix: Procrun. Correct multiple issues related to enabling a
    service to interact with the desktop. Provide a better error
    message if this option is used with an invalid user, install
    the service with the option enabled if requested and correctly
    save the setting if it is enabled in the GUI.
  * Fix: jsvc. Update the list of paths searched for libjvm.so to
    include the path used by OpenJDK 11.
  * Add: Procrun. Add additional debug logging for Java start mode.
  * Fix: jsvc. Remove incorrect definition 'supported_os' which
    defined in psupport.m4 file to fix jsvc build error on s390,
    arm, aarch64, mipsel and mips.
  * Add: More debug logging in prunsrv.c and javajni.c.
  * Add: Update arguments.c to support Java 11 --enable-preview.
  * Add: jsvc and Procrun. Add support for Java native memory tracking.
  * Add: Procrun. Add a new command, print, that outputs the command to
    (re-)configure the service with the current settings. This is
    intended to be used to save settings such as before an upgrade.
- Rebase apache-commons-daemon-riscv64.patch
- Remove apache-commons-daemon-s390x.patch fixed upstream
* Tue Jun  9 2020 Fridrich Strba <fstrba@suse.com>
- Generate ant build file and customize it in order to be able to
  build this ring package without cycles. Ring packages cannot be
  built using maven.
- Modified patches:
  * apache-commons-daemon-JAVA_OS.patch
  * apache-commons-daemon-riscv64.patch
  * apache-commons-daemon-s390x.patch
    + Do not patch configure file itself, since we generate it
    during the build
* Fri Jun  5 2020 Pedro Monreal Gonzalez <pmonrealgonzalez@suse.com>
- Update to 1.2.2
  * Release 1.2.2 - 2019-10-04
  - Fix: Procrun. Correct a regression in the fix for DAEMON-401
    that prevented the service from starting unless support for the
    universal C runtime had been installed.
  - Update: Update Commons-Parent to version 49.
  * Release 1.2.1 - 2019-09-09
  - Fix: jsvc. Correct debug log message that reports change in umask.
  - Fix: Procrun. Correct a regression in the previous fix for this
    issue that caused 32-bit services to crash on start-up. Fixes DAEMON-401.
  - Fix: Procrun. Correct a regression in the fix for DAEMON-391
    that caused the GUI to mix-up the WARN and INFO logging levels.
  * Release 1.2.0 - 2019-07-02
  - Fix: Procrun. Only set the global shutdown event if the event is created.
  - Fix: Unable to build with Java 9 using ant; dropped Ant build files.
  - Fix: Procrun. prunsrv stopping with error due to hard-coded timeout.
  - Fix: Update config.guess and config.sub.
  - Fix: Jsvc. Set the sun.java.command system property when starting via jsvc
    so that tools like jconsole show something meaningful for the process name.
  - Fix: Procrun. Correct the level name used in the GUI for WARN so that
    changes made via the GUI are recognised. Order the log levels in the
    drop-down from ERROR to DEBUG.
  - Fix: Procrun. Correct reversed code comments for JRE and JDK locations
    in the registry.
  - Fix: Procrun. Fix a bug that meant a value provided for LibraryPath
    replaced the value of the PATH environment variable rather than prepended to it.
  - Fix: Procrun. Ensure that the java.library.path environment variable is
    correctly configured when running on a JRE that depends on the Universal CRT.
  - Add: Procrun. Log the error code returned if JVM creation fails to aid debugging.
  - Fix: Procrun. Ensure that environment variables set via prunsrv are visible
    to native libraries that depend on the Universal CRT.
  - Fix: Procrun. Remove the code that removed quotes from configured Java and
    Java 9 Options.
  - Add: Procrun. Add an option to configure the service to use the 'Automatic
    (Delayed Start)' startup mode.
  - Add: Procrun. When running in jre mode, if the standard Java registry
    entries for JavaHome and RuntimeLib are not present, attempt to use the
    Procrun JavaHome key to find the runtime library.
  - Add: jsvc. Include the full path to the jsvc executable in the debug log.
  * Release 1.1.0 - 2017-11-15
  - Update: Update the minimum Java requirement from version 5 to 6.
  - Update: Add AArch64 support to src/native/unix/support/apsupport.m4.
  - Fix: Remove calls to explicit garbage collection during daemon start and stop.
  - Fix: Update config.guess and config.sub to add support, amongst others,
    for the 64-bit PowerPC Little-Endian architecture.
  - Update: Update Commons-Parent to version 41.
  - Fix: Update apsupport.m4 add support for 64-bit PowerPC architectures.
  - Fix: Suppress spurious "The data area passed to a system call is too small"
    error message in the log when Procrun fails to stop the service.
  - Fix: Enable jsvc to start when running on Java 9.
  - Fix: Fix a resource leak opening the JVM configuration file.
    _ Fix: Improve the jsvc code that restarts the process if the JVM crashes so
    that if the JVM crashes after a signal has been received to shut down jsvc
    does not attempt to restart the JVM.
  - Fix: Ensure that the child process is started with the correct umask.
  - Fix: Correct conflicting information for the behaviour of Procrun when
    using jvm mode.
  - Fix: Ensure that, when using Procrun in java or exe mode, the service
    process waits for the stop process to complete before starting clean-up
    to avoid a crash in the stop process.
  - Fix: Enable jsvc to find the jvm when running on AIX.
  - Fix: Ensure that Procrun treats JVM crashes as service failures so the
    recovery options will apply.
  - Fix: Ensure that the //MQ command closes the prunmgr process even if
    the configuration dialog is open when the //MQ command is used.
  - Fix: Add support for Java 9 command line arguments to jsvc.
  - Add: Add a restarts options to jsvc to control the number of permitted
    restarts after a system crash.
  - Remove: Remove support for building Procrun for the Itanium platform.
  - Fix: Fix race conditions in PID file handling in jsvc.
- Remove patches:
  * apache-commons-daemon-ppc64.patch
  * apache-commons-daemon-aarch64.patch
- Refresh patches:
  * apache-commons-daemon-riscv64.patch
  * apache-commons-daemon-JAVA_OS.patch
- Update project keyring.
* Mon Mar 25 2019 Fridrich Strba <fstrba@suse.com>
- Remove pom parent, since we don't use it when not building with
  maven
* Thu Jul 12 2018 schwab@suse.de
- apache-commons-daemon-riscv64.patch: add riscv64 to the list of
  supported cpus
- Use %%license for LICENSE.txt
* Tue May 15 2018 fstrba@suse.com
- Build with source and target 8 to prepare for a possible removal
  of 1.6 compatibility
- Run fdupes on documentation
* Thu Sep 14 2017 fstrba@suse.com
- Fix jdk9 build by specifying java source and target 1.6
* Fri May 19 2017 pcervinka@suse.com
- New build dependency: javapackages-local
* Wed Mar 25 2015 tchvatal@suse.com
- Drop gpg verification. We can stick to what osc services do for us
* Tue Mar 24 2015 tchvatal@suse.com
- Drop unused patches:
  * 0001-execve-path-warning.patch
  * config-guess-sub-update.patch
  * jsvc-libcap-relative.patch
* Wed Mar 18 2015 tchvatal@suse.com
- Fix build with new javapackages-tools
* Fri Sep 13 2013 mvyskocil@suse.com
- add javapackages-tools to build requires
* Thu May 16 2013 mvyskocil@suse.com
- update to 1.0.15
  * bugfix release, see RELEASE-NOTES.txt for a list of fixed bugs
- obsoleted patches:
  * 0001-execve-path-warning.patch, already upstream
  * jsvc-libcap-relative.patch, already upstream
  * config-guess-sub-update.patch, already upstream
- don't install pointless filesfor SUSE Linux
- verify package signature on openSUSE 12.3+
- use source urls
* Mon Mar 25 2013 schwab@suse.de
- config-guess-sub-update.patch: update config.guess/sub for aarch64
- apache-commons-daemon-aarch64.patch: add aarch64 to the list of
  supported cpus
* Thu Jul 19 2012 mvyskocil@suse.cz
- fix bnc#771802: jsvc fails to load libcap
* Tue Jul  3 2012 dvaleev@suse.com
- read ppc64 as known platform.
* Fri Jun 15 2012 mvyskocil@suse.cz
- Update to 1.0.10 (bugfix release)
- Rename to apache-commons-daemon
  * put the binary to -jsvc package
  * return jars from -java package to main one
- Obsoleted ppc patch
* Mon Apr  2 2012 dvaleev@suse.com
- fix ppc64 architecture detection
* Tue Sep  6 2011 mvyskocil@suse.cz
- Update to 1.0.7
  * fix bnc#CVE-2011-2729/bnc#715656
  * proper file closing  and other minor fixes
* Wed Jan 19 2011 bitshuffler@opensuse.org
- Updated to 1.0.5.
- Reworked spec.
- Removed obsolete patches.
* Wed Aug 26 2009 mls@suse.de
- make patch0 usage consistent
* Mon Sep 25 2006 skh@suse.de
- don't use icecream
- use source="1.4" and target="1.4" for build with java 1.5
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Mon Jan 16 2006 jsmeix@suse.de
- Current version 1.0.1 from JPackage.org
* Wed Jul 27 2005 jsmeix@suse.de
- Adjustments in the spec file.
* Wed Jul 20 2005 jsmeix@suse.de
- Current version 1.0 from JPackage.org
* Mon Jul 18 2005 jsmeix@suse.de
- Current version 1.0 from JPackage.org
* Thu Sep 16 2004 skh@suse.de
- Fix prerequires of javadoc subpackage
* Thu Sep  2 2004 skh@suse.de
- Initial package created with version 1.0 (JPackage 1.5)
