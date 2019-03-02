### setup your ~/.pypirc file
```
index-servers =
    pypi
    testpypi

[pypi]
repository: https://upload.pypi.org/legacy/
username: <your username>
password: <your password>

[testpypi]
repository: https://test.pypi.org/legacy/
username: <your username>
password: <your password>
```

### Make sure that you have properly incremented the version
this can be done by modifying the __version__ variable in version_info.py

### if you have previously pushed to pypi
```
rm dist/*
```

### create the necessary dists using setup.py, this will put the wheel and source in dist/
```
python setup.py sdist bdist_wheel
```

### ensure twine is installed
```
pip install twine
```

### push to pypi
```
twine upload dist/*
```
