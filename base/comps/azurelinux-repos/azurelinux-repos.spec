%global evergreen_major 5
%global evergreen_release %{evergreen_major}.0

Summary:        Azure Linux package repositories
Name:           azurelinux-repos
Version:        4.0
Release:        0.1
License:        MIT
URL:            https://aka.ms/azurelinux

Provides:       azurelinux-repos(%{version}) = %{release}
Requires:       system-release(%{version})
%if "%{evergreen_release}" == "%{version}"
Requires:       azurelinux-repos-evergreen = %{version}-%{release}
%endif
Requires:       azurelinux-gpg-keys >= %{version}-%{release}
BuildArch:      noarch
# Required by %%check
BuildRequires:  gnupg sed rpm

Source1:        archmap
Source2:        azurelinux.repo
Source3:        azurelinux-evergreen.repo

Source10:       RPM-GPG-KEY-azurelinux-4.0-primary

# When bumping Evergreen to fN, create N+1 key (and update archmap). (This
# ensures users have the next future key installed and referenced, even if they
# don't update very often. This will smooth out Evergreen N->N+1 transition for them).

# IMA certs: dracut integrity module only recognizes DER format
# TODO(azl): review
# Source500:      azurelinux-ima-ca.der
# Source501:      azurelinux-4.0-ima.der

%description
Azure Linux package repository files for yum and dnf along with gpg public keys.

%package evergreen
Summary:        Evergreen repo definitions
Requires:       azurelinux-repos = %{version}-%{release}

%description evergreen
This package provides the evergreen repo definitions.

%package -n azurelinux-gpg-keys
Summary:        Azure Linux RPM keys
Requires:       filesystem >= 3.18-6

%description -n azurelinux-gpg-keys
This package provides the RPM signature keys.


%prep

%build

%install
# Install the keys
install -d -m 755 $RPM_BUILD_ROOT/etc/pki/rpm-gpg
install -m 644 %{_sourcedir}/RPM-GPG-KEY* $RPM_BUILD_ROOT/etc/pki/rpm-gpg/

# Link the primary/secondary keys to arch files, according to archmap.
# Ex: if there's a key named RPM-GPG-KEY-azurelinux-4.0-primary, and archmap
#     says "azurelinux-4.0-primary: x86_64 aarch64",
#     RPM-GPG-KEY-azurelinux-4.0-{x86_64,aarch64} will be symlinked to that key.
pushd $RPM_BUILD_ROOT/etc/pki/rpm-gpg/
# Also add a symlink for Evergreen keys
ln -s RPM-GPG-KEY-azurelinux-%{evergreen_release}-primary RPM-GPG-KEY-azurelinux-evergreen-primary
for keyfile in RPM-GPG-KEY*; do
    # resolve symlinks, so that we don't need to keep duplicate entries in archmap
    real_keyfile=$(basename $(readlink -f $keyfile))
    key=${real_keyfile#RPM-GPG-KEY-} # e.g. 'azurelinux-4.0-primary'
    if ! grep -q "^${key}:" %{_sourcedir}/archmap; then
        echo "ERROR: no archmap entry for $key"
        exit 1
    fi
    arches=$(sed -ne "s/^${key}://p" %{_sourcedir}/archmap)
    for arch in $arches; do
        # replace last part with $arch (azurelinux-4.0-primary -> azurelinux-4.0-$arch)
        ln -s $keyfile ${keyfile%%-*}-$arch # NOTE: RPM replaces %% with %
    done
done
# and add symlink for compat generic location
ln -s RPM-GPG-KEY-azurelinux-%{version}-primary RPM-GPG-KEY-%{version}-azurelinux
popd

# Install the IMA certs
# TODO(azl): review
# install -d -m 755 $RPM_BUILD_ROOT/etc/keys/ima
# install -m 644 %{_sourcedir}/azurelinux*ima.der $RPM_BUILD_ROOT/etc/keys/ima/
# install -d -m 755 $RPM_BUILD_ROOT/usr/share/ima/
# install -m 644 %{_sourcedir}/azurelinux-ima-ca.der $RPM_BUILD_ROOT/usr/share/ima/ca.der

# Install repo files
install -d -m 755 $RPM_BUILD_ROOT/etc/yum.repos.d
for file in %{_sourcedir}/azurelinux*repo ; do
  install -m 644 $file $RPM_BUILD_ROOT/etc/yum.repos.d
done

# Enable or disable repos based on current release cycle state.
%if "%{evergreen_release}" == "%{version}"
evergreen_enabled=1
stable_enabled=0
%else
evergreen_enabled=0
stable_enabled=1
%endif
for repo in $RPM_BUILD_ROOT/etc/yum.repos.d/azurelinux-evergreen*.repo; do
    sed -i "s/^enabled=AUTO_VALUE$/enabled=${evergreen_enabled}/" $repo || exit 1
done
for repo in $RPM_BUILD_ROOT/etc/yum.repos.d/azurelinux.repo; do
    sed -i "s/^enabled=AUTO_VALUE$/enabled=${stable_enabled}/" $repo || exit 1
done

# Adjust Evergreen repo files to include Evergreen+1 GPG key.
# This is necessary for the period when Evergreen gets bumped to N+1 and packages
# start to be signed with a newer key. Without having the key specified in the
# repo file, the system would consider the new packages as untrusted.
evergreen_next=$((%{evergreen_major}+1)).0
for repo in $RPM_BUILD_ROOT/etc/yum.repos.d/azurelinux-evergreen*.repo; do
    sed -i "/^gpgkey=/ s@AUTO_VALUE@file:///etc/pki/rpm-gpg/RPM-GPG-KEY-azurelinux-${evergreen_next}-\$basearch@" \
        $repo || exit 1
done

# Set appropriate metadata_expire in base repo files (6h before Final, 7d after)
%if "%{release}" < "1"
expire_value='6h'
%else
expire_value='7d'
%endif
for repo in $RPM_BUILD_ROOT/etc/yum.repos.d/azurelinux.repo; do
    sed -i "/^metadata_expire=/ s/AUTO_VALUE/${expire_value}/" \
        $repo || exit 1
done


%check
# Make sure all repo variables were substituted
for repo in $RPM_BUILD_ROOT/etc/yum.repos.d/*.repo; do
    if grep -q AUTO_VALUE $repo; then
        echo "ERROR: Repo $repo contains an unsubstituted placeholder value"
        exit 1
    fi
done

# Make sure correct repos were enabled/disabled
enabled_repos=()
disabled_repos=()

%if "%{evergreen_release}" == "%{version}"
enabled_repos+=(azurelinux-evergreen)
disabled_repos+=(azurelinux)
%else
enabled_repos+=(azurelinux)
disabled_repos+=(azurelinux-evergreen)
%endif

for repo in ${enabled_repos[@]}; do
    if ! grep -q 'enabled=1' $RPM_BUILD_ROOT/etc/yum.repos.d/${repo}.repo; then
        echo "ERROR: Repo $repo should have been enabled, but it isn't"
        exit 1
    fi
done
for repo in ${disabled_repos[@]}; do
    if grep -q 'enabled=1' $RPM_BUILD_ROOT/etc/yum.repos.d/${repo}.repo; then
        echo "ERROR: Repo $repo should have been disabled, but it isn't"
        exit 1
    fi
done

# Make sure metadata_expire was correctly set
%if "%{release}" < "1"
expire_value='6h'
%else
expire_value='7d'
%endif
for repo in $RPM_BUILD_ROOT/etc/yum.repos.d/azurelinux.repo; do
    lines=$(grep '^metadata_expire=' $repo | sort | uniq)
    if [ "$(echo "$lines" | wc -l)" -ne 1 ]; then
        echo "ERROR: Non-matching metadata_expire lines in $repo: $lines"
        exit 1
    fi
    if test "$lines" != "metadata_expire=${expire_value}"; then
        echo "ERROR: Wrong metadata_expire value in $repo: $lines"
        exit 1
    fi
done

# Make sure the Evergreen+1 key wasn't forgotten to be created
evergreen_next=$((%{evergreen_major}+1)).0
test -n "$evergreen_next" || exit 1
if ! test -f $RPM_BUILD_ROOT/etc/pki/rpm-gpg/RPM-GPG-KEY-azurelinux-${evergreen_next}-primary; then
    echo "ERROR: GPG key for Azure Linux ${evergreen_next} is not present"
    exit 1
fi

# Make sure the Evergreen+1 key is present in Evergreen repo files
for repo in $RPM_BUILD_ROOT/etc/yum.repos.d/azurelinux-evergreen*.repo; do
    gpg_lines=$(grep '^gpgkey=' $repo)
    if test -z "$gpg_lines"; then
        echo "ERROR: No gpgkey= lines in $repo"

        exit 1
    fi
    while IFS= read -r line; do
        if ! echo "$line" | grep -q "RPM-GPG-KEY-azurelinux-${evergreen_next}"; then
            echo "ERROR: Azure Linux ${evergreen_next} GPG key missing in $repo"
            exit 1
        fi
    done <<< "$gpg_lines"
done

# Check arch keys exists on supported architectures, and RPM considers
# them valid
TMPRING=$(mktemp)
DBPATH=$(mktemp -d)
for VER in %{version} %{evergreen_release} ${evergreen_next}; do
  echo -n > "$TMPRING"
  for ARCH in $(sed -ne "s/^azurelinux-${VER}-primary://p" %{_sourcedir}/archmap)
  do
    gpg --no-default-keyring --keyring="$TMPRING" \
      --import $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-azurelinux-$VER-$ARCH
    rpm --dbpath "$DBPATH" --import $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-azurelinux-$VER-$ARCH --test
  done
  # Ensure some arch key was imported
  gpg --no-default-keyring --keyring="$TMPRING" --list-keys | grep -A 2 '^pub\s'
done
rm -f "$TMPRING"

%files
%dir /etc/yum.repos.d
%config(noreplace) /etc/yum.repos.d/azurelinux.repo

%files evergreen
%config(noreplace) /etc/yum.repos.d/azurelinux-evergreen.repo


%files -n azurelinux-gpg-keys
%dir /etc/pki/rpm-gpg
/etc/pki/rpm-gpg/RPM-GPG-KEY-*

# ima-certs
# TODO(azl): review
# /etc/keys/ima/azurelinux*ima*
# /usr/share/ima/ca.der


%changelog
* Mon Aug 11 2025 Samyak Jain <samyak.jn11@gmail.com> - 44-0.1
- Rawhide is now F44

* Mon Aug 04 2025 Samyak Jain <samyak.jn11@gmail.com> - 43-0.3
- Add RPM-GPG-KEY-fedora-45-primary
- Add fedora-45-ima.der for ima signing.

* Thu Mar 13 2025 Kevin Fenzi <kevin@scrye.com> - 43-0.2
- Add fedora-43-ima.der and fedora-44-ima.der for ima signing.

* Fri Jan 31 2025 Patrik Polakovic <patrik@alphamail.org> - 43-0.1
- Rawhide is now F43

* Wed Jan 10 2025 Samyak Jain <samyak.jn11@gmail.com> - 42-0.4
- Add RPM-GPG-KEY-fedora-44-primary

* Tue Oct 22 2024 Stephen Gallagher <sgallagh@redhat.com> - 42-0.3
- ELN: Drop ResilientStorage

* Wed Sep 18 2024 Stephen Gallagher <sgallagh@redhat.com> - 42-0.2
- Use mirror links for ELN

* Tue Aug 13 2024 Samyak Jain <samyak.jn11@gmail.com> - 42-0.1
- Setup for evergreen being F42

* Sat Aug 10 2024 Samyak Jain <samyak.jn11@gmail.com> - 41-0.3
- Add RPM-GPG-KEY-fedora-43-primary

* Wed May 08 2024 Coiby Xu <coxu@redhat.com> - 41-0.2
- add/update IMA certs

* Tue Feb 13 2024 Samyak Jain <samyak.jn11@gmail.com> - 41-0.1
- Setup for evergreen being F41

* Wed Sep 27 2023 Sandro Bonazzola <sbonazzo@redhat.com> - 40-0.2
- Allow ELN installation without Rawhide repos

* Tue Aug 08 2023 Samyak Jain <samyak.jn11@gmail.com> - 40-0.1
- Setup for evergreen being F40

* Fri Jul 21 2023 Peter Robinson <pbrobinson@fedoraproject.org> - 39-0.4
- Update IMA keys location for kernel/dracut

* Mon Jul 10 2023 Miro Hrončok <mhroncok@redhat.com> - 39-0.3
- Drop fedora-repos-modular and fedora-repos-evergreen-modular packages
- https://fedoraproject.org/wiki/Changes/RetireModularity

* Sat Feb 18 2023 Kevin Fenzi <kevin@scrye.com> - 39-0.2
- Include IMA public certs.

* Wed Feb 08 2023 Tomas Hrcka <thrcka@redhat.com> - 39-0.1
- Setup for evergreen being F39

* Wed Jan 25 2023 Tomas Hrcka <thrcka@redhat.com> - 38-0.4
- Add RPM-GPG-KEY-fedora-40-primary

* Tue Aug 16 2022 Adam Williamson <awilliam@redhat.com> - 38.0-3
- Fix RPM-GPG-KEY-fedora-39-primary (dustymabe)

* Tue Aug 09 2022 Tomas Hrcka <thrcka@redhat.com> - 38-0.2
- Drop armhfp from archmap on f38,f39

* Tue Aug 09 2022 Tomas Hrcka <thrcka@redhat.com> - 38-0.1
- Setup for evergreen being F38
- Adding F39 key

* Wed Jun 08 2022 Stephen Gallagher <sgallagh@redhat.com> - 37-0.3
- ELN: don't enable layered product repos by default

* Wed May 25 2022 Stephen Gallagher <sgallagh@redhat.com> - 37-0.2
- Rework Fedora ELN repositories

* Tue Feb 08 2022 Tomas Hrcka <thrcka@redhat.com> - 37-0.1
- Setup for evergreen being F37
- Adding F38 key

* Tue Aug 17 2021 Tomas Hrcka <thrcka@redhat.com> - 36-0.3
- Remove spurious space in RPM-GPG-KEY-fedora-37-primary (cgwalters)

* Tue Aug 10 2021 Tomas Hrcka <thrcka@redhat.com> - 36-0.2
- Setup for evergreen being F36

* Wed Apr 28 2021 Dusty Mabe <dusty@dustymabe.com> - 35-0.4
- Enable the updates archive repo on non-evergreen.

* Fri Feb 19 2021 Petr Menšík <pemensik@redhat.com> - 35-0.3
- Check arch key imports during build (#1872248)

* Wed Feb 17 2021 Mohan Boddu <mboddu@bhujji.com> - 35-0.2
- Support $releasever=evergreen on Rawhide (kparal)
- Make archmap entries mandatory, except symlinks (kparal)
- Fixing F36 key

* Tue Feb 09 2021 Tomas Hrcka <thrcka@redhat.com> - 35-0.1
- Setup for evergreen being F35

* Tue Feb 09 2021 Mohan Boddu <mboddu@bhujji.com> - 34-0.10
- Fixing archmap for F35

* Thu Feb 04 2021 Mohan Boddu <mboddu@bhujji.com> - 34-0.9
- Adding F35 key

* Wed Oct 14 2020 Stephen Gallagher <sgallagh@redhat.com> - 34-0.8
- ELN: Drop dependency on fedora-repos-evergreen-modular

* Tue Oct 13 2020 Stephen Gallagher <sgallagh@redhat.com> - 34-0.7
- Ensure that the ELN GPG key always points at the Rawhide key

* Tue Oct 13 2020 Stephen Gallagher <sgallagh@redhat.com> - 34-0.6
- Drop the fedora-eln-modular.repo

* Thu Oct 08 2020 Stephen Gallagher <sgallagh@redhat.com> - 34-0.5
- Update the ELN repos for the BaseOS and AppStream split

* Mon Oct 05 2020 Dusty Mabe <dusty@dustymabe.com> - 34-0.4
- Add the fedora-repos-archive subpackage.

* Fri Aug 21 2020 Miro Hrončok <mhroncok@redhat.com> - 34-0.3
- Fix a copy-paste error in eln repo name
- Drop fedora-modular from base package since it's in the modular subpackage
- Fixes: rhbz#1869150

* Wed Aug 19 2020 Stephen Gallagher <sgallagh@redhat.com> - 34-0.2
- Enable rebuilding of fedora-repos in ELN
- Drop unused modularity-specific release information

* Mon Aug 10 2020 Tomas Hrcka <thrcka@redhat.com> - 34-0.1
- Setup for evergreen being F34

* Thu Aug 06 2020 Mohan Boddu <mboddu@bhujji.com> - 33-0.9
- Adding F34 key

* Tue Jun 30 2020 Stephen Gallagher <sgallagh@redhat.com> - 33-0.8
- Add optional repositories for ELN

* Mon Jun 29 21:10:15 CEST 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 33-0.7
- Split modular repos to the separate packages

* Mon Jun 01 2020 Dusty Mabe <dusty@dustymabe.com> - 33-0.6
- Add fedora compose ostree repo to fedora-repos-ostree

* Mon Apr 13 2020 Stephen Gallagher <sgallagh@redhat.com> - 33-0.5
- Add the release to the fedora-repos(NN) Provides:

* Thu Apr 09 2020 Kalev Lember <klember@redhat.com> - 33-0.4
- Switch to metalink for fedora-cisco-openh264 and disable repo gpgcheck
  (#1768206)
- Use the same metadata_expire time for fedora-cisco-openh264 and -debuginfo
- Remove enabled_metadata key for fedora-cisco-openh264

* Sat Feb 22 2020 Neal Gompa <ngompa13@gmail.com> - 33-0.3
- Enable fedora-cisco-openh264 repo by default

* Wed Feb 19 2020 Adam Williamson <awilliam@redhat.com> - 33-0.2
- Restore baseurl lines, but with example domain

* Tue Feb 11 2020 Mohan Boddu <mboddu@bhujji.com> - 33-0.1
- Setup for evergreen being F33

* Tue Feb 11 2020 Mohan Boddu <mboddu@bhujji.com> - 32-0.4
- Remove baseurl download.fp.o (puiterwijk)
- Enabling dnf countme

* Tue Jan 28 2020 Mohan Boddu <mboddu@bhujji.com> - 32-0.3
- Adding F33 key

* Mon Aug 19 2019 Kevin Fenzi <kevin@scrye.com> - 32-0.2
- Fix f32 key having extra spaces.

* Tue Aug 13 2019 Mohan Boddu <mboddu@bhujji.com> - 32-0.1
- Adding F32 key
- Setup for evergreen being f32

* Tue Mar 12 2019 Vít Ondruch <vondruch@redhat.com> - 31-0.3
- Allow to use newer GPG keys, so Rawhide can be updated after branch.

* Thu Mar 07 2019 Sinny Kumari <skumari@redhat.com> - 31-0.2
- Create fedora-repos-ostree sub-package

* Tue Feb 19 2019 Tomas Hrcka <thrcka@redhat.com> - 31-0.1
- Setup for evergreen being f31

* Mon Feb 18 2019 Mohan Boddu <mboddu@bhujji.com> - 30-0.4
- Adding F31 key

* Sat Jan 05 2019 Kevin Fenzi <kevin@scrye.com> - 30-0.3
- Add fedora-7-primary to archmap. Fixes bug #1531957
- Remove failovermethod option in repos (augenauf(Florian H))

* Tue Nov 13 2018 Mohan Boddu <mboddu@bhujji.com> - 30-0.2
- Adding fedora-iot-2019 key
- Enable skip_if_unavailable for cisco-openh264 repo

* Tue Aug 14 2018 Mohan Boddu <mboddu@bhujji.com> - 30-0.1
- Setup for evergreen being f30
