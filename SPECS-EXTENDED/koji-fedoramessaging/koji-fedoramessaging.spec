%global plugin_dir %{_prefix}/lib/koji-hub-plugins

Name:           koji-fedoramessaging
Version:        1.1.2
Release:        1%{?dist}
Summary:        Enable Koji to send Fedora Messaging messages
License:        GPL-3.0-only
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/fedora-infra/koji-fedoramessaging
Source0:        %{url}/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel

Requires:       python3-koji-hub
Requires:       python3-fedora-messaging
# python3-koji-fedoramessaging-messages (the rich JSON-schema message classes)
# is intentionally NOT a dependency on Azure Linux 3.0. Its schemas use JSON
# Schema draft 2019-09 $anchor references, which the python-jsonschema 2.6.0
# shipped in AzL 3.0 cannot resolve. If it were installed, the hub plugin would
# select those rich schemas and fedora-messaging would validate them on publish
# -- raising RefResolutionError (not caught by the plugin's ValidationError
# fallback) and silently dropping task-tree-bearing events (build.state.change
# with subtasks, task.state.change, etc.). Without it, the plugin falls back to
# the generic permissive Message schema and all events publish fine. Consumers
# that want schema validation can install the package explicitly on a platform
# with python-jsonschema >= 4.

%description
Enable Koji to send Fedora Messaging messages.

%prep
%autosetup -p1

%build

%install
install -D -p -m 0644 koji-fedoramessaging/koji-fedoramessaging.py \
    %{buildroot}%{plugin_dir}/koji_fedoramessaging.py
%py_byte_compile %{__python3} %{buildroot}%{plugin_dir}

%files
%dir %{plugin_dir}
%{plugin_dir}/koji_fedoramessaging.py
%{plugin_dir}/__pycache__/*
%doc README.md

%changelog
* Thu Jun 11 2026 Adit Jha <aditjha@microsoft.com> - 1.1.2-1
- Initial Azure Linux import from the source project (license: same as "License" tag).
- License verified.
- Do not depend on python-koji-fedoramessaging-messages: its draft-2019-09
  schemas are unresolvable by AzL 3.0's python-jsonschema 2.6.0.

* Mon Jun 12 2023 Aurelien Bompard <abompard@fedoraproject.org> - 1.1.2-1
- The files_base_url is only relevant for build and task state changes

* Fri Jun 09 2023 Aurelien Bompard <abompard@fedoraproject.org> - 1.1.1-1
- Don't call get_message_body() needlessly

* Fri Jun 09 2023 Aurelien Bompard <abompard@fedoraproject.org> - 1.1.0-1
- Add more data in the task and build state change messages

* Thu Feb 09 2023 Ryan Lerch <rlerch@redhat.com> - 1.0.1-1
- Tweak logging so kojihub logger can find the logs

* Tue Feb 07 2023 Ryan Lerch <rlerch@redhat.com> - 1.0-1
- Initial Release
