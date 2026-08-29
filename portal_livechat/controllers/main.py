# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.im_livechat.controllers.main import LivechatController
from odoo.addons.mail.models.discuss.mail_guest import add_guest_to_context
from odoo.addons.mail.tools.discuss import Store


class PortalLivechatController(LivechatController):
    """Control Live Chat initialization and session persistence based on settings."""

    def _portal_livechat_is_allowed(self):
        """Check if request is authorized according to configured visibility mode."""
        user = request.env.user
        visibility_mode = request.env["res.config.settings"]._get_portal_livechat_visibility_mode()
        if visibility_mode == "all_identified":
            return True

        # Default 'portal_only': allow only logged-in portal clients (not public, not internal users)
        return (
            bool(request.session.uid)
            and not user._is_public()
            and user.has_group("base.group_portal")
            and not user.has_group("base.group_user")
        )

    def _portal_livechat_store_existing_channel(self, channel):
        """Return the same payload shape as a freshly created session."""
        store = Store()
        channel._portal_livechat_apply_client_label(request.env.user.partner_id)
        member = channel.channel_member_ids.filtered(
            lambda m: m.partner_id == request.env.user.partner_id
        )[:1]
        if member and member.fold_state == "closed":
            member.fold_state = "open"
        # Keep the conversation available for both sides after login.
        if not channel.livechat_active:
            # sudo: discuss.channel - reactivate livechat session for returning portal client
            channel.sudo().livechat_active = True
        # Ensure reused sessions allow attachments.
        channel._portal_livechat_enable_attachments()
        store.add(channel)
        store.add(channel, {"isLoaded": True, "scrollUnread": False})
        request.env["res.users"]._init_store_data(store)
        return store.get_result()

    @http.route()
    @add_guest_to_context
    def livechat_init(self, channel_id):
        if not self._portal_livechat_is_allowed():
            store = Store()
            request.env["res.users"]._init_store_data(store)
            return {
                "available_for_me": False,
                "rule": {},
                "storeData": store.get_result(),
            }
        return super().livechat_init(channel_id)

    @http.route()
    @add_guest_to_context
    def get_session(
        self,
        channel_id,
        anonymous_name,
        previous_operator_id=None,
        chatbot_script_id=None,
        persisted=True,
        **kwargs,
    ):
        if not self._portal_livechat_is_allowed():
            return False

        user = request.env.user
        is_logged_in_portal = (
            bool(request.session.uid)
            and not user._is_public()
            and user.has_group("base.group_portal")
            and not user.has_group("base.group_user")
        )

        persistence_mode = request.env["res.config.settings"]._get_portal_livechat_persistence_mode()

        if persisted and is_logged_in_portal and persistence_mode == "continuous":
            existing = request.env["discuss.channel"]._portal_livechat_find_partner_session(
                channel_id,
                user.partner_id,
            )
            if existing:
                return self._portal_livechat_store_existing_channel(existing)

        result = super().get_session(
            channel_id,
            anonymous_name,
            previous_operator_id=previous_operator_id,
            chatbot_script_id=chatbot_script_id,
            persisted=persisted,
            **kwargs,
        )
        if persisted and result and is_logged_in_portal:
            created = request.env["discuss.channel"]._portal_livechat_find_partner_session(
                channel_id,
                user.partner_id,
            )
            if created:
                created._portal_livechat_apply_client_label(user.partner_id)
                created._portal_livechat_enable_attachments()
        return result
