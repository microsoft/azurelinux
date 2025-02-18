Summary:        Generic IMAP server compliancy tester
Name:           imaptest
# Upstream is not really planning on adding version numbers
Version:        20210705
Release:        8%{?dist}
License:        MIT
URL:            https://www.imapwiki.org/ImapTest
Source0:        https://dovecot.org/nightly/%{name}/%{name}-%{version}.tar.gz
BuildRequires:  gcc, make, dovecot-devel >= 2.3.15
BuildRequires:  autoconf, automake, libtool
# dovecot-devel.i686 was removed with dovecot-2.3.21-7.fc41
%if 0%{?fedora} > 40 || 0%{?rhel} > 9
ExcludeArch:    %{ix86}
%endif

%description
ImapTest is a generic IMAP server compliancy tester that works with all IMAP
servers. It supports stress testing with state tracking, scripted testing and
benchmarking. When stress testing with state tracking ImapTest sends random
commands to the server and verifies that server's output looks correct. Using
the scripted testing ImapTest runs a list of predefined scripted tests and
verifies that server returns expected output.

Examples and details are provided online at: https://www.imapwiki.org/ImapTest

%prep
%setup -q
autoreconf -i

# Workaround for https://bugzilla.redhat.com/show_bug.cgi?id=1103927#c4 (and later)
sed -e 's@\(^LIBDOVECOT .*\)@\1 -Wl,-rpath -Wl,%{_libdir}/dovecot@' -i src/Makefile.in

%build
%configure --with-dovecot=%{_libdir}/dovecot
%make_build

%install
%make_install

# Copy test files for later shipping
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}/
cp -pr src/tests/ $RPM_BUILD_ROOT%{_datadir}/%{name}/

%check
$RPM_BUILD_ROOT%{_bindir}/%{name} --help

%files
%license COPYING COPYING.MIT
%doc AUTHORS ChangeLog profile.conf pop3-profile.conf
%{_bindir}/%{name}
%{_datadir}/%{name}/

%changelog
* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20210705-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20210705-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20210705-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 20210705-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 20210705-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 20210705-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 20210705-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Sep 09 2021 Robert Scheck <robert@fedoraproject.org> 20210705-1
- Upgrade to 20210705 (#1940745)

* Fri Jul 23 2021 Robert Scheck <robert@fedoraproject.org> 20210319-1
- Upgrade to 20210319 (#1940745)

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20210305-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Mar 06 2021 Robert Scheck <robert@fedoraproject.org> 20210305-1
- Upgrade to 20210305 (#1935535)

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20210116-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 18 2021 Robert Scheck <robert@fedoraproject.org> 20210116-1
- Upgrade to 20210116 (#1916982)

* Sat Nov 07 2020 Robert Scheck <robert@fedoraproject.org> 20200904-1
- Upgrade to 20200904

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20190614-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20190614-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Nov 25 2019 Robert Scheck <robert@fedoraproject.org> 20190614-2
- Rebuilt for Dovecot 2.3.x ABI incompatibility (#1776476)

* Sun Jul 28 2019 Robert Scheck <robert@fedoraproject.org> 20190614-1
- Upgrade to 20190614

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20180824-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20180824-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Nov 11 2018 Robert Scheck <robert@fedoraproject.org> 20180824-2
- Remove (broken) versioned dovecot requirement

* Thu Nov 01 2018 Robert Scheck <robert@fedoraproject.org> 20180824-1
- Upgrade to 20180824

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20180221-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Apr 03 2018 Robert Scheck <robert@fedoraproject.org> 20180221-1
- Upgrade to 20180221 (#1562970)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20170719-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Aug 06 2017 Robert Scheck <robert@fedoraproject.org> 20170719-1
- Upgrade to 20170719

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20151228-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20151228-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20151228-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 20151228-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Jan 03 2016 Robert Scheck <robert@fedoraproject.org> 20151228-1
- Upgrade to 20151228

* Sun Dec 27 2015 Robert Scheck <robert@fedoraproject.org> 20151210-1
- Upgrade to 20151210

* Mon Oct 12 2015 Robert Scheck <robert@fedoraproject.org> 20151007-1
- Upgrade to 20151007

* Fri Aug 14 2015 Robert Scheck <robert@fedoraproject.org> 20150812-1
- Upgrade to 20150812

* Wed Jun 24 2015 Robert Scheck <robert@fedoraproject.org> 20150620-1
- Upgrade to 20150620

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20141030-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Nov 07 2014 Robert Scheck <robert@fedoraproject.org> 20141030-1
- Upgrade to 20141030

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20140711-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul 23 2014 Robert Scheck <robert@fedoraproject.org> 20140711-1
- Upgrade to 20140711

* Fri Jun 20 2014 Robert Scheck <robert@fedoraproject.org> 20140528-2
- Added workaround for missing rpath linking (#1103927 #c4)

* Tue Jun 03 2014 Robert Scheck <robert@fedoraproject.org> 20140528-1
- Upgrade to 20140528
- Initial spec file for Fedora and Red Hat Enterprise Linux
