# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary: Localizations for Gnulib
Name:    gnulib-l10n
Version: 20241231
Release: 1%{?dist}
License: LGPL-2.1-or-later

Url:     https://www.gnu.org/software/gnulib
Source0: https://ftp.gnu.org/gnu/gnulib/%{name}-%{version}.tar.gz
Source1: https://ftp.gnu.org/gnu/gnulib/%{name}-%{version}.tar.gz.sig

# From https://www.haible.de/bruno/gpgkeys.html
Source2: gnulib-l10n-keyring.gpg

# Machine objects (*.mo) are architecture independent.
BuildArch: noarch

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: gcc
BuildRequires: gettext-devel
BuildRequires: make

# For gpg verification of source tarball
BuildRequires: gnupg2

%description
The localizations for the GNU portability library.

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup

%build
%configure
%make_build

%install
%make_install
%find_lang gnulib

%files -f gnulib.lang
%doc ABOUT-NLS README
%license COPYING

%changelog
* Mon Sep 29 2025 Lukáš Zaoral <lzaoral@redhat.com> - 20241231-1
- Initial release

