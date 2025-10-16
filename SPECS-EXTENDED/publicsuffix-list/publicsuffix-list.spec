
%bcond_without  dafsa

Name:           publicsuffix-list
Version:        20250116
Release:        2%{?dist}
Summary:        Cross-vendor public domain suffix database

License:        MPL-2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://publicsuffix.org/
Source0:        https://publicsuffix.org/list/public_suffix_list.dat
Source1:        https://www.mozilla.org/media/MPL/2.0/index.txt
Source2:        https://github.com/publicsuffix/list/raw/main/tests/test_psl.txt

BuildArch:      noarch

%if %{with dafsa}
BuildRequires:  psl-make-dafsa
%endif

%description
The Public Suffix List is a cross-vendor initiative to provide
an accurate list of domain name suffixes, maintained by the hard work 
of Mozilla volunteers and by submissions from registries.
Software using the Public Suffix List will be able to determine where 
cookies may and may not be set, protecting the user from being 
tracked across sites.

%if %{with dafsa}
%package dafsa
Summary:        Cross-vendor public domain suffix database in DAFSA form

%description dafsa
The Public Suffix List is a cross-vendor initiative to provide
an accurate list of domain name suffixes, maintained by the hard work 
of Mozilla volunteers and by submissions from registries.
Software using the Public Suffix List will be able to determine where 
cookies may and may not be set, protecting the user from being 
tracked across sites.

This package includes a DAFSA representation of the Public Suffix List
for runtime loading.
%endif

%prep
%setup -c -T
cp -av %{SOURCE0} .
install -m 644 -p -v %{SOURCE1} COPYING

%build
%if %{with dafsa}
LC_CTYPE=C.UTF-8 \
psl-make-dafsa --output-format=binary \
  public_suffix_list.dat public_suffix_list.dafsa
%endif


%install
%if %{with dafsa}
install -m 644 -p -D public_suffix_list.dafsa $RPM_BUILD_ROOT/%{_datadir}/publicsuffix/public_suffix_list.dafsa
%endif
install -m 644 -p -D %{SOURCE0} $RPM_BUILD_ROOT/%{_datadir}/publicsuffix/public_suffix_list.dat
install -m 644 -p -D %{SOURCE2} $RPM_BUILD_ROOT/%{_datadir}/publicsuffix/test_psl.txt
ln -s public_suffix_list.dat $RPM_BUILD_ROOT/%{_datadir}/publicsuffix/effective_tld_names.dat

%files
%license COPYING
%dir %{_datadir}/publicsuffix
%{_datadir}/publicsuffix/effective_tld_names.dat
%{_datadir}/publicsuffix/public_suffix_list.dat
%{_datadir}/publicsuffix/test_psl.txt

%if %{with dafsa}
%files dafsa
%license COPYING
%dir %{_datadir}/publicsuffix
%{_datadir}/publicsuffix/public_suffix_list.dafsa
%endif

%changelog
* Tue Mar 11 2025 Akhila Guruju <v-guakhila@microsoft.com> - 20250116-2
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified

* Mon Jan 20 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 20250116-1
- Update list to 20250116

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 20240107-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20240107-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20240107-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20240107-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 14 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 20240107-1
- Update list to 20240107

* Tue Aug 15 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 20230812-1
- Update list to 20230812

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 20230614-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jun 16 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 20230614-1
- Update list to 20230614

* Tue Mar 28 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 20230318-1
- Update list to 20230318

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 20221208-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Dec 12 2022 Yaakov Selkowitz <yselkowi@redhat.com> - 20221208-1
- Update list to 20221208

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 20210518-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 20210518-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Nov 16 2021 Kamil Dudka <kdudka@redhat.com> - 20210518-3
- unset writable-by-group permission bit on the license file

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20210518-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue May 18 2021 Kamil Dudka <kdudka@redhat.com> - 20210518-1
- Recent revision - 20210518

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20190417-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20190417-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20190417-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20190417-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Apr 17 2019 Kamil Dudka <kdudka@redhat.com> - 20190417-1
- Recent revision - 20190417

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20190128-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 28 2019 Yanko Kaneti <yaneti@declera.com> - 20190128-1
- Recent revision - 20190128

* Mon Jul 23 2018 Kamil Dudka <kdudka@redhat.com> - 20180723-1
- Recent revision - 20180723

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20180514-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue May 22 2018 Yaakov Selkowitz <yselkowi@redhat.com> - 20180514-1
- Recent revision - 20180514

* Wed May 02 2018 Yaakov Selkowitz <yselkowi@redhat.com> - 20180419-1
- Recent revision - 20180419

* Thu Mar 29 2018 Yaakov Selkowitz <yselkowi@redhat.com> - 20180328-1
- Recent revision - 20180328

* Tue Feb 27 2018 Yaakov Selkowitz <yselkowi@redhat.com> - 20180223-1
- Recent revision - 20180223

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20171228-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan  5 2018 Yaakov Selkowitz <yselkowi@redhat.com> - 20171228-1
- Recent revision - 20171228

* Tue Nov 14 2017 Yaakov Selkowitz <yselkowi@redhat.com> - 20171028-1
- Recent revision - 20171028

* Mon Sep  4 2017 Yaakov Selkowitz <yselkowi@redhat.com> - 20170828-1
- Recent revision - 20170828

* Fri Aug 11 2017 Yaakov Selkowitz <yselkowi@redhat.com> - 20170809-1
- Recent revision - 20170809

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20170424-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Apr 27 2017 Yaakov Selkowitz <yselkowi@redhat.com> - 20170424-1
- Recent revision - 20170424

* Wed Feb 22 2017 Yaakov Selkowitz <yselkowi@redhat.com> - 20170206-1
- Recent revision - 20170206

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20170116-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 17 2017 Yaakov Selkowitz <yselkowi@redhat.com> - 20170116-1
- Recent revision - 20170116
- Use system psl-make-dafsa

* Thu Jan  5 2017 Yaakov Selkowitz <yselkowi@redhat.com> - 20161230-1
- Recent revision - 20161230
- Added dafsa package for runtime use by libpsl

* Fri Nov  4 2016 Yaakov Selkowitz <yselkowi@redhat.com> - 20161028-1
- Recent revision - 20161028

* Mon Aug 15 2016 Yaakov Selkowitz <yselkowi@redhat.com> - 20160805-1
- Recent revision - 20160805

* Fri Jul 15 2016 Yanko Kaneti <yaneti@declera.com> - 20160713-1
- Recent revision - 20160713

* Fri Mar 25 2016 Yanko Kaneti <yaneti@declera.com> - 20160323-1
- Recent revision - 20160323

* Mon Feb  8 2016 Yanko Kaneti <yaneti@declera.com> - 20160206-1
- Recent revision - 20160206

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 20151208-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Dec  8 2015 Yanko Kaneti <yaneti@declera.com> - 20151208-1
- Recent revision - 20151208

* Tue Sep  1 2015 Yanko Kaneti <yaneti@declera.com> - 20150831-1
- The latest revision - 20150831
- Add test data - bug 1251921

* Mon Aug  3 2015 Yanko Kaneti <yaneti@declera.com> - 20150731-1
- The latest revision - 20150731
- Move to the new upstream filename. Install a compat symlink for now

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20150506-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May  7 2015 Yanko Kaneti <yaneti@declera.com> - 20150506-1
- The latest revision - 20150506

* Thu Apr 30 2015 Yanko Kaneti <yaneti@declera.com> - 20150430-1
- The latest revision - 20150430

* Tue Apr  7 2015 Yanko Kaneti <yaneti@declera.com> - 20150407-1
- The latest revision - 20150407

* Sat Apr  4 2015 Yanko Kaneti <yaneti@declera.com> - 20150404-1
- The latest revision - 20150404

* Thu Feb 26 2015 Yanko Kaneti <yaneti@declera.com> - 20150226-1
- The latest revision - 20150226

* Wed Feb 18 2015 Yanko Kaneti <yaneti@declera.com> - 20150217-1
- The latest revision - 20150217

* Thu Feb  5 2015 Yanko Kaneti <yaneti@declera.com> - 20150204-1
- The latest revision - 20150204

* Tue Dec 30 2014 Yanko Kaneti <yaneti@declera.com> - 20141230-1
- Initial version for review - 20141124-1
- Today's revision. Add license file - 20141218-1
- Today's revision - 20141223-1
- Today's revision - 20141230-1

