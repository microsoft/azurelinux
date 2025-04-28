Summary:	PostgreSQL-based distributed RDBMS
Name:		citus
Conflicts:	%{name}
Version:	13.0.3
Release:	1%{dist}
License:	AGPLv3
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Source0:	https://github.com/citusdata/%{name}/archive/v%{version}.tar.gz
URL:		https://github.com/citusdata/%{name}
BuildRequires:	postgresql-devel
BuildRequires:	libcurl-devel
BuildRequires:	lz4-devel
BuildRequires:  pkgconfig(icu-i18n)
BuildRequires:  pkgconfig(icu-uc)
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
%configure PG_CONFIG=%{_bindir}/pg_config --with-extra-version="%{?conf_extra_version}" --with-security-flags CC=$(command -v gcc)
make %{?_smp_mflags}

%install
%make_install
# Install documentation with a better name:
%{__mkdir} -p %{buildroot}%{_docdir}/postgresql/extension
%{__cp} README.md %{buildroot}%{_docdir}/postgresql/extension/README-%{name}.md
%{__cp} NOTICE %{buildroot}%{_docdir}/postgresql/extension/NOTICE-%{name}

%files
%defattr(-,root,root,-)
%doc CHANGELOG.md
%license LICENSE
%{_includedir}/*
%{_libdir}/*
%{_datadir}/*
%doc %{_docdir}/postgresql/extension/README-%{name}.md
%doc %{_docdir}/postgresql/extension/NOTICE-%{name}

%changelog
* Mon Feb 17 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 16.7-1
- Initial import for Azure Linux from Azure
- Based on the spec file of citus packaging
