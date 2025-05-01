Summary:	PostgreSQL-based distributed RDBMS
Name:		citus
Conflicts:	%{name}
Version:	13.0.3
Release:	1%{?dist}
License:	AGPLv3
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Source0:	https://github.com/citusdata/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%if 0%{?with_check}
Patch0:         disable_unwanted_tests.patch
%endif
URL:		https://github.com/citusdata/%{name}
BuildRequires:	postgresql-devel
BuildRequires:	libcurl-devel
BuildRequires:	lz4-devel
BuildRequires:  pkgconfig(icu-i18n)
BuildRequires:  pkgconfig(icu-uc)
%if 0%{?with_check}
BuildRequires:  shadow-utils
%endif
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
%autosetup -p1 -n %{name}-%{version}

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

%check
%if 0%{?with_check}
mkdir -p /run/postgresql
useradd -s /usr/bin/sh test
usermod -a -G root test
chmod -R g+w %{_includedir}/postgresql
chmod -R g+w %{_libdir}/postgresql
chmod -R g+w %{_datadir}/postgresql
chmod -R g+w /run/postgresql
chown -R test .
su test -s /bin/sh -c 'make check'
exit 1
%endif

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
* Mon Apr 29 2025 Sandeep Karambelkar <skarambelkar@microsoft.com> - 13.0.3-1
- Original version for Azure Linux
- Based on the spec file of citus packaging
- License verified
