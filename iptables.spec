%define		ULOG_version	0.2
Summary:	extensible packet filtering system && extensible NAT system
Summary(pl):	system filtrowania pakietów oraz system translacji adresów (NAT)
Name:		iptables
Version:	1.1.1
Release:	2
License:	GPL
Group:		Networking/Daemons
Group(pl):	Sieciowe/Serwery
URL:		http://netfilter.kernelnotes.org/
Vendor:		Netfilter mailing list <netfilter@lists.samba.org>
Source0:	http://netfilter.kernelnotes.org/%{name}-%{version}.tar.bz2
Source1:	cvs://cvs.samba.org/netfilter/%{name}-howtos.tar.bz2
Source2:	rc.firewall
Source3:	ftp://ftp.sunbeam.franken.de/pub/netfilter/netfilter_ULOG-%{ULOG_version}.tar.gz
Source4:	ulogd.init
Source5:	ulogd.sysconfig
Source6:	ulogd.logrotate
BuildRequires:	sgml-tools
#Requires:	kernel >= 2.4.0test4
Obsoletes:	netfilter
Obsoletes:	ipchains
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc

%description
An extensible NAT system, and an extensible packet filtering system.

%description -l pl
Wydajny system translacji adresów (NAT) oraz system filtrowania
pakietów.

%prep
%setup -q -a1 -a3

%build
%{__make} -C iptables-howtos NAT-HOWTO.html packet-filtering-HOWTO.html \
	# netfilter-hacking-HOWTO.html networking-concepts-HOWTO.html
%{__make} depend 2> /dev/null || :
%{__make} COPT_FLAGS="$RPM_OPT_FLAGS -DIP6T_LIB_DIR=\\\"%{_libdir}/iptables\\\"" \
	LIBDIR="%{_libdir}" \
	all

cd netfilter_ULOG-%{ULOG_version}
%{__make} -C iptables \
	CFLAGS="$RPM_OPT_FLAGS -DNETFILTER_VERSION=\\\"%{version}\\\" -fPIC \
	-I../../include -DIP6T_LIB_DIR=\\\"%{_libdir}/iptables\\\"" \
	LIBDIR="%{_libdir}" \
	libipt_ULOG.so

%{__make} -C libipulog \
	CFLAGS="$RPM_OPT_FLAGS -I. -I./include \
	-DIP6T_LIB_DIR=\\\"%{_libdir}/iptables\\\"" \
	LIBDIR="%{_libdir}" \
	libipulog.o libipulog.a ulog_test

%{__make} -C ulogd \
	CFLAGS="$RPM_OPT_FLAGS -I. -I./include -I../libipulog/include \
	-DIP6T_LIB_DIR=\\\"%{_libdir}/iptables\\\" \
	-DULOGD_LOGFILE=\\\"/var/log/iptables.ulog\\\" \
	-DULOGD_PLUGIN_DIR=\\\"%{_libdir}/iptables/ulogd\\\"" \
	LIBDIR="%{_libdir}" \
	all

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/{sysconfig,logrotate.d,rc.d/{init.d,rc{0,1,2,3,4,5,6}.d}}
install -d $RPM_BUILD_ROOT/var/log

%{__make} install DESTDIR=$RPM_BUILD_ROOT \
	BINDIR=%{_sbindir} \
	MANDIR=%{_mandir} \
	LIBDIR=%{_libdir}

install ip6tables $RPM_BUILD_ROOT%{_sbindir}/

install -d $RPM_BUILD_ROOT%{_libdir}/iptables/ulogd
install netfilter_ULOG-%{ULOG_version}/iptables/libipt_ULOG.so $RPM_BUILD_ROOT%{_libdir}/iptables
install netfilter_ULOG-%{ULOG_version}/libipulog/ulog_test $RPM_BUILD_ROOT%{_libdir}/iptables/ulogd
install netfilter_ULOG-%{ULOG_version}/ulogd/ulogd $RPM_BUILD_ROOT%{_sbindir}
install netfilter_ULOG-%{ULOG_version}/ulogd/extensions/*.so $RPM_BUILD_ROOT%{_libdir}/iptables/ulogd

install %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/ulogd
install %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/ulogd
install %{SOURCE6} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/ulogd

install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/
ln -s ../rc.firewall $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/rc0.d/K91firewall
ln -s ../rc.firewall $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/rc1.d/K91firewall
ln -s ../rc.firewall $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/rc2.d/S09firewall
ln -s ../rc.firewall $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/rc3.d/S09firewall
ln -s ../rc.firewall $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/rc4.d/S09firewall
ln -s ../rc.firewall $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/rc5.d/S09firewall
ln -s ../rc.firewall $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/rc6.d/K91firewall

mv -f netfilter_ULOG-%{ULOG_version}/README README.ulogd

gzip -9nf README.ulogd $RPM_BUILD_ROOT%{_mandir}/man*/*

strip --strip-unneeded $RPM_BUILD_ROOT{%{_libdir}/*/*.so,%{_sbindir}/*} || :
strip --strip-unneeded $RPM_BUILD_ROOT%{_libdir}/*/*/* || :

touch $RPM_BUILD_ROOT/var/log/iptables.ulog

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -f /var/log/iptables.ulog ]; then
	touch /var/log/iptables.ulog
	chmod 640 /var/log/iptables.ulog
fi

/sbin/chkconfig --add ulogd
if [ -f /var/lock/subsys/ulogd ]; then
    /etc/rc.d/init.d/ulogd restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/ulogd start\" to start ulogd daemon." 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/ulogd ]; then
		/etc/rc.d/init.d/ulogd stop 1>&2
	fi
	/sbin/chkconfig --del ulogd
fi

%files
%defattr(644,root,root,755)
%doc README.ulogd.gz */*.html
%{_sysconfdir}/rc.d/rc*.d/*firewall
%attr(754,root,root) %config(noreplace) %verify(not mtime md5 size) %{_sysconfdir}/rc.d/rc.firewall
%attr(640,root,root) %config(noreplace) %verify(not mtime md5 size) /etc/sysconfig/ulogd
%attr(640,root,root) /etc/logrotate.d/ulogd
%attr(754,root,root) /etc/rc.d/init.d/ulogd

%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_libdir}/iptables/*.so
%attr(755,root,root) %{_libdir}/iptables/ulogd/*.so
%attr(755,root,root) %{_libdir}/iptables/ulogd/ulog_test

%attr(640,root,root) %ghost /var/log/*

%{_mandir}/man*/*
