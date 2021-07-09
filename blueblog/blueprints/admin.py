from flask import render_template,redirect,url_for,Blueprint

from  blueblog.forms import SettingForm, PostForm, CategoryForm, LinkForm
from  blueblog.utils import redirect_back

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/settings', methods=['GET', 'POST'])
def settings():
    form = SettingForm()
    return render_template('admin/settings.html', form = form)

@admin_bp.route('/post/manage')
def manage_post():
    return render_template('admin/manage_post.html')

@admin_bp.route('/post/new', mothods = ['GET' , 'POST'])
def new_post():
    form = PostForm()
    return render_template('admin/new_post.html', form = form)

@admin_bp.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):
    form = PostForm()
    return render_template('admin/edit_post.html', form=form)
