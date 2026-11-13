Summary: External DNF5 publication-time snapshot filter
Name: dnf5-plugin-repo-snapshot
Version: 0.1.0
Release: %autorelease
License: MIT
URL: https://github.com/microsoft/dnf5-plugin-repo-snapshot
Source0: %{url}/releases/download/v%{version}/%{name}-%{version}.tar.gz

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
%autosetup

%build
%cmake -DSNAPSHOT_BUILD_PLUGINS=ON -DCMAKE_INSTALL_SYSCONFDIR=%{_sysconfdir}
%cmake_build

%check
%ctest

%install
%cmake_install

%files
%license LICENSE
%doc README.md
%{_libdir}/dnf5/plugins/repo_snapshot_cmd_plugin.so
%{_libdir}/libdnf5/plugins/repo_snapshot.so
%config(noreplace) %{_sysconfdir}/dnf/libdnf5-plugins/repo_snapshot.conf

%changelog
%autochangelog
