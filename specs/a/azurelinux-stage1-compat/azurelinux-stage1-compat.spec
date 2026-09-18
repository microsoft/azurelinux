# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary:        Azure Linux Stage1 Compat
Name:           azurelinux-stage1-compat
Version:        0.1
Release:        1%{?dist}
License:        MIT
URL:            https://aka.ms/azurelinux

BuildArch:      noarch

%description
Compatibility package only used for Stage 1 bootstrapping.

%build

%install
mkdir -p %{buildroot}/usr/bin

for arch in x86_64 aarch64; do
    ln -sf ${arch}-redhat-linux-gnu-pkg-config %{buildroot}/usr/bin/${arch}-azurelinux-linux-gnu-pkg-config
done

%files
/usr/bin/*-azurelinux-linux-gnu-pkg-config

%changelog
* Mon Mar 02 2026 Reuben Olinsky <reubeno@microsoft.com> - 0.1-1
- Initial version
