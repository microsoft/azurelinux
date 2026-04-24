# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%if 0%{?rhel}
%global prefix ipa
%global productname IPA
%global alt_prefix freeipa
%else
# Fedora
%global prefix freeipa
%global productname FreeIPA
%global alt_prefix ipa
%endif
%global debug_package %{nil}
%global python3dir %{_builddir}/python3-%{name}-%{version}-%{release}
%{!?python3_sitelib: %global python3_sitelib %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%global alt_name %{alt_prefix}-healthcheck

%bcond_without tests

Name:           %{prefix}-healthcheck
Version:        0.19
Release: 3%{?dist}
Summary:        Health check tool for %{productname}
BuildArch:      noarch
License:        GPL-3.0-or-later
URL:            https://github.com/freeipa/freeipa-healthcheck
Source0:        https://github.com/freeipa/freeipa-healthcheck/archive/%{version}.tar.gz
Source1:        ipahealthcheck.conf

Patch0001:      0001-Remove-ipaclustercheck.patch

Requires:       %{name}-core = %{version}-%{release}
Requires:       %{prefix}-server
Requires:       python3-ipalib
Requires:       python3-ipaserver
Requires:       python3-lib389 >= 1.4.2.14-1
Requires:       python3-setuptools
# cronie-anacron provides anacron
Requires:       anacron
Requires:       logrotate
Requires(post): systemd-units
Requires:       %{name}-core = %{version}-%{release}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  systemd-devel
%{?systemd_requires}
# packages for make check
%if %{with tests}
BuildRequires:  python3-pytest
BuildRequires:  python3-ipalib
BuildRequires:  python3-ipaserver
%endif
BuildRequires:  python3-lib389
BuildRequires:  python3-libsss_nss_idmap

# Cross-provides for sibling OS
Provides:       %{alt_name} = %{version}
Conflicts:      %{alt_name}
Obsoletes:      %{alt_name} < %{version}

%description
The %{productname} health check tool provides a set of checks to
proactively detect defects in a FreeIPA cluster.


%package -n %{name}-core
Summary: Core plugin system for healthcheck

# so that freeipa-healthcheck-core can work standalone
Requires:       python3-setuptools

# Cross-provides for sibling OS
Provides:       %{alt_name}-core = %{version}
Conflicts:      %{alt_name}-core
Obsoletes:      %{alt_name}-core < %{version}


%description -n %{name}-core
Core plugin system for healthcheck, usable standalone with other
packages.


%prep
%autosetup -p1  -n freeipa-healthcheck-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install

mkdir -p %{buildroot}%{_sysconfdir}/ipahealthcheck
install -m644 %{SOURCE1} %{buildroot}%{_sysconfdir}/ipahealthcheck

mkdir -p %{buildroot}/%{_unitdir}
install -p -m644 %{_builddir}/freeipa-healthcheck-%{version}/systemd/ipa-healthcheck.service %{buildroot}%{_unitdir}
install -p -m644 %{_builddir}/freeipa-healthcheck-%{version}/systemd/ipa-healthcheck.timer %{buildroot}%{_unitdir}

mkdir -p %{buildroot}/%{_libexecdir}/ipa
install -p -m755 %{_builddir}/freeipa-healthcheck-%{version}/systemd/ipa-healthcheck.sh %{buildroot}%{_libexecdir}/ipa/

mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
install -p -m644 %{_builddir}/freeipa-healthcheck-%{version}/logrotate/ipahealthcheck %{buildroot}%{_sysconfdir}/logrotate.d

mkdir -p %{buildroot}/%{_localstatedir}/log/ipa/healthcheck

mkdir -p %{buildroot}/%{_mandir}/man8
mkdir -p %{buildroot}/%{_mandir}/man5
install -p -m644 %{_builddir}/freeipa-healthcheck-%{version}/man/man8/ipa-healthcheck.8  %{buildroot}%{_mandir}/man8/
install -p -m644 %{_builddir}/freeipa-healthcheck-%{version}/man/man5/ipahealthcheck.conf.5  %{buildroot}%{_mandir}/man5/

(cd %{buildroot}/%{python3_sitelib}/ipahealthcheck && find . -type f  | \
    grep -v '^./core' | \
    grep -v 'opt-1' | \
    sed -e 's,\.py.*$,.*,g' | sort -u | \
    sed -e 's,\./,%%{python3_sitelib}/ipahealthcheck/,g' ) >healthcheck.list


%if %{with tests}
%check
PYTHONPATH=src PATH=$PATH:$RPM_BUILD_ROOT/usr/bin pytest-3 tests/test_*
%endif


%post
%systemd_post ipa-healthcheck.service


%preun
%systemd_preun ipa-healthcheck.service


%postun
%systemd_postun_with_restart ipa-healthcheck.service


%files -f healthcheck.list
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc README.md
%{_bindir}/ipa-healthcheck
%dir %{_sysconfdir}/ipahealthcheck
%dir %{_localstatedir}/log/ipa/healthcheck
%config(noreplace) %{_sysconfdir}/ipahealthcheck/ipahealthcheck.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/ipahealthcheck
%{python3_sitelib}/ipahealthcheck-%{version}.dist-info/
%{python3_sitelib}/ipahealthcheck-%{version}-*-nspkg.pth
%{_unitdir}/*
%{_libexecdir}/*
%{_mandir}/man8/*
%{_mandir}/man5/*


%files -n %{name}-core
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc README.md
%{python3_sitelib}/ipahealthcheck/core/


%changelog
* Fri Oct 31 2025 Rob Crittenden <rcritten@redhat.com> - 0.19-2
- Added Requires on python3-setuptools to the core subpackage

* Mon Sep 22 2025 Rob Crittenden <rcritten@redhat.com> - 0.19-1
- Update to 0.19 release

* Tue Sep 02 2025 Rob Crittenden <rcritten@redhat.com> - 0.18-7
- Add a dependency on python3-setuptools to fix the broken package while we
  work on replacing it.

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.18-6
- Rebuilt for Python 3.14.0rc2 bytecode

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.18-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 08 2025 Rob Crittenden <rcritten@redhat.com> - 0.18-4
- Stop using deprecated python build/install macros (#2377261)

* Wed Jun 04 2025 Python Maint <python-maint@redhat.com> - 0.18-3
- Rebuilt for Python 3.14

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 0.18-2
- Bootstrap for Python 3.14

* Tue May 06 2025 Rob Crittenden <rcritten@redhat.com> - 0.18-1
- Update to 0.18 release

* Mon Jan 20 2025 Rob Crittenden <rcritten@redhat.com> - 0.17-6
- Upstream patch to fix python-cryptography 42+ deprecation errors from
  ipalib/x509.py

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 10 2024 Python Maint <python-maint@redhat.com> - 0.17-3
- Rebuilt for Python 3.13

* Mon Jun 10 2024 Python Maint <python-maint@redhat.com> - 0.17-2
- Bootstrap for Python 3.13

* Mon Jun 03 2024 Rob Crittenden <rcritten@redhat.com> - 0.17-1
- Update to 0.17 release

* Wed Feb 14 2024 Rob Crittenden <rcritten@redhat.com> - 0.16-5
- Skip DogtagCertsConfigCheck for PKI versions >= 11.5.0

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Nov 14 2023 Rob Crittenden <rcritten@redhat.com> - 0.16-2
- Don't fail if a service name cannot be looked up in LDAP
- Disable the ipa-ods-exporter service check

* Wed Nov  8 2023 Rob Crittenden <rcritten@redhat.com> - 0.16-1
- Update to 0.16 release
- This fixes pki-healthcheck

* Tue Nov  7 2023 Rob Crittenden <rcritten@redhat.com> - 0.15-1
- Update to 0.15 release

* Mon Aug 21 2023 Rob Crittenden <rcritten@redhat.com> - 0.14-1
- Update to 0.14 release

* Wed Jul 19 2023 Rob Crittenden <rcritten@redhat.com> - 0.13-1
- Update to 0.13 release

* Thu Jun 29 2023 Python Maint <python-maint@redhat.com> - 0.12-5
- Rebuilt for Python 3.12

* Wed Jun 28 2023 Python Maint <python-maint@redhat.com> - 0.12-4
- Bootstrap for Python 3.12

* Wed Mar 29 2023 Rob Crittenden <rcritten@redhat.com> - 0.12-3
- Migrated to SPDX license

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Dec  1 2022 Rob Crittenden <rcritten@redhat.com> - 0.12
- Update to 0.12 release

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jun 16 2022 Python Maint <python-maint@redhat.com> - 0.11-4
- Rebuilt for Python 3.11

* Thu Jun 16 2022 Python Maint <python-maint@redhat.com> - 0.11-3
- Bootstrap for Python 3.11

* Mon Jun 06 2022 Rob Crittenden <rcritten@redhat.com> - 0.11-2
- Don't WARN on KDC workers if cpus == 1 and KRB5KDC_ARGS is empty

* Thu Jun 02 2022 Rob Crittenden <rcritten@redhat.com> - 0.11-1
- Update to 0.11 release

* Tue Feb  8 2022 Rob Crittenden <rcritten@redhat.com> - 0.10-1
- Update to 0.10 release

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jun 14 2021 Rob Crittenden <rcritten@redhat.com> - 0.9-2
- FileCheck would raise a CRITICAL for non-existent files

* Tue Jun  8 2021 Rob Crittenden <rcritten@redhat.com> - 0.9-1
- Update to upstream 0.9
- Fix bad date in 0.8-6.1 changelog entry

* Mon Jun 07 2021 Python Maint <python-maint@redhat.com> - 0.8-8.1
- Rebuilt for Python 3.10

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.8-7.1
- Bootstrap for Python 3.10

* Thu Apr 15 2021 Rob Crittenden <rcritten@redhat.com> - 0.8-6.1
- Switch from tox to pytest as the test runner. tox is being deprecated
  in some distros.

* Mon Mar  8 2021 François Cami <fcami@redhat.com> - 0.8-6
- Make the spec file distribution-agnostic (rhbz#1935773).

* Tue Mar  2 2021 Alexander Scheel <ascheel@redhat.com> - 0.8-5
- Make the spec file more distribution-agnostic
- Use tox as the test runner when tests are enabled

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.8-4
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 18 2021 Rob Crittenden <rcritten@redhat.com> - 0.8-2
- A bad file group was reported as a python list, not a string

* Wed Jan 13 2021 Rob Crittenden <rcritten@redhat.com> - 0.8-1
- Update to upstream 0.8
- Fix FTBFS in F34/rawhide (#1915256)

* Wed Dec 16 2020 Rob Crittenden <rcritten@redhat.com> - 0.7-3
- Include upstream patch to fix parsing input from json files

* Tue Nov 17 2020 Rob Crittenden <rcritten@redhat.com> - 0.7-2
- Include upstream patch to fix collection of AD trust domains
- Include upstream patch to fix failing not-valid-after test

* Thu Oct 29 2020 Rob Crittenden <rcritten@redhat.com> - 0.7-1
- Update to upstream 0.7

* Wed Jul 29 2020 Rob Crittenden <rcritten@redhat.com> - 0.6-4
- Set minimum Requires on python3-lib389
- Don't assume that all users of healthcheck-core provide the same
  set of options.

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 24 2020 Rob Crittenden <rcritten@redhat.com> - 0.6-2
- Don't collect IPA servers in MetaCheck
- Skip if dirsrv not available in IPAMetaCheck

* Wed Jul  1 2020 Rob Crittenden <rcritten@redhat.com> - 0.6-1
- Update to upstream 0.6
- Don't include cluster checking yet

* Tue Jun 23 2020 Rob Crittenden <rcritten@redhat.com> - 0.5-5
- Add BuildRequires on python3-setuptools

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.5-4
- Rebuilt for Python 3.9

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 27 2020 Rob Crittenden <rcritten@redhat.com> - 0.5-2
- Rebuild

* Thu Jan  2 2020 Rob Crittenden <rcritten@redhat.com> - 0.5-1
- Update to upstream 0.5

* Mon Dec 2 2019 François Cami <fcami@redhat.com> - 0.4-2
- Create subpackage to split out core processing (#1771710)

* Mon Dec 2 2019 François Cami <fcami@redhat.com> - 0.4-1
- Update to upstream 0.4
- Change Source0 to something "spectool -g" can use. 
- Correct URL (#1773512)
- Errors not translated to strings (#1752849)
- JSON output not indented by default (#1729043)
- Add dependencies to checks to avoid false-positives (#1727900)
- Verify expected DNS records (#1695125

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.3-3
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.3-2
- Rebuilt for Python 3.8

* Thu Jul 25 2019 François Cami <fcami@redhat.com> - 0.3-1
- Update to upstream 0.3
- Add logrotate configs + depend on anacron and logrotate

* Thu Jul 25 2019 François Cami <fcami@redhat.com> - 0.2-6
- Fix permissions

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jul 11 2019 François Cami <fcami@redhat.com> - 0.2-4
- Fix ipa-healthcheck.sh installation path (rhbz#1729188)
- Create and own log directory (rhbz#1729188)

* Tue Apr 30 2019 François Cami <fcami@redhat.com> - 0.2-3
- Add python3-lib389 to BRs

* Tue Apr 30 2019 François Cami <fcami@redhat.com> - 0.2-2
- Fix changelog

* Thu Apr 25 2019 Rob Crittenden <rcritten@redhat.com> - 0.2-1
- Update to upstream 0.2

* Thu Apr 4 2019 François Cami <fcami@redhat.com> - 0.1-2
- Explicitly list dependencies

* Tue Apr 2 2019 François Cami <fcami@redhat.com> - 0.1-1
- Initial package import
