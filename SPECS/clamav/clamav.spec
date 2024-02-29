Summary:        Open source antivirus engine
Name:           clamav
Version:        0.105.2
Release:        4%{?dist}
License:        ASL 2.0 AND BSD AND bzip2-1.0.4 AND GPLv2 AND LGPLv2+ AND MIT AND Public Domain AND UnRar
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Security
URL:            https://www.clamav.net
Source0:        https://github.com/Cisco-Talos/clamav/archive/refs/tags/%{name}-%{version}.tar.gz
# Note: the %%{name}-%%{name}-%%{version}-cargo.tar.gz file contains a cache created by capturing the contents downloaded into $CARGO_HOME.
# To update the cache run:
#   [repo_root]/toolkit/scripts/build_cargo_cache.sh %%{name}-%%{version}.tar.gz %%{name}-%%{name}-%%{version}

# Note: Required an updated cargo cache when rust was updated to 1.72.0, added "-rev2" to the filename to indicate the new cache for this
# specific event. Revert back to the original filename when a new cache is created for a different version.
Source1:        %{name}-%{name}-%{version}-cargo-rev2.tar.gz
Patch0:         CVE-2022-48579.patch
BuildRequires:  bzip2-devel
BuildRequires:  check-devel
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gdb
BuildRequires:  git
BuildRequires:  json-c-devel
BuildRequires:  libcurl-devel
BuildRequires:  libxml2-devel
BuildRequires:  make
BuildRequires:  ncurses-devel
BuildRequires:  openssl-devel
BuildRequires:  pcre2-devel
BuildRequires:  python3
BuildRequires:  python3-pip
BuildRequires:  python3-pytest
BuildRequires:  rust
BuildRequires:  systemd-devel
BuildRequires:  valgrind
BuildRequires:  zlib-devel
Requires:       openssl
Requires:       zlib
Requires(pre):  shadow-utils
Requires(postun): shadow-utils
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-lib = %{version}-%{release}

%description
ClamAV® is an open source (GPL) anti-virus engine used in a variety of situations
including email scanning, web scanning, and end point security. It provides a number
of utilities including a flexible and scalable multi-threaded daemon, a command
line scanner and an advanced tool for automatic database updates.

%prep
# Setup .cargo directory
mkdir -p $HOME
pushd $HOME
tar xf %{SOURCE1} --no-same-owner
popd
%autosetup -p1 -n clamav-clamav-%{version}

%build
export CARGO_NET_OFFLINE=true
# Notes:
# - milter must be disable because CBL-Mariner does not provide 'sendmail' packages
#   which provides the necessary pieces to build 'clamav-milter'
# - systemd should be enabled because default value is off
cmake \
    -D CMAKE_INSTALL_LIBDIR=%{_libdir} \
    -D CMAKE_INSTALL_BINDIR=%{_bindir} \
    -D CMAKE_INSTALL_SBINDIR=%{_sbindir} \
    -D CMAKE_INSTALL_MANDIR=%{_mandir} \
    -D CMAKE_INSTALL_DOCDIR=%{_docdir} \
    -D CMAKE_INSTALL_INCLUDEDIR=%{_includedir} \
    -D SYSTEMD_UNIT_DIR=%{_libdir}/systemd/system \
    -D APP_CONFIG_DIRECTORY=%{_sysconfdir}/clamav \
    -D DATABASE_DIRECTORY=%{_sharedstatedir}/clamav \
    -D ENABLE_SYSTEMD=ON \
    -D ENABLE_MILTER=OFF \
    -D ENABLE_EXAMPLES=OFF
%cmake_build

%check
cd build
ctest --verbose

%install
%cmake_install
# do not install html doc ('clamav' cmake has no flag to specify that => remove the doc)
rm -rf %{buildroot}%{_docdir}
mkdir -p %{buildroot}%{_sharedstatedir}/clamav

### freshclam config processing (from Fedora)
sed -ri \
    -e 's!^Example!#Example!' \
    -e 's!^#?(UpdateLogFile )!#\1!g;' %{buildroot}%{_sysconfdir}/clamav/freshclam.conf.sample

mv %{buildroot}%{_sysconfdir}/clamav/freshclam.conf{.sample,}
# Can contain HTTPProxyPassword (bugz#1733112)
chmod 600 %{buildroot}%{_sysconfdir}/clamav/freshclam.conf

%pre
if [ $1 -eq 1 ]; then
    if ! getent group clamav >/dev/null; then
        groupadd -r clamav
    fi
    if ! getent passwd clamav >/dev/null; then
        useradd -g clamav -d %{_sharedstatedir}/clamav\
            -s /bin/false -M -r clamav
    fi
fi

%postun
if [ $1 -eq 0 ]; then
    if getent passwd clamav >/dev/null; then
        userdel clamav
    fi
    if getent group clamav >/dev/null; then
        groupdel clamav
    fi
fi

%files
%defattr(-,root,root)
%license COPYING.txt COPYING/COPYING.LGPL COPYING/COPYING.bzip2 COPYING/COPYING.file COPYING/COPYING.llvm COPYING/COPYING.pcre COPYING/COPYING.unrar COPYING/COPYING.YARA COPYING/COPYING.curl COPYING/COPYING.getopt COPYING/COPYING.lzma COPYING/COPYING.regex COPYING/COPYING.zlib
%{_libdir}/*.so
%{_libdir}/*.so.*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/systemd/system/*
%{_bindir}/*
%{_sbindir}/*
%{_sysconfdir}/clamav/*.sample
%{_sysconfdir}/clamav/freshclam.conf
%{_includedir}/*.h
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%dir %attr(-,clamav,clamav) %{_sharedstatedir}/clamav

%changelog
* Fri Dec 08 2023 Neha Agarwal <nehaagarwal@microsoft.com> - 0.105.2-4
- Fix resetting of user and group settings on package update

* Thu Sep 07 2023 Daniel McIlvaney <damcilva@microsoft.com> - 0.105.2-3
- Bump package to rebuild with rust 1.72.0

* Tue Aug 29 2023 Tobias Brick <tobiasb@microsoft.com> - 0.105.2-2
- Patch CVE-2022-48579

* Fri Feb 17 2023 corvus-callidus <108946721+corvus-callidus@users.noreply.github.com> - 0.105.2-1
- Upgrade to 0.105.2 to fix CVE-2023-20032 and CVE-2023-20052

* Wed Sep 07 2022 Olivia Crain <oliviacrain@microsoft.com> - 0.105.0-3
- Add pre/postun requirements on shadow-utils

* Wed Aug 31 2022 Olivia Crain <oliviacrain@microsoft.com> - 0.105.0-2
- Bump package to rebuild with stable Rust compiler

* Mon Jun 13 2022 Andrew Phelps <anphel@microsoft.com> - 0.105.0-1
- Upgrade to version 0.105.0

* Wed Jun 08 2022 Tom Fay <tomfay@microsoft.com> - 0.104.2-2
- Fix freshclam DB download

* Fri Jan 14 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 0.104.2-1
- Upgrade to 0.104.2

* Fri Sep 10 2021 Thomas Crain <thcrain@microsoft.com> - 0.103.2-3
- Remove libtool archive files from final packaging

* Fri Jul 23 2021 Thomas Crain <thcrain@microsoft.com> - 0.103.2-2
- Add provides for devel, lib subpackages
- Use make macros throughout

* Tue Apr 20 2021 Thomas Crain <thcrain@microsoft.com> - 0.103.2-1
- Updating to 0.103.2 to fix CVE-2021-1252, CVE-2021-1404, CVE-2021-1405

* Fri Apr 02 2021 Thomas Crain <thcrain@microsoft.com> - 0.103.0-2
- Merge the following releases from dev to 1.0 spec
- v-ruyche@microsoft.com, 0.101.2-4: Systemd supports merged /usr. Update units file location and macro.

* Tue Oct 27 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 0.103.0-1
- Updating to 0.103.0 to fix: CVE-2019-12625, CVE-2019-15961.

* Mon Oct 19 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.101.2-3
- License verified.
- Added %%license macro.
- Switching to using the %%configure macro.
- Extended package's summary and description.

* Wed Oct 02 2019 Mateusz Malisz <mamalisz@microsoft.com> - 0.101.2-2
- Fix vendor and distribution. Add systemd files to the list.

* Thu Jul 25 2019 Chad Zawistowski <chzawist@microsoft.com> - 0.101.2-1
- Initial CBL-Mariner import from Azure.
