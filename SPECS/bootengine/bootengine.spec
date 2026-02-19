%define commit_hash daf43bf9c1ca45bf1a43566c3a6f96ec0cb44a36

Name:           bootengine
Version:        0.0.38
Release:        1%{?dist}
Summary:        Flatcar bootengine dracut modules and helper utilities

License:        BSD-2-Clause
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/flatcar/bootengine
Source0:        https://github.com/flatcar/bootengine/archive/%{commit_hash}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         0001-modify-tests.patch
BuildArch:      noarch
BuildRequires:  dracut
Requires:       util-linux

# Keep this local so the spec works even if a global dracut macro isn't defined.
%global dracutlibdir %{_prefix}/lib/dracut

%description
Flatcar bootengine content intended for initramfs usage via dracut modules.
This package installs the bootengine dracut module directory (modules.d)
and any included helper utilities/scripts from the Flatcar bootengine source.

%prep
%autosetup -p1 -n %{name}-%{commit_hash}

%build
# no build step (content is scripts/modules)

%install
rm -rf %{buildroot}

# Install dracut modules
# Adjust "dracut/modules.d/*" if upstream uses a different directory.
if [ -d dracut ]; then
  install -d -p %{buildroot}%{dracutlibdir}/modules.d
  cp -a dracut/* %{buildroot}%{dracutlibdir}/modules.d/
fi

# Optional: install any helper script if present (adjust names as needed)
# Common pattern: provide a helper in %{_sbindir} or %{_bindir}
if [ -f update-bootengine ]; then
  install -d -p %{buildroot}%{_sbindir}
  install -p -m 0755 update-bootengine %{buildroot}%{_sbindir}/update-bootengine
fi

chmod +x \
  %{buildroot}%{dracutlibdir}/modules.d/10*-generator/*-generator \
  %{buildroot}%{dracutlibdir}/modules.d/10diskless-generator/diskless-btrfs \
  %{buildroot}%{dracutlibdir}/modules.d/10networkd-dependency-generator/*-generator \
  %{buildroot}%{dracutlibdir}/modules.d/03flatcar-network/parse-ip-for-networkd.sh \
  %{buildroot}%{dracutlibdir}/modules.d/30disk-uuid/disk-uuid.sh \
  %{buildroot}%{dracutlibdir}/modules.d/30ignition/ignition-generator \
  %{buildroot}%{dracutlibdir}/modules.d/30ignition/ignition-setup.sh \
  %{buildroot}%{dracutlibdir}/modules.d/30ignition/ignition-setup-pre.sh \
  %{buildroot}%{dracutlibdir}/modules.d/30ignition/ignition-kargs-helper \
  %{buildroot}%{dracutlibdir}/modules.d/30ignition/retry-umount.sh \
  %{buildroot}%{dracutlibdir}/modules.d/99setup-root/initrd-setup-root \
  %{buildroot}%{dracutlibdir}/modules.d/99setup-root/initrd-setup-root-after-ignition \
  %{buildroot}%{dracutlibdir}/modules.d/99setup-root/gpg-agent-wrapper

%check
./test

%files
%license LICENSE
%doc README.md
%{dracutlibdir}/modules.d/*
%{_sbindir}/update-bootengine

%changelog
* Tue Jan 27 2026 Sumit Jena <v-sumitjena@microsoft.com> - 0.0.38-1
- Initial Azure Linux import from the source project (license: same as "License" tag).
- License verified.
