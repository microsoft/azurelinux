# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond_without gui


%if 0%{?fedora}
%bcond_without default_editor
%bcond_without gpm
%bcond_without libsodium_crypt
%else
%bcond_with default_editor
%bcond_with gpm
%bcond_with libsodium_crypt
%endif


%define patchlevel 2146
%define withnetbeans 1

%define withhunspell 0
%define withlua 1
%define withperl 1

# VIm upstream wants to build with FORTIFY_SOURCE=1,
# because higher levels causes crashes of valid code constructs
# and their reimplementation would cost unnecessary maintenance
# https://github.com/vim/vim/pull/3507
%define _fortify_level 1

%define baseversion 9.1
%define vimdir vim91


%if %{?WITH_SELINUX:0}%{!?WITH_SELINUX:1}
%define WITH_SELINUX 1
%endif

%if %{with gui}
%define desktop_file 1
%else
%define desktop_file 0
%endif

%if %{desktop_file}
%define desktop_file_utils_version 0.2.93
%endif

%if 0%{?flatpak}
%define withruby 0
%else
%define withruby 1
%endif


Summary: The VIM editor
URL:     https://www.vim.org/
Name: vim
Version: %{baseversion}.%{patchlevel}
Release: 3%{?dist}
Epoch: 2
# swift.vim contains Apache 2.0 with runtime library exception:
# which is taken as Apache-2.0 WITH Swift-exception - reported to legal as https://gitlab.com/fedora/legal/fedora-license-data/-/issues/188
# resolution: the license is good for Fedora, but the file does not have a creativity from 
#
# Open Publication License 1.0 or later for Vim documentation - reported to legal for adding to the allowed licenses list
# response here: https://lists.fedoraproject.org/archives/list/legal@lists.fedoraproject.org/message/4UTW5GFDELGMG6K3NQ7NBU42LC2FJOB5/
# resolution: take it as OPUBL-1.0, the license won't be added to allowed license list, but if a project uses it for documentation
# and don't use license options mentioned in the OPUBL 1.0 license text (which both are the case for Vim), the license is allowed
License: Vim AND LGPL-2.1-or-later AND MIT AND GPL-1.0-only AND (GPL-2.0-only OR Vim) AND Apache-2.0 AND BSD-2-Clause AND BSD-3-Clause AND GPL-2.0-or-later AND GPL-3.0-or-later AND OPUBL-1.0 AND Apache-2.0 WITH Swift-exception
Source0: ftp://ftp.vim.org/pub/vim/unix/vim-%{baseversion}-%{patchlevel}.tar.bz2
Source1: virc
Source2: vimrc
Source3: gvim16.png
Source4: gvim32.png
Source5: gvim48.png
Source6: gvim64.png
Source7: spec-template.new
Source8: macros.vim
Source9: vim-default-editor.sh
Source10: vim-default-editor.csh
Source11: vim-default-editor.fish
Source12: view_wrapper
Source13: vim.sh
Source14: vim.fish


Patch1: vim-7.0-fixkeys.patch
Patch2: vim-7.4-specsyntax.patch
Patch3: vim-7.3-manpage-typo-668894-675480.patch
Patch4: vim-manpagefixes-948566.patch
Patch5: vim-7.4-globalsyntax.patch
# migrate shebangs in script to /usr/bin/python3 and use python2 when necessary
Patch6: vim-python3-tests.patch
# fips warning (Fedora downstream patch)
Patch7: vim-crypto-warning.patch
# don't ever set mouse (Fedora downstream patch)
Patch8: vim-8.0-copy-paste.patch
# upstream test suite expects mouse to be set in some tests...
Patch9: vim-9.1-copy-paste.patch
# since F42+, if you let glibc to give you random port, it will give you two random ports
# - one for IPv4 address, another for IPv6 address by default. Vim counts on the port being
# the same, because the fake server used for testing (python script simulating netbeans or
# another language server with language server procotol - LSP) saves the port into a file
# for Vim to pick it up and use the informantion when connecting to the server. However,
# the problem appears when client gets localhost resolved into IPv4 address, but used
# the port which is used by fake server for IPv6 address.
# Since such tests are only mocking the real life behavior and in the real life Vim gets
# connection information by a different way, enforcing IPv4 in the test to prevent mismatch
# is a viable solution.
Patch10: vim-test-port-mismatch.patch


# patch only when hunspell is enabled
Patch10000: vim-7.0-hunspell.patch


# uses autoconf in spec file
BuildRequires: autoconf

# gcc is no longer in buildroot by default
BuildRequires: gcc
# for translations
BuildRequires: gettext

# glibc in F35 bootstraped several conversion formats from
# iconv into a separate package. Vim needs those additional
# formats during compilation.
BuildRequires: glibc-gconv-extra

# for setting ACL on created files
BuildRequires: libacl-devel

# uses libtool for linking
BuildRequires: libtool

# uses make
BuildRequires: make
# screen handling library
BuildRequires: ncurses-devel

# for building function prototypes
BuildRequires: python3
BuildRequires: python3-clang

# for python plugin
BuildRequires: python3-devel


%if %{desktop_file}
# for /usr/bin/desktop-file-install
BuildRequires: desktop-file-utils >= %{desktop_file_utils_version}
Requires: desktop-file-utils
%endif

%if %{with gpm}
# for mouse support in console
BuildRequires: gpm-devel
%endif

%if %{withhunspell}
BuildRequires: hunspell-devel
%endif

# for xchacha20 encryption
%if %{with libsodium_crypt}
BuildRequires: libsodium-devel
%endif

# for lua plugin
%if "%{withlua}" == "1"
BuildRequires: lua-devel
%endif

# for perl plugin
%if "%{withperl}" == "1"
BuildRequires: perl-devel
BuildRequires: perl-generators
BuildRequires: perl(ExtUtils::Embed)
BuildRequires: perl(ExtUtils::ParseXS)
%endif

# for ruby plugin
%if "%{withruby}" == "1"
BuildRequires: ruby
BuildRequires: ruby-devel
%endif

# selinux support
%if %{WITH_SELINUX}
BuildRequires: libselinux-devel
%endif


%description
VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  Vi was the first real screen-based editor for UNIX, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and more.


%package common
Summary: The common files needed by any version of the VIM editor
# move evim manpage to common - remove the conflict after C11S is branched
Conflicts: %{name}-X11 < 2:9.1.1706-2
# shared files between common and minimal
Requires: %{name}-data = %{epoch}:%{version}-%{release}
Requires: %{name}-filesystem
# the hexdump binary was part of the package for long time, ship it with it
# still for convenience
Requires: xxd

%description common
VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  Vi was the first real screen-based editor for UNIX, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and more.  The
vim-common package contains files which every VIM binary will need in
order to run.

If you are installing vim-enhanced or vim-X11, you'll also need
to install the vim-common package.


%package minimal
Summary: A minimal version of the VIM editor
Provides: vi
Provides: %{_bindir}/vi
# shared files between common and minimal
Requires: %{name}-data = %{epoch}:%{version}-%{release}

%description minimal
VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  Vi was the first real screen-based editor for UNIX, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and more. The
vim-minimal package includes a minimal version of VIM, providing
the commands vi, view, ex, rvi, and rview. NOTE: The online help is
only available when the vim-common package is installed.


%package enhanced
Summary: A version of the VIM editor which includes recent enhancements
# vim bundles libvterm, which is used during build - so we need to provide
# bundled libvterm for catching possible libvterm CVEs
Provides: bundled(libvterm)
Provides: vim
Provides: vim(plugins-supported)
Provides: %{_bindir}/mergetool
Provides: %{_bindir}/vim
Requires: vim-common = %{epoch}:%{version}-%{release}
# required for vimtutor (#395371)
Requires: which
Suggests: python3
Suggests: python3-libs

# suggest python3, python2, lua, ruby and perl packages because of their 
# embedded functionality in Vim/GVim
%if "%{withlua}" == "1"
Suggests: lua-libs
%endif

%if "%{withperl}" == "1"
Suggests: perl-devel
%endif

%if "%{withruby}" == "1"
Suggests: ruby
Suggests: ruby-libs
%endif

%description enhanced
VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  Vi was the first real screen-based editor for UNIX, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and more.  The
vim-enhanced package contains a version of VIM with extra, recently
introduced features like Python and Perl interpreters.

Install the vim-enhanced package if you'd like to use a version of the
VIM editor which includes recently added enhancements like
interpreters for the Python and Perl scripting languages.  You'll also
need to install the vim-common package.


%package filesystem
Summary: VIM filesystem layout
BuildArch: noarch

%Description filesystem
This package provides some directories which are required by other
packages that add vim files, p.e.  additional syntax files or filetypes.


%package data
Summary: Shared data for Vi and Vim
BuildArch: noarch

%description data
The subpackage is used for shipping files and directories, which need to be
shared between vim-minimal and vim-common packages.


%package -n xxd
Summary: A hex dump utility

%description -n xxd
xxd creates a hex dump of a given file or standard input.  It can also convert
a hex dump back to its original binary form.


%if %{with default_editor}
%package default-editor
Summary: Set vim as the default editor
BuildArch: noarch
Conflicts: system-default-editor
Provides: system-default-editor
Requires: vim-enhanced

%description default-editor
This subpackage contains files needed to set Vim as the default editor.
%endif

%if %{with gui}
%package X11
Summary: The VIM version of the vi editor for the X Window System - GVim
# move evim manpage to common - remove the conflict after C11S is branched
Conflicts: %{name}-common < 2:9.1.1706-2
# devel of libICE, gtk3, libSM, libX11, libXpm and libXt are needed in buildroot
# so configure script can have correct macros enabled for GUI (#1603272)
# generic gnome toolkit for graphical support
BuildRequires: gtk3-devel
# inter-client exchange library - for X session management protocol
BuildRequires: libICE-devel
# X session management library
BuildRequires: libSM-devel
# core X11 protocol client library
BuildRequires: libX11-devel
# X Toolkit Intrinsics library - working with widgets?
BuildRequires: libXt-devel
# for testing validity of appdata file
BuildRequires: libappstream-glib
# for sound support
BuildRequires: libcanberra-devel

Provides: gvim
Provides: vim(plugins-supported)
Provides: %{_bindir}/mergetool
Provides: %{_bindir}/gvim

# glib2 in Fedora 40 introduced a new function, which is not used in GVim, but it is present
# in compiled gvim binary as symbol when Vim is compiled with glib2-2.79.1
# there does not seem to be a better solution than version based requires on glib2...
# https://bugzilla.redhat.com/show_bug.cgi?id=2262371
Requires: glib2 >= 2.79.1
# GVIM graphics are based on GTK3
Requires: gtk3
# needed for icons (#226526)
Requires: hicolor-icon-theme
# for getting/setting extended attributes - they are pairs (name:value)
# from inodes (files, dirs etc.)
Requires: libattr >= 2.4
Requires: vim-common = %{epoch}:%{version}-%{release} 
Suggests: python3
Suggests: python3-libs

# suggest python3, python2, lua, ruby and perl packages because of their 
# embedded functionality in Vim/GVim
  %if "%{withlua}" == "1"
Suggests: lua-libs
  %endif

  %if "%{withperl}" == "1"
Suggests: perl-devel
  %endif

  %if "%{withruby}" == "1"
Suggests: ruby
Suggests: ruby-libs
  %endif

%description X11
VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  Vi was the first real screen-based editor for UNIX, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and
more. VIM-X11 is a version of the VIM editor which will run within the
X Window System.  If you install this package, you can run VIM as an X
application with a full GUI interface and mouse support by command gvim.

Install the vim-X11 package if you'd like to try out a version of vi
with graphics and mouse capabilities.  You'll also need to install the
vim-common package.
%endif


%prep
%setup -q -b 0 -n %{vimdir}

# use %%{__python3} macro for defining shebangs in python3 tests
sed -i -e 's,/usr/bin/python3,%{__python3},' %{PATCH6}

# fix rogue dependencies from sample code
chmod -x runtime/tools/mve.awk
%patch -P 1 -p1 -b .fixkeys
%patch -P 2 -p1 -b .spec-syntax

perl -pi -e "s,bin/nawk,bin/awk,g" runtime/tools/mve.awk

%patch -P 3 -p1 -b .mantypo
%patch -P 4 -p1 -b .manpagefixes
%patch -P 5 -p1 -b .globalsyntax
%patch -P 6 -p1 -b .python-tests
%patch -P 7 -p1 -b .fips-warning
%patch -P 8 -p1 -b .copypaste
%patch -P 9 -p1 -b .newcopy
%patch -P 10 -p1 -b .test-port-mismatch

%if %{withhunspell}
%patch -P 10000 -p1
%endif


%build
cd src
autoconf

# added -std=c17 because F42 uses c23 by default and dynamically loaded Ruby plugin fails to build
# with c23 due using `()` for callback arguments to be able to use callbacks with different number
# of arguments in one function
# reported upstream as https://github.com/vim/vim/issues/16575
export CFLAGS="%{optflags} -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_FORTIFY_SOURCE=2 -std=c17"
export CXXFLAGS="%{optflags} -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_FORTIFY_SOURCE=2 -std=c17"

cp -f os_unix.h os_unix.h.save

# Configure options:
# --enable-fail-if-missing - we need to fail if configure options aren't satisfied
# --with-features - for setting how big amount of features is enabled
# --enable-multibyte - enabling multibyte editing support - for editing files in languages, which one character
#                      cannot be represented by one byte - Asian languages, Unicode
# --disable-netbeans - disabling socket interface for integrating Vim into NetBeans IDE
# --enable-selinux - enabling selinux support
# --enable-Ninterp - enabling internal interpreter
# --with-x - yes if we want X11 support (graphical Vim for X11)
# --with-tlib - which terminal library to use
# --disable-gpm - disabling support for General Purpose Mouse - Linux mouse daemon

perl -pi -e "s/vimrc/virc/"  os_unix.h
%configure CFLAGS="${CFLAGS} -DSYS_VIMRC_FILE='\"/etc/virc\"'" \
  --prefix=%{_prefix} --with-features=tiny --with-x=no \
  --enable-multibyte \
  --disable-netbeans \
%if %{WITH_SELINUX}
  --enable-selinux \
%else
  --disable-selinux \
%endif
  --disable-pythoninterp --disable-perlinterp --disable-tclinterp \
  --with-tlib=ncurses --enable-gui=no --disable-gpm --exec-prefix=/ \
  --with-compiledby="<bugzilla@redhat.com>" \
  --with-modified-by="<bugzilla@redhat.com>" \
  --enable-fips-warning \
  --enable-fail-if-missing \
  --disable-canberra \
  --without-wayland \
  --enable-year2038 \
  --disable-libsodium

%make_build
cp vim minimal-vim
make clean


mv -f os_unix.h.save os_unix.h

%configure CFLAGS="${CFLAGS} -DSYS_VIMRC_FILE='\"/etc/vimrc\"'" \
 --prefix=%{_prefix} --with-features=huge \
 --enable-python3interp=dynamic \
  --with-python3-stable-abi \
 --disable-tclinterp \
 --with-x=no \
 --enable-gui=no --exec-prefix=%{_prefix} --enable-multibyte \
 --enable-cscope --with-modified-by="<bugzilla@redhat.com>" \
 --with-tlib=ncurses \
 --enable-fips-warning \
 --with-compiledby="<bugzilla@redhat.com>" \
%if %{with gpm}
 --enable-gpm \
%else
 --disable-gpm \
%endif
%if "%{withnetbeans}" == "1"
  --enable-netbeans \
%else
  --disable-netbeans \
%endif
%if %{WITH_SELINUX}
  --enable-selinux \
%else
  --disable-selinux \
%endif
%if "%{withperl}" == "1"
  --enable-perlinterp=dynamic \
  --with-xsubpp=$(which xsubpp) \
%else
  --disable-perlinterp \
%endif
%if "%{withruby}" == "1"
  --enable-rubyinterp=dynamic \
%else
  --disable-rubyinterp \
%endif
%if "%{withlua}" == "1"
  --enable-luainterp=dynamic \
%else
  --disable-luainterp \
%endif
%if %{with libsodium_crypt}
  --enable-libsodium \
%else
  --disable-libsodium \
%endif
  --enable-fail-if-missing \
  --without-wayland \
  --enable-year2038 \
  --disable-canberra

%make_build
cp vim enhanced-vim


%if %{with gui}
# More configure options:
# --enable-xim - enabling X Input Method - international input module for X,
#                it is for multibyte languages in Vim with X
# --enable-termtruecolor - use terminal with true colors

%configure CFLAGS="${CFLAGS} -DSYS_VIMRC_FILE='\"/etc/vimrc\"'" \
  --with-features=huge \
  --enable-python3interp=dynamic \
  --with-python3-stable-abi \
  --disable-tclinterp --with-x=yes \
  --enable-xim --enable-multibyte \
  --with-tlib=ncurses \
  --enable-gtk3-check --enable-gui=gtk3 \
  --enable-fips-warning \
  --with-compiledby="<bugzilla@redhat.com>" --enable-cscope \
  --with-modified-by="<bugzilla@redhat.com>" \
  %if %{with gpm}
  --enable-gpm \
  %else
  --disable-gpm \
  %endif
  %if "%{withnetbeans}" == "1"
  --enable-netbeans \
  %else
  --disable-netbeans \
  %endif
  %if %{WITH_SELINUX}
  --enable-selinux \
  %else
  --disable-selinux \
  %endif
  %if "%{withperl}" == "1"
  --enable-perlinterp=dynamic \
  --with-xsubpp=$(which xsubpp) \
  %else
  --disable-perlinterp \
  %endif
  %if "%{withruby}" == "1"
  --enable-rubyinterp=dynamic \
  %else
  --disable-rubyinterp \
  %endif
  %if "%{withlua}" == "1"
  --enable-luainterp=dynamic \
  %else
  --disable-luainterp \
  %endif
  %if %{with libsodium_crypt}
  --enable-libsodium \
  %else
  --disable-libsodium \
  %endif
  --enable-fail-if-missing \
  --with-wayland \
  --enable-year2038 \
  --enable-socketserver \
  --enable-canberra

%make_build
cp vim gvim
make clean
%endif


%install
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_datadir}/%{name}/vimfiles/{after,autoload,colors,compiler,doc,ftdetect,ftplugin,indent,keymap,lang,plugin,print,spell,syntax,tutor}
mkdir -p %{buildroot}/%{_datadir}/%{name}/vimfiles/after/{autoload,colors,compiler,doc,ftdetect,ftplugin,indent,keymap,lang,plugin,print,spell,syntax,tutor}
cp -f %{SOURCE7} %{buildroot}/%{_datadir}/%{name}/vimfiles/template.spec
# Those aren't Linux info files but some binary files for Amiga:
rm -f README*.info

cd src
# related to the issue with `make depend`, auto/osdef.h
# has to be generated
make auto/osdef.h auto/gui_gtk_gresources.h auto/wayland/wlr-data-control-unstable-v1.h
# Adding STRIP=/bin/true, because Vim wants to strip the binaries by himself
# and put the stripped files into correct dirs. Build system (koji/brew) 
# does it for us, so there is no need to do it in Vim
%make_install BINDIR=%{_bindir} STRIP=/bin/true

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/{16x16,32x32,48x48,64x64}/apps
install -m755 minimal-vim %{buildroot}%{_bindir}/vi
install -m755 enhanced-vim %{buildroot}%{_bindir}/vim
install -m755 %{SOURCE12} %{buildroot}%{_bindir}/view

%if %{with gui}
make installgtutorbin  DESTDIR=%{buildroot} BINDIR=%{_bindir}
install -m755 gvim %{buildroot}%{_bindir}/gvim
install -p -m644 %{SOURCE3} \
   %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/gvim.png
install -p -m644 %{SOURCE4} \
   %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/gvim.png
install -p -m644 %{SOURCE5} \
   %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/gvim.png
install -p -m644 %{SOURCE6} \
   %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/gvim.png

# Register as an application to be visible in the software center
#
# NOTE: It would be *awesome* if this file was maintained by the upstream
# project, translated and installed into the right place during `make install`.
#
# See http://www.freedesktop.org/software/appstream/docs/ for more details.
#
mkdir -p $RPM_BUILD_ROOT%{_datadir}/metainfo
cat > $RPM_BUILD_ROOT%{_datadir}/metainfo/gvim.appdata.xml <<"EOF"
<?xml version="1.0" encoding="UTF-8"?>
<!-- Copyright 2014 Richard Hughes <richard@hughsie.com> -->
<!--
EmailAddress: Bram@moolenaar.net>
SentUpstream: 2014-05-22
-->
<component type="desktop-application">
  <id>org.vim.Vim</id>
  <name>GVim</name>
  <metadata_license>CC0-1.0</metadata_license>
  <project_license>Vim</project_license>
  <summary>The VIM version of the vi editor for the X Window System</summary>
  <description>
    <p>
     Vim is an advanced text editor that seeks to provide the power of the
     de-facto Unix editor 'Vi', with a more complete feature set.
     It's useful whether you're already using vi or using a different editor.
    </p>
    <p>
     Vim is a highly configurable text editor built to enable efficient text
     editing.
     Vim is often called a "programmer's editor," and so useful for programming
     that many consider it an entire IDE. It is not just for programmers, though.
     Vim is perfect for all kinds of text editing, from composing email to
     editing configuration files.
    </p>
    <p>
     We ship the current Vim stable release - %{baseversion} - with the upstream
     patchlevel %{patchlevel} applied, which is combined into version %{version}
     used during packaging.
    </p>
  </description>
  <releases>
    <release version="%{version}" date="%(date +%F -r %{SOURCE0})" />
  </releases>
  <screenshots>
    <screenshot type="default">
      <image>https://raw.githubusercontent.com/zdohnal/vim/zdohnal-screenshot/gvim16_9.png</image>
    </screenshot>
  </screenshots>
  <url type="homepage">http://www.vim.org/</url>
  <content_rating type="oars-1.1"/>
  <!--
    Without this tag, the G-S does not display icon properly. But also the
    `appstream-builder` inserts into metadata generic
    `<launchable type="desktop-id">org.vim.Vim.desktop</launchable>`,
    which cannot be found. This results in `Vetos: Has no Icon` and
    therefore rejection of GVim from `appstream-data` package.
  -->
  <launchable type="desktop-id">gvim.desktop</launchable>
</component>
EOF

appstream-util validate-relax --nonet %{buildroot}/%{_datadir}/metainfo/*.appdata.xml

# do not put gvim.1, gview.1, eview.1, rgvim and rgview here - they already contains the link,
# and changing it here will rewrite original vim.1 - bz#2392178
for i in gex.1 vimx.1 evim.1; do
  echo ".so man1/vim.1" > %{buildroot}/%{_mandir}/man1/$i
done

echo ".so man1/vimtutor.1" > %{buildroot}/%{_mandir}/man1/gvimtutor.1
%else
# Remove files included in X11 subpackage, but built by default:
rm %{buildroot}/%{_mandir}/man1/evim.*
rm %{buildroot}/%{_datadir}/applications/{vim,gvim}.desktop
rm %{buildroot}/%{_datadir}/icons/{hicolor,locolor}/*/apps/gvim.png
%endif

( cd %{buildroot}
  ln -sf ../..%{_bindir}/vi .%{_bindir}/rvi
  ln -sf ../..%{_bindir}/vi .%{_bindir}/rview
  ln -sf ../..%{_bindir}/vi .%{_bindir}/ex
  ln -sf vim .%{_bindir}/rvim
  ln -sf vim .%{_bindir}/vimdiff
  perl -pi -e "s,%{buildroot},," .%{_mandir}/man1/vim.1 .%{_mandir}/man1/vimtutor.1
  rm -f .%{_mandir}/man1/rvim.1
  cp -p .%{_mandir}/man1/vim.1 .%{_mandir}/man1/vi.1
  ln -sf vi.1.gz .%{_mandir}/man1/rvi.1.gz
  ln -sf vi.1.gz .%{_mandir}/man1/ex.1
  ln -sf vi.1.gz .%{_mandir}/man1/view.1
  ln -sf vi.1.gz .%{_mandir}/man1/rview.1
  ln -sf vim.1.gz .%{_mandir}/man1/vimdiff.1.gz

%if %{with gui}
  ln -sf gvim ./%{_bindir}/evim
  ln -sf gvim ./%{_bindir}/eview
  ln -sf gvim ./%{_bindir}/gview
  ln -sf gvim ./%{_bindir}/gex
  ln -sf gvim ./%{_bindir}/gvimdiff
  ln -sf gvim ./%{_bindir}/rgvim
  ln -sf gvim ./%{_bindir}/rgview
  ln -sf gvim ./%{_bindir}/vimx

  %if "%{desktop_file}" == "1"
    desktop-file-install \
        --dir %{buildroot}/%{_datadir}/applications \
        %{buildroot}/%{_datadir}/applications/gvim.desktop
        # --add-category "Development;TextEditor;X-Red-Hat-Base" D\
  %else
    mkdir -p ./%{_sysconfdir}/X11/applnk/Applications
    cp %{buildroot}/%{_datadir}/applications/gvim.desktop ./%{_sysconfdir}/X11/applnk/Applications/gvim.desktop
  %endif

%endif

  # ja_JP.ujis is obsolete, ja_JP.eucJP is recommended.
  ( cd ./%{_datadir}/%{name}/%{vimdir}/lang; \
    ln -sf menu_ja_jp.ujis.vim menu_ja_jp.eucjp.vim )
)

# Dependency cleanups
chmod 644 %{buildroot}/%{_datadir}/%{name}/%{vimdir}/doc/vim2html.pl \
 %{buildroot}/%{_datadir}/%{name}/%{vimdir}/tools/*.pl \
 %{buildroot}/%{_datadir}/%{name}/%{vimdir}/tools/vim132
chmod 644 ../runtime/doc/vim2html.pl

mkdir -p %{buildroot}%{_sysconfdir}
install -p -m644 %{SOURCE1} %{buildroot}%{_sysconfdir}/virc
install -p -m644 %{SOURCE2} %{buildroot}%{_sysconfdir}/vimrc

mkdir -p %{buildroot}%{_rpmconfigdir}/macros.d/
install -p -m644 %{SOURCE8} %{buildroot}%{_rpmconfigdir}/macros.d/

(cd ../runtime; rm -rf doc; ln -svf ../../vim/%{vimdir}/doc docs;) 
rm -f %{buildroot}/%{_datadir}/vim/%{vimdir}/macros/maze/maze*.c
rm -rf %{buildroot}/%{_datadir}/vim/%{vimdir}/tools
rm -rf %{buildroot}/%{_datadir}/vim/%{vimdir}/doc/vim2html.pl
rm -f %{buildroot}/%{_datadir}/vim/%{vimdir}/tutor/tutor.gr.utf-8~

# Remove not UTF-8 manpages
for i in pl.ISO8859-2 it.ISO8859-1 ru.KOI8-R fr.ISO8859-1 da.ISO8859-1 de.ISO8859-1 tr.ISO8859-9 sv.ISO8859-1; do
  rm -rf %{buildroot}/%{_mandir}/$i
done

# use common man1/ru directory
mv %{buildroot}/%{_mandir}/ru.UTF-8 %{buildroot}/%{_mandir}/ru

# Remove duplicate man pages
for i in fr.UTF-8 it.UTF-8 pl.UTF-8 da.UTF-8 de.UTF-8 tr.UTF-8 sv.UTF-8; do
  rm -rf %{buildroot}/%{_mandir}/$i
done

# Install symlink for rvim man page
echo ".so man1/vim.1" > %{buildroot}/%{_mandir}/man1/rvim.1

mkdir -p %{buildroot}/%{_mandir}/man5
echo ".so man1/vim.1" > %{buildroot}/%{_mandir}/man5/vimrc.5
echo ".so man1/vi.1" > %{buildroot}/%{_mandir}/man5/virc.5
touch %{buildroot}/%{_datadir}/%{name}/vimfiles/doc/tags

# upstream now tries to install LICENSE and README into VIMDIR
# but we ship them in licensedir and docdir, so we remove the dupes
# from VIMDIR
rm %{buildroot}%{_datadir}/%{name}/%{vimdir}/LICENSE
rm %{buildroot}%{_datadir}/%{name}/%{vimdir}/README.txt

# if Vim isn't built for Fedora, use redhat augroup
%if 0%{?rhel} >= 7
sed -i -e "s/augroup fedora/augroup redhat/" %{buildroot}/%{_sysconfdir}/vimrc
sed -i -e "s/augroup fedora/augroup redhat/" %{buildroot}/%{_sysconfdir}/virc
%endif

# adding vi->vim aliases per rhbz#2439657 for bash, ksh, zsh and fish
# it won't work without bash reload and under sudo, but reporter was aware
mkdir -p %{buildroot}/%{_sysconfdir}/profile.d
install -p -m644 %{SOURCE13} %{buildroot}/%{_sysconfdir}/profile.d/vim.sh

mkdir -p %{buildroot}/%{_datadir}/fish/vendor_functions.d/
install -p -m644 %{SOURCE14} %{buildroot}/%{_datadir}/fish/vendor_functions.d/vim.fish

%if %{with default_editor}
install -p -m644 %{SOURCE9} %{buildroot}/%{_sysconfdir}/profile.d/vim-default-editor.sh
install -p -m644 %{SOURCE10} %{buildroot}/%{_sysconfdir}/profile.d/vim-default-editor.csh

mkdir -p %{buildroot}/%{_datadir}/fish/vendor_conf.d/
install -p -m644 %{SOURCE11} %{buildroot}/%{_datadir}/fish/vendor_conf.d/vim-default-editor.fish
%endif


# Refresh documentation helptags
%transfiletriggerin common -- %{_datadir}/%{name}/vimfiles/doc
%{_bindir}/vim -c ":helptags %{_datadir}/%{name}/vimfiles/doc" -c :q &> /dev/null || :

%transfiletriggerpostun common -- %{_datadir}/%{name}/vimfiles/doc
> %{_datadir}/%{name}/vimfiles/doc/tags || :
%{_bindir}/vim -c ":helptags %{_datadir}/%{name}/vimfiles/doc" -c :q &> /dev/null || :

%files common
%config(noreplace) %{_sysconfdir}/vimrc
%{!?_licensedir:%global license %%doc}
%doc README*
%doc runtime/docs
%{_datadir}/%{name}/%{vimdir}/autoload
%{_datadir}/%{name}/%{vimdir}/colors
%{_datadir}/%{name}/%{vimdir}/compiler
%{_datadir}/%{name}/%{vimdir}/pack
%{_datadir}/%{name}/%{vimdir}/doc
%{_datadir}/%{name}/%{vimdir}/*.vim
%exclude %{_datadir}/%{name}/%{vimdir}/defaults.vim
%{_datadir}/%{name}/%{vimdir}/ftplugin
%{_datadir}/%{name}/%{vimdir}/import/dist/vimhelp.vim
%{_datadir}/%{name}/%{vimdir}/import/dist/vimhighlight.vim
%{_datadir}/%{name}/%{vimdir}/indent
%{_datadir}/%{name}/%{vimdir}/keymap
%{_datadir}/%{name}/%{vimdir}/lang/*.vim
%{_datadir}/%{name}/%{vimdir}/lang/*.txt
%dir %{_datadir}/%{name}/%{vimdir}/lang
%{_datadir}/%{name}/%{vimdir}/macros
%{_datadir}/%{name}/%{vimdir}/plugin
%{_datadir}/%{name}/%{vimdir}/print
%{_datadir}/%{name}/%{vimdir}/syntax
%{_datadir}/%{name}/%{vimdir}/tutor
%{_datadir}/%{name}/%{vimdir}/spell
%lang(af) %{_datadir}/%{name}/%{vimdir}/lang/af
%lang(ca) %{_datadir}/%{name}/%{vimdir}/lang/ca
%lang(cs) %{_datadir}/%{name}/%{vimdir}/lang/cs
%lang(cs.cp1250) %{_datadir}/%{name}/%{vimdir}/lang/cs.cp1250
%lang(da) %{_datadir}/%{name}/%{vimdir}/lang/da
%lang(de) %{_datadir}/%{name}/%{vimdir}/lang/de
%lang(en_GB) %{_datadir}/%{name}/%{vimdir}/lang/en_GB
%lang(eo) %{_datadir}/%{name}/%{vimdir}/lang/eo
%lang(es) %{_datadir}/%{name}/%{vimdir}/lang/es
%lang(fi) %{_datadir}/%{name}/%{vimdir}/lang/fi
%lang(fr) %{_datadir}/%{name}/%{vimdir}/lang/fr
%lang(ga) %{_datadir}/%{name}/%{vimdir}/lang/ga
%lang(hu) %{_datadir}/%{name}/%{vimdir}/lang/hu
%lang(hy) %{_datadir}/%{name}/%{vimdir}/lang/hy
%lang(it) %{_datadir}/%{name}/%{vimdir}/lang/it
%lang(ja) %{_datadir}/%{name}/%{vimdir}/lang/ja
%lang(ja.euc-jp) %{_datadir}/%{name}/%{vimdir}/lang/ja.euc-jp
%lang(ja.sjis) %{_datadir}/%{name}/%{vimdir}/lang/ja.sjis
%lang(ko) %{_datadir}/%{name}/%{vimdir}/lang/ko
%lang(ko) %{_datadir}/%{name}/%{vimdir}/lang/ko.UTF-8
%lang(lv) %{_datadir}/%{name}/%{vimdir}/lang/lv
%lang(nb) %{_datadir}/%{name}/%{vimdir}/lang/nb
%lang(nl) %{_datadir}/%{name}/%{vimdir}/lang/nl
%lang(no) %{_datadir}/%{name}/%{vimdir}/lang/no
%lang(pl) %{_datadir}/%{name}/%{vimdir}/lang/pl
%lang(pl.UTF-8) %{_datadir}/%{name}/%{vimdir}/lang/pl.UTF-8
%lang(pl.cp1250) %{_datadir}/%{name}/%{vimdir}/lang/pl.cp1250
%lang(pt_BR) %{_datadir}/%{name}/%{vimdir}/lang/pt_BR
%lang(ru) %{_datadir}/%{name}/%{vimdir}/lang/ru
%lang(ru.cp1251) %{_datadir}/%{name}/%{vimdir}/lang/ru.cp1251
%lang(sk) %{_datadir}/%{name}/%{vimdir}/lang/sk
%lang(sk.cp1250) %{_datadir}/%{name}/%{vimdir}/lang/sk.cp1250
%lang(sr) %{_datadir}/%{name}/%{vimdir}/lang/sr
%lang(sv) %{_datadir}/%{name}/%{vimdir}/lang/sv
%lang(ta) %{_datadir}/%{name}/%{vimdir}/lang/ta
%lang(tr) %{_datadir}/%{name}/%{vimdir}/lang/tr
%lang(uk) %{_datadir}/%{name}/%{vimdir}/lang/uk
%lang(uk.cp1251) %{_datadir}/%{name}/%{vimdir}/lang/uk.cp1251
%lang(vi) %{_datadir}/%{name}/%{vimdir}/lang/vi
%lang(zh_CN) %{_datadir}/%{name}/%{vimdir}/lang/zh_CN
%lang(zh_CN.cp936) %{_datadir}/%{name}/%{vimdir}/lang/zh_CN.cp936
%lang(zh_TW) %{_datadir}/%{name}/%{vimdir}/lang/zh_TW
%lang(zh_CN.UTF-8) %{_datadir}/%{name}/%{vimdir}/lang/zh_CN.UTF-8
%lang(zh_TW.UTF-8) %{_datadir}/%{name}/%{vimdir}/lang/zh_TW.UTF-8
%{_mandir}/man1/rvim.*
%{_mandir}/man1/vim.*
%{_mandir}/man1/vimdiff.*
%{_mandir}/man1/vimtutor.*
%{_mandir}/man5/vimrc.*

%if %{with gui}
%{_mandir}/man1/eview.*
%{_mandir}/man1/evim.*
%{_mandir}/man1/gex.*
%{_mandir}/man1/gview.*
%{_mandir}/man1/gvim*
%{_mandir}/man1/rgvim.*
%{_mandir}/man1/rgview.*
%{_mandir}/man1/vimx.*
%endif

%lang(fr) %{_mandir}/fr/man1/*
%lang(da) %{_mandir}/da/man1/*
%lang(de) %{_mandir}/de/man1/*
%lang(it) %{_mandir}/it/man1/*
%lang(ja) %{_mandir}/ja/man1/*
%lang(pl) %{_mandir}/pl/man1/*
%lang(ru) %{_mandir}/ru/man1/*
%lang(sv) %{_mandir}/sv/man1/*
%lang(tr) %{_mandir}/tr/man1/*

%files minimal
%config(noreplace) %{_sysconfdir}/virc
%{_bindir}/ex
%{_bindir}/rvi
%{_bindir}/rview
%{_bindir}/vi
%{_bindir}/view
%{_mandir}/man1/vi.*
%{_mandir}/man1/ex.*
%{_mandir}/man1/rvi.*
%{_mandir}/man1/rview.*
%{_mandir}/man1/view.*
%{_mandir}/man5/virc.*

%files enhanced
%{_bindir}/rvim
%{_bindir}/vim
%{_bindir}/vimdiff
%{_bindir}/vimtutor
%dir %{_datadir}/fish/vendor_functions.d/
%{_datadir}/fish/vendor_functions.d/vim.fish
%config(noreplace) %{_sysconfdir}/profile.d/vim.sh

%files filesystem
%{_rpmconfigdir}/macros.d/macros.vim
%dir %{_datadir}/%{name}/vimfiles/after
%dir %{_datadir}/%{name}/vimfiles/after/*
%dir %{_datadir}/%{name}/vimfiles/autoload
%dir %{_datadir}/%{name}/vimfiles/colors
%dir %{_datadir}/%{name}/vimfiles/compiler
%dir %{_datadir}/%{name}/vimfiles/doc
%ghost %{_datadir}/%{name}/vimfiles/doc/tags
%dir %{_datadir}/%{name}/vimfiles/ftdetect
%dir %{_datadir}/%{name}/vimfiles/ftplugin
%dir %{_datadir}/%{name}/%{vimdir}/import
%dir %{_datadir}/%{name}/%{vimdir}/import/dist
%dir %{_datadir}/%{name}/vimfiles/indent
%dir %{_datadir}/%{name}/vimfiles/keymap
%dir %{_datadir}/%{name}/vimfiles/lang
%dir %{_datadir}/%{name}/vimfiles/plugin
%dir %{_datadir}/%{name}/vimfiles/print
%dir %{_datadir}/%{name}/vimfiles/spell
%dir %{_datadir}/%{name}/vimfiles/syntax
%dir %{_datadir}/%{name}/vimfiles/tutor
%dir %{_sysconfdir}/profile.d

%if %{with gui}
%files X11
  %if "%{desktop_file}" == "1"
%{_datadir}/metainfo/*.appdata.xml
/%{_datadir}/applications/*
%exclude /%{_datadir}/applications/vim.desktop
  %else
/%{_sysconfdir}/X11/applnk/*/gvim.desktop
  %endif
%{_bindir}/gvimtutor
%{_bindir}/gvim
%{_bindir}/gvimdiff
%{_bindir}/gview
%{_bindir}/gex
%{_bindir}/vimtutor
%{_bindir}/vimx
%{_bindir}/evim
%{_bindir}/eview
%{_bindir}/rgvim
%{_bindir}/rgview
%dir %{_datadir}/icons/hicolor
%dir %{_datadir}/icons/hicolor/*
%dir %{_datadir}/icons/hicolor/*/apps
%{_datadir}/icons/hicolor/*/apps/*
%dir %{_datadir}/icons/locolor
%dir %{_datadir}/icons/locolor/*
%dir %{_datadir}/icons/locolor/*/apps
%{_datadir}/icons/locolor/*/apps/*
%endif

%files data
%license LICENSE
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/%{vimdir}
%{_datadir}/%{name}/%{vimdir}/defaults.vim
%dir %{_datadir}/%{name}/vimfiles
%{_datadir}/%{name}/vimfiles/template.spec

%if %{with default_editor}
%files default-editor
%dir %{_datadir}/fish/vendor_conf.d
%{_datadir}/fish/vendor_conf.d/vim-default-editor.fish
%config(noreplace) %{_sysconfdir}/profile.d/vim-default-editor.*
%endif

%files -n xxd
%license LICENSE
%{_bindir}/xxd
%{_mandir}/man1/xxd.*


%changelog
* Mon Feb 16 2026 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.2146-2
- provide previous vi->vim alias (fedora#2439657)

* Fri Feb 13 2026 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.2146-1
- patchlevel 2146

* Wed Feb 04 2026 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.2128-1
- patchlevel 2128

* Tue Feb 03 2026 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.2114-2
- make /usr/bin/vi executable again to be able to use it with sudo option NOEXEC

* Fri Jan 30 2026 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.2114-1
- patchlevel 2114
- added Swedish translation

* Fri Jan 30 2026 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.2086-2
- fix some of test suite failures

* Fri Jan 16 2026 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.2086-1
- patchlevel 2086

* Fri Jan 09 2026 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.2068-1
- patchlevel 2068

* Fri Dec 19 2025 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.1999-1
- patchlevel 1999

* Fri Dec 12 2025 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.1972-1
- patchlevel 1972

* Fri Dec 05 2025 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.1952-1
- patchlevel 1952

* Fri Nov 14 2025 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.1914-1
- patchlevel 1914

* Fri Oct 31 2025 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.1888-1
- patchlevel 1888

* Fri Oct 17 2025 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.1863-1
- patchlevel 1863

* Fri Oct 10 2025 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.1845-1
- patchlevel 1845

* Fri Oct 03 2025 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.1818-1
- patchlevel 1818

* Mon Sep 29 2025 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.1775-2
- remove XPM support - GVim icons work without it

* Fri Sep 19 2025 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.1775-1
- patchlevel 1775

* Wed Sep 10 2025 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.1723-2
- Restore lost --remote-tab... functionality on wayland (fedora#2393716)

* Mon Sep 01 2025 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.1723-1
- patchlevel 1723

* Mon Sep 01 2025 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.1706-2
- broken /usr/bin/ex symlink in vim-9.1.1706-1.fc42 (fedora#2392249)
- vim-common has broken manpages (fedora#2392178)

* Fri Aug 29 2025 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.1706-1
- patchlevel 1706

* Mon Aug 11 2025 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.1623-1
- patchlevel 1623

* Fri Aug 01 2025 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.1591-1
- patchlevel 1591

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2:9.1.1552-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jul 16 2025 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.1552-1
- patchlevel 1552

* Mon Jul 14 2025 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.1537-2
- 2379759 - remove wayland-libs from vim and vi (fedora#2379759)

* Fri Jul 11 2025 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.1537-1
- patchlevel 1537

* Fri Jun 27 2025 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.1484-1
- patchlevel 1484

* Thu Jun 19 2025 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.1435-2
- FTBFS with Python 3.14 (fedora#2373314)

* Fri Jun 06 2025 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.1435-1
- patchlevel 1435

* Fri May 30 2025 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.1418-1
- patchlevel 1418

* Fri Apr 11 2025 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.1291-1
- patchlevel 1291

* Fri Apr 04 2025 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.1275-1
- patchlevel 1275

* Fri Mar 21 2025 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.1227-1
- patchlevel 1227

* Fri Mar 14 2025 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.1202-1
- patchlevel 1202

* Fri Mar 07 2025 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.1179-1
- patchlevel 1179

* Tue Mar 04 2025 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.1169-1
- patchlevel 1169

* Wed Feb 19 2025 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.1122-1
- patchlevel 1122

* Fri Feb 07 2025 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.1081-1
- patchlevel 1081

* Mon Feb 03 2025 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.1000-2
- Fix FTBFS (fedora#2341508)

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2:9.1.1000-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jan 10 2025 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.1000-1
- patchlevel 1000

* Fri Jan 03 2025 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.984-1
- patchlevel 984

* Fri Dec 13 2024 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.919-1
- patchlevel 919

* Fri Dec 06 2024 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.906-1
- patchlevel 906

* Fri Nov 29 2024 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.895-1
- patchlevel 895

* Fri Nov 15 2024 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.866-1
- patchlevel 866

* Fri Nov 01 2024 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.825-1
- patchlevel 825

* Tue Oct 15 2024 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.785-1
- patchlevel 785

* Fri Sep 20 2024 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.737-1
- patchlevel 737 (fedora#2311860)

* Fri Sep 06 2024 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.719-1
- patchlevel 719

* Fri Aug 30 2024 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.703-1
- patchlevel 703

* Mon Aug 12 2024 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.672-1
- patchlevel 672

* Fri Aug 09 2024 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.660-2
- 2303669 - vim in rawhide (41) can't load python library

* Mon Aug 05 2024 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.660-1
- patchlevel 660

* Fri Jul 26 2024 Benjamin Gilbert <bgilbert@backtick.net> - 2:9.1.571-3
- Require gdk-pixbuf2-modules-extra on F41+ -X11 for XPM loading (rhbz#2277751)

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2:9.1.571-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jul 12 2024 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.571-1
- patchlevel 571

* Fri Jul 12 2024 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.544-2
- fix upstream-scripttests in CI - new test needs our downstream 'set mouse=a' to pass

* Mon Jul 08 2024 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.544-1
- patchlevel 544

* Fri May 31 2024 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.452-1
- patchlevel 452

* Mon May 06 2024 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.393-1
- patchlevel 393

* Fri Apr 19 2024 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.354-1
- patchlevel 354

* Fri Apr 12 2024 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.309-1
- patchlevel 309

* Fri Apr 05 2024 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.264-1
- patchlevel 264

* Tue Apr 02 2024 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.252-1
- patchlevel 252

* Fri Mar 15 2024 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.181-1
- patchlevel 181

* Fri Mar 08 2024 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.158-1
- patchlevel 158

* Fri Feb 16 2024 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.113-1
- patchlevel 113

* Fri Feb 09 2024 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.083-1
- patchlevel 083

* Mon Feb 05 2024 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.076-2
- enable building without GPM support - build with GPM in Fedora
- 2262371 - gvim: symbol lookup error: gvim: undefined symbol: g_once_init_enter_pointer

* Mon Feb 05 2024 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.076-1
- patchlevel 076

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2:9.1.031-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Jan 16 2024 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.031-1
- patchlevel 031

* Mon Jan 08 2024 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.1.016-1
- patchlevel 016

* Tue Jan 02 2024 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.2190-1
- patchlevel 2190

* Fri Dec 15 2023 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.2167-1
- patchlevel 2167

* Fri Dec 08 2023 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.2153-1
- patchlevel 2153

* Wed Nov 22 2023 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.2120-1
- patchlevel 2120

* Thu Nov 16 2023 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.2105-1
- patchlevel 2105

* Wed Nov 01 2023 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.2081-1
- patchlevel 2081

* Wed Oct 18 2023 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.2048-1
- patchlevel 2048

* Thu Oct 05 2023 Remi Collet <remi@remirepo.net> - 2:9.0.1984-2
- rebuild for new libsodium

* Thu Oct 05 2023 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.1984-1
- patchlevel 1984

* Mon Oct 02 2023 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.1968-1
- patchlevel 1968

* Fri Sep 22 2023 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.1927-1
- patchlevel 1927

* Thu Sep 07 2023 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.1882-1
- patchlevel 1882

* Wed Sep 06 2023 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.1872-2
- test_xxd_color2 is flaky

* Tue Sep 05 2023 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.1872-1
- patchlevel 1872

* Wed Aug 30 2023 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.1822-1
- patchlevel 1822

* Mon Aug 14 2023 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.1712-1
- patchlevel 1712

* Fri Aug 11 2023 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.1677-4
- fix test suite from python3 syntax warnings

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2:9.0.1677-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jul 13 2023 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.1677-2
- 2222671 - fix FTBFS due Python3 rebase
- 2222648 - fix FailToInstall due Perl rebase

* Tue Jul 11 2023 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.1677-2
- patchlevel 1677

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 2:9.0.1671-2
- Perl 5.38 rebuild

* Fri Jun 30 2023 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.1671-1
- patchlevel 1671

* Fri Jun 23 2023 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.1649-1
- patchlevel 1649

* Tue Jun 13 2023 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.1627-1
- patchlevel 1627

* Mon Jun 05 2023 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.1607-1
- patchlevel 1607

* Wed May 31 2023 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.1592-1
- patchlevel 1592

* Mon May 29 2023 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.1587-1
- patchlevel 1587

* Wed May 24 2023 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.1575-1
- patchlevel 1575

* Thu May 18 2023 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.1562-1
- patchlevel 1562

* Thu Apr 27 2023 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.1491-1
- patchlevel 1491

* Tue Apr 25 2023 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.1486-1
- patchlevel 1486

* Fri Apr 21 2023 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.1472-1
- patchlevel 1472

* Tue Apr 11 2023 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.1443-1
- patchlevel 1443

* Tue Apr 11 2023 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.1440-2
- incorporate License tag changes based on legal team response

* Wed Apr 05 2023 Andreas Schneider <asn@redhat.com> - 2:9.0.1440-2
- create xxd package, because it is used by hex.nvim

* Wed Apr 05 2023 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.1440-2
- list most licenses available in binary rpms and migrate them into SPDX syntax

* Wed Apr 05 2023 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.1440-1
- patchlevel 1440

* Mon Mar 27 2023 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.1429-1
- patchlevel 1429

* Wed Mar 22 2023 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.1423-1
- patchlevel 1423

* Thu Mar 16 2023 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.1407-1
- patchlevel 1407

* Tue Mar 14 2023 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.1403-1
- patchlevel 1403

* Thu Mar 02 2023 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.1367-1
- patchlevel 1367

* Fri Feb 17 2023 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.1314-1
- patchlevel 1314

* Tue Feb 14 2023 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.1307-1
- patchlevel 1307

* Tue Feb 14 2023 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.1293-2
- 2169641 - Syntax highlight for sh files broken

* Thu Feb 09 2023 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.1293-1
- patchlevel 1293

* Mon Jan 30 2023 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.1262-1
- patchlevel 1262

* Thu Jan 19 2023 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.1221-1
- patchlevel 1221

* Thu Jan 12 2023 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.1182-1
- patchlevel 1182

* Mon Jan 09 2023 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.1160-1
- patchlevel 1160

* Mon Jan 09 2023 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.1054-2
- FTBFS with new FORTIFY_SOURCE=3 - remove it since Vim wants level 1

* Wed Dec 14 2022 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.1054-1
- patchlevel 1054

* Mon Dec 05 2022 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.1006-1
- patchlevel 1006

* Mon Nov 28 2022 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.963-1
- patchlevel 963

* Mon Nov 21 2022 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.915-1
- patchlevel 915

* Thu Nov 03 2022 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.828-1
- patchlevel 828

* Thu Oct 20 2022 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.803-1
- patchlevel 803

* Mon Oct 17 2022 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.777-1
- patchlevel 777

* Wed Oct 12 2022 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.720-2
- the current configure option for Vi is 'tiny'

* Tue Oct 11 2022 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.720-1
- patchlevel 720

* Wed Sep 28 2022 Carl George <carl@george.computer> - 2:9.0.475-2
- Obsolete vim-toml since the runtime files are now part of vim-common

* Fri Sep 16 2022 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.475-1
- patchlevel 475

* Fri Sep 16 2022 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.412-2
- provide 'vim(plugins-supported)' for plugins to require Vim/GVim

* Thu Sep 08 2022 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.412-1
- patchlevel 412

* Thu Sep 01 2022 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.348-1
- patchlevel 348

* Tue Aug 30 2022 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.327-1
- patchlevel 327

* Tue Aug 23 2022 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.246-1
- patchlevel 246

* Mon Aug 15 2022 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.213-1
- patchlevel 213

* Thu Aug 11 2022 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.189-1
- patchlevel 189

* Thu Aug 04 2022 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.137-1
- patchlevel 137

* Tue Jul 26 2022 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.077-1
- patchlevel 077

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2:9.0.049-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jul 11 2022 Zdenek Dohnal <zdohnal@redhat.com> - 2:9.0.049-1
- patchlevel 049

* Tue Jun 28 2022 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.5172-1
- patchlevel 5172

* Tue Jun 21 2022 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.5141-1
- patchlevel 5141

* Tue Jun 14 2022 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.5085-1
- patchlevel 5085

* Fri Jun 03 2022 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.5052-1
- patchlevel 5052

* Tue May 31 2022 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.5046-1
- patchlevel 5046

* Wed May 18 2022 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.4975-1
- patchlevel 4975

* Tue May 17 2022 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.4969-1
- patchlevel 4969

* Mon May 09 2022 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.4927-1
- patchlevel 4927

* Mon May 09 2022 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.4877-2
- add new file vimhelp.vim

* Fri May 06 2022 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.4877-1
- patchlevel 4877

* Mon May 02 2022 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.4857-1
- patchlevel 4857

* Fri Apr 29 2022 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.4845-1
- patchlevel 4845

* Fri Apr 22 2022 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.4804-1
- patchlevel 4804

* Fri Apr 08 2022 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.4701-2
- fix the upstream testsuite failure due downstream patch

* Thu Apr 07 2022 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.4701-1
- patchlevel 4701

* Fri Mar 25 2022 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.4621-1
- patchlevel 4621

* Wed Mar 16 2022 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.4579-1
- patchlevel 4579

* Wed Mar 09 2022 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.4529-1
- patchlevel 4529

* Tue Mar 01 2022 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.4485-1
- patchlevel 4485

* Thu Feb 24 2022 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.4460-1
- patchlevel 4460

* Mon Feb 21 2022 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.4428-1
- patchlevel 4428

* Tue Feb 15 2022 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.4386-1
- patchlevel 4386

* Mon Feb 07 2022 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.4314-1
- patchlevel 4314

* Thu Jan 27 2022 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.4232-1
- patchlevel 4232

* Mon Jan 24 2022 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.4198-1
- patchlevel 4198

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2:8.2.4068-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jan 12 2022 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.4068-1
- patchlevel 4068

* Mon Jan 10 2022 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.4051-1
- patchlevel 4051

* Fri Jan 07 2022 Malcolm Inglis <miinglis@amazon.com> - 2:8.2.4006-2
- add 'gui' build condition for vim-X11

* Wed Jan 05 2022 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.4006-1
- patchlevel 4006

* Wed Dec 15 2021 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.3811-1
- patchlevel 3811

* Tue Dec 07 2021 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.3755-1
- patchlevel 3755

* Thu Dec 02 2021 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.3717-1
- patchlevel 3717

* Thu Nov 25 2021 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.3642-2
- 2026651 - defaults.vim changes create conflicts between vim-minimal and vim-common

* Mon Nov 22 2021 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.3642-1
- patchlevel 3642

* Mon Nov 08 2021 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.3582-1
- patchlevel 3582

* Mon Nov 01 2021 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.3568-1
- patchlevel 3568

* Fri Oct 15 2021 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.3512-1
- patchlevel 3512

* Thu Oct 14 2021 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.3404-2
- adjust test suite to Python 3.10

* Thu Oct 14 2021 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.3404-2
- remove filetype plugin from virc - it doesn't work with vi

* Mon Oct 11 2021 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.3404-2
- set system vimrc via compiler macros

* Thu Sep 23 2021 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.3404-2
- remove downstream patch vim-8.0-copypaste.patch - put mouse settings into defaults.vim again

* Mon Sep 06 2021 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.3404-1
- patchlevel 3404

* Wed Sep 01 2021 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.3391-1
- patchlevel 3391

* Mon Aug 23 2021 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.3367-1
- patchlevel 3367

* Mon Aug 16 2021 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.3354-1
- patchlevel 3354

* Mon Aug 09 2021 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.3318-1
- patchlevel 3318

* Thu Aug 05 2021 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.3290-1
- patchlevel 3290

* Mon Aug 02 2021 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.3273-1
- patchlevel 3273

* Mon Jul 26 2021 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.3223-1
- patchlevel 3223

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2:8.2.3182-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jul 19 2021 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.3182-1
- patchlevel 3182

* Mon Jul 12 2021 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.3154-1
- patchlevel 3154

* Mon Jun 28 2021 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.3070-1
- patchlevel 3070

* Fri Jun 25 2021 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.3046-1
- patchlevel 3046

* Thu Jun 24 2021 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.3043-1
- patchlevel 3043
- enable libsodium encryption in Fedora
- require glibc-gconv-extra on F35 and later

* Wed Jun 16 2021 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.3009-1
- patchlevel 3009

* Thu Jun 10 2021 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.2956-2
- 1969936 - Failed to source defaults.vim

* Mon Jun 07 2021 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.2956-1
- patchlevel 2956

* Fri Jun 04 2021 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.2932-1
- patchlevel 2932

* Mon May 24 2021 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.2879-1
- patchlevel 2879

* Fri May 21 2021 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.2875-1
- patchlevel 2875

* Mon May 10 2021 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.2846-1
- patchlevel 2846

* Wed May 05 2021 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.2825-2
- make default-editor built only on Fedora

* Mon May 03 2021 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.2825-1
- patchlevel 2825

* Mon Apr 26 2021 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.2811-1
- patchlevel 2811

* Tue Apr 20 2021 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.2787-1
- patchlevel 2787

* Mon Apr 12 2021 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.2756-1
- patchlevel 2756

* Thu Apr 08 2021 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.2735-1
- patchlevel 2735

* Mon Mar 22 2021 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.2637-1
- patchlevel 2637

* Mon Mar 15 2021 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.2607-1
- patchlevel 2607

* Mon Mar 08 2021 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.2576-1
- patchlevel 2576

* Mon Mar 01 2021 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.2559-1
- patchlevel 2559

* Mon Mar 01 2021 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.2541-2
- 1928442 - vim-enhanced is replacing vim-wrappers-8.2.2465-1

* Mon Feb 22 2021 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.2541-1
- patchlevel 2541
- 1931099 - Build version numbers don't match the actual build patchlevel

* Thu Feb 18 2021 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.2529-1
- patchlevel 2529

* Tue Feb 09 2021 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.2488-1
- patchlevel 2488

* Tue Feb 09 2021 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.2465-2
- remove vim-wrappers, vim is a binary again, vi and view stay as wrappers
- removed vim -> vi functionality, because it cannot be optional and work
  for all cases at the same time

* Mon Feb 08 2021 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.2465-2
- view is not readonly right now, fix it by -R

* Thu Feb 04 2021 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.2465-1
- patchlevel 2465
- 1918575 - Use wrappers for vi/vim instead of aliases

* Thu Feb 04 2021 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.2451-2
- vim-update.sh: apply changes master->rawhide

* Tue Feb 02 2021 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.2451-1
- patchlevel 2451

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2:8.2.2311-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 11 2021 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.2311-2
- conflicting the version when the change happened doesnt make sense

* Fri Jan 08 2021 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.2311-1
- patchlevel 2311

* Fri Dec 18 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.2146-2
- install vim-minimal profiles under different name to avoid future conflicts
- remove old conflicts

* Wed Dec 16 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.2146-1
- patchlevel 2146

* Wed Dec 16 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.2143-2
- make profile files as ghosts to prevent further conflicts
- remove ownership of /etc/profile.d - rpmlinter reports it as an error
- remove interactive prompt from profile scripts

* Mon Dec 14 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.2143-1
- patchlevel 2143

* Mon Dec 14 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.2115-2
- 1907335 - installing vim no longer works, due to package conflicts with vim-minimal

* Wed Dec 09 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.2115-1
- patchlevel 2115

* Wed Dec 09 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.2108-2
- 1902772 - "vim" from vim-minimal defunct on zsh

* Tue Dec 08 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.2108-1
- patchlevel 2108

* Fri Dec 04 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.2086-1
- patchlevel 2086

* Tue Dec 01 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.2072-1
- patchlevel 2072

* Fri Nov 20 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.2018-1
- patchlevel 2018

* Tue Nov 10 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.1971-1
- patchlevel 1971

* Fri Nov 06 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.1961-1
- patchlevel 1961

* Thu Nov 05 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.1941-2
- make is no longer in buildroot by default
- disable F31 updating

* Mon Nov 02 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.1941-1
- patchlevel 1941

* Mon Nov 02 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.1885-2
- move vim.fish to vendor_functions.d

* Thu Oct 22 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.1885-1
- patchlevel 1885

* Mon Oct 19 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.1815-2
- vim.sh, vim.csh, vim.fish - drop 'which', use 'command'

* Thu Oct 15 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.1815-2
- vim-default-editor.fish - dont give EDITOR universal scope
- vim.sh, vim.csh - set aliases only for OS default vi and vim
- add fish profile for Vim

* Mon Oct 12 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.1815-2
- fix installing fish profile, set virtual provide for default editor
  (thanks Neal Gompa and Kamil Dudka)
- set conflicts to nano-default-editor which doesnt provide system-default-editor

* Fri Oct 09 2020 Paweł Marciniak <sunwire+repo@gmail.com> - 2:8.2.1815-2
- A new subpackage, set vim as a default editor.

* Fri Oct 09 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.1815-1
- patchlevel 1815

* Tue Oct 06 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.1805-1
- patchlevel 1805

* Tue Sep 29 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.1770-1
- patchlevel 1770

* Tue Sep 15 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.1687-1
- patchlevel 1687

* Thu Sep 10 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.1651-1
- patchlevel 1651

* Tue Sep 08 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.1634-1
- patchlevel 1634

* Mon Aug 31 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.1551-1
- patchlevel 1551

* Mon Aug 31 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.1522-3
- F33 has update-testing now

* Tue Aug 25 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.1522-2
- typo in vim-update.sh

* Tue Aug 25 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.1522-1
- patchlevel 1522

* Mon Aug 24 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.1520-1
- patchlevel 1520

* Thu Aug 20 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.1484-2
- explicitly disable canberra for vi and vim

* Wed Aug 19 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.1484-1
- patchlevel 1484

* Tue Aug 18 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.1412-2
- F33 got branched, updates-testing isn't enabled for it yet
- enable sounds for gvim

* Mon Aug 10 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.1412-1
- patchlevel 1412

* Fri Aug 07 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.1382-1
- patchlevel 1382

* Wed Aug 05 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.1359-2
- own directories for icons

* Mon Aug 03 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.1359-1
- patchlevel 1359

* Fri Jul 31 2020 Zane Bitter <zbitter@redhat.com> - 2:8.2.1328-2
- Alias view to "vim -R" when available

* Fri Jul 31 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.1328-1
- patchlevel 1328

* Wed Jul 29 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.1307-2
- 1703774 - ex, view and rview manpages were dangling symlinks

* Tue Jul 28 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.1307-1
- patchlevel 1307

* Fri Jul 24 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.1273-2
- vim-update.sh: bodhi no longer sets a default automatic time to stable

* Thu Jul 23 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.1273-1
- patchlevel 1273

* Thu Jul 23 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.1224-4
- python3 dynamic linking patch is already in upstream, remove it

* Wed Jul 22 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.1224-3
- use %%make_build and %%make_install according FPG

* Thu Jul 16 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.1224-2
- proper fix for python3 dynamic linking

* Thu Jul 16 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.1224-1
- patchlevel 1224

* Wed Jul 15 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.1217-1
- patchlevel 1217

* Wed Jul 15 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.1199-1
- fix python3 dynamic linking with python >= 3.8
- clean up unused stuff

* Tue Jul 14 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.1199-1
- FTBFS with Lua - backported patch from upstream pull request to prevent linking with lua

* Mon Jul 13 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.1199-1
- patchlevel 1199

* Mon Jun 29 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.1081-1
- patchlevel 1081

* Thu Jun 25 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.1052-2
- remove python2 stuff for RHEL
- %%{fedora} macro is undefined in ELN, causes python3-config to use old options

* Thu Jun 25 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.1052-1
- patchlevel 1052

* Fri Jun 19 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.1009-1
- patchlevel 1009

* Wed Jun 17 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.993-1
- patchlevel 993

* Tue Jun 16 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.987-1
- patchlevel 987

* Fri Jun 05 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.905-1
- patchlevel 905

* Tue Jun 02 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.869-2
- remove tests from dist-git, we use base os ci

* Mon Jun 01 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.869-1
- patchlevel 869

* Thu May 28 2020 Miro Hrončok <mhroncok@redhat.com> - 2:8.2.834-2
- Rebuilt for Python 3.9

* Thu May 28 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.834-1
- patchlevel 834

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 2:8.2.806-2
- Rebuilt for Python 3.9

* Fri May 22 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.806-1
- patchlevel 806

* Mon May 18 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.789-1
- patchlevel 789

* Thu May 14 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.752-2
- F30 will be EOL in less than 14 days, remove it from automatic updates

* Thu May 14 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.752-1
- patchlevel 752

* Mon May 11 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.735-1
- patchlevel 735

* Mon May 04 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.694-1
- patchlevel 694

* Fri Apr 24 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.628-1
- patchlevel 628

* Tue Apr 21 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.613-1
- patchlevel 613

* Fri Apr 17 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.587-1
- patchlevel 587

* Thu Apr 09 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.534-1
- patchlevel 534

* Tue Apr 07 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.525-1
- patchlevel 525

* Mon Apr 06 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.520-1
- patchlevel 520

* Mon Mar 30 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.480-1
- patchlevel 480

* Thu Mar 26 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.448-1
- patchlevel 448

* Wed Mar 25 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.444-1
- patchlevel 444

* Mon Mar 16 2020 Lubomir Rintel <lkundrak@v3.sk> - 2:8.2.390-2
- source /etc/vimrc.local if it exists

* Mon Mar 16 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.390-1
- patchlevel 390

* Tue Mar 10 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.357-2
- put providing bundled libvterm into subpackage vim-enhanced

* Fri Mar 06 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.357-1
- patchlevel 357

* Thu Mar 05 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.356-1
- patchlevel 356

* Tue Mar 03 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.348-1
- patchlevel 348

* Thu Feb 13 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.236-2
- F32 got branched - do separate update for it

* Mon Feb 10 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.236-1
- patchlevel 236

* Wed Jan 29 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.158-2
- man page file format conversion is not needed anymore

* Mon Jan 27 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.158-1
- patchlevel 158

* Fri Jan 10 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.109-1
- patchlevel 109

* Thu Jan 02 2020 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.076-1
- patchlevel 076

* Wed Dec 18 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.019-1
- patchlevel 019

* Mon Dec 16 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.2.012-1
- patchlevel 012

* Thu Dec 12 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.2424-1
- patchlevel 2424

* Thu Nov 28 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.2352-1
- patchlevel 2352

* Thu Nov 28 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.2267-2
- leave out f29, will be soon EOL

* Thu Nov 07 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.2267-1
- patchlevel 2267

* Wed Nov 06 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.2234-2
- do not add python-libs into LDFLAGS until we build vim and gvim

* Wed Oct 30 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.2234-1
- patchlevel 2234

* Tue Oct 22 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.2198-1
- patchlevel 2198

* Mon Oct 21 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.2197-1
- patchlevel 2197

* Thu Oct 17 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.2168-1
- patchlevel 2168

* Mon Oct 07 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.2120-1
- patchlevel 2120

* Mon Sep 30 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.2102-1
- patchlevel 2102

* Thu Sep 19 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.2056-1
- patchlevel 2056

* Mon Sep 16 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.2019-2
- enable fips warning

* Tue Sep 10 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.2019-1
- patchlevel 2019

* Fri Sep 06 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.1991-2
- add f32 as rawhide and f31 as standalone branch

* Fri Sep 06 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.1991-1
- patchlevel 1991

* Tue Sep 03 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.1912-3
- 1744956 - vim does not build with python3.8

* Mon Aug 26 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.1912-2
- remove python2 interpreter - python2 will be retired soon.
- use 'file' with '--mime' option - output is more stable

* Fri Aug 23 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.1912-1
- patchlevel 1912

* Fri Aug 23 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.1890-2
- revert vimx removal

* Tue Aug 20 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.1890-1
- patchlevel 1890

* Tue Aug 20 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.1790-2
- 1740892 - vimx is symlink to gvim instead of vim

* Fri Aug 02 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.1790-1
- patchlevel 1790

* Fri Jul 26 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.1749-1
- patchlevel 1749

* Tue Jul 23 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.1713-6
- Provides must be unversioned according FPG

* Mon Jul 22 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.1713-5
- remove perl-libs, because they are supplied perl MODULE_COMPAT

* Fri Jul 19 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.1713-4
- remove unused patch

* Fri Jul 19 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.1713-3
- 1724126 - disable showing spec template for new file with .spec suffix
- minor changes in spec.template - tabs->spaces

* Fri Jul 19 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.1713-2
- remove skip_defaults_vim - it does not make sense to have it in system vimrc

* Thu Jul 18 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.1713-1
- patchlevel 1713

* Thu Jul 18 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.1661-2
- 1643311 - add several defaults from Vim upstream and remove forcing fileencodings

* Thu Jul 11 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.1661-1
- patchlevel 1661

* Fri Jun 28 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.1602-1
- patchlevel 1602

* Mon Jun 17 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.1561-1
- patchlevel 1561

* Tue Jun 11 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.1517-1
- patchlevel 1517

* Tue Jun 11 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.1471-2
- remove desktop patch, already in upstream

* Thu Jun 06 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.1471-1
- patchlevel 1471

* Tue May 28 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.1413-1
- patchlevel 1413

* Mon May 20 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.1359-2
- stop updating f28

* Mon May 20 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.1359-1
- patchlevel 1359

* Mon May 20 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.1137-2
- remove upstream patch

* Mon Apr 08 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.1137-1
- patchlevel 1137

* Mon Apr 08 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.1099-2
- 1697104 - new spec file template contains deprecated tags

* Tue Apr 02 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.1099-1
- patchlevel 1099

* Tue Mar 26 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.1048-2
- add bundled libvterm

* Mon Mar 25 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.1048-1
- patchlevel 1048

* Fri Mar 08 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.998-1
- patchlevel 998

* Fri Mar 08 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.994-2
- F30 is already active in bodhi 

* Mon Mar 04 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.994-1
- patchlevel 994

* Wed Feb 20 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.956-1
- patchlevel 956

* Wed Feb 20 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.918-2
- we have Fedora 30 branch now, enable updates for it in vim-update.sh

* Thu Feb 14 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.918-1
- patchlevel 918

* Thu Feb 14 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.897-2
- we do not need exact include path for python3 now

* Tue Feb 12 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.897-1
- patchlevel 897

* Fri Feb 08 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.880-1
- patchlevel 880

* Mon Feb 04 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.873-1
- patchlevel 873

* Mon Feb 04 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.847-4
- remove downstream fix for new ruby, upstream solved it different way

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2:8.1.847-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 31 2019  Karsten Hopp <karsten@redhat.com> - 2:8.1.847-2
- remove ancient Changelog.rpm

* Wed Jan 30 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.847-2
- fix patch for new ruby-2.6

* Wed Jan 30 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.847-1
- patchlevel 847

* Tue Jan 29 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.837-2
- FTBFS with new ruby-2.6

* Mon Jan 28 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.837-1
- patchlevel 837

* Fri Jan 25 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.818-1
- patchlevel 818

* Tue Jan 22 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.789-1
- patchlevel 789

* Fri Jan 11 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.714-1
- patchlevel 714

* Tue Jan 08 2019 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.702-1
- patchlevel 702

* Mon Dec 10 2018 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.575-1
- patchlevel 575

* Wed Dec 05 2018 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.549-2
- do not strip binaries before build system strips it

* Tue Nov 27 2018 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.549-1
- patchlevel 549

* Tue Nov 27 2018 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.527-2
- update vim-update.sh - F27 EOL

* Fri Nov 16 2018 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.527-1
- patchlevel 527

* Thu Nov 08 2018 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.513-2
- #1646183 - do not forget the epoch

* Thu Nov 08 2018 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.513-1
- patchlevel 513

* Thu Nov 08 2018 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.511-2
- fix #1646183 properly - we need to conflict with vim-enhanced, not vim-common

* Mon Nov 05 2018 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.511-1
- patchlevel 511

* Mon Nov 05 2018 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.497-2
- 1646183 - Man file conflict for vim-minimal and vim-enhanced

* Fri Oct 26 2018 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.497-1
- patchlevel 497

* Fri Oct 19 2018 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.483-1
- patchlevel 483

* Fri Oct 19 2018 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.451-2
- 1640972 - vimrc/virc should reflect correct augroup

* Fri Oct 05 2018 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.451-1
- patchlevel 451

* Wed Oct 03 2018 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.450-1
- patchlevel 450

* Wed Sep 19 2018 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.408-1
- patchlevel 408
- src/libvterm/src/termscreen.c is missing

* Fri Sep 07 2018 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.351-1
- patchlevel 351

* Fri Aug 31 2018 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.328-2
- vim-update.sh - F29 got enabled in bodhi

* Mon Aug 27 2018 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.328-1
- patchlevel 328

* Wed Aug 15 2018 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.287-2
- vim-update.sh - add f29 branch

* Wed Aug 15 2018 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.287-1
- patchlevel 287

* Mon Aug 13 2018 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.279-1
- patchlevel 279

* Fri Aug 10 2018 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.264-1
- patchlevel 264

* Thu Aug 09 2018 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.258-1
- patchlevel 258

* Wed Aug 08 2018 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.254-1
- patchlevel 254

* Mon Aug 06 2018 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.240-1
- patchlevel 240

* Thu Aug 02 2018 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.233-1
- patchlevel 233

* Tue Jul 31 2018 Florian Weimer <fweimer@redhat.com> - 2:8.1.229-2
- Rebuild with fixed binutils

* Mon Jul 30 2018 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.229-1
- patchlevel 229

* Fri Jul 27 2018 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.213-1
- patchlevel 213

* Fri Jul 27 2018 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.209-2
- fail if configure option isn't satisfied

* Wed Jul 25 2018 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.209-1
- patchlevel 209

* Tue Jul 24 2018 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.207-2
- correcting license

* Mon Jul 23 2018 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.207-1
- patchlevel 207

* Fri Jul 20 2018 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.197-1
- patchlevel 197

* Thu Jul 19 2018 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.189-2
- 1603272 - vim-X11 doesn't provide the gui when certain devel packages missing from buildroot

* Mon Jul 16 2018 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.189-1
- patchlevel 189

* Mon Jul 16 2018 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.177-3
- remove disable-gtk3-check configure option

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2:8.1.177-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.177-1
- patchlevel 177

* Wed Jul 11 2018 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.119-8
- add packager and epoch into update script to have better changelog

* Wed Jul 11 2018 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.119-7
- use %%{__python3} macro for defining shebang in python3 tests

* Tue Jul 10 2018 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.1.119-6
- 1599663 - Conflicting manpages rvi.1.gz and vi.1.gz during update

* Fri Jul 06 2018 Petr Pisar <ppisar@redhat.com> - 2:8.1.119-5
- Perl 5.28 rebuild

* Wed Jul 04 2018 Ondřej Lysoněk <olysonek@redhat.com> - 2:8.1.119-4
- Backport patch 8.1.0121: crash when using ballooneval related to 'vartabstop'
- Resolves: rhbz#1597842

* Tue Jul 03 2018 Petr Pisar <ppisar@redhat.com> - 2:8.1.119-3
- Perl 5.28 rebuild

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 2:8.1.119-2
- Rebuilt for Python 3.7

* Thu Jun 28 2018 Karsten Hopp <karsten@redhat.com> 8.1.119-1
- patchlevel 119

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2:8.1.117-2
- Perl 5.28 rebuild

* Wed Jun 27 2018 Karsten Hopp <karsten@redhat.com> 8.1.117-1
- patchlevel 117

* Mon Jun 25 2018 Karsten Hopp <karsten@redhat.com> 8.1.115-1
- patchlevel 115

* Fri Jun 22 2018 Karsten Hopp <karsten@redhat.com> 8.1.095-1
- patchlevel 095

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 2:8.1.072-2
- Rebuilt for Python 3.7

* Mon Jun 18 2018 Karsten Hopp <karsten@redhat.com> 8.1.072-1
- patchlevel 072

* Fri Jun 15 2018 Karsten Hopp <karsten@redhat.com> 8.1.055-1
- patchlevel 055

* Mon Jun 11 2018 Karsten Hopp <karsten@redhat.com> 8.1.042-1
- patchlevel 042

* Fri Jun 08 2018 Karsten Hopp <karsten@redhat.com> 8.1.039-1
- patchlevel 039

* Wed Jun 06 2018 Karsten Hopp <karsten@redhat.com> 8.1.035-1
- patchlevel 035

* Tue Jun 05 2018 Karsten Hopp <karsten@redhat.com> 8.1.034-1
- patchlevel 034

* Mon May 28 2018 Karsten Hopp <karsten@redhat.com> 8.1.026-1
- patchlevel 026

* Thu May 24 2018 Karsten Hopp <karsten@redhat.com> 8.1.022-1
- patchlevel 022

* Wed May 23 2018 Karsten Hopp <karsten@redhat.com> 8.1.020-1
- patchlevel 020

* Tue May 22 2018 Karsten Hopp <karsten@redhat.com> 8.1.016-1
- patchlevel 016

* Mon May 21 2018 Karsten Hopp <karsten@redhat.com> 8.1.010-1
- patchlevel 010

* Fri May 18 2018 Karsten Hopp <karsten@redhat.com> 8.1.001-1
- patchlevel 001

* Fri May 18 2018 Zdenek Dohnal <zdohnal@redhat.com> - 8.0.1848-2
- vim-update.sh - update vimdir and baseversion(for major rebases)
- vim-update.sh - enhance debugging of vim-update script

* Thu May 17 2018 Karsten Hopp <karsten@redhat.com> 8.0.1848-1
- patchlevel 1848

* Tue May 15 2018 Zdenek Dohnal <zdohnal@redhat.com> - 8.0.1842-2
- do not update F26 anymore - EOL in 2 weeks

* Tue May 15 2018 Karsten Hopp <karsten@redhat.com> 8.0.1842-1
- patchlevel 1842

* Tue May 15 2018 Zdenek Dohnal <zdohnal@redhat.com> - 8.0.1813-2
- use environment variable in build phase

* Fri May 11 2018 Karsten Hopp <karsten@redhat.com> 8.0.1813-1
- patchlevel 1813

* Fri May 11 2018 Zdenek Dohnal <zdohnal@redhat.com> - 8.0.1806-2
- use python2 and python3 in code

* Thu May 10 2018 Karsten Hopp <karsten@redhat.com> 8.0.1806-1
- patchlevel 1806

* Wed May 09 2018 Zdenek Dohnal <zdohnal@redhat.com> - 8.0.1789-2
- 1575354 - suggest more packages for embedded interpreters

* Fri May 04 2018 Karsten Hopp <karsten@redhat.com> 8.0.1789-1
- patchlevel 1789

* Thu May 03 2018 Karsten Hopp <karsten@redhat.com> 8.0.1788-1
- patchlevel 1788

* Wed May 02 2018 Karsten Hopp <karsten@redhat.com> 8.0.1787-1
- patchlevel 1787

* Fri Apr 27 2018 Karsten Hopp <karsten@redhat.com> 8.0.1766-1
- patchlevel 1766

* Thu Apr 26 2018 Karsten Hopp <karsten@redhat.com> 8.0.1765-1
- patchlevel 1765

* Wed Apr 25 2018 Karsten Hopp <karsten@redhat.com> 8.0.1763-1
- patchlevel 1763

* Tue Apr 24 2018 Karsten Hopp <karsten@redhat.com> 8.0.1755-1
- patchlevel 1755

* Fri Apr 13 2018 Karsten Hopp <karsten@redhat.com> 8.0.1704-1
- patchlevel 1704

* Mon Apr 09 2018 Karsten Hopp <karsten@redhat.com> 8.0.1679-1
- patchlevel 1679

* Fri Apr 06 2018 Zdenek Dohnal <zdohnal@redhat.com> - 8.0.1666-2
- suggests ruby-libs, python2-libs, python3-libs, perl-libs and lua-libs for vim and gvim(bug #1562057)

* Fri Apr 06 2018 Karsten Hopp <karsten@redhat.com> 8.0.1666-1
- patchlevel 1666

* Thu Apr 05 2018 Karsten Hopp <karsten@redhat.com> 8.0.1661-1
- patchlevel 1661

* Fri Mar 23 2018 Karsten Hopp <karsten@redhat.com> 8.0.1630-1
- patchlevel 1630

* Thu Mar 22 2018 Karsten Hopp <karsten@redhat.com> 8.0.1626-1
- patchlevel 1626

* Wed Mar 21 2018 Karsten Hopp <karsten@redhat.com> 8.0.1625-1
- patchlevel 1625

* Wed Mar 14 2018 Karsten Hopp <karsten@redhat.com> 8.0.1605-1
- patchlevel 1605

* Tue Mar 13 2018 Karsten Hopp <karsten@redhat.com> 8.0.1603-1
- patchlevel 1603

* Mon Mar 12 2018 Karsten Hopp <karsten@redhat.com> 8.0.1599-1
- patchlevel 1599

* Fri Mar 09 2018 Karsten Hopp <karsten@redhat.com> 8.0.1591-1
- patchlevel 1591

* Thu Mar 08 2018 Karsten Hopp <karsten@redhat.com> 8.0.1589-1
- patchlevel 1589

* Wed Mar 07 2018 Karsten Hopp <karsten@redhat.com> 8.0.1587-1
- patchlevel 1587

* Tue Mar 06 2018 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.0.1573-2
- vim-update.sh - unify if condition style

* Tue Mar 06 2018 Karsten Hopp <karsten@redhat.com> 8.0.1573-1
- patchlevel 1573

* Tue Mar 06 2018 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.0.1569-2
- update spec
- f28 got enabled in bodhi

* Mon Mar 05 2018 Karsten Hopp <karsten@redhat.com> 8.0.1569-1
- patchlevel 1569

* Wed Feb 28 2018 Karsten Hopp <karsten@redhat.com> 8.0.1553-1
- added Serbian localization files
- patchlevel 1553

* Wed Feb 28 2018 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.0.1543-2
- fix vim-update.sh - bodhi update wasn't created

* Tue Feb 27 2018 Karsten Hopp <karsten@redhat.com> 8.0.1543-1
- patchlevel 1543

* Mon Feb 26 2018 Zdenek Dohnal <zdohnal@redhat.com> - 8.0.1527-3
- add Provides for vim, gvim and correcting paths to /usr/bin

* Wed Feb 21 2018 Zdenek Dohnal <zdohnal@redhat.com> - 8.0.1527-2
- adapt vim-update.sh for Fedora 28 and adding check for bodhi enablement

* Tue Feb 20 2018 Karsten Hopp <karsten@redhat.com> 8.0.1527-1
- patchlevel 1527

* Mon Feb 19 2018 Zdenek Dohnal <zdohnal@redhat.com> - 8.0.1523-2
- gcc is no longer in buildroot by default
- 1546116 - make vim-filesystem noarch package
- remove %%{_libdir}/vim, because it is unused

* Mon Feb 19 2018 Karsten Hopp <karsten@redhat.com> 8.0.1523-1
- patchlevel 1523

* Wed Feb 14 2018 Karsten Hopp <karsten@redhat.com> 8.0.1520-1
- patchlevel 1520

* Tue Feb 13 2018 Karsten Hopp <karsten@redhat.com> 8.0.1509-1
- patchlevel 1509

* Mon Feb 12 2018 Karsten Hopp <karsten@redhat.com> 8.0.1505-1
- patchlevel 1505

* Fri Feb 09 2018 Karsten Hopp <karsten@redhat.com> 8.0.1478-1
- patchlevel 1478

* Thu Feb 08 2018 Zdenek Dohnal <zdohnal@redhat.com> - 8.0.1475-2
- remove old stuff

* Wed Feb 07 2018 Karsten Hopp <karsten@redhat.com> 8.0.1475-1
- patchlevel 1475

* Mon Feb 05 2018 Karsten Hopp <karsten@redhat.com> 8.0.1473-1
- patchlevel 1473

* Thu Feb 01 2018 Karsten Hopp <karsten@redhat.com> 8.0.1451-1
- patchlevel 1451

* Mon Jan 29 2018 Karsten Hopp <karsten@redhat.com> 8.0.1438-1
- patchlevel 1438

* Tue Jan 23 2018 Zdenek Dohnal <zdohnal@redhat.com> - 8.0.1428-4
- throw vim.1.gz out from vim-minimal and other manpages from vim-common
- appdata should be in metainfo folder now

* Fri Jan 19 2018 Zdenek Dohnal <zdohnal@redhat.com> - 8.0.1428-3
- 1525506 - gvim goes into infinite loop when blink_state is OFF

* Fri Jan 12 2018 Zdenek Dohnal <zdohnal@redhat.com> - 8.0.1428-2
- removing old icon cache update

* Wed Jan 03 2018 Karsten Hopp <karsten@redhat.com> 8.0.1428-1
- patchlevel 1428

* Tue Jan 02 2018 Karsten Hopp <karsten@redhat.com> 8.0.1427-1
- patchlevel 1427

* Tue Dec 19 2017 Karsten Hopp <karsten@redhat.com> 8.0.1406-1
- patchlevel 1406

* Mon Dec 18 2017 Karsten Hopp <karsten@redhat.com> 8.0.1401-1
- patchlevel 1401

* Fri Dec 15 2017 Karsten Hopp <karsten@redhat.com> 8.0.1390-1
- patchlevel 1390

* Fri Dec 15 2017 Zdenek Dohnal <zdohnal@redhat.com> - 8.0.1389-2
- fixing vim-update.sh

* Wed Dec 13 2017 Karsten Hopp <karsten@redhat.com> 8.0.1389-1
- patchlevel 1389

* Tue Dec 12 2017 Karsten Hopp <karsten@redhat.com> 8.0.1387-1
- patchlevel 1387

* Mon Dec 11 2017 Karsten Hopp <karsten@redhat.com> 8.0.1386-1
- patchlevel 1386

* Fri Dec 08 2017 Karsten Hopp <karsten@redhat.com> 8.0.1379-1
- patchlevel 1379

* Wed Dec 06 2017 Karsten Hopp <karsten@redhat.com> 8.0.1376-1
- patchlevel 1376

* Mon Dec 04 2017 Zdenek Dohnal <zdohnal@redhat.com> - 8.0.1367-2
- fix regexp in vim-update.sh

* Mon Dec 04 2017 Karsten Hopp <karsten@redhat.com> 8.0.1367-1
- patchlevel 1367

* Fri Dec 01 2017 Zdenek Dohnal <zdohnal@redhat.com> - 8.0.1360-2
- fix in vim-update.sh

* Fri Dec 01 2017 Karsten Hopp <karsten@redhat.com> 8.0.1360-1
- patchlevel 1360

* Fri Dec 01 2017 Zdenek Dohnal <zdohnal@redhat.com> - 8.0.1359-3
- rewrite vim-update to update from the newest branch to the oldest

* Thu Nov 30 2017 Zdenek Dohnal <zdohnal@redhat.com> - 8.0.1359-2
- 1508629 - missing full path and safe guards in file triggers in -common

* Thu Nov 30 2017 Karsten Hopp <karsten@redhat.com> 8.0.1359-1
- patchlevel 1359

* Wed Nov 29 2017 Karsten Hopp <karsten@redhat.com> 8.0.1358-1
- patchlevel 1358
- fix error in vim-update.sh

* Tue Nov 28 2017 Karsten Hopp <karsten@redhat.com> 8.0.1351-1
- patchlevel 1351

* Mon Nov 27 2017 Karsten Hopp <karsten@redhat.com> 8.0.1349-1
- patchlevel 1349

* Mon Nov 27 2017 Zdenek Dohnal <zdohnal@redhat.com> - 8.0.1330-2
- removing vim-8.0-beval-pro.patch and stop updating f25

* Wed Nov 22 2017 Karsten Hopp <karsten@redhat.com> 8.0.1330-1
- patchlevel 1330

* Tue Nov 21 2017 Karsten Hopp <karsten@redhat.com> 8.0.1326-1
- patchlevel 1326

* Mon Nov 20 2017 Karsten Hopp <karsten@redhat.com> 8.0.1322-1
- patchlevel 1322

* Fri Nov 10 2017 Karsten Hopp <karsten@redhat.com> 8.0.1283-1
- patchlevel 1283

* Tue Nov 07 2017 Karsten Hopp <karsten@redhat.com> 8.0.1274-1
- patchlevel 1274

* Mon Nov 06 2017 Karsten Hopp <karsten@redhat.com> 8.0.1272-1
- patchlevel 1272

* Fri Nov 03 2017 Karsten Hopp <karsten@redhat.com> 8.0.1257-1
- patchlevel 1257

* Wed Nov 01 2017 Karsten Hopp <karsten@redhat.com> 8.0.1241-1
- patchlevel 1241

* Tue Oct 31 2017 Karsten Hopp <karsten@redhat.com> 8.0.1240-1
- patchlevel 1240

* Mon Oct 30 2017 Karsten Hopp <karsten@redhat.com> 8.0.1238-1
- patchlevel 1238

* Fri Oct 27 2017 Karsten Hopp <karsten@redhat.com> 8.0.1226-1
- patchlevel 1226

* Thu Oct 26 2017 Zdenek Dohnal <zdohnal@redhat.com> - 8.0.1216-2
- mention GVim in Summary and Description of vim-x11 subpackage

* Wed Oct 25 2017 Karsten Hopp <karsten@redhat.com> 8.0.1216-1
- patchlevel 1216

* Mon Oct 23 2017 Karsten Hopp <karsten@redhat.com> 8.0.1213-1
- patchlevel 1213

* Fri Oct 20 2017 Karsten Hopp <karsten@redhat.com> 8.0.1207-1
- patchlevel 1207

* Mon Oct 16 2017 Karsten Hopp <karsten@redhat.com> 8.0.1203-1
- patchlevel 1203

* Fri Oct 13 2017 Karsten Hopp <karsten@redhat.com> 8.0.1187-1
- patchlevel 1187

* Mon Oct 09 2017 Karsten Hopp <karsten@redhat.com> 8.0.1184-1
- patchlevel 1184

* Fri Oct 06 2017 Karsten Hopp <karsten@redhat.com> 8.0.1176-1
- patchlevel 1176

* Thu Oct 05 2017 Karsten Hopp <karsten@redhat.com> 8.0.1175-1
- patchlevel 1175

* Tue Oct 03 2017 Karsten Hopp <karsten@redhat.com> 8.0.1173-1
- patchlevel 1173

* Mon Oct 02 2017 Karsten Hopp <karsten@redhat.com> 8.0.1171-1
- patchlevel 1171

* Wed Sep 27 2017 Karsten Hopp <karsten@redhat.com> 8.0.1155-1
- patchlevel 1155

* Tue Sep 26 2017 Zdenek Dohnal <zdohnal@redhat.com> - 8.0.1144-2
- removing README.patches

* Mon Sep 25 2017 Karsten Hopp <karsten@redhat.com> 8.0.1144-1
- patchlevel 1144

* Fri Sep 22 2017 Karsten Hopp <karsten@redhat.com> 8.0.1132-1
- patchlevel 1132

* Wed Sep 20 2017 Zdenek Dohnal <zdohnal@redhat.com> - 8.0.1129-2
- vim-update.sh - update was in bad form

* Wed Sep 20 2017 Karsten Hopp <karsten@redhat.com> 8.0.1129-1
- patchlevel 1129

* Wed Sep 20 2017 Zdenek Dohnal <zdohnal@redhat.com> - 8.0.1127-2
- vim-update.sh - update script tried to push for previous version

* Tue Sep 19 2017 Karsten Hopp <karsten@redhat.com> 8.0.1127-1
- patchlevel 1127

* Tue Sep 19 2017 Zdenek Dohnal <zdohnal@redhat.com> - 8.0.1123-2
- vim-update.sh - fixing bug with submiting update (update got submitted for previous version)

* Mon Sep 18 2017 Karsten Hopp <karsten@redhat.com> 8.0.1123-1
- patchlevel 1123

* Thu Sep 14 2017 Karsten Hopp <karsten@redhat.com> 8.0.1102-1
- vim-update.sh - add test for succesful build and fixing grepping of update's list
- patchlevel 1102

* Wed Sep 13 2017 Karsten Hopp <karsten@redhat.com> 8.0.1098-1
- editing vim-update.sh - check updates for newer releases and create update
- patchlevel 1098

* Tue Sep 12 2017 Karsten Hopp <karsten@redhat.com> 8.0.1097-1
- patchlevel 1097
- editing vim-update.sh - wrong condition for checking fedkpg push return value

* Mon Sep 11 2017 Karsten Hopp <karsten@redhat.com> 8.0.1092-1
- editing vim-update.sh for building package
- patchlevel 1092
- 1487175 - VIm conflicts in man pages

* Fri Sep 08 2017 Zdenek Dohnal <zdohnal@redhat.com> - 8.0.1071-2
- fixing merge and push in vim-update.sh

* Fri Sep 08 2017 Karsten Hopp <karsten@redhat.com> 8.0.1071-1
- patchlevel 1071

* Fri Sep 08 2017 Zdenek Dohnal <zdohnal@redhat.com> - 8.0.1067-2
- editing vim-update.sh to do whole update automatically

* Thu Sep 07 2017 Karsten Hopp <karsten@redhat.com> 8.0.1067-1
- patchlevel 1067

* Wed Sep 06 2017 Karsten Hopp <karsten@redhat.com> 8.0.1064-1
- patchlevel 1064

* Tue Sep 05 2017 Karsten Hopp <karsten@redhat.com> 8.0.1056-1
- patchlevel 1056

* Mon Sep 04 2017 Karsten Hopp <karsten@redhat.com> 8.0.1052-1
- patchlevel 1052

* Fri Sep 01 2017 Karsten Hopp <karsten@redhat.com> 8.0.1030-1
- patchlevel 1030

* Thu Aug 24 2017 Karsten Hopp <karsten@redhat.com> 8.0.992-1
- patchlevel 992

* Wed Aug 23 2017 Karsten Hopp <karsten@redhat.com> 8.0.987-1
- patchlevel 987

* Tue Aug 22 2017 Karsten Hopp <karsten@redhat.com> 8.0.983-1
- patchlevel 983

* Fri Aug 18 2017 Karsten Hopp <karsten@redhat.com> 8.0.956-1
- patchlevel 956

* Tue Aug 15 2017 Karsten Hopp <karsten@redhat.com> 8.0.946-1
- patchlevel 946

* Mon Aug 14 2017 Karsten Hopp <karsten@redhat.com> 8.0.938-1
- patchlevel 938

* Fri Aug 11 2017 Karsten Hopp <karsten@redhat.com> 8.0.896-1
- patchlevel 896

* Thu Aug 10 2017 Karsten Hopp <karsten@redhat.com> 8.0.895-1
- patchlevel 895

* Wed Aug 09 2017 Karsten Hopp <karsten@redhat.com> 8.0.893-1
- patchlevel 893

* Wed Aug 09 2017 Zdenek Dohnal <zdohnal@redhat.com> 8.0.891-2
- editing vim-update.sh - now it takes branch name as argument for switching and run mockbuild

* Tue Aug 08 2017 Karsten Hopp <karsten@redhat.com> 8.0.891-1
- patchlevel 891

* Mon Aug 07 2017 Karsten Hopp <karsten@redhat.com> 8.0.885-1
- patchlevel 885

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2:8.0.844-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Aug 03 2017 Karsten Hopp <karsten@redhat.com> 8.0.844-1
- patchlevel 844

* Tue Aug 01 2017 Karsten Hopp <karsten@redhat.com> 8.0.826-1
- patchlevel 826

* Mon Jul 31 2017 Karsten Hopp <karsten@redhat.com> 8.0.823-1
- patchlevel 823

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2:8.0.739-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 21 2017 Karsten Hopp <karsten@redhat.com> 8.0.739-1
- patchlevel 739

* Thu Jul 20 2017 Karsten Hopp <karsten@redhat.com> 8.0.738-1
- patchlevel 738

* Wed Jul 19 2017 Karsten Hopp <karsten@redhat.com> 8.0.730-1
- patchlevel 730

* Tue Jul 18 2017 Karsten Hopp <karsten@redhat.com> 8.0.728-1
- patchlevel 728

* Thu Jul 13 2017 Karsten Hopp <karsten@redhat.com> 8.0.711-1
- patchlevel 711

* Tue Jul 11 2017 Karsten Hopp <karsten@redhat.com> 8.0.705-1
- patchlevel 705

* Fri Jun 30 2017 Karsten Hopp <karsten@redhat.com> 8.0.691-1
- patchlevel 691

* Thu Jun 29 2017 Karsten Hopp <karsten@redhat.com> 8.0.688-1
- patchlevel 688

* Thu Jun 29 2017 Zdenek Dohnal <zdohnal@redhat.com> - 8.0.685-3
- update python dependencies accordingly Fedora Guidelines for Python (python-devel -> python2-devel)

* Wed Jun 28 2017 Karsten Hopp <karsten@redhat.com> 8.0.685-1
- patchlevel 685

* Mon Jun 26 2017 Karsten Hopp <karsten@redhat.com> 8.0.679-1
- patchlevel 679

* Fri Jun 23 2017 Karsten Hopp <karsten@redhat.com> 8.0.662-1
- patchlevel 662

* Tue Jun 20 2017 Karsten Hopp <karsten@redhat.com> 8.0.648-1
- patchlevel 648

* Mon Jun 19 2017 Karsten Hopp <karsten@redhat.com> 8.0.647-1
- patchlevel 647

* Thu Jun 15 2017 Karsten Hopp <karsten@redhat.com> 8.0.642-1
- patchlevel 642

* Mon Jun 12 2017 Karsten Hopp <karsten@redhat.com> 8.0.636-1
- patchlevel 636, removing perl ftbfs patch

* Fri Jun 09 2017 Karsten Hopp <karsten@redhat.com> 8.0.628-1
- patchlevel 628

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2:8.0.627-2
- Perl 5.26 re-rebuild of bootstrapped packages

* Wed Jun 07 2017 Karsten Hopp <karsten@redhat.com> 8.0.627-1
- patchlevel 627

* Mon Jun 05 2017 Karsten Hopp <karsten@redhat.com> 8.0.617-1
- patchlevel 617

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2:8.0.606-3
- Perl 5.26 rebuild

* Mon May 29 2017 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.0.606-2
- 1456455 - vim-8.0.600-1.fc27 FTBFS with Perl 5.26.0 

* Mon May 29 2017 Karsten Hopp <karsten@redhat.com> 8.0.606-1
- patchlevel 606

* Thu May 25 2017 Karsten Hopp <karsten@redhat.com> 8.0.604-1
- patchlevel 604

* Fri May 19 2017 Karsten Hopp <karsten@redhat.com> 8.0.600-1
- patchlevel 600

* Wed May 17 2017 Karsten Hopp <karsten@redhat.com> 8.0.599-1
- patchlevel 599

* Tue May 16 2017 Karsten Hopp <karsten@redhat.com> 8.0.598-1
- patchlevel 598

* Mon May 15 2017 Karsten Hopp <karsten@redhat.com> 8.0.597-1
- patchlevel 597

* Tue May 02 2017 Karsten Hopp <karsten@redhat.com> 8.0.596-1
- patchlevel 596

* Mon Apr 24 2017 Karsten Hopp <karsten@redhat.com> 8.0.586-1
- patchlevel 586

* Tue Apr 18 2017 Karsten Hopp <karsten@redhat.com> 8.0.566-1
- patchlevel 566

* Thu Apr 13 2017 Karsten Hopp <karsten@redhat.com> 8.0.563-1
- patchlevel 563

* Tue Apr 11 2017 Karsten Hopp <karsten@redhat.com> 8.0.562-1
- patchlevel 562

* Mon Apr 10 2017 Karsten Hopp <karsten@redhat.com> 8.0.559-1
- patchlevel 559

* Thu Apr 06 2017 Karsten Hopp <karsten@redhat.com> 8.0.543-1
- patchlevel 543

* Mon Apr 03 2017 Karsten Hopp <karsten@redhat.com> 8.0.540-1
- patchlevel 540

* Fri Mar 31 2017 Karsten Hopp <karsten@redhat.com> 8.0.529-1
- patchlevel 529

* Thu Mar 30 2017 Karsten Hopp <karsten@redhat.com> 8.0.525-1
- patchlevel 525

* Wed Mar 29 2017 Karsten Hopp <karsten@redhat.com> 8.0.517-1
- patchlevel 517
- enhance rhbz#1436124

* Tue Mar 28 2017 Karsten Hopp <karsten@redhat.com> 8.0.515-1
- patchlevel 515

* Mon Mar 27 2017 Karsten Hopp <karsten@redhat.com> 8.0.514-1
- patchlevel 514
- 1436124 - VIM chooses ft=bindzone for sudoedit /etc/named.conf

* Fri Mar 24 2017 Karsten Hopp <karsten@redhat.com> 8.0.503-1
- patchlevel 503

* Wed Mar 22 2017 Karsten Hopp <karsten@redhat.com> 8.0.502-1
- patchlevel 502

* Tue Mar 21 2017 Karsten Hopp <karsten@redhat.com> 8.0.497-1
- patchlevel 497

* Mon Mar 20 2017 Karsten Hopp <karsten@redhat.com> 8.0.494-1
- patchlevel 494

* Wed Mar 15 2017 Karsten Hopp <karsten@redhat.com> 8.0.458-1
- patchlevel 458

* Tue Mar 14 2017 Karsten Hopp <karsten@redhat.com> 8.0.456-1
- patchlevel 456

* Fri Mar 10 2017 Karsten Hopp <karsten@redhat.com> 8.0.442-1
- patchlevel 442

* Wed Mar 08 2017 Karsten Hopp <karsten@redhat.com> 8.0.430-1
- patchlevel 430

* Tue Mar 07 2017 Karsten Hopp <karsten@redhat.com> 8.0.427-1
- patchlevel 427

* Mon Mar 06 2017 Karsten Hopp <karsten@redhat.com> 8.0.425-1
- patchlevel 425

* Fri Mar 03 2017 Karsten Hopp <karsten@redhat.com> 8.0.402-1
- patchlevel 402

* Thu Mar 02 2017 Karsten Hopp <karsten@redhat.com> 8.0.398-1
- patchlevel 398

* Wed Mar 01 2017 Karsten Hopp <karsten@redhat.com> 8.0.388-1
- patchlevel 388

* Tue Feb 28 2017 Karsten Hopp <karsten@redhat.com> 8.0.386-1
- patchlevel 386

* Mon Feb 27 2017 Karsten Hopp <karsten@redhat.com> 8.0.381-1
- patchlevel 381

* Fri Feb 24 2017 Karsten Hopp <karsten@redhat.com> 8.0.363-1
- patchlevel 363
- removing vim-8.0-gtk-render.patch

* Fri Feb 24 2017 Karsten Hopp <karsten@redhat.com> 8.0.347-1
- patchlevel 347
- 1405234 - Gvim fails to properly render after Openbox desktop switch
- 1426296 - vim: FTBFS with python3-3.6.0-18.fc26

* Tue Feb 21 2017 Karsten Hopp <karsten@redhat.com> 8.0.344-1
- patchlevel 344

* Mon Feb 20 2017 Karsten Hopp <karsten@redhat.com> 8.0.342-1
- patchlevel 342

* Thu Feb 16 2017 Zdenek Dohnal <zdohnal@redhat.com> 8.0.329-1
- 1422833 - Syntax error in tex.vim: missing bracket

* Mon Feb 13 2017 Karsten Hopp <karsten@redhat.com> 8.0.329-1
- patchlevel 329

* Fri Feb 10 2017 Karsten Hopp <karsten@redhat.com> 8.0.324-1
- patchlevel 324

* Thu Feb 09 2017 Karsten Hopp <karsten@redhat.com> 8.0.318-1
- patchlevel 318

* Tue Feb 07 2017 Karsten Hopp <karsten@redhat.com> 8.0.314-1
- patchlevel 314, added screenshot to appdata and testing validity of appdata.xml

* Mon Feb 06 2017 Karsten Hopp <karsten@redhat.com> 8.0.311-1
- patchlevel 311

* Fri Feb 03 2017 Karsten Hopp <karsten@redhat.com> 8.0.297-1
- patchlevel 297

* Wed Feb 01 2017 Karsten Hopp <karsten@redhat.com> 8.0.275-1
- patchlevel 275

* Tue Jan 31 2017 Karsten Hopp <karsten@redhat.com> 8.0.273-1
- patchlevel 273

* Mon Jan 30 2017 Karsten Hopp <karsten@redhat.com> 8.0.271-1
- patchlevel 271

* Thu Jan 26 2017 Karsten Hopp <karsten@redhat.com> 8.0.238-1
- patchlevel 238

* Thu Jan 19 2017 Karsten Hopp <karsten@redhat.com> 8.0.206-1
- patchlevel 206

* Tue Jan 17 2017 Karsten Hopp <karsten@redhat.com> 8.0.197-1
- patchlevel 197
- update runtime files

* Mon Jan 16 2017 Karsten Hopp <karsten@redhat.com> 8.0.194-1
- patchlevel 194

* Fri Jan 13 2017 Karsten Hopp <karsten@redhat.com> 8.0.176-1
- patchlevel 176

* Thu Jan 12 2017 Karsten Hopp <karsten@redhat.com> 8.0.172-1
- patchlevel 172

* Wed Jan 11 2017 Karsten Hopp <karsten@redhat.com> 8.0.170-1
- patchlevel 170

* Mon Jan 09 2017 Karsten Hopp <karsten@redhat.com> 8.0.160-1
- patchlevel 160

* Tue Jan 03 2017 Karsten Hopp <karsten@redhat.com> 8.0.142-1
- patchlevel 142

* Mon Dec 19 2016 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.0.134-2
- f24->f25 vim: copy paste no longer works (bug #1401410) - fixing error in prep

* Mon Dec 19 2016 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.0.134-2
- f24->f25 vim: copy paste no longer works (bug #1401410) - deleting mouse setting block from defaults.vim

* Mon Dec 19 2016 Karsten Hopp <karsten@redhat.com> 8.0.134-1
- patchlevel 134
- f24->f25 vim: copy paste no longer works (bug #1401410) - revert previous changes, set mouse=v in defaults.vim

* Thu Dec 15 2016 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.0.133-2
- f24->f25 vim: copy paste no longer works (bug #1401410) - change mouse default setting to 'v'

* Thu Dec 15 2016 Karsten Hopp <karsten@redhat.com> - 8.0.133-2
- fix fstab syntax highlighting (rhbz#1365258)

* Mon Dec 12 2016 Karsten Hopp <karsten@redhat.com> 8.0.133-1
- patchlevel 133

* Mon Dec 05 2016 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.0.124-2
- add new sources

* Mon Dec 05 2016 Karsten Hopp <karsten@redhat.com> 8.0.124-1
- patchlevel 124

* Fri Dec 02 2016 Karsten Hopp <karsten@redhat.com> 8.0.118-1
- patchlevel 118

* Mon Nov 28 2016 Zdenek Dohnal <zdohnal@redhat.com> - 2:8.0.104-2
- do not ship vim.desktop

* Mon Nov 28 2016 Karsten Hopp <karsten@redhat.com> 8.0.104-1
- patchlevel 104

* Thu Nov 24 2016 Karsten Hopp <karsten@redhat.com> 8.0.095-1
- patchlevel 095

* Thu Nov 24 2016 Karsten Hopp <karsten@redhat.com> 8.0.095-1
- patchlevel 095

* Thu Nov 24 2016 Karsten Hopp <karsten@redhat.com> 8.0.095-1
- patchlevel 095

* Thu Nov 24 2016 Karsten Hopp <karsten@redhat.com> 8.0.095-2
- disable download of spec.vim, main sources are newer

* Tue Nov 22 2016 Karsten Hopp <karsten@redhat.com> 8.0.095-1
- patchlevel 095

* Mon Nov 21 2016 Karsten Hopp <karsten@redhat.com> 8.0.094-1
- patchlevel 094

* Wed Nov 16 2016 Karsten Hopp <karsten@redhat.com> 8.0.086-1
- patchlevel 086

* Tue Nov 15 2016 Karsten Hopp <karsten@redhat.com> 8.0.085-1
- patchlevel 085

* Mon Nov 14 2016 Karsten Hopp <karsten@redhat.com> 8.0.084-1
- patchlevel 084

* Mon Nov 14 2016 Zdenek Dohnal <zdohnal@redhat.com> - 8.0.070-1
- patchlevel 070

* Mon Nov 14 2016 Karsten Hopp <karsten@redhat.com> 8.0.000-1
- patchlevel 000

* Wed Nov 09 2016 Karsten Hopp <karsten@redhat.com> 8.0.057-1
- patchlevel 057

* Mon Nov 07 2016 Vít Ondruch <vondruch@redhat.com> - 8.0.037-2
- Add RPM file triggers support.

* Wed Oct 19 2016 Karsten Hopp <karsten@redhat.com> 8.0.037-1
- patchlevel 037

* Wed Oct 19 2016 Karsten Hopp <karsten@redhat.com> 8.0.018-1
- switch to gtk3

* Thu Oct 06 2016 Karsten Hopp <karsten@redhat.com> 8.0.018-1
- patchlevel 018

* Tue Sep 13 2016 Karsten Hopp <karsten@redhat.com> 8.0.003-1
- patchlevel 003

* Wed Sep 07 2016 Karsten Hopp <karsten@redhat.com> 7.4.2342-1
- patchlevel 2342

* Mon Sep 05 2016 Karsten Hopp <karsten@redhat.com> 7.4.2330-1
- patchlevel 2330

* Thu Aug 04 2016 Karsten Hopp <karsten@redhat.com> 7.4.1989-2
- redo patches, some upstream updates broke them

* Tue Jul 05 2016 Karsten Hopp <karsten@redhat.com> 7.4.1989-1
- patchlevel 1989

* Mon Jul 04 2016 Karsten Hopp <karsten@redhat.com> 7.4.1988-1
- patchlevel 1988

* Thu Jun 02 2016 Karsten Hopp <karsten@redhat.com> 7.4.1868-1
- patchlevel 1868

* Wed May 25 2016 Karsten Hopp <karsten@redhat.com> 7.4.1842-1
- patchlevel 1842

* Tue May 24 2016 Karsten Hopp <karsten@redhat.com> - 7.4.1835-2
- compile perl support as a dynamic module (rhbz#1327755)

* Tue May 24 2016 Karsten Hopp <karsten@redhat.com> 7.4.1835-1
- patchlevel 1835

* Tue May 24 2016 Karsten Hopp <karsten@redhat.com> - 7.4.1830-3
- mv vim.sh and vim.csh to source files
- sh profile.d improvements: don't leak $ID, don't fail on nounset
  (rhbz#1339106 Ville Skyttä)

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2:7.4.1830-2
- Perl 5.24 rebuild

* Fri May 13 2016 Karsten Hopp <karsten@redhat.com> 7.4.1830-1
- patchlevel 1830

* Mon May 02 2016 Karsten Hopp <karsten@redhat.com> 7.4.1816-1
- patchlevel 1816

* Fri Apr 29 2016 Karsten Hopp <karsten@redhat.com> - 7.4.1797-3
- use uncompressed help files. vimtutor and vi will access those when
  vim-common is installed.  (rhbz#1262182)
  No hard requirement vim-minimal -> vim-common added, to allow minimal
  installations

* Fri Apr 29 2016 Karsten Hopp <karsten@redhat.com> - 7.4.1797-2
- merge git branches and rebuild

* Fri Apr 29 2016 Karsten Hopp <karsten@redhat.com> 7.4.1797-1
- patchlevel 1797

* Tue Apr 26 2016 Karsten Hopp <karsten@redhat.com> 7.4.1786-1
- patchlevel 1786

* Tue Apr 26 2016 Karsten Hopp <karsten@redhat.com> - 7.4.1775-2
- fix error in spec.vim (rhbz#1318991)

* Mon Apr 25 2016 Karsten Hopp <karsten@redhat.com> - 7.4.1320-2
- update ftplugin/spec.vim, syntax/spec.vim (rhbz#1297746)

* Fri Apr 22 2016 Karsten Hopp <karsten@redhat.com> 7.4.1775-1
- patchlevel 1775

* Tue Apr 12 2016 Karsten Hopp <karsten@redhat.com> - 7.4.1718-2
- add vimfiles_root macro (rhbz#844975)
- add %%_libdir/vim  directory for plugins (rhbz#1193230)
- vi, rvi, rview, ex, view don't read vimrc anymore. They use virc instead
  (rhbz#1045815)
- fix dates in changelogs when spec.vim is used and locale != 'C'

* Fri Apr 08 2016 Karsten Hopp <karsten@redhat.com> 7.4.1718-1
- patchlevel 1718

* Tue Mar 15 2016 Karsten Hopp <karsten@redhat.com> 7.4.1570-1
- patchlevel 1570

* Wed Feb 17 2016 Karsten Hopp <karsten@redhat.com> 7.4.1344-1
- patchlevel 1344

* Mon Feb 15 2016 Karsten Hopp <karsten@redhat.com> 7.4.1320-1
- patchlevel 1320

* Sun Feb 14 2016 Karsten Hopp <karsten@redhat.com> 7.4.1317-1
- patchlevel 1317

* Sat Feb 13 2016 Karsten Hopp <karsten@redhat.com> 7.4.1308-1
- patchlevel 1308

* Fri Feb 12 2016 Karsten Hopp <karsten@redhat.com> 7.4.1304-1
- patchlevel 1304

* Thu Feb 11 2016 Karsten Hopp <karsten@redhat.com> 7.4.1301-1
- patchlevel 1301

* Wed Feb 10 2016 Karsten Hopp <karsten@redhat.com> 7.4.1297-1
- patchlevel 1297

* Tue Feb 09 2016 Karsten Hopp <karsten@redhat.com> 7.4.1293-1
- patchlevel 1293

* Mon Feb 08 2016 Karsten Hopp <karsten@redhat.com> 7.4.1290-1
- patchlevel 1290

* Sun Feb 07 2016 Karsten Hopp <karsten@redhat.com> 7.4.1273-1
- patchlevel 1273

* Sat Feb 06 2016 Karsten Hopp <karsten@redhat.com> 7.4.1265-1
- patchlevel 1265

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2:7.4.1229-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Feb 01 2016 Karsten Hopp <karsten@redhat.com> 7.4.1229-1
- patchlevel 1229

* Sat Jan 23 2016 Karsten Hopp <karsten@redhat.com> 7.4.1153-1
- patchlevel 1153

* Fri Jan 22 2016 Karsten Hopp <karsten@redhat.com> 7.4.1152-1
- patchlevel 1152

* Thu Jan 21 2016 Karsten Hopp <karsten@redhat.com> 7.4.1147-1
- patchlevel 1147

* Wed Jan 20 2016 Karsten Hopp <karsten@redhat.com> 7.4.1143-1
- patchlevel 1143

* Tue Jan 19 2016 Karsten Hopp <karsten@redhat.com> 7.4.1142-1
- patchlevel 1142

* Tue Jan 19 2016 Karsten Hopp <karsten@redhat.com> 7.4.1131-1
- patchlevel 1131

* Mon Jan 18 2016 Karsten Hopp <karsten@redhat.com> 7.4.1129-1
- patchlevel 1129

* Sun Jan 17 2016 Karsten Hopp <karsten@redhat.com> 7.4.1112-1
- patchlevel 1112

* Sat Jan 16 2016 Karsten Hopp <karsten@redhat.com> 7.4.1101-1
- patchlevel 1101

* Fri Jan 15 2016 Karsten Hopp <karsten@redhat.com> 7.4.1090-1
- patchlevel 1090

* Wed Jan 13 2016 Karsten Hopp <karsten@redhat.com> 7.4.1089-1
- patchlevel 1089

* Tue Jan 12 2016 Karsten Hopp <karsten@redhat.com> - 7.4.1087-2
- fix ssh syntax files
- fix %%global in spec.vim (rhbz#1058041)

* Mon Jan 11 2016 Karsten Hopp <karsten@redhat.com> 7.4.1087-1
- patchlevel 1087

* Sun Dec 20 2015 Karsten Hopp <karsten@redhat.com> 7.4.979-1
- patchlevel 979

* Fri Dec 18 2015 Karsten Hopp <karsten@redhat.com> 7.4.977-1
- patchlevel 977

* Mon Dec 14 2015 Karsten Hopp <karsten@redhat.com> 7.4.972-1
- patchlevel 972

* Sun Dec 13 2015 Karsten Hopp <karsten@redhat.com> 7.4.970-1
- patchlevel 970

* Sat Dec 12 2015 Karsten Hopp <karsten@redhat.com> 7.4.969-1
- patchlevel 969

* Mon Dec 07 2015 Karsten Hopp <karsten@redhat.com> 7.4.963-1
- patchlevel 963

* Sun Dec 06 2015 Karsten Hopp <karsten@redhat.com> 7.4.962-1
- patchlevel 962

* Fri Dec 04 2015 Karsten Hopp <karsten@redhat.com> 7.4.960-1
- patchlevel 960

* Wed Dec 02 2015 Karsten Hopp <karsten@redhat.com> 7.4.947-1
- patchlevel 947

* Tue Dec 01 2015 Karsten Hopp <karsten@redhat.com> 7.4.945-1
- patchlevel 945

* Mon Nov 30 2015 Karsten Hopp <karsten@redhat.com> 7.4.944-1
- patchlevel 944

* Thu Nov 26 2015 Karsten Hopp <karsten@redhat.com> 7.4.942-1
- patchlevel 942

* Wed Nov 25 2015 Karsten Hopp <karsten@redhat.com> 7.4.941-1
- patchlevel 941

* Mon Nov 23 2015 Karsten Hopp <karsten@redhat.com> 7.4.936-1
- patchlevel 936

* Sun Nov 22 2015 Karsten Hopp <karsten@redhat.com> 7.4.934-1
- patchlevel 934

* Fri Nov 20 2015 Karsten Hopp <karsten@redhat.com> 7.4.930-1
- patchlevel 930

* Wed Nov 11 2015 Karsten Hopp <karsten@redhat.com> 7.4.922-1
- patchlevel 922

* Tue Nov 10 2015 Karsten Hopp <karsten@redhat.com> 7.4.917-1
- patchlevel 917

* Wed Nov 04 2015 Karsten Hopp <karsten@redhat.com> 7.4.909-1
- patchlevel 909
- Fedora vim now uses tarballs created from upstream git instead
  of just upstream patches. Now runtime files will have fixes, too.

* Tue Nov 03 2015 Karsten Hopp <karsten@redhat.com> 7.4.908-1
- patchlevel 908

* Mon Nov 02 2015 Karsten Hopp <karsten@redhat.com> 7.4.903-1
- patchlevel 903

* Sat Oct 31 2015 Karsten Hopp <karsten@redhat.com> 7.4.902-1
- patchlevel 902

* Mon Oct 26 2015 Karsten Hopp <karsten@redhat.com> 7.4.900-1
- patchlevel 900

* Wed Oct 14 2015 Karsten Hopp <karsten@redhat.com> 7.4.898-1
- patchlevel 898

* Thu Oct 08 2015 Karsten Hopp <karsten@redhat.com> 7.4.891-1
- patchlevel 891

* Wed Oct 07 2015 Karsten Hopp <karsten@redhat.com> 7.4.890-1
- patchlevel 890

* Wed Sep 30 2015 Karsten Hopp <karsten@redhat.com> 7.4.889-1
- patchlevel 889

* Sat Sep 26 2015 Karsten Hopp <karsten@redhat.com> 7.4.884-1
- patchlevel 884

* Tue Sep 22 2015 Karsten Hopp <karsten@redhat.com> 7.4.873-2
- fix garbled xxd manpage in Japanese locale (bugzilla #1035606), Masayuki Oshima

* Tue Sep 22 2015 Karsten Hopp <karsten@redhat.com> 7.4.873-1
- add Provides: mergetool for bugzilla #990444

* Fri Sep 18 2015 Karsten Hopp <karsten@redhat.com> 7.4.873-1
- patchlevel 873

* Wed Sep 16 2015 Karsten Hopp <karsten@redhat.com> 7.4.871-1
- patchlevel 871

* Thu Sep 10 2015 Karsten Hopp <karsten@redhat.com> 7.4.865-1
- patchlevel 865

* Wed Sep 09 2015 Karsten Hopp <karsten@redhat.com> 7.4.861-1
- patchlevel 861

* Wed Sep 02 2015 Karsten Hopp <karsten@redhat.com> 7.4.854-1
- patchlevel 854

* Fri Aug 28 2015 Karsten Hopp <karsten@redhat.com> 7.4.843-1
- patchlevel 843

* Thu Aug 27 2015 Karsten Hopp <karsten@redhat.com> 7.4.841-1
- patchlevel 841

* Wed Aug 26 2015 Karsten Hopp <karsten@redhat.com> 7.4.838-1
- patchlevel 838

* Wed Aug 19 2015 Karsten Hopp <karsten@redhat.com> 7.4.827-1
- patchlevel 827
- re-enable lua
- enable python3

* Fri Jul 10 2015 Lubomir Rintel <lkundrak@v3.sk> 7.4.769-3
- drop forcing background, vim detects this since 7.4.757, rhbz#1159920

* Sat Jul 04 2015 Karsten Hopp <karsten@redhat.com> 7.4.769-1
- patchlevel 769

* Fri Jul 03 2015 Karsten Hopp <karsten@redhat.com> 7.4.768-1
- patchlevel 768

* Mon Jun 29 2015 Karsten Hopp <karsten@redhat.com> 7.4.764-1
- patchlevel 764

* Sun Jun 28 2015 Karsten Hopp <karsten@redhat.com> 7.4.763-1
- patchlevel 763

* Fri Jun 26 2015 Karsten Hopp <karsten@redhat.com> 7.4.761-1
- patchlevel 761

* Thu Jun 25 2015 Karsten Hopp <karsten@redhat.com> 7.4.757-1
- patchlevel 757

* Mon Jun 22 2015 Karsten Hopp <karsten@redhat.com> 7.4.752-1
- patchlevel 752

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:7.4.737-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Karsten Hopp <karsten@redhat.com> 7.4.737-1
- patchlevel 737

* Thu May 14 2015 Karsten Hopp <karsten@redhat.com> 7.4.729-1
- patchlevel 729

* Wed May 06 2015 Karsten Hopp <karsten@redhat.com> 7.4.728-1
- patchlevel 728

* Tue May 05 2015 Karsten Hopp <karsten@redhat.com> 7.4.726-1
- patchlevel 726

* Mon May 04 2015 Karsten Hopp <karsten@redhat.com> 7.4.723-1
- patchlevel 723

* Thu Apr 23 2015 Karsten Hopp <karsten@redhat.com> 7.4.712-1
- patchlevel 712

* Wed Apr 22 2015 Karsten Hopp <karsten@redhat.com> 7.4.711-1
- patchlevel 711

* Tue Apr 21 2015 Karsten Hopp <karsten@redhat.com> 7.4.708-1
- patchlevel 708

* Sat Apr 18 2015 Karsten Hopp <karsten@redhat.com> 7.4.703-1
- patchlevel 703

* Fri Apr 17 2015 Karsten Hopp <karsten@redhat.com> 7.4.702-1
- patchlevel 702

* Wed Apr 15 2015 Karsten Hopp <karsten@redhat.com> 7.4.701-1
- patchlevel 701

* Tue Apr 14 2015 Karsten Hopp <karsten@redhat.com> 7.4.699-1
- patchlevel 699

* Mon Apr 13 2015 Karsten Hopp <karsten@redhat.com> 7.4.698-1
- patchlevel 698

* Fri Apr 10 2015 Karsten Hopp <karsten@redhat.com> 7.4.692-1
- patchlevel 692

* Sat Apr 04 2015 Karsten Hopp <karsten@redhat.com> 7.4.691-1
- patchlevel 691

* Fri Apr 03 2015 Karsten Hopp <karsten@redhat.com> 7.4.690-1
- patchlevel 690

* Wed Apr 01 2015 Karsten Hopp <karsten@redhat.com> 7.4.688-1
- patchlevel 688

* Tue Mar 31 2015 Karsten Hopp <karsten@redhat.com> 7.4.686-1
- patchlevel 686

* Thu Mar 26 2015 Karsten Hopp <karsten@redhat.com> 7.4.683-1
- patchlevel 683

* Wed Mar 25 2015 Karsten Hopp <karsten@redhat.com> 7.4.682-1
- patchlevel 682

* Tue Mar 24 2015 Karsten Hopp <karsten@redhat.com> 7.4.681-1
- patchlevel 681

* Sun Mar 22 2015 Karsten Hopp <karsten@redhat.com> 7.4.674-1
- patchlevel 674

* Sat Mar 21 2015 Karsten Hopp <karsten@redhat.com> 7.4.672-1
- patchlevel 672

* Fri Mar 20 2015 Karsten Hopp <karsten@redhat.com> 7.4.668-1
- patchlevel 668

* Thu Mar 19 2015 Jitka Plesnikova <jplesnik@redhat.com> - 7.4.663-3
- Perl 5.22 rebuild

* Wed Mar 18 2015 Richard Hughes <rhughes@redhat.com> - 7.4.663-2
- Add an AppData file for the software center

* Sat Mar 14 2015 Karsten Hopp <karsten@redhat.com> 7.4.663-1
- patchlevel 663

* Fri Mar 13 2015 Karsten Hopp <karsten@redhat.com> 7.4.662-1
- patchlevel 662

* Sun Mar 08 2015 Karsten Hopp <karsten@redhat.com> 7.4.658-1
- patchlevel 658

* Sat Mar 07 2015 Karsten Hopp <karsten@redhat.com> 7.4.657-1
- patchlevel 657

* Fri Mar 06 2015 Karsten Hopp <karsten@redhat.com> 7.4.656-1
- patchlevel 656

* Thu Mar 05 2015 Karsten Hopp <karsten@redhat.com> 7.4.652-1
- patchlevel 652

* Sat Feb 28 2015 Karsten Hopp <karsten@redhat.com> 7.4.648-1
- patchlevel 648

* Fri Feb 27 2015 Karsten Hopp <karsten@redhat.com> 7.4.643-1
- patchlevel 643

* Fri Feb 27 2015 Dave Airlie <airlied@redhat.com> 7.4.640-4
- fix vimrc using wrong comment character

* Thu Feb 26 2015 Karsten Hopp <karsten@redhat.com> 7.4.640-3
- bump release

* Thu Feb 26 2015 Karsten Hopp <karsten@redhat.com> 7.4.640-2
- set background to dark in gnome-terminal, rhbz#1159920

* Wed Feb 25 2015 Karsten Hopp <karsten@redhat.com> 7.4.640-1
- patchlevel 640

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 7.4.629-2
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Wed Feb 11 2015 Karsten Hopp <karsten@redhat.com> 7.4.629-2
- fix syntax highlighting for some ssh_config sshd_config keywords

* Wed Feb 11 2015 Karsten Hopp <karsten@redhat.com> 7.4.629-1
- patchlevel 629

* Fri Feb 06 2015 Karsten Hopp <karsten@redhat.com> 7.4.622-1
- patchlevel 622

* Thu Feb 05 2015 Karsten Hopp <karsten@redhat.com> 7.4.621-1
- patchlevel 621

* Wed Feb 04 2015 Karsten Hopp <karsten@redhat.com> 7.4.618-1
- patchlevel 618

* Tue Feb 03 2015 Karsten Hopp <karsten@redhat.com> 7.4.615-1
- patchlevel 615

* Wed Jan 28 2015 Karsten Hopp <karsten@redhat.com> 7.4.608-1
- patchlevel 608

* Tue Jan 27 2015 Karsten Hopp <karsten@redhat.com> 7.4.604-1
- patchlevel 604

* Fri Jan 23 2015 Karsten Hopp <karsten@redhat.com> 7.4.591-1
- patchlevel 591

* Wed Jan 21 2015 Karsten Hopp <karsten@redhat.com> 7.4.589-1
- patchlevel 589

* Tue Jan 20 2015 Karsten Hopp <karsten@redhat.com> 7.4.586-1
- patchlevel 586

* Sun Jan 18 2015 Karsten Hopp <karsten@redhat.com> 7.4.582-1
- patchlevel 582

* Thu Jan 15 2015 Karsten Hopp <karsten@redhat.com> 7.4.580-1
- patchlevel 580

* Wed Jan 14 2015 Karsten Hopp <karsten@redhat.com> 7.4.576-1
- patchlevel 576

* Mon Jan 12 2015 Karsten Hopp <karsten@redhat.com> 7.4.567-1
- use %%make_install in spec-template.new (rhbz#919270)

* Thu Jan 08 2015 Karsten Hopp <karsten@redhat.com> 7.4.567-1
- patchlevel 567

* Wed Jan 07 2015 Karsten Hopp <karsten@redhat.com> 7.4.566-1
- patchlevel 566

* Thu Dec 18 2014 Karsten Hopp <karsten@redhat.com> 7.4.560-1
- patchlevel 560

* Wed Dec 17 2014 Karsten Hopp <karsten@redhat.com> 7.4.557-1
- patchlevel 557

* Sun Dec 14 2014 Karsten Hopp <karsten@redhat.com> 7.4.552-1
- patchlevel 552

* Sat Dec 13 2014 Karsten Hopp <karsten@redhat.com> 7.4.546-1
- patchlevel 546

* Mon Dec 08 2014 Karsten Hopp <karsten@redhat.com> 7.4.542-1
- patchlevel 542

* Sun Dec 07 2014 Karsten Hopp <karsten@redhat.com> 7.4.541-1
- patchlevel 541

* Mon Dec 01 2014 Karsten Hopp <karsten@redhat.com> 7.4.540-1
- patchlevel 540

* Sun Nov 30 2014 Karsten Hopp <karsten@redhat.com> 7.4.539-1
- patchlevel 539

* Fri Nov 28 2014 Karsten Hopp <karsten@redhat.com> 7.4.537-1
- patchlevel 537

* Thu Nov 27 2014 Karsten Hopp <karsten@redhat.com> 7.4.534-1
- patchlevel 534

* Sun Nov 23 2014 Karsten Hopp <karsten@redhat.com> 7.4.527-1
- patchlevel 527

* Fri Nov 21 2014 Karsten Hopp <karsten@redhat.com> 7.4.526-1
- patchlevel 526

* Thu Nov 20 2014 Karsten Hopp <karsten@redhat.com> 7.4.525-1
- patchlevel 525

* Wed Nov 19 2014 Karsten Hopp <karsten@redhat.com> 7.4.521-1
- patchlevel 521

* Thu Nov 13 2014 Karsten Hopp <karsten@redhat.com> 7.4.516-1
- patchlevel 516

* Wed Nov 12 2014 Karsten Hopp <karsten@redhat.com> 7.4.512-1
- patchlevel 512

* Thu Nov 06 2014 Karsten Hopp <karsten@redhat.com> 7.4.507-1
- patchlevel 507

* Wed Nov 05 2014 Karsten Hopp <karsten@redhat.com> 7.4.502-1
- patchlevel 502

* Sat Nov 01 2014 Karsten Hopp <karsten@redhat.com> 7.4.492-1
- patchlevel 492

* Fri Oct 31 2014 Karsten Hopp <karsten@redhat.com> 7.4.491-1
- patchlevel 491

* Thu Oct 23 2014 Karsten Hopp <karsten@redhat.com> 7.4.488-1
- patchlevel 488

* Wed Oct 22 2014 Karsten Hopp <karsten@redhat.com> 7.4.487-1
- patchlevel 487

* Tue Oct 21 2014 Karsten Hopp <karsten@redhat.com> 7.4.483-1
- patchlevel 483

* Fri Oct 17 2014 Karsten Hopp <karsten@redhat.com> 7.4.481-1
- patchlevel 481

* Thu Oct 16 2014 Karsten Hopp <karsten@redhat.com> 7.4.480-1
- patchlevel 480

* Wed Oct 15 2014 Karsten Hopp <karsten@redhat.com> 7.4.477-1
- patchlevel 477

* Mon Oct 13 2014 Karsten Hopp <karsten@redhat.com> 7.4.475-2
- add support for %%license macro (Petr Šabata)

* Sat Oct 11 2014 Karsten Hopp <karsten@redhat.com> 7.4.475-1
- patchlevel 475

* Fri Oct 10 2014 Karsten Hopp <karsten@redhat.com> 7.4.473-1
- patchlevel 473

* Thu Oct 09 2014 Karsten Hopp <karsten@redhat.com> 7.4.471-1
- patchlevel 471

* Tue Oct 07 2014 Karsten Hopp <karsten@redhat.com> 7.4.465-1
- patchlevel 465

* Tue Sep 30 2014 Karsten Hopp <karsten@redhat.com> 7.4.463-1
- patchlevel 463

* Mon Sep 29 2014 Karsten Hopp <karsten@redhat.com> 7.4.462-1
- patchlevel 462

* Sat Sep 27 2014 Karsten Hopp <karsten@redhat.com> 7.4.461-1
- patchlevel 461

* Wed Sep 24 2014 Karsten Hopp <karsten@redhat.com> 7.4.460-1
- patchlevel 460

* Wed Sep 24 2014 Karsten Hopp <karsten@redhat.com> 7.4.458-1
- patchlevel 458

* Tue Sep 23 2014 Karsten Hopp <karsten@redhat.com> 7.4.457-1
- patchlevel 457

* Sat Sep 20 2014 Karsten Hopp <karsten@redhat.com> 7.4.453-1
- patchlevel 453

* Tue Sep 16 2014 Karsten Hopp <karsten@redhat.com> 7.4.444-1
- patchlevel 444

* Mon Sep 15 2014 Karsten Hopp <karsten@redhat.com> 7.4.443-1
- patchlevel 443

* Wed Sep 10 2014 Karsten Hopp <karsten@redhat.com> 7.4.442-1
- patchlevel 442

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2:7.4.417-2
- Perl 5.20 rebuild

* Tue Aug 26 2014 Karsten Hopp <karsten@redhat.com> 7.4.417-1
- patchlevel 417

* Fri Aug 22 2014 Karsten Hopp <karsten@redhat.com> 7.4.410-1
- patchlevel 410
- xsubpp-path patch is obsolete now

* Fri Aug 22 2014 Karsten Hopp <karsten@redhat.com> 7.4.402-3
- fix help file names

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:7.4.402-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild


* Wed Aug 13 2014 Karsten Hopp <karsten@redhat.com> 7.4.402-1
- patchlevel 402

* Tue Aug 12 2014 Karsten Hopp <karsten@redhat.com> 7.4.401-1
- patchlevel 401

* Wed Aug  6 2014 Tom Callaway <spot@fedoraproject.org> 2:7.4.373-2
- fix license handling

* Tue Jul 22 2014 Karsten Hopp <karsten@redhat.com> 7.4.373-1
- patchlevel 373

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:7.4.307-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Karsten Hopp <karsten@redhat.com> 7.4.307-1
- patchlevel 307

* Tue Apr 29 2014 Vít Ondruch <vondruch@redhat.com> - 2:7.4.258-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.1

* Wed Apr 16 2014 Karsten Hopp <karsten@redhat.com> 7.4.258-1
- patchlevel 258

* Mon Apr 07 2014 Karsten Hopp <karsten@redhat.com> 7.4.253-1
- patchlevel 253

* Wed Mar 12 2014 Karsten Hopp <karsten@redhat.com> 7.4.204-1
- patchlevel 204

* Mon Feb 24 2014 Karsten Hopp <karsten@redhat.com> 7.4.192-1
- patchlevel 192

* Tue Feb 18 2014 Karsten Hopp <karsten@redhat.com> 7.4.182-1
- patchlevel 182

* Tue Feb 18 2014 Karsten Hopp <karsten@redhat.com> 7.4.179-2
- enable dynamic lua interpreter

* Sat Feb 15 2014 Karsten Hopp <karsten@redhat.com> 7.4.179-1
- patchlevel 179

* Wed Jan 29 2014 Karsten Hopp <karsten@redhat.com> 7.4.160-1
- patchlevel 160

* Tue Dec 17 2013 Karsten Hopp <karsten@redhat.com> 7.4.131-1
- patchlevel 131

* Wed Nov 20 2013 Karsten Hopp <karsten@redhat.com> 7.4.094-1
- patchlevel 094

* Tue Oct 15 2013 Karsten Hopp <karsten@redhat.com> 7.4.052-1
- patchlevel 052

* Wed Sep 11 2013 Karsten Hopp <karsten@redhat.com> 7.4.027-2
- update vim icons (#1004788)
- check if 'id -u' returns empty string (vim.sh)

* Wed Sep 11 2013 Karsten Hopp <karsten@redhat.com> 7.4.027-1
- patchlevel 027

* Wed Sep 04 2013 Karsten Hopp <karsten@redhat.com> 7.4.016-1
- patchlevel 016

* Wed Aug 28 2013 Karsten Hopp <karsten@redhat.com> 7.4.009-1
- patchlevel 009
  mkdir("foo/bar/", "p") gives an error message
  creating a preview window on startup messes up the screen
  new regexp engine can't be interrupted
  too easy to write a file was not decrypted (yet)

* Wed Aug 21 2013 Karsten Hopp <karsten@redhat.com> 7.4.5-1
- patchlevel 5
- when closing a window fails ":bwipe" may hang
- "vaB" while 'virtualedit' is set selects the wrong area

* Wed Aug 21 2013 Karsten Hopp <karsten@redhat.com> 7.4.3-1
- patchlevel 3, memory access error in Ruby syntax highlighting

* Wed Aug 21 2013 Karsten Hopp <karsten@redhat.com> 7.4.2-1
- patchlevel 2, pattern with two alternative look-behind matches doesn't match

* Wed Aug 21 2013 Karsten Hopp <karsten@redhat.com> 7.4.1-1
- patchlevel 1, 'ic' doesn't work for patterns such as [a-z]

* Mon Aug 12 2013 Karsten Hopp <karsten@redhat.com> 7.4.0-1
- update to vim-7.4

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:7.3.1314-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 26 2013 Karsten Hopp <karsten@redhat.com> 7.3.1314-2
- document gex and vimx in man page
- fix gvimdiff and gvimtutor man page redirects

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 2:7.3.1314-2
- Perl 5.18 rebuild

* Tue Jul 09 2013 Karsten Hopp <karsten@redhat.com> 7.3.1314-1
- patchlevel 1314

* Thu Jul 04 2013 Karsten Hopp <karsten@redhat.com> 7.3.1293-1
- patchlevel 1293

* Fri Jun 14 2013 Karsten Hopp <karsten@redhat.com> 7.3.1189-1
- patchlevel 1189

* Tue Jun 04 2013 Karsten Hopp <karsten@redhat.com> 7.3.1109-1
- patchlevel 1109

* Wed May 22 2013 Karsten Hopp <karsten@redhat.com> 7.3.1004-1
- patchlevel 1004

* Wed May 22 2013 Karsten Hopp <karsten@redhat.com> 7.3.1000-1
- patchlevel 1000 !

* Tue May 21 2013 Karsten Hopp <karsten@redhat.com> 7.3.987-1
- patchlevel 987

* Tue May 21 2013 Karsten Hopp <karsten@redhat.com> 7.3.944-2
- consistent use of macros in spec file
- add some links to man pages

* Tue May 14 2013 Karsten Hopp <karsten@redhat.com> 7.3.944-1
- patchlevel 944

* Mon May 13 2013 Karsten Hopp <karsten@redhat.com> 7.3.943-2
- add BR perl(ExtUtils::ParseXS)

* Mon May 13 2013 Karsten Hopp <karsten@redhat.com> 7.3.943-1
- patchlevel 943

* Wed May 08 2013 Karsten Hopp <karsten@redhat.com> 7.3.931-1
- patchlevel 931

* Wed May 08 2013 Karsten Hopp <karsten@redhat.com> 7.3.903-1
- fix ruby version check

* Fri Apr 19 2013 Karsten Hopp <karsten@redhat.com> 7.3.903-1
- drop crv patch
- update 7.3.838 patch, it was broken upstream

* Mon Apr 15 2013 Karsten Hopp <karsten@redhat.com> 7.3.903-1
- patchlevel 903

* Mon Feb 18 2013 Karsten Hopp <karsten@redhat.com> 7.3.822-1
- patchlevel 822

* Fri Feb 15 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 7.3.797-2
- Only use --vendor for desktop-file-install on F18 or less

* Thu Jan 31 2013 Karsten Hopp <karsten@redhat.com> 7.3.797-1
- patchlevel 797

* Mon Jan 28 2013 Karsten Hopp <karsten@redhat.com> 7.3.785-1
- patchlevel 785

* Tue Nov 20 2012 Karsten Hopp <karsten@redhat.com> 7.3.715-1
- patchlevel 715

* Mon Nov 12 2012 Karsten Hopp <karsten@redhat.com> 7.3.712-1
- patchlevel 712

* Mon Nov 12 2012 Karsten Hopp <karsten@redhat.com> 7.3.682-2
- fix vim.csh syntax

* Tue Oct 23 2012 Karsten Hopp <karsten@redhat.com> 7.3.712-1
- patchlevel 712

* Mon Oct 15 2012 Karsten Hopp <karsten@redhat.com> 7.3.691-1
- patchlevel 691

* Fri Oct 05 2012 Karsten Hopp <karsten@redhat.com> 7.3.682-1
- patchlevel 682
- use --enable-rubyinterp=dynamic and --enable-pythoninterp=dynamic

* Mon Sep 03 2012 Karsten Hopp <karsten@redhat.com> 7.3.646-1
- patchlevel 646

* Tue Aug 28 2012 Karsten Hopp <karsten@redhat.com> 7.3.638-2
- fix some man page typos (#668894, #675480)
- own usr/share/vim/vimfiles/doc/tags (#845564)
- add path to csope database (#844843)

* Tue Aug 28 2012 Karsten Hopp <karsten@redhat.com> 7.3.638-1
- patchlevel 638

# vim:nrformats-=octal
