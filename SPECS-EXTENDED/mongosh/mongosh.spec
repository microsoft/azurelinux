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
Version: 2.5.1
Release: 1%{?dist}
Group: Development/Tools
Summary: MongoDB Shell CLI REPL Package
License: ASL 2.0 and Proprietary
URL: https://github.com/mongodb-js/mongosh
Source0: https://github.com/mongodb-js/mongosh/archive/refs/tags/v2.5.1.tar.gz
# The Tarball contains all the node_modules on which the package is dependent upon. 
# To generate the tarball we need to run rpm install --force under source. 
# Once all the node_modules are fetch a tarball needs to be generated using the command tar -cvzf node_modules.tar.gz node_modules
# additionally we need to add the packages folder as well.
Source1: node_modules.tar.gz
Source2: packages.tar.gz

BuildRequires: nodejs-devel
BuildRequires: nodejs-packaging
BuildRequires: nodejs-npm
Requires:       openssl-devel >= 1.1.1
Requires:       zlib-devel

%description
MongoDB Shell CLI REPL Package

%prep
%autosetup
tar -zxvf %{SOURCE1}
tar -zxvf %{SOURCE2}

%build
SEGMENT_API_KEY="dummy" BOXEDNODE_CONFIGURE_ARGS="--shared-openssl,--shared-zlib" npm run compile-exec

%install
mkdir -p %{buildroot}/%{_bindir}/.
install -m 755 dist/mongosh %{buildroot}/%{_bindir}/mongosh
mkdir -p %{buildroot}/%{_mandir}/man1
install -m 644 mongosh.1.gz %{buildroot}/%{_mandir}/man1/mongosh.1.gz

%files
%{_bindir}/mongosh
%license LICENSE-mongosh
%doc README
%doc THIRD_PARTY_NOTICES
%{_mandir}/man1/mongosh.1.gz

%changelog
* Thu Jun 12 2025 Sumit Jena <v-sumitjena@microsoft.com> - 2.5.2-1
- Initial Azure Linux import from upstream
- License Verified