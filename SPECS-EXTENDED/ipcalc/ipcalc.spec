Vendor:         Microsoft Corporation
Distribution:   Mariner
Name: ipcalc
Version: 0.4.1
Release: 2%{?dist}
Summary: IP network address calculator
License: GPLv2+
URL: https://gitlab.com/ipcalc/ipcalc
Source0: https://gitlab.com/ipcalc/ipcalc/-/archive/%{version}/ipcalc-%{version}.tar.gz

BuildRequires: gcc, libmaxminddb-devel, meson
Recommends:    libmaxminddb, geolite2-city, geolite2-country

# Explicitly conflict with older initscript packages that ship ipcalc
Conflicts: initscripts < 9.63
# Obsolete ipcalculator
Obsoletes:  ipcalculator < 0.41-20


%description
ipcalc provides a simple way to calculate IP information for a host
or network. Depending on the options specified, it may be used to provide
IP network information in human readable format, in a format suitable for
parsing in scripts, generate random private addresses, resolve an IP address,
or check the validity of an address.

%prep
%autosetup

%build
%meson -Duse_maxminddb=enabled -Duse_runtime_linking=enabled
%meson_build

%install
%meson_install

%check
%meson_test

%files

%{_bindir}/ipcalc
%license COPYING
%doc README.md
%{_mandir}/man1/ipcalc.1*

%changelog
* Thu Jul 08 2021 Muhammad Falak Wani <mwani@microsoft.com> - 0.4.1-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- fix typo in changelog date `Aor -> Apr`

* Fri Apr 24 2020 Nikos Mavrogiannopoulos <nmav@redhat.com> - 0.4.1-1
- Updated to 0.4.1

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Dec 28 2019 Nikos Mavrogiannopoulos <nmav@redhat.com> - 0.4.0-1
- Updated to 0.4.0

* Sat Nov 23 2019 Nikos Mavrogiannopoulos <nmav@redhat.com> - 0.3.0-1
- Updated to 0.3.0

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Feb 19 2019 Nikos Mavrogiannopoulos <nmav@redhat.com> - 0.2.5-2
- Re-added the geolite2-city, geolite2-country dependencies

* Mon Feb 18 2019 Nikos Mavrogiannopoulos <nmav@redhat.com> - 0.2.5-1
- Updated to 0.2.5

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Aug 09 2018 Nikos Mavrogiannopoulos <nmav@redhat.com> - 0.2.4-2
- Fix crash when -g option is used

* Mon Jul 23 2018 Nikos Mavrogiannopoulos <nmav@redhat.com> - 0.2.4-1
- New upstream release

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu May 31 2018 Nikos Mavrogiannopoulos <nmav@redhat.com> - 0.2.3-1
- New upstream release

* Fri Feb  9 2018 Florian Weimer <fweimer@redhat.com> - 0.2.2-4
- Another attempt at injecting LDFLAGS

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Feb  1 2018 Florian Weimer <fweimer@redhat.com> - 0.2.2-2
- Build with linker flags from redhat-rpm-config

* Tue Jan 02 2018 Nikos Mavrogiannopoulos <nmav@redhat.com> - 0.2.2-1
- New upstream release

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 15 2017 Nikos Mavrogiannopoulos <nmav@redhat.com> - 0.2.0-1
- New upstream release

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jun 15 2016 Nikos Mavrogiannopoulos <nmav@redhat.com> - 0.1.8-1
- New upstream release

* Fri Apr  1 2016 Nikos Mavrogiannopoulos <nmav@redhat.com> - 0.1.7-1
- New upstream release

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Dec  8 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> - 0.1.6-1
- New upstream release

* Wed Oct 14 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> - 0.1.4-2
- Corrected issue on --all-info

* Wed Oct 14 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> - 0.1.4-1
- New upstream release

* Tue Oct  6 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> - 0.1.3-1
- New upstream release
- Prints GeoIP information on generic info

* Mon Sep 21 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> - 0.1.2-3
- This package obsoletes ipcalculator

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun  9 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> - 0.1.2-1
- New upstream release

* Tue May 19 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> - 0.1.1-1
- Compatibility fixes (allow a mask of 0)

* Mon May 18 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> - 0.1.0-1
- First independent release outside initscripts
