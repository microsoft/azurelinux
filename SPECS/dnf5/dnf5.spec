%global project_version_major 5
%global project_version_minor 0
%global project_version_patch 14
# ========== versions of dependencies ==========
%global libmodulemd_version 2.5.0
%global librepo_version 1.15.0
%global libsolv_version 0.7.21
%global sqlite_version 3.35.0
%global swig_version 4
%global zchunk_version 0.9.11
# ========== build options ==========
%bcond_with dnf5daemon_client
%bcond_with dnf5daemon_server
%bcond_without libdnf_cli
%bcond_without dnf5
%bcond_without dnf5_plugins
%bcond_without plugin_actions
%bcond_without python_plugins_loader
%bcond_without comps
%bcond_with modulemd
%bcond_without zchunk
%bcond_with    html
%bcond_with    man
# TODO Go bindings fail to build, disable for now
%bcond_with    go
%bcond_with    perl5
%bcond_without python3
%bcond_with    ruby
%bcond_with    clang
%bcond_with    sanitizers
%bcond_without tests
%bcond_with    performance_tests
%bcond_with    dnf5daemon_tests
%if %{with clang}
    %global toolchain clang
%endif
Summary:        Command-line package manager
Name:           dnf5
Version:        %{project_version_major}.%{project_version_minor}.%{project_version_patch}
Release:        3%{?dist}
License:        GPL-2.0-or-later
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/rpm-software-management/dnf5
Source0:        %{url}/archive/%{version}/dnf5-%{version}.tar.gz
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
%if %{with tests}
BuildRequires:  createrepo_c
BuildRequires:  rpm-build
BuildRequires:  pkgconfig(cppunit)
%endif
%if %{with comps}
BuildRequires:  pkgconfig(libcomps)
%endif
#%if %{with modulemd}
#BuildRequires:  pkgconfig(modulemd-2.0) >= %{libmodulemd_version}
#%endif
%if %{with zchunk}
BuildRequires:  pkgconfig(zck) >= %{zchunk_version}
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
%if %{with dnf5daemon_server}
BuildRequires:  systemd-rpm-macros
# required for dnf5daemon-server
BuildRequires:  pkgconfig(sdbus-c++) >= 0.8.1
%if %{with dnf5daemon_tests}
BuildRequires:  dbus-daemon
BuildRequires:  polkit
BuildRequires:  python3-devel
BuildRequires:  python3dist(dbus-python)
%endif
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
BuildRequires:  perl(Test::Exception)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
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

%if %{with man}
%{_mandir}/man8/dnf5.8.*
%{_mandir}/man8/dnf5-advisory.8.*
%{_mandir}/man8/dnf5-autoremove.8.*
%{_mandir}/man8/dnf5-clean.8.*
%{_mandir}/man8/dnf5-distro-sync.8.*
%{_mandir}/man8/dnf5-downgrade.8.*
%{_mandir}/man8/dnf5-download.8.*
%{_mandir}/man8/dnf5-environment.8.*
%{_mandir}/man8/dnf5-group.8.*
# TODO(jkolarik): history is not ready yet
# %%{_mandir}/man8/dnf5-history.8.*
%{_mandir}/man8/dnf5-install.8.*
%{_mandir}/man8/dnf5-leaves.8.*
%{_mandir}/man8/dnf5-makecache.8.*
%{_mandir}/man8/dnf5-mark.8.*
# TODO(jkolarik): module is not ready yet
# %%{_mandir}/man8/dnf5-module.8.*
%{_mandir}/man8/dnf5-reinstall.8.*
%{_mandir}/man8/dnf5-remove.8.*
%{_mandir}/man8/dnf5-repo.8.*
%{_mandir}/man8/dnf5-repoquery.8.*
%{_mandir}/man8/dnf5-search.8.*
%{_mandir}/man8/dnf5-swap.8.*
%{_mandir}/man8/dnf5-upgrade.8.*
%{_mandir}/man7/dnf5-comps.7.*
# TODO(jkolarik): filtering is not ready yet
# %%{_mandir}/man7/dnf5-filtering.7.*
%{_mandir}/man7/dnf5-installroot.7.*
# TODO(jkolarik): modularity is not ready yet
# %%{_mandir}/man7/dnf5-modularity.7.*
%{_mandir}/man7/dnf5-specs.7.*
%endif

# ========== libdnf5 ==========
%package -n libdnf5
Summary:        Package management library
License:        LGPL-2.1-or-later
Requires:       librepo%{?_isa} >= %{librepo_version}
#Requires:       libmodulemd{?_isa} >= {libmodulemd_version}
Requires:       libsolv%{?_isa} >= %{libsolv_version}
Requires:       sqlite-libs%{?_isa} >= %{sqlite_version}

%description -n libdnf5
Package management library.

%files -n libdnf5
%exclude %{_sysconfdir}/dnf/dnf.conf
%dir %{_libdir}/libdnf5
%{_libdir}/libdnf5.so.1*
%license lgpl-2.1.txt
%{_var}/cache/libdnf/

# ========== libdnf5-cli ==========

%if %{with libdnf_cli}
%package -n libdnf5-cli
Summary:        Library for working with a terminal in a command-line package manager
License:        LGPL-2.1-or-later
Requires:       libdnf5%{?_isa} = %{version}-%{release}

%description -n libdnf5-cli
Library for working with a terminal in a command-line package manager.

%files -n libdnf5-cli
%{_libdir}/libdnf-cli.so.1*
%license COPYING.md
%license lgpl-2.1.txt
%endif

# ========== dnf5-devel ==========

%package -n dnf5-devel
Summary:        Development files for dnf5
License:        LGPL-2.1-or-later
Requires:       dnf5%{?_isa} = %{version}-%{release}
Requires:       libdnf5-cli-devel%{?_isa} = %{version}-%{release}
Requires:       libdnf5-devel%{?_isa} = %{version}-%{release}

%description -n dnf5-devel
Develpment files for dnf5.

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
%{_includedir}/libdnf/
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
%{_includedir}/libdnf-cli/
%{_libdir}/libdnf-cli.so
%{_libdir}/pkgconfig/libdnf-cli.pc
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
%{?python_provide:%python_provide python3-libdnf}
Summary:        Python 3 bindings for the libdnf library
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
%{?python_provide:%python_provide python3-libdnf5-cli}
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
Requires:       libdnf5%{?_isa} = %{version}-%{release}
Requires:       ruby(release)
Provides:       ruby(libdnf) = %{version}-%{release}

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
Requires:       libdnf5-cli%{?_isa} = %{version}-%{release}
Requires:       ruby(release)
Provides:       ruby(libdnf_cli) = %{version}-%{release}

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
Summary:        Libdnf plugin that allows to run actions (external executables) on hooks
License:        LGPL-2.1-or-later
Requires:       libdnf5%{?_isa} = %{version}-%{release}

%description -n libdnf5-plugin-actions
Libdnf plugin that allows to run actions (external executables) on hooks.

%files -n libdnf5-plugin-actions
%{_libdir}/libdnf5/plugins/actions.*
%endif


# ========== python3-libdnf5-plugins-loader ==========

%if %{with python_plugins_loader}
%package -n python3-libdnf5-python-plugins-loader
Summary:        Libdnf plugin that allows loading Python plugins
License:        LGPL-2.1-or-later
Requires:       libdnf5%{?_isa} = %{version}-%{release}
Requires:       python3-libdnf5%{?_isa} = %{version}-%{release}

%description -n python3-libdnf5-python-plugins-loader
Libdnf plugin that allows loading Python plugins.

%files -n python3-libdnf5-python-plugins-loader
%{_libdir}/libdnf5/plugins/python_plugins_loader.*
%dir %{python3_sitelib}/libdnf_plugins/
%doc %{python3_sitelib}/libdnf_plugins/README
%endif


# ========== dnf5daemon-client ==========

%if %{with dnf5daemon_client}
%package -n dnf5daemon-client
Summary:        Command-line interface for dnf5daemon-server
License:        GPL-2.0-or-later
Requires:       dnf5daemon-server
Requires:       libdnf5%{?_isa} = %{version}-%{release}
Requires:       libdnf5-cli%{?_isa} = %{version}-%{release}

%description -n dnf5daemon-client
Command-line interface for dnf5daemon-server.

%files -n dnf5daemon-client
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
Requires:       dbus
Requires:       libdnf5%{?_isa} = %{version}-%{release}
Requires:       libdnf5-cli%{?_isa} = %{version}-%{release}
Requires:       polkit

%description -n dnf5daemon-server
Package management service with a DBus interface.

%post -n dnf5daemon-server
%systemd_post dnf5daemon-server.service

%preun -n dnf5daemon-server
%systemd_preun dnf5daemon-server.service

%postun -n dnf5daemon-server
%systemd_postun_with_restart dnf5daemon-server.service

%files -n dnf5daemon-server
%{_sbindir}/dnf5daemon-server
%{_unitdir}/dnf5daemon-server.service
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.rpm.dnf.v0.conf
%{_datadir}/dbus-1/system-services/org.rpm.dnf.v0.service
%{_datadir}/dbus-1/interfaces/org.rpm.dnf.v0.*.xml
%{_datadir}/polkit-1/actions/org.rpm.dnf.v0.policy
%license COPYING.md
%license gpl-2.0.txt
%if %{with man}
%{_mandir}/man8/dnf5daemon-server.8.*
%{_mandir}/man8/dnf5daemon-dbus-api.8.*
%endif
%endif


# ========== dnf5-plugins ==========

%if %{with dnf5_plugins}
%package -n dnf5-plugins
Summary:        Plugins for dnf5
License:        LGPL-2.1-or-later
Requires:       dnf5%{?_isa} = %{version}-%{release}

%description -n dnf5-plugins
Core DNF5 plugins that enhance dnf5 with builddep, changelog, copr, and repoclosure commands.

%files -n dnf5-plugins
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
    -DWITH_DNF5DAEMON_CLIENT=%{?with_dnf5daemon_client:ON}%{!?with_dnf5daemon_client:OFF} \
    -DWITH_DNF5DAEMON_SERVER=%{?with_dnf5daemon_server:ON}%{!?with_dnf5daemon_server:OFF} \
    -DWITH_LIBDNF5_CLI=%{?with_libdnf_cli:ON}%{!?with_libdnf_cli:OFF} \
    -DWITH_DNF5=%{?with_dnf5:ON}%{!?with_dnf5:OFF} \
    -DWITH_PLUGIN_ACTIONS=%{?with_plugin_actions:ON}%{!?with_plugin_actions:OFF} \
    -DWITH_PYTHON_PLUGINS_LOADER=%{?with_python_plugins_loader:ON}%{!?with_python_plugins_loader:OFF} \
    \
    -DWITH_COMPS=%{?with_comps:ON}%{!?with_comps:OFF} \
    -DWITH_MODULEMD=%{?with_modulemd:ON}%{!?with_modulemd:OFF} \
    -DWITH_ZCHUNK=%{?with_zchunk:ON}%{!?with_zchunk:OFF} \
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
    -DPROJECT_VERSION_MAJOR=%{project_version_major} \
    -DPROJECT_VERSION_MINOR=%{project_version_minor} \
    -DPROJECT_VERSION_PATCH=%{project_version_patch}
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
* Tue Nov 14 2023 Sam Meluch <sammeluch@microsoft.com> - 5.0.14-3
- compile without modulemd

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 5.0.14-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Wed Jun 21 2023 Sam Meluch <sammeluch@microsoft.com> - 5.0.14-1
- Add "if with man" sections for files section
- turn off man, ruby, perl for mariner
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
