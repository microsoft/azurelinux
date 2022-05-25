%global debug_package %{nil}
%global gem_name ruby2_keywords
Summary:        Shim library for Module#ruby2_keywords
Name:           rubygem-%{gem_name}
Version:        0.0.5
Release:        1%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/ruby/ruby2_keywords
Source0:        https://github.com/ruby/ruby2_keywords/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
Patch0:         remove-missing-files.patch
BuildRequires:  ruby

%description
Provides empty Module#ruby2_keywords method, for the forward
source-level compatibility against ruby2.7 and ruby3.

%prep
%autosetup -p1 -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem
#add LICENSE file to buildroot from Source0
cp LICENSE %{buildroot}%{gem_instdir}/

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/LICENSE
%{gemdir}

%changelog
* Wed Jan 06 2021 Henry Li <lihl@microsoft.com> - 0.0.2-1
- License verified
- Original version for CBL-Mariner
