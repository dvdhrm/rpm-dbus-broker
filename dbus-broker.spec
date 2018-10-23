%global dbus_user_id 81

Name:           dbus-broker
Version:        16
Release:        1%{?dist}
Summary:        Linux D-Bus Message Broker
License:        ASL 2.0
URL:            https://github.com/bus1/dbus-broker
Source0:        https://github.com/bus1/dbus-broker/releases/download/v%{version}/dbus-broker-%{version}.tar.xz
Provides:       bundled(c-dvar) = 1
Provides:       bundled(c-list) = 3
Provides:       bundled(c-rbtree) = 3
%{?systemd_requires}
BuildRequires:  pkgconfig(audit)
BuildRequires:  pkgconfig(expat)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(libcap-ng)
BuildRequires:  pkgconfig(libselinux)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(systemd)
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  meson
BuildRequires:  python3-docutils
Requires:       dbus-common
Requires(pre):  shadow-utils

%description
dbus-broker is an implementation of a message bus as defined by the D-Bus
specification. Its aim is to provide high performance and reliability, while
keeping compatibility to the D-Bus reference implementation. It is exclusively
written for Linux systems, and makes use of many modern features provided by
recent Linux kernel releases.

%prep
%autosetup -p1

%build
%meson -Dselinux=true -Daudit=true -Ddocs=true -Dsystem-console-users=gdm
%meson_build

%install
%meson_install

%check
%meson_test

%pre
# create dbus user and group
getent group %{dbus_user_id} >/dev/null || \
        /usr/sbin/groupadd \
                -g %{dbus_user_id} \
                -r dbus
getent passwd %{dbus_user_id} >/dev/null || \
        /usr/sbin/useradd \
                -c 'System message bus' \
                -u %{dbus_user_id} \
                -g %{dbus_user_id} \
                -s /sbin/nologin \
                -d '/' \
                -r dbus

%post
%systemd_post dbus-broker.service
%systemd_user_post dbus-broker.service

%preun
%systemd_preun dbus-broker.service
%systemd_user_preun dbus-broker.service

%postun
%systemd_postun dbus-broker.service
%systemd_user_postun dbus-broker.service

%triggerpostun -- dbus-daemon
systemctl --no-reload preset dbus-broker.service &>/dev/null || :
systemctl --no-reload --global preset dbus-broker.service &>/dev/null || :

%files
%license AUTHORS
%license LICENSE
%{_bindir}/dbus-broker
%{_bindir}/dbus-broker-launch
%{_mandir}/man1/dbus-broker.1*
%{_mandir}/man1/dbus-broker-launch.1*
%{_unitdir}/dbus-broker.service
%{_userunitdir}/dbus-broker.service

%changelog
* Tue Oct 23 2018 David Herrmann <dh.herrmann@gmail.com> - 16-2
- create dbus user and group if non-existant

* Fri Oct 12 2018 Tom Gundersen <teg@jklm.no> - 16-1
- make resource limits configurable
- rerun presets in case dbus-daemon is disabled

* Thu Aug 30 2018 Tom Gundersen <teg@jklm.no> - 15-4
- depend on dbus-common rather than dbus

* Wed Aug 29 2018 Tom Gundersen <teg@jklm.no> - 15-3
- run %%systemd_user rpm macros

* Mon Aug 27 2018 Tom Gundersen <teg@jklm.no> - 15-2
- add back --verbose switch for backwards compatibility

* Wed Aug 08 2018 Tom Gundersen <teg@jklm.no> - 15-1
- fix audit support
- make logging about invalid config less verbose

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 03 2018 Tom Gundersen <teg@jklm.no> - 14-1
- use inotify to reload config automatically
- run as the right user
- new compatibility features, bugfixes and performance enhancements

* Mon Apr 23 2018 Tom Gundersen <teg@jklm.no> - 13-1
- Namespace transient systemd units per launcher instance
- Reduce reliance on NSS
- Fix deadlock with nss-systemd

* Wed Feb 21 2018 Tom Gundersen <teg@jklm.no> - 11-1
- The 'gdm' user is now considered at_console=true
- Bugfixes and performance enhancements

* Wed Feb 07 2018 Tom Gundersen <teg@jklm.no> - 10-1
- Bugfixes and performance enhancements

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Nov 30 2017 Tom Gundersen <teg@jklm.no> - 9-1
- Avoid nss deadlock at start-up
- Support ExecReload
- Respect User= in service files

* Tue Oct 17 2017 Tom Gundersen <teg@jklm.no> - 8-1
- Don't clean-up children of activated services by default
- Don't use audit from the user instance
- Support the ReloadConfig() API

* Tue Oct 17 2017 Tom Gundersen <teg@jklm.no> - 7-1
- Upstream bugfix release

* Mon Oct 16 2017 Tom Gundersen <teg@jklm.no> - 6-1
- Upstream bugfix release

* Tue Oct 10 2017 Tom Gundersen <teg@jklm.no> - 5-1
- Drop downstream SELinux module
- Support (in a limited way) at_console= policies
- Order dbus-broker before basic.target

* Fri Sep 08 2017 Tom Gundersen <teg@jklm.no> - 4-1
- Use audit for SELinux logging
- Support full search-paths for service files
- Log policy failures

* Fri Aug 18 2017 Tom Gundersen <teg@jklm.no> - 3-1
- Add manpages

* Wed Aug 16 2017 Tom Gundersen <teg@jklm.no> - 2-2
- Add license to package

* Wed Aug 16 2017 Tom Gundersen <teg@jklm.no> - 2-1
- Add SELinux support

* Sun Aug 13 2017 Tom Gundersen <teg@jklm.no> - 1-1
- Initial RPM release

