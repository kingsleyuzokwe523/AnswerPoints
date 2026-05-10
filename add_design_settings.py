#!/usr/bin/env python3
from app import create_app, db
from app.models import init_home_content

app = create_app()
with app.app_context():
    init_home_content()
    print("Design settings added successfully!")
