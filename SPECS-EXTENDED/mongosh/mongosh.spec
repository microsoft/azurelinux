# https://rpm-packaging-guide.github.io/#what-is-a-spec-file
%define _binary_payload w2.xzdio
# https://jira.mongodb.org/browse/MONGOSH-1159
%define _build_id_links none
# Work around https://salsa.debian.org/debian/debhelper/-/commit/8f29a0726bdebcb01b6fd768fde8016fcd5dc3f4
# (only relevant when building from Debian/Ubuntu)
%undefine _libexecdir
%define _libexecdir %{_exec_prefix}/libexec

Name: mongosh
Provides: mongodb-shell = 2.0
Version: 2.5.2
Release: 1%{?dist}
Group: Development/Tools
Summary: MongoDB Shell CLI REPL Package
License: ASL 2.0 and Proprietary
URL: https://github.com/mongodb-js/mongosh
Source: https://github.com/mongodb-js/mongosh/archive/refs/tags/v2.5.2.tar.gz

BuildRequires: nodejs-devel
BuildRequires: nodejs-npm
BuildRequires: nodejs-packaging
Requires:       openssl-devel >= 1.1.1
Requires:       zlib-devel

%description
MongoDB Shell CLI REPL Package

%prep
%autosetup

%build
npm install --no-package-lock
SEGMENT_API_KEY="dummy" BOXEDNODE_CONFIGURE_ARGS="--shared-openssl,--shared-zlib" npm run compile-exec

%install
ls dist/

mkdir -p %{buildroot}/%{_bindir}/.
install -m 755 dist/mongosh %{buildroot}/%{_bindir}/mongosh
mkdir -p %{buildroot}/%{_mandir}/man1
install -m 644 mongosh.1.gz %{buildroot}/%{_mandir}/man1/mongosh.1.gz

%files
%{_bindir}/mongosh
%{_libdir}/mongosh_crypt_v1.so
%license LICENSE-mongosh
%license LICENSE-crypt-library
%doc README
%doc THIRD_PARTY_NOTICES
%doc .sbom.json
%{_mandir}/man1/mongosh.1.gz

%changelog
* Thu Jun 12 2025 Sumit Jena <v-sumitjena@microsoft.com> - 2.5.2-1
- Initial Azure Linux import from upstream
- License Verified