Summary:        Unzip-6.0
Name:           unzip
Version:        6.0
Release:        19%{?dist}
License:        BSD
URL:            http://infozip.sourceforge.net/UnZip.html
Source0:        https://downloads.sourceforge.net/infozip/unzip60.tar.gz
Group:          System Environment/Utilities
Vendor:         Microsoft Corporation
Distribution:   Mariner

Patch0:         CVE-2014-9636.patch
Patch1:         CVE-2015-1315.patch
Patch2:         CVE-2015-7696.patch
Patch3:         CVE-2016-9844.patch
Patch4:         CVE-2014-9913.patch
Patch5:         unzip_cfactor_overflow-CVE-2018-18384.patch
Patch6:         CVE-2014-8139.patch
Patch7:         CVE-2014-8140.patch
Patch8:         CVE-2014-8141.patch
Patch9:         unzip-zipbomb-part1-CVE-2019-13232.patch
Patch10:        unzip-zipbomb-part2.patch
Patch11:        unzip-zipbomb-part3.patch
Patch12:        unzip-zipbomb-manpage.patch
Patch13:        CVE-2015-7697.patch
# Fixes CVE-2018-1000035
Patch14:        CVE-2018-1000035.patch
# Upstream has fixed CVE-2008-0888 in 6.0
Patch15:        CVE-2008-0888.nopatch

%description
The UnZip package contains ZIP extraction utilities. These are useful
for extracting files from ZIP archives. ZIP archives are created
with PKZIP or Info-ZIP utilities, primarily in a DOS environment.

%prep
%autosetup -p1 -n unzip60

%build
case `uname -m` in
  i?86)
    sed -i -e 's/DASM_CRC"/DASM_CRC -DNO_LCHMOD"/' unix/Makefile
    make -f unix/Makefile linux %{?_smp_mflags}
    ;;
  *)
    sed -i -e 's/CFLAGS="-O -Wall/& -DNO_LCHMOD/' unix/Makefile
    sed -i 's/CFLAGS="-O -Wall/CFLAGS="-O -g -Wall/' unix/Makefile
    sed -i 's/LF2 = -s/LF2 =/' unix/Makefile
    sed -i 's|STRIP = strip|STRIP = /bin/true|' unix/Makefile
    make -f unix/Makefile linux_noasm %{?_smp_mflags}
    ;;
esac

%install
install -v -m755 -d %{buildroot}%{_bindir}
make DESTDIR=%{buildroot} prefix=%{_prefix} install
cp %{_builddir}/unzip60/funzip %{buildroot}%{_bindir}
cp %{_builddir}/unzip60/unzip %{buildroot}%{_bindir}
cp %{_builddir}/unzip60/unzipsfx %{buildroot}%{_bindir}
cp %{_builddir}/unzip60/unix/zipgrep %{buildroot}%{_bindir}
ln -sf unzip %{buildroot}%{_bindir}/zipinfo

%check
make %{?_smp_mflags}  check

%files
%defattr(-,root,root)
%license LICENSE
%{_bindir}/*

%changelog
* Tue Apr 27 2021 Thomas Crain <thcrain@microsoft.com> - 6.0-19
- Remove contents of nopatch files

* Fri Oct 23 2020 Nick Samson <nisamson@microsoft.com> 6.0-18
- Renamed patch files for CVE-2019-13232 and CVE-2018-18384 to ensure detection by CVE tooling

* Thu Oct 22 2020 Nicolas Ontiveros <niontive@microsoft.com> 6.0-17
- Use autosetup
- Fix names for CVE patches

* Mon Sep 28 2020 Daniel McIlvaney <damcilva@microsoft.com> 6.0-16
- Nopatch CVE-2008-0888, fixed in 6.0

* Thu Jul 09 2020 Daniel McIlvaney <damcilva@microsoft.com> 6.0-15
- Add patch for CVE-2018-1000035 from Fedora 6.0-47 package

* Thu May 13 2020 Henry Beberman <henry.beberman@microsoft.com> - 6.0-14
- Add patches for CVE-2014-8139, CVE-2014-8140, CVE-2014-8141, CVE-2019-13232
- Fix detection for CVE-2015-7696, CVE-2015-7697, CVE-2018-18384
- Rename CVE-2014-9844 patch to CVE-2016-9844

* Sat May 09 00:21:29 PST 2020 Nick Samson <nisamson@microsoft.com> - 6.0-13
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 6.0-12
- Initial CBL-Mariner import from Photon (license: Apache2).

* Thu Jan 24 2019 Ankit Jain <ankitja@vmware.com> 6.0-11
- Fix for CVE-2018-18384

* Thu Nov 02 2017 Xiaolin Li <xiaolinl@vmware.com> 6.0-10
- Fix CVE-2014-9844, CVE-2014-9913

* Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 6.0-9
- Ensure non empty debuginfo

* Wed Nov 30 2016 Dheeraj Shetty <dheerajs@vmware.com> 6.0-8
- Added patch for CVE-2015-7696 and CVE-2015-7697

* Wed Oct 05 2016 ChangLee <changlee@vmware.com> 6.0-7
- Modified %check

* Tue Sep 20 2016 Kumar Kaushik <kaushikk@vmware.com> 6.0-6
- Added patch for CVE-2015-1315

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 6.0-5
- GA - Bump release of all rpms

* Tue May 10 2016 Nick Shi <nshi@vmware.com> 6.0-4
- Added unzipsfx, zipgrep and zipinfo to unzip rpm

* Sat Aug 15 2015 Sharath George <sharathg@vmware.com> 6.0-3
- Added patch for CVE-2014-9636

* Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> 6.0-2
- Updated group.

* Mon Nov 24 2014 Divya Thaluru <dthaluru@vmware.com> 6.0-1
- Initial build. First version
