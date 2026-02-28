from typing import Never

from agent_framework import Executor, WorkflowContext, handler, executor

class Dispatcher(Executor):
    @handler
    async def handle(self, num_str: str, ctx: WorkflowContext[list[int], Never]) -> None:
        if not num_str:
            raise RuntimeError("必须输入整型数列表")

        await ctx.send_message([int(n) for n in num_str.split(",")])

@executor(id="sum_executor")
async def sum_list(numbers: list[int], ctx: WorkflowContext[int, Never]) -> None:
    total: int = sum(numbers)
    await ctx.send_message(total)


@executor(id="average_executor")
async def average_list(numbers: list[int], ctx: WorkflowContext[float, Never]) -> None:
    average: float = sum(numbers) / len(numbers)
    await ctx.send_message(average)

@executor(id="aggregate_executor")
async def aggregate(results: list[int | float], ctx: WorkflowContext[Never, list[int | float]]) -> None:
    await ctx.yield_output(results)
