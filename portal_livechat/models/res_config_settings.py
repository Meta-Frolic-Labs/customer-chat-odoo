# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    portal_livechat_channel_id = fields.Many2one(
        "im_livechat.channel",
        string="Portal Live Chat Channel",
        config_parameter="portal_livechat.channel_id",
        help="Live Chat channel shown to authenticated portal users.",
    )

    portal_livechat_visibility_mode = fields.Selection(
        [
            ("portal_only", "Portal Users Only (Restricted)"),
            ("all_identified", "All Visitors (Auto-identify logged-in Portal Users)"),
        ],
        string="Visibility Mode",
        default="portal_only",
        config_parameter="portal_livechat.visibility_mode",
        help="Choose whether live chat is restricted only to logged-in portal clients or open to all visitors while identifying logged-in clients.",
    )

    portal_livechat_persistence_mode = fields.Selection(
        [
            ("continuous", "Single Continuous Channel (Reuse History)"),
            ("new_session", "New Session per Visit (Maintain Identity)"),
        ],
        string="Session Persistence",
        default="continuous",
        config_parameter="portal_livechat.persistence_mode",
        help="Choose whether to reuse the existing conversation thread for persistent history across logins, or start a new session each time.",
    )

    @api.model
    def _get_portal_livechat_channel(self):
        """Return the configured live chat channel, or an empty recordset."""
        channel_id = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("portal_livechat.channel_id")
        )
        if not channel_id:
            return self.env["im_livechat.channel"]
        try:
            channel_id = int(channel_id)
        except (TypeError, ValueError):
            return self.env["im_livechat.channel"]
        return self.env["im_livechat.channel"].sudo().browse(channel_id).exists()

    @api.model
    def _get_portal_livechat_visibility_mode(self):
        """Return 'portal_only' or 'all_identified'."""
        return (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("portal_livechat.visibility_mode", "portal_only")
        )

    @api.model
    def _get_portal_livechat_persistence_mode(self):
        """Return 'continuous' or 'new_session'."""
        return (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("portal_livechat.persistence_mode", "continuous")
        )
