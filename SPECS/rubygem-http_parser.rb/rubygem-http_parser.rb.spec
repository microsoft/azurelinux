%global gem_name http_parser.rb
Summary:        simple callback-based HTTP request/response parser
Name:           rubygem-%{gem_name}
Version:        0.6.1
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/tmm1/http_parser.rb
Source0:        %{_mariner_sources_url}/%{gem_name}-%{version}.tar.gz
# A buildable snappy environment needs functioning submodules that do not work from the archive download
# To recreate the tar.gz run the following
#  git clone https://github.com/tmm1/http_parser.rb
#  pushd rubygem-http_parser.rb
#  git checkout <version>
#  git submodule init
#  git submodule update
#  popd
#  sudo mv %{name} %{name}-%{version}
#  sudo tar -cvf %{name}-%{version}.tar.gz %{name}-%{version}/

BuildRequires:  git
BuildRequires:  rubygem-ffi
BuildRequires:  rubygem-json
BuildRequires:  rubygem-rake-compiler
BuildRequires:  rubygem-rspec
BuildRequires:  rubygem-yajl-ruby
BuildRequires:  ruby
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
A simple callback-based HTTP request/response parser for writing
http servers, clients and proxies.

%prep
%setup -q -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/LICENSE-MIT
%{gemdir}

%changelog
* Wed Jun 22 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 0.6.1-1
- Downgrade to v0.6.1.
- Build from .tar.gz source.

* Wed Jan 06 2021 Henry Li <lihl@microsoft.com> - 0.8.0-1
- License verified
- Original version for CBL-Mariner
