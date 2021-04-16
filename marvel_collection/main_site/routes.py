from flask import Blueprint, render_template

main_site = Blueprint('main_site', __name__, template_folder='site_templates')

@main_site.route('/')
def home():
    return render_template('index.html')