%global git_date 20241029
%global git_commit 8baf55743b6f68ae889584b194970f8f3f613a8c
%{?git_commit:%global git_commit_hash %(c=%{git_commit}; echo ${c:0:7})}

%global _python_bytecompile_extra 0

# File used as marker to preserve the auto-bindmount of the FIPS policy across
# upgrades while temporarily removing it for the RPM transaction.
%define rpmstatedir %{_localstatedir}/lib/rpm-state/%{name}
%define rpmstate_autopolicy %{rpmstatedir}/autopolicy-reapplication-needed

Name:           crypto-policies
Version:        %{git_date}
Release:        1.git%{git_commit_hash}%{?dist}
Summary:        System-wide crypto policies

License:        LGPL-2.1-or-later
URL:            https://gitlab.com/redhat-crypto/fedora-crypto-policies
Source0:        https://gitlab.com/redhat-crypto/fedora-crypto-policies/-/archive/%{git_commit_hash}/%{name}-git%{git_commit_hash}.tar.gz

BuildArch: noarch
#ExclusiveArch:  %{java_arches} noarch
BuildRequires: asciidoc
BuildRequires: libxslt
BuildRequires: openssl
BuildRequires: nss-tools
BuildRequires: gnutls-utils
BuildRequires: openssh-clients
BuildRequires: java-devel
BuildRequires: bind
BuildRequires: python3-devel >= 3.12
BuildRequires: python3-pytest
BuildRequires: make
BuildRequires: sequoia-policy-config
BuildRequires: systemd-rpm-macros

Conflicts: openssl-libs < 3.0.2-2
Conflicts: nss < 3.101
Conflicts: libreswan < 3.28
Conflicts: openssh < 9.0p1-5
Conflicts: gnutls < 3.8.6-6

# Most users want this, the split is mostly for Fedora CoreOS
Recommends: crypto-policies-scripts

%description
This package provides pre-built configuration files with
cryptographic policies for various cryptographic back-ends,
such as SSL/TLS libraries.

%package scripts
Summary: Tool to switch between crypto policies
Requires: %{name} = %{version}-%{release}
Recommends: (grubby if kernel)
Provides: fips-mode-setup = %{version}-%{release}

%description scripts
This package provides a tool update-crypto-policies, which applies
the policies provided by the crypto-policies package. These can be
either the pre-built policies from the base package or custom policies
defined in simple policy definition files.

The package also provides a tool fips-mode-setup, which can be used
to enable or disable the system FIPS mode.

%prep
%setup -q -n fedora-crypto-policies-%{git_commit_hash}-%{git_commit}
%autopatch -p1

%build
%make_build

%install
mkdir -p -m 755 %{buildroot}%{_datarootdir}/crypto-policies/
mkdir -p -m 755 %{buildroot}%{_datarootdir}/crypto-policies/back-ends/
mkdir -p -m 755 %{buildroot}%{_sysconfdir}/crypto-policies/back-ends/
mkdir -p -m 755 %{buildroot}%{_sysconfdir}/crypto-policies/state/
mkdir -p -m 755 %{buildroot}%{_sysconfdir}/crypto-policies/local.d/
mkdir -p -m 755 %{buildroot}%{_sysconfdir}/crypto-policies/policies/
mkdir -p -m 755 %{buildroot}%{_sysconfdir}/crypto-policies/policies/modules/
mkdir -p -m 755 %{buildroot}%{_bindir}

make DESTDIR=%{buildroot} DIR=%{_datarootdir}/crypto-policies MANDIR=%{_mandir} %{?_smp_mflags} install
install -p -m 644 default-config %{buildroot}%{_sysconfdir}/crypto-policies/config
install -p -m 644 default-fips-config %{buildroot}%{_datarootdir}/crypto-policies/default-fips-config
touch %{buildroot}%{_sysconfdir}/crypto-policies/state/current
touch %{buildroot}%{_sysconfdir}/crypto-policies/state/CURRENT.pol

# Drop pre-generated GOST-ONLY & BSI policies, we do not need to ship the files
rm -rf %{buildroot}%{_datarootdir}/crypto-policies/GOST-ONLY
rm -rf %{buildroot}%{_datarootdir}/crypto-policies/BSI
# Same for the experimental test-only TEST-FEDORA41
rm -rf %{buildroot}%{_datarootdir}/crypto-policies/TEST-FEDORA41
# and FEDORA40, a legacy snapshot of Fedora 40 DEFAULT
rm -rf %{buildroot}%{_datarootdir}/crypto-policies/FEDORA40
# Not having symlinks is also more robust for upgraders when policies go away

# Create back-end configs for mounting with read-only /etc/
for d in LEGACY DEFAULT FUTURE FIPS ; do
    mkdir -p -m 755 %{buildroot}%{_datarootdir}/crypto-policies/back-ends/$d
    for f in %{buildroot}%{_datarootdir}/crypto-policies/$d/* ; do
        ln $f %{buildroot}%{_datarootdir}/crypto-policies/back-ends/$d/$(basename $f .txt).config
    done
done

for f in %{buildroot}%{_datarootdir}/crypto-policies/DEFAULT/* ; do
    ln -sf %{_datarootdir}/crypto-policies/DEFAULT/$(basename $f) %{buildroot}%{_sysconfdir}/crypto-policies/back-ends/$(basename $f .txt).config
done

%py_byte_compile %{__python3} %{buildroot}%{_datadir}/crypto-policies/python

%check
make test %{?_smp_mflags} SKIP_LINTING=1

# Migrate away from removed policies; can be dropped 3 releases later
%pretrans -p <lua>
if posix.access("%{_sysconfdir}/crypto-policies/config") then
    local cf = io.open("%{_sysconfdir}/crypto-policies/config", "r")
    if cf then
        local prev = cf:read()
        cf:close()
        local new
        if prev == "TEST-FEDORA39" or prev:sub(1, 14) == "TEST-FEDORA39:" then
            new = "DEFAULT" .. prev:sub(14)
        elseif prev == "FEDORA38" or prev:sub(1, 9) == "FEDORA38:" then
            new = "DEFAULT" .. prev:sub(9)
        else
            new = prev
        end
        while new:find(":FEDORA32:") ~= nil do
            new = new:gsub(":FEDORA32:", ":")
        end
        new = new:gsub(":FEDORA32$", "")
        if new ~= prev then
            cf = io.open("%{_sysconfdir}/crypto-policies/config", "w")
            if cf then
                cf:write(new)
                cf:close()
            end
        end
    end
end

if arg[2] == 2 then
    posix.unlink("%{rpmstate_autopolicy}")

    local mountinfo = io.open("/proc/self/mountinfo", "r");
    if mountinfo then
        local mountpoints = {}
        for mount in mountinfo:lines() do
            -- See proc_pid_mountinfo(5) for the format
            local pos, _, _, _, _, mountroot, mountpoint = string.find(mount, "^(%d+) (%d+) (%d+:%d+) ([^ ]+) ([^ ]+) ")
            if pos == nil then
                print("Failed to parse /proc/self/mountinfo line, ignoring:", mount)
            else
                mountpoints[mountpoint] = mountroot
            end
        end
        mountinfo:close()

        local expected_backend_suffix = "/%{name}/back-ends/FIPS"
        local expected_config_suffix = "/%{name}/default-fips-config"

        local backends_automount =
            mountpoints["%{_sysconfdir}/%{name}/back-ends"] and
            string.sub(mountpoints["%{_sysconfdir}/%{name}/back-ends"], string.len(expected_backend_suffix) * -1, -1) == expected_backend_suffix
        local config_automount =
            mountpoints["%{_sysconfdir}/%{name}/config"] and
            string.sub(mountpoints["%{_sysconfdir}/%{name}/config"], string.len(expected_config_suffix) * -1, -1) == expected_config_suffix

        if backends_automount and config_automount then
            if posix.access("%{_bindir}/umount", "x") then
                rpm.execute("%{_bindir}/umount", "%{_sysconfdir}/%{name}/config")
                rpm.execute("%{_bindir}/umount", "%{_sysconfdir}/%{name}/back-ends")
            end

            local res, msg, errno = posix.mkdir("%{rpmstatedir}")
            if res ~= 0 and errno ~= 17  then -- 17 is EEXIST
                print("Failed to create state directory: " .. msg)
            else
                local marker, err = io.open("%{rpmstate_autopolicy}", "w+")
                if not marker then
                    print("Failed to create marker file %{rpmstate_autopolicy} for automatic FIPS policy bind-mount: " .. err)
                else
                    marker:close()
                end
            end
        end
    end
end

%post -p <lua>
if not posix.access("%{_sysconfdir}/crypto-policies/config") then
    local policy = "DEFAULT"
    local cf = io.open("/proc/sys/crypto/fips_enabled", "r")
    if cf then
        if cf:read() == "1" then
            policy = "FIPS"
        end
        cf:close()
    end
    cf = io.open("%{_sysconfdir}/crypto-policies/config", "w")
    if cf then
        cf:write(policy.."\n")
        cf:close()
    end
    cf = io.open("%{_sysconfdir}/crypto-policies/state/current", "w")
    if cf then
        cf:write(policy.."\n")
        cf:close()
    end
    local policypath = "%{_datarootdir}/crypto-policies/"..policy
    for fn in posix.files(policypath) do
        if fn ~= "." and fn ~= ".." then
            local backend = fn:gsub(".*/", ""):gsub("%%..*", "")
            local cfgfn = "%{_sysconfdir}/crypto-policies/back-ends/"..backend..".config"
            posix.unlink(cfgfn)
            posix.symlink(policypath.."/"..fn, cfgfn)
        end
    end
else
    if posix.access("%{rpmstate_autopolicy}") then
        os.execute("%{_libexecdir}/fips-crypto-policy-overlay >/dev/null 2>/dev/null || :")
        posix.unlink("%{rpmstate_autopolicy}")
    end
end

%pre
# Drop removed javasystem backend; can be dropped in F43
rm -f "%{_sysconfdir}/crypto-policies/back-ends/javasystem.config" || :
exit 0

%posttrans scripts
%{_bindir}/update-crypto-policies --no-check >/dev/null 2>/dev/null || :


%files

%dir %{_sysconfdir}/crypto-policies/
%dir %{_sysconfdir}/crypto-policies/back-ends/
%dir %{_sysconfdir}/crypto-policies/state/
%dir %{_sysconfdir}/crypto-policies/local.d/
%dir %{_sysconfdir}/crypto-policies/policies/
%dir %{_sysconfdir}/crypto-policies/policies/modules/
%dir %{_datarootdir}/crypto-policies/

%ghost %config(missingok,noreplace) %{_sysconfdir}/crypto-policies/config

%ghost %config(missingok,noreplace) %verify(not mode) %{_sysconfdir}/crypto-policies/back-ends/gnutls.config
%ghost %config(missingok,noreplace) %verify(not mode) %{_sysconfdir}/crypto-policies/back-ends/openssl.config
%ghost %config(missingok,noreplace) %verify(not mode) %{_sysconfdir}/crypto-policies/back-ends/opensslcnf.config
%ghost %config(missingok,noreplace) %verify(not mode) %{_sysconfdir}/crypto-policies/back-ends/openssh.config
%ghost %config(missingok,noreplace) %verify(not mode) %{_sysconfdir}/crypto-policies/back-ends/opensshserver.config
%ghost %config(missingok,noreplace) %verify(not mode) %{_sysconfdir}/crypto-policies/back-ends/nss.config
%ghost %config(missingok,noreplace) %verify(not mode) %{_sysconfdir}/crypto-policies/back-ends/bind.config
%ghost %config(missingok,noreplace) %verify(not mode) %{_sysconfdir}/crypto-policies/back-ends/java.config
%ghost %config(missingok,noreplace) %verify(not mode) %{_sysconfdir}/crypto-policies/back-ends/krb5.config
%ghost %config(missingok,noreplace) %verify(not mode) %{_sysconfdir}/crypto-policies/back-ends/libreswan.config
%ghost %config(missingok,noreplace) %verify(not mode) %{_sysconfdir}/crypto-policies/back-ends/libssh.config
%ghost %config(missingok,noreplace) %verify(not mode) %{_sysconfdir}/crypto-policies/back-ends/openssl_fips.config
%ghost %config(missingok,noreplace) %verify(not mode) %{_sysconfdir}/crypto-policies/back-ends/sequoia.config
%ghost %config(missingok,noreplace) %verify(not mode) %{_sysconfdir}/crypto-policies/back-ends/rpm-sequoia.config
# %verify(not mode) comes from the fact
# these turn into symlinks and back to regular files at will, see bz1898986

%ghost %{_sysconfdir}/crypto-policies/state/current
%ghost %{_sysconfdir}/crypto-policies/state/CURRENT.pol

%{_mandir}/man7/crypto-policies.7*
%{_datarootdir}/crypto-policies/LEGACY
%{_datarootdir}/crypto-policies/DEFAULT
%{_datarootdir}/crypto-policies/FUTURE
%{_datarootdir}/crypto-policies/FIPS
%{_datarootdir}/crypto-policies/EMPTY
%{_datarootdir}/crypto-policies/back-ends
%{_datarootdir}/crypto-policies/default-config
%{_datarootdir}/crypto-policies/default-fips-config
%{_datarootdir}/crypto-policies/reload-cmds.sh
%{_datarootdir}/crypto-policies/policies

%{_libexecdir}/fips-setup-helper
%{_libexecdir}/fips-crypto-policy-overlay
%{_unitdir}/fips-crypto-policy-overlay.service

%license COPYING.LESSER

%files scripts
%{_bindir}/update-crypto-policies
%{_mandir}/man8/update-crypto-policies.8*
%{_datarootdir}/crypto-policies/python

%{_bindir}/fips-mode-setup
%{_bindir}/fips-finish-install
%{_mandir}/man8/fips-mode-setup.8*
%{_mandir}/man8/fips-finish-install.8*

%changelog
* Tue Oct 29 2024 Alexander Sosedkin <asosedkin@redhat.com> - 20241029-1.git8baf557
- Bump version for the f41 package to sort higher that the f40 one

* Thu Oct 10 2024 Alexander Sosedkin <asosedkin@redhat.com> - 20241010-1.git8baf557
- LEGACY: enable 192-bit ciphers for nss pkcs12/smime
- openssl: map NULL to TLS_SHA256_SHA256:TLS_SHA384_SHA384

* Fri Sep 27 2024 Alexander Sosedkin <asosedkin@redhat.com> - 20240927-1.git93b7251
- nss: be stricter with new purposes

* Wed Aug 28 2024 Alexander Sosedkin <asosedkin@redhat.com> - 20240828-1.git5f66e81
- fips-mode-setup: small Argon2 detection fix

* Mon Aug 26 2024 Alexander Sosedkin <asosedkin@redhat.com> - 20240826-1.gite824389
- SHA1: add __openssl_block_sha1_signatures = 0

* Thu Aug 22 2024 Alexander Sosedkin <asosedkin@redhat.com> - 20240822-1.git64c9381
- fips-mode-setup: block if LUKS devices using Argon2 are detected

* Wed Aug 07 2024 Alexander Sosedkin <asosedkin@redhat.com> - 20240807-1.git5795660
- fips-crypto-policy-overlay: a unit to automount FIPS policy when fips=1
- fips-setup-helper: add a libexec helper for anaconda
- fips-mode-setup: force --no-bootcfg when UKI is detected

* Fri Aug 02 2024 Alexander Sosedkin <asosedkin@redhat.com> - 20240802-1.git2e5e430
- nss: rewrite backend for nss 3.101

* Thu Jul 25 2024 Alexander Sosedkin <asosedkin@redhat.com> - 20240725-1.git9555558
- gnutls: wire X25519-KYBER768 to GROUP-X25519-KYBER768
- openssh: make dss no longer enableble, support is dropped

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20240717-2.git154fd4e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jul 17 2024 Alexander Sosedkin <asosedkin@redhat.com> - 20240717-1.git154fd4e
- Changes/OpenSSLDistrustSHA1SigVer: implement, see below
- DEFAULT: switch to rh-allow-sha1-signatures = no...
- TEST-FEDORA41: reset to DEFAULT
- FEDORA40: introduce with the previous contents of DEFAULT
- nss: wire XYBER768D00 to X25519-KYBER768, not KYBER768
- TEST-PQ: disable KYBER768

* Tue Jul 16 2024 Alexander Sosedkin <asosedkin@redhat.com> - 20240715-2.gitf8b6a29
- fix running pre scriptlet in first transaction ever, pre-coreutils

* Mon Jul 15 2024 Alexander Sosedkin <asosedkin@redhat.com> - 20240715-1.gitf8b6a29
- BSI: Update BSI policy for new 2024 minimum recommendations
- java: use and include jdk.disabled.namedCurves
- ec_min_size: introduce and use in java, default to 256
- java: stop specifying jdk.tls.namedGroups in javasystem
- java: drop unused javasystem backend

* Fri Jun 28 2024 Alexander Sosedkin <asosedkin@redhat.com> - 20240628-1.gitddd11d3
- nss: wire KYBER768 to XYBER768D00
- java: start controlling / disable DTLSv1.0
- java: disable anon ciphersuites, tying them to NULL
- java: respect more key size restrictions
- java: specify jdk.tls.namedGroups system property
- java: make hash, mac and sign more orthogonal
- fips-mode-setup: add another scary "unsupported"
- fips-mode-setup: flashy ticking warning upon use
- BSI: switch to 3072 minimum RSA key size

* Tue May 21 2024 Alexander Sosedkin <asosedkin@redhat.com> - 20240521-1.gitf71d135
- nss: unconditionally include p11-kit-proxy
- TEST-PQ: update algorithm list, mark all PQ algorithms experimental

* Wed May 15 2024 Alexander Sosedkin <asosedkin@redhat.com> - 20240515-1.gita24a14b
- gnutls: use tls-session-hash option, enforcing EMS in FIPS mode
- gnutls: DTLS 0.9 is controllable again
- gnutls: remove extraneous newline
- openssh: remove support for old names of RequiredRSASize

* Wed Mar 20 2024 Alexander Sosedkin <asosedkin@redhat.com> - 20240320-1.git58e3d95
- modules/FEDORA32, FEDORA38, TEST-FEDORA39: drop
- openssl: mark liboqsprovider groups optional with ?
- TEST-PQ: add more group and sign values, marked experimental
- TEST-FEDORA41: add a new policy with __openssl_block_sha1_signatures = 1
- TEST-PQ: also enable sntrup761x25519-sha512@openssh.com

* Mon Mar 04 2024 Alexander Sosedkin <asosedkin@redhat.com> - 20240304-1.git0375239
- packaging: remove perl build-dependency, it's not needed anymore
- packaging: stop linting at check-time, relying on upstream CI instead
- packaging: drop stale workarounds
- libreswan: do not use up pfs= / ikev2= keywords for default behaviour

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 20240201-2.git9f501f3
- Rebuilt for java-21-openjdk as system jdk

* Thu Feb 01 2024 Alexander Sosedkin <asosedkin@redhat.com> - 20240201-1.git9f501f3
- fips-finish-install: make sure ostree is detected in chroot
- fips-mode-setup: make sure ostree is detected in chroot
- java: disable ChaCha20-Poly1305 where applicable

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20231204-3.git1e3a2e4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20231204-2.git1e3a2e4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 04 2023 Alexander Sosedkin <asosedkin@redhat.com> - 20231204-1.git1e3a2e4
- TEST-PQ: add a subpolicy to test post-quantum algorithms. Do not rely on.

* Mon Nov 13 2023 Clemens Lang <cllang@redhat.com> - 20231113-1.gitb402e82
- fips-mode-setup: Write error messages to stderr
- fips-mode-setup: Fix some shellcheck warnings
- fips-mode-setup: Fix test for empty /boot
- fips-mode-setup: Avoid 'boot=UUID=' if /boot == /

* Thu Nov 09 2023 Clemens Lang <cllang@redhat.com> - 20231109-1.gitadb5572
- Restore support for scoped ssh_etm directives
- Print matches in syntax deprecation warnings

* Tue Nov 07 2023 Clemens Lang <cllang@redhat.com> - 20231107-1.gitd5877b3
- fips-mode-setup: Fix usage with --no-bootcfg

* Tue Nov 07 2023 Clemens Lang <cllang@redhat.com> - 20231107-1.git8f49dfa
- turn ssh_etm into an etm@SSH tri-state
- fips-mode-setup: increase chroot-friendliness (rhbz#2164847)

* Wed Sep 20 2023 Alexander Sosedkin <asosedkin@redhat.com> - 20230920-1.git570ea89
- OSPP subpolicy: tighten beyond reason for OSPP 4.3
- fips-mode-setup: more thorough --disable, still unsupported

* Tue Jul 25 2023 Alexander Sosedkin <asosedkin@redhat.com> - 20230731-1.git5ed06e0
- BSI: start a BSI TR 02102 policy
- krb5: sort enctypes mac-first, cipher-second, prioritize SHA-2 ones
- FIPS: enforce EMS in FIPS mode
- NO-ENFORCE-EMS: add subpolicy to undo the EMS enforcement in FIPS mode
- nss: implement EMS enforcement in FIPS mode (not enabled yet)
- openssl: implement EMS enforcement in FIPS mode
- gnutls: implement EMS enforcement in FIPS mode (not enabled yet)
- docs: replace `FIPS 140-2` with just `FIPS 140`

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 20230614-2.git5f3458e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Alexander Sosedkin <asosedkin@redhat.com> - 20230614-1.git5f3458e
- policies: restore group order to old OpenSSL default order

* Thu Apr 20 2023 Alexander Sosedkin <asosedkin@redhat.com> - 20230420-1.git3d08ae7
- openssl: specify Groups explicitly
- openssl: add support for Brainpool curves

* Wed Mar 01 2023 Alexander Sosedkin <asosedkin@redhat.com> - 20230301-1.git2ea6d2a
- rpm-sequoia: add separate rpm-sequoia backend
- DEFAULT: allow SHA-1 and 1024 bit DSA in RPM (https://pagure.io/fesco/issue/2960)

* Mon Feb 20 2023 Alexander Sosedkin <asosedkin@redhat.com> - 20230220-1.git8c7de04
- Makefile: support asciidoc 10

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 20221215-2.gita4c31a3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Dec 15 2022 Alexander Sosedkin <asosedkin@redhat.com> - 20221215-1.gita4c31a3
- bind: expand the list of disableable algorithms

* Thu Nov 10 2022 Alexander Sosedkin <asosedkin@redhat.com> - 20221110-1.git87a75f4
- sequoia: introduce new backend
- migrate license tag to SPDX

* Mon Oct 03 2022 Alexander Sosedkin <asosedkin@redhat.com> - 20221003-1.gitcb1ad32
- openssh: force RequiredRSASize option name

* Wed Aug 24 2022 Alexander Sosedkin <asosedkin@redhat.com> - 20220824-2.git2187e9c
- revert premature Fedora 38 Rawhide SHA-1 "jump scare" until
  https://fedoraproject.org/wiki/Changes/StrongCryptoSettings3Forewarning2
  gets approved

* Wed Aug 24 2022 Alexander Sosedkin <asosedkin@redhat.com> - 20220824-1.gitd4b71ab
- disable SHA-1 further for a Fedora 38 Rawhide "jump scare"
  as described at
  https://fedoraproject.org/wiki/Changes/StrongCryptoSettings3Forewarning2
  This change will be reverted for the branched-off Fedora 38,
  but never for Fedora 39.
  Thus the change will reach the users with Fedora 39 release.
  `update-crypto-policies --set FEDORA38` for the former, obsolete DEFAULT.
- openssh: control HostbasedAcceptedAlgorithms
  Systems having it set at /etc/ssh/sshd_config
  will have the value ignored and should instead configure it per-host.

* Mon Aug 15 2022 Alexander Sosedkin <asosedkin@redhat.com> - 20220815-1.gite4ed860
- openssh: add RSAMinSize option following min_rsa_size

* Tue Aug 02 2022 Alexander Sosedkin <asosedkin@redhat.com> - 20220802-1.gita99dfd2
- tests/java: fix java.security.disableSystemPropertiesFile=true
- docs: add customization recommendation

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 20220428-3.gitdfb10ea
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 08 2022 Jiri Vanek <jvanek@redhat.com> - 20220428-2.gitdfb10ea
- Rebuilt for Drop i686 JDKs

* Thu Apr 28 2022 Alexander Sosedkin <asosedkin@redhat.com> - 20220428-1.gitdfb10ea
- policies: add FEDORA38 and TEST-FEDORA39
- fix condition of conflicting with openssl

* Wed Apr 27 2022 Alexander Sosedkin <asosedkin@redhat.com> - 20220427-1.gitca01c3e
- bind: control ED25519/ED448

* Tue Apr 12 2022 Alexander Sosedkin <asosedkin@redhat.com> - 20220412-1.git97fe449
- openssl: disable SHA-1 signatures in FUTURE/NO-SHA1
- skip pylint until it's fixed in Fedora (tracked in bz206983)

* Mon Apr 04 2022 Alexander Sosedkin <asosedkin@redhat.com> - 20220404-1.git17914f1
- fips-mode-setup: improve handling FIPS plus subpolicies
- fips-mode-setup: catch more inconsistencies, clarify --check
- fips-mode-setup, fips-finish-install: abandon /etc/system-fips
- openssh: add support for sntrup761x25519-sha512@openssh.com

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 20220203-2.git112f859
- Rebuilt for java-17-openjdk as system jdk

* Thu Feb 03 2022 Alexander Sosedkin <asosedkin@redhat.com> - 20220203-1.git112f859
- gnutls: enable SHAKE, needed for Ed448
- fips-mode-setup: improve handling FIPS plus subpolicies

* Wed Jan 19 2022 Alexander Sosedkin <asosedkin@redhat.com> - 20220119-1.git50109e7
- gnutls: switch to allowlisting
  (https://fedoraproject.org/wiki/Changes/GnutlsAllowlisting)
- openssl: add newlines at the end of the output

* Mon Nov 15 2021 Alexander Sosedkin <asosedkin@redhat.com> - 20211115-1.git1b1c04c
- OSPP: relax -ECDSA-SHA2-512, -FFDHE-*
- fips-mode-setup, fips-finish-install: call zipl more often (s390x-specific)

* Fri Sep 17 2021 Alexander Sosedkin <asosedkin@redhat.com> - 20210917-1.gitc9d86d1
- openssl: fix disabling ChaCha20
- fix minor things found by pylint 2.11

* Thu Aug 19 2021 Alexander Sosedkin <asosedkin@redhat.com> - 20210819-1.gitd0fdcfb
- gnutls: revert hard-disabling DTLS 0.9
- update-crypto-policies: fix --check's sorting when walking the directories
- update-crypto-policies: always regenerate the policy to --check against
- fix minor things found by new pylint

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20210621-2.gita0e819e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jun 21 2021 Alexander Sosedkin <asosedkin@redhat.com> - 20210621-1.gita0e819e
- bump LEGACY key size requirements from 1023 to 1024
- add javasystem backend
- *ssh: condition ecdh-sha2-nistp384 on SECP384R1
- set %verify(not mode) for backend sometimes-symlinks-sometimes-not

* Tue Jun 15 2021 Alexander Sosedkin <asosedkin@redhat.com> - 20210615-1.giteed6c85
- implement scoped policies, e.g., cipher@SSH = ...
- implement algorithm globbing, e.g., cipher@SSH = -*-CBC
- deprecate derived properties:
  tls_cipher, ssh_cipher, ssh_group, ike_protocol, sha1_in_dnssec
- deprecate unscoped form of protocol property
- openssl: set MinProtocol / MaxProtocol separately for TLS and DTLS
- openssh: use PubkeyAcceptedAlgorithms instead of PubkeyAcceptedKeyTypes
- libssh: respect ssh_certs
- restrict FIPS:OSPP further
- improve Python 3.10 compatibility
- update documentation
- expand upstream test coverage

* Sat Feb 13 2021 Alexander Sosedkin <asosedkin@redhat.com> - 20210213-1.git5c710c0
- exclude RC4 from LEGACY
- introduce rc4_md5_in_krb5 to narrow AD_SUPPORT's impact
- an assortment of small fixes

* Wed Jan 27 2021 Alexander Sosedkin <asosedkin@redhat.com> - 20210127-2.gitb21c811
- fix comparison in %post lua scriptlet

* Wed Jan 27 2021 Alexander Sosedkin <asosedkin@redhat.com> - 20210127-1.gitb21c811
- don't create /etc/crypto-policies/back-ends/.config in %post

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20210118-2.gitb21c811
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 18 2021 Alexander Sosedkin <asosedkin@redhat.com> - 20210118-1.gitb21c811
- output sigalgs required by nss >=3.59 (or 3.60 in Fedora case)
- bump Python requirement to 3.6

* Tue Dec 15 2020 Alexander Sosedkin <asosedkin@redhat.com> - 20201215-1.giteb57e00
- Kerberos 5: Fix policy generator to account for macs

* Tue Dec 08 2020 Alexander Sosedkin <asosedkin@redhat.com> - 20201208-1.git70def9f
- add AES-192 support (non-TLS scenarios)
- add documentation of the --check option

* Wed Sep 23 2020 Tomáš Mráz <tmraz@redhat.com> - 20200918-1.git85dccc5
- add RSA-PSK algorithm support
- add GOST algorithms support for openssl
- add GOST-ONLY policy and fix GOST subpolicy
- update-crypto-policies: added --check parameter to perform
  comparison of actual configuration files with the policy

* Thu Aug 13 2020 Tomáš Mráz <tmraz@redhat.com> - 20200813-1.git66d4068
- libreswan: enable X25519 group
- libreswan: properly disable FFDH in ECDHE-ONLY subpolicy
- libreswan: add generation of authby parameter based on sign property
- libssh: Add diffie-hellman-group14-sha256

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20200702-2.gitc40cede
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 13 2020 Tomáš Mráz <tmraz@redhat.com> - 20200702-1.gitc40cede
- OSPP subpolicy: remove AES-CCM
- openssl: handle the AES-CCM removal properly
- openssh/libssh: drop CBC ciphersuites from DEFAULT and FIPS
- add AD-SUPPORT subpolicy which re-enables RC4 for Kerberos
- gnutls: disallow X448/ED448 in FIPS policy
- merge fips-mode-setup package into the scripts subpackage

* Thu Jun 25 2020 Tomáš Mráz <tmraz@redhat.com> - 20200625-1.gitb298a9e
- DEFAULT policy: Drop DH < 2048 bits, TLS 1.0, 1.1, SHA-1
- make the NEXT policy just an alias for DEFAULT as they are now identical
- policies: introduce sha1_in_dnssec value for BIND
- add SHA1 and FEDORA32 policy modules to provide backwards compatibility
  they can be applied as DEFAULT:SHA1 or DEFAULT:FEDORA32
- avoid duplicates of list items in resulting policy

* Wed Jun 24 2020 Tomáš Mráz <tmraz@redhat.com> - 20200619-1.git781bbd4
- gnutls: enable DSA signatures in LEGACY

* Wed Jun 10 2020 Tomáš Mráz <tmraz@redhat.com> - 20200610-1.git7f9d474
- openssh server: new format of configuration to be loaded by config include
- fallback to FIPS policy instead of the default-config in FIPS mode
- java: Document properly how to override the crypto policy
- reorder the signature algorithms to follow the order in default openssl list

* Tue Jun  9 2020 Tomáš Mráz <tmraz@redhat.com> - 20200527-5.gitb234a47
- make the post script work in environments where /proc/sys is not available

* Fri May 29 2020 Tomáš Mráz <tmraz@redhat.com> - 20200527-4.gitb234a47
- move the symlink fix-up script to post and fix it

* Fri May 29 2020 Tomáš Mráz <tmraz@redhat.com> - 20200527-3.gitb234a47
- automatically set up FIPS policy in FIPS mode on first install

* Thu May 28 2020 Tomáš Mráz <tmraz@redhat.com> - 20200527-2.gitb234a47
- require the base package from scripts subpackage
- add Recommends for fips-mode-setup to the scripts subpackage

* Wed May 27 2020 Tomáš Mráz <tmraz@redhat.com> - 20200527-1.gitb234a47
- explicitly enable DHE-DSS in gnutls config if enabled in policy
- use grubby with --update-kernel=ALL to avoid breaking kernelopts
- OSPP subpolicy: Allow GCM for SSH protocol
- openssh: Support newly standardized ECDHE-GSS and DHE-GSS key exchanges
- if the policy in FIPS mode is not a FIPS policy print a message
- openssl: Add SignatureAlgorithms support

* Thu Mar 12 2020 Tomáš Mráz <tmraz@redhat.com> - 20200312-1.git3ae59d2
- custom crypto policies: enable completely overriding contents of the list
  value
- added ECDHE-ONLY.pmod policy module example
- openssh: make LEGACY policy to prefer strong public key algorithms
- openssh: support FIDO/U2F (with the exception of FIPS policy)
- gnutls: add support for GOST ciphers
- various python code cleanups
- update-crypto-policies: dump the current policy to
  /etc/crypto-policies/state/CURRENT.pol

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20191128-5.gitcd267a5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 14 2020 Tomáš Mráz <tmraz@redhat.com> - 20191128-4.gitcd267a5
- the base package must ship the DEFAULT policy config symlinks in case
  the scripts package is not installed via the weak dependency

* Tue Jan 07 2020 Andrew Jeddeloh <ajeddelo@redhat.com> 20191128-3.gitcd267a5
- split scripts into their own subpackage. See
  https://github.com/coreos/fedora-coreos-tracker/issues/280 for more details.

* Mon Dec 16 2019 Tomáš Mráz <tmraz@redhat.com> - 20191128-2.gitcd267a5
- move the pre-built .config files to /usr/share/crypto-policies/back-ends

* Thu Nov 28 2019 Tomáš Mráz <tmraz@redhat.com> - 20191128-1.gitcd267a5
- add FIPS subpolicy for OSPP
- fips-mode-setup: do not reload daemons when changing policy
- fips-mode-setup: gracefully handle OSTree-based systems
- gnutls: use new configuration file format

* Tue Oct 29 2019 Tomáš Mráz <tmraz@redhat.com> - 20191002-1.gitc93dc99
- update-crypto-policies: fix handling of list operations in policy modules
- update-crypto-policies: fix updating of the current policy marker
- fips-mode-setup: fixes related to containers and non-root execution

* Tue Sep 24 2019 Tomáš Mráz <tmraz@redhat.com> - 20190816-4.gitbb9bf99
- add the /etc/crypto-policies/state directory

* Tue Sep 10 2019 Tomáš Mráz <tmraz@redhat.com> - 20190816-3.gitbb9bf99
- make it possible to use fips-mode-setup --check without dracut
- add .config symlinks so a crypto policy can be set with read-only
  /etc by bind-mounting /usr/share/crypto-policies/<policy> to
  /etc/crypto-policies/back-ends

* Mon Aug 19 2019 Tomáš Mráz <tmraz@redhat.com> - 20190816-2.gitbb9bf99
- run the update-crypto-policies in posttrans
- the current config should work fine with OpenSSL >= 7.9p1
- fix the python bytecompilation

* Fri Aug 16 2019 Tomáš Mráz <tmraz@redhat.com> - 20190816-1.gitbb9bf99
- custom crypto policies support
- openssh: Support new configuration option CASignatureAlgorithms
- libssh: Add libssh as supported backend
- multiple fixes in fips-mode-setup, BLS support

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20190527-2.git0b3add8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon May 27 2019 Tomáš Mráz <tmraz@redhat.com> - 20190211-1.git0b3add8
- libreswan: coalesce proposals to avoid IKE packet fragmentation
- openssh: add missing curve25519-sha256 to the key exchange list
- nss: map X25519 to CURVE25519

* Thu Apr 25 2019 Tomáš Mráz <tmraz@redhat.com> - 20190211-4.gite3eacfc
- do not fail in the Java test if the EMPTY policy is not really empty

* Thu Mar  7 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 20190211-3.gite3eacfc
- Split out fips-mode-setup into separate subpackage

* Mon Feb 11 2019 Tomáš Mráz <tmraz@redhat.com> - 20190211-2.gite3eacfc
- add crypto-policies.7 manual page
- Java: Fix FIPS and FUTURE policy to allow RSA certificates in TLS
- cleanup duplicate and incorrect information from update-crypto-policies.8
  manual page
- update-crypto-policies: Fix endless loop
- update-crypto-policies: Add warning about the need of system restart
- FUTURE: Add mistakenly ommitted EDDSA-ED25519 signature algorithm
- openssh: Add missing SHA2 variants of RSA certificates to the policy
- return exit code 2 when printing usage from all the tools
- update-crypto-policies: add --no-reload option for testing

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20181122-2.git70769d9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Nov 22 2018 Tomáš Mráz <tmraz@redhat.com> - 20181122-1.git70769d9
- update-crypto-policies: fix error on multiple matches in local.d

* Tue Nov 20 2018 Tomáš Mráz <tmraz@redhat.com> - 20181120-1.gitd2b3bc4
- Print warning when update-crypto-policies --set is used in the FIPS mode
- Java: Add 3DES and RC4 to legacy algorithms in LEGACY policy
- OpenSSL: Properly disable non AEAD and AES128 ciphersuites in FUTURE
- libreswan: Add chacha20_poly1305 to all policies and drop ikev1 from LEGACY

* Fri Oct 26 2018 Tomáš Mráz <tmraz@redhat.com> - 20181026-1.gitd42aaa6
- Fix regression in discovery of additional configuration
- NSS: add DSA keyword to LEGACY policy
- GnuTLS: Add 3DES and RC4 to LEGACY policy

* Tue Sep 25 2018 Tomáš Mráz <tmraz@redhat.com> - 20180925-1.git71ca85f
- Use Recommends instead of Requires for grubby
- Revert setting of HostKeyAlgorithms for ssh client for now

* Fri Sep 21 2018 Tomáš Mráz <tmraz@redhat.com> - 20180921-2.git391ed9f
- Fix requires for grubby

* Fri Sep 21 2018 Tomáš Mráz <tmraz@redhat.com> - 20180921-1.git391ed9f
- OpenSSH: Generate policy for sign algorithms
- Enable >= 255 bits EC curves in FUTURE policy
- OpenSSH: Add group1 key exchanges in LEGACY policy
- NSS: Add SHA224 to hash lists
- Print warning when update-crypto-policies --set FIPS is used
- fips-mode-setup: Kernel boot options are now modified with grubby

* Thu Aug  2 2018 Tomáš Mráz <tmraz@redhat.com> - 20180802-1.git1626592
- Introduce NEXT policy

* Mon Jul 30 2018 Tomáš Mráz <tmraz@redhat.com> - 20180730-1.git9d9f21d
- Add OpenSSL configuration file include support

* Tue Jul 24 2018 Tomáš Mráz <tmraz@redhat.com> - 20180723-1.gitdb825c0
- Initial FIPS mode setup support
- NSS: Add tests for the generated policy
- Enable TLS-1.3 if available in the respective TLS library
- Enable SHA1 in certificates in LEGACY policy
- Disable CAMELLIA
- libreswan: Multiple bug fixes in policies

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20180425-6.git6ad4018
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri May 18 2018 Björn Esser <besser82@fedoraproject.org> - 20180425-5.git6ad4018
- Fix patch0

* Fri May 18 2018 Björn Esser <besser82@fedoraproject.org> - 20180425-4.git6ad4018
- Remove Requires: systemd
- Add Patch to silence warnings from reload-cmds

* Thu May 17 2018 Björn Esser <besser82@fedoraproject.org> - 20180425-3.git6ad4018
- Requires: systemd should be added too

* Thu May 17 2018 Björn Esser <besser82@fedoraproject.org> - 20180425-2.git6ad4018
- Add Requires(post): systemd to fix:
  crypto-policies/reload-cmds.sh: line 1: systemctl: command not found

* Wed Apr 25 2018 Tomáš Mráz <tmraz@redhat.com> - 20180425-1.git6ad4018
- Restart/reload only enabled services
- Do not enable PSK ciphersuites by default in gnutls and openssl
- krb5: fix when more than 2048 bits keys are required
- Fix discovery of additional configurations #1564595
- Fix incorrect ciphersuite setup for libreswan

* Tue Mar  6 2018 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20180306-1.gitaea6928
- Updated policy to reduce DH parameter size on DEFAULT level, taking into
  account feedback in #1549242,1#534532.
- Renamed openssh-server.config to opensshserver.config to reduce conflicts
  when local.d/ appending is used.

* Tue Feb 27 2018 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20180227-1.git0ce1729
- Updated to include policies for libreswan

* Mon Feb 12 2018 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20180112-1.git386e3fe
- Updated to apply the settings as in StrongCryptoSettings project. The restriction
  to TLS1.2, is not yet applied as we have no method to impose that in openssl.
  https://fedoraproject.org/wiki/Changes/StrongCryptoSettings

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 20171115-3.git921600e
- Escape macros in %%changelog

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20171115-2.git921600e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Nov 15 2017 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20171115-1.git921600e
- Updated openssh policies for new openssh without rc4
- Removed policies for compat-gnutls28

* Wed Aug 23 2017 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20170823-1.git8d18c27
- Updated gnutls policies for 3.6.0

* Wed Aug 16 2017 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20170816-1.git2618a6c
- Updated to latest upstream
- Restarts openssh server on policy update

* Wed Aug  2 2017 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20170802-1.git9300620
- Updated to latest upstream
- Reloads openssh server on policy update

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20170606-4.git7c32281
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jul 25 2017 Igor Gnatenko <ignatenko@redhat.com> - 20170606-3.git7c32281
- Restore Requires(post)

* Mon Jul 24 2017 Troy Dawson <tdawson@redhat.com> 20170606-2.git7c32281
- perl dependency renamed to perl-interpreter <ppisar@redhat.com>
- remove useless Requires(post) <ignatenko@redhat.com>
- Fix path of libdir in generate-policies.pl (#1474442) <tdawson@redhat.com>

* Tue Jun  6 2017 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20170606-1.git7c32281
- Updated to latest upstream
- Allows gnutls applications in LEGACY mode, to use certificates of 768-bits

* Wed May 31 2017 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20170531-1.gitce0df7b
- Updated to latest upstream
- Added new kerberos key types

* Sat Apr 01 2017 Björn Esser <besser82@fedoraproject.org> - 20170330-3.git55b66da
- Add Requires for update-crypto-policies in %%post

* Fri Mar 31 2017 Petr Šabata <contyk@redhat.com> - 20170330-2.git55b66da
- update-crypto-policies uses gred and sed, require them

* Thu Mar 30 2017 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20170330-1-git55b66da
- GnuTLS policies include RC4 in legacy mode (#1437213)

* Fri Feb 17 2017 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20160214-2-gitf3018dd
- Added openssh file

* Tue Feb 14 2017 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20160214-1-gitf3018dd
- Updated policies for BIND to address #1421875

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20161111-2.gita2363ce
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Nov 11 2016 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20161111-1-gita2363ce
- Include OpenJDK documentation.

* Tue Sep 27 2016 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20160926-2-git08b5501
- Improved messages on error.

* Mon Sep 26 2016 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20160926-1-git08b5501
- Added support for openssh client policy

* Wed Sep 21 2016 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20160921-1-git75b9b04
- Updated with latest upstream.

* Thu Jul 21 2016 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20160718-2-gitdb5ca59
- Added support for administrator overrides in generated policies in local.d

* Thu Jul 21 2016 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20160718-1-git340cb69
- Fixed NSS policy generation to include allowed hash algorithms

* Wed Jul 20 2016 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20160718-1-gitcaa4a8d
- Updated to new version with auto-generated policies

* Mon May 16 2016 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20160516-1-git8f69c35
- Generate policies for NSS
- OpenJDK policies were updated for opendjk 8

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 20151104-2.gitf1cba5f
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Nov  4 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20151104-1-gitcf1cba5f
- Generate policies for compat-gnutls28 (#1277790)

* Fri Oct 23 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20151005-2-gitc8452f8
- Generated files are put in a %%ghost directive

* Mon Oct  5 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20151005-1-gitc8452f8
- Updated policies from upstream
- Added support for the generation of libkrb5 policy
- Added support for the generation of openjdk policy

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20150518-2.gitffe885e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 18 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20150518-1-gitffe885e
- Updated policies to remove SSL 3.0 and RC4 (#1220679)

* Fri Mar  6 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20150305-3-git2eeb03b
- Added make check

* Fri Mar  6 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20150305-2-git44afaa1
- Removed support for SECLEVEL (#1199274)

* Thu Mar  5 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20150305-1-git098a8a6
- Include AEAD ciphersuites in gnutls (#1198979)

* Sun Jan 25 2015 Peter Robinson <pbrobinson@fedoraproject.org> 20150115-3-git9ef7493
- Bump release so lastest git snapshot is newer NVR

* Thu Jan 15 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20150115-2-git9ef7493
- Updated to newest upstream version.
- Includes bind policies (#1179925)

* Tue Dec 16 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20141124-2-gitd4aa178
- Corrected typo in gnutls' future policy (#1173886)

* Mon Nov 24 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20141124-1-gitd4aa178
- re-enable SSL 3.0 (until its removal is coordinated with a Fedora change request)

* Thu Nov 20 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20141120-1-git9a26a5b
- disable SSL 3.0 (doesn't work in openssl)

* Fri Sep 05 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20140905-1-git4649b7d
- enforce the acceptable TLS versions in openssl

* Wed Aug 27 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20140827-1-git4e06f1d
- fix issue with RC4 being disabled in DEFAULT settings for openssl

* Thu Aug 14 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20140814-1-git80e1e98
- fix issue in post script run on upgrade (#1130074)

* Tue Aug 12 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20140812-1-gitb914bfd
- updated crypto-policies from repository

* Fri Jul 11 2014 Tom Callaway <spot@fedoraproject.org> - 20140708-2-git3a7ae3f
- fix license handling

* Tue Jul 08 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20140708-1-git3a7ae3f
- updated crypto-policies from repository

* Fri Jun 20 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 20140620-1-gitdac1524
- updated crypto-policies from repository
- changed versioning

* Thu Jun 12 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 0.9-7-20140612gita2fa0c6
- updated crypto-policies from repository

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-7.20140522gita50bad2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 29 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 0.9-6-20140522gita50bad2
- Require(post) coreutils (#1100335).

* Tue May 27 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 0.9-5-20140522gita50bad2
- Require coreutils.

* Thu May 22 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 0.9-4-20140522gita50bad2
- Install the default configuration file.

* Wed May 21 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 0.9-3-20140520git81364e4
- Run update-crypto-policies after installation.

* Tue May 20 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 0.9-2-20140520git81364e4
- Updated spec based on comments by Petr Lautrbach.

* Mon May 19 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 0.9-1-20140519gitf15621a
- Initial package build

