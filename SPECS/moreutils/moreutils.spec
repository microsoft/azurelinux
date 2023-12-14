Vendor:         Microsoft Corporation
Distribution:   Mariner
## START: Set by rpmautospec
## (rpmautospec version 0.3.5)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 6;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

Name:           moreutils
Version:        0.67
Release:        7
Summary:        Additional unix utilities
License:        GPLv2
URL:            https://joeyh.name/code/moreutils/
Source0:        https://deb.debian.org/debian/pool/main/m/%{name}/%{name}_%{version}.orig.tar.gz
# fixes docbook XSL path
Patch1:         0001-dont-overwrite-docbooxsl-path.patch
# Accepted upstream, pending release of 0.68
Patch2:         0002-Use-pclose-instead-of-fclose.patch
BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  docbook2X
BuildRequires:  docbook-dtds
BuildRequires:  libxml2
BuildRequires:  perl-generators
BuildRequires:  perl-podlators
BuildRequires:  docbook-style-xsl
Requires:       perl(TimeDate)
Requires:       perl(Time::Duration)
Requires:       perl(Time::HiRes)
Requires:       perl(IPC::Run)
# These perl modules add functionality to the ts command, as they are added in eval'd code they are not
# picked up automatically by rpm.

%description
 This is a growing collection of the unix tools that nobody thought
 to write thirty years ago.

 So far, it includes the following utilities:
  - chronic: runs a command quietly, unless it fails
  - combine: combine the lines in two files using boolean operations
  - errno: look up errno names and descriptions
  - ifdata: get network interface info without parsing ifconfig output
  - ifne: run a program if the standard input is not empty
  - isutf8: check if a file or standard input is utf-8
  - lckdo: execute a program with a lock held
  - mispipe: pipe two commands, returning the exit status of the first
  - parallel: run multiple jobs at once (contained in moreutils-parallel
              sub package)
  - pee: tee standard input to pipes
  - sponge: soak up standard input and write to a file
  - ts: timestamp standard input
  - vidir: edit a directory in your text editor
  - vipe: insert a text editor into a pipe
  - zrun: automatically uncompress arguments to command

%package parallel
Summary:        Additional unix utility - parallel command
Requires:       %{name} = %{version}-%{release}
Conflicts:      parallel

%description parallel
 This is a growing collection of the unix tools that nobody thought
 to write thirty years ago.

 This is a sub package containing the parallel command only.

  - parallel: run multiple jobs at once


%prep
%autosetup -n %{name}-%{version}
# the required dtd's are not where this package expects them to be, let's fix that
DTDFILE=`xmlcatalog /usr/share/sgml/docbook/xmlcatalog "-//OASIS//DTD DocBook XML V4.4//EN" "-//OASIS//DTD DocBook XML V4.3//EN"|grep -v "No entry"|head -n1`
sed -r -i "s|/usr/share/xml/docbook/schema/dtd/4.4/docbookx.dtd|$DTDFILE|" *.docbook
# the docbook2x-man command is different in fedora, let's fix that too
sed -r -i "s|docbook2x-man|db2x_docbook2man|" Makefile
# a slightly different syntax is required here for the man pages to be built successfully
sed -r -i "s| rep=\"repeat\"||" *.docbook
# add path to pdf2man
sed -r -i "s|pod2man|/usr/bin/pod2man|" Makefile
# don't strip bins
sed -r -i "s|install -s|install|" Makefile

%build
%make_build

%check
make check

%install
%make_install

%files
%doc README COPYING
%{_mandir}/man1/chronic.1.gz
%{_mandir}/man1/combine.1.gz
%{_mandir}/man1/errno.1.gz
%{_mandir}/man1/ifdata.1.gz
%{_mandir}/man1/ifne.1.gz
%{_mandir}/man1/isutf8.1.gz
%{_mandir}/man1/lckdo.1.gz
%{_mandir}/man1/mispipe.1.gz
%{_mandir}/man1/pee.1.gz
%{_mandir}/man1/sponge.1.gz
%{_mandir}/man1/ts.1.gz
%{_mandir}/man1/vidir.1.gz
%{_mandir}/man1/vipe.1.gz
%{_mandir}/man1/zrun.1.gz
%{_bindir}/chronic
%{_bindir}/combine
%{_bindir}/errno
%{_bindir}/ifdata
%{_bindir}/ifne
%{_bindir}/isutf8
%{_bindir}/lckdo
%{_bindir}/mispipe
%{_bindir}/pee
%{_bindir}/sponge
%{_bindir}/ts
%{_bindir}/vidir
%{_bindir}/vipe
%{_bindir}/zrun

%files parallel
%doc README COPYING
%{_mandir}/man1/parallel.1.gz
%{_bindir}/parallel

%changelog
* Thu Dec 14 2023 Sindhu Karri <lakarri@microsoft.com> - 0.67-7
- Initial CBL-Mariner import from Fedora 39 (license: MIT)
- Source license verified to be GPLv2

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.67-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.67-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.67-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed May 18 2022 Mikel Olasagasti Uranga <mikel@olasagasti.info> - 0.67-3
- Patch to fix leak - Closes rhbz#2041371

* Fri May 06 2022 Mikel Olasagasti Uranga <mikel@olasagasti.info> - 0.67-2
- Fix usage of perl's virtual naming for Requires

* Sun Apr 17 2022 Mikel Olasagasti Uranga <mikel@olasagasti.info> - 0.67-1
- Update to 0.67
- Convert to rpmautospec
- Update home and source URLs
- Update perl's requires to use virtual naming
- Use make_build and make_install macros
- Add check section
- Fix rpmlint error on description
- Add conflict to moreutils-parallel against parallel package

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.63-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.63-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.63-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.63-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.63-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Oct 20 2019 Sven Lankes <sven@lank.es> - 0.63-1
- Update to latest upstream (thanks brandfbb)

* Sun Oct 20 2019 Filipe Brandenburger <filbranden@gmail.com> - 0.57-12
- Update RPM description: add "errno" and sort entries

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.57-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.57-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.57-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.57-8
- Escape macros in %%changelog

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.57-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.57-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.57-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.57-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.57-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Dec 04 2015 Ryan S Brown <ryansb@redhat.com> - 0.57-2
- Add dep on perl-IPC-Run

* Thu Dec 03 2015 Ryan S Brown <ryansb@redhat.com> - 0.57-1
- Update to 0.57 upstream release

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.49-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.49-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.49-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jan 27 2014 Michael Schwendt <mschwendt@fedoraproject.org>
- Drop insufficient Obsoletes tag (#1002134).

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.49-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Aug 01 2013 Petr Pisar <ppisar@redhat.com> - 0.49-1
- 0.49 bump

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 0.47-3
- Perl 5.18 rebuild

* Sun Feb 17 2013 Sven Lankes <sven@lank.es> - 0.47-2
- really fix rebuild failure - pod2man is now in perl-podlators

* Sat Feb 16 2013 Sven Lankes <sven@lank.es> - 0.47-1
- new upstream release
- fix rebuild failure

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.46-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.46-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Apr 22 2012 Sven Lankes <sven@lank.es> - 0.46-1
- new upstream release

* Sun Jan 22 2012 Sven Lankes <sven@lank.es> - 0.45-1
- new upstream release

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.44-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Mar 14 2011 Marc Bradshaw <fedora@marcbradshaw.co.uk> 0.44-1%{?dist}
- Split parallel into sub package to allow gnu parallel to be packaged for fedora
- moreutils 0.44 released with these changes
- * pee: Propigate exit status of commands run.
- moreutils 0.43 released with these changes
- * chronic: New command, runs a command quietly, unless it fails.
- * Now depends on IPC::Run, used by chronic.
- moreutils 0.42 released with these changes
- * sponge: Guarantee that output file is always updated atomically, by renaming a temp file into place.
- * sponge: Ensure that output file permissions are always preserved if it already exists.
- moreutils 0.41 released with these changes
- * ifdata.docbook: Mark interface as required in synopsis.
- * Add missing AUTHOR section to docbook man pages.
- * sponge: Correct bad use of fread that caused a trailing quantity of soaked data to be silently
-   discarded when a temp file was used and sponge output to stdout.

* Wed Jul 14 2010 Marc Bradshaw <fedora@marcbradshaw.co.uk> 0.40-1%{?dist}
- new upstream version moreutils 0.40 released with these changes
- * lckdo: Now deprecated, since util-linux's flock(1) can do the same thing.
- * parallel: -i will now replace {} inside parameters, before the {} had to be a separate parameter.
- new upstream version moreutils 0.39 released with these changes
- * parallel: Fix exit code handling when commands are specified after --
- * parallel: Make -j 0 do something reasonable (start all jobs at once).
- * parallel: Fix to really avoid running new jobs when load is too high.
- * parallel: Fix logic error in code handling -l that could make parallel return a bogus 255 exit code when all jobs succeeded.
- * parallel: Allow a decimal load value to be specified with -l
- * Caps sillyness.
- * zrun: Add support for .xz files.

* Wed Feb 10 2010 Marc Bradshaw <fedora@marcbradshaw.co.uk> 0.38-1%{?dist}
- new upstream version moreutils 0.38 released with these changes
- * parallel: Fix exit code handling when commands are specified after --
- * parallel: Make -j 0 do something reasonable (start all jobs at once).
- * parallel: Fix to really avoid running new jobs when load is too high.
- * parallel: Fix logic error in code handling -l that could make parallel return a bogus 255 exit code when all jobs succeeded. Closes: #569617
- * parallel: Allow a decimal load value to be specified with -l
- * Caps sillyness. Closes: #570815
- * zrun: Add support for .xz files.

* Wed Feb 10 2010 Marc Bradshaw <fedora@marcbradshaw.co.uk> 0.38-1%{?dist}
- new upstream version moreutils 0.38 released with these changes
- * Description improvements. Closes: #549450 (Thanks, Justin B Rye)
- * parallel: Allow running independent commands, like parallel -j3 -- ls df "echo hi"
- * ifdata: Add FreeBSD kernel support, although some of the more esoteric interface options are not currently supported in FreeBSD.
- * parallel: Define WEXITED to allow building on FreeBSD kernel.
- * Thanks Enrico Tassi for the FreeBSD kernel support, which should be enough to get moreutils built on Debian kFreeBSD. Closes: #562609

* Mon Oct 19 2009 Marc Bradshaw <fedora@marcbradshaw.co.uk> 0.37-1%{?dist}
- new upstream version 0.36 released with these changes
- * parallel: Clarify man page regarding CPUs. Closes: #536597
- * parallel: Add -n option. Thanks, Pierre Habouzit. Closes: #537992 (As a side effect, fixes a segfault if -- was omitted.)
- * parallel.1: Typo fixes. Closes: #538147

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.36-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 16 2009 Marc Bradshaw <fedora@marcbradshaw.co.uk> 0.36-1%{?dist}
- new upstream version 0.36 released with these changes
- * parallel: New program, contributed by Tollef Fog Heen, that can run multiple jobs in parallel, optionally checking load average.
- * mispipe: Fix closing of extra pipe FD before starting command so it is not inherited by daemons. Closes: #533448 (Thanks, Jeremie Koenig)

* Sat Jul 4 2009 Marc Bradshaw <fedora@marcbradshaw.co.uk> 0.35-1%{?dist}
- new upstream version 0.35 released with these changes
- * ifdata: Don't assume that all interface names are 6 characters or less, for instance "wmaster0" is longer.
-   Increase the limit to 20 characters. Closes: #526654 (Thanks, Alan Pope)
- * isutf8: Reject UTF-8-encoded UTF-16 surrogates. Closes: #525301 (Thanks, Jakub Wilk and liw)

* Tue Feb 24 2009 Marc Bradshaw <fedora@marcbradshaw.co.uk> 0.34-1%{?dist}
- new upstream version 0.34
- * vipe: Avoid dying on empty input. Thanks, Anders Kaseorg Closes: #508491
- new upstream version 0.33
- * Support installing moreutils into prefixes other than /usr (Evan Broder)
- * Fix zrun breakage introduced last version. Closes: #504129
- new upstream version 0.32
- * zrun: Can be linked to zsomeprog to run the equivilant of zrun someprog. Closes: #411623 (Stefan Fritsch)
- * zrun: Add support for lzma and lzo. (Stefan Fritsch)
- * Fix pod error in vidir(1).

* Thu Oct 16 2008 Marc Bradshaw <fedora@marcbradshaw.co.uk> 0.31-3%{?dist}
- Fix for EPEL docbook dtd version

* Sat Oct 11 2008 Marc Bradshaw <fedora@marcbradshaw.co.uk> 0.31-2%{?dist}
- Fix for EPEL docbook dtd version

* Thu Aug 21 2008 Marc Bradshaw <fedora@marcbradshaw.co.uk> 0.31-1%{?dist}
- new upstream version 0.31 released with these changes
- * pee.1: Document difference with tee in stdout.
- * ts: Support displaying fractional seconds via a "%%.S" conversion specification.

* Tue May 20 2008 Marc Bradshaw <fedora@marcbradshaw.co.uk> 0.30-1%{?dist}
- new upstream version 0.29 released with these changes
- * Add ifne, contributed by Javier Merino.
- * sponge, ifne: Ensure that suspending/resuming doesn't result in partial writes of the data, by using fwrite() rather than write().
- * sponge: Handle large data sizes by using a temp file rather than by consuming arbitrary amounts of memory. Patch by Brock Noland.
- * ts: Allow both -r and a format to be specified, to parse dates and output in a specified format.
- * ts: Fix bug in timezone regexp.
- New upstream version 0.30 released with these changes
- * debhelper v7; rules file minimisation
- * Use DESTDIR instead of PREFIX.
- * Add a DOCBOOK2XMAN setting. (Greg KH)
- * ifne: Add -n which makes it run the command if stdin is empty.
- * ifne: If no command is specified, print usage information.

* Wed Feb 13 2008 Marc Bradshaw <fedora@marcbradshaw.co.uk> 0.28-3%{?dist}
- fixed typo in changelog

* Wed Feb 13 2008 Marc Bradshaw <fedora@marcbradshaw.co.uk> 0.28-2%{?dist}
- fixed typo in changelog

* Wed Feb 13 2008 Marc Bradshaw <fedora@marcbradshaw.co.uk> 0.28-1%{?dist}
- New upstream version released with these changes
- vidir: Applied patch from Stefan Fritsch
- * Check for control characters (especially newlines) in filenames and error out, since this can greatly confuse the editor or vidir.
- * If the source of a rename does not exist (and thus the rename will fail anyway), vidir should not move an existing target file to a tmpfile.
- * If a directory is renamed, vidir should take that into account when renaming files in this directory.
- * If a directory name is passed as name/ to vidir, vidir should not add second slash after the name.
- vidir: Add support for unlinking directories.
- Add example to man page about recursive modification of directories.

- isutf8: Correct inverted exit code when passed a file to check.

* Wed Dec 12 2007 Marc Bradshaw <fedora@marcbradshaw.co.uk> 0.26-1%{?dist}
- Docboox dtd path will now be found using xmlcatalog.
- New upstream version released with these changes
- isutf8: Correct inverted exit code when passed a file to check.

* Wed Nov 14 2007 Marc Bradshaw <fedora@marcbradshaw.co.uk> 0.25-1%{?dist}
- New upstream version

* Wed Sep 19 2007 Marc Bradshaw <fedora@marcbradshaw.co.uk> 0.24-2%{?dist}
- Added optional perl modules to requirements

* Tue Sep 18 2007 Marc Bradshaw <fedora@marcbradshaw.co.uk> 0.24-1%{?dist}
- Version update
- Fixed specfile issues

* Mon Aug 13 2007 Marc Bradshaw <fedora@marcbradshaw.co.uk> 0.20-3%{?dist}
- Updated license field re new guidelines

* Mon Jun 18 2007 Marc Bradshaw <fedora@marcbradshaw.co.uk> 0.20-2%{?dist}
- optflags fix and extra doc files

* Thu May 24 2007 Marc Bradshaw <fedora@marcbradshaw.co.uk> 0.20-1%{?dist}
- Initial fedora release
