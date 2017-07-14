#!/bin/bash
# скрипт предназначен только для деплоя на animals-stage. не стоит его использовать где либо еще.

# устанавливаем среду исполнения кода в STAGE
export ENVIRONMENT=STAGE

# Подготовим окружение для конфига
export DATABASE_NAME=${DATABASE_NAME}
export DATABASE_USER=${DATABASE_USER}
export DATABASE_PASSWORD=${DATABASE_PASSWORD}
export DATABASE_HOST=${DATABASE_HOST}
export DATABASE_PORT=${DATABASE_PORT}


export DEPLOY_PATH=/local/karbidsoft/web/animals_stage
export VENV_PATH=/local/karbidsoft/venv/animals_py3_stage
revision=`git describe`

# подготовим вирутальное окружение для проекта
rm -fr ${VENV_PATH}
virtualenv -p python3 ${VENV_PATH}
source ${VENV_PATH}/bin/activate

mkdir -p ${DEPLOY_PATH}/releases

#копируем
rsync -au --exclude ".git" ./* ${DEPLOY_PATH}/releases/${CI_COMMIT_REF_NAME}


# переходим в папку и делаем всякое
cd ${DEPLOY_PATH}/releases/${CI_COMMIT_REF_NAME}
# установим зависимости проекта
pip3 install -r requiriments.txt
# очистим базу данных, накатим миграции и создадим супер пользователя
python3 manage.py flush --noinput --no-initial-data
python3 manage.py makemigrations
python3 manage.py migrate
echo "from django.contrib.auth.models import User; User.objects.create_superuser('${SUPERUSER_LOGIN}', '${SUPERUSER_EMAIL}', '${SUPERUSER_PASSWORD}')" | python3 manage.py shell

# сделаем симлинк на текущую дерикторию
rm ${DEPLOY_PATH}/current
ln -s ${DEPLOY_PATH}/releases/${CI_COMMIT_REF_NAME} ${DEPLOY_PATH}/current
cd ${DEPLOY_PATH}/current
