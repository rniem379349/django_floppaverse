from user_agents import parse


def get_user_agent(request):
    user_agent_str = request.headers.get("user-agent")
    return parse(user_agent_str)
