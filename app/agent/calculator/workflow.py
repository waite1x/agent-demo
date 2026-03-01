from agent_framework import WorkflowBuilder

from app.agent.calculator.excutor import Dispatcher, aggregate, average_list, sum_list

dispatcher = Dispatcher(id="dispatcher_executor")
calc_workflow = (
    WorkflowBuilder(start_executor=dispatcher)
    .add_fan_out_edges(dispatcher, [sum_list, average_list])
    .add_fan_in_edges([sum_list, average_list], aggregate)
    .build()
)
