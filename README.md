## 說明
不需資料庫之對話腳本代理。


## pip.sh

```
指令推新版本
```

## unittest

```
pip install -e .
python3 -m unittest __tests__/*.py
```

## unittest - coverage
```
pip install pytest-cov
python3 -m pytest  __tests__/*.py --cov=ConversationAgent
```

## set env
```
# python 3.10
python3 -m venv .venv && source .venv/bin/activate
```

## delete env
```
rm -r .venv && \
rm -r __tests__/__pycache__ && \
rm -r ConversationAgent.egg-info
```