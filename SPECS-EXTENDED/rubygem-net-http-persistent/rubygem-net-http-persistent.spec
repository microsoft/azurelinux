Vendor:         Microsoft Corporation
Distribution:   Mariner
%global	gem_name	net-http-persistent

Summary:	Persistent connections using Net::HTTP plus a speed fix
Name:		rubygem-%{gem_name}
Version:	2.9.4
Release:	15%{?dist}
License:	MIT

URL:		https://github.com/drbrain/net-http-persistent
Source0:	https://rubygems.org/downloads/%{gem_name}-%{version}.gem
Patch0:		rubygem-net-http-persistent-2.1-no-net-test.patch

Requires:	ruby(release)
BuildRequires:	ruby(release)
BuildRequires:	rubygems-devel
BuildRequires:	rubygem(minitest)

Requires:	rubygems
BuildArch:	noarch

Provides:	rubygem(%{gem_name}) = %{version}

%description
Persistent connections using Net::HTTP plus a speed fix for 1.8.  It's
thread-safe too.

%package	doc
Summary:	Documentation for %{name}
Requires:	%{name} = %{version}-%{release}

%description    doc
This package contains documentation for %{name}.


%prep
%setup -q -c -T

TOPDIR=$(pwd)
mkdir tmpunpackdir
pushd tmpunpackdir

gem unpack %{SOURCE0}
cd %{gem_name}-%{version}




%patch0 -p1

# Don't use SSLv3
sed -i test/test_net_http_persistent_ssl_reuse.rb \
	-e 's|SSLv3|TLSv1_2|'

gem specification -l --ruby %{SOURCE0} > %{gem_name}.gemspec
gem build %{gem_name}.gemspec
mv %{gem_name}-%{version}.gem $TOPDIR

popd
rm -rf tmpunpackdir

%build
%gem_install

#chmod 0644 ./%{gem_dir}/cache/%{gem_name}-%{version}.gem

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
	%{buildroot}/%{gem_dir}/
rm -f %{buildroot}%{gem_instdir}/{.autotest,.gemtest}

%check
pushd .%{gem_instdir}
# testrb -Ilib test
# Skip one test
sed -i test/test_net_http_persistent_ssl_reuse.rb \
	-e '\@def test_ssl_connection_reuse@s|^\(.*\)$|\1 ; skip "ignore for now"|'

ruby -Ilib:. -e 'Dir.glob("test/test_*.rb").each{|f| require f}'
popd

%files
%license README.rdoc
%dir	%{gem_instdir}
%doc	%{gem_instdir}/[A-Z]*
%exclude	%{gem_instdir}/Rakefile
%{gem_instdir}/lib/
%exclude	%{gem_cache}
%{gem_spec}

%files	doc
%exclude	%{gem_instdir}/Rakefile
%exclude	%{gem_instdir}/test/
%{gem_docdir}/

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.9.4-15
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.4-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon May 14 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.9.4-10
- Ignore test_ssl_connection_reuse for now

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jun 30 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.9.4-5
- Don't use SSLv3 for test

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 12 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.9.4-3
- Use minitest 5 correctly for F-21+

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Feb 22 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.9.4-1
- 2.9.4

* Mon Feb 10 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.9.3-1
- 2.9.3

* Mon Jan 27 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.9.1-1
- 2.9.1

* Wed Aug  7 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.9-1
- 2.9

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 21 2013 Vít Ondruch <vondruch@redhat.com> - 2.8-4
- Fix EL compatibility.
- Test are passing now.
- Cleanup.

* Thu Feb 28 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.8-3
- F-19: Rebuild for ruby 2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan  2 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.8-1
- Update to 2.8

* Mon Nov 26 2012 Vít Ondruch <vondruch@redhat.com> - 2.1-6
- Add EL compatibility macros.
- Drop rubygem({hoe,rake}) build dependencies.

* Thu Aug  2 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.1-5
- Rescue test failure for now

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Feb  5 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.1-3
- F-17: rebuild against ruby19

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Oct  9 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.1-1
- 2.1

* Sun Aug 28 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.0-1
- 2.0

* Sun Aug 14 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.8.1-1
- 1.8.1

* Mon Jul  4 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.8-1
- 1.8

* Sun Apr 24 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.7-1
- 1.7

* Thu Mar 10 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.6.1-1
- 1.6.1

* Thu Mar  3 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.6-1
- 1.6

* Sat Feb 26 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.5.2-1
- 1.5.2
- Patch0 merged

* Sat Feb 12 2011 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.5.1-1
- 1.5.1

* Thu Feb 10 2011 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.5-3
- Rescue the case where socket is Nil, for mechanize testsuite

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 27 2011 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.5-1
- 1.5

* Sun Jan 16 2011 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.4.1-1
- Initial package
