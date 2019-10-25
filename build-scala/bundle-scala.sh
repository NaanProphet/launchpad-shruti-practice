#!/bin/sh

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
SCALA_EXE_NAME="Scala_Setup.exe"
SCALA_DOWNLOAD="http://www.huygens-fokker.org/software/${SCALA_EXE_NAME}"
SCALA_SHA256=d7cb4c94f5927c266fd1c4ad38490a992a9083cbc476e87fa86d14fad83daba1
GTK_EXE_NAME="gtk2-runtime-2.24.10-2012-10-10-ash.exe"
GTK_DOWNLOAD="http://downloads.sourceforge.net/gtk-win/${GTK_EXE_NAME}"
GTK_SHA1=afd74fbc35743a5528f07f21837978e10c078965
WINE_PREFIX_DIR="${DIR}/prefixtmp"
SCALA_ICON="${DIR}/Scala-Icon.icns"
WINE_BUNDLER_APP="wine-bundler"
WINE_BUNDLER_DOWNLOAD="https://raw.githubusercontent.com/sormy/wine-bundler/master/${WINE_BUNDLER_APP}"
SCALA_WIN_PATH="c:\Program Files (x86)\Scala22\scala.exe"
WIN_ARCH=win64


brew cask install xquartz
brew install wine


wget "${SCALA_DOWNLOAD}"
shasum -a 256 -c <<< "${SCALA_SHA256} *${SCALA_EXE_NAME}"
if [ $? != 0 ]; then
  exit 1
fi

wget "${GTK_DOWNLOAD}"
shasum -c <<< "${GTK_SHA1} *${GTK_EXE_NAME}"
if [ $? != 0 ]; then
  exit 1
fi

# manually select OK
winearch=${WIN_ARCH} WINEPREFIX="${WINE_PREFIX_DIR}" winecfg

# select next and accept all defaults
winearch=${WIN_ARCH} WINEPREFIX="${WINE_PREFIX_DIR}" wine "${GTK_EXE_NAME}"

# select next and accept all defaults, need not open megamid
winearch=${WIN_ARCH} WINEPREFIX="${WINE_PREFIX_DIR}" wine "${SCALA_EXE_NAME}"

wget "${WINE_BUNDLER_DOWNLOAD}"

sh ${WINE_BUNDLER_APP} \
  -i "${SCALA_ICON}" \
  -n "Scala" \
  -a ${WIN_ARCH} \
  -p "${WINE_PREFIX_DIR}" \
  -s "${SCALA_WIN_PATH}"

# cleanup
rm "${SCALA_EXE_NAME}" "${GTK_EXE_NAME}"
rm -rf "${WINE_PREFIX_DIR}"
rm "${WINE_BUNDLER_APP}"
