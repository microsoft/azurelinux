%global debug_package %{nil}
%global gem_name rexml
Summary:        REXML is an XML toolkit for Ruby
Name:           rubygem-%{gem_name}
Version:        3.2.7
Release:        3%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/ruby/rexml
Source0:        https://github.com/ruby/rexml/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
Patch0:         CVE-2024-41946.patch
Patch1:         CVE-2024-49761.patch
BuildRequires:  git
BuildRequires:  ruby
Requires:       ruby(release)
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
REXML was inspired by the Electric XML library for Java, which features an easy-to-use API, small size, and speed. Hopefully, REXML, designed with the same philosophy, has these same features. I've tried to keep the API as intuitive as possible, and have followed the Ruby methodology for method naming and code flow, rather than mirroring the Java API.
REXML supports both tree and stream document parsing. Stream parsing is faster (about 1.5 times as fast). However, with stream parsing, you don't get access to features such as XPath.

%prep
%autosetup -p1 -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%doc %{gemdir}/gems/%{gem_name}-%{version}/LICENSE.txt
%{gemdir}

%changelog
* Mon Nov 04 2024 Saul Paredes <saulparedes@microsoft.com> - 3.2.7-3
- Add patch for CVE-2024-49761

* Thu Sep 19 2024 Harshit Gupta <guptaharshit@microsoft.com> - 3.2.7-2
- Add patch for CVE-2024-41946

* Fri May 31 2024 Minghe Ren <mingheren@microsoft.com> - 3.2.7-1
- Upgrade to 3.2.7 to resolve CVE-2024-35176
- Remove CVE-2024-35176.patch as it is no longer needed

* Tue May 28 2024 Minghe Ren <mingheren@microsoft.com> - 3.2.5-2
- Add patch for CVE-2024-35176

* Mon Jun 13 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 3.2.5-1
- License verified
- Original version for CBL-Mariner
