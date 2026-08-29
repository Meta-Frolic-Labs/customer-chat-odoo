# -*- coding: utf-8 -*-
from odoo import api, models


class DiscussChannel(models.Model):
    _inherit = "discuss.channel"

    @api.model
    def _portal_livechat_find_partner_session(self, livechat_channel_id, partner):
        """Return the portal client's live chat session for this channel.

        Prefers an active session, otherwise the most recent one so history
        can be restored after login.
        """
        if not livechat_channel_id or not partner:
            return self.browse()
        Domain = self.env["discuss.channel"]
        domain = [
            ("channel_type", "=", "livechat"),
            ("livechat_channel_id", "=", livechat_channel_id),
            ("channel_member_ids.partner_id", "=", partner.id),
        ]
        active = Domain.sudo().search(
            domain + [("livechat_active", "=", True)],
            order="write_date desc, id desc",
            limit=1,
        )
        if active:
            return active
        return Domain.sudo().search(domain, order="write_date desc, id desc", limit=1)

    @api.model
    def _portal_livechat_client_label(self, partner):
        """Human-readable label for agents (contact name, with email if useful)."""
        partner.ensure_one()
        name = (partner.name or "").strip() or (partner.display_name or "").strip()
        email = (partner.email or "").strip()
        if email and email.lower() not in (name or "").lower():
            return f"{name} ({email})" if name else email
        return name or email or partner.display_name

    def _portal_livechat_enable_attachments(self):
        """Allow portal clients to upload files on this live chat session.

        Odoo 18 Community gates the composer paperclip and
        ``/mail/attachment/upload`` on ``allow_public_upload`` for
        non-internal users; there is no Live Chat settings toggle.
        """
        to_enable = self.filtered(
            lambda c: c.channel_type == "livechat" and not c.allow_public_upload
        )
        if to_enable:
            to_enable.sudo().write({"allow_public_upload": True})
        return self

    def _portal_livechat_apply_client_label(self, partner=None):
        """Set channel / operator sidebar title to the portal client's identity."""
        for channel in self:
            if channel.channel_type != "livechat":
                continue
            client = partner
            if not client:
                operator = channel.livechat_operator_id
                client_members = channel.channel_member_ids.filtered(
                    lambda m: m.partner_id and m.partner_id != operator
                )
                client = client_members[:1].partner_id
            if not client:
                continue
            label = channel._portal_livechat_client_label(client)
            channel.sudo().write({"name": label, "anonymous_name": False})
            # Agents see custom_channel_name in the Discuss sidebar for livechat.
            operator_members = channel.sudo().channel_member_ids.filtered(
                lambda m: m.partner_id == channel.livechat_operator_id
            )
            for member in operator_members:
                if member.custom_channel_name != label:
                    member.write({"custom_channel_name": label})
                    member._bus_send_store(channel, {"custom_channel_name": label})
        return self
