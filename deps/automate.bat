@echo off

echo --Step 1--
echo Upgrading `pip`...
python -m pip install --upgrade pip

echo --Step 2--
echo Installing `deps`...
pip install pipreqs
pip install -r ./python/requirements.txt

echo --Step 3--
echo Writing `deps`...
ping -n 3 localhost >nul
pipreqs . --force --encoding=utf-8 --ignore tests --savepath ./python/requirements.txt

echo --Step 4--
echo Done performing `dep` jobs!
echo Ending...

pause
