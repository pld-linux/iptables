#
# Conditional build:
# _without_patchedkernel - without ippool, prestate, log (which requires patched 2.4.x kernel)
# _without_tex - without TeX documentation (HOWTOS)
#
Summary:	extensible packet filtering system && extensible NAT system
Summary(pl):	system filtrowania pakietów oraz system translacji adresów (NAT)
Name:		iptables
Version:	1.2.7a
%define		_rel	3
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL
Group:		Networking/Daemons
URL:		http://www.netfilter.org/
Vendor:		Netfilter mailing list <netfilter@lists.samba.org>
Source0:	http://www.netfilter.org/files/%{name}-%{version}.tar.bz2
Source1:	cvs://cvs.samba.org/netfilter/%{name}-howtos.tar.bz2
Patch0:		%{name}-man.patch
Patch3:		http://luxik.cdi.cz/~patrick/imq/iptables-1.2.6a-imq.diff-3
Patch4:		grsecurity-1.2.7a-iptables.patch
# patches from netfilter
Patch10:	ipt_REJECT-fake-source.patch.userspace
Patch11:	mark-bitwise-ops.patch.userspace
Patch12:	raw.patch.userspace
%{?!_without_tex:	BuildRequires:	sgml-tools}
%{?!_without_tex:	BuildRequires:	sgmls}
%{?!_without_tex:	BuildRequires:	tetex-latex}
%{?!_without_tex:	BuildRequires:	tetex-dvips}
BuildRequires:	perl
%{!?_without_patchedkernel:BuildRequires:	kernel_netfilter = 1.2.7a}
BuildConflicts:	kernel-headers < 2.3.0
Obsoletes:	netfilter
Obsoletes:	ipchains
%{!?_without_patchedkernel:Requires:	kernel_netfilter = 1.2.7a}
Provides:	firewall-userspace-tool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc

%description
An extensible NAT system, and an extensible packet filtering system.
Replacement of ipchains in 2.4 kernels.

%description -l pl
Wydajny system translacji adresów (NAT) oraz system filtrowania
pakietów. Zamiennik ipchains w j±drach 2.4

%package devel
Summary:	Libraries and headers for developing iptables extensions
Summary(pl):	Biblioteki i nag³ówki do tworzenia rozszerzeñ iptables
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
Libraries and headers for developing iptables extensions.

%description devel -l pl
Biblioteki i pliki nag³ówkowe niezbêdne do tworzenia rozszerzeñ dla
iptables.

%prep
%setup -q -a1
%patch0 -p1
%{!?_without_patchedkernel:%patch3 -p1}
%{!?_without_patchedkernel:%patch4 -p1}
%{!?_without_patchedkernel:%patch10 -p1}
%{!?_without_patchedkernel:%patch11 -p1}
%{!?_without_patchedkernel:%patch12 -p1}

chmod 755 extensions/.*-test*
mv -f extensions/.NETLINK.test extensions/.NETLINK-test
perl -pi -e 's/\$\(HTML_HOWTOS\)//g; s/\$\(PSUS_HOWTOS\)//g' iptables-howtos/Makefile

%build
%{__make} depend 2> /dev/null || :
%{__make} CC="%{__cc}" \
	COPT_FLAGS="%{rpmcflags} -D%{!?debug:N}DEBUG" \
	LIBDIR="%{_libdir}" \
	all experimental

%{?!_without_tex:%{__make} -C iptables-howtos}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir}/iptables,%{_mandir}/man3}

echo ".so iptables-save.8" > ip6tables-save.8
echo ".so iptables-restore.8" > ip6tables-restore.8

%{__make} install install-experimental \
	DESTDIR=$RPM_BUILD_ROOT \
	BINDIR=%{_sbindir} \
	MANDIR=%{_mandir} \
	LIBDIR=%{_libdir}

echo ".so iptables.8" > $RPM_BUILD_ROOT%{_mandir}/man8/ip6tables.8

# Devel stuff
cp -a include/* $RPM_BUILD_ROOT%{_includedir}/iptables
install lib*/lib*.a $RPM_BUILD_ROOT%{_libdir}
install libipq/*.3 $RPM_BUILD_ROOT%{_mandir}/man3

#%{!?_without_patchedkernel:install ippool/lib*.a $RPM_BUILD_ROOT%{_libdir}}
#%{!?_without_patchedkernel:install ippool/ippool $RPM_BUILD_ROOT%{_sbindir}}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc KNOWN_BUGS
%{?!_without_tex:%doc iptables-howtos/{NAT,networking-concepts,packet-filtering}-HOWTO*}

%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_libdir}/iptables/*.so

%{_mandir}/man8/*

%files devel
%defattr(644,root,root,755)
%{?!_without_tex:%doc iptables-howtos/netfilter-hacking-HOWTO*}
%{_libdir}/lib*.a
%{_includedir}/iptables
%{_mandir}/man3/*
