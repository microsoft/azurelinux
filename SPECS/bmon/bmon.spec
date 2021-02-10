Summary:        Monitoring and debugging tool to capture networking related statistics
Name:           bmon
Version:        4.0
Release:        1%{?dist}
License:        BSD-2-Clause AND MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://github.com/tgraf/bmon
Source0:        https://github.com/tgraf/bmon/archive/%{name}-%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  libconfuse-devel
BuildRequires:  libnl3-devel
BuildRequires:  make
BuildRequires:  ncurses-devel
Requires:       libconfuse
Requires:       libnl3
Requires:       ncurses

%description
bmon is a monitoring and debugging tool to capture networking related
statistics and prepare them visually in a human friendly way. It features
various output methods including an interactive curses user interface and
a programmable text output for scripting.

%prep
%autosetup -p1

%build
./autogen.sh
%configure
%make_build

%install
%make_install

%files
%license LICENSE.BSD LICENSE.MIT
%{_bindir}/bmon
%{_docdir}/bmon/examples/bmon.conf
%{_mandir}/man8/bmon.8.gz

%changelog
* Mon Feb 08 2021 Henry Beberman <henry.beberman@microsoft.com> 4.0-1
- Add bmon spec
- License verified
- Original version for CBL-Mariner
