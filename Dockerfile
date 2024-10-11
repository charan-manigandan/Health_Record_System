FROM python:3.11

WORKDIR /secured_health_record_system

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Creating and setting up permisisons for media dir
RUN mkdir -p /secured_health_record_system/media && chmod -R 755 /secured_health_record_system/media

COPY cmds.sh /cmds.sh
RUN chmod +x /cmds.sh

EXPOSE 8000

CMD ["/start.sh"]
