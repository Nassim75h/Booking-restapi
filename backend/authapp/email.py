from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.core import mail
from django.template.context import make_context
from django.template.loader import get_template
from django.views.generic.base import ContextMixin
from authapp.utils import make_token


class BaseEmailMessage(mail.EmailMultiAlternatives, ContextMixin):
    template_name = None
    # _blocks_map keys are used in the template. These keys map to instance attributes
    # where the rendered content will be assigned.eg: self._blocks_map[key] = rendered_content
    _blocks_map = {
        "subject": "subject",
        "text_body": "body",
        "html_body": "html",
    }

    def __init__(self, request=None, context=None, template_name=None, *args, **kwargs):
        # Make sure to include => subject, body, to, bcc, attachments,  alternatives in kwargs
        super().__init__(*args, **kwargs)
        self.request = request
        self.context = {} if context is None else context
        self.html = None

    def get_context_data(self, **kwargs):
        """
        Build the context that will be used in the email template
        """
        contx = super().get_context_data(**kwargs)
        context = dict(contx, **self.context)
        if self.request:
            site = get_current_site(self.request)
            domain = context.get('domain') or (settings.DOMAIN or site.domain)
            protocol = context.get('protocol') or (
                "https" if self.request.is_secure() else "http")
            site_name = context.get("site_name") or (
                settings.SITE_NAME or site.name)
            user = context.get("user") or self.request.user
        else:
            # when we don't have request this mainly for development `django shell` but even if we send emails in background tasks it will work properly
            domain = context.get("domain") or settings.DOMAIN
            protocol = context.get("protocol") or "http"
            site_name = context.get("site_name") or settings.SITE_NAME
            user = context.get("user")

        context.update({
            "domain": domain,
            "protocol": protocol,
            "site_name": site_name,
            "user": user,
        })
        return context

    def _process_blocks(self, block, context):
        """
        This method process blocks provided in template , it render the content of each block and assign the rendered content to BaseEmailMessage instance  
        This method processes template blocks (e.g., for the subject, body, HTML) and assigns the rendered content to the corresponding attributes on the BaseEmailMessage instance
        """
        block_name = block.name if hasattr(block, 'name') else None
        if block_name and block_name in self._blocks_map:
            attr = self._blocks_map[block_name]
            # eg: self.subject = block.render(context).strip()
            setattr(self, attr, block.render(context).strip())

    def render(self):
        """
        Render the email template and process the blocks.
        """
        context = make_context(self.get_context_data(), request=self.request)
        template = get_template(self.template_name)
        with context.bind_template(template.template):
            for block in template.template.nodelist:
                self._process_blocks(block, context)
        self._attach_body()

    def _attach_body(self):
        """
        Attach the body (HTML or text) to the email.
        """
        if self.body and self.html:
            self.attach_alternative(self.html, "text/html")
        elif self.html:
            self.body = self.html
            self.content_subtype = "html"


class ActivationEmail(BaseEmailMessage):
    template_name = "email/activation.html"

    def get_context_data(self, **kwargs):
        """
        Build the context specific to activation emails.
        """
        context = super().get_context_data(**kwargs)
        context.pop("view", None)
        user = context.get("user")
        # get activation token
        activation_token = make_token(user)
        # Build URL: https(s)://domain.com/activate/4SDfsjjdbS387yjnjkew9yguye.....
        activation_url = f"{context['protocol']}://localhost:8080/activate/{activation_token}/"
        context["activation_url"] = activation_url

        return context

    def send(self, email, fail_silently=False):
        """
        Send the activation email to the user.
        """
        # context = self.get_context_data(request, user)
        self.to = [email]
        self.render()

        super().send(fail_silently=fail_silently)


class SendPasswordResetEmail(BaseEmailMessage):
    template_name = "email/confirmpasswordreset.html"

    def get_context_data(self, **kwargs):
        """
        Build the context specific to rest password via email
        """
        context = super().get_context_data(**kwargs)
        context.pop("view", None)
        user = context.get("user")
        # get activation token
        reset_pass_token = make_token(user)
        # Build URL: https(s)://domain.com/confirmrestpassword/4SDfsjjdbS387yjnjkew9yguye.....
        reset_url = f"{context['protocol']}://localhost:8080/confirmrestpassword/{reset_pass_token}/"

        context["reset_url"] = reset_url

        return context

    def send(self, email, fail_silently=False):
        """
        Send the reset password email to the user
        """
        # context = self.get_context_data(request, user)
        self.to = [email]
        self.render()
        super().send(fail_silently=fail_silently)
