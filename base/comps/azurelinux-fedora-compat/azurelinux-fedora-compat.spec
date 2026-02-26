
Summary:        Azure Linux bootstrap Fedora compat
Name:           azurelinux-fedora-compat
Version:        4.0
Release:        %autorelease
License:        MIT
URL:            https://aka.ms/azurelinux

BuildArch:      noarch

%description
Azure Linux compatibility with Fedora. This generates any symlinks, files,
dirs, etc with RedHat/Fedora naming until users of those names can be changed.

%package release
Provides: fedora-release
Requires: azurelinux-release
%description release
Azure Linux compatibility providing 'fedora-release'.

%package release-variant
Provides: fedora-release-variant
Requires: azurelinux-release-variant
%description release-variant
Azure Linux compatibility providing 'fedora-release-variant'.

%package release-common
Provides: fedora-release-common
Requires: azurelinux-release-common
%description release-common
Azure Linux compatibility providing 'fedora-release-common'.

%package release-identity
Provides: fedora-release-identity
Requires: azurelinux-release-identity
%description release-identity
Azure Linux compatibility providing 'fedora-release-identity'.

%package repos
Provides: fedora-repos
Requires: azurelinux-repos
%description repos
Azure Linux compatibility providing 'fedora-repos'.

%package gpg-keys
Provides: fedora-gpg-keys
Requires: azurelinux-gpg-keys
%description gpg-keys
Azure Linux compatibility providing 'fedora-gpg-keys'.

%package rpm-config
Provides: redhat-rpm-config = 1004
Requires: azurelinux-rpm-config
%description rpm-config
Azure Linux compatibility providing 'redhat-rpm-config'.

%prep

%build

%install
install -d -m 0755 %{buildroot}/usr/lib/rpm
ln -s azurelinux %{buildroot}/usr/lib/rpm/redhat

%files

%files rpm-config
/usr/lib/rpm/redhat

%changelog
%autochangelog
