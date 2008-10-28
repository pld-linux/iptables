#
# TODO:
# - fix makefile (-D_UNKNOWN_KERNEL_POINTER_SIZE issue)
# - owner needs rewrite to xt
# - add manual sections from xtable-addons
# - ACCOUNT has been removed from iptables-20070806.patch, now should be taken
#   from http://www.intra2net.com/de/produkte/opensource/ipt_account/libipt_ACCOUNT-1.3.tar.gz
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
%define		rel 4
Summary:	Extensible packet filtering system && extensible NAT system
Summary(pl.UTF-8):	System filtrowania pakietów oraz system translacji adresów (NAT)
Summary(pt_BR.UTF-8):	Ferramenta para controlar a filtragem de pacotes no kernel-2.6.x
Summary(ru.UTF-8):	Утилиты для управления пакетными фильтрами ядра Linux
Summary(uk.UTF-8):	Утиліти для керування пакетними фільтрами ядра Linux
Summary(zh_CN.UTF-8):	Linux内核包过滤管理工具
Name:		iptables
Version:	1.4.1.1
Release:	%{rel}
License:	GPL
Group:		Networking/Daemons
Source0:	ftp://ftp.netfilter.org/pub/iptables/%{name}-%{version}.tar.bz2
# Source0-md5:	723fa88d8a0915e184f99e03e9bf06cb
Source1:	cvs://cvs.samba.org/netfilter/%{name}-howtos.tar.bz2
# Source1-md5:	2ed2b452daefe70ededd75dc0061fd07
Source2:	%{name}.init
Source3:	%{name6}.init
Patch0:		%{name}-%{netfilter_snap}.patch
Patch1:		%{name}-man.patch
# based on http://www.linuximq.net/patchs/iptables-1.4.0-imq.diff
Patch2:		%{name}-imq.patch
# http://www.balabit.com/downloads/files/tproxy/tproxy-iptables-20080204-1915.patch
Patch3:		%{name}-tproxy.patch
Patch4:		%{name}-stealth.patch
# almost based on iptables-1.4-for-kernel-2.6.20forward-layer7-2.18.patch
# http://switch.dl.sourceforge.net/sourceforge/l7-filter/netfilter-layer7-v2.18.tar.gz
Patch5:		%{name}-layer7.patch
Patch6:		%{name}-old-1.3.7.patch
# based on http://www.svn.barbara.eu.org/ipt_account/attachment/wiki/Software/ipt_account-0.1.21-20070804164729.tar.gz?format=raw
Patch7:		%{name}-account.patch
# http://people.linux-vserver.org/~dhozac/p/m/iptables-1.3.5-owner-xid.patch
Patch8:		%{name}-1.3.5-owner-xid.patch
Patch9:		%{name}-batch.patch
Patch10:	%{name}-headers.patch
Patch11:	%{name}-owner-struct-size-vs.patch
Patch999:	%{name}-llh-dirty-hack.patch
URL:		http://www.netfilter.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
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
BuildRequires:	kernel%{_alt_kernel}-headers(netfilter) >= %{netfilter_snap}
BuildRequires:	kernel%{_alt_kernel}-source
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
%patch3 -p0
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%if %{with vserver}
#patch8 -p1
%patch11 -p1
%endif
%patch9 -p1
%patch10 -p1

#patch999 -p1

chmod 755 extensions/.*-test*

%build
%{__libtoolize}
%{__aclocal}
%{__automake}
%configure \
	--with-kbuild=%{_kernelsrcdir} \
	--with-ksource=%{_kernelsrcdir} \
	--enable-devel \
	--enable-libipq \
	--enable-shared

%{__make} -j1 all \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -D%{!?debug:N}DEBUG" \
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

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	BINDIR=%{_sbindir} \
	MANDIR=%{_mandir} \
	LIBDIR=%{_libdir}

# install library needed for collectd:
install libiptc/libiptc.a $RPM_BUILD_ROOT%{_libdir}

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
%attr(755,root,root) %{_bindir}/iptables-xml
%attr(755,root,root) %{_sbindir}/iptables
%attr(755,root,root) %{_sbindir}/iptables-batch
%attr(755,root,root) %{_sbindir}/iptables-multi
%attr(755,root,root) %{_sbindir}/iptables-restore
%attr(755,root,root) %{_sbindir}/iptables-save
%attr(755,root,root) %{_sbindir}/ip6tables
%attr(755,root,root) %{_sbindir}/ip6tables-batch
%attr(755,root,root) %{_sbindir}/ip6tables-multi
%attr(755,root,root) %{_sbindir}/ip6tables-restore
%attr(755,root,root) %{_sbindir}/ip6tables-save
%dir %{_libdir}/xtables
%if %{with dist_kernel}
%attr(755,root,root) %{_libdir}/xtables/libip6t_ah.so
%attr(755,root,root) %{_libdir}/xtables/libip6t_dst.so
%attr(755,root,root) %{_libdir}/xtables/libip6t_eui64.so
%attr(755,root,root) %{_libdir}/xtables/libip6t_frag.so
%attr(755,root,root) %{_libdir}/xtables/libip6t_hbh.so
%attr(755,root,root) %{_libdir}/xtables/libip6t_hl.so
%attr(755,root,root) %{_libdir}/xtables/libip6t_HL.so
%attr(755,root,root) %{_libdir}/xtables/libip6t_icmp6.so
%attr(755,root,root) %{_libdir}/xtables/libip6t_IMQ.so
%attr(755,root,root) %{_libdir}/xtables/libip6t_ipv6header.so
%attr(755,root,root) %{_libdir}/xtables/libip6t_LOG.so
%attr(755,root,root) %{_libdir}/xtables/libip6t_mh.so
%attr(755,root,root) %{_libdir}/xtables/libip6t_policy.so
%attr(755,root,root) %{_libdir}/xtables/libip6t_REJECT.so
%attr(755,root,root) %{_libdir}/xtables/libip6t_ROUTE.so
%attr(755,root,root) %{_libdir}/xtables/libip6t_rt.so
%attr(755,root,root) %{_libdir}/xtables/libipt_account.so
#attr(755,root,root) %{_libdir}/xtables/libipt_ACCOUNT.so
%attr(755,root,root) %{_libdir}/xtables/libipt_addrtype.so
%attr(755,root,root) %{_libdir}/xtables/libipt_ah.so
%attr(755,root,root) %{_libdir}/xtables/libipt_CLUSTERIP.so
%attr(755,root,root) %{_libdir}/xtables/libipt_DNAT.so
%attr(755,root,root) %{_libdir}/xtables/libipt_ecn.so
%attr(755,root,root) %{_libdir}/xtables/libipt_ECN.so
%attr(755,root,root) %{_libdir}/xtables/libipt_icmp.so
%attr(755,root,root) %{_libdir}/xtables/libipt_IMQ.so
%attr(755,root,root) %{_libdir}/xtables/libipt_ipv4options.so
%attr(755,root,root) %{_libdir}/xtables/libipt_IPV4OPTSSTRIP.so
%attr(755,root,root) %{_libdir}/xtables/libipt_layer7.so
%attr(755,root,root) %{_libdir}/xtables/libipt_LOG.so
%attr(755,root,root) %{_libdir}/xtables/libipt_MASQUERADE.so
%attr(755,root,root) %{_libdir}/xtables/libipt_MIRROR.so
%attr(755,root,root) %{_libdir}/xtables/libipt_NETMAP.so
%attr(755,root,root) %{_libdir}/xtables/libipt_policy.so
%attr(755,root,root) %{_libdir}/xtables/libipt_realm.so
%attr(755,root,root) %{_libdir}/xtables/libipt_recent.so
%attr(755,root,root) %{_libdir}/xtables/libipt_REDIRECT.so
%attr(755,root,root) %{_libdir}/xtables/libipt_REJECT.so
%attr(755,root,root) %{_libdir}/xtables/libipt_ROUTE.so
%attr(755,root,root) %{_libdir}/xtables/libipt_rpc.so
%attr(755,root,root) %{_libdir}/xtables/libipt_SAME.so
%attr(755,root,root) %{_libdir}/xtables/libipt_set.so
%attr(755,root,root) %{_libdir}/xtables/libipt_SET.so
%attr(755,root,root) %{_libdir}/xtables/libipt_SNAT.so
%attr(755,root,root) %{_libdir}/xtables/libipt_stealth.so
%attr(755,root,root) %{_libdir}/xtables/libipt_ttl.so
%attr(755,root,root) %{_libdir}/xtables/libipt_TTL.so
%attr(755,root,root) %{_libdir}/xtables/libipt_ULOG.so
%attr(755,root,root) %{_libdir}/xtables/libipt_unclean.so
%attr(755,root,root) %{_libdir}/xtables/libxt_CLASSIFY.so
%attr(755,root,root) %{_libdir}/xtables/libxt_comment.so
%attr(755,root,root) %{_libdir}/xtables/libxt_connbytes.so
%attr(755,root,root) %{_libdir}/xtables/libxt_connlimit.so
%attr(755,root,root) %{_libdir}/xtables/libxt_connmark.so
%attr(755,root,root) %{_libdir}/xtables/libxt_CONNMARK.so
%attr(755,root,root) %{_libdir}/xtables/libxt_CONNSECMARK.so
%attr(755,root,root) %{_libdir}/xtables/libxt_conntrack.so
%attr(755,root,root) %{_libdir}/xtables/libxt_dccp.so
%attr(755,root,root) %{_libdir}/xtables/libxt_dscp.so
%attr(755,root,root) %{_libdir}/xtables/libxt_DSCP.so
%attr(755,root,root) %{_libdir}/xtables/libxt_esp.so
%attr(755,root,root) %{_libdir}/xtables/libxt_hashlimit.so
%attr(755,root,root) %{_libdir}/xtables/libxt_helper.so
%attr(755,root,root) %{_libdir}/xtables/libxt_iprange.so
%attr(755,root,root) %{_libdir}/xtables/libxt_length.so
%attr(755,root,root) %{_libdir}/xtables/libxt_limit.so
%attr(755,root,root) %{_libdir}/xtables/libxt_mac.so
%attr(755,root,root) %{_libdir}/xtables/libxt_mark.so
%attr(755,root,root) %{_libdir}/xtables/libxt_MARK.so
%attr(755,root,root) %{_libdir}/xtables/libxt_multiport.so
%attr(755,root,root) %{_libdir}/xtables/libxt_NFLOG.so
%attr(755,root,root) %{_libdir}/xtables/libxt_NFQUEUE.so
%attr(755,root,root) %{_libdir}/xtables/libxt_NOTRACK.so
%attr(755,root,root) %{_libdir}/xtables/libxt_owner.so
%attr(755,root,root) %{_libdir}/xtables/libxt_physdev.so
%attr(755,root,root) %{_libdir}/xtables/libxt_pkttype.so
%attr(755,root,root) %{_libdir}/xtables/libxt_quota.so
%attr(755,root,root) %{_libdir}/xtables/libxt_RATEEST.so
%attr(755,root,root) %{_libdir}/xtables/libxt_rateest.so
%attr(755,root,root) %{_libdir}/xtables/libxt_sctp.so
%attr(755,root,root) %{_libdir}/xtables/libxt_SECMARK.so
%attr(755,root,root) %{_libdir}/xtables/libxt_socket.so
%attr(755,root,root) %{_libdir}/xtables/libxt_standard.so
%attr(755,root,root) %{_libdir}/xtables/libxt_state.so
%attr(755,root,root) %{_libdir}/xtables/libxt_statistic.so
%attr(755,root,root) %{_libdir}/xtables/libxt_string.so
%attr(755,root,root) %{_libdir}/xtables/libxt_tcpmss.so
%attr(755,root,root) %{_libdir}/xtables/libxt_TCPMSS.so
%attr(755,root,root) %{_libdir}/xtables/libxt_TCPOPTSTRIP.so
%attr(755,root,root) %{_libdir}/xtables/libxt_tcp.so
%attr(755,root,root) %{_libdir}/xtables/libxt_time.so
%attr(755,root,root) %{_libdir}/xtables/libxt_tos.so
%attr(755,root,root) %{_libdir}/xtables/libxt_TOS.so
%attr(755,root,root) %{_libdir}/xtables/libxt_TPROXY.so
%attr(755,root,root) %{_libdir}/xtables/libxt_TRACE.so
%attr(755,root,root) %{_libdir}/xtables/libxt_u32.so
%attr(755,root,root) %{_libdir}/xtables/libxt_udp.so
%else
%attr(755,root,root) %{_libdir}/xtables/*.so
%endif
%{_mandir}/man8/*

%files devel
%defattr(644,root,root,755)
%{?with_doc:%doc iptables-howtos/netfilter-hacking-HOWTO*}
%{_libdir}/lib*.a
%{_includedir}/*.h
%dir %{_includedir}/libiptc
%{_includedir}/libiptc/*.h
%{_mandir}/man3/*

%files init
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/iptables
%attr(754,root,root) /etc/rc.d/init.d/ip6tables
