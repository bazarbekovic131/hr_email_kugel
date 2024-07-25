Шаги по установке этого компонента:

1) Скопировать это приложение

2) set environment:

### Database Settings
DBNAME = 'hr'
DBHOST = 'localhost'
DBUSER = ''
DBPASSWORD = ''
DBPORT = '5432'


### EMAIL Settings

EMAIL_HOST = ''
EMAIL_PORT = 465
EMAIL_USER = ''
EMAIL_PASSWORD = ''

3) Установить модули:

```bash
pip install schedule python-dotenv psycopg2-binary pandas
```

4) Copy the service app

5) run these commands:

```bash
sudo ln -s /home/$user/hr_email_kugel/hrkugel.service /etc/systemd/system/hrkugel.service
systemctl daemon-reload
systemctl enable hrkugel
systemctl start hrkugel
```