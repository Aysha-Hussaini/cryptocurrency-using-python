**Activate the virtual environment**

```
source blockchain-env/Scripts/activate
```

**Install all packages**
```
pip3 install -r requirements.txt
```

**Run the tests**

Make sure to activate the virtual environment

```
python -m pytest Backend\tests\test_crypto_hash.py
```