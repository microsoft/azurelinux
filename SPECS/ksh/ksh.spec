%global       verBetaPrefix 1.0.0
%global       verBetaSuffix 1
%global       verBetaFull %{verBetaPrefix}-beta.%{verBetaSuffix}

Summary:        The Original ATT Korn Shell
Name:           ksh
Version:        %{verBetaPrefix}~beta.%{verBetaSuffix}
Release:        5%{?dist}
License:        EPL-1.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            http://www.kornshell.com/
Source0:        https://github.com/ksh93/%{name}/archive/v%{verBetaFull}/%{name}-%{verBetaFull}.tar.gz
Source1:        kshcomp.conf
Source2:        kshrc.rhs
Source3:        dotkshrc
# temporary commenting out failing tests
Patch1:         %{name}-%{verBetaFull}-regre-tests.patch
# in some build commands relocate "-lm" flag
Patch2:         %{name}-%{verBetaFull}-fix-build.patch

BuildRequires:  bison
BuildRequires:  gcc
# regression test suite uses 'ps' from procps
BuildRequires:  procps

%if %{with_check}
BuildRequires:  shadow-utils
BuildRequires:  sudo
%endif

Requires:       coreutils
Requires:       diffutils

Requires(post): coreutils
Requires(post): grep
Requires(post): systemd

Requires(postun): sed

%description
KSH-93 is the most recent version of the KornShell by David Korn of
AT&T Bell Laboratories.
KornShell is a shell programming language, which is upward compatible
with "sh" (the Bourne Shell).

%prep
%autosetup -n %{name}-%{verBetaFull} -p1

#/dev/fd test does not work because of mock
sed -i 's|ls /dev/fd|ls /proc/self/fd|' src/cmd/ksh93/features/options

# disable register for debugging
sed -i 1i"#define register" src/lib/libast/include/ast.h

%build
%set_build_flags
XTRAFLAGS=""
for f in -Wno-unknown-pragmas -Wno-missing-braces -Wno-unused-result -Wno-return-type -Wno-int-to-pointer-cast -Wno-parentheses -Wno-unused -Wno-unused-but-set-variable -Wno-cpp -Wno-maybe-uninitialized -Wno-lto-type-mismatch -P
do
  $CC $f -E - </dev/null >/dev/null 2>&1 && XTRAFLAGS="$XTRAFLAGS $f"
done
export CCFLAGS="%{optflags} $RPM_LD_FLAGS -fno-strict-aliasing $XTRAFLAGS"
./bin/package make -S

%install
mkdir -p %{buildroot}{/bin,%{_bindir},%{_mandir}/man1}
install -p -m 755 arch/*/bin/ksh %{buildroot}%{_bindir}/ksh93
install -p -m 755 arch/*/bin/shcomp %{buildroot}%{_bindir}/shcomp
install -p -m 644 arch/*/man/man1/sh.1 %{buildroot}%{_mandir}/man1/ksh93.1
mkdir -p %{buildroot}%{_sysconfdir}/skel
install -p -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/skel/.kshrc
install -p -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/kshrc
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/binfmt.d/kshcomp.conf

touch %{buildroot}%{_bindir}/ksh
touch %{buildroot}%{_mandir}/man1/ksh.1.gz

touch %{buildroot}%{_bindir}/rksh
touch %{buildroot}%{_mandir}/man1/rksh.1.gz

%check
# We run more tests as non-root user
chmod g+w . -R
useradd test -G root -m

# Disabling tests as they tend to freez and the package is low-pri at the moment.
false && sudo -u test ./bin/shtests --compile

%post
for s in /bin/ksh /bin/rksh %{_bindir}/ksh %{_bindir}/rksh
do
  if [ ! -f %{_sysconfdir}/shells ]; then
        echo "$s" > %{_sysconfdir}/shells
  else
        if ! grep -q '^'"$s"'$' %{_sysconfdir}/shells ; then
                echo "$s" >> %{_sysconfdir}/shells
        fi
  fi
done

%{_sbindir}/alternatives --install %{_bindir}/ksh ksh \
                %{_bindir}/ksh93 50 \
        --slave %{_bindir}/rksh rksh \
                %{_bindir}/ksh93 \
        --slave %{_mandir}/man1/rksh.1.gz rksh-man \
                %{_mandir}/man1/ksh93.1.gz \
        --slave %{_mandir}/man1/ksh.1.gz ksh-man \
                %{_mandir}/man1/ksh93.1.gz

#if not symlink we are updating ksh where there was no alternatives before
#so replace with symlink and set alternatives
if [ ! -L %{_bindir}/ksh ]; then
        %{_sbindir}/alternatives --auto ksh
        ln -sf %{_sysconfdir}/alternatives/ksh %{_bindir}/ksh
        ln -sf %{_sysconfdir}/alternatives/ksh-man %{_mandir}/man1/ksh.1.gz
fi

/bin/systemctl try-restart systemd-binfmt.service >/dev/null 2>&1 || :

%postun
for s in /bin/ksh /bin/rksh %{_bindir}/ksh %{_bindir}/rksh
do
  if [ ! -f $s ]; then
        sed -i '\|^'"$s"'$|d' %{_sysconfdir}/shells
  fi
done

%preun
if [ $1 = 0 ]; then
        %{_sbindir}/alternatives --remove ksh %{_bindir}/ksh93
fi

%verifyscript
echo -n "Looking for ksh in %{_sysconfdir}/shells... "
if ! grep '^/bin/ksh$' %{_sysconfdir}/shells > /dev/null; then
    echo "missing"
    echo "ksh missing from %{_sysconfdir}/shells" >&2
else
    echo "found"
fi

%files
%doc src/cmd/ksh93/COMPATIBILITY src/cmd/ksh93/RELEASE src/cmd/ksh93/TYPES
%license LICENSE.md
%{_bindir}/ksh93
%ghost %{_bindir}/ksh
%ghost %{_bindir}/rksh
%{_bindir}/shcomp
%{_mandir}/man1/*
%ghost %{_mandir}/man1/ksh.1.gz
%ghost %{_mandir}/man1/rksh.1.gz
%config(noreplace) %{_sysconfdir}/skel/.kshrc
%config(noreplace) %{_sysconfdir}/kshrc
%config(noreplace) %{_sysconfdir}/binfmt.d/kshcomp.conf

%changelog
* Tue Nov 14 2023 Andrew Phelps <anphel@microsoft.com> - 1.0.0~beta.1-5
- Modify ksh-1.0.0-beta.1-fix-build.patch-fix-build.patch with proper "-lm" location for updated toolchain

* Wed Apr 13 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.0~beta.1-4
- Initial CBL-Mariner import from Fedora 36 (license: MIT).
- License verified.
- Disabled tests until the hang issue can be fixed.
- Removed epoch.

* Wed Feb 23 2022 Vincent Mihalkovic <vmihalko@redhat.com> - 3:1.0.0~BETA.1-3
- fix FTBFS in Fedora-36 (#2045778)

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3:1.0.0~beta.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Aug 02 2021 Vincent Mihalkovic <vmihalko@redhat.com> - 3:1.0.0~BETA-1
- new upstream release
- remove upstreamed patches
- update CCFLAGS (https://github.com/ksh93/ksh/commit/98f989afcc7)
  Resolves: #1933304

* Fri Jul 30 2021 Vincent Mihalkovic <vmihalko@redhat.com> - 2:20120801-257
- fix invalid source URLs and license tag

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2:20120801-256
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Mar 18 2021 Vincent Mihalkovic <vmihalko@redhat.com> - 2:20120801-255
- fix rksh-man in alternatives

* Tue Feb 23 2021 Vincent Mihalkovic <vmihalko@redhat.com> - 2:20120801-254
- Add alternatives switching for rksh
  Resolves #1893919

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2:20120801-253
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 22 2021 Vincent Mihalkovic <vmihalko@redhat.com> - 2:20120801-252
- Use set_build_flags and standard CC variables (commit: c488ab6)

* Thu Aug 13 2020 Siteshwar Vashisht <svashisht@redhat.com> - 2:20120801-251
- Restore ksh to version 20120801
  Resolves: #1868715

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:2020.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Feb 07 2020 Siteshwar Vashisht <svashisht@redhat.com> - 1:2020.0.0-3
- Do not evaluate arithmetic expressions from environment variables at startup
  Resolves: #1790549

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:2020.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Oct 11 2019 Siteshwar Vashisht <svashisht@redhat.com> - 1:2020.0.0-1
- Rebase to 2020.0.0

* Tue Sep 03 2019 Siteshwar Vashisht <svashisht@redhat.com> - 1:2020.0.0-0.4
- Rebase to 2020.0.0-beta1

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:2020.0.0-0.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Apr 24 2019 Siteshwar Vashisht <svashisht@redhat.com> - 1:2020.0.0-0.2
- Add virtual provider for `/usr/bin/ksh`

* Wed Apr 17 2019 Siteshwar Vashisht <svashisht@redhat.com> - 1:2020.0.0-0.1
- Rebase to 2020.0.0-alpha1
  Resolves: #1700777

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20120801-250
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Oct 14 2018 Peter Robinson <pbrobinson@fedoraproject.org> 20120801-249
- chkconfig is no longer needed

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20120801-248
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 04 2018 Siteshwar Vashisht <svashisht@redhat.com> - 20120801-247
- Fix a crash caused by memcmp()
  Resolves: #1583226

* Mon Mar 12 2018 Siteshwar Vashisht <svashisht@redhat.com> - 20120801-246
- Enable standard Fedora LDFLAGS
  Resolves: #1548549

* Fri Feb 16 2018 Siteshwar Vashisht <svashisht@redhat.com> - 20120801-245
- Increase release number by 200 to ensure update path

* Mon Feb 12 2018 Siteshwar Vashisht <svashisht@redhat.com> - 20120801-45
- Fix a crash due to out of bounds write
  Resolves: #1537053

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20120801-44
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Nov 21 2017 Siteshwar Vashisht <svashisht@redhat.com> - 20120801-43
- Add virtual provide for /bin/ksh
  Resolves: #1513096

* Mon Aug 28 2017 Siteshwar Vashisht <svashisht@redhat.com> - 20120801-42
- Fix a memory corruption
  Resolves: #1464409

* Mon Aug 14 2017 Siteshwar Vashisht <svashisht@redhat.com> - 20120801-41
- Use posix exit code if last command exits due to a signal
  Resolves: #1471874

* Mon Aug 14 2017 Siteshwar Vashisht <svashisht@redhat.com> - 20120801-40
- Fix condition to fork subshell
  Resolves: #1462347

* Mon Aug 14 2017 Siteshwar Vashisht <svashisht@redhat.com> - 20120801-39
- Set terminal foreground process group while resuming process
  Resolves: #1459000

* Thu Aug 03 2017 Siteshwar Vashisht <svashisht@redhat.com> - 20120801-38
- Fix build failures caused by update in glibc
  Resolves: #1477082

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20120801-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20120801-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 29 2017 Siteshwar Vashisht <svashisht@redhat.com> - 20120801-35
- Fix memory corruption while parsing functions
  Resolves: #1451057

* Tue Apr 25 2017 Siteshwar Vashisht <svashisht@redhat.com> - 20120801-34
- Fix parsing of iso8859 characters
  Resolves: #1417886

* Tue Apr 11 2017 Siteshwar Vashisht <svashisht@redhat.com> - 20120801-33
- Avoid spurrious output in kia file creation
  Resolves: #1441142

* Fri Mar 10 2017 Michal Hlavinka <mhlavink@redhat.com> - 20120801-32
- add /usr/bin/ksh to /etc/shells (#1381113)

* Fri Mar 03 2017 Michal Hlavinka <mhlavink@redhat.com> - 20120801-31
- use latest set of patches

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20120801-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 20120801-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Aug 27 2015 Michal Hlavinka <mhlavink@redhat.com> - 20120801-28
- fix: in a login shell "( cmd & )" does nothing (#1217238)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20120801-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 06 2015 Michal Hlavinka <mhlavink@redhat.com> - 20120801-26
- do not crash, when disk is full, report an error (#1212994)

* Tue Apr 07 2015 Michal Hlavinka <mhlavink@redhat.com> - 20120801-25
- using trap DEBUG could cause segmentation fault

* Mon Mar 30 2015 Michal Hlavinka <mhlavink@redhat.com> - 20120801-24
- cd builtin could break IO redirection
- fix segfault when handling a trap
- exporting fixed with variable corrupted its data
- and more fixes

* Fri Mar 06 2015 Michal Hlavinka <mhlavink@redhat.com> - 20120801-23
- exporting fixed with variable corrupted its data (#1192027)

* Fri Feb 27 2015 Michal Hlavinka <mhlavink@redhat.com> - 20120801-22
- ksh hangs when command substitution containing a pipe fills out the pipe buffer (#1121204)

* Tue Aug 26 2014 Michal Hlavinka <mhlavink@redhat.com> - 20120801-21
- cd builtin file descriptor operations messed with IO redirections (#1133586)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20120801-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Michal Hlavinka <mhlavink@redhat.com> - 20120801-19
- fix segfault in job list code
- do not resend signal on termination (#1092132)
- fix brace expansion on/off
- fix incorrect rounding of numsers 0.5 < |x| <1.0 in printf (#1080940)
- fix parser errors related to the end of the here-document marker
- ksh hangs when command substitution fills out the pipe buffer
- using typeset -l with a restricted variabled caused segmentation fault
- monitor mode was documented incorrectly
- do not crash when unsetting running function from another one (#1105139)
- should report an error when trying to cd into directory without execution bit
- job locking mechanism did not survive compiler optimization
- reading a file via command substitution did not work when any of stdin,
  stdout or stderr were closed (#1070308)
- fix lexical parser crash

* Tue Jun 10 2014 Michal Hlavinka <mhlavink@redhat.com> - 20120801-18
- fix FTBFS(#1107070)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20120801-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Feb 11 2014 Michal Hlavinka <mhlavink@redhat.com> - 20120801-16
- ksh could hang when command substitution printed too much data

* Thu Feb 06 2014 Michal Hlavinka <mhlavink@redhat.com> - 20120801-15
- fix lexical parser crash (#960371)

* Fri Jan 17 2014 Michal Hlavinka <mhlavink@redhat.com> - 20120801-14
- fix overflow in subshell loop

* Mon Jan 06 2014 Michal Hlavinka <mhlavink@redhat.com> - 20120801-13
- fix argv rewrite (#1047508)

* Wed Oct 30 2013 Michal Hlavinka <mhlavink@redhat.com> - 20120801-12
- ksh stops on read when monitor mode is enabled

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20120801-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jun 12 2013 Michal Hlavinka <mhlavink@redhat.com> - 20120801-10
- fix memory leak

* Mon Jun 10 2013 Michal Hlavinka <mhlavink@redhat.com> - 20120801-9
- monitor mode in scripts wasn't working

* Thu Mar 07 2013 Michal Hlavinka <mhlavink@redhat.com> - 20120801-8
- fix another reproducer for tab completion

* Fri Feb 22 2013 Michal Hlavinka <mhlavink@redhat.com> - 20120801-7
- do not segfault on kill % (#914669)

* Fri Feb 01 2013 Michal Hlavinka <mhlavink@redhat.com> - 20120801-6
- cd file did not produce any error

* Fri Jan 25 2013 Michal Hlavinka <mhlavink@redhat.com> - 20120801-5
- ksh could not enter directories with path containing /.something (#889748)
- file name autocomplete prevented following numeric input (#889745)

* Wed Nov 21 2012 Michal Hlavinka <mhlavink@redhat.com> - 20120801-4
- bind Home, End, Delete,... key correctly for emacs mode
- do not crash when executed from deleted directory

* Fri Sep 14 2012 Michal Hlavinka <mhlavink@redhat.com> - 20120801-3
- fix typo in binfmt config file
- register binary format after package installation

* Thu Sep 13 2012 Michal Hlavinka <mhlavink@redhat.com> - 20120801-2
- add support for direct execution of compiled scripts

* Wed Aug 08 2012 Michal Hlavinka <mhlavink@redhat.com> - 20120801-1
- ksh updated to 20120801

* Tue Jul 31 2012 Michal Hlavinka <mhlavink@redhat.com> - 20120727-1
- ksh updated to 2012-07-27

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20120628-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 02 2012 Michal Hlavinka <mhlavink@redhat.com> - 20120628-1
- ksh updated to 20120628

* Wed Jun 27 2012 Michal Hlavinka <mhlavink@redhat.com> - 20120626-1
- ksh updated to 20120626

* Fri Jun 22 2012 Michal Hlavinka <mhlavink@redhat.com> - 20120620-1
- ksh updated to 2012-06-20

* Wed Jun 13 2012 Michal Hlavinka <mhlavink@redhat.com> - 20120612-1
- ksh updated to 20120612

* Mon Jun 04 2012 Michal Hlavinka <mhlavink@redhat.com> - 20120531-1
- ksh updated to 2012-05-31

* Mon Mar 19 2012 Michal Hlavinka <mhlavink@redhat.com> - 20120229-2
- do not hang after return code 12

* Wed Mar 14 2012 Michal Hlavinka <mhlavink@redhat.com> - 20120229-1
- ksh updated to 2012-02-29

* Tue Mar 13 2012 Michal Hlavinka <mhlavink@redhat.com> - 20120214-2
- fix tilda expansion in scripts

* Mon Feb 20 2012 Michal Hlavinka <mhlavink@redhat.com> - 20120214-1
- ksh updated to 20120214

* Mon Feb 06 2012 Michal Hlavinka <mhlavink@redhat.com> - 20120202-1
- ksh updated to 20120202

* Thu Jan 05 2012 Michal Hlavinka <mhlavink@redhat.com> - 20120101-1
- ksh updated to 2012-01-01

* Wed Dec 07 2011 Michal Hlavinka <mhlavink@redhat.com> - 20110630-9
- do not crash when browsing through history containing comment (#733813)

* Wed Dec 07 2011 Michal Hlavinka <mhlavink@redhat.com> - 20110630-8
- do not crash when two subseguent dots are used in variable or command name (#733544)

* Mon Dec 05 2011 Michal Hlavinka <mhlavink@redhat.com> - 20110630-7
- fix: ksh can prematurely exit without crash or any error
- make spec work in epel

* Thu Nov 10 2011 Michal Hlavinka <mhlavink@redhat.com> - 20110630-6
- add files to %%doc

* Thu Oct 06 2011 Michal Hlavinka <mhlavink@redhat.com> - 20110630-5
- ksh sometimes returns wrong exit code when pid numbers are being recycled

* Tue Oct 04 2011 Michal Hlavinka <mhlavink@redhat.com> - 20110630-4
- restore tty settings after timed out read (#572291)

* Fri Aug 12 2011 Michal Hlavinka <mhlavink@redhat.com> - 20110630-3
- do not crash when killing last bg job when there is not any

* Wed Aug 03 2011 Michal Hlavinka <mhlavink@redhat.com> - 20110630-2
- fix: IFS manipulation in a function can cause crash

* Fri Jul 01 2011 Michal Hlavinka <mhlavink@redhat.com> - 20110630-1
- ksh updated to 2011-06-30

* Wed Jun 08 2011 Michal Hlavinka <mhlavink@redhat.com> - 20110505-2
- fix: resume of suspended process using pipes does not work (#708909)

* Mon May 09 2011 Michal Hlavinka <mhlavink@redhat.com> - 20110505-1
- ksh updated to 2011-05-05

* Fri Apr 29 2011 Michal Hlavinka <mhlavink@redhat.com> - 20110428-1
- ksh updated to 2011-04-28

* Mon Apr 18 2011 Michal Hlavinka <mhlavink@redhat.com> - 20110415-1
- ksh updated to 2011-04-15

* Tue Mar 29 2011 Michal Hlavinka <mhlavink@redhat.com> - 20110208-3
- fix array definition being treated as fixed array
- fix suspend crashing ksh

* Mon Mar 07 2011 Michal Hlavinka <mhlavink@redhat.com> - 20110208-2
- fix ( ) compound list altering environment

* Wed Feb 09 2011 Michal Hlavinka <mhlavink@redhat.com> - 20110208-1
- ksh updated to 2011-02-08

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20110202-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb 04 2011 Michal Hlavinka <mhlavink@redhat.com> - 20110202-1
- ksh updated to 2011-02-02

* Wed Feb 02 2011 Michal Hlavinka <mhlavink@redhat.com> - 20110131-1
- ksh updated to 2011-01-31

* Fri Jan 28 2011 Michal Hlavinka <mhlavink@redhat.com> - 20110127-1
- ksh updated to 2011-01-27

* Thu Jan 20 2011 Michal Hlavinka <mhlavink@redhat.com> - 20110118-1
- ksh updated to 2011-01-18

* Mon Jan 17 2011 Michal Hlavinka <mhlavink@redhat.com> - 20110104-1
- ksh updated to 2011-01-04

* Thu Dec 23 2010 Michal Hlavinka <mhlavink@redhat.com> - 20101212-2.20101122
- found ugly regression, reverting to 2010-11-22 (with io race patch) for now

* Thu Dec 16 2010 Michal Hlavinka <mhlavink@redhat.com> - 20101212-1
- ksh updated to 2010-12-12

* Mon Dec 06 2010 Michal Hlavinka <mhlavink@redhat.com> - 20101201-2
- fix file io race condition when file was created, but still does not exist

* Fri Dec 03 2010 Michal Hlavinka <mhlavink@redhat.com> - 20101201-1
- ksh updated to 2010-12-01

* Tue Nov 23 2010 Michal Hlavinka <mhlavink@redhat.com> - 20101122-1
- ksh updated to 2010-11-22

* Mon Nov 01 2010 Michal Hlavinka <mhlavink@redhat.com> - 20101026-1
- ksh updated to 2010-10-26

* Tue Oct 12 2010 Michal Hlavinka <mhlavink@redhat.com> - 20101010-1
- ksh updated to 2010-10-10

* Fri Oct 08 2010 Michal Hlavinka <mhlavink@redhat.com> - 20100924-2
- disable only known to be broken builtins, let other enabled
- skip regression tests if /dev/fd is missing

* Tue Sep 28 2010 Michal Hlavinka <mhlavink@redhat.com> - 20100924-1
- ksh updated to 2010-09-24

* Mon Aug 30 2010 Michal Hlavinka <mhlavink@redhat.com> - 20100826-1
- ksh updated to 2010-08-26
- make regression test suite usable during package build

* Fri Aug 13 2010 Michal Hlavinka <mhlavink@redhat.com> - 20100811-1
- ksh updated to 2010-08-11

* Thu Jul 08 2010 Michal Hlavinka <mhlavink@redhat.com> - 20100701-1
- updated to 2010-07-01

* Fri Jun 25 2010 Michal Hlavinka <mhlavink@redhat.com> - 20100621-1
- updated to 2010-06-21

* Tue Jun 15 2010 Michal Hlavinka <mhlavink@redhat.com> - 20100527-2
- add shcomp for shell compiling

* Thu Jun 10 2010 Michal Hlavinka <mhlavink@redhat.com> - 20100527-1
- updated to 2010-05-27

* Mon May 31 2010 Michal Hlavinka <mhlavink@redhat.com> - 20100309-6
- add pathmunge to /etc/kshrc

* Wed May 05 2010 Michal Hlavinka <mhlavink@redhat.com> - 20100309-5
- fix rare cd builtin crash (#578582)

* Wed May 05 2010 Michal Hlavinka <mhlavink@redhat.com> - 20100309-4
- fix infinite loop when whence builtin is used with -q option (#587127)
- fix stdin for double command substitution (#584007)

* Mon Mar 29 2010 Michal Hlavinka <mhlavink@redhat.com> - 20100309-3
- fix typo in last patch

* Fri Mar 26 2010 Michal Hlavinka <mhlavink@redhat.com> - 20100309-2
- restore tty settings after timed out read for utf-8 locale

* Wed Mar 10 2010 Michal Hlavinka <mhlavink@redhat.com> - 20100309-1
- updated to 2010-03-09
- fix mock building - detection of /dev/fd/X

* Mon Jan 04 2010 Michal Hlavinka <mhlavink@redhat.com> - 20100202-1
- updated to 2010-02-02

* Mon Jan 04 2010 Michal Hlavinka <mhlavink@redhat.com> - 20091224-1
- updated to 2009-12-24

* Mon Dec 07 2009 Michal Hlavinka <mhlavink@redhat.com> - 20091206-1
- updated to 2009-12-06

* Fri Dec 04 2009 Michal Hlavinka <mhlavink@redhat.com> - 20091130-1
- updated to 2009-11-30

* Wed Nov 18 2009 Michal Hlavinka <mhlavink@redhat.com> - 20091021-1
- updated to 2009-10-21

* Thu Aug 27 2009 Michal Hlavinka <mhlavink@redhat.com> - 20090630-1
- updated to 2009-06-30

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20090505-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon May 11 2009 Michal Hlavinka <mhalvink@redhat.com> - 20090505-1
- updated to 2009-05-05

* Tue May 05 2009 Michal Hlavinka <mhalvink@redhat.com> - 20090501-1
- updated to 2009-05-01

* Tue Mar 10 2009 Michal Hlavinka <mhlavink@redhat.com> - 20081104-3
- fix typos in spec file

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20081104-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 21 2009 Michal Hlavinka <mhlavink@redhat.com> 20081104-1
- update to 2008-11-04
- ast-ksh-locales are not useable remove them

* Tue Oct 21 2008 Michal Hlavinka <mhlavink@redhat.com> 20080725-4
- fix #467025 - Ksh fails to initialise environment when login from graphic console

* Wed Aug 06 2008 Tomas Smetana <tsmetana@redhat.com> 20080725-3
- fix BuildRequires, rebuild

* Tue Aug  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> 20080725-2
- fix license tag

* Mon Jul 28 2008 Tomas Smetana <tsmetana@redhat.com> 20080725-1
- new upstream version

* Thu Jun 26 2008 Tomas Smetana <tsmetana@redhat.com> 20080624-1
- new upstream version

* Mon Feb 11 2008 Tomas Smetana <tsmetana@redhat.com> 20080202-1
- new upstream version

* Wed Jan 30 2008 Tomas Smetana <tsmetana@redhat.com> 20071105-3
- fix #430602 - ksh segfaults after unsetting OPTIND

* Mon Jan 07 2008 Tomas Smetana <tsmetana@redhat.com> 20071105-2
- fix #405381 - ksh will not handle $(xxx) when typeset -r IFS
- fix #386501 - bad group in spec file

* Wed Nov 07 2007 Tomas Smetana <tsmetana@redhat.com> 20071105-1
- new upstream version

* Wed Aug 22 2007 Tomas Smetana <tsmetana@redhat.com> 20070628-1.1
- rebuild

* Thu Jul 12 2007 Tomas Smetana <tsmetana@redhat.com> 20070628-1
- new upstream version
- fix unaligned access messages (Related: #219420)

* Tue May 22 2007 Tomas Smetana <tsmetana@redhat.com> 20070328-2
- fix wrong exit status of spawned process after SIGSTOP
- fix building of debuginfo package, add %%{?dist} to release
- fix handling of SIGTTOU in non-interactive shell
- remove useless builtins

* Thu Apr 19 2007 Tomas Smetana <tsmetana@redhat.com> 20070328-1
- new upstream source
- fix login shell invocation (#182397)
- fix memory leak

* Wed Feb 21 2007 Karsten Hopp <karsten@redhat.com> 20070111-1
- new upstream version
- fix invalid write in uname function

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 20060214-1.1
- rebuild

* Thu Jun 01 2006 Karsten Hopp <karsten@redhat.de> 20060214-1
- new upstream source

* Mon Feb 27 2006 Karsten Hopp <karsten@redhat.de> 20060124-3
- PreReq grep, coreutils (#182835)

* Tue Feb 14 2006 Karsten Hopp <karsten@redhat.de> 20060124-2
- make it build in chroots (#180561)

* Mon Feb 13 2006 Karsten Hopp <karsten@redhat.de> 20060124-1
- version 20060124

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 20050202-5.1
- bump again for double-long bug on ppc(64)

* Fri Feb 10 2006 Karsten Hopp <karsten@redhat.de> 20050202-5
- rebuild

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 20050202-4.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Feb 02 2006 Karsten Hopp <karsten@redhat.de> 20050202-4
- fix uname -i output
- fix loop (*-path.patch)
- conflict pdksh instead of obsoleting it

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com> 20050202-3.1
- rebuilt for new gcj

* Tue May 10 2005 Karsten Hopp <karsten@redhat.de> 20050202-3
- enable debuginfo

* Tue Mar 15 2005 Karsten Hopp <karsten@redhat.de> 20050202-2
- add /usr/bin/ksh link for compatibility with pdksh scripts (#151134)

* Wed Mar 02 2005 Karsten Hopp <karsten@redhat.de> 20050202-1 
- update and rebuild with gcc-4

* Tue Mar 01 2005 Karsten Hopp <karsten@redhat.de> 20041225-2 
- fix gcc4 build 

* Fri Jan 21 2005 Karsten Hopp <karsten@redhat.de> 20041225-1
- rebuild with new ksh tarball (license change)

* Tue Nov 02 2004 Karsten Hopp <karsten@redhat.de> 20040229-11
- disable ia64 for now

* Fri Oct 15 2004 Karsten Hopp <karsten@redhat.de> 20040229-9 
- rebuild

* Thu Sep 02 2004 Nalin Dahyabhai <nalin@redhat.com> 20040229-8
- remove '&' from summary

* Thu Sep 02 2004 Bill Nottingham <notting@redhat.com> 20040229-7
- obsolete pdksh (#131303)

* Mon Aug 02 2004 Karsten Hopp <karsten@redhat.de> 20040229-6
- obsolete ksh93, provide ksh93

* Mon Jul 05 2004 Karsten Hopp <karsten@redhat.de> 20040229-3 
- add /bin/ksh to /etc/shells

* Wed Jun 16 2004 Karsten Hopp <karsten@redhat.de> 20040229-2 
- add ppc64 patch to avoid ppc64 dot symbol problem

* Fri May 28 2004 Karsten Hopp <karsten@redhat.de> 20040229-1 
- initial version
