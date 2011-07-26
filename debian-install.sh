#!/bin/sh

export LC_ALL=C


# track return code
rc=0

# save current path
CURRENT_PATH=`pwd`

# check if ubuntu (:sudo) or debian (:su) is running
/usr/bin/lsb_release -i|/bin/grep "Ubuntu" && PRIV="/usr/bin/sudo /bin/sh -c"
/usr/bin/lsb_release -i|/bin/grep "Debian" && PRIV="/bin/su root -c"

install_deps() {
	# install dist deps
	DEPS="libpoppler-qt4-dev pyqt4-dev-tools python-qt4-dev python-sip-dev"
	# check if packages are already installed
	STATUS=`/usr/bin/dpkg-query -W -f='${Status}\n' $DEPS 2>&1| /bin/grep -v "^install ok" | /usr/bin/wc -l`
	if [ 0 -ne $STATUS ]
	then
		echo "Installing required packages"
		# install required packages
		$PRIV "/usr/bin/aptitude install $DEPS"
		rc=`expr $rc + $?`
	fi

	# install pypoppler-qt4
	/usr/bin/wget http://pyqt4-extrawidgets.googlecode.com/files/pypoppler-qt4-20962-fixed.tar.gz
	/bin/tar xvzf pypoppler-qt4-20962-fixed.tar.gz 
	/bin/rm -f pypoppler-qt4-20962-fixed.tar.gz
	cd pypoppler-qt4
	echo "Configuring pypoppler-qt4 ..."
	/usr/bin/python configure.py
	/usr/bin/make
	rc=`expr $rc + $?`
	echo "Installing pypoppler-qt4 ..."
	$PRIV "/usr/bin/make install"
	rc=`expr $rc + $?`
	# goto initial path
	cd $CURRENT_PATH
}

# install dependencies
install_deps

# prepare start of pdfpresenter.py
/bin/chmod +x pdfpresenter.py

# --help
echo "[x] DONE

Usage:
1. Run: ./pdfpresenter.py
2. Focus on black window
3. Press 'o' to open a file
4. Move presentation view to projector/external display
5. Press 'f' to enter fullscreen mode
6. Wait for caching to finish
7. Use right/left arrow keys to go to next/previous slide"

exit $rc
