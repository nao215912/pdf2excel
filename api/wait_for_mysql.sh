#!/bin/.sh
# MySQLサーバーが起動するまでループで待機する

until nc -z db 3306; do
  >&2 echo "mysql is unavailable - sleeping"
  sleep 3
done