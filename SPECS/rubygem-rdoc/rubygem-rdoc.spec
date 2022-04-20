%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name rdoc
Summary:        RDoc produces HTML and command-line documentation for Ruby projects
Name:           rubygem-rdoc
Version:        6.4.0
Release:        2%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://ruby.github.io/rdoc/
Source0:        https://github.com/ruby/rdoc/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
Patch0:         remove_files_from_gitignore.patch
BuildRequires:  git
BuildRequires:  ruby
Requires:       rubygem-io-console
Requires:       rubygem-json
Requires:       rubygem-psych
Provides:       rdoc = %{version}-%{release}
Provides:       ri = %{version}-%{release}
Provides:       rubygem(rdoc) = %{version}-%{release}
Provides:       rubygem(ri) = %{version}-%{release}
BuildArch:      noarch

%description
RDoc produces HTML and command-line documentation for Ruby projects.  RDoc
includes the 'rdoc' and 'ri' tools for generating and displaying online
documentation.

%prep
%autosetup -p1 -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem
#add LICENSE.rdoc and LEGAL.rdoc files to buildroot from Source0
cp LICENSE.rdoc %{buildroot}%{gem_instdir}/
cp LEGAL.rdoc %{buildroot}%{gem_instdir}/

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/LICENSE.rdoc
%license %{gemdir}/gems/%{gem_name}-%{version}/LEGAL.rdoc
%{gemdir}

%changelog
* Wed Apr 20 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 6.4.0-2
- Add provides

* Fri Apr 15 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 6.4.0-1
- License verified
- Included descriptions from Fedora 36 spec (license: MIT).
- Original version for CBL-Mariner
