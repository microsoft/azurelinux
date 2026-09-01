# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global erlang_minver 26.2
# We want to install into /usr/lib, even on 64-bit platforms
%global _rabbit_libdir %{_exec_prefix}/lib/rabbitmq
# Technically, we're noarch; but Elixir we're using is not.
%global debug_package %{nil}


Name: rabbitmq-server
Version: 4.0.7
Release: 5%{?dist}
License: MPL-2.0
Source0: https://github.com/rabbitmq/rabbitmq-server/releases/download/v%{version}/%{name}_%{version}.orig.tar.xz
Source1: https://github.com/rabbitmq/rabbitmq-server/releases/download/v%{version}/%{name}_%{version}.orig.tar.xz.asc
Source2: https://github.com/rabbitmq/signing-keys/releases/download/2.0/rabbitmq-release-signing-key.asc
# curl -O https://raw.githubusercontent.com/lemenkov/rabbitmq-server/cdfc661/packaging/RPMS/Fedora/rabbitmq-server.logrotate
Source3: rabbitmq-server.logrotate
# curl -O https://raw.githubusercontent.com/rabbitmq/rabbitmq-server-release/rabbitmq_v3_6_16/packaging/RPMS/Fedora/rabbitmq-server.tmpfiles
Source5: rabbitmq-server.tmpfiles
Source6: rabbitmq-server-cuttlefish
Patch1: rabbitmq-elixir-119.patch
Patch2: rabbitmq-server-0002-Use-default-EPMD-socket.patch
Patch3: rabbitmq-server-0003-Use-proto_dist-from-command-line.patch
Patch4: rabbitmq-server-0004-force-python3.patch
Patch5: rabbitmq-server-0005-Partially-revert-Use-template-in-rabbitmq-script-wra.patch

URL: https://www.rabbitmq.com/
BuildRequires: elixir
BuildRequires: erlang >= %{erlang_minver}
# for %%gpgverify
BuildRequires: gnupg2
BuildRequires: hostname
BuildRequires: libxslt
BuildRequires: make
BuildRequires: python3
BuildRequires: python3-simplejson
BuildRequires: rsync
BuildRequires: systemd
BuildRequires: xmlto
BuildRequires: zip
Requires: logrotate
Requires: erlang-erts%{?_isa} >= %{erlang_minver}
Requires: erlang-kernel%{?_isa} >= %{erlang_minver}
Requires: erlang-eldap%{?_isa} >= %{erlang_minver}
Requires: erlang-mnesia%{?_isa} >= %{erlang_minver}
Requires: erlang-os_mon%{?_isa} >= %{erlang_minver}
Requires: erlang-public_key%{?_isa} >= %{erlang_minver}
Requires: erlang-sasl%{?_isa} >= %{erlang_minver}
Requires: erlang-ssl%{?_isa} >= %{erlang_minver}
Requires: erlang-stdlib%{?_isa} >= %{erlang_minver}
Requires: erlang-syntax_tools%{?_isa} >= %{erlang_minver}
Requires: erlang-tools%{?_isa} >= %{erlang_minver}
Requires: erlang-xmerl%{?_isa} >= %{erlang_minver}
Summary: The RabbitMQ server
# Users and groups
Requires(pre): systemd
Requires(post): systemd
Requires(preun): systemd

%description
RabbitMQ is an implementation of AMQP, the emerging standard for high
performance enterprise messaging. The RabbitMQ server is a robust and
scalable implementation of an AMQP broker.

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -p1

# We have to remove it until common_test subpackage lands RHOS
rm -f \
	deps/amqp_client/src/rabbit_ct_client_helpers.erl \
	deps/rabbit_common/src/rabbit_ct_broker_helpers.erl \
	deps/rabbit_common/src/rabbit_ct_helpers.erl

# Create a sysusers.d config file
cat >rabbitmq-server.sysusers.conf <<EOF
u rabbitmq - 'RabbitMQ messaging server' %{_localstatedir}/lib/rabbitmq -
EOF

%build
#USE_SPECS="true" USE_PROPER_QC="false" make %%{?_smp_mflags}
make PROJECT_VERSION="%{version}" V=1  # Doesn't support %%{?_smp_mflags}


%install
make install \
	PROJECT_VERSION="%{version}" \
	DESTDIR=%{buildroot} \
	PREFIX=%{_prefix} \
	RMQ_ROOTDIR=%{_rabbit_libdir}

make install-man \
	PROJECT_VERSION="%{version}" \
	DESTDIR=%{buildroot} \
	PREFIX=%{_prefix} \
	RMQ_ROOTDIR=%{_rabbit_libdir}

mkdir -p %{buildroot}%{_localstatedir}/lib/rabbitmq/mnesia
mkdir -p %{buildroot}%{_localstatedir}/log/rabbitmq

#Copy all necessary lib files etc.
install -p -D -m 0644 ./deps/rabbit/docs/rabbitmq-server.service.example %{buildroot}%{_unitdir}/%{name}.service
install -p -D -m 0755 ./scripts/rabbitmq-script-wrapper %{buildroot}%{_sbindir}/rabbitmqctl
install -p -D -m 0755 ./scripts/rabbitmq-script-wrapper %{buildroot}%{_sbindir}/rabbitmq-server
install -p -D -m 0755 ./scripts/rabbitmq-script-wrapper %{buildroot}%{_sbindir}/rabbitmq-plugins
install -p -D -m 0755 ./scripts/rabbitmq-script-wrapper %{buildroot}%{_sbindir}/rabbitmq-diagnostics

# Make necessary symlinks
mkdir -p %{buildroot}%{_rabbit_libdir}/bin
for app in $(basename -a %{buildroot}%{_rabbit_libdir}/lib/rabbitmq_server-%{version}/sbin/*); do
       ln -s ../lib/rabbitmq_server-%{version}/sbin/${app} %{buildroot}%{_rabbit_libdir}/bin/${app}
done

install -p -D -m 0755 %{S:3} %{buildroot}%{_rabbit_libdir}/bin/cuttlefish

install -p -D -m 0755 scripts/rabbitmq-server.ocf %{buildroot}%{_exec_prefix}/lib/ocf/resource.d/rabbitmq/rabbitmq-server

install -p -D -m 0644 %{S:3} %{buildroot}%{_sysconfdir}/logrotate.d/rabbitmq-server

install -p -D -m 0644 ./deps/rabbit/docs/rabbitmq.conf.example %{buildroot}%{_sysconfdir}/rabbitmq/rabbitmq.conf

install -d %{buildroot}%{_localstatedir}/run/rabbitmq
install -p -D -m 0644 %{SOURCE5} %{buildroot}%{_prefix}/lib/tmpfiles.d/%{name}.conf
install -m0644 -D rabbitmq-server.sysusers.conf %{buildroot}%{_sysusersdir}/rabbitmq-server.conf


%check
#make check


%post
%systemd_post %{name}.service


%preun
# We do not remove /var/log and /var/lib directories
# Leave rabbitmq user and group
%systemd_preun %{name}.service

# Clean out plugin activation state, both on uninstall and upgrade
rm -rf %{_localstatedir}/lib/rabbitmq/plugins
rm -f %{_rabbit_libdir}/lib/rabbitmq_server-%{version}/ebin/rabbit.{rel,script,boot}


%postun
%systemd_postun_with_restart %{name}.service


%files
%dir %attr(0755, rabbitmq, rabbitmq) %{_sysconfdir}/rabbitmq
%config(noreplace) %attr(0644, rabbitmq, rabbitmq) %{_sysconfdir}/rabbitmq/rabbitmq.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/rabbitmq-server
%{_sbindir}/rabbitmqctl
%{_sbindir}/rabbitmq-server
%{_sbindir}/rabbitmq-plugins
%{_sbindir}/rabbitmq-diagnostics
%{_rabbit_libdir}/
%{_unitdir}/%{name}.service
# FIXME this should add dependency on "/usr/lib/ocf/resource.d/" owner
%dir /usr/lib/ocf/resource.d/rabbitmq/
/usr/lib/ocf/resource.d/rabbitmq/rabbitmq-server
%{_tmpfilesdir}/%{name}.conf
%dir %attr(0750, rabbitmq, rabbitmq) %{_localstatedir}/lib/rabbitmq
%dir %attr(0750, rabbitmq, rabbitmq) %{_localstatedir}/log/rabbitmq
%dir %attr(0755, rabbitmq, rabbitmq) %{_localstatedir}/run/rabbitmq
%license LICENSE LICENSE-*
%{_mandir}/man5/rabbitmq-env.conf.5*
%{_mandir}/man8/rabbitmq-diagnostics.8*
%{_mandir}/man8/rabbitmq-echopid.8*
%{_mandir}/man8/rabbitmq-plugins.8*
%{_mandir}/man8/rabbitmq-server.8*
%{_mandir}/man8/rabbitmq-service.8*
%{_mandir}/man8/rabbitmq-streams.8*
%{_mandir}/man8/rabbitmq-queues.8*
%{_mandir}/man8/rabbitmq-upgrade.8*
%{_mandir}/man8/rabbitmqctl.8*
%{_sysusersdir}/rabbitmq-server.conf


%changelog
* Tue Feb 10 2026 Stephen Gallagher <sgallagh@redhat.com> - 4.0.7-5
- Use PROJECT_VERSION instead of VERSION to set the internal version

* Wed Jan 28 2026 Stephen Gallagher <sgallagh@redhat.com> - 4.0.7-4
- Adapt the build to support Erlang 26.2

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Mar 10 2025 Zbigniew Jedrzejewski-Szmek  <zbyszek@in.waw.pl> - 4.0.7-2
- Add sysusers.d config file to allow rpm to create users/groups automatically

* Fri Feb 28 2025 Robert Scheck <robert@fedoraproject.org> - 4.0.7-1
- Ver. 4.0.7

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jan 02 2025 Richard W.M. Jones <rjones@redhat.com> - 4.0.5-2
- Remove downstream patch which allowed remote connections (RHBZ#2333072)
- Move license to MPL 2.0 (RHBZ#2333074)

* Wed Dec 18 2024 Robert Scheck <robert@fedoraproject.org> - 4.0.5-1
- Ver. 4.0.5

* Mon Dec 02 2024 Robert Scheck <robert@fedoraproject.org> - 4.0.4-1
- Ver. 4.0.4

* Sat Nov 09 2024 Robert Scheck <robert@fedoraproject.org> - 4.0.3-1
- Ver. 4.0.3

* Wed Oct 16 2024 Robert Scheck <robert@fedoraproject.org> - 4.0.2-1
- Ver. 4.0.2

* Wed Sep 04 2024 Miroslav Suchý <msuchy@redhat.com> - 3.13.7-2
- convert license to SPDX

* Tue Sep 03 2024 Robert Scheck <robert@fedoraproject.org> - 3.13.7-1
- Ver. 3.13.7

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.13.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri May 17 2024 John Eckersberg <jeckersb@redhat.com> - 3.13.2-1
- Ver. 3.13.2

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Dec 13 2023 Adam Williamson <awilliam@redhat.com> - 3.12.10-1
- Ver. 3.12.10

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.11.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Apr  3 2023 Peter Lemenkov <lemenkov@gmail.com> - 3.11.13-1
- Ver. 3.11.13

* Fri Mar 31 2023 Peter Lemenkov <lemenkov@gmail.com> - 3.11.12-1
- Ver. 3.11.12

* Mon Mar 20 2023 Peter Lemenkov <lemenkov@gmail.com> - 3.11.11-1
- Ver. 3.11.11

* Fri Mar  3 2023 Peter Lemenkov <lemenkov@gmail.com> - 3.11.10-1
- Ver. 3.11.10

* Sun Feb 12 2023 Peter Lemenkov <lemenkov@gmail.com> - 3.11.9-1
- Ver. 3.11.9

* Tue Jan 31 2023 Peter Lemenkov <lemenkov@gmail.com> - 3.11.8-1
- Ver. 3.11.8

* Wed Jan 18 2023 Peter Lemenkov <lemenkov@gmail.com> - 3.11.7-1
- Ver. 3.11.7

* Thu Jan  5 2023 Peter Lemenkov <lemenkov@gmail.com> - 3.11.6-1
- Ver. 3.11.6

* Wed Dec 14 2022 Peter Lemenkov <lemenkov@gmail.com> - 3.11.5-1
- Ver. 3.11.5

* Tue Dec 13 2022 Peter Lemenkov <lemenkov@gmail.com> - 3.10.13-1
- Ver. 3.10.13

* Wed Dec  7 2022 Peter Lemenkov <lemenkov@gmail.com> - 3.10.12-1
- Ver. 3.10.12

* Sun Oct  2 2022 Peter Lemenkov <lemenkov@gmail.com> - 3.10.8-1
- Ver. 3.10.8

* Mon Aug  8 2022 Peter Lemenkov <lemenkov@gmail.com> - 3.10.7-1
- Ver. 3.10.7

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 20 2022 Peter Lemenkov <lemenkov@gmail.com> - 3.10.6-1
- Ver. 3.10.6

* Tue Jul 12 2022 Peter Lemenkov <lemenkov@gmail.com> - 3.9.21-1
- Ver. 3.9.21

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Nov 22 2021 Peter Lemenkov <lemenkov@gmail.com> - 3.9.10-1
- Ver. 3.9.10

* Thu Nov 18 2021 Peter Lemenkov <lemenkov@gmail.com> - 3.9.8-3
- Added missing requires - erlang-syntax_tools

* Wed Nov  3 2021 Peter Lemenkov <lemenkov@gmail.com> - 3.9.8-2
- Added BR hostname
- Removed dependency - erlang-sd_notify

* Wed Oct 20 2021 Peter Lemenkov <lemenkov@gmail.com> - 3.9.8-1
- Ver. 3.9.8

* Tue Oct 12 2021 Peter Lemenkov <lemenkov@gmail.com> - 3.9.7-1
- Ver. 3.9.7

* Wed Aug 11 2021 Peter Lemenkov <lemenkov@gmail.com> - 3.8.19-1
- Ver. 3.8.19

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun Jun 27 2021 Peter Lemenkov <lemenkov@gmail.com> - 3.8.18-1
- Ver. 3.8.18

* Fri Jun 11 2021 John Eckersberg <jeckersb@redhat.com> - 3.8.17-1
- Ver. 3.8.17
- Switch from /var/run to /run in tmpfiles to remove warning

* Sun May  9 2021 Peter Lemenkov <lemenkov@gmail.com> - 3.8.16-1
- Ver. 3.8.16

* Mon May  3 2021 Peter Lemenkov <lemenkov@gmail.com> - 3.8.15-1
- Ver. 3.8.15

* Tue Mar  2 2021 Peter Lemenkov <lemenkov@gmail.com> - 3.8.14-1
- Ver. 3.8.14

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.8.12-2
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Wed Feb 17 2021 John Eckersberg <jeckersb@redhat.com> - 3.8.12-1
- Ver. 3.8.12

* Mon Feb  1 2021 John Eckersberg <jeckersb@redhat.com> - 3.8.11-1
- Ver. 3.8.11

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Oct  7 2020 Peter Lemenkov <lemenkov@gmail.com> - 3.8.9-2
- Rely on bundled cuttlefish for now

* Fri Sep 25 2020 John Eckersberg <jeckersb@redhat.com> - 3.8.9-1
- Ver. 3.8.9

* Wed Sep  9 2020 John Eckersberg <jeckersb@redhat.com> - 3.8.8-1
- Ver. 3.8.8

* Tue Sep  1 2020 Peter Lemenkov <lemenkov@gmail.com> - 3.8.7-1
- Ver. 3.8.7

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 16 2020 Peter Lemenkov <lemenkov@gmail.com> - 3.8.5-1
- Ver. 3.8.5

* Mon Apr 20 2020 Peter Lemenkov <lemenkov@gmail.com> - 3.8.3-1
- Ver. 3.8.3

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan  7 2020 Peter Lemenkov <lemenkov@gmail.com> - 3.8.2-2
- Properly set up user/group on some script(s).

* Sat Dec  7 2019 Peter Lemenkov <lemenkov@gmail.com> - 3.8.2-1
- Ver. 3.8.2

* Thu Nov 28 2019 Peter Lemenkov <lemenkov@gmail.com> - 3.8.1-1
- Ver. 3.8.1

* Tue Oct  1 2019 John Eckersberg <eck@redhat.com> - 3.8.0-1
- Ver. 3.8.0

* Tue Sep 24 2019 John Eckersberg <eck@redhat.com> - 3.7.16-2
- Enable rabbitmq-diagnostics command

* Wed Jul 24 2019 Peter Lemenkov <lemenkov@gmail.com> - 3.7.16-1
- Ver. 3.7.16

* Wed May 22 2019 Peter Lemenkov <lemenkov@gmail.com> - 3.7.15-1
- Ver. 3.7.15

* Wed Apr 17 2019 Peter Lemenkov <lemenkov@gmail.com> - 3.7.14-2
- Mark it as arch-dependent because it uses Elixir.

* Fri Mar 29 2019 Peter Lemenkov <lemenkov@gmail.com> - 3.7.14-1
- Ver. 3.7.14

* Thu Mar 21 2019 Peter Lemenkov <lemenkov@gmail.com> - 3.7.13-2
- Force Python3

* Mon Mar 11 2019 Peter Lemenkov <lemenkov@gmail.com> - 3.7.13-1
- Ver. 3.7.13

* Tue Feb 19 2019 Peter Lemenkov <lemenkov@gmail.com> - 3.7.12-1
- Ver. 3.7.12

* Mon Feb 04 2019 Peter Lemenkov <lemenkov@gmail.com> - 3.7.11-1
- Ver. 3.7.11

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 20 2018 Richard W.M. Jones <rjones@redhat.com> - 3.6.16-3
- Add BR python-unversioned-command (RHBZ#1606068).

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 14 2018 Peter Lemenkov <lemenkov@gmail.com> - 3.6.16-1
- Ver. 3.6.16

* Mon Apr 09 2018 Peter Lemenkov <lemenkov@gmail.com> - 3.6.15-3
- Handle noport at epmd monitor startup
- Handle EXIT from TCP port more gracefully

* Sun Mar 18 2018 Iryna Shcherbina <ishcherb@redhat.com> - 3.6.15-2
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Feb 08 2018 Peter Lemenkov <lemenkov@gmail.com> - 3.6.15-1
- Ver. 3.6.15

* Tue Nov 14 2017 Peter Lemenkov <lemenkov@gmail.com> - 3.6.14-1
- Ver. 3.6.14

* Tue Sep 19 2017 Peter Lemenkov <lemenkov@gmail.com> - 3.6.12-1
- Ver. 3.6.12

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun  7 2017 Peter Lemenkov <lemenkov@gmail.com> - 3.6.10-1
- Ver. 3.6.10

* Thu Apr 20 2017 Peter Lemenkov <lemenkov@gmail.com> - 3.6.9-1
- Ver. 3.6.9

* Wed Mar  8 2017 Peter Lemenkov <lemenkov@gmail.com> - 3.6.6-2
- Set version explicitly

* Wed Mar  1 2017 Peter Lemenkov <lemenkov@gmail.com> - 3.6.6-1
- Ver. 3.6.6
- Revert "Listing items in parallel" patches

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Aug 23 2016 Peter Lemenkov <lemenkov@gmail.com> - 3.6.5-1
- Ver. 3.6.5

* Mon Jul 25 2016 John Eckersberg <eck@redhat.com> - 3.6.3-6
- Install rabbitmq-server-ha agent

* Fri Jul 22 2016 Peter Lemenkov <lemenkov@gmail.com> - 3.6.3-5
- Don't die while retrieving status from faulty node

* Sun Jul 17 2016 Peter Lemenkov <lemenkov@gmail.com> - 3.6.3-4
- Fixed rabbitmq-server script to use RABBITMQ_SERVER_ERL_ARGS everywhere

* Sun Jul 17 2016 Peter Lemenkov <lemenkov@gmail.com> - 3.6.3-3
- Improve proto_dist usage patch

* Fri Jul 15 2016 Peter Lemenkov <lemenkov@gmail.com> - 3.6.3-2
- Avoid RPC roundtrips in list commands
- Use proto_dist from config instead of always using default (inet_tcp)

* Thu Jul  7 2016 Peter Lemenkov <lemenkov@gmail.com> - 3.6.3-1
- Ver. 3.6.3

* Wed Jun 29 2016 Peter Lemenkov <lemenkov@gmail.com> - 3.6.2-4
- Fixed crash during slave promotion

* Thu May 26 2016 Peter Lemenkov <lemenkov@gmail.com> - 3.6.2-3
- Use empty list for non-allowed user names for loopback connection

* Wed May 25 2016 Peter Lemenkov <lemenkov@gmail.com> - 3.6.2-2
- Keep error codes the same with ver. 3.3.5

* Mon May 23 2016 Peter Lemenkov <lemenkov@gmail.com> - 3.6.2-1
- Ver. 3.6.2

* Wed Apr  6 2016 Peter Lemenkov <lemenkov@gmail.com> - 3.6.1-2
- Fix start up failure

* Thu Mar 24 2016 Peter Lemenkov <lemenkov@gmail.com> - 3.6.1-1
- Ver. 3.6.1

* Tue Feb  2 2016 Peter Lemenkov <lemenkov@gmail.com> - 3.5.7-4
- Remove compatibility triggerun scriptlet
- Don't wait for slave stop messages forever (patches #2, #3)
- Drop dependency on syslog.target - this seems to be a leftover
- Require epmd@0.0.0.0 to run. This is a default value. User should override it
  if necessary. This fixes rhbz #1302368

* Wed Dec 16 2015 Peter Lemenkov <lemenkov@gmail.com> - 3.5.7-3
- Mark configs as owned by rabbitmq user/group
- No need to mark tmpfiles-file as config
- Various config cleanups

* Wed Dec 16 2015 Peter Lemenkov <lemenkov@gmail.com> - 3.5.7-2
- Kill support for SysV branches (no more love for EL5 and EL6). Well keep
  scriptlet for upgrading from pre-2.8.4 versions for a while.

* Tue Dec 15 2015 Peter Lemenkov <lemenkov@gmail.com> - 3.5.7-1
- New upstream release - 3.5.7

* Fri Dec 11 2015 Peter Lemenkov <lemenkov@gmail.com> - 3.5.6-5
- Updated out-of-tarball scripts

* Fri Oct 23 2015 Peter Lemenkov <lemenkov@gmail.com> - 3.5.6-4
- Added help subcommand for the scripts

* Fri Oct  9 2015 Peter Lemenkov <lemenkov@gmail.com> - 3.5.6-3
- Install sample config-file (rhbz#1160810)

* Fri Oct  9 2015 Peter Lemenkov <lemenkov@gmail.com> - 3.5.6-2
- RabbitMQ should use /sbin/nologin as a login shell

* Thu Oct  8 2015 John Eckersberg <eck@redhat.com> - 3.5.6-1
- New upstream release - 3.5.6

* Fri Oct  2 2015 Peter Lemenkov <lemenkov@gmail.com> - 3.5.5-2
- Fix issue with recent systemd Notify access control. See this link for
  further details: https://bodhi.fedoraproject.org/updates/rabbitmq-server-3.5.5-1.fc23#comment-330781

* Thu Sep 24 2015 John Eckersberg <eck@redhat.com> - 3.5.5-1
- New upstream release - 3.5.5

* Thu Sep  3 2015 John Eckersberg <eck@redhat.com> - 3.5.4-3
- Fix service restart on package upgrade (RHBZ#1259564)

* Fri Aug  7 2015 John Eckersberg <eck@redhat.com> - 3.5.4-2
- Update logrotate config to use rabbitmqctl rotate_logs (rhbz#1148444)

* Wed Jul 22 2015 John Eckersberg <eck@redhat.com> - 3.5.4-1
- New upstream release - 3.5.4

* Mon Jul 20 2015 John Eckersberg <eck@redhat.com> - 3.5.4-0.1.rc2
- New upstream release candidate 3.5.4 RC2

* Wed Jul 15 2015 John Eckersberg <eck@redhat.com> - 3.5.4-0.1.rc1
- Fix incorrect NVR for pre-release package

* Tue Jul 14 2015 John Eckersberg <eck@redhat.com> - 3.5.4.rc1-1
- New upstream release candidate 3.5.4 RC1

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri May 22 2015 John Eckersberg <eck@redhat.com> - 3.5.3-1
- New upstream release - 3.5.3

* Tue May 12 2015 John Eckersberg <eck@redhat.com> - 3.5.2-1
- New upstream release - 3.5.2

* Sat Apr  4 2015 John Eckersberg <eck@redhat.com> - 3.5.1-1
- New upstream release - 3.5.1

* Thu Mar 12 2015 John Eckersberg <eck@redhat.com> - 3.5.0-2
- Add requires on erlang-eldap (RHBZ#1192089)

* Wed Mar 11 2015 John Eckersberg <eck@redhat.com> - 3.5.0-1
- New upstream release - 3.5.0

* Wed Feb 11 2015 John Eckersberg <eck@redhat.com> - 3.4.4-1
- New upstream release - 3.4.4

* Mon Jan 19 2015 Richard W.M. Jones <rjones@redhat.com> - 3.4.3-2
- Move /etc/tmpfiles.d/* to /usr/lib/tmpfiles.d/*
  See: https://bugzilla.redhat.com/show_bug.cgi?id=1180990

* Wed Jan  7 2015 John Eckersberg <eck@redhat.com> - 3.4.3-1
- New upstream release - 3.4.3

* Wed Nov 26 2014 John Eckersberg <eck@redhat.com> - 3.4.2-1
- New upstream release - 3.4.2

* Wed Oct 29 2014 John Eckersberg <eck@redhat.com> - 3.4.1-1
- New upstream release - 3.4.1

* Wed Oct 22 2014 John Eckersberg <eck@redhat.com> - 3.4.0-1
- New upstream release - 3.4.0

* Tue Sep 30 2014 John Eckersberg <eck@redhat.com> - 3.3.5-2
- Add rabbitmq-plugins to default path (#1033305)

* Wed Aug 27 2014 John Eckersberg <jeckersb@redhat.com> - 3.3.5-1
- New upstream release - 3.3.5
- Updated systemd notify support patch to match implementation from
  couchdb (Thanks Peter Lemenkov for the much more concise patch!)

* Wed Jul 02 2014 John Eckersberg <jeckersb@redhat.com> - 3.1.5-9
- Add systemd notify support (RHBZ#1103524)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Jun 01 2014 Lon Hohberger <lhh@redhat.com> - 3.1.5-7
- Use specific subpackages of erlang instead of the entire
  metapackage (bz1083637)

* Wed Apr 09 2014 Alan Pevec <apevec@redhat.com> - 3.1.5-6
- Fix failure to start on boot on RHEL7 (#1085418)

* Tue Apr  1 2014 Richard W.M. Jones <rjones@redhat.com> - 3.1.5-5
- Fix race in systemd service startup (RHBZ#1059913).

* Mon Mar 31 2014 Richard W.M. Jones <rjones@redhat.com> - 3.1.5-4
- Use ephemeral port (32768 and up instead of 10000+) (RHBZ#998682).

* Thu Mar 27 2014 Lubomir Rintel <lkundrak@v3.sk> - 3.1.5-3
- Do not clobber a file outside the build hierarchy

* Tue Aug 27 2013 Peter Lemenkov <lemenkov@gmail.com> - 3.1.5-2
- Fix permissoon for *.service file (rhbz #1001472)

* Sat Aug 24 2013 Peter Lemenkov <lemenkov@gmail.com> - 3.1.5-1
- New Upstream Release - 3.1.5 (bugfix release)

* Wed Aug 07 2013 Peter Lemenkov <lemenkov@gmail.com> - 3.1.4-1
- New Upstream Release - 3.1.4 (bugfix release)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jun 29 2013 Peter Lemenkov <lemenkov@gmail.com> - 3.1.3-1
- New Upstream Release - 3.1.3 (fixes issue bug in the management plugin)

* Tue Jun 25 2013 Peter Lemenkov <lemenkov@gmail.com> - 3.1.2-1
- New Upstream Release - 3.1.2 (works with Erlang R16B01)

* Sun Mar 17 2013 Peter Lemenkov <lemenkov@gmail.com> - 3.0.4-1
- New Upstream Release - 3.0.4

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 02 2012 Peter Lemenkov <lemenkov@gmail.com> - 2.8.7-1
- New Upstream Release - 2.8.7

* Sat Aug 18 2012 Peter Lemenkov <lemenkov@gmail.com> - 2.8.5-1
- New Upstream Release - 2.8.5

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jul 12 2012 Peter Lemenkov <lemenkov@gmail.com> - 2.8.4-1
- New Upstream Release - 2.8.4

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 08 2011 Peter Lemenkov <lemenkov@gmail.com> - 2.6.1-1
- New Upstream Release - 2.6.1
- Fixed rhbz #738067 (service cannot start - rabbitmq-multi missing)

* Mon Sep 12 2011 Peter Lemenkov <lemenkov@gmail.com> - 2.6.0-1
- New Upstream Release - 2.6.0

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 15 2011 Hubert Plociniczak <hubert.plociniczak@gmail.com> 2.2.0-1
- New Upstream Release

* Mon Nov 1 2010 Hubert Plociniczak <hubert.plociniczak@gmail.com> 2.1.1-1
- New Upstream Release

* Tue Oct 5 2010 Hubert Plociniczak <hubert.plociniczak@gmail.com> 2.1.0-1
- New Upstream Release
- Added python as a build dependency

* Mon Aug 23 2010 Mike Bridgen <mikeb@rabbitmq.com> 2.0.0-1
- New Upstream Release

* Mon Jun 28 2010 Hubert Plociniczak <hubert@lshift.net> 1.8.0-1
- New Upstream Release
- Backported fix for bug 22871, fixes issues with erlang >= R14A

* Mon Feb 15 2010 Matthew Sackman <matthew@lshift.net> 1.7.2-1
- New Upstream Release

* Fri Jan 22 2010 Matthew Sackman <matthew@lshift.net> 1.7.1-1
- New Upstream Release

* Mon Oct 5 2009 David Wragg <dpw@lshift.net> 1.7.0-1
- New upstream release

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 17 2009 Matthias Radestock <matthias@lshift.net> 1.6.0-1
- New upstream release

* Tue May 26 2009 Hubert Plociniczak <hubert@lshift.net> 1.5.5-2
- Include dist macro in the release number

* Tue May 19 2009 Matthias Radestock <matthias@lshift.net> 1.5.5-1
- Maintenance release for the 1.5.x series

* Mon Apr 6 2009 Matthias Radestock <matthias@lshift.net> 1.5.4-1
- Maintenance release for the 1.5.x series

* Tue Feb 24 2009 Tony Garnock-Jones <tonyg@lshift.net> 1.5.3-1
- Maintenance release for the 1.5.x series

* Mon Feb 23 2009 Tony Garnock-Jones <tonyg@lshift.net> 1.5.2-1
- Maintenance release for the 1.5.x series

* Mon Jan 19 2009 Ben Hood <0x6e6562@gmail.com> 1.5.1-1
- Maintenance release for the 1.5.x series

* Wed Dec 17 2008 Matthias Radestock <matthias@lshift.net> 1.5.0-1
- New upstream release

* Thu Jul 24 2008 Tony Garnock-Jones <tonyg@lshift.net> 1.4.0-1
- New upstream release

* Mon Mar 3 2008 Adrien Pierard <adrian@lshift.net> 1.3.0-1
- New upstream release

* Wed Sep 26 2007 Simon MacMullen <simon@lshift.net> 1.2.0-1
- New upstream release

* Wed Aug 29 2007 Simon MacMullen <simon@lshift.net> 1.1.1-1
- New upstream release

* Mon Jul 30 2007 Simon MacMullen <simon@lshift.net> 1.1.0-1.alpha
- New upstream release

* Tue Jun 12 2007 Hubert Plociniczak <hubert@lshift.net> 1.0.0-1.20070607
- Building from source tarball, added starting script, stopping

* Mon May 21 2007 Hubert Plociniczak <hubert@lshift.net> 1.0.0-1.alpha
- Initial build of server library of RabbitMQ package
