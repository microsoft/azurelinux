%global debug_package %{nil}

Summary:        Azure Linux shim-to-systemd-boot UKI boot layout
Name:           azurelinux-uki-boot
Version:        0.1.0
Release:        %autorelease
License:        MIT
URL:            https://github.com/microsoft/azurelinux
ExclusiveArch:  x86_64
BuildRequires:  efi-srpm-macros

Source1:        50-azurelinux-uki.conf
Source2:        entry-token
Source3:        loader.conf
Source4:        azurelinux-uki-boot.conf

Requires:       shim-%{efi_arch}
Requires:       systemd-boot
Requires:       kernel-uki-virt
Requires:       coreutils
Conflicts:      grub2-efi-%{efi_arch}
Conflicts:      uki-direct

%description
Configure Azure Linux UKI booting through shim and systemd-boot. The stock
shim, systemd-boot, and kernel-uki-virt packages are used unmodified; this
package supplies the kernel-install and ESP configuration and copies
systemd-boot to shim's second-stage path. Secure Boot requires the installed
systemd-boot binary to be signed by a key that shim trusts.

This package is intended for fresh x86_64 UKI boot layouts and their later
package updates. Installing it over an existing boot layout is not supported.

%prep

%build

%install
install -d -m 0755 %{buildroot}%{_prefix}/lib/kernel/install.conf.d
install -m 0644 %{SOURCE1} %{buildroot}%{_prefix}/lib/kernel/install.conf.d/50-azurelinux-uki.conf
install -d -m 0755 %{buildroot}%{_sysconfdir}/kernel
install -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/kernel/entry-token
install -d -m 0700 %{buildroot}%{efi_esp_root}/loader
install -m 0700 %{SOURCE3} %{buildroot}%{efi_esp_root}/loader/loader.conf
install -d -m 0755 %{buildroot}%{_sysconfdir}/dnf/protected.d
install -m 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/dnf/protected.d/%{name}.conf

# Firmware reads EFI programs from the ESP; shim loads grub<arch>.efi from its
# vendor directory. The signing pipeline signs the canonical systemd-boot binary
# under /usr/lib/systemd/boot/efi, not an ESP copy: keep those bytes identical.
# This runs at the end of transactions installing/updating/reinstalling that tree
# (including the initial image transaction), or when installed after systemd-boot.
# bootctl update does not manage this copy. After fixing an ESP error, restore it
# with "dnf reinstall systemd-boot" and verify it with
# "cmp /usr/lib/systemd/boot/efi/systemd-boot%{efi_arch}.efi %{efi_esp_dir}/grub%{efi_arch}.efi".
%transfiletriggerin -- /usr/lib/systemd/boot/efi
set -eu
src=/usr/lib/systemd/boot/efi/systemd-boot%{efi_arch}.efi
dir=%{efi_esp_dir}
dest="$dir/grub%{efi_arch}.efi"
tmp="$dest.new"

# 1. Consume RPM's matched-path list even on a no-op, so its writer sees no SIGPIPE.
cat >/dev/null
# Other EFI files can fire this trigger: an absent source is a no-op.
# A present but unreadable or broken source must fail during the copy.
if [ ! -e "$src" ] && [ ! -L "$src" ]; then exit 0; fi

# 2. Create shim's ESP vendor directory, then copy with the required permissions.
# Clean up an incomplete .new on every failure, including a failed rename.
trap 'rm -f -- "$tmp"' 0
if ! install -d -m 0700 -- "$dir"; then
    echo "azurelinux-uki-boot: cannot create $dir" >&2
    exit 1
fi
if ! install -m 0700 -- "$src" "$tmp"; then
    echo "azurelinux-uki-boot: cannot copy $src to $tmp" >&2
    exit 1
fi
# 3. Flush the copy so a crash cannot leave a renamed but incomplete second stage.
if ! sync -- "$tmp"; then
    echo "azurelinux-uki-boot: cannot flush $tmp" >&2
    exit 1
fi
# 4. Atomically replace the second stage; fail if the destination is a directory.
if ! mv -fT -- "$tmp" "$dest"; then
    echo "azurelinux-uki-boot: cannot replace $dest" >&2
    exit 1
fi
trap - 0
# 5. Persist the rename on the ESP.
if ! sync -f -- "$dest"; then
    echo "azurelinux-uki-boot: cannot sync the file system holding $dest" >&2
    exit 1
fi

%files
# kernel-install selects the ESP as boot root and the stable azurelinux entry token.
%dir %{_prefix}/lib/kernel/install.conf.d
%{_prefix}/lib/kernel/install.conf.d/50-azurelinux-uki.conf
%config(noreplace) %{_sysconfdir}/kernel/entry-token
# systemd-boot selects the default azurelinux-* entry at the ESP loader path.
%dir %attr(0700,root,root) %{efi_esp_root}/loader
%config(noreplace) %attr(0700,root,root) %{efi_esp_root}/loader/loader.conf
# Like GRUB, which otherwise owns this second stage, dnf must not remove this package.
%config(noreplace) %{_sysconfdir}/dnf/protected.d/%{name}.conf
# The trigger creates this copy at transaction end, not in the RPM payload.
%ghost %attr(0700,root,root) %{efi_esp_dir}/grub%{efi_arch}.efi

%changelog
%autochangelog
