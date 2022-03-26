%global py3pluginpath %{python3_sitelib}/%{name}-plugins
%global relate_libdnf_version 0.48.0-3
%global hawkey_version 0.65.0
%global libcomps_version 0.1.8
%global libmodulemd_version 2.9.3
%global conflicts_dnf_plugins_core_version 4.0.26
%define __cmake_in_source_build 1

Name:                 dnf
Version:              4.11.1
Release:              1
Summary:              A software package manager that manages packages on Linux distributions.
License:              GPLv2+ and GPLv2 and GPL
URL:                  https://github.com/rpm-software-management/dnf
Source0:              https://github.com/rpm-software-management/dnf/archive/%{version}/%{name}-%{version}.tar.gz

BuildArch:            noarch
BuildRequires:        cmake gettext systemd bash-completion python3-sphinx
Requires:             python3-%{name} = %{version}-%{release} libreport-filesystem 
Recommends:           (%{_bindir}/sqlite3 if bash-completion) (python3-dbus if NetworkManager)
Provides:             dnf-command(alias) dnf-command(autoremove) dnf-command(check-update) dnf-command(clean)
Provides:             dnf-command(distro-sync) dnf-command(downgrade) dnf-command(group)  dnf-command(history)
Provides:             dnf-command(info) dnf-command(install) dnf-command(list) dnf-command(makecache)
Provides:             dnf-command(mark) dnf-command(provides) dnf-command(reinstall) dnf-command(remove)
Provides:             dnf-command(repolist) dnf-command(repoquery) dnf-command(repository-packages)
Provides:             dnf-command(search) dnf-command(updateinfo) dnf-command(upgrade) dnf-command(upgrade-to)
Conflicts:            python2-dnf-plugins-core < %{conflicts_dnf_plugins_core_version} python3-dnf-plugins-core < %{conflicts_dnf_plugins_core_version}
Provides:             dnf-data %{name}-conf = %{version}-%{release} %{name}-automatic = %{version}-%{release}
Obsoletes:            dnf-data %{name}-conf < %{version}-%{release} %{name}-automatic < %{version}-%{release}

%description
DNF is a software package manager that installs, updates, and removespackages
on RPM-based Linux distributions. It automatically computes dependencies and
determines the actions required to install packages.DNF also makes it easier
to maintain groups of machines, eliminating the need to manually update each
one using rpm.

%package -n           yum 
Requires:             %{name} = %{version}-%{release}
Summary:              Package manager

%description -n       yum
Utility that allows users to manage packages on their systems.\
It supports RPMs, modules and comps groups & environments.

%package -n           python3-%{name}
Summary:              Python 3 interface to DNF
%{?python_provide:%python_provide python3-%{name}}
BuildRequires:        python3-devel python3-hawkey >= %{hawkey_version} python3-libdnf >= 0.48.0
BuildRequires:        python3-libcomps >= %{libcomps_version} libmodulemd >= %{libmodulemd_version}
BuildRequires:        python3-nose python3-gpg python3-rpm >= 4.14.0
Requires:             python3-gpg %{name}-data = %{version}-%{release} libmodulemd >= %{libmodulemd_version}
Requires:             python3-hawkey >= %{hawkey_version} python3-libdnf >= %{relate_libdnf_version}
Requires:             python3-libcomps >= %{libcomps_version} python3-rpm >= 4.14.0
Recommends:           python3-unbound
Obsoletes:	      python2-%{name}

%description -n python3-%{name}
Python 3 interface to DNF.

%package              help
Summary:              Documents for dnf and yum
Buildarch:            noarch
Requires:             man info
Provides:             yum-help = %{version}-%{release}
Obsoletes:            yum-help < %{version}-%{release}

%description          help
Man pages and other related documents for dnf and yum

%prep
%autosetup -p1
mkdir build-py3

%build
pushd build-py3
%cmake .. -DPYTHON_DESIRED:FILEPATH=%{__python3} -DDNF_VERSION=%{version}
%make_build
make doc-man
popd

%install
pushd build-py3
%make_install
popd

%find_lang %{name}
mkdir -p %{buildroot}%{_sysconfdir}/%{name}/vars
mkdir -p %{buildroot}%{_sysconfdir}/%{name}/aliases.d
mkdir -p %{buildroot}%{_sysconfdir}/%{name}/plugins/
mkdir -p %{buildroot}%{_sysconfdir}/%{name}/modules.d
mkdir -p %{buildroot}%{_sysconfdir}/bash_completion.d/dnf
mkdir -p %{buildroot}%{_sysconfdir}/%{name}/modules.defaults.d
mkdir -p %{buildroot}%{py3pluginpath}/__pycache__/
mkdir -p %{buildroot}%{_localstatedir}/log/
mkdir -p %{buildroot}%{_var}/cache/dnf/
touch %{buildroot}%{_localstatedir}/log/%{name}.log
ln -sr %{buildroot}%{_bindir}/dnf-3 %{buildroot}%{_bindir}/dnf
mv %{buildroot}%{_bindir}/dnf-automatic-3 %{buildroot}%{_bindir}/dnf-automatic
rm -vf %{buildroot}%{_bindir}/dnf-automatic-*
mv -f %{buildroot}%{_sysconfdir}/%{name}/%{name}-strict.conf %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf
ln -sr  %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf %{buildroot}%{_sysconfdir}/yum.conf
ln -sr  %{buildroot}%{_bindir}/dnf-3 %{buildroot}%{_bindir}/yum
mkdir -p %{buildroot}%{_sysconfdir}/yum
ln -sr  %{buildroot}%{_sysconfdir}/%{name}/plugins %{buildroot}%{_sysconfdir}/yum/pluginconf.d
ln -sr  %{buildroot}%{_sysconfdir}/%{name}/protected.d %{buildroot}%{_sysconfdir}/yum/protected.d
ln -sr  %{buildroot}%{_sysconfdir}/%{name}/vars %{buildroot}%{_sysconfdir}/yum/vars

%check
export TERM=linux
pushd build-py3
ctest -VV
popd

%post
%systemd_post dnf-makecache.timer dnf-automatic.timer dnf-automatic-notifyonly.timer dnf-automatic-download.timer dnf-automatic-install.timer

%preun
%systemd_preun dnf-automatic.timer dnf-makecache.timer dnf-automatic-notifyonly.timer dnf-automatic-download.timer dnf-automatic-install.timer

%postun
%systemd_postun_with_restart dnf-makecache.timer dnf-automatic.timer dnf-automatic-notifyonly.timer dnf-automatic-download.timer dnf-automatic-install.timer

%files
%license COPYING PACKAGE-LICENSING
%doc AUTHORS README.rst
%{_bindir}/%{name}
%{_bindir}/%{name}-automatic
%{_sysconfdir}/bash_completion.d/%{name}
%{_unitdir}/%{name}-automatic.timer
%{_unitdir}/%{name}-makecache.timer
%{_unitdir}/%{name}-automatic.service
%{_unitdir}/%{name}-makecache.service
%{_unitdir}/%{name}-automatic-notifyonly.service
%{_unitdir}/%{name}-automatic-notifyonly.timer
%{_unitdir}/%{name}-automatic-download.service
%{_unitdir}/%{name}-automatic-download.timer
%{_unitdir}/%{name}-automatic-install.service
%{_unitdir}/%{name}-automatic-install.timer
%{_var}/cache/%{name}/
%{python3_sitelib}/%{name}/automatic/
%dir %{_sysconfdir}/%{name} 
%dir %{_sysconfdir}/%{name}/modules.d
%dir %{_sysconfdir}/%{name}/modules.defaults.d
%dir %{_sysconfdir}/%{name}/plugins
%dir %{_sysconfdir}/%{name}/protected.d
%dir %{_sysconfdir}/%{name}/vars
%dir %{_sysconfdir}/%{name}/aliases.d
%exclude %{_sysconfdir}/%{name}/aliases.d/zypper.conf
%config(noreplace) %{_sysconfdir}/%{name}/automatic.conf
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/protected.d/%{name}.conf
%ghost %attr(644,-,-) %{_localstatedir}/log/hawkey.log
%ghost %attr(644,-,-) %{_localstatedir}/log/%{name}.log
%ghost %attr(644,-,-) %{_localstatedir}/log/%{name}.librepo.log
%ghost %attr(644,-,-) %{_localstatedir}/log/%{name}.rpm.log
%ghost %attr(644,-,-) %{_localstatedir}/log/%{name}.plugin.log
%ghost %attr(755,-,-) %dir %{_sharedstatedir}/%{name}
%ghost %attr(644,-,-) %{_sharedstatedir}/%{name}/groups.json
%ghost %attr(755,-,-) %dir %{_sharedstatedir}/%{name}/yumdb
%ghost %attr(755,-,-) %dir %{_sharedstatedir}/%{name}/history
%{_tmpfilesdir}/%{name}.conf
%{_sysconfdir}/libreport/events.d/collect_dnf.conf

%files -n yum 
%{_bindir}/yum
%{_sysconfdir}/yum/vars
%{_sysconfdir}/yum.conf
%{_sysconfdir}/yum/pluginconf.d
%{_sysconfdir}/yum/protected.d
%config(noreplace) %{_sysconfdir}/%{name}/protected.d/yum.conf

%files -n python3-%{name}
%{_bindir}/%{name}-3
%exclude %{python3_sitelib}/%{name}/automatic
%{python3_sitelib}/%{name}/
%dir %{py3pluginpath}
%dir %{py3pluginpath}/__pycache__

%files help
%{_datadir}/locale/*
%{_datadir}/bash-completion/*
%{_mandir}/man8/yum.8*
%{_mandir}/man8/yum2dnf.8*
%{_mandir}/man8/%{name}.8*
%{_mandir}/man5/yum.conf.5.*
%{_mandir}/man8/yum-shell.8*
%{_mandir}/man1/yum-aliases.1*
%{_mandir}/man5/dnf-transaction-json.5*
%{_mandir}/man5/%{name}.conf.5*
%{_mandir}/man7/dnf.modularity.7*
%{_mandir}/man8/%{name}-automatic.8*

%changelog
 * Sat Mar 26 2022 Jiacheng Zhou <jchzhou@outlook.com> - 4.11.1-1
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:upgrade to 4.11.1-1

* Thu Jul 15 2021 gaihuiying <gaihuiying1@huawei.com> - 4.2.23-6
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:remove recommends rpm-plugins-systemd-inhibit
       backport community patches and fix CVE-2021-3445
       delete duplicate python3-libdnf dependency

* Tue Mar 30 2021 gaihuiying <gaihuiying1@huawei.com> - 4.2.23-5
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:fix errors when use "yum module remove --all per:common" command
       fix test test_mode_tty failed

* Fri Nov 20 2020 lunankun <lunankun@huawei.com> - 4.2.23-4
- Type:requirement
- ID:NA
- SUG:NA
- DESC:remove depend deltarpm

* Tue Sep 01 2020 zhangrui <zhangrui182@huawei.com> - 4.2.23-3
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:provide automatic files and provide yum help

* Tue Aug 04 2020 yuboyun <yuboyun@huawei.com> - 4.2.23-2
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:fix conflicts error for new version

* Tue Apr 28 2020 zhouyihang <zhouyihang3@huawei.com> - 4.2.23-1
- Type:requirement
- ID:NA
- SUG:NA
- DESC:update dnf version to 4.2.23

* Wed Mar 18 2020 songnannan <songnannan2@huawei.com> - 4.2.15-8
- add obsoletes the python2-dnf

* Tue Mar 3 2020 openEuler Buildteam <buildteam@openeuler.org> - 4.2.15-7
- modify the patch name

* Thu Feb 27 2020 openEuler Buildteam <buildteam@openeuler.org> - 4.2.15-6
- remove extra brace

* Mon Feb 24 2020 openEuler Buildteam <buildteam@openeuler.org> - 4.2.15-5
- Revert Fix messages for starting and failing scriptlets

* Fri Feb 14 2020 openEuler Buildteam <buildteam@openeuler.org> - 4.2.15-4
- remove python2

* Fri Jan 17 2020 openEuler Buildteam <buildteam@openeuler.org> - 4.2.15-3
- bug fix format problem

* Mon Jan 6 2020 openEuler Buildteam <buildteam@openeuler.org> - 4.2.15-2
- Package Init
