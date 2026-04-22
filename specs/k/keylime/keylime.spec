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

%global policy_version 43.1.1

%global with_selinux 1
%global selinuxtype targeted

Name:    keylime
Version: 7.14.1
Release: %autorelease
Summary: Open source TPM software for Bootstrapping and Maintaining Trust

URL:            https://github.com/keylime/keylime
Source0:        https://github.com/keylime/keylime/archive/refs/tags/v%{version}.tar.gz
# The selinux policy for keylime is distributed via this repo: https://github.com/RedHat-SP-Security/keylime-selinux
Source1:        https://github.com/RedHat-SP-Security/%{name}-selinux/archive/v%{policy_version}/keylime-selinux-%{policy_version}.tar.gz
Source2:        %{name}.sysusers
Source3:        %{name}.tmpfiles

Patch: 0001-Fix-timestamp-conversion-to-use-UTC-timezone.patch
Patch: 0002-Fix-efivar-availability-check-in-test_create_mb_poli.patch

# Main program: Apache-2.0
# Icons: MIT
License: Apache-2.0 AND MIT

BuildArch: noarch

BuildRequires: git-core
BuildRequires: openssl
BuildRequires: openssl-devel
BuildRequires: python3-devel
BuildRequires: python3-dbus
BuildRequires: python3-jinja2
BuildRequires: python3-cryptography
BuildRequires: python3-docutils
BuildRequires: python3-gpg
BuildRequires: python3-pip
BuildRequires: python3-pyasn1
BuildRequires: python3-pyasn1-modules
BuildRequires: python3-requests
BuildRequires: python3-tornado
BuildRequires: python3-sqlalchemy
BuildRequires: python3-lark-parser
BuildRequires: python3-psutil
BuildRequires: python3-pyyaml
BuildRequires: python3-jsonschema
BuildRequires: python3-setuptools
BuildRequires: systemd-rpm-macros
BuildRequires: rpm-sign
BuildRequires: createrepo_c
BuildRequires: tpm2-tools

Requires: python3-%{name} = %{version}-%{release}
Requires: %{name}-base = %{version}-%{release}
Requires: %{name}-verifier = %{version}-%{release}
Requires: %{name}-registrar = %{version}-%{release}
Requires: %{name}-tenant = %{version}-%{release}
Requires: %{name}-tools = %{version}-%{release}

# webapp was removed upstream in release 6.4.2.
Obsoletes: %{name}-webapp < 6.4.2

# python agent was removed upstream in release 7.0.0.
Obsoletes: python3-%{name}-agent < 7.0.0

# Agent.
Requires: keylime-agent
Suggests: %{name}-agent-rust

# Conflicts with the monolithic versions of the package, before the split.
Conflicts: keylime < 6.3.0-3

%{?python_enable_dependency_generator}
%description
Keylime is a TPM based highly scalable remote boot attestation
and runtime integrity measurement solution.

%package base
Summary: The base package contains the default configuration
License: MIT

# Conflicts with the monolithic versions of the package, before the split.
Conflicts: keylime < 6.3.0-3

Requires(pre): python3-jinja2
Requires: procps-ng
Requires: tpm2-tss
Requires: openssl

%if 0%{?with_selinux}
# This ensures that the *-selinux package and all it’s dependencies are not pulled
# into containers and other systems that do not use SELinux
Recommends:       (%{name}-selinux = %{version}-%{release} if selinux-policy-%{selinuxtype})
%endif

# This generates lines like 'Requires: (efivar-libs if filesystem(aarch64))'.
# We need to transform x86_64 into x86-64, hence the gsub.
%{lua:
  for i in string.gmatch(rpm.expand("%efi"):gsub("_","-"), "%S+") do
    print('Requires: (efivar-libs if filesystem('..i..'))\n')
  end
}

%description base
The base package contains the Keylime default configuration

%package -n python3-%{name}
Summary: The Python Keylime module
License: MIT

# Conflicts with the monolithic versions of the package, before the split.
Conflicts: keylime < 6.3.0-3

Requires: %{name}-base = %{version}-%{release}
%{?python_provide:%python_provide python3-%{name}}

Requires: python3-tornado
Requires: python3-sqlalchemy
Requires: python3-alembic
Requires: python3-cryptography
Requires: python3-pyyaml
Requires: python3-packaging
Requires: python3-requests
Requires: python3-gpg
Requires: python3-lark
Requires: python3-pyasn1
Requires: python3-pyasn1-modules
Requires: python3-psutil
Requires: python3-jsonschema
Requires: python3-typing-extensions
Requires: tpm2-tools

%description -n python3-%{name}
The python3-keylime module implements the functionality used
by Keylime components.

%package verifier
Summary: The Python Keylime Verifier component
License: MIT

# Conflicts with the monolithic versions of the package, before the split.
Conflicts: keylime < 6.3.0-3

Requires: %{name}-base = %{version}-%{release}
Requires: python3-%{name} = %{version}-%{release}

%description verifier
The Keylime Verifier continuously verifies the integrity state
of the machine that the agent is running on.

%package registrar
Summary: The Keylime Registrar component
License: MIT

# Conflicts with the monolithic versions of the package, before the split.
Conflicts: keylime < 6.3.0-3

Requires: %{name}-base = %{version}-%{release}
Requires: python3-%{name} = %{version}-%{release}

%description registrar
The Keylime Registrar is a database of all agents registered
with Keylime and hosts the public keys of the TPM vendors.

%if 0%{?with_selinux}
# SELinux subpackage
%package selinux
Summary:             keylime SELinux policy
Requires:            selinux-policy-%{selinuxtype}
Requires(post):      selinux-policy-%{selinuxtype}
BuildRequires:       selinux-policy-devel
%{?selinux_requires}

%description selinux
Custom SELinux policy module
%endif

%package tenant
Summary: The Python Keylime Tenant
License: MIT

# Conflicts with the monolithic versions of the package, before the split.
Conflicts: keylime < 6.3.0-3

Requires: %{name}-base = %{version}-%{release}
Requires: python3-%{name} = %{version}-%{release}


%description tenant
The Keylime Tenant can be used to provision a Keylime Agent.

%package tools
Summary: Keylime tools
License: MIT

# Conflicts with the monolithic versions of the package, before the split.
Conflicts: keylime < 6.3.0-3

Requires: %{name}-base = %{version}-%{release}
Requires: python3-%{name} = %{version}-%{release}

%description tools
The keylime tools package includes miscelaneous tools.


%prep
%autosetup -S git -n %{name}-%{version} -a1

%build
%if 0%{?with_selinux}
# SELinux policy (originally from selinux-policy-contrib)
# this policy module will override the production module

make -f %{_datadir}/selinux/devel/Makefile %{name}.pp
bzip2 -9 %{name}.pp
%endif

%pyproject_wheel

mkdir -p manpages
rst2man --syntax-highlight=none docs/man/keylime_tenant.1.rst manpages/keylime_tenant.1
rst2man --syntax-highlight=none docs/man/keylime-policy.1.rst manpages/keylime-policy.1
rst2man --syntax-highlight=none docs/man/keylime_registrar.8.rst manpages/keylime_registrar.8
rst2man --syntax-highlight=none docs/man/keylime_verifier.8.rst manpages/keylime_verifier.8

%install
%pyproject_install
mkdir -p %{buildroot}/%{_sharedstatedir}/%{name}
mkdir -p --mode=0700 %{buildroot}/%{_rundir}/%{name}

mkdir -p --mode=0700 %{buildroot}/%{_sysconfdir}/%{name}/
for comp in "verifier" "tenant" "registrar" "ca" "logging"; do
    mkdir -p --mode=0700  %{buildroot}/%{_sysconfdir}/%{name}/${comp}.conf.d
    install -Dpm 400 config/${comp}.conf %{buildroot}/%{_sysconfdir}/%{name}
done

# Ship some scripts.
mkdir -p %{buildroot}/%{_datadir}/%{name}/scripts
for s in create_runtime_policy.sh \
         create_mb_refstate \
         ek-openssl-verify \
         keylime_oneshot_attestation; do
    install -Dpm 755 scripts/${s} \
        %{buildroot}/%{_datadir}/%{name}/scripts/${s}
done

# Ship configuration templates.
cp -r ./templates %{buildroot}%{_datadir}/%{name}/templates/

mkdir -p --mode=0755 %{buildroot}/%{_bindir}
install -Dpm 755 ./keylime/cmd/convert_config.py %{buildroot}/%{_bindir}/keylime_upgrade_config

%if 0%{?with_selinux}
install -D -m 0644 %{name}.pp.bz2 %{buildroot}%{_datadir}/selinux/packages/%{selinuxtype}/%{name}.pp.bz2
install -D -p -m 0644 keylime-selinux-%{policy_version}/%{name}.if %{buildroot}%{_datadir}/selinux/devel/include/distributed/%{name}.if
%endif

install -Dpm 644 ./services/%{name}_verifier.service \
    %{buildroot}%{_unitdir}/%{name}_verifier.service

install -Dpm 644 ./services/%{name}_registrar.service \
    %{buildroot}%{_unitdir}/%{name}_registrar.service

# TPM cert store is deployed to both /usr/share/keylime/tpm_cert_store
# and then /var/lib/keylime/tpm_cert_store.
for cert_store_dir in %{_datadir} %{_sharedstatedir}; do
    mkdir -p %{buildroot}/"${cert_store_dir}"/%{name}
    cp -r ./tpm_cert_store %{buildroot}/"${cert_store_dir}"/%{name}/
done

# Install the sysusers + tmpfiles.d configuration.
install -p -D -m 0644 %{SOURCE2} %{buildroot}/%{_sysusersdir}/%{name}.conf
install -p -D -m 0644 %{SOURCE3} %{buildroot}/%{_tmpfilesdir}/%{name}.conf

# Install manpages
install -d %{buildroot}%{_mandir}/man1
install -d %{buildroot}%{_mandir}/man8
install -m 644 manpages/keylime_tenant.1 %{buildroot}%{_mandir}/man1/
install -m 644 manpages/keylime-policy.1 %{buildroot}%{_mandir}/man1/
install -m 644 manpages/keylime_registrar.8 %{buildroot}%{_mandir}/man8/
install -m 644 manpages/keylime_verifier.8 %{buildroot}%{_mandir}/man8/

%pyproject_save_files -l %{name}

%check
# Create the default configuration files to be used by the tests.
# Also set the associated environment variables so that the tests
# will actually use them.
CONF_TEMP_DIR="$(mktemp -d)"

%{python3} -m keylime.cmd.convert_config --out "${CONF_TEMP_DIR}" --templates templates/
export KEYLIME_VERIFIER_CONFIG="${CONF_TEMP_DIR}/verifier.conf"
export KEYLIME_TENANT_CONFIG="${CONF_TEMP_DIR}/tenant.conf"
export KEYLIME_REGISTRAR_CONFIG="${CONF_TEMP_DIR}/registrar.conf"
export KEYLIME_CA_CONFIG="${CONF_TEMP_DIR}/ca.conf"
export KEYLIME_LOGGING_CONFIG="${CONF_TEMP_DIR}/logging.conf"

# Run the tests.
%{python3} -m unittest

# Cleanup.
[ "${CONF_TEMP_DIR}" ] && rm -rf "${CONF_TEMP_DIR}"
for e in KEYLIME_VERIFIER_CONFIG \
         KEYLIME_TENANT_CONFIG \
         KEYLIME_REGISTRAR_CONFIG \
         KEYLIME_CA_CONFIG \
         KEYLIME_LOGGING_CONFIG; do
    unset "${e}"
done
exit 0

%pre base
%sysusers_create_compat %{SOURCE2}
exit 0

%post base
for c in ca logging; do
    [ -e /etc/keylime/"${c}.conf" ] || continue
    /usr/bin/keylime_upgrade_config --component "${c}" \
                                    --input /etc/keylime/"${c}.conf" \
                                    >/dev/null
done
exit 0

%posttrans base
if [ -d %{_sysconfdir}/%{name} ]; then
    chmod 500 %{_sysconfdir}/%{name}
    chown -R %{name}:%{name} %{_sysconfdir}/%{name}

    for comp in "verifier" "tenant" "registrar" "ca" "logging"; do
        [ -d %{_sysconfdir}/%{name}/${comp}.conf.d ] && \
            chmod 500 %{_sysconfdir}/%{name}/${comp}.conf.d
    done
fi

[ -d %{_sharedstatedir}/%{name} ] && \
    chown -R %{name} %{_sharedstatedir}/%{name}/

[ -d %{_sharedstatedir}/%{name}/tpm_cert_store ] && \
    chmod 400 %{_sharedstatedir}/%{name}/tpm_cert_store/*.pem && \
    chmod 500 %{_sharedstatedir}/%{name}/tpm_cert_store/

[ -d %{_localstatedir}/log/%{name} ] && \
    chown -R %{name} %{_localstatedir}/log/%{name}/
exit 0

%post verifier
[ -e /etc/keylime/verifier.conf ] && \
    /usr/bin/keylime_upgrade_config --component verifier \
                                    --input /etc/keylime/verifier.conf \
                                    >/dev/null
%systemd_post %{name}_verifier.service
exit 0

%post registrar
[ -e /etc/keylime/registrar.conf ] && \
    /usr/bin/keylime_upgrade_config --component registrar \
                                    --input /etc/keylime/registrar.conf /
                                    >/dev/null
%systemd_post %{name}_registrar.service
exit 0

%post tenant
[ -e /etc/keylime/tenant.conf ] && \
    /usr/bin/keylime_upgrade_config --component tenant \
                                    --input /etc/keylime/tenant.conf \
                                    >/dev/null
exit 0

%preun verifier
%systemd_preun %{name}_verifier.service

%preun registrar
%systemd_preun %{name}_registrar.service

%postun verifier
%systemd_postun_with_restart %{name}_verifier.service

%postun registrar
%systemd_postun_with_restart %{name}_registrar.service

%if 0%{?with_selinux}
# SELinux contexts are saved so that only affected files can be
# relabeled after the policy module installation
%pre selinux
%selinux_relabel_pre -s %{selinuxtype}

%post selinux
%selinux_modules_install -s %{selinuxtype} %{_datadir}/selinux/packages/%{selinuxtype}/%{name}.pp.bz2
%selinux_relabel_post -s %{selinuxtype}

if [ "$1" -le "1" ]; then # First install
    # The services need to be restarted for the custom label to be
    # applied in case they where already present in the system,
    # restart fails silently in case they where not.
    for svc in registrar verifier; do
        [ -f "%{_unitdir}/%{name}_${svc}".service ] && \
            %systemd_postun_with_restart "%{name}_${svc}".service
    done
fi
exit 0

%postun selinux
if [ $1 -eq 0 ]; then
    %selinux_modules_uninstall -s %{selinuxtype} %{name}
    %selinux_relabel_post -s %{selinuxtype}
fi
%endif

%files verifier
%license LICENSE
%attr(500,%{name},%{name}) %dir %{_sysconfdir}/%{name}/verifier.conf.d
%config(noreplace) %verify(not md5 size mode mtime) %attr(400,%{name},%{name}) %{_sysconfdir}/%{name}/verifier.conf
%{_bindir}/%{name}_verifier
%{_bindir}/%{name}_ca
%{_unitdir}/keylime_verifier.service
%{_mandir}/man8/keylime_verifier.8*

%files registrar
%license LICENSE
%attr(500,%{name},%{name}) %dir %{_sysconfdir}/%{name}/registrar.conf.d
%config(noreplace) %verify(not md5 size mode mtime) %attr(400,%{name},%{name}) %{_sysconfdir}/%{name}/registrar.conf
%{_bindir}/%{name}_registrar
%{_unitdir}/keylime_registrar.service
%{_mandir}/man8/keylime_registrar.8*

%if 0%{?with_selinux}
%files selinux
%{_datadir}/selinux/packages/%{selinuxtype}/%{name}.pp.*
%{_datadir}/selinux/devel/include/distributed/%{name}.if
%ghost %verify(not md5 size mode mtime) %{_sharedstatedir}/selinux/%{selinuxtype}/active/modules/200/%{name}
%endif

%files tenant
%license LICENSE
%attr(500,%{name},%{name}) %dir %{_sysconfdir}/%{name}/tenant.conf.d
%config(noreplace) %verify(not md5 size mode mtime) %attr(400,%{name},%{name}) %{_sysconfdir}/%{name}/tenant.conf
%{_bindir}/%{name}_tenant
%{_mandir}/man1/keylime_tenant.1*

%files -n python3-%{name} -f %{pyproject_files}
%license LICENSE
%{_datadir}/%{name}/scripts/create_mb_refstate
%{_bindir}/keylime_attest
%{_bindir}/keylime_convert_runtime_policy
%{_bindir}/keylime_create_policy
%{_bindir}/keylime_sign_runtime_policy
%{_bindir}/keylime-policy
%{_mandir}/man1/keylime-policy.1*


%files tools
%license LICENSE
%{_bindir}/%{name}_userdata_encrypt

%files base
%license LICENSE
%doc README.md
%attr(500,%{name},%{name}) %dir %{_sysconfdir}/%{name}
%attr(500,%{name},%{name}) %dir %{_sysconfdir}/%{name}/{ca,logging}.conf.d
%config(noreplace) %verify(not md5 size mode mtime) %attr(400,%{name},%{name}) %{_sysconfdir}/%{name}/ca.conf
%config(noreplace) %verify(not md5 size mode mtime) %attr(400,%{name},%{name}) %{_sysconfdir}/%{name}/logging.conf
%attr(700,%{name},%{name}) %dir %{_rundir}/%{name}
%attr(700,%{name},%{name}) %dir %{_sharedstatedir}/%{name}
%attr(755,root,root) %dir %{_datadir}/%{name}/tpm_cert_store
%attr(644,root,root) %{_datadir}/%{name}/tpm_cert_store/*.pem
%attr(500,%{name},%{name}) %dir %{_sharedstatedir}/%{name}/tpm_cert_store
%attr(400,%{name},%{name}) %{_sharedstatedir}/%{name}/tpm_cert_store/*.pem
%{_tmpfilesdir}/%{name}.conf
%{_sysusersdir}/%{name}.conf
%{_datadir}/%{name}/scripts/create_runtime_policy.sh
%{_datadir}/%{name}/scripts/ek-openssl-verify
%{_datadir}/%{name}/scripts/keylime_oneshot_attestation
%{_datadir}/%{name}/templates
%{_bindir}/keylime_upgrade_config

%files
%license LICENSE

%changelog
## START: Generated by rpmautospec
* Wed Apr 22 2026 azldev <azurelinux@microsoft.com> - 7.14.1-2
- Latest state for keylime

* Fri Feb 13 2026 Sergio Correia <scorreia@redhat.com> - 7.14.1-1
- Updating for Keylime release v7.14.1

* Sat Feb 07 2026 Sergio Correia <scorreia@redhat.com> - 7.13.1-1
- Updating for Keylime release v7.13.1

* Mon Sep 29 2025 Sergio Correia <scorreia@redhat.com> - 7.13.0-2
- Update e2e tests

* Mon Sep 29 2025 Sergio Correia <scorreia@redhat.com> - 7.13.0-1
- Updating for Keylime release v7.13.0

* Mon Sep 29 2025 Sergio Correia <scorreia@redhat.com> - 7.12.1-8
- Stop using deprecated %%py3_build/%%py3_install macros

* Mon Sep 29 2025 Sergio Correia <scorreia@redhat.com> - 7.12.1-7
- Update SELinux policy to v42.1.2

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 7.12.1-6
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 7.12.1-5
- Rebuilt for Python 3.14.0rc2 bytecode

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 7.12.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 7.12.1-3
- Rebuilt for Python 3.14

* Sat Feb 22 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 7.12.1-2
- Drop call to %%sysusers_create_compat

* Thu Feb 20 2025 Sergio Correia <scorreia@redhat.com> - 7.12.1-1
- Updating for Keylime release v7.12.1

* Wed Feb 19 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 7.11.0-9
- Make package noarch

* Wed Feb 19 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 7.11.0-8
- Remove unnecessary macro

* Wed Feb 19 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 7.11.0-7
- Drop call to %%sysusers_create_compat

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 7.11.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Oct 11 2024 Sergio Correia <scorreia@redhat.com> - 7.11.0-5
- Update keylime-selinux to v40.1.0

* Fri Oct 11 2024 Sergio Correia <scorreia@redhat.com> - 7.11.0-4
- Backport revocation_notifier: Use web_util to generate TLS context

* Tue Sep 10 2024 Sergio Correia <scorreia@redhat.com> - 7.11.0-3
- Backport fixes for certificate generation to follow RFC 5280

* Mon Sep 09 2024 Sergio Correia <scorreia@redhat.com> - 7.11.0-2
- Update e2e tests

* Sun Sep 08 2024 Sergio Correia <scorreia@redhat.com> - 7.11.0-1
- Updating for Keylime release v7.11.0

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.10.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 7.10.0-4
- Rebuilt for Python 3.13

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 7.10.0-3
- Rebuilt for Python 3.13

* Tue Apr 30 2024 Miro Hrončok <miro@hroncok.cz> - 7.10.0-2
- Require python3-lark instead of python3-lark-parser

* Tue Mar 26 2024 Sergio Correia <scorreia@redhat.com> - 7.10.0-1
- Updating for Keylime release v7.10.0

* Mon Mar 25 2024 Nils Philippsen <nils@redhat.com> - 7.9.0-5
- Revert constraining SQLAlchemy version

* Thu Mar 21 2024 Nils Philippsen <nils@redhat.com> - 7.9.0-4
- Require SQLAlchemy < 2

* Mon Feb 12 2024 Sergio Correia <scorreia@redhat.com> - 7.9.0-2
- Fixes for rawhide

* Tue Jan 30 2024 Sergio Correia <scorreia@redhat.com> - 7.9.0-1
- Updating for Keylime release v7.9.0
- Migrated license to SPDX

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Dec 05 2023 Sergio Correia <scorreia@redhat.com> - 7.8.0-1
- Updating for Keylime release v7.8.0

* Thu Nov 02 2023 Sergio Correia <scorreia@redhat.com> - 7.7.0-1
- Updating for Keylime release v7.7.0

* Thu Aug 24 2023 Sergio Correia <scorreia@redhat.com> - 7.5.0-1
- Updating for Keylime release v7.5.0

* Mon Jul 31 2023 Sergio Correia <scorreia@redhat.com> - 7.3.0-1
- Updating for Keylime release v7.3.0

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 7.2.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 7.2.5-3
- Rebuilt for Python 3.12

* Tue Jun 06 2023 Sergio Correia <scorreia@redhat.com> - 7.2.5-2
- Update test plan

* Mon Jun 05 2023 Sergio Correia <scorreia@redhat.com> - 7.2.5-1
- Updating for Keylime release v7.2.5

* Fri Feb 03 2023 Sergio Correia <scorreia@redhat.com> - 6.6.0-1
- Updating for Keylime release v6.6.0

* Wed Jan 25 2023 Sergio Correia <scorreia@redhat.com> - 6.5.3-2
- e2e tests: do not change the tpm hash alg to sha256

* Wed Jan 25 2023 Sergio Correia <scorreia@redhat.com> - 6.5.3-1
- Updating for Keylime release v6.5.3

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.4.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Dec 12 2022 Karel Srot <ksrot@redhat.com> - 6.4.3-7
- Ignore non-keylime AVCs on Fedora Rawhide

* Fri Dec 09 2022 Sergio Correia <scorreia@redhat.com> - 6.4.3-6
- Proper exception handling in tornado_requests

* Fri Dec 09 2022 Sergio Correia <scorreia@redhat.com> - 6.4.3-5
- Do not remove tag-repository.repo

* Thu Dec 01 2022 Karel Srot <ksrot@redhat.com> - 6.4.3-4
- Add dynamic_ref reference to e2e_tests.fmf

* Tue Oct 25 2022 Patrik Koncity <pkoncity@redhat.com> - 6.4.3-3
- Add keylime selinux policy as subpackage and update CI

* Wed Sep 14 2022 Sergio Correia <scorreia@redhat.com> - 6.4.3-2
- Update tests branch to fedora-main

* Thu Aug 25 2022 Sergio Correia <scorreia@redhat.com> - 6.4.3-1
- Updating for Keylime release v6.4.3

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jul 11 2022 Sergio Correia <scorreia@redhat.com> - 6.4.2-3
- Wrap efivar-libs dependency in a "ifarch %%efi"

* Fri Jul 08 2022 Sergio Correia <scorreia@redhat.com> - 6.4.2-2
- Fix efivar-libs dependency
- Some arches do not have efivar-libs, so let's require it conditionally.

* Fri Jul 08 2022 Sergio Correia <scorreia@redhat.com> - 6.4.2-1
- Updating for Keylime release v6.4.2
- Remove keylime-webapp and mark package as obsolete
- Configure tmpfiles.d
- Move common python dependencies to python3-keylime
- Change dependency from python3-gnupg to python3-gpg
- Use sysusers.d for handling user creation

* Fri Jul 08 2022 Sergio Correia <scorreia@redhat.com> - 6.4.1-4
- Adjust Fedora CI test plan as per upstream

* Thu Jul 07 2022 Sergio Correia <scorreia@redhat.com> - 6.4.1-3
- Opt in to rpmautospec

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 6.4.1-2
- Rebuilt for Python 3.11

* Mon Jun 06 2022 Sergio Correia <scorreia@redhat.com> - 6.4.1-1
- Updating for Keylime release v6.4.1

* Wed May 04 2022 Sergio Correia <scorreia@redhat.com> - 6.4.0-1
- Updating for Keylime release v6.4.0

* Wed Apr 06 2022 Sergio Correia <scorreia@redhat.com> - 6.3.2-1
- Updating for Keylime release v6.3.2

* Mon Feb 14 2022 Sergio Correia <scorreia@redhat.com> - 6.3.1-1
- Updating for Keylime release v6.3.1

* Tue Feb 08 2022 Sergio Correia <scorreia@redhat.com> - 6.0.3-4
- Add Conflicts clauses for the subpackages

* Mon Feb 07 2022 Sergio Correia <scorreia@redhat.com> - 6.3.0-3
- Split keylime into subpackages
  Related: rhbz#2045874 - Keylime subpackaging and agent alternatives

* Thu Jan 27 2022 Sergio Correia <scorreia@redhat.com> - 6.3.0-2
- Fix permissions of config file

* Thu Jan 27 2022 Sergio Correia <scorreia@redhat.com> - 6.3.0-1
- Updating for Keylime release v6.3.0

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 6.1.0-3
- Rebuilt for Python 3.10

* Thu Mar 25 2021 Luke Hinds <lhinds@redhat.com> 6.0.1-1
- Updating for Keylime release v6.1.0

* Wed Mar 03 2021 Luke Hinds <lhinds@redhat.com> 6.0.1-1
- Updating for Keylime release v6.0.1

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 6.0.0-2
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Wed Feb 24 2021 Luke Hinds <lhinds@redhat.com> 6.0.0-1
- Updating for Keylime release v6.0.0

* Tue Feb 02 2021 Luke Hinds <lhinds@redhat.com> 5.8.1-1
- Updating for Keylime release v5.8.1

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Jan 23 2021 Luke Hinds <lhinds@redhat.com> 5.8.0-1
- Updating for Keylime release v5.8.0

* Fri Jul 17 2020 Luke Hinds <lhinds@redhat.com> 5.7.2-1
- Updating for Keylime release v5.7.2

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 5.6.2-2
- Rebuilt for Python 3.9

* Fri May 01 2020 Luke Hinds <lhinds@redhat.com> 5.6.2-1
- Updating for Keylime release v5.6.2

* Thu Feb 06 2020 Luke Hinds <lhinds@redhat.com> 5.5.0-1
- Updating for Keylime release v5.5.0

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Dec 12 2019 Luke Hinds <lhinds@redhat.com> 5.4.1-1
– Initial Packaging

## END: Generated by rpmautospec
