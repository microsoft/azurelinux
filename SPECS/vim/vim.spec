%define debug_package %{nil}
Summary:        Text editor
Name:           vim
Version:        9.0.2010
Release:        1%{?dist}
License:        Vim
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/Editors
URL:            https://www.vim.org
Source0:        https://github.com/%{name}/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  ncurses-devel
BuildRequires:  python3-devel
Requires(post): sed
Provides:       vi = %{version}-%{release}
Provides:       %{name}-minimal = %{version}-%{release}

%description
The Vim package contains a powerful text editor.

%package        extra
Summary:        Extra files for Vim text editor
Group:          Applications/Editors
Requires:       %{name} = %{version}-%{release}
Requires:       tcsh
Conflicts:      toybox

%description extra
The vim extra package contains a extra files for powerful text editor.

%prep
%autosetup -p1
echo '#define SYS_VIMRC_FILE "%{_sysconfdir}/vimrc"' >> src/feature.h
%py3_shebang_fix runtime/tools/demoserver.py

%build
%configure --enable-multibyte
%make_build

%install
%make_install
ln -sv vim %{buildroot}%{_bindir}/vi
install -vdm 755 %{buildroot}%{_sysconfdir}
cat > %{buildroot}%{_sysconfdir}/vimrc << "EOF"
" Begin %{_sysconfdir}/vimrc

set shell=/bin/bash
set nocompatible
set backspace=2
set ruler
syntax on
set tags=./tags;/
color desert
if (&term == "iterm") || (&term == "putty")
  set background=dark
endif
" Binds
nmap <F2> :w<CR>
imap <F2> <Esc>:w<CR>
nmap <F10> :q!<CR>
nmap <Esc><Esc> :q<CR>
" Use 4 space characters instead of tab for python files
au BufEnter,BufNew *.py set tabstop=4 shiftwidth=4 expandtab
" Move the swap file location to protect against CVE-2017-1000382
" More information at http://security.cucumberlinux.com/security/details.php?id=120
if ! isdirectory("~/.vim/swap/")
        call system('install -d -m 700 ~/.vim/swap')
endif
set directory=~/.vim/swap/
" End %{_sysconfdir}/vimrc
EOF

%check
sed -i '/source test_recover.vim/d' src/testdir/test_alot.vim
sed -i '916d' src/testdir/test_search.vim
sed -i '454,594d' src/testdir/test_autocmd.vim
sed -i '1,9d' src/testdir/test_modeline.vim
sed -i '133d' ./src/testdir/Make_all.mak
%make_build test

%post
if ! sed -n -e '0,/[[:space:]]*call[[:space:]]\+system\>/p' %{_sysconfdir}/vimrc | \
     grep -q '^[[:space:]]*set[[:space:]]\+shell=/bin/bash'; then
  sed -i -e 's#^\([[:space:]]*\)\(call[[:space:]]\+system.*\)$#\1set shell=/bin/bash\n\1\2#g' %{_sysconfdir}/vimrc
fi

%files extra
%license README.txt
%doc %{_datarootdir}/vim/vim*/doc/*
%defattr(-,root,root)
%{_bindir}/vimtutor
%{_bindir}/xxd
%{_mandir}/*/*
%{_datarootdir}/vim/vim*/autoload/*
%{_datarootdir}/vim/vim*/bugreport.vim
%{_datarootdir}/vim/vim*/colors/*
%exclude %{_datarootdir}/vim/vim*/colors/desert.vim
%exclude %{_datarootdir}/vim/vim*/colors/lists/default.vim
%{_datarootdir}/applications/gvim.desktop
%{_datarootdir}/applications/vim.desktop
%{_datarootdir}/icons/hicolor/48x48/apps/gvim.png
%{_datarootdir}/icons/locolor/16x16/apps/gvim.png
%{_datarootdir}/icons/locolor/32x32/apps/gvim.png
%{_datarootdir}/vim/vim*/pack/dist/opt/*
%{_datarootdir}/vim/vim*/compiler/*
%{_datarootdir}/vim/vim*/delmenu.vim
%{_datarootdir}/vim/vim*/evim.vim
%{_datarootdir}/vim/vim*/ftoff.vim
%{_datarootdir}/vim/vim*/ftplugin.vim
%{_datarootdir}/vim/vim*/ftplugin/*
%{_datarootdir}/vim/vim*/ftplugof.vim
%{_datarootdir}/vim/vim*/gvimrc_example.vim
%{_datarootdir}/vim/vim*/import/dist/vimhelp.vim
%{_datarootdir}/vim/vim*/import/dist/vimhighlight.vim
%{_datarootdir}/vim/vim*/indent.vim
%{_datarootdir}/vim/vim*/indent/*
%{_datarootdir}/vim/vim*/indoff.vim
%{_datarootdir}/vim/vim*/keymap/*
%{_datarootdir}/vim/vim*/macros/*
%{_datarootdir}/vim/vim*/menu.vim
%{_datarootdir}/vim/vim*/mswin.vim
%{_datarootdir}/vim/vim*/optwin.vim
%{_datarootdir}/vim/vim*/plugin/*
%{_datarootdir}/vim/vim*/synmenu.vim
%{_datarootdir}/vim/vim*/vimrc_example.vim
%{_datarootdir}/vim/vim*/print/*
%{_datarootdir}/vim/vim*/scripts.vim
%{_datarootdir}/vim/vim*/spell/*
%{_datarootdir}/vim/vim*/syntax/*
%exclude %{_datarootdir}/vim/vim90/syntax/nosyntax.vim
%exclude %{_datarootdir}/vim/vim90/syntax/syntax.vim
%exclude %{_datarootdir}/vim/vim90/autoload/dist/ft.vim
%{_datarootdir}/vim/vim*/tools/*
%{_datarootdir}/vim/vim*/tutor/*
%{_datarootdir}/vim/vim*/lang/*.vim
%doc %{_datarootdir}/vim/vim*/lang/*.txt
%lang(af) %{_datarootdir}/vim/vim*/lang/af/LC_MESSAGES/vim.mo
%lang(ca) %{_datarootdir}/vim/vim*/lang/ca/LC_MESSAGES/vim.mo
%lang(cs) %{_datarootdir}/vim/vim*/lang/cs/LC_MESSAGES/vim.mo
%lang(de) %{_datarootdir}/vim/vim*/lang/de/LC_MESSAGES/vim.mo
%lang(eb_GB) %{_datarootdir}/vim/vim*/lang/en_GB/LC_MESSAGES/vim.mo
%lang(eo) %{_datarootdir}/vim/vim*/lang/eo/LC_MESSAGES/vim.mo
%lang(es) %{_datarootdir}/vim/vim*/lang/es/LC_MESSAGES/vim.mo
%lang(fi) %{_datarootdir}/vim/vim*/lang/fi/LC_MESSAGES/vim.mo
%lang(fr) %{_datarootdir}/vim/vim*/lang/fr/LC_MESSAGES/vim.mo
%lang(ga) %{_datarootdir}/vim/vim*/lang/ga/LC_MESSAGES/vim.mo
%lang(it) %{_datarootdir}/vim/vim*/lang/it/LC_MESSAGES/vim.mo
%lang(ja) %{_datarootdir}/vim/vim*/lang/ja/LC_MESSAGES/vim.mo
%lang(ko.UTF-8) %{_datarootdir}/vim/vim*/lang/ko.UTF-8/LC_MESSAGES/vim.mo
%lang(ko) %{_datarootdir}/vim/vim*/lang/ko/LC_MESSAGES/vim.mo
%lang(nb) %{_datarootdir}/vim/vim*/lang/nb/LC_MESSAGES/vim.mo
%lang(no) %{_datarootdir}/vim/vim*/lang/no/LC_MESSAGES/vim.mo
%lang(pl) %{_datarootdir}/vim/vim*/lang/pl/LC_MESSAGES/vim.mo
%lang(pt_BR) %{_datarootdir}/vim/vim*/lang/pt_BR/LC_MESSAGES/vim.mo
%lang(ru) %{_datarootdir}/vim/vim*/lang/ru/LC_MESSAGES/vim.mo
%lang(sk) %{_datarootdir}/vim/vim*/lang/sk/LC_MESSAGES/vim.mo
%lang(sv) %{_datarootdir}/vim/vim*/lang/sv/LC_MESSAGES/vim.mo
%lang(uk) %{_datarootdir}/vim/vim*/lang/uk/LC_MESSAGES/vim.mo
%lang(da) %{_datarootdir}/vim/vim*/lang/da/LC_MESSAGES/vim.mo
%lang(lv) %{_datarootdir}/vim/vim*/lang/lv/LC_MESSAGES/vim.mo
%lang(sr) %{_datarootdir}/vim/vim*/lang/sr/LC_MESSAGES/vim.mo
%lang(tr) %{_datarootdir}/vim/vim*/lang/tr/LC_MESSAGES/vim.mo
%lang(vi) %{_datarootdir}/vim/vim*/lang/vi/LC_MESSAGES/vim.mo
%lang(zh_CN.UTF-8) %{_datarootdir}/vim/vim*/lang/zh_CN.UTF-8/LC_MESSAGES/vim.mo
%lang(zh_CN) %{_datarootdir}/vim/vim*/lang/zh_CN/LC_MESSAGES/vim.mo
%lang(zh_TW.UTF-8) %{_datarootdir}/vim/vim*/lang/zh_TW.UTF-8/LC_MESSAGES/vim.mo
%lang(zh_TW) %{_datarootdir}/vim/vim*/lang/zh_TW/LC_MESSAGES/vim.mo
%lang(cs.cp1250) %{_datarootdir}/vim/vim*/lang/cs.cp1250/LC_MESSAGES/vim.mo
%lang(ja.euc-jp) %{_datarootdir}/vim/vim*/lang/ja.euc-jp/LC_MESSAGES/vim.mo
%lang(ja.sjis) %{_datarootdir}/vim/vim*/lang/ja.sjis/LC_MESSAGES/vim.mo
%lang(nl) %{_datarootdir}/vim/vim*/lang/nl/LC_MESSAGES/vim.mo
%lang(pl.UTF-8) %{_datarootdir}/vim/vim*/lang/pl.UTF-8/LC_MESSAGES/vim.mo
%lang(pl.cp1250) %{_datarootdir}/vim/vim*/lang/pl.cp1250/LC_MESSAGES/vim.mo
%lang(ru.cp1251) %{_datarootdir}/vim/vim*/lang/ru.cp1251/LC_MESSAGES/vim.mo
%lang(sk.cp1250) %{_datarootdir}/vim/vim*/lang/sk.cp1250/LC_MESSAGES/vim.mo
%lang(uk.cp1251) %{_datarootdir}/vim/vim*/lang/uk.cp1251/LC_MESSAGES/vim.mo
%lang(zh_CN.cp936) %{_datarootdir}/vim/vim*/lang/zh_CN.cp936/LC_MESSAGES/vim.mo

%files
%defattr(-,root,root)
%license README.txt runtime/doc/uganda.txt
%config(noreplace) %{_sysconfdir}/vimrc
%{_datarootdir}/vim/vim*/syntax/syntax.vim
%{_datarootdir}/vim/vim*/colors/desert.vim
%{_datarootdir}/vim/vim*/colors/lists/default.vim
%{_datarootdir}/vim/vim*/defaults.vim
%{_datarootdir}/vim/vim*/filetype.vim
%{_datarootdir}/vim/vim90/syntax/nosyntax.vim
%{_datarootdir}/vim/vim90/autoload/dist/ft.vim
%{_bindir}/ex
%{_bindir}/vi
%{_bindir}/view
%{_bindir}/rvim
%{_bindir}/rview
%{_bindir}/vim
%{_bindir}/vimdiff

%changelog
* Tue Oct 17 2023 Neha Agarwal <nehaagarwal@microsoft.com> - 9.0.2010-1
- Update version to 9.0.2010 to fix CVE-2023-5535.
- Remove patches that no longer apply in the new version.
- Remove file listed twice.

* Wed Oct 11 2023 Mykhailo Bykhovtsev <mbykhovtsev@microsft.com> - 9.0.1897-3
- Patch CVE-2023-5441

* Mon Oct 09 2023 Mitch Zhu <mitchzhu@microsoft.com> - 9.0.1897-2
- Patch CVE-2023-5344

* Tue Sep 12 2023 Henry Li <lihl@microsoft.com> - 9.0.1897-1
- Upgrade version to resolve CVE-2023-4738, CVE-2023-4750, CVE-2023-4781,
  CVE-2023-4752 and CVE-2023-4733

* Thu Sep 07 2023 Brian Fjeldstad <bfjelds@microsoft.com> - 9.0.1847-1
- Bump version to address CVE-2023-4734 CVE-2023-4735 CVE-2023-4736

* Wed Aug 16 2023 Bala <balakumaran.kannan@microsoft.com> - 9.0.1562-2
- Patch CVE-2023-3896

* Wed May 17 2023 Muhammad Falak <mwani@microsoft.com> - 9.0.1562-1
- Bump version to address CVE-2023-2609 & CVE-2023-2610

* Mon May 08 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 9.0.1527-1
- Auto-upgrade to 9.0.1527 - Fix CVE-2023-2426

* Thu Mar 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 9.0.1402-1
- Auto-upgrade to 9.0.1402 - fix CVE-2023-1355, CVE-2023-1264

* Fri Mar 10 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 9.0.1378-1
- Auto-upgrade to 9.0.1378 - to fix CVE-2023-1175

* Thu Mar 09 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 9.0.1367-1
- Auto-upgrade to 9.0.1367 - to fix CVE-2023-1127

* Wed Feb 08 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 9.0.1247-1
- Auto-upgrade to 9.0.1247 - to fix CVE-2023-0512

* Mon Feb 06 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 9.0.1225-1
- Auto-upgrade to 9.0.1225 - to fix CVE-2023-0433

* Mon Jan 23 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 9.0.1189-1
- Auto-upgrade to 9.0.1189 - to fix CVE-2023-0288

* Tue Jan 17 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 9.0.1145-1
- Auto-upgrade to 9.0.1145 - to fix CVE-2023-0049, CVE-2023-0051, CVE-2023-0054

* Thu Dec 01 2022 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 9.0.0982-1
- Auto-upgrade to 9.0.0982 - CVE-2022-4141

* Sun Oct 30 2022 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 9.0.0805-1
- Upgrade to 9.0.0805

* Tue Oct 04 2022 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 9.0.0614-1
- Upgrade to 9.0.0614

* Fri Sep 30 2022 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 9.0.0598-1
- Upgrade to 9.0.0598

* Thu Sep 22 2022 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 9.0.0490-1
- Upgrade to 9.0.0490

* Thu Sep 15 2022 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 9.0.0404-1
- Upgrade to 9.0.0404

* Mon Aug 29 2022 Henry Beberman <henry.beberman@microsoft.com> - 9.0.0325-1
- Upgrade to 9.0.0325 to fix: CVE-2022-2980, CVE-2022-2982, CVE-2022-2923, CVE-2022-2946

* Fri Aug 19 2022 Andrew Phelps <anphel@microsoft.com> - 9.0.0232-1
- Upgrade to 9.0.0232 to fix: CVE-2022-2522, CVE-2022-2571, CVE-2022-2580, CVE-2022-2581,
  CVE-2022-2598, CVE-2022-2816, CVE-2022-2817, CVE-2022-2819, CVE-2022-2845, CVE-2022-2849,
  CVE-2022-2862, CVE-2022-2874, CVE-2022-2889

* Mon Jul 18 2022 Aadhar Agarwal <aadagarwal@microsoft.com> - 9.0.0050-2
- Add sed requires as vim has an implicit dependency on sed in the post-install script.

* Tue Jul 12 2022 Mandeep Plaha <mandeepplaha@microsoft.com> - 9.0.0050-1
- Upgrade to 9.0.0050 to fix CVEs: 2022-2257, 2022-2264, 2022-2284, 2022-2285, 2022-2286, 2022-2287

* Tue Jul 12 2022 Olivia Crain <oliviacrain@microsoft.com> - 8.2.5172-2
- Fix unversioned python shebang in demoserver.py example script

* Thu Jun 30 2022 Daniel McIlvaney <damcilva@microsoft.com> - 8.2.5172-1
- Upgrade to 8.2.5172 to fix CVE-2022-2175, CVE-2022-2182

* Tue Jun 28 2022 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 8.2.5154-1
- Upgrade to 8.2.5154 to fix CVEs: 2022-2124, 2022-2125, 2022-2126 and 2022-2129

* Mon Jun 06 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 8.2.5064-1
- Update to version 8.2.5064 to fix CVEs: 2022-1851, 2022-1886, and 2022-1898.

* Fri May 27 2022 Max Brodeur-Urbas <maxbr@microsoft.com> - 8.2.4979-1
- Update version to 8.2.4979 to fix CVE-2022-1619, CVE-2022-1621, CVE-2022-1629, 
  CVE-2022-1616, CVE-2022-1733, CVE-2022-1735, CVE-2022-1769, CVE-2022-1620, 
  CVE-2022-1674, CVE-2022-1771, CVE-2022-1785, CVE-2022-1796.

* Fri May 20 2022 Chris Co <chrco@microsoft.com> - 8.2.4925-1
- Update version to 8.2.4925 to address CVE-2022-1381, CVE-2022-1420,
  CVE-2022-1616, CVE-2022-1619, CVE-2022-1620, CVE-2022-1621, CVE-2022-1629
- Add new file vimhelp.vim

* Fri Apr 22 2022 Olivia Crain <oliviacrain@microsoft.com> - 8.2.4743-2
- Fix invalid vi provide with reversed %%{release}-%%{version} EVR

* Tue Apr 12 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 8.2.4743-1
- Update version to 8.2.4743 to fix CVE-2022-0408,CVE-2022-0413,CVE-2022-0417,CVE-2022-0443,
- CVE-2022-0554,CVE-2022-0572,CVE-2022-0629,CVE-2022-0685,CVE-2022-0729,CVE-2022-1160

* Thu Feb 03 2022 Chris Co <chrco@microsoft.com> - 8.2.4233-1
- Update version to 8.2.4233 to fix CVE-2022-0392,CVE-2022-0393,CVE-2022-0359,CVE-2022-0361,CVE-2022-0368

* Mon Jan 31 2022 Chris Co <chrco@microsoft.com> - 8.2.4151-1
- Update version to 8.2.4151 to fix CVE-2022-0318.

* Wed Jan 26 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 8.2.4120-1
- Update version to 8.2.4120 to fix CVE-2022-0261.

* Thu Jan 13 2022 Rachel Menge <rachelmenge@microsoft.com> - 8.2.4081-1
- Update version to 8.2.4081 to fix CVE-2022-0128.

* Thu Jan 06 2022 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 8.2.4006-1
- Update version to 8.2.4006 to fix CVE CVE-2021-4166.

* Tue Dec 28 2021 Henry Beberman <henry.beberman@microsoft.com> - 8.2.3668-4
- Backported patch for CVE-2021-4136 from upstream

* Wed Dec 08 2021 Mariner Autopatcher <cblmargh@microsoft.com> - 8.2.3668-3
- Added patch file(s) CVE-2021-4069.patch

* Sat Dec 04 2021 Mariner Autopatcher <cblmargh@microsoft.com> - 8.2.3668-2
- Added patch file(s) CVE-2021-4019.patch

* Thu Nov 25 2021 Muhammad Falak <mwani@microsoft.com> - 8.2.3668-1
- Bump version to 8.2.3668 to fix CVE-2021-3968,CVE-2021-3973,CVE-2021-3974

* Wed Nov 10 2021 Nick Samson <nisamson@microsoft.com> - 8.2.3582-1
- Upgrade to 8.2.3582 to fix CVE-2021-3927 and CVE-2021-3928

* Fri Nov 05 2021 Thomas Crain <thcrain@microsoft.com> - 8.2.3564-2
- Package default color list in main package for use by default theme

* Wed Nov 03 2021 Thomas Crain <thcrain@microsoft.com> - 8.2.3564-1
- Upgrade to 8.2.3564 to fix CVE-2021-3903
- Package actual license text
- License verified
- Remove rgb.txt from packaging- removed in patch level 3562
- Use make macros

* Tue Oct 26 2021 Chris Co <chrco@microsoft.com> - 8.2.3489-1
- Fix CVE-2021-3875 and CVE-2021-3872 by updated to 8.2.3489

* Tue Oct 05 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 8.2.3441-2
- Fix vim startup error.
- vim-extra requires vim and fix for make check failure.

* Mon Sep 27 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 8.2.3441-1
- Fix CVE-2021-3778 and CVE-2021-3796 CVEs by updating to 8.2.3441.

* Fri Oct 30 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 8.1.1667-1
- Fix CVE-2019-20807 by updating to 8.1.1667.

* Thu Oct 15 2020 Emre Girgin <mrgirgin@microsoft.com> - 8.1.0388-7
- Fix CVE-2019-12735.

* Mon Jun 01 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 8.1.0388-6
- Adding a license reference.

* Mon Apr 13 2020 Eric Li <eli@microsoft.com> - 8.1.0388-5
- Add #Source0: comment and delete sha1. Verified license.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 8.1.0388-4
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue Jan 29 2019 Dweep Advani <dadvani@vmware.com> - 8.1.0388-3
- Fixed swap file creation error for custom login shell

* Wed Sep 12 2018 Anish Swaminathan <anishs@vmware.com> - 8.1.0388-2
- Add conflicts toybox for vim-extra.

* Wed Sep 12 2018 Anish Swaminathan <anishs@vmware.com> - 8.1.0388-1
- Update to version 8.1.0388.

* Tue Jul 10 2018 Tapas Kundu <tkundu@vmware.com> - 8.0.0533-4
- Fix for CVE-2017-17087 and CVE-2017-1000382.

* Mon Aug 14 2017 Chang Lee <changlee@vmware.com> - 8.0.0533-3
- Disabled Test_recover_root_dir in %check.

* Tue May 02 2017 Anish Swaminathan <anishs@vmware.com> - 8.0.0533-2
- Remove tcsh requires.

* Fri Apr 14 2017 Xiaolin Li <xiaolinl@vmware.com> - 8.0.0533-1
- Updated to version 8.0.0533.

* Tue Feb 28 2017 Anish Swaminathan <anishs@vmware.com> - 7.4-10
- Fix for CVE-2017-6349 and CVE-2017-6350.

* Fri Feb 17 2017 Anish Swaminathan <anishs@vmware.com> - 7.4-9
- Fix for CVE-2017-5953.

* Fri Nov 18 2016 Anish Swaminathan <anishs@vmware.com> - 7.4-8
- Fix for CVE-2016-1248.

* Wed Oct 05 2016 ChangLee <changlee@vmware.com> - 7.4-7
- Modified %check.

* Wed Aug 24 2016 Alexey Makhalov <amakhalov@vmware.com> - 7.4-6
- vimrc: Added tags search, tab->spaces and some bindings.

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 7.4-5
- GA - Bump release of all rpms.

* Thu Jul 16 2015 Touseef Liaqat <tliaqat@vmware.com> - 7.4-3
- Added profile related files in minimal vim package.

* Tue Jun 30 2015 Touseef Liaqat <tliaqat@vmware.com> - 7.4-3
- Pack extra files separately, to make vim package small.

* Fri Jun 19 2015 Alexey Makhalov <amakhalov@vmware.com> - 7.4-2
- Disable debug package. Use 'desert' colorscheme.

* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> - 7.4-1
- Initial build First version.
