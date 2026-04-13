# Standalone package for GDM PAM extension headers.
# Extracted from the gdm source to avoid pulling in the full GNOME display
# manager and its desktop stack. Only sssd needs these headers.

%global major_version %(echo %{version} | cut -d. -f1)

Name:           gdm-pam-extensions-devel
Version:        49.2
Release:        1%{?dist}
Summary:        Macros for developing GDM extensions to PAM
License:        GPL-2.0-or-later
URL:            https://wiki.gnome.org/Projects/GDM
Source0:        https://download.gnome.org/sources/gdm/%{major_version}/gdm-%{version}.tar.xz

BuildArch:      noarch
Requires:       pam-devel

# This package replaces the gdm-pam-extensions-devel subpackage from the
# full gdm build.
Provides:       gdm-pam-extensions-devel = 1:%{version}-%{release}
Conflicts:      gdm < 1:%{version}

%description
The gdm-pam-extensions-devel package contains headers and other
files that are helpful to PAM modules wishing to support
GDM specific authentication features.

This is a standalone extraction from the GDM source — it does not
require or include the GDM display manager.

%prep
%autosetup -n gdm-%{version}

%build
# Generate the pkgconfig file from the template
sed -e 's|@prefix@|%{_prefix}|' \
    -e 's|@exec_prefix@|%{_exec_prefix}|' \
    -e 's|@libdir@|%{_libdir}|' \
    -e 's|@includedir@|%{_includedir}|' \
    -e 's|@VERSION@|%{version}|' \
    pam-extensions/gdm-pam-extensions.pc.in > gdm-pam-extensions.pc

%install
install -dm755 %{buildroot}%{_includedir}/gdm
install -pm644 pam-extensions/gdm-pam-extensions.h %{buildroot}%{_includedir}/gdm/
install -pm644 pam-extensions/gdm-choice-list-pam-extension.h %{buildroot}%{_includedir}/gdm/
install -pm644 pam-extensions/gdm-custom-json-pam-extension.h %{buildroot}%{_includedir}/gdm/
install -pm644 pam-extensions/gdm-pam-extensions-common.h %{buildroot}%{_includedir}/gdm/
install -dm755 %{buildroot}%{_libdir}/pkgconfig
install -pm644 gdm-pam-extensions.pc %{buildroot}%{_libdir}/pkgconfig/

%files
%license COPYING
%{_includedir}/gdm/gdm-pam-extensions.h
%{_includedir}/gdm/gdm-choice-list-pam-extension.h
%{_includedir}/gdm/gdm-custom-json-pam-extension.h
%{_includedir}/gdm/gdm-pam-extensions-common.h
%{_libdir}/pkgconfig/gdm-pam-extensions.pc

%changelog
* Sat Apr 12 2026 Azure Linux Team <azurelinux@microsoft.com> - 49.2-1
- Standalone extraction of gdm-pam-extensions-devel from gdm 49.2
