%{!?python2_sitelib: %global python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %global python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

# Switch "sources_generation" to 1 when running a package build to generate cached sources for regular builds.
%define sources_generation 0
%define m2_cache_tarball_name %{name}-%{version}-m2.tar.gz

%if ! 0%{?sources_generation}
%define offline_build -o
%endif

%if ! %{with_check}
%define skip_tests -DskipTests
%endif

Summary:        Google's data interchange format
Name:           protobuf
Version:        3.15.0
Release:        1%{?dist}
License:        BSD
Group:          Development/Libraries
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://developers.google.com/protocol-buffers/
#Source0:       https://github.com/protocolbuffers/protobuf/archive/v%%{version}/%%{name}-%%{version}-all.tar.gz
Source0:        protobuf-%{version}.tar.gz
# In order to re-generate this source after a version update, switch "sources_generation" to 1
# and make sure network is enabled during the build. The tarballs will be inside the built 'maven-cached-sources' subpackage.
%if ! 0%{?sources_generation}
Source1:        %{m2_cache_tarball_name}
%endif

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  libstdc++
BuildRequires:  curl
BuildRequires:  make
BuildRequires:  unzip

%description
Protocol Buffers (a.k.a., protobuf) are Google's language-neutral, platform-neutral, extensible mechanism for serializing structured data. You can find protobuf's documentation on the Google Developers site.

%if 0%{?sources_generation}

%package cached-sources
Summary:    NOT TO BE USED AS REGULAR PACKAGE! REQUIRES NETWORK ACCESS!

%description cached-sources
%{summary}
This is an artificial package to ease generation of cached sources for
the regular builds when the "sources_generation" macro is set to 0.

%endif

%package        devel
Summary:        Development files for protobuf
Group:          Development/Libraries
Requires:       protobuf = %{version}-%{release}

%description    devel
The protobuf-devel package contains libraries and header files for
developing applications that use protobuf.

%package        static
Summary:        protobuf static lib
Group:          Development/Libraries
Requires:       protobuf = %{version}-%{release}

%description    static
The protobuf-static package contains static protobuf libraries.

%package        python
Summary:        protobuf python lib
Group:          Development/Libraries
BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
Requires:       python2
Requires:       python2-libs
Requires:       protobuf = %{version}-%{release}

%description    python
This contains protobuf python libraries.

%package        python3
Summary:        protobuf python3 lib
Group:          Development/Libraries
BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-libs
Requires:       protobuf = %{version}-%{release}

%description    python3
This contains protobuf python3 libraries.

%package        java
Summary:        protobuf java
Group:          Development/Libraries
BuildRequires:  chkconfig
BuildRequires:  openjre8 >= 1.8.0.45
BuildRequires:  openjdk8 >= 1.8.0.45
BuildRequires:  maven >= 3.3.3
Requires:       openjre8 >= 1.8.0.45

%description    java
This contains protobuf java package.

%prep

%if ! 0%{?sources_generation}

# Setup maven .m2 cache directory
mkdir /root/.m2
pushd /root/.m2
tar xf %{SOURCE1} --no-same-owner
popd

%endif

%setup
autoreconf -iv

%build
%configure --disable-silent-rules
export JAVA_HOME=$(find /usr/lib/jvm -name "OpenJDK*")
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(find $JAVA_HOME/lib -name "jli")
make %{?_smp_mflags}

pushd python
python2 setup.py build
python3 setup.py build
popd

pushd java
mvn package %{?offline_build} %{?skip_tests}
popd

%install
export JAVA_HOME=$(find /usr/lib/jvm -name "OpenJDK*")
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(find $JAVA_HOME/lib -name "jli")
make DESTDIR=%{buildroot} install
pushd python
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
popd
pushd java
mvn install %{?offline_build} %{?skip_tests}
install -vdm755 %{buildroot}%{_libdir}/java/protobuf
install -vm644 core/target/protobuf-java-%{version}.jar %{buildroot}%{_libdir}/java/protobuf
install -vm644 util/target/protobuf-java-util-%{version}.jar %{buildroot}%{_libdir}/java/protobuf
popd

%if 0%{?sources_generation}

echo "Compressing cached repositories."
tar --sort=name \
    --mtime="2021-04-26 00:00Z" \
    --owner=0 --group=0 --numeric-owner \
    --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
    -C /root/.m2 \
    -cpvz -f %{m2_cache_tarball_name} repository
mv %{m2_cache_tarball_name} %{buildroot}%{_prefix}

%endif

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license LICENSE
%{_bindir}/protoc
%{_libdir}/libprotobuf-lite.so.*
%{_libdir}/libprotobuf.so.*
%{_libdir}/libprotoc.so.*

%if 0%{?sources_generation}

%files cached-sources
%{_prefix}/%{m2_cache_tarball_name}

%endif

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_libdir}/libprotobuf-lite.la
%{_libdir}/libprotobuf-lite.so
%{_libdir}/libprotobuf.la
%{_libdir}/libprotobuf.so
%{_libdir}/libprotoc.la
%{_libdir}/libprotoc.so

%files static
%defattr(-,root,root)
%{_libdir}/libprotobuf-lite.a
%{_libdir}/libprotobuf.a
%{_libdir}/libprotoc.a

%files python
%{python2_sitelib}/*

%files python3
%{python3_sitelib}/*

%files java
%{_libdir}/java/protobuf/*.jar

%changelog
* Thu Sep 01 2022 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.15.0-1
- Upgrade to 3.15.0

* Mon Jun 21 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.14.0-1
- Updating to version 3.14.0 to satisfy requirements from 'grpc' and 'collectd'.
- Adding steps for re-building Maven cache.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 3.6.1-8
- Added %%license line automatically

*   Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> 3.6.1-7
-   Renaming apache-maven to maven
*   Wed Apr 29 2020 Nicolas Guibourge <nicolasg@microsoft.com> 3.6.1-6
-   Add add JAVA_HOME and path to libjli.so in LD_LIBRARY_PATH
*   Mon Apr 13 2020 Jon Slobodzian <joslobo@microsoft.com> 3.6.1-5
-   Verified license. Removed sha1. Fixed Source0 URL. Updated URL.
*   Thu Apr 09 2020 Andrew Phelps <anphel@microsoft.com> 3.6.1-4
-   Support building offline.
*   Thu Feb 27 2020 Andrew Phelps <anphel@microsoft.com> 3.6.1-3
-   Removed "--build=unknown-unknown-linux" configure flag
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 3.6.1-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Tue Sep 18 2018 Tapas Kundu <tkundu@vmware.com> 3.6.1-1
-   Update to version 3.6.1
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 3.2.0-6
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.2.0-5
-   Use python2 explicitly while building
*   Thu May 18 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.2.0-4
-   Renamed openjdk to openjdk8
*   Fri Apr 28 2017 Siju Maliakkal <smaliakkal@vmware.com> 3.2.0-3
-   Update python3 version
*   Thu Apr 13 2017 Vinay Kulkarni <kulkarniv@vmware.com> 3.2.0-2
-   Build protobuf-java.
*   Fri Mar 31 2017 Rongrong Qiu <rqiu@vmware.com> 3.2.0-1
-   Upgrade to 3.2.0
*   Tue Mar 28 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.6.1-3
-   Build protobuf-python.
*   Mon Mar 20 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.6.1-2
-   Build static lib.
*   Fri Mar 03 2017 Xiaolin Li <xiaolinl@vmware.com> 2.6.1-1
-   Initial packaging for Photon
