from markupsafe import Markup, escape

from odoo import http
from odoo.exceptions import AccessDenied
from odoo.http import request
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


class ApplicantSummaryRecovery(http.Controller):

    @http.route(
        "/ans/backfill_applicant_summaries",
        type="json",
        auth="user",
        methods=["POST"],
    )
    def backfill_applicant_summaries(self, limit=5):
        if not request.env.user.has_group("base.group_system"):
            raise AccessDenied()

        limit = max(1, min(int(limit), 100))
        applicants = request.env["hr.applicant"].search(
            [("description", "in", [False, ""])],
            order="id desc",
            limit=limit,
        )

        updated_ids = []
        for applicant in applicants:
            values = [
                ("Applicant Name", applicant.partner_name),
                ("Email", applicant.email_from),
                ("Mobile", applicant.partner_mobile or applicant.partner_phone),
                ("Degree", applicant.type_id.display_name),
                ("Applied Job", applicant.job_id.display_name),
                ("Department", applicant.department_id.display_name),
                ("LinkedIn Profile", applicant.linkedin_profile),
            ]
            rows = [
                Markup("<strong>{}</strong>: {}<br>").format(
                    escape(label), escape(value)
                )
                for label, value in values
                if value
            ]
            applicant.description = Markup(
                "<p><strong>Available Information (Recovered)</strong><br>{}</p>"
            ).format(Markup("").join(rows))
            updated_ids.append(applicant.id)

        return {"updated_count": len(updated_ids), "updated_ids": updated_ids}
