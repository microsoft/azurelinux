Name:       mock-core-configs
Version:    36.4
Release:    1%{?dist}
Summary:    Mock core config files basic chroots

License:    GPLv2+
URL:        https://github.com/rpm-software-management/mock/
# Source is created by
# git clone https://github.com/rpm-software-management/mock.git
# cd mock/mock-core-configs
# git reset --hard %%{name}-%%{version}
# tito build --tgz
Source:     https://github.com/rpm-software-management/mock/archive/refs/tags/%{name}-%{version}-1/%{name}-%{version}-1.tar.gz#/%{name}-%{version}.tar.gz
BuildArch:  noarch

# The mock.rpm requires this.  Other packages may provide this if they tend to
# replace the mock-core-configs.rpm functionality.
Provides: mock-configs

# distribution-gpg-keys contains GPG keys used by mock configs
Requires:   distribution-gpg-keys >= 1.59
# specify minimal compatible version of mock
Requires:   mock >= 2.5
Requires:   mock-filesystem

Requires(post): coreutils

%description
Config files which allow you to create chroots for:
 * Fedora
 * Epel
 * Mageia
 * Custom chroot
 * OpenSuse Tumbleweed and Leap

%prep
%setup -q -n mock-%{name}-%{version}-1/mock-core-configs


%build

%install
mkdir -p %{buildroot}%{_sysusersdir}

mkdir -p %{buildroot}%{_sysconfdir}/mock/eol/templates
mkdir -p %{buildroot}%{_sysconfdir}/mock/templates
cp -a etc/mock/*.cfg %{buildroot}%{_sysconfdir}/mock
cp -a etc/mock/templates/*.tpl %{buildroot}%{_sysconfdir}/mock/templates
cp -a etc/mock/eol/*cfg %{buildroot}%{_sysconfdir}/mock/eol
cp -a etc/mock/eol/templates/*.tpl %{buildroot}%{_sysconfdir}/mock/eol/templates

# generate files section with config - there is many of them
echo "%defattr(0644, root, mock)" > %{name}.cfgs
find %{buildroot}%{_sysconfdir}/mock -name "*.cfg" -o -name '*.tpl' \
    | sed -e "s|^%{buildroot}|%%config(noreplace) |" >> %{name}.cfgs
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
    ver=$(source /etc/os-release && echo $VERSION_ID | cut -d. -f1 | grep -o '[0-9]\+')
fi
mock_arch=$(python -c "import rpmUtils.arch; baseArch = rpmUtils.arch.getBaseArch(); print baseArch")
cfg=%{?fedora:fedora}%{?rhel:epel}%{?mageia:mageia}-$ver-${mock_arch}.cfg
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
%ghost %config(noreplace,missingok) %{_sysconfdir}/mock/default.cfg

%changelog
* Wed Jan 5 2022 Cameron Baird <cameronbaird@microsoft.com>  - 36.4-1
- Initial CBL-Mariner import from Fedora 33 (license: GPLv2)
- Update to 36.4 source

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


