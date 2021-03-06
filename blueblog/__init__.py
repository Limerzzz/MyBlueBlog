import os

import click
from flask import Flask, render_template
from flask_login import current_user
from flask_sqlalchemy import get_debug_queries
from flask_wtf.csrf import CSRError


from blueblog.blueprints.admin import admin_bp
from blueblog.blueprints.auth import auth_bp
from blueblog.blueprints.blog import blog_bp
from blueblog.extensions import bootstrap, db, ckeditor, mail, moment
from blueblog.models import Admin, Post, Category, Comment, Link
from blueblog.settings import config

# 返回项目的基本地址
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

def create_app(config_name = None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'developemnt')
    
    app = Flask('blueblog')
    app.config.from_object(config[config_name])

    register_logging(app)
    register_extensions(app)
    register_commands(app)
    register_errors(app)
    register_shell_context(app)
    return app

def register_logging(app):
    pass

def register_extensions(app):
    bootstrap.init_app(app);
    db.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)
    moment.init_app(app)

def register_blueprints(app):
    # 蓝本需要注册才可以使用
    # 这些 *_bp 本身就是一个 用于注册蓝本的工具
    # 蓝本的注册流程 使用 声明 *_bp , 使用 *_bp注册视图, 注册*_bp
    app.register_blueprint(blog_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')

def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db = db, Admin = Admin, Post = Post, Category = Category, Comment = Comment)

def register_template_context(app):
    @app.context_processor
    def make_template_context():
        # 查询数据库admin的第一个记录
        admin = Admin.query.first()
        categories = Category.query.order_by(Category.name).all()
        links = Link.query.order_by(link.name).all()
        return dict(admin = admin, categories = categories, links = links)

def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500


def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')

    @app.cli.command()
    @click.option('--usernanme', prompt=True, help='The username used to login')
    @click.option('--password', prompt=True, hide_input=True,
                    confirmation_prompt=True, help='The password used to login in')
    def init(username, password):
        click.echo('Initializing the database ...')
        db.create_all()

        admin = Admin.query.first()
        if admin is not None:
            click.echo('The administrator already exists, updating ...')
            admin.username = username
            admin.set_password(password)
        else:
            click.echo('Creating the temporary administrator account...')
            admin = Admin(
                username=username,
                blog_title='Bluelog',
                blog_sub_title='No, I'm the real thing.' ,
                name='Admin' ,
                about='Anything about you'
            )
    @app.cli.command()
    @click.option('--category', default=10, help='Quantity of categories, default is 10.')
    @click.option('--post', default=50, help='Quantity of posts, default is 50.')
    @click.option('--comment', default=500, help='Quantity of comments, default is 500.')
    def forge(category, post, comment):
        """Generate fake data."""
        from blueblog.fakes import fake_admin, fake_categories, fake_posts, fake_comments, fake_links

        db.drop_all()
        db.create_all()

        click.echo('Generating the administrator...')
        fake_admin()

        click.echo('Generating %d categories...' % category)
        fake_categories(category)

        click.echo('Generating %d posts...' % post)
        fake_posts(post)

        click.echo('Generating %d comments...' % comment)
        fake_comments(comment)

        click.echo('Generating links...')
        fake_links()

        click.echo('Done.')



