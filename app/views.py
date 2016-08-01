from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
from app.models import Plate, ExtraIngredient
from flask.ext.mongoengine.wtf import model_form

plates = Blueprint('plates', __name__, template_folder='templates')

class ListView(MethodView):

    def get(self):
        plates = Plate.objects.all()
        return render_template('plates/list.html', plates=plates)


class DetailView(MethodView):
	
    form = model_form(ExtraIngredient, exclude=['created_at'])

    def get_context(self, slug):
        plate = Plate.objects.get_or_404(slug=slug)
        form = self.form(request.form)

        context = {
            "plate": plate,
            "form": form
        }
        return context

    def get(self, slug):
        context = self.get_context(slug)
        return render_template('plates/detail.html', **context)

    def post(self, slug):
        context = self.get_context(slug)
        form = context.get('form')

        if form.validate():
            extra_ingredients = ExtraIngredient()
            form.populate_obj(extra_ingredients)

            plate = context.get('plate')
            plate.extra_ingredients.append(extra_ingredients)
            plate.save()

            return redirect(url_for('plates.detail', slug=slug))

        return render_template('plates/detail.html', **context)


# Register the urls
plates.add_url_rule('/', view_func=ListView.as_view('list'))
plates.add_url_rule('/<slug>/', view_func=DetailView.as_view('detail'))
