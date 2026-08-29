# -*- coding: utf-8 -*-
from odoo import models


class ImLivechatChannel(models.Model):
    _inherit = "im_livechat.channel"

    def _get_livechat_discuss_channel_vals(
        self,
        anonymous_name,
        previous_operator_id=None,
        chatbot_script=None,
        user_id=None,
        country_id=None,
        lang=None,
    ):
        vals = super()._get_livechat_discuss_channel_vals(
            anonymous_name,
            previous_operator_id=previous_operator_id,
            chatbot_script=chatbot_script,
            user_id=user_id,
            country_id=country_id,
            lang=lang,
        )
        if not vals or chatbot_script or not user_id:
            return vals

        visitor_user = self.env["res.users"].browse(user_id)
        if not visitor_user or not visitor_user.active:
            return vals

        # Only set create-allowed fields here. custom_channel_name must be
        # applied after create (see _portal_livechat_apply_client_label).
        partner = visitor_user.partner_id
        client_label = self.env["discuss.channel"]._portal_livechat_client_label(partner)
        vals["name"] = client_label
        vals["anonymous_name"] = False
        # Enable composer attachments for portal clients (Odoo 18 Community
        # has no Live Chat setting for this; core gates on allow_public_upload).
        vals["allow_public_upload"] = True
        return vals
