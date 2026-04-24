# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond_without check

%global upstream_name psqlodbc

Name: postgresql-odbc
Summary: PostgreSQL ODBC driver
Version: 16.00.0000
Release: 7%{?dist}
License: LGPL-2.0-or-later
URL: https://odbc.postgresql.org/

Source0: https://ftp.postgresql.org/pub/odbc/versions/src/%{upstream_name}-%{version}.tar.gz

Patch0: postgresql-odbc-09.06.0200-revert-money-fix.patch
Patch1: postgresql-odbc-09.05.0400-revert-money-testsuite-fix.patch
Patch2: postgresql-odbc-endianity-test-fix.patch

BuildRequires: make
BuildRequires:  gcc
BuildRequires: unixODBC-devel
BuildRequires: pkgconfig(libpq)

%if %{with check}
BuildRequires: postgresql-test-rpm-macros
%endif

Provides: %upstream_name = %version-%release

# This spec file and ancillary files are licensed in accordance with
# the psqlodbc license.

%description
This package includes the driver needed for applications to access a
PostgreSQL system via ODBC (Open Database Connectivity).


%prep
%autosetup -p1 -n %{upstream_name}-%{version}

cat <<EOF >README.rpmdist
The upstream psqlodbc testsuite is distributed in '%{name}-tests'
(sub)package.
EOF

%build
export CFLAGS="$CFLAGS -std=gnu17"
%configure --with-unixodbc --disable-dependency-tracking
# GCC 10 defaults to -fno-common
# https://gcc.gnu.org/gcc-10/changes.html (see C section)
%make_build CFLAGS="%{optflags} -fcommon -std=gnu17"


%install
%make_install

%global testsuitedir %{_libdir}/%{name}
install -d -m 755 $RPM_BUILD_ROOT/%{testsuitedir}
cp -R test $RPM_BUILD_ROOT/%{testsuitedir}
sed -i 's~^drvr=.*~drvr=%{_libdir}/psqlodbc~' $RPM_BUILD_ROOT/%{testsuitedir}/test/odbcini-gen.sh

# Provide the old library name "psqlodbc.so" as a symlink,
# and remove the rather useless .la file
pushd ${RPM_BUILD_ROOT}%{_libdir}
	ln -s psqlodbcw.so psqlodbc.so
	rm psqlodbcw.la psqlodbca.la
popd

%if %{with check}
%check
%postgresql_tests_run

# make sure that we are testing aginst expected output "utf8" case
mv test/expected/wchar-char_1.out test/expected/wchar-char.out
rm -rf test/expected/wchar-char_2.out
rm -rf test/expected/wchar-char_3.out

cd test && make installcheck %{_smp_mflags} CFLAGS="%{optflags} -fcommon -std=gnu17" || {
	echo "=== trying to find all regression.diffs files in build directory ==="
	find -name regression.diffs | while read line; do
		cat "$line"
	done
	false
}
%endif



%package tests
Summary: Testsuite files for psqlodbc
Requires: postgresql-test
Requires: %{name} = %{version}-%{release}
# Those are requires to successful testsuite run
Requires: gcc make unixODBC-devel


%description tests
The postgresql-odbc-tests package contains files needed for various tests for
the PostgreSQL unixODBC driver.


%files
%{_libdir}/psqlodbc.so
%{_libdir}/psqlodbca.so
%{_libdir}/psqlodbcw.so
%doc license.txt readme.txt docs/* README.rpmdist


%files tests
%doc license.txt
%dir %{testsuitedir}
%defattr(-,postgres,postgres)
%{testsuitedir}/test


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 16.00.0000-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 16.00.0000-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 16.00.0000-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 16.00.0000-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 16.00.0000-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 25 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 16.00.0000-1
- Update to 16.00.0000

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 13.01.0000-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 13.01.0000-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 13.01.0000-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 13.01.0000-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Filip Januš <fjanus@redhat.com> - 13.01.0000-1
- Update to 13.01.0000

* Mon Feb 08 2021 Pavel Raiskup <praiskup@redhat.com> - 12.02.0000-4
- rebuild for libpq ABI fix rhbz#1908268

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 12.02.0000-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 12.02.0000-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 02 2020 Ondrej Dubaj <odubaj@redhat.com> - 12.02.0000-1
- Rebase to upstream release 12.02.0000

* Mon Mar 09 2020 Patrik Novotný <panovotn@redhat.com> - 12.01.0000-1
- Rebase to upstream release 12.01.0000

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 10.03.0000-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 10.03.0000-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 10.03.0000-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 10.03.0000-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon May 21 2018 Pavel Raiskup <praiskup@redhat.com> - 10.03.0000-1
- update to new upstream release, per announcement:
  https://www.postgresql.org/message-id/20180519131632.8E59CB40E51%40winpg.jp

* Fri Apr 13 2018 Pavel Raiskup <praiskup@redhat.com> - 10.02.0000-2
- BR postgresql-test-rpm-macros
- add %%bcond for check section

* Mon Apr 02 2018 Pavel Raiskup <praiskup@redhat.com> - 10.02.0000-1
- update to new upstream release, per announcement:
  https://www.postgresql.org/message-id/20180330143925.88CEDB40E51%40winpg.jp

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 10.01.0000-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Dec 27 2017 Pavel Raiskup <praiskup@redhat.com> - 10.01.0000-1
- update to new upstream release, per announcement:
  https://www.postgresql.org/message-id/20171227144219.0ABC4B4C417%40winpg.jp

* Mon Oct 23 2017 Pavel Raiskup <praiskup@redhat.com> - 10.00.0000-1
- update to new upstream release, per announcement:
  https://www.postgresql.org/message-id/20171013143455.9D0E5B4C412%40winpg.jp

* Tue Sep 05 2017 Pavel Raiskup <praiskup@redhat.com> - 09.06.0500-1
- update to new upstream release, per:
  https://www.postgresql.org/message-id/20170905143318.95448B4C411@winpg.jp

* Thu Jul 27 2017 Pavel Raiskup <praiskup@redhat.com> - 09.06.0410-1
  https://odbc.postgresql.org/docs/release.html

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 09.06.0310-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri May 12 2017 Pavel Raiskup <praiskup@redhat.com> - 09.06.0310-1
- rebase to latest upstream version, per release notes:
  https://odbc.postgresql.org/docs/release.html

* Tue May 09 2017 Pavel Raiskup <praiskup@redhat.com> - 09.06.0300-1
- rebase to latest upstream version, per release notes:
  https://odbc.postgresql.org/docs/release.html

* Mon Mar 13 2017 Pavel Raiskup <praiskup@redhat.com> - 09.06.0200-1
- rebase to latest upstream version, per release notes:
  https://odbc.postgresql.org/docs/release.html

* Mon Feb 06 2017 Pavel Raiskup <praiskup@redhat.com> - 09.06.0100-1
- rebase to latest upstream version, per release notes:
  https://odbc.postgresql.org/docs/release.html

* Thu Oct 20 2016 Pavel Raiskup <praiskup@redhat.com> - 09.05.0400-4
- provide 'psqlodbc', we possibly should rename the package in future

* Wed Oct 05 2016 Pavel Raiskup <praiskup@redhat.com> - 09.05.0400-3
- depend on postgresql-setup 5.0 (in postgresql-devel package)

* Mon Aug 29 2016 Petr Kubat <pkubat@redhat.com> - 09.05.0400-2
- once again revert upstream commit d5374bcc4d
- also revert its accompanying testsuite commit eb480e19ee

* Thu Aug 11 2016 Petr Kubat <pkubat@redhat.com> - 09.05.0400-1
- rebase to latest upstream version, per release notes:
  https://odbc.postgresql.org/docs/release.html

* Tue Jul 26 2016 Pavel Raiskup <praiskup@redhat.com> - 09.05.0300-2
- backport upstream fixes for testsuite failures (rhbz#1350486)

* Sat Jun 18 2016 Pavel Raiskup <praiskup@redhat.com> - 09.05.0300-1
- rebase to latest upstream version, per release notes:
  https://odbc.postgresql.org/docs/release.html

* Mon May 02 2016 Pavel Raiskup <praiskup@redhat.com> - 09.05.0210-1
- rebase to latest upstream version, per release notes:
  https://odbc.postgresql.org/docs/release.html
- revert one upstream commit to fix testsuite issues
- disable one armv7hl related issue during self-testing (rhbz#1330031)

* Thu Apr 14 2016 Pavel Raiskup <praiskup@redhat.com> - 09.05.0200-2
- enable testsuite during build

* Tue Apr 12 2016 Pavel Raiskup <praiskup@redhat.com> - 09.05.0200-1
- rebase to latest upstream version, per release notes:
  https://odbc.postgresql.org/docs/release.html

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 09.05.0100-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 11 2016 Pavel Raiskup <praiskup@redhat.com> - 09.05.0100-1
- rebase to latest upstream version, per release notes:
  http://psqlodbc.projects.pgfoundry.org/docs/release.html

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 09.03.0400-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Nov 19 2014 Pavel Raiskup <praiskup@redhat.com> - 09.03.0400-3
- fix testsuite requirements

* Wed Nov 19 2014 Pavel Raiskup <praiskup@redhat.com> - 09.03.0400-2
- install the testsuite

* Wed Oct 29 2014 Pavel Raiskup <praiskup@redhat.com> - 09.03.0400-1
- rebase to latest upstream version, per release notes:
  http://psqlodbc.projects.pgfoundry.org/docs/release.html

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 09.03.0300-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 09.03.0300-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 19 2014 Pavel Raiskup <praiskup@redhat.com> - 09.03.0300-2
- run upstream testsuite when '%%runselftest' defined

* Mon May 19 2014 Pavel Raiskup <praiskup@redhat.com> - 09.03.0300-1
- rebase to latest upstream version, per release notes:
  http://psqlodbc.projects.pgfoundry.org/docs/release.html

* Wed Apr 23 2014 Pavel Raiskup <praiskup@redhat.com> - 09.03.0210-1
- rebase to latest upstream version (#1090345), per release notes:
  http://psqlodbc.projects.pgfoundry.org/docs/release.html

* Thu Dec 19 2013 Pavel Raiskup <praiskup@redhat.com> - 09.03.0100-1
- rebase to latest upstream version

* Mon Nov 18 2013 Pavel Raiskup <praiskup@redhat.com> - 09.02.0100-1
- rebase to latest upstream version

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 09.01.0200-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 09.01.0200-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 16 2012 Tom Lane <tgl@redhat.com> 09.01.0200-2
- Update tarball URL in specfile (no actual package change)

* Mon Aug 20 2012 Tom Lane <tgl@redhat.com> 09.01.0200-1
- Update to version 09.01.0200
- Minor specfile cleanup per suggestions from Tom Callaway
Related: #845110

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 09.01.0100-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jan 10 2012 Tom Lane <tgl@redhat.com> 09.01.0100-1
- Update to version 09.01.0100

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 09.00.0200-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 29 2010 Tom Lane <tgl@redhat.com> 09.00.0200-1
- Update to version 09.00.0200

* Wed Jan 20 2010 Tom Lane <tgl@redhat.com> 08.04.0200-2
- Correct Source0: tag and comment to reflect how to get the tarball

* Wed Dec 30 2009 Tom Lane <tgl@redhat.com> 08.04.0200-1
- Update to version 08.04.0200

* Fri Aug 28 2009 Tom Lane <tgl@redhat.com> 08.04.0100-2
- Rebuild with new openssl

* Tue Aug 18 2009 Tom Lane <tgl@redhat.com> 08.04.0100-1
- Update to version 08.04.0100

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 08.03.0200-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 08.03.0200-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Tom Lane <tgl@redhat.com> 08.03.0200-2
- Rebuild for unixODBC 2.2.14.

* Tue Aug  5 2008 Tom Lane <tgl@redhat.com> 08.03.0200-1
- Update to version 08.03.0200

* Tue Feb 12 2008 Tom Lane <tgl@redhat.com> 08.03.0100-1
- Update to version 08.03.0100
- Since it looks like upstream has decided to stick with psqlodbcw.so
  permanently, allow the library to have that name.  But continue to
  provide psqlodbc.so as a symlink.

* Fri Nov  2 2007 Tom Lane <tgl@redhat.com> 08.02.0500-1
- Update to version 08.02.0500

* Thu Aug  2 2007 Tom Lane <tgl@redhat.com> 08.02.0200-2
- Update License tag to match code.

* Wed Apr 25 2007 Tom Lane <tgl@redhat.com> 08.02.0200-1
- Update to version 08.02.0200

* Mon Dec 11 2006 Tom Lane <tgl@redhat.com> 08.01.0200-4
- Rebuild for new Postgres libraries

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 08.01.0200-3.1
- rebuild

* Sat Jun 10 2006 Tom Lane <tgl@redhat.com> 08.01.0200-3
- Fix BuildRequires: for mock build environment

* Wed Mar 22 2006 Tom Lane <tgl@redhat.com> 08.01.0200-2
- Change library name back to psqlodbc.so, because it appears that upstream
  will revert to that name in next release; no point in thrashing the name.
- Include documentation files unaccountably omitted before (bug #184158)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 08.01.0200-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 08.01.0200-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Feb  3 2006 Tom Lane <tgl@redhat.com> 08.01.0200-1
- Update to version 08.01.0200.
- Upstream now calls the library psqlodbcw.so ... add a symlink to avoid
  breaking existing odbc configuration files.

* Wed Dec 14 2005 Tom Lane <tgl@redhat.com> 08.01.0102-1
- Update to version 08.01.0102.
- Add buildrequires postgresql-devel (bz #174505)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Nov  7 2005 Tom Lane <tgl@redhat.com> 08.01.0100-1
- Update to version 08.01.0100.

* Wed Mar  2 2005 Tom Lane <tgl@redhat.com> 08.00.0100-1
- Update to version 08.00.0100.

* Fri Nov 12 2004 Tom Lane <tgl@redhat.com> 7.3-9
- back-port 64-bit fixes from current upstream (bug #139004)

* Tue Sep 21 2004 Tom Lane <tgl@redhat.com> 7.3-8
- rebuilt

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Mar 10 2004 Tom Lane <tgl@redhat.com>
- Correct License: annotation.

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Nov 21 2003 David Jee <djee@redhat.com> 7.3-5
- rebuild

* Wed Nov 05 2003 David Jee <djee@redhat.com> 7.3-4
- import new community version 07.03.0200

* Mon Sep 15 2003 Andrew Overholt <overholt@redhat.com> 7.3-3
- autotools fixes (courtesy Alex Oliva <aoliva@redhat.com> and
  Owen Taylor <otaylor@redhat.com>)

* Tue Jul 08 2003 Andrew Overholt <overholt@redhat.com> 7.3-3
- allow use with unixODBC (courtesy Troels Arvin) [Bug #97998]

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jun 02 2003 Andrew Overholt <overholt@redhat.com> 7.3-1
- sync to new community version (07.03.0100 => v7.3, r1)

* Thu Jan 23 2003 Tim Powers <timp@redhat.com> 1-2
- rebuild

* Tue Jan 14 2003 Andrew Overholt <overholt@redhat.com>
- 1-1
- initial build (just took old package sections)
