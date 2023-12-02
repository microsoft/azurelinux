%global debug_package %{nil}
%global gem_name nokogiri
Summary:        a Rubygem providing HTML, XML, SAX, and Reader parsers with XPath and CSS selector support
Name:           rubygem-nokogiri
Version:        1.15.4
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://nokogiri.org/
Source0:        https://github.com/sparklemotion/nokogiri/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
BuildRequires:  git
BuildRequires:  ruby
BuildRequires:  libxml2-devel
BuildRequires:  libxslt-devel
BuildRequires:  rubygem-mini_portile2
Requires:       rubygem-mini_portile2
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
Nokogiri (鋸) makes it easy and painless to work with XML and HTML from Ruby.
It provides a sensible, easy-to-understand API for reading, writing, modifying,
and querying documents. It is fast and standards-compliant by relying on native
parsers like libxml2 (C) and xerces (Java).

%prep
%setup -q -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem --platform=ruby -- --use-system-libraries

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/LICENSE.md
%{gemdir}

%changelog
* Thu Nov 02 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.15.4-1
- Auto-upgrade to 1.15.4 - Azure Linux 3.0 - package upgrades

* Wed Jun 22 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.13.6-1
- Update to v1.13.6.
- Build from .tar.gz source.

* Mon Jan 04 2021 Henry Li <lihl@microsoft.com> - 1.11.0.rc2-1
- License verified
- Original version for CBL-Mariner
