Vendor:         Microsoft Corporation
Distribution:   Mariner
%global macrosdir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)
# We'd like to be noarch, but Lmod encodes the system lua path
%global debug_package %{nil}

Name:           Lmod
Version:        8.2.10
Release:        4%{?dist}
Summary:        Environmental Modules System in Lua
AutoReq:        0

# Lmod-5.3.2/tools/base64.lua is LGPLv2
License:        MIT and LGPLv2
URL:            https://www.tacc.utexas.edu/tacc-projects/lmod
Source0:        https://github.com/TACC/Lmod/archive/%{version}/Lmod-%{version}.tar.gz
Source1:        macros.%{name}

# redirect more echo stmts to stderr in init/bash.in
# Having them go to stdout breaks openQA tests when Lmod is installed
# https://github.com/TACC/Lmod/pull/435
Patch0:         435.patch

BuildRequires:  gcc
BuildRequires:  lua-devel
BuildRequires:  lua-filesystem
BuildRequires:  lua-json
BuildRequires:  lua-posix
BuildRequires:  lua-term
BuildRequires:  tcl-devel
BuildRequires:  zsh
Requires:       lua-filesystem
Requires:       lua-json
Requires:       lua-posix
Requires:       lua-term
Requires:       /bin/ps
Requires:       tcl-devel
Requires(post): coreutils
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives
Provides:       environment(modules)

%description
Lmod is a Lua based module system that easily handles the MODULEPATH
Hierarchical problem.  Environment Modules provide a convenient way to
dynamically change the users' environment through modulefiles. This includes
easily adding or removing directories to the PATH environment variable.
Modulefiles for library packages provide environment variables that specify
where the library and header files can be found.


%prep
%setup -q
%patch0 -p1
sed -i -e 's,/usr/bin/env ,/usr/bin/,' src/*.tcl
# Remove bundled lua-filesystem and lua-term
rm -r pkgs/{luafilesystem,term} tools/json.lua
#sed -i -e 's, pkgs , ,' Makefile.in
# Remove unneeded shbangs
sed -i -e '/^#!/d' init/*.in


%build
%configure --prefix=%{_datadir} PS=/bin/ps
%make_build


%install
%make_install
# init scripts are sourced
find %{buildroot}%{_datadir}/lmod/%{version}/init -type f -exec chmod -x {} +
mkdir -p %{buildroot}%{_sysconfdir}/modulefiles
mkdir -p %{buildroot}%{_datadir}/modulefiles
mkdir -p %{buildroot}%{_sysconfdir}/profile.d
# Setup for alternatives on Fedora
touch %{buildroot}%{_sysconfdir}/profile.d/modules.{csh,sh}

# Fedora defaults
cat <<'EOF' > %{buildroot}%{_sysconfdir}/profile.d/00-modulepath.sh
[ -z "$MODULEPATH" ] &&
  [ "$(readlink /etc/alternatives/modules.sh)" = "/usr/share/lmod/lmod/init/profile" -o -f /etc/profile.d/z00_lmod.sh ] &&
  export MODULEPATH=%{_sysconfdir}/modulefiles:%{_datadir}/modulefiles || :
EOF

cat << 'EOF' > %{buildroot}%{_sysconfdir}/profile.d/00-modulepath.csh
if (! $?MODULEPATH && ( `readlink /etc/alternatives/modules.csh` == /usr/share/lmod/lmod/init/cshrc || -f /etc/profile.d/z00_lmod.csh ) ) then
  setenv MODULEPATH %{_sysconfdir}/modulefiles:%{_datadir}/modulefiles
endif
EOF

# Add a snippet to make sure that the 00-modulepath.* is included, when
# the user calls /etc/profile.d/modules.sh directly, just below
# the shbang line.
sed -i '2i\. /etc/profile.d/00-modulepath.sh\n' \
  %{buildroot}%{_datadir}/lmod/lmod/init/profile

%if 0%{?rhel} && 0%{?rhel} < 8
# Install profile links to override environment-modules
ln -s %{_datadir}/lmod/lmod/init/profile %{buildroot}%{_sysconfdir}/profile.d/z00_lmod.sh
ln -s %{_datadir}/lmod/lmod/init/cshrc %{buildroot}%{_sysconfdir}/profile.d/z00_lmod.csh
%endif
# Install the rpm config file
install -Dpm 644 %{SOURCE1} %{buildroot}/%{macrosdir}/macros.%{name}
# TODO - contrib


%post
# Cleanup from pre-alternatives
[ ! -L %{_sysconfdir}/profile.d/modules.sh ] && rm -f %{_sysconfdir}/profile.d/modules.sh
%{_sbindir}/update-alternatives --install %{_sysconfdir}/profile.d/modules.sh modules.sh \
                                          %{_datadir}/lmod/lmod/init/profile 20 \
                                --slave %{_sysconfdir}/profile.d/modules.csh modules.csh \
                                        %{_datadir}/lmod/lmod/init/cshrc

%postun
if [ $1 -eq 0 ] ; then
  %{_sbindir}/update-alternatives --remove modules.sh %{_datadir}/lmod/lmod/init/profile
fi

%files
%license License
%doc INSTALL README.md README_lua_modulefiles.txt
%{_sysconfdir}/modulefiles
%config(noreplace) %{_sysconfdir}/profile.d/00-modulepath.csh
%config(noreplace) %{_sysconfdir}/profile.d/00-modulepath.sh
%ghost %{_sysconfdir}/profile.d/modules.csh
%ghost %{_sysconfdir}/profile.d/modules.sh
%{_datadir}/lmod
%{_datadir}/modulefiles
%{macrosdir}/macros.%{name}


%changelog
* Fri Jan 08 2021 Joe Schmitt <joschmit@microsoft.com> - 8.2.10-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Remove Fedora/RHEL version checks
- Add runtime dependency on tcl-devel.
- Turn off autoreq.

* Tue Feb 25 2020 Adam Williamson <awilliam@redhat.com> - 8.2.10-3
- Redirect echo stmts to stderr in init/bash.in (don't break openQA)

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 8.2.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Dec 17 2019 Orion Poplawski <orion@nwra.com> - 8.2.10-1
- Update to 8.2.10

* Thu Dec 05 2019 Orion Poplawski <orion@nwra.com> - 8.2.9-1
- Update to 8.2.9

* Tue Dec 03 2019 Orion Poplawski <orion@nwra.com> - 8.2.8-1
- Update to 8.2.8

* Sat Nov 30 2019 Orion Poplawski <orion@nwra.com> - 8.2.7-1
- Update to 8.2.7

* Fri Nov 29 2019 Orion Poplawski <orion@nwra.com> - 8.2.6-1
- Update to 8.2.6

* Mon Nov 25 2019 orion - 8.2.5-1
- Update to 8.2.5

* Fri Nov 15 2019 Orion Poplawski <orion@nwra.com> - 8.2.4-1
- Update to 8.2.4

* Tue Nov  5 2019 Orion Poplawski <orion@nwra.com> - 8.2.3-1
- Update to 8.2.3

* Fri Nov  1 2019 Orion Poplawski <orion@nwra.com> - 8.2.2-1
- Update to 8.2.2

* Thu Oct 31 2019 Orion Poplawski <orion@nwra.com> - 8.2-1
- Update to 8.2

* Wed Sep 25 2019 Orion Poplawski <orion@nwra.com> - 8.1.17-3
- Make 00-modulepath.sh return 0, but not exit (bugz#1755666)

* Wed Sep 25 2019 Orion Poplawski <orion@nwra.com> - 8.1.17-2
- Make 00-modulepath.sh return 0

* Tue Sep 24 2019 Orion Poplawski <orion@nwra.com> - 8.1.17-1
- Update to 8.1.17

* Sat Sep 21 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 8.1.10-3
- Make sure /etc/profile.d/modules.sh has $MODULEPATH (#1461656)

* Thu Aug 1 2019 Orion Poplawski <orion@nwra.com> - 8.1.10-2
- RHEL8 environment-modules uses alternatives

* Tue Jul 30 2019 Orion Poplawski <orion@nwra.com> - 8.1.10-1
- Update to 8.1.10

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 8.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat May 11 2019 Orion Poplawski <orion@nwra.com> - 8.1.3-1
- Update to 8.1.3

* Tue May 7 2019 Orion Poplawski <orion@nwra.com> - 8.1.0-1
- Update to 8.1.0

* Thu Apr 18 2019 Orion Poplawski <orion@nwra.com> - 8.0.6-1
- Update to 8.0.6

* Tue Apr 16 2019 Orion Poplawski <orion@nwra.com> - 8.0.5-1
- Update to 8.0.5

* Sat Apr 13 2019 Orion Poplawski <orion@nwra.com> - 8.0.4-1
- Update to 8.0.4

* Thu Apr  4 2019 Orion Poplawski <orion@nwra.com> - 8.0.1-1
- Update to 8.0.1

* Fri Feb 22 2019 Orion Poplawski <orion@cora.nwra.com> - 7.8.21-1
- Update to 7.8.21

* Sat Feb 9 2019 Orion Poplawski <orion@cora.nwra.com> - 7.8.17-1
- Update to 7.8.17

* Sat Feb 2 2019 Orion Poplawski <orion@cora.nwra.com> - 7.8.16-1
- Update to 7.8.16

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.8.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Nov 20 2018 Orion Poplawski <orion@cora.nwra.com> - 7.8.9-1
- Update to 7.8.9

* Fri Sep 28 2018 Orion Poplawski <orion@cora.nwra.com> - 7.8.6-1
- Update to 7.8.6, fixes bug #1594964

* Thu Sep 27 2018 Orion Poplawski <orion@cora.nwra.com> - 7.8.4-1
- Update to 7.8.4

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7.7.35-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 21 2018 Orion Poplawski <orion@cora.nwra.com> - 7.7.35-1
- Update to 7.7.35

* Wed Mar 7 2018 Orion Poplawski <orion@cora.nwra.com> - 7.7.18-1
- Update to 7.7.18
- Add BR gcc

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7.5.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.5.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.5.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 20 2017 Orion Poplawski <orion@cora.nwra.com> - 7.5.16-1
- Update to 7.5.16

* Tue Jun 20 2017 Orion Poplawski <orion@cora.nwra.com> - 7.5.3-1
- Update to 7.5.3

* Fri Jun 16 2017 Orion Poplawski <orion@cora.nwra.com> - 7.5-1
- Update to 7.5

* Mon Jun 12 2017 Orion Poplawski <orion@cora.nwra.com> - 7.4.20-1
- Update to 7.4.20

* Fri May 26 2017 Orion Poplawski <orion@cora.nwra.com> - 7.4.17-1
- Update to 7.4.17

* Mon May 22 2017 Orion Poplawski <orion@cora.nwra.com> - 7.4.15-1
- Update to 7.4.15

* Wed Apr 19 2017 Orion Poplawski <orion@cora.nwra.com> - 7.4.7-1
- Update to 7.4.7

* Thu Mar 23 2017 Orion Poplawski <orion@cora.nwra.com> - 7.4.1-1
- Update to 7.4.1

* Tue Mar 21 2017 Orion Poplawski <orion@cora.nwra.com> - 7.4-1
- Update to 7.4

* Tue Feb 28 2017 Orion Poplawski <orion@cora.nwra.com> - 7.3.20-1
- Update to 7.3.20

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.3.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 26 2017 Orion Poplawski <orion@cora.nwra.com> - 7.3.10-1
- Update to 7.3.10

* Fri Jan 20 2017 Orion Poplawski <orion@cora.nwra.com> - 7.3.6-1
- Update to 7.3.6

* Fri Jan 13 2017 Orion Poplawski <orion@cora.nwra.com> - 7.3.2-1
- Update to 7.3.2

* Thu Jan 12 2017 Orion Poplawski <orion@cora.nwra.com> - 7.3-1
- Update to 7.3

* Mon Jan 9 2017 Orion Poplawski <orion@cora.nwra.com> - 7.2.2-1
- Update to 7.2.2

* Fri Jan 6 2017 Orion Poplawski <orion@cora.nwra.com> - 7.2.1-1
- Update to 7.2.1

* Tue Dec 6 2016 Orion Poplawski <orion@cora.nwra.com> - 7.1.4-1
- Update to 7.1.4

* Thu Dec 1 2016 Orion Poplawski <orion@cora.nwra.com> - 7.1-1
- Update to 7.1

* Sun Nov 13 2016 Orion Poplawski <orion@cora.nwra.com> - 7.0-1
- Update to 7.0

* Sat Oct 15 2016 Orion Poplawski <orion@cora.nwra.com> - 6.6-1
- Update to 6.6

* Tue Oct 11 2016 Orion Poplawski <orion@cora.nwra.com> - 6.5.17-1
- Update to 6.5.17

* Wed Oct 5 2016 Orion Poplawski <orion@cora.nwra.com> - 6.5.16-1
- Update to 6.5.16

* Mon Sep 26 2016 Orion Poplawski <orion@cora.nwra.com> - 6.5.13-1
- Update to 6.5.13

* Wed Sep 7 2016 Orion Poplawski <orion@cora.nwra.com> - 6.5.10-1
- Update to 6.5.10

* Tue Sep 6 2016 Orion Poplawski <orion@cora.nwra.com> - 6.5.8-1
- Update to 6.5.8

* Thu Sep 1 2016 Orion Poplawski <orion@cora.nwra.com> - 6.5.5-1
- Update to 6.5.5

* Wed Aug 31 2016 Orion Poplawski <orion@cora.nwra.com> - 6.5.4-1
- Update to 6.5.4

* Tue Aug 30 2016 Orion Poplawski <orion@cora.nwra.com> - 6.5.3-1
- Update to 6.5.3

* Mon Aug 29 2016 Orion Poplawski <orion@cora.nwra.com> - 6.5.2-1
- Update to 6.5.2

* Thu Aug 18 2016 Orion Poplawski <orion@cora.nwra.com> - 6.5.1-2
- Do not add Tcl environment-modules specific path to MODULEPATH
  (bug #1243030)

* Thu Aug 18 2016 Orion Poplawski <orion@cora.nwra.com> - 6.5.1-1
- Update to 6.5.1

* Tue Jul 26 2016 Orion Poplawski <orion@cora.nwra.com> - 6.4.4-1
- Update to 6.4.4

* Mon Jun 20 2016 Orion Poplawski <orion@cora.nwra.com> - 6.4.3-2
- Add needed requires on coreutils (#1348077)

* Fri Jun 17 2016 Orion Poplawski <orion@cora.nwra.com> - 6.4.3-1
- Update to 6.4.3

* Thu Jun 16 2016 Orion Poplawski <orion@cora.nwra.com> - 6.4.2-1
- Update to 6.4.2

* Mon Jun 6 2016 Orion Poplawski <orion@cora.nwra.com> - 6.4.1-1
- Update to 6.4.1

* Tue May 24 2016 Orion Poplawski <orion@cora.nwra.com> - 6.3.7-1
- Update to 6.3.7

* Mon May 23 2016 Orion Poplawski <orion@cora.nwra.com> - 6.3.6-1
- Update to 6.3.6

* Thu May 19 2016 Orion Poplawski <orion@cora.nwra.com> - 6.3.5-1
- Update to 6.3.5

* Wed May 11 2016 Orion Poplawski <orion@cora.nwra.com> - 6.3.4-1
- Update to 6.3.4 (fixes bug #1334529)

* Tue Apr 26 2016 Orion Poplawski <orion@cora.nwra.com> - 6.3.1-3
- Change ps path for EL6

* Tue Apr 26 2016 Orion Poplawski <orion@cora.nwra.com> - 6.3.1-2
- Fix ps requirement on EL6

* Mon Apr 25 2016 Orion Poplawski <orion@cora.nwra.com> - 6.3.1-1
- Update to 6.3.1
- Do not overwrite MODULEPATH (bug #1326075)

* Tue Apr 19 2016 Orion Poplawski <orion@cora.nwra.com> - 6.2.4-2
- Make arch specific package as Lmod now encodes the system lua path

* Tue Apr 19 2016 Orion Poplawski <orion@cora.nwra.com> - 6.2.4-1
- Update to 6.2.4

* Sun Apr 10 2016 Orion Poplawski <orion@cora.nwra.com> - 6.1.7-1
- Update to 6.1.7

* Tue Mar 22 2016 Orion Poplawski <orion@cora.nwra.com> - 6.1.5-1
- Update to 6.1.5

* Thu Feb 11 2016 Orion Poplawski <orion@cora.nwra.com> - 6.1.3-1
- Update to 6.1.3

* Wed Feb 10 2016 Orion Poplawski <orion@cora.nwra.com> - 6.1.2-1
- Update to 6.1.2

* Sat Feb 6 2016 Orion Poplawski <orion@cora.nwra.com> - 6.1-1
- Update to 6.1

* Fri Feb 5 2016 Orion Poplawski <orion@cora.nwra.com> - 6.0.29-1
- Update to 6.0.29

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Feb 1 2016 Orion Poplawski <orion@cora.nwra.com> - 6.0.26-1
- Update to 6.0.26

* Tue Jan 12 2016 Orion Poplawski <orion@cora.nwra.com> - 6.0.25-1
- Update to 6.0.25

* Tue Dec 22 2015 Orion Poplawski <orion@cora.nwra.com> - 6.0.24-2
- Add Requires: /usr/bin/ps

* Tue Dec 1 2015 Orion Poplawski <orion@cora.nwra.com> - 6.0.24-1
- Update to 6.0.24

* Wed Nov 25 2015 Orion Poplawski <orion@cora.nwra.com> - 6.0.22-1
- Update to 6.0.22

* Mon Nov 23 2015 Orion Poplawski <orion@cora.nwra.com> - 6.0.21-1
- Update to 6.0.21

* Fri Nov 20 2015 Orion Poplawski <orion@cora.nwra.com> - 6.0.20-1
- Update to 6.0.20

* Wed Nov 18 2015 Orion Poplawski <orion@cora.nwra.com> - 6.0.19-1
- Update to 6.0.19

* Mon Nov 16 2015 Orion Poplawski <orion@cora.nwra.com> - 6.0.18-1
- Update to 6.0.18

* Thu Nov 12 2015 Orion Poplawski <orion@cora.nwra.com> - 6.0.17-1
- Update to 6.0.17

* Wed Nov 11 2015 Orion Poplawski <orion@cora.nwra.com> - 6.0.16-1
- Update to 6.0.16

* Wed Oct 28 2015 Orion Poplawski <orion@cora.nwra.com> - 6.0.15-2
- Set PS path
- Add BR zsh

* Mon Oct 26 2015 Orion Poplawski <orion@cora.nwra.com> - 6.0.15-1
- Update to 6.0.15

* Wed Oct 21 2015 Orion Poplawski <orion@cora.nwra.com> - 6.0.12-2
- Mark 00-modulepath files as config

* Mon Oct 19 2015 Orion Poplawski <orion@cora.nwra.com> - 6.0.12-1
- Update to 6.0.12
- Drop shell patch fixed upstream

* Mon Oct 19 2015 Orion Poplawski <orion@cora.nwra.com> - 6.0.11-2
- Add patch to support generic and non-bash shells

* Tue Oct 6 2015 Orion Poplawski <orion@cora.nwra.com> - 6.0.11-1
- Update to 6.0.11

* Sun Sep 6 2015 Orion Poplawski <orion@cora.nwra.com> - 6.0.10-1
- Update to 6.0.10

* Wed Aug 12 2015 Orion Poplawski <orion@cora.nwra.com> - 6.0.9-1
- Update to 6.0.9

* Tue Jul 14 2015 Orion Poplawski <orion@cora.nwra.com> - 6.0.5-1
- Update to 6.0.5
- Drop tput patch applied upstream

* Mon Jul 13 2015 Orion Poplawski <orion@cora.nwra.com> - 6.0.4-1
- Update to 6.0.4

* Thu Jul 9 2015 Orion Poplawski <orion@cora.nwra.com> - 5.9.4.2-4
- Add patch to suppress tput output

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 26 2015 Orion Poplawski <orion@cora.nwra.com> - 5.9.4.2-2
- Fix alternatives script handling

* Tue May 19 2015 Orion Poplawski <orion@cora.nwra.com> - 5.9.4.2-1
- Update to 5.9.4.2

* Wed Apr 8 2015 Orion Poplawski <orion@cora.nwra.com> - 5.9.3-1
- Update to 5.9.3

* Tue Mar 31 2015 Orion Poplawski <orion@cora.nwra.com> - 5.9.2-1.git76a45db
- Update to 5.9.2-1.git76a45db for Lua 5.3 support

* Wed Mar 18 2015 Orion Poplawski <orion@cora.nwra.com> - 5.9-1
- Update to 5.9

* Tue Nov 4 2014 Orion Poplawski <orion@cora.nwra.com> - 5.8-1
- Update to 5.8

* Fri Sep 5 2014 Orion Poplawski <orion@cora.nwra.com> - 5.7.5-1
- Update to 5.7.5

* Wed Aug 20 2014 Orion Poplawski <orion@cora.nwra.com> - 5.7.4-1
- Update to 5.7.4

* Tue Aug 5 2014 Orion Poplawski <orion@cora.nwra.com> - 5.7.1-1
- Update to 5.7.1

* Thu Jun 26 2014 Orion Poplawski <orion@cora.nwra.com> - 5.6.2-1
- Update to 5.6.2

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Orion Poplawski <orion@cora.nwra.com> - 5.6-1
- Update to 5.6

* Mon May 5 2014 Orion Poplawski <orion@cora.nwra.com> - 5.5.1-1
- Update to 5.5.1

* Fri May 2 2014 Orion Poplawski <orion@cora.nwra.com> - 5.5-2
- Add EL support

* Thu May 1 2014 Orion Poplawski <orion@cora.nwra.com> - 5.5-1
- Update to 5.5

* Fri Apr 18 2014 Orion Poplawski <orion@cora.nwra.com> - 5.4.2-1
- Update to 5.4.2

* Mon Apr 14 2014 Orion Poplawski <orion@cora.nwra.com> - 5.4.1-1
- Update to 5.4.1

* Tue Apr  1 2014 Orion Poplawski <orion@cora.nwra.com> - 5.3.2-1
- Initial package
