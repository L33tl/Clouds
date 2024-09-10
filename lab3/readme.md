# Third Lab

## Разберем возможные ошибки на примере `workflow` файла `github-actions`

## 1 Отрытое хранение секретов

### Как делать плохо:
```yml
name: Clouds Lab3 Workflow

on: [ commit ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy
        run: ssh user@server "deploy-script.sh"
        env:
          DB_PASSWORD: "secretgiraffe"
```

### Как надо:
```yml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy
        run: ssh user@server "deploy-script.sh"
        env:
          DB_PASSWORD: ${{ secrets.DB_PASSWORD }}
```

Так секрет хранится в безопасном хранилище - `Github Secrets`


## 2 Заупск независимых `pipeline`'ов последовательно

### Как делать плохо:
```yml
jobs:
  all_tests:
    runs-on: ubuntu-latest
    steps:
      - name: Unit tests
        run: ./build.sh
      - name: Integration tests
        run: ./integration-tests.sh
```

### Как надо:
```yml
jobs:
  unit_tests:
    runs-on: ubuntu-latest
    steps:
      - name: Unit tests
        run: ./build.sh
  integration_test:
    runs-on: ubuntu-latest
    steps:
      - name: Integration tests
        run: ./integration-tests.sh  
```

Это ускорит работу `CI`


## 3 *Хардкод* ссылок, названий файлов и версий

### Как делать плохо:
```yml
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Install Node.js
        run: curl -sL https://deb.nodesource.com/setup_13.x | sudo -E bash -
      - name: Install dependencies
        run: npm install
```

### Как надо:
```yml
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Install Node.js
        run: curl -sL https://deb.nodesource.com/setup_${{ env.NODE_VERSION }}.x | sudo -E bash -
      - name: Install dependencies
        run: npm install
```

Это позволит сохранять актульные и *одинаковые* версии инструментов во всём проекте

## 4 Пренебрижение кешированием
К предыдущему варианту можно добавить кеширование установки зависимостей

Заменим:
```yml
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Install dependencies
        run: npm install
```

На:
```yml
  build:
    runs-on: ubuntu-latest
    steps:
    - name: Cache node dependencies installation
      uses: actions/cache@v2
      with:
        path: node_modules
        key: ${{ runner.os }}-node-${{ hashFiles('package-lock.json') }}
        restore-keys: |
          ${{ runner.os }}-node-
    - name: Install dependencies
      run: npm install
```

Теперь если установочные пакеты не изменились, будет использована закешированная версия

## 5 Большой нагруженный `pipeline`

### Как делать плохо:
```yml
  huge_pipeline:
    runs-on: ubuntu-latest
    steps:
      - name: Build
        run: ./build.sh
      - name: Unit tests
        run: ./unit-tests.sh
      - name: Integration tests
        run: ./integration-tests.sh
      - name: Deploy
        run: ./deploy.sh
```

### Как надо:
```yml
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Build
        run: ./build.sh

  unit_tests:
    runs-on: ubuntu-latest
    steps:
    - name: Unit tests
      run: ./unit-tests.sh

  integration_tests:
    runs-on: ubuntu-latest
    steps:
      - name: Integration tests
        run: ./integration-tests.sh

  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy
        run: ./deploy.sh
```

Большой `pipeline` будет долго исполняться, если разбить его на несколько более мелких, иожно будет настроить условия запуска каждого из них, что ускорит процесс `CI/CD`


# ⭐

