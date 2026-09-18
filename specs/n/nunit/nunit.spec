# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global debug_package %{nil}

Name:           nunit
Version:        3.7.1
Release:        22%{?dist}
Summary:        Unit test framework for CLI
# Automatically converted from old format: MIT with advertising - review is highly recommended.
License:        LicenseRef-Callaway-MIT-with-advertising
Url:            http://www.nunit.org/
Source0:        https://github.com/nunit/nunit/archive/%{version}.tar.gz
Source1:        nunit.pc
Source2:        nunitlite-runner.sh
BuildRequires:  mono-devel
ExclusiveArch:  %{mono_arches}
Provides:       mono-nunit = 4.0.2-5
Obsoletes:      mono-nunit < 4.0.2-6
Obsoletes:      nunit-runner <= 2.6.4-10

%description
NUnit is a unit testing framework for all .NET languages. It serves the
same purpose as JUnit does in the Java world. It supports test
categories, testing for exceptions and writing test results in plain
text or XML.

NUnit targets the CLI (Common Language Infrastructure) and supports Mono and
the Microsoft .NET Framework.

%package        devel
Summary:        Development files for NUnit
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig
Provides:       mono-nunit-devel = 4.0.2-5
Obsoletes:      mono-nunit-devel < 4.0.2-6

%description devel
Development files for %{name}.

%prep
%setup -qn nunit-%{version}

%build

# Remove prebuilt binaries
find . -name "*.dll" -print -delete

%{?exp_env}
%{?env_options}

xbuild /property:Configuration=Release src/NUnitFramework/framework/nunit.framework-4.5.csproj
xbuild /property:Configuration=Release src/NUnitFramework/nunitlite/nunitlite-4.5.csproj
xbuild /property:Configuration=Release src/NUnitFramework/nunitlite-runner/nunitlite-runner-4.5.csproj
xbuild /property:Configuration=Release src/NUnitFramework/mock-assembly/mock-assembly-4.5.csproj

xbuild /property:Configuration=Release src/NUnitFramework/slow-tests/slow-nunit-tests-4.5.csproj
xbuild /property:Configuration=Release src/NUnitFramework/testdata/nunit.testdata-4.5.csproj
xbuild /property:Configuration=Release src/NUnitFramework/tests/nunit.framework.tests-4.5.csproj
xbuild /property:Configuration=Release src/NUnitFramework/nunitlite.tests/nunitlite.tests-4.5.csproj

%install
%{?env_options}
%{__mkdir_p} %{buildroot}%{_monodir}/nunit
%{__mkdir_p} %{buildroot}%{_libdir}/pkgconfig
%{__mkdir_p} %{buildroot}%{_bindir}
%{__mkdir_p} %{buildroot}%{_datadir}/applications
%{__mkdir_p} %{buildroot}%{_datadir}/icons/NUnit
%{__install} -m0644 %{SOURCE1} %{buildroot}%{_libdir}/pkgconfig/
%{__install} -m0755 %{SOURCE2} %{buildroot}%{_bindir}/nunitlite-runner
%{__install} -m0644 src/NUnitFramework/nunitlite-runner/App.config %{buildroot}%{_monodir}/nunit/nunitlite-runner.exe.config
find %{_builddir}/%{?buildsubdir}/bin -name \*.dll -exec %{__install} \-m0755 "{}" "%{buildroot}%{_monodir}/nunit/" \;
find %{_builddir}/%{?buildsubdir}/bin -name \*.exe -exec %{__install} \-m0755 "{}" "%{buildroot}%{_monodir}/nunit/" \;
for i in nunit.framework.dll nunit.framework.tests.dll nunitlite.dll nunit.testdata.dll; do
    gacutil -i %{buildroot}%{_monodir}/nunit/$i -package nunit -root %{buildroot}%{_monodir}/../
done

%files
%license LICENSE.txt
%{_bindir}/nunitlite-runner
%{_monogacdir}/nunit*
%{_monodir}/nunit/

%files devel
%{_libdir}/pkgconfig/nunit.pc

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.1-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Sep 02 2024 Miroslav Suchý <msuchy@redhat.com> - 3.7.1-20
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Aug 27 2017 Ville Skyttä <ville.skytta@iki.fi> - 3.7.1-3
- Own the %%{_monodir}/nunit dir

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 26 2017 Timotheus Pokorra <tp@tbits.net> - 3.7.1-1
- Update to 3.7.1

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 13 2017 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> - 3.6-1
- Update to 3.6

* Thu Oct 13 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5-3
- mono rebuild for aarch64 support

* Thu Oct 13 2016 Peter Robinson <pbrobinson@fedoraproject.org> - 3.5-2
- aarch64 bootstrap

* Wed Oct 05 2016 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> - 3.5-1
- Update to 3.5
- Move from nunit3-console to nunitlite-runner

* Fri Sep 02 2016 Timotheus Pokorra <timotheus.pokorra@solidcharity.com> - 3.4.1-2
- fix obsoletes nunit-runner

* Wed Jul 20 2016 Timotheus Pokorra <timotheus.pokorra@solidcharity.com> - 3.4.1-1
- upgrade to 3.4.1. nunit-gui will be in separate package (#1360389)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> - 2.6.4-11
- Replace nunit-runner with nunit-gui with only desktop frontend

* Sun Nov 01 2015 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> - 2.6.4-10
- Split runner tool in subpackage

* Tue Aug 04 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com> - 2.6.4-9
- obsoleting mono-nunit and mono-nunit-devel (bug 1247825)

* Fri Jul 17 2015 Dan Horák <dan[at]danny.cz> - 2.6.4-8
- set ExclusiveArch

* Mon Jul 13 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com> - 2.6.4-7
- require desktop-file-utils for building and make sure we own the icons/NUnit directory

* Mon Jul 13 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com> - 2.6.4-5
- fix Requires for devel package, and fixing other issues

* Mon Jul 13 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com> - 2.6.4-2
- include a desktop file and install the icon

* Mon Jun 22 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com> - 2.6.4-1
- upgrade to 2.6.4
- fix the license
- fix some rpmlint warnings and errors

* Thu Jun 04 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com> - 2.6.3-6
- do not replace mono-nunit. fix some rpmlint warnings and errors

* Wed Jun 03 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com> - 2.6.3-5
- Use mono macros
- Require isa in devel subpackage
- Use global insted define

* Tue May 19 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com> - 2.6.3-4
- this package replaces mono-nunit

* Mon May 04 2015 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> - 2.6.3-3
- Move to 2.6 folder for compat with other versions
- Use real source file

* Tue Apr 21 2015 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> - 2.6.3-2
- Split nunit.pc into devel package
- Use upstream zip source
- Add ExclusiveArch

* Thu Apr 16 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com> - 2.6.3-1
- build with Mono4

* Thu Apr 16 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com> - 2.6.3-0
- copy from Xamarin NUnit spec
