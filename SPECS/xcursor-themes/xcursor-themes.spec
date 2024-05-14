#
# spec file for package xcursor-themes
#
# Copyright (c) 2020 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#

Summary:        Default set of cursor themes for X
Name:           xcursor-themes
Version:        1.0.7
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          System/X11/Icons
URL:            https://xorg.freedesktop.org/
Source0:        https://xorg.freedesktop.org/releases/individual/data/%{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  pkg-config
BuildRequires:  xorg-x11-apps
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(xorg-macros) >= 1.3

%description
This is a default set of cursor themes for use with libXcursor,
originally created for the XFree86 Project, and now shipped as part
of the X.Org software distribution.

%prep
%autosetup

%build
%configure
%make_build

%install
%make_install

%files
%defattr(-,root,root)
%license COPYING
%doc ChangeLog README.md
%{_datadir}/icons/handhelds/
%{_datadir}/icons/redglass/
%{_datadir}/icons/whiteglass/

%changelog
* Thu Feb 15 2024 Aditya Dubey <adityadubey@microsoft.com> - 1.0.7-1
- Update to 1.0.7

* Fri Oct 08 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.6-2
- Switching to using a single digit for the 'Release' tag.
- Adding distribution information to the 'Release' tag.

* Tue Jan 19 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.6-1.3
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- License verified.
- Removed BR on 'fdupes'.

* Thu Apr 23 2020 Callum Farmer <callumjfarmer13@gmail.com>
- Update to version 1.0.6
  + Switch to NO_ARCH
  + Remove unneded dependency on xorgproto
  + This adds some symlinks to the whiteglass cursor theme, that gnome-shell expects

* Wed Apr  4 2018 sndirsch@suse.com
- Update to version 1.0.5:
  * configure: Drop AM_MAINTAINER_MODE
  * autogen.sh: Honor NOCONFIGURE=1
  * autogen.sh: use quoted string variables
  * config: replace deprecated use of AC_OUTPUT with AC_CONFIG_FILES
  * Add copyright files for redglass and whiteglass themes.
  * autogen: add default patch prefix
  * autogen.sh: use exec instead of waiting for configure to finish

* Thu Feb  6 2014 sndirsch@suse.com
- fixed license to X11 in specfile

* Sun Jul 21 2013 zaitor@opensuse.org
- Update to version 1.0.4:
  + Create missing symlinks for cursor animations (fdo#6466).
  + config: Add missing AC_CONFIG_SRCDIR.
  + genmakefile.sh:
  - Split up EXTRA_DIST lines.
  - Fix autogeneration of handhelds/Makefile.cursor.
  - Change echo to printf for better portability & control.

* Fri Apr 13 2012 vuntz@opensuse.org
- Split xcursor-themes from xorg-x11. Initial version: 1.0.3.
