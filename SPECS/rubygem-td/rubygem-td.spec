%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name td
Summary:        CUI Interface
Name:           rubygem-td
Version:        0.16.8
Release:        1%{?dist}
License:        Apache 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
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

%description
This CUI utility wraps the Ruby Client Library td-client-ruby to
interact with the REST API in managing databases and jobs on the Treasure Data Cloud.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Tue Jan 05 2021 Henry Li <lihl@microsoft.com> - 0.16.8-1
- License verified
- Original version for CBL-Mariner