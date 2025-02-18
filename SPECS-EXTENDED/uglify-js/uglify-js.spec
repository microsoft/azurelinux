%{?nodejs_find_provides_and_requires}

#enable/disable tests in case the deps aren't there
%bcond_with tests

Name:           uglify-js
Version:        3.19.3
Release:        1%{?dist}
Summary:        JavaScript parser, mangler/compressor and beautifier toolkit
License:        BSD-2-Clause
URL:            https://github.com/mishoo/UglifyJS
Source0:        https://registry.npmjs.org/%{name}/-/%{name}-%{version}.tgz

BuildArch:      noarch
ExclusiveArch:  %{nodejs_arches} noarch

Provides:       nodejs-uglify-js = %{version}-%{release}

Provides:       uglify-js3 = %{version}-%{release}
Obsoletes:      uglify-js3 < 3.14.5-2

Provides:       nodejs-uglify-js3 = %{version}-%{release}

BuildRequires:  nodejs
BuildRequires:  nodejs-packaging
BuildRequires:  web-assets-devel

%if %{with tests}
BuildRequires:  npm(acorn)
BuildRequires:  npm(semver)
%endif

Requires:       js-uglify = %{version}-%{release}

%description
JavaScript parser, mangler/compressor and beautifier toolkit.

This package ships the uglifyjs command-line tool and a library suitable for
use within Node.js.

%package -n js-uglify
Summary:        JavaScript parser, mangler/compressor and beautifier toolkit - core library

Provides:       js-uglify3 = %{version}-%{release}
Obsoletes:      js-uglify3 < 3.14.5-2

Provides:       uglify-js-common = %{version}-%{release}
Obsoletes:      uglify-js-common < 2.2.5-4

Requires:       web-assets-filesystem

%description -n js-uglify
JavaScript parser, mangler/compressor and beautifier toolkit.

This package ships a JavaScript library suitable for use by any JavaScript
runtime.

%prep
%autosetup -n package

chmod 0755 bin/uglifyjs

%build
#nothing to do


%install
mkdir -p %{buildroot}%{_jsdir}/%{name}-3
cp -pr lib/* %{buildroot}%{_jsdir}/%{name}-3
ln -s %{name}-3 %{buildroot}%{_jsdir}/%{name}

#compat symlink
mkdir -p %{buildroot}%{_datadir}
ln -rs %{buildroot}%{_jsdir}/%{name} %{buildroot}%{_datadir}/%{name}

mkdir -p %{buildroot}%{nodejs_sitelib}/uglify-js@3
cp -pr bin tools package.json %{buildroot}%{nodejs_sitelib}/uglify-js@3
ln -rs %{buildroot}%{_jsdir}/%{name}-3 \
       %{buildroot}%{nodejs_sitelib}/uglify-js@3/lib
# Fix for rpmlint.
sed -i -e 's|^#! */usr/bin/env node|#!/usr/bin/node|' \
  %{buildroot}%{nodejs_sitelib}/uglify-js@3/bin/uglifyjs
chmod 755 %{buildroot}%{nodejs_sitelib}/uglify-js@3/bin/uglifyjs

mkdir -p %{buildroot}%{_bindir}
ln -rs %{buildroot}%{nodejs_sitelib}/uglify-js@3/bin/uglifyjs \
       %{buildroot}%{_bindir}/uglifyjs-3
ln -s uglifyjs-3 %{buildroot}%{_bindir}/uglifyjs

%nodejs_symlink_deps

ln -s uglify-js@3 %{buildroot}%{nodejs_sitelib}/uglify-js


%check
%nodejs_symlink_deps --check
%{__nodejs} -e 'require("./")'
%if %{with tests}
# Prevent timeout error on an ARM builder which is slower than the x86 builder.
sed -i '/timeout/ s/5000/10000/' test/mocha/cli.js
sed -i '/timeout/ s/10000/20000/' test/mocha/let.js
sed -i '/timeout/ s/20000/40000/' test/mocha/spidermonkey.js
NODE_DISABLE_COLORS=true %{__nodejs} test/run-tests.js
%endif


%pretrans -p <lua>
st = posix.stat("%{nodejs_sitelib}/uglify-js")
if st and st.type == "directory" then
  os.execute("rm -rf %{nodejs_sitelib}/uglify-js")
end


%pretrans -n js-uglify -p <lua>
st = posix.stat("%{_datadir}/%{name}")
if st and st.type == "directory" then
  os.execute("rm -rf %{_datadir}/%{name}")
end


%files
%{nodejs_sitelib}/uglify-js
%{nodejs_sitelib}/uglify-js@3
%{_bindir}/uglifyjs-3
%{_bindir}/uglifyjs


%files -n js-uglify
%{_jsdir}/%{name}-3
%{_jsdir}/%{name}
%{_datadir}/%{name}
%doc README.md
%license LICENSE


%changelog
* Tue Sep 10 2024 Mattias Ellert <mattias.ellert@physics.uu.se> - 3.19.3-1
- Update to 3.19.3

* Mon Aug 12 2024 Mattias Ellert <mattias.ellert@physics.uu.se> - 3.19.2-1
- Update to 3.19.2

* Sun Aug 04 2024 Mattias Ellert <mattias.ellert@physics.uu.se> - 3.19.1-1
- Update to 3.19.1

* Thu Jul 18 2024 Mattias Ellert <mattias.ellert@physics.uu.se> - 3.19.0-1
- Update to 3.19.0

* Mon Jun 10 2024 Mattias Ellert <mattias.ellert@physics.uu.se> - 3.18.0-1
- Update to 3.18.0

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.17.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.17.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Mar 15 2023 Mattias Ellert <mattias.ellert@physics.uu.se> - 3.17.4-1
- Update to 3.17.4
- Rebuilt for updated rpm macros (Fedora 37+)

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.17.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Sep 20 2022 Mattias Ellert <mattias.ellert@physics.uu.se> - 3.17.1-1
- Update to 3.17.1

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.16.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 17 2022 Mattias Ellert <mattias.ellert@physics.uu.se> - 3.16.1-1
- Update to 3.16.1

* Wed Apr 20 2022 Mattias Ellert <mattias.ellert@physics.uu.se> - 3.15.4-1
- Update to 3.15.4

* Sun Mar 20 2022 Mattias Ellert <mattias.ellert@physics.uu.se> - 3.15.3-1
- Update to 3.15.3

* Mon Feb 28 2022 Mattias Ellert <mattias.ellert@physics.uu.se> - 3.15.2-1
- Update to 3.15.2

* Mon Feb 07 2022 Mattias Ellert <mattias.ellert@physics.uu.se> - 3.15.1-1
- Update to 3.15.1

* Wed Jan 26 2022 Mattias Ellert <mattias.ellert@physics.uu.se> - 3.15.0-1
- Update to 3.15.0

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.14.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jan 19 2022 Mattias Ellert <mattias.ellert@physics.uu.se> - 3.14.5-2
- Update uglify-js for EPEL 7 to version 3
- Provide/Obsolete uglify-js3

* Thu Dec 16 2021 Mattias Ellert <mattias.ellert@physics.uu.se> - 3.14.5-1
- Update to 3.14.5

* Wed Dec 01 2021 Mattias Ellert <mattias.ellert@physics.uu.se> - 3.14.4-1
- Update to 3.14.4

* Tue Nov 02 2021 Mattias Ellert <mattias.ellert@physics.uu.se> - 3.14.3-1
- Update to 3.14.3

* Thu Oct 14 2021 Mattias Ellert <mattias.ellert@physics.uu.se> - 3.14.2-1
- Update to 3.14.2

* Fri Aug 13 2021 Sérgio Basto <sergio@serjux.com> - 3.14.1-1
- Update to 3.14.1

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Sep 18 2020 Troy Dawson <tdawson@redhat.com> - 3.10.4-1
- Update to 3.10.4

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.22-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.22-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jan 22 2020 Jan Staněk <jstanek@redhat.com> - 2.8.22-8
- Remove unneeded legacy conditionals around %%{nodejs_arches} and %%{_jsdir}
- Disable colors in tests
- Use %%bcond_without for conditional compilation

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.22-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.22-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.22-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.22-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Aug 15 2017 Jun Aruga <jaruga@redhat.com> - 2.8.22-3
- Remove duplicate BuildArch entry: BuildArch: noarch

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jul 04 2017 Jun Aruga <jaruga@redhat.com> - 2.8.22-1
- Update to upstream 2.8.22 release

* Wed Mar 29 2017 Jun Aruga <jaruga@redhat.com> - 2.8.17-1
- Update to upstream 2.8.17 release

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Aug 01 2016 Jun Aruga <jaruga@redhat.com> - 2.7.0-2
- Update to prevent timeout error on an ARM builder. (rhbz#1361179)

* Thu Jul 28 2016 Jared Smith <jsmith@fedoraproject.org> - 2.7.0-1
- Update to upstream 2.7.0 release

* Sat Jul 09 2016 Jared Smith <jsmith@fedoraproject.org> - 2.6.4-1
- Update to upstream 2.6.4 release

* Wed Feb 10 2016 Tom Hughes <tom@compton.nu> - 2.6.1-1
- Update to 2.6.1 upstream release

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.13-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Nov 21 2015 Tom Hughes <tom@compton.nu> - 2.4.13-8
- update async dependency

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.13-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.13-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 08 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 2.4.13-5
- add logic for building on EL6

* Tue Apr 29 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 2.4.13-4
- pretrans script should actually be split in two, so one half should run in
  uglify-js and the other half should run in js-uglify (#1092184)

* Tue Apr 01 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 2.4.13-3
- pretrans script should run in js-uglify subpackage (#1082946)

* Sat Mar 15 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 2.4.13-2
- add logic for building on EPEL 6 as web-assets-{devel,filesystem} are not
  yet available

* Thu Mar 13 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 2.4.13-1
- update to upstream release 2.4.13

* Mon Jan 20 2014 T.C. Hollingsworth <tchollingsworth@gmail.com> - 2.2.5-4
- port to new JS guidelines
- provide the nodejs- form

* Sun Jan 19 2014 Tom Hughes <tom@compton.nu> - 2.2.5-3
- use new multi-version packaging rules
- update to latest nodejs packaging standards

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Apr 16 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 2.2.5-1
- new upstream release 2.2.5

* Tue Apr 16 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 2.2.4-3
- call nodejs_symlink_deps
- fix optimist dep for 0.4.0

* Wed Feb 13 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 2.2.4-2
- install tools dir
- enable tests

* Wed Feb 13 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 2.2.4-1
- new upstream release 2.2.4

* Fri Feb 01 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 2.2.3-6
- rearrange symlinks so dep generator works

* Fri Feb 01 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 2.2.3-5
- really fix install section
- conditionalize tests

* Thu Jan 31 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 2.2.3-4
- fix install section

* Thu Jan 31 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 2.2.3-3
- split off -common subpackage for use with other runtimes

* Fri Jan 18 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 2.2.3-2
- BuildRequire deps so tests work

* Tue Jan 08 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 2.2.3-1
- initial package generated by npm2rpm
