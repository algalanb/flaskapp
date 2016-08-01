from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView

from flask.ext.mongoengine.wtf import model_form

from app.auth import requires_auth
from app.models import Plate, ExtraIngredient

admin = Blueprint('admin', __name__, template_folder='templates')


class List(MethodView):
    decorators = [requires_auth]
    cls = Plate

    def get(self):
        plates = self.cls.objects.all()
        return render_template('admin/list.html', plates=plates)


class Detail(MethodView):

    decorators = [requires_auth]

    def get_context(self, slug=None):
        form_cls = model_form(Plate, exclude=('created_at', 'extra_ingredient'))

        if slug:
            plate = Plate.objects.get_or_404(slug=slug)
            if request.method == 'POST':
                form = form_cls(request.form, inital=plate._data)
            else:
                form = form_cls(obj=plate)
        else:
            plate = Plate()
            form = form_cls(request.form)

        context = {
            "plate": plate,
            "form": form,
            "create": slug is None
        }
        return context

    def get(self, slug):
        context = self.get_context(slug)
        return render_template('admin/detail.html', **context)

    def post(self, slug):
        context = self.get_context(slug)
        form = context.get('form')

        if form.validate():
            plate = context.get('plate')
            form.populate_obj(plate)
            plate.save()

            return redirect(url_for('admin.index'))
        return render_template('admin/detail.html', **context)


# Register the urls
admin.add_url_rule('/admin/', view_func=List.as_view('index'))
admin.add_url_rule('/admin/create/', defaults={'slug': None}, view_func=Detail.as_view('create'))
admin.add_url_rule('/admin/<slug>/', view_func=Detail.as_view('edit'))