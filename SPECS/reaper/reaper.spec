%global debug_package %{nil}

%define srcdir cassandra-%{name}-%{version}

%define bower_components reaper-bower-components-%{version}.tar.gz
%define srcui_node_modules reaper-srcui-node-modules-%{version}.tar.gz
%define bower_cache reaper-bower-cache-%{version}.tar.gz
%define maven_cache reaper-m2-cache-%{version}.tar.gz
%define npm_cache reaper-npm-cache-%{version}.tar.gz
%define local_lib_node_modules reaper-local-lib-node-modules-%{version}.tar.gz
%define local_n reaper-local-n-%{version}.tar.gz

Name:           reaper
Version:        3.1.1
Release:        1%{?dist}
Summary:        Reaper for cassandra is a tool for running Apache Cassandra repairs against single or multi-site clusters.
License:        ASL 2.0
Distribution:   Mariner
Vendor:         Microsoft Corporation
Group:          Applications/System
URL:            https://cassandra-reaper.io/
Source0:        https://github.com/thelastpickle/cassandra-reaper/archive/refs/tags/%{version}.tar.gz#/cassandra-reaper-%{version}.tar.gz

# Building reaper from sources downloads artifacts related to maven/node/etc. These artifacts need to be downloaded as caches in order to build reaper using maven in offline mode.
# Below is the list of cached sources.
# bower-components downloaded under src/ui
# NOTE: USE "reaper_build_caches.sh" TO RE-GENERATE BUILD CACHES.
Source1:        %{bower_components}
# node_modules downloaded under src/ui
Source2:        %{srcui_node_modules}
# bower cache
Source3:        %{bower_cache}
# m2 cache
Source4:        %{maven_cache}
# npm cache
Source5:        %{npm_cache}
# node_modules downloaded to /usr/local/lib
Source6:        %{local_lib_node_modules}
# v14.18.0 node binary under /usr/local
Source7:        %{local_n}

BuildRequires:  git
BuildRequires:  javapackages-tools
BuildRequires:  maven
BuildRequires:  msopenjdk-11
BuildRequires:  nodejs
BuildRequires:  python3
Requires(pre):  %{_sbindir}/groupadd
Requires(pre):  %{_sbindir}/useradd
Provides:       reaper = %{version}-%{release}

%description
Cassandra reaper is an open source tool that aims to schedule and orchestrate repairs of Apache Cassandra clusters.

%prep
%autosetup -n cassandra-%{name}-%{version}

%build
export JAVA_HOME="%{_libdir}/jvm/msopenjdk-11"
export LD_LIBRARY_PATH="%{_libdir}/jvm/msopenjdk-11/lib/jli"

pushd "$HOME"
echo "Installing bower cache."
tar xf %{SOURCE3}

echo "Installing m2 cache."
tar xf %{SOURCE4}

echo "Installing npm cache"
tar xf %{SOURCE5}
popd

# Reaper build fails when trying to install node-sass@4.9.0/node-gyp@3.8.0 and build node native addons using mariner default node@16.14.2/npm@8.5.0.
# ERROR:
# npm ERR! Building: /usr/bin/node /usr/src/mariner/BUILD/cassandra-reaper-3.1.1/src/ui/node_modules/node-gyp/bin/node-gyp.js rebuild --verbose --libsass_ext= --libsass_cflags= --libsass_l dflags= --libsass_library=" - python/python2 not found. node-gyp 3.8.0 does not support python3.
# Howerver, using node@14.18.0/npm@6.14.15 does not cause this issue.
# There is no way to remove node-sass dependency from builds, hence we need to install local node/npm and caches to be able to build reaper.
# NOTE: This issue was also faced on Fedora Fc37 when trying to build reaper.
# NOTE: node-sass seems to be deprecated, the spec and build process will be modified once reaper removes its dependencies as well.
pushd %{_prefix}/local
echo "Installing node_modules"
tar xf %{SOURCE6} -C ./lib/

echo "Installing n version 14.18.0"
tar xf %{SOURCE7}

echo "Creating symlinks under local/bin"
cd ./bin
ln -sf ../lib/node_modules/bower/bin/bower bower
ln -sf ../lib/node_modules/npm/bin/npm-cli.js npm
ln -sf ../lib/node_modules/npm/bin/npx-cli.js npx

cp ../n/versions/node/14.18.0/bin/node .

ls -al
popd

cd %{_builddir}/%{srcdir}
echo "Installing src caches"
pushd ./src/ui
echo "Installing bower_components"
tar xf %{SOURCE1}

echo "Installing npm_modules"
tar fx %{SOURCE2}
popd

# Building using maven in offline mode.
mvn -DskipTests package -o

%install
mkdir -p %{buildroot}%{_datadir}/cassandra-reaper
mkdir -p %{buildroot}%{_prefix}/local/bin
mkdir -p %{buildroot}%{_sysconfdir}/init.d
mkdir -p %{buildroot}%{_sysconfdir}/cassandra-reaper
mkdir -p %{buildroot}%{_sysconfdir}/cassandra-reaper/configs
mkdir -p %{buildroot}%{_sysconfdir}/bash_completion.d
mkdir -p %{buildroot}/lib/systemd/system/
mkdir -p %{buildroot}%{_datadir}/licenses/reaper
cd %{_builddir}/%{srcdir}/src/packaging

cp resource/cassandra-reaper.yaml %{buildroot}%{_sysconfdir}/cassandra-reaper/
cp resource/cassandra-reaper*.yaml %{buildroot}%{_sysconfdir}/cassandra-reaper/configs
cp resource/cassandra-reaper-ssl.properties %{buildroot}%{_sysconfdir}/cassandra-reaper/configs
cp ../server/target/cassandra-reaper-%{version}.jar %{buildroot}%{_datadir}/cassandra-reaper
cp bin/* %{buildroot}%{_prefix}/local/bin/
cp etc/bash_completion.d/spreaper %{buildroot}%{_sysconfdir}/bash_completion.d/
cp debian/reaper.init %{buildroot}%{_sysconfdir}/init.d/cassandra-reaper
cp debian/cassandra-reaper.service %{buildroot}/lib/systemd/system/cassandra-reaper.service
chmod 7555 %{buildroot}%{_sysconfdir}/init.d/cassandra-reaper

cp %{_builddir}/%{srcdir}/LICENSE.txt %{buildroot}%{_datadir}/licenses/reaper

%pre
if id -u reaper; then
  echo "skipping user"
else
  %{_sbindir}/groupadd reaper || true
  %{_sbindir}/useradd -r -g reaper -s /sbin/nologin -d %{_localstatedir}/empty -c 'cassandra-reaper' reaper || true
fi

%post
mkdir -p %{_localstatedir}/log/cassandra-reaper/
touch %{_localstatedir}/log/cassandra-reaper/reaper.log
chown -R reaper: %{_localstatedir}/log/cassandra-reaper/

%files
%license LICENSE.txt
%{_sysconfdir}/cassandra-reaper/cassandra-reaper.yaml
%{_sysconfdir}/cassandra-reaper/configs/cassandra-reaper-astra.yaml
%{_sysconfdir}/cassandra-reaper/configs/cassandra-reaper-cassandra-sidecar.yaml
%{_sysconfdir}/cassandra-reaper/configs/cassandra-reaper-cassandra-ssl.yaml
%{_sysconfdir}/cassandra-reaper/configs/cassandra-reaper-cassandra.yaml
%{_sysconfdir}/cassandra-reaper/configs/cassandra-reaper-memory.yaml
%{_sysconfdir}/cassandra-reaper/configs/cassandra-reaper.yaml
%{_sysconfdir}/cassandra-reaper/configs/cassandra-reaper-ssl.properties
%{_datadir}/cassandra-reaper/cassandra-reaper-%{version}.jar
%{_prefix}/local/bin/cassandra-reaper
%{_prefix}/local/bin/spreaper
%{_sysconfdir}/bash_completion.d/spreaper
%{_sysconfdir}/init.d/cassandra-reaper
/lib/systemd/system/cassandra-reaper.service

%changelog
* Mon Jun 13 2022 Sumedh Sharma <sumsharma@microsoft.com> - 3.1.1-1
- Original version for CBL-Mariner (license: MIT)
- License verified
