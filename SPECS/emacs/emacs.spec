Summary:        GNU Emacs text editor
Name:           emacs
Version:        28.1
Release:        3%{?dist}
Vendor:         Microsoft Corporation
Distribution:   Mariner
License:        GPLv3+ and CC0-1.0
URL:            https://www.gnu.org/software/emacs/
Group:          Applications/Editors
Source0:        https://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  ncurses-devel
BuildRequires:  systemd-devel
BuildRequires:  gnutls-devel

%description
Emacs is a powerful, customizable, self-documenting, modeless text
editor. Emacs contains special code editing features, a scripting
language (elisp), and the capability to read mail, news, and more
without leaving the editor.

%prep
%autosetup

%build
%configure \
            --without-xpm            \
            --without-jpeg           \
            --without-tiff           \
            --without-gif            \
            --without-png            \
            --without-rsvg           \
            --without-lcms2          \
            --without-xft            \
            --without-harfbuzz       \
            --without-m17n-flt       \
            --without-toolkit-scroll-bars \
            --without-xaw3d          \
            --without-xim            \
            --without-makeinfo
%make_build

%install
%make_install

rm -rf %{buildroot}%{_infodir}
rm -rf %{buildroot}%{_mandir}
rm -rf %{buildroot}%{_datadir}/icons

rm %{buildroot}%{_bindir}/ctags
rm %{buildroot}%{_datadir}/applications/*.desktop

%files
%defattr(-,root,root)
%{_bindir}/ebrowse
%{_bindir}/emacs
%{_bindir}/emacs-%{version}
%{_bindir}/emacsclient
%{_bindir}/etags
%{_includedir}/emacs-module.h
%{_libdir}/systemd/user/emacs.service
%{_libexecdir}/emacs
%{_datadir}/emacs/%{version}/etc/*
%{_datadir}/emacs/%{version}/lisp/*
%{_datadir}/emacs/%{version}/site-lisp/subdirs.el
%{_datadir}/emacs/site-lisp/subdirs.el
%{_datadir}/metainfo/emacs.metainfo.xml

%changelog
* Fri Jun 17 2022 Muhammad Falak <mwani@microsoft.com> - 28.1-3
- Nopatch CVE-2007-6109

* Tue Jun 14 2022 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 28.1-2
- Initial CBL-Mariner import from Photon (license: Apache2).
- License verified

* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> - 28.1-1
- Automatic Version Bump

* Mon Apr 12 2021 Gerrit Photon <photon-checkins@vmware.com> - 27.2-1
- Automatic Version Bump

* Fri Oct 16 2020 Shreenidhi Shedi <sshedi@vmware.com> - 27.1-2
- Fix aarch64 build error

* Tue Oct 06 2020 Susant Sahani <ssahani@vmware.com>  - 27.1-1
- Initial rpm release.
