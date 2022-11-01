# Nginx Configuration

## Configure Nginx

```
sudo rm /etc/nginx/sites-enabled/default

sudo nano /etc/nginx/sites-enabled/vulnscanner
```

#### Nginx Config Template

```
server {
    listen 80;
    server_name ip_address;
    
    location /api/v1 {
        alias /home/{$username}/path/to/project
    }
    
    location / {
        proxy_pass http://localhost:8000;
        include /etc/nginx/proxy_params;
        proxy_redirect off;
    }
}
```
