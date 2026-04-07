# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global posttag g
%global debian_release 16

Name:       man2html
Version:    1.6
Release:    40.%{posttag}%{?dist}
Summary:    Convert man pages to HTML - CGI scripts

# man2html.c and debian/sources/man2html.cgi.c are man2html
# utils.c is GPL-1.0-or-later
# everything else is GPL-2.0-or-later
License:    GPL-2.0-or-later AND GPL-1.0-or-later AND man2html

URL:        http://www.kapiti.co.nz/michael/vhman2html.html
Source0:    http://primates.ximian.com/~flucifredi/man/man-%{version}%{posttag}.tar.gz
# Debian CGI scripts
Source1:    https://ftp.debian.org/debian/pool/main/m/man2html/man2html_%{version}%{posttag}-%{debian_release}.debian.tar.xz
# Apache configuration file
Source2:    man2html.conf

# Patch1XXX are from Debian, XXX matches their patch number
# Copyright (C) Christoph Lameter <clameter@debian.org>, Nicolás Lichtmaier
# <nick@feedback.net.ar>, and Robert Luberda <robert@debian.org>.  GPLv2+

# fix a bashism in %%{_bindir}/hman, allows it to work on other shells
Patch1001:  001-hman-bashism.patch
# use relative links instead of http://localhost/
Patch1002:  002-man2html-default-cgibase.patch
# use file:/// links instead of file:/ (per RFC 1738)
Patch1004:  004-spelling.patch
Patch1011:  011-man2html-doctype-status.patch
Patch1012:  012-man2html-TH.patch
Patch1013:  013-man2html-file-link.patch
# show hman(1) in man2html(1) see also section
Patch1017:  017-man2html.seealso.patch
# *roff parser fix:  add support for \(lq and \(rq escape sequences
Patch1018:  018-man2html-quotes.patch
# fix SEGFAULT on manpages with no sections
Patch1019:  019-man2html-noindex-segfault.patch
# *roff parser fix: convert \N'123' to &#123
Patch1020:  020-man2html-escape_N.patch
# fix typo in Italian man page
Patch1022:  022-man2html-it-manpage.patch
# *roff parser: properly decode quotes inside quoted text
Patch1023:  023-man2html-double-quotes.patch
Patch1024:  024-man2html-uncompress.patch
# *roff parser: handle \$* and \$@ escapes.
Patch1025:  025-man2html-macro-all-args.patch
# *roff parser: support macro names longer than two characters
Patch1026:  026-man2html-macro-longname.patch
# *roff parser: parse user defined macros before global ones
Patch1027:  027-man2html-macro-priority.patch
# fix a segfault that only happens on groff(1) [lol]
Patch1028:  028-man2html-segfault.patch
# *roff parser:  support "\[xx]"
Patch1029:  029-man2html-new-macros.patch
# ignore font change requests that aren't followed by any words
Patch1030:  030-man2html-man-hyphens.patch
Patch1031:  031-man2html-BR-empty-line.patch
Patch1032:  032-man2html-man-remove-LO-tags.patch
# fix some GCC warnings
Patch1033:  033-gcc-warnings.patch
Patch1034:  034-UTF8-charset.patch
Patch1036:  036-fix-tbl-font-parsing.patch
Patch1037:  037-man2html-Nm-and-Bk-mdoc.patch
Patch1038:  038-man2html-colon-escape-sequence.patch
Patch1042:  042-man2html-CVE-2021-40647.patch
Patch1043:  043-man2html-fix-asan-issues.patch

# Fedora patches
# use /usr/lib/man2html for CGI
# originally based on Debian patches 000 and 005
Patch1:  man2html-paths.patch
# fix up CGI scripts/Makefile with Fedora paths
Patch4:  man2html-cgi.patch
# hman cleanup: use xdg-open instead of lynxcgi by default and use correct path
#               for lynxcgi when manually requested
Patch5:  man2html-hman.patch
# manpage cleanup:  mention Fedora paths as default, use modern browser examples,
#                   and describe LYNXCGI issues as runtime, not compile-time
Patch6:  man2html-doc.patch
# fix a bug in hman that linked to the wrong URL for mansec and manwhatis
# (e.g. when just invoking `hman 1`)
Patch8:  man2html-hman-section.patch
# fix the paths in localized manpages
Patch9:  man2html-localized-manpage-paths.patch
# permit autolinking manual pages with textual suffixes (e.g. "3p" for perl)
# (resolves RHBZ#1077297)
Patch10: man2html-suffixes.patch
Patch11: man2html-configure-c99.patch
Patch12: man2html-c99.patch

BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  recode

Requires:   %{name}-core%{?_isa} = %{version}-%{release}
Requires:   httpd

%description
man2html is a man page to HTML converter.

This package contains CGI scripts that allow you to view, browse, and search
man pages using a web server.


%package core
Summary:  Convert man pages to HTML

%description core
man2html is a man page to HTML converter.

This package contains the man2html executable.


%prep
%autosetup -p1 -n man-%{version}%{posttag} -a1

%build
CFLAGS="${CFLAGS:-%optflags} -std=gnu17" ; export CFLAGS ;

# Configure and make man2html binary
#  (not autoconf so don't use %%configure)
./configure -d +fhs
make %{?_smp_mflags}

# make cgi scripts from debian
cd debian/sources
make %{?_smp_mflags}


%install
#install man2html binary
make -C man2html DESTDIR=%{buildroot} install install-hman

#install CGI scripts
make -C debian/sources DESTDIR=%{buildroot} install

#install localized manpages
install -Dpm0644 man2html/locales/fr/man2html.1 %{buildroot}%{_mandir}/fr/man1/man2html.1
install -Dpm0644 man2html/locales/it/man2html.1 %{buildroot}%{_mandir}/it/man1/man2html.1
install -Dpm0644 man2html/locales/it/hman.1 %{buildroot}%{_mandir}/it/man1/hman.1

#convert localized manpages to UTF-8
recode latin1..utf8 \
    %{buildroot}%{_mandir}/fr/man1/man2html.1 \
    %{buildroot}%{_mandir}/it/man1/man2html.1 \
    %{buildroot}%{_mandir}/it/man1/hman.1 

#install httpd configuration
install -Dpm0644 %SOURCE2 %{buildroot}%{_sysconfdir}/httpd/conf.d/man2html.conf

#create cache directory for cgi scripts
mkdir -p %{buildroot}%{_localstatedir}/cache/man2html


%post
#clear out the cache directory so all future pages are regenerated with the new build
rm -f %{_localstatedir}/cache/man2html/* || :


%files
%attr(0755,-,-) %{_bindir}/hman
%{_prefix}/lib/man2html/
%attr(0775,root,apache) %{_localstatedir}/cache/man2html
%config(noreplace) %{_sysconfdir}/httpd/conf.d/man2html.conf
%{_mandir}/man1/hman.1.*


%files core
%{_bindir}/man2html
%{_mandir}/man1/man2html.1.*
%{_mandir}/*/man1/*.1.*
%doc COPYING HISTORY man2html/README man2html/TODO


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-40.g
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Feb 26 2025 Sérgio Basto <sergio@serjux.com> - 1.6-39.g
- Add more patches from Debian
         004-spelling.patch
         011-man2html-doctype-status.patch
         012-man2html-TH.patch
         013-man2html-file-link.patch
         030-man2html-man-hyphens.patch
         032-man2html-man-remove-LO-tags.patch
         034-UTF8-charset.patch
         036-fix-tbl-font-parsing.patch
         037-man2html-Nm-and-Bk-mdoc.patch
         038-man2html-colon-escape-sequence.patch
         042-man2html-CVE-2021-40647.patch
         043-man2html-fix-asan-issues.patch
     
         man2html-ungzip.patch rename to 024-man2html-uncompress.patch

* Tue Feb 25 2025 Sérgio Basto <sergio@serjux.com> - 1.6-38.g
- Add -std=gnu17 to CFLAGS to fix the build

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-37.g
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-36.g
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-35.g
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-34.g
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-33.g
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Feb 07 2023 Florian Weimer <fweimer@redhat.com> - 1.6-32.g
- C99 compatibility fixes (#2167940)

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-31.g
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-30.g
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-29.g
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-28.g
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-27.g
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-26.g
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-25.g
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-24.g
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-23.g
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-22.g
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild
- https://fedoraproject.org/wiki/Changes/Remove_GCC_from_BuildRoot

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-21.g
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-20.g
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-19.g
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-18.g
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-17.g
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-16.g
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-15.g
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-14.g
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 18 2014 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.6-13.g
- fix autolinking manual pages with textual suffixes (RHBZ#1077297)

* Sat Aug 03 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.6-12.g
- Fix stray trailing slash in files list

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-12.g
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-11.g
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan  7 2013 Remi Collet <rcollet@redhat.com> - 1.6-10.g
- fix configuration file for httpd 2.4, #871417

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-9.g
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.6-8.g
- remove SELinux hack; now supported in selinux-policy

* Mon Jul 16 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.6-7.g
- restore Italian manpages
- fix paths in localized manpages

* Thu May 24 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.6-6.g
- fix hman bug that caused linked to wrong URLs for sections (e.g. `hman 1`)
- don't ship Italian man pages; they're provided by man-pages-it

* Fri May 18 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.6-5.g
- fix accidental use of wrong macro in %%post

* Sun May 13 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.6-4.g
- clean up old cruft from patches and split them out more logically
- hman: use xdg-open and proper paths
- improve manpages
- temporarily fix SELinux until selinux-policy is patched
- clarify licensing

* Wed May 09 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.6-3.g
- convert localized man page encoding properly

* Mon May 07 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.6-2.g
- respect OPTFLAGS
- fix entries in file list
- fix links in man2html CGI output

* Fri Dec 15 2011 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.6-1.g
- initial RPM package
 
