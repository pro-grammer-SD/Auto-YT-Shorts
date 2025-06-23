@echo off

echo Only Python `deps` will be installed!

echo --Step 1--
echo Upgrading `pip`...
python -m pip install --upgrade pip
echo Upgraded `pip`!

echo --Step 2--
echo Installing `deps`...
pip install pipreqs
pip install -r ./python/requirements.txt
echo Installing `deps` done!

echo --Step 3--
echo Writing `deps`...
ping -n 3 localhost >nul
pipreqs . --force --encoding=utf-8 --ignore tests --savepath ./python/requirements.txt
echo Writing `deps` Done!

echo --Step 4--
echo Done performing `dep` jobs!
echo Ending...

pause
