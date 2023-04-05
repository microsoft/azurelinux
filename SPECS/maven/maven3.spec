%global homedir %{_datadir}/%{name}
%global debug_package %{nil}
%global pkg_base_name maven
%define m2_cache_tarball_name apache-%{pkg_base_name}-%{version}-m2.tar.gz
%define licenses_tarball_name apache-%{pkg_base_name}-%{version}-licenses.tar.gz
%define offline_build -o
%define _prefixmvn %{_var}/opt/apache-%{pkg_base_name}
%define _bindirmvn %{_prefixmvn}/bin
%define _libdirmvn %{_prefixmvn}/lib
# maven 1.0 package version being used. This needs to be updated in case of updates in 1.0.
%define mvn_1_0_pmc_ver 3.5.4-13
Summary:        Apache Maven alternative package with no jdk bindings
Name:           maven3
Version:        3.8.7
Release:        2%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://maven.apache.org/
Source0:        https://archive.apache.org/dist/%{pkg_base_name}/%{pkg_base_name}-3/%{version}/source/apache-%{pkg_base_name}-%{version}-src.tar.gz
# Since bootstrap has been removed for maven, it requires a pre-built maven binary to build itself.
# Relying on 1.0 maven rpm to provide the mvn binary for the build.
Source1:        %{_mariner_sources_url}/%{pkg_base_name}-%{mvn_1_0_pmc_ver}.cm1.x86_64.rpm
Source2:        %{_mariner_sources_url}/%{pkg_base_name}-%{mvn_1_0_pmc_ver}.cm1.aarch64.rpm
# CBL-Mariner build are without network connection. Hence, we need to generate build caches
# as tarballs to build rpms in offline mode.
# In order to generate tarballs, use "maven_build_caches.sh".
# ./maven_build_caches.sh -v <Maven version string> -a <x86_64 | aarch64>
# ex: ./maven_build_caches.sh -v 3.8.4 -a x86_64
Source3:        %{m2_cache_tarball_name}
Source4:        %{licenses_tarball_name}
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  msopenjdk-11
BuildRequires:  wget
BuildRequires:  which
Requires:       %{_bindir}/which
Conflicts:      maven

%description
Maven is a software project management and comprehension tool. Based on the concept of a project object model (POM). Maven can manage a project's build, reporting and documentation from a central piece of information.

%package openjdk11
Summary:        MSOpenJDK 11 binding for Maven
RemovePathPostfixes: -openjdk11
Requires: %{name} = %{version}-%{release}
Requires: msopenjdk-11
Provides: %{name}-jdk-binding = %{version}-%{release}

%description openjdk11
Configures Maven to run with OpenJDK 11.

%prep
# Installing 1.0 PMC packages to provide prebuilt mvn binary.
echo "Installing mvn 1.0 using rpm with --nodeps."
%ifarch x86_64
rpm -i --nodeps %{SOURCE1}
%else
rpm -i --nodeps %{SOURCE2}
%endif
mvn -v

# Setup maven .m2 cache directory
mkdir /root/.m2
pushd /root/.m2
tar xf %{SOURCE3} --no-same-owner
popd

%setup -q -n apache-%{pkg_base_name}-%{version}
# Setup licenses. Remove LICENSE.vm script, which downloads all subproject license files, and replace with prepopulated license tarball.
rm -v apache-maven/src/main/appended-resources/META-INF/LICENSE.vm
pushd apache-maven
tar xf %{SOURCE4} --no-same-owner
cp -v ./target/licenses/lib/* %{_var}/opt/apache-maven/lib
popd

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


mkdir -p %{buildroot}%{homedir}/bin
ln -sfv %{_bindirmvn}/mvn %{buildroot}%{homedir}/bin/mvn
ln -sfv %{_bindirmvn}/mvnDebug %{buildroot}%{homedir}/bin/mvnDebug
ln -sfv %{_bindirmvn}/mvn.1.gz %{buildroot}%{homedir}/bin/mvn.1.gz
ln -sfv %{_bindirmvn}/mvnDebug.1.gz %{buildroot}%{homedir}/bin/mvnDebug.1.gz

install -d -m 755 %{buildroot}%{_sysconfdir}/java/
echo JAVA_HOME=%{_lib}/jvm/msopenjdk-11 >%{buildroot}%{_sysconfdir}/java/maven.conf-openjdk11

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
%{homedir}/bin/mvn*
/bin/*
%{_datadir}/java/maven/*.jar
%{_prefixmvn}/boot/plexus-classworlds*
%{_prefixmvn}/conf/logging/simplelogger.properties
%{_prefixmvn}/conf/settings.xml
%{_prefixmvn}/conf/toolchains.xml
%{_prefixmvn}/LICENSE
%{_prefixmvn}/NOTICE
%{_prefixmvn}/README.txt

%files openjdk11
%config /etc/java/maven.conf-openjdk11

%changelog
* Tue Apr 04 2023 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 3.8.7-2
- Added openjdk11 subpackage
- Added symlink for binaries requires by xmvn package

* Thu Feb 16 2023 Sumedh Sharma <sumsharma@microsoft.com> - 3.8.7-1
- Original version for CBL-Mariner (license: MIT)
- Remove Runtime dependency on any msopenjdk-* version
- License verified
