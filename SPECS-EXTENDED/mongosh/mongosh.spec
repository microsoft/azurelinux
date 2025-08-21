Summary:        MongoDB Shell CLI REPL Package.
Name:           mongosh
Version:        2.5.5
Release:        1%{?dist}
License:        Apache License Version 2.0
Group:          Development/Tools
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Url:            https://github.com/mongodb-js/mongosh
Source0:        https://github.com/mongodb-js/%{name}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        mongosh_node_modules.tar.gz
Source2:        mongosh_packages.tar.gz
Source3:        mongodb-client-encryption.tar.gz
Source4:        mongosh_lazy-webpack-modules.tar.gz
Source5:        mongosh_npm_lazy_cache.tar.gz
Source6:        node-v20.19.3.tar.gz
Source7:        SHASUMS256.txt
Patch0:         fix_build_with_local_files.patch
BuildRequires:  nodejs-npm
BuildRequires:  nodejs-devel
BuildRequires:  git

%description
MongoDB Shell CLI REPL Package

%prep
%autosetup -p1
tar -xf %{SOURCE1}
tar -xf %{SOURCE2}
mkdir -p tmp/fle-buildroot
tar -xf %{SOURCE3} -C tmp/fle-buildroot/
tar -xf %{SOURCE4} -C tmp/
tar -xf %{SOURCE5} -C /root/
mkdir -p /tmp/boxednode/mongosh
cp %{SOURCE6} /tmp/boxednode/mongosh/
cp %{SOURCE7} /tmp/boxednode/mongosh/SHASUMS256.txt

%build
# Run npm_lazy server in the background for npm requests proxying from local cache
./node_modules/npm_lazy/bin/npm_lazy > ~/npm_lazy.log 2>&1 &

# Route npm calls to npm_lazy
npm config set registry http://localhost:8080/

#npm run compile
#Run with BOXEDNODE_MAKE_ARGS="-j2" if running in container
BOXEDNODE_MAKE_ARGS="-j6" SEGMENT_API_KEY="dummy" NODE_JS_VERSION=20.19.3 npm run compile-exec

#stop the npm_lazy server
kill %1

%install
mkdir -p %{buildroot}/%{_bindir}/.
install -m 755 dist/mongosh %{buildroot}/%{_bindir}/mongosh

%files
%{_bindir}/mongosh
%license LICENSE
%license THIRD_PARTY_NOTICES.md
%doc README.md
# doc THIRD_PARTY_NOTICES.md

%changelog
%changelog
* Thu Jul 03 2025 Sandeep Karambelkar <skarambelkar@microsoft.com> - 2.5.5-1
- Original version for Azure Linux
- License Verified
