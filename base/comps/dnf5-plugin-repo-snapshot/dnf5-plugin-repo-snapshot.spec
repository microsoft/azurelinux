Summary: External DNF5 publication-time snapshot filter
Name: dnf5-plugin-repo-snapshot
Version: 0.1.0
Release: %autorelease
License: MIT
URL: https://github.com/microsoft/azurelinux
Source0: CMakeLists.txt
Source1: snapshot.cpp
Source2: snapshot.hpp
Source3: cli.cpp
Source4: hook.cpp
Source5: tests.cpp
Source6: LICENSE
Source7: repo_snapshot.conf

BuildRequires: cmake
BuildRequires: gcc-c++
BuildRequires: pkgconfig(libdnf5)
BuildRequires: pkgconfig(libdnf5-cli)
BuildRequires: dnf5-devel
BuildRequires: dnf5(plugin-post-base-setup) = 1
BuildRequires: libdnf5(package-filetime) = 1
Requires: dnf5%{?_isa} >= 5.2.18.0
Requires: dnf5(plugin-post-base-setup)%{?_isa} = 1
Requires: libdnf5%{?_isa} >= 5.2.18.0
Requires: libdnf5(package-filetime)%{?_isa} = 1

%description
An opt-in external DNF5 CLI extension and libdnf5 repository hook which
rejects available RPMs published after a selected timestamp. The plugin
reads the publication timestamp directly from the loaded libdnf5 package sack.

%prep
%setup -q -c -T
cp -p %{SOURCE0} %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5} %{SOURCE6} %{SOURCE7} .

%build
%cmake -DSNAPSHOT_BUILD_PLUGINS=ON -DCMAKE_INSTALL_SYSCONFDIR=%{_sysconfdir}
%cmake_build

%check
%ctest

%install
%cmake_install

%files
%license LICENSE
%{_libdir}/dnf5/plugins/repo_snapshot_cmd_plugin.so
%{_libdir}/libdnf5/plugins/repo_snapshot.so
%config(noreplace) %{_sysconfdir}/dnf/libdnf5-plugins/repo_snapshot.conf

%changelog
%autochangelog
