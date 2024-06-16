# Esta documentacion solo esta aqui para nuestros yo futuros

# Importar en MariaDB
mysql -u root -p
CREATE DATABASE nueva_bbdd;
mysql -u nombre_usuario -p nueva_bbdd < nombre_archivo_dump.sql

# Exportar en MariaDB
mysqldump -u nombre_usuario -p nueva_bbdd > nombre_archivo_dump.sql

# Fix for MySQL in MariaDB
sed -i 's/utf8mb4_0900_ai_ci/utf8_general_ci/g' games_backup.sql  
sed -i 's/CHARSET=utf8mb4/CHARSET=utf8/g' games_backup.sql 

# Crons para  hacer backups de la base de datos

```bash
# Backup cron. Each 24h
# RUN echo '* * * * * /bin/sh -c "mysqldump --no-tablespaces -u root -p12345678 games > /var/lib/mysql/gamomagic_backup.sql"' > /var/spool/cron/crontabs/root

# Start cron server
# CMD ["/bin/sh", "-c", "crond && /usr/bin/mysqld --user=root --console"]
```