## 說明
不需資料庫之對話腳本代理。


## pip.sh

```
指令推新版本
```

## unittest

```
pip install -r requirements.txt
python3 -m unittest __tests_pkg__/*.py
```

## unittest - coverage
```
pip install pytest-cov
python3 -m pytest  __tests__/*.py --cov=ConversationAgent
```

## set env
```cd
# python 3.10
python3 -m venv .venv && source .venv/bin/activate
```

## delete env
```
rm -r .venv && \
rm -r __tests__/__pycache__ && \
rm -r ConversationAgent.egg-info
```
##docker run -it -v "$PWD":/usr/src -w /usr/src -p "3000:3000" teracy/create-react-app /bin/bash
### TODO
- swagger can't access backend api
- github-action need fix.
- frontend should rebuild with react.js
- update the readme.md
 