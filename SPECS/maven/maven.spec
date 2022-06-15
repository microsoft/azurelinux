Summary:        Apache Maven
Name:           maven
Version:        3.8.4
Release:        1%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://maven.apache.org/
Source0:        https://archive.apache.org/dist/%{name}/%{name}-3/%{version}/source/apache-%{name}-%{version}-src.tar.gz
# Using pre-compiled binaries because 'maven' requires itself during build-time.
Source1:        https://archive.apache.org/dist/%{name}/%{name}-3/%{version}/binaries/apache-%{name}-%{version}-bin.tar.gz
%global debug_package %{nil}
# Switch "sources_generation" to 1 when running a package build to generate cached sources for regular builds.
%define sources_generation 0
%define m2_cache_tarball_name apache-%{name}-%{version}-m2.tar.gz
%define licenses_tarball_name apache-%{name}-%{version}-licenses.tar.gz
%if ! 0%{?sources_generation}
%define offline_build -o
%endif
%define _prefixmvn %{_var}/opt/apache-%{name}
%define _bindirmvn %{_prefixmvn}/bin
%define _libdirmvn %{_prefixmvn}/lib
BuildRequires:  ant
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  msopenjdk-11
BuildRequires:  wget
Requires:       %{_bindir}/which
Requires:       msopenjdk-11
# In order to re-generate these sources after a version update, switch "sources_generation" to 1
# and make sure network is enabled during the build. The tarballs will be inside the built 'maven-cached-sources' subpackage.
%if ! 0%{?sources_generation}
Source2:        %{m2_cache_tarball_name}
Source3:        %{licenses_tarball_name}
%endif

%description
Maven is a software project management and comprehension tool. Based on the concept of a project object model (POM). Maven can manage a project's build, reporting and documentation from a central piece of information.

%if 0%{?sources_generation}
%package cached-sources
Summary:    	NOT TO BE USED AS REGULAR PACKAGE! REQUIRES NETWORK ACCESS!

%description cached-sources
%{summary}
This is an artificial package to ease generation of cached sources for
the regular builds of "maven" when the "sources_generation" macro is set to 0.

%endif

%prep
# Setup mvn binary
tar xf %{SOURCE1} --no-same-owner
mv ./apache-maven-%{version} %{_var}/opt/
ln -sfvn apache-maven-%{version} %{_var}/opt/apache-maven
ln -sfv %{_var}/opt/apache-maven/bin/mvn %{_bindir}/mvn

%if ! 0%{?sources_generation}
# Setup maven .m2 cache directory
mkdir /root/.m2
pushd /root/.m2
tar xf %{SOURCE2} --no-same-owner
popd
%endif

%setup -q -n apache-%{name}-%{version}
%if ! 0%{?sources_generation}
# Setup licenses. Remove LICENSE.vm script, which downloads all subproject license files, and replace with prepopulated license tarball.
rm -v apache-maven/src/main/appended-resources/META-INF/LICENSE.vm
pushd apache-maven
tar xf %{SOURCE3} --no-same-owner
cp -v ./target/licenses/lib/* %{_var}/opt/apache-maven/lib
popd
%endif

%build
# Changing distribution dir to BUILD directory as install macro clears buildroot prior to creating a fresh directory, thus clearing artifacts copied by maven. We copy them later.
MAVEN_DIST_DIR=%{_builddir}%{_prefixmvn}

export JAVA_HOME="%{_libdir}/jvm/msopenjdk-11"
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(find $JAVA_HOME/lib -name "jli")

sed -i 's/www.opensource/opensource/g' DEPENDENCIES
pwd
echo $LD_LIBRARY_PATH
echo $MAVEN_DIST_DIR
mvn -DdistributionTargetDir=$MAVEN_DIST_DIR -DskipTests clean package %{?offline_build}

%install
mkdir -p %{buildroot}%{_prefixmvn}
mkdir -p %{buildroot}%{_libdirmvn}
mkdir -p %{buildroot}%{_bindirmvn}

%if 0%{?sources_generation}

tar -C /root/.m2 -cpvz -f %{m2_cache_tarball_name} repository
mv %{m2_cache_tarball_name} %{buildroot}%{_prefixmvn}

tar -C apache-maven -cpvz -f %{licenses_tarball_name} target/licenses/lib
mv %{licenses_tarball_name} %{buildroot}%{_prefixmvn}

%endif

mkdir -p %{buildroot}%{_datadir}/java/maven
for jar in %{_builddir}%{_libdirmvn}/*.jar
do
    jarname=$(basename $jar .jar)
    cp %{_builddir}%{_libdirmvn}/${jarname}.jar %{buildroot}%{_libdirmvn}/${jarname}.jar
    ln -sfv %{_libdirmvn}/${jarname}.jar %{buildroot}%{_datadir}/java/maven/${jarname}.jar
done

mkdir -p %{buildroot}/bin
for b in %{_builddir}%{_bindirmvn}/*
do
    binaryname=$(basename $b)
    cp %{_builddir}%{_bindirmvn}/${binaryname} %{buildroot}%{_bindirmvn}/${binaryname}
    ln -sfv %{_bindirmvn}/${binaryname} %{buildroot}/bin/${binaryname}
done

mkdir -p %{buildroot}%{_prefixmvn}/conf
mkdir -p %{buildroot}%{_prefixmvn}/boot

cp -a %{_builddir}%{_prefixmvn}/conf/* %{buildroot}%{_prefixmvn}/conf
cp -a %{_builddir}%{_prefixmvn}/boot/* %{buildroot}%{_prefixmvn}/boot

cp %{_builddir}/apache-maven-%{version}/LICENSE %{buildroot}%{_prefixmvn}/
cp %{_builddir}/apache-maven-%{version}/NOTICE %{buildroot}%{_prefixmvn}/
cp %{_builddir}/apache-maven-%{version}/apache-maven/README.txt %{buildroot}%{_prefixmvn}/

%files
%defattr(-,root,root)
%license LICENSE
%dir %{_libdirmvn}
%dir %{_bindirmvn}
%dir %{_prefixmvn}/conf
%dir %{_prefixmvn}/boot
%dir %{_datadir}/java/maven
%{_libdirmvn}/*
%{_bindirmvn}/*
/bin/*
%{_datadir}/java/maven/*.jar
%{_prefixmvn}/boot/plexus-classworlds*
%{_prefixmvn}/conf/logging/simplelogger.properties
%{_prefixmvn}/conf/settings.xml
%{_prefixmvn}/conf/toolchains.xml
%{_prefixmvn}/LICENSE
%{_prefixmvn}/NOTICE
%{_prefixmvn}/README.txt

%if 0%{?sources_generation}
%files cached-sources
%{_prefixmvn}/%{m2_cache_tarball_name}
%{_prefixmvn}/%{licenses_tarball_name}

%endif

%changelog
* Mon Jun 13 2022 Sumedh Sharma <sumsharma@microsoft.com> - 3.8.4-1
- Adding apache maven as build dependency for cassandra reaper.
- Updated to version 3.8.4.

* Wed May 05 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.8.1-1
- Updated to version 3.8.1 to fix CVE-2021-26291.
- Added an artificial 'cached-sources' subpackage.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 3.5.4-13
- Added %%license line automatically

* Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> - 3.5.4-12
- Renaming apache-ant to ant

* Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> - 3.5.4-11
- Renaming apache-maven to maven

* Wed Apr 29 2020 Nicolas Guibourge <nicolasg@microsoft.com> - 3.5.4-10
- Add path to libjli.so in LD_LIBRARY_PATH and skip test while building

* Thu Apr 23 2020 Andrew Phelps <anphel@microsoft.com> - 3.5.4-9
- Replace downloaded license files with new source tarball.

* Thu Apr 16 2020 Nick Samson <nisamson@microsoft.com> - 3.5.4-8
- Updated Source0, License info to use Fedora guidelines. Signature verified.

* Fri Apr 10 2020 Andrew Phelps <anphel@microsoft.com> - 3.5.4-7
- Support building offline for CDPX.

* Wed Apr 01 2020 Andrew Phelps <anphel@microsoft.com> - 3.5.4-6
- Support building standalone by adding mvn binary. License verified.

* Wed Feb 12 2020 Andrew Phelps <anphel@microsoft.com> - 3.5.4-5
- Remove ExtraBuildRequires

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 3.5.4-4
- Initial CBL-Mariner import from Photon (license: Apache2).

* Mon Nov 05 2018 Alexey Makhalov <amakhalov@vmware.com> - 3.5.4-3
- Removed dependency on JAVA8_VERSION macro

* Mon Oct 29 2018 Alexey Makhalov <amakhalov@vmware.com> - 3.5.4-2
- Use ExtraBuildRequires

* Tue Sep 18 2018 Ankit Jain <ankitja@vmware.com> - 3.5.4-1
- Updated apache-maven to version 3.5.4

* Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> - 3.5.0-5
- Remove BuildArch

* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> - 3.5.0-4
- Requires /usr/bin/which

* Mon Jun 19 2017 Divya Thaluru <dthaluru@vmware.com> - 3.5.0-3
- Removed dependency on ANT_HOME
- Removed apache-maven profile file
- Removed version from directory path

* Thu May 18 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> - 3.5.0-2
- Renamed openjdk to openjdk8

* Mon Apr 24 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> - 3.5.0-1
- Updated apache-maven to version 3.5.0

* Fri Mar 31 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 3.3.9-8
- use java rpm macros to determine versions

* Wed Dec 21 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 3.3.9-7
- Updated JAVA_HOME path to point to latest JDK.

* Thu Oct 27 2016 Alexey Makhalov <amakhalov@vmware.com> - 3.3.9-6
- Fix build issue - unable to fetch opensource.org/.../mit-license.php

* Tue Oct 04 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 3.3.9-5
- Updated JAVA_HOME path to point to latest JDK.

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 3.3.9-4
- GA - Bump release of all rpms

* Fri May 20 2016 Divya Thaluru <dthaluru@vmware.com> - 3.3.9-3
- Updated JAVA_HOME path to point to latest JDK.

* Tue Mar 01 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> - 3.3.9-2
- Updated the apache-ant version to 1.9.6

* Fri Feb 26 2016 Kumar Kaushik <kaushikk@vmware.com> - 3.3.9-2
- Updated JAVA_HOME path to point to latest JDK.

* Thu Jan 21 2016 Xiaolin Li <xiaolinl@vmware.com> - 3.3.9-1
- Updated to version 3.3.9

* Tue Jan 5 2016 Xiaolin Li <xiaolinl@vmware.com> - 3.3.3-4
- Increase build timeout from 600000 to 1200000

* Mon Nov 16 2015 Sharath George <sharathg@vmware.com> - 3.3.3-3
- Change path to /var/opt.

* Wed Sep 16 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> - 3.3.3-2
- Updated dependencies after repackaging openjdk.

* Thu Jul 9 2015     Sarah Choi<sarahc@vmware.com> - 3.3.3-1
- Add a script to set environment variables for MAVEN

* Fri May 22 2015 Sriram Nambakam <snambakam@vmware.com> - 1.9.4
- Initial build.    First version
