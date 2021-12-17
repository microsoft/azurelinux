Summary:        The Berkley DB database library for C
Name:           libdb
Version:        5.3.28
Release:        6%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System/Libraries
URL:            https://oss.oracle.com/berkeley-db.html
Source0:        http://download.oracle.com/berkeley-db/db-%{version}.tar.gz
Obsoletes:      db

%description
The Berkeley DB package contains libraries used by many other applications for database related functions.

%package	devel
Summary:        Header and development files
Requires:       %{name} = %{version}
Obsoletes:      db-devel

%description	devel
It contains the libraries and header files to create applications

%package        docs
Summary:        DB docs
Group:          Databases
Obsoletes:      db-docs

%description docs
The package contains the DB doc files

%package utils
Summary:        Command line tools for managing Berkeley DB databases
Requires:       %{name} = %{version}-%{release}

%description utils
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. Berkeley DB includes B+tree, Extended
Linear Hashing, Fixed and Variable-length record access methods,
transactions, locking, logging, shared memory caching, and database
recovery. DB supports C, C++, Java and Perl APIs.

%prep
%setup -q -n db-%{version}

%build
cd build_unix
../dist/configure \
	--host=%{_host} --build=%{_build} \
	--prefix=%{_prefix} \
	--enable-compat185 \
	--enable-dbm       \
	--disable-static
make %{?_smp_mflags}

%install
pushd build_unix
make DESTDIR=%{buildroot} docdir=%{_docdir}/%{name}-%{version} install
popd
find %{buildroot} -type f -name "*.la" -delete -print
install -v -d -m755 %{buildroot}/%{_datadir}/licenses/
install -D -m755 LICENSE %{buildroot}/%{_datadir}/licenses/LICENSE
install -D -m755 README %{buildroot}/%{_datadir}/licenses/README

%files
%defattr(-,root,root)
%license LICENSE
%{_libdir}/*.so
%{_datadir}/licenses/*

%files docs
%defattr(-,root,root)
%{_docdir}/%{name}-%{version}/*

%files devel
%defattr(-,root,root)
%exclude %{_includedir}/db_cxx.h
%{_includedir}/*

%files utils
%{_bindir}/db*_archive
%{_bindir}/db*_checkpoint
%{_bindir}/db*_deadlock
%{_bindir}/db*_dump*
%{_bindir}/db*_hotbackup
%{_bindir}/db*_load
%{_bindir}/db*_printlog
%{_bindir}/db*_recover
%{_bindir}/db*_replicate
%{_bindir}/db*_stat
%{_bindir}/db*_upgrade
%{_bindir}/db*_verify
%{_bindir}/db*_tuner

%changelog
* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 5.3.28-6
- Removing the explicit %%clean stage.
- License verified.

* Tue Nov 03 2020 Joe Schmitt <joschmit@microsoft.com> - 5.3.28-5
- Create utils subpackage.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 5.3.28-4
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 5.3.28-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue Nov 14 2017 Alexey Makhalov <amakhalov@vmware.com> 5.3.28-2
- Aarch64 support

* Thu Oct 27 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 5.3.28-1
- Initial build. First version
