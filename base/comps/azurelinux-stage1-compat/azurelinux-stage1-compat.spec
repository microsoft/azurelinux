Summary:        Azure Linux Stage1 Compat
Name:           azurelinux-stage1-compat
Version:        0.1
Release:        %autorelease
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
%autochangelog
