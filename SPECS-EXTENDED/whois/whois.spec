%global alternative md
%global cfgfile %{name}.conf
%global genname whois

Summary:        Improved WHOIS client
Name:           whois
Version:        5.5.15
Release:        1%{?dist}
License:        GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://www.linux.it/~md/software/
Source0:        https://ftp.debian.org/debian/pool/main/w/%{name}/%{name}_%{version}.tar.xz
BuildRequires:  coreutils
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  make
BuildRequires:  perl-interpreter
BuildRequires:  perl(autodie)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
Requires:       iana-etc
Requires:       whois-nls = %{version}-%{release}
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives
# Add IDN support
%{bcond_without whois_enables_idn}
# Use libidn2 instead of libidn
%{bcond_without whois_enables_libidn2}
# Package mkpasswd tool
%if 0%{?rhel}
%{bcond_with whois_enables_mkpasswd}
%else
%{bcond_without whois_enables_mkpasswd}
%endif
%if %{with whois_enables_idn}
%if %{with whois_enables_libidn2}
BuildRequires:  pkgconfig(libidn2) >= 2.0.3
%else
BuildRequires:  pkgconfig(libidn)
BuildConflicts: pkgconfig(libidn2)
%endif
%else
BuildConflicts: pkgconfig(libidn)
BuildConflicts: pkgconfig(libidn2)
%endif
%if %{with whois_enables_mkpasswd}
BuildRequires:  pkgconfig(libcrypt)
BuildRequires:  pkgconfig(libxcrypt) >= 4.1
%endif

%description
Searches for an object in a RFC 3912 database.

This version of the WHOIS client tries to guess the right server to ask for
the specified object. If no guess can be made it will connect to
whois.networksolutions.com for NIC handles or whois.arin.net for IPv4
addresses and network names.

%if %{with whois_enables_mkpasswd}
%package -n mkpasswd
Summary:        Encrypt a password with crypt(3) function using a salt
Requires:       whois-nls = %{version}-%{release}
# /usr/bin/mkpasswd was provided by "expect" package, bug #1649426
Conflicts:      expect < 5.45.4-8.fc30
# whois-mkpasswd package renamed to mkpasswd in 5.4.0-2.fc30, bug #1649426
Obsoletes:      whois-mkpasswd <= 5.4.0-1.fc30
# but we continued upgrading whois in Fedoras < 30 without the rename
Obsoletes:      whois-mkpasswd <= 5.5.3-1.fc29
Provides:       whois-mkpasswd = %{version}-%{release}

%description -n mkpasswd
mkpasswd tool encrypts a given password with the crypt(3) libc function
using a given salt.
%endif

# The same gettext catalogs are used by whois tool and mkpasswd tool. But we
# want to have the tools installable independently.
%package nls
Summary:        Gettext catalogs for whois tools
Conflicts:      whois < 5.3.2-2
BuildArch:      noarch

%description nls
whois tools messages translated into different natural languages.

%prep
%setup -q -n %{name}

%build
%make_build CONFIG_FILE="%{_sysconfdir}/%{cfgfile}" \
    HAVE_ICONV=1 \
    CFLAGS="%{optflags}" LDFLAGS="%{__global_ldflags}"

%install
%if %{with whois_enables_mkpasswd}
make install-mkpasswd install-pos BASEDIR=%{buildroot}
%endif
make install-whois install-pos BASEDIR=%{buildroot}
install -p -m644 -D %{cfgfile} %{buildroot}%{_sysconfdir}/%{cfgfile}
%find_lang %{name}

# Rename to alternative names
mv %{buildroot}%{_bindir}/%{name}{,.%{alternative}}
touch %{buildroot}%{_bindir}/%{name}
chmod 755 %{buildroot}%{_bindir}/%{name}
mv %{buildroot}%{_mandir}/man1/%{name}{,.%{alternative}}.1
touch %{buildroot}%{_mandir}/man1/%{name}.1

%post
%{_sbindir}/update-alternatives \
    --install %{_bindir}/%{name} \
        %{genname} %{_bindir}/%{name}.%{alternative} 30 \
    --slave %{_mandir}/man1/%{name}.1.gz \
        %{genname}-man %{_mandir}/man1/%{name}.%{alternative}.1.gz

%postun
if [ $1 -eq 0 ] ; then
    %{_sbindir}/update-alternatives --remove \
        %{genname} %{_bindir}/%{name}.%{alternative}
fi

%files
%license COPYING debian/copyright
%doc README debian/changelog
%config(noreplace) %{_sysconfdir}/%{cfgfile}
%{_bindir}/%{name}.%{alternative}
%ghost %{_bindir}/%{name}
%{_mandir}/man1/%{name}.%{alternative}.*
%ghost %{_mandir}/man1/%{name}.1.gz
%{_mandir}/man5/%{cfgfile}.5.*

%files nls -f %{name}.lang

%if %{with whois_enables_mkpasswd}
%files -n mkpasswd
%license COPYING debian/copyright
%doc README debian/changelog
%{_bindir}/mkpasswd
%{_mandir}/man1/mkpasswd.*
%endif

%changelog
* Thu Feb 02 2023 Toshi Aoyama <toaoyama@microsoft.com> - 5.5.15-1
- 5.5.15 bump
- License verified

* Tue Jan 31 2023 Toshi Aoyama <toaoyama@microsoft.com> - 5.5.7-3
- Add requirement of iana-etc package.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 5.5.7-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Mon Oct 05 2020 Petr Pisar <ppisar@redhat.com> - 5.5.7-1
- 5.5.7 bump

* Mon Feb 17 2020 Petr Pisar <ppisar@redhat.com> - 5.5.6-1
- 5.5.6 bump

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 23 2020 Petr Pisar <ppisar@redhat.com> - 5.5.5-1
- 5.5.5 bump

* Wed Jan 15 2020 Petr Pisar <ppisar@redhat.com> - 5.5.4-2
- Fix hiding legal strings on at. subdomains (bug #1791035)

* Fri Jan 03 2020 Petr Pisar <ppisar@redhat.com> - 5.5.4-1
- 5.5.4 bump

* Mon Nov 18 2019 Petr Pisar <ppisar@redhat.com> - 5.5.3-1
- 5.5.3 bump

* Tue Oct 29 2019 Petr Pisar <ppisar@redhat.com> - 5.5.2-2
- Adjusts obsoletance for whois-mkpasswd-5.5.2 (bug #1684112)

* Thu Oct 03 2019 Jitka Plesnikova <jplesnik@redhat.com> - 5.5.2-1
- 5.5.2 bump

* Mon Aug 19 2019 Petr Pisar <ppisar@redhat.com> - 5.5.1-1
- 5.5.1 bump

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 23 2019 Petr Pisar <ppisar@redhat.com> - 5.5.0-1
- 5.5.0 bump

* Thu Jun 13 2019 Petr Pisar <ppisar@redhat.com> - 5.4.3-1
- 5.4.3 bump

* Wed Apr 24 2019 Petr Pisar <ppisar@redhat.com> - 5.4.2-2
- Modernize spec file

* Thu Mar 28 2019 Petr Pisar <ppisar@redhat.com> - 5.4.2-1
- 5.4.2 bump

* Tue Feb 26 2019 Petr Pisar <ppisar@redhat.com> - 5.4.1-3
- Adjust whois-mkpasswd obsoleteness to 5.4.1 rebase (bug #1649426)

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 28 2019 Petr Pisar <ppisar@redhat.com> - 5.4.1-1
- 5.4.1 bump

* Mon Jan 14 2019 Björn Esser <besser82@fedoraproject.org> - 5.4.0-3
- Rebuilt for libcrypt.so.2 (#1666033)

* Mon Nov 26 2018 Petr Pisar <ppisar@redhat.com> - 5.4.0-2
- Rename whois-mkpasswd package to mkpasswd (bug #1649456)

* Wed Nov 14 2018 Petr Pisar <ppisar@redhat.com> - 5.4.0-1
- 5.4.0 bump

* Tue Nov 13 2018 Petr Pisar <ppisar@redhat.com> - 5.3.2-2
- Package mkpasswd tool into whois-mkpasswd package (bug #1649426)

* Mon Jul 16 2018 Petr Pisar <ppisar@redhat.com> - 5.3.2-1
- 5.3.2 bump

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri May 25 2018 Petr Pisar <ppisar@redhat.com> - 5.3.1-1
- 5.3.1 bump

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 24 2018 Petr Pisar <ppisar@redhat.com> - 5.3.0-1
- 5.3.0 bump

* Tue Jan 02 2018 Petr Pisar <ppisar@redhat.com> - 5.2.20-1
- 5.2.20 bump

* Mon Dec 11 2017 Petr Pisar <ppisar@redhat.com> - 5.2.19-1
- 5.2.19 bump

* Wed Aug 23 2017 Petr Pisar <ppisar@redhat.com> - 5.2.18-1
- 5.2.18 bump

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Fri Jul 28 2017 Petr Pisar <ppisar@redhat.com> - 5.2.17-1
- 5.2.17 bump

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 13 2017 Petr Pisar <ppisar@redhat.com> - 5.2.16-1
- 5.2.16 bump

* Wed Apr 26 2017 Petr Pisar <ppisar@redhat.com> - 5.2.15-2
- Use libidn2 instead of libidn

* Mon Feb 27 2017 Petr Pisar <ppisar@redhat.com> - 5.2.15-1
- 5.2.15 bump

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 02 2017 Petr Pisar <ppisar@redhat.com> - 5.2.14-1
- 5.2.14 bump

* Mon Oct 31 2016 Petr Pisar <ppisar@redhat.com> - 5.2.13-1
- 5.2.13 bump

* Tue Mar 29 2016 Petr Pisar <ppisar@redhat.com> - 5.2.12-1
- 5.2.12 bump

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Dec 09 2015 Petr Pisar <ppisar@redhat.com> - 5.2.11-2
- Pass linker flags properly

* Tue Dec 08 2015 Petr Pisar <ppisar@redhat.com> - 5.2.11-1
- 5.2.11 bump

* Thu Jul 30 2015 Petr Pisar <ppisar@redhat.com> - 5.2.10-1
- 5.2.10 bump

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun 09 2015 Petr Pisar <ppisar@redhat.com> - 5.2.9-1
- 5.2.9 bump

* Tue May 19 2015 Petr Pisar <ppisar@redhat.com> - 5.2.8-1
- 5.2.8 bump

* Fri Mar 27 2015 Petr Pisar <ppisar@redhat.com> - 5.2.7-1
- 5.2.7 bump

* Tue Mar 24 2015 Petr Pisar <ppisar@redhat.com> - 5.2.6-2
- Fix a regression in hiding disclaimers

* Tue Mar 24 2015 Petr Pisar <ppisar@redhat.com> - 5.2.6-1
- 5.2.6 bump

* Tue Mar 03 2015 Petr Pisar <ppisar@redhat.com> - 5.2.5-1
- 5.2.5 bump

* Mon Feb 02 2015 Petr Pisar <ppisar@redhat.com> - 5.2.4-1
- 5.2.4 bump

* Mon Jan 05 2015 Petr Pisar <ppisar@redhat.com> - 5.2.3-1
- 5.2.3 bump

* Thu Nov 13 2014 Petr Pisar <ppisar@redhat.com> - 5.2.2-1
- 5.2.2 bump

* Fri Oct 17 2014 Petr Pisar <ppisar@redhat.com> - 5.2.1-1
- 5.2.1 bump

* Fri Sep 19 2014 Petr Pisar <ppisar@redhat.com> - 5.2.0-1
- 5.2.0 bump

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Aug 05 2014 Petr Pisar <ppisar@redhat.com> - 5.1.5-1
- 5.1.5 bump

* Mon Jul 07 2014 Petr Pisar <ppisar@redhat.com> - 5.1.4-1
- 5.1.4 bump

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 26 2014 Petr Pisar <ppisar@redhat.com> - 5.1.3-1
- 5.1.3 bump

* Wed May 07 2014 Petr Pisar <ppisar@redhat.com> - 5.1.2-1
- 5.1.2 bump

* Mon Jan 13 2014 Petr Pisar <ppisar@redhat.com> - 5.1.1-1
- 5.1.1 bump

* Tue Jan 07 2014 Petr Pisar <ppisar@redhat.com> - 5.1.0-1
- 5.1.0 bump

* Thu Nov 28 2013 Petr Pisar <ppisar@redhat.com> - 5.0.26-3
- Fix a typo in the manual (bug #1029065)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 5.0.26-1
- 5.0.26 bump

* Mon May 13 2013 Petr Pisar <ppisar@redhat.com> - 5.0.25-1
- 5.0.25 bump

* Thu Apr 18 2013 Petr Pisar <ppisar@redhat.com> - 5.0.24-1
- 5.0.24 bump

* Mon Apr 08 2013 Petr Pisar <ppisar@redhat.com> - 5.0.23-1
- 5.0.23 bump

* Thu Apr 04 2013 Petr Pisar <ppisar@redhat.com> - 5.0.22-1
- 5.0.22 bump

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 08 2012 Petr Pisar <ppisar@redhat.com> - 5.0.20-1
- 5.0.20 bump

* Wed Sep 19 2012 Petr Pisar <ppisar@redhat.com> - 5.0.19-1
- 5.0.19 bump

* Thu Aug 02 2012 Petr Pisar <ppisar@redhat.com> - 5.0.18-1
- 5.0.18 bump

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jul 13 2012 Petr Pisar <ppisar@redhat.com> - 5.0.17-2
- .xn--mgbaam7a8 is handled by whois.aeda.net.ae (bug #839893)
- Document how to write IDN in whois.conf (bug #839898)

* Wed Jun 27 2012 Petr Pisar <ppisar@redhat.com> - 5.0.17-1
- 5.0.17 bump

* Mon Apr 30 2012 Petr Pisar <ppisar@redhat.com> - 5.0.16-1
- 5.0.16 bump

* Thu Mar 08 2012 Petr Pisar <ppisar@redhat.com> - 5.0.15-1
- 5.0.15 bump

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jan 02 2012 Petr Pisar <ppisar@redhat.com> - 5.0.14-1
- 5.0.14 bump

* Mon Nov 28 2011 Petr Pisar <ppisar@redhat.com> - 5.0.13-1
- 5.0.13 bump

* Wed Oct 12 2011 Petr Pisar <ppisar@redhat.com> - 5.0.12-1
- 5.0.12 bump
- Remove defattr from spec code

* Thu Mar 03 2011 Petr Pisar <ppisar@redhat.com> - 5.0.11-1
- 5.0.11 bump

* Mon Dec 06 2010 Petr Pisar <ppisar@redhat.com> - 5.0.10-1
- 5.0.10 bump

* Wed Sep 29 2010 Petr Pisar <ppisar@redhat.com> - 5.0.7-1
- 5.0.7 imported
