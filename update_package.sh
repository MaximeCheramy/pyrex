#!/bin/bash
## Copier le dossier python de git dans le même répertoire! ##

echo "entrez la version exacte du paquet"
read version

## Creation de la base du paquet si ça n'existe pas
if [ ! -d pyRex ]; then
    mkdir -p pyRex/DEBIAN/
    mkdir -p pyRex/usr/share/pyrex/
    mkdir -p pyRex/usr/bin/
    cat > pyRex/usr/bin/pyrex << EOF
#!/bin/sh
exec python /usr/share/pyrex/pyrex.py
EOF
    cat > pyRex/DEBIAN/prerm << EOF
sudo rm -rf /usr/share/pyrex/
sudo rm /usr/bin/pyrex
EOF
    chmod +x pyRex/usr/bin/pyrex
fi

## On balance les infos dans le paquet
cd pyRex
cp -r ../pyrex/* usr/share/pyrex/
rm usr/share/pyrex/*.pyc usr/share/pyrex/*~ usr/share/pyrex/gui/*.pyc usr/share/pyrex/gui/*~
cat > DEBIAN/control << EOF
Package: pyrex
Version: $version
Section: Python
Priority: optional
Architecture: all
Depends: python (>= 2.7), python (<< 2.8), python-qt4 (>= 4.7), rex
Maintainer: J. SIVADIER <sivadier@etud.insa-toulouse.fr> and M. CHERAMY <mcheramy@etud.insa-toulouse.fr>
Homepage: http://etud.insa-toulouse.fr/~rex
Description: Client FTP pour les étudiants de l'INSA de Toulouse codé en python. Compatible avec Rex Daemon.
EOF
find usr -exec md5sum {} + > DEBIAN/md5sums
chmod 755 DEBIAN/*

## On compile
cd ../
dpkg-deb --build pyRex

## On change le nom
mv pyRex.deb pyRex_$version.deb
