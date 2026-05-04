# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Generated from minitest-mock-5.27.0.gem by gem2rpm -*- rpm-spec -*-
%global	gem_name	minitest-mock

Name:		rubygem-%{gem_name}
Version:	5.27.0
Release: 3%{?dist}

Summary:	minitest/mock, by Steven Baker, is a beautifully tiny mock (and stub) object framework
# From README.rdoc
# SPDX confirmed
License:	MIT
URL:		https://minite.st/

Source0:	https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires:	ruby(release)
BuildRequires:	rubygems-devel
BuildRequires:	rubygem(minitest)
BuildArch:	noarch

%description
minitest/mock, by Steven Baker, is a beautifully tiny mock (and stub)
object framework.
The minitest-mock gem is an extraction of minitest/mock.rb from
minitest in order to make it easier to maintain independent of
minitest.


%package	doc
Summary:	Documentation for %{name}
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description	doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version}

%build
gem build ../%{gem_name}-%{version}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
	%{buildroot}%{gem_dir}/

rm -f %{buildroot}%{gem_cache}
pushd %{buildroot}%{gem_instdir}
rm -rf \
	Manifest.txt \
	Rakefile \
	test/ \
	%{nil}
popd

%check
pushd .%{gem_instdir}
export RUBYLIB=$(pwd)/lib:$(pwd)/test

# TODO
# test/minitest/test_minitest_mock.rb:670
# this test needs minitest 6
sed -i test/minitest/test_minitest_mock.rb \
	-e '\@assertion_count@s|assert_equal|#assert_equal|'
ruby -e \
	'Dir.glob "./test/minitest/test_*.rb", &method(:require)'
popd

%files
%dir	%{gem_instdir}
%license	%{gem_instdir}/README.rdoc
%{gem_libdir}
%{gem_spec}

%files doc
%doc	%{gem_docdir}
%doc	%{gem_instdir}/History.rdoc
%doc %{gem_instdir}/README.rdoc

%changelog
* Tue Dec 23 2025 Mamoru TASAKA <mtasaka@fedoraproject.org> - 5.27.0-2
- Remove unneeded BR: rubygem(hoe)

* Mon Dec 22 2025 Mamoru TASAKA <mtasaka@fedoraproject.org> - 5.27.0-1
- Initial package
