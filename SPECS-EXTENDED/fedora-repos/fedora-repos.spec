Vendor:         Microsoft Corporation
Distribution:   Mariner
%global rawhide_release 38
%global updates_testing_enabled 0

Summary:        Fedora package repositories
Name:           fedora-repos
Version:        37
Release:        2%{?eln:.eln%{eln}}
License:        MIT
URL:            https://fedoraproject.org/

Provides:       fedora-repos(%{version}) = %{release}
Requires:       system-release(%{version})
Obsoletes:      fedora-repos < 33-0.7
%if %{rawhide_release} == %{version}
Requires:       fedora-repos-rawhide = %{version}-%{release}
%endif
Requires:       fedora-gpg-keys >= %{version}-%{release}
BuildArch:      noarch
# Required by %%check
BuildRequires:  gnupg sed

Source1:        archmap
Source2:        fedora.repo
Source3:        fedora-updates.repo
Source4:        fedora-updates-testing.repo
Source5:        fedora-rawhide.repo
Source6:        fedora-cisco-openh264.repo
Source7:        fedora-updates-archive.repo
Source8:        fedora-eln.repo


Source10:       RPM-GPG-KEY-fedora-7-primary
Source11:       RPM-GPG-KEY-fedora-8-primary
Source12:       RPM-GPG-KEY-fedora-8-primary-original
Source13:       RPM-GPG-KEY-fedora-9-primary
Source14:       RPM-GPG-KEY-fedora-9-primary-original
Source15:       RPM-GPG-KEY-fedora-9-secondary
Source16:       RPM-GPG-KEY-fedora-10-primary
Source17:       RPM-GPG-KEY-fedora-11-primary
Source18:       RPM-GPG-KEY-fedora-12-primary
Source19:       RPM-GPG-KEY-fedora-13-primary
Source20:       RPM-GPG-KEY-fedora-13-secondary
Source21:       RPM-GPG-KEY-fedora-14-primary
Source22:       RPM-GPG-KEY-fedora-14-secondary
Source23:       RPM-GPG-KEY-fedora-15-primary
Source24:       RPM-GPG-KEY-fedora-15-secondary
Source25:       RPM-GPG-KEY-fedora-16-primary
Source26:       RPM-GPG-KEY-fedora-16-secondary
Source27:       RPM-GPG-KEY-fedora-17-primary
Source28:       RPM-GPG-KEY-fedora-17-secondary
Source29:       RPM-GPG-KEY-fedora-18-primary
Source30:       RPM-GPG-KEY-fedora-18-secondary
Source31:       RPM-GPG-KEY-fedora-19-primary
Source32:       RPM-GPG-KEY-fedora-19-secondary
Source33:       RPM-GPG-KEY-fedora-20-primary
Source34:       RPM-GPG-KEY-fedora-20-secondary
Source35:       RPM-GPG-KEY-fedora-21-primary
Source36:       RPM-GPG-KEY-fedora-21-secondary
Source37:       RPM-GPG-KEY-fedora-22-primary
Source38:       RPM-GPG-KEY-fedora-22-secondary
Source39:       RPM-GPG-KEY-fedora-23-primary
Source40:       RPM-GPG-KEY-fedora-23-secondary
Source41:       RPM-GPG-KEY-fedora-24-primary
Source42:       RPM-GPG-KEY-fedora-24-secondary
Source43:       RPM-GPG-KEY-fedora-25-primary
Source44:       RPM-GPG-KEY-fedora-25-secondary
Source45:       RPM-GPG-KEY-fedora-26-primary
Source46:       RPM-GPG-KEY-fedora-26-secondary
Source47:       RPM-GPG-KEY-fedora-27-primary
Source48:       RPM-GPG-KEY-fedora-28-primary
Source49:       RPM-GPG-KEY-fedora-29-primary
Source50:       RPM-GPG-KEY-fedora-30-primary
Source51:       RPM-GPG-KEY-fedora-31-primary
Source52:       RPM-GPG-KEY-fedora-32-primary
Source53:       RPM-GPG-KEY-fedora-33-primary
Source54:       RPM-GPG-KEY-fedora-34-primary
Source55:       RPM-GPG-KEY-fedora-35-primary
Source56:       RPM-GPG-KEY-fedora-36-primary
Source57:       RPM-GPG-KEY-fedora-37-primary
Source58:       RPM-GPG-KEY-fedora-38-primary
Source59:       RPM-GPG-KEY-fedora-39-primary
Source60:       RPM-GPG-KEY-fedora-40-primary
# When bumping Rawhide to fN, create N+1 key (and update archmap). (This
# ensures users have the next future key installed and referenced, even if they
# don't update very often. This will smooth out Rawhide N->N+1 transition for them).

Source100:      fedora-modular.repo
Source101:      fedora-updates-modular.repo
Source102:      fedora-updates-testing-modular.repo
Source103:      fedora-rawhide-modular.repo
Source104:      RPM-GPG-KEY-fedora-modularity

Source150:      RPM-GPG-KEY-fedora-iot-2019
Source151:      fedora.conf
Source152:      fedora-compose.conf

%description
Fedora package repository files for yum and dnf along with gpg public keys.

%package modular
Summary:        Fedora modular package repositories
Requires:       fedora-repos = %{version}-%{release}
%if %{rawhide_release} == %{version}
Requires:       fedora-repos-rawhide-modular = %{version}-%{release}
%endif
Obsoletes:      fedora-repos < 33-0.7

%description modular
This package provides the repo definitions with modular packages.

%package rawhide
Summary:        Rawhide repo definitions
Requires:       fedora-repos = %{version}-%{release}
Obsoletes:      fedora-repos-rawhide < 33-0.7

%description rawhide
This package provides the rawhide repo definitions.

%package archive
Summary:        Fedora updates archive package repository
Requires:       fedora-repos = %{version}-%{release}

%description archive
This package provides the repo definition for the updates archive repo.
It is a package repository that contains any RPM that has made it to
stable in Bodhi and been available in the Fedora updates repo in the past.

%package rawhide-modular
Summary:        Rawhide modular repo definitions
Requires:       fedora-repos = %{version}-%{release}
Requires:       fedora-repos-rawhide = %{version}-%{release}
Obsoletes:      fedora-repos-rawhide < 33-0.7

%description rawhide-modular
This package provides the rawhide modular repo definitions.

%package -n fedora-gpg-keys
Summary:        Fedora RPM keys

%description -n fedora-gpg-keys
This package provides the RPM signature keys.


%package ostree
Summary:        OSTree specific files

%description ostree
This package provides ostree specfic files like remote config from
where client's system will pull OSTree updates.


%package eln
Summary: ELN repo definitions

%description eln
This package provides repository files for ELN (Enterprise Linux Next)
packages. Note that these packages are experimental and should not be used
in a production environment.


%prep

%build

%install
# Install the keys
install -d -m 755 $RPM_BUILD_ROOT/etc/pki/rpm-gpg
install -m 644 %{_sourcedir}/RPM-GPG-KEY* $RPM_BUILD_ROOT/etc/pki/rpm-gpg/

# Link the primary/secondary keys to arch files, according to archmap.
# Ex: if there's a key named RPM-GPG-KEY-fedora-19-primary, and archmap
#     says "fedora-19-primary: i386 x86_64",
#     RPM-GPG-KEY-fedora-19-{i386,x86_64} will be symlinked to that key.
pushd $RPM_BUILD_ROOT/etc/pki/rpm-gpg/
# Also add a symlink for Rawhide and ELN keys
ln -s RPM-GPG-KEY-fedora-%{rawhide_release}-primary RPM-GPG-KEY-fedora-rawhide-primary
ln -s RPM-GPG-KEY-fedora-%{rawhide_release}-primary RPM-GPG-KEY-fedora-eln-primary
for keyfile in RPM-GPG-KEY*; do
    # resolve symlinks, so that we don't need to keep duplicate entries in archmap
    real_keyfile=$(basename $(readlink -f $keyfile))
    key=${real_keyfile#RPM-GPG-KEY-} # e.g. 'fedora-20-primary'
    if ! grep -q "^${key}:" %{_sourcedir}/archmap; then
        echo "ERROR: no archmap entry for $key"
        exit 1
    fi
    arches=$(sed -ne "s/^${key}://p" %{_sourcedir}/archmap)
    for arch in $arches; do
        # replace last part with $arch (fedora-20-primary -> fedora-20-$arch)
        ln -s $keyfile ${keyfile%%-*}-$arch # NOTE: RPM replaces %% with %
    done
done
# and add symlink for compat generic location
ln -s RPM-GPG-KEY-fedora-%{version}-primary RPM-GPG-KEY-%{version}-fedora
popd

# Install repo files
install -d -m 755 $RPM_BUILD_ROOT/etc/yum.repos.d
for file in %{_sourcedir}/fedora*repo ; do
  install -m 644 $file $RPM_BUILD_ROOT/etc/yum.repos.d
done

# Enable or disable repos based on current release cycle state.
%if 0%{?eln}
rawhide_enabled=0
stable_enabled=0
testing_enabled=0
archive_enabled=0
eln_enabled=1
%elif %{rawhide_release} == %{version}
rawhide_enabled=1
stable_enabled=0
testing_enabled=0
archive_enabled=0
eln_enabled=0
%else
rawhide_enabled=0
stable_enabled=1
testing_enabled=%{updates_testing_enabled}
archive_enabled=1
eln_enabled=0
%endif
for repo in $RPM_BUILD_ROOT/etc/yum.repos.d/fedora-rawhide*.repo; do
    sed -i "s/^enabled=AUTO_VALUE$/enabled=${rawhide_enabled}/" $repo || exit 1
done
for repo in $RPM_BUILD_ROOT/etc/yum.repos.d/fedora{,-modular,-updates,-updates-modular}.repo; do
    sed -i "s/^enabled=AUTO_VALUE$/enabled=${stable_enabled}/" $repo || exit 1
done
for repo in $RPM_BUILD_ROOT/etc/yum.repos.d/fedora-updates-testing{,-modular}.repo; do
    sed -i "s/^enabled=AUTO_VALUE$/enabled=${testing_enabled}/" $repo || exit 1
done
for repo in $RPM_BUILD_ROOT/etc/yum.repos.d/fedora-updates-archive.repo; do
    sed -i "s/^enabled=AUTO_VALUE$/enabled=${archive_enabled}/" $repo || exit 1
done
for repo in $RPM_BUILD_ROOT/etc/yum.repos.d/fedora-eln*.repo; do
    sed -i "s/^enabled=AUTO_VALUE$/enabled=${eln_enabled}/" $repo || exit 1
done

# Adjust Rawhide repo files to include Rawhide+1 GPG key.
# This is necessary for the period when Rawhide gets bumped to N+1 and packages
# start to be signed with a newer key. Without having the key specified in the
# repo file, the system would consider the new packages as untrusted.
rawhide_next=$((%{rawhide_release}+1))
for repo in $RPM_BUILD_ROOT/etc/yum.repos.d/fedora-rawhide*.repo; do
    sed -i "/^gpgkey=/ s@AUTO_VALUE@file:///etc/pki/rpm-gpg/RPM-GPG-KEY-fedora-${rawhide_next}-\$basearch@" \
        $repo || exit 1
done

# Set appropriate metadata_expire in base repo files (6h before Final, 7d after)
%if "%{release}" < "1"
expire_value='6h'
%else
expire_value='7d'
%endif
for repo in $RPM_BUILD_ROOT/etc/yum.repos.d/fedora{,-modular}.repo; do
    sed -i "/^metadata_expire=/ s/AUTO_VALUE/${expire_value}/" \
        $repo || exit 1
done

# Install ostree remote config
install -d -m 755 $RPM_BUILD_ROOT/etc/ostree/remotes.d/
install -m 644 %{_sourcedir}/fedora.conf $RPM_BUILD_ROOT/etc/ostree/remotes.d/
install -m 644 %{_sourcedir}/fedora-compose.conf $RPM_BUILD_ROOT/etc/ostree/remotes.d/


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

%if 0%{?eln}
enabled_repos+=(fedora-eln)
disabled_repos+=(fedora fedora-modular fedora-updates fedora-updates-archive \
  fedora-updates-modular fedora-updates-testing fedora-updates-testing-modular)
%elif %{rawhide_release} == %{version}
enabled_repos+=(fedora-rawhide fedora-rawhide-modular fedora-cisco-openh264)
disabled_repos+=(fedora fedora-modular fedora-updates fedora-updates-archive \
  fedora-updates-modular fedora-updates-testing fedora-updates-testing-modular)
%else
enabled_repos+=(fedora fedora-modular fedora-updates fedora-updates-archive \
  fedora-updates-modular)
disabled_repos+=(fedora-rawhide fedora-rawhide-modular)
%if %{updates_testing_enabled}
enabled_repos+=(fedora-updates-testing fedora-updates-testing-modular)
%else
disabled_repos+=(fedora-updates-testing fedora-updates-testing-modular)
%endif
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

# Make sure updates-testing is not enabled in a Final (stable) release
%if "%{release}" >= "1"
for repo in $RPM_BUILD_ROOT/etc/yum.repos.d/fedora-updates-testing{,-modular}.repo; do
    if grep -q 'enabled=1' $repo; then
        echo "ERROR: Repo $repo should be disabled in a stable release, but it isn't"
        exit 1
    fi
done
%endif

# Make sure metadata_expire was correctly set
%if "%{release}" < "1"
expire_value='6h'
%else
expire_value='7d'
%endif
for repo in $RPM_BUILD_ROOT/etc/yum.repos.d/fedora{,-modular}.repo; do
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

# Make sure the Rawhide+1 key wasn't forgotten to be created
rawhide_next=$((%{rawhide_release}+1))
test -n "$rawhide_next" || exit 1
if ! test -f $RPM_BUILD_ROOT/etc/pki/rpm-gpg/RPM-GPG-KEY-fedora-${rawhide_next}-primary; then
    echo "ERROR: GPG key for Fedora ${rawhide_next} is not present"
    exit 1
fi

# Make sure the Rawhide+1 key is present in Rawhide repo files
for repo in $RPM_BUILD_ROOT/etc/yum.repos.d/fedora-rawhide*.repo; do
    gpg_lines=$(grep '^gpgkey=' $repo)
    if test -z "$gpg_lines"; then
        echo "ERROR: No gpgkey= lines in $repo"

        exit 1
    fi
    while IFS= read -r line; do
        if ! echo "$line" | grep -q "RPM-GPG-KEY-fedora-${rawhide_next}"; then
            echo "ERROR: Fedora ${rawhide_next} GPG key missing in $repo"
            exit 1
        fi
    done <<< "$gpg_lines"
done

# Check arch keys exists on supported architectures
TMPRING=$(mktemp)
for VER in %{version} %{rawhide_release} ${rawhide_next}; do
  echo -n > "$TMPRING"
  for ARCH in $(sed -ne "s/^fedora-${VER}-primary://p" %{_sourcedir}/archmap)
  do
    gpg --no-default-keyring --keyring="$TMPRING" \
      --import $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-fedora-$VER-$ARCH
  done
  # Ensure some arch key was imported
  gpg --no-default-keyring --keyring="$TMPRING" --list-keys | grep -A 2 '^pub\s'
done
rm -f "$TMPRING"

%files
%dir /etc/yum.repos.d
%config(noreplace) /etc/yum.repos.d/fedora.repo
%config(noreplace) /etc/yum.repos.d/fedora-cisco-openh264.repo
%config(noreplace) /etc/yum.repos.d/fedora-updates.repo
%config(noreplace) /etc/yum.repos.d/fedora-updates-testing.repo

%files modular
%config(noreplace) /etc/yum.repos.d/fedora-modular.repo
%config(noreplace) /etc/yum.repos.d/fedora-updates-modular.repo
%config(noreplace) /etc/yum.repos.d/fedora-updates-testing-modular.repo

%files archive
%config(noreplace) /etc/yum.repos.d/fedora-updates-archive.repo

%files rawhide
%config(noreplace) /etc/yum.repos.d/fedora-rawhide.repo

%files rawhide-modular
%config(noreplace) /etc/yum.repos.d/fedora-rawhide-modular.repo


%files -n fedora-gpg-keys
%dir /etc/pki/rpm-gpg
/etc/pki/rpm-gpg/RPM-GPG-KEY-*


%files ostree
%dir /etc/ostree/remotes.d/
/etc/ostree/remotes.d/fedora.conf
/etc/ostree/remotes.d/fedora-compose.conf

%files eln
%config(noreplace) /etc/yum.repos.d/fedora-eln.repo


%changelog
* Sun Jan 29 2023 Tomas Hrcka <thrcka@redhat.com> - 37-2
- Adding F40 key

* Mon Oct 10 2022 Kevin Fenzi <kevin@scrye.com> - 37-1
- Setup for f37 release. rhbz#2133425

* Tue Aug 16 2022 Adam Williamson <awilliam@redhat.com> - 37.0-6
- Fix RPM-GPG-KEY-fedora-39-primary (dustymabe)

* Tue Aug 09 2022 Tomas Hrcka <thrcka@redhat.com> - 37-0.5
- updated archmap

* Tue Aug 09 2022 Tomas Hrcka <thrcka@redhat.com> - 37-0.4
- Setup for rawhide being F38
- Adding F39 key
- enable updates-testing for Branched

* Wed Jun 08 2022 Stephen Gallagher <sgallagh@redhat.com> - 37-0.3
- ELN: don't enable layered product repos by default

* Wed May 25 2022 Stephen Gallagher <sgallagh@redhat.com> - 37-0.2
- Rework Fedora ELN repositories

* Tue Feb 08 2022 Tomas Hrcka <thrcka@redhat.com> - 37-0.1
- Setup for rawhide being F37
- Adding F38 key

* Tue Aug 17 2021 Tomas Hrcka <thrcka@redhat.com> - 36-0.3
- Remove spurious space in RPM-GPG-KEY-fedora-37-primary (cgwalters)

* Tue Aug 10 2021 Tomas Hrcka <thrcka@redhat.com> - 36-0.2
- Setup for rawhide being F36

* Wed Apr 28 2021 Dusty Mabe <dusty@dustymabe.com> - 35-0.4
- Enable the updates archive repo on non-rawhide.

* Fri Feb 19 2021 Petr Menšík <pemensik@redhat.com> - 35-0.3
- Check arch key imports during build (#1872248)

* Wed Feb 17 2021 Mohan Boddu <mboddu@bhujji.com> - 35-0.2
- Support $releasever=rawhide on Rawhide (kparal)
- Make archmap entries mandatory, except symlinks (kparal)
- Fixing F36 key

* Tue Feb 09 2021 Tomas Hrcka <thrcka@redhat.com> - 35-0.1
- Setup for rawhide being F35

* Tue Feb 09 2021 Mohan Boddu <mboddu@bhujji.com> - 34-0.10
- Fixing archmap for F35

* Thu Feb 04 2021 Mohan Boddu <mboddu@bhujji.com> - 34-0.9
- Adding F35 key

* Wed Oct 14 2020 Stephen Gallagher <sgallagh@redhat.com> - 34-0.8
- ELN: Drop dependency on fedora-repos-rawhide-modular

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
- Setup for rawhide being F34

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
- Setup for rawhide being F33

* Tue Feb 11 2020 Mohan Boddu <mboddu@bhujji.com> - 32-0.4
- Remove baseurl download.fp.o (puiterwijk)
- Enabling dnf countme

* Tue Jan 28 2020 Mohan Boddu <mboddu@bhujji.com> - 32-0.3
- Adding F33 key

* Mon Aug 19 2019 Kevin Fenzi <kevin@scrye.com> - 32-0.2
- Fix f32 key having extra spaces.

* Tue Aug 13 2019 Mohan Boddu <mboddu@bhujji.com> - 32-0.1
- Adding F32 key
- Setup for rawhide being f32

* Tue Mar 12 2019 Vít Ondruch <vondruch@redhat.com> - 31-0.3
- Allow to use newer GPG keys, so Rawhide can be updated after branch.

* Thu Mar 07 2019 Sinny Kumari <skumari@redhat.com> - 31-0.2
- Create fedora-repos-ostree sub-package

* Tue Feb 19 2019 Tomas Hrcka <thrcka@redhat.com> - 31-0.1
- Setup for rawhide being f31

* Mon Feb 18 2019 Mohan Boddu <mboddu@bhujji.com> - 30-0.4
- Adding F31 key

* Sat Jan 05 2019 Kevin Fenzi <kevin@scrye.com> - 30-0.3
- Add fedora-7-primary to archmap. Fixes bug #1531957
- Remove failovermethod option in repos (augenauf(Florian H))

* Tue Nov 13 2018 Mohan Boddu <mboddu@bhujji.com> - 30-0.2
- Adding fedora-iot-2019 key
- Enable skip_if_unavailable for cisco-openh264 repo

* Tue Aug 14 2018 Mohan Boddu <mboddu@bhujji.com> - 30-0.1
- Setup for rawhide being f30
