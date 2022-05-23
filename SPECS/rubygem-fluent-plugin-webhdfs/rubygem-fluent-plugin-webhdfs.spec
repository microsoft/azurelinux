%global debug_package %{nil}
%global gem_name fluent-plugin-webhdfs
Summary:        Hadoop WebHDFS output plugin for Fluentd
Name:           rubygem-fluent-plugin-webhdfs
Version:        1.5.0
Release:        1%{?dist}
License:        Apache 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/fluent/fluent-plugin-webhdfs
Source0:        https://github.com/fluent/fluent-plugin-webhdfs/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
BuildRequires:  git
BuildRequires:  ruby
Requires:       rubygem-fluentd
Requires:       rubygem-webhdfs

%description
Fluentd output plugin to write data into Hadoop HDFS over WebHDFS/HttpFs.

%prep
%setup -q -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem
#add LICENSE.txt file to buildroot from Source0
cp LICENSE.txt %{buildroot}%{gem_instdir}/

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/LICENSE.txt
%{gemdir}

%changelog
* Mon Jan 04 2021 Henry Li <lihl@microsoft.com> - 1.2.4-1
- License verified
- Original version for CBL-Mariner
