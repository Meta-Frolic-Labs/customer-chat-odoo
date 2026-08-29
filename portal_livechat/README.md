# Portal Live Chat (Odoo 19 Community & Enterprise)

**Portal Live Chat** transforms your Odoo Customer Portal (`/my`) into a secure, real-time client communication channel. It connects logged-in portal clients with operators in Discuss while identifying contacts by name/email, maintaining conversation history across logins, and enabling document attachments.

---

## 🌟 Key Features

1. **Authenticated Client Identification**: 
   - Operators in Discuss see the real client's name and email rather than anonymous tags like `Visitor #1234`.
2. **Persistent Session & History**:
   - When a portal user logs in or returns to the portal, their ongoing conversation thread is restored rather than opening duplicate channels.
3. **File & Attachment Sharing**:
   - Enables file uploads (PDF, DOCX, images) directly from the live chat composer for portal clients.
4. **Customizable Visibility & Persistence Modes**:
   - **Visibility Mode**: `Portal Users Only` (strict privacy) or `All Visitors with Auto-Identification`.
   - **Persistence Mode**: `Single Continuous Channel` (history preserved) or `New Session per Visit`.
5. **Zero Website Dependency**:
   - Built purely on `im_livechat` and `portal`. Works on standalone Customer Portal setups without needing `website` or `website_livechat`.

---

## 📋 Requirements & Dependencies

- **Odoo Version**: 19.0 (Community & Enterprise)
- **Required Modules**:
  - `im_livechat` (Live Chat)
  - `portal` (Customer Portal)
  - `base_setup` (General Settings)

---

## 🚀 Quick Setup Guide

1. Place `portal_livechat` inside your Odoo `custom_addons` directory.
2. Update the Apps list in Developer Mode and install **Portal Live Chat**.
3. Go to **Live Chat → Channels**, create or select a support channel, and assign your employee operators.
4. Navigate to **Settings → General Settings → Portal Live Chat**:
   - Select your **Portal Live Chat Channel**.
   - Set **Visibility Mode** (`Portal Users Only` recommended).
   - Set **Session Persistence** (`Single Continuous Channel` recommended).
5. Have a portal user log into `/my` — the chat widget will appear and connect directly to your Discuss backend!

---

## 🧪 Running Automated Tests

Run the included test suite with standard Odoo CLI commands:

```bash
odoo-bin -c /path/to/odoo.conf -d your_db -i portal_livechat --test-enable --stop-after-init
```

---

## 📦 App Store Publishing Guide

To publish on the **Odoo Apps Store**:
1. Push this module to a dedicated Git repository on branch `18.0`.
2. Ensure `static/description/icon.png` (128x128) and `static/description/index.html` are present.
3. Log in to [apps.odoo.com](https://apps.odoo.com) with your author account and link your Git repository.

---

## 📄 License & Support

- **License**: LGPL-3
- **Author**: Muhammad Kamil
- **Support**: support@example.com
