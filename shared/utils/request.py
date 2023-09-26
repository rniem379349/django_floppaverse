def get_user_agent_browser(request):
    user_agent_str = request.headers.get("user-agent")
    return user_agent_str.split(" ")[-1].split("/")[0].lower()
