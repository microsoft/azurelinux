%global debug_package %{nil}
%global gem_name td
%global gems_version 3.1.0
Summary:        CUI Interface
Name:           rubygem-%{gem_name}
Version:        0.16.8
Release:        2%{?dist}
License:        Apache 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://www.treasuredata.com/
Source0:        https://github.com/treasure-data/td/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
Patch0:         fix-file_list.patch
BuildRequires:  git
BuildRequires:  ruby
AutoReq:        no
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
%autosetup -p1 -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} --bindir %{buildroot}%{_prefix}/lib/ruby/gems/%{gems_version}/bin/ %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Wed Jun 22 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 0.16.8-2
- Build from .tar.gz source.

* Tue Jan 05 2021 Henry Li <lihl@microsoft.com> - 0.16.8-1
- License verified
- Original version for CBL-Mariner
