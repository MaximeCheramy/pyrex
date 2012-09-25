#!/bin/bash
## Copier le dossier python de git dans le même répertoire! ##

echo "entrez la version exacte du paquet"
read version

## Creation de la base du paquet si ça n'existe pas
if [ ! -d pyRex ]; then
    mkdir -p pyRex/DEBIAN/
    mkdir -p pyRex/usr/share/pyrex/
    mkdir -p pyRex/usr/bin/
    echo "#!/bin/sh
exec python /usr/share/pyrex/pyrex.py " > pyRex/usr/bin/pyrex
    echo '#!/bin/bash
sudo rm -r /usr/share/pyrex
sudo rm /usr/bin/pyrex' > pyRex/DEBIAN/prerm
    chmod 755 pyRex/DEBIAN/*
fi

## On balance les infos dans le paquet
cd pyRex
cp -r ../pyrex/* usr/share/pyrex/
rm usr/share/pyrex/*.pyc usr/share/pyrex/*~ usr/share/pyrex/gui/*.pyc usr/share/pyrex/gui/*~
echo "Package: pyrex
Version: "$version"
Section: Python
Priority: optional
Architecture: all
Depends: bash, python (= 2.7), python-qt4 (>= 4.7), rex
Maintainer: J. SIVADIER <sivadier@etud.insa-toulouse.fr> and M. CHERAMY <mcheramy@etud.insa-toulouse.fr>
Homepage: http://etud.insa-toulouse.fr/~rex
Description: Client FTP pour les étudiants de l'INSA de Toulouse codé en python. Successeur de Rex." > DEBIAN/control
find usr -exec md5sum {} + > DEBIAN/md5sums

## On compile
cd ../
dpkg-deb --build pyRex

## On change le nom
mv pyRex.deb pyRex_$version.deb
