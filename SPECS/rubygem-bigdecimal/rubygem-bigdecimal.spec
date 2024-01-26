%global debug_package %{nil}
%global gem_name bigdecimal
Summary:        BigDecimal provides arbitrary-precision floating point decimal arithmetic
Name:           rubygem-%{gem_name}
Version:        3.1.6
Release:        3%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/ruby/%{gem_name}
Source0:        https://github.com/ruby/%{gem_name}/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
BuildRequires:  git
BuildRequires:  ruby
Requires:       ruby(release)
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
Ruby provides built-in support for arbitrary precision integer arithmetic.
For example:

42**13 -> 1265437718438866624512

BigDecimal provides similar support for very large or very accurate floating
point numbers. Decimal arithmetic is also useful for general calculation,
because it provides the correct answers people expect–whereas normal binary
floating point arithmetic often introduces subtle errors because of the
conversion between base 10 and base 2.

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
* Tue May 31 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 3.1.2-3
- Cleanup

* Wed Apr 20 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 3.1.2-2
- Add provides

* Fri Apr 15 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 3.1.2-1
- License verified
- Included descriptions from Fedora 36 spec (license: MIT).
- Original version for CBL-Mariner
