# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{!?postgresql_default:%global postgresql_default 1}

%global pre Final
%global majorname postgres-decoderbufs
%global pgversion 18

Name:		postgresql%{pgversion}-decoderbufs
Version:	3.2.0
Release:	2%{?pre:.%pre}%{?dist}
Summary:	PostgreSQL Protocol Buffers logical decoder plugin

License:	MIT
URL:		https://github.com/debezium/postgres-decoderbufs

%global full_version %{version}.%{?pre:%pre}%{?!pre:Final}

Source0:	https://github.com/debezium/%{majorname}/archive/v%{full_version}.tar.gz

%if %?postgresql_default
%global pkgname %{majorname}
%package -n %{pkgname}
Summary: PostgreSQL Audit Extension
%else
%global pkgname %name
%endif

BuildRequires:	make
BuildRequires:	gcc
BuildRequires:	postgresql-server-devel >= 18, postgresql-server-devel < 19
BuildRequires:	protobuf-c-devel

Requires:	protobuf-c
Requires(pre): postgresql-server >= 18, postgresql-server < 19

%global precise_version %{?epoch:%epoch:}%version-%release
Provides: %{pkgname} = %precise_version
%if %?postgresql_default
Provides: %name = %precise_version
Provides: postgresql-%{majorname} = %precise_version
%endif
Provides: %{pkgname}%{?_isa} = %precise_version
Provides: %{majorname}-any
Conflicts: %{majorname}-any

%description
A PostgreSQL logical decoder output plugin to deliver data as Protocol Buffers messages.

%description -n %{pkgname}
A PostgreSQL logical decoder output plugin to deliver data as Protocol Buffers messages.

%if 0%{?postgresql_server_llvmjit}
%package llvmjit
Summary:	Just-in-time compilation support for %{majorname}
Requires:	%{majorname}%{?_isa} = %{version}-%{release}

%description llvmjit
Just-in-time compilation support for %{majorname}.
%endif

%prep
%autosetup -n %{majorname}-%{full_version} -p1

%build
%make_build

%install
%make_install

%files -n %{pkgname}
%doc README.md
%license LICENSE
%{_libdir}/pgsql/decoderbufs.so
%{_datadir}/pgsql/extension/decoderbufs.control

%if 0%{?postgresql_server_llvmjit}
%files llvmjit
%{_libdir}/pgsql/bitcode/decoderbufs.index.bc
%{_libdir}/pgsql/bitcode/decoderbufs/
%endif


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-2.Final
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jul 24 2025 Nikola Davidova <ndavidov@redhat.com> - 3.2.0-1
- Initial packaging
