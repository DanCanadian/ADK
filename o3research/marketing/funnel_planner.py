import time
from google.adk import Agent
from o3research.lifecycle import finish_run, start_run
from .prompt_observability import record_prompt


class FunnelPlannerAgent(Agent):
    """Create a simple marketing funnel with actions for each stage."""

    def __init__(self) -> None:
        super().__init__(name="FunnelPlannerAgent")

    def run(self, product_type: str, goal: str) -> str:  # type: ignore[override]
        """Return funnel stages for the given product and goal."""
        start_run(self.name)
        start = time.perf_counter()
        ref = "docs/performance_marketing/reforge_growth_loops.md lines 9-25"
        goal_lower = goal.lower()
        tofu_action = "subscribe" if goal_lower == "lead" else "learn more"
        mofu_action = "request demo" if goal_lower == "sale" else "download guide"
        bofu_action = "purchase" if goal_lower == "sale" else "contact sales"
        lines = [
            f"Funnel plan for {product_type} ({goal_lower} goal):",
            "TOFU: awareness content -> blogs, social videos",
            f"  - Primary CTA: {tofu_action}",
            "MOFU: education -> webinars, case studies",
            f"  - Primary CTA: {mofu_action}",
            "BOFU: conversion -> pricing page, retargeting ads",
            f"  - Primary CTA: {bofu_action}",
            f"(See {ref})",
        ]
        result = "\n".join(lines)
        latency = time.perf_counter() - start
        latency = time.perf_counter() - start
        record_prompt(
            "funnel_plan",
            self.name,
            result,
            timing=latency,
            cost=0.0,
        )
        finish_run(self.name)
        return result


if __name__ == "__main__":  # pragma: no cover
    agent = FunnelPlannerAgent()
    print(agent.run("software", "lead"))
