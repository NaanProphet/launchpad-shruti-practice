#!/bin/sh

###
### Mac bottler script for Scala (http://www.huygens-fokker.org/scala/) 
### Tested on Mac OS X 10.14 Mojave
### @NaanProphet, github
###
### This script will download and bundle Scala.app in the same folder as this script.
### Usage: sh bundle-scala.sh
###
### Dependencies will be installed if not present:
### - Homebrew (https://brew.sh)
### - XQuartz
### - Wine
### - wine-bundler (https://github.com/sormy/wine-bundler)
###
### Note: the actual Scala download site only indicates the version in the webpage 
### text, not in the filename. This script will need to be updated when versions are 
### released, as the checksum will fail. The checksum is not present on the download
### page and must be calculated manually. Oh, currently the website is only HTTP...🧐
###

# leave blank for OFF
DEBUG=
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
TEMP_DIR="${DIR}/temp"
RESOURCE_DIR="${DIR}/resources"

SCALA_DOWNLOAD_FILE="Scala_Portable_Win32.zip"
SCALA_DOWNLOAD="http://www.huygens-fokker.org/software/${SCALA_DOWNLOAD_FILE}"
SCALA_UNZIP_FOLDER_NAME="Scala22"
SCALA_SHA256=88b9d1809f72f66c479a87f13afb553229595a6b79ace22ba60321f5a6f8120d
SCALA_VERSION='2.44p'

# although the Scala22 app is 32bit, use a 64bit wine bottle for less bugs
WIN_ARCH=win64
WINE_PREFIX_DIR="${TEMP_DIR}/prefixtmp"
WINE_BUNDLER_APP="wine-bundler"
WINE_BUNDLER_DOWNLOAD="https://raw.githubusercontent.com/sormy/wine-bundler/master/${WINE_BUNDLER_APP}"
WINE_PROGRAM_FILES_FOLDER="${WINE_PREFIX_DIR}/drive_c/Program Files (x86)/"
SCALA_WIN_EXE_PATH="c:\Program Files (x86)\Scala22\scala.exe"
SCALA_ICON="${RESOURCE_DIR}/Scala-Icon.icns"
SCALA_PLIST="${TEMP_DIR}/Scala.app/Contents/Info.plist"

# check/update required dependencies
if [[ $(command -v brew) == "" ]]; then
    echo "Installing Homebrew"
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
fi
brew bundle

rm -rf ${TEMP_DIR}
mkdir -p ${TEMP_DIR}
cd ${TEMP_DIR}

# attempt to get latest
wget -q "${SCALA_DOWNLOAD}"
shasum -a 256 -c -s <<< "${SCALA_SHA256} *${SCALA_DOWNLOAD_FILE}"
if [ $? != 0 ]; then
  echo "\033[1;31mScala version has changed!"
  echo "Please update checksum and version in script (run in DEBUG mode)."
  echo "http://www.huygens-fokker.org/scala/downloads.html"
  echo "\033[1;33mProceeding with older version ${SCALA_VERSION}...\033[0m"
  cp "${RESOURCE_DIR}/${SCALA_DOWNLOAD_FILE}" ${TEMP_DIR}
fi

# create intial prefix (windows base image)
# all defaults are fine - use wineboot instead of winecfg for no GUI
WINEARCH=${WIN_ARCH} WINEPREFIX="${WINE_PREFIX_DIR}" WINEDEBUG=-all wineboot

# creates a folder called Scala22
unzip -q "${SCALA_DOWNLOAD_FILE}"
if [ ! -f "${SCALA_UNZIP_FOLDER_NAME}/scala.exe" ]; then
  echo "Scale zip file has changed! Cannot find file "${SCALA_UNZIP_FOLDER_NAME}/scala.exe" from unzip."
  exit 1
fi
mv "${SCALA_UNZIP_FOLDER_NAME}" "${WINE_PROGRAM_FILES_FOLDER}"

# bottle up Mac App
wget -q "${WINE_BUNDLER_DOWNLOAD}"
sh ${WINE_BUNDLER_APP} \
  -i "${SCALA_ICON}" \
  -n "Scala" \
  -a ${WIN_ARCH} \
  -p "${WINE_PREFIX_DIR}" \
  -s "${SCALA_WIN_EXE_PATH}" \
  -w "stable-4.0.2-osx64"
# latest 5.0 bundle 64bit is a little over 2 GB whereas v4 is around 1 GB, YMMV
# https://dl.winehq.org/wine-builds/macosx/pool/

plutil -remove CFBundleGetInfoString "${SCALA_PLIST}"
plutil -insert CFBundleGetInfoString -string "${SCALA_VERSION}" "${SCALA_PLIST}"
plutil -insert CFBundleShortVersionString -string "${SCALA_VERSION}" "${SCALA_PLIST}"
plutil -insert NSHumanReadableCopyright -string 'Copyright E.F. Op de Coul, the Netherlands, 1992-2020' "${SCALA_PLIST}"

rm -rf "${DIR}/Scala.app"
mv -f "${TEMP_DIR}/Scala.app" "${DIR}"
if [ -z $DEBUG ]; then
	rm -rf ${TEMP_DIR}
fi
echo "👋🏾"
