#!/usr/bin/env bash
./make_virtual_env.sh
source .env/bin/activate
.env/bin/gunicorn --bind 192.168.1.110:3000 jill_box:app
