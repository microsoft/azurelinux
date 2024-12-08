%global gem_name scanf

Name: rubygem-%{gem_name}
Version: 1.0.0
Release: 1%{?dist}
Summary: A Ruby implementation of the C function scanf(3)
# Automatically converted from old format: BSD - review is highly recommended.
License: LicenseRef-Callaway-BSD
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL: https://github.com/ruby/scanf
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# License is not included in the gem, copied from git
Source1: LICENSE.txt
# Tests are not included in the gem, copied from git
Source2: data.txt
Source3: test_scanf.rb
Source4: test_scanfblocks.rb
Source5: test_scanfio.rb
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby >= 2.3.0
# Required for %check
BuildRequires: rubygem(test-unit)
BuildArch: noarch

%description
A Ruby implementation of the C function scanf(3).


%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version}
cp %{SOURCE1} LICENSE.txt

%build
# Create the gem as gem install only works on a gem file
gem build ../%{gem_name}-%{version}.gemspec

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/



%check
ruby -I.%{gem_instdir}/lib %{SOURCE3} %{SOURCE4} %{SOURCE5}

%files
%license LICENSE.txt
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}


%changelog
* Fri Dec 06 2024 Sumit Jena <v-sumitjena@microsoft.com> - 1.0.0-1
- Initial CBL-Mariner import from Fedora 41.
- License verified
