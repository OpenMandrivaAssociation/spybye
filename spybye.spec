Summary:	A proxy to help finding malware
Name:		spybye
Version:	0.3
Release:	%mkrel 6
Group:		System/Servers
License:	GPLv2
URL:		http://www.monkey.org/~provos/spybye/
Source0:	http://www.monkey.org/~provos/%{name}-%{version}.tar.gz
Source1:	http://www.monkey.org/~provos/%{name}-%{version}.tar.gz.sig
Source2:	spybye.init
Source3:	spybye.sysconfig
Source4:	spybye.logrotate
Source5:	README.Mandriva
Patch0:		spybye-memleak.diff
BuildRequires:	autoconf2.5
BuildRequires:	libevent-devel
#BuildRequires:	clamav-devel
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires:	clamav
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The crawl tool provide a proxy server through which web pages can be fetched
and analyzed for potentially dangerous includes. To use , you need to configure
your web browser to use the port configured by -p as proxy port.


%prep

%setup -q -n %{name}-%{version}
%patch0 -p0

cp %{SOURCE2} %{name}.init
cp %{SOURCE3} %{name}.sysconfig
cp %{SOURCE4} %{name}.logrotate
cp %{SOURCE5} README.Mandriva

%build

%configure2_5x \
    --bindir=%{_sbindir} \
    --datadir=%{_localstatedir}/lib

%make

%install
rm -rf %{buildroot}

# don't fiddle with the initscript!
export DONT_GPRINTIFY=1

%makeinstall_std

install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_sysconfdir}/sysconfig
install -d %{buildroot}%{_sysconfdir}/logrotate.d
install -d %{buildroot}/var/log/%{name}

install -m0755 %{name}.init %{buildroot}%{_initrddir}/%{name}
install -m0644 %{name}.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -m0644 %{name}.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

# create ghostfile
touch %{buildroot}/var/log/%{name}/%{name}.log

%post
%create_ghostfile /var/log/%{name}/%{name}.log root root 0644
%_post_service %{name}

%preun
%_preun_service %{name}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README.Mandriva
%attr(0755,root,root) %{_initrddir}/%{name}
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/logrotate.d/%{name}
%attr(0755,root,root) %{_sbindir}/*
%dir %{_localstatedir}/lib/%{name}
%{_localstatedir}/lib/%{name}/*
%dir %attr(0755,root,root) /var/log/%{name}
%attr(0644,root,root) %ghost %config(noreplace) /var/log/%{name}/%{name}.log
%attr(0644,root,root) %{_mandir}/man?/*
