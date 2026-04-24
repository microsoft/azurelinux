# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{!?postgresql_default:%global postgresql_default 1}

%global majorname pg_repack
%global pgversion 18
Name:           postgresql%{pgversion}-%{majorname}
Version:        1.5.2
Release: 2%{?dist}
Summary:        Reorganize tables in PostgreSQL databases without any locks

License:        BSD-3-Clause
URL:            http://reorg.github.io/%{majorname}/
Source0:        https://github.com/reorg/%{majorname}/archive/ver_%{version}.tar.gz

%if %?postgresql_default
%global pkgname %{majorname}
%package -n %{pkgname}
Summary: Reorganize tables in PostgreSQL databases without any locks
%else
%global pkgname %name
%endif

BuildRequires: make
BuildRequires:  gcc, openssl-devel, lz4-devel, libzstd-devel
BuildRequires:  postgresql-server-devel >= 18, postgresql-server-devel < 19
BuildRequires:  postgresql-server >= 18, postgresql-server < 19
BuildRequires:  postgresql-static >= 18, postgresql-static < 19
BuildRequires:  readline-devel, zlib-devel
BuildRequires:  python3-docutils
Requires(pre):  postgresql-server >= 18, postgresql-server < 19

%global precise_version %{?epoch:%epoch:}%version-%release
Provides: %{pkgname} = %precise_version
%if %?postgresql_default
Provides: postgresql-%{majorname} = %precise_version
Provides: %name = %precise_version
%endif
Provides: %{pkgname}%{?_isa} = %precise_version
Provides: %{majorname}-any
Conflicts: %{majorname}-any

%description
pg_repack is a PostgreSQL extension which lets you remove
bloat from tables and indexes, and optionally
restore the physical order of clustered indexes.
Unlike CLUSTER and VACUUM FULL it works online,
without holding an exclusive lock on the processed tables during processing.
pg_repack is efficient to boot,
with performance comparable to using CLUSTER directly.

Please check the documentation (in the doc directory or online)
for installation and usage instructions.

%description -n %{pkgname}
pg_repack is a PostgreSQL extension which lets you remove
bloat from tables and indexes, and optionally
restore the physical order of clustered indexes.
Unlike CLUSTER and VACUUM FULL it works online,
without holding an exclusive lock on the processed tables during processing.
pg_repack is efficient to boot,
with performance comparable to using CLUSTER directly.

Please check the documentation (in the doc directory or online)
for installation and usage instructions.

%prep
%setup -n %{majorname}-ver_%{version} -q


%build

make %{?_smp_mflags}
cd doc
make


%install
%make_install

%files -n %{pkgname}
%{_bindir}/%{majorname}
%{_libdir}/pgsql/%{majorname}.so
%if 0%{?postgresql_server_llvmjit}
%{_libdir}/pgsql/bitcode/%{majorname}.index.bc
%{_libdir}/pgsql/bitcode/%{majorname}/pgut/pgut-spi.bc
%{_libdir}/pgsql/bitcode/%{majorname}/repack.bc
%endif
%{_datadir}/pgsql/extension/%{majorname}.control
%{_datadir}/pgsql/extension/%{majorname}--%{version}.sql

%license COPYRIGHT

%doc README.rst
%doc doc/%{majorname}.html
%doc doc/%{majorname}.rst
%doc doc/%{majorname}_jp.html
%doc doc/%{majorname}_jp.rst
%doc doc/release.html
%doc doc/release.rst

%changelog
* Thu Jul 24 2025 Nikola Davidova <ndavidov@redhat.com> - 1.5.2-1
- Initial packaging
