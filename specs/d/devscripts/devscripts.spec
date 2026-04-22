# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           devscripts
Version:        2.25.33
Release: 2%{?dist}
Summary:        Scripts for Debian Package maintainers
BuildArch:      noarch

License:        GPL-2.0-or-later
URL:            https://tracker.debian.org/pkg/%{name}
Source0:        http://ftp.debian.org/debian/pool/main/d/%{name}/%{name}_%{version}.tar.xz
# Fixes path to xsl-stylesheet manpages docbook.xsl
Patch0:         devscripts_docbook.patch
# Removes the debian-only --install-layout python-setuptools option
Patch1:         devscripts_install-layout.patch
# Install some additional man pages
Patch2:         devscripts_install-man.patch

BuildRequires:  make
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(base)
BuildRequires:  perl(constant)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(DB_File)
BuildRequires:  perl(Digest::MD5)
BuildRequires:  perl(Dpkg::Changelog::Debian)
BuildRequires:  perl(Dpkg::Changelog::Parse)
BuildRequires:  perl(Dpkg::Control)
BuildRequires:  perl(Dpkg::Control::Hash)
BuildRequires:  perl(Dpkg::Vendor)
BuildRequires:  perl(Dpkg::Version)
BuildRequires:  perl(Encode)
BuildRequires:  perl(Encode::Locale)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(feature)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::DesktopEntry)
BuildRequires:  perl(File::DirList)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::HomeDir)
BuildRequires:  perl(FileHandle)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(filetest)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(Git::Wrapper)
BuildRequires:  perl(IO::Dir)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IPC::Run)
BuildRequires:  perl(JSON::PP)
BuildRequires:  perl(List::Compare)
BuildRequires:  perl(List::Util)
BuildRequires:  perl(LWP::UserAgent)
BuildRequires:  perl(Net::SMTP)
BuildRequires:  perl(open)
BuildRequires:  perl(Parse::DebControl)
BuildRequires:  perl(Pod::Checker)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(strict)
BuildRequires:  perl(Text::ParseWords)
BuildRequires:  perl(Text::Wrap)
BuildRequires:  perl(URI) >= 1.37
BuildRequires:  perl(URI::QueryParam)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)

BuildRequires:  docbook-style-xsl
BuildRequires:  libxslt
BuildRequires:  po4a
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  /usr/bin/dpkg-buildflags
BuildRequires:  /usr/bin/dpkg-vendor
BuildRequires:  /usr/bin/dpkg-parsechangelog
BuildRequires:  /usr/bin/help2man
BuildRequires:  pkgconfig(bash-completion)

Requires:       dpkg-dev
Requires:       sensible-utils
# man for manpage-alert
Requires:       %{_bindir}/man
Requires:       %{name}-checkbashisms

%description
Scripts to make the life of a Debian Package maintainer easier.

%package checkbashisms
Summary:        Devscripts checkbashisms script

%description checkbashisms
This package contains the devscripts checkbashisms script.


%prep
%autosetup -p1 -C


%build
%make_build


%install
%make_install

# Install docs through %%doc
rm -rf %{buildroot}%{_datadir}/doc

# archpath requires tla (gnu-arch) or baz (bazaar), both of which are obsolete
# and the respective Fedora packages dead. See #1128503
rm %{buildroot}%{_bindir}/archpath %{buildroot}%{_mandir}/man1/archpath*

# whodepends requires configured deb repositories
rm %{buildroot}%{_bindir}/whodepends %{buildroot}%{_mandir}/man1/whodepends*

# Create symlinks like the debian package does
ln -s %{_bindir}/cvs-debi      %{buildroot}%{_bindir}/cvs-debc
ln -s %{_bindir}/debchange     %{buildroot}%{_bindir}/dch
ln -s %{_bindir}/pts-subscribe %{buildroot}%{_bindir}/pts-unsubscribe
ln -s %{_mandir}/man1/debchange.1.gz     %{buildroot}%{_mandir}/man1/dch.1.gz
ln -s %{_mandir}/man1/pts-subscribe.1.gz %{buildroot}%{_mandir}/man1/pts-unsubscribe.1.gz

# This already is in bash-completion
rm -f %{buildroot}%{_datadir}/bash-completion/completions/bts


%files
%doc README.md
%license COPYING
%{_datadir}/bash-completion
%{_bindir}/*
%{python3_sitelib}/%{name}
%{python3_sitelib}/%{name}*.egg-info/
%{_datadir}/%{name}/
%{_mandir}/man1/*
%{_mandir}/man7/*
%{perl_vendorlib}/Devscripts
%exclude %{_bindir}/checkbashisms
%exclude %{_mandir}/man1/checkbashisms.1*
%exclude %{_datadir}/bash-completion/completions/checkbashisms

%files checkbashisms
%license COPYING
%{_bindir}/checkbashisms
%{_mandir}/man1/checkbashisms.1*
%{_mandir}/man5/devscripts.conf.5*
%dir %{_datadir}/bash-completion
%dir %{_datadir}/bash-completion/completions
%{_datadir}/bash-completion/completions/checkbashisms


%changelog
* Tue Dec 30 2025 Sandro Mani <manisandro@gmail.com> - 2.25.33-1
- Update to 2.25.33

* Tue Dec 23 2025 Sandro Mani <manisandro@gmail.com> - 2.25.32-1
- Update to 2.25.32

* Wed Dec 17 2025 Sandro Mani <manisandro@gmail.com> - 2.25.31-1
- Update to 2.25.31

* Sat Dec 13 2025 Sandro Mani <manisandro@gmail.com> - 2.25.30-1
- Update to 2.25.30

* Fri Dec 05 2025 Sandro Mani <manisandro@gmail.com> - 2.25.29-1
- Update to 2.25.29

* Wed Dec 03 2025 Sandro Mani <manisandro@gmail.com> - 2.25.28-1
- Update to 2.25.28

* Sat Nov 22 2025 Sandro Mani <manisandro@gmail.com> - 2.25.27-1
- Update to 2.25.27

* Sat Nov 22 2025 Sandro Mani <manisandro@gmail.com> - 2.25.26-1
- Update to 2.25.26

* Thu Nov 06 2025 Sandro Mani <manisandro@gmail.com> - 2.25.25-1
- Update to 2.25.25

* Tue Oct 28 2025 Sandro Mani <manisandro@gmail.com> - 2.25.22-1
- Update to 2.25.22

* Sun Oct 26 2025 Sandro Mani <manisandro@gmail.com> - 2.25.21-1
- Update to 2.25.21

* Tue Oct 21 2025 Sandro Mani <manisandro@gmail.com> - 2.25.20-1
- Update to 2.25.20

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 2.25.19-2
- Rebuilt for Python 3.14.0rc3 bytecode

* Mon Aug 25 2025 Sandro Mani <manisandro@gmail.com> - 2.25.19-1
- Update to 2.25.19

* Sat Aug 16 2025 Sandro Mani <manisandro@gmail.com> - 2.25.18-1
- Update to 2.25.18

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 2.25.17-2
- Rebuilt for Python 3.14.0rc2 bytecode

* Tue Jul 29 2025 Sandro Mani <manisandro@gmail.com> - 2.25.17-1
- Update to 2.25.17

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.25.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jul 20 2025 Sandro Mani <manisandro@gmail.com> - 2.25.16-1
- Update to 2.25.16

* Tue Jun 17 2025 Sandro Mani <manisandro@gmail.com> - 2.25.15-1
- Update to 2.25.15

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 2.25.14-2
- Rebuilt for Python 3.14

* Thu May 29 2025 Sandro Mani <manisandro@gmail.com> - 2.25.14-1
- Update to 2.25.14

* Sun May 11 2025 Sandro Mani <manisandro@gmail.com> - 2.25.12-1
- Update to 2.25.12

* Sat May 03 2025 Sandro Mani <manisandro@gmail.com> - 2.25.11-1
- Update to 2.25.11

* Thu Apr 17 2025 Sandro Mani <manisandro@gmail.com> - 2.25.10-1
- Update to 2.25.10

* Tue Apr 15 2025 Sandro Mani <manisandro@gmail.com> - 2.25.9-1
- Update to 2.25.9

* Wed Apr 02 2025 Packit <hello@packit.dev> - 2.25.7-1
- Update to version 2.25.7
- Resolves: rhbz#2355676

* Tue Feb 25 2025 Packit <hello@packit.dev> - 2.25.5-1
- Update to version 2.25.5
- Resolves: rhbz#2343865

* Fri Jan 24 2025 Sandro Mani <manisandro@gmail.com> - 2.25.1-1
- Update to 2.25.1

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.24.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jan 01 2025 Sandro Mani <manisandro@gmail.com> - 2.24.10-1
- Update to 2.24.10

* Sat Dec 28 2024 Sandro Mani <manisandro@gmail.com> - 2.24.9-1
- Update to 2.24.9

* Wed Dec 25 2024 Sandro Mani <manisandro@gmail.com> - 2.24.8-1
- Update to 2.24.8

* Sun Dec 15 2024 Sandro Mani <manisandro@gmail.com> - 2.24.7-1
- Update to 2.24.7

* Mon Dec 02 2024 Sandro Mani <manisandro@gmail.com> - 2.24.5-1
- Update to 2.24.5

* Thu Nov 14 2024 Sérgio Basto <sergio@serjux.com> - 2.24.3-2
- Change homepage URL to https://tracker.debian.org/pkg/devscripts

* Tue Nov 12 2024 Sérgio M. Basto <sergio@serjux.com> - 2.24.3-1
- Update to version 2.24.3

* Sun Nov 03 2024 Sandro Mani <manisandro@gmail.com> - 2.24.2-1
- Update to 2.24.2

* Thu Sep 19 2024 Sandro Mani <manisandro@gmail.com> - 2.24.1-1
- Update to 2.24.1

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.23.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 2.23.7-4
- Rebuilt for Python 3.13

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.23.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.23.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Dec 13 2023 Sandro Mani <manisandro@gmail.com> - 2.23.7-1
- Update to 2.23.7

* Wed Aug 23 2023 Sandro Mani <manisandro@gmail.com> - 2.23.6-1
- Update to 2.23.6

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.23.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jun 16 2023 Python Maint <python-maint@redhat.com> - 2.23.5-2
- Rebuilt for Python 3.12

* Thu Jun 15 2023 Sandro Mani <manisandro@gmail.com> - 2.23.5-1
- Update to 2.23.5

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 2.23.4-2
- Rebuilt for Python 3.12

* Wed Apr 05 2023 Sandro Mani <manisandro@gmail.com> - 2.23.4-1
- Update to 2.23.4

* Sun Mar 19 2023 Sandro Mani <manisandro@gmail.com> - 2.23.3-1
- Update to 2.23.3

* Mon Feb 20 2023 Sandro Mani <manisandro@gmail.com> - 2.23.2-1
- Update to 2.23.2

* Sat Feb 11 2023 Sandro Mani <manisandro@gmail.com> - 2.23.1-1
- Update to 2.23.1

* Sun Feb 05 2023 Sandro Mani <manisandro@gmail.com> - 2.23.0-1
- Update to 2.23.0

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.22.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.22.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun Jun 19 2022 Python Maint <python-maint@redhat.com> - 2.22.2-2
- Rebuilt for Python 3.11

* Sun Jun 19 2022 Sandro Mani <manisandro@gmail.com> - 2.22.2-1
- Update to 2.22.2

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 2.22.1-3
- Rebuilt for Python 3.11

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2.22.1-2
- Perl 5.36 rebuild

* Tue Jan 25 2022 Sandro Mani <manisandro@gmail.com> - 2.22.1-1
- Update to 2.22.1

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.21.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sun Dec 12 2021 Sandro Mani <manisandro@gmail.com> - 2.21.7-1
- Update to 2.21.7

* Wed Dec 01 2021 Sandro Mani <manisandro@gmail.com> - 2.21.6-1
- Update to 2.21.6

* Thu Nov 11 2021 Sandro Mani <manisandro@gmail.com> - 2.21.5-1
- Update to 2.21.5

* Thu Aug 19 2021 Sandro Mani <manisandro@gmail.com> - 2.21.4-1
- Update to 2.21.4

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.21.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jul 05 2021 Sandro Mani <manisandro@gmail.com> - 2.21.3-1
- Update to 2.21.3

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.21.2-3
- Rebuilt for Python 3.10

* Sun May 23 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.21.2-2
- Perl 5.34 rebuild

* Mon May 03 2021 Sandro Mani <manisandro@gmail.com> - 2.21.2-1
- Update to 2.21.2

* Wed Feb 17 2021 Sandro Mani <manisandro@gmail.com> - 2.21.1-1
- Update to 2.21.1

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.20.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Dec  2 12:57:12 CET 2020 Sandro Mani <manisandro@gmail.com> - 2.20.5-2
- Rebuild for changed perl(File::DirList) dependency

* Sat Nov 28 2020 Sandro Mani <manisandro@gmail.com> - 2.20.5-1
- Update to 2.20.5

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.20.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 30 2020 Sérgio Basto <sergio@serjux.com> - 2.20.4-1
- Update devscripts to 2.20.4 (#1851772)

* Thu Jun 25 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.20.3-3
- Perl 5.32 rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 2.20.3-2
- Rebuilt for Python 3.9

* Sat Apr 25 2020 Sandro Mani <manisandro@gmail.com> - 2.20.3-1
- Update to 2.20.3

* Thu Feb 06 2020 Sandro Mani <manisandro@gmail.com> - 2.20.2-1
- Update to 2.20.2

* Fri Jan 31 2020 Sandro Mani <manisandro@gmail.com> - 2.20.1-1
- Update to 2.20.1

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.19.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 17 2019 Sandro Mani <manisandro@gmail.com> - 2.19.7-1
- Update to 2.19.7

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 2.19.6-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 2.19.6-3
- Rebuilt for Python 3.8

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.19.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 22 2019 Sandro Mani <manisandro@gmail.com> - 2.19.6-1
- Update to 2.19.6

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.19.5-2
- Perl 5.30 rebuild

* Mon May 13 2019 Sandro Mani <manisandro@gmail.com> - 2.19.5-1
- Update to 2.19.5

* Tue Mar 26 2019 Sandro Mani <manisandro@gmail.com> - 2.19.4-1
- Update to 2.19.4

* Mon Feb 18 2019 Sandro Mani <manisandro@gmail.com> - 2.19.3-1
- Update to 2.19.3

* Tue Feb 12 2019 Pete Walter <pwalter@fedoraproject.org> - 2.19.2-4
- Obsolete devscripts-compat

* Mon Feb 11 2019 Björn Esser <besser82@fedoraproject.org> - 2.19.2-3
- Add Obsoletes / Provides for hardening-check (#1508087, 1536718)

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.19.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 14 2019 Sandro Mani <manisandro@gmail.com> - 2.19.2-1
- Update to 2.19.2

* Mon Dec 10 2018 Sandro Mani <manisandro@gmail.com> - 2.18.10-1
- Update to 2.18.10

* Tue Nov 13 2018 Sandro Mani <manisandro@gmail.com> - 2.18.9-1
- Update to 2.18.9

* Tue Nov 13 2018 Sandro Mani <manisandro@gmail.com> - 2.18.8-1
- Update to 2.18.8

* Sat Oct 27 2018 Sandro Mani <manisandro@gmail.com> - 2.18.7-1
- Update to 2.18.7

* Fri Oct 05 2018 Sandro Mani <manisandro@gmail.com> - 2.18.6-1
- Update to 2.18.6

* Thu Oct 04 2018 Sandro Mani <manisandro@gmail.com> - 2.18.5-1
- Update to 2.18.5

* Tue Sep 04 2018 Sandro Mani <manisandro@gmail.com> - 2.18.4-1
- Update to 2.18.4

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 03 2018 Petr Pisar <ppisar@redhat.com> - 2.18.3-4
- Perl 5.28 rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.18.3-3
- Perl 5.28 rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 2.18.3-2
- Rebuilt for Python 3.7

* Mon May 28 2018 Sandro Mani <manisandro@gmail.com> - 2.18.3-1
- Update to 2.18.3

* Mon Apr 23 2018 Sandro Mani <manisandro@gmail.com> - 2.18.2-1
- Update to 2.18.2

* Wed Mar 07 2018 Sandro Mani <manisandro@gmail.com> - 2.18.1-1
- Update to 2.18.1

* Sun Feb 18 2018 Sandro Mani <manisandro@gmail.com> - 2.17.12-3
- Add missing BR: gcc, make

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.17.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Dec 31 2017 Sandro Mani <manisandro@gmail.com> - 2.17.12-1
- Update to 2.17.12

* Mon Oct 30 2017 Sandro Mani <manisandro@gmail.com> - 2.17.11-1
- Update to 2.17.11

* Thu Sep 14 2017 Sandro Mani <manisandro@gmail.com> - 2.17.10-1
- Update to 2.17.10

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.17.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Sandro Mani <manisandro@gmail.com> - 2.17.9-1
- Update to 2.17.9

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.17.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jul 11 2017 Sandro Mani <manisandro@gmail.com> - 2.17.8-1
- Update to 2.17.8

* Sun Jul 09 2017 Sandro Mani <manisandro@gmail.com> - 2.17.7-1
- Update to 2.17.7

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.17.6-2
- Perl 5.26 rebuild

* Sun Jun 04 2017 Sandro Mani <manisandro@gmail.com> - 2.17.6-1
- Update to 2.17.6

* Sun Mar 19 2017 Sandro Mani <manisandro@gmail.com> - 2.17.5-1
- Update to 2.17.5

* Sat Mar 18 2017 Sandro Mani <manisandro@gmail.com> - 2.17.4-1
- Update to 2.17.4

* Mon Mar 06 2017 Sandro Mani <manisandro@gmail.com> - 2.17.2-1
- Update to 2.17.2

* Wed Feb 15 2017 Igor Gnatenko <ignatenko@redhat.com> - 2.17.1-4
- Rebuild for brp-python-bytecompile

* Mon Feb 13 2017 Sérgio Basto <sergio@serjux.com> - 2.17.1-3
- Epel 7 fixes: python3 requires and one compile error

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.17.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 02 2017 Sandro Mani <manisandro@gmail.com> - 2.17.1-1
- Update to 2.17.1

* Fri Jan 13 2017 Sandro Mani <manisandro@gmail.com> - 2.17.0-1
- Update to 2.17.0

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 2.16.13-2
- Rebuild for Python 3.6

* Sat Dec 17 2016 Sandro Mani <manisandro@gmail.com> - 2.16.13-1
- Update to 2.16.13

* Sun Dec 11 2016 Sandro Mani <manisandro@gmail.com> - 2.16.12-1
- Update to 2.16.12

* Wed Dec 07 2016 Sandro Mani <manisandro@gmail.com> - 2.16.11-1
- Update to 2.16.11

* Thu Nov 24 2016 Sandro Mani <manisandro@gmail.com> - 2.16.10-1
- Update to 2.16.10

* Thu Nov 24 2016 Sandro Mani <manisandro@gmail.com> - 2.16.9-1
- Update to 2.16.9

* Tue Oct 18 2016 Sandro Mani <manisandro@gmail.com> - 2.16.8-1
- Update to 2.16.8

* Mon Sep 05 2016 Sandro Mani <manisandro@gmail.com> - 2.16.7-1
- Update to 2.16.7

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.16.6-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Jul 06 2016 Sandro Mani <manisandro@gmail.com> - 2.16.6-1
- Update to 2.16.6
- Introduce devscripts-checkbashisms
- Introduce devscripts-compat compatibility package for
  devscripts-minimal -> {devscripts-checkbashisms, licensecheck} transition
- Remove Conflicts: rpmdevtools < 8.4, no current version of Fedora ships rpmdevtools < 8.4
- Drop unused BRs

* Sun Jun 05 2016 Sandro Mani <manisandro@gmail.com> - 2.16.5-1
- Update to 2.16.5

* Tue May 17 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.16.4-2
- Perl 5.24 rebuild

* Mon Apr 25 2016 Sandro Mani <manisandro@gmail.com> - 2.16.4-1
- Update to 2.16.4

* Mon Mar 21 2016 Sandro Mani <manisandro@gmail.com> - 2.16.2-1
- Update to 2.16.2

* Fri Feb 12 2016 Sandro Mani <manisandro@gmail.com> - 2.16.1-1
- Update to 2.16.1

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.15.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Jan 03 2016 Sandro Mani <manisandro@gmail.com> - 2.15.10-2
- Exclude %%{_datadir}/bash-completion/completions/bts which already is in bash-completion

* Thu Dec 31 2015 Sandro Mani <manisandro@gmail.com> - 2.15.10-1
- Update to 2.15.10

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.15.9-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Fri Oct 09 2015 Sandro Mani <manisandro@gmail.com> - 2.15.9-2
- Add devscripts_ipc-run.patch to remove dpkg-perl dependency on licensecheck

* Tue Oct 06 2015 Sandro Mani <manisandro@gmail.com> - 2.15.9-1
- Update to 2.15.9

* Mon Aug 03 2015 Sandro Mani <manisandro@gmail.com> - 2.15.8-1
- Update to 2.15.8

* Sat Aug 01 2015 Sandro Mani <manisandro@gmail.com> - 2.15.7-1
- Update to 2.15.7

* Sat Aug 01 2015 Sandro Mani <manisandro@gmail.com> - 2.15.6-2
- Fix licensecheck incorrectly detecting mime strings such as text/x-c++ as a binary file (#1249227)

* Wed Jul 29 2015 Sandro Mani <manisandro@gmail.com> - 2.15.6-1
- Update to 2.15.6

* Thu Jul 09 2015 Sandro Mani <manisandro@gmail.com> - 2.15.5-6
- Make licensecheck print a warning when scanned file is not a text file (#1240914)

* Fri Jun 26 2015 Sandro Mani <manisandro@gmail.com> - 2.15.5-5
- Create symlinks like the debian package does (#1236122)

* Wed Jun 17 2015 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.15.5-4
- Add: "Requires: perl(:MODULE_COMPAT_...)"

* Wed Jun 17 2015 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.15.5-3
- Fix FTBFS.
- Eliminate libvfork, PKGLIBDIR (Abandoned upstream).
- Rework perl-BRs.
- Reflect upstream installing perl-modules into perl_vendordir.
- Reflect upstream installing bash-completion into /usr/share/bash-completion.
- BR: /usr/bin/dpkg-buildflags, /usr/bin/dpkg-vendor, /usr/bin/dpkg-parsechangelog.
- BR: pkgconfig(bash-completion).
- Remove archpath, whodepends's man-pages.
- Rebase patches.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.15.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 12 2015 Sandro Mani <manisandro@gmail.com> - 2.15.5-1
- Update to 2.15.5

* Tue Apr 28 2015 Sandro Mani <manisandro@gmail.com> - 2.15.4-1
- Update to 2.15.4

* Mon Apr 13 2015 Sandro Mani <manisandro@gmail.com> - 2.15.3-1
- Update to 2.15.3

* Fri Apr 03 2015 Sandro Mani <manisandro@gmail.com> - 2.15.2-1
- Update to 2.15.2
- Don't install whodepends (#1185511)

* Fri Jan 02 2015 Sandro Mani <manisandro@gmail.com> - 2.15.1-1
- Update to 2.15.1

* Thu Dec 04 2014 Sandro Mani <manisandro@gmail.com> - 2.14.11-1
- Update to 2.14.11

* Wed Oct 15 2014 Sandro Mani <manisandro@gmail.com> - 2.14.10-1
- Update to 2.14.10

* Mon Oct 13 2014 Sandro Mani <manisandro@gmail.com> - 2.14.9-1
- Update to 2.14.9

* Sat Oct 11 2014 Sandro Mani <manisandro@gmail.com> - 2.14.8-1
- Update to 2.14.8, fixes CVE-2014-1833 (#1059947)

* Fri Sep 26 2014 Sandro Mani <manisandro@gmail.com> - 2.14.7-1
- Update to 2.14.7

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.14.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Aug 11 2014 Sandro Mani <manisandro@gmail.com> - 2.14.6-2
- Remove /usr/bin/archpath from package (#1128503)

* Wed Aug 06 2014 Sandro Mani <manisandro@gmail.com> - 2.14.6-1
- Update to 2.14.6

* Wed Jun 11 2014 Sandro Mani <manisandro@gmail.com> - 2.14.5-1
- Update to 2.14.5

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.14.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jun 02 2014 Sandro Mani <manisandro@gmail.com> - 2.14.4-1
- Update to 2.14.4

* Thu May 29 2014 Sandro Mani <manisandro@gmail.com> - 2.14.3-1
- Update to 2.14.3

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 2.14.2-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Mon May 12 2014 Sandro Mani <manisandro@gmail.com> - 2.14.2-1
- Update to 2.14.2

* Thu Feb 27 2014 Sandro Mani <manisandro@gmail.com> - 2.14.1-2
- Require sensible-utils (rhbz#1067869)

* Sun Jan 26 2014 Sandro Mani <manisandro@gmail.com> - 2.14.1-1
- Update to 2.14.1

* Wed Dec 25 2013 Sandro Mani <manisandro@gmail.com> - 2.13.9-1
- Update to 2.13.9
- Fixes CVE-2013-7085 (rhbz#1040949)

* Wed Dec 11 2013 Sandro Mani <manisandro@gmail.com> - 2.13.8-1
- Update to 2.13.8

* Wed Dec 11 2013 Sandro Mani <manisandro@gmail.com> - 2.13.5-2
- Add upstream patch to fix arbitrary command execution when using
  USCAN_EXCLUSION (rhbz#1040266, debian#731849)

* Thu Dec 05 2013 Sandro Mani <manisandro@gmail.com> - 2.13.5-1
- Update to 2.13.5

* Sun Oct 20 2013 Sandro Mani <manisandro@gmail.com> - 2.13.4-5
- Honour RPM_LD_FLAGS

* Sat Oct 19 2013 Sandro Mani <manisandro@gmail.com> - 2.13.4-4
- Honour optflags
- Improve -minimal subpackage description

* Thu Oct 17 2013 Sandro Mani <manisandro@gmail.com> - 2.13.4-3
- Split scripts used by rpm developers into a subpackage
- Install some additional manpages

* Mon Oct  7 2013 Ville Skyttä <ville.skytta@iki.fi> - 2.13.4-2
- Add dependency on man for manpage-alert.

* Mon Oct 07 2013 Sandro Mani <manisandro@gmail.com> - 2.13.4-1
- Update to 2.13.4
- Drop devscripts_item.patch
- Drop devscripts_spurious-pod.patch

* Sat Sep 21 2013 Sandro Mani <manisandro@gmail.com> - 2.13.3-5
- Fix typo builroot -> buildroot
- Require perl modules instead of the providing packages

* Fri Sep 20 2013 Sandro Mani <manisandro@gmail.com> - 2.13.3-4
- Conflict with rpmdevtools < 8.4

* Fri Sep 20 2013 Sandro Mani <manisandro@gmail.com> - 2.13.3-3
- Revert: Require rpmdevtools and drop scripts which are in rpmdevtools
- Add conflicts from rpmdevtools < 8.3-6

* Thu Sep 19 2013 Sandro Mani <manisandro@gmail.com> - 2.13.3-2
- Require rpmdevtools and drop scripts which are in rpmdevtools

* Thu Sep 19 2013 Sandro Mani <manisandro@gmail.com> - 2.13.3-1
- Initial package
