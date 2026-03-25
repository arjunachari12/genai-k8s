import asyncio
import json
import os
from typing import Any, TypedDict

from langchain_ollama import ChatOllama
from langgraph.graph import END, START, StateGraph
from mcp.client.session import ClientSession
from mcp.client.sse import sse_client


MCP_SERVER_URL = os.environ.get(
    "MCP_SERVER_URL",
    "http://mcp-server-svc.genai.svc.cluster.local:80/sse",
)
OLLAMA_BASE_URL = os.environ.get(
    "OLLAMA_BASE_URL",
    "http://ollama.genai.svc.cluster.local:11434",
)
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "tinyllama")
TARGET_NAMESPACE = os.environ.get("TARGET_NAMESPACE", "genai")
ASSISTANT_PROMPT = os.environ.get(
    "ASSISTANT_PROMPT",
    "Investigate the genai namespace. Summarize any unhealthy pods and the most likely fix.",
)


class AssistantState(TypedDict, total=False):
    prompt: str
    namespace: str
    pod_report: str
    events_report: str
    logs_report: str
    unhealthy_pod: str
    should_fetch_logs: bool
    final_answer: str


async def call_mcp_tool(tool_name: str, arguments: dict[str, Any]) -> str:
    async with sse_client(MCP_SERVER_URL) as streams:
        read_stream, write_stream = streams
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            result = await session.call_tool(tool_name, arguments=arguments)

    content = []
    for item in result.content:
        text = getattr(item, "text", None)
        if text:
            content.append(text)
    return "\n".join(content) if content else str(result)


def call_mcp_tool_sync(tool_name: str, arguments: dict[str, Any]) -> str:
    return asyncio.run(call_mcp_tool(tool_name, arguments))


def fetch_pods(state: AssistantState) -> AssistantState:
    namespace = state["namespace"]
    print(f"[tool] get_pods_in_namespace namespace={namespace}")
    pod_report = call_mcp_tool_sync("get_pods_in_namespace", {"namespace": namespace})
    return {"pod_report": pod_report}


def plan_investigation(state: AssistantState) -> AssistantState:
    unhealthy_pod = ""
    should_fetch_logs = False
    pod_data = json.loads(state["pod_report"])
    no_log_reasons = {"ImagePullBackOff", "ErrImagePull", "InvalidImageName"}
    priority_reasons = ["CrashLoopBackOff", "ImagePullBackOff", "ErrImagePull", "CreateContainerError"]
    best_score = -1

    for pod in pod_data:
        phase = pod.get("phase")
        if phase == "Succeeded":
            continue

        statuses = pod.get("container_statuses") or []
        for status in statuses:
            reason = status.get("reason") or ""
            if status.get("ready", True) and not reason and phase == "Running":
                continue

            score = 1
            if reason in priority_reasons:
                score = 10 - priority_reasons.index(reason)
            elif phase in {"Pending", "Failed", "Unknown"}:
                score = 5

            if score > best_score:
                best_score = score
                unhealthy_pod = pod["name"]
                should_fetch_logs = reason not in no_log_reasons

        if not statuses and phase in {"Pending", "Failed", "Unknown"} and 5 > best_score:
            best_score = 5
            unhealthy_pod = pod["name"]
            should_fetch_logs = False

    if unhealthy_pod:
        print(f"[plan] Found unhealthy pod: {unhealthy_pod}. fetch_logs={should_fetch_logs}")
    else:
        print("[plan] No unhealthy pods found.")

    return {
        "unhealthy_pod": unhealthy_pod,
        "should_fetch_logs": should_fetch_logs,
    }


def fetch_events(state: AssistantState) -> AssistantState:
    namespace = state["namespace"]
    print(f"[tool] get_recent_events namespace={namespace}")
    events_report = call_mcp_tool_sync(
        "get_recent_events",
        {"namespace": namespace, "limit": 10},
    )
    return {"events_report": events_report}


def fetch_logs(state: AssistantState) -> AssistantState:
    pod_name = state["unhealthy_pod"]
    namespace = state["namespace"]
    print(f"[tool] get_pod_logs namespace={namespace} pod_name={pod_name}")
    logs_report = call_mcp_tool_sync(
        "get_pod_logs",
        {
            "namespace": namespace,
            "pod_name": pod_name,
            "tail_lines": 50,
        },
    )
    return {"logs_report": logs_report}


def should_investigate(state: AssistantState) -> str:
    return "fetch_events" if state.get("unhealthy_pod") else "summarize"


def should_read_logs(state: AssistantState) -> str:
    return "fetch_logs" if state.get("should_fetch_logs") else "summarize"


def summarize(state: AssistantState) -> AssistantState:
    model = ChatOllama(
        model=OLLAMA_MODEL,
        base_url=OLLAMA_BASE_URL,
        temperature=0,
    )

    pod_data = json.loads(state["pod_report"])
    unhealthy_pod_data = next(
        (pod for pod in pod_data if pod.get("name") == state.get("unhealthy_pod")),
        None,
    )
    recent_events = state.get("events_report", "No event data collected")
    logs_report = state.get("logs_report", "No logs collected")
    summary_prompt = f"""
You are a beginner-friendly AI Kubernetes assistant.

User request:
{state["prompt"]}

Namespace:
{state["namespace"]}

Unhealthy pod details:
{json.dumps(unhealthy_pod_data, indent=2) if unhealthy_pod_data else "No unhealthy pod found"}

Recent events:
{recent_events}

Pod logs:
{logs_report}

Write a short answer with:
1. Health summary
2. Root cause
3. Exact next kubectl command or manifest fix
"""
    try:
        response = model.invoke(summary_prompt)
        return {"final_answer": response.content}
    except Exception as exc:
        fallback_answer = f"""Health summary: Pod `{state.get('unhealthy_pod', 'unknown')}` in namespace `{state['namespace']}` is unhealthy.

Root cause: Based on the collected pod status and events, the workload likely failed because of a Kubernetes startup issue such as an invalid image tag or container startup error.

Next step: Run `kubectl describe pod {state.get('unhealthy_pod', '<pod-name>')} -n {state['namespace']}` and then fix the deployment image or container configuration.

Model note: Ollama summarization failed with `{exc}` after the MCP tools completed successfully.
"""
        return {"final_answer": fallback_answer}


def build_graph():
    graph = StateGraph(AssistantState)
    graph.add_node("fetch_pods", fetch_pods)
    graph.add_node("plan_investigation", plan_investigation)
    graph.add_node("fetch_events", fetch_events)
    graph.add_node("fetch_logs", fetch_logs)
    graph.add_node("summarize", summarize)

    graph.add_edge(START, "fetch_pods")
    graph.add_edge("fetch_pods", "plan_investigation")
    graph.add_conditional_edges(
        "plan_investigation",
        should_investigate,
        {
            "fetch_events": "fetch_events",
            "summarize": "summarize",
        },
    )
    graph.add_conditional_edges(
        "fetch_events",
        should_read_logs,
        {
            "fetch_logs": "fetch_logs",
            "summarize": "summarize",
        },
    )
    graph.add_edge("fetch_logs", "summarize")
    graph.add_edge("summarize", END)

    return graph.compile()


def main() -> None:
    print(f"Using Ollama model: {OLLAMA_MODEL}")
    print(f"Using Ollama endpoint: {OLLAMA_BASE_URL}")
    print(f"Using MCP endpoint: {MCP_SERVER_URL}")
    print(f"Prompt: {ASSISTANT_PROMPT}")

    app = build_graph()
    result = app.invoke(
        {
            "prompt": ASSISTANT_PROMPT,
            "namespace": TARGET_NAMESPACE,
        }
    )

    print("==== Final Answer ====")
    print(result["final_answer"])
    print("======================")


if __name__ == "__main__":
    main()
