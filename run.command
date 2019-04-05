command -v python3 >/dev/null 2>&1 || { echo >&2 "Charmed requires Python 3 to run, but it isn't installed. Install it from python.org."; exit 1; }

if python3 -c 'import pkgutil; exit(pkgutil.find_loader("pynput"))'; then
    echo This game requires the pynput package to run. Install it? \(y/n\)
    read answer
    if [ "$answer" = 'y' ]; then
        echo Running pip to install pynput:
        python3 -m pip install pynput
        echo Done.
    else
        exit
    fi
fi
cd "$(dirname "$0")"
python3 main.py
read
