# -*- coding: utf-8 -*-
{
    "name": "Customer Live Chat",
    "version": "19.0.1.0.01",
    "category": "Website/Live Chat",

    "summary": "Authenticated customer live chat with persistent history and file sharing",

    "description": """
Customer Live Chat for Odoo 19
==============================

Turn your Odoo Customer Portal into a secure, real-time communication
channel between customers and your internal team.

Key Features
------------

* **Authenticated Customer Identification**:
  Identify customers by their real name and email when they initiate a chat.

* **Persistent Conversation History**:
  Returning customers can continue their existing conversation without
  creating unnecessary duplicate chat sessions.

* **File & Document Sharing**:
  Allow customers and operators to share images, PDFs, and documents
  directly through the live chat composer.

* **Flexible Visibility Controls**:
  Configure the chat experience for authenticated portal users according
  to your business requirements.

* **Portal-Focused Experience**:
  Designed specifically for customer portal communication with Odoo's
  native Live Chat and Discuss infrastructure.

* **No Website Builder Dependency**:
  Designed to operate without requiring the Odoo Website Builder module.
    """,

    "author": "Meta Frolic Labs",
    "website": "https://metafroliclabs.com",
    "support": "systems@metafroliclabs.com",

    "license": "LGPL-3",

    "price": 0.00,
    "currency": "USD",

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
    "application": True,
    "auto_install": False,
}