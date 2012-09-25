#!/bin/bash
## Copier le dossier python de git dans le même répertoire! ##

echo "entrez la version exacte du paquet"
read version

# Mémorise le répertoire courant
pushd .

## Creation de la base du paquet si ça n'existe pas
if [ ! -d dist ]; then
    mkdir -p dist/DEBIAN/
    mkdir -p dist/usr/share/pyrex/
    mkdir -p dist/usr/bin/
    cat > dist/usr/bin/pyrex << EOF
#!/bin/sh
cd /usr/share/pyrex/
exec python pyrex.py
EOF
    chmod +x dist/usr/bin/pyrex
fi

## On balance les infos dans le paquet
cd dist
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
popd
fakeroot dpkg-deb --build dist

## On change le nom
mv dist.deb pyrex_$version.deb
