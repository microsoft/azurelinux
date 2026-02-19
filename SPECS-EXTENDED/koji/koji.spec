# This package depends on selective manual byte compilation
# https://fedoraproject.org/wiki/Changes/No_more_automagic_Python_bytecompilation_phase_2
%global _python_bytecompile_extra 0
 
%define __python %{__python3}
 
# If the definition isn't available for python3_pkgversion, define it
%{?!python3_pkgversion:%global python3_pkgversion 3}
 
Name: koji
Version: 1.35.3
Release: 10%{?dist}
# the included arch lib from yum's rpmUtils is GPLv2+
License: LGPL-2.1-only AND GPL-2.0-or-later
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Summary: Build system tools
URL: https://pagure.io/koji/
Source0: https://releases.pagure.org/koji/koji-%{version}.tar.bz2
 
# https://pagure.io/koji/pull-request/4342
# download-build: allow fallback to unsigned with --key
Patch0: 0001-download-build-allow-fallback-to-unsigned-with-key.patch
Patch1: 0002-Fix-flake8-and-unit-test.patch
 
BuildArch: noarch
Requires: python%{python3_pkgversion}-%{name} = %{version}-%{release}
Requires: python%{python3_pkgversion}-libcomps
Requires: python3-libcomps
BuildRequires: systemd
BuildRequires: pkgconfig
BuildRequires: sed
 
%description
Koji is a system for building and tracking RPMS.  The base package
contains shared libraries and the command-line interface.
 
%package -n python%{python3_pkgversion}-%{name}
Summary: Build system tools python library
%{?python_provide:%python_provide python%{python3_pkgversion}-%{name}}
BuildRequires: python%{python3_pkgversion}-devel
BuildRequires: python%{python3_pkgversion}-setuptools
BuildRequires: make
BuildRequires: python3-pip
BuildRequires: python3-wheel
 
%description -n python%{python3_pkgversion}-%{name}
Koji is a system for building and tracking RPMS.
This subpackage provides python functions and libraries.
 
%package -n python%{python3_pkgversion}-%{name}-cli-plugins
Summary: Koji client plugins
License: LGPL-2.1-only
Requires: python%{python3_pkgversion}-%{name} = %{version}-%{release}
 
%description -n python%{python3_pkgversion}-%{name}-cli-plugins
Plugins to the koji command-line interface
 
%package hub
Summary: Koji XMLRPC interface
License: LGPL-2.1-only
Requires: %{name} = %{version}-%{release}
Requires: %{name}-hub-code
%if 0%{?fedora} || 0%{?rhel} > 7
Suggests: python%{python3_pkgversion}-%{name}-hub
Suggests: python%{python3_pkgversion}-%{name}-hub-plugins
%endif
 
%description hub
koji-hub is the XMLRPC interface to the koji database
 
%package -n python%{python3_pkgversion}-%{name}-hub
Summary: Koji XMLRPC interface
License: LGPL-2.1-only
# rpmdiff lib (from rpmlint) is GPLv2 (only)
Requires: httpd
Requires: python%{python3_pkgversion}-psycopg2
Requires: python%{python3_pkgversion}-%{name} = %{version}-%{release}
Provides: %{name}-hub-code = %{version}-%{release}
 
%description -n python%{python3_pkgversion}-%{name}-hub
koji-hub is the XMLRPC interface to the koji database
 
%package hub-plugins
Summary: Koji hub plugins
License: LGPL-2.1-only
Requires: %{name}-hub-plugins-code = %{version}-%{release}
%if 0%{?fedora} || 0%{?rhel} > 7
Suggests: python%{python3_pkgversion}-%{name}-hub-plugins
%endif
 
%description hub-plugins
Plugins to the koji XMLRPC interface
 
%package -n python%{python3_pkgversion}-%{name}-hub-plugins
Summary: Koji hub plugins
License: LGPL-2.1-only
Requires: python%{python3_pkgversion}-%{name}-hub = %{version}-%{release}
Requires: cpio
Provides: %{name}-hub-plugins-code = %{version}-%{release}
 
%description -n python%{python3_pkgversion}-%{name}-hub-plugins
Plugins to the koji XMLRPC interface
 
%package builder-plugins
Summary: Koji builder plugins
License: LGPL-2.1-only
Requires: %{name} = %{version}-%{release}
Requires: %{name}-builder = %{version}-%{release}
 
%description builder-plugins
Plugins for the koji build daemon
 
%package builder
Summary: Koji RPM builder daemon
License: LGPL-2.1-only
Requires: mock >= 0.9.14
Requires: squashfs-tools
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
Requires: /usr/bin/svn
Requires: /usr/bin/git
Requires: createrepo_c >= 0.10.0
Requires: python%{python3_pkgversion}-%{name} = %{version}-%{release}
Requires: python%{python3_pkgversion}-librepo
 
%description builder
koji-builder is the daemon that runs on build machines and executes
tasks that come through the Koji system.
 
%package vm
Summary: Koji virtual machine management daemon
License: LGPL-2.1-only
Requires: %{name} = %{version}-%{release}
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
Requires: python%{python3_pkgversion}-libvirt
Requires: python%{python3_pkgversion}-libxml2
Requires: qemu-img
 
%description vm
koji-vm contains a supplemental build daemon that executes certain tasks in a
virtual machine. This package is not required for most installations.
 
%package utils
Summary: Koji Utilities
License: LGPL-2.1-only
Requires: %{name} = %{version}-%{release}
Requires: python%{python3_pkgversion}-psycopg2
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
 
%description utils
Utilities for the Koji system
 
%package web
Summary: Koji Web UI
License: LGPL-2.1-only
Requires: %{name} = %{version}-%{release}
Requires: %{name}-web-code = %{version}-%{release}
%if 0%{?fedora} || 0%{?rhel} > 7
Suggests: python%{python3_pkgversion}-%{name}-web
%endif
 
%description web
koji-web is a web UI to the Koji system.
 
%package -n python%{python3_pkgversion}-%{name}-web
Summary: Koji Web UI
License: LGPL-2.1-only
%{?python_provide:%python_provide python%{python3_pkgversion}-%{name}-web}
Requires: httpd
Requires: python%{python3_pkgversion}-psycopg2
Requires: python%{python3_pkgversion}-%{name} = %{version}-%{release}
Provides: %{name}-web-code = %{version}-%{release}
 
%description -n python%{python3_pkgversion}-%{name}-web
koji-web is a web UI to the Koji system.
 
%prep
%autosetup -p1
# we'll be packaging these separately and don't want them registered
# to the wheel we will produce.
sed -e '/util\/koji/g' -e '/koji_cli_plugins/g' -i setup.py
 
%if 0%{?fedora} > 42 || 0%{?rhel} >= 10
# Create a sysusers.d config file
cat >koji.sysusers.conf <<EOF
u kojibuilder - - /builddir /bin/bash
m kojibuilder mock
EOF
%endif
 
%build
%py3_build_wheel
%install
%define make_with_dirs make DESTDIR=$RPM_BUILD_ROOT SBINDIR=%{_sbindir}
 
%py3_install_wheel %{name}-%{version}-py3-none-any.whl
mkdir -p %{buildroot}/etc/koji.conf.d
cp cli/koji.conf %{buildroot}/etc/koji.conf
for D in kojihub builder plugins util www vm schemas ; do
    pushd $D
    %{make_with_dirs} PYTHON=%{__python3} install
    popd
done
 
# alter python interpreter in koji CLI
scripts='%{_bindir}/koji %{_sbindir}/kojid %{_sbindir}/kojira %{_sbindir}/koji-shadow
         %{_sbindir}/koji-gc %{_sbindir}/kojivmd %{_sbindir}/koji-sweep-db
         %{_sbindir}/koji-sidetag-cleanup'
for fn in $scripts ; do
    sed -i 's|#!/usr/bin/python2|#!/usr/bin/python3|' $RPM_BUILD_ROOT$fn
done
 
# handle extra byte compilation
extra_dirs='
    %{_prefix}/lib/koji-builder-plugins
    %{_prefix}/koji-hub-plugins
    %{_datadir}/koji-hub
    %{_datadir}/koji-web/lib/kojiweb
    %{_datadir}/koji-web/scripts'
for fn in $extra_dirs ; do
    %py_byte_compile %{__python3} %{buildroot}$fn
done
 
%if 0%{?fedora} > 42 || 0%{?rhel} >= 10
install -m0644 -D koji.sysusers.conf %{buildroot}%{_sysusersdir}/koji.conf
%endif
 
%files
%{_bindir}/koji
%{_datadir}/koji
%config(noreplace) /etc/koji.conf
%dir /etc/koji.conf.d
%doc docs Authors COPYING LGPL
 
%files -n python%{python3_pkgversion}-koji
%{python3_sitelib}/%{name}
%{python3_sitelib}/%{name}-%{version}.*-info
%{python3_sitelib}/koji_cli
 
%files -n python%{python3_pkgversion}-%{name}-cli-plugins
%{python3_sitelib}/koji_cli_plugins
# we don't have config files for default plugins yet
#%%dir %%{_sysconfdir}/koji/plugins
#%%config(noreplace) %%{_sysconfdir}/koji/plugins/*.conf
 
%files hub
%config(noreplace) /etc/httpd/conf.d/kojihub.conf
%dir /etc/koji-hub
%config(noreplace) /etc/koji-hub/hub.conf
%dir /etc/koji-hub/hub.conf.d
%{_sbindir}/koji-sweep-db
%{_unitdir}/koji-sweep-db.service
%{_unitdir}/koji-sweep-db.timer
 
%files -n python%{python3_pkgversion}-%{name}-hub
%{_datadir}/koji-hub/*.py
%{_datadir}/koji-hub/__pycache__
%{python3_sitelib}/kojihub
 
%files hub-plugins
%dir /etc/koji-hub/plugins
%config(noreplace) /etc/koji-hub/plugins/*.conf
 
%files -n python%{python3_pkgversion}-%{name}-hub-plugins
%{_prefix}/lib/koji-hub-plugins/*.py
%{_prefix}/lib/koji-hub-plugins/__pycache__
 
%files builder-plugins
%dir /etc/kojid/plugins
%config(noreplace) /etc/kojid/plugins/*.conf
%dir %{_prefix}/lib/koji-builder-plugins
%{_prefix}/lib/koji-builder-plugins/*.py*
%{_prefix}/lib/koji-builder-plugins/__pycache__
 
%files utils
%{_sbindir}/kojira
%{_unitdir}/koji-gc.service
%{_unitdir}/koji-gc.timer
%{_unitdir}/kojira.service
%dir /etc/kojira
%config(noreplace) /etc/kojira/kojira.conf
%{_sbindir}/koji-gc
%dir /etc/koji-gc
%config(noreplace) /etc/koji-gc/koji-gc.conf
%config(noreplace) /etc/koji-gc/email.tpl
%{_sbindir}/koji-shadow
%dir /etc/koji-shadow
%{_sbindir}/koji-sidetag-cleanup
%config(noreplace) /etc/koji-shadow/koji-shadow.conf
 
%files web
%dir /etc/kojiweb
%config(noreplace) /etc/kojiweb/web.conf
%config(noreplace) /etc/httpd/conf.d/kojiweb.conf
%dir /etc/kojiweb/web.conf.d
 
%files -n python%{python3_pkgversion}-%{name}-web
%{_datadir}/koji-web
 
%files builder
%{_sbindir}/kojid
%{_unitdir}/kojid.service
%dir /etc/kojid
%config(noreplace) /etc/kojid/kojid.conf
%attr(-,kojibuilder,kojibuilder) /etc/mock/koji
%if 0%{?fedora} > 42 || 0%{?rhel} >= 10
%{_sysusersdir}/koji.conf
%endif
 
%post builder
%systemd_post kojid.service
 
%preun builder
%systemd_preun kojid.service
 
%postun builder
%systemd_postun kojid.service
 
%files vm
%{_sbindir}/kojivmd
#dir %%{_datadir}/kojivmd
%{_datadir}/kojivmd/kojikamid
%{_unitdir}/kojivmd.service
%dir /etc/kojivmd
%config(noreplace) /etc/kojivmd/kojivmd.conf
 
%post vm
%systemd_post kojivmd.service
 
%preun vm
%systemd_preun kojivmd.service
 
%postun vm
%systemd_postun kojivmd.service
 
%post utils
%systemd_post kojira.service
 
%preun utils
%systemd_preun kojira.service
 
%postun utils
%systemd_postun kojira.service
 
%changelog
* Tue Feb 17 2026 Akarsh Chaudhary <v-akarshc@microsoft.com> - 1.35.3-10
- Initial CBL-Mariner import from Fedora 44 (license: MIT).
- License verified

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1.35.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild
 
* Tue Dec 16 2025 Adam Williamson <awilliam@redhat.com> - 1.35.3-8
- Backport PR #4342 (--fallback-unsigned feature) for Bodhi's benefit
 
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.35.3-7
- Rebuilt for Python 3.14.0rc3 bytecode
 
* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.35.3-6
- Rebuilt for Python 3.14.0rc2 bytecode
 
* Fri Jul 25 2025 Adam Williamson <awilliam@redhat.com> - 1.35.3-5
- Also do sysusers for EL 10+
 
* Wed Jul 23 2025 Kevin Fenzi <kevin@scrye.com> - 1.35.3-4
- Conditionalize sysusers for f43+
 
* Sun Jul 06 2025 Kevin Fenzi <kevin@scrye.com> - 1.35.3-3
- Add patch from Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> with sysusers.d handling
- Fixes rhbz#2364015
 
* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 1.35.3-2
- Rebuilt for Python 3.14
 
* Tue Mar 18 2025 Kevin Fenzi <kevin@scrye.com> - 1.35.2-1
- Update to 1.35.2. Fixes rhbz#2346249
- Fix FTBFS. Fixed rhbz#2340700
- Update license tags
- Add patch to handle older python versions (already upstream)
- Add patch for /usr/sbin merge handling.
 
* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.35.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild
 
* Tue Nov 26 2024 Romain Geissler <romain.geissler@amadeus.com> - 1.35.1-5
- Drop the cvs requirement.
 
* Tue Nov 19 2024 Igor Raits <ignatenkobrain@fedoraproject.org> - 1.35.1-4
- Fix symlink_if_latest() logic
 
* Thu Oct 31 2024 Mike McLean <mikem@redhat.com> - 1.35.1-3
- Backport PR #4251: drop cgi import
 
* Thu Oct 24 2024 Mike McLean <mikem@redhat.com> - 1.35.1-2
- Backport PR #4228: wait for a current repo by default
 
* Tue Oct 08 2024 Kevin Fenzi <kevin@scrye.com> - 1.35.1-1
- Update to 1.35.1. Fixes rhbz#2316304
- Fixes CVE-2024-9427
 
* Wed Sep 18 2024 Kevin Fenzi <kevin@scrye.com> - 1.35.0-1
- Update to 1.35.0. Fixes rhbz#2312848
 
* Mon Sep 02 2024 Miroslav Suchý <msuchy@redhat.com> - 1.34.1-6
- convert license to SPDX
 
* Mon Aug 26 2024 Adam Williamson <awilliam@redhat.com> - 1.34.1-5
- Backport PR #4184 to support overriding version and releasever for Kiwi
 
* Thu Aug 22 2024 Adam Williamson <awilliam@redhat.com> - 1.34.1-4
- Backport PR #4157 to support overriding Kiwi image file name format
 
* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.34.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild
 
* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.34.1-2
- Rebuilt for Python 3.13
 
* Wed Jun 05 2024 Kevin Fenzi <kevin@scrye.com> - 1.34.1-1
- Upgrade to 1.34.1. Fixes rhbz#2283973
 
* Fri Mar 22 2024 Kevin Fenzi <kevin@scrye.com> - 1.34.0-3
- Add back in missing schema files. rhbz#2270743
 
* Mon Mar 18 2024 Kevin Fenzi <kevin@scrye.com> - 1.34.0-2
- Carry scm policy plugin for hub, it's already upstream
- Use dnf5 compatible 'group install' command
- Allow specifying with a tag value what arches noarch builds happen on.
- Fix image-build to not pass units to oz (to avoid GB/GiB issues)
- Fix a typo in scheduler (already upstreamed)
- Add back index for rpminfo table that was mistakenly dropped.
 
* Thu Jan 25 2024 Kevin Fenzi <kevin@scrye.com> - 1.34.0-1
- Update to 1.34.0. Fixes rhbz#2260055
 
* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.33.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild
 
* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.33.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild
 
* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.33.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild
 
* Fri Jul 14 2023 Kevin Fenzi <kevin@scrye.com> - 1.33.1-1
- Update to 1.31.1. Fixes rhbz#2222032
 
* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 1.33.0-2
- Rebuilt for Python 3.12
 
* Wed May 24 2023 Kevin Fenzi <kevin@scrye.com> - 1.33.0-1
- Update to 1.33.0. Fixes rhbz#2209371
 
* Tue Apr 04 2023 Kevin Fenzi <kevin@scrye.com> - 1.32.1-1
- Update tp 1.32.1. Fixes rhbz#2184380
 
* Thu Feb 16 2023 Kevin Fenzi <kevin@scrye.com> - 1.32.0-1
- Update to 1.32.0. Fixes rhbz#2170361
 
* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.31.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild
 
* Thu Jan 12 2023 Kevin Fenzi <kevin@scrye.com> - 1.31.1-1
- Update to 1.31.1. Fixes rhbz#2160428
 
* Mon Nov 21 2022 Kevin Fenzi <kevin@scrye.com> - 1.31.0-1
- Update to 1.31.0. Fixes rhbz#2144498
 
* Tue Oct 25 2022 Neal Gompa <ngompa@fedoraproject.org> - 1.30.1-2
- Backport more fixes for kiwibuild command for CBS
 
* Wed Oct 12 2022 Kevin Fenzi <kevin@scrye.com> - 1.30.1-1
- Update to 1.30.1. Fixed rhbz#2133004
 
* Mon Oct 03 2022 Neal Gompa <ngompa@fedoraproject.org> - 1.30.0-3
- Refresh kiwi-build patches to latest versions
 
* Thu Sep 22 2022 Neal Gompa <ngompa@fedoraproject.org> - 1.30.0-2
- Backport fixes for kiwi-build command
 
* Mon Aug 29 2022 Kevin Fenzi <kevin@scrye.com> - 1.30.0-1
- Update to 1.30.0. Fixes rhbz#2122127
 
* Wed Aug 10 2022 Adam Williamson <awilliam@redhat.com> - 1.29.1-4
- Replace PR #3458 with PR #3459 (preferred by upstream)
 
* Tue Aug 09 2022 Adam Williamson <awilliam@redhat.com> - 1.29.1-3
- Backport PR #3458 to fix download-task arch filtering. fixes rhbz#2116674
 
* Wed Jul 20 2022 Adam Williamson <awilliam@redhat.com> - 1.29.1-2
- Backport PR #3445 to fix a koji crash in image builds
 
* Tue Jul 12 2022 Kevin Fenzi <kevin@scrye.com> - 1.29.1-1
- Update to 1.29.1. Fiex rhbz#2106294
 
* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.29.0-2
- Rebuilt for Python 3.11
 
* Fri May 27 2022 Kevin Fenzi <kevin@scrye.com> - 1.29.0-1
- Update to 1.29.0. Fixes rhbz#2090641
 
* Thu Apr 07 2022 Kevin Fenzi <kevin@scrye.com> - 1.28.1-1
- Update to 1.28.1. Fixes rhbz#2072899
 
* Mon Feb 21 2022 Kevin Fenzi <kevin@scrye.com> - 1.28.0-1
- Update to 1.28.0. Fixes rhbz#2056503
 
* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.27.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild
 
* Thu Jan 13 2022 Kevin Fenzi <kevin@scrye.com> - 1.27.1-1
- Update to 1.27.1. Fixes rhbz#2040251
 
* Tue Nov 23 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.27.0-3
- Correct topurl in fedora-config.patch. Fixes rhbz#2025562
 
* Thu Nov 18 2021 Kevin Fenzi <kevin@scrye.com> - 1.27.0-2
- Fix rebasing issue in koji.conf
 
* Thu Nov 18 2021 Kevin Fenzi <kevin@scrye.com> - 1.27.0-1
- Update to 1.27.0. Fixes rhbz#2024552
 
* Sun Oct 10 2021 Kevin Fenzi <kevin@scrye.com> - 1.26.1-1
- Update to 1.26.1. Fixes rhbz#2011804
 
* Fri Sep 10 2021 Carl George <carl@george.computer> - 1.26.0-2
- Remove duplicate dist provides that are now automatic
 
* Wed Aug 25 2021 Kevin Fenzi <kevin@scrye.com> - 1.26.0-1
- Update to 1.26.0. Fixes rhbz#1996614
 
* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.25.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild
 
* Thu Jul 01 2021 Kevin Fenzi <kevin@scrye.com> - 1.25.1-1
- Update to 1.25.1. Fixes rhbz#1978116
 
* Tue Jun 15 2021 Jiri Popelka <jpopelka@redhat.com> - 1.25.0-3
- Python egginfo. Fixes rhbz#1968618
 
* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.25.0-2
- Rebuilt for Python 3.10
 
* Thu May 20 2021 Kevin Fenzi <kevin@scrye.com> - 1.25.0-1
- Update to 1.25.0. Fixes rhbz#1962636
 
* Tue Apr 13 2021 Kevin Fenzi <kevin@scrye.com> - 1.24.1-1
- Update to 1.24.1. Fixes rhbz#1948545
 
* Thu Feb 18 2021 Kevin Fenzi <kevin@scrye.com> - 1.24.0-1
- Update to 1.24.0. Fixes rhbz#1930032
 
* Thu Jan 28 2021 Kevin Fenzi <kevin@scrye.com> - 1.23.1-1
- Update to 1.23.1. Fixes rhbz#1917340
 
* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.23.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild
 
* Sun Jan 17 2021 Igor Raits <ignatenkobrain@fedoraproject.org> - 1.23.0-3
- Fixup compatibility of kojid with koji-hub 1.21
 
* Mon Nov 30 2020 Kevin Fenzi <kevin@scrye.com> - 1.23.0-2
- Fix 32 bit arm install issue. Fixes bug #1894261
 
* Thu Oct 22 2020 Kevin Fenzi <kevin@scrye.com> - 1.23.0-1
- Update to 1.23.0. Fixes bug #1890435
 
* Mon Sep 07 2020 Kevin Fenzi <kevin@scrye.com> - 1.22.1-1
- Update to 1.22.1. Fixes 1876427
 
* Wed Aug 12 2020 Kevin Fenzi <kevin@scrye.com> - 1.22.0-2
- Change Requires to python3-libcomps, the epel8 one doesn't provide python-libcomps
 
* Sun Aug 02 2020 Kevin Fenzi <kevin@scrye.com> - 1.22.0-1
- Update to 1.22.0.
- Remove python2 suppport, move to python3 on everything except epel6/7
 
* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.21.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild
 
* Fri Jun 12 2020 Kevin Fenzi <kevin@scrye.com> - 1.21.1-1
- Update to 1.21.1. (really this time!)
 
* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 1.21.0-3
- Rebuilt for Python 3.9
 
* Thu Apr 30 2020 Kevin Fenzi <kevin@scrye.com> - 1.21.0-2
- Add patch to fix issue with admins not being able to force tagging. 
- Fixes https://pagure.io/koji/issue/2202 upstream.
 
* Tue Apr 21 2020 Kevin Fenzi <kevin@scrye.com> - 1.21.0-1
- Update to 1.21.0. Fixes bug #1826406
 
* Fri Mar 06 2020 Kevin Fenzi <kevin@scrye.com> - 1.20.1-1
- Update to 1.20.0
 
* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild
 
* Mon Jan 20 2020 Kevin Fenzi <kevin@scrye.com> - 1.20.0-1
- Update to 1.20.0.
 
* Wed Nov 27 2019 Kevin Fenzi <kevin@scrye.com> - 1.19.1-2
- Add Requires to koji builder on python3-pycdio/pycdio. Fixes bug #1775536
 
* Fri Nov 08 2019 Kevin Fenzi <kevin@scrye.com> - 1.19.1-1
- Update to 1.19.1
 
* Fri Nov 01 2019 Mohan Boddu <mboddu@bhujji.com> - 1.19.0-1
- Rebase to 1.19.0
- Removing downstream patch 1613
 
* Wed Oct 09 2019 Patrick Uiterwijk <patrick@puiterwijk.org> - 1.18.1-1
- Rebase to 1.18.1 for CVE-2019-17109
 
* Wed Sep 18 2019 Jiri Popelka <jpopelka@redhat.com> - 1.18.0-6
- Fix macro added in previous change.
 
* Tue Sep 17 2019 Kevin Fenzi <kevin@scrye.com> - 1.18.0-5
- Add provides for python3 subpackage. Fixes bug #1750391
 
* Sat Aug 17 2019 Miro Hrončok <mhroncok@redhat.com> - 1.18.0-4
- Rebuilt for Python 3.8
 
* Fri Aug 16 2019 Kevin Fenzi <kevin@scrye.com> - 1.18.0-3
- Fix pkgsurl/topurl default mistake.
 
* Fri Aug 16 2019 Kevin Fenzi <kevin@scrye.com> - 1.18.0-2
- Fix mergerepos conditional for f30.
 
* Fri Aug 16 2019 Kevin Fenzi <kevin@scrye.com> - 1.18.0-1
- Update to 1.18.0.
 
* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild
 
* Thu May 30 2019 Kevin Fenzi <kevin@scrye.com> - 1.17.0-7
- Add patch to fix koji kerberos auth with python3.
- Drop internal mergerepos so we can go all python3. Fixes bug #1715257
 
* Wed May 29 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.17.0-7
- Expose dynamic_buildrequires mock setting
 
* Tue May 28 2019 Kevin Fenzi <kevin@scrye.com> - 1.17.0-6
- Switch kojid back to python3 as imagefactory and oz have moved.
- Backport patch to download only repomd.xml instead of all repodata.
- Backport patch to allow 'bare' repo merging for modularity.
- Backport patch to allow for seperate srpm repos in buildroot repos.
 
* Mon Mar 11 2019 Neal Gompa <ngompa13@gmail.com> - 1.17.0-5
- Switch kojid back to Python 2 so that imgfac doesn't get disabled
 
* Sun Mar 10 2019 Neal Gompa <ngompa13@gmail.com> - 1.17.0-4
- Add patch proposed upstream to use createrepo_c by default to drop yum dependency
 
* Sun Mar 10 2019 Neal Gompa <ngompa13@gmail.com> - 1.17.0-3
- Remove remnants of unused /usr/libexec/koji-hub
 
* Thu Mar 07 2019 Neal Gompa <ngompa13@gmail.com> - 1.17.0-2
- Enable Python 3 for Fedora 30+ and EL8+
- Sync packaging changes from upstream
 
* Thu Mar 07 2019 Patrick Uiterwijk <puiterwijk@redhat.com> - 1.17.0-1
- Rebase to 1.17.0
 
* Thu Feb 21 2019 Patrick Uiterwijk <puiterwijk@redhat.com> - 1.16.2-1
- Rebase to 1.16.2 for CVE-2018-1002161
 
* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild
 
* Wed Jan 09 2019 Adam Williamson <awilliam@redhat.com> - 1.16.1-3
- Backport fix for Python 3 connection failure bug (#1192, PR #1203)
 
* Fri Sep 14 2018 Kevin Fenzi <kevin@scrye.com> - 1.16.1-2
- Fix bad sed that caused python32 dep.
 
* Thu Sep 13 2018 Kevin Fenzi <kevin@scrye.com> - 1.16.1-1
- Update to 1.16.1
 
* Tue Jul 31 2018 Kevin Fenzi <kevin@scrye.com> - 1.16.0-1
- Update to 1.16.0
 
* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild
 
* Mon Jun 18 2018 Miro Hrončok <mhroncok@redhat.com> - 1.15.1-2
- Rebuilt for Python 3.7
 
* Tue Apr 03 2018 Patrick Uiterwijk <puiterwijk@redhat.com> - 1.15.1-1
- Rebase to 1.15.1
- Fixes CVE-2018-1002150
 
* Fri Mar 16 2018 Kevin Fenzi <kevin@scrye.com> - 1.15.0-7
- Backport PR #841 to allow configurable timeout for oz
 
* Tue Feb 20 2018 Patrick Uiterwijk <patrick@puiterwijk.org> - 1.15.0-6
- Backport PR #796
 
* Sun Feb 18 2018 Patrick Uiterwijk <patrick@puiterwijk.org> - 1.15.0-5
- Add  workaround patch for bug #808
 
* Fri Feb 16 2018 Patrick Uiterwijk <patrick@puiterwijk.org> - 1.15.0-4
- Backport patch from PR#794
- Fix macro escaping in comments
 
* Mon Feb 12 2018 Owen Taylor <otaylor@redhat.com> - 1.15.0-3
- Make hub, builder, etc, require python2-koji not koji
 
* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild
 
* Sat Jan 27 2018 Patrick Uiterwijk <patrick@puiterwijk.org> - 1.15.0-1
- Rebase to koji 1.15.0
 
* Mon Jan 22 2018 Troy Dawson <tdawson@redhat.com> - 1.14.0-4
- Update conditional
 
* Thu Dec 07 2017 Patrick Uiterwijk <patrick@puiterwijk.org> - 1.14.0-3
- Backport py3 runroot encoding patch (PR#735)
 
* Mon Dec 04 2017 Patrick Uiterwijk <patrick@puiterwijk.org> - 1.14.0-2
- Backport py3 keytab patch (PR#708)
- Backport patches for exit code (issue#696)
 
* Tue Sep 26 2017 Dennis Gilmore <dennis@ausil.us> - 1.14.0-1
- update to upstream 1.14.0
 
* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild
 
* Wed Jul 12 2017 Patrick Uiterwijk <puiterwijk@redhat.com> - 1.13.0-3
- Remove the 2 postfix for pycurl and libcomps on RHEL
 
* Tue Jul 11 2017 Randy Barlow <bowlofeggs@fedoraproject.org> - 1.13.0-2
- Require python2-koji on Fedora <= 26.
 
* Mon Jul 03 2017 Dennis Gilmore <dennis@ausil.us> - 1.13.0-1
- update to upstream 1.13.0
- remove old  changelog entries