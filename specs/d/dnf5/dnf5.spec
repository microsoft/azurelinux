# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# All Azure Linux specs with overlays include this macro file, irrespective of whether new macros have been added.
%{load:%{_sourcedir}/dnf5.azl.macros}

%global project_version_prime 5
%global project_version_major 2
%global project_version_minor 18
%global project_version_micro 0

%bcond dnf5_obsoletes_dnf %[0%{?fedora} > 40 || 0%{?rhel} > 10]

Name:           dnf5
Version:        %{project_version_prime}.%{project_version_major}.%{project_version_minor}.%{project_version_micro}
Release: 2%{?dist}
Summary:        Command-line package manager
License:        GPL-2.0-or-later
URL:            https://github.com/rpm-software-management/dnf5
Source0:        %{url}/archive/%{version}/dnf5-%{version}.tar.gz
Source9999: dnf5.azl.macros

Requires:       libdnf5%{?_isa} = %{version}-%{release}
Requires:       libdnf5-cli%{?_isa} = %{version}-%{release}
%if %{without dnf5_obsoletes_dnf}
Requires:       dnf-data
%endif
Recommends:     (dnf5-plugins if dnf-plugins-core)
Recommends:     bash-completion
Requires:       coreutils
%if 0%{?fedora} > 41
Recommends:     (libdnf5-plugin-expired-pgp-keys if gnupg2)
%endif

%if 0%{?fedora} || 0%{?rhel} > 10
Provides:       microdnf = %{version}-%{release}
Obsoletes:      microdnf < 4
%endif

%if %{with dnf5_obsoletes_dnf}
Provides:       dnf = %{version}-%{release}
Obsoletes:      dnf < 5

Provides:       yum = %{version}-%{release}
Obsoletes:      yum < 5

Conflicts:      python3-dnf-plugins-core < 4.7.0
%endif

Provides:       dnf5-command(advisory)
Provides:       dnf5-command(autoremove)
Provides:       dnf5-command(check)
Provides:       dnf5-command(check-upgrade)
Provides:       dnf5-command(clean)
Provides:       dnf5-command(distro-sync)
Provides:       dnf5-command(downgrade)
Provides:       dnf5-command(download)
Provides:       dnf5-command(environment)
Provides:       dnf5-command(group)
Provides:       dnf5-command(history)
Provides:       dnf5-command(info)
Provides:       dnf5-command(install)
Provides:       dnf5-command(leaves)
Provides:       dnf5-command(list)
Provides:       dnf5-command(makecache)
Provides:       dnf5-command(mark)
Provides:       dnf5-command(module)
Provides:       dnf5-command(offline)
Provides:       dnf5-command(provides)
Provides:       dnf5-command(reinstall)
Provides:       dnf5-command(replay)
Provides:       dnf5-command(remove)
Provides:       dnf5-command(repo)
Provides:       dnf5-command(repoquery)
Provides:       dnf5-command(search)
Provides:       dnf5-command(swap)
Provides:       dnf5-command(system-upgrade)
Provides:       dnf5-command(upgrade)
Provides:       dnf5-command(versionlock)


# ========== build options ==========

%bcond_without dnf5daemon_client
%bcond_without dnf5daemon_server
%bcond_without libdnf_cli
%bcond_without dnf5
%bcond_without dnf5_plugins
%bcond_without plugin_actions
%bcond_without plugin_appstream
%bcond_without plugin_expired_pgp_keys
%bcond_without plugin_rhsm
%bcond_without python_plugins_loader
%bcond_without plugin_local

%bcond_without comps
%bcond_without modulemd
%bcond_without systemd

%bcond_with    html
%if 0%{?rhel} == 8
%bcond_with    man
%else
%bcond_without man
%endif

# TODO Go bindings fail to build, disable for now
%bcond_with    go
%bcond_without perl5
%bcond_without python3
%bcond_without ruby

%bcond_with    clang
%bcond_with    sanitizers
%bcond_without tests
%bcond_with    performance_tests
%bcond_with    dnf5daemon_tests

# Disable SOLVER_FLAG_FOCUS_NEW only for RHEL
%if 0%{?rhel} && 0%{?rhel} < 11
%bcond_with    focus_new
%else
%bcond_without focus_new
%endif

%if %{with clang}
    %global toolchain clang
%endif

# ========== versions of dependencies ==========

%global libmodulemd_version 2.5.0
%global librepo_version 1.20.0
%if %{with focus_new}
    %global libsolv_version 0.7.30
%else
    %global libsolv_version 0.7.25
%endif
%global sqlite_version 3.35.0
%global swig_version 4


# ========== build requires ==========

%if 0%{?fedora} > 40 || 0%{?rhel} > 10
BuildRequires:  bash-completion-devel
%else
BuildRequires:  bash-completion
%endif
BuildRequires:  cmake >= 3.21
BuildRequires:  doxygen
BuildRequires:  gettext
BuildRequires:  pkgconfig(check)
BuildRequires:  pkgconfig(fmt)
BuildRequires:  pkgconfig(json-c)
BuildRequires:  pkgconfig(libcrypto)
BuildRequires:  pkgconfig(librepo) >= %{librepo_version}
BuildRequires:  pkgconfig(libsolv) >= %{libsolv_version}
BuildRequires:  pkgconfig(libsolvext) >= %{libsolv_version}
BuildRequires:  pkgconfig(rpm) >= 4.17.0
BuildRequires:  pkgconfig(sqlite3) >= %{sqlite_version}
BuildRequires:  toml11-static
BuildRequires:  zlib-devel

%if %{with clang}
BuildRequires:  clang
%else
BuildRequires:  gcc-c++ >= 10.1
%endif

%if %{with tests}
BuildRequires:  createrepo_c
BuildRequires:  pkgconfig(cppunit)
BuildRequires:  rpm-build
%endif

%if %{with comps}
BuildRequires:  pkgconfig(libcomps)
%endif

%if %{with modulemd}
BuildRequires:  pkgconfig(modulemd-2.0) >= %{libmodulemd_version}
%endif

%if %{with systemd}
BuildRequires:  pkgconfig(sdbus-c++) >= 0.8.1
BuildRequires:  systemd-devel

 # We need to get the SYSTEMD_SYSTEM_UNIT_DIR from
 # /usr/share/pkgconfig/systemd.pc
BuildRequires:  systemd
%endif

%if %{with html} || %{with man}
BuildRequires:  python3dist(breathe)
BuildRequires:  python3dist(sphinx) >= 4.1.2
BuildRequires:  python3dist(sphinx-rtd-theme)
%endif

%if %{with sanitizers}
# compiler-rt is required by sanitizers in clang
BuildRequires:  compiler-rt
BuildRequires:  libasan
BuildRequires:  liblsan
BuildRequires:  libubsan
%endif

%if %{with libdnf_cli}
# required for libdnf5-cli
BuildRequires:  pkgconfig(smartcols)
%endif

%if %{with dnf5_plugins}
BuildRequires:  libcurl-devel >= 7.62.0
%endif

%if %{with dnf5daemon_server}
# required for dnf5daemon-server
BuildRequires:  pkgconfig(sdbus-c++) >= 0.9.0
BuildRequires:  systemd-rpm-macros
%if %{with dnf5daemon_tests}
BuildRequires:  dbus-daemon
BuildRequires:  polkit
BuildRequires:  python3-devel
BuildRequires:  python3dist(dbus-python)
%endif
%endif

%if %{with plugin_rhsm}
BuildRequires:  pkgconfig(librhsm) >= 0.0.3
BuildRequires:  pkgconfig(glib-2.0) >= 2.44.0
%endif

# ========== language bindings section ==========

%if %{with perl5} || %{with ruby} || %{with python3}
BuildRequires:  swig >= %{swig_version}
%endif

%if %{with perl5}
# required for perl-libdnf5 and perl-libdnf5-cli
BuildRequires:  perl-devel
BuildRequires:  perl-generators
%if %{with tests}
BuildRequires:  perl(strict)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Exception)
BuildRequires:  perl(warnings)
BuildRequires:  perl(FindBin)
%endif
%endif

%if %{with ruby}
# required for ruby-libdnf5 and ruby-libdnf5-cli
BuildRequires:  pkgconfig(ruby)
%if %{with tests}
BuildRequires:  rubygem-test-unit
%endif
%endif

%if %{with python3}
# required for python3-libdnf5 and python3-libdnf5-cli
BuildRequires:  python3-devel
%endif

Provides: tdnf = %{version}-%{release}
%description
DNF5 is a command-line package manager that automates the process of installing,
upgrading, configuring, and removing computer programs in a consistent manner.
It supports RPM packages, modulemd modules, and comps groups & environments.

%post
%if %{with dnf5_obsoletes_dnf}
%systemd_post dnf-makecache.timer
%else
%systemd_post dnf5-makecache.timer
%endif

%preun
%if %{with dnf5_obsoletes_dnf}
%systemd_preun dnf-makecache.timer
%else
%systemd_preun dnf5-makecache.timer
%endif

%postun
%if %{with dnf5_obsoletes_dnf}
%systemd_postun_with_restart dnf-makecache.timer
%else
%systemd_postun_with_restart dnf5-makecache.timer
%endif

%files -f dnf5.lang
%{_bindir}/dnf5
%if %{with dnf5_obsoletes_dnf}
%{_bindir}/dnf
%{_bindir}/yum
%endif
%{_unitdir}/dnf*-makecache.service
%{_unitdir}/dnf*-makecache.timer

%if 0%{?fedora} || 0%{?rhel} > 10
%{_bindir}/microdnf
%endif

%dir %{_sysconfdir}/dnf/dnf5-aliases.d
%doc %{_sysconfdir}/dnf/dnf5-aliases.d/README
%dir %{_datadir}/dnf5
%dir %{_datadir}/dnf5/aliases.d
%{_datadir}/dnf5/aliases.d/compatibility.conf
%dir %{_libdir}/dnf5
%dir %{_libdir}/dnf5/plugins
%dir %{_datadir}/dnf5/dnf5-plugins
%dir %{_sysconfdir}/dnf/dnf5-plugins
%doc %{_libdir}/dnf5/plugins/README
%dir %{_libdir}/libdnf5/plugins
%dir %{_datadir}/bash-completion/
%dir %{_datadir}/bash-completion/completions/
%{_datadir}/bash-completion/completions/dnf*
%license COPYING.md
%license gpl-2.0.txt
%doc AUTHORS.md CHANGELOG.md CONTRIBUTING.md README.md
%if %{with man}
%{_mandir}/man8/dnf5.8.*
%if %{with dnf5_obsoletes_dnf}
%{_mandir}/man8/dnf.8.*
%endif
%{_mandir}/man8/dnf*-advisory.8.*
%{_mandir}/man8/dnf*-autoremove.8.*
%{_mandir}/man8/dnf*-check.8.*
%{_mandir}/man8/dnf*-check-upgrade.8.*
%{_mandir}/man8/dnf*-clean.8.*
%{_mandir}/man8/dnf*-distro-sync.8.*
%{_mandir}/man8/dnf*-do.8.*
%{_mandir}/man8/dnf*-downgrade.8.*
%{_mandir}/man8/dnf*-download.8.*
%{_mandir}/man8/dnf*-environment.8.*
%{_mandir}/man8/dnf*-group.8.*
%{_mandir}/man8/dnf*-history.8.*
%{_mandir}/man8/dnf*-info.8.*
%{_mandir}/man8/dnf*-install.8.*
%{_mandir}/man8/dnf*-leaves.8.*
%{_mandir}/man8/dnf*-list.8.*
%{_mandir}/man8/dnf*-makecache.8.*
%{_mandir}/man8/dnf*-mark.8.*
%{_mandir}/man8/dnf*-module.8.*
%{_mandir}/man8/dnf*-offline.8.*
%{_mandir}/man8/dnf*-provides.8.*
%{_mandir}/man8/dnf*-reinstall.8.*
%{_mandir}/man8/dnf*-remove.8.*
%{_mandir}/man8/dnf*-replay.8.*
%{_mandir}/man8/dnf*-repo.8.*
%{_mandir}/man8/dnf*-repoquery.8.*
%{_mandir}/man8/dnf*-search.8.*
%{_mandir}/man8/dnf*-swap.8.*
%{_mandir}/man8/dnf*-system-upgrade.8.*
%{_mandir}/man8/dnf*-upgrade.8.*
%{_mandir}/man8/dnf*-versionlock.8.*
%{_mandir}/man7/dnf*-aliases.7.*
%{_mandir}/man7/dnf*-caching.7.*
%{_mandir}/man7/dnf*-comps.7.*
%{_mandir}/man7/dnf*-filtering.7.*
%{_mandir}/man7/dnf*-forcearch.7.*
%{_mandir}/man7/dnf*-installroot.7.*
%{_mandir}/man7/dnf*-modularity.7.*
%{_mandir}/man7/dnf*-specs.7.*
%{_mandir}/man7/dnf*-system-state.7.*
%{_mandir}/man7/dnf*-changes-from-dnf4.7.*
%{_mandir}/man5/dnf*.conf.5.*
%{_mandir}/man5/dnf*.conf-todo.5.*
%{_mandir}/man5/dnf*.conf-deprecated.5.*
%endif

%if %{with systemd}
%{_unitdir}/dnf5-offline-transaction.service
%{_unitdir}/dnf5-offline-transaction-cleanup.service
%{_unitdir}/system-update.target.wants/dnf5-offline-transaction.service
%endif

%if %{without dnf5_plugins}
%exclude %{_datadir}/dnf5/aliases.d/compatibility-plugins.conf
%exclude %{_datadir}/dnf5/aliases.d/compatibility-reposync.conf
%endif

# ========== libdnf5 ==========
%{_bindir}/tdnf
%package -n libdnf5
Summary:        Package management library
License:        LGPL-2.1-or-later
#Requires:       libmodulemd{?_isa} >= {libmodulemd_version}
Requires:       libsolv%{?_isa} >= %{libsolv_version}
Requires:       librepo%{?_isa} >= %{librepo_version}
Requires:       sqlite-libs%{?_isa} >= %{sqlite_version}
%if %{with dnf5_obsoletes_dnf}
Conflicts:      dnf-data < 4.20.0
%endif

%description -n libdnf5
Package management library.

%files -n libdnf5 -f libdnf5.lang
%if %{with dnf5_obsoletes_dnf}
%config(noreplace) %{_sysconfdir}/dnf/dnf.conf
%dir %{_sysconfdir}/dnf/vars
%dir %{_sysconfdir}/dnf/protected.d
%else
%exclude %{_sysconfdir}/dnf/dnf.conf
%endif
%ghost %attr(0644, root, root) %{_sysconfdir}/dnf/versionlock.toml
%dir %{_datadir}/dnf5/libdnf.conf.d
%dir %{_sysconfdir}/dnf/libdnf5.conf.d
%dir %{_datadir}/dnf5/repos.override.d
%dir %{_sysconfdir}/dnf/repos.override.d
%dir %{_sysconfdir}/dnf/libdnf5-plugins
%dir %{_datadir}/dnf5/repos.d
%dir %{_datadir}/dnf5/vars.d
%dir %{_libdir}/libdnf5
%{_libdir}/libdnf5.so.2*
%dir %{_prefix}/lib/sysimage/libdnf5
%attr(0755, root, root) %ghost %dir %{_prefix}/lib/sysimage/libdnf5/comps_groups
%verify(not md5 size mtime) %attr(0644, root, root) %ghost %{_prefix}/lib/sysimage/libdnf5/environments.toml
%verify(not md5 size mtime) %attr(0644, root, root) %ghost %{_prefix}/lib/sysimage/libdnf5/groups.toml
%verify(not md5 size mtime) %attr(0644, root, root) %ghost %{_prefix}/lib/sysimage/libdnf5/modules.toml
%verify(not md5 size mtime) %attr(0644, root, root) %ghost %{_prefix}/lib/sysimage/libdnf5/nevras.toml
%attr(0755, root, root) %ghost %dir %{_prefix}/lib/sysimage/libdnf5/offline
%verify(not md5 size mtime) %attr(0644, root, root) %ghost %{_prefix}/lib/sysimage/libdnf5/offline/offline-transaction-state.toml
%attr(0755, root, root) %ghost %dir %{_prefix}/lib/sysimage/libdnf5/offline/packages
%verify(not md5 size mtime) %attr(0644, root, root) %ghost %{_prefix}/lib/sysimage/libdnf5/offline/transaction.json
%verify(not md5 size mtime) %attr(0644, root, root) %ghost %{_prefix}/lib/sysimage/libdnf5/packages.toml
%verify(not md5 size mtime) %attr(0644, root, root) %ghost %{_prefix}/lib/sysimage/libdnf5/system.toml
%verify(not md5 size mtime) %attr(0644, root, root) %ghost %{_prefix}/lib/sysimage/libdnf5/transaction_history.sqlite{,-shm,-wal}
%license lgpl-2.1.txt
%ghost %attr(0755, root, root) %dir %{_var}/cache/libdnf5
%ghost %attr(0755, root, root) %dir %{_sharedstatedir}/dnf

# ========== libdnf5-cli ==========

%if %{with libdnf_cli}
%package -n libdnf5-cli
Summary:        Library for working with a terminal in a command-line package manager
License:        LGPL-2.1-or-later
Requires:       libdnf5%{?_isa} = %{version}-%{release}

%description -n libdnf5-cli
Library for working with a terminal in a command-line package manager.

%files -n libdnf5-cli -f libdnf5-cli.lang
%{_libdir}/libdnf5-cli.so.2*
%license COPYING.md
%license lgpl-2.1.txt
%endif

# ========== dnf5-devel ==========

%package -n dnf5-devel
Summary:        Development files for dnf5
License:        LGPL-2.1-or-later
Requires:       dnf5%{?_isa} = %{version}-%{release}
Requires:       libdnf5-devel%{?_isa} = %{version}-%{release}
Requires:       libdnf5-cli-devel%{?_isa} = %{version}-%{release}

%description -n dnf5-devel
Development files for dnf5.

%files -n dnf5-devel
%{_includedir}/dnf5/
%license COPYING.md
%license lgpl-2.1.txt


# ========== libdnf5-devel ==========

%package -n libdnf5-devel
Summary:        Development files for libdnf
License:        LGPL-2.1-or-later
Requires:       libdnf5%{?_isa} = %{version}-%{release}
Requires:       libsolv-devel%{?_isa} >= %{libsolv_version}

%description -n libdnf5-devel
Development files for libdnf.

%files -n libdnf5-devel
%{_includedir}/libdnf5/
%dir %{_libdir}/libdnf5
%{_libdir}/libdnf5.so
%{_libdir}/pkgconfig/libdnf5.pc
%license COPYING.md
%license lgpl-2.1.txt


# ========== libdnf5-cli-devel ==========

%package -n libdnf5-cli-devel
Summary:        Development files for libdnf5-cli
License:        LGPL-2.1-or-later
Requires:       libdnf5-cli%{?_isa} = %{version}-%{release}

%description -n libdnf5-cli-devel
Development files for libdnf5-cli.

%files -n libdnf5-cli-devel
%{_includedir}/libdnf5-cli/
%{_libdir}/libdnf5-cli.so
%{_libdir}/pkgconfig/libdnf5-cli.pc
%license COPYING.md
%license lgpl-2.1.txt


# ========== perl-libdnf5 ==========

%if %{with perl5}
%package -n perl-libdnf5
Summary:        Perl 5 bindings for the libdnf library
License:        LGPL-2.1-or-later
Requires:       libdnf5%{?_isa} = %{version}-%{release}


%description -n perl-libdnf5
Perl 5 bindings for the libdnf library.

%files -n perl-libdnf5
%{perl_vendorarch}/libdnf5
%{perl_vendorarch}/auto/libdnf5
%license COPYING.md
%license lgpl-2.1.txt
%endif


# ========== perl-libdnf5-cli ==========

%if %{with perl5} && %{with libdnf_cli}
%package -n perl-libdnf5-cli
Summary:        Perl 5 bindings for the libdnf5-cli library
License:        LGPL-2.1-or-later
Requires:       libdnf5-cli%{?_isa} = %{version}-%{release}


%description -n perl-libdnf5-cli
Perl 5 bindings for the libdnf5-cli library.

%files -n perl-libdnf5-cli
%{perl_vendorarch}/libdnf5_cli
%{perl_vendorarch}/auto/libdnf5_cli
%license COPYING.md
%license lgpl-2.1.txt
%endif


# ========== python3-libdnf5 ==========

%if %{with python3}
%package -n python3-libdnf5
Summary:        Python 3 bindings for the libdnf5 library
License:        LGPL-2.1-or-later
Requires:       libdnf5%{?_isa} = %{version}-%{release}

%description -n python3-libdnf5
Python 3 bindings for the libdnf library.

%files -n python3-libdnf5
%{python3_sitearch}/libdnf5
%{python3_sitearch}/libdnf5-*.dist-info
%license COPYING.md
%license lgpl-2.1.txt
%endif


# ========== python3-libdnf5-cli ==========

%if %{with python3} && %{with libdnf_cli}
%package -n python3-libdnf5-cli
Summary:        Python 3 bindings for the libdnf5-cli library
License:        LGPL-2.1-or-later
Requires:       libdnf5-cli%{?_isa} = %{version}-%{release}

%description -n python3-libdnf5-cli
Python 3 bindings for the libdnf5-cli library.

%files -n python3-libdnf5-cli
%{python3_sitearch}/libdnf5_cli
%{python3_sitearch}/libdnf5_cli-*.dist-info
%license COPYING.md
%license lgpl-2.1.txt
%endif


# ========== ruby-libdnf5 ==========

%if %{with ruby}
%package -n ruby-libdnf5
Summary:        Ruby bindings for the libdnf library
License:        LGPL-2.1-or-later
Provides:       ruby(libdnf) = %{version}-%{release}
Requires:       libdnf5%{?_isa} = %{version}-%{release}
Requires:       ruby(release)

%description -n ruby-libdnf5
Ruby bindings for the libdnf library.

%files -n ruby-libdnf5
%{ruby_vendorarchdir}/libdnf5
%license COPYING.md
%license lgpl-2.1.txt
%endif


# ========== ruby-libdnf5-cli ==========

%if %{with ruby} && %{with libdnf_cli}
%package -n ruby-libdnf5-cli
Summary:        Ruby bindings for the libdnf5-cli library
License:        LGPL-2.1-or-later
Provides:       ruby(libdnf_cli) = %{version}-%{release}
Requires:       libdnf5-cli%{?_isa} = %{version}-%{release}
Requires:       ruby(release)

%description -n ruby-libdnf5-cli
Ruby bindings for the libdnf5-cli library.

%files -n ruby-libdnf5-cli
%{ruby_vendorarchdir}/libdnf5_cli
%license COPYING.md
%license lgpl-2.1.txt
%endif


# ========== libdnf5-plugin-actions ==========

%if %{with plugin_actions}
%package -n libdnf5-plugin-actions
Summary:        Libdnf5 plugin that allows to run actions (external executables) on hooks
License:        LGPL-2.1-or-later
Requires:       libdnf5%{?_isa} = %{version}-%{release}

%description -n libdnf5-plugin-actions
Libdnf5 plugin that allows to run actions (external executables) on hooks.

%files -n libdnf5-plugin-actions -f libdnf5-plugin-actions.lang
%{_libdir}/libdnf5/plugins/actions.*
%config %{_sysconfdir}/dnf/libdnf5-plugins/actions.conf
%dir %{_sysconfdir}/dnf/libdnf5-plugins/actions.d
%if %{with man}
%{_mandir}/man8/libdnf5-actions.8.*
%endif
%endif

# ========== libdnf5-plugin-appstream ==========

%if %{with plugin_appstream}

%package -n libdnf5-plugin-appstream
Summary:        Libdnf5 plugin to install repository AppStream data
License:        LGPL-2.1-or-later
Requires:       libdnf5%{?_isa} = %{version}-%{release}
BuildRequires:  pkgconfig(appstream) >= 0.16

%description -n libdnf5-plugin-appstream
Libdnf5 plugin that installs repository's AppStream data, for repositories which provide them.

%files -n libdnf5-plugin-appstream
%{_libdir}/libdnf5/plugins/appstream.so
%config %{_sysconfdir}/dnf/libdnf5-plugins/appstream.conf

%endif

# ========== libdnf5-plugin-expired-pgp-keys ==========

%if %{with plugin_expired_pgp_keys}
%package -n libdnf5-plugin-expired-pgp-keys
Summary:        Libdnf5 plugin for detecting and removing expired PGP keys
License:        LGPL-2.1-or-later
Requires:       libdnf5%{?_isa} = %{version}-%{release}
Requires:       gnupg2
%if 0%{?fedora} >= 43 || 0%{?rhel} >= 11
Requires:       rpm-libs%{?_isa} >= 5.99.90
%endif

%description -n libdnf5-plugin-expired-pgp-keys
Libdnf5 plugin for detecting and removing expired PGP keys.

%files -n libdnf5-plugin-expired-pgp-keys -f libdnf5-plugin-expired-pgp-keys.lang
%{_libdir}/libdnf5/plugins/expired-pgp-keys.*
%config %{_sysconfdir}/dnf/libdnf5-plugins/expired-pgp-keys.conf
%if %{with man}
%{_mandir}/man8/libdnf5-expired-pgp-keys.8.*
%endif
%endif

# ========== libdnf5-plugin-plugin_rhsm ==========

%if %{with plugin_rhsm}
%package -n libdnf5-plugin-rhsm
Summary:        Libdnf5 rhsm (Red Hat Subscription Manager) plugin
License:        LGPL-2.1-or-later
Requires:       libdnf5%{?_isa} = %{version}-%{release}

%description -n libdnf5-plugin-rhsm
Libdnf5 plugin with basic support for Red Hat subscriptions.
Synchronizes the the enrollment with the vendor system. This can change
the contents of the repositories configuration files according
to the subscription levels.

%files -n libdnf5-plugin-rhsm -f libdnf5-plugin-rhsm.lang
%{_libdir}/libdnf5/plugins/rhsm.*
%config %{_sysconfdir}/dnf/libdnf5-plugins/rhsm.conf
%endif


# ========== python3-libdnf5-plugins-loader ==========

%if %{with python_plugins_loader}
%package -n python3-libdnf5-python-plugins-loader
Summary:        Libdnf5 plugin that allows loading Python plugins
License:        LGPL-2.1-or-later
Requires:       libdnf5%{?_isa} = %{version}-%{release}
Requires:       python3-libdnf5%{?_isa} = %{version}-%{release}

%description -n python3-libdnf5-python-plugins-loader
Libdnf5 plugin that allows loading Python plugins.

%files -n python3-libdnf5-python-plugins-loader
%{_libdir}/libdnf5/plugins/python_plugins_loader.*
%dir %{python3_sitelib}/libdnf_plugins/
%doc %{python3_sitelib}/libdnf_plugins/README
%endif

# ========== libdnf5-plugin-local ==========

%if %{with plugin_local}
%package -n libdnf5-plugin-local
Summary:        Libdnf5 plugin that automatically copies all downloaded packages to a local repository
License:        LGPL-2.1-or-later
Requires:       libdnf5%{?_isa} = %{version}-%{release}
Requires:       createrepo_c

%description -n libdnf5-plugin-local
Libdnf5 plugin that automatically copies all downloaded packages to a repository on the local filesystem and generates repo metadata.

%files -n libdnf5-plugin-local
%{_libdir}/libdnf5/plugins/local.*
%config %{_sysconfdir}/dnf/libdnf5-plugins/local.conf
%if %{with man}
%{_mandir}/man8/libdnf5-local.8.*
%endif
%endif


# ========== dnf5daemon-client ==========

%if %{with dnf5daemon_client}
%package -n dnf5daemon-client
Summary:        Command-line interface for dnf5daemon-server
License:        GPL-2.0-or-later
Requires:       libdnf5%{?_isa} = %{version}-%{release}
Requires:       libdnf5-cli%{?_isa} = %{version}-%{release}
Requires:       dnf5daemon-server

%description -n dnf5daemon-client
Command-line interface for dnf5daemon-server.

%files -n dnf5daemon-client -f dnf5daemon-client.lang
%{_bindir}/dnf5daemon-client
%license COPYING.md
%license gpl-2.0.txt
%if %{with man}
%{_mandir}/man8/dnf5daemon-client.8.*
%endif
%endif


# ========== dnf5daemon-server ==========

%if %{with dnf5daemon_server}
%package -n dnf5daemon-server
Summary:        Package management service with a DBus interface
License:        GPL-2.0-or-later
Requires:       libdnf5%{?_isa} = %{version}-%{release}
Requires:       libdnf5-cli%{?_isa} = %{version}-%{release}
Requires:       dbus
Requires:       polkit
%if %{without dnf5_obsoletes_dnf}
Requires:       dnf-data
%endif

%description -n dnf5daemon-server
Package management service with a DBus interface.

%post -n dnf5daemon-server
%systemd_post dnf5daemon-server.service

%preun -n dnf5daemon-server
%systemd_preun dnf5daemon-server.service

%postun -n dnf5daemon-server
%systemd_postun_with_restart dnf5daemon-server.service

%files -n dnf5daemon-server -f dnf5daemon-server.lang
%config(noreplace) %{_sysconfdir}/dnf/dnf5daemon-server.conf
%{_sbindir}/dnf5daemon-server
%{_unitdir}/dnf5daemon-server.service
%{_datadir}/dbus-1/system.d/org.rpm.dnf.v0.conf
%{_datadir}/dbus-1/system-services/org.rpm.dnf.v0.service
%{_datadir}/dbus-1/interfaces/org.rpm.dnf.v0.*.xml
%{_datadir}/polkit-1/actions/org.rpm.dnf.v0.policy
%license COPYING.md
%license gpl-2.0.txt
%if %{with man}
%{_mandir}/man8/dnf5daemon-server.8.*
%{_mandir}/man8/dnf5daemon-dbus-api.8.*
%endif


# ========== dnf5daemon-server-polkit ==========

%package -n dnf5daemon-server-polkit
Summary:        Polkit rule to allow wheel group members install trusted packages
License:        GPL-2.0-or-later
Requires:       polkit
Requires:       dnf5daemon-server = %{version}-%{release}
BuildArch:      noarch

%description -n dnf5daemon-server-polkit
Polkit rule to allow active local wheel group members install packages from
trusted repositories using dnf5daemon-server.

%files -n dnf5daemon-server-polkit
%{_datadir}/polkit-1/rules.d/org.rpm.dnf.v0.rules
%endif


# ========== dnf5-plugins ==========
%if %{with dnf5_plugins}

%package -n dnf5-plugins
Summary:        Plugins for dnf5
License:        LGPL-2.1-or-later
Requires:       dnf5%{?_isa} = %{version}-%{release}
Requires:       libcurl%{?_isa} >= 7.62.0
Requires:       libdnf5%{?_isa} = %{version}-%{release}
Requires:       libdnf5-cli%{?_isa} = %{version}-%{release}
Provides:       dnf5-command(builddep)
Provides:       dnf5-command(changelog)
Provides:       dnf5-command(config-manager)
Provides:       dnf5-command(copr)
Provides:       dnf5-command(needs-restarting)
Provides:       dnf5-command(repoclosure)
Provides:       dnf5-command(reposync)
Provides:       dnf5-command(repomanage)

%description -n dnf5-plugins
Core DNF5 plugins that enhance dnf5 with builddep, changelog,
config-manager, copr, repoclosure, repomanage and reposync commands.

%files -n dnf5-plugins -f dnf5-plugin-builddep.lang -f dnf5-plugin-changelog.lang -f dnf5-plugin-config-manager.lang -f dnf5-plugin-copr.lang -f dnf5-plugin-needs-restarting.lang -f dnf5-plugin-repoclosure.lang -f dnf5-plugin-reposync.lang
%{_libdir}/dnf5/plugins/builddep_cmd_plugin.so
%{_libdir}/dnf5/plugins/changelog_cmd_plugin.so
%{_libdir}/dnf5/plugins/config-manager_cmd_plugin.so
%{_libdir}/dnf5/plugins/copr_cmd_plugin.so
%{_libdir}/dnf5/plugins/needs_restarting_cmd_plugin.so
%{_libdir}/dnf5/plugins/repoclosure_cmd_plugin.so
%{_libdir}/dnf5/plugins/reposync_cmd_plugin.so
%{_libdir}/dnf5/plugins/repomanage_cmd_plugin.so
%if %{with man}
%{_mandir}/man8/dnf*-builddep.8.*
%{_mandir}/man8/dnf*-changelog.8.*
%{_mandir}/man8/dnf*-config-manager.8.*
%{_mandir}/man8/dnf*-copr.8.*
%{_mandir}/man8/dnf*-needs-restarting.8.*
%{_mandir}/man8/dnf*-repoclosure.8.*
%{_mandir}/man8/dnf*-reposync.8.*
%{_mandir}/man8/dnf*-repomanage.8.*
%endif
%{_datadir}/dnf5/aliases.d/compatibility-plugins.conf
%{_datadir}/dnf5/aliases.d/compatibility-reposync.conf


# ========== dnf5-automatic plugin ==========

%package plugin-automatic
Summary:        Package manager - automated upgrades
License:        LGPL-2.1-or-later
Requires:       dnf5%{?_isa} = %{version}-%{release}
Requires:       libcurl-full%{?_isa}
Requires:       libdnf5%{?_isa} = %{version}-%{release}
Requires:       libdnf5-cli%{?_isa} = %{version}-%{release}
Provides:       dnf5-command(automatic)
%if %{with dnf5_obsoletes_dnf}
Provides:       dnf-automatic = %{version}-%{release}
Obsoletes:      dnf-automatic < 5
%else
Conflicts:      dnf-automatic < 5
%endif

%description plugin-automatic
Alternative command-line interface "dnf upgrade" suitable to be executed
automatically and regularly from systemd timers, cron jobs or similar.

%files plugin-automatic -f dnf5-plugin-automatic.lang
%ghost %attr(0644, root, root) %{_sysconfdir}/motd.d/dnf5-automatic
%{_libdir}/dnf5/plugins/automatic_cmd_plugin.so
%{_datadir}/dnf5/dnf5-plugins/automatic.conf
%ghost %attr(0644, root, root) %config(noreplace) %{_sysconfdir}/dnf/automatic.conf
%ghost %attr(0644, root, root) %config(noreplace) %{_sysconfdir}/dnf/dnf5-plugins/automatic.conf
%if %{with man}
%{_mandir}/man8/dnf*-automatic.8.*
%endif
%{_unitdir}/dnf5-automatic.service
%{_unitdir}/dnf5-automatic.timer
%{_unitdir}/dnf-automatic.service
%{_unitdir}/dnf-automatic.timer
%if %{with dnf5_obsoletes_dnf}
%{_bindir}/dnf-automatic
%else
%exclude %{_bindir}/dnf-automatic
%endif

%endif


# ========== unpack, build, check & install ==========

%prep
%autosetup -p1 -n dnf5-%{version}


%build
%cmake \
    -DPACKAGE_VERSION=%{version} \
    -DPERL_INSTALLDIRS=vendor \
    \
    -DENABLE_SOLV_FOCUSNEW=%{?with_focus_new:ON}%{!?with_focus_new:OFF} \
    \
    -DWITH_DNF5DAEMON_CLIENT=%{?with_dnf5daemon_client:ON}%{!?with_dnf5daemon_client:OFF} \
    -DWITH_DNF5DAEMON_SERVER=%{?with_dnf5daemon_server:ON}%{!?with_dnf5daemon_server:OFF} \
    -DWITH_LIBDNF5_CLI=%{?with_libdnf_cli:ON}%{!?with_libdnf_cli:OFF} \
    -DWITH_DNF5=%{?with_dnf5:ON}%{!?with_dnf5:OFF} \
    -DWITH_DNF5_OBSOLETES_DNF=%{?with_dnf5_obsoletes_dnf:ON}%{!?with_dnf5_obsoletes_dnf:OFF} \
    -DWITH_DNF5_PLUGINS=%{?with_dnf5_plugins:ON}%{!?with_dnf5_plugins:OFF} \
    -DWITH_PLUGIN_ACTIONS=%{?with_plugin_actions:ON}%{!?with_plugin_actions:OFF} \
    -DWITH_PLUGIN_APPSTREAM=%{?with_plugin_appstream:ON}%{!?with_plugin_appstream:OFF} \
    -DWITH_PLUGIN_EXPIRED_PGP_KEYS=%{?with_plugin_expired_pgp_keys:ON}%{!?with_plugin_expired_pgp_keys:OFF} \
    -DWITH_PLUGIN_RHSM=%{?with_plugin_rhsm:ON}%{!?with_plugin_rhsm:OFF} \
    -DWITH_PYTHON_PLUGINS_LOADER=%{?with_python_plugins_loader:ON}%{!?with_python_plugins_loader:OFF} \
    \
    -DWITH_COMPS=%{?with_comps:ON}%{!?with_comps:OFF} \
    -DWITH_MODULEMD=%{?with_modulemd:ON}%{!?with_modulemd:OFF} \
    -DWITH_SYSTEMD=%{?with_systemd:ON}%{!?with_systemd:OFF} \
    \
    -DWITH_HTML=%{?with_html:ON}%{!?with_html:OFF} \
    -DWITH_MAN=%{?with_man:ON}%{!?with_man:OFF} \
    \
    -DWITH_GO=%{?with_go:ON}%{!?with_go:OFF} \
    -DWITH_PERL5=%{?with_perl5:ON}%{!?with_perl5:OFF} \
    -DWITH_PYTHON3=%{?with_python3:ON}%{!?with_python3:OFF} \
    -DWITH_RUBY=%{?with_ruby:ON}%{!?with_ruby:OFF} \
    \
    -DWITH_SANITIZERS=%{?with_sanitizers:ON}%{!?with_sanitizers:OFF} \
    -DWITH_TESTS=%{?with_tests:ON}%{!?with_tests:OFF} \
    -DWITH_PERFORMANCE_TESTS=%{?with_performance_tests:ON}%{!?with_performance_tests:OFF} \
    -DWITH_DNF5DAEMON_TESTS=%{?with_dnf5daemon_tests:ON}%{!?with_dnf5daemon_tests:OFF} \
    \
    -DVERSION_PRIME=%{project_version_prime} \
    -DVERSION_MAJOR=%{project_version_major} \
    -DVERSION_MINOR=%{project_version_minor} \
    -DVERSION_MICRO=%{project_version_micro}
%cmake_build
%if %{with man}
    %cmake_build --target doc-man
%endif


%check
%if %{with tests}
    %ctest
%endif


%install
%cmake_install

%if %{with dnf5_obsoletes_dnf}
ln -sr %{buildroot}%{_bindir}/dnf5 %{buildroot}%{_bindir}/dnf
ln -sr %{buildroot}%{_bindir}/dnf5 %{buildroot}%{_bindir}/yum
ln -sr %{buildroot}%{_datadir}/bash-completion/completions/dnf5 %{buildroot}%{_datadir}/bash-completion/completions/dnf
%if %{with man}
    for file in %{buildroot}%{_mandir}/man[578]/dnf5[-.]*; do
        dir=$(dirname $file)
        filename=$(basename $file)
        ln -sr $file $dir/${filename/dnf5/dnf}
    done
%endif
# Make "dnf-makecache" the "real" unit name, but keep compatibility for playbooks that refer to dnf5-makecache
mv %{buildroot}%{_unitdir}/dnf5-makecache.service %{buildroot}%{_unitdir}/dnf-makecache.service
mv %{buildroot}%{_unitdir}/dnf5-makecache.timer %{buildroot}%{_unitdir}/dnf-makecache.timer
ln -s dnf-makecache.service %{buildroot}%{_unitdir}/dnf5-makecache.service
ln -s dnf-makecache.timer %{buildroot}%{_unitdir}/dnf5-makecache.timer
%endif

# own dirs and files that dnf5 creates on runtime
mkdir -p %{buildroot}%{_prefix}/lib/sysimage/libdnf5
for file in \
    environments.toml groups.toml modules.toml nevras.toml packages.toml \
    system.toml \
    transaction_history.sqlite transaction_history.sqlite-shm \
    transaction_history.sqlite-wal
do
    touch %{buildroot}%{_prefix}/lib/sysimage/libdnf5/$file
done
mkdir -p %{buildroot}%{_prefix}/lib/sysimage/libdnf5/comps_groups
mkdir -p %{buildroot}%{_prefix}/lib/sysimage/libdnf5/offline
touch %{buildroot}%{_sysconfdir}/dnf/versionlock.toml

%if 0%{?fedora} || 0%{?rhel} > 10
ln -sr %{buildroot}%{_bindir}/dnf5 %{buildroot}%{_bindir}/microdnf
%endif

%if %{with systemd}
mkdir -p %{buildroot}%{_unitdir}/system-update.target.wants/
pushd %{buildroot}%{_unitdir}/system-update.target.wants/
  ln -sr ../dnf5-offline-transaction.service
popd
%endif

mkdir -p %{buildroot}%{_libdir}/libdnf5/plugins

%find_lang dnf5
%if %{with dnf5_plugins}
%find_lang dnf5-plugin-automatic
%find_lang dnf5-plugin-builddep
%find_lang dnf5-plugin-changelog
%find_lang dnf5-plugin-config-manager
%find_lang dnf5-plugin-copr
%find_lang dnf5-plugin-needs-restarting
%find_lang dnf5-plugin-repoclosure
%find_lang dnf5-plugin-reposync
%endif
%if %{with dnf5daemon_client}
%find_lang dnf5daemon-client
%endif
%if %{with dnf5daemon_server}
%find_lang dnf5daemon-server
%endif
%find_lang libdnf5
%if %{with libdnf_cli}
%find_lang libdnf5-cli
%endif
%if %{with plugin_actions}
%find_lang libdnf5-plugin-actions
%endif
%if %{with plugin_expired_pgp_keys}
%find_lang libdnf5-plugin-expired-pgp-keys
%endif
%if %{with plugin_rhsm}
%find_lang libdnf5-plugin-rhsm
%endif

%ldconfig_scriptlets

ln -sr %{buildroot}%{_bindir}/dnf5 %{buildroot}%{_bindir}/tdnf
%changelog
* Wed Feb 04 2026 Packit <hello@packit.dev> - 5.2.18.0-1
- Update to version 5.2.18.0

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 5.2.17.0-2
- Rebuilt for Python 3.14.0rc3 bytecode

* Tue Sep 02 2025 Packit <hello@packit.dev> - 5.2.17.0-1
- Update to version 5.2.17.0

* Tue Aug 19 2025 Marek Blaha <mblaha@redhat.com> - 5.2.16.0-3
- Fix confirm_key_with_options D-Bus signature

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 5.2.16.0-2
- Rebuilt for Python 3.14.0rc2 bytecode

* Thu Aug 07 2025 Packit <hello@packit.dev> - 5.2.16.0-1
- Update to version 5.2.16.0

* Thu Jul 24 2025 Petr Pisar <ppisar@redhat.com> - 5.2.15.0-3
- Fix a crash when downloading packages with enabled fastestmirror option
  (bug #2381859)

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.15.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jul 11 2025 Packit <hello@packit.dev> - 5.2.15.0-1
- Update to version 5.2.15.0

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 5.2.14.0-4
- Perl 5.42 rebuild

* Thu Jun 26 2025 Marek Blaha <mblaha@redhat.com> - 5.2.14.0-3
- dnfdaemon: Make permission check more consistent

* Wed Jun 25 2025 Marek Blaha <mblaha@redhat.com> - 5.2.14.0-2
- Remove incorrect dnfdaemon output parameter names (https://github.com/rpm-software-management/dnf5/issues/2317)

* Fri Jun 20 2025 Packit <hello@packit.dev> - 5.2.14.0-1
- Update to version 5.2.14.0

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 5.2.13.1-3
- Rebuilt for Python 3.14

* Tue May 13 2025 Marek Blaha <mblaha@redhat.com> - 5.2.13.1-2
- Rebuilt for sdbus-cpp-2.1

* Thu Apr 24 2025 Packit <hello@packit.dev> - 5.2.13.1-1
- Update to version 5.2.13.1

* Mon Apr 21 2025 Packit <hello@packit.dev> - 5.2.13.0-1
- Update to version 5.2.13.0

* Fri Apr 11 2025 Jonathan Wright <jonathan@almalinux.org> - 5.2.12.0-4
- Fix conditional controlling SOLVER_FLAG_FOCUS_NEW support on RHEL

* Wed Apr 09 2025 Marek Blaha <mblaha@redhat.com> - 5.2.12.0-3
- Rebuilt for sdbus-cpp-2.1

* Wed Apr 02 2025 Petr Pisar <ppisar@redhat.com> - 5.2.12.0-2
- Set a mode for ghost files to 0644 (bug #2343342)
- Respect install root in expired-pgp-keys plugin (bug #2356528)
- Add "-i" and "-f" short options for repoquery command (bug #2338174)
- Document environment variables for a terminal and temporary files
  (bug #2353349)

* Tue Mar 18 2025 Packit <hello@packit.dev> - 5.2.12.0-1
- Update to version 5.2.12.0

* Fri Mar 07 2025 Packit <hello@packit.dev> - 5.2.11.0-1
- Update to version 5.2.11.0

* Fri Feb 14 2025 Jan Kolarik <jkolarik@redhat.com> - 5.2.10.0-2
- Recommend expired-pgp-keys plugin by default on F42+

* Thu Feb 06 2025 Packit <hello@packit.dev> - 5.2.10.0-1
- Update translations from weblate
- plugins: Provide the actual API version used
- plugins: Check only major version of API for incompatibility
- expired-pgp-keys: New plugin for detecting expired PGP keys
- rpm_signature: Fix rpmdb_lookup comparison case mismatch
- actions: Update with resolved hook
- libdnf plugins: Add resolved hook
- SWIG bindings for common::Message and common::EmptyMessage
- EmptyMessage: class for passing an empty message
- Message: base class for passing a message for formatting in the destination
- utils::format: Support for user defined locale
- SWIG bindings for utils::Locale
- utils::Locale: class for passing C and CPP locale
- utils::format: Support for formatting args according to BgettextMessage
- bgettext: Add function b_gettextmsg_get_plural_id

* Tue Feb 04 2025 Packit <hello@packit.dev> - 5.2.9.0-1
- Update translations from weblate
- automatic: Translate end-of-lines in email emitter by DNF
- ruby: Fix swig namespacing in Ruby.
- Correct Ruby %%module definition in swig files.
- Documentation enhancements
- Add a hint to `history info` without trans IDs when no match found
- Add `--contains-pkgs=..` option to `history` `list` and `info`
- During package download setup first add all downloads then handle local
- Enhance `perform_control_sequences()` to handle colors
- versionlock: Fix wildcards handling in `add` command
- ruby: Implement Enumerable for libdnf5::advisory::AdvisorySet.
- ruby: Implement Enumerable for libdnf5::rpm::ReldepList.
- ruby: Implement Enumerable for libdnf5::rpm::PackageSet.
- Implement each() for iterating over collection in ruby.
- Add --json output to advisory info
- I18N: Annotate indentation of the transaction summary
- libdnf5: Load plugins with RTLD_NODELETE flag set
- libdnf5: Add a plugin to download and install repo's Appstream data
- Fix bash completion if colon is in the word to complete
- Remove and rename global variables in bash completion
- DNF5 bash completion: Offer package NAMEs in all cases
- Bash completion: always offer NEVRAs for packages
- repo: Fix logging metadata download errors handling
- Copr plugin: Fix resource leak in load_all_configuration
- Own /var/lib/dnf by libdnf5
- Display remaining time as nonnegative number
- automatic: Substitute variables in command_format
- Bumb readthedocs ubuntu image version to fix the docs generation
- automatic: add a default setting to not emit boring messages
- Incorrect library name in libdnf5-cli.pc
- Fix reporting disk space to be freed on a pure package removal
- Support ProgressBar messages with wide characters
- Add padding to ProgressBar messages to avoid overlapping
- SWIG: support repo::DownloadCallbacks user_data
- Remove redundant %%python_provide statements
- python3-libdnf5: Remove superfluous provides for python-libdnf
- Update pre-commit hooks to latest versions in F41

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.8.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jan 09 2025 Petr Pisar <ppisar@redhat.com> - 5.2.8.1-4
- Fix plural form in "Replacing N packages" message
- Fix reporting disk space to be freed on a pure package removal (GH #1938)
- Fix a library name in libdnf5-cli pkg-config file
- Fix expanding "{body}" in command_format option of automatic plugin
  (GH #1951)
- Display remaining time as nonnegative number (bug #2332931)
- Document removal of "userinstalled" subcommand (bug #2335257)
- Own /var/lib/dnf by libdnf5 (bug #2332856)
- Fix a memory leak in copr plugin
- Fix a crash when reporting metadata download errors (GH #1919)
- Fix end-of-lines in messages sent by email emitter of automatic plugin
  (bug #2335508)

* Wed Jan 08 2025 Mamoru TASAKA <mtasaka@fedoraproject.org> - 5.2.8.1-3
- Rebuild for https://fedoraproject.org/wiki/Changes/Ruby_3.4

* Fri Dec 06 2024 Miro Hrončok <mhroncok@redhat.com> - 5.2.8.1-2
- python3-libdnf5: Remove superfluous provides for python-libdnf

* Thu Dec 05 2024 Packit <hello@packit.dev> - 5.2.8.1-1
## What's Changed
 * Fix libdnf5 actions plugin sign conversion compilation err by @jrohel in https://github.com/rpm-software-management/dnf5/pull/1921
 * builddep: Add support for --spec and --srpm options by @m-blaha in https://github.com/rpm-software-management/dnf5/pull/1907
 * Implement reposync plugin by @m-blaha in https://github.com/rpm-software-management/dnf5/pull/1903
 * `MultiProgressBar` fixes and tests by @kontura in https://github.com/rpm-software-management/dnf5/pull/1925
 * changes_from_dnf4: fix formatting of indented `list` points by @kontura in https://github.com/rpm-software-management/dnf5/pull/1930
 * Python API: Method `DownloadCallbacks.add_new_download` can return `None` by @jrohel in https://github.com/rpm-software-management/dnf5/pull/1929
 * doc: Use OpenPGP instead of PGP by @ppisar in https://github.com/rpm-software-management/dnf5/pull/1931
 * Release 5.2.8.1 by @github-actions in https://github.com/rpm-software-management/dnf5/pull/1934


 **Full Changelog**: https://github.com/rpm-software-management/dnf5/compare/5.2.8.0...5.2.8.1

* Mon Dec 02 2024 Packit <hello@packit.dev> - 5.2.8.0-1
## What's Changed
 * rpm: Reset RPM log callback upon RpmLogGuard destruction by @m-blaha in https://github.com/rpm-software-management/dnf5/pull/1870
 * SWIG bindings for user_cb_data in repo::DownloadCallbacks, unit tests by @jrohel in https://github.com/rpm-software-management/dnf5/pull/1849
 * I18N: Mark messages in "dnf search" output for a translation by @sunwire in https://github.com/rpm-software-management/dnf5/pull/1861
 * Hint when an unknown option is available on different commands by @kontura in https://github.com/rpm-software-management/dnf5/pull/1858
 * builddep: add support for remote arguments by @kontura in https://github.com/rpm-software-management/dnf5/pull/1874
 * I18N: Mark "Total" message in MultiProgressBar() for a translation by @sunwire in https://github.com/rpm-software-management/dnf5/pull/1885
 * Make `test_multi_progress_bar` test more resilient by @kontura in https://github.com/rpm-software-management/dnf5/pull/1882
 * package_downloader: Ensure creation of intermediate directories by @m-blaha in https://github.com/rpm-software-management/dnf5/pull/1876
 * I18N: Mark <unknown> message in dnf list --installed output for a translation by @sunwire in https://github.com/rpm-software-management/dnf5/pull/1883
 * repo: Make Repo::download_metadata() method public by @m-blaha in https://github.com/rpm-software-management/dnf5/pull/1878
 * repo: While cloning root metadata copy also metalink by @m-blaha in https://github.com/rpm-software-management/dnf5/pull/1880
 * spec: toggle dnf5_obsoletes_dnf for RHEL 11 by @yselkowitz in https://github.com/rpm-software-management/dnf5/pull/1886
 * rpm: New API to check PGP signature of RPM file by @m-blaha in https://github.com/rpm-software-management/dnf5/pull/1877
 * repo: Add option to download all repository metadata by @m-blaha in https://github.com/rpm-software-management/dnf5/pull/1879
 * Add packit job to run ABI check on testing farm by @kontura in https://github.com/rpm-software-management/dnf5/pull/1869
 * Fix copr chroot specification: replace faulty regex with simpler split by @kontura in https://github.com/rpm-software-management/dnf5/pull/1863
 * Download cmd: Require at leats one argument/package to download by @jrohel in https://github.com/rpm-software-management/dnf5/pull/1905
 * Install defs.h for /usr/include/dnf5/context.hpp by @ppisar in https://github.com/rpm-software-management/dnf5/pull/1914
 * doc: Use PGP instead of GPG by @ppisar in https://github.com/rpm-software-management/dnf5/pull/1917

## New Contributors
 * @sunwire made their first contribution in https://github.com/rpm-software-management/dnf5/pull/1861

 **Full Changelog**: https://github.com/rpm-software-management/dnf5/compare/5.2.7.0...5.2.8.0

* Thu Nov 21 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 5.2.7.0-2
- Toggle dnf5_obsoletes_dnf for ELN

* Tue Nov 12 2024 Packit <hello@packit.dev> - 5.2.7.0-1
## What's Changed
 * copr: use pubkey URL returned by Copr API by @FrostyX in https://github.com/rpm-software-management/dnf5/pull/1725
 * Package file documenting dnf4/dnf5 changes as man page by @m-blaha in https://github.com/rpm-software-management/dnf5/pull/1729
 * daemon: Reset the goal by @m-blaha in https://github.com/rpm-software-management/dnf5/pull/1678
 * Consistently use "removing" instead of "erasing" packages by @ppisar in https://github.com/rpm-software-management/dnf5/pull/1732
 * Add --allmirros option for `dnf download --url` by @alimirjamali in https://github.com/rpm-software-management/dnf5/pull/1735
 * comps: Fix memory issues in group serialization by @m-blaha in https://github.com/rpm-software-management/dnf5/pull/1743
 * Print RPM messages to the user by @m-blaha in https://github.com/rpm-software-management/dnf5/pull/1728
 * i18n: Update translation templates from Weblate by @ppisar in https://github.com/rpm-software-management/dnf5/pull/1745
 * i18n: Fix plural forms for "Warning: skipped PGP checks..." message by @ppisar in https://github.com/rpm-software-management/dnf5/pull/1746
 * Set `POOL_FLAG_ADDFILEPROVIDESFILTERED` only when not loading filelists by @kontura in https://github.com/rpm-software-management/dnf5/pull/1741
 * When writing main solv file (primary.xml) don't store filelists by @kontura in https://github.com/rpm-software-management/dnf5/pull/1752
 * Fix libdnf5::utils::patterns: Include missing headers, no inline API funcs, mark `noexcept` by @jrohel in https://github.com/rpm-software-management/dnf5/pull/1742
 * Allow unlimited number of arguments for history `list` and `info` by @kontura in https://github.com/rpm-software-management/dnf5/pull/1755
 * [swig] Bindings and tests for libdnf5::utils::[is_glob_pattern | is_file_pattern] by @jrohel in https://github.com/rpm-software-management/dnf5/pull/1738
 * doc: "dnf repoquery --unsatisfied" is not supported by @ppisar in https://github.com/rpm-software-management/dnf5/pull/1758
 * comps: add get_base() to {Group,Environment}{,Query} by @gotmax23 in https://github.com/rpm-software-management/dnf5/pull/1722
 * Make most descriptions for `dnf5 --help` translatable. by @bc-lee in https://github.com/rpm-software-management/dnf5/pull/1751
 * test: Normalize Python code by @ppisar in https://github.com/rpm-software-management/dnf5/pull/1762
 * Recommend --use-host-config if --installroot is used and not all repositories can be enabled by @ppisar in https://github.com/rpm-software-management/dnf5/pull/1760
 * log: Preserve log messages during RPM transaction by @m-blaha in https://github.com/rpm-software-management/dnf5/pull/1772
 * chore: Clean up Fedora 37-related conditionals in RPM spec by @bc-lee in https://github.com/rpm-software-management/dnf5/pull/1765
 * Change `gpgcheck` option to `pkg_gpgcheck` but stay compatible by @kontura in https://github.com/rpm-software-management/dnf5/pull/1766
 * Drop `errorlevel` config option by @kontura in https://github.com/rpm-software-management/dnf5/pull/1788
 * build: Remove an explicit swig option -ruby by @ppisar in https://github.com/rpm-software-management/dnf5/pull/1795
 * Revert "Drop `errorlevel` config option" by @kontura in https://github.com/rpm-software-management/dnf5/pull/1793
 * Update dnf5.conf.5 to reflect change in fastestmirror behavior by @PhirePhly in https://github.com/rpm-software-management/dnf5/pull/1784
 * historydb: Prevent insertion of duplicate group packages by @m-blaha in https://github.com/rpm-software-management/dnf5/pull/1798
 * Optimize getting counts of transaction items by @kontura in https://github.com/rpm-software-management/dnf5/pull/1778
 * Fix parsing of offline transaction JSON file by @m-blaha in https://github.com/rpm-software-management/dnf5/pull/1807
 * When `multi_progress_bar` finishes print new line automatically by @kontura in https://github.com/rpm-software-management/dnf5/pull/1805
 * Run "makecache" periodically to keep the cache ready. by @gordonmessmer in https://github.com/rpm-software-management/dnf5/pull/1791
 * DownloadCallbacks: Ensure `end` for every successful `add_new_download` by @jrohel in https://github.com/rpm-software-management/dnf5/pull/1814
 * Clear up changes doc about optional subcommands by @kontura in https://github.com/rpm-software-management/dnf5/pull/1834
 * MultiProgressBar now buffers the output text to a single write by @Giedriusj1 in https://github.com/rpm-software-management/dnf5/pull/1825
 * repo: Fix invalid free() by @m-blaha in https://github.com/rpm-software-management/dnf5/pull/1850
 * daemon: API to reset the session.base instance by @m-blaha in https://github.com/rpm-software-management/dnf5/pull/1757
 * Release 5.2.7.0 by @github-actions in https://github.com/rpm-software-management/dnf5/pull/1857

## New Contributors
 * @FrostyX made their first contribution in https://github.com/rpm-software-management/dnf5/pull/1725
 * @alimirjamali made their first contribution in https://github.com/rpm-software-management/dnf5/pull/1735
 * @bc-lee made their first contribution in https://github.com/rpm-software-management/dnf5/pull/1751
 * @PhirePhly made their first contribution in https://github.com/rpm-software-management/dnf5/pull/1784
 * @Giedriusj1 made their first contribution in https://github.com/rpm-software-management/dnf5/pull/1825

 **Full Changelog**: https://github.com/rpm-software-management/dnf5/compare/5.2.6.2...5.2.7.0

* Fri Sep 20 2024 Packit <hello@packit.dev> - 5.2.6.2-1
## What's Changed
 * chore: static_cast to fix sign conversion warning by @evan-goode in https://github.com/rpm-software-management/dnf5/pull/1715
 * Fix `sdbus::ObjectPath` when checking signals `object_path` by @kontura in https://github.com/rpm-software-management/dnf5/pull/1711
 * Do not install /var/cache/libdnf5 directory by @ppisar in https://github.com/rpm-software-management/dnf5/pull/1712
 * setlocale: If locale setting fails, try using C.UTF-8 as fallback by @jrohel in https://github.com/rpm-software-management/dnf5/pull/1713
 * Birectional communication of libdnf5 actions plugin with running processes - "json" mode by @jrohel in https://github.com/rpm-software-management/dnf5/pull/1642
 * Release 5.2.6.2 by @github-actions in https://github.com/rpm-software-management/dnf5/pull/1719


 **Full Changelog**: https://github.com/rpm-software-management/dnf5/compare/5.2.6.1...5.2.6.2

* Thu Sep 19 2024 Packit <hello@packit.dev> - 5.2.6.1-1
## What's Changed
 * doc: dnf5-repoquery: Mention %%{reason} query tag at --userinstalled by @ppisar in https://github.com/rpm-software-management/dnf5/pull/1683
 * automatic: Use original dnf4 config file location by @m-blaha in https://github.com/rpm-software-management/dnf5/pull/1690
 * spec: Recommend dnf5-plugins if dnf-plugins-core installed by @evan-goode in https://github.com/rpm-software-management/dnf5/pull/1691
 * transaction_callbacks: Deprecate confusing alias by @m-blaha in https://github.com/rpm-software-management/dnf5/pull/1689
 * offline: Update usage of toml11-devel by @evan-goode in https://github.com/rpm-software-management/dnf5/pull/1694
 * doc: add typical dnf5 workflow by @kontura in https://github.com/rpm-software-management/dnf5/pull/1661
 * swig: Add wrappers for TransactionEnvironment and TransactionGroup by @pkratoch in https://github.com/rpm-software-management/dnf5/pull/1697
 * I18N: Mark messages in "dnf install" output for a translation by @ppisar in https://github.com/rpm-software-management/dnf5/pull/1696
 * doc: Document arch override for API users by @m-blaha in https://github.com/rpm-software-management/dnf5/pull/1695
 * Fix: libdnf5-cli: TransactionSummary counters data type by @jrohel in https://github.com/rpm-software-management/dnf5/pull/1701
 * I18N: Mark messages in "dnf info" output for a translation by @ppisar in https://github.com/rpm-software-management/dnf5/pull/1698
 * dnf5: Run transaction test for offline transactions by @m-blaha in https://github.com/rpm-software-management/dnf5/pull/1672
 * Warn on sign conversion by @ppisar in https://github.com/rpm-software-management/dnf5/pull/1703
 * dnf clean: Do not report an error on a nonexistent cache directory by @ppisar in https://github.com/rpm-software-management/dnf5/pull/1707
 * Release 5.2.6.1 by @github-actions in https://github.com/rpm-software-management/dnf5/pull/1714


 **Full Changelog**: https://github.com/rpm-software-management/dnf5/compare/5.2.6.0...5.2.6.1

* Mon Sep 09 2024 Packit <hello@packit.dev> - 5.2.6.0-1
## What's Changed
 * Make offline transactions work with local rpm files by @m-blaha in https://github.com/rpm-software-management/dnf5/pull/1586
 * Add `history redo` command by @kontura in https://github.com/rpm-software-management/dnf5/pull/1595
 * Improve "After this operation" disk usage messages by @ppisar in https://github.com/rpm-software-management/dnf5/pull/1600
 * Add an example how to disable repo to `repo` command man page by @kontura in https://github.com/rpm-software-management/dnf5/pull/1601
 * dnfdaemon: implement D-Bus API for cleaning caches by @m-blaha in https://github.com/rpm-software-management/dnf5/pull/1589
 * Add some docs about environments by @dschwoerer in https://github.com/rpm-software-management/dnf5/pull/1562
 * Fix a use-after-free in EmitterEmail::notify() by @ppisar in https://github.com/rpm-software-management/dnf5/pull/1604
 * spec: Stricten a dependency on DNF libraries in plugin subpackages by @ppisar in https://github.com/rpm-software-management/dnf5/pull/1607
 * Reduce the noise around running scriptlets by @m-blaha in https://github.com/rpm-software-management/dnf5/pull/1606
 * builddep: Support the --with/--without options to toggle bconds by @dm0- in https://github.com/rpm-software-management/dnf5/pull/1509
 * Use `SOLVER_FLAG_FOCUS_NEW` to install latests versions of deps by @kontura in https://github.com/rpm-software-management/dnf5/pull/1582
 * spec: fix cmake focus_new arg by @kontura in https://github.com/rpm-software-management/dnf5/pull/1615
 * dnfdaemon: system-upgrade API and command by @m-blaha in https://github.com/rpm-software-management/dnf5/pull/1588
 * Enhance docs for `system_cachedir`, `cachedir` and `logdir` by @kontura in https://github.com/rpm-software-management/dnf5/pull/1618
 * Backport countme bucket calculation fix by @kontura in https://github.com/rpm-software-management/dnf5/pull/1613
 * doc: Use ~ instead of /home/$USER by @ppisar in https://github.com/rpm-software-management/dnf5/pull/1619
 * doc: fix arguments for install, upgrade and remove by @kontura in https://github.com/rpm-software-management/dnf5/pull/1621
 * doc: Naming of source and debug repos by @pkratoch in https://github.com/rpm-software-management/dnf5/pull/1627
 * Use correct path when destdir option is set by @m-blaha in https://github.com/rpm-software-management/dnf5/pull/1628
 * doc: Revise packages filtering doc section by @m-blaha in https://github.com/rpm-software-management/dnf5/pull/1632
 * spec: fix modularity man page by @kontura in https://github.com/rpm-software-management/dnf5/pull/1639
 * Update toml11-devel usage for 4.0.0 by @kontura in https://github.com/rpm-software-management/dnf5/pull/1625
 * Better error messages for system state loading by @m-blaha in https://github.com/rpm-software-management/dnf5/pull/1623
 * Implement a default user_agent string by @lleyton in https://github.com/rpm-software-management/dnf5/pull/1590
 * [dnf5] Add argument "-c" - alias to "--config" (dnf4 compatibility) by @jrohel in https://github.com/rpm-software-management/dnf5/pull/1650
 * Install `defs.h` include for `libdnf5-cli` by @kontura in https://github.com/rpm-software-management/dnf5/pull/1657
 * Show the output of failed scriptlets to the user by @m-blaha in https://github.com/rpm-software-management/dnf5/pull/1652
 * doc: configuration options update by @kontura in https://github.com/rpm-software-management/dnf5/pull/1648
 * Print diagnostic messages on stderr, not stdout by @evan-goode in https://github.com/rpm-software-management/dnf5/pull/1641
 * daemon: D-Bus API to cancel current transaction by @m-blaha in https://github.com/rpm-software-management/dnf5/pull/1665
 * config-manager: Fix addrepo from-repofile with empty/comment lines by @jrohel in https://github.com/rpm-software-management/dnf5/pull/1671
 * Fix regressions from stderr/stdout changes by @evan-goode in https://github.com/rpm-software-management/dnf5/pull/1677
 * doc: TransactionCallbacks class documentation by @m-blaha in https://github.com/rpm-software-management/dnf5/pull/1670
 * dnfdaemon: Correct D-Bus signal argument type by @mcrha in https://github.com/rpm-software-management/dnf5/pull/1679
 * Release 5.2.6.0 by @github-actions in https://github.com/rpm-software-management/dnf5/pull/1686

## New Contributors
 * @dschwoerer made their first contribution in https://github.com/rpm-software-management/dnf5/pull/1562
 * @dm0- made their first contribution in https://github.com/rpm-software-management/dnf5/pull/1509
 * @lleyton made their first contribution in https://github.com/rpm-software-management/dnf5/pull/1590

 **Full Changelog**: https://github.com/rpm-software-management/dnf5/compare/5.2.5.0...5.2.6.0

* Fri Aug 02 2024 Petr Pisar <ppisar@redhat.com> - 5.2.5.0-2
- Fix a crash when sending e-mail notifications by the automatic plugin
  (bug #2298385)

* Tue Jul 23 2024 Packit <hello@packit.dev> - 5.2.5.0-1
- Support colon in username, use LRO_USERNAME and LRO_PASSWORD by @jrohel in https://github.com/rpm-software-management/dnf5/pull/1560
- Debuginfo-install command by @j-mracek in https://github.com/rpm-software-management/dnf5/pull/1566
- Implement conditional compilation `-DWITH_MODULEMD=OFF` by @kontura in https://github.com/rpm-software-management/dnf5/pull/1521
- Add reports when corresponding debug package is not available by @j-mracek in https://github.com/rpm-software-management/dnf5/pull/1572
- Add history rollback command and transaction merging by @kontura in https://github.com/rpm-software-management/dnf5/pull/1558
- Fix DNF5: Don't trigger filelists download if abs path to local RPM by @jrohel in https://github.com/rpm-software-management/dnf5/pull/1578
- Documentation: ABI: Defining public (exported) symbols by @jrohel in https://github.com/rpm-software-management/dnf5/pull/1576
- dnfdaemon: Support to run transactions offline by @m-blaha in https://github.com/rpm-software-management/dnf5/pull/1543
- TransactionReplay: handle group package types by @kontura in https://github.com/rpm-software-management/dnf5/pull/1569
- Improvements and fixes for storing transactions by @kontura in https://github.com/rpm-software-management/dnf5/pull/1585
- Release 5.2.5.0 by @github-actions in https://github.com/rpm-software-management/dnf5/pull/1591

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 26 2024 Packit <hello@packit.dev> - 5.2.4.0-1
- spec: Fix files and directories ownership by @m-blaha in https://github.com/rpm-software-management/dnf5/pull/1527
- Add --minimal option for check-ugrade command by @j-mracek in https://github.com/rpm-software-management/dnf5/pull/1519
- repolist: Implement JSON output by @jan-kolarik in https://github.com/rpm-software-management/dnf5/pull/1522
- repoinfo: Implement JSON output by @jan-kolarik in https://github.com/rpm-software-management/dnf5/pull/1529
- Move offline from dnf5 to libdnf5 by @m-blaha in https://github.com/rpm-software-management/dnf5/pull/1520
- Add `history undo` command by @kontura in https://github.com/rpm-software-management/dnf5/pull/1452
- Do not export internal symbols in shared object files by @jrohel in https://github.com/rpm-software-management/dnf5/pull/1307
- Build libdnf5 static library, re-enable unit tests that use hidden (private) libdnf5 symbols by @jrohel in https://github.com/rpm-software-management/dnf5/pull/1507
- daemon: Generate transfer_id on server side by @m-blaha in https://github.com/rpm-software-management/dnf5/pull/1517
- Fix: dnf5 builddep plugin: Link with "common" by @jrohel in https://github.com/rpm-software-management/dnf5/pull/1546
- builddep: Add build-dep alias by @jan-kolarik in https://github.com/rpm-software-management/dnf5/pull/1532
- `undo` command man page and translations by @kontura in https://github.com/rpm-software-management/dnf5/pull/1549
- Add JSON output to advisory list by @stewartsmith in https://github.com/rpm-software-management/dnf5/pull/1531
- docs: Update nightly copr repo name by @jan-kolarik in https://github.com/rpm-software-management/dnf5/pull/1551
- [libdnf, actions plugin] Support get/set repositories options, ver 1.1.0 by @jrohel in https://github.com/rpm-software-management/dnf5/pull/1539
- Add `replay` command to replay stored transactions by @kontura in https://github.com/rpm-software-management/dnf5/pull/1536
- Add "Complete!" message after succesfull transaction by @j-mracek in https://github.com/rpm-software-management/dnf5/pull/1553
- Release 5.2.4.0 by @github-actions in https://github.com/rpm-software-management/dnf5/pull/1565

* Wed Jun 12 2024 Jitka Plesnikova <jplesnik@redhat.com> - 5.2.3.0-3
- Perl 5.40 rebuild

* Sun Jun 09 2024 Python Maint <python-maint@redhat.com> - 5.2.3.0-2
- Rebuilt for Python 3.13

* Mon Jun 03 2024 Packit <hello@packit.dev> - 5.2.3.0-1
- Update translations from weblate
- const: Shared constant defining RPM transaction lock file
- main: Implement checking of privileges before executing commands
- exception: Add new exception for user insufficient privileges
- locker: Move to public API
- distro-sync: Add downloadonly option
- commands: Fix using store option
- Enhance warning about RPMs that were not validate by RPM

* Tue May 28 2024 Packit <hello@packit.dev> - 5.2.2.0-1
- Vars::substitute: fix use-out-of-scope leaks
- docs: correct the default for pluginconfpath
- cli: Add skipped packages to the transaction table
- i18n: Improve formatting an error message for multiple streams
- Add/fix documentation for rpm::PackageQuery methods
- i18n: Unwind "No {} to remove for argument: {}"
- `history list`: count also groups and envs in total `Altered`
- Fix typo in translatable string
- [libdnf5] Actions plugin: Add hooks `repos_configured`, `repos_loaded`, `pre/post_add_cmdline_packages`
- Option `--providers-of` doesn't require available repos
- Improve docs regarding the keepcache option and download command
- needs_restarting: Fix invalid reference usage
- download: add `--source` alias for `--srpm`
- automatic: Fix documentation and ship config file
- fix: quote `dnf5-command({})' in command suggestion when plugin not found
- i18n: Unwind "Cannot {} package \"{}\"" message
- base: Add repository to solver problem messages
- conf: New classes for append options
- docs: Document changes to repoinfo and repolist
- dnf5daemon: The buildtime attribute has been added to the package_attrs option

* Mon May 06 2024 Packit <hello@packit.dev> - 5.2.1.0-1
- Update translations from weblate
- bindings: Tests for using struct attributes in Python
- bindings: Add Python attributes for structs
- docs: Fix diff link on the dnf 5.2.0.0 changes page
- docs: Add diff with API changes in dnf5-5.2.0.0
- docs: Add a page about public API changes in dnf 5.2.0.0
- system-upgrade: fix missing \n before transaction test
- system-upgrade: comment to clarify progress bar logic
- system-upgrade: drop [[maybe_unused]] from reboot() arg
- system-upgrade: fix progress bars, set transaction description
- system-upgrade: adapt to new transaction serialization format
- system-upgrade: clean up releasever logic
- system-upgrade: fix poweroff_after
- copr: the dnf5 copr enable sets CoprRepoPart.enabled = true
- Add file search result for repoquery --whatprovides
- doc: Add enviroment variables and clarify options for loading the plugins
- dnfdaemon: Fix Rpm interface introspection file

* Wed Apr 24 2024 Packit <hello@packit.dev> - 5.2.0.0-1
- Update translations from weblate
- [DNF5] `--enable-plugin` and `--disable-pluin`: no match found message
- [DNF5] API: Move Context::libdnf5_plugins_enablement to p_impl
- spec: Add conflict with the former provider of plugin man pages
- spec: Add conflict with the old provider of dnf.conf
- [DNF5] Fix: Remove transaction_store_path from public, add getter/setter
- [libdnf5 API] Base::get_plugins_info
- [libdnf5 plugins] include iplugin.hpp in plugins instead of base.hpp
- repo_sack: Treat all repos with solv_repo created as loaded (RhBug:2275530)
- [DNF5] API: No inline methods in shared_options.hpp
- [DNF5] API: offline::OfflineTransactionState: no inline methods, move cpp
- [DNF5] API: Remove unused and buggy RpmTransactionItem class
- [DNF5] Command: no inline methods
- [DNF5] API: Context: add p_impl, move public vars to p_impl, getters
- API: cli::session: no inline methods and public vars in opts classes
- API: cli::session::Command: no inline methods
- API: add p_impl to cli::session::Session
- API: rpm::TransactionCallbacks: no inline methods
- API: repo::RepoCallbacks: no inline methods
- Prepare for switch of dnf5 in Rawhide
- base: Make get_transaction_history unstable
- Set `group` reason for packages removed by a group removal
- [DNF5] Implement `--enable-plugin` and `--disable-pluin`
- [libdnf5 API] Base::enable_disable_plugins
- spec: Simplify man page files
- Loggers: Fix: Add missing "null_loger.cpp" file
- Loggers API: unify, explicit ctors, non-inline methods, use p_impl
- doc: Review of DNF4 vs DNF5 CLI and configuration changes
- Re-enable clang builds after API changes
- Add `--store` option for storing arbitrary transaction
- libdnf5::Goal: when adding serialized transaction accept local items
- Goal: change `add_serialized_transaction()` to accept path to trans
- Add group/env paths for transaction parsing/serializing
- base::Transaction: during serialization allow specifying paths
- base::Transaction: add `store_comps(...)` method
- repo_sack: add stored_transaction repo and its private API
- repo: add private API `add_xml_comps(path)`
- Generalize logging of `read_group_solvable_from_xml(..)`
- Add `environment_no_groups` to `GoalJobSettings`
- libdnf5 IPlugin: Pass IPluginData instead of Base to constructor
- libdnf5 IPlugin: Use pImpl
- libdnf5 IPlugin: Do not use inline methods
- dnf5 IPlugin: Do not use inline methods on API
- libdnf5 IPlugin: Add argumets description
- libdnf5 plugins: New hooks `pre/post_add_cmdline_packages`
- libdnf5 plugins: New hook `repos_loaded`
- libdnf5 plugins: New hook `repos_configured`
- Base: notify_repos_configured and are_repos_configured methods
- Fix: implicit conversion changes signedness, unused value
- Disable unit tests for Copr dnf5 plugin
- dnfdaemon: Document Polit CheckAuthorization call
- dnfdaemon: Catch timeout during CheckAuthorization
- Not handle compatibility.conf as configuration file
- config: add search (se) and info (if) aliases
- Improve documentation of repo config directories
- Cross reference documentation
- Document Repos and Vars Dirs
- doc: Unify style and move "Files" section
- Document repos configuration overrides
- doc: Remove ":" in titles
- Bump libdnf5/libdnf5-cli so version
- Mark multiple strings for translation
- Set locale for dnf5 run
- spec: Add missing dnf-config-manager.8.gz file
- Generate documentation for ConfigRepo Class
- [Doc] Describe denerating repo cache path
- dnf5daemon: Make availability case insensitive
- dnf5: Drop unneeded severities capitalization
- dnf5: Document --available as default for advisory cmd
- dnf5daemon-client: Drop unneeded severities capitalization
- advisory: filter_severity and filter_type case insensitive
- dnfdaemon: Fix and enhance Advisory interface doc
- Enable import data from DNF4 for systems without state dir
- libdnf5 options: Unify constructors - pass args for storing by value
- dnfdaemon: Missing signal registration
- doc: config manager plugin: wrap too long lines
- doc: document config-manager plugin
- Packit: get version from specfile for copr_builds againts main
- Update tests to use new `load_repos()` API
- Use new load_repos instead of deprecated update_and_load_enabled_repos
- Make `libdnf5::repo::Repo::load()` private
- Deprecate: `update_and_load_enabled_repos`
- RepoSack: add new `load_repos` method
- Move update_and_load_repos and fix_group_missing_xml to Impl
- Prevent loading plugins for unittests
- Respect plugins configuration option for loading plugins
- Add pImpl to `libdnf5::LogRouter`
- Add pImpl to `libdnf5::MemoryBufferLogger`
- Add pImpl to `libdnf5::OptionBinds`
- Add pImpl to `libdnf5::OptionBinds::Item`
- Add pImpl to `libdnf5::Config`
- Add pImpl to `libdnf5::OptionStringList`
- OptionStringList: remove assignment operators and move constructor
- Add pImpl to `libdnf5::OptionBool`
- OptionBool: remove assignment operators and move constructor
- Add pImpl to `libdnf5::OptionNumber`
- Add pImpl to `libdnf5::OptionPath`
- Add pImpl to `libdnf5::OptionString`
- libdnf5::OptionEnum: remove template, add pImpl
- Add pImpl to `libdnf5::Option`
- modules: Report problems with switching module streams
- modules: Report switched module streams
- modules: Add switching module streams as a possible transaction action
- modules: Add replaces and replaced_by to TransactionModule
- Add missing info updates alias, to match list command
- Update `package_info_sections` not to use `scols_table_print_range`
- libdnf-cli: Extract package info printing
- ArgumentParser: use p_impl, no inline methods
- ArgumentParser:PositionalArg: Unit tests: Support repeating of pos arg
- ArgumentParser:PositionalArg: Support repeating of positional argument
- Hide/Remove deprecated `libdnf5::repo::Repo` API
- Remove deprecated members from `/include/libdnf5/logger/factory.hpp`
- Remove deprecated unused function `create_forcearch_option()`
- builddep: Don't escape globs, use expand_globs = false
- builddep: Don't try to expand globs in pkg specs
- libdnf5-cli::output: Use ifaces instead templates. Move code to .cpp files
- Interfaces and adapters
- module::ModuleStatus: Move to separate header file
- comps::PackageType: Move to separate header file
- cmp_naevr: Fix: pass by reference
- modules: Report module solver problems
- Accept SolverProblems for transacion resolve log
- modules: Return problems from the module solver
- modules: Add a method to process module solver problems
- modules: Add a separate set of problem rules for modules
- modules: Store the original module context also in the libsolv solvable
- modules: Internalize modular repositories
- Add pImpl to `libdnf5::repo::RepoCache` and `RepoCacheRemoveStatistics`
- Add pImpl to `libdnf5::repo::RepoQuery`
- Hide deprecated `libdnf5::base::with_config_file_path` into Impl
- Remove deprecated `libdnf5::Base::load_config_from_file`
- Move all `libdnf5::Base` members to pImpl
- Add pImpl to `libdnf5::rpm::Reldep`
- Add pImpl to `libdnf5::rpm::Changelog`
- Add pImpl to `libdnf5::rpm::Nevra`
- Add pImpl to `libdnf5::rpm::Checksum`
- Add pImpl to `libdnf5::rpm::Package`
- Adjust code to new rpm::PackageQuery::filter_* methods after the rebase
- Add a method accepting std::string for filter_repo_id()
- Add a method accepting std::string for filter_location()
- Add a method accepting std::string for filter_file()
- Add a method accepting std::string for filter_supplements()
- Add a method accepting std::string for filter_enhances()
- Add a method accepting std::string for filter_suggests()
- Add a method accepting std::string for filter_recommends()
- Add a method accepting std::string for filter_obsoletes()
- Add a method accepting std::string for filter_conflicts()
- Add a method accepting std::string for filter_requires()
- Add a method accepting std::string for filter_description()
- Add a method accepting std::string for filter_summary()
- Add a method accepting std::string for filter_url()
- Add a method accepting std::string for filter_sourcerpm()
- Add a method accepting std::string for filter_nevra()
- Add a method accepting std::string for filter_evr()
- Add a method accepting std::string for filter_arch()
- Add a method accepting std::string for filter_release()
- Add a method accepting std::string for filter_version()
- Add a method accepting std::string and int for filter_epoch()
- Add a method accepting std::string for filter_name()
- Add a method accepting std::string for filter_provides()
- Extend version to four numbers (5.x.y.z)
- Unify smallest version number name
- cmake: rename PROJECT_VERSION_* to just VERSION_*
- dnf5daemon: Document before_begin / after_complete signals
- dnf5daemon: Signals to wrap rpm transaction execution
- rpm: New callback to wrap whole rpm transaction
- Add pImpl to `libdnf5::module::ModuleProfile`
- Add pImpl to `libdnf5::module::ModuleDependency`
- Add pImpl to `libdnf5::module::Nsvcap`
- Add pImpl to `libdnf5::module::ModuleQuery`
- Add pImpl to `libdnf5::comps::EnvironmentQuery`
- Add pImpl to `libdnf5::comps::GroupQuery`
- Add pImpl to `libdnf5::comps::Environment`
- Add pImpl to `libdnf5::comps::Package`
- Add pImpl to `libdnf5::comps::Group`
- Remove unused `libdnf5::comps::GroupSack`
- Remove unused `libdnf5::comps::EnvironmentSack`
- Remove unused `libdnf5::comps::Comps`
- Add pImpl to `libdnf5::advisory::Advisory`
- Add pImpl to `libdnf5::advisory::AdvisoryReference`
- Add pImpl to `libdnf5::advisory::AdvisoryCollection`
- Add pImpl to `libdnf5::advisory::AdvisoryQuery`
- Add pImpl to `libdnf5::rpm::RpmSignature`
- Add pImpl to `libdnf5::transaction::Transaction`
- Add pImpl to `libdnf5::rpm::KeyInfo`
- Add pImpl to `libdnf5::repo::RepoSack`
- Add pImpl to `libdnf5::base::SolverProblems`
- Add pImpl to `libdnf5::base::LogEvent`
- Add pImpl to `libdnf5::ConfigParser`
- Add pImpl to `libdnf5::Vars`
- Add pImpl to `libdnf5::transaction::TransactionHistory`
- Add pImpl to `libdnf5::transaction::Package`
- Add pImpl to `libdnf5::transaction::CompsGroup`
- Add pImpl to `libdnf5::transaction::CompsEnvironment`
- Add pImpl to `libdnf5::transaction::TransactionItem`
- Remove several not needed imports
- repo: add p_Impl and several needed utility methods
- Repo: remove unused `fresh()` and `timestamp` attribute
- Add pImpl to `ModuleItem` and remove definitions from header
- Add pImpl to `libdnf5::base::transaction_*` classes
- Add p_impl to libdnf5::GoalJobSettings and add getters and setters
- Add p_impl to libdnf5::ResolveSpecSettings and add getters and setters
- dnf5: bash completion: Prefer using "_comp_initialize" with fallback
- dnf5: Bash completion: Switch to `_init_completion`
- Fix `DISTRO_SYNC_ALL` (distro-sync without arguments, system upgrade)
- Support RPMTRANS_FLAG_DEPLOOPS
- Give inline methods hidden visibility by default
- dnfdaemon: Make only internally used funcs static
- dnfdaemon: Enhance Rpm.list() / Rpm.list_fd() documentation
- doc: Add example of Rpm.list_fd usage in Python
- dnf5daemon-client: Repoquery uses new Rpm:list_fd() API
- dnfdaemon: New method list_fd() on Rpm interface
- dnfdaemon: Serialize package object to JSON string
- dnf5daemon: Handler that return data using UNIX_FD
- dnf5daemon: Auxiliary method to write string to fd
- dnf5daemon: Move utils functions into dnfdaemon namespace
- dnf5daemon: get_session() method for D-Bus services
- dnf5daemon-server: Ignore SIGPIPE
- Vars: Add unit tests for API methods
- Vars::unset: API method for removing variable
- dnf5daemon-server/dbus: Install config files into /usr
- Fix: libdnf5-cli::output::action_color: Move implementation to .cpp file
- Fix: Do not use Variable-length arrays (VLAs) in C++ code
- Add a hint to call base.setup() prior loading repositories
- dnf5daemon-client: New switches for group list
- doc: Include comps.Group interface to D-Bus API documentatin
- dnfdaemon: Enhance comps.Group.list() method
- dnf5daemon-client: Fix group.get_installed()
- man: Link dnf5 pages to dnf

* Wed Apr 03 2024 Packit <hello@packit.dev> - 5.1.17-1
- Update translations from weblate
- dnf5daemon: Remove reposdir from allowed config overrides

* Tue Apr 02 2024 Packit <hello@packit.dev> - 5.1.16-1
- Update translations from weblate
- Document system-upgrade aliases
- Improved Bash Completion
- Print command line hints after resolve failure
- Docuent Advisory.list() API usage
- Add NEVRA field to advisory packages in dnf5daemon
- Review and fix missing commands
- Document dnf5daemon advisory
- Document system-upgrade
- system-upgrade: offline status subcommand
- Add aliases `offline-distrosync`, `offline-upgrade`
- Add `system-upgrade --offline` option
- Add `offline`, `system-upgrade` commands

* Mon Mar 18 2024 Petr Pisar <ppisar@redhat.com> - 5.1.15-2
- Do not obsolete dnf-4 in ELN 11

* Fri Mar 15 2024 Packit <hello@packit.dev> - 5.1.15-1
- Update translations from weblate
- Automatically set `upgrade --downloadonly` when `--destdir` is used
- Write warnings to stderr too in config-manager plugin
- Add repoid to generated repository name in config-manager plugin
- Bump sdbus-cpp requirement to 0.9.0
- Document and implement dnf5daemon Rpm interface
- Document and implement dnf5daemon Goal interface
- Document and implement dnf5daemon Repo interface
- Document and implement dnf5daemon Base interface
- Document and implement dnf5daemon Advisory interface
- Document and implement dnf5daemon SessionManager interface
- Add `dnf5daemon repo --enable/--disable` commands
- automatic: Skip network availability check without remote repo
- dnf5daemon: Rpm.list() works with commandline pkgs

* Tue Mar 05 2024 Packit <hello@packit.dev> - 5.1.14-1
- Update translations from weblate
- Make the error to resolve module metadata more descriptive
- Switch off deltarpm support
- Limit number of dnf5daemon simultaneously active sessions
- Make info and list commands case insesitive
- Allow dnf5daemon configuration overrides for root
- Add repoquery.hpp for swig-4.2.1 support

* Tue Feb 20 2024 Packit <hello@packit.dev> - 5.1.13-1
- Release 5.1.13
- build: Adapt to changes in Fedora packaging of bash-completion
- Change location of automatic.conf
- Limit message log to one on dnf5 start
- Implement waiting for network for dnf5 automatic
- Write dnf5 commandline to the log
- Implement dnf5-automatic: Tool for managing automatic upgrades
- Parametrize output stream in transaction table
- Add `download --srpm` option
- Add missing dbus signal registations
- Add new versionlock bindings
- Implement `dnf5 versionlock` command

* Fri Feb 09 2024 Packit <hello@packit.dev> - 5.1.12-1
- Release 5.1.12
- Update translations from weblate
- Drop dnf obsoletion temporarily
- Use regex for tmt plan names
- Add tmt tests identifiers
- PackageQuery: Add `filter_{latest,earliest}_evr_ignore_arch`
- Suggest to use dnf5 command to install dnf5 plugins
- Added arch option to the download command
- CI: Upgrade action/checkout to a version with Node.js 20
- Document explicit nevra remove commands and aliases dropped
- build: Include <unistd.h> for isatty()
- Change user info display on history command to include display name and username
- Revert "Use focusbest: prefer latest deps versions over smaller transactions"
- Fix a warning when building docs.
- modules: Add a test for enabling default modules
- modules: Add a new module stream to test data
- modules: Respect defaults when enabling multiple streams of a module
- modules: Fix TransactionItemType for not found modules
- Build: Require GCC 10.1 for std::in_range<>()
- Add --urlprotocol option to download command
- dnfdaemon: Explicitly specify allowed config overrides
- Disable dnf and dnf5daemon tests
- needs-restarting: get systemd boot time from UnitsLoadStartTimestamp
- doc: Add --destdir option to upgrade command manual
- Move number placeholder to postposition in copr_repo.cpp
- Added url option
- Load protected packages from installroot
- Make protected_packages an append options
- doc: Create a man page for Aliases
- I18N: Annotate literals in advisory command
- Extend filter_release and filter_version tests
- package_query: Fix filter_version with non EQ comparator
- Fix clang format
- Fix code for string deduplication
- Use placeholders to deduplicate strings
- Add __hash__(), __str__(), and __repr__() for Package
- Add __hash__() for Reldep Python binding
- Add __repr__() to python bindings of Reldep
- Define tp_str slot for Reldep Class
- group: Fix using allowerasing option
- Fix misspellings
- I18N: Remove duplicate empty message IDs from catalogs
- I18N: Do not mark empty strings for a translation

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 11 2024 Packit <hello@packit.dev> - 5.1.11-1
- Release 5.1.11
- Update translations from weblate
- Fix `--skip-unavailable` documentation
- Make `cachedir`, `system_cachedir` relative to `installroot`
- Workaround for swig-4.2.0 missing fragment dependency
- Add `repoquery --recursive` option
- Add `repoquery --providers-of=PACKAGE_ATTRIBUTE` option
- Update documentation of repoquery
- Update documentation for remove command behavior
- Limit search pattern for remove command to NEVRAs and files
- Packaging: Require an exact release of libdnf5-cli by dnf5-plugins
- Disable zchunk on RHEL
- Add dnf5.conf man page
- Add RPM package Group attribute to dnf5daemon-server
- Document changes related to caching
- Document caching man page
- Document Global Option `--help-cmd` dropped
- log_event: Correct message for HINT_ICASE

* Thu Jan 04 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 5.1.10-3
- Disable zchunk on RHEL

* Wed Jan 03 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 5.1.10-2
- Rebuild for https://fedoraproject.org/wiki/Changes/Ruby_3.3

* Tue Jan 02 2024 Packit <hello@packit.dev> - 5.1.10-1
- Release 5.1.10
- Document dnf5 plugins
- Document How-to write libdnf5 plugin tutorial
- Document How-to write dnf5 plugin tutorial
- Document Templates for libdnf5 plugin
- Document Templates for dnf5 plugin
- Sort the module info table
- `module info` print hint for active modules
- `module info` print "[a]" for active modules
- Ensure write permission before importing packages
- Change module dependency string to be the same as in dnf4
- `module info`: improve summary and description
- Escape glob characters in pkg specs for `builddep`
- Add `mc` alias for `makecache`
- Implement `logdir`, `log_size` and `log_rotate` config options
- remove redundant "all" in command `check`
- Improve bash completion
- Fix progress bars miss newlines on non-interactive output

* Fri Dec 08 2023 Packit <hello@packit.dev> - 5.1.9-1
- Release 5.1.9
- Update translations from weblate
- Fix builds for RISC-V arch
- Fix architecture autodetection
- Move `am_i_root` function to common library
- Implement `module info` command
- Add user confirmation request if `history store` overwrites a file
- Add `history store` command
- Add API to serialize base::transaction in JSON
- Add API to serialize transaction::transaction in JSON
- Add docs for `provides`
- Implement command `provides`
- Read `copr.vendor.conf` in `/usr/share` first
- Add docs for `check` command
- Implement `check` command
- Expose `utis/fs/file.hpp` and `temp.hpp` on API
- Document dropping of the `skip-broken` for `upgrade`
- Update man pages with missing dependency resolving-related options
- Document `skip-broken` option only for related commands
- Test for adding an empty list to memory file
- Check serialized temporary files memory is non-empty
- Add `microcode_ctl` to needs-restarting's reboot list
- Fix reporting spec matches only source

* Fri Nov 24 2023 Packit <hello@packit.dev> - 5.1.8-1
- Release 5.1.8
- Update translations from weblate
- Don't run infinitely when enabling dependent modules and module is not found
- Always print "[d]" in module list for default streams
- Fix transaction table headers for module operations
- Implement `config-manager addrepo --add-or-replace`
- Implement plugin `config-manager`
- Allow globs in module_spec arguments
- Document needs-restarting plugin
- Add no-op `needs-restarting -r` for DNF 4 compat
- Implement `needs-restarting --services`
- Initial implementation of needs-restarting

* Thu Nov 09 2023 Packit <hello@packit.dev> - 5.1.7-1
- Release 5.1.7
- Actions plugin's actions.conf can set "Enabled" for each action separately
- Actions plugin now supports action options
- Implement `get_reason()` for groups and environments
- Disable the RHSM plugin by default and enable it in the RPM spec
- Add missing docs for `get_advisory_packages_sorted_by_name_arch_evr(bool)`
- Update documentation about maintained coprs
- modules: Test `ModuleProfile::is_default()` method
- modules: Simplify finding whether profile is default in module list
- modules: Fix `ModuleProfile::is_default` method
- modules: Store if profile is default in ModuleProfile object
- Generate docs for undocummented functions so they at least show up
- Add python advisory docs
- Add advisory python API tests
- Enable AdvisoryModule bindings

* Thu Oct 26 2023 Packit <hello@packit.dev> - 5.1.6-1
- Release 5.1.6
- Document aliases for command line arguments
- Don't print missing positional argument error with `--help`
- Improve error handling for missing arguments
- Document `--forcearch` as a global argument
- Make `--forcearch` a global argument
- Avoid reinstalling installonly packages marked for ERASE
- Add `filter_installonly` to PackageQuery
- Implement new argument `--show-new-leaves`
- advisory: document advisory command changes and few clean ups
- Document `--dump-main-config` and `--dump-repo-config`
- Implement new argument `--dump-repo-config`
- Implement new argument `--dump-main-config`
- Show default profiles in `module list`
- Print hint for the `module list` table
- Show information about default streams in `module list`
- Document `module list` options
- Add `enabled` and `disabled` arguments to `module list`
- Add module spec filtering to `module list`
- Add `module list` command
- Document `group upgrade`

* Thu Oct 05 2023 Packit <hello@packit.dev> - 5.1.5-1
- Improved ConfigParser
- Improved docs for `group install` and `group remove`
- Fix man pages deployment
- Update API doc related to keepcache
- Implement `rhsm` (Red Hat Subscription Manager) plugin
- Document `--dump-variables`
- Implement `dnf5 --dump-variables`
- Improve contributing guidelines: don't mention "ready-for-review"
- Allow specifying upper-case tags in `repoquery --queryformat`
- api: Make get_base_arch() public
- Improve input for large epochs that don't fit into `time_t`

* Mon Sep 18 2023 Packit <hello@packit.dev> - 5.1.4-1
- Fix Builds on i386
- Print error if unsupported architecture used
- argument_parser: New error class for invalid value
- Allow obsoletion of protected packages
- Add support for repository configuration in /usr

* Wed Aug 16 2023 Nicola Sella <nsella@redhat.com> 5.1.2-1
- Release 5.1.2
- Print error messages in nested errors
- Implement `dnf5daemon-server` introspection xml for Advisory interface
- Implement `dnf5daemon-client advisory info` command
- Implement `dnf5daemon-client advisory list` command
- Implement `dnf5daemon-server` advisory service
- Improve `dnf5daemon-client --help`
- Enable `--repofrompath` repos by default
- Fix error on creating repo with duplicate id

* Fri Aug 04 2023 Packit <hello@packit.dev> - 5.1.1-1
- Postpone replace of DNF to Fedora 41
- Add a description of `with_binaries` option for dnf5daemon
- Include RPM logs in KeyImportError
- Abort PGP checking immediately if any checks fail
- Display warning message when any PGP checks skipped
- Don't allow main gpgcheck=0 to override repo config
- gups and environments to `history info` ouput
- Store missing id and repoid in db for groups/environments
- Fix out-of-bounds access in Goal::Impl::add_install_to_goal
- Fix repoquery `--list`
- `allow_vendor_change` was reverted back to true
- Doc update to allow `logdir` outside the installroot
- Remove `grouplist` and `groupinfo` aliases
- Add `grp` alias for group command
- `repoquery --exactdeps` needs `--whatdepends` or `--whatrequires`
- Update and unify repoquery manpage
- Document replace of `-v` option by `repoinfo` command
- Add `remove --no-autoremove` option
- Document dropped `if` alias of `info` command
- document `actions` plugin
- Fix printing advisories for the running kernel
- Revert "advisory: add running kernel before pkg_specs filtering"

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 18 2023 Packit <hello@packit.dev> - 5.1.0-1
- Minor version update. API is considered stable
- Remove unneeded unused configuration priority
- Don't show dnf5-command hint for unknown options, only commands
- Add hint to install missing command with dnf5-command(<name>)
- Add dnf5-command(<command-name>) provides to dnf5
- Add dnf5-command(<command-name>) provides to dnf5-plugins
- Document several methods as deprecated
- Fix core dump on `--refresh` switch usage
- Add `repoquery -l`/`--list` aliases for `--files` for rpm compat
- Add `vendor` attr to package in `dnfdaemon-server`
- Document `dnf5-plugins` package in man pages

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 5.0.15-4
- Perl 5.38 rebuild

* Sat Jul 01 2023 Python Maint <python-maint@redhat.com> - 5.0.15-3
- Rebuilt for Python 3.12

* Fri Jun 30 2023 Adam Williamson <awilliam@redhat.com> - 5.0.15-2
- Rebuild for fmt 10 again

* Thu Jun 29 2023 Packit <hello@packit.dev> - 5.0.15-1
- Add `module enable` subcommand
- Add `--repofrompath` option
- Add `--forcearch` option to multiple commands
- Add `reinstall --allowerasing` option
- Add `repoquery --sourcerpm` option
- Add `repoquery --srpm` option
- Add `chacheonly` configuration option
- Add `--cacheonly` option
- Add `--refresh` option
- Change default value for `best` configuration to true
- Change default value for `allow_vendor_change` configuration to false
- changelog: Fix behavior of `--since` option
- builddep: Fix handling BuildRequires in spec files
- swig: Return None for unset options in Python
- Verify transaction PGP signatures automatically
- Fix checking whether updateinfo metadata are required
- Fix handling empty epoch when comparing nevra
- Fix building with upcoming fmt-10 library
- Rename namespace, includes and directories from libdnf to libdnf5
- Provide /var/cache/libdnf5 instead of /var/cache/libdnf (RhBug:2216849)

* Wed Jun 28 2023 Vitaly Zaitsev <vitaly@easycoding.org> - 5.0.14-2
- Rebuilt due to fmt 10 update.
- Added upstream patches with fmt 10 build fixes.

* Wed Jun 14 2023 Packit <hello@packit.dev> - 5.0.14-1
- Modify libdnf5-devel to generate pkgconf(libdnf5)
- Handle unnamed environments in transaction table
- Return error exit code on RPM transaction failure
- Add `repoquery --file` option
- Add `repoquery --arch` option
- Add `repoquery --installonly` option
- Add `repoquery --extras`, `--upgrades` and `--recent` options
- Add `repoquery --changelogs` formatting option
- Don't complete ls alias
- Add rq command alias for `repoquery`
- Exclude dnf.conf when not installed
- Improve the download methods API
  - Switch to parameterless download methods and introduce setters for fail_fast and resume
  - Affected classes: libdnf::repo::FileDownloader, libdnf::repo::PackageDownloader

* Tue May 30 2023 Packit <nsella@redhat.com> - 5.0.13-2
- Update specfile to exclude dnf.conf for fedora < 39

* Mon May 29 2023 Packit <hello@packit.dev> - 5.0.13-1
- Release 5.0.13
- Fix resolve behavior for `download`
- Add a message when `--downloadonly` is used
- Add `--downloadonly` option to multiple commands

* Thu May 25 2023 Nicola Sella <nsella@redhat.com> - 5.0.12-1
- Release 5.0.12
- Have DNF update to DNF5
- Add dnf, yum obsoletes and provides
- Symlinks for `dnf` and `yum` binaries
- Move ownership of /etc/dnf/dnf.conf, /etc/dnf/vars, and /etc/dnf/protected.d from dnf-data to libdnf5
- Conflict with older versions of dnf-data that own these files/directories
- Print environments in the transaction table
- Add support for environmantal groups in dnf5daemon
- Handle unnamed groups in transaction table
- Update documentation for `distro-sync --skip-unavailable`
- Update documentation for `downgrade --skip-unavailable`
- Update documentation for `upgrade --skip-unavailable`
- Add repoquery `--files` and `files` querytag instead of `--list`
- Add getters to package for: debug, source, repo-name
- Add `repoquery --querytags` option
- Document `repoquery --queryformat`
- Add `repoquery --qf` alias to `repoquery --queryformat`
- Add get_depends() to package and --depends to repoquery
- Implement keepcache functionality (RhBug:2176384)
- API changes:
- libdnf::repo::PackageDownloader default ctor dropped (now accepting the Base object)
- libdnf::base::Transaction not accepting dest_dir anymore (implicitly taken from configuration)
- A note for existing users:
- Regardless of the keepcache option, all downloaded packages have been cached up until now.
- Starting from now, downloaded packages will be kept only until the next successful transaction (keepcache=False by default).
- To remove all existing packages from the cache, use the `dnf5 clean packages` command.
- goal: Split group specs resolution to separate method
- comps: Possibility to create an empty EnvironmentQuery
- `remove` command accepts `remove spec`
- Refactor remove positional arguments
- Remove duplicates from `group list` output
- Document `copr` plugin command
- Document `builddep` plugin command

* Fri May 19 2023 Petr Pisar <ppisar@redhat.com> - 5.0.11-3
- Rebuild against rpm-4.19 (https://fedoraproject.org/wiki/Changes/RPM-4.19)

* Fri May 19 2023 Nicola Sella <nsella@redhat.com> - 5.0.11-2
- Fix builds for arch non x86_64

* Thu May 18 2023 Packit <hello@packit.dev> - 5.0.11-1
- Release 5.0.11
- Add --contains-pkgs option to group info
- Add filter for containing package names
- Fix parameter names in documentation
- Document create parameter of RelDep::get_id method
- Document RepoQuery::filter_local
- Document repoclosure in man pages
- Document repoclosure command
- Implement repoclosure plugin
- package_query: filter_provides accepts also Reldep
- Fix download callbacks and many segfaults in dnf5daemon
- Add allow-downgrade configuration option
- Release 5.0.10
- dnf5-plugins: implement 'dnf5 copr'
- Add new configuration option exclude_from_weak_autodetect
- Add new config option exclude_from_weak
- Add repoquery --unneeded
- Fix handling of incorrect argument (RhBug:2192854)
- Add detect_release to public API
- Add group --no-packages option
- Add group upgrade command
- Enable group upgrades in transaction table
- Add --destdir option to download command
- Filter latest per argument for download command
- Add builddep --allowerasing
- download command: filter by priority, latest
- Remove --unneeded option from remove command
- Document autoremove differences from dnf4
- Add autoremove command
- state: Add package_types attribute to GroupState
- comps: Add conversion of PackageType to string(s)
- Add check-update alias for check-upgrade
- Add `check-upgrade --changelogs`

* Tue May 02 2023 Richard W.M. Jones <rjones@redhat.com> - 5.0.9-3
- Default tests off (temporarily, hopefully) on riscv64 arch.

* Wed Apr 26 2023 Nicola Sella <nsella@redhat.com> - 5.0.9-2
- Release 5.0.9 (Nicola Sella)
- Add `--userinstalled` to `repoquery` man page
- Implement `repoquery -userinstalled`
- Fix: progressbar: Prevent length_error exception (RhBug:2184271)
- Add dnf5-plugins directory in documentation
- Document `repoquery --leaves`
- Implement `repoquery --leaves`
- Implement new filters rpm::filter_leaves and rpm::filter_leaves_groups

* Thu Apr 13 2023 Nicola Sella <nsella@redhat.com> - 5.0.8-1
- Update to 5.0.8
- Improve error message in download command
- Add repoquery --latest-limit option
- Add dg, in, rei, rm aliases
- Add "up" and "update" aliases for "upgrade" command
- Update documentation with info about package spec expressions (RhBug:2160420)
- Add formatting options repoquery --requires, --provides..
- Remove unused repoquery nevra option
- Add `--queryformat` option to repoquery
- Improved progress bars
- Fix logic of installroot with deduplication
- Correctly load repos from installroot config file
- Improved loading and downloading of key files
- Improved modules: Change State to set and get the whole ModuleState
- New API method rpm::Package::is_available_locally
- Move description of DNF5 changes to doc
- Improved dnf5daemon logic and removed unused code
- Improved progress bar
- Improved handling of obsolete package installation
- Remove showdupesfromrepos config option
- man: Add info about download command destination
- Print resolve logs to stderr
- Fix double loading of system repo in dnf5daemon
- Set a minimal sqlite version
- Change to --use-host-config, warning suggesting --use-host-config
- Add capability to find binaries to resolve_spec
- Add pre-commit file
- Improved by fixing memory leaks
- Improved tests by enabling with multithreading
- Improve documentation  for list command
- Add compatibility alias ls->list
- Implement info command
- Implement list command
- Fix --exactdeps argument description

* Wed Mar 8 2023 Nicola Sella <nsella@redhat.com> - 5.0.7-1
- Document set/get vars in python api
- Document --strict deprecation
- New configuration option "disable_multithreading"
- Improved dnf5daemon to handle support groups and modules in return value
- Ignore inaccessible config unless path specified as --config=...
- Includes reordering and tweaks in advisories
- Add support for package changelogs in swig and tests
- Add many unit tests for dnf5 and python api
- Add new --skip-unavailable command line option
- Add search command
- Add new error for incorrect API usages
- Add a new method whether base was correctly initialized
- Improved python exceptions on undefined var
- transaction: Change API to run transaction without args
- Add explicit package version for libdnf5-cli
- Improved performance of packagequery

* Tue Feb 14 2023 Nicola Sella <nsella@redhat.com> - 5.0.6-1
- Add obsoletes of microdnf
- Many improvements related to internal logic and bugfixes
- Improvements in specfile
- Improved API, drop std::optional
- Use Autoapi instead of Autodoc to generate Python docs
- Improved documentation for modules

* Thu Jan 26 2023 Nicola Sella <nsella@redhat.com> - 5.0.5-1
- Fix build fail in rawhide
- Fixes in the concerning filesystem
- Fixes in the concerning modules
- Fixes in the concerning api

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan 18 2023 Nicola Sella <nsella@redhat.com> - 5.0.4-2
- Backport downstream patch to disable unit tests for python tutorials
- Fix build in rawhide

* Thu Jan 12 2023 Nicola Sella <nsella@redhat.com> - 5.0.4-1
- Many fixes in perl bindings
- Test functions enhanced
- Extend unit tests for OptionString and OptionStringList

* Wed Jan 04 2023 Nicola Sella <nsella@redhat.com> - 5.0.3-1
- Add Python docs for: Base, Goal, RepoQuery, Package and PackageQuery
- Add docs for Python bindings: they are auto generated now
- Add --what* and --exactdeps options to repoquery
- Add "user enter password" to dnf5daemon functionalities
- Fix: remove repeating headers in transaction table
- Fix: Set status of download progress bar after successful download
- Fix: RepoDownloader::get_cache_handle: Don't set callbacks in LibrepoHandle
- Refactor internal utils
- Improved GlobalLogger
- Improved C++ API docs

* Thu Dec 08 2022 Nicola Sella <nsella@redhat.com> - 5.0.2-1
- Implement group remove command
- Improved options in config
- Add support for any number of user IDs in a PGP key
- Use new librepo PGP API
- remove gpgme dependency
- Improved exceptions and dnf5 errors
- Add dnf5-devel package
- Update README.md with up to date information
- Repoquery: Add --duplicates option
- Improved documentation for Repoquery, Upgrande and About section
- Add tutorials for python3 bindings
- dnf5-changes-doc: Add more structure using different headings
- Add ModuleQuery
- Improvements in comps logic

* Fri Nov 25 2022 Nicola Sella <nsella@rehat.com> - 5.0.1-1
- Update to 5.0.1
- Fix loading known keys for RepoGpgme
- Fix dnf5 progress_bar
- Improve modules: conflicting packages, weak resolve, active modules resolving
- plugins.hpp moved away from public headers and improvements logic
- Fix failing builds for i686 arch
- Add man pages to dnf5
- Fix non x86_64 builds
- Remove unimplemented commands

* Wed Nov 2 2022 Nicola Sella <nsella@redhat.com> - 5.0.0-2~pre
- Fix failing builds for i686 arch

* Mon Oct 31 2022 Nicola Sella <nsella@redhat.com> - 5.0.0-1~pre
- Add man pages to dnf5
- Fix non x86_64 builds
- Remove unimplemented commands

* Fri Sep 16 2022 Nicola Sella - <nsella@redhat.com> - 5.0.0-0~pre
- Dnf pre release build for Fedora
