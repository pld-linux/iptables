#
# TODO:
# - update BR to real required llh version
# - check if kernel-headers are still required to properly build iptabels for dist kernel
# - fix makefile (-D_UNKNOWN_KERNEL_POINTER_SIZE issue)
# - owner needs rewrite to xt
#
# Conditional build:
%bcond_without	doc		# without documentation (HOWTOS) which needed TeX
%bcond_without	dist_kernel	# without distribution kernel
%bcond_with	vserver		# build xt_owner module for non-dist kernel with vserver support
%bcond_with	batch		# build iptables-batch
%bcond_with	static		# build static libraries, no dynamic modules (all linked into binaries)
%bcond_with	ipt_IPV4OPTSSTRIP # enable ipt_IPV4OPTSSTRIP for non-dist kernel
%bcond_with	ipt_rpc		# enable ipt_rpc for non-dist kernel
%bcond_with	xt_layer7	# enable xt_layer7 for non-dist kernel
%bcond_with	usekernelsrc	# include kernel headers from %{_kernelsrcdir}

%if %{with dist_kernel}
%define	with_ipt_IPV4OPTSSTRIP	1
%define	with_ipt_rpc		1
%define	with_xt_layer7		1
%define	with_vserver		1
%define	with_usekernelsrc	1
%endif

%define		name6			ip6tables
Summary:	Extensible packet filtering system && extensible NAT system
Summary(pl.UTF-8):	System filtrowania pakietów oraz system translacji adresów (NAT)
Summary(pt_BR.UTF-8):	Ferramenta para controlar a filtragem de pacotes no kernel-2.6.x
Summary(ru.UTF-8):	Утилиты для управления пакетными фильтрами ядра Linux
Summary(uk.UTF-8):	Утиліти для керування пакетними фільтрами ядра Linux
Summary(zh_CN.UTF-8):	Linux内核包过滤管理工具
Name:		iptables
Version:	1.4.11
Release:	1
License:	GPL v2
Group:		Networking/Admin
Source0:	ftp://ftp.netfilter.org/pub/iptables/%{name}-%{version}.tar.bz2
# Source0-md5:	4d77c912d17364e2515fda27d398e15e
Source1:	cvs://cvs.samba.org/netfilter/%{name}-howtos.tar.bz2
# Source1-md5:	2ed2b452daefe70ededd75dc0061fd07
Source2:	%{name}.init
Source3:	%{name6}.init
# --- GENERAL CHANGES (patches<10):
Patch0:		%{name}-man.patch
# additional utils; off by default
Patch1:		%{name}-batch.patch
# --- ADDITIONAL/CHANGED EXTENSIONS:
# just ipt_IPV4OPTSSTRIP now
Patch10:	%{name}-20070806.patch
# xt_layer7; almost based on iptables-1.4-for-kernel-2.6.20forward-layer7-2.18.patch
# http://downloads.sourceforge.net/l7-filter/netfilter-layer7-v2.18.tar.gz
Patch11:	%{name}-layer7.patch
# ipt_rpc
Patch12:	%{name}-old-1.3.7.patch
# xt_IMQ; based on http://www.linuximq.net/patchs/iptables-1.4.6-imq.diff
Patch13:	%{name}-imq.patch
# enhances ipt_owner/ip6t_owner; http://people.linux-vserver.org/~dhozac/p/m/iptables-1.3.5-owner-xid.patch (currently disabled, needs update for xt_owner)
Patch14:	%{name}-1.3.5-owner-xid.patch
# adjusts xt_owner for vserver-enabled kernel
Patch15:	%{name}-owner-struct-size-vs.patch
# ipt_stealth; currently disabled (broken, see below)
Patch16:	%{name}-stealth.patch
URL:		http://www.netfilter.org/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	groff
BuildRequires:	libnfnetlink-devel >= 1.0
BuildRequires:	libtool
BuildRequires:	pkgconfig >= 1:0.9.0
%if %{with doc}
BuildRequires:	sed >= 4.0
BuildRequires:	sgml-tools
BuildRequires:	sgmls
BuildRequires:	tetex-dvips
BuildRequires:	tetex-format-latex
BuildRequires:	tetex-latex
BuildRequires:	tetex-tex-babel
# if texlive: BuildRequires: texlive-fonts-cmsuper
%endif
%if %{with dist_kernel}
BuildRequires:	kernel%{_alt_kernel}-headers(netfilter)
%endif
BuildRequires:	linux-libc-headers >= 7:2.6.22.1
Requires:	%{name}-libs = %{version}-%{release}
Requires:	libnfnetlink >= 1.0
Provides:	firewall-userspace-tool
Obsoletes:	ipchains
Obsoletes:	iptables-ipp2p
Obsoletes:	iptables24-compat
Obsoletes:	netfilter
Conflicts:	xtables-addons < 1.14
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

%package libs
Summary:	iptables libraries
Summary(pl.UTF-8):	Biblioteki iptables
Group:		Libraries
Conflicts:	iptables < 1.4.3-1

%description libs
iptables libraries.

%description libs -l pl.UTF-8
Biblioteki iptables.

%package devel
Summary:	Libraries and headers for developing iptables extensions
Summary(pl.UTF-8):	Biblioteki i nagłówki do tworzenia rozszerzeń iptables
Group:		Development/Libraries
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
Obsoletes:	iptables24-devel

%description devel
Libraries and headers for developing iptables extensions.

%description devel -l pl.UTF-8
Biblioteki i pliki nagłówkowe niezbędne do tworzenia rozszerzeń dla
iptables.

%package static
Summary:	Static iptables libraries
Summary(pl.UTF-8):	Biblioteki statyczne iptables
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static iptables libraries.

%description static -l pl.UTF-8
Biblioteki statyczne iptables.

%package init
Summary:	Iptables init (RedHat style)
Summary(pl.UTF-8):	Iptables init (w stylu RedHata)
Group:		Networking/Admin
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}
Requires:	rc-scripts >= 0.4.3.0
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
%if %{with batch}
%patch1 -p1
%endif
%{?with_ipt_IPV4OPTSSTRIP:%patch10 -p1}
%{?with_xt_layer7:%patch11 -p1}
%{?with_ipt_rpc:%patch12 -p1}
%patch13 -p0
%if %{with vserver}
#patch14 -p1
%patch15 -p1
%endif
# builds but init() api is broken, see warnings
#patch16 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	CFLAGS="%{rpmcflags} %{rpmcppflags} -D%{!?debug:N}DEBUG" \
	%{?with_usekernelsrc:--with-kernel=%{_kernelsrcdir}} \
	--enable-libipq \
	%{?with_static:--enable-static}

%{__make} all \
	V=1

%if %{with doc}
%{__make} -j1 -C iptables-howtos
sed -i 's:$(HTML_HOWTOS)::g; s:$(PSUS_HOWTOS)::g' iptables-howtos/Makefile
%endif

# Make a library, needed for OpenVCP
# unpackaged; is it still valid? --q
ar rcs libiptables.a *iptables*.o
ar rcs libip6tables.a *ip6tables*.o

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,%{_includedir},%{_libdir},%{_mandir}/man3}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	BINDIR=%{_sbindir} \
	MANDIR=%{_mandir} \
	LIBDIR=%{_libdir}

install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name6}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

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
%attr(755,root,root) %{_sbindir}/iptables-restore
%attr(755,root,root) %{_sbindir}/iptables-save
%attr(755,root,root) %{_sbindir}/ip6tables
%attr(755,root,root) %{_sbindir}/ip6tables-restore
%attr(755,root,root) %{_sbindir}/ip6tables-save
%if %{with batch}
%attr(755,root,root) %{_sbindir}/iptables-batch
%attr(755,root,root) %{_sbindir}/ip6tables-batch
%endif
%attr(755,root,root) %{_sbindir}/nfnl_osf
%attr(755,root,root) %{_sbindir}/xtables-multi
%{_datadir}/xtables
%dir %{_libdir}/xtables
%attr(755,root,root) %{_libdir}/xtables/libip6t_HL.so
%attr(755,root,root) %{_libdir}/xtables/libip6t_LOG.so
%attr(755,root,root) %{_libdir}/xtables/libip6t_REJECT.so
%attr(755,root,root) %{_libdir}/xtables/libip6t_ah.so
%attr(755,root,root) %{_libdir}/xtables/libip6t_dst.so
%attr(755,root,root) %{_libdir}/xtables/libip6t_eui64.so
%attr(755,root,root) %{_libdir}/xtables/libip6t_frag.so
%attr(755,root,root) %{_libdir}/xtables/libip6t_hbh.so
%attr(755,root,root) %{_libdir}/xtables/libip6t_hl.so
%attr(755,root,root) %{_libdir}/xtables/libip6t_icmp6.so
%attr(755,root,root) %{_libdir}/xtables/libip6t_ipv6header.so
%attr(755,root,root) %{_libdir}/xtables/libip6t_mh.so
%attr(755,root,root) %{_libdir}/xtables/libip6t_rt.so
%attr(755,root,root) %{_libdir}/xtables/libipt_CLUSTERIP.so
%attr(755,root,root) %{_libdir}/xtables/libipt_DNAT.so
%attr(755,root,root) %{_libdir}/xtables/libipt_ECN.so
%attr(755,root,root) %{_libdir}/xtables/libipt_LOG.so
%attr(755,root,root) %{_libdir}/xtables/libipt_MASQUERADE.so
%attr(755,root,root) %{_libdir}/xtables/libipt_MIRROR.so
%attr(755,root,root) %{_libdir}/xtables/libipt_NETMAP.so
%attr(755,root,root) %{_libdir}/xtables/libipt_REDIRECT.so
%attr(755,root,root) %{_libdir}/xtables/libipt_REJECT.so
%attr(755,root,root) %{_libdir}/xtables/libipt_SAME.so
%attr(755,root,root) %{_libdir}/xtables/libipt_SNAT.so
%attr(755,root,root) %{_libdir}/xtables/libipt_TTL.so
%attr(755,root,root) %{_libdir}/xtables/libipt_ULOG.so
%attr(755,root,root) %{_libdir}/xtables/libipt_addrtype.so
%attr(755,root,root) %{_libdir}/xtables/libipt_ah.so
%attr(755,root,root) %{_libdir}/xtables/libipt_ecn.so
%attr(755,root,root) %{_libdir}/xtables/libipt_icmp.so
%attr(755,root,root) %{_libdir}/xtables/libipt_realm.so
# disabled, see above
#%attr(755,root,root) %{_libdir}/xtables/libipt_stealth.so
%attr(755,root,root) %{_libdir}/xtables/libipt_ttl.so
%attr(755,root,root) %{_libdir}/xtables/libipt_unclean.so
%attr(755,root,root) %{_libdir}/xtables/libxt_AUDIT.so
%attr(755,root,root) %{_libdir}/xtables/libxt_CHECKSUM.so
%attr(755,root,root) %{_libdir}/xtables/libxt_CLASSIFY.so
%attr(755,root,root) %{_libdir}/xtables/libxt_CONNMARK.so
%attr(755,root,root) %{_libdir}/xtables/libxt_CONNSECMARK.so
%attr(755,root,root) %{_libdir}/xtables/libxt_CT.so
%attr(755,root,root) %{_libdir}/xtables/libxt_DSCP.so
%attr(755,root,root) %{_libdir}/xtables/libxt_IDLETIMER.so
%attr(755,root,root) %{_libdir}/xtables/libxt_IMQ.so
%attr(755,root,root) %{_libdir}/xtables/libxt_LED.so
%attr(755,root,root) %{_libdir}/xtables/libxt_MARK.so
%attr(755,root,root) %{_libdir}/xtables/libxt_NFLOG.so
%attr(755,root,root) %{_libdir}/xtables/libxt_NFQUEUE.so
%attr(755,root,root) %{_libdir}/xtables/libxt_NOTRACK.so
%attr(755,root,root) %{_libdir}/xtables/libxt_RATEEST.so
%attr(755,root,root) %{_libdir}/xtables/libxt_SECMARK.so
%attr(755,root,root) %{_libdir}/xtables/libxt_SET.so
%attr(755,root,root) %{_libdir}/xtables/libxt_TCPMSS.so
%attr(755,root,root) %{_libdir}/xtables/libxt_TCPOPTSTRIP.so
%attr(755,root,root) %{_libdir}/xtables/libxt_TEE.so
%attr(755,root,root) %{_libdir}/xtables/libxt_TOS.so
%attr(755,root,root) %{_libdir}/xtables/libxt_TPROXY.so
%attr(755,root,root) %{_libdir}/xtables/libxt_TRACE.so
%attr(755,root,root) %{_libdir}/xtables/libxt_cluster.so
%attr(755,root,root) %{_libdir}/xtables/libxt_comment.so
%attr(755,root,root) %{_libdir}/xtables/libxt_connbytes.so
%attr(755,root,root) %{_libdir}/xtables/libxt_connlimit.so
%attr(755,root,root) %{_libdir}/xtables/libxt_connmark.so
%attr(755,root,root) %{_libdir}/xtables/libxt_conntrack.so
%attr(755,root,root) %{_libdir}/xtables/libxt_cpu.so
%attr(755,root,root) %{_libdir}/xtables/libxt_dccp.so
%attr(755,root,root) %{_libdir}/xtables/libxt_devgroup.so
%attr(755,root,root) %{_libdir}/xtables/libxt_dscp.so
%attr(755,root,root) %{_libdir}/xtables/libxt_esp.so
%attr(755,root,root) %{_libdir}/xtables/libxt_hashlimit.so
%attr(755,root,root) %{_libdir}/xtables/libxt_helper.so
%attr(755,root,root) %{_libdir}/xtables/libxt_iprange.so
%attr(755,root,root) %{_libdir}/xtables/libxt_ipvs.so
%attr(755,root,root) %{_libdir}/xtables/libxt_length.so
%attr(755,root,root) %{_libdir}/xtables/libxt_limit.so
%attr(755,root,root) %{_libdir}/xtables/libxt_mac.so
%attr(755,root,root) %{_libdir}/xtables/libxt_mark.so
%attr(755,root,root) %{_libdir}/xtables/libxt_multiport.so
%attr(755,root,root) %{_libdir}/xtables/libxt_osf.so
%attr(755,root,root) %{_libdir}/xtables/libxt_owner.so
%attr(755,root,root) %{_libdir}/xtables/libxt_physdev.so
%attr(755,root,root) %{_libdir}/xtables/libxt_pkttype.so
%attr(755,root,root) %{_libdir}/xtables/libxt_policy.so
%attr(755,root,root) %{_libdir}/xtables/libxt_quota.so
%attr(755,root,root) %{_libdir}/xtables/libxt_rateest.so
%attr(755,root,root) %{_libdir}/xtables/libxt_recent.so
%attr(755,root,root) %{_libdir}/xtables/libxt_sctp.so
%attr(755,root,root) %{_libdir}/xtables/libxt_set.so
%attr(755,root,root) %{_libdir}/xtables/libxt_socket.so
%attr(755,root,root) %{_libdir}/xtables/libxt_standard.so
%attr(755,root,root) %{_libdir}/xtables/libxt_state.so
%attr(755,root,root) %{_libdir}/xtables/libxt_statistic.so
%attr(755,root,root) %{_libdir}/xtables/libxt_string.so
%attr(755,root,root) %{_libdir}/xtables/libxt_tcp.so
%attr(755,root,root) %{_libdir}/xtables/libxt_tcpmss.so
%attr(755,root,root) %{_libdir}/xtables/libxt_time.so
%attr(755,root,root) %{_libdir}/xtables/libxt_tos.so
%attr(755,root,root) %{_libdir}/xtables/libxt_u32.so
%attr(755,root,root) %{_libdir}/xtables/libxt_udp.so
%{?with_ipt_IPV4OPTSSTRIP:%attr(755,root,root) %{_libdir}/xtables/libipt_IPV4OPTSSTRIP.so}
%{?with_ipt_rpc:%attr(755,root,root) %{_libdir}/xtables/libipt_rpc.so}
%{?with_xt_layer7:%attr(755,root,root) %{_libdir}/xtables/libxt_layer7.so}
%{_mandir}/man8/ip6tables.8*
%{_mandir}/man8/ip6tables-restore.8*
%{_mandir}/man8/ip6tables-save.8*
%{_mandir}/man8/iptables.8*
%{_mandir}/man8/iptables-restore.8*
%{_mandir}/man8/iptables-save.8*
%{_mandir}/man8/iptables-xml.8*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libip4tc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libip4tc.so.0
%attr(755,root,root) %{_libdir}/libip6tc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libip6tc.so.0
%attr(755,root,root) %{_libdir}/libipq.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libipq.so.0
%attr(755,root,root) %{_libdir}/libiptc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libiptc.so.0
%attr(755,root,root) %{_libdir}/libxtables.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libxtables.so.6

%files devel
%defattr(644,root,root,755)
%{?with_doc:%doc iptables-howtos/netfilter-hacking-HOWTO*}
%attr(755,root,root) %{_libdir}/libip4tc.so
%attr(755,root,root) %{_libdir}/libip6tc.so
%attr(755,root,root) %{_libdir}/libipq.so
%attr(755,root,root) %{_libdir}/libiptc.so
%attr(755,root,root) %{_libdir}/libxtables.so
%{_libdir}/libip4tc.la
%{_libdir}/libip6tc.la
%{_libdir}/libipq.la
%{_libdir}/libiptc.la
%{_libdir}/libxtables.la
%{_includedir}/libipq.h
%{_includedir}/xtables.h
%{_includedir}/libiptc
%{_pkgconfigdir}/libiptc.pc
%{_pkgconfigdir}/xtables.pc
%{_mandir}/man3/ipq_*.3*
%{_mandir}/man3/libipq.3*

%if %{with static}
%files static
%defattr(644,root,root,755)
%{_libdir}/libip4tc.a
%{_libdir}/libip6tc.a
%{_libdir}/libipq.a
%{_libdir}/libiptc.a
%{_libdir}/libxtables.a
%endif

%files init
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/iptables
%attr(754,root,root) /etc/rc.d/init.d/ip6tables
