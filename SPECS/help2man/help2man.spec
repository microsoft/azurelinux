# Supported build option:
#
# --with nls ... build this package with --enable-nls 
%bcond_with nls

Summary:        Create simple man pages from --help output
Name:           help2man
Version:        1.49.3
Release:        1%{?dist}
License:        GPLv3+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.gnu.org/software/help2man
Source:         ftp://ftp.gnu.org/gnu/help2man/help2man-%{version}.tar.xz

%{!?with_nls:BuildArch: noarch}

BuildRequires:  gcc
BuildRequires:  perl-generators
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Text::ParseWords)
BuildRequires:  perl(Text::Tabs)
BuildRequires:  perl(strict)
%{?with_nls:BuildRequires: perl(Locale::gettext) %{_bindir}/msgfmt}
%{?with_nls:BuildRequires: perl(Encode)}
%{?with_nls:BuildRequires: perl(I18N::Langinfo)}

%description
help2man is a script to create simple man pages from the --help and
--version output of programs.

Since most GNU documentation is now in info format, this provides a
way to generate a placeholder man page pointing to that resource while
still providing some useful information.

%prep
%setup -q -n help2man-%{version}

%build
%configure --%{!?with_nls:disable}%{?with_nls:enable}-nls --libdir=%{_libdir}/help2man
make %{?_smp_mflags}

%install
make install_l10n DESTDIR=%{buildroot}
make install DESTDIR=%{buildroot}
%find_lang %{name} --with-man

%files -f %{name}.lang
%doc README NEWS THANKS
%license COPYING
%{_bindir}/help2man
%{_infodir}/*
%{_mandir}/man1/*

%if %{with nls}
%{_libdir}/help2man
%endif

%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.49.3-1
- Auto-upgrade to 1.49.3 - Azure Linux 3.0 - package upgrades

* Thu Sep 02 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.47.14-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- License verified.
- Using HTTPS in the 'URL' tag.

* Sat Apr 25 2020 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.47.14-1
- Upstream update.

* Wed Mar 18 2020 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.47.13-1
- Upstream update.

* Tue Mar 17 2020 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.47.12-1
- Upstream update.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.47.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Sep 14 2019 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.47.11-1
- Upstream update.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.47.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Mar 23 2019 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.47.10-1
- Upstream update.

* Tue Mar 19 2019 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.47.9-1
- Upstream update.

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.47.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.47.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar 01 2018 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.47.6-1
- Upstream update.

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.47.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Sep 23 2017 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.47.5-1
- Upstream update.

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.47.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.47.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon May 09 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.47.4-1
- Upstream update.

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.47.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Dec 17 2015 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.47.3-1
- Upstream update.

* Sun Sep 13 2015 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.47.2-1
- Upstream update.

* Tue Jun 16 2015 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.47.1-1
- Upstream update.
- Add %%license.

* Mon Apr 27 2015 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.46.6-1
- Upstream update.

* Tue Feb 17 2015 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.46.5-1
- Upstream update.

* Fri Oct 31 2014 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.46.4-1
- Upstream update.

* Sun Oct 05 2014 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.46.3-1
- Upstream update.

* Tue Sep 16 2014 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.46.2-1
- Upstream update.

* Fri Aug 22 2014 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.46.1-1
- Upstream update.

* Mon Jul 14 2014 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.45.1-1
- Upstream update.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.44.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Mar 13 2014 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.44.1-1
- Upstream update.
- Add finer-grained perl deps.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.43.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.43.3-2
- Perl 5.18 rebuild

* Wed Jul 17 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.43.3-1
- Upstream update.

* Wed Jul 17 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.41.2-1
- Upstream update.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.41.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan 17 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.41.1-1
- Upstream update.

* Thu Jan 17 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.40.13-1
- Upstream update.
- BR: /usr/bin/msgfmt if building with nls enabled.

* Thu Oct 04 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.40.12-1
- Upstream update.

* Fri Jul 20 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.40.10-1
- Upstream update.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.40.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr 12 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.40.8-1
- Upstream update.

* Sat Feb 18 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.40.6-1
- Upstream update.

* Thu Jan 05 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.40.5-1
- Upstream update.

* Thu Dec 15 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.40.4-1
- Upstream update.

* Wed Jun 08 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.40.2-1
- Upstream update.

* Fri Apr 22 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.39.2-1
- Upstream update.
- Spec modernization.
- Abandon patches (unnecessary).

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.38.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Aug 27 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.38.2-1
- Upstream update.
- Add *-locales.diff, *-mans.diff.
- Use %%find_lang --with-man.
- Use %%bcond_with nls.

* Tue Feb 23 2010 Ondrej Vasik <ovasik@redhat.com> - 1.36.4-6
- do ship COPYING file in %%doc

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.36.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon May 18 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.36.4-4
- Apply patch from http://bugs.gentoo.org/show_bug.cgi?id=237378#c6
  to address BZ #494089.

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.36.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Feb 10 2008 Ralf Corsépius <rc040203@freenet.de> - 1.36.4-2
- Update license tag.
- Convert THANKS to utf-8.

* Tue Sep 05 2006 Ralf Corsépius <rc040203@freenet.de> - 1.36.4-1
- Upstream update.
- utf-8 encode l10n'd man pages.

* Fri Dec 23 2005 Ralf Corsépius <rc04203@freenet.de> - 1.36.3-1
- Upstream update.
- Add build option --with nls.

* Fri Dec 23 2005 Ralf Corsépius <rc04203@freenet.de> - 1.35.1-2
- Fix disttag (#176473).
- Cleanup spec.

* Fri Apr 29 2005 Ralf Corsepius <ralf[AT]links2linux.de> - 1.35.1-1
- Update to 1.35.1
- Minor spec fixes.
