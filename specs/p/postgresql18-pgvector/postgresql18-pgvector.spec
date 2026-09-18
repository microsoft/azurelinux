# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{!?postgresql_default:%global postgresql_default 1}

%global pname vector
%global sname pgvector
%global pgversion 18

%ifarch ppc64 ppc64le s390 s390x armv7hl
	%{!?llvm:%global llvm 0}
%else
	%{!?llvm:%global llvm 0}
%endif

Name:		postgresql%{pgversion}-%{sname}
Version:	0.8.0
Release:	1%{?dist}
Summary:	Open-source vector similarity search for Postgres
License:	PostgreSQL
URL:		https://github.com/%{sname}/%{sname}/
Source0:	https://github.com/%{sname}/%{sname}/archive/refs/tags/v%{version}.tar.gz

# Upstream commits for compatiblity with PG18 present on master branch
# not yet included in any tag or release
Patch0:		78ed8f1.patch
Patch1:		2c53c30.patch

%if %?postgresql_default
%global pkgname %{sname}
%package -n %{pkgname}
Summary: Open-source vector similarity search for Postgres
%else
%global pkgname %name
%endif

BuildRequires:	make gcc
BuildRequires:	postgresql%{pgversion}-server-devel
Requires:	postgresql%{pgversion}-server

%global precise_version %{?epoch:%epoch:}%version-%release

%if %?postgresql_default
Provides: postgresql-%{sname} = %precise_version
Provides: %name = %precise_version
%endif
Provides: %{pkgname}%{?_isa} = %precise_version
Provides: %{pkgname} = %precise_version
Provides: %{sname}-any
Conflicts: %{sname}-any

%description
Open-source vector similarity search for Postgres. Supports L2 distance,
inner product, and cosine distance

%description -n %{pkgname}
Open-source vector similarity search for Postgres. Supports L2 distance,
inner product, and cosine distance

%if %llvm
%package -n %{pkgname}-llvmjit
Summary:	Just-in-time compilation support for pgvector
Requires:	%{pkgname}%{?_isa} = %precise_version
Requires:	llvm => 13.0

%description -n %{pkgname}-llvmjit
This packages provides JIT support for pgvector
%endif

%prep
%autosetup -p1 -n %{sname}-%{version}

%build
%make_build %{?_smp_mflags} OPTFLAGS=""

%install
%make_install

#Remove header file, we don't need it right now:
%{__rm} %{buildroot}/%{_includedir}/pgsql/server/extension/%{pname}/%{pname}.h
%{__rm} %{buildroot}/%{_includedir}/pgsql/server/extension/%{pname}/halfvec.h
%{__rm} %{buildroot}/%{_includedir}/pgsql/server/extension/%{pname}/sparsevec.h

%files -n %{pkgname}
%doc README.md
%license LICENSE
%{_libdir}/pgsql/%{pname}.so
%{_datadir}/pgsql/extension//%{pname}.control
%{_datadir}/pgsql/extension/%{pname}*sql
%if %llvm
%files -n %{pkgname}-llvmjit
%{_libdir}/pgsql/bitcode/%{pname}*.bc
%{_libdir}/pgsql/bitcode/%{pname}/src/*.bc
%endif

%changelog
* Thu Jul 24 2025 Nikola Davidova <ndavidov@redhat.com> - 0.8.0-1
- Initial packaging

