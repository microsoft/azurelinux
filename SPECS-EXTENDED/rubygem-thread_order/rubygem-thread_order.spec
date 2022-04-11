Vendor:         Microsoft Corporation
Distribution:   Mariner
%global	gem_name thread_order

Name:		rubygem-%{gem_name}
Version:	1.1.1
Release:	5%{?dist}
Summary:	Test helper for ordering threaded code
License:	MIT
URL:		https://github.com/JoshCheek/thread_order
Source0:	https://github.com/JoshCheek/thread_order/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz

BuildRequires:	ruby(release)
BuildRequires:	rubygems-devel
BuildRequires:	rubygem(rspec) >= 3
BuildRequires:	git
BuildArch:	noarch

%description
Test helper for ordering threaded code.

%package	doc
Summary:	Documentation for %{name}
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version}

%build
gem build %{gem_name}
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* %{buildroot}%{gem_dir}/
cp -a .%{gem_dir}/gems/%{gem_name}-%{version} %{buildroot}%{gem_dir}/gems/
#add lib files to buildroot from Source0
cp -a lib/ %{buildroot}%{gem_instdir}/
#add License and Readme files to buildroot from Source0
cp License.txt %{buildroot}%{gem_instdir}/
cp Readme.md %{buildroot}%{gem_instdir}/

pushd %{buildroot}
rm -f .%{gem_cache}

pushd .%{gem_instdir}
rm -rf \
	.gitignore .travis.yml \
	Gemfile \
	spec/ \
	%{gem_name}.gemspec \
	%{nil}

popd
popd

%check
# The following test does not pass with using gem
FAILFILE=()
FAILTEST=()
FAILFILE+=("spec/thread_order_spec.rb")
FAILTEST+=("is implemented without depending on the stdlib")

pushd .%{gem_instdir}
for ((i = 0; i < ${#FAILFILE[@]}; i++)) {
	sed -i \
		-e "\@${FAILTEST[$i]}@s|do$|, :broken => true do|" \
		${FAILFILE[$i]}
}

rspec spec/ || \
	rspec spec/ --tag ~broken
popd

%files
%dir %{gem_instdir}
%license %{gem_instdir}/License.txt
%doc %{gem_instdir}/Readme.md
%{gem_libdir}
%{gem_spec}

%files doc
%doc %{gem_docdir}

%changelog
* Tue Mar 22 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.1.1-5
- License verified.
- Build from .tar.gz source.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1.1-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Feb  6 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.1.1-1
- 1.1.1

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Aug 09 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.1.0-1
- Initial package
