Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global unicodedir %{_datadir}/unicode
%global emojidir %{unicodedir}/emoji

Name:           unicode-emoji
Version:        16.0
Release:        1%{?dist}
Summary:        Unicode Emoji Data Files

License:        Unicode-DFS-2016
URL:            https://www.unicode.org/emoji/
Source0:        https://www.unicode.org/copyright.html
Source1:        https://www.unicode.org/Public/emoji/15.1/ReadMe.txt
Source2:        https://www.unicode.org/Public/15.1.0/ucd/emoji/emoji-data.txt
Source3:        https://www.unicode.org/Public/emoji/15.1/emoji-sequences.txt
Source4:        https://www.unicode.org/Public/emoji/15.1/emoji-test.txt
Source5:        https://www.unicode.org/Public/15.1.0/ucd/emoji/emoji-variation-sequences.txt
Source6:        https://www.unicode.org/Public/emoji/15.1/emoji-zwj-sequences.txt
Source7:        https://www.unicode.org/license.txt

BuildArch:      noarch

%description
Unicode Emoji Data Files are the machine-readable
emoji data files associated with
https://www.unicode.org/reports/tr51/index.html

%prep
%{nil}

%build
%{nil}

%install
cp -p %{SOURCE0} .
mkdir -p %{buildroot}%{emojidir}
cp -p %{SOURCE1} %{buildroot}%{emojidir}
cp -p %{SOURCE2} %{buildroot}%{emojidir}
cp -p %{SOURCE3} %{buildroot}%{emojidir}
cp -p %{SOURCE4} %{buildroot}%{emojidir}
cp -p %{SOURCE5} %{buildroot}%{emojidir}
cp -p %{SOURCE6} %{buildroot}%{emojidir}

%files
%license license.txt
%dir %{unicodedir}
%dir %{emojidir}
%doc %{emojidir}/ReadMe.txt
%{emojidir}/emoji-*txt

%changelog
* Wed Jan 15 2025 Durga Jagadeesh Palli <v-dpalli@microsoft.com> - 16.0-2
- Initial Azure Linux import from Fedora 41 (license: MIT)
- change the URL from http to https
- License verified

* Wed Sep 11 2024 Mike FABIAN <mfabian@redhat.com> - 16.0-1
- Fix version number, should be 16.0

* Wed Sep 11 2024 Mike FABIAN <mfabian@redhat.com> - 15.1-5
- Update to Unicode Emoji Data 16.0 (was released on September 10, 2024)

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 15.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 15.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Sep 14 2023 Mike FABIAN <mfabian@redhat.com> - 15.1-1
- Update to Unicode Emoji Data 15.1 (was released on September 12, 2023)

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 15.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Apr 14 2023 Mike FABIAN <mfabian@redhat.com> - 15.0-3
- Change license tag from Unicode-TOU to Unicode-DFS-2016
  See: https://gitlab.com/fedora/legal/fedora-license-data/-/issues/199

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 15.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Nov 25 2022 Mike FABIAN <mfabian@redhat.com> - 15.0-1
- Update to Unicode Emoji Data 15.0 (was released on September 13, 2022)
- Migrate license tag to SPDX

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 14.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 14.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Sep 16 2021 Mike FABIAN <mfabian@redhat.com> - 14.0-1
- Update to Unicode Emoji Data 14.0 (was released on September 14, 2021)

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 13.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 13.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 13.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Feb 06 2020 Mike FABIAN <mfabian@redhat.com> - 13.0-1
- Update to Unicode Emoji Data 13.0 (was released on January 29, 2020)

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 12.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 15 2019 Mike FABIAN <mfabian@redhat.com> - 12.0-1
- Update to Unicode Emoji Data 12.0

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 11.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 07 2018 Mike FABIAN <mfabian@redhat.com> - 11.0-1
- Bump Version number to 11.0 because Unicode 11.0.0 is officially
  released now. The emoji data did not change.

* Wed Mar 07 2018 Mike FABIAN <mfabian@redhat.com> - 10.90.20180207-1
- Update to a prerelease of Unicode Emoji Data 11.0

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 20 2017 Mike FABIAN <mfabian@redhat.com> - 5.0-1
- update to Unicode Emoji Data 5.0

* Thu May 04 2017 Mike FABIAN <mfabian@redhat.com> - 4.0-3
- add directory %%{emojidir} to file list

* Tue May 02 2017 Mike FABIAN <mfabian@redhat.com> - 4.0-2
- Fix rpmlint issues: description-line-too-long, corrected
  license tag, tag ReadMe.txt as %%doc

* Tue Apr 25 2017 Mike FABIAN <mfabian@redhat.com> - 4.0-1
- package Unicode Emoji Data 4.0
- MIT license
