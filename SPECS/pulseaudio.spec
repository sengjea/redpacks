%global pa_major   3.0
#global pa_minor   0

%ifarch %{ix86} x86_64 %{arm}
%global with_webrtc 1
%endif

Name:           pulseaudio
Summary:        Improved Linux Sound Server
Version:        %{pa_major}%{?pa_minor:.%{pa_minor}}
Release:        10%{?dist}
License:        LGPLv2+
URL:            http://www.freedesktop.org/wiki/Software/PulseAudio
Source0:        http://freedesktop.org/software/pulseaudio/releases/pulseaudio-%{version}.tar.xz
Source1:        default.pa-for-gdm

## upstream patches
Patch101: 0001-alsa-mixer-Fix-the-analog-output-speaker-always-path.patch
Patch102: 0002-man-Update-log-target-documentation.patch
Patch103: 0003-build-Don-t-enable-BlueZ-if-libbluetooth-is-not-foun.patch
Patch104: 0004-Call-change_cb-only-when-there-s-an-actual-change.patch
Patch105: 0005-Initialize-monitor-s-busy-status-to-false-if-we-own-.patch
Patch106: 0006-reserve-Move-get_name_owner-to-the-public-rd_device-.patch
Patch107: 0007-reserve-Fix-leaking-NameLost-signals-after-release-a.patch

BuildRequires:  m4
BuildRequires:  libtool-ltdl-devel
BuildRequires:  intltool
BuildRequires:  pkgconfig
BuildRequires:  doxygen
BuildRequires:  xmltoman
BuildRequires:  tcp_wrappers-devel
BuildRequires:  libsamplerate-devel
BuildRequires:  libsndfile-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  glib2-devel
BuildRequires:  gtk2-devel
BuildRequires:  GConf2-devel
BuildRequires:  avahi-devel
%if 0%{?rhel} == 0
BuildRequires:  lirc-devel
BuildRequires:  jack-audio-connection-kit-devel
%endif
BuildRequires:  libatomic_ops-static, libatomic_ops-devel
%ifnarch s390 s390x
BuildRequires:  bluez-libs-devel
BuildRequires:  sbc-devel
%endif
BuildRequires:  libXt-devel
BuildRequires:  xorg-x11-proto-devel
BuildRequires:  libXtst-devel
BuildRequires:  libXi-devel
BuildRequires:  libSM-devel
BuildRequires:  libX11-devel
BuildRequires:  libICE-devel
BuildRequires:  xcb-util-devel
BuildRequires:  openssl-devel
BuildRequires:  orc-devel
BuildRequires:  libtdb-devel
BuildRequires:  speex-devel >= 1.2
BuildRequires:  systemd-devel
BuildRequires:  libasyncns-devel
BuildRequires:  systemd-devel >= 184
BuildRequires:  json-c-devel
BuildRequires:  dbus-devel
BuildRequires:  libcap-devel
%if 0%{?with_webrtc}
BuildRequires:  webrtc-audio-processing-devel
%endif

# retired along with -libs-zeroconf, add Obsoletes here for lack of anything better
Obsoletes:      padevchooser < 1.0
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       systemd >= 184
Requires:       rtkit
Requires:       kernel >= 2.6.30

%description
PulseAudio is a sound server for Linux and other Unix like operating
systems. It is intended to be an improved drop-in replacement for the
Enlightened Sound Daemon (ESOUND).

%package esound-compat
Summary:        PulseAudio EsounD daemon compatibility script
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description esound-compat
A compatibility script that allows applications to call /usr/bin/esd
and start PulseAudio with EsounD protocol modules.

%if 0%{?rhel} == 0
%package module-lirc
Summary:        LIRC support for the PulseAudio sound server
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description module-lirc
LIRC volume control module for the PulseAudio sound server.
%endif

%package module-x11
Summary:        X11 support for the PulseAudio sound server
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-utils

%description module-x11
X11 bell and security modules for the PulseAudio sound server.

%package module-zeroconf
Summary:        Zeroconf support for the PulseAudio sound server
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-utils

%description module-zeroconf
Zeroconf publishing module for the PulseAudio sound server.

%ifnarch s390 s390x
%package module-bluetooth
Summary:        Bluetooth support for the PulseAudio sound server
Requires:       %{name} = %{version}-%{release}
Requires:       bluez >= 4.34

%description module-bluetooth
Contains Bluetooth audio (A2DP/HSP/HFP) support for the PulseAudio sound server.

Also contains a module that can be used to automatically turn down the volume if
a bluetooth mobile phone leaves the proximity or turn it up again if it enters the
proximity again
%endif

%if 0%{?rhel} == 0
%package module-jack
Summary:        JACK support for the PulseAudio sound server
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description module-jack
JACK sink and source modules for the PulseAudio sound server.
%endif

%package module-gconf
Summary:        GConf support for the PulseAudio sound server
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description module-gconf
GConf configuration backend for the PulseAudio sound server.

%package libs
Summary:        Libraries for PulseAudio clients
License:        LGPLv2+
Obsoletes:      pulseaudio-libs-zeroconf < 1.1

%description libs
This package contains the runtime libraries for any application that wishes
to interface with a PulseAudio sound server.

%package libs-glib2
Summary:        GLIB 2.x bindings for PulseAudio clients
License:        LGPLv2+
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description libs-glib2
This package contains bindings to integrate the PulseAudio client library with
a GLIB 2.x based application.

%package libs-devel
Summary:        Headers and libraries for PulseAudio client development
License:        LGPLv2+
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       %{name}-libs-glib2%{?_isa} = %{version}-%{release}
%if 0%{?rhel} == 0
Requires:       vala
%endif

%description libs-devel
Headers and libraries for developing applications that can communicate with
a PulseAudio sound server.

%package utils
Summary:        PulseAudio sound server utilities
License:        LGPLv2+
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
# when made non-multilib'd, https://bugzilla.redhat.com/891425
Obsoletes:      pulseaudio-utils < 3.0-3

%description utils
This package contains command line utilities for the PulseAudio sound server.

%package gdm-hooks
Summary:        PulseAudio GDM integration
License:        LGPLv2+
Requires:       gdm >= 1:2.22.0
# for the gdm user
Requires(pre):  gdm

%description gdm-hooks
This package contains GDM integration hooks for the PulseAudio sound server.

%prep
%setup -q -T -b0

%patch101 -p1 -b .0001
%patch102 -p1 -b .0002
## skip to avoid needless (re)autoconf
#patch103 -p1 -b .0003
%patch104 -p1 -b .0004
%patch105 -p1 -b .0005
%patch106 -p1 -b .0006
%patch107 -p1 -b .0007

## kill rpaths
%if "%{_libdir}" != "/usr/lib"
sed -i -e 's|"/lib /usr/lib|"/%{_lib} %{_libdir}|' configure
%endif

%build

%configure \
  --disable-static \
  --disable-rpath \
  --with-system-user=pulse \
  --with-system-group=pulse \
  --with-access-group=pulse-access \
  --disable-oss-output \
  --without-fftw \
%ifarch %{arm}
  --disable-neon-opt \
%endif
  --enable-systemd \
%if 0%{?with_webrtc}
  --enable-webrtc-aec
%endif

# we really should preopen here --preopen-mods=module-udev-detect.la, --force-preopen

make %{?_smp_mflags} V=1
make doxygen

%install
make install DESTDIR=$RPM_BUILD_ROOT

# upstream should use udev.pc
mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/udev/rules.d
mv -f $RPM_BUILD_ROOT/lib/udev/rules.d/90-pulseaudio.rules $RPM_BUILD_ROOT%{_prefix}/lib/udev/rules.d

rm -fv $RPM_BUILD_ROOT%{_libdir}/*.la $RPM_BUILD_ROOT%{_libdir}/pulse-%{pa_major}/modules/*.la
rm -fv $RPM_BUILD_ROOT%{_libdir}/pulse-%{pa_major}/modules/module-detect.so
# preserve time stamps, for multilib's sake
touch -r src/daemon/daemon.conf.in $RPM_BUILD_ROOT%{_sysconfdir}/pulse/daemon.conf
touch -r src/daemon/default.pa.in $RPM_BUILD_ROOT%{_sysconfdir}/pulse/default.pa
touch -r man/pulseaudio.1.xml.in $RPM_BUILD_ROOT%{_mandir}/man1/pulseaudio.1
touch -r man/default.pa.5.xml.in $RPM_BUILD_ROOT%{_mandir}/man5/default.pa.5
touch -r man/pulse-client.conf.5.xml.in $RPM_BUILD_ROOT%{_mandir}/man5/pulse-client.conf.5
touch -r man/pulse-daemon.conf.5.xml.in $RPM_BUILD_ROOT%{_mandir}/man5/pulse-daemon.conf.5
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/pulse
install -p -m644 -D %{SOURCE1} $RPM_BUILD_ROOT%{_localstatedir}/lib/gdm/.pulse/default.pa

sed -i -e 's/^load-module module-console-kit/#load-module module-console-kit/' $RPM_BUILD_ROOT/etc/pulse/default.pa

%find_lang %{name}

%pre
/usr/sbin/groupadd -f -r pulse || :
/usr/bin/id pulse >/dev/null 2>&1 || \
            /usr/sbin/useradd -r -c 'PulseAudio System Daemon' -s /sbin/nologin -d /var/run/pulse -g pulse pulse || :
/usr/sbin/groupadd -f -r pulse-access || :
exit 0

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%posttrans
# handle renamed module-cork-music-on-phone => module-role-cork
(grep '^load-module module-cork-music-on-phone$' %{_sysconfdir}/pulse/default.pa > /dev/null && \
 sed -i.rpmsave -e 's|^load-module module-cork-music-on-phone$|load-module module-role-cork|' \
 %{_sysconfdir}/pulse/default.pa
) ||:

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%post libs-glib2 -p /sbin/ldconfig
%postun libs-glib2 -p /sbin/ldconfig

%files
%doc README LICENSE GPL LGPL
%dir %{_sysconfdir}/pulse/
%config(noreplace) %{_sysconfdir}/pulse/daemon.conf
%config(noreplace) %{_sysconfdir}/pulse/default.pa
%config(noreplace) %{_sysconfdir}/pulse/system.pa
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/pulseaudio-system.conf
%{_bindir}/pulseaudio
%{_libdir}/libpulsecore-%{pa_major}.so
%dir %{_libdir}/pulse-%{pa_major}/
%dir %{_libdir}/pulse-%{pa_major}/modules/
%{_libdir}/pulse-%{pa_major}/modules/libalsa-util.so
%{_libdir}/pulse-%{pa_major}/modules/libcli.so
%{_libdir}/pulse-%{pa_major}/modules/libprotocol-cli.so
%{_libdir}/pulse-%{pa_major}/modules/libprotocol-esound.so
%{_libdir}/pulse-%{pa_major}/modules/libprotocol-http.so
%{_libdir}/pulse-%{pa_major}/modules/libprotocol-native.so
%{_libdir}/pulse-%{pa_major}/modules/libprotocol-simple.so
%{_libdir}/pulse-%{pa_major}/modules/librtp.so
%if 0%{?with_webrtc}
%{_libdir}/pulse-%{pa_major}/modules/libwebrtc-util.so
%endif
%{_libdir}/pulse-%{pa_major}/modules/module-alsa-sink.so
%{_libdir}/pulse-%{pa_major}/modules/module-alsa-source.so
%{_libdir}/pulse-%{pa_major}/modules/module-alsa-card.so
%{_libdir}/pulse-%{pa_major}/modules/module-cli-protocol-tcp.so
%{_libdir}/pulse-%{pa_major}/modules/module-cli-protocol-unix.so
%{_libdir}/pulse-%{pa_major}/modules/module-cli.so
%{_libdir}/pulse-%{pa_major}/modules/module-combine.so
%{_libdir}/pulse-%{pa_major}/modules/module-combine-sink.so
%{_libdir}/pulse-%{pa_major}/modules/module-dbus-protocol.so
%{_libdir}/pulse-%{pa_major}/modules/module-filter-apply.so
%{_libdir}/pulse-%{pa_major}/modules/module-filter-heuristics.so
%{_libdir}/pulse-%{pa_major}/modules/module-device-manager.so
%{_libdir}/pulse-%{pa_major}/modules/module-loopback.so
%{_libdir}/pulse-%{pa_major}/modules/module-esound-compat-spawnfd.so
%{_libdir}/pulse-%{pa_major}/modules/module-esound-compat-spawnpid.so
%{_libdir}/pulse-%{pa_major}/modules/module-esound-protocol-tcp.so
%{_libdir}/pulse-%{pa_major}/modules/module-esound-protocol-unix.so
%{_libdir}/pulse-%{pa_major}/modules/module-esound-sink.so
%{_libdir}/pulse-%{pa_major}/modules/module-udev-detect.so
%{_libdir}/pulse-%{pa_major}/modules/module-hal-detect.so
%{_libdir}/pulse-%{pa_major}/modules/module-http-protocol-tcp.so
%{_libdir}/pulse-%{pa_major}/modules/module-http-protocol-unix.so
%{_libdir}/pulse-%{pa_major}/modules/module-match.so
%{_libdir}/pulse-%{pa_major}/modules/module-mmkbd-evdev.so
%{_libdir}/pulse-%{pa_major}/modules/module-native-protocol-fd.so
%{_libdir}/pulse-%{pa_major}/modules/module-native-protocol-tcp.so
%{_libdir}/pulse-%{pa_major}/modules/module-native-protocol-unix.so
%{_libdir}/pulse-%{pa_major}/modules/module-null-sink.so
%{_libdir}/pulse-%{pa_major}/modules/module-null-source.so
%{_libdir}/pulse-%{pa_major}/modules/module-pipe-sink.so
%{_libdir}/pulse-%{pa_major}/modules/module-pipe-source.so
%{_libdir}/pulse-%{pa_major}/modules/module-rescue-streams.so
%{_libdir}/pulse-%{pa_major}/modules/module-rtp-recv.so
%{_libdir}/pulse-%{pa_major}/modules/module-rtp-send.so
%{_libdir}/pulse-%{pa_major}/modules/module-simple-protocol-tcp.so
%{_libdir}/pulse-%{pa_major}/modules/module-simple-protocol-unix.so
%{_libdir}/pulse-%{pa_major}/modules/module-sine.so
%{_libdir}/pulse-%{pa_major}/modules/module-switch-on-port-available.so
%{_libdir}/pulse-%{pa_major}/modules/module-systemd-login.so
%{_libdir}/pulse-%{pa_major}/modules/module-tunnel-sink.so
%{_libdir}/pulse-%{pa_major}/modules/module-tunnel-source.so
%{_libdir}/pulse-%{pa_major}/modules/module-volume-restore.so
%{_libdir}/pulse-%{pa_major}/modules/module-suspend-on-idle.so
%{_libdir}/pulse-%{pa_major}/modules/module-default-device-restore.so
%{_libdir}/pulse-%{pa_major}/modules/module-device-restore.so
%{_libdir}/pulse-%{pa_major}/modules/module-stream-restore.so
%{_libdir}/pulse-%{pa_major}/modules/module-card-restore.so
%{_libdir}/pulse-%{pa_major}/modules/module-ladspa-sink.so
%{_libdir}/pulse-%{pa_major}/modules/module-remap-sink.so
%{_libdir}/pulse-%{pa_major}/modules/module-always-sink.so
%{_libdir}/pulse-%{pa_major}/modules/module-console-kit.so
%{_libdir}/pulse-%{pa_major}/modules/module-position-event-sounds.so
%{_libdir}/pulse-%{pa_major}/modules/module-augment-properties.so
%{_libdir}/pulse-%{pa_major}/modules/module-role-cork.so
%{_libdir}/pulse-%{pa_major}/modules/module-sine-source.so
%{_libdir}/pulse-%{pa_major}/modules/module-intended-roles.so
%{_libdir}/pulse-%{pa_major}/modules/module-rygel-media-server.so
%{_libdir}/pulse-%{pa_major}/modules/module-echo-cancel.so
%{_libdir}/pulse-%{pa_major}/modules/module-switch-on-connect.so
%{_libdir}/pulse-%{pa_major}/modules/module-virtual-sink.so
%{_libdir}/pulse-%{pa_major}/modules/module-virtual-source.so
%{_libdir}/pulse-%{pa_major}/modules/module-virtual-surround-sink.so
%dir %{_datadir}/pulseaudio/
%dir %{_datadir}/pulseaudio/alsa-mixer/
%{_datadir}/pulseaudio/alsa-mixer/paths/
%{_datadir}/pulseaudio/alsa-mixer/profile-sets/
%{_mandir}/man1/pulseaudio.1*
%{_mandir}/man5/default.pa.5*
%{_mandir}/man5/pulse-cli-syntax.5*
%{_mandir}/man5/pulse-client.conf.5*
%{_mandir}/man5/pulse-daemon.conf.5*
%{_prefix}/lib/udev/rules.d/90-pulseaudio.rules
%dir %{_libexecdir}/pulse
%attr(0700, pulse, pulse) %dir %{_localstatedir}/lib/pulse

%files esound-compat
%{_bindir}/esdcompat
%{_mandir}/man1/esdcompat.1.gz

%if 0%{?rhel} == 0
%files module-lirc
%{_libdir}/pulse-%{pa_major}/modules/module-lirc.so
%endif

%files module-x11
%config %{_sysconfdir}/xdg/autostart/pulseaudio.desktop
%config %{_sysconfdir}/xdg/autostart/pulseaudio-kde.desktop
%{_bindir}/start-pulseaudio-kde
%{_bindir}/start-pulseaudio-x11
%{_libdir}/pulse-%{pa_major}/modules/module-x11-bell.so
%{_libdir}/pulse-%{pa_major}/modules/module-x11-publish.so
%{_libdir}/pulse-%{pa_major}/modules/module-x11-xsmp.so
%{_libdir}/pulse-%{pa_major}/modules/module-x11-cork-request.so
%{_mandir}/man1/start-pulseaudio-kde.1.gz
%{_mandir}/man1/start-pulseaudio-x11.1.gz

%files module-zeroconf
%{_libdir}/pulse-%{pa_major}/modules/libavahi-wrap.so
%{_libdir}/pulse-%{pa_major}/modules/module-zeroconf-publish.so
%{_libdir}/pulse-%{pa_major}/modules/module-zeroconf-discover.so
%{_libdir}/pulse-%{pa_major}/modules/libraop.so
%{_libdir}/pulse-%{pa_major}/modules/module-raop-discover.so
%{_libdir}/pulse-%{pa_major}/modules/module-raop-sink.so

%if 0%{?rhel} == 0
%files module-jack
%{_libdir}/pulse-%{pa_major}/modules/module-jackdbus-detect.so
%{_libdir}/pulse-%{pa_major}/modules/module-jack-sink.so
%{_libdir}/pulse-%{pa_major}/modules/module-jack-source.so
%endif

%ifnarch s390 s390x
%files module-bluetooth
%{_libdir}/pulse-%{pa_major}/modules/module-bluetooth-device.so
%{_libdir}/pulse-%{pa_major}/modules/module-bluetooth-discover.so
%{_libdir}/pulse-%{pa_major}/modules/module-bluetooth-policy.so
%{_libdir}/pulse-%{pa_major}/modules/module-bluetooth-proximity.so
%{_libdir}/pulse-%{pa_major}/modules/libbluetooth-util.so
%{_libexecdir}/pulse/proximity-helper
%endif

%files module-gconf
%{_libdir}/pulse-%{pa_major}/modules/module-gconf.so
%{_libexecdir}/pulse/gconf-helper

%files libs -f %{name}.lang
%doc README LICENSE GPL LGPL
%dir %{_sysconfdir}/pulse/
%config(noreplace) %{_sysconfdir}/pulse/client.conf
%{_libdir}/libpulse.so.*
%{_libdir}/libpulse-simple.so.*
%dir %{_libdir}/pulseaudio/
%{_libdir}/pulseaudio/libpulsecommon-%{pa_major}.*
%{_libdir}/pulseaudio/libpulsedsp.*

%files libs-glib2
%{_libdir}/libpulse-mainloop-glib.so.*

%files libs-devel
%doc doxygen/html
%{_includedir}/pulse/
%{_libdir}/libpulse.so
%{_libdir}/libpulse-mainloop-glib.so
%{_libdir}/libpulse-simple.so
%{_libdir}/pkgconfig/libpulse*.pc
%{_datadir}/vala/vapi/libpulse.vapi
%{_datadir}/vala/vapi/libpulse.deps
%{_datadir}/vala/vapi/libpulse-mainloop-glib.vapi
%{_datadir}/vala/vapi/libpulse-mainloop-glib.deps
%{_libdir}/cmake/PulseAudio/

%files utils
%{_bindir}/pacat
%{_bindir}/pacmd
%{_bindir}/pactl
%{_bindir}/paplay
%{_bindir}/parec
%{_bindir}/pamon
%{_bindir}/parecord
%{_bindir}/pax11publish
%{_bindir}/padsp
%{_bindir}/pasuspender
%{_mandir}/man1/pacat.1.gz
%{_mandir}/man1/pacmd.1.gz
%{_mandir}/man1/pactl.1.gz
%{_mandir}/man1/paplay.1.gz
%{_mandir}/man1/pasuspender.1.gz
%{_mandir}/man1/padsp.1.gz
%{_mandir}/man1/pax11publish.1.gz

%files gdm-hooks
%attr(0700, gdm, gdm) %dir %{_localstatedir}/lib/gdm/.pulse
%attr(0600, gdm, gdm) %{_localstatedir}/lib/gdm/.pulse/default.pa

%changelog
* Thu May 30 2013 Rex Dieter <rdieter@fedoraproject.org> 3.0-10
- avoid needless (re)autoconf

* Thu May 30 2013 Rex Dieter <rdieter@fedoraproject.org> 3.0-9
- [RFE] Build with libcap (#969232)

* Fri May 03 2013 Rex Dieter <rdieter@fedoraproject.org> 3.0-8
- RFE: Restore the pipe-sink and pipe-source modules (#958949)

* Thu Apr 11 2013 Rex Dieter <rdieter@fedoraproject.org> 3.0-7
- pull a few more patches from upstream stable-3.x branch

* Fri Feb 08 2013 Rex Dieter <rdieter@fedoraproject.org> 3.0-6
- default.pa: fix for renamed modules (#908117)

* Sat Jan 19 2013 Ville Skyttä <ville.skytta@iki.fi> - 3.0-5
- Own the %%{_libdir}/pulseaudio dir.
- Fix bogus %%changelog dates.

* Fri Jan 04 2013 Rex Dieter <rdieter@fedoraproject.org> 3.0-4
- alsa-mixer: Fix the analog-output-speaker-always path

* Fri Jan 04 2013 Rex Dieter <rdieter@fedoraproject.org> 3.0-3
- move libpulsedsp plugin to -libs, avoids -utils multilib (#891425)

* Wed Dec 19 2012 Dan Horák <dan[at]danny.cz> 3.0-2
- SBC is needed only when BlueZ is used

* Tue Dec 18 2012 Rex Dieter <rdieter@fedoraproject.org> 3.0-1
- pulseaudio-3.0

* Tue Dec 11 2012 Peter Robinson <pbrobinson@fedoraproject.org> 2.99.3-1
- PulseAudio 2.99.3 (3.0 rc3)

* Wed Oct 10 2012 Dan Horák <dan[at]danny.cz> 2.1-4
- fix the with_webrtc condition

* Tue Oct 09 2012 Dan Horák <dan[at]danny.cz> 2.1-3
- webrtc-aec is x86 and ARM only for now

* Mon Oct 08 2012 Debarshi Ray <rishi@fedoraproject.org> 2.1-2
- Enable webrtc-aec

* Tue Sep 25 2012 Rex Dieter <rdieter@fedoraproject.org> 2.1-1
- pulseaudio-2.1

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 23 2012 Kalev Lember <kalevlember@gmail.com> - 2.0-3
- Move module-jackdbus-detect.so to -module-jack subpackage with the
  rest of the jack modules

* Mon Jun 04 2012 Kay Sievers <kay@redhat.com> - 2.0-2
- rebuild for libudev1

* Sat May 12 2012 Rex Dieter <rdieter@fedoraproject.org> 2.0-1
- pulseaudio-2.0

* Sat Apr 21 2012 Matthias Clasen <mclasen@redhat.com> - 1.1-9
- Don't load the ck module in gdm, either

* Tue Feb 28 2012 Bruno Wolff III <bruno@wolff.to> - 1.1-8
- Bring in Lennart's patch from f17
- Temporary fix for CK/systemd move (#794690)

* Tue Feb 28 2012 Bruno Wolff III <bruno@wolff.to> - 1.1-7
- Fix for building with gcc 4.7

* Mon Jan 23 2012 Dan Horák <dan@danny.cz> - 1.1-6
- rebuilt for json-c-0.9-4.fc17

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 13 2011 Adam Jackson <ajax@redhat.com> 1.1-4
- Fix RHEL build

* Tue Nov 22 2011 Rex Dieter <rdieter@fedoraproject.org> 1.1-3
- Obsoletes: padevchooser < 1.0

* Thu Nov 10 2011 Rex Dieter <rdieter@fedoraproject.org> 1.1-2
- -libs: Obsoletes: pulseaudio-libs-zeroconf
- use versioned Obsoletes/Provides
- tighten subpkg deps via %%_isa
- remove autoconf/libtool hackery

* Thu Nov  3 2011 Lennart Poettering <lpoetter@redhat.com> - 1.1-1
- New upstream release

* Mon Aug 15 2011 Matthias Clasen <mclasen@redhat.com> - 0.9.23-1
- Update to 0.9.23

* Thu Apr  7 2011 Peter Robinson <pbrobinson@gmail.com> - 0.9.22-5
- Add upstream patch to fix compilation on ARM

* Mon Mar 28 2011 Matthias Clasen <mclasen@redhat.com> - 0.9.22-4
- Activate pulseaudio earlier during login

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 30 2011 Ville Skyttä <ville.skytta@iki.fi> - 0.9.22-2
- Own /usr/share/pulseaudio dirs.

* Fri Nov 26 2010 Lennart Poettering <lpoetter@redhat.com> - 0.9.22-1
- New upstream release

* Sun Nov 21 2010 Matěj Cepl <mcepl@redhat.com> - 0.9.21-7
- Fix racy condition with patch by jkratoch (RHBZ# 643296).

* Tue Feb 23 2010 Lennart Poettering <lpoetter@redhat.com> - 0.9.21-6
- backport another 30 fixes from upstream git

* Sun Jan 17 2010 Lennart Poettering <lpoetter@redhat.com> - 0.9.21-5
- fix buffer flushing

* Fri Jan 15 2010 Lennart Poettering <lpoetter@redhat.com> - 0.9.21-4
- backport 31 fixes from upstream git
- sync spec file with rhel

* Tue Dec  8 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 0.9.21-3
- Explicitly BR libatomic_ops-static in accordance with the Packaging
  Guidelines (libatomic_ops-devel is still static-only).

* Wed Dec 02 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.9.21-2
- module-device-manager, kde autostart bits missing (#541419)

* Mon Nov 23 2009 Lennart Poettering <lpoetter@redhat.com> - 0.9.21-1
- New release

* Wed Nov 11 2009 Lennart Poettering <lpoetter@redhat.com> - 0.9.20-1
- New release

* Wed Nov 04 2009 Warren Togami <wtogami@redhat.com> - 0.9.19-2
- Bug #532583 gdm should not require pulseaudio

* Wed Sep 30 2009 Lennart Poettering <lpoetter@redhat.com> - 0.9.19-1
- New release

* Sat Sep 19 2009 Lennart Poettering <lpoetter@redhat.com> - 0.9.18-1
- New release

* Fri Sep 11 2009 Lennart Poettering <lpoetter@redhat.com> 0.9.17-1
- Final release

* Thu Sep 10 2009 Lennart Poettering <lpoetter@redhat.com> 0.9.16-14
- Final release

* Thu Sep 3 2009 Lennart Poettering <lpoetter@redhat.com> 0.9.16-13.test7
- Fix build for ppc

* Thu Sep 3 2009 Lennart Poettering <lpoetter@redhat.com> 0.9.16-12.test7
- New test release

* Thu Aug 27 2009 Tomas Mraz <tmraz@redhat.com> - 0.9.16-11.test6
- rebuilt with new openssl

* Mon Aug 24 2009 Lennart Poettering <lpoetter@redhat.com> 0.9.16-10.test6
- Fix build for ppc

* Mon Aug 24 2009 Lennart Poettering <lpoetter@redhat.com> 0.9.16-9.test6
- New test release

* Thu Aug 20 2009 Matthias Clasen <mclasen@redhat.com> - 0.9.16-7.test5
- Fix install ordering between gdm and pulseaudio-gdm-hooks

* Wed Aug 19 2009 Lennart Poettering <lpoetter@redhat.com> 0.9.16-6.test5
- New test release

* Wed Aug 5 2009 Lennart Poettering <lpoetter@redhat.com> 0.9.16-5.test4
- New test release

* Tue Jul 28 2009 Lennart Poettering <lpoetter@redhat.com> 0.9.16-4.test3
- New test release

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.16-3.test2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 2 2009 Lennart Poettering <lpoetter@redhat.com> 0.9.16-2.test2
- New test release

* Tue Jun 23 2009 Lennart Poettering <lpoetter@redhat.com> 0.9.16-1.test1
- Fix endianess build

* Tue Jun 23 2009 Lennart Poettering <lpoetter@redhat.com> 0.9.16-0.test1
- First 0.9.16 test release

* Wed Apr 22 2009 Warren Togami <wtogami@redhat.com> 0.9.15-11
- Bug #497214
  Do not start pulseaudio daemon if PULSE_SERVER directs pulse elsewhere.

* Mon Apr 13 2009 Lennart Poettering <lpoetter@redhat.com> 0.9.15-10
- Final 0.9.15 release

* Thu Apr 9 2009 Lennart Poettering <lpoetter@redhat.com> 0.9.15-9.test8
- New test release

* Wed Apr 1 2009 Lennart Poettering <lpoetter@redhat.com> 0.9.15-8.test7
- Only load bt modules when installed

* Wed Apr 1 2009 Lennart Poettering <lpoetter@redhat.com> 0.9.15-7.test7
- New test release

* Wed Apr 1 2009 Lennart Poettering <lpoetter@redhat.com> 0.9.15-6.test6
- Fix mistag

* Wed Apr 1 2009 Lennart Poettering <lpoetter@redhat.com> 0.9.15-5.test6
- Fix tarball name

* Wed Apr 1 2009 Lennart Poettering <lpoetter@redhat.com> 0.9.15-4.test6
- New test release

* Thu Mar 5 2009 Lennart Poettering <lpoetter@redhat.com> 0.9.15-3.test5
- New test release

* Thu Mar 5 2009 Lennart Poettering <lpoetter@redhat.com> 0.9.15-3.test4
- New test release

* Fri Feb 27 2009 Lennart Poettering <lpoetter@redhat.com> 0.9.15-3.test3
- Steal patch from git master to fix .so dependencies

* Wed Feb 25 2009 Lennart Poettering <lpoetter@redhat.com> 0.9.15-2.test3
- Add more missing X11 dependencies

* Wed Feb 25 2009 Lennart Poettering <lpoetter@redhat.com> 0.9.15-1.test3
- Add missing dependency on XTEST

* Tue Feb 24 2009 Lennart Poettering <lpoetter@redhat.com> 0.9.15-0.test3
- New test release

* Thu Feb 12 2009 Lennart Poettering <lpoetter@redhat.com> 0.9.15-0.test2
- New test release

* Tue Jan 13 2009 Adel Gadllah <adel.gadllah@gmail.com> 0.9.14-2
- Prefer mixer controls with volumes over switches

* Tue Jan 13 2009 Lennart Poettering <lpoetter@redhat.com> 0.9.14-1
- New release

* Thu Nov 13 2008 Matthias Clasen <mclasen@redhat.com> 0.9.13-7
- Rebuild

* Sat Nov 1 2008 Lennart Poettering <lpoetter@redhat.com> 0.9.13-6
- Backport another two fixes from current git master

* Tue Oct 28 2008 Matthias Clasen <mclasen@redhat.com> 0.9.13-5
- Require new enough speex-devel

* Fri Oct 24 2008 Lennart Poettering <lpoetter@redhat.com> 0.9.13-4
- Backport another fix from current git master

* Thu Oct 23 2008 Lennart Poettering <lpoetter@redhat.com> 0.9.13-3
- Backport a couple of fixes from current git master

* Thu Oct 9 2008 Matthhias Clasen <mclasen@redhat.com> 0.9.13-2
- Handle locales properly

* Mon Oct 6 2008 Lennart Poettering <lpoetter@redhat.com> 0.9.13-1
- New release

* Mon Sep 15 2008 Matthias Clasen <mclasen@redhat.com> 0.9.12-6
- Survive a missing ~/.pulse (#462407)

* Thu Sep 11 2008 - Bastien Nocera <bnocera@redhat.com> 0.9.12-5
- Rebuild

* Tue Sep 9 2008 Lennart Poettering <lpoetter@redhat.com> 0.9.12-4
- Ship /var/lib/pulse in the RPM

* Tue Sep 9 2008 Lennart Poettering <lpoetter@redhat.com> 0.9.12-3
- Don't remove pulse users/groups on package removal

* Tue Sep 9 2008 Lennart Poettering <lpoetter@redhat.com> 0.9.12-2
- Add intltool to deps

* Tue Sep 9 2008 Lennart Poettering <lpoetter@redhat.com> 0.9.12-1
- Release 0.9.12

* Thu Jul 24 2008 Lennart Poettering <lpoetter@redhat.com> 0.9.11-1
- Final release 0.9.11

* Tue Jul 22 2008 Jon McCann <jmccann@redhat.com> 0.9.11-0.7.git20080626
- Fix for CK API changes

* Thu Jun 26 2008 Lennart Poettering <lpoetter@redhat.com> 0.9.11-0.6.git20080626
- New GIT snapshot

* Sun Jun 22 2008 Lennart Poettering <lpoetter@redhat.com> 0.9.11-0.5.svn20080622
- New GIT snapshot

* Wed Jun 18 2008 Lennart Poettering <lpoetter@redhat.com> 0.9.11-0.4.svn20080618
- New SVN snapshot

* Fri May 30 2008 Lennart Poettering <lpoetter@redhat.com> 0.9.11-0.3.svn20080529
- Fix snapshot versioning

* Thu May 29 2008 Lennart Poettering <lpoetter@redhat.com> 0.9.11-0.0.svn20080529
- New SVN snapshot

* Tue May 20 2008 Matthias Clasen <mclasen@redhat.com> 0.9.11-0.2.svn20080516
- Actually apply the patch

* Sat May 17 2008 Matthias Clasen <mclasen@redhat.com> 0.9.11-0.1.svn20080516
- Fix a wrong assertion in module-default-device-restore

* Fri May 16 2008 Matthias Clasen <mclasen@redhat.com> 0.9.11-0.0.svn20080516
- Update to an svn snapshot of the 'glitch-free' rewrite of pulseaudio

* Sun Mar 30 2008 Lennart Poettering <lpoetter@redhat.com> 0.9.10-1
- Update to PulseAudio 0.9.10
- drop all patches, since they have been integrated upstream

* Thu Mar 27 2008 Lubomir Kundrak <lkundrak@redhat.com> 0.9.8-13
- Abort on CPU time comsumption, so we can get core

* Thu Mar 13 2008 Lubomir Kundrak <lkundrak@redhat.com> 0.9.8-12
- Own /usr/libexec/pulse (#437228)

* Wed Mar 12 2008 Adam Jackson <ajax@redhat.com> 0.9.8-11
- pulseaudio-0.9.8-disable-realtime.patch: Don't ask PolicyKit for increased
  scheduling mojo for now.  It's not clear that it's a win; and if it is,
  the policy should just be fixed to always allow it.

* Wed Mar 12 2008 Lubomir Kundrak <lkundrak@redhat.com> 0.9.8-10
- Build the manual pages with xmltoman

* Fri Feb 29 2008 Lubomir Kundrak <lkundrak@redhat.com> 0.9.8-9
- Fix the fix.

* Fri Feb 29 2008 Lubomir Kundrak <lkundrak@redhat.com> 0.9.8-8
- Fix multilib issue (#228383)
- Prevent dumping core if exiting sooner that ltdl initializaion (#427962)

* Thu Feb 21 2008 Adam Tkac <atkac redhat com> 0.9.8-7
- really rebuild against new libcap

* Sun Feb 17 2008 Adam Tkac <atkac redhat com> 0.9.8-6
- rebuild against new libcap

* Wed Jan 23 2008 Lubomir Kundrak <lkundrak@redhat.com> 0.9.8-5
- Fix CVE-2008-0008 security issue (#425481)

* Sun Jan 13 2008 Lubomir Kundrak <lkundrak@redhat.com> 0.9.8-4.1
- Actually add content to pulseaudio-0.9.8-create-dot-pulse.patch
- Make the Source0 tag point to URL instead of a local file
- Drop the nochown patch; it's not applied at all and no longer needed

* Thu Nov 29 2007 Lennart Poettering <lpoetter@redhat.com> 0.9.8-4
- add missing dependency on pulseaudio-utils for pulseaudio-module-x11

* Thu Nov 29 2007 Lennart Poettering <lpoetter@redhat.com> 0.9.8-3
- Create ~/.pulse/ if not existant

* Thu Nov 29 2007 Lennart Poettering <lpoetter@redhat.com> 0.9.8-2
- Add missing dependency on jack-audio-connection-kit-devel

* Wed Nov 28 2007 Lennart Poettering <lpoetter@redhat.com> 0.9.8-1
- Upgrade to current upstream

* Wed Oct 17 2007 Lennart Poettering <lpoetter@redhat.com> 0.9.7-0.16.svn20071017
- Another SVN snapshot, fixing another round of bugs (#330541)
- Split libpulscore into a seperate package to work around multilib limitation (#335011)

* Mon Oct 1 2007 Lennart Poettering <lpoetter@redhat.com> 0.9.7-0.15.svn20071001
- Another SVN snapshot, fixing another round of bugs

* Sat Sep 29 2007 Lennart Poettering <lpoetter@redhat.com> 0.9.7-0.14.svn20070929
- Another SVN snapshot, fixing a couple of subtle bugs

* Tue Sep 25 2007 Lennart Poettering <lpoetter@redhat.com> 0.9.7-0.13.svn20070925
- Remove libpulsecore.so symlink from pulseaudio-libs-devel to avoid multilib issues

* Tue Sep 25 2007 Lennart Poettering <lpoetter@redhat.com> 0.9.7-0.12.svn20070925
- New SVN snapshot
- Split off libflashsupport again
- Rename "-lib" packages to "-libs", like all other packages do it.
- Provide esound

* Fri Sep 7 2007 Lennart Poettering <lpoetter@redhat.com> 0.9.7-0.11.svn20070907
- Update SVN snapshot, don't link libpulsecore.so statically anymore

* Wed Sep 5 2007 Lennart Poettering <lpoetter@redhat.com> 0.9.7-0.10.svn20070905
- Update SVN snapshot

* Tue Sep 4 2007 Lennart Poettering <lpoetter@redhat.com> 0.9.7-0.9.svn20070904
- Update SVN snapshot
- ship libflashsupport in our package
- drop pulseaudio-devel since libpulsecore is not linked statically

* Thu Aug 23 2007 Lennart Poettering <lpoetter@redhat.com> 0.9.7-0.8.svn20070823
- Update SVN snapshot

* Thu Aug 16 2007 Lennart Poettering <lpoetter@redhat.com> 0.9.7-0.7.svn20070816
- Update SVN snapshot

* Thu Aug 16 2007 Lennart Poettering <lpoetter@redhat.com> 0.9.7-0.6.svn20070816
- Update SVN snapshot

* Tue Aug 14 2007 Lennart Poettering <lpoetter@redhat.com> 0.9.7-0.5.svn20070814
- Forgot to upload tarball

* Tue Aug 14 2007 Lennart Poettering <lpoetter@redhat.com> 0.9.7-0.4.svn20070814
- Update snapshot. Install file into /etc/xdg/autostart/ to load module-x11-smp
  only after login

* Sun Aug 12 2007 Lennart Poettering <lpoetter@redhat.com> 0.9.7-0.3.svn20070812
- Depend on tcp_wrappers-devel instead of tcp_wrappers, to make sure we
  actually get the headers installed.

* Sun Aug 12 2007 Lennart Poettering <lpoetter@redhat.com> 0.9.7-0.2.svn20070812
- Update snapshot, contains 64 bit build fixes, and disables module-x11-xsmp by
  default to avoid deadlock when PA is started from gnome-session

* Sun Aug 12 2007 Lennart Poettering <lpoetter@redhat.com> 0.9.7-0.1.svn20070812
- Take snapshot from SVN

* Tue May 29 2007 Pierre Ossman <drzeus@drzeus.cx> 0.9.6-2
- Add libatomic_ops-devel as a build requirement.

* Tue May 29 2007 Pierre Ossman <drzeus@drzeus.cx> 0.9.6-1
- Upgrade to 0.9.6.

* Fri Mar  2 2007 Pierre Ossman <drzeus@drzeus.cx> 0.9.5-5
- Fix merge problems with patch.

* Fri Mar  2 2007 Pierre Ossman <drzeus@drzeus.cx> 0.9.5-4
- Add patch to handle ALSA changing the frame size (bug 230211).
- Add patch for suspended ALSA devices (bug 228205).

* Mon Feb  5 2007 Pierre Ossman <drzeus@drzeus.cx> 0.9.5-3
- Add esound-compat subpackage that allows PulseAudio to be a drop-in
  replacement for esd (based on patch by Matthias Clasen).
- Backport patch allows startup to continue even when the users'
  config cannot be read.

* Mon Oct 23 2006 Pierre Ossman <drzeus@drzeus.cx> 0.9.5-2
- Create user and groups for daemon.

* Mon Aug 28 2006 Pierre Ossman <drzeus@drzeus.cx> 0.9.5-1
- Upgrade to 0.9.5.

* Wed Aug 23 2006 Pierre Ossman <drzeus@drzeus.cx> 0.9.4-3
- Make sure JACK modules are built and packaged.

* Tue Aug 22 2006 Pierre Ossman <drzeus@drzeus.cx> 0.9.4-2
- Merge the ALSA modules into the main package as ALSA is the
  standard API.

* Sun Aug 20 2006 Pierre Ossman <drzeus@drzeus.cx> 0.9.4-1
- Update to 0.9.4.
- Remove fix for rpath as it is merged upstream.

* Fri Jul 21 2006 Toshio Kuratomi <toshio@tiki-lounge.com> 0.9.3-2
- Remove static libraries.
- Fix for rpath issues.

* Fri Jul 21 2006 Pierre Ossman <drzeus@drzeus.cx> 0.9.3-1
- Update to 0.9.3
- GLib 1.2 bindings dropped.
- Howl compat dropped as Avahi is supported natively.
- Added fix for pc files on x86_64.

* Sat Jul  8 2006 Pierre Ossman <drzeus@drzeus.cx> 0.9.2-1
- Update to 0.9.2.
- Added Avahi HOWL compat dependencies.

* Thu Jun  8 2006 Pierre Ossman <drzeus@drzeus.cx> 0.9.1-1
- Update to 0.9.1.

* Mon May 29 2006 Pierre Ossman <drzeus@drzeus.cx> 0.9.0-2
- Build and package doxygen docs
- Call ldconfig for relevant subpackages.

* Mon May 29 2006 Pierre Ossman <drzeus@drzeus.cx> 0.9.0-1
- Update to 0.9.0

* Tue May  9 2006 Pierre Ossman <drzeus@drzeus.cx> 0.8.1-1
- Update to 0.8.1
- Split into more packages
- Remove the modules' static libs as those shouldn't be used (they shouldn't
  even be installed)

* Fri Feb 24 2006 Tom "spot" Callaway <tcallawa@redhat.com> 0.7-2
- dance around with perms so we don't strip the binary
- add missing BR

* Mon Nov 28 2005 Tom "spot" Callaway <tcallawa@redhat.com> 0.7-1
- Initial package for Fedora Extras
