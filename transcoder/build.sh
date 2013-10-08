
#---------
# Goal
#
# Build a static binary of FFMPEG for transcoding my video
#----------

# Install Build Tools:
sudo apt-get install autoconf automake build-essential git libass-dev libgpac-dev libtool pkg-config texi2html zlib1g-dev libmp3lame-dev


# TODO, i might need to modify the path to make these work?...

BUILD_OUTPUT = "$PWD/output"
BUILD_BIN = "$BUILD_OUTPUT/bin"
mkdir $BUILD_OUTPUT
mkdir $BUILD_BIN

#-------
# YASM
#-------

cd $BUILD_OUTPUT
wget http://www.tortall.net/projects/yasm/releases/yasm-1.2.0.tar.gz
tar xzvf yasm-1.2.0.tar.gz
cd yasm*
./configure --prefix="$BUILD_OUTPUT" --bindir=$BUILD_BIN
make
make install


#-----------
# x264
#-----------

cd $BUILD_OUTPUT
git clone --depth 1 git://git.videolan.org/x264.git
cd x264*
./configure --prefix="$BUILD_OUTPUT"  --enable-static --bindir=$BUILD_BIN
make
make install


#-------------
# FDK-AAC
#------------

cd $BUILD_OUTPUT
git clone --depth 1 git://github.com/mstorsjo/fdk-aac.git
cd fdk-aac
autoreconf -fiv
./configure --prefix="$BUILD_OUTPUT" --disable-shared
make
make install

#--------------
# Lib Opus
#-------------

cd $BUILD_OUTPUT
wget http://downloads.xiph.org/releases/opus/opus-1.0.3.tar.gz
tar xzvf opus-1.0.3.tar.gz
cd opus-1.0.3
./configure --prefix="$BUILD_OUTPUT" --disable-shared
make
make install


#------------
# Lib VPx
#-----------
cd $BUILD_OUTPUT
git clone --depth 1 http://git.chromium.org/webm/libvpx.git
cd libvpx
./configure --prefix="$BUILD_OUTPUT" --disable-examples
make
make install


#-------------
# FFMPEG
#------------

cd $BUILD_OUTPUT
git clone --depth 1 git://source.ffmpeg.org/ffmpeg
cd ffmpeg
#PKG_CONFIG_PATH="$HOME/ffmpeg_build/lib/pkgconfig"
#export PKG_CONFIG_PATH
./configure --prefix="$BUILD_OUTPUT" --extra-cflags="-I$BUILD_OUTPUT/include" --extra-ldflags="-L$BUILD_OUTPUT/lib" --bindir="$BUILD_BIN" --extra-libs="-ldl" --enable-gpl --enable-libass --enable-libfdk-aac --enable-libmp3lame --enable-libopus --enable-libvpx --enable-libx264 --enable-nonfree 
make
make install


