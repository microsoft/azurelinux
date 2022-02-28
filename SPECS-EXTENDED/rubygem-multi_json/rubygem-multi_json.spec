%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name multi_json
Summary:        A generic swappable back-end for JSON handling
Name:           rubygem-multi_json
Version:        1.15.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            http://rdoc.info/projects/intridea/multi_json
#Source0:        https://github.com/intridea/multi_json/archive/refs/tags/v%{version}.tar.gz
Source0:        %{gem_name}-%{version}.tar.gz
BuildRequires:  ruby

%description
A common interface to multiple JSON libraries, including Oj, Yajl, the JSON
gem (with C-extensions), the pure-Ruby JSON gem, NSJSONSerialization, gson.rb, JrJackson, and OkJson.

%prep
%setup -q -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/LICENSE.md
%{gemdir}

%changelog
* Tue Jan 05 2021 Henry Li <lihl@microsoft.com> - 1.15.0-1
- License verified
- Original version for CBL-Mariner