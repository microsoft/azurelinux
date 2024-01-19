%global debug_package %{nil}

%define local_n_release 1

%define srcdir cassandra-%{name}-%{version}
%define bower_components reaper-bower-components-%{version}.tar.gz
%define srcui_node_modules reaper-srcui-node-modules-%{version}.tar.gz
%define bower_cache reaper-bower-cache-%{version}.tar.gz
%define maven_cache reaper-m2-cache-%{version}.tar.gz
%define npm_cache reaper-npm-cache-%{version}.tar.gz
%define local_lib_node_modules reaper-local-lib-node-modules-%{version}.tar.gz
%define local_n reaper-local-n-%{version}-%{local_n_release}.tar.gz

Summary:        Reaper for cassandra is a tool for running Apache Cassandra repairs against single or multi-site clusters.
Name:           reaper
Version:        3.1.1
Release:        8%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
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
Patch0:         CVE-2022-37601.patch
Patch1:         CVE-2023-28155.patch
Patch2:         CVE-2018-11694.patch
Patch3:         CVE-2023-26159.patch
BuildRequires:  git
BuildRequires:  javapackages-tools
BuildRequires:  maven
BuildRequires:  msopenjdk-11
BuildRequires:  nodejs
BuildRequires:  python3
BuildRequires:  systemd-rpm-macros
BuildRequires:  openssl-devel
Requires:       msopenjdk-11
Requires(pre):  %{_sbindir}/groupadd
Requires(pre):  %{_sbindir}/useradd
Provides:       reaper = %{version}-%{release}
# Building reaper only for x86_64 architecture for now, as build caches are x86_64 specific.
ExclusiveArch:  x86_64

%description
Cassandra reaper is an open source tool that aims to schedule and orchestrate repairs of Apache Cassandra clusters.

%prep
%setup -q -n %{srcdir}

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
patch -p1 --input %{PATCH0}
patch -p1 --input %{PATCH1}
patch -p1 --input %{PATCH2}
patch -p1 --input %{PATCH3}
popd

# Building using maven in offline mode.
mvn -DskipTests package -o

%install
mkdir -p %{buildroot}%{_datadir}/cassandra-%{name}
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_sysconfdir}/init.d
mkdir -p %{buildroot}%{_sysconfdir}/cassandra-%{name}
mkdir -p %{buildroot}%{_sysconfdir}/cassandra-%{name}/configs
mkdir -p %{buildroot}%{_sysconfdir}/bash_completion.d
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_datadir}/licenses/%{name}
cd %{_builddir}/%{srcdir}/src/packaging

cp resource/cassandra-reaper.yaml %{buildroot}%{_sysconfdir}/cassandra-%{name}/
cp resource/cassandra-reaper*.yaml %{buildroot}%{_sysconfdir}/cassandra-%{name}/configs
cp resource/cassandra-reaper-ssl.properties %{buildroot}%{_sysconfdir}/cassandra-%{name}/configs
cp ../server/target/cassandra-reaper-%{version}.jar %{buildroot}%{_datadir}/cassandra-%{name}
cp bin/* %{buildroot}%{_sbindir}
cp etc/bash_completion.d/spreaper %{buildroot}%{_sysconfdir}/bash_completion.d/
cp debian/reaper.init %{buildroot}%{_sysconfdir}/init.d/cassandra-%{name}

# modify service unit ExecStart to point to binary copied under /sbin. This fixes permission errors when
# starting reaper service as custom user.
sed 's/\(^ExecStart\)\(.*$\)/\1=\/sbin\/cassandra-reaper/' < debian/cassandra-%{name}.service > debian/cassandra-%{name}.new.service
cp debian/cassandra-%{name}.new.service %{buildroot}/%{_unitdir}/cassandra-%{name}.service
chmod 0644 %{buildroot}/%{_unitdir}/cassandra-%{name}.service
chmod 7555 %{buildroot}%{_sysconfdir}/init.d/cassandra-%{name}

cp %{_builddir}/%{srcdir}/LICENSE.txt %{buildroot}%{_datadir}/licenses/%{name}

%pre
getent group reaper > /dev/null || groupadd -r reaper
getent passwd reaper > /dev/null || useradd -r -g reaper -s /sbin/nologin -d /var/empty -c 'cassandra reaper user' reaper || :

%post
mkdir -p %{_localstatedir}/log/cassandra-%{name}/
touch %{_localstatedir}/log/cassandra-%{name}/reaper.log
chown -R reaper: %{_localstatedir}/log/cassandra-%{name}/
%systemd_post cassandra-%{name}.service

%preun
%systemd_preun cassandra-%{name}.service

%postun
%systemd_postun_with_restart cassandra-%{name}.service
if [ $1 -eq 0 ] ; then
    /usr/sbin/userdel reaper
fi

%files
%license LICENSE.txt
%{_sysconfdir}/cassandra-%{name}/cassandra-reaper.yaml
%{_sysconfdir}/cassandra-%{name}/configs/cassandra-reaper-astra.yaml
%{_sysconfdir}/cassandra-%{name}/configs/cassandra-reaper-cassandra-sidecar.yaml
%{_sysconfdir}/cassandra-%{name}/configs/cassandra-reaper-cassandra-ssl.yaml
%{_sysconfdir}/cassandra-%{name}/configs/cassandra-reaper-cassandra.yaml
%{_sysconfdir}/cassandra-%{name}/configs/cassandra-reaper-memory.yaml
%{_sysconfdir}/cassandra-%{name}/configs/cassandra-reaper.yaml
%{_sysconfdir}/cassandra-%{name}/configs/cassandra-reaper-ssl.properties
%{_datadir}/cassandra-%{name}/cassandra-reaper-%{version}.jar
%{_sbindir}/cassandra-%{name}
%{_sbindir}/spreaper
%{_sysconfdir}/bash_completion.d/spreaper
%{_sysconfdir}/init.d/cassandra-%{name}
%{_unitdir}/cassandra-%{name}.service

%changelog
* Thu Jan 11 2024 Henry Li <lihl@microsoft.com> - 3.1.1-8
- Apply patch to resolve CVE-2023-26159

* Thu Aug 17 2023 Bala <balakumaran.kannan@microsoft.com> - 3.1.1-7
- Make openssl as BR and remove openssl from local-n bundle to fix CVE-2023-0286

* Fri Aug 04 2023 Sumedh Sharma <sumsharma@microsoft.com> - 3.1.1-6
- Patch CVE-2018-11694 in libsass module

* Thu May 25 2023 Tobias Brick <tobiasb@microsoft.com> - 3.1.1-5
- Patch CVE-2023-28155 for request npm module

* Tue May 23 2023 Bala <balakumaran.kannan@microsoft.com> - 3.1.1-4
- Update CVE-2022-37601.patch to patch two other occurances of the same CVE

* Wed Apr 19 2023 Bala <balakumaran.kannan@microsoft.com> - 3.1.1-3
- Patch CVE-2022-37601 for webpack/loader-utils npm module

* Tue Sep 06 2022 Sumedh Sharma <sumsharma@microsoft.com> - 3.1.1-2
- Adding Runtime requirement on msopenjdk.
- Fix adding cassandra reaper custom user/group
- Fix issues with starting unit service due to permission errors when executing binaries copied
  to /usr/local/bin (by default, subdir bin does not allow any other user/group to access except root)
  Copying reaper binaries to /usr/sbin instead.
- Add post steps during uninstallation to stop service and remove custom user/group.

* Mon Jun 13 2022 Sumedh Sharma <sumsharma@microsoft.com> - 3.1.1-1
- Original version for CBL-Mariner (license: MIT)
- License verified
