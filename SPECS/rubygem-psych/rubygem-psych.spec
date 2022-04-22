%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name psych
Summary:        A libyaml wrapper for Ruby
Name:           rubygem-psych
Version:        4.0.3
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/ruby/psych
Source0:        https://github.com/ruby/psych/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
BuildRequires:  git
BuildRequires:  ruby
Provides:       rubygem(psych) = %{version}-%{release}

%description
Psych is a YAML parser and emitter. Psych leverages
libyaml[http://pyyaml.org/wiki/LibYAML] for its YAML parsing and emitting
capabilities. In addition to wrapping libyaml, Psych also knows how to
serialize and de-serialize most Ruby objects to and from the YAML format.

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
* Thu Apr 21 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 4.0.3-1
- Update to v4.0.3

* Wed Apr 20 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 3.0.0-2
- Add provides

* Fri Apr 15 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 3.0.0-1
- License verified
- Included descriptions from Fedora 33 spec (license: MIT).
- Original version for CBL-Mariner
