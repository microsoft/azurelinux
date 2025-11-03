%global debug_package %{nil}
%global gem_name webrick
Summary:        HTTP server toolkit
Name:           rubygem-%{gem_name}
Version:        1.8.1
Release:        3%{?dist}
License:        BSD
Vendor:	        Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/ruby/webrick
Source0:        https://github.com/ruby/webrick/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
Patch0:         CVE-2023-40225-content-length-validation.patch
Patch1:         CVE-2025-6442.patch
BuildRequires:  git
BuildRequires:  ruby
BuildRequires:  rubygem-test-unit
BuildRequires:  rubygems-devel
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
WEBrick is an HTTP server toolkit that can be configured as an HTTPS server, a proxy server, and a virtual-host server.
WEBrick features complete logging of both server operations and HTTP access.
WEBrick supports both basic and digest authentication in addition to algorithms not in RFC 2617.
A WEBrick server can be composed of multiple WEBrick servers or servlets to provide differing behavior on a per-host or per-path basis. WEBrick includes servlets for handling CGI scripts, ERB pages, Ruby blocks and directory listings.
WEBrick also includes tools for daemonizing a process and starting a process at a higher privilege level and dropping permissions.

%prep
%autosetup -p1 -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%check
pushd %{buildroot}%{gem_instdir}
# Symlink the test suite from source directory
ln -sf %{_builddir}/%{gem_name}-%{version}/test .
 
# Use --verbose to set $VERBOSE to true. `test_sni` in test/webrick/test_https.rb
# relies on output in $stderr from lib/webrick/ssl.rb that is only written there
# if $VERBOSE is true.
# https://github.com/ruby/webrick/pull/158
ruby --verbose           \
     -Ilib:test:test/lib \
     -rhelper            \
     -e 'Dir.glob "./test/**/test_*.rb", &method(:require)'
popd

%files
%defattr(-,root,root,-)
%license LICENSE.txt
%{gemdir}

%changelog
* Wed Jul 16 2025 Kavya Sree Kaitepalli <kkaitepalli@microsoft.com> - 1.8.1-3
- Add %check section
- Add patch to fix failing tests

* Fri Jun 27 2025 Archana Shettigar <v-shettigara@microsoft.com> - 1.8.1-2
- Patch for CVE-2025-6442

* Thu Nov 02 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.8.1-1
- Auto-upgrade to 1.8.1 - Azure Linux 3.0 - package upgrades

* Mon Jun 13 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.7.0-1
- License verified
- Original version for CBL-Mariner
