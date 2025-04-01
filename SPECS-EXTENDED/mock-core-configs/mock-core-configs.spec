%if 0%{?el8}
%global python3 /usr/libexec/platform-python
%endif

Name:       mock-core-configs
Version:    41.5
Release:    1%{?dist}
Summary:    Mock core config files basic chroots

License:    GPL-2.0-or-later
URL:        https://github.com/rpm-software-management/mock/
# Source is created by
# git clone https://github.com/rpm-software-management/mock.git
# cd mock/mock-core-configs
# git reset --hard %%{name}-%%{version}
# tito build --tgz
Source:     https://github.com/rpm-software-management/mock/releases/download/%{name}-%{version}-1/%{name}-%{version}.tar.gz
BuildArch:  noarch

# The mock.rpm requires this.  Other packages may provide this if they tend to
# replace the mock-core-configs.rpm functionality.
Provides: mock-configs

# distribution-gpg-keys contains GPG keys used by mock configs
Requires:   distribution-gpg-keys >= 1.105
# specify minimal compatible version of mock
Requires:   mock >= 5.4.post1
Requires:   mock-filesystem

Requires(post): coreutils
# to detect correct default.cfg
Requires(post): python3-dnf
Requires(post): python3-hawkey
Requires(post): system-release
Requires(post): python3
Requires(post): sed

%description
Mock configuration files which allow you to create chroots for Alma Linux,
Amazon Linux, CentOS, CentOS Stream, Circle Linux, EuroLinux, Fedora, Fedora EPEL, Mageia,
Navy Linux, OpenMandriva Lx, openSUSE, Oracle Linux, Red Hat Enterprise Linux,
Rocky Linux and various other specific or combined chroots.


%prep
%setup -q


%build


%install
mkdir -p %{buildroot}%{_sysconfdir}/mock/eol/templates
mkdir -p %{buildroot}%{_sysconfdir}/mock/templates
cp -a etc/mock/*.cfg %{buildroot}%{_sysconfdir}/mock
cp -a etc/mock/templates/*.tpl %{buildroot}%{_sysconfdir}/mock/templates
cp -a etc/mock/eol/*cfg %{buildroot}%{_sysconfdir}/mock/eol
cp -a etc/mock/eol/templates/*.tpl %{buildroot}%{_sysconfdir}/mock/eol/templates

# generate files section with config - there is many of them
echo "%defattr(0644, root, mock)" > %{name}.cfgs
find %{buildroot}%{_sysconfdir}/mock -name "*.cfg" -o -name '*.tpl' \
    | grep -v chroot-aliases \
    | sed -e "s|^%{buildroot}|%%config(noreplace) |" >> %{name}.cfgs
echo "%%config %{_sysconfdir}/mock/chroot-aliases.cfg" >> %{name}.cfgs

# just for %%ghosting purposes
ln -s fedora-rawhide-x86_64.cfg %{buildroot}%{_sysconfdir}/mock/default.cfg
# bash-completion
if [ -d %{buildroot}%{_datadir}/bash-completion ]; then
    echo %{_datadir}/bash-completion/completions/mock >> %{name}.cfgs
    echo %{_datadir}/bash-completion/completions/mockchain >> %{name}.cfgs
elif [ -d %{buildroot}%{_sysconfdir}/bash_completion.d ]; then
    echo %{_sysconfdir}/bash_completion.d/mock >> %{name}.cfgs
fi

# reference valid mock.rpm's docdir with example site-defaults.cfg
mock_docs=%{_pkgdocdir}
mock_docs=${mock_docs//mock-core-configs/mock}
mock_docs=${mock_docs//-%version/-*}
sed -i "s~@MOCK_DOCS@~$mock_docs~" %{buildroot}%{_sysconfdir}/mock/site-defaults.cfg

%post
if [ -s /etc/os-release ]; then
    # fedora and rhel7+
    if grep -Fiq Rawhide /etc/os-release; then
        ver=rawhide
    # mageia
    elif [ -s /etc/mageia-release ]; then
        if grep -Fiq Cauldron /etc/mageia-release; then
           ver=cauldron
        fi
    else
        ver=$(source /etc/os-release && echo $VERSION_ID | cut -d. -f1 | grep -o '[0-9]\+')
    fi
else
    # something obsure, use buildtime version
    ver=%{?rhel}%{?fedora}%{?mageia}
fi
if [ -s /etc/mageia-release ]; then
    mock_arch=$(sed -n '/^$/!{$ s/.* \(\w*\)$/\1/p}' /etc/mageia-release)
else
    mock_arch=$(%{python3} -c "import dnf.rpm; import hawkey; print(dnf.rpm.basearch(hawkey.detect_arch()))")
fi

cfg=unknown-distro
%if 0%{?fedora}
cfg=fedora-$ver-$mock_arch.cfg
%endif
%if 0%{?rhel}
# Being installed on RHEL, or a RHEL fork.  Detect it.
distro_id=$(. /etc/os-release; echo $ID)
case $distro_id in
centos)
  # This package is EL8+, and there's only CentOS Stream now.
  distro_id=centos-stream
  ;;
almalinux)
  # AlmaLinux configs look like 'alma+epel'
  distro_id=alma
  ;;
esac
cfg=$distro_id+epel-$ver-$mock_arch.cfg
%endif

%if 0%{?eln}
# overrides rhel value which resolves in fedora+epel-rawhide-$mock_arch.cfg
cfg=fedora-eln-$mock_arch.cfg
%endif

%if 0%{?mageia}
cfg=mageia-$ver-$mock_arch.cfg
%endif

if [ -e %{_sysconfdir}/mock/$cfg ]; then
    if [ "$(readlink %{_sysconfdir}/mock/default.cfg)" != "$cfg" ]; then
        ln -s $cfg %{_sysconfdir}/mock/default.cfg 2>/dev/null || ln -s -f $cfg %{_sysconfdir}/mock/default.cfg.rpmnew
    fi
else
    echo "Warning: file %{_sysconfdir}/mock/$cfg does not exist."
    echo "         unable to update %{_sysconfdir}/mock/default.cfg"
fi
:


%files -f %{name}.cfgs
%license COPYING
%doc README
%ghost %config(noreplace,missingok) %{_sysconfdir}/mock/default.cfg

%changelog
* Thu Dec 19 2024 Pavel Raiskup <praiskup@redhat.com> 41.5-1
- Fedora 39 EOL
- fix openSUSE-tumbleweed update failure during the second build (duli4868@gmail.com)
- use non development bootstrap image for CentOS Stream 10 (romain.geissler@amadeus.com)
- remove ELN ResilientStorage repos (yselkowi@redhat.com)
- update ELN bootstrap image (yselkowi@redhat.com)
- Add epel and epel-testing repos to the EPEL 10 config (carlwgeorge@gmail.com)

* Mon Sep 30 2024 Pavel Raiskup <praiskup@redhat.com> 41.4-1
- update ELN repos (yselkowi@redhat.com)

* Thu Sep 26 2024 Pavel Raiskup <praiskup@redhat.com> 41.3-1
- move anolis-7 to eol directory (msuchy@redhat.com)
- move opensuse-leap-15.4 to eol directory (msuchy@redhat.com)
- configs: the stream9 image is "ready" for Mock bootstrap
- enable bootstrap container for CentOS Stream 10 (carlwgeorge@gmail.com)
- configs: replace `powerpc64le` with `ppc64le` in the `%%_host_cpu` macro
- fix EOL template locations for CentOS7/EPEL7 (thomas.mendorf@ebf.com)

* Thu Aug 15 2024 Pavel Raiskup <praiskup@redhat.com> 41.2-1
- fix centos-stream+epel-10-s390x /bin/sed typo

* Wed Aug 14 2024 Pavel Raiskup <praiskup@redhat.com> 41.1-1
- branch F41 from Rawhide (frostyx@email.cz)
- added centos-stream+epel-10 configs
- Enable RPM sysusers integration (j1.kyjovsky@gmail.com)
- Rawhide to accept GPG key from future Fedora Rawhide+1
- openEuler 24.03 LTS (nucleo@fedoraproject.org)
- drop fedora-eln-i386 (yselkowi@redhat.com)
- Switch CentOS 7 to vault.centos.org (robert@fedoraproject.org)
- Fix GPG keys for CentOS Stream 10 repositories (daan.j.demeyer@gmail.com)
- EOL epel-7 configuration
- CentOS 7 is EOL
- Fedora 41+ configuration images are "dnf5 ready"
- Use metalinks for c10s {baseos,appstream,crb}-{source,debuginfo} (miro@hroncok.cz)

* Sat Jun 15 2024 Pavel Raiskup <praiskup@redhat.com> 40.6-1
- c10s config use mirrored metalinks

* Wed Jun 05 2024 Miroslav Suchý <msuchy@redhat.com> 40.5-1
- CentOS Stream 8 is EOL (andykimpe@gmail.com)
- configs: Fedora 38 goes EOL (praiskup@redhat.com)

* Tue May 14 2024 Jakub Kadlcik <frostyx@email.cz> 40.4-1
- configs: BuildWithDNF5 for ELN (praiskup@redhat.com)
- Add Circle Linux 9 configs (bella@cclinux.org)
- configs: Replace Mageia 10 and Cauldron i586 configs with i686
  (wally@mageia.org)
- Post-release administrivia (frostyx@email.cz)

* Fri Apr 05 2024 Jakub Kadlcik <frostyx@email.cz> 40.3-1
- Add initial c10s mock configs (Koji BUILDROOT only) (miro@hroncok.cz)
- configs: use repo_arch, not target_arch with openSUSE (praiskup@redhat.com)
- configs: Drop modular repositories from Fedora Branched
  (ngompa@fedoraproject.org)
- configs: Drop modular repositories from Fedora Rawhide
  (ngompa@fedoraproject.org)
- Configs 40.2 release notes && post-release administrivia
  (praiskup@redhat.com)

* Fri Feb 16 2024 Pavel Raiskup <praiskup@redhat.com> 40.2-1
- Use dnf5 on Fedora 40+ (miro@hroncok.cz)

* Wed Feb 14 2024 Pavel Raiskup <praiskup@redhat.com> 40.1-1
- new '{{ repo_arch }}' template variable used for Mageia
- Mageia 7 is EOL (wally@mageia.org)
- OpenMandriva i686 is EOL (frostyx@email.cz)
- Fedora 40 branched

* Thu Jan 11 2024 Pavel Raiskup <praiskup@redhat.com> 39.4-1
- configure system_cachedir for dnf5
- configs: EOL Fedora 37
- config: add README.md with maintainers and issue trackers (frostyx@email.cz)

* Fri Dec 01 2023 Pavel Raiskup <praiskup@redhat.com> 39.3-1
- Fedora 40+ to use DNF5 for building
- Mandriva provides python-* not python3-* packages, use them
- mark ELN bootstrap image as "ready" to speedup bootstrap preparation

* Thu Oct 19 2023 Pavel Raiskup <praiskup@redhat.com> 39.2-1
- Switch ELN to use a native bootstrap container image
- Use the correct openSUSE Backports key for Leap 15.5 (neal@gompa.dev)
- Properly handle /etc/mock/default.cfg on Fedora ELN (sbonazzo@redhat.com)

* Fri Sep 15 2023 Pavel Raiskup <praiskup@redhat.com> 39.1-1
- Add openSUSE Leap 15.5 (neal@gompa.dev)
- Move openSUSE Leap 15.3 to EOL (neal@gompa.dev)
- Mageia 9 branched, Mageia Cauldron retargeted to Mageia 10 (neal@gompa.dev)

* Wed Aug 09 2023 Pavel Raiskup <praiskup@redhat.com> 39-1
- new upstream release, per https://rpm-software-management.github.io/mock/Release-Notes-5.0

* Mon Jun 05 2023 Pavel Raiskup <praiskup@redhat.com> 38.6-1
- use python3 macro for post scriptlet (mroche@omenos.dev)
- openEuler: use metalinks instead of baseurls (chenzeng2@huawei.com)

* Mon May 22 2023 Pavel Raiskup <praiskup@redhat.com> 38.5-1
- drop includepkgs=devtoolset* from centos-{6,7} (orion@nwra.com)
- Fedora 35 and 36 is EOL
- remove useradd specific changes in configs - it is not needed for Mock 4+
- openSUSE i586 has been moved out of the main repo into a port (f_krull@gmx.de)

* Sat Apr 15 2023 Pavel Raiskup <praiskup@redhat.com> 38.4-1
- Add Amazon Linux 2023 mock configs (trawets@amazon.com)

* Thu Mar 16 2023 Pavel Raiskup <praiskup@redhat.com> 38.3-1
- new URL for CenOS Stream 8 koji (msuchy@redhat.com)
- Make --enablerepo=local work with centos-stream chroots (miro@hroncok.cz)

* Fri Feb 17 2023 Pavel Raiskup <praiskup@redhat.com> 38.2-1
- update gpg keys for Tumbleweed (msuchy@redhat.com)

* Tue Jan 31 2023 Pavel Raiskup <praiskup@redhat.com> 38.1-1
- update openEuler gpg key (pkwarcraft@gmail.com)
- Branch Fedora 38 (miro@hroncok.cz)
- disable fastestmirror on almalinux (jonathan@almalinux.org)
- openEuler 22.03-SP1 released, use the latest repo url (pkwarcraft@gmail.com)

* Thu Jan 05 2023 Pavel Raiskup <praiskup@redhat.com> 37.9-1
- missmatching gpg key and rpms in openEuler 20.03 LTS (pkwarcraft@gmail.com)
- drop unneccessary module docs from configuration files (nkadel@gmail.com)

* Tue Sep 27 2022 Pavel Raiskup <praiskup@redhat.com> 37.8-1
- openEuler 22.03 configs added (yikunkero@gmail.com)
- openEuler 20.03 configs added (yikunkero@gmail.com)
- Oracle Linux 9 configs added (a.samets@gmail.com)
- change license to spdx (msuchy@redhat.com)
- Update to AlmaLinux Quay.io repo (srbala@gmail.com)
- EPEL Koji repo not exposed when we are on EPEL Next (miro@hroncok.cz)

* Wed Aug 10 2022 Pavel Raiskup <praiskup@redhat.com> 37.7-1
- depend on distribution-gpg-keys 1.76 (F38 key)

* Wed Aug 10 2022 Pavel Raiskup <praiskup@redhat.com> 37.6-1
- Branch Fedora 37 configs (miro@hroncok.cz)
- Add anolis-release for Anolis OS 7 and Anolis OS 8 templates (wb-
  zh951434@alibaba-inc.com)

* Fri Jul 22 2022 Pavel Raiskup <praiskup@redhat.com> 37.5-1
- configs: add ELN local Koji repo
- config: sync epel-8 and epel-9 templates
- Add Rocky Linux 9 Configuration and Mod RL8 (label@rockylinux.org)
- Update Fedora ELN repo template (sgallagh@redhat.com)
- EuroLinux 9 chroot configs added (git@istiak.com)
- Fedora 34 is EOL
- circlelinux+epel-8 as epel-8 alternative
- Fix dist value for openSUSE Leap 15.4 (ngompa@opensuse.org)
- Add CircleLinux 8 configs (bella@cclinux.org)
- Add openSUSE Leap 15.4 configs (ngompa@opensuse.org)
- Move openSUSE Leap 15.2 to EOL directory (ngompa@opensuse.org)
- Use MirrorCache for openSUSE repositories instead of MirrorBrain (ngompa@opensuse.org)
- Add Anolis OS 7 and Anolis OS 8 templates and configs (wb-zh951434@alibaba-inc.com)

* Thu May 19 2022 Pavel Raiskup <praiskup@redhat.com> 37.4-1
- Add AlmaLinux 9 and AlmaLinux 9 + EPEL configs (neal@gompa.dev)
- Update the AlmaLinux 8 GPG key path (neal@gompa.dev)
- Fix description typo on AlmaLinux 8 for x86_64 (neal@gompa.dev)
- Add RHEL9 templates and configs (carl@george.computer)

* Wed Apr 06 2022 Pavel Raiskup <praiskup@redhat.com> 37.3-1
- updated %%description field
- provide 'epel-9' symlinks for 'fedpkg mockbuild'
- allow n-2 gpg key for Fedora ELN (msuchy@redhat.com)
- added config "description" fields for --list-chroots (msuchy@redhat.com)

* Thu Mar 03 2022 Pavel Raiskup <praiskup@redhat.com> 37.2-1
- Update CentOS Stream 9 Extras repo to use correct key (ngompa@centosproject.org)
- Add AlmaLinux+EPEL 8 for POWER (ppc64le) (ngompa13@gmail.com)
- Add AlmaLinux 8 for POWER (ppc64le) (ngompa13@gmail.com)
- Delete Fedora 37/Rawhide armhfp configs (miro@hroncok.cz)

* Fri Feb 04 2022 Pavel Raiskup <praiskup@redhat.com> 37.1-1
- drop EL7 related %%build hack
- link default.cfg file to the right EL N config file
- Add centos-stream+epel-8 configs

* Wed Feb 02 2022 Pavel Raiskup <praiskup@redhat.com> 37-1
- move CentOS/EPEL 8 configs to eol/
- Fedora 36 branching, Rawhide == Fedora 37 now
- depend on distribution-gpg-keys 1.64
- drop failovermethod=priority from EL8 configs
- Add Extras repo for CentOS Stream 9 (ngompa13@gmail.com)
- remove el7 specific parts from the spec file (msuchy@redhat.com)

* Thu Dec 16 2021 Pavel Raiskup <praiskup@redhat.com> 36.4-1
- add CentOS Stream 9 + EPEL Next 9 (ngompa13@gmail.com)
- add compatibility symlinks for EPEL 7 to centos+epel-7-* (ngompa13@gmail.com)
- EPEL 7 for AArch64 and PPC64 are EOL (ngompa13@gmail.com)
- resolve the multiple "local" repo collision (from multiple templates)
- configure the alternative help for missing 'epel-8-*' configs
- Fedora 33 is EOL
- rhelepel moved to rhel+epel
- EOL the EPEL Playground configs (ngompa13@gmail.com)
- Add rocky+epel confs + Disable devel-debug (tucklesepk@gmail.com)
- Rename epel to centos+epel (ngompa13@gmail.com)
- fix the root name and remove Next from the EPEL 9 configs (ngompa13@gmail.com)
- rename 'epel-next' to 'centos-stream+epel-next' (ngompa13@gmail.com)
- add epel9 repos to epel9 template (carl@george.computer)
- rhbz#2026571 - expand dnf_vars (msuchy@redhat.com)
- oraclelinux+epel configs (carl@george.computer)
- Add AlmaLinux+EPEL configs (ngompa13@gmail.com)
- add navy-8-x86_64 (adil@linux.com)
- use quay.io Almalinux image (gotmax@e.email)
- use fully qualified bootstrap_image name (gotmax@e.email)
- update almalinux-8.tpl bootstrap_image (gotmax@e.email)
- add Koji local repos to CentOS Stream configs (ngompa13@gmail.com)
- reduce packages installed in epel chroots (carl@george.computer)

* Fri Oct 29 2021 Pavel Raiskup <praiskup@redhat.com> 36.3-1
- add EuroLinux 8 aarch64 (alex@euro-linux.com)
- add HA and RS configs to EuroLinux configs (alex@euro-linux.com)
- Add epel9-next configs (carl@george.computer)

* Tue Oct 26 2021 Pavel Raiskup <praiskup@redhat.com> 36.2-1
- bump eln to F36 (praiskup@redhat.com)

* Fri Oct 08 2021 Pavel Raiskup <praiskup@redhat.com> 36.1-1
- Finalize CentOS Stream 9 configuration (ngompa13@gmail.com)
- Update Oraclelinux 7/8 configs and add Oraclelinux EPEL 7/8 configs (darren.archibald@oracle.com)

* Thu Sep 16 2021 Miroslav Suchý <msuchy@redhat.com> 36-1
- config: Align CentOS Stream 9 with the production configuration
  (ngompa13@gmail.com)
- config: Disable installing weak dependencies on RHEL rebuilds
  (ngompa13@gmail.com)
- config: Disable installing weak dependencies on CentOS Stream
  (ngompa13@gmail.com)
- config: Validate GPG signatures for CentOS Stream 9 (ngompa13@gmail.com)
- Add eurolinux-8 x86_64 and i686 buildroots (alex@euro-linux.com)

* Mon Aug 16 2021 Pavel Raiskup <praiskup@redhat.com> 35-1
- config: add Fedora 35 configs

* Mon Jul 19 2021 Pavel Raiskup <praiskup@redhat.com> 34.6-1
- Disable Rocky Linux "Devel" repo by default (ngompa13@gmail.com)
- Fix URL for Rocky Linux repos in commented out "baseurl" lines
  (ngompa13@gmail.com)

* Mon Jul 19 2021 Pavel Raiskup <praiskup@redhat.com> 34.5-1
- Add CentOS Stream 9 "preview" files
- Add rocky support to mock (tucklesepk@gmail.com)
- Add AlmaLinux 8 AArch64 target (ngompa13@gmail.com)
- Add AlmaLinux Devel repo as an optional repo for AlmaLinux 8 (ngompa13@gmail.com)
- Fix GPG key path for SLE updates in openSUSE Leap 15.3 (ngompa13@gmail.com)
- Move Requires of shadow-utils from mock-core-configs to mock-filesystem (msuchy@redhat.com)
- Switch CentOS templates to use quay.io images for bootstrap (carl@george.computer)
- Add epel-next-8 configs (carl@george.computer)

* Tue Jun 08 2021 Pavel Raiskup <praiskup@redhat.com> 34.4-1
- Add GPG keys and RPM repositories for openSUSE Leap 15.3 (ngompa13@gmail.com)
- EOL Fedora 32 (msuchy@redhat.com)
- sync centos-stream-8 with centos-stream-repos (msuchy@redhat.com)

* Tue Apr 27 2021 Pavel Raiskup <praiskup@redhat.com> 34.3-1
- Add Oracle Linux 8 (ngompa13@gmail.com)
- Add Oracle Linux 7 (ngompa13@gmail.com)
- Add openSUSE Leap 15.3 (ngompa13@gmail.com)
- openSUSE Leap 15.1 is EOL (ngompa13@gmail.com)
- Add openSUSE Tumbleweed s390x config (ngompa13@gmail.com)
- Add AlmaLinux 8 configs (ngompa13@gmail.com)
- Remove make from default ELN buildroot (miro@hroncok.cz)

* Mon Feb 22 2021 Pavel Raiskup <praiskup@redhat.com> 34.2-1
- configs: use Fedora N-1 gpg keys for ELN (praiskup@redhat.com)

* Thu Feb 11 2021 Pavel Raiskup <praiskup@redhat.com> 34.1-1
- fix rawhide config after branching

* Mon Feb 08 2021 Pavel Raiskup <praiskup@redhat.com> 34-1
- add fedora 34 configs (msuchy@redhat.com)
- require distribution-gpg-keys with F35 keys (msuchy@redhat.com)
- make F35 symlink to rawhide (msuchy@redhat.com)
- Rename centos-stream centos-stream-8 (orion@nwra.com)

* Tue Feb 02 2021 Pavel Raiskup <praiskup@redhat.com> 33.6-1
- Add Mageia 8 stable release configs (ngompa13@gmail.com)
- Update Mageia Cauldron configuration for Mageia 9 (ngompa13@gmail.com)
- add RHEL 6 x86_64 configuration

* Mon Jan 18 2021 Pavel Raiskup <praiskup@redhat.com> 33.5-1
- fix typo in host-specific config generater

* Mon Jan 18 2021 Pavel Raiskup <praiskup@redhat.com> 33.4-1
- fix bootstrapping of newer Fedora on EL7
- efine a bootstrap image for openSUSE Tumbleweed (ngompa13@gmail.com)
- use fully qualified paths for Fedora/CentOS/RHEL images (ngompa13@gmail.com)
- rename repoid for centos8 (msuchy@redhat.com)
- EOL CentOS 6 (msuchy@redhat.com)
- EOL Fedora 31 (msuchy@redhat.com)

* Fri Nov 20 2020 Pavel Raiskup <praiskup@redhat.com> 33.3-1
- ELN should use for build Everything repository (jkonecny@redhat.com)

* Wed Nov 11 2020 Pavel Raiskup <praiskup@redhat.com> 33.2-1
- Add missing CRB repository (jkonecny@redhat.com)

* Wed Nov 11 2020 Pavel Raiskup <praiskup@redhat.com> 33.1-1
- ELN fixups (mmathesi@redhat.com)
- EPEL: fix repo-id and name=
- Add missing repos to CentOS 6 and CentOS 7 configs
- Do --disablerepo=centos-sclo* in templates
- Add plain CentOS 6/7/8 configs (without epel)
- EPEL Playground depends on normal EPEL

* Thu Sep 03 2020 Pavel Raiskup <praiskup@redhat.com> 33-1
- bump version to 33, as we already ship F33 configs
- because of the mock-filesystem change, depend on mock 2.5

* Thu Sep 03 2020 Pavel Raiskup <praiskup@redhat.com> 32.8-1
- set the DNF user_agent in dnf.conf (msuchy@redhat.com)
- add Fedora ELN configs
- introduce mock-filesystem subpackage (msuchy@redhat.com)

* Thu Aug 06 2020 Pavel Raiskup <praiskup@redhat.com> 32.7-1
- add branched Fedora 33 configs
- eol Fedora 30
- tolerate a 1-minute baseurl outages in OpenSUSE configs
- fix site-defaults.cfg reference to docs
- change all openSUSE configs to use the download redirector (baseurl)

* Wed Apr 01 2020 Pavel Raiskup <praiskup@redhat.com> 32.6-1
- the site-defaults.cfg file moved from mock to mock-core-configs
- new option config_opts['isolation'], obsoletes 'use_nspawn'
- declare minimal version of mock, and set this to v2.2 as we use the new
  'isolation' config option now, and we provide site-defaults.cfg file
- specify amazonlinux bootstrap image, to fix --use-bootstrap-image
- allow to replace mock-core-configs by packages that 'Provides: mock-configs'
- rpmlint: remove macro in comment

* Thu Mar 26 2020 Pavel Raiskup <praiskup@redhat.com> 32.5-1
- Add Devel repo to CentOS 8 and CentOS Stream (ngompa13@gmail.com)
- Add PowerTools sources repo entry to CentOS 8 and CentOS Stream
  (ngompa13@gmail.com)
- Fix openSUSE Leap 15.1 aarch64 update repo & package filters
  (ngompa13@gmail.com)
- Add openSUSE Leap 15.2 (ngompa13@gmail.com)
- openSUSE Leap 15.0 is EOL (ngompa13@gmail.com)
- Add OpenMandriva Lx 4.1 (ngompa13@gmail.com)
- OpenMandriva Lx 4.0 is EOL (ngompa13@gmail.com)

* Wed Mar 11 2020 Pavel Raiskup <praiskup@redhat.com> 32.4-1
- disable package_state plugin for openmandriva 4.0/Cooker
- Mageia 6 is EOL
- opensuse: copy ssl ca bundle to correct path

* Fri Feb 21 2020 Pavel Raiskup <praiskup@redhat.com> 32.3-2
- bump version for lost git tag

* Fri Feb 21 2020 Pavel Raiskup <praiskup@redhat.com> 32.3-1
- put back the opensuse-leap-15.1-x86_64 config

* Thu Feb 20 2020 Pavel Raiskup <praiskup@redhat.com> 32.2-1
- use one template for branched fedoras
- templatize F31+ i386
- use 'dnf.conf' in mageia, opensuse and openmandriva configs

* Sat Feb 08 2020 Pavel Raiskup <praiskup@redhat.com> 32.1-1
- centos-8 and centos-stream to use dnf.conf

* Fri Feb 07 2020 Pavel Raiskup <praiskup@redhat.com> 32.0-2
- solve yum.conf vs. dnf.conf inconsistency in config and code

* Thu Feb 06 2020 Pavel Raiskup <praiskup@redhat.com> 32.0-1
- add F32 configs and move rawhide to F33
- make compatibility changes with mock 2.0
- allow host overrides (build-time for now)
- use jinja for gpgkey= in rawhide template
- add rhel-{7,8}-s390x configs
- drop rhel-8-ppc64, it was never supported
- fix rhel-7 configs
- update epel-8 config template to include modular repos as well as missing
  non-modular source repo (mmathesi@redhat.com)
- drop for a long time useless epel-6-ppc64 config
- use template for opensuse, openmandriva, mageia, epel, custom ...
- fix epel-6.tpl config bug
- set default podman image for centos-stream
- remove aarch64 string from repo name in template [RHBZ#1780977]
- EOL F29 configs
- fix rhelepel configs
- allow including configs and templates from relative path (frostyx@email.cz)
- configs: drop cost=2000 from fedora-31+-i386
- add missing metadata_expire=0 to epel configs
- change default of 'package_manager' to 'dnf', and use 'dnf.conf'
- remove rhelbeta-8-*

* Fri Nov 01 2019 Miroslav Suchý <msuchy@redhat.com> 31.7-1
- Add configs for epel8-playground (mmathesi@redhat.com)
- add 3 base packages to epel-playground buildroot [RHBZ#1764445]
- add 3 base packages to epel buildroot [RHBZ#1764445]

* Fri Oct 04 2019 Miroslav Suchý <msuchy@redhat.com> 31.6-1
- disable modular repo for f29
- configure podman containers for Fedora, EPEL and Mageia (frostyx@email.cz)
- Fix baseurl typo in centos-stream config (dollierp@redhat.com)

* Thu Sep 26 2019 Miroslav Suchý <msuchy@redhat.com> 31.5-1
- expand contentdir for now
- expand $stream for now
- add extra_chroot_dirs to centos8
- use dnf for centos8
- add centos-stream-8
- rhelepel: reuse epel-8.tpl (praiskup@redhat.com)
- Add Amazon Linux 2 configs (haroldji@amazon.com)
- centos-8: enable PowerTools repo (praiskup@redhat.com)

* Tue Sep 24 2019 Miroslav Suchý <msuchy@redhat.com> 31.4-1
- provide explanation why modular repos are disabled
- add epel-8
- Changing cfg files for fedora rawhide to use tpl file
  (sisi.chlupova@gmail.com)
- Changing cfg files for fedora 31 to use tpl file (sisi.chlupova@gmail.com)
- Changing cfg files for fedora 29 to use tpl file (sisi.chlupova@gmail.com)

* Sat Sep 14 2019 Miroslav Suchý <msuchy@redhat.com> 31.3-1
- mock-core-configs: installroot fix for fedora 31+ i386 (praiskup@redhat.com)
- Moving templates into templates dir (sisi.chlupova@gmail.com)
- Changing cfg files for fedora 30 to use tpl file (sisi.chlupova@gmail.com)
- Moving fedora-30-x86_64.cfg into templates/fedora-30.tpl
  (sisi.chlupova@gmail.com)
- baseurl for f30-build was changed (sisi.chlupova@gmail.com)
- no i686 repositories [GH#325]
- adds equation sign to --disablerepo (thrnciar@reedhat.com)

* Mon Aug 26 2019 Miroslav Suchý <msuchy@redhat.com> 31.2-1
- revert sysusers setting [RHBZ#1740545]
- add rhelepel-8 configs (praiskup@redhat.com)
- add RHEL 7/8 (praiskup@redhat.com)

* Mon Aug 19 2019 Miroslav Suchý <msuchy@redhat.com> 31.1-1
- add fedora 31 configs and rawhide is now 32
- Add local-source repo definition to Fedora Rawhide (miro@hroncok.cz)

* Mon Aug 19 2019 Miroslav Suchý <msuchy@redhat.com>
- add fedora 31 configs and rawhide is now 32
- Add local-source repo definition to Fedora Rawhide (miro@hroncok.cz)

* Thu Aug 08 2019 Miroslav Suchý <msuchy@redhat.com> 30.5-1
- disable updates-modulare repos for now
- buildrequire systemd-srpm-macros to get _sysusersdir
- removed info about metadata expire (khoidinhtrinh@gmail.com)
- added updates-modular to 29 and 30 (khoidinhtrinh@gmail.com)
- replace groupadd using sysusers.d
- core-configs: epel-7 profiles to use mirrorlists (praiskup@redhat.com)
- EOL Fedora 28
- do not protect packages in chroot [GH#286]
- Fix value for dist for OpenMandriva 4.0 configs (ngompa13@gmail.com)
- Add initial OpenMandriva distribution targets (ngompa13@gmail.com)

* Thu Jun 06 2019 Miroslav Suchý <msuchy@redhat.com> 30.4-1
- Add 'fastestmirror=1' to Mageia mock configs (ngompa13@gmail.com)
- bootstrap: disable sclo* repos for epel --installroot (praiskup@redhat.com)
- drop Fedora ppc64 configs [RHBZ#1714489]

* Thu May 16 2019 Miroslav Suchý <msuchy@redhat.com> 30.3-1
- Allow AArch64 systems to build 32-bit ARM packages (ngompa13@gmail.com)
- Fix openSUSE Tumbleweed DistTag definition (ngompa13@gmail.com)

* Fri Mar 01 2019 Miroslav Suchý <msuchy@redhat.com> 30.2-1
- disable modular repos
- Add openSUSE Leap AArch64 configs (ngompa13@gmail.com)
- Add openSUSE Leap 15.1 configuration (ngompa13@gmail.com)
- Bump releasever in Cauldron to 8 and create symlinks to cauldron configs
  (ngompa13@gmail.com)
- Add Mageia 7 configs (ngompa13@gmail.com)

* Tue Feb 19 2019 Miroslav Suchý <msuchy@redhat.com> 30.1-1
- default for config['decompress_program'] (praiskup@redhat.com)
- require recent distribution-gpg-keys which has F31 key
- add examples how to enable/install module in F29+ configs
- add module_platform_id
- add modular repos
- enable gpgcheck for debuginfo for rawhide
- enable gpgcheck for testing and debuginfo for F30
- EOL Fedora 27 configs
- remove mdpolicy from F30
- add Fedora 30 configs
- add link to distribution-gpg-keys for rhel8 bootstrap

* Fri Nov 16 2018 Miroslav Suchý <msuchy@redhat.com> 29.4-1
- use correct gpg keys for rhelbeta-8
- add virtual platform module

* Thu Nov 15 2018 Miroslav Suchý <msuchy@redhat.com> 29.3-1
- add rhelbeta-8-* configs
- move EOLed configs to /etc/mock/eol directory
- Add source repos to all fedora configs (sfowler@redhat.com)
- add epel-7-ppc64.cfg

* Thu Aug 16 2018 Miroslav Suchý <msuchy@redhat.com> 29.2-1
- add gpg keys for release rawhide-1 (msuchy@redhat.com)

* Mon Aug 13 2018 Miroslav Suchý <msuchy@redhat.com> 29.1-1
- add fedora 29 configs and change rawhide to F30
- defattr is not needed since rpm 4.2
- Replace armv5tl with aarch64 for Mageia Cauldron (ngompa13@gmail.com)
- check gpg keys for rawhide

* Wed May 02 2018 Miroslav Suchý <msuchy@redhat.com> 28.4-1
- requires distribution-gpg-keys with opensuse keys
- Add initial openSUSE distribution targets (ngompa13@gmail.com)
- provide fedora-29 configs as symlinks to fedora-rawhide
- use cp instead of install to preserve symlinks
- use correct url for local repos for s390x for F27+ [RHBZ#1553678]
- add CentOS SCL repositories to EPEL 7 (aarch64 & ppc64le)
  (tmz@pobox.com)

* Thu Mar 01 2018 Miroslav Suchý <msuchy@redhat.com> 28.3-1
- bump up releasever in rawhide configs
- add CentOS SCL repositories to EPEL 6 & 7 (x86_64)
  (tmz@pobox.com)

* Mon Jan 22 2018 Miroslav Suchý <msuchy@redhat.com> 28.2-1
- fix wrong RHEL condition

* Mon Jan 22 2018 Miroslav Suchý <msuchy@redhat.com> 28.1-1
- bump up version to 28.1

* Mon Jan 22 2018 Miroslav Suchý <msuchy@redhat.com> 27.5-1
- add fedora 28 configs
- remove failovermethod=priority for repos which use dnf
- remove fedora 24 configs
- set skip_if_unavailable=False for all repos

* Mon Oct 09 2017 Miroslav Suchý <msuchy@redhat.com> 27.4-1
- Fix mock & mock-core-config specs to support Mageia (ngompa13@gmail.com)
- Ensure mock-core-configs will select the right default on Mageia
  (ngompa13@gmail.com)

* Wed Sep 27 2017 Miroslav Suchý <msuchy@redhat.com> 27.3-1
- use primary key for F-27+ on s390x (dan@danny.cz)

* Tue Sep 12 2017 Miroslav Suchý <msuchy@redhat.com> 27.2-1
- add source url
- grammar fix

* Thu Sep 07 2017 Miroslav Suchý <msuchy@redhat.com> 27.1-1
- Split from Mock package.


