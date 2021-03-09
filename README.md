## Steps:

1. Finish upsert method
2. Finish the other API's
3. Create API test suite
4. Hook up to site

### Day

How do I do alembic migrations?
Job Summary needs to be unique on userID, type, address

Job summary needs : estimate , forms [these just need to be filtered by a day] , config

```
def create_app():
    ...

    with app.app_context():
        # Include our Routes
        from . import routes

        # Register Blueprints
        app.register_blueprint(auth.auth_bp)
        app.register_blueprint(admin.admin_bp)

        return app
```

Could include a flag 