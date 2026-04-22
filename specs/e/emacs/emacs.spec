## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 7;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# This file is encoded in UTF-8.  -*- coding: utf-8 -*-

%bcond gpm %[!(0%{?rhel} >= 10)]
%bcond_without gtkx11
%bcond_without lucid
%bcond_without nw

Summary:       GNU Emacs text editor
Name:          emacs
Epoch:         1
Version:       30.2
Release:       %autorelease
License:       GPL-3.0-or-later AND CC0-1.0
URL:           https://www.gnu.org/software/emacs/
%if %{lua: print(select(3, string.find(rpm.expand('%version'), '%d+%.%d+%.(%d+)')) or 0)} >= 90
Source0:       https://alpha.gnu.org/gnu/emacs/pretest/emacs-%{version}.tar.xz
Source1:       https://alpha.gnu.org/gnu/emacs/pretest/emacs-%{version}.tar.xz.sig
%else
Source0:       https://ftp.gnu.org/gnu/emacs/emacs-%{version}.tar.xz
Source1:       https://ftp.gnu.org/gnu/emacs/emacs-%{version}.tar.xz.sig
%endif
Source100:     https://keys.openpgp.org/vks/v1/by-fingerprint/17E90D521672C04631B1183EE78DAE0F3115E06B
Source101:     https://keys.openpgp.org/vks/v1/by-fingerprint/CEA1DE21AB108493CC9C65742E82323B8F4353EE
Source102:     https://keys.openpgp.org/vks/v1/by-fingerprint/12BB9B400EE3F77282864D18272B5C54E015416A

Source4:       dotemacs.el
Source5:       site-start.el
Source6:       default.el
Source9:       emacs-desktop.sh

Source10:      emacs_lisp.attr
Source11:      emacs_lisp.rec

# Avoid trademark issues
Patch:         0001-Pong-and-Tetris-are-excluded.patch

# rhbz#713600
Patch:         emacs-spellchecker.patch

Patch:         emacs-system-crypto-policies.patch

# causes a dependency on pkgconfig(systemd)
# => remove it if we stop using this patch
Patch:         emacs-libdir-vs-systemd.patch

# Hint what to do to avoid using the pure GTK build on X11, where it is
# unsupported:
Patch:         emacs-pgtk-on-x-error-message.patch

# Workaround for https://bugzilla.redhat.com/show_bug.cgi?id=2276822
# (https://debbugs.gnu.org/cgi/bugreport.cgi?bug=63555).  If GDK ever
# gets any new backends, this patch may need extending.
Patch:         0002-Fall-back-to-the-terminal-from-pure-GTK-when-no-disp.patch

# Don't override StartupWMClass.  The overriding value doesn't work on
# Wayland, and the default should be fine.
# https://debbugs.gnu.org/cgi/bugreport.cgi?bug=49505#67
Patch:         0001-Don-t-specify-StartupWMClass-in-emacs.desktop.patch

BuildRequires: alsa-lib-devel
BuildRequires: atk-devel
BuildRequires: autoconf
BuildRequires: bzip2
BuildRequires: cairo
BuildRequires: cairo-devel
BuildRequires: dbus-devel
BuildRequires: desktop-file-utils
BuildRequires: fontconfig-devel
BuildRequires: freetype-devel
BuildRequires: gcc
BuildRequires: giflib-devel
BuildRequires: glibc-devel
BuildRequires: gnupg2
BuildRequires: gnutls-devel
BuildRequires: gtk3-devel
BuildRequires: gzip
BuildRequires: harfbuzz-devel
BuildRequires: libacl-devel
BuildRequires: libappstream-glib
BuildRequires: libgccjit-devel
BuildRequires: libjpeg-turbo
BuildRequires: libjpeg-turbo-devel
BuildRequires: libotf-devel
BuildRequires: libpng-devel
BuildRequires: librsvg2-devel
BuildRequires: libselinux-devel
BuildRequires: libtiff-devel
BuildRequires: libtree-sitter-devel
BuildRequires: libwebp-devel
BuildRequires: libxml2-devel
BuildRequires: m17n-lib-devel
BuildRequires: make
BuildRequires: ncurses-devel
BuildRequires: sqlite-devel
BuildRequires: systemd-devel
BuildRequires: texinfo
BuildRequires: zlib-devel

%if %{with gpm}
BuildRequires: gpm-devel
%endif

%if %{with lucid} || %{with gtkx11}
BuildRequires: libX11-devel
BuildRequires: libXau-devel
BuildRequires: libXdmcp-devel
BuildRequires: libXi-devel
BuildRequires: libXpm-devel
BuildRequires: libXrender-devel
BuildRequires: libXt-devel
BuildRequires: xorg-x11-proto-devel
%endif

%if %{with lucid}
BuildRequires: Xaw3d-devel
%endif

# for Patch3
BuildRequires: pkgconfig(systemd)

%ifarch %{ix86}
BuildRequires: util-linux
%endif

%if "%{_lib}" == "lib64"
%global marker ()(64bit)
%endif

%define site_lisp %{_datadir}/emacs/site-lisp
%define site_start_d %{site_lisp}/site-start.d
%define pkgconfig %{_datadir}/pkgconfig
%define emacs_libexecdir %{_libexecdir}/emacs/%{version}/%{_host}
%define native_lisp %{_libdir}/emacs/%{version}/native-lisp

%global desc %{expand:GNU Emacs is a powerful, customizable, self-documenting, modeless text
editor. It contains special code editing features, a scripting language
(elisp), and the capability to read mail, news, and more without leaving
the editor.
}

Provides:      emacs(bin) = %{epoch}:%{version}-%{release}
Requires:      (emacs-pgtk = %{epoch}:%{version}-%{release} or emacs-gtk+x11 = %{epoch}:%{version}-%{release} or emacs-lucid = %{epoch}:%{version}-%{release} or emacs-nw = %{epoch}:%{version}-%{release})

Suggests:      (emacs-nw if fedora-release-identity-basic)
Suggests:      (emacs-nw if fedora-release-cloud)
Suggests:      (emacs-nw if fedora-release-container)
Suggests:      (emacs-nw if fedora-release-coreos)
Suggests:      (emacs-gtk+x11 if fedora-release-i3)
Suggests:      (emacs-nw if fedora-release-iot)
Suggests:      (emacs-gtk+x11 if fedora-release-matecompiz)
Suggests:      (emacs-pgtk if fedora-release-miraclewm)
Suggests:      (emacs-pgtk if fedora-release-miraclewm-atomic)
Suggests:      (emacs-pgtk if fedora-release-mobility)
Suggests:      (emacs-nw if fedora-release-server)
Suggests:      (emacs-pgtk if fedora-release-silverblue)
Suggests:      (emacs-pgtk if fedora-release-sway)
Suggests:      (emacs-pgtk if fedora-release-sway-atomic)
Suggests:      (emacs-nw if fedora-release-toolbx)
Suggests:      (emacs-pgtk if fedora-release-workstation)
Suggests:      (emacs-gtk+x11 if fedora-release-xfce)

## If you know the best variant for these editions, please fill
## them in.
# Suggests:      (emacs- if fedora-release-budgie)
# Suggests:      (emacs- if fedora-release-budgie-atomic)
# Suggests:      (emacs- if fedora-release-cinnamon)
# Suggests:      (emacs- if fedora-release-compneuro)
# Suggests:      (emacs- if fedora-release-cosmic)
# Suggests:      (emacs- if fedora-release-cosmic-atomic)
# Suggests:      (emacs- if fedora-release-designsuite)
# Suggests:      (emacs- if fedora-release-kde)
# Suggests:      (emacs- if fedora-release-kde-mobile)
# Suggests:      (emacs- if fedora-release-kinoite)
# Suggests:      (emacs- if fedora-release-kinoite-mobile)
# Suggests:      (emacs- if fedora-release-lxqt)
# Suggests:      (emacs- if fedora-release-soas)
# Suggests:      (emacs- if fedora-release-wsl)

%description
%desc


%package pgtk
Summary:       GNU Emacs text editor with GTK toolkit for Wayland

# Emacs doesn't run without a font, rhbz#732422
Requires:      google-noto-sans-mono-vf-fonts

Requires(preun): /usr/sbin/alternatives
Requires(posttrans): /usr/sbin/alternatives
Requires:      emacs-common = %{epoch}:%{version}-%{release}
Requires:      libpixbufloader-xpm.so%{?marker}
Supplements:   ((libwayland-server and emacs) unless emacs-nw)
Obsoletes:     emacs < 1:30.2-4

%description pgtk
%desc
This package provides an emacs-pgtk binary with support for Wayland, using the
GTK toolkit.


%if %{with gtkx11}
%package gtk+x11
Summary:       GNU Emacs text editor with GTK toolkit for X11
Requires:      google-noto-sans-mono-vf-fonts
Requires(preun): /usr/sbin/alternatives
Requires(posttrans): /usr/sbin/alternatives
Requires:      emacs-common = %{epoch}:%{version}-%{release}
Requires:      libpixbufloader-xpm.so%{?marker}
Supplements:   ((xorg-x11-server-Xorg and emacs) unless emacs-nw)

%description gtk+x11
%desc
This package provides an emacs-gtk+x11 binary with support for the X
Window System, using the GTK toolkit.
%endif


%if %{with lucid}
%package lucid
Summary:       GNU Emacs text editor with Lucid toolkit for X11
Requires:      google-noto-sans-mono-vf-fonts
Requires(preun): /usr/sbin/alternatives
Requires(posttrans): /usr/sbin/alternatives
Requires:      emacs-common = %{epoch}:%{version}-%{release}

%description lucid
%desc
This package provides an emacs-lucid binary with support for the X
Window System, using the Lucid toolkit.
%endif


%if %{with nw}
%package nw
Summary:       GNU Emacs text editor with no window system support
Requires(preun): /usr/sbin/alternatives
Requires(posttrans): /usr/sbin/alternatives
Requires:      emacs-common = %{epoch}:%{version}-%{release}
Provides:      emacs-nox = %{epoch}:%{version}-%{release}
Obsoletes:     emacs-nox < 1:30

%description nw
%desc
This package provides an emacs-nw binary without graphical display
support, for running on a terminal only.
%endif


%package -n emacsclient
Summary:       Remotely control GNU Emacs
Conflicts:     emacs-common < 1:29.4-12

%description -n emacsclient
%desc
This package provides emacsclient, which can be used to control an Emacs
server.


%package common
Summary:       Emacs common files
# The entire source code is GPLv3+ except lib-src/etags.c which is
# also BSD.  Manual (info) is GFDL.
License:       GPL-3.0-or-later AND GFDL-1.3-no-invariants-or-later AND BSD-3-Clause
Requires(preun): /usr/sbin/alternatives
Requires(posttrans): /usr/sbin/alternatives
Requires:      /usr/bin/readlink
Requires:      %{name}-filesystem
Requires:      emacsclient
Requires:      libgccjit
Recommends:    emacs = %{epoch}:%{version}-%{release}
Recommends:    enchant2
Recommends:    info
Provides:      %{name}-el = %{epoch}:%{version}-%{release}
Obsoletes:     emacs-el < 1:24.3-29
# transient.el is provided by emacs in lisp/transient.el
Provides:      emacs-transient = 0.7.2.2
# the existing emacs-transient package is obsoleted by emacs 28+, last package
# version as of the release of emacs 28.1 is obsoleted
Obsoletes:     emacs-transient < 0.3.0-4

# We need the following packages for treesit-install-language-grammar to
# be able to build additional parsers for us at runtime:
Recommends:    /usr/bin/git
Recommends:    gcc
Recommends:    (gcc-c++ if libtree-sitter < 0.24.0)

%global _local_file_attrs emacs_lisp
%{load:%SOURCE10}
%global __emacs_lisp_recommends \
        %{_builddir}/%{name}-%{version}/build-pgtk/src/emacs -x %SOURCE11

%description common
%desc
This package contains all the common files needed by emacs, emacs-gtk+x11,
emacs-lucid, or emacs-nw.


%package devel
Summary: Development header files for Emacs

%description devel
Development header files for Emacs.


%prep
cat '%{SOURCE100}' '%{SOURCE101}' '%{SOURCE102}' > keyring
%{gpgverify} --keyring=keyring --signature='%{SOURCE1}' --data='%{SOURCE0}'
rm keyring

%autosetup -N -c
cd %{name}-%{version}
%autopatch -p1

# Avoid trademark issues
rm lisp/play/pong.el lisp/play/pong.elc \
   lisp/play/tetris.el lisp/play/tetris.elc

autoconf

%ifarch %{ix86}
%define setarch setarch %{_arch} -R
%else
%define setarch %{nil}
%endif

# Avoid duplicating doc files in the common subpackage
ln -s ../../%{name}/%{version}/etc/COPYING doc
ln -s ../../%{name}/%{version}/etc/NEWS doc


cd ..
%if %{with lucid}
cp -a %{name}-%{version} build-lucid
%endif
%if %{with nw}
cp -a %{name}-%{version} build-nw
%endif
%if %{with gtkx11}
cp -a %{name}-%{version} build-gtk+x11
%endif
mv %{name}-%{version} build-pgtk


%build
export CFLAGS="-DMAIL_USE_LOCKF %{build_cflags}"
%set_build_flags

%if %{with lucid}
# Build Lucid binary
cd build-lucid
%configure  \
           --disable-gc-mark-trace \
           --program-suffix=-lucid \
           --with-cairo \
           --with-dbus \
           --with-gif \
           --with-gpm=no \
           --with-harfbuzz \
           --with-jpeg \
           --with-modules \
           --with-native-compilation=aot \
           --with-png \
           --with-rsvg \
           --with-sqlite3 \
           --with-tiff \
           --with-tree-sitter \
           --with-webp \
           --with-x-toolkit=lucid \
           --with-xft \
           --with-xinput2 \
           --with-xpm \
    || ( cat config.log && false )
%{setarch} %make_build bootstrap
%{setarch} %make_build
cd ..
%endif

%if %{with nw}
# Build binary without X support
cd build-nw
%configure \
           --disable-gc-mark-trace \
           --program-suffix=-nw \
           --with-modules \
           --with-native-compilation=aot \
           --with-sqlite3 \
           --with-tree-sitter \
%if %{without gpm}
           --with-gpm=no \
%endif
           --with-x=no \
    || ( cat config.log && false )
%{setarch} %make_build bootstrap
%{setarch} %make_build
cd ..
%endif

%if %{with gtkx11}
# Build GTK/X11 binary
cd build-gtk+x11
%configure  \
           --disable-gc-mark-trace \
           --program-suffix=-gtk+x11 \
           --with-cairo \
           --with-dbus \
           --with-gif \
           --with-gpm=no \
           --with-harfbuzz \
           --with-jpeg \
           --with-modules \
           --with-native-compilation=aot \
           --with-png \
           --with-rsvg \
           --with-sqlite3 \
           --with-tiff \
           --with-tree-sitter \
           --with-webp \
           --with-x-toolkit=gtk3 \
           --with-xinput2 \
           --with-xpm \
    || ( cat config.log && false )
%{setarch} %make_build bootstrap
%{setarch} %make_build
cd ..
%endif

# Build pure GTK binary
cd build-pgtk
%configure  \
           --disable-gc-mark-trace \
           --with-cairo \
           --with-dbus \
           --with-gif \
           --with-gpm=no \
           --with-harfbuzz \
           --with-jpeg \
           --with-modules \
           --with-native-compilation=aot \
           --with-pgtk \
           --with-png \
           --with-rsvg \
           --with-sqlite3 \
           --with-tiff \
           --with-tree-sitter \
           --with-webp \
           --with-xpm \
    || ( cat config.log && false )
%{setarch} %make_build bootstrap
%{setarch} %make_build
cd ..

# Create pkgconfig file
cat > emacs.pc << EOF
sitepkglispdir=%{site_lisp}
sitestartdir=%{site_start_d}

Name: emacs
Description: GNU Emacs text editor
Version: %{epoch}:%{version}
EOF

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
%if %{with nw}
cd build-nw
%{__make} install-arch-dep install-eln DESTDIR=%{?buildroot} INSTALL="%{__install} -p"
cd ..
%endif

%if %{with lucid}
cd build-lucid
%{__make} install-arch-dep install-eln DESTDIR=%{?buildroot} INSTALL="%{__install} -p"
cd ..
%endif

%if %{with gtkx11}
cd build-gtk+x11
%{__make} install-arch-dep install-eln DESTDIR=%{?buildroot} INSTALL="%{__install} -p"
cd ..
%endif

cd build-pgtk
%make_install
cd ..

# Do not compress the files which implement compression itself (#484830)
gunzip %{buildroot}%{_datadir}/emacs/%{version}/lisp/jka-compr.el.gz
gunzip %{buildroot}%{_datadir}/emacs/%{version}/lisp/jka-cmpr-hook.el.gz

# Remove duplicate files with suffixed names
%if %{with nw} || %{with lucid} || %{with gtkx11}
find %{buildroot} \
     -type f \
     ! -name emacs-%{version}-gtk+x11 ! -name emacs-gtk+x11 \
     ! -name emacs-%{version}-lucid   ! -name emacs-lucid \
     ! -name emacs-%{version}-nw      ! -name emacs-nw \
     -regextype posix-extended \
     -regex '.*-(gtk\+x11|lucid|nw)((-mail)?\.[^/]+)?$' \
     -print \
     -delete
%endif

# Rename the emacs binary to indicate it's a "pure GTK" build
mv %{buildroot}%{_bindir}/emacs-%{version} %{buildroot}%{_bindir}/emacs-%{version}-pgtk
ln -s emacs-%{version}-pgtk %{buildroot}%{_bindir}/emacs-pgtk

# Compatibility with earlier Fedora packages
%if %{with nw}
ln -s emacs-%{version}-nw %{buildroot}%{_bindir}/emacs-%{version}-nox
ln -s emacs-%{version}-nw %{buildroot}%{_bindir}/emacs-nox
%endif

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

# Install rpm macros
mkdir -p \
      %{buildroot}%{_fileattrsdir} \
      %{buildroot}%{_rpmconfigdir} \
      %{buildroot}%{_rpmmacrodir}
install -p -m 0644 %SOURCE10 %{buildroot}%{_fileattrsdir}
install -p -m 0755 %SOURCE11 %{buildroot}%{_rpmconfigdir}
install -p -m 0644 macros.emacs %{buildroot}%{_rpmmacrodir}

# After everything is installed, remove info dir
rm -f %{buildroot}%{_infodir}/dir

# Install a wrapper to avoid running the Wayland-only build on X11
install -p -m 0755 %SOURCE9 %{buildroot}%{_bindir}/emacs-desktop

# Remove duplicate desktop-related files
rm %{buildroot}%{_datadir}/%{name}/%{version}/etc/%{name}.{desktop,metainfo.xml,service} \
   %{buildroot}%{_datadir}/%{name}/%{version}/etc/%{name}-mail.desktop \
   %{buildroot}%{_datadir}/%{name}/%{version}/etc/org.gnu.emacs.defaults.gschema.xml

# We don't ship the client variants yet
# https://src.fedoraproject.org/rpms/emacs/pull-request/12
rm %{buildroot}%{_datadir}/applications/emacsclient.desktop
rm %{buildroot}%{_datadir}/applications/emacsclient-mail.desktop

#
# Create file lists
#
rm -f *-filelist {common,el}-*-files

( TOPDIR=${PWD}
  cd %{buildroot}

  find .%{_datadir}/emacs/%{version}/lisp .%{site_lisp} \
    \( -type f -name '*.elc' -fprint $TOPDIR/common-lisp-none-elc-files \) -o \( -type d -fprintf $TOPDIR/common-lisp-dir-files "%%%%dir %%p\n" \) -o \( -name '*.el.gz' -fprint $TOPDIR/el-bytecomped-files -o -fprint $TOPDIR/common-not-comped-files \)

)

# Sorted list of info files
%define info_files auth autotype bovine calc ccmode cl dbus dired-x ebrowse ede ediff edt efaq eglot eieio eintr elisp emacs-gnutls emacs-mime emacs epa erc ert eshell eudc eww flymake forms gnus htmlfontify idlwave ido mairix-el message mh-e modus-themes newsticker nxml-mode octave-mode org pcl-cvs pgg rcirc reftex remember sasl sc semantic ses sieve smtpmail speedbar srecode todo-mode tramp transient url use-package vhdl-mode vip viper vtable widget wisent woman

for info_f in %info_files; do
    echo "%{_infodir}/${info_f}.info*" >> info-filelist
done
# info.gz is a rename of info.info.gz and thus needs special handling
echo "%{_infodir}/info*" >> info-filelist
# elisp.info.gz has additional files
echo "%{_infodir}/elisp_type_hierarchy*" >> info-filelist

# Put the lists together after filtering  ./usr to /usr
sed -i -e "s|\.%{_prefix}|%{_prefix}|" *-files
grep -vhE '%{site_lisp}(|/(default\.el|site-start\.d|site-start\.el))$' {common,el}-*-files > common-filelist

# Remove old icon
rm %{buildroot}%{_datadir}/icons/hicolor/scalable/mimetypes/emacs-document23.svg

# Install native compiled Lisp of all builds
(TOPDIR=${PWD}
 cd %{buildroot}
 find ".%{native_lisp}/$(ls $TOPDIR/build-pgtk/native-lisp)" \
      \( -type f -name '*eln' -fprintf "$TOPDIR/pgtk-filelist" "%%%%attr(755,-,-) %%p\n" \) \
      -o \( -type d -fprintf "$TOPDIR/pgtk-dirlist" "%%%%dir %%p\n" \)
)
echo "%{emacs_libexecdir}/emacs-$(./build-pgtk/src/emacs --fingerprint).pdmp" \
     >> pgtk-filelist

%if %{with gtkx11}
(TOPDIR=${PWD}
 cd %{buildroot}
 find ".%{native_lisp}/$(ls $TOPDIR/build-gtk+x11/native-lisp)" \
      \( -type f -name '*eln' -fprintf "$TOPDIR/gtk+x11-filelist" "%%%%attr(755,-,-) %%p\n" \) \
      -o \( -type d -fprintf "$TOPDIR/gtk+x11-dirlist" "%%%%dir %%p\n" \)
)
echo "%{emacs_libexecdir}/emacs-$(./build-gtk+x11/src/emacs --fingerprint).pdmp" \
     >> gtk+x11-filelist
%endif

%if %{with lucid}
(TOPDIR=${PWD}
 cd %{buildroot}
 find ".%{native_lisp}/$(ls $TOPDIR/build-lucid/native-lisp)" \
      \( -type f -name '*eln' -fprintf "$TOPDIR/lucid-filelist" "%%%%attr(755,-,-) %%p\n" \) \
      -o \( -type d -fprintf "$TOPDIR/lucid-dirlist" "%%%%dir %%p\n" \)
)
echo "%{emacs_libexecdir}/emacs-$(./build-lucid/src/emacs --fingerprint).pdmp" \
     >> lucid-filelist
%endif

%if %{with nw}
(TOPDIR=${PWD}
 cd %{buildroot}
 find ".%{native_lisp}/$(ls $TOPDIR/build-nw/native-lisp)" \
      \( -type f -name '*eln' -fprintf "$TOPDIR/nw-filelist" "%%%%attr(755,-,-) %%p\n" \) \
      -o \( -type d -fprintf "$TOPDIR/nw-dirlist" "%%%%dir %%p\n" \)
)
echo "%{emacs_libexecdir}/emacs-$(./build-nw/src/emacs --fingerprint).pdmp" \
     >> nw-filelist
%endif

# remove leading . from filelists
sed -i -e "s|\.%{native_lisp}|%{native_lisp}|" *-filelist *-dirlist

# remove exec permissions from eln files to prevent the debuginfo extractor from
# trying to extract debuginfo from them
find %{buildroot}%{native_lisp}/ -name '*.eln' -type f -print0 \
    | xargs -0 chmod -x

# ensure native files are newer than byte-code files
# see: https://bugzilla.redhat.com/show_bug.cgi?id=2157979#c11
find %{buildroot}%{native_lisp}/ -name '*.eln' -type f -print0 \
    | xargs -0 touch

export QA_SKIP_BUILD_ROOT=0


%check
appstream-util validate-relax --nonet %{buildroot}/%{_metainfodir}/*.metainfo.xml
desktop-file-validate %{buildroot}/%{_datadir}/applications/*.desktop


%preun pgtk
if [ $1 = 0 ]; then
  /usr/sbin/alternatives --remove emacs %{_bindir}/emacs-desktop || :
  /usr/sbin/alternatives --remove emacs %{_bindir}/emacs-pgtk || :
fi

%posttrans pgtk
/usr/sbin/alternatives --install %{_bindir}/emacs emacs %{_bindir}/emacs-desktop 85 || :
/usr/sbin/alternatives --install %{_bindir}/emacs emacs %{_bindir}/emacs-pgtk 80 || :

%if %{with lucid}
%preun lucid
if [ $1 = 0 ]; then
  /usr/sbin/alternatives --remove emacs %{_bindir}/emacs-lucid || :
fi

%posttrans lucid
/usr/sbin/alternatives --install %{_bindir}/emacs emacs %{_bindir}/emacs-lucid 70 || :
# The preun scriptlet of packages before 29.4-5 will remove this symlink
# after it has been installed, so we may need to put it back:
if [ $1 = 2 -a ! -h %{_bindir}/emacs-lucid ]; then
    ln -s emacs-%{version}-lucid %{_bindir}/emacs-lucid
fi
%endif

%if %{with gtkx11}
%preun gtk+x11
if [ $1 = 0 ]; then
  /usr/sbin/alternatives --remove emacs %{_bindir}/emacs-gtk+x11 || :
fi

%posttrans gtk+x11
/usr/sbin/alternatives --install %{_bindir}/emacs emacs %{_bindir}/emacs-gtk+x11 75 || :
# The preun scriptlet of packages before 29.4-5 will remove this symlink
# after it has been installed, so we may need to put it back:
if [ $1 = 2 -a ! -h %{_bindir}/emacs-gtk+x11 ]; then
    ln -s emacs-%{version}-gtk+x11 %{_bindir}/emacs-gtk+x11
fi
%endif

%if %{with nw}
%preun nw
if [ $1 = 0 ]; then
  /usr/sbin/alternatives --remove emacs %{_bindir}/emacs-nw || :
fi

%posttrans nw
/usr/sbin/alternatives --install %{_bindir}/emacs emacs %{_bindir}/emacs-nw 65 || :
# The preun scriptlet of packages before 29.4-5 will remove this symlink
# after it has been installed, so we may need to put it back:
if [ $1 = 2 -a ! -h %{_bindir}/emacs-nw ]; then
    ln -s emacs-%{version}-nw %{_bindir}/emacs-nw
fi
%endif

%preun common
if [ $1 = 0 ]; then
  /usr/sbin/alternatives --remove emacs.etags %{_bindir}/etags.emacs || :
fi

%posttrans common
/usr/sbin/alternatives --install %{_bindir}/etags emacs.etags %{_bindir}/etags.emacs 80 \
       --slave %{_mandir}/man1/etags.1.gz emacs.etags.man %{_mandir}/man1/etags.emacs.1.gz || :


%files

%files pgtk -f pgtk-filelist -f pgtk-dirlist
%ghost %{_bindir}/emacs
%{_bindir}/emacs-desktop
%{_bindir}/emacs-%{version}-pgtk
%{_bindir}/emacs-pgtk
%{_datadir}/glib-2.0/schemas/org.gnu.emacs.defaults.gschema.xml

%if %{with gtkx11}
%files gtk+x11 -f gtk+x11-filelist -f gtk+x11-dirlist
%ghost %{_bindir}/emacs
%{_bindir}/emacs-%{version}-gtk+x11
%{_bindir}/emacs-gtk+x11
%endif

%if %{with lucid}
%files lucid -f lucid-filelist -f lucid-dirlist
%ghost %{_bindir}/emacs
%{_bindir}/emacs-%{version}-lucid
%{_bindir}/emacs-lucid
%endif

%if %{with nw}
%files nw -f nw-filelist -f nw-dirlist
%ghost %{_bindir}/emacs
%{_bindir}/emacs-%{version}-nox
%{_bindir}/emacs-%{version}-nw
%{_bindir}/emacs-nox
%{_bindir}/emacs-nw
%endif

%files -n emacsclient
%license build-pgtk/etc/COPYING
%{_bindir}/emacsclient
%{_mandir}/man1/emacsclient.1*

%files common -f common-filelist -f info-filelist
%config(noreplace) %{_sysconfdir}/skel/.emacs
%{_fileattrsdir}/emacs_lisp.attr
%{_rpmconfigdir}/emacs_lisp.rec
%{_rpmconfigdir}/macros.d/macros.emacs
%license build-pgtk/etc/COPYING
%doc build-pgtk/doc/NEWS build-pgtk/BUGS build-pgtk/README
%{_bindir}/ebrowse
%ghost %{_bindir}/etags
%{_bindir}/etags.emacs
%{_bindir}/gctags
%{_datadir}/applications/emacs.desktop
%{_datadir}/applications/emacs-mail.desktop
%{_metainfodir}/%{name}.metainfo.xml
%{_datadir}/icons/hicolor/*/apps/emacs.png
%{_datadir}/icons/hicolor/scalable/apps/emacs.svg
%{_datadir}/icons/hicolor/scalable/apps/emacs.ico
%{_datadir}/icons/hicolor/scalable/mimetypes/emacs-document.svg
%{_mandir}/man1/ebrowse.1*
%{_mandir}/man1/emacs.1*
%{_mandir}/man1/etags.emacs.1*
%ghost %{_mandir}/man1/etags.1.gz
%{_mandir}/man1/gctags.1*
%dir %{_datadir}/emacs/%{version}
%{_datadir}/emacs/%{version}/etc
%{_datadir}/emacs/%{version}/site-lisp
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/%{version}
%dir %{native_lisp}
%dir %{_libexecdir}/emacs
%dir %{_libexecdir}/emacs/%{version}
%dir %{emacs_libexecdir}
%{emacs_libexecdir}/movemail
%{emacs_libexecdir}/hexl
%{emacs_libexecdir}/rcs2log
%{_userunitdir}/emacs.service
%attr(0644,root,root) %config(noreplace) %{site_lisp}/default.el
%attr(0644,root,root) %config %{site_lisp}/site-start.el
%{pkgconfig}/emacs.pc


%files devel
%{_includedir}/emacs-module.h

%changelog
## START: Generated by rpmautospec
* Wed Apr 22 2026 azldev <azurelinux@microsoft.com> - 1:30.2-7
- Latest state for emacs

* Fri Nov 14 2025 Peter Oliver <git@mavit.org.uk> - 1:30.2-6
- Glob doesn’t work with the %%ghost macro

* Fri Nov 14 2025 Peter Oliver <git@mavit.org.uk> - 1:30.2-5
- Own etags and man page (rhbz#2414055).

* Fri Oct 24 2025 Peter Oliver <git@mavit.org.uk> - 1:30.2-4
- Bump release until F43 overtakes F41.

* Fri Oct 24 2025 Peter Oliver <git@mavit.org.uk> - 1:30.2-3
- Bump release until F43 overtakes F41.

* Fri Oct 24 2025 Peter Oliver <git@mavit.org.uk> - 1:30.2-2
- Ensure on upgrade from F42/F41 that emacs-pgtk replaces emacs
  (rhbz#2406058)

* Fri Aug 15 2025 Peter Oliver <git@mavit.org.uk> - 1:30.2-1
- Update to version 30.2, fixing rhbz#2388544

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:30.1-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 22 2025 Peter Oliver <git@mavit.org.uk> - 1:30.1-33
- Fix typo.

* Mon Jul 21 2025 Peter Oliver <git@mavit.org.uk> - 1:30.1-32
- Suggest emacs-nw for emacs within mock.

* Fri Jul 18 2025 Peter Oliver <git@mavit.org.uk> - 1:30.1-31
- Dependency generator: look for absolute symlinks in $RPM_BUILD_ROOT

* Fri Jul 18 2025 Peter Oliver <git@mavit.org.uk> - 1:30.1-30
- Dependency generator: ensure error messages are sent to stderr only.

* Fri Jul 18 2025 Peter Oliver <git@mavit.org.uk> - 1:30.1-29
- RPMAUTOSPEC: unresolvable merge
## END: Generated by rpmautospec
