# Disable automatic compilation of Python files in extra directories
%global _python_bytecompile_extra 0
# set following to the actual commit or, for final release, concatenate
# "boothver" macro to "v" (will yield a tag per the convention)
%global commit 5d837d2b5bf1c240a5f1c5efe4e8d79f55727cca
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}}
%{!?_licensedir:%global license %doc}
%global test_path   %{_datadir}/booth/tests
# RPMs are split as follows:
# * booth:
#   - envelope package serving as a syntactic shortcut to install
#     booth-site (with architecture reliably preserved)
# * booth-core:
#   - package serving as a base for booth-{arbitrator,site},
#     carrying also basic documentation, license, etc.
# * booth-arbitrator:
#   - package to be installed at a machine accessible within HA cluster(s),
#     but not (necessarily) a member of any, hence no dependency
#     on anything from cluster stack is required
# * booth-site:
#   - package to be installed at a cluster member node
#     (requires working cluster environment to be useful)
# * booth-test:
#   - files for testing booth
#
# TODO:
# wireshark-dissector.lua currently of no use (rhbz#1259623), but if/when
# this no longer persists, add -wireshark package (akin to libvirt-wireshark)
%bcond_with html_man
%bcond_with glue
Summary:        Ticket Manager for Multi-site Clusters
Name:           booth
Version:        1.0
Release:        8%{?dist}
License:        GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/ClusterLabs/%{name}
Source0:        https://github.com/ClusterLabs/%{name}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:    CVE-2022-2553.patch
# direct build process dependencies
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  coreutils
BuildRequires:  make
## ./autogen.sh
BuildRequires:  /bin/sh
# general build dependencies
BuildRequires:  asciidoc
BuildRequires:  gcc
BuildRequires:  pkgconfig
# linking dependencies
BuildRequires:  libgcrypt-devel
BuildRequires:  libxml2-devel
## just for <pacemaker/crm/services.h> include
BuildRequires:  pacemaker-libs-devel
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  zlib-devel
## logging provider
BuildRequires:  pkgconfig(libqb)
## random2range provider
BuildRequires:  pkgconfig(glib-2.0)
## nametag provider
BuildRequires:  systemd-devel
# check scriptlet (for hostname and killall respectively)
BuildRequires:  hostname psmisc
BuildRequires:  python3-devel
# spec file specifics
## for _unitdir, systemd_requires and specific scriptlet macros
BuildRequires:  systemd
## for autosetup
BuildRequires:  git
# this is for a composite-requiring-its-components arranged
# as an empty package (empty files section) requiring subpackages
# (_isa so as to preserve the architecture)
Requires:       %{name}-core%{?_isa}
Requires:       %{name}-site

%files
# intentionally empty

%description
Booth manages tickets which authorize cluster sites located
in geographically dispersed locations to run resources.
It facilitates support of geographically distributed
clustering in Pacemaker.

# SUBPACKAGES #
%package        core
Summary:        Booth core files (executables, etc.)
# for booth-keygen (chown, dd)
Requires:       coreutils
# deal with pre-split arrangement
Conflicts:      %{name} < 1.0-1

%description    core
Core files (executables, etc.) for Booth, ticket manager for
multi-site clusters.

%package        arbitrator
Summary:        Booth support for running as an arbitrator
Requires:       %{name}-core = %{version}-%{release}
# deal with pre-split arrangement
Conflicts:      %{name} < 1.0-1
BuildArch:      noarch
%{?systemd_requires}

%description    arbitrator
Support for running Booth, ticket manager for multi-site clusters,
as an arbitrator.

%post arbitrator
%systemd_post booth@.service booth-arbitrator.service

%preun arbitrator
%systemd_preun booth@.service booth-arbitrator.service

%postun arbitrator
%systemd_postun_with_restart booth@.service booth-arbitrator.service

%package        site
Summary:        Booth support for running as a full-fledged site
Requires:       %{name}-core = %{version}-%{release}
# for crm_{resource,simulate,ticket} utilities
Requires:       pacemaker >= 1.1.8
# for ocf-shellfuncs and other parts of OCF shell-based environment
Requires:       resource-agents
# deal with pre-split arrangement
Conflicts:      %{name} < 1.0-1
BuildArch:      noarch

%description    site
Support for running Booth, ticket manager for multi-site clusters,
as a full-fledged site.

%package        test
Summary:        Test scripts for Booth
# any of the following internal dependencies will pull -core package
## for booth@booth.service
Requires:       %{name}-arbitrator = %{version}-%{release}
## for booth-site and service-runnable scripts
## (and /usr/lib/ocf/resource.d/booth)
Requires:       %{name}-site = %{version}-%{release}
Requires:       gdb
# runtests.py suite (for hostname and killall respectively)
Requires:       hostname
Requires:       psmisc
Requires:       python3
Requires:       python3-pexpect
BuildArch:      noarch

%description    test
Automated tests for running Booth, ticket manager for multi-site clusters.

%prep
%autosetup -p1 -n %{name}-%{commit}

%build
export CFLAGS=" %{build_cflags} -I/usr/include/pacemaker "
./autogen.sh
%configure \
        --with-initddir=%{_initrddir} \
        --docdir=%{_pkgdocdir} \
        --enable-user-flags \
        %{!?with_html_man:--without-html_man} \
        %{!?with_glue:--without-glue} \
        PYTHON=python3
%make_build

%install
%make_install
mkdir -p %{buildroot}/%{_unitdir}
cp -a -t %{buildroot}/%{_unitdir} \
        -- conf/booth@.service conf/booth-arbitrator.service
install -D -m 644 -t %{buildroot}/%{_mandir}/man8 \
        -- docs/boothd.8
ln -s boothd.8 %{buildroot}/%{_mandir}/man8/booth.8
cp -a -t %{buildroot}/%{_pkgdocdir} \
        -- ChangeLog README-testing conf/booth.conf.example
# drop what we don't package anyway (COPYING added via tarball-relative path)
rm -rf %{buildroot}/%{_initrddir}/booth-arbitrator
rm -rf %{buildroot}/%{_pkgdocdir}/README.upgrade-from-v0.1
rm -rf %{buildroot}/%{_pkgdocdir}/COPYING
# tests
mkdir -p %{buildroot}/%{test_path}
cp -a -t %{buildroot}/%{test_path} \
        -- conf test unit-tests script/unit-test.py
chmod +x %{buildroot}/%{test_path}/test/booth_path
chmod +x %{buildroot}/%{test_path}/test/live_test.sh
mkdir -p %{buildroot}/%{test_path}/src
ln -s -t %{buildroot}/%{test_path}/src \
        -- %{_sbindir}/boothd

# https://fedoraproject.org/wiki/Packaging:Python_Appendix#Manual_byte_compilation
%py_byte_compile %{__python3} %{buildroot}/%{test_path}

%check
# alternatively: test/runtests.py
VERBOSE=1 make check

%files core
%license COPYING
%doc %{_pkgdocdir}/AUTHORS
%doc %{_pkgdocdir}/ChangeLog
%doc %{_pkgdocdir}/README
%doc %{_pkgdocdir}/booth.conf.example
# core command(s) + man pages
%{_sbindir}/booth*
%{_mandir}/man8/booth*.8*
# configuration
%dir %{_sysconfdir}/booth
%exclude %{_sysconfdir}/booth/booth.conf.example

%files arbitrator
%{_unitdir}/booth@.service
%{_unitdir}/booth-arbitrator.service

%files site
# OCF (agent + a helper)
%{_libdir}/ocf/resource.d/pacemaker/booth-site
%dir %{_libdir}/ocf/lib/booth
%{_libdir}/ocf/lib/booth/geo_attr.sh
# geostore (command + OCF agent)
%{_sbindir}/geostore
%{_mandir}/man8/geostore.8*
%dir %{_libdir}/ocf/resource.d/booth
%{_libdir}/ocf/resource.d/booth/geostore
# helper (possibly used in the configuration hook)
%dir %{_datadir}/booth
%{_datadir}/booth/service-runnable

%files test
%doc %{_pkgdocdir}/README-testing
# /usr/share/booth provided by -site
%{test_path}
# /usr/lib/ocf/resource.d/booth provided by -site
%{_libdir}/ocf/resource.d/booth/sharedrsc

%changelog
* Wed Aug 30 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.0-8
- Add patch for CVE-2022-2553

* Wed Mar 08 2023 Sumedh Sharma <sumsharma@microsoft.com> - 1.0-7
- license verified

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0-6
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Wed Aug 11 2021 Olivia Crain <oliviacrain@microsoft.com> - 1.0-5.5d837d2.git
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Substitute asciidoc for asciidoctor build requirement

* Mon May 4 2020 Jan Friesse <jfriesse@redhat.com> - 1.0-4.5d837d2.git
- Update to current snapshot (commit 5d837d2) to build with gcc10
- Pass full path of Python3 to configure

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-3.f2d38ce.git.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-3.f2d38ce.git.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-3.f2d38ce.git.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Jan Pokorný <jpokorny+rpm-booth@fedoraproject.org> - 1.0-3.f2d38ce.git
- update for another, current snapshot beyond booth-1.0
  (commit f2d38ce), including:
  . support for solely manually managed tickets (9a365f9)
  . use asciidoctor instead of asciidoc for generating man pages (65e6a6b)
- switch to using Python 3 for the tests instead of Python 2
  (behind unversioned "python" references; rhbz#1555651)

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-2.570876d.git.6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-2.570876d.git.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-2.570876d.git.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-2.570876d.git.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-2.570876d.git.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-2.570876d.git.1
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed May 25 2016 Jan Pokorný <jpokorny+rpm-booth@fedoraproject.org> - 1.0-3.570876d.git
- update per the changesets recently accepted by the upstream
  (memory/resource leaks fixes, patches previously attached separately
  that make unit test pass, internal cleanups, etc.)

* Thu May 05 2016 Jan Pokorný <jpokorny+rpm-booth@fedoraproject.org> - 1.0-2.eb4256a.git
- update a subset of out-of-tree patches per
  https://github.com/ClusterLabs/booth/pull/22#issuecomment-216936987
- pre-inclusion cleanups in the spec (apply systemd scriptlet operations
  with booth-arbitrator, avoid overloading file implicitly considered %%doc
  as %%license)
  Resolves: rhbz#1314865
  Related: rhbz#1333509

* Thu Apr 28 2016 Jan Pokorný <jpokorny+rpm-booth@fedoraproject.org> - 1.0-1.eb4256a.git
- initial build
