%define prefix /opt/borhan
Summary: Toolkit for RTMP streams
Name: borhan-rtmpdump
Version: 2.3
Release: 3
License: GPLv2+
Group: Applications/Internet
URL: http://rtmpdump.mplayerhq.hu/

Source0: http://rtmpdump.mplayerhq.hu/download/rtmpdump-%{version}.tgz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: gnutls-devel >= 2.0
BuildRequires: zlib-devel
BuildRequires: libgcrypt-devel

%description
rtmpdump is a toolkit for RTMP streams. All forms of RTMP are supported,
including rtmp://, rtmpt://, rtmpe://, rtmpte://, and rtmps://. 

%package -n borhan-librtmp
Summary: Support library for RTMP streams
License: LGPLv2+
Group: Applications/Internet
Provides: librtmp

%description -n borhan-librtmp
librtmp is a suport library for RTMP streams. All forms of RTMP are supported,
including rtmp://, rtmpt://, rtmpe://, rtmpte://, and rtmps://. 

%package -n borhan-librtmp-devel
Summary: Files for librtmp development
License: LGPLv2+
Group: Applications/Internet
Requires: librtmp = %{version}-%{release}
Provides: librtmp-devel

%description -n borhan-librtmp-devel
librtmp is a suport library for RTMP streams. The librtmp-devel package
contains include files needed to develop applications using librtmp.

%prep
%setup -qn rtmpdump-%{version}

%build
%{__make} CRYPTO="GNUTLS" SHARED="yes" OPT="%{optflags}" LIB_GNUTLS="-lgnutls -lgcrypt -ldl" LIBRTMP="librtmp/librtmp.so" LIBS=""

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR="%{buildroot}" CRYPTO="GNUTLS" SHARED="yes" prefix="%{prefix}" mandir="%{prefix}/share/man" libdir="%{prefix}/lib"

%clean
%{__rm} -rf %{buildroot}

%post -n borhan-librtmp -p /sbin/ldconfig
%postun -n borhan-librtmp -p /sbin/ldconfig

%files
%defattr(-, root, root, 0755)
%doc COPYING README
%doc %{prefix}/share/man/man1/rtmpdump.1*
%doc %{prefix}/share/man/man8/rtmpgw.8*
%{prefix}/bin/rtmpdump
%{prefix}/sbin/rtmpgw
%{prefix}/sbin/rtmpsrv
%{prefix}/sbin/rtmpsuck

%files -n borhan-librtmp
%defattr(-, root, root, 0755)
%doc librtmp/COPYING
%{prefix}/lib/librtmp.so.0

%files -n borhan-librtmp-devel
%defattr(-, root, root, 0755)
%doc ChangeLog
%doc %{prefix}/share/man/man3/librtmp.3*
%{prefix}/include/librtmp/
%{prefix}/lib/librtmp.so
%{prefix}/lib/pkgconfig/librtmp.pc
%exclude %{prefix}/lib/librtmp.a

%changelog
* Mon Dec 8 2014 Jess Portnoy <jess.portnoy@borhan.com> 2.3-3
- Added Provides librtmp-devel tag

* Sun Jan 5 2014 Jess Portnoy <jess.portnoy@borhan.com> 2.3-2
- Adopted for Borhan. Required for borhan-ffmpeg. 
