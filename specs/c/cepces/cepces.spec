## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 2;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond_without selinux
%global selinux_variants targeted
%global selinuxtype targeted
%global selinux_package_dir %{_datadir}/selinux/packages

%global logdir %{_localstatedir}/log/%{name}
%global modulename %{name}

Name:           cepces
Version:        0.3.17
Release:        %autorelease
Summary:        Certificate Enrollment through CEP/CES

License:        GPL-3.0-or-later
URL:            https://github.com/openSUSE/%{name}
Source0:        https://github.com/openSUSE/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3dist(pytest)

Requires:       python%{python3_pkgversion}-%{name} = %{version}-%{release}
%if %{with selinux}
Requires:       (%{name}-selinux if selinux-policy-%{selinuxtype})
%endif

Recommends:     logrotate

Supplements:    %{name}-certmonger = %{version}-%{release}

%generate_buildrequires
%pyproject_buildrequires

%description
cepces is an application for enrolling certificates through CEP and CES.
It requires certmonger to operate.

Only simple deployments using Microsoft Active Directory Certificate Services
have been tested.

%package -n python%{python3_pkgversion}-%{name}
Summary:        Python part of %{name}
# cepces/krb5/lib.py dynamically loads libgssapi_krb5.so.2
Requires:       krb5-libs
Requires(pre):  krb5-libs
Requires(post): krb5-libs
# Uses keyctl for keyring handling
Recommends:     keyutils
# Uses pinentry for username/password
Recommends:     pinentry
Recommends:     (pinentry-qt6 if plasma-workspace)

%description -n python%{python3_pkgversion}-%{name}
%{name} is an application for enrolling certificates through CEP and CES.
This package provides the Python part for CEP and CES interaction.

%package certmonger
Summary:        certmonger integration for %{name}
Requires(pre):  %{name} = %{version}-%{release}
Requires:       certmonger

%description certmonger
Installing %{name}-certmonger adds %{name} as a CA configuration.
Uninstall revert the action.

%if %{with selinux}
%package selinux
Summary:        SELinux support for %{name}

BuildRequires:  selinux-policy-devel

Requires:       %{name} = %{version}-%{release}
Requires:       selinux-policy-%{selinuxtype}
Requires(post): selinux-policy-%{selinuxtype}

%description selinux
SELinux support for %{name}
#endif with selinux
%endif

%prep
%autosetup -p1

%build
%pyproject_wheel

%if %{with selinux}
# Build the SELinux module(s).
for SELINUXVARIANT in %{selinux_variants}; do
    make %{?_smp_mflags} -C selinux clean all
    mv -v selinux/%{modulename}.pp selinux/%{modulename}-${SELINUXVARIANT}.pp
done
%endif

%install
%pyproject_install
%pyproject_save_files %{name}

install -d -m0755 %{buildroot}%{logdir}

%if %{with selinux}
# Install the SELinux module(s).
rm -fv selinux-files.txt

for SELINUXVARIANT in %{selinux_variants}; do
    install -d -m 755 %{buildroot}%{selinux_package_dir}/${SELINUXVARIANT}
    bzip2 selinux/%{modulename}-${SELINUXVARIANT}.pp
    MODULE_PATH=%{selinux_package_dir}/${SELINUXVARIANT}/%{modulename}.pp.bz2
    install -p -m 644 selinux/%{name}-${SELINUXVARIANT}.pp.bz2 \
      %{buildroot}${MODULE_PATH}

    echo ${MODULE_PATH} >> selinux-files.txt
done
#endif with selinux
%endif

# Configuration files
install -d -m 0755 %{buildroot}%{_sysconfdir}/%{name}/
install -m 644  conf/cepces.conf.dist  %{buildroot}%{_sysconfdir}/%{name}/cepces.conf
install -m 644  conf/logging.conf.dist %{buildroot}%{_sysconfdir}/%{name}/logging.conf

# Default logrotate file
install -d -m 0755 %{buildroot}%{_sysconfdir}/logrotate.d
cat <<EOF>%{buildroot}%{_sysconfdir}/logrotate.d/%{name}
/var/log/%{name}/*.log {
    compress
    delaycompress
    missingok
    rotate 4
}
EOF

%check
%pyproject_check_import
%pytest

%if %{with selinux}
%pre selinux
for SELINUXVARIANT in %{selinux_variants}; do
    %selinux_relabel_pre -s ${SELINUXVARIANT}
done

%post selinux
for SELINUXVARIANT in %{selinux_variants}; do
    MODULE_PATH=%{selinux_package_dir}/${SELINUXVARIANT}/%{modulename}.pp.bz2
    %selinux_modules_install -s ${SELINUXVARIANT} ${MODULE_PATH}
done

%postun selinux
if [ $1 -eq 0 ]; then
    for SELINUXVARIANT in %{selinux_variants}; do
        %selinux_modules_uninstall -s ${SELINUXVARIANT} %{modulename}
    done
fi

%posttrans selinux
for SELINUXVARIANT in %{selinux_variants}; do
    %selinux_relabel_post -s ${SELINUXVARIANT}
done
#endif with selinux
%endif

%post certmonger
# Install the CA into certmonger.
if [[ "$1" == "1" ]]; then
    getcert add-ca -c %{name} \
      -e %{_libexecdir}/certmonger/%{name}-submit --install >/dev/null || :
fi

%preun certmonger
# Remove the CA from certmonger, unless it's an upgrade.
if [[ "$1" == "0" ]]; then
    getcert remove-ca -c %{name} >/dev/null || :
fi

%files
%doc README.rst
%dir %{_sysconfdir}/%{name}/
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %{_sysconfdir}/%{name}/logging.conf
%attr(0700,-,-) %dir %{logdir}
%dir %{_sysconfdir}/logrotate.d
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}

%files -n python%{python3_pkgversion}-%{name} -f %{pyproject_files}
%license LICENSE

%files certmonger
%{_libexecdir}/certmonger/%{name}-submit

%if %{with selinux}
%files selinux -f selinux-files.txt
%endif

%changelog
## START: Generated by rpmautospec
* Wed Apr 22 2026 azldev <azurelinux@microsoft.com> - 0.3.17-2
- Latest state for cepces

* Thu Jan 22 2026 Andreas Schneider <asn@redhat.com> - 0.3.17-1
- Update to version 0.3.17

* Mon Dec 22 2025 Andreas Schneider <asn@redhat.com> - 0.3.16-1
- Update to version 0.3.16

* Tue Dec 09 2025 Andreas Schneider <asn@redhat.com> - 0.3.13-2
- Add missing requirement to krb5-libs

* Tue Dec 09 2025 Andreas Schneider <asn@redhat.com> - 0.3.13-1
- Update to version 0.3.13

* Wed Nov 12 2025 Andreas Schneider <asn@redhat.com> - 0.3.12-1
- Update to version 0.3.12

* Wed Nov 12 2025 Andreas Schneider <asn@redhat.com> - 0.3.11-1
- Update to version 0.3.11

* Mon Oct 20 2025 Andreas Schneider <asn@redhat.com> - 0.3.10-2
- Remove manual Requires

* Fri Oct 17 2025 Andreas Schneider <asn@redhat.com> - 0.3.10-1
- Update to version 0.3.10

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.3.9-11
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.3.9-10
- Rebuilt for Python 3.14.0rc2 bytecode

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.9-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 0.3.9-8
- Rebuilt for Python 3.14

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.9-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Oct 27 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 0.3.9-6
- Avoid tox, use more pyproject macros

* Thu Oct 24 2024 Andreas Schneider <asn@cryptomilk.org> - 0.3.9-5
- Convert to pyproject.toml to fix build with setuptools
- resolves: rhbz#2319622

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.3.9-2
- Rebuilt for Python 3.13

* Tue Mar 19 2024 Andreas Schneider <asn@redhat.com> - 0.3.9-1
- Update to version 0.3.9
  * https://github.com/openSUSE/cepces/releases/tag/v0.3.9

* Fri Feb 09 2024 Andreas Schneider <asn@redhat.com> - 0.3.8-3
- Fix installing cepces-selinux

* Mon Feb 05 2024 Andreas Schneider <asn@redhat.com> - 0.3.8-2
- Require selinux package if selinux is enabled

* Tue Jan 23 2024 Andreas Schneider <asn@redhat.com> - 0.3.8-1
- Update to version 0.3.8
  * https://github.com/openSUSE/cepces/releases/tag/v0.3.8

* Tue Jan 23 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 28 2023 Python Maint <python-maint@redhat.com> - 0.3.7-2
- Rebuilt for Python 3.12

* Wed Jun 28 2023 Andreas Schneider <asn@redhat.com> - 0.3.7-1
- Update to version 0.3.7
  * https://github.com/openSUSE/cepces/releases/tag/v0.3.7

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 0.3.5-8
- Rebuilt for Python 3.12

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Jul 24 2022 Ding-Yi Chen <dchen@redhat.com> - 0.3.5-6
- Review comment #16 addressed
- It make more sense that -selinux and -certmonger depends on main package,
  Not the other round
- Recommends: logrotate
- Supplements: -selinux, -certmonger

* Wed Jul 20 2022 Ding-Yi Chen <dchen@redhat.com> - 0.3.5-5
- Add Pull request #19
- Remove Pull request #17 as it is not accepted
- Review comment #13, #14 addressed

* Mon Jun 27 2022 Ding-Yi Chen <dchen@redhat.com> - 0.3.5-4
- Add Pull request #18
- Replaces kerberos with gssapi
- Replaces requests_kerberos with requests_gssapi

* Fri Jun 24 2022 Ding-Yi Chen <dchen@redhat.com> - 0.3.5-3
- Review comment #4, #7 addressed

* Wed Jun 22 2022 Ding-Yi Chen <dchen@redhat.com> - 0.3.5-2
- Review comment #1 addressed

* Thu Jun 16 2022 Ding-Yi Chen <dchen@redhat.com> - 0.3.5-1
- Initial import to Fedora
- Add logrotate
- Applied patch for https://github.com/openSUSE/cepces/issues/15

* Fri Oct 01 2021 Daniel Uvehag <daniel.uvehag@gmail.com> - 0.3.4-1
- Fix collections deprecation

* Fri Oct 01 2021 Daniel Uvehag <daniel.uvehag@gmail.com> - 0.3.4-1
- Fix collections deprecation

* Mon Jul 29 2019 Daniel Uvehag <daniel.uvehag@gmail.com> - 0.3.3-2
- Add missing log directory

* Mon Jul 29 2019 Daniel Uvehag <daniel.uvehag@gmail.com> - 0.3.3-1
- Update to version 0.3.3-1

* Mon Feb 05 2018 Daniel Uvehag <daniel.uvehag@gmail.com> - 0.3.0-1
- Update to version 0.3.0-1

* Thu Feb 01 2018 Daniel Uvehag <daniel.uvehag@gmail.com> - 0.2.1-1
- Update to version 0.2.1-1

* Mon Jun 27 2016 Daniel Uvehag <daniel.uvehag@gmail.com> - 0.1.0-1
- Initial package.

## END: Generated by rpmautospec
