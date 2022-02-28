%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name rdiscount

Summary:       Converts documents in Markdown syntax to HTML
Name:          rubygem-%{gem_name}
Version:       2.2.0.2
Release:       1%{?dist}
License:       MIT
Vendor:	       Microsoft Corporation
Distribution:  Mariner
URL:           http://github.com/rtomayko/rdiscount
#Source0:       https://github.com/davidfstr/rdiscount/archive/refs/tags/%{version}.tar.gz
Source0:       %{gem_name}-%{version}.tar.gz
BuildRequires: ruby

%description
RDiscount converts documents in Markdown syntax to HTML.

%prep
%setup -q -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/COPYING
%{gemdir}

%changelog
* Thu Dec 30 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 2.2.0.2-1
- License verified
- Original version for CBL-Mariner
