from fastapi import APIRouter, Request, HTTPException
import logging
from core.telegram import send_telegram_msg

logger = logging.getLogger(__name__)

router = APIRouter(
    tags=["GitHub Webhook"]
)

@router.post("/github-webhook")
async def github_webhook(request: Request):
    """
    Endpoint for GitHub Webhook.
    """
    try:
        event = request.headers.get("X-GitHub-Event")
        payload = await request.json()

        if event == "push":
            pusher = payload.get("pusher", {}).get("name", "Unknown")
            repo_name = payload.get("repository", {}).get("name", "UnknownRepo")
            commits = payload.get("commits", [])
            
            # Format
            message = f"🚀 <b>New Push</b> to <b>{repo_name}</b> by <b>{pusher}</b>\n\n"
            for commit in commits[:5]:
                message += f"• {commit.get('message')} (<a href='{commit.get('url')}'>link</a>)\n"

            send_telegram_msg(message)
            return {"status": "success", "event": "push"}

        elif event == "pull_request":
            action = payload.get("action")
            pr = payload.get("pull_request", {})
            title = pr.get("title", "No title")
            url = pr.get("html_url", "")
            user = pr.get("user", {}).get("login", "Unknown")
            repo_name = payload.get("repository", {}).get("name", "UnknownRepo")

            message = f"🔀 <b>Pull Request {action}</b> in <b>{repo_name}</b>\n"
            message += f"<b>Title:</b> {title}\n"
            message += f"<b>Author:</b> {user}\n"
            message += f"<a href='{url}'>View PR</a>"

            send_telegram_msg(message)
            return {"status": "success", "event": f"pull_request {action}"}

        return {"status": "ignored", "message": f"Event {event} is not handled yet"}

    except Exception as e:
        logger.error(f"Error processing GitHub webhook: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
