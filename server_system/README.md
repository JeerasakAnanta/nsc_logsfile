```bash
uv run python logforwarder.py \
  --log-file /var/log/apache2/access.log \
  --endpoint http://localhost:5000/api/logs
```