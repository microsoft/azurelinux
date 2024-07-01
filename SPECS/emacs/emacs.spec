Summary:        GNU Emacs text editor
Name:           emacs
Version:        29.4
Release:        1%{?dist}
License:        GPLv3+ AND CC0-1.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Applications/Editors
URL:            https://www.gnu.org/software/emacs/
Source0:        https://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz
Source1:        site-start.el
Source2:        default.el
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  gnutls-devel
BuildRequires:  ncurses-devel
BuildRequires:  systemd-devel
Requires:       %{name}-filesystem = %{version}-%{release}

%define site_lisp %{_datadir}/emacs/site-lisp
%define site_start_d %{site_lisp}/site-start.d

%description
Emacs is a powerful, customizable, self-documenting, modeless text
editor. Emacs contains special code editing features, a scripting
language (elisp), and the capability to read mail, news, and more
without leaving the editor.

%package filesystem
Summary:        Emacs filesystem layout
BuildArch:      noarch

%description filesystem
This package provides some directories which are required by other
packages that add functionality to Emacs.

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

# Create macros.emacs RPM macro file
cat > macros.emacs << EOF
%%_emacs_version %{version}
%%_emacs_ev %{?epoch:%{epoch}:}%{version}
%%_emacs_evr %{?epoch:%{epoch}:}%{version}-%{release}
%%_emacs_sitelispdir %{site_lisp}
%%_emacs_sitestartdir %{site_start_d}
%%_emacs_bytecompile(W) /usr/bin/emacs -batch --no-init-file --no-site-file --eval '(push nil load-path)' %%{-W:--eval '(setq byte-compile-error-on-warn t)' }-f batch-byte-compile %%*
EOF

%install
%make_install

rm -rf %{buildroot}%{_infodir}
rm -rf %{buildroot}%{_mandir}
rm -rf %{buildroot}%{_datadir}/icons

rm %{buildroot}%{_bindir}/ctags
rm %{buildroot}%{_datadir}/applications/*.desktop

mkdir -p %{buildroot}%{_datadir}/emacs/site-lisp/site-start.d

# Install rpm macro definition file
mkdir -p %{buildroot}%{_rpmconfigdir}/macros.d
install -p -m 0644 macros.emacs %{buildroot}%{_rpmconfigdir}/macros.d/

mkdir -p %{buildroot}%{site_lisp}
install -p -m 0644 %SOURCE1 %{buildroot}%{site_lisp}/site-start.el
install -p -m 0644 %SOURCE2 %{buildroot}%{site_lisp}

# This solves bz#474958, "update-directory-autoloads" now finally
# works the path is different each version, so we'll generate it here
echo "(setq source-directory \"%{_datadir}/emacs/%{version}/\")" \
 >> %{buildroot}%{site_lisp}/site-start.el

#
# Create file lists
#
rm -f *-filelist {common,el}-*-files
 
( TOPDIR=${PWD}
  cd %{buildroot}
 
  find .%{_datadir}/emacs/%{version}/lisp .%{site_lisp} \
    \( -type f -name '*.elc' -fprint $TOPDIR/common-lisp-none-elc-files \) -o \( -type d -fprintf $TOPDIR/common-lisp-dir-files "%%%%dir %%p\n" \) -o \( -name '*.el.gz' -fprint $TOPDIR/el-bytecomped-files -o -fprint $TOPDIR/common-not-comped-files \)
 
)

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
%{_datadir}/emacs/%{version}%{_sysconfdir}/*
%{_datadir}/emacs/%{version}/lisp/*
%{_datadir}/emacs/%{version}/site-lisp/subdirs.el
%{_datadir}/emacs/site-lisp/subdirs.el
%{_datadir}/metainfo/emacs.metainfo.xml
%attr(0644,root,root) %config(noreplace) %{site_lisp}/default.el
%attr(0644,root,root) %config %{site_lisp}/site-start.el
%{_rpmconfigdir}/macros.d/macros.emacs

%files filesystem
%dir %{_datadir}/emacs
%dir %{_datadir}/emacs/site-lisp
%dir %{_datadir}/emacs/site-lisp/site-start.d

%changelog
* Mon Jul 01 2024 Sharath Srikanth Chellappa <sharathsr@microsoft.com> - 29.4-1
- Upgrade to 29.4 to fix  CVE-2024-39331.

* Wed May 01 2024 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 29.3-2
- Added macros.emacs RPM macro file to be produced and provided by the package

* Wed Apr 03 2024 Betty Lakes <bettylakes@microsoft.com> - 29.3-1
- Upgrade to 29.3

* Mon Nov 06 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 29.1-1
- Auto-upgrade to 29.1 - Azure Linux 3.0 - package upgrades

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 28.2-6
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Mon Mar 27 2023 Pawel Winogrodzki <pawelwi@microsoft.com> - 28.2-5
- Applied upstream patches to fix CVE-2023-28617.

* Thu Mar 16 2023 Nicolas Guibourge <nicolasg@microsoft.com> - 28.2-4
- Apply upstream patches to fix CVE-2023-27986, CVE-2023-27985

* Thu Mar 09 2023 Nan Liu <liunan@microsoft.com> - 28.2-3
- Apply upstream patches to fix CVE-2022-48338, CVE-2022-48339

* Tue Mar 07 2023 Sindhu Karri <lakarri@microsoft.com> - 28.2-2
- Apply upstream patch for CVE-2022-48337

* Mon Mar 06 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 28.2-1
- Auto-upgrade to 28.2 - fix CVE-2022-48338, CVE-2022-48339

* Wed Dec 07 2022 Henry Beberman <henry.beberman@microsoft.com> - 28.1-5
- Apply upstream patch for CVE-2022-45939

* Wed Sep 07 2022 Mateusz Malisz <mamalisz@microsoft.com> - 28.1-4
- Add filesystem subpackage.

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
