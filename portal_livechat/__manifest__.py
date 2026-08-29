# -*- coding: utf-8 -*-
{
    "name": "Portal Live Chat",
    "version": "18.0.1.0.0",
    "category": "Website/Live Chat",
    "summary": "Authenticated customer live chat on portal with persistent history and attachments",
    "description": """
Portal Live Chat for Odoo 18 (Community & Enterprise)
=====================================================

Turn your Odoo Customer Portal into a secure, real-time client communication channel.

Key Highlights:
---------------
* **Authenticated Client Identification**: Real client name and email displayed to operators in Discuss.
* **Continuous Conversation History**: Reconnect returning portal users to their active chat session without creating duplicate threads.
* **File & Document Sharing**: Out-of-the-box support for sharing PDFs, documents, and images via the live chat composer.
* **Flexible Visibility Controls**: Restrict the live chat widget to logged-in portal users only or allow all visitors with auto-identification.
* **Zero Website Module Dependency**: Runs smoothly on standalone Portal setups without requiring the website builder module.
    """,
    "author": "Muhammad Kamil",
    "website": "https://github.com/muhammadkamil",
    "support": "support@example.com",
    "license": "LGPL-3",
    "price": 0.00,
    "currency": "EUR",
    "images": [
        "static/description/banner.png",
    ],
    "depends": [
        "base_setup",
        "im_livechat",
        "portal",
    ],
    "data": [
        "views/res_config_settings_views.xml",
        "views/discuss_channel_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
