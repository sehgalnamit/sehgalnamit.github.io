---
layout: post
title: "Dual-Engine System 2 Architecture: Unifying Declarative Rules and Procedural World Models"
date: 2026-09-23
author: Namit Sehgal
excerpt: "Executive Summary While System 1 provides the fast, deterministic, sub-100ms execution layer for enterprise AI platforms, System 2 governs complex, long-horizon decision-making. However, pure text-bas"
hashnode_url: https://articles.namitsehgal.com/dual-engine-system-2-architecture-unifying-declarative-rules-and-procedural-world-models
---

## Executive Summary

While **System 1** provides the fast, deterministic, sub-100ms execution layer for enterprise AI platforms, **System 2** governs complex, long-horizon decision-making. However, pure text-based Chain-of-Thought (CoT) and static agent scaffolds break down when encountering unstructured edge cases, non-deterministic API failures, or implicit business constraints.

To achieve enterprise-grade reliability, System 2 must unify two complementary paradigms:

1. **Declarative Reasoning Engine ("What must be true"):** Evaluates business rules, domain invariants, regulatory compliance, and constraint satisfiability prior to and during plan execution.
2. **Procedural World Models ("How to act"):** Construct dynamic Directed Acyclic Graphs (DAGs) with explicit node dependencies, preconditions, and localized error-repair loops.

By enforcing a strict separation between declarative domain logic and procedural execution topologies, enterprise agents eliminate hardcoded business rules, prune non-compliant search spaces early, and achieve verifiable long-horizon task completion with minimal token bloat.

## Architectural Dataflow & Dual-Engine State Model

The System 2 runtime receives compacted state payloads from System 1. The **Declarative Engine** first validates invariants and prunes the action space; then, the **Procedural Planner** builds the execution topology, handles tool invocations, and dynamically repairs graph nodes upon failure.

![](https://cdn.hashnode.com/uploads/covers/6a157ef2da253d50d4a02fc4/cbcd6a85-1440-41d9-8b23-549dbf007886.png)

## Declarative vs. Procedural Matrix

| Dimension | Declarative Knowledge Engine | Procedural Graph World Model |
| --- | --- | --- |
| **Core Intent** | Defines domain facts, regulatory constraints, and invariants (*What must be true*). | Defines step execution, dependency tracking, and tool orchestration (*How to act*). |
| **Primitives** | Entities, Logical Relations, Invariants, Assertions. | DAG Nodes, Tool Adapters, Preconditions, Repair Handlers. |
| **Evaluation Strategy** | Pattern Matching, Constraint Satisfaction, Resolution. | Topological Sort, Graph Traversal, Dynamic Node Repair. |
| **Failure Mode** | Policy Constraint Violation / Unstatisfiability. | Precondition Failure / API Exception / Blocked Edge. |
| **Optimization** | Declarative Policy Store updates (zero model retrain). | Co-evolution of harness scaffolding & model weights. |

## Production Code Implementation (Python)

```
import asyncio
import logging
import time
from typing import Any, Dict, List, Optional, Tuple
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("System2DualEngine")

# =====================================================================
# 1. Declarative Domain Constraints & Invariants
# =====================================================================

class PolicyInvariant(BaseModel):
    rule_id: str
    description: str

    def evaluate(self, facts: Dict[str, Any]) -> bool:
        """Evaluates logical constraints over current state facts."""
        raise NotImplementedError


class MaxLTVInvariant(PolicyInvariant):
    rule_id: str = "POL_LTV_MAX_80"
    description: str = "Loan-to-Value (LTV) ratio must not exceed 0.80 (80%)."

    def evaluate(self, facts: Dict[str, Any]) -> bool:
        ltv = facts.get("ltv_ratio", 0.0)
        return ltv <= 0.80


class DeclarativeKnowledgeEngine:
    """Evaluates business rules, regulatory constraints, and domain facts."""

    def __init__(self, invariants: List[PolicyInvariant]):
        self.invariants = invariants

    def validate_state(self, facts: Dict[str, Any]) -> Tuple[bool, List[str]]:
        violations = []
        for invariant in self.invariants:
            if not invariant.evaluate(facts):
                violations.append(f"[{invariant.rule_id}] {invariant.description}")
        return len(violations) == 0, violations


# =====================================================================
# 2. Procedural World Model & Graph Execution Engine
# =====================================================================

class GraphNode(BaseModel):
    node_id: str
    action_type: str
    preconditions: List[str]
    is_completed: bool = False
    result_payload: Optional[Dict[str, Any]] = None


class ProceduralGraphPlan(BaseModel):
    graph_id: str
    nodes: Dict[str, GraphNode]
    execution_order: List[str]


class System2DualEnginePlanner:
    """Unified System 2 Planner combining Declarative Guardrails with Procedural Graph Execution."""

    def __init__(self):
        self.declarative_engine = DeclarativeKnowledgeEngine([MaxLTVInvariant()])

    async def build_procedural_graph(self, prompt: str) -> ProceduralGraphPlan:
        logger.info("[System 2 Procedural] Constructing Directed Graph Topology...")
        start_time = time.perf_counter()

        await asyncio.sleep(0.1)  # Simulate graph construction overhead

        node_1 = GraphNode(
            node_id="node_fetch_credit",
            action_type="FETCH_CREDIT_SCORE",
            preconditions=["valid_user_identity"]
        )
        node_2 = GraphNode(
            node_id="node_evaluate_risk",
            action_type="RUN_UNDERWRITING_MODEL",
            preconditions=["node_fetch_credit"]
        )
        node_3 = GraphNode(
            node_id="node_generate_offer",
            action_type="GENERATE_LOAN_OFFER",
            preconditions=["node_evaluate_risk"]
        )

        plan = ProceduralGraphPlan(
            graph_id="grp_99812",
            nodes={node.node_id: node for node in [node_1, node_2, node_3]},
            execution_order=["node_fetch_credit", "node_evaluate_risk", "node_generate_offer"]
        )

        elapsed = (time.perf_counter() - start_time) * 1000
        logger.info(f"[System 2 Procedural] Graph built with {len(plan.nodes)} nodes in {elapsed:.2f}ms")
        return plan

    async def execute_plan(self, plan: ProceduralGraphPlan, runtime_facts: Dict[str, Any]) -> Dict[str, Any]:
        total_start = time.perf_counter()
        logger.info("[System 2 Execution] Commencing dual declarative-procedural pipeline...")

        # Step 1: Pre-flight Declarative Verification
        is_valid, violations = self.declarative_engine.validate_state(runtime_facts)
        if not is_valid:
            logger.error(f"[Declarative Engine] Pre-flight policy block: {violations}")
            return {"status": "BLOCKED_BY_POLICY", "violations": violations}

        # Step 2: Procedural Graph Traversal with Mid-Flight Declarative Auditing
        completed_nodes = {}
        for node_id in plan.execution_order:
            node = plan.nodes[node_id]
            logger.info(f"[Procedural Graph] Executing Node '{node.node_id}' ({node.action_type})...")

            # Verify preconditions
            for pre in node.preconditions:
                if pre.startswith("node_") and pre not in completed_nodes:
                    logger.warning(f"[Graph Repair] Missing precondition '{pre}' for node '{node_id}'. Repairing...")
                    await asyncio.sleep(0.05)

            # Simulate tool execution
            await asyncio.sleep(0.1)

            # Simulated state update mid-flight
            if node_id == "node_evaluate_risk":
                runtime_facts["ltv_ratio"] = 0.75  # Safe boundary state

            # Mid-Flight Invariant Audit
            is_valid, violations = self.declarative_engine.validate_state(runtime_facts)
            if not is_valid:
                logger.error(f"[Declarative Engine] Invariant violated after node '{node_id}': {violations}")
                return {
                    "status": "ABORTED_INVARIANT_VIOLATION",
                    "failed_node": node_id,
                    "violations": violations
                }

            node.is_completed = True
            node.result_payload = {"status": "SUCCESS", "node_id": node_id}
            completed_nodes[node_id] = node.result_payload

        elapsed = (time.perf_counter() - total_start) * 1000
        return {
            "status": "SUCCESS",
            "executed_nodes": list(completed_nodes.keys()),
            "total_latency_ms": round(elapsed, 2)
        }


async def main():
    planner = System2DualEnginePlanner()
    
    # Context facts initialized from System 1
    facts = {"user_id": "usr_991", "ltv_ratio": 0.72}
    
    plan = await planner.build_procedural_graph("Synthesize debt restructuring offer")
    result = await planner.execute_plan(plan, facts)
    print(f"\nExecution Result:\n{result}")


if __name__ == "__main__":
    asyncio.run(main())
```

## Operational Analysis & Trajectory Modeling

The efficiency gains of graph repair and declarative early pruning versus unconstrained Chain-of-Thought (CoT) token consumption can be modeled in R:

```
# Load libraries
library(ggplot2)
library(dplyr)

# Simulation data: Linear CoT vs Dual-Engine Procedural Graph
steps <- 1:10
linear_cot_tokens <- steps * 1200          # Compound context bloat on failure
procedural_graph_tokens <- steps * 150     # Isolated node repair cost

comparison_df <- data.frame(
  Step = rep(steps, 2),
  Token_Cost = c(linear_cot_tokens, procedural_graph_tokens),
  Approach = rep(c("Linear CoT Retry", "Dual-Engine Graph Repair"), each = 10)
)

# Render Token Consumption Trajectory
ggplot(comparison_df, aes(x = Step, y = Token_Cost, color = Approach, group = Approach)) +
  geom_line(size = 1.2) +
  geom_point(size = 3) +
  theme_minimal() +
  labs(
    title = "Token Accumulation Under Execution Failure Recovery",
    x = "Workflow Depth (Steps)",
    y = "Accumulated Token Consumption"
  ) +
  scale_color_manual(values = c("Linear CoT Retry" = "#EF4444", "Dual-Engine Graph Repair" = "#10B981"))
```

## Key Takeaway

Architecting enterprise-grade System 2 planners requires moving beyond unstructured prompting toward a unified **Declarative-Procedural Dual Engine**. By decoupling business rule verification (declarative) from execution pathing and graph repair (procedural), AI systems achieve predictable long-horizon execution, continuous compliance, and strictly bounded operational costs.
