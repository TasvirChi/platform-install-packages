
%define base_prefix /opt/borhan/ffmpeg
%define _without_gsm 1
%define _without_nut 1

### No package yet
%define _without_vpx 1

### Use native vorbis
%define _without_vorbis 1

### Use native xvid
%define _without_xvid 1


%{?el6:%define _without_dc1394 1}
%{?el6:%define _without_schroedinger 1}
#%{?el6:%define _without_speex 1}
%{?el6:%define _without_theora 1}

%{?el5:%define _without_dc1394 1}
%{?el5:%define _without_schroedinger 1}
%{?el5:%define _without_speex 1}
%{?el5:%define _without_theora 1}

Summary: Utilities and libraries to record, convert and stream audio and video
Name: borhan-ffmpeg
Version: 3.2 
Release: 1
License: GPL
Group: Applications/Multimedia
URL: http://ffmpeg.org/

Packager: Jess Portnoy <jess.portnoy@borhan.com> 
Vendor: Borhan, Inc.

Source: http://www.ffmpeg.org/releases/ffmpeg-%{version}.tar.bz2
Source1: vf_transform.c 
#Patch0: allfilters.c.patch 
#Patch1: crypto.c.patch 
#Patch2: libopenjpegdec.c.patch 
#Patch3: libopenjpegenc.c.patch
Patch4: vf_transform.patch 
#Patch5: ffmpeg-3.1.3-configure.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: SDL-devel
BuildRequires: freetype-devel
BuildRequires: imlib2-devel
BuildRequires: zlib-devel
BuildRequires: schroedinger-devel
BuildRequires: libtheora-devel
BuildRequires: libvorbis-devel
BuildRequires: xvidcore-devel
BuildRequires: x265-devel
%{!?_without_a52dec:BuildRequires: borhan-a52dec-devel}
%{!?_without_dc1394:BuildRequires: libdc1394-devel}
%{!?_without_gsm:BuildRequires: gsm-devel}
%{!?_without_lame:BuildRequires: borhan-lame-devel}
%{!?_without_nut:BuildRequires: libnut-devel}
%{!?_without_opencore_amr:BuildRequires: borhan-libopencore-amr-devel}
%{!?_without_openjpeg:BuildRequires: openjpeg-devel}
%{!?_without_rtmp:BuildRequires: borhan-librtmp-devel}
%{!?_without_schroedinger:BuildRequires: schroedinger-devel}
%{!?_without_texi2html:BuildRequires: texi2html}
%{!?_without_theora:BuildRequires: libogg-devel, libtheora-devel}
%{!?_without_vorbis:BuildRequires: libogg-devel, libvorbis-devel}
%{!?_without_vpx:BuildRequires: libvpx-devel >= 1.3.0}
%{!?_without_x264:BuildRequires: borhan-x264-devel}
%{!?_without_xvid:BuildRequires: xvidcore-devel}
%{!?_without_a52dec:Requires: a52dec}
BuildRequires: yasm-devel
BuildRequires: libass-devel 
BuildRequires: borhan-x264-devel 
BuildRequires: gsm-devel
BuildRequires: speex-devel
BuildRequires: libvpx-devel >= 1.3.0
BuildRequires: schroedinger-devel 
BuildRequires: libtheora-devel
BuildRequires: xvidcore-devel >= 1.3.2
Requires:borhan-a52dec,libass,borhan-x264
Requires: libvpx >= 1.3.0
Requires: x265-libs

%description
FFmpeg is a very fast video and audio converter. It can also grab from a
live audio/video source.
The command line interface is designed to be intuitive, in the sense that
ffmpeg tries to figure out all the parameters, when possible. You have
usually to give only the target bitrate you want. FFmpeg can also convert
from any sample rate to any other, and resize video on the fly with a high
quality polyphase filter.

%package devel
Summary: Header files and static library for the ffmpeg codec library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: imlib2-devel, SDL-devel, freetype-devel, zlib-devel, pkgconfig,borhan-x264
%{!?_without_a52dec:Requires: borhan-a52dec-devel}
%{!?_without_dc1394:Requires: libdc1394-devel}
#%{!?_without_faad:Requires: faad2-devel}
%{!?_without_gsm:Requires: gsm-devel}
%{!?_without_lame:Requires: borhan-lame-devel}
%{!?_without_openjpeg:Requires: openjpeg-devel}
%{!?_without_rtmp:Requires: borhan-librtmp-devel}
%{!?_without_schroedinger:Requires: schroedinger-devel}
%{!?_without_vorbis:Requires: libogg-devel, libvorbis-devel}
%{!?_without_vpx:Requires: libvpx-devel}
%{!?_without_x264:Requires: borhan-x264-devel}
%{!?_without_xvid:Requires: xvidcore-devel}

%description devel
FFmpeg is a very fast video and audio converter. It can also grab from a
live audio/video source.
The command line interface is designed to be intuitive, in the sense that
ffmpeg tries to figure out all the parameters, when possible. You have
usually to give only the target bitrate you want. FFmpeg can also convert
from any sample rate to any other, and resize video on the fly with a high
quality polyphase filter.

Install this package if you want to compile apps with ffmpeg support.

%prep
%setup -qn ffmpeg-%{version}
#%patch0 -p1
#%patch1 -p1
#%patch2 -p1
#%patch3 -p1
%patch4 -p1
#%patch5 -p1
cp %{SOURCE1} %{_builddir}/ffmpeg-%{version}/libavfilter/


%build
export CFLAGS="%{optflags}"


./configure \
    --prefix="%{base_prefix}-%{version}" \
    --libdir="%{base_prefix}-%{version}/lib" \
    --shlibdir="%{base_prefix}-%{version}/lib" \
%{?_without_v4l:--disable-demuxer=v4l --disable-demuxer=v4l2} \
%ifarch %ix86
    --extra-cflags="%{optflags}" \
%endif
%ifarch x86_64
    --extra-cflags="%{optflags} -fPIC" \
%endif
    --extra-cflags="%{optflags} -fPIC -I/opt/borhan/include" \
    --extra-ldflags="-L/opt/borhan/lib" \
    --disable-devices \
    --enable-bzlib \
    --enable-libgsm \
    --enable-libmp3lame \
    --enable-libschroedinger \
    --enable-libtheora \
    --enable-libvorbis \
    --enable-libx264 \
    --enable-libx265 \
    --enable-avisynth \
    --enable-libxvid \
    --enable-filter=movie \
    --enable-avfilter \
    --enable-libopencore-amrnb \
    --enable-libopencore-amrwb \
    --enable-libopenjpeg \
    --enable-libvpx \
    --enable-libspeex \
    --enable-libass \
    --enable-postproc \
    --enable-pthreads \
    --enable-static \
    --enable-shared \
    --enable-gpl \
     --disable-debug \
    --disable-optimizations \
--enable-gpl \
--enable-pthreads \
--enable-swscale \
--enable-vdpau \
--enable-bzlib \
--disable-devices \
--enable-filter=movie \
    --enable-version3 \
--enable-indev=lavfi \
--enable-x11grab

%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot} _docs
%{__make} install DESTDIR="%{buildroot}"
cd tools && gcc qt-faststart.c -o qt-faststart
mv qt-faststart %{buildroot}%{base_prefix}-%{version}/bin
cd - 
# Remove unwanted files from the included docs
%{__cp} -a doc _docs
%{__rm} -rf _docs/{Makefile,*.texi,*.pl}

# The <postproc/postprocess.h> is now at <ffmpeg/postprocess.h>, so provide
# a compatibility symlink
%{__mkdir_p} %{buildroot}%{base_prefix}-%{version}/include/postproc/
%{__mkdir_p} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
cat > $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/borhan_ffmpeg.sh << EOF
PATH=\$PATH:%{base_prefix}-%{version}/bin
export PATH
EOF
%{__mkdir_p} $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d
cat > $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/borhan_ffmpeg.conf << EOF
%{base_prefix}-%{version}/lib
EOF

%clean
%{__rm} -rf %{buildroot}

%post
/sbin/ldconfig
chcon -t textrel_shlib_t %{base_prefix}-%{version}/lib/libav{codec,device,format,util}.so.*.*.* &>/dev/null || :
ln -fs %{base_prefix}-%{version}/bin/ffmpeg /opt/borhan/bin 
ln -fs %{base_prefix}-%{version}/bin/ffprobe /opt/borhan/bin 
ln -fs %{base_prefix}-%{version}/bin/qt-faststart /opt/borhan/bin 

%postun 
/sbin/ldconfig
if [ "$1" = 0 ] ; then
	rm -f /opt/borhan/bin/ffmpeg
	rm -f /opt/borhan/bin/qt-faststart
fi


%files
%defattr(-, root, root, 0755)
%doc Changelog COPYING* CREDITS INSTALL.md MAINTAINERS RELEASE RELEASE_NOTES README.md 
#%doc Changelog COPYING* CREDITS INSTALL MAINTAINERS RELEASE README
%doc %{base_prefix}-%{version}/share/man/man1
%config %{_sysconfdir}/profile.d/borhan_ffmpeg.sh
%config %{_sysconfdir}/ld.so.conf.d/borhan_ffmpeg.conf
#%{base_prefix}-%{version}/bin/ffprobe
%{base_prefix}-%{version}/bin/*
#%{base_prefix}-%{version}/bin/ffplay
#%{base_prefix}-%{version}/bin/ffserver
%{base_prefix}-%{version}/share/ffmpeg/
%{base_prefix}-%{version}/lib/*.so*
%{base_prefix}-%{version}/lib/pkgconfig/
%exclude %{base_prefix}-%{version}/lib/*.a
%exclude %{base_prefix}-%{version}/include

%files devel
%defattr(-, root, root, 0755)
%doc _docs/*
%{base_prefix}-%{version}/include/libavcodec/
%{base_prefix}-%{version}/include/libavdevice/
%{base_prefix}-%{version}/include/libavfilter/
%{base_prefix}-%{version}/include/libavformat/
%{base_prefix}-%{version}/include/libavutil/
%{base_prefix}-%{version}/include/libswscale/
#%{base_prefix}-%{version}/lib/libavcodec.a
#%{base_prefix}-%{version}/lib/libavdevice.a
#%{base_prefix}-%{version}/lib/libavfilter.a
#%{base_prefix}-%{version}/lib/libavformat.a
#%{base_prefix}-%{version}/lib/libavutil.a
#%{base_prefix}-%{version}/lib/libswscale.a
#%{base_prefix}-%{version}/lib/libavcodec.so
#%{base_prefix}-%{version}/lib/libavdevice.so
#%{base_prefix}-%{version}/lib/libavfilter.so
#%{base_prefix}-%{version}/lib/libavformat.so
#%{base_prefix}-%{version}/lib/libavutil.so
#%{base_prefix}-%{version}/lib/libswscale.so
%{base_prefix}-%{version}/lib/*so*
%{base_prefix}-%{version}/lib/pkgconfig/libavcodec.pc
%{base_prefix}-%{version}/lib/pkgconfig/libavdevice.pc
%{base_prefix}-%{version}/lib/pkgconfig/libavfilter.pc
%{base_prefix}-%{version}/lib/pkgconfig/libavformat.pc
%{base_prefix}-%{version}/lib/pkgconfig/libavutil.pc
%{base_prefix}-%{version}/lib/pkgconfig/libswscale.pc
%{base_prefix}-%{version}/share

%changelog
* Tue Dec 6 2016 Jess Portnoy <jess.portnoy@borhan.com> - 3.2-1
- 3.2 first release

* Mon Sep 19 2016 Jess Portnoy <jess.portnoy@borhan.com> - 3.1.3-2
- Patches:
	https://github.com/FFmpeg/FFmpeg/commit/a13a81a0dc98a35293f3f2603db9b01bf76b6a05
	https://trac.ffmpeg.org/attachment/ticket/5694/ffmpeg_opj2.patch
	https://github.com/facebook/transform

* Sun Sep 18 2016 Jess Portnoy <jess.portnoy@borhan.com> - 3.1.3-1
- 3.1.3 first build.

* Thu Oct 8 2015 Jess Portnoy <jess.portnoy@borhan.com> - 2.7.2-2
- symlink ffprobe to /opt/borhan/bin

* Wed Oct 7 2015 Jess Portnoy <jess.portnoy@borhan.com> - 2.7.2-1
- 2.7.2

* Thu Aug 6 2015 Jess Portnoy <jess.portnoy@borhan.com> - 2.1.3-8
- Require libvpx >=1.3.0 since CentOS 6 also had 1.2.0 at some stage and they are not binary compatible.

* Wed Aug 5 2015 Jess Portnoy <jess.portnoy@borhan.com> - 2.1.3-7
- Do not compile against FDK and faac as distributing the binary with such support violates license.
  See:
  https://github.com/borhan/platform-install-packages/issues/392
  https://trac.ffmpeg.org/ticket/4735

* Mon Jul 7 2014 Jess Portnoy <jess.portnoy@borhan.com> - 2.1.3-1
- 2.1.3.

* Sun Jan 12 2014 Jess Portnoy <jess.portnoy@borhan.com> - 1.1.1-4
- Added qt-faststart.

* Sun Jan 12 2014 Jess Portnoy <jess.portnoy@borhan.com> - 1.1.1-3
- Remove symlink to /opt/borhan/bin/ffmpeg at %%postun.

* Sun Jan 5 2014 Jess Portnoy <jess.portnoy@borhan.com> - 1.1.1-2 
- path in /etc/profile.d/borhan_ffmpeg.sh corrected.

* Wed Dec 25 2013 Jess Portnoy <jess.portnoy@borhan.com> - 1.1.1-1
- Initial build.
