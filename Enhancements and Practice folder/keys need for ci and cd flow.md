Your repository now has: 

CI requirements
DOCKERHUB_USERNAME     ✅
DOCKERHUB_TOKEN        ✅

MAIL_USERNAME          ✅
MAIL_PASSWORD          ✅
MAIL_TO                ✅
MAIL_CC                ✅

So CI can now:

Run tests ✅
Send CI success email ✅
Send CI failure email ✅
Build Docker image on tags ✅
Push Docker image to Docker Hub on tags ✅
CD requirements
RENDER_DEPLOY_HOOK        ✅
APPLICATION_HEALTH_URL    ✅

MAIL_USERNAME             ✅
MAIL_PASSWORD             ✅
MAIL_TO                   ✅
MAIL_CC                   ✅

So CD can now:

Trigger Render deployment ✅
Wait for startup ✅
Run health check ✅
Send deployment success email ✅
Send deployment failure email ✅

