#
# TODO:
# - recheck ebtables functionality:
#   - is it still valid: "The original old ebtables is still needed e.g. for libvirt's nwfilter"?
#   - is ebtables init script/service usable with iptables ebtables implementation now?
#     if so, then move them here from legacy ebtables.spec
# - update BR to real required llh version
#
# Conditional build:
%bcond_without	doc		# HOWTOS documentation (which requires TeX)
%bcond_without	dist_kernel	# distribution (patched) kernel enhancements (alias for with: ipt_IPV4OPTSSTRIP ipt_rpc xt_layer7)
%bcond_without	nftables	# nftables compatibility
%bcond_without	pcap		# pcap-dependend utils (nfbpf_compile, nfsynproxy)
%bcond_with	vserver		# xt_owner module with vserver support
%bcond_with	batch		# iptables-batch utils
%bcond_with	static		# static libraries, no dynamic modules (all linked into binaries)
%bcond_with	ipt_IPV4OPTSSTRIP # ipt_IPV4OPTSSTRIP module (requires kernel patch to work)
%bcond_with	ipt_rpc		# ipt_rpc module (requires kernel patch to work)
%bcond_with	xt_layer7	# xt_layer7 module (requires kernel patch to work)
%bcond_with	usekernelsrc	# include kernel headers from %{_kernelsrcdir}
%bcond_with	default_nft	# use nftables backend by default

%if %{with dist_kernel}
%define	with_ipt_IPV4OPTSSTRIP	1
%define	with_ipt_rpc		1
%define	with_xt_layer7		1
%endif

%define		orgname	iptables

Summary:	Extensible packet filtering system && extensible NAT system
Summary(pl.UTF-8):	System filtrowania pakietów oraz system translacji adresów (NAT)
Summary(pt_BR.UTF-8):	Ferramenta para controlar a filtragem de pacotes no kernel-2.6.x
Summary(ru.UTF-8):	Утилиты для управления пакетными фильтрами ядра Linux
Summary(uk.UTF-8):	Утиліти для керування пакетними фільтрами ядра Linux
Summary(zh_CN.UTF-8):	Linux内核包过滤管理工具
Name:		iptables%{?with_vserver:-vserver}
Version:	1.8.13
Release:	1
License:	GPL v2
Group:		Networking/Admin
Source0:	https://netfilter.org/projects/iptables/files/%{orgname}-%{version}.tar.xz
# Source0-md5:	81b5edf500e2672bfbc744581ff7dc3e
Source1:	cvs://cvs.samba.org/netfilter/%{orgname}-howtos.tar.bz2
# Source1-md5:	2ed2b452daefe70ededd75dc0061fd07
Source2:	iptables.init
Source3:	ip6tables.init
Source6:	iptables-config
Source7:	ip6tables-config
Source8:	iptables.service
Source9:	ip6tables.service
# these are not compatible with this package! there are no ebtables-save and ebtables-restore here
Source10:	ebtables.init
Source11:	ebtables-config
Source12:	ebtables.service
# --- GENERAL CHANGES (patches<10):
Patch0:		%{orgname}-man.patch
# additional utils; off by default
Patch1:		%{orgname}-batch.patch
Patch2:		no-libiptc.patch
Patch3:		%{orgname}-aligned_u64.patch
# --- ADDITIONAL/CHANGED EXTENSIONS:
# just ipt_IPV4OPTSSTRIP now
Patch10:	%{orgname}-20070806.patch
# xt_layer7; almost based on iptables-1.4-for-kernel-2.6.20forward-layer7-2.18.patch
# http://downloads.sourceforge.net/l7-filter/netfilter-layer7-v2.18.tar.gz
Patch11:	%{orgname}-layer7.patch
# ipt_rpc
Patch12:	%{orgname}-old-1.3.7.patch
# xt_IMQ; http://linuximq.net/patchs/iptables-1.4.12-IMQ-test4.diff
Patch13:	%{orgname}-imq.patch
# enhances ipt_owner/ip6t_owner; http://people.linux-vserver.org/~dhozac/p/m/iptables-1.3.5-owner-xid.patch (currently disabled, needs update for xt_owner)
Patch14:	%{orgname}-owner-xid.patch
# adjusts xt_owner for vserver-enabled kernel
Patch15:	%{orgname}-owner-struct-size-vs.patch
Patch16:	%{orgname}-rpc.patch
Patch18:	%{orgname}-default_nft.patch
URL:		https://netfilter.org/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	groff
%{?with_nftables:BuildRequires:	libmnl-devel >= 1.0}
BuildRequires:	libnetfilter_conntrack-devel >= 1.0.6
BuildRequires:	libnfnetlink-devel >= 1.0
%{?with_nftables:BuildRequires:	libnftnl-devel >= 1.2.6}
%{?with_pcap:BuildRequires:	libpcap-devel}
BuildRequires:	libtirpc-devel >= 0.2.0
BuildRequires:	libtool >= 2:2
BuildRequires:	linux-libc-headers >= 7:2.6.22.1
BuildRequires:	pkgconfig >= 1:0.9.0
BuildRequires:	rpmbuild(macros) >= 1.647
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
%if %{with doc}
BuildRequires:	sed >= 4.0
BuildRequires:	sgml-tools
BuildRequires:	sgmls
BuildRequires:	tetex-dvips
BuildRequires:	tetex-format-latex
BuildRequires:	tetex-latex
BuildRequires:	tetex-tex-babel
BuildRequires:	texlive-fonts-cmsuper
BuildRequires:	texlive-fonts-jknappen
%endif
Requires:	%{orgname}-libs = %{version}-%{release}
%{?with_nftables:Requires:	libmnl >= 1.0}
Requires:	libnetfilter_conntrack >= 1.0.6
Requires:	libnfnetlink >= 1.0
%{?with_nftables:Requires:	libnftnl >= 1.2.6}
Provides:	firewall-userspace-tool
%{?with_vserver:Provides:	iptables = %{version}-%{release}}
Conflicts:	arptables < 0.0.5
Obsoletes:	ipchains < 1.4
Obsoletes:	iptables24-compat < 1.3
Obsoletes:	netfilter
Conflicts:	xtables-addons < 1.25
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
Requires:	%{orgname}-libs = %{epoch}:%{version}-%{release}
Obsoletes:	iptables24-devel < 1.3

%description devel
Libraries and headers for developing iptables extensions.

%description devel -l pl.UTF-8
Biblioteki i pliki nagłówkowe niezbędne do tworzenia rozszerzeń dla
iptables.

%package static
Summary:	Static iptables libraries
Summary(pl.UTF-8):	Biblioteki statyczne iptables
Group:		Development/Libraries
Requires:	%{orgname}-devel = %{epoch}:%{version}-%{release}

%description static
Static iptables libraries.

%description static -l pl.UTF-8
Biblioteki statyczne iptables.

%package init
Summary:	Iptables init (RedHat style)
Summary(pl.UTF-8):	Iptables init (w stylu RedHata)
Group:		Networking/Admin
Requires(post,preun):	/sbin/chkconfig
Requires(post,preun,postun):	systemd-units >= 38
Requires:	%{name} = %{version}-%{release}
Requires:	rc-scripts >= 0.4.3.0
Requires:	systemd-units >= 38
Obsoletes:	firewall-init < 3
Obsoletes:	firewall-init-ipchains < 2.2
Obsoletes:	iptables24-init < 1.3
%{?with_vserver:Provides:	iptables-init = %{version}-%{release}}

%description init
Iptables-init is meant to provide an alternate way than firewall-init
to start and stop packet filtering through iptables(8).

%description init -l pl.UTF-8
Iptables-init ma na celu udostępnienie alternatywnego w stosunku do
firewall-init sposobu włączania i wyłączania filtrów IP jądra poprzez
iptables(8).

%package ebtables
Summary:	Ethernet Bridge Tables - xtables compatibility wrapper
Summary(pl.UTF-8):	Ethernet Bridge Tables – nakładka kompatybilności na xtables
Group:		Networking/Admin
Requires(post,preun):	/sbin/chkconfig
Requires(post,preun,postun):	systemd-units >= 38
Requires:	%{name} = %{version}-%{release}
Requires:	rc-scripts >= 0.4.3.0
Requires:	systemd-units >= 38
# do not 'provide' something this is not really compatible with
#Provides:	ebtables
Conflicts:	ebtables < 2.0.11
%{?with_vserver:Provides:	iptables-ebtables = %{version}-%{release}}

%description ebtables
ebtables is a tool for managing Linux 2.5.x (and above) Link Layer
firewalling subsystem.

This package contains a compatibility wrapper over xtables providing
some functionality of the original ebtables tool.

Note: this is not really a fully-compatible drop-in replacement!

%description ebtables -l pl.UTF-8
ebtables to narzędzie do zarządzania podsystemem firewalla warstwy
połączenia (Link Layer) Linuksa 2.5.x (i nowszych).

Ten pakiet zawiera warstwę zgodności dla xtables zapewniającą część
funkcjonalności oryginalnego narzędzia ebtables.

Uwaga: nie jest to w pełni zgodny zamiennik!

%prep
%setup -q -n iptables-%{version} -a1
%patch -P0 -p1
%if %{with batch}
%patch -P1 -p1
%endif
%patch -P2 -p1
%patch -P3 -p1

%{?with_ipt_IPV4OPTSSTRIP:%patch -P10 -p1}
%{?with_xt_layer7:%patch -P11 -p1}
%{?with_ipt_rpc:%patch -P12 -p1}
%patch -P13 -p1
%if %{with vserver}
%patch -P14 -p1
%patch -P15 -p1
%endif
%patch -P16 -p1
%if %{with nftables} && %{with default_nft}
%patch -P18 -p1
%endif

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	CFLAGS="%{rpmcflags} %{rpmcppflags} -D%{!?debug:N}DEBUG" \
	%{?with_usekernelsrc:--with-kernel=%{_kernelsrcdir}} \
	%{?with_pcap:--enable-bpf-compiler} \
	--enable-libipq \
	%{?with_pcap:--enable-nfsynproxy} \
	%{!?with_nftables:--disable-nftables} \
	%{?with_static:--enable-static}

%{__make} -j1 all \
	V=1

%if %{with doc}
%{__make} -j1 -C iptables-howtos
sed -i 's:$(HTML_HOWTOS)::g; s:$(PSUS_HOWTOS)::g' iptables-howtos/Makefile
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig} \
	$RPM_BUILD_ROOT{%{_includedir},%{_libdir},%{_mandir}/man3} \
	$RPM_BUILD_ROOT%{systemdunitdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	BINDIR=%{_sbindir} \
	MANDIR=%{_mandir} \
	LIBDIR=%{_libdir}

# use ld script for -liptc backward compat (see no-libiptc.patch for source)
%{__sed} \
%ifarch %{x8664} alpha aarch64 hppa64 mips64 ppc64 s390x sparc64
	-e 's,@BITS@,64,' \
%else
	-e 's,@BITS@,32,' \
%endif
	-e 's,@LIBDIR@,%{_libdir},g' \
	-e "s,@ARCH@,$(echo "%{_build_arch}" | tr _ -)," libiptc/libiptc.ld.in >$RPM_BUILD_ROOT%{_libdir}/libiptc.so

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib{ip4tc,ip6tc,ipq,xtables}.la

install -p %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/iptables
install -p %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/ip6tables

install -p %{SOURCE6} $RPM_BUILD_ROOT/etc/sysconfig/iptables-config
install -p %{SOURCE7} $RPM_BUILD_ROOT/etc/sysconfig/ip6tables-config

install -p %{SOURCE8} $RPM_BUILD_ROOT%{systemdunitdir}/iptables.service
install -p %{SOURCE9} $RPM_BUILD_ROOT%{systemdunitdir}/ip6tables.service

# these won't work as they are now
#install -p %{SOURCE10} $RPM_BUILD_ROOT/etc/rc.d/init.d/ebtables
#install -p %{SOURCE11} $RPM_BUILD_ROOT/etc/sysconfig/ebtables-config
#install -p %{SOURCE12} $RPM_BUILD_ROOT%{systemdunitdir}/ebtables.service

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post init
/sbin/chkconfig --add iptables
/sbin/chkconfig --add ip6tables
%systemd_post iptables.service ip6tables.service

%preun init
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del iptables
	/sbin/chkconfig --del ip6tables
fi
%systemd_preun iptables.service ip6tables.service

%postun init
%systemd_reload

%triggerpostun init -- iptables-init < 1.4.13-2
%systemd_trigger iptables.service ip6tables.service

%files
%defattr(644,root,root,755)
%if %{with doc}
%doc iptables-howtos/{NAT,networking-concepts,packet-filtering}-HOWTO*
%endif
%attr(755,root,root) %{_sbindir}/iptables-apply
%if %{with batch}
%attr(755,root,root) %{_sbindir}/iptables-batch
%attr(755,root,root) %{_sbindir}/ip6tables-batch
%endif
%attr(755,root,root) %{_sbindir}/nfnl_osf
%if %{with pcap}
%attr(755,root,root) %{_sbindir}/nfbpf_compile
%attr(755,root,root) %{_sbindir}/nfsynproxy
%endif
%attr(755,root,root) %{_sbindir}/xtables-legacy-multi
# symlink to iptables-apply
%{_sbindir}/ip6tables-apply
# symlinks to xtables-legacy-multi
%{_bindir}/iptables-xml
%{_sbindir}/ip6tables
%{_sbindir}/ip6tables-legacy
%{_sbindir}/ip6tables-legacy-restore
%{_sbindir}/ip6tables-legacy-save
%{_sbindir}/ip6tables-restore
%{_sbindir}/ip6tables-save
%{_sbindir}/iptables
%{_sbindir}/iptables-legacy
%{_sbindir}/iptables-legacy-restore
%{_sbindir}/iptables-legacy-save
%{_sbindir}/iptables-restore
%{_sbindir}/iptables-save
%{_datadir}/xtables
%dir %{_libdir}/xtables
%{_libdir}/xtables/libip6t_DNPT.so
%{_libdir}/xtables/libip6t_HL.so
%{_libdir}/xtables/libip6t_NETMAP.so
%{_libdir}/xtables/libip6t_REJECT.so
%{_libdir}/xtables/libip6t_SNPT.so
%{_libdir}/xtables/libip6t_ah.so
%{_libdir}/xtables/libip6t_dst.so
%{_libdir}/xtables/libip6t_eui64.so
%{_libdir}/xtables/libip6t_frag.so
%{_libdir}/xtables/libip6t_hbh.so
%{_libdir}/xtables/libip6t_hl.so
%{_libdir}/xtables/libip6t_icmp6.so
%{_libdir}/xtables/libip6t_ipv6header.so
%{_libdir}/xtables/libip6t_mh.so
%{_libdir}/xtables/libip6t_rt.so
%{_libdir}/xtables/libip6t_srh.so
%{_libdir}/xtables/libipt_CLUSTERIP.so
%{_libdir}/xtables/libipt_ECN.so
%if %{with ipt_IPV4OPTSSTRIP}
%{_libdir}/xtables/libipt_IPV4OPTSSTRIP.so
%endif
%{_libdir}/xtables/libipt_NETMAP.so
%{_libdir}/xtables/libipt_REJECT.so
%{_libdir}/xtables/libipt_TTL.so
%{_libdir}/xtables/libipt_ULOG.so
%{_libdir}/xtables/libipt_ah.so
%{_libdir}/xtables/libipt_icmp.so
%{_libdir}/xtables/libipt_realm.so
%if %{with ipt_rpc}
%{_libdir}/xtables/libipt_rpc.so
%endif
%{_libdir}/xtables/libipt_ttl.so
%{_libdir}/xtables/libxt_AUDIT.so
%{_libdir}/xtables/libxt_CHECKSUM.so
%{_libdir}/xtables/libxt_CLASSIFY.so
%{_libdir}/xtables/libxt_CONNMARK.so
%{_libdir}/xtables/libxt_CONNSECMARK.so
%{_libdir}/xtables/libxt_CT.so
%{_libdir}/xtables/libxt_DNAT.so
%{_libdir}/xtables/libxt_DSCP.so
%{_libdir}/xtables/libxt_HMARK.so
%{_libdir}/xtables/libxt_IDLETIMER.so
%{_libdir}/xtables/libxt_IMQ.so
%{_libdir}/xtables/libxt_LED.so
%{_libdir}/xtables/libxt_LOG.so
%{_libdir}/xtables/libxt_MARK.so
%{_libdir}/xtables/libxt_MASQUERADE.so
%{_libdir}/xtables/libxt_NAT.so
%{_libdir}/xtables/libxt_NFLOG.so
%{_libdir}/xtables/libxt_NFQUEUE.so
%{_libdir}/xtables/libxt_NOTRACK.so
%{_libdir}/xtables/libxt_RATEEST.so
%{_libdir}/xtables/libxt_REDIRECT.so
%{_libdir}/xtables/libxt_SECMARK.so
%{_libdir}/xtables/libxt_SET.so
%{_libdir}/xtables/libxt_SNAT.so
%{_libdir}/xtables/libxt_SYNPROXY.so
%{_libdir}/xtables/libxt_TCPMSS.so
%{_libdir}/xtables/libxt_TCPOPTSTRIP.so
%{_libdir}/xtables/libxt_TEE.so
%{_libdir}/xtables/libxt_TOS.so
%{_libdir}/xtables/libxt_TPROXY.so
%{_libdir}/xtables/libxt_TRACE.so
%{_libdir}/xtables/libxt_addrtype.so
%{_libdir}/xtables/libxt_bpf.so
%{_libdir}/xtables/libxt_cgroup.so
%{_libdir}/xtables/libxt_cluster.so
%{_libdir}/xtables/libxt_comment.so
%{_libdir}/xtables/libxt_connbytes.so
%{_libdir}/xtables/libxt_connlabel.so
%{_libdir}/xtables/libxt_connlimit.so
%{_libdir}/xtables/libxt_connmark.so
%{_libdir}/xtables/libxt_conntrack.so
%{_libdir}/xtables/libxt_cpu.so
%{_libdir}/xtables/libxt_dccp.so
%{_libdir}/xtables/libxt_devgroup.so
%{_libdir}/xtables/libxt_dscp.so
%{_libdir}/xtables/libxt_ecn.so
%{_libdir}/xtables/libxt_esp.so
%{_libdir}/xtables/libxt_hashlimit.so
%{_libdir}/xtables/libxt_helper.so
%{_libdir}/xtables/libxt_ipcomp.so
%{_libdir}/xtables/libxt_iprange.so
%{_libdir}/xtables/libxt_ipvs.so
%if %{with xt_layer7}
%{_libdir}/xtables/libxt_layer7.so
%endif
%{_libdir}/xtables/libxt_length.so
%{_libdir}/xtables/libxt_limit.so
%{_libdir}/xtables/libxt_mac.so
%{_libdir}/xtables/libxt_mark.so
%{_libdir}/xtables/libxt_multiport.so
%{_libdir}/xtables/libxt_nfacct.so
%{_libdir}/xtables/libxt_osf.so
%{_libdir}/xtables/libxt_owner.so
%{_libdir}/xtables/libxt_physdev.so
%{_libdir}/xtables/libxt_pkttype.so
%{_libdir}/xtables/libxt_policy.so
%{_libdir}/xtables/libxt_quota.so
%{_libdir}/xtables/libxt_rateest.so
%{_libdir}/xtables/libxt_recent.so
%{_libdir}/xtables/libxt_rpfilter.so
%{_libdir}/xtables/libxt_sctp.so
%{_libdir}/xtables/libxt_set.so
%{_libdir}/xtables/libxt_socket.so
%{_libdir}/xtables/libxt_standard.so
%{_libdir}/xtables/libxt_state.so
%{_libdir}/xtables/libxt_statistic.so
%{_libdir}/xtables/libxt_string.so
%{_libdir}/xtables/libxt_tcp.so
%{_libdir}/xtables/libxt_tcpmss.so
%{_libdir}/xtables/libxt_time.so
%{_libdir}/xtables/libxt_tos.so
%{_libdir}/xtables/libxt_u32.so
%{_libdir}/xtables/libxt_udp.so
%{_mandir}/man1/iptables-xml.1*
%{_mandir}/man8/ip6tables.8*
%{_mandir}/man8/ip6tables-apply.8*
%{_mandir}/man8/ip6tables-restore.8*
%{_mandir}/man8/ip6tables-save.8*
%{_mandir}/man8/iptables.8*
%{_mandir}/man8/iptables-apply.8*
%{_mandir}/man8/iptables-extensions.8*
%{_mandir}/man8/iptables-restore.8*
%{_mandir}/man8/iptables-save.8*
%{_mandir}/man8/nfnl_osf.8*
%if %{with pcap}
%{_mandir}/man8/nfbpf_compile.8*
%endif
%if %{with nftables}
%attr(755,root,root) %{_sbindir}/xtables-nft-multi
# symlinks to xtables-nft-multi
%{_sbindir}/arptables
%{_sbindir}/arptables-nft
%{_sbindir}/arptables-nft-restore
%{_sbindir}/arptables-nft-save
%{_sbindir}/arptables-restore
%{_sbindir}/arptables-save
%{_sbindir}/arptables-translate
%{_sbindir}/ip6tables-nft
%{_sbindir}/ip6tables-nft-restore
%{_sbindir}/ip6tables-nft-save
%{_sbindir}/iptables-nft
%{_sbindir}/iptables-nft-restore
%{_sbindir}/iptables-nft-save
%{_sbindir}/iptables-restore-translate
%{_sbindir}/iptables-translate
%{_sbindir}/ip6tables-restore-translate
%{_sbindir}/ip6tables-translate
%{_sbindir}/xtables-monitor
%{_libdir}/xtables/libarpt_mangle.so
%{_libdir}/xtables/libebt_802_3.so
%{_libdir}/xtables/libebt_among.so
%{_libdir}/xtables/libebt_arp.so
%{_libdir}/xtables/libebt_arpreply.so
%{_libdir}/xtables/libebt_dnat.so
%{_libdir}/xtables/libebt_ip.so
%{_libdir}/xtables/libebt_ip6.so
%{_libdir}/xtables/libebt_log.so
%{_libdir}/xtables/libebt_mark.so
%{_libdir}/xtables/libebt_mark_m.so
%{_libdir}/xtables/libebt_nflog.so
%{_libdir}/xtables/libebt_pkttype.so
%{_libdir}/xtables/libebt_redirect.so
%{_libdir}/xtables/libebt_snat.so
%{_libdir}/xtables/libebt_stp.so
%{_libdir}/xtables/libebt_vlan.so
%{_mandir}/man8/arptables-nft.8*
%{_mandir}/man8/arptables-nft-restore.8*
%{_mandir}/man8/arptables-nft-save.8*
%{_mandir}/man8/arptables-translate.8*
%{_mandir}/man8/ip6tables-restore-translate.8*
%{_mandir}/man8/ip6tables-translate.8*
%{_mandir}/man8/iptables-restore-translate.8*
%{_mandir}/man8/iptables-translate.8*
%{_mandir}/man8/xtables-legacy.8*
%{_mandir}/man8/xtables-monitor.8*
%{_mandir}/man8/xtables-nft.8*
%{_mandir}/man8/xtables-translate.8*
%endif

%files libs
%defattr(644,root,root,755)
%{_libdir}/libip4tc.so.*.*.*
%ghost %{_libdir}/libip4tc.so.2
%{_libdir}/libip6tc.so.*.*.*
%ghost %{_libdir}/libip6tc.so.2
%{_libdir}/libipq.so.*.*.*
%ghost %{_libdir}/libipq.so.0
%{_libdir}/libxtables.so.*.*.*
%ghost %{_libdir}/libxtables.so.12

%files devel
%defattr(644,root,root,755)
%if %{with doc}
%doc iptables-howtos/netfilter-hacking-HOWTO*
%endif
%{_libdir}/libip4tc.so
%{_libdir}/libip6tc.so
%{_libdir}/libipq.so
%{_libdir}/libiptc.so
%{_libdir}/libxtables.so
%{_includedir}/libipq.h
%{_includedir}/xtables.h
%{_includedir}/xtables-version.h
%{_includedir}/libiptc
%{_pkgconfigdir}/libip4tc.pc
%{_pkgconfigdir}/libip6tc.pc
%{_pkgconfigdir}/libipq.pc
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
%{_libdir}/libxtables.a
%endif

%files init
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/iptables-config
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/ip6tables-config
%attr(754,root,root) /etc/rc.d/init.d/iptables
%attr(754,root,root) /etc/rc.d/init.d/ip6tables
%{systemdunitdir}/iptables.service
%{systemdunitdir}/ip6tables.service

%if %{with nftables}
%files ebtables
%defattr(644,root,root,755)
# symlinks to xtables-nft-multi
%{_sbindir}/ebtables
%{_sbindir}/ebtables-nft
%{_sbindir}/ebtables-nft-restore
%{_sbindir}/ebtables-nft-save
%{_sbindir}/ebtables-restore
%{_sbindir}/ebtables-save
%{_sbindir}/ebtables-translate
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ethertypes
%{_mandir}/man8/ebtables-nft.8*
%{_mandir}/man8/ebtables-translate.8*
%endif
