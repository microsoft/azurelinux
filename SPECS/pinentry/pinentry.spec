Summary:        A collection of PIN or passphrase entry dialogs
Name:           pinentry
Version:        1.2.1
Release:        1%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/Cryptography
URL:            https://gnupg.org/software/pinentry/index.html
Source0:        https://gnupg.org/ftp/gcrypt/%{name}/%{name}-%{version}.tar.bz2
BuildRequires:  libassuan-devel >= 2.1.0
BuildRequires:  libgpg-error-devel >= 1.16
BuildRequires:  ncurses-devel
Requires:       libassuan >= 2.1.0
Requires:       libgpg-error >= 1.16
Requires:       ncurses-libs

%description
pinentry is a small collection of dialog programs that allow GnuPG to read passphrases and PIN numbers in a secure manner.
There are versions for the common GTK and Qt toolkits as well as for the text terminal (Curses).
They utilize the Assuan protocol as specified in the Libassuan manual.

%prep
%autosetup

%build
%configure \
    --enable-pinentry-tty
%make_build

%install
%make_install

%files
%defattr(-,root,root)
%license AUTHORS COPYING
%{_bindir}/pinentry
%{_bindir}/%{name}-curses
%{_bindir}/%{name}-tty
%{_infodir}/%{name}.info*
%exclude %{_infodir}/dir

%changelog
* Mon Nov 27 2023 Andrew Phelps <anphel@microsoft.com> - 1.2.1-1
- Upgrade to 1.2.1

* Mon Nov 22 2021 Olivia Crain <oliviacrain@microsoft.com> - 1.2.0-1
- Upgrade to latest upstream
- Better specify build/runtime requirements
- Lint spec
- License verified

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.1.0-3
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 1.1.0-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Mon Sep 24 2018 Dweep Advani <dadvani@vmware.com> - 1.1.0-1
- Update to version 1.1.0

* Wed Aug 16 2017 Danut Moraru <dmoraru@vmware.com> - 1.0.0-2
- Build pinentry-tty

* Wed Jun 07 2017 Danut Moraru <dmoraru@vmware.com> - 1.0.0-1
- Initial Build.
