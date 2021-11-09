%define _use_internal_dependency_generator 0
%global security_hardening none
%define _jdk_update 292
%define _jdk_build 10
%define _repo_ver aarch64-shenandoah-jdk8u%{_jdk_update}-b%{_jdk_build}
%define _url_src https://github.com/AdoptOpenJDK/openjdk-aarch64-jdk8u/
%define bootstrapjdk %{_libdir}/jvm/OpenJDK-1.8.0.181-bootstrap
Summary:        OpenJDK
Name:           openjdk8
Version:        1.8.0.292
Release:        2%{?dist}
License:        ASL 1.1 AND ASL 2.0 AND BSD AND BSD WITH advertising AND GPL+ AND GPLv2 AND GPLv2 WITH exceptions AND IJG AND LGPLv2+ AND MIT AND MPLv2.0 AND Public Domain AND W3C AND zlib
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Tools
URL:            https://hg.openjdk.java.net/aarch64-port/jdk8u-shenandoah/
Source0:        %{_url_src}/archive/%{_repo_ver}.tar.gz
Patch0:         Awt_build_headless_only.patch
Patch1:         check-system-ca-certs-292.patch
BuildRequires:  fontconfig-devel
BuildRequires:  freetype-devel
BuildRequires:  glib-devel
BuildRequires:  pcre-devel
BuildRequires:  unzip
BuildRequires:  which
BuildRequires:  zip
BuildRequires:  zlib-devel
Requires:       chkconfig
Requires:       openjre8 = %{version}-%{release}
AutoReqProv:    no
Obsoletes:      openjdk <= %{version}
Provides:       java-devel = %{version}-%{release}
Provides:       java-1.8.0-openjdk = %{version}-%{release}
Provides:       java-1.8.0-openjdk-headless = %{version}-%{release}
Provides:       java-1.8.0-openjdk-devel = %{version}-%{release}
ExclusiveArch:  aarch64

%description
The OpenJDK package installs java class library and javac java compiler.

%package	-n openjre8
Summary:        Java runtime environment
Requires:       chkconfig
Requires:       libstdc++
AutoReqProv:    no
Obsoletes:      openjre <= %{version}
Provides:       java = %{version}-%{release}
Provides:       java-headless = %{version}-%{release}

%description	-n openjre8
It contains the libraries files for Java runtime environment

%package	sample
Summary:        Sample java applications.
Group:          Development/Languages/Java
Requires:       %{name} = %{version}-%{release}
Obsoletes:      openjdk-sample <= %{version}

%description	sample
It contains the Sample java applications.

%package		doc
Summary:        Documentation and demo applications for openjdk
Group:          Development/Languages/Java
Requires:       %{name} = %{version}-%{release}
Obsoletes:      openjdk-doc <= %{version}

%description	doc
It contains the documentation and demo applications for openjdk

%package 		src
Summary:        OpenJDK Java classes for developers
Group:          Development/Languages/Java
Requires:       %{name} = %{version}-%{release}
Obsoletes:      openjdk-src <= %{version}

%description	src
This package provides the runtime library class sources.

%prep -p exit
%setup -n openjdk-aarch64-jdk8u-%{_repo_ver}
%patch0 -p1
%patch1 -p1
rm jdk/src/solaris/native/sun/awt/CUPSfuncs.c
sed -i "s#\"ft2build.h\"#<ft2build.h>#g" jdk/src/share/native/sun/font/freetypeScaler.c
sed -i '0,/BUILD_LIBMLIB_SRC/s/BUILD_LIBMLIB_SRC/BUILD_HEADLESS_ONLY := 1\nOPENJDK_TARGET_OS := linux\n&/' jdk/make/lib/Awt2dLibraries.gmk

%build
export CFLAGS="%{build_cflags} -Wno-error=register -Wno-error=format-overflow= -Wno-error=stringop-overflow="
export CXXFLAGS="%{build_cxxflags} -Wno-error=register -Wno-error=format-overflow= -Wno-error=stringop-overflow="
export CFLAGS=$(echo $CFLAGS | sed "s/-Wall//" | sed "s/-Wformat//" | sed "s/-Werror=format-security//")
export CXXFLAGS=$(echo $CXXFLAGS | sed "s/-Wall//" | sed "s/-Wformat// | sed "s/-Werror=format-security//"")
unset JAVA_HOME &&
sh configure \
	CUPS_NOT_NEEDED=yes \
	--with-target-bits=64 \
	--with-boot-jdk=%{bootstrapjdk} \
	--disable-headful \
	--with-cacerts-file=%{bootstrapjdk}/jre/lib/security/cacerts \
	--with-extra-cxxflags="-Wno-error -std=gnu++98 -fno-delete-null-pointer-checks -fno-lifetime-dse" \
	--with-extra-cflags="-std=gnu++98 -fno-delete-null-pointer-checks -Wno-error -fno-lifetime-dse" \
	--with-freetype-include=%{_includedir}/freetype2 \
	--with-freetype-lib=%{_libdir} \
	--with-native-debug-symbols=none \
	--disable-zip-debug-info \
	--with-stdc++lib=dynamic

make \
    DEBUG_BINARIES=true \
    BUILD_HEADLESS_ONLY=1 \
    OPENJDK_TARGET_OS=linux \
    JAVAC_FLAGS=-g \
    STRIP_POLICY=no_strip \
    DISABLE_HOTSPOT_OS_VERSION_CHECK=ok \
    CLASSPATH=%{bootstrapjdk}/jre \
    POST_STRIP_CMD="" \
    LOG=trace \
    SCTP_WERROR=

%install
make DESTDIR=%{buildroot} install \
	BUILD_HEADLESS_ONLY=yes \
	OPENJDK_TARGET_OS=linux \
	DISABLE_HOTSPOT_OS_VERSION_CHECK=ok \
	CLASSPATH=%{bootstrapjdk}/jre

install -vdm755 %{buildroot}%{_libdir}/jvm/OpenJDK-%{version}
chown -R root:root %{buildroot}%{_libdir}/jvm/OpenJDK-%{version}
install -vdm755 %{buildroot}%{_bindir}
find %{_prefix}/local/jvm/openjdk-1.8.0-internal/jre/lib/aarch64 -iname \*.diz -delete
mv %{_prefix}/local/jvm/openjdk-1.8.0-internal/* %{buildroot}%{_libdir}/jvm/OpenJDK-%{version}/

%post
alternatives --install %{_bindir}/javac javac %{_libdir}/jvm/OpenJDK-%{version}/bin/javac 2000 \
  --slave %{_bindir}/appletviewer appletviewer %{_libdir}/jvm/OpenJDK-%{version}/bin/appletviewer \
  --slave %{_bindir}/extcheck extcheck %{_libdir}/jvm/OpenJDK-%{version}/bin/extcheck \
  --slave %{_bindir}/idlj idlj %{_libdir}/jvm/OpenJDK-%{version}/bin/idlj \
  --slave %{_bindir}/jar jar %{_libdir}/jvm/OpenJDK-%{version}/bin/jar \
  --slave %{_bindir}/jarsigner jarsigner %{_libdir}/jvm/OpenJDK-%{version}/bin/jarsigner \
  --slave %{_bindir}/javadoc javadoc %{_libdir}/jvm/OpenJDK-%{version}/bin/javadoc \
  --slave %{_bindir}/javah javah %{_libdir}/jvm/OpenJDK-%{version}/bin/javah \
  --slave %{_bindir}/javap javap %{_libdir}/jvm/OpenJDK-%{version}/bin/javap \
  --slave %{_bindir}/jcmd jcmd %{_libdir}/jvm/OpenJDK-%{version}/bin/jcmd \
  --slave %{_bindir}/jconsole jconsole %{_libdir}/jvm/OpenJDK-%{version}/bin/jconsole \
  --slave %{_bindir}/jdb jdb %{_libdir}/jvm/OpenJDK-%{version}/bin/jdb \
  --slave %{_bindir}/jdeps jdeps %{_libdir}/jvm/OpenJDK-%{version}/bin/jdeps \
  --slave %{_bindir}/jhat jhat %{_libdir}/jvm/OpenJDK-%{version}/bin/jhat \
  --slave %{_bindir}/jinfo jinfo %{_libdir}/jvm/OpenJDK-%{version}/bin/jinfo \
  --slave %{_bindir}/jmap jmap %{_libdir}/jvm/OpenJDK-%{version}/bin/jmap \
  --slave %{_bindir}/jps jps %{_libdir}/jvm/OpenJDK-%{version}/bin/jps \
  --slave %{_bindir}/jrunscript jrunscript %{_libdir}/jvm/OpenJDK-%{version}/bin/jrunscript \
  --slave %{_bindir}/jsadebugd jsadebugd %{_libdir}/jvm/OpenJDK-%{version}/bin/jsadebugd \
  --slave %{_bindir}/jstack jstack %{_libdir}/jvm/OpenJDK-%{version}/bin/jstack \
  --slave %{_bindir}/jstat jstat %{_libdir}/jvm/OpenJDK-%{version}/bin/jstat \
  --slave %{_bindir}/jstatd jstatd %{_libdir}/jvm/OpenJDK-%{version}/bin/jstatd \
  --slave %{_bindir}/native2ascii native2ascii %{_libdir}/jvm/OpenJDK-%{version}/bin/native2ascii \
  --slave %{_bindir}/rmic rmic %{_libdir}/jvm/OpenJDK-%{version}/bin/rmic \
  --slave %{_bindir}/schemagen schemagen %{_libdir}/jvm/OpenJDK-%{version}/bin/schemagen \
  --slave %{_bindir}/serialver serialver %{_libdir}/jvm/OpenJDK-%{version}/bin/serialver \
  --slave %{_bindir}/wsgen wsgen %{_libdir}/jvm/OpenJDK-%{version}/bin/wsgen \
  --slave %{_bindir}/wsimport wsimport %{_libdir}/jvm/OpenJDK-%{version}/bin/wsimport \
  --slave %{_bindir}/xjc xjc %{_libdir}/jvm/OpenJDK-%{version}/bin/xjc
/sbin/ldconfig

%post -n openjre8
alternatives --install %{_bindir}/java java %{_libdir}/jvm/OpenJDK-%{version}/jre/bin/java 2000 \
  --slave %{_libdir}/jvm/jre jre %{_libdir}/jvm/OpenJDK-%{version}/jre \
  --slave %{_bindir}/jjs jjs %{_libdir}/jvm/OpenJDK-%{version}/jre/bin/jjs \
  --slave %{_bindir}/keytool keytool %{_libdir}/jvm/OpenJDK-%{version}/jre/bin/keytool \
  --slave %{_bindir}/orbd orbd %{_libdir}/jvm/OpenJDK-%{version}/jre/bin/orbd \
  --slave %{_bindir}/pack200 pack200 %{_libdir}/jvm/OpenJDK-%{version}/jre/bin/pack200 \
  --slave %{_bindir}/rmid rmid %{_libdir}/jvm/OpenJDK-%{version}/jre/bin/rmid \
  --slave %{_bindir}/rmiregistry rmiregistry %{_libdir}/jvm/OpenJDK-%{version}/jre/bin/rmiregistry \
  --slave %{_bindir}/servertool servertool %{_libdir}/jvm/OpenJDK-%{version}/jre/bin/servertool \
  --slave %{_bindir}/tnameserv tnameserv %{_libdir}/jvm/OpenJDK-%{version}/jre/bin/tnameserv \
  --slave %{_bindir}/unpack200 unpack200 %{_libdir}/jvm/OpenJDK-%{version}/jre/bin/unpack200
/sbin/ldconfig

%postun
alternatives --remove javac %{_libdir}/jvm/OpenJDK-%{version}/bin/javac
/sbin/ldconfig

%postun -n openjre8
alternatives --remove java %{_libdir}/jvm/OpenJDK-%{version}/jre/bin/java
/sbin/ldconfig

%clean
rm -rf %{buildroot}/*



%files
%defattr(-,root,root)
%license LICENSE
%{_libdir}/jvm/OpenJDK-%{version}/ASSEMBLY_EXCEPTION
%{_libdir}/jvm/OpenJDK-%{version}/LICENSE
%{_libdir}/jvm/OpenJDK-%{version}/release
%{_libdir}/jvm/OpenJDK-%{version}/THIRD_PARTY_README
%{_libdir}/jvm/OpenJDK-%{version}/lib
%{_libdir}/jvm/OpenJDK-%{version}/include/
%{_libdir}/jvm/OpenJDK-%{version}/bin/clhsdb
%{_libdir}/jvm/OpenJDK-%{version}/bin/extcheck
%{_libdir}/jvm/OpenJDK-%{version}/bin/hsdb
%{_libdir}/jvm/OpenJDK-%{version}/bin/idlj
%{_libdir}/jvm/OpenJDK-%{version}/bin/jar
%{_libdir}/jvm/OpenJDK-%{version}/bin/jfr
%{_libdir}/jvm/OpenJDK-%{version}/bin/jarsigner
%{_libdir}/jvm/OpenJDK-%{version}/bin/java-rmi.cgi
%{_libdir}/jvm/OpenJDK-%{version}/bin/javac
%{_libdir}/jvm/OpenJDK-%{version}/bin/javadoc
%{_libdir}/jvm/OpenJDK-%{version}/bin/javah
%{_libdir}/jvm/OpenJDK-%{version}/bin/javap
%{_libdir}/jvm/OpenJDK-%{version}/bin/jcmd
%{_libdir}/jvm/OpenJDK-%{version}/bin/jconsole
%{_libdir}/jvm/OpenJDK-%{version}/bin/jdb
%{_libdir}/jvm/OpenJDK-%{version}/bin/jdeps
%{_libdir}/jvm/OpenJDK-%{version}/bin/jhat
%{_libdir}/jvm/OpenJDK-%{version}/bin/jinfo
%{_libdir}/jvm/OpenJDK-%{version}/bin/jjs
%{_libdir}/jvm/OpenJDK-%{version}/bin/jmap
%{_libdir}/jvm/OpenJDK-%{version}/bin/jps
%{_libdir}/jvm/OpenJDK-%{version}/bin/jrunscript
%{_libdir}/jvm/OpenJDK-%{version}/bin/jsadebugd
%{_libdir}/jvm/OpenJDK-%{version}/bin/jstack
%{_libdir}/jvm/OpenJDK-%{version}/bin/jstat
%{_libdir}/jvm/OpenJDK-%{version}/bin/jstatd
%{_libdir}/jvm/OpenJDK-%{version}/bin/native2ascii
%{_libdir}/jvm/OpenJDK-%{version}/bin/rmic
%{_libdir}/jvm/OpenJDK-%{version}/bin/schemagen
%{_libdir}/jvm/OpenJDK-%{version}/bin/serialver
%{_libdir}/jvm/OpenJDK-%{version}/bin/wsgen
%{_libdir}/jvm/OpenJDK-%{version}/bin/wsimport
%{_libdir}/jvm/OpenJDK-%{version}/bin/xjc
%exclude %{_libdir}/jvm/OpenJDK-%{version}/bin/*.debuginfo

%files -n openjre8
%defattr(-,root,root)
%dir %{_libdir}/jvm/OpenJDK-%{version}
%{_libdir}/jvm/OpenJDK-%{version}/jre/
%{_libdir}/jvm/OpenJDK-%{version}/bin/java
%{_libdir}/jvm/OpenJDK-%{version}/bin/keytool
%{_libdir}/jvm/OpenJDK-%{version}/bin/orbd
%{_libdir}/jvm/OpenJDK-%{version}/bin/pack200
%{_libdir}/jvm/OpenJDK-%{version}/bin/rmid
%{_libdir}/jvm/OpenJDK-%{version}/bin/rmiregistry
%{_libdir}/jvm/OpenJDK-%{version}/bin/servertool
%{_libdir}/jvm/OpenJDK-%{version}/bin/tnameserv
%{_libdir}/jvm/OpenJDK-%{version}/bin/unpack200
%{_libdir}/jvm/OpenJDK-%{version}/lib/aarch64/jli/
%exclude %{_libdir}/jvm/OpenJDK-%{version}/lib/aarch64/*.diz

%files sample
%defattr(-,root,root)
%{_libdir}/jvm/OpenJDK-%{version}/sample/

%files doc
%defattr(-,root,root)
%{_libdir}/jvm/OpenJDK-%{version}/man/
%{_libdir}/jvm/OpenJDK-%{version}/demo

%files src
%defattr(-,root,root)
%{_libdir}/jvm/OpenJDK-%{version}/src.zip

%changelog
* Fri Oct 22 2021 Andrew Phelps <anphel@microsoft.com> - 1.8.0.292-2
- Modify to fix issues with gcc 11.2.0

* Sun Apr 18 2021 Nick Samson <nick.samson@microsoft.com> - 1.8.0.292-1
- Update to 8u292 to address CVEs.
- Switch to Shenandoah version of the aarch64 port

* Fri Feb 05 2021 Joe Schmitt <joschmit@microsoft.com> - 1.8.0.181-13
- Replace incorrect %%{_lib} usage with %%{_libdir}

* Tue Nov 17 2020 Joe Schmitt <joschmit@microsoft.com> - 1.8.0.181-12
- Provide java and java-headless.

* Mon Nov 02 2020 Joe Schmitt <joschmit@microsoft.com> - 1.8.0.181-11
- Provide java-1.8.0-openjdk and java-devel.

*   Thu Oct 15 2020 Joe Schmitt <joschmit@microsoft.com> 1.8.0.181-10
-   Provide java-1.8.0-openjdk-devel.

*   Mon Sep 28 2020 Joe Schmitt <joschmit@microsoft.com> 1.8.0.181-9
-   Remove unused buildrequires.
-   Provide java-1.8.0-openjdk-headless.

*   Thu Jun 11 2020 Henry Beberman <henry.beberman@microsoft.com> 1.8.0.181-8
-   Disable -Werrors that break the build in cflags and cxxflags.

*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 1.8.0.181-7
-   Added %%license line automatically

*   Wed May 06 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 1.8.0.181-6
-   Removing *Requires for "ca-certificates".

*   Mon May 04 2020 Emre Girgin <mrgirgin@microsoft.com> 1.8.0.181-5
-   Replace BuildArch with ExclusiveArch

*   Thu Apr 30 2020 Nicolas Ontiveros <niontive@microsoft.com> 8.0.181-4
-   Rename freetype2-devel to freetype-devel.

*   Thu Apr 16 2020 Paul Monson <paulmon@microsoft.com> 8.0.181-3
-   Remove harfbuzz-devel.  License verified.

*   Wed Feb 12 2020 Andrew Phelps <anphel@microsoft.com> 8.0.181-2
-   Remove ExtraBuildRequires

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 8.0.181-1
-   Initial CBL-Mariner import from Photon (license: Apache2).

*   Thu Mar 21 2019 Ajay Kaher <akaher@vmware.com> 1.8.0.181-1
-   Update to version 1.8.0.181

*   Mon Oct 29 2018 Ajay Kaher <akaher@vmware.com> 1.8.0.151-3
-   Adding BuildArch

*   Mon Oct 29 2018 Alexey Makhalov <amakhalov@vmware.com> 1.8.0.151-2
-   Use ExtraBuildRequires

*   Thu Dec 21 2017 Alexey Makhalov <amakhalov@vmware.com> 1.8.0.151-1
-   Initial version of OpenJDK for aarch64. SPEC file was forked from
    openjdk8-1.8.0.152-1 of x86_64
