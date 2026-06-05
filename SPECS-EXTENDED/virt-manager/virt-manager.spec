# -*- rpm-spec -*-

%global default_hvs         "qemu,xen,lxc"
%global have_spice         0

Name:           virt-manager
Version:        5.1.0
Release:        1%{?dist}
%global verrel %{version}-%{release}

Summary:        Desktop tool for managing virtual machines via libvirt
License:        GPL-2.0-or-later
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
BuildArch:      noarch
URL:            https://virt-manager.org/
Source0:        https://releases.pagure.org/%{name}/%{name}-%{version}.tar.xz

Patch1:         0001-virtinst-cloudinit-include-empty-meta-data-file.patch

Requires:       virt-manager-common = %{verrel}
Requires:       python3-gobject >= 3.31.3
Requires:       gtk3 >= 3.22.0
Requires:       libvirt-glib >= 0.0.9
%if %{have_spice}
Requires:       spice-gtk3
%endif

# virt-manager is one of those apps that people will often install onto
# a headless machine for use over SSH. This means the virt-manager dep
# chain needs to provide everything we need to get a usable app experience.
# Unfortunately nothing in our chain has an explicit dep on some kind
# of usable gsettings backend, so we explicitly depend on dconf so that
# user settings actually persist across app runs.
#
# That said, we skip this dep for flatpak, where dconf isn't used in
# the runtime. gsettings defaults to ini file in that case
%if ! 0%{?flatpak}
Requires:       dconf
%endif

# The vte291 package is actually the latest vte with API version 2.91, while
# the vte3 package is effectively a compat package with API version 2.90.
# virt-manager works fine with either, so pull the latest bits so there's
# no ambiguity.
Requires:       vte291

# We can use GtkTextView, gtksourceview 3 or gtksourceview4, recommend
# the latest one but don't make it a hard requirement
Recommends:     gtksourceview4

# Weak dependencies for the common virt-manager usecase
Recommends:     (libvirt-daemon-kvm or libvirt-daemon-qemu)
Recommends:     libvirt-daemon-config-network

# Optional inspection of guests
Suggests:       python3-libguestfs

BuildRequires:  gettext
BuildRequires:  python3-devel
BuildRequires:  python3-docutils
BuildRequires:  meson

%description
Virtual Machine Manager provides a graphical tool for administering virtual
machines for KVM, Xen, and LXC. Start, stop, add or remove virtual devices,
connect to a graphical or serial console, and see resource usage statistics
for existing VMs on local or remote machines. Uses libvirt as the backend
management API.

%package common
Summary:        Common files used by the different Virtual Machine Manager interfaces

Requires:       python3-argcomplete
Requires:       python3-libvirt
Requires:       python3-libxml2
Requires:       python3-requests
Requires:       libosinfo >= 0.2.10
# Required for gobject-introspection infrastructure
Requires:       python3-gobject-base
# Required for pulling files from iso media
Requires:       xorriso

%description common
Common files used by the different virt-manager interfaces, as well as
virt-install related tools.

%package -n virt-install
Summary:        Utilities for installing virtual machines

Requires:       virt-manager-common = %{verrel}
# For 'virsh console'
Requires:       libvirt-client

Provides:       virt-install
Provides:       virt-clone
Provides:       virt-xml

%description -n virt-install
Package includes several command line utilities, including virt-install
(build and install new VMs) and virt-clone (clone an existing virtual
machine).

%prep
%autosetup -p1

%build
%if ! %{have_spice}
%global _default_graphics -Ddefault-graphics=vnc
%endif

%meson \
    -Ddefault-hvs=%{default_hvs} \
    %{?_default_graphics} \
    -Dupdate-icon-cache=false \
    -Dcompile-schemas=false \
    -Dtests=disabled
%meson_build

%install
%meson_install

%find_lang %{name}

%if 0%{?py_byte_compile:1}
%py_byte_compile %{__python3} %{buildroot}%{_datadir}/virt-manager/
%endif

%files
%{_bindir}/%{name}

%{_mandir}/man1/%{name}.1*

%{_datadir}/%{name}/ui
%{_datadir}/%{name}/virtManager

%{_datadir}/%{name}/icons
%{_datadir}/icons/hicolor/*/apps/*

%{_datadir}/applications/%{name}.desktop
%{_datadir}/glib-2.0/schemas/org.virt-manager.virt-manager.gschema.xml
%{_datadir}/metainfo/%{name}.appdata.xml

%files common -f %{name}.lang
%license COPYING
%doc README.md NEWS.md

%dir %{_datadir}/%{name}
%{_datadir}/%{name}/virtinst

%files -n virt-install
%{_mandir}/man1/virt-install.1*
%{_mandir}/man1/virt-clone.1*
%{_mandir}/man1/virt-xml.1*

%{_datadir}/bash-completion/completions/virt-install
%{_datadir}/bash-completion/completions/virt-clone
%{_datadir}/bash-completion/completions/virt-xml

%{_bindir}/virt-install
%{_bindir}/virt-clone
%{_bindir}/virt-xml

%changelog
* Mon Apr 6 2026 Akarsh Chaudhary <v-akarshc@microsoft.com> - 5.1.0-1
- Initial CBL-Mariner import from Fedora 44 (license: MIT).
- License verified
