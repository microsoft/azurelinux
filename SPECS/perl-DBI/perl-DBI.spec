# Got the intial spec from Fedora and modified it
# Filter unwanted dependencies
%global __requires_exclude %{?__requires_exclude|%__requires_exclude|}^perl\\(RPC::\\)

Summary:        A database access API for perl
Name:           perl-DBI
Version:        1.643
Release:        3%{?dist}
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://dbi.perl.org/
# The source tarball must be repackaged to remove the DBI/FAQ.pm, since the
# license is not a FSF free license.
Source0:        https://cpan.metacpan.org/authors/id/T/TI/TIMB/DBI-%{version}.tar.gz
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
BuildRequires:  perl >= 5.28.0
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
%if 0%{?with_check}
BuildRequires:  perl(blib)
BuildRequires:  perl(Test::More)
%endif

Requires:       perl-libs
Requires:       perl(FileHandle)
Requires:       perl(Math::BigInt)

Provides:       perl(DBD::DBM) = %{version}-%{release}
Provides:       perl(DBD::DBM::Statement) = %{version}-%{release}
Provides:       perl(DBD::DBM::Table) = %{version}-%{release}
Provides:       perl(DBD::DBM::db) = %{version}-%{release}
Provides:       perl(DBD::DBM::dr) = %{version}-%{release}
Provides:       perl(DBD::DBM::st) = %{version}-%{release}
Provides:       perl(DBD::ExampleP) = %{version}-%{release}
Provides:       perl(DBD::File) = %{version}-%{release}
Provides:       perl(DBD::File::DataSource::File) = %{version}-%{release}
Provides:       perl(DBD::File::DataSource::Stream) = %{version}-%{release}
Provides:       perl(DBD::File::Statement) = %{version}-%{release}
Provides:       perl(DBD::File::Table) = %{version}-%{release}
Provides:       perl(DBD::File::TableSource::FileSystem) = %{version}-%{release}
Provides:       perl(DBD::File::db) = %{version}-%{release}
Provides:       perl(DBD::File::dr) = %{version}-%{release}
Provides:       perl(DBD::File::st) = %{version}-%{release}
Provides:       perl(DBD::Gofer) = %{version}-%{release}
Provides:       perl(DBD::Gofer::Policy::Base) = %{version}-%{release}
Provides:       perl(DBD::Gofer::Policy::classic) = %{version}-%{release}
Provides:       perl(DBD::Gofer::Policy::pedantic) = %{version}-%{release}
Provides:       perl(DBD::Gofer::Policy::rush) = %{version}-%{release}
Provides:       perl(DBD::Gofer::Transport::Base) = %{version}-%{release}
Provides:       perl(DBD::Gofer::Transport::null) = %{version}-%{release}
Provides:       perl(DBD::Gofer::Transport::pipeone) = %{version}-%{release}
Provides:       perl(DBD::Gofer::Transport::stream) = %{version}-%{release}
Provides:       perl(DBD::Mem) = %{version}-%{release}
Provides:       perl(DBD::Mem::DataSource) = %{version}-%{release}
Provides:       perl(DBD::Mem::Statement) = %{version}-%{release}
Provides:       perl(DBD::Mem::Table) = %{version}-%{release}
Provides:       perl(DBD::Mem::db) = %{version}-%{release}
Provides:       perl(DBD::Mem::dr) = %{version}-%{release}
Provides:       perl(DBD::Mem::st) = %{version}-%{release}
Provides:       perl(DBD::NullP) = %{version}-%{release}
Provides:       perl(DBD::Sponge) = %{version}-%{release}
Provides:       perl(DBDI) = %{version}-%{release}
Provides:       perl(DBI) = %{version}-%{release}
Provides:       perl(DBI::Const::GetInfo::ANSI) = %{version}-%{release}
Provides:       perl(DBI::Const::GetInfo::ODBC) = %{version}-%{release}
Provides:       perl(DBI::Const::GetInfoReturn) = %{version}-%{release}
Provides:       perl(DBI::Const::GetInfoType) = %{version}-%{release}
Provides:       perl(DBI::DBD) = %{version}-%{release}
Provides:       perl(DBI::DBD::Metadata) = %{version}-%{release}
Provides:       perl(DBI::DBD::SqlEngine) = %{version}-%{release}
Provides:       perl(DBI::DBD::SqlEngine::DataSource) = %{version}-%{release}
Provides:       perl(DBI::DBD::SqlEngine::Statement) = %{version}-%{release}
Provides:       perl(DBI::DBD::SqlEngine::Table) = %{version}-%{release}
Provides:       perl(DBI::DBD::SqlEngine::TableSource) = %{version}-%{release}
Provides:       perl(DBI::DBD::SqlEngine::TieMeta) = %{version}-%{release}
Provides:       perl(DBI::DBD::SqlEngine::TieTables) = %{version}-%{release}
Provides:       perl(DBI::DBD::SqlEngine::db) = %{version}-%{release}
Provides:       perl(DBI::DBD::SqlEngine::dr) = %{version}-%{release}
Provides:       perl(DBI::DBD::SqlEngine::st) = %{version}-%{release}
Provides:       perl(DBI::Gofer::Execute) = %{version}-%{release}
Provides:       perl(DBI::Gofer::Request) = %{version}-%{release}
Provides:       perl(DBI::Gofer::Response) = %{version}-%{release}
Provides:       perl(DBI::Gofer::Serializer::Base) = %{version}-%{release}
Provides:       perl(DBI::Gofer::Serializer::DataDumper) = %{version}-%{release}
Provides:       perl(DBI::Gofer::Serializer::Storable) = %{version}-%{release}
Provides:       perl(DBI::Gofer::Transport::Base) = %{version}-%{release}
Provides:       perl(DBI::Gofer::Transport::pipeone) = %{version}-%{release}
Provides:       perl(DBI::Gofer::Transport::stream) = %{version}-%{release}
Provides:       perl(DBI::Profile) = %{version}-%{release}
Provides:       perl(DBI::ProfileData) = %{version}-%{release}
Provides:       perl(DBI::ProfileDumper) = %{version}-%{release}
Provides:       perl(DBI::ProfileDumper::Apache) = %{version}-%{release}
Provides:       perl(DBI::ProfileSubs) = %{version}-%{release}
Provides:       perl(DBI::SQL::Nano) = %{version}-%{release}
Provides:       perl(DBI::SQL::Nano::Statement_) = %{version}-%{release}
Provides:       perl(DBI::SQL::Nano::Table_) = %{version}-%{release}
Provides:       perl(DBI::Util::CacheMemory) = %{version}-%{release}
Provides:       perl(DBI::Util::_accessor) = %{version}-%{release}
Provides:       perl(DBI::common) = %{version}-%{release}

%description
DBI is a database access Application Programming Interface (API) for
the Perl Language. The DBI API Specification defines a set of
functions, variables and conventions that provide a consistent
database interface independent of the actual database being used.

%prep
%setup -q -n DBI-%{version}
for F in lib/DBD/Gofer.pm; do
    iconv -f ISO-8859-1 -t UTF-8 < "$F" > "${F}.utf8"
    touch -r "$F" "${F}.utf8"
    mv "${F}.utf8" "$F"
done
chmod 644 ex/*
chmod 744 dbixs_rev.pl
# Fix shell bangs
for F in dbixs_rev.pl ex/corogofer.pl; do
    perl -MExtUtils::MakeMaker -e "ExtUtils::MM_Unix->fixin(q{$F})"
done

rm lib/DBD/Gofer/Transport/corostream.pm
sed -i -e '/^lib\/DBD\/Gofer\/Transport\/corostream.pm$/d' MANIFEST

# Remove RPC::Pl* reverse dependencies due to security concerns,
# CVE-2013-7284, bug #1051110
for F in lib/Bundle/DBI.pm lib/DBD/Proxy.pm lib/DBI/ProxyServer.pm \
        dbiproxy.PL t/80proxy.t; do
    rm "$F"
    sed -i -e '\|^'"$F"'|d' MANIFEST
done
sed -i -e 's/"dbiproxy$ext_pl",//' Makefile.PL
# Remove Win32 specific files to avoid unwanted dependencies
for F in lib/DBI/W32ODBC.pm lib/Win32/DBIODBC.pm; do
    rm "$F"
    sed -i -e '\|^'"$F"'|d' MANIFEST
done

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -empty -exec rm -f {} ';'
%{_fixperms} '%{buildroot}'/*

%check
make test

%files
%license LICENSE
%{_bindir}/dbipro*
%{_bindir}/dbilogstrip
%{perl_vendorarch}/*.p*
%{perl_vendorarch}/DBD/
%{perl_vendorarch}/DBI/
%{perl_vendorarch}/auto/DBI/
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3*

%changelog
* Fri May 24 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.643-3
- Release bump to regenerate package's requires and provides.

* Mon Aug 01 2022 Muhammad Falak <mwani@microsoft.com> - 1.643-2
- Add BR on `perl(blib)` & `perl(Test::More)` to fix ptest build

* Tue Apr 26 2022 Mateusz Malisz <mamalisz@microsoft.com> - 1.643-1
- Update to 1.643

* Fri Jan 28 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.641-6
- Removing dependency on "perl-DB_File".
- Removing unused macros.

* Wed Jan 19 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.641-5
- Adding 'BuildRequires: perl-generators'.
- License verified.

* Mon Oct 12 2020 Joe Schmitt <joschmit@microsoft.com> 1.641-4
- Use new perl package names.
- Provide perl(DB*)

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 1.641-3
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.641-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 1.641-1
- Update to version 1.641

* Mon Apr 3 2017 Robert Qi <qij@vmware.com> 1.636-1
- Upgraded to 1.636

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.634-2
- GA - Bump release of all rpms

* Thu Jan 21 2016 Anish Swaminathan <anishs@vmware.com> 1.634-1
- Upgrade version

* Fri Apr 3 2015 Divya Thaluru <dthaluru@vmware.com> 1.633-1
- Initial version.
