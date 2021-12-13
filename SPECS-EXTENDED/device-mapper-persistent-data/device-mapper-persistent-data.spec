Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# Copyright (C) 2011-2017 Red Hat, Inc
#

Summary: Device-mapper Persistent Data Tools
Name: device-mapper-persistent-data
Version: 0.8.5
Release: 4%{?dist}
License: GPLv3+
URL: https://github.com/jthornber/thin-provisioning-tools
#Source0: https://github.com/jthornber/thin-provisioning-tools/archive/thin-provisioning-tools-% {version}.tar.gz
Source0: https://github.com/jthornber/thin-provisioning-tools/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0: device-mapper-persistent-data-avoid-strip.patch

BuildRequires: autoconf, expat-devel, libaio-devel, libstdc++-devel, boost-devel, gcc-c++
Requires: expat

%description
thin-provisioning-tools contains check,dump,restore,repair,rmap
and metadata_size tools to manage device-mapper thin provisioning
target metadata devices; cache check,dump,metadata_size,restore
and repair tools to manage device-mapper cache metadata devices
are included and era check, dump, restore and invalidate to manage
snapshot eras

%prep
%setup -q -n thin-provisioning-tools-%{version}
%patch0 -p1 -b .avoid_strip
echo %{version}-%{release} > VERSION

%build
autoconf
%configure --with-optimisation=
make %{?_smp_mflags} V=

%install
make DESTDIR=%{buildroot} MANDIR=%{_mandir} install

%files
%doc COPYING README.md
%{_mandir}/man8/cache_check.8.gz
%{_mandir}/man8/cache_dump.8.gz
%{_mandir}/man8/cache_metadata_size.8.gz
%{_mandir}/man8/cache_repair.8.gz
%{_mandir}/man8/cache_restore.8.gz
%{_mandir}/man8/cache_writeback.8.gz
%{_mandir}/man8/era_check.8.gz
%{_mandir}/man8/era_dump.8.gz
%{_mandir}/man8/era_invalidate.8.gz
%{_mandir}/man8/era_restore.8.gz
%{_mandir}/man8/thin_check.8.gz
%{_mandir}/man8/thin_delta.8.gz
%{_mandir}/man8/thin_dump.8.gz
%{_mandir}/man8/thin_ls.8.gz
%{_mandir}/man8/thin_metadata_size.8.gz
%{_mandir}/man8/thin_repair.8.gz
%{_mandir}/man8/thin_restore.8.gz
%{_mandir}/man8/thin_rmap.8.gz
%{_mandir}/man8/thin_trim.8.gz
%{_sbindir}/pdata_tools
%{_sbindir}/cache_check
%{_sbindir}/cache_dump
%{_sbindir}/cache_metadata_size
%{_sbindir}/cache_repair
%{_sbindir}/cache_restore
%{_sbindir}/cache_writeback
%{_sbindir}/era_check
%{_sbindir}/era_dump
%{_sbindir}/era_invalidate
%{_sbindir}/era_restore
%{_sbindir}/thin_check
%{_sbindir}/thin_delta
%{_sbindir}/thin_dump
%{_sbindir}/thin_ls
%{_sbindir}/thin_metadata_size
%{_sbindir}/thin_repair
%{_sbindir}/thin_restore
%{_sbindir}/thin_rmap
%{_sbindir}/thin_trim
#% {_sbindir}/thin_show_duplicates

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.8.5-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jun 04 2019 Marian Csontos <mcsontos@redhat.com> - 0.8.5-1
- Update to latest upstream version

* Sat May 04 2019 Marian Csontos <mcsontos@redhat.com> - 0.8.1-1
- Fix thin_repair should not require --repair option.

* Mon Apr 29 2019 Marian Csontos <mcsontos@redhat.com> - 0.8.0-1
- Update to latest upstream version

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jan 25 2019 Jonathan Wakely <jwakely@redhat.com> - 0.7.6-3
- Rebuilt for Boost 1.69

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Apr 24 2018 Marian Csontos <mcsontos@redhat.com> - 0.7.6-1
- Update to latest upstream version

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 23 2018 Jonathan Wakely <jwakely@redhat.com> - 0.7.5-2
- Rebuilt for Boost 1.66

* Tue Nov 14 2017 Marian Csontos <mcsontos@redhat.com> - 0.7.5-1
- Fix version 2 metadata corruption in cache_restore.

* Fri Oct 06 2017 Marian Csontos <mcsontos@redhat.com> - 0.7.3-1
- Update to latest bugfix and documentation update release.
- *_restore tools wipe superblock as a last resort.
- Add thin_check --override-mapping-root.

* Fri Sep 22 2017 Marian Csontos <mcsontos@redhat.com> - 0.7.2-1
- Update to latest upstream release including various bug fixes and new features.
- Fix segfault when dump tools are given a tiny metadata file.
- Fix -V exiting with 1.
- Fix thin_check when running on XML dump instead of binary data.
- Speed up free block searching.

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-0.6.rc6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-0.5.rc6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 03 2017 Jonathan Wakely <jwakely@redhat.com> - 0.7.0-0.4.rc6
- Rebuilt for Boost 1.64

* Tue May 23 2017 Marian Csontos <mcsontos@redhat.com> - 0.7.0-0.3.rc6
- Rebuilt for mass rebuild incorrectly tagging master to .fc26

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-0.2.rc6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Mon Mar 27 2017 Peter Rajnoha <prajnoha@redhat.com> - 0.7.0-0.1-rc6
- Don't open devices as writeable if --clear-needs-check-flag is not set.
- Fix cache metadata format version 2 superblock packing.

* Wed Mar 22 2017 Peter Rajnoha <prajnoha@redhat.com> - 0.7.0-0.1-rc5
- Switch to a faster implementation of crc32 used for checksums.

* Tue Mar 21 2017 Peter Rajnoha <prajnoha@redhat.com> - 0.7.0-0.1-rc4
- Add support for cache metadata format version 2 in cache tools.

* Thu Mar 16 2017 Peter Rajnoha <prajnoha@redhat.com> - 0.7.0-0.1-rc3
- Fix compilation warnings and further code cleanup.

* Thu Mar 09 2017 Peter Rajnoha <prajnoha@redhat.com> - 0.7.0-0.1-rc2
- Update to latest upstream release including various bug fixes and new features.
- New thin_show_duplicates command.
- Add '--skip-mappings' and '--format custom' options to thin_dump.

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 27 2017 Jonathan Wakely <jwakely@redhat.com> - 0.6.3-2
- Rebuilt for Boost 1.63

* Thu Sep 22 2016 Peter Rajnoha <prajnoha@redhat.com> - 0.6.3-1
- Preallocate output file for thin_repair and thin_restore.

* Mon Jul 11 2016 Peter Rajnoha <prajnoha@redhat.com> - 0.6.2-1
- Fixes providing proper use of compiler flags.

* Mon Apr 11 2016 Peter Rajnoha <prajnoha@redhat.com> - 0.6.2-0.1.rc8
- Fixes for thin_trim.

* Tue Mar 22 2016 Peter Rajnoha <prajnoha@redhat.com> - 0.6.2-0.1.rc7
- Fixes for thin_repair.

* Wed Mar 09 2016 Peter Rajnoha <prajnoha@redhat.com> - 0.6.2-0.1.rc6
- Add new fields to thin_ls: MAPPED_BYTES, EXCLUSIVE_BYTES and SHARED_BYTES.

* Thu Feb 18 2016 Peter Rajnoha <prajnoha@redhat.com> - 0.6.2-0.1.rc5
- Fixes for thin_delta.

* Mon Feb 15 2016 Peter Rajnoha <prajnoha@redhat.com> - 0.6.2-0.1.rc4
- Fix bug in mapping comparison while using thin_delta.

* Mon Feb 15 2016 Peter Rajnoha <prajnoha@redhat.com> - 0.6.2-0.1.rc3
- Fix recent regression in thin_repair.
- Force g++-98 dialect.

* Mon Feb 15 2016 Peter Rajnoha <prajnoha@redhat.com> - 0.6.2-0.1.rc1
- Fix bug in thin_dump when using metadata snaps.

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 20 2016 Peter Rajnoha <prajnoha@redhat.com> - 0.6.0-1
- New thin_ls command.

* Wed Jan 20 2016 Peter Rajnoha <prajnoha@redhat.com> - 0.5.6-1
- era_invalidate may be run on live metadata if the --metadata-snap
  option is given.

* Fri Jan 15 2016 Jonathan Wakely <jwakely@redhat.com> - 0.5.5-3
- Rebuilt for Boost 1.60

* Thu Aug 27 2015 Jonathan Wakely <jwakely@redhat.com> - 0.5.5-2
- Rebuilt for Boost 1.59

* Thu Aug 13 2015 Peter Rajnoha <prajnoha@redhat.com> - 0.5.5-1
- Support thin_delta's --metadata_snap option without specifying snap location.
- Update man pages to make it clearer that tools shoulnd't be run on live metadata.
- Fix bugs in the metadata reference counting for thin_check.

* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.4-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 0.5.4-2
- rebuild for Boost 1.58

* Fri Jul 17 2015 Peter Rajnoha <prajnoha@redhat.com> - 0.5.4-1
- Fix cache_check with --clear-needs-check-flag option to
  make sure metadata device is not open already by the tool
  when open with O_EXCL mode is requested.

* Fri Jul 03 2015 Peter Rajnoha <prajnoha@redhat.com> - 0.5.3-1
- Tools now open the metadata device in O_EXCL mode to stop
  running the tools on active metadata.

* Fri Jul 03 2015 Peter Rajnoha <prajnoha@redhat.com> - 0.5.2-1
- Fix bug in damage reporting in thin_dump and thin_check.

* Thu Jun 25 2015 Peter Rajnoha <prajnoha@redhat.com> - 0.5.1-1
- Fix crash if tools are given a very large metadata device to restore to.

* Mon Jun 22 2015 Peter Rajnoha <prajnoha@redhat.com> - 0.5.0-1
- Add space map checking for thin_check.
- Add --clear-needs-check option for cache_check.
- Update to latest upstream release.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 08 2015 Peter Rajnoha <prajnoha@redhat.com> - 0.4.2-1
- New thin_delta and thin_trim commands.
- Update to latest upstream release.

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.4.1-4
- Rebuilt for GCC 5 C++11 ABI change

* Mon Jan 26 2015 Petr Machata <pmachata@redhat.com> - 0.4.1-3
- Rebuild for boost 1.57.0

* Wed Oct 29 2014 Heinz Mauelshagen <heinzm@redhat.com> - 0.4.1-2
- Resolves: bz#1159466

* Wed Oct 29 2014 Heinz Mauelshagen <heinzm@redhat.com> - 0.4.1-1
- New upstream version
- Manual header additions/fixes

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 22 2014 Petr Machata <pmachata@redhat.com> - 0.3.2-2
- Rebuild for boost 1.55.0

* Fri Apr 11 2014 Heinz Mauelshagen <heinzm@redhat.com> - 0.3.2-1
- New upstream version 0.3.2 fixing needs_check flag processing

* Thu Mar 27 2014 Heinz Mauelshagen <heinzm@redhat.com> - 0.3.0-1
- New upstream version 0.3.0 introducing era_{check,dump,invalidate}

* Fri Oct 18 2013 Heinz Mauelshagen <heinzm@redhat.com> - 0.2.8-1
- New upstream version 0.2.8 introducing cache_{check,dump,repair,restore}

* Tue Sep 17 2013 Heinz Mauelshagen <heinzm@redhat.com> - 0.2.7-1
- New upstream version 0.2.7

* Wed Jul 31 2013 Heinz Mauelshagen <heinzm@redhat.com> - 0.2.3-1
- New upstream version

* Tue Jul 30 2013 Dennis Gilmore <dennis@ausil.us> - 0.2.2-2
- rebuild against boost 1.54.0

* Tue Jul 30 2013 Heinz Mauelshagen <heinzm@redhat.com> - 0.2.2-1
- New upstream version
- manual header fixes 

* Tue Jul 30 2013 Petr Machata <pmachata@redhat.com> - 0.2.1-6
- Rebuild for boost 1.54.0

* Thu Jul 25 2013 Heinz Mauelshagen <heinzm@redhat.com> - 0.2.1-5
- enhance manual pages and fix typos

* Thu Jul 18 2013 Heinz Mauelshagen <heinzm@redhat.com> - 0.2.1-4
- Update thin_metadata_size manual page
- thin_dump: support dumping default metadata snapshot

* Thu Jul 18 2013 Heinz Mauelshagen <heinzm@redhat.com> - 0.2.1-3
- New thin_metadata_size tool to estimate amount of metadata space
  based on block size, pool size and maximum amount of thin devs and snapshots
- support metadata snapshots in thin_dump tool
- New man pages for thin_metadata_size, thin_repair and thin_rmap and man page fixes

* Tue Jul 16 2013 Heinz Mauelshagen <heinzm@redhat.com> - 0.2.1-2
- Build with nostrip fix from Ville Skyttä

* Mon Jul 15 2013 Ville Skyttä <ville.skytta@iki.fi> - 0.2.1-2
- Let rpmbuild strip binaries, don't override optflags, build more verbose.

* Fri Jul 12 2013 Heinz Mauelshagen <heinzm@redhat.com> - 0.2.1-1
- New upstream version.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr 19 2012 Milan Broz <mbroz@redhat.com> - 0.1.4-1
- Fix thin_check man page (add -q option).
- Install utilities in /usr/sbin.

* Tue Mar 13 2012 Milan Broz <mbroz@redhat.com> - 0.1.2-1
- New upstream version.

* Mon Mar 05 2012 Milan Broz <mbroz@redhat.com> - 0.1.1-1
- Fix quiet option.

* Fri Mar 02 2012 Milan Broz <mbroz@redhat.com> - 0.1.0-1
- New upstream version.

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.1-3
- Rebuilt for c++ ABI breakage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 21 2011 Milan Broz <mbroz@redhat.com> - 0.0.1-1
- Initial version
