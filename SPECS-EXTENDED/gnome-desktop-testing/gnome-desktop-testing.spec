Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           gnome-desktop-testing
Version:        2018.1
Release:        4%{?dist}
Summary:        GNOME test runner for installed tests

License:        LGPLv2+
URL:            https://live.gnome.org/Initiatives/GnomeGoals/InstalledTests
Source0:        https://gitlab.gnome.org/GNOME/%{name}/-/archive/v%{version}/%{name}-v%{version}.tar.gz

BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  systemd-devel
BuildRequires:  pkgconfig(libgsystem)
BuildRequires:  git automake autoconf libtool

# https://gitlab.gnome.org/GNOME/gnome-desktop-testing/merge_requests/1
Patch0: 0001-Don-t-crash-on-unknown-command-line-options.patch

%description
gnome-desktop-testing-runner is a basic runner for tests that are
installed in /usr/share/installed-tests.  For more information, see
"https://wiki.gnome.org/Initiatives/GnomeGoals/InstalledTests"

%prep
%autosetup -S git_am -n %{name}-v%{version}
NOCONFIGURE=1 ./autogen.sh

%build
%configure --with-systemd-journal
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

%files
%doc COPYING README
%{_bindir}/gnome-desktop-testing-runner
%{_bindir}/ginsttest-runner

%changelog
* Tue Sep 19 2023 Jon Slobodzian <joslobo@microsoft.com> - 2018.1-4
- Fix build issue for systemd/systemd-bootstrap confusion
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2018.1-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2018.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Nov 28 2019 Bastien Nocera <bnocera@redhat.com> - 2018.1-1
+ gnome-desktop-testing-2018.1-1
- Update to 2018.1

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2016.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2016.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2016.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2016.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Aug 07 2017 Colin Walters <walters@verbum.org> - 2016.1-6
- Fix systemd BR

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2016.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2016.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2016.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Mar 31 2016 Colin Walters <walters@redhat.com> - 2016.1-2
- New upstream version

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2014.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2014.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2014.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2014.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jan 30 2014 Colin Walters <walters@verbum.org> - 2014.1-1
- New upstream release

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2013.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 21 2013 Matthias Clasen <mclasen@redhat.com> - 2013.1-1
- Initial packaging (#976919)
