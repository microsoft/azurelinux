#need to disable debuginfo till we bring in x11 deps
%define debug_package %{nil}

Summary:        Java Native Access
Name:           jna
Version:        4.5.2
Release:        9%{?dist}
License:        LGPLv2.1+ or ASL 2.0
URL:            https://github.com/java-native-access/jna
Group:          Applications/System
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://github.com/java-native-access/jna/archive/%{version}/%{name}-%{version}.tar.gz

Patch0:         jna_remove_clover_jar.patch
Patch1:         remove_werror.patch
BuildRequires: openjre8
BuildRequires: openjdk8
BuildRequires: ant
BuildRequires: libffi
BuildRequires: libffi-devel
Requires:      openjre8

%define _prefix /var/opt/%{name}-%{version}

%description
The JNA package contains libraries for interop from Java to native libraries.

%package devel
Summary:    Sources for JNA
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
Sources for JNA

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%clean
rm -rf %{buildroot}

%build
export JAVA_HOME=$(find /usr/lib/jvm -name "OpenJDK*")
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(find $JAVA_HOME/lib -name "jli")

# Intermittent issue happens:
#
# BUILD FAILED
# /usr/src/mariner/BUILD/jna-4.4.0/build.xml:717: API for native code has changed, or javah output is inconsistent.
# Re-run this build after checking /usr/src/mariner/BUILD/jna-4.4.0/build/native-linux-x86-64/jni.checksum or updating jni.version and jni.md5 in build.xml
#
# Rerun the build will pass it
ant -Dcflags_extra.native=-DNO_JAWT -Dtests.exclude-patterns="**/*.java" -Drelease=true -Ddynlink.native=true || \
ant -Dcflags_extra.native=-DNO_JAWT -Dtests.exclude-patterns="**/*.java" -Drelease=true -Ddynlink.native=true

%install
export JAVA_HOME=$(find /usr/lib/jvm -name "OpenJDK*")
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(find $JAVA_HOME/lib -name "jli")
export JNA_DIST_DIR=%{buildroot}%{_prefix}

mkdir -p -m 700 $JNA_DIST_DIR

ant -Ddist=$JNA_DIST_DIR dist -Drelease=true

%check
#ignore a unicode name test which fails in chroot checks
sed -i 's/testLoadLibraryWithUnicodeName/ignore_testLoadLibraryWithUnicodeName/' test/com/sun/jna/LibraryLoadTest.java
ant

%files
%defattr(-,root,root)
%license LICENSE
%dir %{_prefix}
%{_prefix}/*.jar
%exclude %{_prefix}/*javadoc.jar
%exclude %{_prefix}/*sources.jar

%exclude %{_prefix}/jnacontrib/*

%files devel
%defattr(-,root,root)
%{_prefix}/src-full.zip
%{_prefix}/src.zip
%{_prefix}/doc.zip
%{_prefix}/*javadoc.jar
%{_prefix}/*sources.jar
%{_prefix}/*.aar

%changelog
*   Sun May 31 2020 Henry Beberman <henry.beberman@microsoft.com> - 4.5.2-9
-   Fix libffi static link in configure
*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 4.5.2-8
-   Added %%license line automatically
*   Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> 4.5.2-7
-   Renaming apache-ant to ant
*   Fri Apr 24 2020 Nicolas Guibourge <nicolasg@microsoft.com> 4.5.2-6
-   Add path to libjli.so in LD_LIBRARY_PATH
*   Wed  Mar 25 2020 Henry Beberman <henry.beberman@microsoft.com> 4.5.2-5
-   Fix gcc9 build break with remove_werror.patch.  License fixed.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 4.5.2-4
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Mon Nov 05 2018 Alexey Makhalov <amakhalov@vmware.com> 4.5.2-3
-   Removed dependency on JAVA8_VERSION macro
*   Thu Oct 25 2018 Ankit Jain <ankitja@vmware.com> 4.5.2-2
-   Removed clover.jar from jna-devel source-full.zip file
*   Mon Sep 10 2018 Ankit Jain <ankitja@vmware.com> 4.5.2-1
-   Updated to version 4.5.2
*   Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 4.4.0-9
-   Remove BuildArch
*   Thu Sep 14 2017 Dheeraj Shetty <dheerajs@vmware.com> 4.4.0-8
-   Makecheck for jna
*   Tue Sep 05 2017 Alexey Makhalov <amakhalov@vmware.com> 4.4.0-7
-   Rerun the build on failure
*   Thu Aug 17 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.4.0-6
-   Removed clover.jar from jna-devel source-full.zip file
*   Mon Jun 19 2017 Divya Thaluru <dthaluru@vmware.com> 4.4.0-5
-   Removed dependency on ANT_HOME
*   Thu May 18 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.4.0-4
-   Renamed openjdk to openjdk8
*   Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.4.0-3
-   disable debuginfo temporarily - wait for x11 deps
*   Tue Apr 04 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.4.0-2
-   use java rpm macros to determine versions
*   Mon Apr 03 2017 Divya Thaluru <dthaluru@vmware.com> 4.4.0-1
-   Updated package to version 4.4.0
*   Wed Dec 21 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.2.1-6
-   Updated JAVA_HOME path to point to latest JDK.
*   Tue Oct 04 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.2.1-5
-   Updated JAVA_HOME path to point to latest JDK.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.2.1-4
-   GA - Bump release of all rpms
*   Fri May 20 2016 Divya Thaluru<dthaluru@vmware.com> 4.2.1-3
-   Updated JAVA_HOME path to point to latest JDK.
*   Thu Mar 03 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.1-2
-   Updated the apache-ant version to 1.9.6
*   Fri Feb 26 2016 Kumar Kaushik <kaushikk@vmware.com> 4.2.1-1
-   Updating version
*   Mon Nov 16 2015 Sharath George <sharathg@vmware.com> 4.1.0-3
-   Changing path to /var/optttt.
*   Fri Sep 18 2015 Divya Thaluru <dthaluru@vmware.com> 4.1.0-2
-   Disabling tests
*   Wed Sep 16 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.1.0-1
-   Updated dependencies after repackaging openjdk.
*   Fri May 29 2015 Sriram Nambakam <snambakam@vmware.com> 4.1.0-0
-   Initial commit
