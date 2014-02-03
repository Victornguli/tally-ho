from django.core.exceptions import SuspiciousOperation
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import FormView

from libya_tally.apps.tally.forms.intake_barcode_form import\
    IntakeBarcodeForm
from libya_tally.apps.tally.forms.reconciliation_form import\
    ReconciliationForm
from libya_tally.apps.tally.models.quality_control import QualityControl
from libya_tally.apps.tally.models.result_form import ResultForm
from libya_tally.libs.models.enums.form_state import FormState
from libya_tally.libs.permissions import groups
from libya_tally.libs.utils.common import session_matches_post_result_form
from libya_tally.libs.views import mixins
from libya_tally.libs.views.form_state import form_in_state


class QualityControlView(mixins.GroupRequiredMixin,
                         mixins.ReverseSuccessURLMixin,
                         FormView):
    form_class = IntakeBarcodeForm
    group_required = groups.QUALITY_CONTROL_CLERK
    template_name = "tally/quality_control/home.html"
    success_url = 'quality-control-dashboard'

    def post(self, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            barcode = form.cleaned_data['barcode']
            result_form = get_object_or_404(ResultForm, barcode=barcode)
            form_in_state(result_form, FormState.QUALITY_CONTROL)
            self.request.session['result_form'] = result_form.pk

            QualityControl.objects.create(result_form=result_form,
                                          user=self.request.user)

            return redirect(self.success_url)
        else:
            return self.form_invalid(form)


class QualityControlDashboardView(mixins.GroupRequiredMixin,
                                  mixins.ReverseSuccessURLMixin,
                                  FormView):
    group_required = groups.QUALITY_CONTROL_CLERK
    template_name = "tally/quality_control/dashboard.html"
    success_url = 'quality-control-home'

    def get(self, *args, **kwargs):
        pk = self.request.session.get('result_form')
        result_form = get_object_or_404(ResultForm, pk=pk)
        form_in_state(result_form, FormState.QUALITY_CONTROL)

        return self.render_to_response(
            self.get_context_data(result_form=result_form))

    def post(self, *args, **kwargs):
        # abort
        del self.request.session['result_form']
        return redirect(self.success_url)


class QualityControlReconciliationView(mixins.GroupRequiredMixin,
                                       mixins.ReverseSuccessURLMixin,
                                       FormView):
    group_required = groups.QUALITY_CONTROL_CLERK
    template_name = "tally/quality_control/reconciliation.html"
    success_url = 'quality-control-dashboard'

    def get(self, *args, **kwargs):
        pk = self.request.session.get('result_form')
        result_form = get_object_or_404(ResultForm, pk=pk)
        reconciliation_form = ReconciliationForm(data=model_to_dict(
            result_form.reconciliationform))
        form_in_state(result_form, FormState.QUALITY_CONTROL)

        return self.render_to_response(
            self.get_context_data(result_form=result_form,
                                  reconciliation_form=reconciliation_form))

    def post(self, *args, **kwargs):
        post_data = self.request.POST
        pk = session_matches_post_result_form(post_data, self.request)
        result_form = get_object_or_404(ResultForm, pk=pk)
        form_in_state(result_form, FormState.QUALITY_CONTROL)

        if 'correct' in post_data:
            # send to dashboard
            quality_control = result_form.qualitycontrol
            quality_control.passed_reconciliation = True
            quality_control.save()

            return redirect(self.success_url)
        elif 'incorrect' in post_data:
            # send to reject page
            quality_control = result_form.qualitycontrol
            quality_control.passed_reconciliation = False
            quality_control.active = False
            quality_control.save()
            result_form.form_state = FormState.DATA_ENTRY_1
            result_form.save()

            return redirect('quality-control-reject')
        elif 'abort' in post_data:
            # send to entry
            del self.request.session['result_form']
            quality_control = result_form.qualitycontrol
            quality_control.active = False
            quality_control.save()

            return redirect('quality-control-home')

        raise SuspiciousOperation('Missing expected POST data')


class QualityControlGeneralView(mixins.GroupRequiredMixin,
                                mixins.ReverseSuccessURLMixin,
                                FormView):
    group_required = groups.QUALITY_CONTROL_CLERK
    template_name = "tally/quality_control/reconciliation.html"
    success_url = 'quality-control-dashboard'

    def get(self, *args, **kwargs):
        pk = self.request.session.get('result_form')
        result_form = get_object_or_404(ResultForm, pk=pk)
        form_in_state(result_form, FormState.QUALITY_CONTROL)

        return self.render_to_response(
            self.get_context_data(result_form=result_form))

    def post(self, *args, **kwargs):
        # abort
        del self.request.session['result_form']
        return redirect(self.success_url)


class QualityControlWomenView(mixins.GroupRequiredMixin,
                              mixins.ReverseSuccessURLMixin,
                              FormView):
    group_required = groups.QUALITY_CONTROL_CLERK
    template_name = "tally/quality_control/reconciliation.html"
    success_url = 'quality-control-dashboard'

    def get(self, *args, **kwargs):
        pk = self.request.session.get('result_form')
        result_form = get_object_or_404(ResultForm, pk=pk)
        form_in_state(result_form, FormState.QUALITY_CONTROL)

        return self.render_to_response(
            self.get_context_data(result_form=result_form))

    def post(self, *args, **kwargs):
        # abort
        del self.request.session['result_form']
        return redirect(self.success_url)