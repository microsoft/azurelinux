%bcond_with gui

Vendor:         Microsoft Corporation
Distribution:   Mariner
%global _hardened_build 1

# This file is encoded in UTF-8.  -*- coding: utf-8 -*-
Summary:       GNU Emacs text editor
Name:          emacs
Version:       27.1
Release:       3%{?dist}
License:       GPLv3+ and CC0-1.0
URL:           http://www.gnu.org/software/emacs/
Source0:       https://ftp.gnu.org/gnu/emacs/emacs-%{version}.tar.xz
Source1:       https://ftp.gnu.org/gnu/emacs/emacs-%{version}.tar.xz.sig
# generate the keyring via:
# wget https://ftp.gnu.org/gnu/gnu-keyring.gpg
# gpg2 --import gnu-keyring.gpg
# gpg2 --armor --export D405AA2C862C54F17EEE6BE0E8BCD7866AFCF978 > gpgkey-D405AA2C862C54F17EEE6BE0E8BCD7866AFCF978.gpg
Source2:       gpgkey-D405AA2C862C54F17EEE6BE0E8BCD7866AFCF978.gpg
Source3:       emacs.desktop
Source4:       dotemacs.el
Source5:       site-start.el
Source6:       default.el
# Emacs Terminal Mode, #551949, #617355
Source7:       emacs-terminal.desktop
Source8:       emacs-terminal.sh
Source9:       emacs.service
Source10:      %{name}.appdata.xml
# rhbz#713600
Patch1:        emacs-spellchecker.patch
Patch2:        emacs-system-crypto-policies.patch

BuildRequires: gcc
BuildRequires: atk-devel
BuildRequires: cairo-devel
BuildRequires: dbus-devel
BuildRequires: giflib-devel
BuildRequires: glibc-devel
BuildRequires: ncurses-devel
BuildRequires: zlib-devel
BuildRequires: gnutls-devel
BuildRequires: m17n-lib-devel
BuildRequires: libotf-devel
BuildRequires: libselinux-devel
BuildRequires: alsa-lib-devel
BuildRequires: gpm-devel
BuildRequires: liblockfile-devel
BuildRequires: libxml2-devel
BuildRequires: autoconf
BuildRequires: bzip2
BuildRequires: cairo
BuildRequires: texinfo
BuildRequires: gzip
BuildRequires: desktop-file-utils
BuildRequires: libacl-devel
BuildRequires: harfbuzz-devel
BuildRequires: jansson-devel
BuildRequires: systemd-devel
BuildRequires: libjpeg-turbo-devel
BuildRequires: libtiff-devel

%if %{with gui}
BuildRequires: freetype-devel
BuildRequires: fontconfig-devel
BuildRequires: libpng-devel
BuildRequires: libX11-devel
BuildRequires: libXau-devel
BuildRequires: libXdmcp-devel
BuildRequires: libXrender-devel
BuildRequires: libXt-devel
BuildRequires: libXpm-devel
BuildRequires: xorg-x11-proto-devel
BuildRequires: librsvg2-devel
BuildRequires: gtk3-devel
BuildRequires: webkit2gtk3-devel
%endif

BuildRequires: gnupg2

# For lucid
BuildRequires: Xaw3d-devel

%ifarch %{ix86}
BuildRequires: util-linux
%endif


# Emacs doesn't run without dejavu-sans-mono-fonts, rhbz#732422
Requires:      desktop-file-utils
Requires:      dejavu-sans-mono-fonts
Requires(preun): %{_sbindir}/alternatives
Requires(posttrans): %{_sbindir}/alternatives
Requires:      emacs-common = %{version}-%{release}
Provides:      emacs(bin) = %{version}-%{release}

%define site_lisp %{_datadir}/emacs/site-lisp
%define site_start_d %{site_lisp}/site-start.d
%define bytecompargs -batch --no-init-file --no-site-file -f batch-byte-compile
%define pkgconfig %{_datadir}/pkgconfig
%define emacs_libexecdir %{_libexecdir}/emacs/%{version}/%{_host}


%description
Emacs is a powerful, customizable, self-documenting, modeless text
editor. Emacs contains special code editing features, a scripting
language (elisp), and the capability to read mail, news, and more
without leaving the editor.

%if %{with gui}
This package provides an emacs binary with support for X windows.

%package lucid
Summary:       GNU Emacs text editor with LUCID toolkit X support
Requires(preun): %{_sbindir}/alternatives
Requires(posttrans): %{_sbindir}/alternatives
Requires:      emacs-common = %{version}-%{release}
Provides:      emacs(bin) = %{version}-%{release}

%description lucid
Emacs is a powerful, customizable, self-documenting, modeless text
editor. Emacs contains special code editing features, a scripting
language (elisp), and the capability to read mail, news, and more
without leaving the editor.

This package provides an emacs binary with support for X windows
using LUCID toolkit.
%endif

%package nox
Summary:       GNU Emacs text editor without X support
Requires(preun): %{_sbindir}/alternatives
Requires(posttrans): %{_sbindir}/alternatives
Requires:      emacs-common = %{version}-%{release}
Provides:      emacs(bin) = %{version}-%{release}

%description nox
Emacs is a powerful, customizable, self-documenting, modeless text
editor. Emacs contains special code editing features, a scripting
language (elisp), and the capability to read mail, news, and more
without leaving the editor.

This package provides an emacs binary with no X windows support for running
on a terminal.

%package common
Summary:       Emacs common files
# The entire source code is GPLv3+ except lib-src/etags.c which is
# also BSD.  Manual (info) is GFDL.
License:       GPLv3+ and GFDL and BSD
Requires(preun): %{_sbindir}/alternatives
Requires(posttrans): %{_sbindir}/alternatives
Requires:      %{name}-filesystem = %{version}-%{release}
Provides:      %{name}-el = %{version}-%{release}

%description common
Emacs is a powerful, customizable, self-documenting, modeless text
editor. Emacs contains special code editing features, a scripting
language (elisp), and the capability to read mail, news, and more
without leaving the editor.

This package contains all the common files needed by emacs, emacs-lucid
or emacs-nox.

%package terminal
Summary:       A desktop menu item for GNU Emacs terminal.
Requires:      emacs = %{version}-%{release}
BuildArch:     noarch

%description terminal
Contains a desktop menu item running GNU Emacs terminal. Install
emacs-terminal if you need a terminal with Malayalam support.

Please note that emacs-terminal is a temporary package and it will be
removed when another terminal becomes capable of handling Malayalam.

%package filesystem
Summary:       Emacs filesystem layout
BuildArch:     noarch

%description filesystem
This package provides some directories which are required by other
packages that add functionality to Emacs.

%package devel
Summary: Development header files for Emacs

%description devel
Development header files for Emacs.

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%setup -q

%patch1 -p1 -b .spellchecker
%patch2 -p1 -b .system-crypto-policies
autoconf

# We prefer our emacs.desktop file
cp %SOURCE3 etc/emacs.desktop

grep -v "tetris.elc" lisp/Makefile.in > lisp/Makefile.in.new \
   && mv lisp/Makefile.in.new lisp/Makefile.in
grep -v "pong.elc" lisp/Makefile.in > lisp/Makefile.in.new \
   && mv lisp/Makefile.in.new lisp/Makefile.in

# Avoid trademark issues
rm -f lisp/play/tetris.el lisp/play/tetris.elc
rm -f lisp/play/pong.el lisp/play/pong.el

# Sorted list of info files
%define info_files ada-mode auth autotype bovine calc ccmode cl dbus dired-x ebrowse ede ediff edt efaq-w32 efaq eieio eintr elisp emacs-gnutls emacs-mime emacs epa erc ert eshell eudc eww flymake forms gnus htmlfontify idlwave ido info mairix-el message mh-e newsticker nxml-mode octave-mode org pcl-cvs pgg rcirc reftex remember sasl sc semantic ses sieve smtpmail speedbar srecode todo-mode tramp url vhdl-mode vip viper widget wisent woman

# Since the list of info files has to be maintained, check if all info files
# from the upstream tarball are actually present in %%info_files.
cd info
fs=( $(ls *.info) )
is=( %info_files  )
files=$(echo ${fs[*]} | sed 's/\.info//'g | sort | tr -d '\n')
for i in $(seq 0 $(( ${#fs[*]} - 1 ))); do
  if test "${fs[$i]}" != "${is[$i]}.info"; then
    echo Please update %%info_files: ${fs[$i]} != ${is[$i]}.info >&2
    break
  fi
done
cd ..

%ifarch %{ix86}
%define setarch setarch %{_arch} -R
%else
%define setarch %{nil}
%endif

# Avoid duplicating doc files in the common subpackage
ln -s ../../%{name}/%{version}/etc/COPYING doc
ln -s ../../%{name}/%{version}/etc/NEWS doc


%build
export CFLAGS="-DMAIL_USE_LOCKF %{build_cflags}"
%set_build_flags

%if %{with gui}
# Build GTK+ binary
mkdir build-gtk && cd build-gtk
ln -s ../configure .

LDFLAGS=-Wl,-z,relro;  export LDFLAGS;

%configure --with-dbus --with-gif --with-jpeg --with-png --with-rsvg \
           --with-tiff --with-xft --with-xpm --with-x-toolkit=gtk3 --with-gpm=no \
           --with-xwidgets --with-modules --with-harfbuzz --with-cairo --with-json
make bootstrap
%{setarch} %make_build
cd ..

# Build Lucid binary
mkdir build-lucid && cd build-lucid
ln -s ../configure .

LDFLAGS=-Wl,-z,relro;  export LDFLAGS;

%configure --with-dbus --with-gif --with-jpeg --with-png --with-rsvg \
           --with-tiff --with-xft --with-xpm --with-x-toolkit=lucid --with-gpm=no \
           --with-modules --with-harfbuzz --with-cairo --with-json
make bootstrap
%{setarch} %make_build
cd ..
%endif

# Build binary without X support
mkdir build-nox && cd build-nox
ln -s ../configure .
%configure --with-x=no --with-modules --with-json --with-jpeg=ifavailable --with-tiff=ifavailable
%{setarch} %make_build
cd ..

# Remove versioned file so that we end up with .1 suffix and only one DOC file
%if %{with gui}
rm build-{gtk,lucid}/src/emacs-%{version}.*
%endif
rm build-nox/src/emacs-%{version}.*

# Create pkgconfig file
cat > emacs.pc << EOF
sitepkglispdir=%{site_lisp}
sitestartdir=%{site_start_d}

Name: emacs
Description: GNU Emacs text editor
Version: %{version}
EOF

# Create macros.emacs RPM macro file
cat > macros.emacs << EOF
%%_emacs_version %{version}
%%_emacs_ev %{version}
%%_emacs_evr {version}-%{release}
%%_emacs_sitelispdir %{site_lisp}
%%_emacs_sitestartdir %{site_start_d}
%%_emacs_bytecompile /usr/bin/emacs -batch --no-init-file --no-site-file --eval '(progn (setq load-path (cons "." load-path)))' -f batch-byte-compile
EOF

%install
%if %{with gui}
cd build-gtk
%make_install
cd ..
%endif

cd build-nox
%make_install
cd ..

# Let alternatives manage the symlink
rm %{buildroot}%{_bindir}/emacs
touch %{buildroot}%{_bindir}/emacs

# Remove emacs.pdmp from common
rm %{buildroot}%{emacs_libexecdir}/emacs.pdmp

# Do not compress the files which implement compression itself (#484830)
gunzip %{buildroot}%{_datadir}/emacs/%{version}/lisp/jka-compr.el.gz
gunzip %{buildroot}%{_datadir}/emacs/%{version}/lisp/jka-cmpr-hook.el.gz

%if %{with gui}
# Install emacs.pdmp of the emacs with GTK+
install -p -m 0644 build-gtk/src/emacs.pdmp %{buildroot}%{_bindir}/emacs-%{version}.pdmp

# Install the emacs with LUCID toolkit
install -p -m 0755 build-lucid/src/emacs %{buildroot}%{_bindir}/emacs-%{version}-lucid
install -p -m 0644 build-lucid/src/emacs.pdmp %{buildroot}%{_bindir}/emacs-%{version}-lucid.pdmp
%endif

# Install the emacs without X
install -p -m 0755 build-nox/src/emacs %{buildroot}%{_bindir}/emacs-%{version}-nox
install -p -m 0644 build-nox/src/emacs.pdmp %{buildroot}%{_bindir}/emacs-%{version}-nox.pdmp

# Make sure movemail isn't setgid
chmod 755 %{buildroot}%{emacs_libexecdir}/movemail

mkdir -p %{buildroot}%{site_lisp}
install -p -m 0644 %SOURCE5 %{buildroot}%{site_lisp}/site-start.el
install -p -m 0644 %SOURCE6 %{buildroot}%{site_lisp}

# This solves bz#474958, "update-directory-autoloads" now finally
# works the path is different each version, so we'll generate it here
echo "(setq source-directory \"%{_datadir}/emacs/%{version}/\")" \
 >> %{buildroot}%{site_lisp}/site-start.el

mv %{buildroot}%{_bindir}/{etags,etags.emacs}
mv %{buildroot}%{_mandir}/man1/{ctags.1.gz,gctags.1.gz}
mv %{buildroot}%{_mandir}/man1/{etags.1.gz,etags.emacs.1.gz}
mv %{buildroot}%{_bindir}/{ctags,gctags}
# BZ 927996
mv %{buildroot}%{_infodir}/{info.info.gz,info.gz}

mkdir -p %{buildroot}%{site_lisp}/site-start.d

# Default initialization file
mkdir -p %{buildroot}%{_sysconfdir}/skel
install -p -m 0644 %SOURCE4 %{buildroot}%{_sysconfdir}/skel/.emacs

# Install pkgconfig file
mkdir -p %{buildroot}/%{pkgconfig}
install -p -m 0644 emacs.pc %{buildroot}/%{pkgconfig}

# Install app data
mkdir -p %{buildroot}/%{_datadir}/appdata
cp -a %SOURCE10 %{buildroot}/%{_datadir}/appdata
# Upstream ships its own appdata file, but it's quite terse.
rm %{buildroot}/%{_datadir}/metainfo/emacs.appdata.xml

# Install rpm macro definition file
mkdir -p %{buildroot}%{_rpmconfigdir}/macros.d
install -p -m 0644 macros.emacs %{buildroot}%{_rpmconfigdir}/macros.d/

# Installing emacs-terminal binary
install -p -m 755 %SOURCE8 %{buildroot}%{_bindir}/emacs-terminal

# After everything is installed, remove info dir
rm -f %{buildroot}%{_infodir}/dir

# Installing service file
mkdir -p %{buildroot}%{_userunitdir}
install -p -m 0644 %SOURCE9 %{buildroot}%{_userunitdir}/emacs.service
# Emacs 26.1 installs the upstream unit file to /usr/lib64 on 64bit archs, we don't want that
rm -f %{buildroot}/usr/lib64/systemd/user/emacs.service

# Install desktop files
mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install --dir=%{buildroot}%{_datadir}/applications \
                     %SOURCE3
desktop-file-install --dir=%{buildroot}%{_datadir}/applications \
                     %SOURCE7

#
# Create file lists
#
rm -f *-filelist {common,el}-*-files

( TOPDIR=${PWD}
  cd %{buildroot}

  find .%{_datadir}/emacs/%{version}/lisp \
    .%{_datadir}/emacs/%{version}/lisp/leim \
    .%{_datadir}/emacs/site-lisp \( -type f -name '*.elc' -fprint $TOPDIR/common-lisp-none-elc-files \) -o \( -type d -fprintf $TOPDIR/common-lisp-dir-files "%%%%dir %%p\n" \) -o \( -name '*.el.gz' -fprint $TOPDIR/el-bytecomped-files -o -fprint $TOPDIR/common-not-comped-files \)

)

# Put the lists together after filtering  ./usr to /usr
sed -i -e "s|\.%{_prefix}|%{_prefix}|" *-files
cat common-*-files > common-filelist
cat el-*-files common-lisp-dir-files > el-filelist

# Remove old icon
rm %{buildroot}%{_datadir}/icons/hicolor/scalable/mimetypes/emacs-document23.svg

%preun
%{_sbindir}/alternatives --remove emacs %{_bindir}/emacs-%{version}

%posttrans
%{_sbindir}/alternatives --install %{_bindir}/emacs emacs %{_bindir}/emacs-%{version} 80

%if %{with gui}
%preun lucid
%{_sbindir}/alternatives --remove emacs %{_bindir}/emacs-%{version}-lucid
%{_sbindir}/alternatives --remove emacs-lucid %{_bindir}/emacs-%{version}-lucid

%posttrans lucid
%{_sbindir}/alternatives --install %{_bindir}/emacs emacs %{_bindir}/emacs-%{version}-lucid 70
%{_sbindir}/alternatives --install %{_bindir}/emacs-lucid emacs-lucid %{_bindir}/emacs-%{version}-lucid 60
%endif

%preun nox
%{_sbindir}/alternatives --remove emacs %{_bindir}/emacs-%{version}-nox
%{_sbindir}/alternatives --remove emacs-nox %{_bindir}/emacs-%{version}-nox

%posttrans nox
%{_sbindir}/alternatives --install %{_bindir}/emacs emacs %{_bindir}/emacs-%{version}-nox 70
%{_sbindir}/alternatives --install %{_bindir}/emacs-nox emacs-nox %{_bindir}/emacs-%{version}-nox 60

%preun common
%{_sbindir}/alternatives --remove emacs.etags %{_bindir}/etags.emacs

%posttrans common
%{_sbindir}/alternatives --install %{_bindir}/etags emacs.etags %{_bindir}/etags.emacs 80 \
       --slave %{_mandir}/man1/etags.1.gz emacs.etags.man %{_mandir}/man1/etags.emacs.1.gz

%files
%{_bindir}/emacs-%{version}
%attr(0755,-,-) %ghost %{_bindir}/emacs
%{_datadir}/applications/emacs.desktop
%{_datadir}/appdata/%{name}.appdata.xml
%{_datadir}/icons/hicolor/*/apps/emacs.png
%{_datadir}/icons/hicolor/scalable/apps/emacs.svg
%{_datadir}/icons/hicolor/scalable/apps/emacs.ico
%{_datadir}/icons/hicolor/scalable/mimetypes/emacs-document.svg

%if %{with gui}
%files lucid
%{_bindir}/emacs-%{version}-lucid
%{_bindir}/emacs-%{version}-lucid.pdmp
%attr(0755,-,-) %ghost %{_bindir}/emacs
%attr(0755,-,-) %ghost %{_bindir}/emacs-lucid
%endif

%files nox
%{_bindir}/emacs-%{version}-nox
%{_bindir}/emacs-%{version}-nox.pdmp
%attr(0755,-,-) %ghost %{_bindir}/emacs
%attr(0755,-,-) %ghost %{_bindir}/emacs-nox

%files common -f common-filelist -f el-filelist
%config(noreplace) %{_sysconfdir}/skel/.emacs
%{_rpmconfigdir}/macros.d/macros.emacs
%license etc/COPYING
%doc doc/NEWS BUGS README
%{_bindir}/ebrowse
%{_bindir}/emacsclient
%{_bindir}/etags.emacs
%{_bindir}/gctags
%{_mandir}/*/*
%{_infodir}/*
%dir %{_datadir}/emacs/%{version}
%{_datadir}/emacs/%{version}/etc
%{_datadir}/emacs/%{version}/site-lisp
%{_libexecdir}/emacs
%{_userunitdir}/emacs.service
%attr(0644,root,root) %config(noreplace) %{_datadir}/emacs/site-lisp/default.el
%attr(0644,root,root) %config %{_datadir}/emacs/site-lisp/site-start.el
%{pkgconfig}/emacs.pc

%files terminal
%{_bindir}/emacs-terminal
%{_datadir}/applications/emacs-terminal.desktop

%files filesystem
%dir %{_datadir}/emacs
%dir %{_datadir}/emacs/site-lisp
%dir %{_datadir}/emacs/site-lisp/site-start.d

%files devel
%{_includedir}/emacs-module.h

%changelog
* Thu Aug 12 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 27.1-3
- Conditionally disabled build of GUI-dependent components.
- Removed epoch since this is new in CBL-Mariner.
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Aug 18 2020 Jan Synáček <jsynacek@redhat.com> - 1:27.1-2
- use make macros (original patch provided by Tom Stellard)
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Tue Aug 11 2020 Bhavin Gandhi <bhavin7392@gmail.com> - 1:27.1-1
- emacs-27.1 is available (#1867841)
- Add systemd-devel to support Type=notify in unit file
- Build with Cairo and Jansson support
- Remove ImageMagick dependency as it's no longer used

* Thu Apr 16 2020 Dan Čermák <dan.cermak@cgc-instruments.com> - 1:26.3-3
- Drop dependency on GConf2

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:26.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Sep 08 2019 Maximiliano Sandoval <msandoval@protonmail.com> - 1:26.3-1
- emacs-26.3 is available (#1747101)

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:26.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Apr 17 2019 Jan Synáček <jsynacek@redhat.com> - 1:26.2-1
- emacs-26.2 is available (#1699434)

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:26.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Aug 28 2018 Michael Cronenworth <mike@cchtml.com> - 1:26.1-7
- Rebuild for new ImageMagick 6.9.10

* Mon Aug 13 2018 Jan Synáček <jsynacek@redhat.com> - 1:26.1-6
- remove python dependencies, emacs*.py have not been there for a while

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:26.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 1:26.1-4
- Rebuilt for Python 3.7

* Tue Jun 26 2018 Jan Synáček <jsynacek@redhat.com> - 1:26.1-3
- Refix: Emacs crashes when loading color fonts (#1519038)
  + emacs SIGABRT after XProtocolError on displaying an email in Gnus (#1591223)

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1:26.1-2
- Rebuilt for Python 3.7

* Wed May 30 2018 Jan Synáček <jsynacek@redhat.com> - 1:26.1-1
- emacs-26.1 is available (#1583433)

* Wed Apr  4 2018 Jan Synáček <jsynacek@redhat.com> - 1:25.3-9
- Emacs crashes when loading color fonts (#1519038)

* Sun Feb 11 2018 Sandro Mani <manisandro@gmail.com> - 1:25.3-8
- Rebuild (giflib)

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1:25.3-7
- Escape macros in %%changelog

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:25.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 12 2018 Tomas Popela <tpopela@redhat.com> - 1:25.3-5
- Adapt to the webkitgtk4 rename

* Thu Jan 11 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1:25.3-4
- Remove obsolete scriptlets

* Thu Sep 14 2017 Pete Walter <pwalter@fedoraproject.org> - 1:25.3-3
- Rebuilt for ImageMagick 6.9.9 soname bump

* Wed Sep 13 2017 Richard W.M. Jones <rjones@redhat.com> - 1:25.3-2
- Rebuild to try to fix: libwebkit2gtk-4.0.so.37: undefined symbol:
  soup_auth_manager_clear_cached_credentials

* Tue Sep 12 2017 Jan Synáček <jsynacek@redhat.com> - 1:25.3-1
- update to 25.3 (#1490649 #1490409)

* Wed Sep 06 2017 Michael Cronenworth <mike@cchtml.com> - 1:25.2-10
- Rebuild for ImageMagick 6

* Fri Aug 25 2017 Michael Cronenworth <mike@cchtml.com> - 1:25.2-9
- Add patch for ImageMagick 7 detection

* Fri Aug 25 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1:25.2-8
- Rebuilt for ImageMagick soname bump

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:25.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Sun Jul 30 2017 Florian Weimer <fweimer@redhat.com> - 1:25.2-6
- Rebuild with binutils fix for ppc64le (#1475636)

* Fri Jul 28 2017 Björn Esser <besser82@fedoraproject.org> - 1:25.2-5
- Rebuilt for new ImageMagick so-name

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:25.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 14 2017 Gregory Shimansky <gshimansky@gmail.com> - 25.2-3
- Added package with LUCID X toolkit support (#1471258)

* Fri Apr 28 2017 Jan Synáček <jsynacek@redhat.com> - 25.2-2
- compile with support for dynamic modules (#1421087)

* Mon Apr 24 2017 Jan Synáček <jsynacek@redhat.com> - 25.2-1
- update to 25.2 (#1444818)

* Mon Feb 27 2017 Jan Synáček <jsynacek@redhat.com> - 25.2-0.1-rc2
- update to 25.2 rc2
- depend on the latest webkit (#1375834)

* Wed Feb 01 2017 Stephen Gallagher <sgallagh@redhat.com> - 25.1-4
- Add missing %%license macro

* Mon Dec 12 2016 Jan Synáček <jsynacek@redhat.com> - 1:25.1-3
- Emacs 25.1 fc25 often crashes with emacs-auctex (#1398718)

* Wed Oct 12 2016 Jan Synáček <jsynacek@redhat.com> - 1:25.1-2
- emacs leaves behind corrupted symlinks on CIFS share (#1271407)

* Mon Sep 19 2016 Jan Synáček <jsynacek@redhat.com> - 1:25.1-1
- update to 25.1 (#1377031)

* Wed Sep 14 2016 Richard Hughes <rhughes@redhat.com> - 1:25.1-0.4.rc2
- Upgrade AppData file to specification 0.6+

* Tue Aug 30 2016 Jan Synáček <jsynacek@redhat.com> - 1:25.1-0.3.rc2
- update to 25.1 rc2

* Mon Jul 25 2016 Jan Synáček <jsynacek@redhat.com> - 1:25.1-0.2.rc1
- do not set frame-title-format in default.el (#1359732)

* Mon Jul 25 2016 Jan Synáček <jsynacek@redhat.com> - 1:25.1-0.1.rc1
- update to 25.1 rc1

* Fri Jul 22 2016 Jan Synáček <jsynacek@redhat.com> - 1:25.0.95-4
- fix: emacs build failure due to high memory consumption on ppc64 (#1356919)

* Mon Jul 18 2016 Jan Synáček <jsynacek@redhat.com> - 1:25.0.95-3
- workaround: emacs build failure due to high memory consumption on ppc64 (#1356919)
  (patch provided by Sinny Kumari)

* Thu Jul 14 2016 Jan Synáček <jsynacek@redhat.com> - 1:25.0.95-2
- fix: info file entries are not installed (#1350128)

* Mon Jun 13 2016 Jan Synáček <jsynacek@redhat.com> - 1:25.0.95-1
- update to 25.0.95

* Wed May 18 2016 Jan Synáček <jsynacek@redhat.com> - 1:25.0.94-1
- update to 25.0.94

* Tue May  3 2016 Jan Synáček <jsynacek@redhat.com> - 1:25.0.93-2
- emacs starts in a very small window (#1332451)

* Mon Apr 25 2016 Jan Synáček <jsynacek@redhat.com> - 1:25.0.93
- update to 25.0.93 and enable webkit support

* Fri Mar  4 2016 Jan Synáček <jsynacek@redhat.com> - 1:25.0.92
- update to 25.0.92

* Mon Feb 15 2016 Jan Synáček <jsynacek@redhat.com> - 1:24.5-10
- fix build failure on ppc64le (#1306793)

* Mon Feb  8 2016 Jan Synáček <jsynacek@redhat.com> - 1:24.5-10
- refix: set default value for smime-CA-directory (#1131558)

* Tue Feb  2 2016 Jan Synáček <jsynacek@redhat.com> - 1:24.5-9
- emacs "deadlocked" after using mercurial with huge amounts of ignored files in the repository (#1232422)
- GDB interface gets confused by non-ASCII (#1283412)

* Tue Jan  5 2016 Jan Synáček <jsynacek@redhat.com> - 1:24.5-9
- set default value for smime-CA-directory (#1131558)
- remove emacsclient.desktop (#1175969)

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:24.5-8
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Fri Sep 18 2015 Richard Hughes <rhughes@redhat.com> - 1:24.5-7
- Remove no longer required AppData file

* Fri Sep 11 2015 Petr Hracek <phracek@redhat.com> - 1:24.5-6
- Support BBDB >= 3 (EUDC) (#1261668)

* Wed Jun 17 2015 Petr Hracek <phracek@redhat.com> - 1:24.5-5
- game and Trademark problem (#1231676)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:24.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 11 2015 Petr Hracek <phracek@kiasportyw-brq-redhat-com> - 1:24.5-3
- Utilize system-wide crypto-policies (#1179285)

* Wed Apr 22 2015 Petr Hracek <phracek@redhat.com> - 1:24.5-2
- Build with ACL support (#1208945)

* Tue Apr 14 2015 Petr Hracek <phracek@redhat.com> - 1:24.5-1
- New upstream version 24.5 (#1210919)

* Tue Apr  7 2015 Petr Hracek <phracek@redhat.com> - 1:24.4-6
- emacs grep warns 'GREP_OPTIONS is deprecated' (#1176547)

* Thu Mar 26 2015 Richard Hughes <rhughes@redhat.com> - 1:24.4-5
- Add an AppData file for the software center

* Tue Mar 17 2015 Petr Hracek <phracek@redhat.com> - 1:24.4-4
- emacs option --no-bitmap-icon does not work (#1199160)

* Tue Nov 18 2014 Petr Hracek <phracek@redhat.com> - 1:24.4-3
- Resolves #1124892 Add appdata file

* Wed Oct 29 2014 Petr Hracek <phracek@redhat.com> - 1:24.4-2
- Bump version. Correct obsolete version

* Mon Oct 27 2014 Petr Hracek <phracek@redhat.com> - 1:24.4-1
- resolves: #1155101
  Update to the newest upstream version (24.4)

* Thu Oct 23 2014 Petr Hracek <phracek@redhat.com> - 1:24.3-29
- resolves: #1151652
  emacs-el files are part of emacs-common

* Thu Oct 23 2014 Petr Hracek <phracek@redhat.com> - 1:24.3-28
- resolves: #1151652
  emacs-el is required by emacs-common

* Tue Sep 30 2014 jchaloup <jchaloup@redhat.com> - 1:24.3-27
- resolves: #1147912
  Service dont start. Must be replace: "Type=Forking" > "Type=forking".

* Mon Aug 18 2014 jchaloup <jchaloup@redhat.com> - 1:24.3-26
- resolves: #1130587
  unremove emacs from emacs-nox package, emacs and emacs-nox co-exist

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:24.3-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Aug 13 2014 Petr Hracek <phracek@redhat.com> - 1:24.3-24
- emacs.service file for systemd (#1128723)

* Tue Aug 05 2014 jchaloup <jchaloup@redhat.com> - 1:24.3-23
- resolves: #1104012
  initialize kbd_macro_ptr and kbd_macro_end to kdb_macro_buffer

* Mon Aug 04 2014 Petr Hracek <phracek@redhat.com> - 1:24.3-22
- remove /usr/bin/emacs-nox from install section

* Mon Aug 04 2014 Petr Hracek <phracek@redhat.com> - 1:24.3-21
- /usr/bin/emacs-nox link marked as %%ghost file (#1123573)

* Fri Aug 01 2014 Petr Hracek <phracek@redhat.com> - 1:24.3-20
- Provide /usr/bin/emacs-nox (#1123573)

* Mon Jul 28 2014 Petr Hracek <phracek@redhat.com> - 1:24.3-19
- Add patch to remove timstamp from .elc files (#1122157)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:24.3-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 20 2014 Petr Hracek <phracek@redhat.com> - 1:24.3-17
- CVE-2014-3421 CVE-2014-3422 CVE-2014-3423 CVE-2014-3424 (#1095587)

* Thu Apr 17 2014 Petr Hracek <phracek@redhat.com> - 1:24.3-16
- Info files are not installed (#1062792)

* Fri Apr 11 2014 Richard W.M. Jones <rjones@redhat.com> - 1:24.3-16
- Rebuild because of unannounced ImageMagick soname bump in Rawhide.

* Tue Apr 01 2014 Richard W.M. Jones <rjones@redhat.com> - 1:24.3-15
- Rebuild because of unannounced ImageMagick soname bump in Rawhide.

* Mon Feb 03 2014 Petr Hracek <phracek@redhat.com> - 1:24.3-14
- replace sysconfdir/rpm with rpmconfigdir/macros.d

* Wed Aug 14 2013 Jaromir Koncicky <jkoncick@redhat.com> - 1:24.3-13
- Fix default PDF viewer (#971162)

* Fri Aug 09 2013 Petr Hracek <phracek@redhat.com> - 1:24.3-12
- emacs -mm (maximized) does not work (#985729)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:24.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 1:24.3-10
- Perl 5.18 rebuild

* Tue Apr 09 2013 Petr Hracek <phracek@redhat.com> - 1:24.3-9
- Help and man page corrections (#948838)

* Tue Apr 09 2013 Petr Hracek <phracek@redhat.com> - 1:24.3-8
- Rebuild with new file package

* Mon Apr 08 2013 Petr Hracek <phracek@redhat.com> - 1:24.3-7
- Spell checking broken by non-default dictionary (#827033)

* Thu Apr 04 2013 Petr Hracek <phracek@redhat.com> - 1:24.3-6
- Rebuild with new ImageMagick

* Thu Apr 04 2013 Petr Hracek <phracek@redhat.com> - 1:24.3-5
- Fix for Gtk-Warning (#929353)

* Wed Apr 03 2013 Petr Hracek <phracek@redhat.com> - 1:24.3-4
- Fix for info page. info.info.gz page was renamed to info.gz (#927996)

* Thu Mar 28 2013 Petr Hracek <phracek@redhat.com> - 1:24.3-3
- Fix for emacs bug 112144, style_changed_cb (#922519)
- Fix for emacs bug 112131, bell does not work (#562719)

* Mon Mar 18 2013 Petr Hracek <phracek@redhat.com> - 1:24.3-2
- fix #927996 correcting bug. Info pages were not delivered

* Mon Mar 18 2013 Petr Hracek <phracek@redhat.com> - 1:24.3-1
- Updated to the newest upstream release
- solved problem with distribution flag in case of rhel
- rcs-checking not availble anymore
- emacs22.png are not installed anymore

* Mon Mar 18 2013 Rex Dieter <rdieter@fedoraproject.org> 1:24.2-12
- rebuild (ImageMagick)

* Fri Mar 08 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 1:24.2-11
- Remove %%config from %%{_sysconfdir}/rpm/macros.*
  (https://fedorahosted.org/fpc/ticket/259).
- Fix broken spec-file changelog entry.

* Wed Mar  6 2013 Tomáš Mráz <tmraz@redhat.com> - 1:24.2-10
- Rebuild with new gnutls

* Mon Jan 21 2013 Jochen Schmitt <Jochen herr-schmitt de> - 1:24.2-9
- Fix for emacs bug #13460, ispell-change dictionary hunspell issue (#903151)

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 1:24.2-8
- rebuild due to "jpeg8-ABI" feature drop

* Tue Nov 06 2012 Sergio Durigan Junior <sergiodj@riseup.net> - 1:24.2-7
- Fix for Emacs bug #11580, 'Fix querying BBDB for entries without a last
  name'.

* Mon Oct 22 2012 Karel Klíč <kklic@redhat.com> - 1:24.2-6
- Change xorg-x11-fonts-misc dependency to dejavu-sans-mono-fonts, rhbz#732422

* Thu Sep 20 2012 Karel Klíč <kklic@redhat.com> - 1:24.2-5
- Add BSD to emacs-common licenses because of etags.

* Fri Sep 14 2012 Karel Klíč <kklic@redhat.com> - 1:24.2-4
- Moved RPM spec mode to a separate package (rhbz#857865)

* Fri Sep 14 2012 Karel Klíč <kklic@redhat.com> - 1:24.2-3
- Removed patch glibc-open-macro, which seems to be no longer necessary

* Thu Sep 13 2012 Karel Klíč <kklic@redhat.com> - 1:24.2-2
- Removed focus-init.el which used to set focus-follows-mouse to nil.
  It is set to nil by default in Emacs 24.2.

* Thu Sep 13 2012 Karel Klíč <kklic@redhat.com> - 1:24.2-1
- Updated to the newest upstream release
- Switched from bz2 upstream package to xz
- Make the spec file usable on EL6
- Removed the nogets and CVE-2012-3479 patches, because the upstream
  package fixes the associated issues
- Added GFDL license to emacs-common package

* Mon Aug 13 2012 Karel Klíč <kklic@redhat.com> - 1:24.1-6
- Fix CVE-2012-3479: Evaluation of 'eval' forms in file-local variable
  sections, when 'enable-local-variables' set to ':safe'

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:24.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jul 13 2012 Karel Klíč <kklic@redhat.com> - 1:24.1-4
- Remove php-mode from the main package. It should be packaged separately. rhbz#751749

* Wed Jul 11 2012 Karel Klíč <kklic@redhat.com> - 1:24.1-3
- Fix org-mode to work without emacs-el installed. rhbz#830162
- Fix building without gets function, which is removed from recent version of glibc.

* Wed Jul 11 2012 Ville Skyttä <ville.skytta@iki.fi> - 1:24.1-2
- Build -el, -terminal, and -filesystem as noarch (rhbz#834907).

* Mon Jun 18 2012 Karel Klíč <kklic@redhat.com> - 1:24.1-1
- New upstream release
- Switch from GTK 2 to GTK 3

* Fri Jun  8 2012 Karel Klíč <kklic@redhat.com> - 1:24.1-0.rc1
- New upstream prerelease
- Cleanup of the %%changelog section

* Mon May 21 2012 Karel Klíč <kklic@redhat.com> - 1:24.0.97-1
- Newest prerelease

* Fri Apr  6 2012 Karel Klíč <kklic@redhat.com> - 1:24.0.95-1
- New upstream prerelease

* Mon Mar 19 2012 Karel Klíč <kklic@redhat.com> - 1:24.0.94-3
- Another rebuild for ImageMagick update

* Fri Mar  2 2012 Karel Klíč <kklic@redhat.com> - 1:24.0.94-2
- Rebuild for ImageMagick update

* Mon Feb 27 2012 Karel Klíč <kklic@redhat.com> - 1:24.0.94-1
- Update to the newest prerelease
- Remove unpatched files in the lisp directory, where all files are
  installed

* Tue Feb 21 2012 Dan Horák <dan[at]danny.cz> - 1:24.0.93-4
- add upstream fix for emacs bug 10780, revert the workaround

* Mon Feb 13 2012 Dan Horák <dan[at]danny.cz> - 1:24.0.93-3
- workaround build failure on ppc and s390
  (http://debbugs.gnu.org/cgi/bugreport.cgi?bug=10780)

* Wed Feb  8 2012 Kay Sievers <kay@redhat.com> - 1:24.0.93-2
- Drop dependency on 'dev' package; it is gone since many years

* Mon Feb  6 2012 Karel Klíč <kklic@redhat.com> - 1:24.0.93-1
- Update to newer pre-release version

* Thu Jan 19 2012 Karel Klíč <kklic@redhat.com> - 1:24.0.92-1
- Upstream pre-release

* Thu Jan 12 2012 Karel Klíč <kklic@redhat.com> - 1:23.3-19
- Added patch to handle CVE-2012-0035: CEDET global-ede-mode file loading vulnerability (rhbz#773024)

* Sun Nov 27 2011 Ville Skyttä <ville.skytta@iki.fi> - 1:23.3-18
- Apply upstream Subversion >= 1.7 dir structure fix for vc-svn.el.

* Fri Nov 25 2011 Karel Klíč <kklic@redhat.com> - 1:23.3-17
- Add a new command rpm-goto-add-change-log-entry (C-c C-w) to
  rpm-spec mode (Jaroslav Skarvada)

* Fri Nov 25 2011 Karel Klíč <kklic@redhat.com> - 1:23.3-16
- Initialize xgselect in function xg_select when
  gfds_size == 0 (rhbz#751154)

* Wed Nov 23 2011 Karel Klíč <kklic@redhat.com> - 1:23.3-15
- Check for _NET_WM_STATE_HIDDEN (rhbz#711739)

* Tue Nov 22 2011 Karel Klíč <kklic@redhat.com> - 1:23.3-14
- Build Gtk+ version without gpm

* Wed Nov 16 2011 Karel Klíč <kklic@redhat.com> - 1:23.3-13
- Check the presence of hunspell before checking for aspell (rhbz#713600)

* Mon Nov 14 2011 Karel Klíč <kklic@redhat.com> - 1:23.3-12
- Rebuild (rhbz#751154, rhbz#752936)

* Sat Oct 22 2011 Ville Skyttä <ville.skytta@iki.fi> - 1:23.3-11
- Build with gpm and liblockfile support.
- Drop ssl.el (superseded by tls.el).
- Update php-mode to 1.5.0.

* Tue Sep 27 2011 Karel Klíč <kklic@redhat.com> - 1:23.3-10
- Keep COPYING and NEWS in the etc subdir, and symlinks in the docs (rhbz#714212)
  Author: fedora.dm0@gmail.com

* Tue Sep 27 2011 Karel Klíč <kklic@redhat.com> - 1:23.3-9
- Added dependency on xorg-x11-fonts-misc (rhbz#732422)

* Mon Aug  8 2011 Karel Klíč <kklic@redhat.com> - 1:23.3-8
- Updated release archive to 23.3a, which includes grammar files that are
  necessary to modify Semantic parsers

* Thu Jun 30 2011 Ville Skyttä <ville.skytta@iki.fi> - 1:23.3-7
- Use custom-set-variables for customizable variables in .emacs (#716440).
- Move frame-title-format default from .emacs to default.el (#716443).

* Thu May 26 2011 Karel Klíč <kklic@redhat.com> - 1:23.3-6
- Enumerate binaries in emacs-common to avoid packaging single binary
  multiple times by accident

* Mon May 23 2011 Karel Klíč <kklic@redhat.com> - 1:23.3-5
- Removed %%defattr from %%files sections, as RPM no longer needs it
- Removed %%dir %%{_libexecdir}/emacs and similar from emacs and
  emacs-nox packages, as the directories are used and present only in
  emacs-common (rhbz#704067)

* Tue Mar 22 2011 Karel Klic <kklic@redhat.com> - 1:23.3-4
- Rebuild to fix an RPM issue (rhbz689182)

* Tue Mar 15 2011 Ville Skyttä <ville.skytta@iki.fi> - 1:23.3-3
- Use UTC timestamps in rpm-spec-mode changelog entries by default (rhbz#672350)
- Consider *.elc in addition to *.el when loading files from site-start.d (rhbz#672324)

* Tue Mar 15 2011 Karel Klic <kklic@redhat.com> - 1:23.3-2
- Another attempt to fix the handling of alternatives (rhbz#684447)
  The current process loses alternatives preference on every upgrade,
  but there seems to be no elegant way how to prevent this while
  having versioned binaries (/bin/emacs-%%{version}) at the same time.
- Removed 'rm -rf %%{buildroot}' from %%install section

* Thu Mar 10 2011 Karel Klic <kklic@redhat.com> - 1:23.3-1
- New upstream release
- Depend on util-linux directly, as the package no longer provides setarch

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:23.2-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 10 2011 Karel Klic <kklic@redhat.com> - 1:23.2-17
- Added filesystem subpackage (rhbz#661866)
- Added emacsclient desktop file (rhbz#665362)

* Fri Jan  7 2011 Karel Klic <kklic@redhat.com> - 1:23.2-16
- Removed dependency on both hunspell and aspell. Emacs does not
  _require_ spell checker, e.g. if user wants to uninstall one, there
  is no reason why Emacs should also be uninstalled. Emacs can run one
  like it can run GDB, pychecker, (La)TeX, make, gcc, and all VCSs out
  there.
- Removed conflict with old gettext package
- Cleaned spec file header
- Removed gcc-4.5.0 specific CFLAGS

* Fri Jan  7 2011 Karel Klic <kklic@redhat.com> - 1:23.2-15
- The emacs-terminal package now requires emacs package

* Thu Jan  6 2011 Karel Klic <kklic@redhat.com> - 1:23.2-14
- Patch emacs-terminal to use /usr/bin/emacs (rhbz#635213)

* Mon Sep  6 2010 Karel Klic <kklic@redhat.com> - 1:23.2-13
- Removed transient-mark-mode suggestion from dotemacs.el, as this
  minor mode is enabled by default in recent versions of Emacs

* Thu Aug 19 2010 Karel Klic <kklic@redhat.com> - 1:23.2-12
- Mention xdg-open in browse-url-default-browser docstring (rhbz#624359)
  Updates emacs-23.1-xdg.patch

* Tue Aug 17 2010 Karel Klic <kklic@redhat.com> - 1:23.2-11
- Own /usr/bin/emacs (rhbz#614935)
- Updated the handling of alternatives to match
  https://fedoraproject.org/wiki/Packaging:Alternatives

* Mon Aug 16 2010 Karel Klic <kklic@redhat.com> - 1:23.2-10
- Removed the png extension from the Icon entry in emacs.desktop (rhbz#507231)

* Wed Aug  4 2010 Karel Klic <kklic@redhat.com> - 1:23.2-9
- Added Fedora conditionals

* Mon Aug  2 2010 Karel Klic <kklic@redhat.com> - 1:23.2-8
- Moved the terminal desktop menu item to a separate package (rhbz#617355)

* Thu Jul  8 2010 Karel Klic <kklic@redhat.com> - 1:23.2-7
- Added workaround for an GCC 4.5.0 bug

* Thu Jul  8 2010 Karel Klic <kklic@redhat.com> - 1:23.2-6
- Removed Obsoletes: emacs-nxml-mode, it was obsoleted in F-11
- Added COPYING to emacs-el, moved COPYING in emacs-common to %%doc

* Thu Jun  3 2010 Karel Klic <kklic@redhat.com> - 1:23.2-5
- Fixed handling of dual spacing fonts rhbz#599437

* Thu May 27 2010 Karel Klíč <kklic@redhat.com> - 1:23.2-4
- Add patch to fix rhbz#595546 hideshow library matches wrong parenthesis
  under certain circumstances
- Removed %%clean section

* Wed May 19 2010 Naveen Kumar <nkumar@redhat.com> - 1:23.2-3
- Added a desktop file for adding terminal mode to menu (RHBZ #551949)

* Tue May 11 2010 Karel Klic <kklic@redhat.com> - 1:23.2-2
- Added a patch fixing m17n and libotf version checking (m17ncheck)

* Mon May 10 2010 Karel Klic <kklic@redhat.com> - 1:23.2-1
- Updated the prerelase to final version

* Sun Apr 25 2010 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 1:23.1.96-3
- Add BuildRequires for GConf2-devel to build in Gconf2 support (RHBZ #585447)

* Sun Apr 25 2010 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 1:23.1.96-2
- Remove po-mode files since they are now packaged separately as a sub-package
  of gettext (RHBZ #579452)

* Tue Apr 20 2010 Karel Klic <kklic@redhat.com> - 1:23.1.96-1
- Updated to the newest prerelease
- Remove -movemail patch as it has been merged by upstream

* Thu Apr  1 2010 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 1:23.1.94-6
- Add patch to fix RHBZ #578272 - security vulnerability with movemail
  (CVE-2010-0825)

* Tue Mar 30 2010 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 1:23.1.94-5
- Fix typo in spec file changelog
- Use standard %%patch macro to apply all patches to silent rpmlint warnings

* Tue Mar 30 2010 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 1:23.1.94-4
- Remove unnecessary buildroot tag
- Remove explicit dependency on librsvg2 (but keep BuildRequires for
  librsvg2-devel)
- Add properly versioned Provides for emacs(bin)
- Remove long unneeded Obsoletes for emacs-leim
- Fix summary for emacs-el

* Tue Mar 30 2010 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 1:23.1.94-3
- Use out of tree builds so that we can build multibple versions in the
  %%build section

* Tue Mar 23 2010 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 1:23.1.94-2
- Remove checks for old version of Emacs in postrtrans

* Mon Mar 22 2010 Karel Klic <kklic@redhat.com> - 1:23.1.94-1
- Update to 23.2 pretest version
- Removed patches applied by upstream

* Fri Mar 19 2010 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 1:23.1-26
- Fix broken byte compilation of emacs2.py and emacs3.py with the relevant
  python binaries - requires turning off brp-python-bytecompile script

* Mon Mar 15 2010 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 1:23.1-25
- Add --eval '(progn (setq load-path (cons "." load-path)))' to byte
  compilation macro for packaging add-ons

* Tue Feb  9 2010 Karel Klic <kklic@redhat.com> 1:23.1-24
- Added a comment about alternatives(8) in %%posttrans to the spec file

* Thu Jan 14 2010 Jonathan G. Underwood <jonathan.underwood@gmail.com> 1:23.1-23
- Add patch to fix rhbz#547566 (from Juanma Barranquero)

* Tue Jan 12 2010 Karel Klic <kklic@redhat.com> 1:23.1-22
- Removed invalid URL for rpm-spec-mode.el. This mode is no longer
  found on Internet in this version.

* Thu Jan  7 2010 Karel Klic <kklic@redhat.com> 1:23.1-21
- Removed PreReq from spec file

* Thu Jan  7 2010 Karel Klic <kklic@redhat.com> 1:23.1-20
- Simpler fix for rhbz#517272

* Thu Jan  7 2010 Jens Petersen <petersen@redhat.com> - 1:23.1-19
- m17n-lib-flt requires m17n-db-flt so no longer need to require explicitly
  m17n-db-datafiles for complex text rendering (#542657)

* Mon Jan  4 2010 Karel Klic <kklic@redhat.com> 1:23.1-18
- Fixed rhbz#517272 - emacs-23.1 update shows fonts in double the normal size

* Tue Dec  8 2009 Karel Klic <kklic@redhat.com> 1:23.1-17
- Fixed rhbz#545398 - ETags messes up filenames

* Thu Dec 03 2009 Daniel Novotny <dnovotny@redhat.com> 1:23.1-16
- fix #542657 -  emacs does not display indic text

* Wed Dec 02 2009 Daniel Novotny <dnovotny@redhat.com> 1:23.1-15
- fix #543046 -  Using scroll bar in emacs highlights/selects text

* Mon Nov 30 2009 Daniel Novotny <dnovotny@redhat.com> 1:23.1-14
- fixed FTBFS in F12 and higher (#540921)

* Mon Oct 19 2009 Daniel Novotny <dnovotny@redhat.com> 1:23.1-13
- fixed update-directory-autoloads (#474958)

* Wed Oct 14 2009 Daniel Novotny <dnovotny@redhat.com> 1:23.1-12
- do not compress the files which implement compression itself (#484830)

* Wed Oct 14 2009 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 1:23.1-11
- Update macros.xemacs to treat epoch correctly and be consistent with xemacs package
- Use site_start_d macro consistently

* Tue Sep 29 2009 Daniel Novotny <dnovotny@redhat.com> 1:23.1-10
- emacs contains nxml-mode (#516391)

* Thu Sep 24 2009 Daniel Novotny <dnovotny@redhat.com> 1:23.1-9
- use xdg-open(1) for opening URLs (#316131)

* Wed Sep 23 2009 Daniel Novotny <dnovotny@redhat.com> 1:23.1-8
- updated rpm-spec-mode.el to latest upstream version (#524851)

* Tue Sep 22 2009 Daniel Novotny <dnovotny@redhat.com> 1:23.1-7
- updated %%info_files (#510750)

* Mon Aug 31 2009 Daniel Novotny <dnovotny@redhat.com> 1:23.1-6
- fixed buffer menu (#515722)

* Wed Aug 26 2009 Daniel Novotny <dnovotny@redhat.com> 1:23.1-5
- correct BuildRequires for libotf (#519151)

* Tue Aug 25 2009 Daniel Novotny <dnovotny@redhat.com> 1:23.1-4
- alsa-lib-devel added to BuildRequires (#518659)

* Thu Aug 13 2009 Daniel Novotny <dnovotny@redhat.com> 1:23.1-3
- fixed Name and GenericName in desktop file (#514599)

* Mon Aug 10 2009 Ville Skyttä <ville.skytta@iki.fi> - 1:23.1-2
- Use bzipped upstream tarball.

* Fri Jul 31 2009 Daniel Novotny <dnovotny@redhat.com> 1:23.1-1
- new upstream version 23.1

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:23.0.93-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 26 2009 Daniel Novotny <dnovotny@redhat.com> 1:23.0.93-6
- removed dependency to bitmap fonts: emacs version 23 does not need them

* Thu Jun 25 2009 Daniel Novotny <dnovotny@redhat.com> 1:23.0.93-5
- revoked default.el change (#508033)
- added build dependency: librsvg2-devel (#507852)
- added dependency: aspell (#443549)

* Wed Jun 24 2009 Daniel Novotny <dnovotny@redhat.com> 1:23.0.93-4
- added xorg-x11-fonts-misc to dependencies (#469220)

* Fri Jun 19 2009 Jens Petersen <petersen@redhat.com> - 1:23.0.93-3
- drop igrep since lgrep and rgrep are maintained in emacs now
- specify the list of *-init.el files to be install explicitly

* Thu Jun 11 2009 Daniel Novotny <dnovotny@redhat.com> 1:23.0.93-2
- fix bz#505083 - rpm-add-change-log-entry date format rejected by rpmbuild

* Mon May 18 2009 Daniel Novotny <dnovotny@redhat.com> 1:23.0.93-1
- new upstream version

* Fri Apr 10 2009 Daniel Novotny <dnovotny@redhat.com> 1:22.3-11
- fix bz#443549 -  spell-buffer, flyspell-mode do not work

* Fri Mar 27 2009 Daniel Novotny <dnovotny@redhat.com> 1:22.3-10
- fix segfaults when emacsclient connects to a tcp emacs server (#489066)

* Thu Mar 12 2009 Daniel Novotny <dnovotny@redhat.com> 1:22.3-9
- implement UTC change log option in rpm-spec-mode.el (#489829)

* Wed Mar  4 2009 Michel Salim <salimma@fedoraproject.org> - 1:22.3-8
- Use desktop-file-utils to handle desktop file
- Update icon cache if GTK2 is installed

* Wed Feb 25 2009 Daniel Novotny <dnovotny@redhat.com> 1:22.3-7
- site-lisp/default.el is now config(noreplace)

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:22.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 16 2009 Daniel Novotny <dnovotny@redhat.com> 1:22.3-5
- fix #474578 - /usr/bin/emacs link not updated on upgrade
  (added a script to scan the alternatives and update them)

* Mon Feb 09 2009 Daniel Novotny <dnovotny@redhat.com> 1:22.3-4
- fix bz#484309 (alternatives error message)

* Sun Jan 18 2009 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 1:22.3-3
- Add /etc/rpm/macros.emacs file

* Mon Dec 01 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1:22.3-2
- Rebuild for Python 2.6

* Sat Nov  8 2008 Jens Petersen <petersen@redhat.com> - 1:22.3-1
- update to 22.3 (#461448)
- emacs-22.1.50-sparc64.patch and emacs-22.1.50-regex.patch no longer needed
- update rpm-spec-mode.el to look for fields at bol (#466407)

* Thu May 01 2008 Tom "spot" Callaway <tcallawa@redhat.com>
- fix requires to include epoch

* Thu May 01 2008 Dennis Gilmore <dennis@ausil.us> 1:22.2-4
- add patch from bz#435767

* Thu May 01 2008 Dennis Gilmore <dennis@ausil.us> 1:22.2-3
- add epoch
- put epoch in .pc file

* Thu Apr 24 2008 Dennis Gilmore <dennis@ausil.us> 22.2-2
- add patch fixing libdir on sparc64

* Tue Apr 22 2008 Chip Coldwell <coldwell@redhat.com> 22.2-1
- revert back to emacs-22.2 (bz443639)
- update to php-mode-1.4.0
- update to rpm-spec-mode.el v0.12.1x (bz432209)
- patch rpm-spec-mode to use compilation mode (bz227418)
- fix the Release tag (bz440624)
- drop superfluous configure options
- move the new icons into the right destination directory
- the heuristics for detecting address space randomization in the emacs dumper
  seem insufficient, so bring back setarch -R

* Fri Apr 18 2008 Chip Coldwell <coldwell@redhat.com> 23.0.60-2
- New upstream tarball (fixes bz435767)
- configure tweaks
- drop files.el patch (now upstream)
- drop parallel build patch (now upstream)

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 22.1.50-4
- Autorebuild for GCC 4.3

* Wed Jan  2 2008 Chip Coldwell <coldwell@redhat.com> 22.1.50-3.1
- parallel build patch from Dan Nicolaescu <dann@ics.uci.edu>

* Fri Dec  7 2007 Chip Coldwell <coldwell@redhat.com> 22.1.50-3
- scriptlets shouldn't fail needlessly.
- new upstream tarball

* Thu Dec  6 2007 Chip Coldwell <coldwell@redhat.com> 22.1.50-2
- drop -DSYSTEM_PURESIZE_EXTRA=16777216 (bz409581)

* Mon Nov 19 2007 Chip Coldwell <coldwell@redhat.com> 22.1.50-1
- pulled sources from GNU CVS

* Mon Nov 19 2007 Chip Coldwell <coldwell@redhat.com> 22.1-9
- fixup alternatives mess (bz239745, bz246540)

* Tue Nov  6 2007 Chip Coldwell <coldwell@redhat.com> 22.1-8
- fix insufficient safe-mode checks (Resolves: bz367601)

* Thu Nov  1 2007 Chip Coldwell <coldwell@redhat.com> 22.1-7
- Update rpm-spec-mode to the current upstream, drop compat patch (bz306841)

* Wed Oct 24 2007 Jeremy Katz <katzj@redhat.com> - 22.1-6
- Update rpm-spec-mode to the current upstream (#306841)

* Wed Sep 12 2007 Chip Coldwell <coldwell@redhat.com> - 22.1-5
- require xorg-x11-fonts-ISO8859-1-100dpi instead of 75dpi (Resolves: bz281861)
- drop broken python mode (Resolves: bz262801)

* Mon Sep 10 2007 Chip Coldwell <coldwell@redhat.com> - 22.1-4
- fix pkgconfig path (from pkg-config to pkgconfig (Jonathan Underwood)
- use macro instead of variable style for buildroot.

* Tue Aug 28 2007 Chip Coldwell <coldwell@redhat.com> - 22.1-3
- change group from Development to Utility

* Mon Aug 13 2007 Chip Coldwell <coldwell@redhat.com> - 22.1-2
- add pkgconfig file for emacs-common and virtual provides (Resolves: bz242176)
- glibc-open-macro.patch to deal with glibc turning "open" into a macro.
- leave emacs info pages in default section (Resolves: bz199008)

* Wed Jun  6 2007 Chip Coldwell <coldwell@redhat.com> - 22.1-1
- move alternatives install to posttrans scriptlet (Resolves: bz239745)
- new release tarball from FSF (Resolves: bz245303)
- new php-mode 1.2.0

* Wed May 23 2007 Chip Coldwell <coldwell@redhat.com> - 22.0.990-2
- revert all spec file changes since 22.0.95-1 (Resolves: bz239745)
- new pretest tarball from FSF (Resolves: bz238234)
- restore php-mode (Resolves: bz235941)

* Mon May 21 2007 Chip Coldwell <coldwell@redhat.com> - 22.0.990-1
- new pretest tarball from FSF
- removed Ulrich Drepper's patch to prevent mmapped pages during dumping
  removed BuildRequires: glibc >= 2.5.90-22
  (bug traced to glibc Resolves: bz239344)
- fix alternatives removal scriptlet (Resolves: bz239745)

* Thu May 17 2007 Chip Coldwell <coldwell@redhat.com> - 22.0.99-4
- format of freed blocks changed between glibc 2.5.90-21 and 2.5.90-22
- BuildRequires: glibc >= 2.5.90-22 (Ulrich Drepper)

* Sun May 13 2007 Chip Coldwell <coldwell@redhat.com> - 22.0.99-2
- prevent mmapped pages during dumping (Ulrich Drepper Resolves: bz239344)

* Tue Apr 24 2007 Chip Coldwell <coldwell@redhat.com> - 22.0.99-1
- new (last?) pretest tarball from FSF
- update to php-mode-1.2.0 (Ville Skyttä Resolves: bz235941)
- use /etc/alternatives instead of wrapper script

* Tue Mar  6 2007 Chip Coldwell <coldwell@redhat.com> - 22.0.95-1
- new pretest tarball from FSF

* Mon Feb 26 2007 Chip Coldwell <coldwell@redhat.com> - 22.0.94-1
- new pretest tarball obsoletes loaddefs.el dependencies patch

* Fri Feb 23 2007 Chip Coldwell <coldwell@redhat.com> - 22.0.93-7
- fix po-mode-init.el (Kjartan Maraas #228143)

* Tue Feb 13 2007 Chip Coldwell <coldwell@redhat.com> - 22.0.93-6
- remove --without-xim configure flag to fix dead keys (Alexandre Oliva #224626)

* Fri Jan 26 2007 Chip Coldwell <coldwell@redhat.com> - 22.0.93-5
- remove Tetris to avoid trademark problems (Ville Skyttä #224627)

* Thu Jan 25 2007 Chip Coldwell <coldwell@redhat.com> - 22.0.93-4
- fixup loaddefs.el dependencies (Dan Nicolaescu #176171)
- add BuildRequires: automake (changes to Makefile.in)

* Wed Jan 24 2007 Chip Coldwell <coldwell@redhat.com> - 22.0.93-3
- po-mode.el was being left out

* Tue Jan 23 2007 Chip Coldwell <coldwell@redhat.com> - 22.0.93-1
- new pretest version
- removed setarch since new dumper copes with execshield
- clean up site initialization files (varions #176171)

* Tue Jan  2 2007 Chip Coldwell <coldwell@redhat.com> - 22.0.92-1
- new pretest version
- removed almost all emacs 21 patches from emacs 22
- clean up spec file,
- many new BuildRequires (David Woodhouse #221250)

* Tue Nov 14 2006 Chip Coldwell <coldwell@redhat.com> - 22.0.90-1
- first pretest rpm build

* Mon Nov  6 2006 Chip Coldwell <coldwell@redhat.com> - 21.4-19
- BuildRequires: sendmail (Wolfgang Rupprecht #213813)

* Thu Aug  3 2006 Chip Coldwell <coldwell@redhat.com> - 21.4-18
- non-CJK text broken by default for Western locale (James Ralston #144707)

* Thu Aug  3 2006 Chip Coldwell <coldwell@redhat.com> - 21.4-17
- use UTF-8 keyboard input encoding on terminals that support it (Axel Thimm #185399)

* Thu Aug  3 2006 Chip Coldwell <coldwell@redhat.com> - 21.4-16
- fix German spell checking for UTF-8 encoded buffers (Daniel Hammer #197737)

* Wed Jul 26 2006 Chip Coldwell <coldwell@redhat.com> - 21.4-15
- fix src/unexelf.c to build on PowerPC64 (backport from emacs-22, #183304)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 21.4-14.1.1
- rebuild

* Tue Apr 18 2006 Chip Coldwell <coldwell@redhat.com> - 21.4-14.1
- don't clobber site-lisp/default.el (Ritesh Khadgaray, 180153)

* Tue Mar  7 2006 Jens Petersen <petersen@redhat.com> - 21.4-14
- bring back setarch for i386 with -R option in spec file and drop
  emacs-21-personality-linux32-101818.patch since it no longer seems
  sufficient with recent kernels (Sam Peterson, #174736)
- buildrequire giflib-devel instead of libungif-devel

* Thu Mar  2 2006 Jens Petersen <petersen@redhat.com>
- avoid backup for fix-x-vs-no-x-diffs.dpatch (Ian Collier, #183503)
- remove the old ccmode info manual (#182084)

* Mon Feb 27 2006 Jens Petersen <petersen@redhat.com> - 21.4-13
- buildrequire libXaw-devel for menus and scrollbar
- pass -R to setarch to disable address randomization during dumping
  (Sam Peterson, #174736)
- install cc-mode.info correctly (Sam Peterson, #182084)
- fix sort-columns not to use deprecated non-posix sort key syntax
  with sort-columns-posix-key-182282.patch (Richard Ryniker, #182282)
- use system-name function not variable when setting frame-title-format in
  /etc/skel/.emacs for XEmacs users hitting .emacs

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 21.4-12.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 21.4-12.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Feb  3 2006 Jens Petersen <petersen@redhat.com> - 21.4-12
- add mule-cmd.el-X11-locale.alias-173781.patch to correct location of X11
  locale.alias file (Paul Dickson, #173781)
- fix autoload of php-mode in php-mode-init.el (Christopher Beland, #179484)

* Wed Dec 14 2005 Jens Petersen <petersen@redhat.com> - 21.4-11
- avoid building with -fstack-protector on i386 to prevent crashing
  (Jonathan Kamens, #174730)
- require xorg-x11-fonts-ISO8859-1-75dpi instead of xorg-x11-fonts-75dpi
  for modular X (#174614)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Nov 25 2005 Jens Petersen <petersen@redhat.com> - 21.4-10
- fix missing parenthesis in lang-coding-systems-init.el

* Tue Nov 22 2005 Jens Petersen <petersen@redhat.com> - 21.4-9
- fix keyboard-coding-system on console for utf-8 (Dawid Gajownik, #173855)
- update etags to latest cvs (Hideki Iwamoto, #173023)
  - replace etags-14.21-17.11-diff.patch with etags-update-to-cvs.patch
- update smtpmail.el to latest cvs version for better authentication support
  with smtpmail-cvs-update.patch (Alberto Brizio, #167804)

* Mon Nov 14 2005 Jeremy Katz <katzj@redhat.com> - 21.4-8
- update dep for new xorg fonts packages

* Wed Aug 24 2005 Jens Petersen <petersen@redhat.com>
- fix name of aspell-es dictionary (#147964)
  - update emacs-21.3-lisp-textmodes-ispell-languages.patch

* Thu Jul 14 2005 Jens Petersen <petersen@redhat.com> - 21.4-7
- update rpm-spec-mode.el to cvs revision 1.17 (Ville Skyttä)
  - fixes expansion of %%{?dist}
- replace emacs-21.4-setarch_for_loadup-101818.patch with backport
  emacs-21-personality-linux32-101818.patch from cvs (Jan Djärv)
  which also turns off address randomization during dumping (Masatake Yamato)
  - no longer need to pass SETARCH to make on i386 (#160814)
- move ownership of %%{_datadir}/emacs/ and %%{_datadir}/emacs/%%{version}/
  from emacs to emacs-el and emacs-leim subpackages
- don't build tramp html and dvi documentation
- drop src/config.in part of bzero-and-have-stdlib.dpatch to avoid
  compiler warnings

* Thu Jun 23 2005 Jens Petersen <petersen@redhat.com> - 21.4-6
- merge in changes from emacs22.spec conditionally
  - define emacs21 rpm macro switch to control major version and use it
- update tramp to 2.0.49

* Fri Jun 17 2005 Jens Petersen <petersen@redhat.com>
- set arg0 to emacs in wrapper script (Peter Oliver, 149512#3)

* Mon May 30 2005 Jens Petersen <petersen@redhat.com>
- move setting of require-final-newline from default.el to a comment in default
  .emacs (Ralph Loader, 119141)

* Wed May 18 2005 Jens Petersen <petersen@redhat.com> - 21.4-5
- update cc-mode to 5.30.9 stable release to address font-lock problems
  (126165,148977,150197,155292,158044)

* Mon May 16 2005 Jens Petersen <petersen@redhat.com> - 21.4-4
- don't accidently exclude emacsclient from common package
  (Jonathan Kamens, #157808)
- traditional Chinese desktop file translation (Wei-Lun Chao, #157287)

* Wed Apr 20 2005 Jens Petersen <petersen@redhat.com> - 21.4-3
- add igrep.el and init file

* Mon Apr 11 2005 Jens Petersen <petersen@redhat.com> - 21.4-2
- update etags to 17.11 (idht4n@hotmail.com, 151390)
  - add etags-14.21-17.11-diff.patch
- replace i386 setarch redefinitions of __make and makeinstall with
  emacs-21.4-setarch_for_loadup-101818.patch and setting SETARCH on i386
  (Jason Vas Dias, 101818)

* Sun Apr 10 2005 Jens Petersen <petersen@redhat.com> - 21.4-1
- update to 21.4 movemail vulnerability release
  - no longer need movemail-CAN-2005-0100.patch
- replace %%{_bindir}/emacs alternatives with a wrapper script (Warren Togami)
  to prevent it from disappearing when upgrading (Michal Jaegermann, 154326)
  - suffix the X emacs binaries with -x and the no X binaries with -nox
  - the wrapper script %%{_bindir}/emacs-%%version runs emacs-x if installed or
    otherwise emacs-nox.  %%{_bindir}/emacs is a symlink to the wrapper
- make emacs and emacs-nox own the subdirs in %%{_libexecdir}
- add a bunch of fixes from debian's emacs21_21.4a-1 patch:
    battery-acpi-support.dpatch, bzero-and-have-stdlib.dpatch,
    coding-region-leak.dpatch, detect-coding-iso2022.dpatch,
    fix-batch-mode-signal-handling.dpatch, pcl-cvs-format.dpatch,
    python-completion-ignored-extensions.dpatch,
    remote-files-permissions.dpatch, save-buffer.dpatch, scroll-margin.dpatch,
    xfree86-4.3-modifiers.dpatch
  - add fix-x-vs-no-x-diffs.dpatch
    - define emacs_libexecdir
    - build both emacs and emacs-nox as %%{version}.1 and move common DOC file
      to emacs-common
    - suffix version in fns-%%{version}.1.el with -x and -nox respectively
- add 100 to elisp patches

* Wed Apr  6 2005 Jens Petersen <petersen@redhat.com> - 22.0.50-0.20050406
- update to snapshot of current cvs
  - configure xim support off by default
  - bootstrap snapshot

* Wed Apr  6 2005 Jens Petersen <petersen@redhat.com> - 21.3-27
- use alternatives to switch _bindir/emacs between emacs and emacs-nox
  (Henning Schmiedehausen, #151067)
  - remove emacs and emacs-nox from bindir
  - prereq alternatives for emacs and emacs-nox
  - add post and postun scripts to handle alternatives
- buildrequire xorg-x11-devel instead of XFree86-devel
- really include and apply emacs-21.3-latex-mode-hook-144083.patch
- make emacs and emacs-nox own _datadir/emacs/version too

* Wed Mar  9 2005 Jens Petersen <petersen@redhat.com> - 21.3-26
- rebuild with gcc 4.0
  - add emacs-21.3-gcc4.patch for emacsclient

* Mon Feb 28 2005 Jens Petersen <petersen@redhat.com> - 21.3-25
- add tramp-2.1.3 to site-lisp (David Woodhouse, 149703)
  - move removal of info dir to after its installation
  - add tramp-init.el to put tramp into load-path

* Thu Feb 24 2005 Jens Petersen <petersen@redhat.com> - 21.3-24
- mark default.el as a noreplace config file (Pawel Salek, 149310)
- only set keyboard-coding-system in xterms to fix problem with input
  Latin characters becoming prefixes and making emacs loop
  (Eddahbi Karim, 126007)
- make emacs-el own its lisp directories
- run latex-mode-hook in latex-mode (Martin Biely, 144083)
  - add emacs-21.3-latex-mode-hook-144083.patch

* Fri Feb 18 2005 Jens Petersen <petersen@redhat.com> - 21.3-23
- install %%{_bindir}/emacs-nox as a hardlink of the versioned binary
- drop explicit lib requirements
- use sed instead of perl to fix up filelists

* Mon Feb 14 2005 Jens Petersen <petersen@redhat.com> - 21.3-22
- use prereq instead of contexts for common script requirements
  (Axel Thimm, 147791)
- move emacs.png from common to main package

* Fri Feb  4 2005 Jens Petersen <petersen@redhat.com> - 21.3-21
- fix CAN-2005-0100 movemail vulnerability with movemail-CAN-2005-0100.patch
  (Max Vozeler, 146701)

* Fri Jan 14 2005 Jens Petersen <petersen@redhat.com> - 21.3-20
- workaround xorg-x11 modifier key problem with
  emacs-21.3-xterm-modifiers-137868.patch (Thomas Woerner, 137868)

* Mon Nov 29 2004 Jens Petersen <petersen@redhat.com> - 21.3-19
- prefer XIM status under-the-window for now to stop xft httx from dying
  (125413): add emacs-xim-status-under-window-125413.patch
- default diff to unified format in .emacs

* Wed Nov 10 2004 Jens Petersen <petersen@redhat.com> - 21.3.50-0.20041111
- initial packaging of cvs emacs
  - leim and elisp manual now in main tarball
  - no leim subpackage anymore, so make common obsolete it
  - no longer need MuleUCS, nor rfc1345.el
  - buildrequire and use autoconf rather autoconf213
  - no longer need emacs-21.2-x86_64.patch,
    editfns.c-Fformat-multibyte-davej.patch
  - bring back game for now
  - TODO: some patches still need updating
  - fns.el no longer installed
  - remove /var/games for now
  - update filelist generation to single sweep
  - update info_files list

* Thu Nov  4 2004 Jens Petersen <petersen@redhat.com> - 21.3-18
- show emacs again in the desktop menu (132567)
- require fonts-xorg-75dpi to prevent empty boxes at startup due to missing
  fonts (Johannes Kaiser, 137060)

* Mon Oct 18 2004 Jens Petersen <petersen@redhat.com> - 21.3-17
- fix etag alternatives removal when uninstalling (Karsten Hopp, 136137)

* Fri Oct 15 2004 Jens Petersen <petersen@redhat.com> - 21.3-16
- do not setup frame-title-format in default.el, since it will override
  setting by users (Henrik Bakken, 134520)
- emacs-el no longer requires emacs for the sake of -nox users
  (Lars Hupfeldt Nielsen, 134479)
- condition calling of global-font-lock-mode in default .emacs
  in case xemacs should happen to load it

* Wed Sep 29 2004 Jens Petersen <petersen@redhat.com> - 21.3-15
- cleanup and update .desktop file
- make emacs not appear in the desktop menu (Seth Nickell,132567)
- move the desktop file from -common to main package
- go back to using just gctags for ctags
- etags is now handled by alternatives (92256)
- improve the default frame title by prefixing the buffer name
  (Christopher Beland, 128110)
- fix the names of some European aspell languages with
  emacs-21.3-lisp-textmodes-ispell-languages.patch (David Jansen, 122618)
- fixing running "libtool gdb program" in gud with
  emacs-21.3-gud-libtool-fix.patch (Dave Malcolm, 130955)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Apr 30 2004 Jens Petersen <petersen@redhat.com> - 21.3-13
- unset focus-follows-mouse in default.el to make switching frames work for
  click-to-focus (Theodore Belding,114736)

* Thu Apr 15 2004 Jens Petersen <petersen@redhat.com> - 21.3-12
- update php-mode to 1.1.0
- add emacs-21.3-no-rpath.patch so that /usr/X11R6/lib is not rpath'ed
- require /bin/ln for %%post (Tim Waugh, 119817)
- move prereq for dev and /sbin/install-info to emacs-common
- leim no longer requires emacs
- use source site-lisp dir in %%prep to setup site files
- define and use site_lisp for buildroot in %%install
- default ispell dictionary to "english" for CJK locale
- add comment to top of site-start.el about load order
- turn on auto-compression-mode in default.el (114808)
- set require-final-newline with setq (David Olsson,119141)
  and remove redundant next-line-add-newlines setting
- update info_file list (Reuben Thomas,114729)

* Tue Mar 16 2004 Mike A. Harris <mharris@redhat.com> 21.3-11
- Removed bogus Requires: XFree86-libs that was added in 21.3-8, as rpm
  find-requires will automatically pick up the dependancies on any runtime
  libraries, and such hard coded requires is not X11 implementation
  agnostic (#118471)

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat Jan 24 2004 Jens Petersen <petersen@redhat.com> - 21.3-9
- bring back emacs-nox subpackage (emacs built without X support) (#113001)
  [suggested by Frank Kruchio]
- base emacs package now only contains emacs binary built with X support
  and no longer obsoletes emacs-nox
- all the common files required by emacs and emacs-nox are now in emacs-common
- update php-mode.el to 1.0.5
- add missing rfc1345.el leim input method
- update po-compat.el to version in gettext-0.13.1
- update base package summary
- add url for python-mode.el and php-mode.el
- gctags is now a symlink to ctags.emacs

* Wed Jan 14 2004 Jens Petersen <petersen@redhat.com> - 21.3-8
- comment out setting transient-mark-mode in skel .emacs (#102441,#90193)
  [reported by mal@gromco.com, Jonathan Kamens]
- improve lang-coding-systems-init.el to set-language-environment for CJK
  utf-8 locale too and use utf-8 for default-coding-systems and
  terminal-coding-system (#111172) [Yoshinori Kuniga]
- update rpm-spec-mode.el to newer one in xemacs package cvs (#105888) [Dams]
- rename etags to etags.emacs and make etags a symlink to it at install time
  if it doesn't exist (#92256) [marc_soft@merlins.org]
- apply editfns.c-Fformat-multibyte-davej.patch to fix multibyte code typo
  in Fformat [patch from Dave Jones]
- add runtime requirements for XFree86-libs, image libraries, ncurses and zlib
- improve -el and -leim package summaries
- no longer configure build with redundant --with-gcc

* Tue Nov 25 2003 Jens Petersen <petersen@redhat.com>
- buildrequire autoconf213 (#110741) [reported by mvd@mylinux.com.ua]

* Mon Oct 27 2003 Jens Petersen <petersen@redhat.com> - 21.3-7
- use "setarch i386" to build on ix86 (#101818) [reported by Michael Redinger]
- use __make to %%build and %%install
- set keyboard coding-system for utf-8 in lang-coding-systems-init.el (#106929)
  [reported with fix by Axel Thimm]
- add source url for MuleUCS
- update base package description (#103551) [reported by Tim Landscheidt]

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May  7 2003 Jens Petersen <petersen@redhat.com> - 21.3-5
- move transient-mark-mode and global-font-lock-mode setting from default.el
  back to dotemacs, so as not to surprise old users (#90193)
  [reported by jik@kamens.brookline.ma.us]
- change require-final-newline to query (default.el)
- don't make a backup when applying browse-url-htmlview-84262.patch (#90226)
  [reported by mitr@volny.cz]

* Fri May  2 2003 Elliot Lee <sopwith@redhat.com>
- Add emacs-21.3-ppc64.patch

* Fri Apr 25 2003 Jens Petersen <petersen@redhat.com> - 21.3-3
- use Mule-UCS utf-8 coding-system for CJK subprocess IO
- no need to set fontset anymore in CJK locale

* Wed Apr 16 2003 Jens Petersen <petersen@redhat.com> - 21.3-2
- add Mule-UCS for CJK utf-8 support (suggested by Akira Tagoh)
  and use it by default in CJK UTF-8 locale
- move emacs-asian startup files into new lang-coding-systems-init.el
- utf-8 setup in site-start.el is no longer needed in Emacs 21.3
- generate filelist for site-lisp automatically like base lisp and leim
- don't setup aspell in site-start.el
- rename dotemacs to dotemacs.el and move former contents to new default.el

* Mon Apr  7 2003 Jens Petersen <petersen@redhat.com> - 21.3-1
- update to 21.3
- no longer set compound-text-with-extensions in dotemacs, since it is now
  the default
- emacs-21.2-pop.patch is no longer needed
- update php-mode to 1.0.4

* Thu Feb 20 2003 Jens Petersen <petersen@redhat.com> - 21.2-33
- default browse-url to use htmlview (#84262)
- remove info dir file rather than excluding it

* Sat Feb  8 2003 Jens Petersen <petersen@redhat.com> - 21.2-32
- set X copy'n'paste encoding to extended compound-text (#74100)
  by default in .emacs file [suggested by olonho@hotmail.com]
- .emacs file cleanup (xemacs now has a separate init file)

* Fri Feb  7 2003 Jens Petersen <petersen@redhat.com> - 21.2-31
- block input in allocate_vectorlike to prevent malloc hangs (#83600)
  [thanks to Jim Blandy]
- set startup wmclass notify in desktop file

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Jan 15 2003 Jens Petersen <petersen@redhat.com> 21.2-29
- update to newer po-mode.el and po-compat.el from gettext-0.11.4
- patch po-mode's po-replace-revision-date for when
  po-auto-replace-revision-date is nil (#71264)
- update po-mode-init.el
- examine LC_ALL before LC_CTYPE in site-start.el for utf-8 (#79535)
- don't install etc/DOC files explicitly by hand
- make sure all lisp .elc files are up to date
- pass _smp_mflags to make
- remove games that we shouldn't ship

* Mon Jan 13 2003 Karsten Hopp <karsten@redhat.de> 21.2-28
- s390x lib64 fix

* Fri Jan  3 2003 Jens Petersen <petersen@redhat.com> 21.2-27
- look at LANG after LC_CTYPE when checking for UTF-8 locale encoding
  in site-start.el (#79535)
- don't set desktop file config(noreplace)

* Fri Dec 20 2002 Jens Petersen <petersen@redhat.com> 21.2-26
- unset the sticky bit of emacs in bindir (#80049)

* Wed Dec 18 2002 Jens Petersen <petersen@redhat.com> 21.2-25
- no need to patch config.{sub,guess}

* Tue Dec  3 2002 Tim Waugh <twaugh@redhat.com>
- Fix python-mode-init.el (bug #78910).

* Sun Dec  1 2002 Jens Petersen <petersen@redhat.com> 21.2-24
- rpm-spec-mode update fixes
  - patch in XEmacs compat functions rather than defining them with apel
    macros in init file (#78764)
  - autoload "rpm-spec-mode" not "rpm-spec-mode.el" in same file
- let emacs base also own leim dir to avoid startup warning about missing dir
  when -el and -leim aren't installed (#78764)

* Thu Nov 28 2002 Jens Petersen <petersen@redhat.com>
- use LC_CTYPE rather than LANG to determine default encoding (#78678)
  [reported by starback@stp.ling.uu.se]

* Wed Nov 27 2002 Jens Petersen <petersen@redhat.com> 21.2-23
- set transient-mark-mode in dotemacs for Emacs not XEmacs (#75440)
- update rpm-spec-mode.el to 0.12
  - define needed XEmacs compat functions in new rpm-spec-mode-init.el
- tidy site-start.el
  - move python-mode setup to python-mode
- don't build with sbin in path
- use _libexecdir, _bindir and _sysconfdir
- don't gzip info files explicitly
- use tar's C and j options
- generate lisp file-lists in single find sweeps over lisp and leim dirs
  - use -fprint and -fprintf
  - correct more dir ownerships

* Sun Nov 24 2002 Florian La Roche <Florian.LaRoche@redhat.de> 21.2-22
- add correct alloca defines for s390

* Wed Nov  6 2002 Jens Petersen <petersen@redhat.com> 21.2-21
- uses patches for x86_64 and s390 support and config.{guess,sub} updating

* Tue Nov  5 2002 Jens Petersen <petersen@redhat.com> 21.2-20
- add support for x86_64 and merge in s390 support from cvs
- add alloca defines to amdx86-64.h (from SuSE)

* Wed Oct 30 2002 Jens Petersen <petersen@redhat.com> 21.2-19
- own our libexec dir (#73984)
- only set transient-mark-mode in dotemacs for Emacs (#75440)
- update to latest config.{guess,sub}
- use _datadir macro

* Wed Aug 28 2002 Trond Eivind Glomsrød <teg@redhat.com> 21.2-18
- Desktop file fix - add Application to make it show up
- DNS lookup fix for pop (#64802)

* Tue Aug 27 2002 Trond Eivind Glomsrød <teg@redhat.com> 21.2-17
- Fix gdb arrow when used in non-windowed mode (#56890)

* Fri Aug  9 2002 Trond Eivind Glomsrød <teg@redhat.com> 21.2-16
- Handle UTF-8 input (#70855).

* Tue Aug  6 2002 Trond Eivind Glomsrød <teg@redhat.com> 21.2-15
- Don't use canna by default (#70870)

* Thu Aug  1 2002 Trond Eivind Glomsrød <teg@redhat.com> 21.2-14
- Fixes to desktop file (add encoding, add missing a ";")
- Update s390 patch

* Wed Jul 24 2002 Trond Eivind Glomsrød <teg@redhat.com> 21.2-13
- rpm -> rpmbuild for rpmspec mode (#68185)

* Mon Jul 22 2002 Trond Eivind Glomsrød <teg@redhat.com> 21.2-12
- desktop file changes (#69385)

* Mon Jul  8 2002 Trond Eivind Glomsrød <teg@redhat.com> 21.2-11
- Fix php-mode to not initialize on e.g.  foophp.c (#67592)

* Thu Jun 27 2002 Trond Eivind Glomsrød <teg@redhat.com> 21.2-10
- Downgrade po-mode

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Jun 17 2002 Trond Eivind Glomsrød <teg@redhat.com> 21.2-8
- #66808

* Wed May 29 2002 Trond Eivind Glomsrød <teg@redhat.com> 21.2-7
- Rebuild

* Mon May 20 2002 Trond Eivind Glomsrød <teg@redhat.com> 21.2-6
- Prereq dev

* Thu May 16 2002 Trond Eivind Glomsrød <teg@redhat.com> 21.2-5
- Update the elisp manual and po-mode

* Tue May  7 2002 Trond Eivind Glomsrød <teg@redhat.com> 21.2-4
- php-mode 1.0.2

* Thu Apr 25 2002 Trond Eivind Glomsrød <teg@redhat.com> 21.2-3
- Update po-mode to the one from gettext 0.11.1

* Mon Apr  8 2002 Trond Eivind Glomsrød <teg@redhat.com> 21.2-2
- Tweak mouse init process (#59757)

* Mon Mar 18 2002 Trond Eivind Glomsrød <teg@redhat.com> 21.2-1
- 21.2

* Fri Mar  8 2002 Trond Eivind Glomsrød <teg@redhat.com> 21.1.95-1
- 21.1.95

* Fri Feb  8 2002 Trond Eivind Glomsrød <teg@redhat.com> 21.1.90-2
- Upgrade po-mode to the version bundled with gettext 0.11
- Upgrade rpm-spec-mode to 0.11h

* Thu Jan 31 2002 Trond Eivind Glomsrød <teg@redhat.com> 21.1.90-1
- 21.1.90

* Fri Jan 18 2002 Trond Eivind Glomsrød <teg@redhat.com> 21.1.80-2
- Add ebrowse
- Set transient-mode to t in /etc/skel/.emacs

* Mon Jan 14 2002 Trond Eivind Glomsrød <teg@redhat.com> 21.1.80-1
- 21.1.80

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Dec  6 2001 Trond Eivind Glomsrød <teg@redhat.com> 21.1-3
- Increase recursive-load-depth-limit from 10 to 50

* Wed Dec  5 2001 Trond Eivind Glomsrød <teg@redhat.com> 21.1-2
- Make it conflict with old versions of gettext

* Thu Nov 29 2001 Trond Eivind Glomsrød <teg@redhat.com> 21.1-1
- rpm-spec-mode 0.11h, should fix #56748

* Tue Nov  6 2001 Trond Eivind Glomsrød <teg@redhat.com> 21.1-0.4
- php mode 1.0.1. Should fix some speedbar problems.

* Tue Oct 23 2001 Trond Eivind Glomsrød <teg@redhat.com> 21.1-0.3
- Minor cleanups
- add ssl.el

* Mon Oct 22 2001 Trond Eivind Glomsrød <teg@redhat.com> 21.1-0.2
- Add more files from the libexec directory (#54874, #54875)

* Sun Oct 21 2001 Trond Eivind Glomsrød <teg@redhat.com> 21.1-0.1
- 21.1
- Build on IA64 again - the default config now handles it
- Drop all old patches
- Misc cleanups
- Update the elisp manual to 21-2.7
- Deprecate the emacs-nox and emacs-X11 subpackages.
  Simplify build procedure to match.
- Update php-mode to 1.0.0

* Mon Oct 15 2001 Trond Eivind Glomsrød <teg@redhat.com> 20.7-43
- Add php-mode 0.9.9
- Add URL (#54603)
- don't run autoconf/libtoolize during build - they're broken
- don't build on IA64 until they are fixed

* Sun Sep 16 2001 Trond Eivind Glomsrød <teg@redhat.com> 20.7-42
- Update python-mode to the version in the python 2.2a3
- Include po-mode in emacs, instead of including in gettext

* Mon Jul 30 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Minor fix to make-mode fontify regexp (#50010)
- Build without emacs being installed (#49085)

* Tue Jun 19 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Much cleaner site-start.d sourcing
- Add more build dependencies
- Add the emacs lisp reference info pages (RFE #44577)
- Don't require tamago - just plug it in for Japanese support

* Mon Jun 18 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Add Xaw3d-devel to buildrequires (#44736)

* Mon Jun 18 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- merged s390x patch from <oliver.paukstadt@millenux.com>

* Mon Jun  4 2001 Trond Eivind Glomsrød <teg@redhat.com>
- New rpm-spec-mode.el, which fixes #43323

* Thu Apr 26 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- fix linker problem on s390 (fix by Than Ngo than@redhat.com)

* Wed Apr 25 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Make sure that mwheel is initialized for XEmacs (#37451)

* Fri Mar 16 2001 Trond Eivind Glomsrød <teg@redhat.com>
- New locale.alias file for emacs-nox

* Tue Mar  6 2001 Trond Eivind Glomsrød <teg@redhat.com>
- update rpm-spec-mode.el to 0.11e - this should fix #30702

* Fri Feb 16 2001 Preston Brown <pbrown@redhat.com>
- require tamago, or japanese cannot be input (#27932).

* Sat Jan 27 2001 Jakub Jelinek <jakub@redhat.com>
- Preprocess Makefiles as if they were assembly, not C source.

* Wed Jan 24 2001 Yukihiro Nakai <ynakai@redhat.com>
- Fix the fontset problem when creating a new frame.

* Thu Jan 18 2001 Trond Eivind Glomsrød <teg@redhat.com>
- add Japanese support from Yukihiro Nakai <ynakai@redhat.com>

* Thu Jan 04 2001 Preston Brown <pbrown@redhat.com>
- do not remove etags, only ctags, per Tom Tromey's suggestion.

* Wed Dec 27 2000 Tim Powers <timp@redhat.com>
- bzipped sources to conserve space

* Mon Dec 18 2000 Trond Eivind Glomsrød <teg@redhat.com>
- add /usr/share/emacs/locale.alias , which had gone AWOL
- update rpm-spec-mode to 0.11a, fresh from the author
  (Stig Bjorlykke <stigb@tihlde.org>). The changes we made
  are integrated.

* Fri Dec 15 2000 Trond Eivind Glomsrød <teg@redhat.com>
- prereq fileutils for emacs-nox

* Mon Dec 11 2000 Trond Eivind Glomsrød <teg@redhat.com>
- do locale.alias fix for emacs-nox only, as it somehow
  broke the subject line in gnus. Weird.
- update to gnus 5.8.7

* Fri Dec 08 2000 Than Ngo <than@redhat.com>
- add support s390 machine

* Thu Dec 07 2000 Trond Eivind Glomsrød <teg@redhat.com>
- add rpm-spec-mode after modifying (use Red Hat groups,
  from /usr/share/doc/rpm-version/GROUPS) and fixing
  colours(don't specify "yellow" on "bright") Also,
  use gpg, not pgp.
- use it (site-start.el)
- add mwheel
- use it, in /etc/skel/.emacs

* Thu Nov 30 2000 Trond Eivind Glomsrød <teg@redhat.com>
- add /usr/share/emacs/site-lisp/site-start.d
- change site-start.el so files in the above directory
  are automatically run on startup
- don't set the ispell name in site-start.el, use the
  above directory instead

* Thu Oct 19 2000 Trond Eivind Glomsrød <teg@redhat.com>
- fix icon name in the .desktop file
- don't have site-start.el "noreplace"
- load psgml-init (if present) in the default site-start.el
  to avoid psgml modifying the file

* Tue Oct 17 2000 Trond Eivind Glomsrød <teg@redhat.com>
- new and better emacs.desktop file

* Tue Oct 10 2000 Trond Eivind Glomsrød <teg@redhat.com>
- remove ctags.1 and etags.1 from the emacs etc directory
  (#18011)
- fix the emacs-nox not to use the locale.alias in XFree86
  (#18548)... copy it into /usr/share/emacs and patch
  the startup files to use it. Argh.

* Wed Oct 04 2000 Trond Eivind Glomsrød <teg@redhat.com>
- fix initialization of python mode (require it before
  customizing it)

* Fri Sep 22 2000 Bill Nottingham <notting@redhat.com>
- don't use bcopy without a prototype

* Thu Aug 24 2000 Trond Eivind Glomsrød <teg@redhat.com>
- define MAIL_USE_LOCKF
- remove setgid on movemail

* Mon Aug 07 2000 Trond Eivind Glomsrød <teg@redhat.com>
- add /usr/share/emacs/site-lisp/subdirs.el (#15639)

* Tue Jul 25 2000 Trond Eivind Glomsrød <teg@redhat.com>
- remove "-b" option from manpage

* Fri Jul 21 2000 Trond Eivind Glomsrød <teg@redhat.com>
- remove Japanese support

* Mon Jul 17 2000 Matt Wilson <msw@redhat.com>
- updated .desktop entry and icon

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Fri Jul 07 2000 Trond Eivind Glomsrød <teg@redhat.com>
- fix some typos in spec file

* Sun Jul 02 2000 Trond Eivind Glomsrød <teg@redhat.com>
- make /etc/skel/.emacs 0644

* Wed Jun 28 2000 Trond Eivind Glomsrød <teg@redhat.com>
- include python mode and change in site-start.el related to this
- some changes to the default .emacs

* Mon Jun 26 2000 Matt Wilson <msw@redhat.com>
- don't build with -O2 on alpha until we can track down the compiler
  bug that causes crashes in the garbage collector
- removed all the nox Japanese packages

* Mon Jun 19 2000 Trond Eivind Glomsrød <teg@redhat.com>
- include site-start.el as a a config file
- add aspell support via the above

* Fri Jun 16 2000 Trond Eivind Glomsrød <teg@redhat.com>
- (from MSW) different compression on IA64 to avoid hangs
- remove etags/ctags - use a separate package. Disable patch1

* Wed Jun 14 2000 Matt Wilson <msw@redhat.com>
- edited japanese patch not to patch configure
- fixed a missing escaped \" in a wc string
- merge japanese support to head of development

* Tue Jun 13 2000 Trond Eivind Glomsrød <teg@redhat.com>
- Version 20.7
- Add requirement for final newline to the default .emacs
- redid the Xaw3d patch
- checked all patches, discarded those we've upstreamed

* Wed Jun 07 2000 Trond Eivind Glomsrød <teg@redhat.com>
- use %%{_mandir} and %%{_infodir}

* Fri Jun  2 2000 Bill Nottingham <notting@redhat.com>
- add yet another ia64 patch

* Mon May 22 2000 Bill Nottingham <notting@redhat.com>
- add another ia64 patch

* Fri May 19 2000 Trond Eivind Glomsrød <teg@redhat.com>
- Disabled the compile patch for 20.6

* Thu May 18 2000 Bill Nottingham <notting@redhat.com>
- add in ia64 patch

* Thu May 18 2000 Trond Eivind Glomsrød <teg@redhat.com>
- don't apply the unexelf patch - use a new unexelf.c file
  from the 21 source tree (this will go into the 20.7 tree)

* Wed May 17 2000 Trond Eivind Glomsrød <teg@redhat.com>
- added patch by jakub to make it work with glibc2.2

* Mon May 08 2000 Trond Eivind Glomsrød <teg@redhat.com>
- fixed a problem with ange-ftp and kerberized ftp

* Mon May 08 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- rebuild with new Xaw3d

* Thu Apr 20 2000 Trond Eivind Glomsrød <teg@redhat.com>
- let the build system handle gzipping man pages and stripping
- added patch to increase keyboard buffer size

* Thu Apr 20 2000 Trond Eivind Glomsrød <teg@redhat.com>
- gzip man pages

* Thu Apr 20 2000 Trond Eivind Glomsrød <teg@redhat.com>
- added a security patch from RUS-CERT, which fixes
  bugs mentioned in "Advisory 200004-01: GNU Emacs 20"

* Tue Apr 18 2000 Trond Eivind Glomsrød <teg@redhat.com>
- patched to detect bash2 scripts.

* Thu Apr 06 2000 Trond Eivind Glomsrød <teg@redhat.com>
- removed configuraton file status from /usr/share/pixmaps/emacs.png

* Fri Mar 24 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- update to 20.6 and make it compile

* Mon Feb 21 2000 Preston Brown <pbrown@redhat.com>
- add .emacs make the delete key work to delete forward character for X ver.

* Wed Feb 16 2000 Cristian Gafton <gafton@redhat.com>
- fix bug #2988
- recompile patched .el files (suggested by Pavel.Janik@linux.cz)
- prereq /sbin/install-info

* Mon Feb 07 2000 Preston Brown <pbrown@redhat.com>
- wmconfig gone

* Thu Feb 03 2000 Cristian Gafton <gafton@redhat.com>
- fix descriptions and summary
- fix permissions for emacs niaries (what the hell does 1755 means for a
  binary?)
- added missing, as per emacs Changelog, NCURSES_OSPEED_T compilation
  flag; without it emacs on Linux is making global 'ospeed' short which
  is not the same as 'speed_t' expected by libraries. (reported by Michal
  Jaegermann <michal@harddata.com>)

* Mon Jan 10 2000 David S. Miller <davem@redhat.com>
- Revert src/unexecelf.c to 20.4 version, fixes SPARC problems.

* Sun Jan  9 2000 Matt Wilson <msw@redhat.com>
- strip emacs binary
- disable optimizations for now, they cause illegal instructions on SPARC.

* Sun Jan 09 2000 Paul Fisher <pnfisher@redhat.com>
- upgrade to 20.5a
- remove python-mode, wheelmouse support, and auctex menu
- import emacs.desktop with icon from GNOME

* Wed Dec 08 1999 Ngo Than <than@redhat.de>
- added python-mode, wheelmouse support and auctex menu
- added Comment[de] in emacs.desktop

* Sat Sep 25 1999 Preston Brown <pbrown@redhat.com>
- added desktop entry

* Thu Sep 23 1999 Preston Brown <pbrown@redhat.com>
- tried to fix triggers, hopefully working now.

* Wed Sep 01 1999 Preston Brown <pbrown@redhat.com>
- added trigger for making symlink to /usr/bin/emacs in emacs-nox package

* Thu Jul 22 1999 Paul Fisher <pnfisher@redhat.com>
- upgrade to 20.4
- cleaned up spec

* Fri Apr 16 1999 Owen Taylor <otaylor@redhat.com>
- replace bad xemacs compiled .elc file for mh-e with one compiled
  on emacs

* Thu Apr 15 1999 Bill Nottingham <notting@redhat.com>
- make sure movemail doesn't get %%defattr()'d to root.root

* Wed Apr 14 1999 Cristian Gafton <gafton@redhat.com>
- patch to make it work with dxpc

* Wed Mar 31 1999 Preston Brown <pbrown@redhat.com>
- updated mh-utils emacs lisp file to match our nmh path locations

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com>
- auto rebuild in the new build environment (release 9)

* Fri Feb 26 1999 Cristian Gafton <gafton@redhat.com>
- linker scripts hack to make it build on the alpha

* Fri Jan  1 1999 Jeff Johnson <jbj@redhat.com>
- add leim package (thanks to Pavel.Janik@inet.cz).

* Fri Dec 18 1998 Cristian Gafton <gafton@redhat.com>
- build against glibc 2.1

* Wed Sep 30 1998 Cristian Gafton <gafton@redhat.com>
- backed up changes to uncompress.el (it seems that the one from 20.2 works
  much better)

* Mon Sep 28 1998 Jeff Johnson <jbj@redhat.com>
- eliminate /tmp race in rcs2log

* Wed Sep 09 1998 Cristian Gafton <gafton@redhat.com>
- upgrade to 20.3

* Tue Jun  9 1998 Jeff Johnson <jbj@redhat.com>
- add --with-pop to X11 compile.
- include contents of /usr/share/.../etc with main package.

* Mon Jun 01 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr

* Mon Jun 01 1998 David S. Miller <davem@dm.cobaltmicro.com>
- fix signals when linked with glibc on non-Intel architectures
  NOTE: This patch is not needed with emacs >20.2

* Thu May 07 1998 Prospector System <bugs@redhat.com>

- translations modified for de, fr, tr

* Thu May 07 1998 Cristian Gafton <gafton@redhat.com>
- added /usr/lib/emacs/20.2/*-redhat-linux directory in the filelist

* Thu Apr 09 1998 Cristian Gafton <gafton@redhat.com>
- alpha started to like emacs-nox again :-)

* Thu Nov  6 1997 Michael Fulbright <msf@redhat.com>
- alpha just doesnt like emacs-nox, taking it out for now

* Mon Nov  3 1997 Michael Fulbright <msf@redhat.com>
- added multibyte support back into emacs 20.2
- added wmconfig for X11 emacs
- fixed some errant buildroot references

* Thu Oct 23 1997 Michael Fulbright <msf@redhat.com>
- joy a new version of emacs! Of note - no lockdir any more.
- use post/preun sections to handle numerous GNU info files

* Mon Oct 06 1997 Erik Troan <ewt@redhat.com>
- stopped stripping it as it seems to break things

* Sun Sep 14 1997 Erik Troan <ewt@redhat.com>
- turned off ecoff support on the Alpha (which doesn't build anymore)

* Mon Jun 16 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Fri Feb 07 1997 Michael K. Johnson <johnsonm@redhat.com>
- Moved ctags to gctags to fit in the more powerful for C (but less
  general) exuberant ctags as the binary /usr/bin/ctags and the
  man page /usr/man/man1/ctags.1
