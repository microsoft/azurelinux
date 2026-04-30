## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
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
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 1:30.2-7
- test: add initial lock files

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
- Merge branch 'pr46' into rawhide, fixing indentation.

* Fri Jul 18 2025 Peter Oliver <git@mavit.org.uk> - 1:30.1-28
- Rebuild against tree-sitter-0.25.8-1.fc43

* Mon Jun 16 2025 Peter Oliver <git@mavit.org.uk> - 1:30.1-27
- Package emacsclient should conflict with the last F40 emacs-common.

* Sun Jun 15 2025 Peter Oliver <git@mavit.org.uk> - 1:30.1-26
- Fix pretest version detection.

* Sun Jun 15 2025 Peter Oliver <git@mavit.org.uk> - 1:30.1-25
- Restore compatibility with recent Tree-sitter parsers.

* Fri Jun 13 2025 Peter Oliver <git@mavit.org.uk> - 1:30.1-24
- Rebuild against tree-sitter-0.25.6-1.fc43

* Wed May 28 2025 Peter Oliver <git@mavit.org.uk> - 1:30.1-23
- Rebuild against tree-sitter-0.25.5-1.fc43

* Mon May 12 2025 Peter Oliver <git@mavit.org.uk> - 1:30.1-22
- Rebuild against tree-sitter-0.25.4-3.fc43

* Thu Apr 24 2025 Peter Oliver <git@mavit.org.uk> - 1:30.1-21
- Emacs 31 compatibility for Tree-sitter Recommends generation.

* Mon Apr 14 2025 Peter Oliver <git@mavit.org.uk> - 1:30.1-20
- Rebuild against tree-sitter-0.25.3-1.fc43

* Tue Apr 08 2025 Peter Oliver <git@mavit.org.uk> - 1:30.1-19
- Fix compilation errors due to insufficient compiler safety

* Tue Mar 25 2025 Peter Oliver <git@mavit.org.uk> - 1:30.1-18
- Suggest an Emacs build based on Fedora edition.

* Tue Mar 25 2025 Peter Oliver <git@mavit.org.uk> - 1:30.1-17
- Now there is no emacs subpackage, all emacs(bin) providers can provide
  it.

* Tue Mar 25 2025 Peter Oliver <git@mavit.org.uk> - 1:30.1-16
- Drop emacs-terminal subpackage again

* Tue Mar 25 2025 Peter Oliver <git@mavit.org.uk> - 1:30.1-15
- Rename emacs subpackage to emacs-pgtk

* Wed Mar 19 2025 Peter Oliver <git@mavit.org.uk> - 1:30.1-14
- Move emacs-desktop wrapper into emacs package

* Tue Mar 18 2025 Peter Oliver <git@mavit.org.uk> - 1:30.1-13
- Ensure desktop icon is found

* Mon Mar 17 2025 Peter Oliver <git@mavit.org.uk> - 1:30.1-12
- Offer emacs-desktop as the highest priority alternative for emacs

* Sun Mar 16 2025 Peter Oliver <git@mavit.org.uk> - 1:30.1-11
- Lower alternatives priority of emacs-nw

* Thu Mar 13 2025 Peter Oliver <git@mavit.org.uk> - 1:30.1-10
- Tidy up Recommends of emacs-common.

* Thu Mar 13 2025 Peter Oliver <git@mavit.org.uk> - 1:30.1-9
- Restore emacs-terminal subpackage

* Thu Mar 13 2025 Peter Oliver <git@mavit.org.uk> - 1:30.1-8
- Correct provided emacs-transient version.

* Fri Mar 07 2025 Peter Oliver <git@mavit.org.uk> - 1:30.1-7
- Automatically generate Recommends for Tree-sitter parsers.

* Fri Mar 07 2025 Peter Oliver <git@mavit.org.uk> - 1:30.1-6
- Drop recommendation of gcc-c++ for newer Tree-sitter versions

* Thu Feb 27 2025 Peter Oliver <git@mavit.org.uk> - 1:30.1-5
- Stricter matching of native-compiled lisp files.

* Thu Feb 27 2025 Peter Oliver <git@mavit.org.uk> - 1:30.1-4
- Avoid duplicating native lisp across subpackages.

* Tue Feb 25 2025 Peter Oliver <git@mavit.org.uk> - 1:30.1-3
- Abandon checks

* Tue Feb 25 2025 Peter Oliver <git@mavit.org.uk> - 1:30.1-2
- Rebuild against tree-sitter-0.25.2-5.fc42

* Mon Feb 24 2025 Peter Oliver <git@mavit.org.uk> - 1:30.1-1
- Update to version 30.1.

* Mon Feb 24 2025 Peter Oliver <git@mavit.org.uk> - 1:30.0.93-2
- Disable GC mark trace buffer for about 5%% better GC performance.

* Mon Feb 24 2025 Peter Oliver <git@mavit.org.uk> - 1:30.0.93-1
- Update to version 30.0.93.

* Mon Feb 24 2025 Peter Oliver <git@mavit.org.uk> - 1:30.0.92-1
- Update to version 30.0.92.

* Mon Feb 24 2025 Bhavin Gandhi <bhavin7392@gmail.com> - 1:30.0.91-3
- Elisp info has new image and a text file

* Mon Feb 24 2025 Bhavin Gandhi <bhavin7392@gmail.com> - 1:30.0.91-2
- Fix for failing uniquify-tests

* Mon Feb 24 2025 Peter Oliver <git@mavit.org.uk> - 1:30.0.91-1
- Update to version 30.0.91.

* Thu Feb 20 2025 Tom spot Callaway <spotaws@amazon.com> - 1:29.4-53
- rebuild for tree-sitter

* Wed Feb 19 2025 Peter Oliver <git@mavit.org.uk> - 1:29.4-52
- Rebuild against tree-sitter-0.25.2-3.fc43

* Mon Feb 03 2025 Peter Oliver <git@mavit.org.uk> - 1:29.4-51
- Rebuild against tree-sitter-0.25.1-5.fc42

* Mon Feb 03 2025 Peter Oliver <git@mavit.org.uk> - 1:29.4-50
- Rebuild against tree-sitter-0.25.1-3.fc42

* Fri Jan 17 2025 Peter Oliver <git@mavit.org.uk> - 1:29.4-49
- Debug configure failures.

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:29.4-48
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jan 15 2025 Jens Petersen <petersen@redhat.com> - 1:29.4-47
- rebuild rawhide against tree-sitter-0.24

* Fri Jan 03 2025 Peter Oliver <git@mavit.org.uk> - 1:29.4-46
- Require XPM pixbuf loader for GTK builds (#2335309)

* Thu Oct 31 2024 Peter Oliver <git@mavit.org.uk> - 1:29.4-45
- Fix typo in emacs-gtk+x11 Requires.

* Thu Oct 31 2024 Peter Oliver <git@mavit.org.uk> - 1:29.4-44
- Drop emacs-terminal subpackage

* Thu Oct 31 2024 Peter Oliver <git@mavit.org.uk> - 1:29.4-43
- Isolate builds from each other

* Thu Oct 31 2024 Peter Oliver <git@mavit.org.uk> - 1:29.4-42
- Prefer `make install` to our own approximations.

* Thu Oct 31 2024 Peter Oliver <git@mavit.org.uk> - 1:29.4-41
- Skip unstable test mml-secure-find-usable-keys-2.

* Wed Oct 30 2024 Peter Oliver <git@mavit.org.uk> - 1:29.4-40
- Skip unstable test mml-secure-select-preferred-keys-2.

* Tue Oct 22 2024 Richard W.M. Jones <rjones@redhat.com> - 1:29.4-39
- Rebuild for Jansson 2.14 (https://lists.fedoraproject.org/archives/list/d
  evel@lists.fedoraproject.org/thread/3PYINSQGKQ4BB25NQUI2A2UCGGLAG5ND/)

* Wed Oct 09 2024 Peter Oliver <git@mavit.org.uk> - 1:29.4-38
- Skip unstable test mml-secure-key-checks.

* Wed Oct 09 2024 Peter Oliver <git@mavit.org.uk> - 1:29.4-37
- Don’t pull in GUI builds if emacs-nw is installed (#2273786).

* Thu Oct 03 2024 Peter Oliver <git@mavit.org.uk> - 1:29.4-36
- RPM git-core is sufficient for fetching Tree-sitter grammar source
  (#2316238)

* Thu Sep 26 2024 Peter Oliver <git@mavit.org.uk> - 1:29.4-35
- Don’t mention removed games in menus or documentation.

* Tue Sep 24 2024 Peter Oliver <git@mavit.org.uk> - 1:29.4-34
- Rebuild against tree-sitter-0.23.0-2.fc41.

* Sun Sep 22 2024 Peter Oliver <git@mavit.org.uk> - 1:29.4-33
- Fix typo.

* Sun Sep 22 2024 Peter Oliver <git@mavit.org.uk> - 1:29.4-32
- Drop WebKit, since recent versions are incompatible with Emacs

* Wed Aug 28 2024 Peter Oliver <git@mavit.org.uk> - 1:29.4-31
- Relax libtree-sitter requirement.

* Thu Aug 22 2024 Jacek Migacz <jmigacz@redhat.com> - 1:29.4-30
- Unset custom linker flags

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:29.4-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jul 17 2024 Peter Oliver <git@mavit.org.uk> - 1:29.4-28
- More test stabilisation.

* Tue Jul 16 2024 Peter Oliver <git@mavit.org.uk> - 1:29.4-27
- Try harder to stabalise dired-test-bug27243-02

* Tue Jul 16 2024 Peter Oliver <git@mavit.org.uk> - 1:29.4-26
- Skip another unstable test.

* Tue Jul 16 2024 Peter Oliver <git@mavit.org.uk> - 1:29.4-25
- Builds on i686 are working again.

* Mon Jul 15 2024 Peter Oliver <git@mavit.org.uk> - 1:29.4-24
- Skip intermittently failing tests.

* Mon Jul 15 2024 Peter Oliver <git@mavit.org.uk> - 1:29.4-23
- Fix another intermittent test failure.

* Sun Jul 14 2024 Peter Oliver <git@mavit.org.uk> - 1:29.4-22
- Fall back to the terminal from pure GTK when no display is available

* Fri Jul 12 2024 Peter Oliver <git@mavit.org.uk> - 1:29.4-21
- Fix typos.

* Fri Jul 12 2024 Peter Oliver <git@mavit.org.uk> - 1:29.4-20
- Fix intermittently failing test wdired-test-unfinished-edit-01.

* Fri Jul 12 2024 Peter Oliver <git@mavit.org.uk> - 1:29.4-19
- Drop i686, which is currently failing to build.

* Thu Jul 11 2024 Peter Oliver <git@mavit.org.uk> - 1:29.4-18
- Restore former alternatives symlinks, if they are missing

* Thu Jul 11 2024 Peter Oliver <git@mavit.org.uk> - 1:29.4-17
- Skip tests that are unstable when run on GNU EMBA

* Thu Jul 11 2024 Peter Oliver <git@mavit.org.uk> - 1:29.4-16
- Emacs’ -*- line has to come first.

* Thu Jul 11 2024 Peter Oliver <git@mavit.org.uk> - 1:29.4-15
- Patches no-longer require numbering.

* Thu Jul 11 2024 Peter Oliver <git@mavit.org.uk> - 1:29.4-14
- Don’t explicitly specify a hardened build, since that’s now default.

* Thu Jul 11 2024 Peter Oliver <git@mavit.org.uk> - 1:29.4-13
- Don’t pacakge duplicate desktop-related files.

* Thu Jul 11 2024 Peter Oliver <git@mavit.org.uk> - 1:29.4-12
- Gitignore more temporary packaging-related files.

* Thu Jul 11 2024 Peter Oliver <git@mavit.org.uk> - 1:29.4-11
- Own unowned directories.

* Wed Jul 10 2024 Peter Oliver <git@mavit.org.uk> - 1:29.4-10
- Fix another failing test.

* Mon Jul 08 2024 Peter Oliver <git@mavit.org.uk> - 1:29.4-9
- Conditionalise build of alternative binaries

* Mon Jul 08 2024 Peter Oliver <git@mavit.org.uk> - 1:29.4-8
- Run tests.

* Mon Jul 08 2024 Peter Oliver <git@mavit.org.uk> - 1:29.4-7
- Add missing symlink to package.

* Wed Jul 03 2024 Peter Oliver <git@mavit.org.uk> - 1:29.4-6
- Reduce use of alternatives

* Tue Jul 02 2024 Peter Oliver <git@mavit.org.uk> - 1:29.4-5
- Add Missing Requires for emacs-desktop wrapper

* Tue Jul 02 2024 Peter Oliver <git@mavit.org.uk> - 1:29.4-4
- Conflicts of emacsclient should reflect emacs-common in F40.

* Sun Jun 23 2024 Peter Oliver <git@mavit.org.uk> - 1:29.4-3
- Remember to commit key.

* Sun Jun 23 2024 Peter Oliver <git@mavit.org.uk> - 1:29.4-2
- Emacs 29.4 tarball is signed by Stefan Kangas, not Eli Zaretskii.

* Sun Jun 23 2024 Peter Oliver <git@mavit.org.uk> - 1:29.4-1
- Update to version 29.4.

* Sat Apr 27 2024 Peter Oliver <git@mavit.org.uk> - 1:29.3-10
- Tweak subpackage summaries and descriptions.

* Sat Apr 27 2024 Peter Oliver <git@mavit.org.uk> - 1:29.3-9
- Split emacsclient into a package that can be installed independently

* Fri Apr 26 2024 Peter Oliver <git@mavit.org.uk> - 1:29.3-8
- Rebuild Emacs, fixing Tree-sitter crash #2277250.

* Tue Apr 23 2024 Pavol Žáčik <pzacik@redhat.com> - 1:29.3-7
- Remove liblockfile dependency

* Tue Apr 09 2024 Peter Oliver <git@mavit.org.uk> - 1:29.3-6
- Split emacs-filesystem into a separate source package.

* Tue Apr 09 2024 Peter Oliver <git@mavit.org.uk> - 1:29.3-5
- Don’t assume a prerelease Emacs version in emacs-desktop

* Mon Apr 08 2024 Peter Oliver <git@mavit.org.uk> - 1:29.3-4
- Use HTTPS for URL.

* Fri Apr 05 2024 Peter Oliver <git@mavit.org.uk> - 1:29.3-3
- Require any emacs-filesystem

* Wed Apr 03 2024 Peter Oliver <git@mavit.org.uk> - 1:29.3-2
- Obsolete the newer emacs-nox now in F39, fixing system upgrades

* Mon Mar 25 2024 Dan Čermák <dan.cermak@cgc-instruments.com> - 1:29.3-1
- New upstream release 29.3, fixes rhbz#2271287

* Tue Feb 06 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 1:29.2-4
- Disable gpm on ELN

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:29.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Peter Oliver <git@mavit.org.uk> - 1:29.2-2
- Remember to update sources.

* Mon Jan 22 2024 Peter Oliver <git@mavit.org.uk> - 1:29.2-1
- Update to version 29.2

* Mon Jan 22 2024 Peter Oliver <mavit@fedoraproject.org> - 1:29.1-17
- Merge #37 `Add -W option to %%_emacs_bytecompile`

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:29.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 05 2024 Lukáš Zaoral <lzaoral@redhat.com> - 1:29.1-15
- use correct BuildRequires for SQLite support

* Sun Nov 19 2023 Peter Oliver <git@mavit.org.uk> - 1:29.1-14
- Recommend libtree-sitter-java.

* Tue Nov 07 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 1:29.1-13
- Fix alternatives dependencies

* Sat Oct 21 2023 Peter Oliver <git@mavit.org.uk> - 1:29.1-12
- Fix typo.

* Sat Oct 21 2023 Peter Oliver <git@mavit.org.uk> - 1:29.1-11
- Fix typo.

* Sat Oct 21 2023 Peter Oliver <git@mavit.org.uk> - 1:29.1-10
- Merge remote-tracking branch 'yselkowitz/rawhide' into rawhide

* Mon Sep 25 2023 Peter Oliver <git@mavit.org.uk> - 1:29.1-9
- Rename emacs-nox subpackage to emacs-nw

* Mon Sep 25 2023 Peter Oliver <git@mavit.org.uk> - 1:29.1-8
- Switch the default `emacs` binary to pure-GTK, suitable for Wayland

* Sun Sep 24 2023 Peter Oliver <git@mavit.org.uk> - 1:29.1-7
- Consolidate more files and requirements into the common subpackage

* Fri Apr 14 2023 Peter Oliver <rpm@mavit.org.uk> - 1:28.2-5
- Eliminate "file listed twice" warings during RPM build.

* Sun Aug  6 2023 Peter Oliver <rpm@mavit.org.uk> - 1:29.1-2
- Enable new features in Emacs 29: SQLite, Tree-sitter, WEBP, XInput 2.

* Mon Jul 31 2023 Dan Čermák <dan.cermak@cgc-instruments.com> - 1:29.1-1
- New upstream release 29.1, fixes rhbz#2227492

* Tue Jul 25 2023 Scott Talbert <swt@techie.net> - 1:28.2-10
- Rebuild for libotf soname bump

* Sat Jul 22 2023 Benson Muite <benson_muite@emailplus.org> - 1:28.2-9
- Add entry for change made by jthat (Fedora fas) to fix typo
  play/pong.el to play/pong.elc

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:28.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed May 31 2023 Benson Muite <benson_muite@emailplus.org> 1:28.2-7
- Apply patch to prevent infinite loops when editing python files
  fixes rhbz#2187041

* Mon Apr 24 2023 Lukáš Zaoral <lzaoral@redhat.com> - 1:28.2-6
- migrate to SPDX license format

* Fri Feb 10 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 1:28.2-5
- Use webkit2gtk-4.1

* Fri Jan 27 2023 Dan Čermák <dan.cermak@cgc-instruments.com> - 1:28.2-4
- Ensure that emacs-nox loads the correct eln files

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:28.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jan 17 2023 Dan Čermák <dan.cermak@cgc-instruments.com> - 1:28.2-2
- Don't include everything in %%emacs_libexecdir in common subpackage, fixes rhbz#2160550
- Don't remove exec permissions from eln files, fixes rhbz#2160547

* Tue Nov  1 2022 Dan Čermák <dan.cermak@cgc-instruments.com> - 1:28.2-1
- New upstream release 28.2, fixes rhbz#2126048
- Add patch to fix CVE-2022-45939, fixes rhbz#2149381
- spawn native-compilation processes with -Q rhbz#2155824 (petersen)

* Fri Dec 23 2022 Florian Weimer <fweimer@redhat.com> - 1:28.1-4
- C99 compatibility fixes for the configure script

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:28.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jul 14 2022 Dan Čermák <dan.cermak@cgc-instruments.com> - 1:28.1-2
- Obsolete emacs-transient to prevent update issues, fixes rhbz#2107269

* Mon Apr  4 2022 Bhavin Gandhi <bhavin7392@gmail.com> - 1:28.1-1
- emacs-28.1 is available, fixes rhbz#2071638
- Build with Native Compilation support and natively compile all .el files
- Use upstream app data file
- Use pdmp files with fingerprints

* Wed Mar 23 2022 Dan Čermák <dan.cermak@cgc-instruments.com> - 1:27.2-11
- Include upstream version of bundled glib cdefs.h, fixes rhbz#2045136

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:27.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Aug  7 2021 Dan Čermák <dan.cermak@cgc-instruments.com> - 1:27.2-9
- Add Requires: info to fix info-mode
- Fixes rhbz#1989264

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:27.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun Jul 11 2021 Dan Čermák <dan.cermak@cgc-instruments.com> - 1:27.2-7
- Add patch to fix pdump page size incompatibility
- Fixes rhbz#1974244

* Sun Jun 13 2021 Dan Čermák <dan.cermak@cgc-instruments.com> - 1:27.2-6
- Swallow %%preun and %%posttrans scriptlet exit status
- Fixes rhbz#1962181

* Sat Jun  5 2021 Peter Oliver <rpm@mavit.org.uk> - 1:27.2-5
- Validate AppStream metainfo.

* Tue May 25 2021 Peter Oliver <rpm@mavit.org.uk> - 1:27.2-4
- Prefer upstream emacs.desktop.
- Remove duplicate emacs.desktop from /usr/share/emacs/27.2/etc/.

* Mon Apr 26 2021 Dan Čermák <dan.cermak@cgc-instruments.com> - 1:27.2-3
- Add emacs-modula2.patch
- Fixes rhbz#1950158

* Sat Mar 27 2021 Peter Oliver <rpm@mavit.org.uk> - 1:27.2-2
- Prefer upstream systemd service definition.

* Sat Mar 27 2021 Scott Talbert <swt@techie.net> - 1:27.1-5
- Fix FTBFS with glibc 2.34

* Thu Mar 25 2021 Bhavin Gandhi <bhavin7392@gmail.com> - 1:27.2-1
- emacs-27.2 is available

* Fri Feb 05 2021 Peter Oliver <rpm@mavit.org.uk> - 1:27.1-4
- Make Enchant the default for ispell-program-name when available.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:27.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Aug 18 2020 Jan Synáček <jsynacek@redhat.com> - 1:27.1-2
- use make macros (original patch provided by Tom Stellard)
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Tue Aug 11 2020 Bhavin Gandhi <bhavin7392@gmail.com> - 1:27.1-1
- emacs-27.1 is available (#1867841)
- Add systemd-devel to support Type=notify in unit file
- Build with Cairo and Jansson support
- Remove ImageMagick dependency as it's no longer used

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:26.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

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

## END: Generated by rpmautospec
