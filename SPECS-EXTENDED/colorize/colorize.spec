Summary:        Perl script to colorize logs
Name:           colorize
Version:        0.3.4
Release:        22%{?dist}
License:        GPLv2+
Vendor:		Microsoft Corporation
Distribution:   Azure Linux
Source0:        https://web.archive.org/web/20040604132106/https://colorize.raszi.hu/downloads/colorize_0.3.4.tar.bz2
# https://web.archive.org/web/20040607115833/colorize.raszi.hu/
URL:            https://colorize.raszi.hu/
BuildRequires:  perl
BuildRequires:	perl-generators
BuildArch:      noarch

%description
This is a short perl script to colorize your logs. You can use your
own colors, you can simply modify your config file in your home
directory, or system-wide (/etc/colorize).

%prep
%setup -q

%build

%install
rm -rf %{buildroot}
install -d %{buildroot}{%{_bindir},%{_mandir}/man1,%{_sysconfdir}}

install colorize %{buildroot}%{_bindir}/colorize
install colorize.1.gz %{buildroot}%{_mandir}/man1/
install colorizerc %{buildroot}%{_sysconfdir}/colorizerc

%files
%doc changelog.gz copyright examples/ README THANKS TIPS TODO
%attr(755,root,root) %{_bindir}/colorize
%{_mandir}/man1/colorize.1*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/colorizerc

%changelog
* Mon Dec 27 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 0.3.4-22
- Initial CBL-Mariner import from Fedora 35 (license: MIT)
- License verified

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.4-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.4-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.4-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.4-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.4-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.4-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.4-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.4-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 0.3.4-7
- Perl 5.18 rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 17 2010 Pavel Alexeev <Pahan@Hubbitus.info> - 0.3.4-2
- Changes in review process. Thanks to Manuel Wolfshant.
- Delete old PLD changelog entries.
- Replace source0 by webarchive working link.

* Sat Jul 11 2009 Pavel Alexeev <Pahan@Hubbitus.info> - 0.3.4-1
- Imported from ftp://ftp.icm.edu.pl/vol/rzm1/linux-pld-linux/dists/3.0/PLD/SRPMS/RPMS/colorize-0.3.4-1.src.rpm
- All Log saved, but it is not in common format, so, all commented.
- Summary(pl.UTF-8), Description -l pl.UTF-8 turned to just Summary(pl), Description -l pl
- Add Summary(ru), Description -l ru
- $RPM_BUILD_ROOT replaced by %%{buildroot}
- Replace buildRoot from "%%{tmpdir}/%%{name}-%%{version}-root-%%(id -u -n)" to Fedora standard one.
- Delete %%include	/usr/lib/rpm/macros.perl
- Add empty %%build section (to do not shut rpmlint)
- Add %%{?dist} part into Release.
- BuildRequires: perl-base replaced bu simple BuildRequires:	perl
- Delete Requires: perl-Term-ANSIColor because: 1) It is incorrect, 2) Such dependencies should be automatically handled by rpm.
- Licence changed to GPLv2+ from GPL
