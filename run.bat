py -c "" >> NUL
if ERRORLEVEL == 1
(
    echo "Charmed requires Python 3 to run, but it isn't installed. Install it from python.org."
set /p NUL=""
    goto eof
)
set pynputInstalled=python3 -c 'import pkgutil; exit(pkgutil.find_loader("pynput"))'
if NOT %pynputInstalled%
(
    set /p install="This game required the pynput package to run. Install it? (y/n) "
    if %install%=="y"
    (
        echo "Running pip to install pynput:"
        py -m pip install pynput
        echo "Done."
    )
    else
    (
        goto eof
    )
)
py main.py
set /p NUL=""