## create the app by
```
$ mkdir react-app
$ cd react-app
$ docker run -it --rm -v "$PWD":/usr/src -w /usr/src -p "3000:3000" node /bin/bash

> root@4b15ab7dbf21:/usr/src# npx create-react-app . --template typescript
```