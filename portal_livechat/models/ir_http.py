# -*- coding: utf-8 -*-
from odoo import models
from odoo.http import request


class IrHttp(models.AbstractModel):
    _inherit = "ir.http"

    def get_frontend_session_info(self):
        session_info = super().get_frontend_session_info()
        livechat_data = self._get_portal_livechat_data()
        if livechat_data is not None:
            session_info["livechatData"] = livechat_data
        return session_info

    def _get_portal_livechat_data(self):
        """Provide livechat bootstrap data according to configured visibility and persistence modes.

        When persistence is 'continuous', restores an existing discuss.channel via
        ``force_thread`` so login does not open a brand-new conversation (history is kept).
        """
        if not request:
            return None

        unavailable = {
            "isAvailable": False,
            "serverUrl": request.env["ir.http"].get_base_url(),
            "options": {},
        }

        user = request.env.user
        visibility_mode = request.env["res.config.settings"]._get_portal_livechat_visibility_mode()
        is_logged_in_portal = (
            bool(request.session.uid)
            and not user._is_public()
            and user.has_group("base.group_portal")
            and not user.has_group("base.group_user")
        )

        # In portal_only mode, deny non-portal visitors
        if visibility_mode == "portal_only" and not is_logged_in_portal:
            return unavailable

        channel = request.env["res.config.settings"]._get_portal_livechat_channel()
        if not channel:
            return unavailable

        # If logged in as portal client, identify username and resolve persistent channel
        username = False
        partner = False
        if is_logged_in_portal:
            partner = user.partner_id
            username = request.env["discuss.channel"]._portal_livechat_client_label(partner)

        info = channel.get_livechat_info(username=username)
        options = info.get("options") or {}

        # Handle persistence mode
        persistence_mode = request.env["res.config.settings"]._get_portal_livechat_persistence_mode()
        existing = False
        if is_logged_in_portal and persistence_mode == "continuous" and partner:
            existing = request.env["discuss.channel"]._portal_livechat_find_partner_session(
                channel.id,
                partner,
            )
            if existing:
                existing._portal_livechat_apply_client_label(partner)
                options = dict(options)
                options["force_thread"] = {
                    "id": existing.id,
                    "model": "discuss.channel",
                }
                # Reactivate on login so both sides can continue the history
                if not existing.livechat_active:
                    # sudo: discuss.channel - reactivate livechat session for logged-in portal user
                    existing.sudo().livechat_active = True

        return {
            "isAvailable": bool(info.get("available")) or bool(existing),
            "serverUrl": info.get("server_url") or request.env["ir.http"].get_base_url(),
            "options": options,
        }
