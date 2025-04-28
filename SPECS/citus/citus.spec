Summary:	PostgreSQL-based distributed RDBMS
Name:		citus
Conflicts:	%{name}
Version:	13.0.3
Release:	1%{dist}
License:	AGPLv3
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Source0:	https://github.com/citusdata/%{name}/archive/v%{version}.tar.gz#%{name}-%{version}.tar.gz
URL:		https://github.com/citusdata/%{name}
BuildRequires:	postgresql-devel libcurl-devel
Requires:	postgresql
Provides:	%{name}

%description
Citus horizontally scales PostgreSQL across commodity servers
using sharding and replication. Its query engine parallelizes
incoming SQL queries across these servers to enable real-time
responses on large datasets.

Citus extends the underlying database rather than forking it,
which gives developers and enterprises the power and familiarity
of a traditional relational database. As an extension, Citus
supports new PostgreSQL releases, allowing users to benefit from
new features while maintaining compatibility with existing
PostgreSQL tools. Note that Citus supports many (but not all) SQL
commands.

%prep
%autosetup -n %{name}-%{version}

%build
currentgccver="$(gcc -dumpversion)"
requiredgccver="4.8.2"
if [ "$(printf '%s\n' "$requiredgccver" "$currentgccver" | sort -V | head -n1)" != "$requiredgccver" ]; then
    echo ERROR: At least GCC version "$requiredgccver" is needed to build with security flags
    exit 1
fi
exit 1
%configure PG_CONFIG=%{pginstdir}/bin/pg_config --with-extra-version="%{?conf_extra_version}" --with-security-flags CC=$(command -v gcc)
make %{?_smp_mflags}

%install
%make_install
# Install documentation with a better name:
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension
%{__cp} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md
%{__cp} NOTICE %{buildroot}%{pginstdir}/doc/extension/NOTICE-%{sname}
# Set paths to be packaged other than LICENSE, README & CHANGELOG.md
echo %{pginstdir}/include/server/citus_*.h >> installation_files.list
echo %{pginstdir}/include/server/distributed/*.h >> installation_files.list
echo %{pginstdir}/lib/%{sname}.so >> installation_files.list
[[ -f %{buildroot}%{pginstdir}/lib/citus_columnar.so ]] && echo %{pginstdir}/lib/citus_columnar.so >> installation_files.list
[[ -f %{buildroot}%{pginstdir}/lib/citus_decoders/pgoutput.so ]] && echo %{pginstdir}/lib/citus_decoders/pgoutput.so >> installation_files.list
[[ -f %{buildroot}%{pginstdir}/lib/citus_decoders/wal2json.so ]] && echo %{pginstdir}/lib/citus_decoders/wal2json.so >> installation_files.list
[[ -f %{buildroot}%{pginstdir}/lib/citus_pgoutput.so ]] && echo %{pginstdir}/lib/citus_pgoutput.so >> installation_files.list
[[ -f %{buildroot}%{pginstdir}/lib/citus_wal2json.so ]] && echo %{pginstdir}/lib/citus_wal2json.so >> installation_files.list
echo %{pginstdir}/share/extension/%{sname}-*.sql >> installation_files.list
echo %{pginstdir}/share/extension/%{sname}.control >> installation_files.list
# Since files below may be non-existent in some versions, ignoring the error in case of file absence
[[ -f %{buildroot}%{pginstdir}/share/extension/citus_columnar.control ]] && echo %{pginstdir}/share/extension/citus_columnar.control >> installation_files.list
columnar_sql_files=(`find %{buildroot}%{pginstdir}/share/extension -maxdepth 1 -name "columnar-*.sql"`)
if [ ${#columnar_sql_files[@]} -gt 0 ]; then
    echo %{pginstdir}/share/extension/columnar-*.sql >> installation_files.list
fi

citus_columnar_sql_files=(`find %{buildroot}%{pginstdir}/share/extension -maxdepth 1 -name "citus_columnar-*.sql"`)
if [ ${#citus_columnar_sql_files[@]} -gt 0 ]; then
    echo %{pginstdir}/share/extension/citus_columnar-*.sql >> installation_files.list
fi

[[ -f %{buildroot}%{pginstdir}/bin/pg_send_cancellation ]] && echo %{pginstdir}/bin/pg_send_cancellation >> installation_files.list
%ifarch ppc64 ppc64le
%else
    %if 0%{?rhel} && 0%{?rhel} <= 6
    %else
        echo %{pginstdir}/lib/bitcode/%{sname}/*.bc >> installation_files.list
        echo %{pginstdir}/lib/bitcode/%{sname}*.bc >> installation_files.list
        echo %{pginstdir}/lib/bitcode/%{sname}/*/*.bc >> installation_files.list

        # Columnar does not exist in Citus versions < 10.0
        # At this point, we don't have %{pginstdir},
        # so first check build directory for columnar.
        [[ -d %{buildroot}%{pginstdir}/lib/bitcode/columnar/ ]] && echo %{pginstdir}/lib/bitcode/columnar/*.bc >> installation_files.list
        [[ -d %{buildroot}%{pginstdir}/lib/bitcode/citus_columnar/ ]] && echo %{pginstdir}/lib/bitcode/citus_columnar/*.bc >> installation_files.list
        [[ -d %{buildroot}%{pginstdir}/lib/bitcode/citus_columnar/safeclib ]] && echo %{pginstdir}/lib/bitcode/citus_columnar/safeclib/*.bc >> installation_files.list
        [[ -d %{buildroot}%{pginstdir}/lib/bitcode/citus_pgoutput ]] && echo %{pginstdir}/lib/bitcode/citus_pgoutput/*.bc >> installation_files.list
        [[ -d %{buildroot}%{pginstdir}/lib/bitcode/citus_wal2json ]] && echo %{pginstdir}/lib/bitcode/citus_wal2json/*.bc >> installation_files.list
    %endif
%endif

%clean
%{__rm} -rf %{buildroot}

%files -f installation_files.list
%files
%defattr(-,root,root,-)
%doc CHANGELOG.md
%if 0%{?rhel} && 0%{?rhel} <= 6
%doc LICENSE
%else
%license LICENSE
%endif
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%doc %{pginstdir}/doc/extension/NOTICE-%{sname}

%changelog
* Mon Feb 17 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 16.7-1
- Initial import for Azure Linux from Azure
- Based on the spec file of citus packaging
