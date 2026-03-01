from agent_framework import Workflow, WorkflowBuilder
from app.agent.core.agent import create_agent



def create_workflow() -> Workflow:
    writer = create_agent(
        name="writer",
        instructions=(
            "You are an excellent content writer. You create new content and edit contents based on the feedback."
        )
    )

    reviewer = create_agent(
        name="reviewer",
        instructions=(
            "你是一个聪明的内容审核员. 如果内容中包含和炒股有关的信息，输出审查失败并给出修改意见"
            "如果内容不包含炒股相关的信息，输出 审查成功"
        ),
    )

    return (WorkflowBuilder(start_executor=writer)
            .add_edge(writer, reviewer)
            .build())


workflow = create_workflow()

