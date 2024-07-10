%global debug_package %{nil}

%define local_n_release 1
%define local_srcui_release 1

Summary:        Reaper for cassandra is a tool for running Apache Cassandra repairs against single or multi-site clusters.
Name:           reaper
Version:        3.1.1
Release:        10%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://cassandra-reaper.io/
Source0:        https://github.com/thelastpickle/cassandra-reaper/archive/refs/tags/%{version}.tar.gz#/cassandra-reaper-%{version}.tar.gz
# Building reaper from sources downloads artifacts related to maven/node/etc.
# These artifacts need to be downloaded as caches in order to build reaper using maven in offline mode.
# Below is the list of cached sources.
# bower-components downloaded under src/ui
# NOTE: USE "reaper_build_caches.sh" TO RE-GENERATE BUILD CACHES.
Source1:        reaper-bower-components-%{version}-%{local_srcui_release}.tar.gz
# node_modules downloaded under src/ui
Source2:        reaper-srcui-node-modules-%{version}-%{local_srcui_release}.tar.gz
# m2 cache
Source4:        reaper-m2-cache-%{version}.tar.gz
# node_modules downloaded to /usr/local/lib
Source6:        reaper-local-lib-node-modules-%{version}.tar.gz
# v14.18.0 node binary under /usr/local
Source7:        reaper-local-n-%{version}-%{local_n_release}.tar.gz
# Patches the src/ui/node_modules/ws/lib/websocket-server.js file, which comes
# from the "reaper-srcui-node-modules*" tarball.
# The src/ui/node_modules/ws/package.json file suggest we're on the
# 6.x version of "ws". Patch for this version taken from here:
# https://github.com/websockets/ws/commit/eeb76d313e2a00dd5247ca3597bba7877d064a63
Patch0:         CVE-2024-37890.patch
Patch1:         CVE-2023-42282.patch
Patch2:         CVE-2017-18214.patch
BuildRequires:  git
BuildRequires:  javapackages-tools
BuildRequires:  maven
BuildRequires:  msopenjdk-11
BuildRequires:  nodejs
BuildRequires:  python3
BuildRequires:  rsync
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
%autosetup -N -n cassandra-%{name}-%{version}

echo "Installing bower_components and npm_modules caches."
for source in "%{SOURCE1}" "%{SOURCE2}"; do
    tar -C src/ui -xf "$source"
done

echo "Installing the m2 cache."
tar -C "$HOME" -xf "%{SOURCE4}"

# Reaper build fails when trying to install node-sass@4.9.0/node-gyp@3.8.0 and build node native addons using mariner default node@16.14.2/npm@8.5.0.
# ERROR:
# npm ERR! Building: /usr/bin/node /usr/src/mariner/BUILD/cassandra-reaper-3.1.1/src/ui/node_modules/node-gyp/bin/node-gyp.js rebuild --verbose --libsass_ext= --libsass_cflags= --libsass_l dflags= --libsass_library=" - python/python2 not found. node-gyp 3.8.0 does not support python3.
# Howerver, using node@14.18.0/npm@6.14.15 does not cause this issue.
# There is no way to remove node-sass dependency from builds, hence we need to install local node/npm and caches to be able to build reaper.
# NOTE: This issue was also faced on Fedora Fc37 when trying to build reaper.
# NOTE: node-sass seems to be deprecated, the spec and build process will be modified once reaper removes its dependencies as well.

# Extracting to intermediate folder to apply patch.
tmp_local_dir=tmp_local
mkdir -p $tmp_local_dir/{bin,lib}
pushd $tmp_local_dir
echo "Installing node_modules"
tar -C ./lib/ -xf %{SOURCE6}

echo "Installing n version 14.18.0"
tar -xf %{SOURCE7}

echo "Creating symlinks under local/bin"
ln -sf ../lib/node_modules/bower/bin/bower bin/bower
ln -sf ../lib/node_modules/npm/bin/npm-cli.js bin/npm
ln -sf ../lib/node_modules/npm/bin/npx-cli.js bin/npx

cp n/versions/node/14.18.0/bin/node bin

ls -al
popd

%autopatch -p1

rsync -azvhr $tmp_local_dir/ "%{_prefix}/local"
rm -rf $tmp_local_dir

%build
export JAVA_HOME="%{_libdir}/jvm/msopenjdk-11"
export LD_LIBRARY_PATH="%{_libdir}/jvm/msopenjdk-11/lib/jli"

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

pushd src/packaging

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

popd

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
* Tue Jul 09 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.1.1-10
- Patching CVE-2024-37890, CVE-2023-42282, and CVE-2017-18214.

* Thu May 23 2024 Archana Choudhary <archana1@microsoft.com> - 3.1.1-9
- Repackage and update src/ui node modules and bower components to 3.1.1-1
- Address CVE-2024-4068 by upgrading the version of the npm module "braces" to 3.0.3
- Remove patch for CVE-2023-28155 as request npm module upgraded to 2.88.2
- Remove patch for CVE-2018-11694 as node-sass npm module upgraded to 4.14.1
- Remove patch for CVE-2022-37601 as loader-utils npm module upgraded to 1.4.2
- Remove patch for CVE-2023-26159 as follow-redirects npm module upgraded to 1.15.6

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
