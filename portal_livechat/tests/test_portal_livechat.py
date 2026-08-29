# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase


class TestPortalLivechat(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Create livechat operator user and partner
        cls.operator_user = cls.env["res.users"].create({
            "name": "Livechat Operator",
            "login": "operator@test.com",
            "email": "operator@test.com",
            "groups_id": [(6, 0, [
                cls.env.ref("base.group_user").id,
                cls.env.ref("im_livechat.im_livechat_group_user").id,
            ])],
        })

        # Create livechat channel
        cls.livechat_channel = cls.env["im_livechat.channel"].create({
            "name": "Portal Support Channel",
            "user_ids": [(6, 0, [cls.operator_user.id])],
        })

        # Create portal client user and partner
        cls.portal_user = cls.env["res.users"].create({
            "name": "John Doe",
            "login": "johndoe@test.com",
            "email": "johndoe@test.com",
            "groups_id": [(6, 0, [cls.env.ref("base.group_portal").id])],
        })

        # Configure portal livechat channel in ir.config_parameter
        cls.env["ir.config_parameter"].sudo().set_param(
            "portal_livechat.channel_id",
            cls.livechat_channel.id,
        )
        cls.env["ir.config_parameter"].sudo().set_param(
            "portal_livechat.visibility_mode",
            "portal_only",
        )
        cls.env["ir.config_parameter"].sudo().set_param(
            "portal_livechat.persistence_mode",
            "continuous",
        )

    def test_01_portal_livechat_config_getters(self):
        """Test configuration getters resolve correctly."""
        channel = self.env["res.config.settings"]._get_portal_livechat_channel()
        self.assertEqual(channel.id, self.livechat_channel.id)

        vis_mode = self.env["res.config.settings"]._get_portal_livechat_visibility_mode()
        self.assertEqual(vis_mode, "portal_only")

        persist_mode = self.env["res.config.settings"]._get_portal_livechat_persistence_mode()
        self.assertEqual(persist_mode, "continuous")

    def test_02_portal_client_label_generation(self):
        """Test formatting of human-readable client label with email."""
        label = self.env["discuss.channel"]._portal_livechat_client_label(self.portal_user.partner_id)
        self.assertEqual(label, "John Doe (johndoe@test.com)")

        # When email is already in the name, avoid duplication
        self.portal_user.partner_id.name = "John Doe johndoe@test.com"
        label_no_dup = self.env["discuss.channel"]._portal_livechat_client_label(self.portal_user.partner_id)
        self.assertEqual(label_no_dup, "John Doe johndoe@test.com")

    def test_03_portal_channel_vals_and_naming(self):
        """Test channel vals generated for portal user use proper naming and clear anonymous flag."""
        vals = self.livechat_channel._get_livechat_discuss_channel_vals(
            anonymous_name="Visitor",
            user_id=self.portal_user.id,
        )
        self.assertTrue(vals)
        self.assertFalse(vals.get("anonymous_name"))
        self.assertIn("johndoe@test.com", vals.get("name", ""))

    def test_04_session_search_and_reuse(self):
        """Test session search finds active or existing channel for portal partner."""
        discuss_channel = self.env["discuss.channel"].sudo().create({
            "name": "John Doe (johndoe@test.com)",
            "channel_type": "livechat",
            "livechat_channel_id": self.livechat_channel.id,
            "livechat_operator_id": self.operator_user.partner_id.id,
            "livechat_active": True,
            "channel_member_ids": [
                (0, 0, {"partner_id": self.portal_user.partner_id.id}),
                (0, 0, {"partner_id": self.operator_user.partner_id.id}),
            ],
        })

        found = self.env["discuss.channel"]._portal_livechat_find_partner_session(
            self.livechat_channel.id,
            self.portal_user.partner_id,
        )
        self.assertEqual(found.id, discuss_channel.id)

    def test_05_attachment_enablement(self):
        """Test _portal_livechat_enable_attachments turns on allow_public_upload."""
        discuss_channel = self.env["discuss.channel"].sudo().create({
            "name": "Attachment Test Channel",
            "channel_type": "livechat",
            "livechat_channel_id": self.livechat_channel.id,
            "livechat_operator_id": self.operator_user.partner_id.id,
            "allow_public_upload": False,
        })
        self.assertFalse(discuss_channel.allow_public_upload)

        discuss_channel._portal_livechat_enable_attachments()
        self.assertTrue(discuss_channel.allow_public_upload)
