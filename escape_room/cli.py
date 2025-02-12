import click

from .core import create_model, run_agent
from .room_tools import get_tool
from .prompts import SOLVE_PROBLEM


@click.command()
@click.option("--tools", "-t", multiple=True)
@click.option("--problem", "-p", prompt="What is the problem?")
@click.option("--situation", "-s", prompt="What is the situation?")
@click.option("--model", "-m", default="ollama_chat/deepseek-r1:14b")
def main(tools, problem, situation, model):
    """A agent that solves a problem given a situation and a set of tools"""
    model = create_model(model)
    state = {'LOCKED': True}
    run_agent(
        tools=[get_tool(state, t) for t in tools],
        model=model,
        problem_statement=SOLVE_PROBLEM.format(
            problem=problem, situation=situation
        ),
    )


if __name__ == "__main__":
    main()
