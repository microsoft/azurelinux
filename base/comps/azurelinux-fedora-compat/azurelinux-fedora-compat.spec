
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

%prep

%build

%install

%files

%changelog
%autochangelog
