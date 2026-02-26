
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

%prep

%build

%install

%files

%changelog
%autochangelog
