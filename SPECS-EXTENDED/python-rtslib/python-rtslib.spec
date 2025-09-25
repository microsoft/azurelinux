%global oname rtslib-fb

# epydoc is gone, so disable for now
%bcond_with apidocs

Name:             python-rtslib
License:          Apache-2.0
Vendor:           Microsoft Corporation
Distribution:     Azure Linux
Summary:          API for Linux kernel LIO SCSI target
Version:          2.1.76
Release:          10%{?dist}
URL:              https://github.com/open-iscsi/%{oname}
Source0:          %{url}/archive/v%{version}/%{oname}-%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:           0001-disable-xen_pvscsi.patch
Patch1:           0002-rtslib-explicitely-import-kmod.error-and-kmod.Kmod.patch
BuildArch:        noarch
%if %{with apidocs}
BuildRequires:    epydoc
%endif
BuildRequires:    systemd

%global _description\
API for generic Linux SCSI kernel target. Includes the 'target'\
service and targetctl tool for restoring configuration.

%description %_description

%if %{with apidocs}
%package doc
Summary:        Documentation for python-rtslib
Requires:       python3-rtslib = %{version}-%{release}

%description doc
API documentation for rtslib, to configure the generic Linux SCSI
multiprotocol kernel target.
%endif

%package -n python3-rtslib
Summary:        API for Linux kernel LIO SCSI target

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-kmod
BuildRequires:  python3-six
BuildRequires:  python3-pyudev

Requires:       python3-kmod
Requires:       python3-six
Requires:       python3-pyudev
%if ! %{with apidocs}
Obsoletes:      %{name}-doc < %{version}-%{release}
%endif

%description -n python3-rtslib
API for generic Linux SCSI kernel target.

%package -n target-restore
Summary:          Systemd service for targetcli/rtslib
Requires:         python3-rtslib = %{version}-%{release}
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

%description -n target-restore
Systemd service to restore the LIO kernel target settings
on system restart.

%prep
%autosetup -p1 -n %{oname}-%{version}

%build
%py3_build

%if %{with apidocs}
mkdir -p doc/html
epydoc --no-sourcecode --html -n rtslib -o doc/html rtslib/*.py
%endif

%install
# remove py2 scripts if py3 enabled
%py3_install

mkdir -p %{buildroot}%{_mandir}/man8/
mkdir -p %{buildroot}%{_mandir}/man5/
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_sysconfdir}/target/backup
mkdir -p %{buildroot}%{_localstatedir}/target/pr
mkdir -p %{buildroot}%{_localstatedir}/target/alua
install -m 644 systemd/target.service %{buildroot}%{_unitdir}/target.service
install -m 644 doc/targetctl.8 %{buildroot}%{_mandir}/man8/
install -m 644 doc/saveconfig.json.5 %{buildroot}%{_mandir}/man5/

%post -n target-restore
%systemd_post target.service

%preun -n target-restore
%systemd_preun target.service

%postun -n target-restore
%systemd_postun_with_restart target.service


%files -n python3-rtslib
%license COPYING
%{python3_sitelib}/rtslib*
%doc README.md doc/getting_started.md

%files -n target-restore
%{_bindir}/targetctl
%{_unitdir}/target.service
%dir %{_sysconfdir}/target
%dir %{_sysconfdir}/target/backup
%dir %{_localstatedir}/target
%dir %{_localstatedir}/target/pr
%dir %{_localstatedir}/target/alua
%{_mandir}/man8/targetctl.8*
%{_mandir}/man5/saveconfig.json.5*

%if %{with apidocs}
%files doc
%doc doc/html
%endif

%changelog
* Mon Dec 23 2024 Akhila Guruju <v-guakhila@microsoft.com> - 2.1.76-10
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified.

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.76-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 2.1.76-8
- Rebuilt for Python 3.13

* Mon Feb 12 2024 Maurizio Lombardi <mlombard@redhat.com> - 2.1.76-7
- Migrated to SPDX license

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.76-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.76-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Aug 02 2023 Maurizio Lombardi <mlombard@redhat.com> - 2.1.76-4
- Fix kmod import

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.76-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jul 07 2023 Python Maint <python-maint@redhat.com> - 2.1.76-2
- Rebuilt for Python 3.12


* Tue Jun 06 2023 Maurizio Lombardi <mlombard@redhat.com> - 2.1.76-1
- Rebase to version 2.1.76

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.75-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.75-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 2.1.75-2
- Rebuilt for Python 3.11

* Mon May 16 2022 Maurizio Lombardi <mlombard@redhat.com> - 2.1.75-1
- Update to new upstream version

* Wed Mar 30 2022 Maurizio Lombardi <mlombard@redhat.com> - 2.1.74-7
- Add support for cpus_allowed_list attribute

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.74-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.74-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.1.74-4
- Rebuilt for Python 3.10

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.1.74-3
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.74-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Aug 31 2020 Maurizio Lombardi <mlombard@redhat.com> - 2.1.74-1
- New upstream version

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.73-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jun 25 2020 Matt Coleman <matt@datto.com> - 2.1.73-1
- New upstream version
- Use upstream's systemd service

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 2.1.fb69-9
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.fb69-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Nov 01 2019 Neal Gompa <ngompa13@gmail.com> - 2.1.fb69-7
- Fix file list for python3-rtslib subpackage
- Don't compress manpages in build phase, as rpm auto-compresses manpages
- Move systemd requires to the target-restore subpackage
- Disable building apidocs as epydoc is gone

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 2.1.fb69-6
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 2.1.fb69-5
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.fb69-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.fb69-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Oct 12 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.1.fb69-2
- Python2 binary package has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Wed Oct 10 2018 Andy Grover <agrover@redhat.com> - 2.1.fb69-1
- New upstream version
- Fix URL so spectool -g works

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.fb67-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 2.1.fb67-4
- Rebuilt for Python 3.7

* Fri Mar 16 2018 Charalampos Stratakis <cstratak@redhat.com> - 2.1.fb67-3
- Don't build the Python 2 subpackage on EL > 7

* Thu Feb 15 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2.1.fb67-2
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Wed Feb 14 2018 Andy Grover <agrover@redhat.com> - 2.1.fb67-1
- New upstream version

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.fb66-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 31 2018 Andy Grover <agrover@redhat.com> - 2.1.fb66-1
- New upstream version

* Fri Jan 26 2018 Andy Grover <agrover@redhat.com> - 2.1.fb65-1
- New upstream version

* Fri Sep 29 2017 Troy Dawson <tdawson@redhat.com> - 2.1.fb63-4
- Cleanup spec file conditionals

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.1.fb63-3
- Python 2 binary package renamed to python2-rtslib
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.fb63-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Mar 1 2017 Andy Grover <agrover@redhat.com> - 2.1.fb63-1
- New upstream version

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.fb60-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 2.1.fb60-3
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.fb60-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Apr 7 2016 Andy Grover <agrover@redhat.com> - 2.1.fb60-1
- New upstream version

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.fb59-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Dec 11 2015 Andy Grover <agrover@redhat.com> - 2.1.fb59-1
- New upstream version

* Tue Dec 8 2015 Andy Grover <agrover@redhat.com> - 2.1.fb58-2
- Add patch 0001-disable-xen_pvscsi.patch

* Tue Dec 1 2015 Andy Grover <agrover@redhat.com> - 2.1.fb58-1
- New upstream version

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.fb57-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Mon Aug 31 2015 Andy Grover <agrover@redhat.com> - 2.1.fb57-4
- Fix deps for python3 pkg

* Fri Aug 28 2015 Andy Grover <agrover@redhat.com> - 2.1.fb57-3
- Fix an unowned directory

* Tue Aug 18 2015 Andy Grover <agrover@redhat.com> - 2.1.fb57-2
- Move targetctl and scripts to separate 'target-restore' pkg

* Tue Jun 23 2015 Andy Grover <agrover@redhat.com> - 2.1.fb57-1
- New upstream version
- Change from 2to3 to python-six

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.fb53-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Apr 17 2015 Andy Grover <agrover@redhat.com> - 2.1.fb53-1
- New upstream version

* Tue Jan 13 2015 Andy Grover <agrover@redhat.com> - 2.1.fb52-1
- New upstream version

* Tue Dec 2 2014 Andy Grover <agrover@redhat.com> - 2.1.fb51-1
- New upstream version

* Wed Sep 24 2014 Andy Grover <agrover@redhat.com> - 2.1.fb50-1
- New upstream version

* Thu Aug 28 2014 Andy Grover <agrover@redhat.com> - 2.1.fb49-1
- New upstream version

* Fri Jun 20 2014 Andy Grover <agrover@redhat.com> - 2.1.fb48-1
- New upstream version

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.fb47-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 2.1.fb47-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Fri Mar 14 2014 Andy Grover <agrover@redhat.com> - 2.1.fb47-1
- New upstream version

* Tue Feb 18 2014 Andy Grover <agrover@redhat.com> - 2.1.fb46-1
- New upstream version

* Wed Jan 15 2014 Andy Grover <agrover@redhat.com> - 2.1.fb45-1
- New upstream version

* Wed Dec 18 2013 Andy Grover <agrover@redhat.com> - 2.1.fb44-1
- New upstream version

* Wed Dec 4 2013 Andy Grover <agrover@redhat.com> - 2.1.fb43-1
- New upstream version
- Remove rtslib-fix-setup.patch

* Wed Nov 6 2013 Andy Grover <agrover@redhat.com> - 2.1.fb41-3
- Don't overwrite py2 scripts with py3 scripts

* Mon Nov 4 2013 Andy Grover <agrover@redhat.com> - 2.1.fb41-2
- Update rtslib-fix-setup.patch with backported fixups
- Add in missing systemd requires

* Fri Nov 1 2013 Andy Grover <agrover@redhat.com> - 2.1.fb41-1
- New upstream version
- Remove obsolete spec stuff: clean, buildroot
- Add target.service

* Mon Sep 23 2013 Andy Grover <agrover@redhat.com> - 2.1.fb40-1
- New upstream version, fixes restore of mappedluns

* Wed Sep 11 2013 Andy Grover <agrover@redhat.com> - 2.1.fb39-1
- New upstream version, fixes fcoe

* Tue Sep 10 2013 Andy Grover <agrover@redhat.com> - 2.1.fb38-1
- New upstream version

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.fb37-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Andy Grover <agrover@redhat.com> - 2.1.fb37-1
- New upstream version
- License now Apache 2.0

* Tue Jul 2 2013 Andy Grover <agrover@redhat.com> - 2.1.fb36-1
- New upstream version
- Remove fix-tabs.patch

* Fri Jun 7 2013 Andy Grover <agrover@redhat.com> - 2.1.fb35-1
- New upstream version
- add fix-tabs.patch

* Thu May 9 2013 Andy Grover <agrover@redhat.com> - 2.1.fb34-1
- New upstream version

* Thu May 2 2013 Andy Grover <agrover@redhat.com> - 2.1.fb33-1
- New upstream version
- Update source file location

* Tue Apr 16 2013 Andy Grover <agrover@redhat.com> - 2.1.fb32-2
- Add python3 subpackage

* Tue Apr 9 2013 Andy Grover <agrover@redhat.com> - 2.1.fb32-1
- New upstream version

* Tue Feb 26 2013 Andy Grover <agrover@redhat.com> - 2.1.fb30-1
- New upstream version
- Update description and summary
- Remove patch0, upstream doesn't include usb gadget any more

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.fb28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 7 2013 Andy Grover <agrover@redhat.com> - 2.1.fb28-1
- New upstream version

* Wed Jan 2 2013 Andy Grover <agrover@redhat.com> - 2.1.fb27-1
- Specfiles removed upstream, remove handling
- Refresh no-usb.patch

* Thu Dec 20 2012 Andy Grover <agrover@redhat.com> - 2.1.fb26-1
- New upstream release
- Remove kernel dependency
- Remove python-ethtool and python-ipaddr dependencies

* Tue Nov 13 2012 Andy Grover <agrover@redhat.com> - 2.1.fb24-1
- New upstream release

* Tue Oct 30 2012 Andy Grover <agrover@redhat.com> - 2.1.fb23-1
- New upstream release

* Thu Sep 6 2012 Andy Grover <agrover@redhat.com> - 2.1.fb22-1
- New upstream release

* Wed Aug 8 2012 Andy Grover <agrover@redhat.com> - 2.1.fb21-1
- New upstream release

* Tue Aug 7 2012 Andy Grover <agrover@redhat.com> - 2.1.fb20-2
- Add patch no-usb.patch

* Tue Aug 7 2012 Andy Grover <agrover@redhat.com> - 2.1.fb20-1
- New upstream release. Add kernel version dependency.
- Don't claim python_sitelib

* Thu Aug 2 2012 Andy Grover <agrover@redhat.com> - 2.1.fb19-1
- New upstream release. Add kmod dependency.

* Tue Jul 31 2012 Andy Grover <agrover@redhat.com> - 2.1.fb18-1
- New upstream release. Remove configobj dependency

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.fb17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 28 2012 Andy Grover <agrover@redhat.com> - 2.1.fb17-1
- New upstream release
- Remove patch retry-target-creation.patch, upstream has alternate
  fix.

* Tue Jun 12 2012 Andy Grover <agrover@redhat.com> - 2.1.fb15-1
- New upstream release

* Wed May 30 2012 Andy Grover <agrover@redhat.com> - 2.1.fb14-1
- Update Source URL to proper tarball
- Add patch retry-target-creation.patch
- New upstream release

* Mon Apr 9 2012 Andy Grover <agrover@redhat.com> - 2.1.fb13-1
- New upstream release

* Wed Feb 29 2012 Andy Grover <agrover@redhat.com> - 2.1.fb12-2
- Add -doc package of epydoc-generated html docs

* Wed Feb 29 2012 Andy Grover <agrover@redhat.com> - 2.1.fb12-1
- New upstream release

* Tue Feb 21 2012 Andy Grover <agrover@redhat.com> - 2.1.fb11-1
- New upstream release

* Fri Feb 10 2012 Andy Grover <agrover@redhat.com> - 2.1.fb9-1
- New upstream release

* Fri Feb 3 2012 Andy Grover <agrover@redhat.com> - 2.1.fb8-1
- New upstream release

* Tue Jan 24 2012 Andy Grover <agrover@redhat.com> - 2.1.fb7-1
- New upstream release

* Tue Jan 24 2012 Andy Grover <agrover@redhat.com> - 2.1.fb6-1
- New upstream release

* Fri Jan 13 2012 Andy Grover <agrover@redhat.com> - 2.1.fb5-1
- New upstream release

* Fri Jan 13 2012 Andy Grover <agrover@redhat.com> - 2.1.fb4-1
- New upstream release

* Tue Jan 10 2012 Andy Grover <agrover@redhat.com> - 2.1.fb3-1
- New upstream release

* Tue Dec 6 2011 Andy Grover <agrover@redhat.com> - 2.1.fb2-1
- New upstream release

* Tue Dec 6 2011 Andy Grover <agrover@redhat.com> - 2.1.fb1-1
- Change upstream URL
- New upstream release
- Remove upstreamed patches:
  * python-rtslib-git-version.patch
  * python-rtslib-use-ethtool.patch
  * python-rtslib-update-specpath.patch

* Mon Nov 14 2011 Andy Grover <agrover@redhat.com> - 1.99.1.git644eece-8
- Change archive instructions to use gzip -n
- Fix issues raised in Fedora package review (#744349)

* Thu Oct 6 2011 Andy Grover <agrover@redhat.com> - 1.99.1.git644eece-7
- Remove patch
  * python-rtslib-del-unused-specs.patch

* Wed Aug 17 2011 Andy Grover <agrover@redhat.com> - 1.99-6
- Update based on review comments
  - Fully document steps to build archive
  - Remove commented-out extraneous text
  - Remove a repeat in Requires line
  - Update git-version.patch to have proper sha1
  - Change location of fabric spec files to /var/lib/target
- Remove unused specs

* Tue May 10 2011 Andy Grover <agrover@redhat.com> - 1.99-1
- Initial packaging
