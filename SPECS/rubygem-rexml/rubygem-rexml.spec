%global debug_package %{nil}
%global gem_name rexml
Summary:        REXML is an XML toolkit for Ruby
Name:           rubygem-%{gem_name}
Version:        3.2.8
Release:        1%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Languages
URL:            https://github.com/ruby/rexml
Source0:        https://github.com/ruby/rexml/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
Patch0:         add-support-for-old-strscan.patch
BuildRequires:  git
BuildRequires:  ruby
Requires:       ruby(release)
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
REXML was inspired by the Electric XML library for Java, which features an easy-to-use API, small size, and speed. Hopefully, REXML, designed with the same philosophy, has these same features. I've tried to keep the API as intuitive as possible, and have followed the Ruby methodology for method naming and code flow, rather than mirroring the Java API.
REXML supports both tree and stream document parsing. Stream parsing is faster (about 1.5 times as fast). However, with stream parsing, you don't get access to features such as XPath.

%prep
%autosetup -n %{gem_name}-%{version} -p1

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%license LICENSE.txt
%{gemdir}

%changelog
* Wed May 22 2024 Neha Agarwal <nehaagarwal@microsoft.com> - 3.2.8-1
- Upgrade to v3.2.8 to fix CVE-2024-35176
- Add patch to support old strscan

* Fri Nov 03 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.2.6-1
- Auto-upgrade to 3.2.6 - Azure Linux 3.0 - package upgrades

* Mon Jun 13 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 3.2.5-1
- License verified
- Original version for CBL-Mariner
