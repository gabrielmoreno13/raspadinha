module.exports = {
  apps: [{
    name: 'raspadinha-backend',
    script: '/var/www/raspadinha/raspadinha-backend/venv/bin/python',
    args: '/var/www/raspadinha/raspadinha-backend/src/main.py',
    cwd: '/var/www/raspadinha/raspadinha-backend',
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '1G',
    env: {
      NODE_ENV: 'production',
      PORT: 5000,
      FLASK_ENV: 'production'
    },
    error_file: '/var/log/pm2/raspadinha-backend-error.log',
    out_file: '/var/log/pm2/raspadinha-backend-out.log',
    log_file: '/var/log/pm2/raspadinha-backend.log',
    time: true
  }]
};

