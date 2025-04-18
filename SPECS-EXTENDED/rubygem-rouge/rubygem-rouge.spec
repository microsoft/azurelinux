%global gem_name rouge

Name:           rubygem-%{gem_name}
Version:        4.4.0
Release:        2%{?dist}
Summary:        Pure-ruby colorizer based on pygments
# From LICENSE file
# SPDX confirmed
License:        MIT AND BSD-2-Clause
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            http://rouge.jneen.net/
Source0:        https://github.com/rouge-ruby/rouge/archive/refs/tags/v4.4.0.tar.gz#/%{name}-%{version}.tar.gz

Source10:       spec_helper_assert.rb
Source11:       bundler.rb
BuildRequires:  ruby(release)
BuildRequires:  rubygems-devel
BuildRequires:  help2man
BuildRequires:  rubygem(minitest)
BuildRequires:  rubygem(rake)

BuildArch:      noarch

%description
Rouge aims to a be a simple, easy-to-extend drop-in replacement for pygments.

%package        doc
Summary:        Documentation for %{name}
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description    doc
Documentation for %{name}.

%prep
%autosetup -n %{gem_name}-%{version}

cp -a spec ..
mkdir FAKE
cp -a %{SOURCE11} FAKE/
cp -pa %{SOURCE10} spec/

%build
gem build %{gem_name}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{_bindir}
cp -pa .%{_bindir}/* %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

# Generate man page from "rougify --help" output
export GEM_PATH="%{buildroot}%{gem_dir}:%{gem_dir}"

mkdir -p %{buildroot}%{_mandir}/man1
help2man -N -s1 -o %{buildroot}%{_mandir}/man1/rougify.1 \
    %{buildroot}%{_bindir}/rougify

rm -f %{buildroot}%{gem_cache}
pushd %{buildroot}%{gem_instdir}
rm -rf \
    Gemfile \
    %{gem_name}.gemspec \
    %{nil}
popd

%check
find spec -name \*_spec.rb -print0 | \
	sort --zero-terminated |  \
	xargs --null ruby -Ilib:FAKE \
	-r./spec/spec_helper \
	-r./spec/spec_helper_assert \
	-r rake/rake_test_loader  \
	%{nil}

%files
%dir %{gem_instdir}
%license %{gem_instdir}/LICENSE
%{gem_libdir}
%exclude %{gem_libdir}/%{gem_name}/demos
%{_bindir}/rougify
%{gem_instdir}/bin
%{_mandir}/man1/rougify.1*
%{gem_spec}

%files doc
%doc %{gem_docdir}
%{gem_libdir}/%{gem_name}/demos

%changelog
* Tue Dec 24 2024 Akhila Guruju <v-guakhila@microsoft.com> - 4.4.0-2
- Initial Azure Linux import from Fedora 41 (license: MIT).
- Build with .tar.gz
- License verified.

* Fri Sep 20 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4.4.0-1
- 4.4.0

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jun 18 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4.3.0-1
- 4.3.0

* Mon Mar 18 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4.2.1-1
- 4.2.1

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Oct 25 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4.2.0-1
- 4.2.0

* Fri Aug 18 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4.1.3-1
- 4.1.3

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Feb 17 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4.1.0-1
- 4.1.0

* Sun Feb 12 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4.0.1-3
- Execute spec test provided by the upstream
- Backport upstream patch for ruby32 regex issue with hash character

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Dec 21 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4.0.1-1
- 4.0.1

* Sun Oct  9 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4.0.0-2
- 4.0.0

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.26.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.26.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sun Sep 19 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.26.1-1
- 3.26.1

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.26.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.26.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Dec 11 2020 Fabio Valentini <decathorpe@gmail.com> - 3.26.0-1
- Update to version 3.26.0.

* Wed Nov 18 2020 Fabio Valentini <decathorpe@gmail.com> - 3.25.0-1
- Update to version 3.25.0.

* Fri Oct 16 2020 Fabio Valentini <decathorpe@gmail.com> - 3.24.0-1
- Update to version 3.24.0.

* Wed Sep 09 2020 Fabio Valentini <decathorpe@gmail.com> - 3.23.0-1
- Update to version 3.23.0.

* Wed Aug 12 2020 Fabio Valentini <decathorpe@gmail.com> - 3.22.0-1
- Update to version 3.22.0.

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.21.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 15 2020 Fabio Valentini <decathorpe@gmail.com> - 3.21.0-1
- Update to version 3.21.0.

* Fri Jun 12 2020 Fabio Valentini <decathorpe@gmail.com> - 3.20.0-1
- Update to version 3.20.0.

* Fri May 15 2020 Fabio Valentini <decathorpe@gmail.com> - 3.19.0-1
- Update to version 3.19.0.

* Sat Apr 18 2020 Fabio Valentini <decathorpe@gmail.com> - 3.18.0-1
- Update to version 3.18.0.

* Wed Mar 11 2020 Fabio Valentini <decathorpe@gmail.com> - 3.17.0-1
- Update to version 3.17.0.

* Sat Feb 15 2020 Fabio Valentini <decathorpe@gmail.com> - 3.16.0-1
- Update to version 3.16.0.

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.15.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 17 2020 Fabio Valentini <decathorpe@gmail.com> - 3.15.0-1
- Update to version 3.15.0.

* Thu Dec 19 2019 Fabio Valentini <decathorpe@gmail.com> - 3.14.0-1
- Update to version 3.14.0.

* Sat Nov 16 2019 Fabio Valentini <decathorpe@gmail.com> - 3.13.0-1
- Update to version 3.13.0.

* Wed Oct 30 2019 Fabio Valentini <decathorpe@gmail.com> - 3.12.0-1
- Update to version 3.12.0.

* Mon Oct 07 2019 Fabio Valentini <decathorpe@gmail.com> - 3.11.1-1
- Update to version 3.11.1.

* Sat Sep 28 2019 Fabio Valentini <decathorpe@gmail.com> - 3.11.0-1
- Update to version 3.11.0.

* Wed Sep 04 2019 Fabio Valentini <decathorpe@gmail.com> - 3.10.0-1
- Update to version 3.10.0.

* Thu Aug 15 2019 Fabio Valentini <decathorpe@gmail.com> - 3.8.0-1
- Update to version 3.8.0.

* Tue Jul 30 2019 Fabio Valentini <decathorpe@gmail.com> - 3.7.0-1
- Update to version 3.7.0.

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 10 2019 Fabio Valentini <decathorpe@gmail.com> - 3.6.0-1
- Update to version 3.6.0.

* Tue Jul 02 2019 Fabio Valentini <decathorpe@gmail.com> - 3.5.1-1
- Update to version 3.5.1.

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Oct 02 2018 Fabio Valentini <decathorpe@gmail.com> - 3.3.0-1
- Update to version 3.3.0.

* Fri Aug 17 2018 Fabio Valentini <decathorpe@gmail.com> - 3.2.1-1
- Update to version 3.2.1.

* Thu Aug 02 2018 Fabio Valentini <decathorpe@gmail.com> - 3.2.0-1
- Update to version 3.2.0.

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 04 2018 Fabio Valentini <decathorpe@gmail.com> - 3.1.1-1
- Update to version 3.1.1.

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Aug 23 2016 Björn Esser <fedora@besser82.io> - 1.11.1-1
- initial import (#1368850)

* Sun Aug 21 2016 Björn Esser <fedora@besser82.io> - 1.11.1-0.1
- initial rpm-release (#1368850)

