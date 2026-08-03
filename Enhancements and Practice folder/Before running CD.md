# 🔐 CD Required Repository Secrets

Before running the **Continuous Deployment (CD)** pipeline, the product repository must have the following GitHub Actions secrets configured:

| Secret Key | Status | Purpose |
|---|---|---|
| `RENDER_DEPLOY_HOOK` | ✅ Required | Triggers the Render deployment process |
| `APPLICATION_HEALTH_URL` | ✅ Required | Verifies application availability after deployment |
| `MAIL_USERNAME` | ✅ Required | SMTP email authentication username |
| `MAIL_PASSWORD` | ✅ Required | SMTP email authentication password/app password |
| `MAIL_TO` | ✅ Required | Primary deployment notification receiver |
| `MAIL_CC` | ✅ Required | Additional deployment notification receivers |

---

## ✅ CD Pipeline Prerequisites

Before starting deployment, confirm:

- ✅ Render deployment hook is configured
- ✅ Application health check URL is available
- ✅ Email notification credentials are configured
- ✅ Deployment notification recipients are added

Once all secrets are available, the CD workflow can:

- 🚀 Trigger Render deployment
- ⏳ Wait for application startup
- ❤️ Run application health checks
- 📧 Send deployment success notifications
- ❌ Send deployment failure notifications
