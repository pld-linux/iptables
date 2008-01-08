#
# TODO:
#		- fix makefile (-D_UNKNOWN_KERNEL_POINTER_SIZE issue)
#
# Conditional build:
%bcond_without	doc		# without documentation (HOWTOS) which needed TeX
%bcond_without	dist_kernel	# without distribution kernel
%bcond_without  vserver         # kernel build without vserver
#
%define		netfilter_snap		20070806
%define		llh_version		7:2.6.22.1
%define		name6			ip6tables
#
%define		rel 8
Summary:	Extensible packet filtering system && extensible NAT system
Summary(pl.UTF-8):	System filtrowania pakietów oraz system translacji adresów (NAT)
Summary(pt_BR.UTF-8):	Ferramenta para controlar a filtragem de pacotes no kernel-2.6.x
Summary(ru.UTF-8):	Утилиты для управления пакетными фильтрами ядра Linux
Summary(uk.UTF-8):	Утиліти для керування пакетними фільтрами ядра Linux
Summary(zh_CN.UTF-8):	Linux内核包过滤管理工具
Name:		iptables
Version:	1.3.8
Release:	%{rel}
License:	GPL
Group:		Networking/Daemons
Source0:	ftp://ftp.netfilter.org/pub/iptables/%{name}-%{version}.tar.bz2
# Source0-md5:	0a9209f928002e5eee9cdff8fef4d4b3
Source1:	cvs://cvs.samba.org/netfilter/%{name}-howtos.tar.bz2
# Source1-md5:	2ed2b452daefe70ededd75dc0061fd07
Source2:	%{name}.init
Source3:	%{name6}.init
Patch0:		%{name}-%{netfilter_snap}.patch
Patch1:		%{name}-man.patch
# http://www.linuximq.net/patchs/iptables-1.3.6-imq.diff
Patch2:		%{name}-1.3.0-imq1.diff
Patch3:		%{name}-connbytes-xtables.patch
Patch4:		grsecurity-1.2.11-%{name}.patch
Patch5:		%{name}-layer7.patch
Patch6:		%{name}-old-1.3.7.patch
Patch7:		%{name}-account.patch
# http://people.linux-vserver.org/~dhozac/p/m/iptables-1.3.5-owner-xid.patch
Patch8:		%{name}-1.3.5-owner-xid.patch
Patch999:	%{name}-llh-dirty-hack.patch
URL:		http://www.netfilter.org/
%if %{with doc}
BuildRequires:	sed >= 4.0
BuildRequires:	sgml-tools
BuildRequires:	sgmls
BuildRequires:	tetex-dvips
BuildRequires:	tetex-format-latex
BuildRequires:	tetex-latex
BuildRequires:	tetex-tex-babel
%endif
%if %{with dist_kernel} && %{netfilter_snap} != 0
BuildRequires:	kernel-headers(netfilter) >= %{netfilter_snap}
BuildRequires:	kernel-source
Requires:	kernel(netfilter) >= %{netfilter_snap}
%endif
#BuildRequires:	linux-libc-headers >= %{llh_version}
BuildConflicts:	kernel-headers < 2.3.0
Provides:	firewall-userspace-tool
Obsoletes:	ipchains
Obsoletes:	iptables-ipp2p
Obsoletes:	iptables24-compat
Obsoletes:	netfilter
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
An extensible NAT system, and an extensible packet filtering system.
Replacement of ipchains in 2.4 and higher kernels.

%description -l pl.UTF-8
Wydajny system translacji adresów (NAT) oraz system filtrowania
pakietów. Zamiennik ipchains w jądrach 2.4 i nowszych.

%description -l pt_BR.UTF-8
Esta é a ferramenta que controla o código de filtragem de pacotes do
kernel 2.4, obsoletando ipchains. Com esta ferramenta você pode
configurar filtros de pacotes, NAT, mascaramento (masquerading),
regras dinâmicas (stateful inspection), etc.

%description -l ru.UTF-8
iptables управляют кодом фильтрации сетевых пакетов в ядре Linux. Они
позволяют вам устанавливать межсетевые экраны (firewalls) и IP
маскарадинг, и т.п.

%description -l uk.UTF-8
iptables управляють кодом фільтрації пакетів мережі в ядрі Linux. Вони
дозволяють вам встановлювати міжмережеві екрани (firewalls) та IP
маскарадинг, тощо.

%package devel
Summary:	Libraries and headers for developing iptables extensions
Summary(pl.UTF-8):	Biblioteki i nagłówki do tworzenia rozszerzeń iptables
Group:		Development/Libraries
Obsoletes:	iptables24-devel

%description devel
Libraries and headers for developing iptables extensions.

%description devel -l pl.UTF-8
Biblioteki i pliki nagłówkowe niezbędne do tworzenia rozszerzeń dla
iptables.

%package init
Summary:	Iptables init (RedHat style)
Summary(pl.UTF-8):	Iptables init (w stylu RedHata)
Release:	%{rel}
Group:		Networking/Admin
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}
Requires:	rc-scripts
Obsoletes:	firewall-init
Obsoletes:	firewall-init-ipchains
Obsoletes:	iptables24-init

%description init
Iptables-init is meant to provide an alternate way than firewall-init
to start and stop packet filtering through iptables(8).

%description init -l pl.UTF-8
Iptables-init ma na celu udostępnienie alternatywnego w stosunku do
firewall-init sposobu włączania i wyłączania filtrów IP jądra poprzez
iptables(8).

%prep
%setup -q -a1
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%if %{with vserver}
%patch8 -p1
%endif

#patch999 -p1

chmod 755 extensions/.*-test*

%build
%{__make} all experimental \
	CC="%{__cc}" \
	COPT_FLAGS="%{rpmcflags} -D%{!?debug:N}DEBUG" \
	KERNEL_DIR="%{_kernelsrcdir}" \
	LIBDIR="%{_libdir}" \
	DO_SELINUX=1 \
	LDLIBS="-ldl"

%if %{with doc}
%{__make} -j1 -C iptables-howtos
sed -i 's:$(HTML_HOWTOS)::g; s:$(PSUS_HOWTOS)::g' iptables-howtos/Makefile
%endif

# Make a library, needed for OpenVCP
ar rcs libiptables.a iptables.o
ar rcs libip6tables.a ip6tables.o

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,%{_includedir},%{_libdir},%{_mandir}/man3}

echo ".so iptables-save.8" > %{name6}-save.8
echo ".so iptables-restore.8" > %{name6}-restore.8

%{__make} install install-experimental \
	DESTDIR=$RPM_BUILD_ROOT \
	BINDIR=%{_sbindir} \
	MANDIR=%{_mandir} \
	LIBDIR=%{_libdir}

install extensions/*so $RPM_BUILD_ROOT%{_libdir}/iptables

echo ".so iptables.8" > $RPM_BUILD_ROOT%{_mandir}/man8/%{name6}.8

# Devel stuff
cp -a include/{lib*,ip*} $RPM_BUILD_ROOT%{_includedir}
install lib*.a $RPM_BUILD_ROOT%{_libdir}
install lib*/lib*.a $RPM_BUILD_ROOT%{_libdir}
install libipq/*.3 $RPM_BUILD_ROOT%{_mandir}/man3

install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name6}

%clean
rm -rf $RPM_BUILD_ROOT

%post init
/sbin/chkconfig --add %{name}
/sbin/chkconfig --add %{name6}

%preun init
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del %{name}
	/sbin/chkconfig --del %{name6}
fi

%files
%defattr(644,root,root,755)
%{?with_doc:%doc iptables-howtos/{NAT,networking-concepts,packet-filtering}-HOWTO*}
%attr(755,root,root) %{_sbindir}/iptables
%attr(755,root,root) %{_sbindir}/iptables-restore
%attr(755,root,root) %{_sbindir}/iptables-save
%attr(755,root,root) %{_sbindir}/iptables-xml
%attr(755,root,root) %{_sbindir}/ip6tables
%attr(755,root,root) %{_sbindir}/ip6tables-restore
%attr(755,root,root) %{_sbindir}/ip6tables-save
%dir %{_libdir}/iptables
%attr(755,root,root) %{_libdir}/iptables/libip6t_CONNMARK.so
%attr(755,root,root) %{_libdir}/iptables/libip6t_CONNSECMARK.so
%attr(755,root,root) %{_libdir}/iptables/libip6t_HL.so
%attr(755,root,root) %{_libdir}/iptables/libip6t_IMQ.so
%attr(755,root,root) %{_libdir}/iptables/libip6t_LOG.so
%attr(755,root,root) %{_libdir}/iptables/libip6t_MARK.so
%attr(755,root,root) %{_libdir}/iptables/libip6t_NFLOG.so
%attr(755,root,root) %{_libdir}/iptables/libip6t_NFQUEUE.so
%attr(755,root,root) %{_libdir}/iptables/libip6t_REJECT.so
%attr(755,root,root) %{_libdir}/iptables/libip6t_ROUTE.so
%attr(755,root,root) %{_libdir}/iptables/libip6t_SECMARK.so
%attr(755,root,root) %{_libdir}/iptables/libip6t_TCPMSS.so
%attr(755,root,root) %{_libdir}/iptables/libip6t_ah.so
%attr(755,root,root) %{_libdir}/iptables/libip6t_connmark.so
%attr(755,root,root) %{_libdir}/iptables/libip6t_esp.so
%attr(755,root,root) %{_libdir}/iptables/libip6t_eui64.so
%attr(755,root,root) %{_libdir}/iptables/libip6t_frag.so
%attr(755,root,root) %{_libdir}/iptables/libip6t_hashlimit.so
%attr(755,root,root) %{_libdir}/iptables/libip6t_hl.so
%attr(755,root,root) %{_libdir}/iptables/libip6t_icmp6.so
%attr(755,root,root) %{_libdir}/iptables/libip6t_ipv6header.so
%attr(755,root,root) %{_libdir}/iptables/libip6t_length.so
%attr(755,root,root) %{_libdir}/iptables/libip6t_limit.so
%attr(755,root,root) %{_libdir}/iptables/libip6t_mac.so
%attr(755,root,root) %{_libdir}/iptables/libip6t_mark.so
%attr(755,root,root) %{_libdir}/iptables/libip6t_mh.so
%attr(755,root,root) %{_libdir}/iptables/libip6t_multiport.so
%attr(755,root,root) %{_libdir}/iptables/libip6t_owner.so
%attr(755,root,root) %{_libdir}/iptables/libip6t_physdev.so
%attr(755,root,root) %{_libdir}/iptables/libip6t_policy.so
%attr(755,root,root) %{_libdir}/iptables/libip6t_rt.so
%attr(755,root,root) %{_libdir}/iptables/libip6t_sctp.so
%attr(755,root,root) %{_libdir}/iptables/libip6t_standard.so
%attr(755,root,root) %{_libdir}/iptables/libip6t_state.so
%attr(755,root,root) %{_libdir}/iptables/libip6t_tcp.so
%attr(755,root,root) %{_libdir}/iptables/libip6t_udp.so
%attr(755,root,root) %{_libdir}/iptables/libipt_ACCOUNT.so
%attr(755,root,root) %{_libdir}/iptables/libipt_CLASSIFY.so
%attr(755,root,root) %{_libdir}/iptables/libipt_CLUSTERIP.so
%attr(755,root,root) %{_libdir}/iptables/libipt_CONNMARK.so
%attr(755,root,root) %{_libdir}/iptables/libipt_CONNSECMARK.so
%attr(755,root,root) %{_libdir}/iptables/libipt_DNAT.so
%attr(755,root,root) %{_libdir}/iptables/libipt_DSCP.so
%attr(755,root,root) %{_libdir}/iptables/libipt_ECN.so
%attr(755,root,root) %{_libdir}/iptables/libipt_IMQ.so
%attr(755,root,root) %{_libdir}/iptables/libipt_IPMARK.so
%attr(755,root,root) %{_libdir}/iptables/libipt_IPV4OPTSSTRIP.so
%attr(755,root,root) %{_libdir}/iptables/libipt_LOG.so
%attr(755,root,root) %{_libdir}/iptables/libipt_MARK.so
%attr(755,root,root) %{_libdir}/iptables/libipt_MASQUERADE.so
%attr(755,root,root) %{_libdir}/iptables/libipt_MIRROR.so
%attr(755,root,root) %{_libdir}/iptables/libipt_NETMAP.so
%attr(755,root,root) %{_libdir}/iptables/libipt_NFLOG.so
%attr(755,root,root) %{_libdir}/iptables/libipt_NFQUEUE.so
%attr(755,root,root) %{_libdir}/iptables/libipt_NOTRACK.so
%attr(755,root,root) %{_libdir}/iptables/libipt_REDIRECT.so
%attr(755,root,root) %{_libdir}/iptables/libipt_REJECT.so
%attr(755,root,root) %{_libdir}/iptables/libipt_ROUTE.so
%attr(755,root,root) %{_libdir}/iptables/libipt_SAME.so
%attr(755,root,root) %{_libdir}/iptables/libipt_SECMARK.so
%attr(755,root,root) %{_libdir}/iptables/libipt_SET.so
%attr(755,root,root) %{_libdir}/iptables/libipt_SNAT.so
%attr(755,root,root) %{_libdir}/iptables/libipt_TARPIT.so
%attr(755,root,root) %{_libdir}/iptables/libipt_TCPMSS.so
%attr(755,root,root) %{_libdir}/iptables/libipt_TOS.so
%attr(755,root,root) %{_libdir}/iptables/libipt_TTL.so
%attr(755,root,root) %{_libdir}/iptables/libipt_ULOG.so
%attr(755,root,root) %{_libdir}/iptables/libipt_account.so
%attr(755,root,root) %{_libdir}/iptables/libipt_addrtype.so
%attr(755,root,root) %{_libdir}/iptables/libipt_ah.so
%attr(755,root,root) %{_libdir}/iptables/libipt_comment.so
%attr(755,root,root) %{_libdir}/iptables/libipt_connbytes.so
%attr(755,root,root) %{_libdir}/iptables/libipt_connlimit.so
%attr(755,root,root) %{_libdir}/iptables/libipt_connmark.so
%attr(755,root,root) %{_libdir}/iptables/libipt_conntrack.so
%attr(755,root,root) %{_libdir}/iptables/libipt_dccp.so
%attr(755,root,root) %{_libdir}/iptables/libipt_dscp.so
%attr(755,root,root) %{_libdir}/iptables/libipt_ecn.so
%attr(755,root,root) %{_libdir}/iptables/libipt_esp.so
%attr(755,root,root) %{_libdir}/iptables/libipt_geoip.so
%attr(755,root,root) %{_libdir}/iptables/libipt_hashlimit.so
%attr(755,root,root) %{_libdir}/iptables/libipt_helper.so
%attr(755,root,root) %{_libdir}/iptables/libipt_icmp.so
%attr(755,root,root) %{_libdir}/iptables/libipt_ipp2p.so
%attr(755,root,root) %{_libdir}/iptables/libipt_iprange.so
%attr(755,root,root) %{_libdir}/iptables/libipt_ipv4options.so
%attr(755,root,root) %{_libdir}/iptables/libipt_layer7.so
%attr(755,root,root) %{_libdir}/iptables/libipt_length.so
%attr(755,root,root) %{_libdir}/iptables/libipt_limit.so
%attr(755,root,root) %{_libdir}/iptables/libipt_mac.so
%attr(755,root,root) %{_libdir}/iptables/libipt_mark.so
%attr(755,root,root) %{_libdir}/iptables/libipt_multiport.so
%attr(755,root,root) %{_libdir}/iptables/libipt_owner.so
%attr(755,root,root) %{_libdir}/iptables/libipt_physdev.so
%attr(755,root,root) %{_libdir}/iptables/libipt_pkttype.so
%attr(755,root,root) %{_libdir}/iptables/libipt_policy.so
%attr(755,root,root) %{_libdir}/iptables/libipt_quota.so
%attr(755,root,root) %{_libdir}/iptables/libipt_realm.so
%attr(755,root,root) %{_libdir}/iptables/libipt_recent.so
%attr(755,root,root) %{_libdir}/iptables/libipt_rpc.so
%attr(755,root,root) %{_libdir}/iptables/libipt_sctp.so
%attr(755,root,root) %{_libdir}/iptables/libipt_set.so
%attr(755,root,root) %{_libdir}/iptables/libipt_standard.so
%attr(755,root,root) %{_libdir}/iptables/libipt_state.so
%attr(755,root,root) %{_libdir}/iptables/libipt_statistic.so
%attr(755,root,root) %{_libdir}/iptables/libipt_string.so
%attr(755,root,root) %{_libdir}/iptables/libipt_tcp.so
%attr(755,root,root) %{_libdir}/iptables/libipt_tcpmss.so
%attr(755,root,root) %{_libdir}/iptables/libipt_time.so
%attr(755,root,root) %{_libdir}/iptables/libipt_tos.so
%attr(755,root,root) %{_libdir}/iptables/libipt_ttl.so
%attr(755,root,root) %{_libdir}/iptables/libipt_u32.so
%attr(755,root,root) %{_libdir}/iptables/libipt_udp.so
%attr(755,root,root) %{_libdir}/iptables/libipt_unclean.so
%{_mandir}/man8/*

%files devel
%defattr(644,root,root,755)
%{?with_doc:%doc iptables-howtos/netfilter-hacking-HOWTO*}
%{_libdir}/lib*.a
%{_includedir}/*.h
%dir %{_includedir}/libip*
%{_includedir}/libip*/*.h
%{_mandir}/man3/*

%files init
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/iptables
%attr(754,root,root) /etc/rc.d/init.d/ip6tables
