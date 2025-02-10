%global	gem_name	racc

Name:		rubygem-%{gem_name}
Version:	1.8.1
Release:	1%{?dist}
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Summary:	LALR(1) parser generator
# SPDX confirmed
License:	BSD-2-Clause
URL:		https://github.com/tenderlove/racc

Source0:	https://rubygems.org/gems/%{gem_name}-%{version}.gem
Source10:	rubygem-%{gem_name}-%{version}-missing-files.tar.gz
# Source10 is created by %%{SOURCE11} %%version
Source11:	racc-create-tarball-missing-files.sh

BuildRequires:	gcc
BuildRequires:	rubygems-devel
BuildRequires:	ruby-devel
BuildRequires:	rubygem(test-unit)
BuildRequires:	rubygem(test-unit-ruby-core)

%description
Racc is a LALR(1) parser generator.
It is written in Ruby itself, and generates Ruby program.


%package	doc
Summary:	Documentation for %{name}
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description	doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version} -a 10

mv ../%{gem_name}-%{version}.gemspec .

# Fix shebang
grep -rl /usr/local . | xargs -r sed -i -e 's|/usr/local|/usr|'

%build
gem build %{gem_name}-%{version}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{_prefix}
cp -a .%{_prefix}/* \
	%{buildroot}%{_prefix}/

cp -a ./%{gem_name}-%{version}/sample \
	%{buildroot}%{gem_instdir}

mkdir -p %{buildroot}%{gem_extdir_mri}
cp -a ./usr/lib/ruby/gems/3.3.0/extensions/x86_64-linux/3.3.0/racc-1.8.1/* \
	%{buildroot}%{gem_extdir_mri}/
rm -f %{buildroot}%{gem_extdir_mri}/{gem_make.out,mkmf.log}

rm -f %{buildroot}%{gem_cache}
pushd %{buildroot}%{gem_instdir}
rm -rf \
	ext/ \
	fastcache/ \
	misc/ \
	tasks/ \
	test/ \
	DEPENDS \
	Manifest.txt \
	Rakefile \
	setup.rb \
	%{nil}

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

%check
cp -a %{gem_name}-%{version}/* .%{gem_instdir}
pushd .%{gem_instdir}

LANG=C.utf8
export RUBYLIB=$(pwd)/lib:$(pwd)/test:$(pwd)/test/lib
ruby -Ilib:test:test/lib:. -e \
	"gem 'test-unit' ; require 'helper' ; Dir.glob('test/test_*.rb').each {|f| require f}"
popd

%files
%dir	%{gem_instdir}

%license	%{gem_instdir}/BSDL
%license	%{gem_instdir}/COPYING
%doc	%lang(ja)	%{gem_instdir}/README.ja.rdoc
%doc	%{gem_instdir}/README.rdoc
%doc	%{gem_instdir}/ChangeLog

%{_bindir}/racc

%{gem_extdir_mri}
%{gem_instdir}/bin
%{gem_libdir}
/usr/lib/ruby/gems/3.3.0/extensions/x86_64-linux/3.3.0/racc-1.8.1/gem.build_complete
/usr/lib/ruby/gems/3.3.0/extensions/x86_64-linux/3.3.0/racc-1.8.1/gem_make.out
/usr/lib/ruby/gems/3.3.0/extensions/x86_64-linux/3.3.0/racc-1.8.1/racc/cparse.so
%{gem_spec}

%files	doc
%doc	%{gem_docdir}
%doc	%{gem_instdir}/TODO
%doc	%{gem_instdir}/doc
%doc	%{gem_instdir}/sample

%changelog
* Fri Dec 06 2024 Sumit Jena <v-sumitjena@microsoft.com> - 1.8.1-1
- Initial CBL-Mariner import from Fedora 41.
- License verified

* Wed Jul 31 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.8.1-100
- 1.8.1

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-101
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue May 21 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.8.0-100
- 1.8.0

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.3-202
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 03 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.7.3-201
- Rebuild for https://fedoraproject.org/wiki/Changes/Ruby_3.3

* Sun Nov 12 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.7.3-200
- 1.7.3

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-201
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 18 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.7.1-200
- 1.7.1

* Thu Jun  8 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.7.0-200
- 1.7.0

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2-202
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jan 03 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.6.2-201
- Rebuild for https://fedoraproject.org/wiki/Changes/Ruby_3.2

* Fri Dec 23 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.6.2-200
- 1.6.2

* Mon Dec  5 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.6.1-200
- 1.6.1

* Mon Sep 26 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.6.0-205
- Pull upstream #191 PR for Regexp.compile argument mistake

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-204
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 26 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.6.0-203
- F-36: rebuild against ruby31

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-201
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Oct 19 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.6.0-200
- 1.6.0

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-202
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-201
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan  6 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.5.2-200
- 1.5.2

* Tue Nov 17 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.5.1-200
- 1.5.1

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-201
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Apr 21 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.5.0-200
- 1.5.0
- racc2y, y2racc removed

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.16-201
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 17 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.4.16-200
- F-32: rebuild against ruby27

* Mon Dec 30 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.4.16-1
- 1.4.16

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Mar  6 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.4.15-1
- 1.4.15

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.14-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 21 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.4.14-11
- F-30: rebuild against ruby26

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.14-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.14-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 1.4.14-8
- Rebuilt for switch to libxcrypt

* Thu Jan 04 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.4.14-7
- F-28: rebuild for ruby25

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.14-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.14-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 11 2017 Vít Ondruch <vondruch@redhat.com> - 1.4.14-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.4

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Dec  6 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.4.14-1
- 1.4.14

* Tue Nov 03 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.4.13-1
- Initial package
