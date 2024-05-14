Summary:        MirBSD enhanced version of the Korn Shell
Name:           mksh
Version:        59c
Release:        3%{?dist}
# BSD (setmode.c), ISC (strlcpy.c), MirOS (the rest)
License:        MirOS AND ISC AND BSD
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://www.mirbsd.org/mksh.htm
Source0:        https://www.mirbsd.org/MirOS/dist/mir/%{name}/%{name}-R%{version}.tgz
Source1:        dot-mkshrc
Source2:        rtchecks.expected
BuildRequires:  ed
BuildRequires:  gcc
BuildRequires:  perl-interpreter
BuildRequires:  sed
BuildRequires:  util-linux
BuildRequires:  perl(Getopt::Std)
Requires(post): %{_sbindir}/alternatives
Requires(post): grep
Requires(postun): sed
Requires(preun): %{_sbindir}/alternatives
Conflicts:      filesystem < 3
Provides:       /bin/ksh
Provides:       /bin/lksh
Provides:       /bin/mksh
Provides:       /bin/rlksh
Provides:       /bin/rmksh

%description
mksh is the MirBSD enhanced version of the Public Domain Korn shell (pdksh),
a bourne-compatible shell which is largely similar to the original AT&T Korn
shell. It includes bug fixes and feature improvements in order to produce a
modern, robust shell good for interactive and especially script use, being a
bourne shell replacement, pdksh successor and an alternative to the C shell.

%prep
%setup -q -n %{name}

# we'll need this later
cat >rtchecks <<'EOF'
typeset -i sari=0
typeset -Ui uari=0
typeset -i x=0
print -r -- $((x++)):$sari=$uari. #0
let --sari --uari
print -r -- $((x++)):$sari=$uari. #1
sari=2147483647 uari=2147483647
print -r -- $((x++)):$sari=$uari. #2
let ++sari ++uari
print -r -- $((x++)):$sari=$uari. #3
let --sari --uari
let 'sari *= 2' 'uari *= 2'
let ++sari ++uari
print -r -- $((x++)):$sari=$uari. #4
let ++sari ++uari
print -r -- $((x++)):$sari=$uari. #5
sari=-2147483648 uari=-2147483648
print -r -- $((x++)):$sari=$uari. #6
let --sari --uari
print -r -- $((x++)):$sari=$uari. #7
(( sari = -5 >> 1 ))
((# uari = -5 >> 1 ))
print -r -- $((x++)):$sari=$uari. #8
(( sari = -2 ))
((# uari = sari ))
print -r -- $((x++)):$sari=$uari. #9
EOF

%build
CFLAGS="%{optflags} -DMKSH_DISABLE_EXPERIMENTAL" LDFLAGS="$RPM_LD_FLAGS" sh Build.sh -r
cp test.sh test_mksh.sh
HAVE_PERSISTENT_HISTORY=0; export HAVE_PERSISTENT_HISTORY
CFLAGS="%{optflags} -DMKSH_DISABLE_EXPERIMENTAL" LDFLAGS="$RPM_LD_FLAGS" sh Build.sh -L -r
cp -f test.sh test_lksh.sh
./mksh FAQ2HTML.sh

%install
install -D -m 755 %{name} %{buildroot}%{_bindir}/%{name}
install -D -m 755 lksh %{buildroot}%{_bindir}/lksh
install -D -m 644 %{name}.1 %{buildroot}%{_mandir}/man1/%{name}.1
install -D -m 644 lksh.1 %{buildroot}%{_mandir}/man1/lksh.1
install -D -p -m 644 dot.mkshrc %{buildroot}%{_sysconfdir}/mkshrc
install -D -p -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/skel/.mkshrc
ln -s %{name} %{buildroot}%{_bindir}/rmksh
ln -s lksh %{buildroot}%{_bindir}/rlksh
ln -s %{name}.1 %{buildroot}%{_mandir}/man1/rmksh.1
ln -s lksh.1 %{buildroot}%{_mandir}/man1/rlksh.1
touch $RPM_BUILD_ROOT{%{_bindir}/ksh,%{_mandir}/man1/ksh.1}

%check
./mksh rtchecks >rtchecks.got 2>&1
if ! cmp --quiet rtchecks.got %{SOURCE2}
then
  echo "rtchecks failed"
  diff -Naurp %{SOURCE2} rtchecks.got
  exit 1
fi

for tf in test_mksh.sh test_lksh.sh
do
  echo > test.wait
  script -qc "./$tf"' -v; x=$?; rm -f test.wait; exit $x'
  maxwait=0
  while test -e test.wait; do
    sleep 1
    maxwait=$(expr $maxwait + 1)
    test $maxwait -lt 900 || break
  done
done

%post

grep -q "^/bin/%{name}$" %{_sysconfdir}/shells 2>/dev/null || \
  echo "/bin/%{name}" >> %{_sysconfdir}/shells

grep -q "^%{_bindir}/%{name}$" %{_sysconfdir}/shells 2>/dev/null || \
  echo "%{_bindir}/%{name}" >> %{_sysconfdir}/shells

%{_sbindir}/alternatives --install %{_bindir}/ksh ksh %{_bindir}/%{name} 10 \
  --slave %{_mandir}/man1/ksh.1.gz ksh-man %{_mandir}/man1/%{name}.1.gz

%preun
if [ $1 = 0 ]; then
  %{_sbindir}/alternatives --remove ksh %{_bindir}/%{name}
fi

%postun
if [ ! -x %{_bindir}/%{name} ]; then

  sed -e 's@^/bin/%{name}$@POSTUNREMOVE@' -e '/^POSTUNREMOVE$/d' -i %{_sysconfdir}/shells

  sed -e 's@^%{_bindir}/%{name}$@POSTUNREMOVE@' -e '/^POSTUNREMOVE$/d' -i %{_sysconfdir}/shells
fi

%files
%doc dot.mkshrc FAQ.htm
%ghost %{_bindir}/ksh
%{_bindir}/lksh
%{_bindir}/%{name}
%{_bindir}/rlksh
%{_bindir}/rmksh
%config(noreplace) %{_sysconfdir}/mkshrc
%config(noreplace) %{_sysconfdir}/skel/.mkshrc
%ghost %{_mandir}/man1/ksh.1*
%{_mandir}/man1/lksh.1*
%{_mandir}/man1/%{name}.1*
%{_mandir}/man1/rlksh.1*
%{_mandir}/man1/rmksh.1*

%changelog
* Wed Feb 22 2023 Muhammad Falak <mwani@microsoft.com> - 59c-3
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 59c-2
- Initial CBL-Mariner import from Fedora 33 (license: MIT).

* Mon Nov 02 2020 Robert Scheck <robert@fedoraproject.org> 59c-1
- Upgrade to 59c (#1893414)
- Add alternatives switching for ksh (#1879002)

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 59b-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun May 17 2020 Robert Scheck <robert@fedoraproject.org> 59b-1
- Upgrade to 59b (#1836572)

* Wed Apr 15 2020 Robert Scheck <robert@fedoraproject.org> 59-1
- Upgrade to 59 (#1823973)

* Fri Mar 27 2020 Robert Scheck <robert@fedoraproject.org> 58-1
- Upgrade to 58 (#1817981)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 57-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 57-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Mar 25 2019 Robert Scheck <robert@fedoraproject.org> 57-1
- Upgrade to 57 (#1684737)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 56c-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 56c-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Feb 18 2018 Robert Scheck <robert@fedoraproject.org> 56c-3
- Build flags injection is only partially successful (#1543842)

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 56c-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Jan 14 2018 Robert Scheck <robert@fedoraproject.org> 56c-1
- Upgrade to 56c

* Tue Aug 29 2017 Robert Scheck <robert@fedoraproject.org> 56b-1
- Upgrade to 56b

* Wed Aug 09 2017 Michal Hlavinka <mhlavink@redhat.com> 56-1
- Upgrade to 56 (#1479800)
- fixes wait exit codes of co-processes when run in interactive mode (#1479320)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 55-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 55-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Apr 13 2017 Robert Scheck <robert@fedoraproject.org> 55-1
- Upgrade to 55

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 54-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Nov 13 2016 Robert Scheck <robert@fedoraproject.org> 54-1
- Upgrade to 54 (#1394477)

* Sun Aug 28 2016 Robert Scheck <robert@fedoraproject.org> 53a-1
- Upgrade to 53a (#1370764)

* Mon Mar 07 2016 Robert Scheck <robert@fedoraproject.org> 52c-1
- Upgrade to 52c

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 52b-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 21 2016 Robert Scheck <robert@fedoraproject.org> 52b-1
- Upgrade to 52b (#1300482)

* Sun Dec 13 2015 Robert Scheck <robert@fedoraproject.org> 52-1
- Upgrade to 52 (#1291069)

* Sat Jul 11 2015 Robert Scheck <robert@fedoraproject.org> 51-1
- Upgrade to 51 (#1242108)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 50f-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Apr 20 2015 Robert Scheck <robert@fedoraproject.org> 50f-1
- Upgrade to 50f

* Thu Mar 19 2015 Robert Scheck <robert@fedoraproject.org> 50e-1
- Upgrade to 50e
- Apply https://fedoraproject.org/wiki/Features/UsrMove

* Wed Oct 08 2014 Robert Scheck <robert@fedoraproject.org> 50d-1
- Upgrade to 50d (#1150493)

* Fri Oct 03 2014 Robert Scheck <robert@fedoraproject.org> 50c-1
- Upgrade to 50c

* Thu Sep 11 2014 Robert Scheck <robert@fedoraproject.org> 50b-1
- Upgrade to 50b

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 50-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 03 2014 Robert Scheck <robert@fedoraproject.org> 50-1
- Upgrade to 50

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 49-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jan 14 2014 Robert Scheck <robert@fedoraproject.org> 49-1
- Upgrade to 49

* Sun Aug 25 2013 Robert Scheck <robert@fedoraproject.org> 48b-1
- Upgrade to 48b

* Sat Aug 03 2013 Robert Scheck <robert@fedoraproject.org> 47-1
- Upgrade to 47

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 46-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri May 03 2013 Thorsten Glaser <tg@mirbsd.org> 46-1
- Upgrade mksh to R46

* Wed May 01 2013 Thorsten Glaser <tg@mirbsd.org> 45-1
- Upgrade mksh to R45 and the other files to the accompanying versions
- Drop workaround for GCC PR55009 (no longer needed)
- Use https for homepage

* Mon Mar 18 2013 Robert Scheck <robert@fedoraproject.org> 44-1
- Upgrade to 44 and work around bug in GCC 4.8 (#922974)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 41-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec 03 2012 Michal Hlavinka <mhlavink@redhat.com> - 41-1
- Upgrade to 41

* Fri Jul 20 2012 Michal Hlavinka <mhlavink@redhat.com> - 40i-0.20120630
- Upgrade to pre-release of 40i
- includes new legacy shell lksh for old scripts requiring pdksh or similar old
  ksh-88 shell, see man lksh for differences

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 40d-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 40d-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Dec 11 2011 Robert Scheck <robert@fedoraproject.org> 40d-1
- Upgrade to 40d

* Tue Nov 22 2011 Robert Scheck <robert@fedoraproject.org> 40c-1
- Upgrade to 40c

* Thu Jul 28 2011 Robert Scheck <robert@fedoraproject.org> 40b-2
- Use new "Build.sh -r -c lto" rather "Build.sh -r -combine"

* Thu Jul 28 2011 Robert Scheck <robert@fedoraproject.org> 40b-1
- Upgrade to 40b

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 39c-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 04 2011 Michal Hlavinka <mhlavink@redhat.com> 39c-4
- fix crash when bad substitution is used

* Wed Jul 21 2010 Michal Hlavinka <mhlavink@redhat.com> 39c-3
- fix crash when alias contains alias
- fix crash when xtrace is enabled

* Sun Jul 11 2010 Robert Scheck <robert@fedoraproject.org> 39c-2
- Added default configuration /etc/mkshrc & /etc/skel/.mkshrc
  as default skel (like at bash; thanks to Michal Hlavinka)
- Corrected the license tag (thanks to Michal Hlavinka)
- Removed the arc4random.c file (upstream is phasing it out)

* Sat Feb 27 2010 Robert Scheck <robert@fedoraproject.org> 39c-1
- Upgrade to 39c and updated arc4random.c file

* Thu Aug 13 2009 Robert Scheck <robert@fedoraproject.org> 39-1
- Upgrade to 39 and updated arc4random.c file

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 38b-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun May 31 2009 Robert Scheck <robert@fedoraproject.org> 38b-1
- Upgrade to 38b

* Sun May 31 2009 Robert Scheck <robert@fedoraproject.org> 38-1
- Upgrade to 38 and updated arc4random.c file
- Used -combine (-fwhole-program) rather the old -j switch

* Sun Apr 05 2009 Robert Scheck <robert@fedoraproject.org> 37b-1
- Upgrade to 37b

* Mon Feb 23 2009 Robert Scheck <robert@fedoraproject.org> 36b-2
- Rebuild against gcc 4.4 and rpm 4.6

* Sun Dec 14 2008 Robert Scheck <robert@fedoraproject.org> 36b-1
- Upgrade to 36b and updated arc4random.c file

* Tue Dec 02 2008 Robert Scheck <robert@fedoraproject.org> 36-2
- Upstream patch for command hang/high cpu workload (#474115)

* Sat Oct 25 2008 Robert Scheck <robert@fedoraproject.org> 36-1
- Upgrade to 36

* Sat Jul 19 2008 Robert Scheck <robert@fedoraproject.org> 35b-1
- Upgrade to 35b

* Sun Jul 13 2008 Robert Scheck <robert@fedoraproject.org> 35-1
- Upgrade to 35

* Sat Apr 12 2008 Robert Scheck <robert@fedoraproject.org> 33d-1
- Upgrade to 33d

* Fri Apr 04 2008 Robert Scheck <robert@fedoraproject.org> 33c-1
- Upgrade to 33c and updated arc4random.c file

* Mon Mar 03 2008 Robert Scheck <robert@fedoraproject.org> 33-1
- Upgrade to 33

* Sun Feb 10 2008 Robert Scheck <robert@fedoraproject.org> 32-2
- Rebuild against gcc 4.3

* Sat Nov 10 2007 Robert Scheck <robert@fedoraproject.org> 32-1
- Upgrade to 32
- Solved fork problems in %%check (thanks to Thorsten Glaser)

* Mon Oct 15 2007 Robert Scheck <robert@fedoraproject.org> 31d-1
- Upgrade to 31d

* Wed Sep 12 2007 Robert Scheck <robert@fedoraproject.org> 31c-1
- Upgrade to 31c
- Added a buildrequirement to ed, added arc4random.c file

* Tue Sep 11 2007 Robert Scheck <robert@fedoraproject.org> 31b-1
- Upgrade to 31b
- Use script to get %%check happy (thanks to Thorsten Glaser)

* Sat Sep 08 2007 Robert Scheck <robert@fedoraproject.org> 31-1
- Upgrade to 31

* Tue Aug 28 2007 Robert Scheck <robert@fedoraproject.org> 30-2
- Updated the license tag according to the guidelines

* Sat Jul 28 2007 Robert Scheck <robert@fedoraproject.org> 30-1
- Upgrade to 30

* Sat Jul 14 2007 Robert Scheck <robert@fedoraproject.org> 29g-1
- Upgrade to 29g

* Sun Jun 03 2007 Robert Scheck <robert@fedoraproject.org> 29f-1
- Upgrade to 29f
- Initial spec file for Fedora and Red Hat Enterprise Linux
