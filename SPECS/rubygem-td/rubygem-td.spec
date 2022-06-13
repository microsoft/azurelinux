%global debug_package %{nil}
%global gem_name td
Summary:        CUI Interface
Name:           rubygem-%{gem_name}
Version:        0.16.10
Release:        1%{?dist}
License:        Apache 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://www.treasuredata.com/
Source0:        https://github.com/treasure-data/td/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
BuildRequires:  git
BuildRequires:  ruby
Requires:       rubygem-hirb
Requires:       rubygem-msgpack
Requires:       rubygem-parallel
Requires:       rubygem-ruby-progressbar
Requires:       rubygem-rubyzip
Requires:       rubygem-td-client
Requires:       rubygem-td-logger
Requires:       rubygem-yajl-ruby
Requires:       rubygem-zip-zip
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
This CUI utility wraps the Ruby Client Library td-client-ruby to
interact with the REST API in managing databases and jobs on the Treasure Data Cloud.

%prep
%setup -q -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Tue Jan 05 2021 Henry Li <lihl@microsoft.com> - 0.16.8-1
- License verified
- Original version for CBL-Mariner
