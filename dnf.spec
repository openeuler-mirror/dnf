%bcond_with python2
%bcond_without python3

%if %{with python2}
    %global py2pluginpath %{python2_sitelib}/%{name}-plugins
%endif

%if %{with python3}
    %global py3pluginpath %{python3_sitelib}/%{name}-plugins
%endif

Name:           dnf
Version:        4.0.4
Release:        2
Summary:        A software package manager that manages packages on Linux distributions.
License:        GPLv2+ and GPLv2 and GPL
URL:            https://github.com/rpm-software-management/dnf
Source0:        https://github.com/rpm-software-management/dnf/archive/%{version}/%{name}-%{version}.tar.gz

Patch6000:      automatic-Fix-the-systemd-ordering-loop-RhBug-163648.patch
Patch6001:      conf-setopt-not-create-rewrite-other-option_parser-o.patch
Patch6002:      Set-tsi-state-if-multiple-pkgs-have-same-nevra-RhBug.patch
Patch6003:      Fix-traceback-with-repoquery-location-RhBug-1639827.patch
Patch6004:      Run-plugins-hook-safely-RhBug-1495482.patch
Patch6005:      Format-messages-properly-RhBug-1509393.patch
Patch6006:      Add-best-as-default-behavior-RhBug-1670776-1671683.patch
Patch6007:      callback-Bring-PKG_ERASE-back-for-compatibility-reas.patch
Patch6008:      Solve-traceback-with-the-dnf-install-module-RhBug-16.patch
Patch6009:      Fix-multilib-obsoletes-RhBug-1672947.patch
Patch6010:      Fix-the-installation-of-completion_helper.py.patch

BuildArch:      noarch
BuildRequires:  cmake gettext python2-sphinx systemd bash-completion
Requires:       libreport-filesystem systemd %{name} = %{version}-%{release}
%if %{with python3}
Requires:       python3-%{name} = %{version}-%{release}
Recommends:     (python3-dbus if NetworkManager)
%else
Requires:       python2-%{name} = %{version}-%{release}
Recommends:     (python2-dbus if NetworkManager)
%endif
Recommends:     (sqlite if bash-completion)
%{?systemd_requires}
Provides:       dnf-command(autoremove) dnf-command(check-update) dnf-command(clean) dnf-command(distro-sync)
Provides:       dnf-command(downgrade) dnf-command(group) dnf-command(history) dnf-command(info)
Provides:       dnf-command(install) dnf-command(list) dnf-command(makecache) dnf-command(mark)
Provides:       dnf-command(provides) dnf-command(reinstall) dnf-command(remove) dnf-command(repolist)
Provides:       dnf-command(repoquery) dnf-command(repository-packages) dnf-command(updateinfo)
Provides:       dnf-command(search) dnf-command(upgrade) dnf-command(upgrade-to)
Provides:       %{name}-conf = %{version}-%{release} dnf-data
Obsoletes:      %{name}-conf <= %{version}-%{release} dnf-data
Conflicts:      python2-dnf-plugins-core < 3.1 python3-dnf-plugins-core < 3.1
Conflicts:      python2-dnf-plugins-extras < 3.0.2 python3-dnf-plugins-extras < 3.0.2

%description
DNF is a software package manager that installs, updates, and removespackages
on RPM-based Linux distributions. It automatically computes dependencies and
determines the actions required to install packages.DNF also makes it easier
to maintain groups of machines, eliminating the need to manually update each
one using rpm.

%package help
Summary: Help documents for dnf

%description help
This package helps to deploy dnf and contains some man help files.

%package -n yum
Requires:       %{name} = %{version}-%{release}
Summary:        A command-line package-management utility for RPM-based Linux distributions
Conflicts:      yum < 3.4.3-505

%description -n yum
This package allows for automatic updates and package and dependency management on
RPM-based Linux distributions.

%if %{with python2}
%package -n python2-dnf
Summary:        Python 2 interface to DNF
%{?python_provide:%python_provide python2-%{name}}

BuildRequires:  python2-devel python2-libdnf python2-nose python2-hawkey >= 0.22.0
BuildRequires:  python2-libcomps >= 0.1.8 python2-libdnf >= 0.22.0
BuildRequires:  python2-rpm >= 4.14.0 libmodulemd >= 1.4.0
BuildRequires:  python2-gpg python2-enum34 pyliblzma python2-iniparse
Requires:       libmodulemd >= 1.4.0 python2-gpg python2-enum34
Requires:       %{name}-data = %{version}-%{release} deltarpm python2-rpm >= 4.14.0
Requires:       python2-libdnf >= 0.22.0 python2-libcomps >= 0.1.8
Requires:       python2-hawkey >= 0.22.0 python2-libdnf pyliblzma python2-iniparse
Recommends:     deltarpm python2-unbound rpm-plugin-systemd-inhibit
Conflicts:      dnfdaemon < 0.3.19

%description -n python2-dnf
Python2 interface for DNF.
%endif

%if %{with python3}
%package -n python3-dnf
Summary:        Python 3 interface to DNF
%{?python_provide:%python_provide python3-%{name}}

BuildRequires:  python3-hawkey >= 0.22.0 python3-libdnf >= 0.22.0
BuildRequires:  python3-libcomps >= 0.1.8 libmodulemd >= 1.4.0
BuildRequires:  python3-devel python3-libdnf python3-iniparse
BuildRequires:  python3-gpg python3-nose python3-rpm >= 4.14.0
Requires:       libmodulemd >= 1.4.0 python3-libdnf >= 0.22.0
Requires:       python3-hawkey >= 0.22.0 %{name}-data = %{version}-%{release}
Requires:       python3-libcomps >= 0.1.8 python3-rpm >= 4.14.0
Requires:       python3-iniparse python3-gpg python3-libdnf deltarpm
Recommends:     python3-unbound deltarpm rpm-plugin-systemd-inhibit

%description -n python3-dnf
Python3 interface for DNF.
%endif

%prep
%autosetup -p1
mkdir python2
mkdir python3

%build
%if %{with python2}
    pushd python2
    %cmake .. -DPYTHON_DESIRED:FILEPATH=%{__python2}
    %make_build all doc-man
    popd
%endif

%if %{with python3}
    pushd python3
    %cmake .. -DPYTHON_DESIRED:FILEPATH=%{__python3}
    %make_build all doc-man
    popd
%endif

%install
%if %{with python2}
    pushd python2
    %make_install
    popd
%endif

%if %{with python3}
    pushd python3
    %make_install
    popd
%endif

%find_lang %{name}
install -d %{buildroot}{/etc/dnf/vars,/etc/dnf/plugins/,%{_localstatedir}/log/,%{_var}/cache/dnf/}
install -d %{buildroot}%{_sysconfdir}/%{name}/{modules.d,modules.defaults.d}
ln -sr  %{buildroot}/etc/dnf/%{name}.conf %{buildroot}%{_sysconfdir}/yum.conf
touch %{buildroot}%{_localstatedir}/log/%{name}.log

%if %{with python2}
install -d %{buildroot}%{py2pluginpath}/
%endif
%if %{with python3}
install -d %{buildroot}%{py3pluginpath}/__pycache__/
%endif

%if %{with python3}
ln -sr %{buildroot}%{_bindir}/dnf-3 %{buildroot}%{_bindir}/dnf
mv %{buildroot}%{_bindir}/dnf-automatic-3 %{buildroot}%{_bindir}/dnf-automatic
ln -sr  %{buildroot}%{_bindir}/dnf-3 %{buildroot}%{_bindir}/yum
%else
ln -sr %{buildroot}%{_bindir}/dnf-2 %{buildroot}%{_bindir}/dnf
mv %{buildroot}%{_bindir}/dnf-automatic-2 %{buildroot}%{_bindir}/dnf-automatic
ln -sr  %{buildroot}%{_bindir}/dnf-2 %{buildroot}%{_bindir}/yum
%endif
rm -vf %{buildroot}%{_bindir}/dnf-automatic-*
install -d %{buildroot}%{_sysconfdir}/yum
ln -sr  %{buildroot}/etc/dnf/vars %{buildroot}%{_sysconfdir}/yum/vars
ln -sr  %{buildroot}/etc/dnf/plugins %{buildroot}%{_sysconfdir}/yum/pluginconf.d
ln -sr  %{buildroot}/etc/dnf/protected.d %{buildroot}%{_sysconfdir}/yum/protected.d


%check
%if %{?_with_check:1}%{!?_with_check:0}
  %if %{with python2}
      pushd python2
      ctest -VV
      popd
  %endif

  %if %{with python3}
      pushd python3
      ctest -VV
      popd
  %endif
%endif
%post
%systemd_post dnf-makecache.timer
%systemd_post dnf-automatic.timer
%systemd_post dnf-automatic-notifyonly.timer
%systemd_post dnf-automatic-download.timer
%systemd_post dnf-automatic-install.timer

%preun
%systemd_preun dnf-makecache.timer
%systemd_preun dnf-automatic.timer
%systemd_preun dnf-automatic-notifyonly.timer
%systemd_preun dnf-automatic-download.timer
%systemd_preun dnf-automatic-install.timer

%postun
%systemd_postun_with_restart dnf-makecache.timer
%systemd_postun_with_restart dnf-automatic.timer
%systemd_postun_with_restart dnf-automatic-notifyonly.timer
%systemd_postun_with_restart dnf-automatic-download.timer
%systemd_postun_with_restart dnf-automatic-install.timer


%files -f %{name}.lang
%license COPYING PACKAGE-LICENSING
%doc AUTHORS README.rst
%{_bindir}/%{name}
%{_var}/cache/%{name}/
%{_unitdir}/%{name}-*
%{_datadir}/bash-completion/completions/%{name}
%{_tmpfilesdir}/%{name}.conf
%{_sysconfdir}/libreport/events.d/collect_dnf.conf
%{_bindir}/%{name}-automatic

%dir /etc/dnf/{vars,modules.d,modules.defaults.d,protected.d,plugins}
%dir %{_datadir}/bash-completion/completions
%config(noreplace) /etc/dnf/%{name}.conf
%config(noreplace) /etc/dnf/protected.d/%{name}.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) /etc/dnf/automatic.conf
%ghost %{_localstatedir}/log/hawkey.log
%ghost %{_localstatedir}/log/%{name}.log
%ghost %{_localstatedir}/log/%{name}.librepo.log
%ghost %{_localstatedir}/log/%{name}.rpm.log
%ghost %{_localstatedir}/log/%{name}.plugin.log
%ghost %{_sharedstatedir}/%{name}
%ghost %{_sharedstatedir}/%{name}/groups.json
%ghost %{_sharedstatedir}/%{name}/yumdb
%ghost %{_sharedstatedir}/%{name}/history
%if %{with python3}
%{python3_sitelib}/%{name}/automatic/
%else
%{python2_sitelib}/%{name}/automatic/
%endif

%if %{with python2}
%files -n python2-%{name}
%{_bindir}/%{name}-2
%{python2_sitelib}/%{name}/
%dir %{py2pluginpath}
%exclude %{python2_sitelib}/%{name}/automatic
%endif

%if %{with python3}
%files -n python3-%{name}
%{_bindir}/%{name}-3
%{python3_sitelib}/%{name}/
%dir %{py3pluginpath}
%dir %{py3pluginpath}/__pycache__
%exclude %{python3_sitelib}/%{name}/automatic
%endif

%files -n yum
%{_bindir}/yum
%{_sysconfdir}/yum.conf
%{_sysconfdir}/yum/{vars,pluginconf.d,protected.d}

%files help
%{_mandir}/man5/yum.conf.5.*
%{_mandir}/man5/%{name}.conf.5*
%{_mandir}/man8/yum*
%{_mandir}/man8/dnf*

%changelog
* Fri Sep 20 2019 yanzhihua<yanzhihua4@huawei.com> - 4.0.4-2
- Package init.

