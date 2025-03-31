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
%bcond_with run_build_tests

## User and group to use for nonprivileged services (should be in sync with pacemaker)
%global uname hacluster
%global gname haclient

# Disable automatic compilation of Python files in extra directories
%global _python_bytecompile_extra 0

%global github_owner ClusterLabs

%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}}
# https://fedoraproject.org/wiki/EPEL:Packaging?rd=Packaging:EPEL#The_.25license_tag
%{!?_licensedir:%global license %doc}

%global test_path   %{_datadir}/booth/tests

Name:           booth
Version:        1.2
Release:        2%{?dist}
Summary:        Ticket Manager for Multi-site Clusters
License:        GPL-2.0-or-later
Url:            https://github.com/%{github_owner}/%{name}
Source0:        https://github.com/%{github_owner}/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.gz

# direct build process dependencies
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  coreutils
BuildRequires:  make
## ./autogen.sh
BuildRequires:  /bin/sh
# general build dependencies
BuildRequires:  asciidoctor
BuildRequires:  gcc
BuildRequires:  pkgconfig
# linking dependencies
BuildRequires:  gnutls-devel
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
BuildRequires:  pkgconfig(libsystemd)
# check scriptlet (for hostname and killall respectively)
BuildRequires:  hostname psmisc
BuildRequires:  python3-devel
# For generating tests
BuildRequires:  sed
# spec file specifics
## for _unitdir, systemd_requires and specific scriptlet macros
BuildRequires:  systemd
## for autosetup
BuildRequires:  git
%if 0%{?with_run_build_tests}
# check scriptlet (for perl and ss)
BuildRequires:  perl-interpreter iproute
%endif

# this is for a composite-requiring-its-components arranged
# as an empty package (empty files section) requiring subpackages
# (_isa so as to preserve the architecture)
Requires:       %{name}-core%{?_isa}
Requires:       %{name}-site
%files
%license COPYING
%dir %{_datadir}/pkgconfig
%{_datadir}/pkgconfig/booth.pc

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
BuildArch:      noarch
Requires:       %{name}-core = %{version}-%{release}
%{?systemd_requires}
# deal with pre-split arrangement
Conflicts:      %{name} < 1.0-1

%description    arbitrator
Support for running Booth, ticket manager for multi-site clusters,
as an arbitrator.

%post arbitrator
%systemd_post booth-arbitrator.service

%preun arbitrator
%systemd_preun booth-arbitrator.service

%postun arbitrator
%systemd_postun_with_restart booth-arbitrator.service

%package        site
Summary:        Booth support for running as a full-fledged site
BuildArch:      noarch
Requires:       %{name}-core = %{version}-%{release}
# for crm_{resource,simulate,ticket} utilities
Requires:       pacemaker >= 1.1.8
# for ocf-shellfuncs and other parts of OCF shell-based environment
Requires:       resource-agents
# deal with pre-split arrangement
Conflicts:      %{name} < 1.0-1

%description    site
Support for running Booth, ticket manager for multi-site clusters,
as a full-fledged site.

%package        test
Summary:        Test scripts for Booth
BuildArch:      noarch
# runtests.py suite (for hostname and killall respectively)
Requires:       hostname psmisc
# any of the following internal dependencies will pull -core package
## for booth@booth.service
Requires:       %{name}-arbitrator = %{version}-%{release}
## for booth-site and service-runnable scripts
## (and /usr/lib/ocf/resource.d/booth)
Requires:       %{name}-site = %{version}-%{release}
Requires:       gdb
Requires:       %{__python3}
# runtests.py suite (for perl and ss)
Requires:       perl-interpreter iproute

%description    test
Automated tests for running Booth, ticket manager for multi-site clusters.

# BUILD #

%prep
%autosetup -n %{name}-%{version} -S git_am

%build
./autogen.sh
%{configure} \
        --with-initddir=%{_initrddir} \
        --docdir=%{_pkgdocdir} \
        --enable-user-flags \
        %{?with_html_man:--with-html_man} \
        %{!?with_glue:--without-glue} \
        PYTHON=%{__python3}
%{make_build}

%install
%{make_install}
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
# Copy tests from tarball
cp -a -t %{buildroot}/%{test_path} \
        -- conf test
chmod +x %{buildroot}/%{test_path}/test/booth_path
chmod +x %{buildroot}/%{test_path}/test/live_test.sh
mkdir -p %{buildroot}/%{test_path}/src
ln -s -t %{buildroot}/%{test_path}/src \
        -- %{_sbindir}/boothd
# Generate runtests.py and boothtestenv.py
sed -e 's#PYTHON_SHEBANG#%{__python3} -Es#g' \
    -e 's#TEST_SRC_DIR#%{test_path}/test#g' \
    -e 's#TEST_BUILD_DIR#%{test_path}/test#g' \
    %{buildroot}/%{test_path}/test/runtests.py.in > %{buildroot}/%{test_path}/test/runtests.py

chmod +x %{buildroot}/%{test_path}/test/runtests.py

sed -e 's#PYTHON_SHEBANG#%{__python3} -Es#g' \
    -e 's#TEST_SRC_DIR#%{test_path}/test#g' \
    -e 's#TEST_BUILD_DIR#%{test_path}/test#g' \
    %{buildroot}/%{test_path}/test/boothtestenv.py.in > %{buildroot}/%{test_path}/test/boothtestenv.py

# https://fedoraproject.org/wiki/Packaging:Python_Appendix#Manual_byte_compilation
%py_byte_compile %{__python3} %{buildroot}/%{test_path}

%check
# alternatively: test/runtests.py
%if 0%{?with_run_build_tests}
VERBOSE=1 make check
%endif

%files          core
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

%dir %attr (750, %{uname}, %{gname}) %{_var}/lib/booth/
%dir %attr (750, %{uname}, %{gname}) %{_var}/lib/booth/cores

# Generated html docs
%if 0%{?with_html_man}
%{_pkgdocdir}/booth-keygen.8.html
%{_pkgdocdir}/boothd.8.html
%endif

%files          arbitrator
%{_unitdir}/booth@.service
%{_unitdir}/booth-arbitrator.service

%files          site
# OCF (agent + a helper)
## /usr/lib/ocf/resource.d/pacemaker provided by pacemaker
%{_usr}/lib/ocf/resource.d/pacemaker/booth-site
%dir %{_usr}/lib/ocf/lib/booth
     %{_usr}/lib/ocf/lib/booth/geo_attr.sh
# geostore (command + OCF agent)
%{_sbindir}/geostore
%{_mandir}/man8/geostore.8*
## /usr/lib/ocf/resource.d provided by resource-agents
%dir %{_usr}/lib/ocf/resource.d/booth
     %{_usr}/lib/ocf/resource.d/booth/geostore
# helper (possibly used in the configuration hook)
%dir %{_datadir}/booth
     %{_datadir}/booth/service-runnable

# Generated html docs
%if 0%{?with_html_man}
%{_pkgdocdir}/geostore.8.html
%endif

%files          test
%doc %{_pkgdocdir}/README-testing
# /usr/share/booth provided by -site
%{test_path}
# /usr/lib/ocf/resource.d/booth provided by -site
%{_usr}/lib/ocf/resource.d/booth/sharedrsc

%changelog
* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Jan Friesse <jfriesse@redhat.com> - 1.2-1
- New upstream release

* Tue Jan 23 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Oct 18 2023 Jan Friesse <jfriesse@redhat.com> - 1.1-1
- New upstream release
- Upstream releases should now be released regularly, so convert spec
  to use them instead of git snapshots

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-283.4.9d4029a.git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 06 2023 Jan Friesse <jfriesse@redhat.com> - 1.0-283.3.9d4029a.git
- migrated to SPDX license

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-283.2.9d4029a.git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Nov 21 2022 Jan Friesse <jfriesse@redhat.com> - 1.0-283.1.9d4029a.git
- Rebase to newest upstream snapshot

* Fri Sep 30 2022 Jan Friesse <jfriesse@redhat.com> - 1.0-272.1.7acb757.git
- Rebase to newest upstream snapshot

* Thu Sep 29 2022 Jan Friesse <jfriesse@redhat.com> - 1.0-266.4.f288d59.git
- Remove Alias directive from booth@.service unit file

* Tue Aug 09 2022 Jan Friesse <jfriesse@redhat.com> - 1.0-266.3.f288d59.git
- Remove template unit from systemd_(post|preun|postun_with_restart) macro

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-266.2.f288d59.git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 20 2022 Jan Friesse <jfriesse@redhat.com> - 1.0-266.1.f288d59.git
- Rebase to newest upstream snapshot
- This version fixes a critical bug that caused the authfile directive
  to be ignored. After installing the patched version, nodes may stop
  communicating. Solution is to either remove authfile from configuration
  file or update all other nodes.

* Thu May 19 2022 Jan Friesse <jfriesse@redhat.com> - 1.0-262.1.d0ac26c.git
- Rebase to newest upstream snapshot

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-251.3.bfb2f92.git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-251.2.bfb2f92.git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu May 20 2021 Jan Friesse <jfriesse@redhat.com> - 1.0-251.1.bfb2f92.git
- Rebase to newest upstream snapshot

* Tue May 18 2021 Jan Friesse <jfriesse@redhat.com> - 1.0-249.1.977726e.git
- Do not include unit-test by default
- Rebase to newest upstream snapshot

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.0-239.3.52ec255.git
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-239.2.52ec255.git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Nov 23 2020 Jan Friesse <jfriesse@redhat.com> - 1.0-239.1.52ec255.git
- Rebase to newest upstream snapshot

* Thu Oct 15 2020 Jan Friesse <jfriesse@redhat.com> - 1.0-237.2.dd88847.git
- Fix dist macro

* Thu Oct 15 2020 Jan Friesse <jfriesse@redhat.com> - 1.0-237.1.dd88847.git
- Rebase to newest upstream snapshot

* Thu Oct 15 2020 Jan Friesse <jfriesse@redhat.com> - 1.0-199.1.ac1d34c.git
- Implement new versioning scheme

* Tue Sep 29 2020 Jan Friesse <jfriesse@redhat.com> - 1.0-6.ac1d34c.git.5
- Remove net-tools (netstat) dependency and replace it with iproute (ss)
- Disable running tests during build by default (conditional run_build_tests)

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-6.ac1d34c.git.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jun 3 2020 Jan Friesse <jfriesse@redhat.com> - 1.0-6.ac1d34c.git.3
- Do not link with the pcmk libraries
- Generate runtests.py and boothtestenv.py with -Es as make check does

* Tue Jun 2 2020 Jan Friesse <jfriesse@redhat.com> - 1.0-6.ac1d34c.git.2
- Require the Python interpreter directly instead of using the package name

* Tue Jun 2 2020 Jan Friesse <jfriesse@redhat.com> - 1.0-6.ac1d34c.git.1
- Update to current snapshot (commit ac1d34c) to fix test suite

* Mon Jun 1 2020 Jan Friesse <jfriesse@redhat.com> - 1.0-5.385cc25.git.3
- Add CI tests
- Enable gating
- Fix hardcoded-library-path

* Mon Jun 1 2020 Jan Friesse <jfriesse@redhat.com> - 1.0-5.385cc25.git.2
- Package /var/lib/booth where booth can chroot

* Thu May 28 2020 Jan Friesse <jfriesse@redhat.com> - 1.0-5.385cc25.git.1
- Fix test subpackage generating

* Wed May 27 2020 Jan Friesse <jfriesse@redhat.com> - 1.0-5.385cc25.git
- Update to current snapshot (commit 385cc25) to fix build warnings

* Wed May 13 2020 Jan Friesse <jfriesse@redhat.com> - 1.0-4.5d837d2.git.2
- Rebuild for the new libqb

* Mon May 4 2020 Jan Friesse <jfriesse@redhat.com> - 1.0-4.5d837d2.git.1
- Add '?dist' macro to release field

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
