"""Naming task scenarios and configuration."""
from dataclasses import dataclass


@dataclass
class NamingScenario:
    name: str
    system_desc: str
    expected_component_count: int = 10


SCENARIOS = [
    NamingScenario(
        name="ml-training-pipeline",
        system_desc="A distributed task queue for ML model training jobs. Components include: job submission, resource allocation, data loading, model checkpointing, gradient synchronization, failure recovery, result aggregation, scheduling, monitoring, and artifact storage.",
    ),
    NamingScenario(
        name="content-moderation-system",
        system_desc="An automated content moderation pipeline for a social platform. Components include: content ingestion, classification, human review queue, appeal handling, policy enforcement, audit logging, reporter feedback, false positive tracking, escalation routing, and metrics dashboard.",
    ),
    NamingScenario(
        name="supply-chain-tracker",
        system_desc="A real-time supply chain visibility platform. Components include: shipment tracking, inventory sync, supplier onboarding, demand forecasting, exception alerting, customs documentation, carrier integration, warehouse coordination, returns processing, and compliance reporting.",
    ),
]
