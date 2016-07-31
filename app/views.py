from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
from app.models import Plate, ExtraIngredient


plates = Blueprint('plates', __name__, template_folder='templates')

class ListView(MethodView):

    def get(self):
        plates = Plate.objects.all()
        return render_template('plates/list.html', plates=plates)


class DetailView(MethodView):

    def get(self, slug):
        plate = Plate.objects.get_or_404(slug=slug)
        return render_template('plates/detail.html', plate=plate)


# Register the urls
plates.add_url_rule('/', view_func=ListView.as_view('list'))
plates.add_url_rule('/<slug>/', view_func=DetailView.as_view('detail'))
