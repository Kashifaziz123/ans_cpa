from odoo.addons.website.controllers.form import WebsiteForm


class WebsiteFormInherit(WebsiteForm):

    def insert_record(self, request, model, values, custom, meta=None):
        if model.model == "crm.lead":
            request.update_context(
                from_website_form=True,
                form_values=values,
                mail_create_nosubscribe=True,
                mail_auto_subscribe_no_notify=True,
                mail_notify_force_send=False,
            )

        return super().insert_record(request, model, values, custom, meta=meta)
