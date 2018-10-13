from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Layout, Submit, HTML
from django import forms
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from speaker.models import Speaker


def get_edit_speaker_layout(submit_text):
    return Layout(
        Div(
            Field('name', autofocus='autofocus',
                  wrapper_class='col-12 col-md-6'),
            Field('twitter_handle', wrapper_class='col-12 col-md-6'),
            css_class='form-row'
        ),
        Div(
            Field('phone', wrapper_class='col-12 col-md-6'),
            Field('shirt_size', wrapper_class='col-12 col-md-6'),
            css_class='form-row'
        ),
        Div(
            Field('position', wrapper_class='col-12 col-md-6'),
            Field('organization', wrapper_class='col-12 col-md-6'),
            css_class='form-row'
        ),
        Div(
            Field('video_permission', wrapper_class='col-12 col-md-6'),
            css_class='form-row'
        ),
        Div(
            Field('short_biography', wrapper_class='col-12'),
            css_class='form-row'
        ),
        Div(
            Div(
                Submit('submit', submit_text,
                       css_class='btn btn-primary'),
                css_class='col-12'
            ),
            css_class='form-row'
        )
    )


class CreateSpeakerForm(forms.ModelForm):
    class Meta:
        model = Speaker
        fields = (
            'name', 'twitter_handle', 'phone', 'position',
            'organization', 'video_permission', 'short_biography',
            'shirt_size')
        widgets = {
            'short_biography': forms.Textarea({'rows': 3})
        }
        help_texts = {
            'name': _('How should we present your name to the audience?'),
            'short_biography': _(
                'Tell your audience who you are and what you want people to'
                ' know about you.')
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.html5_required = True
        self.helper.layout = get_edit_speaker_layout(_('Register as speaker'))

    def save(self, commit=True):
        self.instance.user = self.user
        return super(CreateSpeakerForm, self).save(commit)


class EditSpeakerForm(forms.ModelForm):
    class Meta:
        model = Speaker
        fields = (
            'name', 'twitter_handle', 'phone', 'position',
            'organization', 'video_permission', 'short_biography',
            'shirt_size')
        widgets = {
            'short_biography': forms.Textarea({'rows': 3})
        }
        help_texts = {
            'name': _('How should we present your name to the audience?'),
            'short_biography': _(
                'Tell your audience who you are and what you want people to'
                ' know about you.')
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.html5_required = True
        self.helper.layout = get_edit_speaker_layout(
            _('Update your speaker details'))


class UserSpeakerPortraitForm(forms.ModelForm):
    class Meta:
        model = Speaker
        fields = ('portrait',)

    def __init__(self, instance, *args, **kwargs):
        super().__init__(instance=instance, *args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = reverse_lazy('upload_user_speaker_portrait')
        self.helper.form_id = 'profile-img-upload'
        self.helper.layout = Layout(
            Div(
                Field('portrait', wrapper_class='col-12'),
                css_class='form-row',
            ),
            Div(
                Div(
                    Submit('submit', _('Submit your portrait'), css_class='btn btn-primary'),
                    HTML('<a href="{}" class="btn btn-secondary">{}</a>'.format(
                        reverse_lazy('user_speaker_profile'),
                        _('Skip upload'))),
                    css_class='col-12'
                ),
                css_class='form-row'
            ),
        )
