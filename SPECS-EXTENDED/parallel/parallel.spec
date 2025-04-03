
Name:           parallel
Summary:        Shell tool for executing jobs in parallel
Version:        20240922
Release:        3%{?dist}
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
# Automatically converted from old format: GFDL and GPLv3+ - review is highly recommended.
License:        LicenseRef-Callaway-GFDL AND GPL-3.0-or-later
URL:            https://www.gnu.org/software/parallel/
Source0:        https://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.bz2
BuildArch:      noarch
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-podlators
BuildRequires:  perl-FileHandle
BuildRequires:  sed

%define __requires_exclude sh$

# Due to a naming conflict, both packages cannot be installed in parallel
# To prevent user confusion, GNU parallel is installed in a compatibility
# mode to be commandline compatible to moreutils' parallel.
# This mode can be turned off system wide or on a per-user base.
Conflicts:      moreutils-parallel

%description
GNU Parallel is a shell tool for executing jobs in parallel using one or more
machines. A job is typically a single command or a small script that has to be
run for each of the lines in the input. The typical input is a list of files, a
list of hosts, a list of users, or a list of tables.

If you use xargs today you will find GNU Parallel very easy to use. If you
write loops in shell, you will find GNU Parallel may be able to replace most of
the loops and make them run faster by running jobs in parallel. If you use ppss
or pexec you will find GNU Parallel will often make the command easier to read.

GNU Parallel also makes sure output from the commands is the same output as you
would get had you run the commands sequentially. This makes it possible to use
output from GNU Parallel as input for other programs.

GNU Parallel is command-line-compatible with moreutils' parallel, but offers
additional features.

%prep
%autosetup
# Replace shebang by replacing "env" by removing "env ".
# FIXME: this is quite a hack
sed -i '1s:/env :/:' src/env_parallel.*

%build
autoreconf -ivf
%configure
%make_build

%install
%make_install
rm -vrf %{buildroot}%{_pkgdocdir}

%files
%license LICENSES/GPL-3.0-or-later.txt LICENSES/GFDL-1.3-or-later.txt
%doc README NEWS
%{_bindir}/parallel
%{_bindir}/parcat
%{_bindir}/parset
%{_bindir}/parsort
%{_mandir}/man1/parallel.1*
%{_mandir}/man1/parcat.1*
%{_mandir}/man1/parset.1*
%{_mandir}/man1/parsort.1*
%{_mandir}/man7/parallel*
%{_bindir}/env_parallel*
%{_mandir}/man1/env_parallel.1*
%{_bindir}/sem
%{_mandir}/man1/sem.1*
%{_bindir}/sql
%{_mandir}/man1/sql.1*
%{_bindir}/niceload
%{_mandir}/man1/niceload.1*
%{_datadir}/bash-completion/completions/parallel
%{_datadir}/zsh/site-functions/_parallel

%changelog
* Wed Dec 18 2024 Jyoti kanase <v-jykanase@microsoft.com> -  20240922 -3
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified.

* Mon Sep 23 2024 Filipe Rosset <rosset.filipe@gmail.com> - 20240922-2
- update parallel to 20240922

* Mon Sep 23 2024 Filipe Rosset <rosset.filipe@gmail.com> - 20240922-1
- update parallel to 20240922

* Mon Sep 16 2024 Filipe Rosset <rosset.filipe@gmail.com> - 20240822-1
- update parallel to 20240822

* Mon Sep 02 2024 Miroslav Suchý <msuchy@redhat.com> - 20240722-2
- convert license to SPDX

* Wed Aug 14 2024 Filipe Rosset <rosset.filipe@gmail.com> - 20240722-1
- update parallel to 20240722

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20240622-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jul 15 2024 Filipe Rosset <rosset.filipe@gmail.com> - 20240622-1
- update to 20240622 fixes rbhz#2267428

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20230822-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20230822-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Sep 09 2023 Filipe Rosset <rosset.filipe@gmail.com> - 20230822-1
- update to parallel-20230822

* Sun Jul 30 2023 Filipe Rosset <rosset.filipe@gmail.com> - 20230722-1
- update to 20230722

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 20230522-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jun 09 2023 Filipe Rosset <rosset.filipe@gmail.com> - 20230522-1
- update to 20230522

* Tue May 02 2023 Filipe Rosset <rosset.filipe@gmail.com> - 20230422-2
- update parallel to 20230422

* Tue May 02 2023 Filipe Rosset <rosset.filipe@gmail.com> - 20230422-1
- update parallel to 20230422

* Fri Mar 31 2023 Filipe Rosset <rosset.filipe@gmail.com> - 20230322-1
- update to 20230322

* Sun Feb 19 2023 Filipe Rosset <rosset.filipe@gmail.com> - 20230122-1
- update to 20230122

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 20221122-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Nov 24 2022 Filipe Rosset <rosset.filipe@gmail.com> - 20221122-1
- updated to latest version

* Mon Oct 24 2022 Filipe Rosset <rosset.filipe@gmail.com> - 20221022-1
- update to 20221022

* Sat Sep 24 2022 Filipe Rosset <rosset.filipe@gmail.com> - 20220922-1
- Update to 20220922

* Tue Aug 23 2022 Filipe Rosset <rosset.filipe@gmail.com> - 20220822-1
- update to 20220822

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 20220322-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Mar 30 2022 Filipe Rosset <rosset.filipe@gmail.com> - 20220322-1
- update to 20220322

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 20211222-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jan 05 2022 Jirka Hladky <jhladky@redhat.com> - 20211222-2
- Remove all shell dependencies

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20201222-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20201222-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Jan 16 2021 Filipe Rosset <rosset.filipe@gmail.com> - 20201222-1
- Update to 20201222

* Mon Aug 17 2020 Filipe Rosset <rosset.filipe@gmail.com> - 20200722-1
- Update to 20200722

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20200522-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Filipe Rosset <rosset.filipe@gmail.com> - 20200522-1
- Update to 20200522

* Wed Apr 22 2020 Filipe Rosset <rosset.filipe@gmail.com> - 20200322-1
- Update to 20200322 fixes rhbz#1740919

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20190922-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Oct 16 2019 Jirka Hladky <hladky.jiri@gmail.com> - 20190922-1
- Update to 20190922

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20180322-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20180322-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20180322-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Apr 15 2018 Filipe Rosset <rosset.filipe@gmail.com> - 20180322-1
- update to latest upstream 20180322 fixes rhbz #1520477

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20160722-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20160722-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20160722-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Aug 30 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 20160722-2
- Fix shebang (RHBZ #1370706)

* Sun Aug 21 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 20160722-1
- Update to 20160722

* Mon Apr 04 2016 Golo Fuchert <packages@golotop.de> 20160222-1
- Update to version 20160222-1 to fix bugs (#1285888,1307846,1320511,1320956,1320958)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 20141122-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20141122-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Dec 03 2014 Golo Fuchert <packages@golotop.de> 20141122-1
- Updated to newest version 20141122

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20131222-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jan 22 2014 Golo Fuchert <packages@golotop.de> 20131222-2
- Corrected typo in changelog
- Removed directory, which is no longer needed

* Sun Jan 19 2014 Golo Fuchert <packages@golotop.de> 20131222-1
- Updated to newest versoin 20131222
- Removed patches that are no longer needed (see below for details)
- Remvoal of parallel-config, feature deprecated
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20130522-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild
* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 20130522-3
- Perl 5.18 rebuild
* Thu Jun 13 2013 Golo Fuchert <packages@golotop.de> - 20130522-2
- Patch of parallel.pod due to new syntax 
* Wed May 22 2013 Golo Fuchert <packages@golotop.de> - 20130522-1
- Updated to newest version 20130522 
* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20121222-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild
* Wed Jan 16 2013 Golo Fuchert <packages@golotop.de> - 20121222-1
- Updated to newest version 20121222 (due to #895971)
* Wed Mar 21 2012 Golo Fuchert <packages@golotop.de> - 20120222-1
- Updated to newest version 20120222
- renamed manpage sql to parallel-sql (naming conflict, bug 797823)
* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20110722-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild
* Fri Sep 09 2011 Golo Fuchert <packages@golotop.de> - 20110722-3
- Added niceload.html to doc
* Fri Sep 09 2011 Golo Fuchert <packages@golotop.de> - 20110722-2
- Minor cosmetic changes and consistent macro usage
* Sat Aug 13 2011 Golo Fuchert <packages@golotop.de> - 20110722-1
- Updated to newest version 20110722
* Sun May 22 2011 Golo Fuchert <packages@golotop.de> - 20110522-1
- Update to version 20110522
- Conflict with moreutils-parallel
- Incl. config file to make gnu parallel compatible with moreutils' by default
- Added a comment to the description, concerning the moreutils compatibility
* Sun Feb 6 2011 Golo Fuchert <packages@golotop.de> - 20110205-1
- Initial package. Based on a package by Ole Tange and Markus Ammer.

## END: Generated by rpmautospec
