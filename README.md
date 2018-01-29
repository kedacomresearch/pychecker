# pychecker: stream check python utils

## set environment
```
set GST_PLUGIN_PATH=C:\cerbero\x86_64\bin;C:\cerbero\x86_64\lib\gstreamer-1.0;C:\cerbero\x86_64\lib\gstreamer-1.0\validate

set PATH=C:\cerbero\x86_64\bin;C:\cerbero\x86_64\lib\gstreamer-1.0;%PATH%
```

## install
```
python setup.py install --record record.txt
```

## test
```
cd test && python test.py
```

## uninstall
```shell
# windows
FOR /F "delims=" %f in (record.txt) DO del "%f"

# linux
cat files.txt | xargs rm -rf
```

