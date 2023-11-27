%global project_version_major 5
%global project_version_minor 0
%global project_version_patch 14
# ========== versions of dependencies ==========
%global libmodulemd_version 2.5.0
%global librepo_version 1.15.0
%global libsolv_version 0.7.21
%global sqlite_version 3.35.0
# ========== build options ==========
%bcond_without libdnf_cli
%bcond_without dnf5
%bcond_without dnf5_plugins
%bcond_without plugin_actions
%if %{with clang}
    %global toolchain clang
%endif
Summary:        Command-line package manager
Name:           dnf5-bootstrap
Version:        %{project_version_major}.%{project_version_minor}.%{project_version_patch}
Release:        1%{?dist}
License:        GPL-2.0-or-later
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/rpm-software-management/dnf5
Source0:        %{url}/archive/%{version}/dnf5-%{version}.tar.gz
Patch0:         0001-add-WITH_MODULEMD-patch.patch
# ========== build requires ==========
BuildRequires:  bash-completion
BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  gettext
BuildRequires:  pkg-config
BuildRequires:  toml11-devel
BuildRequires:  pkgconfig(check)
BuildRequires:  pkgconfig(fmt)
BuildRequires:  pkgconfig(json-c)
BuildRequires:  pkgconfig(libcrypto)
BuildRequires:  pkgconfig(librepo) >= %{librepo_version}
BuildRequires:  pkgconfig(libsolv) >= %{libsolv_version}
BuildRequires:  pkgconfig(libsolvext) >= %{libsolv_version}
BuildRequires:  pkgconfig(rpm) >= 4.17.0
BuildRequires:  pkgconfig(sqlite3) >= %{sqlite_version}
Requires:       libdnf5%{?_isa} = %{version}-%{release}
Requires:       libdnf5-cli%{?_isa} = %{version}-%{release}
Recommends:     bash-completion
%if %{with clang}
BuildRequires:  clang
%else
BuildRequires:  gcc-c++
%endif
%if %{with libdnf_cli}
# required for libdnf5-cli
BuildRequires:  pkgconfig(smartcols)
%endif

%description
DNF5 is a command-line package manager that automates the process of installing,
upgrading, configuring, and removing computer programs in a consistent manner.
It supports RPM packages, modulemd modules, and comps groups & environments.

%files
%{_bindir}/dnf5

%dir %{_sysconfdir}/dnf/dnf5-aliases.d
%doc %{_sysconfdir}/dnf/dnf5-aliases.d/README
%dir %{_datadir}/dnf5
%dir %{_datadir}/dnf5/aliases.d
%config %{_datadir}/dnf5/aliases.d/compatibility.conf
%dir %{_libdir}/dnf5
%dir %{_libdir}/dnf5/plugins
%doc %{_libdir}/dnf5/plugins/README
%dir %{_libdir}/libdnf5/plugins
%dir %{_datadir}/bash-completion/
%dir %{_datadir}/bash-completion/completions/
%{_datadir}/bash-completion/completions/dnf5
%dir %{_libdir}/sysimage/dnf
%verify(not md5 size mtime) %ghost %{_libdir}/sysimage/dnf/*
%license COPYING.md
%license gpl-2.0.txt

# ========== libdnf5 ==========
%package -n libdnf5-bootstrap
Summary:        Package management library
License:        LGPL-2.1-or-later
Requires:       librepo%{?_isa} >= %{librepo_version}
Requires:       libsolv%{?_isa} >= %{libsolv_version}
Requires:       sqlite-libs%{?_isa} >= %{sqlite_version}

%description -n libdnf5-bootstrap
Package management library.

%files -n libdnf5-bootstrap
%exclude %{_sysconfdir}/dnf/dnf.conf
%dir %{_libdir}/libdnf5
%{_libdir}/libdnf5.so.1*
%license lgpl-2.1.txt
%{_var}/cache/libdnf/

# ========== libdnf5-cli ==========

%if %{with libdnf_cli}
%package -n libdnf5-bootstrap-cli
Summary:        Library for working with a terminal in a command-line package manager
License:        LGPL-2.1-or-later
Requires:       libdnf5%{?_isa} = %{version}-%{release}

%description -n libdnf5-bootstrap-cli
Library for working with a terminal in a command-line package manager.

%files -n libdnf5-bootstrap-cli
%{_libdir}/libdnf-cli.so.1*
%license COPYING.md
%license lgpl-2.1.txt
%endif

# ========== dnf5-devel ==========

%package -n dnf5-bootstrap-devel
Summary:        Development files for dnf5
License:        LGPL-2.1-or-later
Requires:       dnf5-bootstrap%{?_isa} = %{version}-%{release}
Requires:       libdnf5-bootstrap-cli-devel%{?_isa} = %{version}-%{release}
Requires:       libdnf5-bootstrap-devel%{?_isa} = %{version}-%{release}

%description -n dnf5-bootstrap-devel
Develpment files for dnf5.

%files -n dnf5-bootstrap-devel
%{_includedir}/dnf5/
%license COPYING.md
%license lgpl-2.1.txt

# ========== libdnf5-devel ==========

%package -n libdnf5-bootstrap-devel
Summary:        Development files for libdnf
License:        LGPL-2.1-or-later
Requires:       libdnf5-bootstrap%{?_isa} = %{version}-%{release}
Requires:       libsolv-devel%{?_isa} >= %{libsolv_version}

%description -n libdnf5-bootstrap-devel
Development files for libdnf.

%files -n libdnf5-bootstrap-devel
%{_includedir}/libdnf/
%dir %{_libdir}/libdnf5
%{_libdir}/libdnf5.so
%{_libdir}/pkgconfig/libdnf5.pc
%license COPYING.md
%license lgpl-2.1.txt

# ========== libdnf5-cli-devel ==========

%package -n libdnf5-bootstrap-cli-devel
Summary:        Development files for libdnf5-cli
License:        LGPL-2.1-or-later
Requires:       libdnf5-bootstrap-cli%{?_isa} = %{version}-%{release}

%description -n libdnf5-bootstrap-cli-devel
Development files for libdnf5-cli.

%files -n libdnf5-bootstrap-cli-devel
%{_includedir}/libdnf-cli/
%{_libdir}/libdnf-cli.so
%{_libdir}/pkgconfig/libdnf-cli.pc
%license COPYING.md
%license lgpl-2.1.txt

# ========== libdnf5-plugin-actions ==========

%if %{with plugin_actions}
%package -n libdnf5-bootstrap-plugin-actions
Summary:        Libdnf plugin that allows to run actions (external executables) on hooks
License:        LGPL-2.1-or-later
Requires:       libdnf5-bootstrap%{?_isa} = %{version}-%{release}

%description -n libdnf5-bootstrap-plugin-actions
Libdnf plugin that allows to run actions (external executables) on hooks.

%files -n libdnf5-bootstrap-plugin-actions
%{_libdir}/libdnf5/plugins/actions.*
%endif

# ========== dnf5-plugins ==========

%if %{with dnf5_plugins}
%package -n dnf5-bootstrap-plugins
Summary:        Plugins for dnf5
License:        LGPL-2.1-or-later
Requires:       dnf5%{?_isa} = %{version}-%{release}

%description -n dnf5-bootstrap-plugins
Core DNF5 plugins that enhance dnf5 with builddep, changelog, copr, and repoclosure commands.

%files -n dnf5-bootstrap-plugins
%{_libdir}/dnf5/plugins/*.so
%if %{with man}
%{_mandir}/man8/dnf5-builddep.8.*
%{_mandir}/man8/dnf5-copr.8.*
%{_mandir}/man8/dnf5-repoclosure.8.*
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
    -DWITH_DNF5DAEMON_CLIENT=OFF \
    -DWITH_DNF5DAEMON_SERVER=OFF \
    -DWITH_LIBDNF5_CLI=%{?with_libdnf_cli:ON}%{!?with_libdnf_cli:OFF} \
    -DWITH_DNF5=%{?with_dnf5:ON}%{!?with_dnf5:OFF} \
    -DWITH_PLUGIN_ACTIONS=%{?with_plugin_actions:ON}%{!?with_plugin_actions:OFF} \
    -DWITH_PYTHON_PLUGINS_LOADER=OFF \
    \
    -DWITH_COMPS=OFF \
    -DWITH_MODULEMD=OFF \
    -DWITH_ZCHUNK=OFF \
    \
    -DWITH_HTML=OFF \
    -DWITH_MAN=OFF \
    \
    -DWITH_GO=OFF \
    -DWITH_PERL5=OFF \
    -DWITH_PYTHON3=OFF \
    -DWITH_RUBY=OFF \
    \
    -DWITH_SANITIZERS=OFF \
    -DWITH_TESTS=OFF \
    -DWITH_PERFORMANCE_TESTS=OFF \
    -DWITH_DNF5DAEMON_TESTS=OFF \
    \
    -DPROJECT_VERSION_MAJOR=%{project_version_major} \
    -DPROJECT_VERSION_MINOR=%{project_version_minor} \
    -DPROJECT_VERSION_PATCH=%{project_version_patch}
%cmake_build


%install
%cmake_install


# own dirs and files that dnf5 creates on runtime
mkdir -p %{buildroot}%{_libdir}/sysimage/dnf
for files in \
    groups.toml modules.toml nevras.toml packages.toml \
    system.toml transaction_history.sqlite \
    transaction_history.sqlite-shm \
    transaction_history.sqlite-wal userinstalled.toml
do
    touch %{buildroot}%{_libdir}/sysimage/dnf/$files
done

#find_lang {name}

%ldconfig_scriptlets


%changelog
* Wed Jun 21 2023 Sam Meluch <sammeluch@microsoft.com> - 5.0.14-1
- Strip spec file of language binding packages, man pages, html docs
- update spec file for Mariner
- License Verified
- Initial CBL-Mariner import from RPM software management source (license: GPLv2+)

* Wed Jun 14 2023 Packit Team <hello@packit.dev> - 5.0.14-1
- New upstream release 5.0.14

* Mon May 29 2023 Packit Team <hello@packit.dev> - 5.0.13-1
- New upstream release 5.0.13

* Thu May 25 2023 Packit Team <hello@packit.dev> - 5.0.12-1
- New upstream release 5.0.12

* Thu May 18 2023 Packit Team <hello@packit.dev> - 5.0.11-1
- New upstream release 5.0.11

* Tue May 09 2023 Packit Team <hello@packit.dev> - 5.0.10-1
- New upstream release 5.0.10

* Tue Apr 18 2023 Nicola Sella <nsella@redhat.com> - 5.0.9-1
- New upstream release 5.0.9

* Thu Apr 13 2023 Nicola Sella <nsella@redhat.com> - 5.0.8-1
- New upstream release 5.0.8

* Wed Mar 8 2023 Nicola Sella <nsella@redhat.com> - 5.0.7-1
- New upstream release 5.0.7

* Tue Feb 14 2023 Nicola Sella <nsella@redhat.com> - 5.0.6-1
- New upstream release 5.0.6

* Thu Jan 26 2023 Nicola Sella <nsella@redhat.com> - 5.0.5-1
- New upstream release 5.0.5

* Thu Jan 12 2023 Nicola Sella <nsella@redhat.com> - 5.0.4-1
- New upstream release 5.0.4

* Wed Jan 04 2023 Nicola Sella <nsella@redhat.com> - 5.0.3-1
- New upstream release 5.0.3

* Thu Dec 08 2022 Nicola Sella <nsella@redhat.com> - 5.0.2-1
- New upstream release 5.0.2

* Thu Nov 24 2022 Nicola Sella <nsella@redhat.com> - 5.0.1-1
- New upstream release 5.0.1

* Wed Nov 2 2022 Nicola Sella <nsella@redhat.com> - 5.0.0-2~pre
- New upstream pre release 5.0.0

* Mon Oct 31 2022 Nicola Sella <nsella@redhat.com> - 5.0.0-1~pre
- New upstream pre release 5.0.0

* Fri Sep 16 2022 Nicola Sella - <nsella@redhat.com> - 5.0.0-0~pre
- New upstream pre release 5.0.0
