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
Requires:       python3-koji-fedoramessaging-messages

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
