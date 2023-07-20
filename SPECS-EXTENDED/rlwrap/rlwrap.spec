Summary:        Wrapper for GNU readline
Name:           rlwrap
Version:        0.46.1
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/hanslub42/rlwrap
Source:         https://github.com/hanslub42/rlwrap/releases/download/%{version}/%{name}-%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  ncurses-devel
BuildRequires:  readline-devel

%description
rlwrap is a 'readline wrapper' that uses the GNU readline library to
allow the editing of keyboard input for any other command. Input
history is remembered across invocations, separately for each command;
history completion and search work as in bash and completion word
lists can be specified on the command line.

%prep
%autosetup -p1


%build
%configure
%make_build

%install
%make_install


%check
make check


%files
%license COPYING
%doc AUTHORS NEWS README.md
%{_bindir}/rlwrap
%{_mandir}/*/rlwrap.*
%{_mandir}/man3/RlwrapFilter.*
%{_datadir}/rlwrap

%changelog
* Wed Jul 05 2023 Saranya R <rsaranya@microsoft.com> - 0.46.1-1
- Initial CBL-Mariner import from Fedora 38 (license: MIT).
- License verified

* Thu Feb 09 2023 Michel Alexandre Salim <salimma@fedoraproject.org> - 0.46.1-1
- Update to 0.46.1

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.45.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Sep 28 2022 Michel Alexandre Salim <salimma@fedoraproject.org> - 0.45.2-3
- Fix version parsing in rlwrapfilter.py (rhbz#2091749)

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.45.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Feb 02 2022 Michel Alexandre Salim <salimma@fedoraproject.org> - 0.45.2-1
- Update to 0.45.2

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.44-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.44-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild
