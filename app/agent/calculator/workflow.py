from agent_framework import WorkflowBuilder
from app.agent.calculator.excutor import Dispatcher, aggregate, average_list, sum_list

dispatcher = Dispatcher(id="dispatcher_executor")
workflow = (
    WorkflowBuilder(start_executor=dispatcher, name="calculator_workflow", description="计算器工作流")
    .add_fan_out_edges(dispatcher, [sum_list, average_list])
    .add_fan_in_edges([sum_list, average_list], aggregate)
    .build()
)
