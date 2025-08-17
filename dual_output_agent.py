#!/usr/bin/env python3
"""
Dual Output Decision-Making Agent

This agent provides two outputs:
1. Text file with decision-making logic using parameters like OR/IF/THEN
2. Mermaid flowchart for visual representation
"""

import json
import os
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path


class DualOutputDecisionAgent:
    """
    Agent that generates both decision logic text and Mermaid flowcharts.
    """
    
    def __init__(self):
        self.decision_tree = {}
        self.logic_rules = []
        self.conditions = []
        self.actions = []
    
    def create_emergency_room_logic(self) -> Tuple[str, str]:
        """Generate both logic text and Mermaid for emergency room decisions."""
        
        # Decision logic text
        logic_text = """EMERGENCY ROOM DECISION LOGIC
================================

IF patient_experiencing_symptoms THEN
    IF severe_symptoms = TRUE THEN
        action = call_911_immediately
        outcome = emergency_transport
    ELSE IF severe_symptoms = FALSE THEN
        evaluate_urgency_level()
        
        IF urgency_level = HIGH THEN
            IF urgent_care_available = TRUE THEN
                action = visit_emergency_room
                outcome = receive_urgent_care
            ELSE
                action = schedule_primary_care
                outcome = receive_standard_care
        ELSE IF urgency_level = LOW THEN
            action = schedule_primary_care
            outcome = receive_standard_care
        END IF
    END IF
END IF

CONDITION DEFINITIONS:
- severe_symptoms: chest_pain OR difficulty_breathing OR severe_bleeding OR loss_of_consciousness
- high_urgency: temperature > 39°C OR severe_pain OR breathing_difficulty
- urgent_care_available: emergency_room_wait_time < 2_hours

ACTION PRIORITIES:
1. life_threatening = call_911
2. high_urgency = emergency_room
3. low_urgency = primary_care
"""

        # Mermaid flowchart
        mermaid_chart = """```mermaid
flowchart TD
    A[Patient experiencing symptoms] --> B{Severe symptoms?}
    B -->|Yes| C[Call 911 immediately]
    B -->|No| D[Evaluate urgency level]
    C --> E[Emergency transport]
    D --> F{Urgent care needed?}
    F -->|High urgency| G{Emergency room available?}
    F -->|Low urgency| H[Schedule primary care]
    G -->|Yes| I[Visit emergency room]
    G -->|No| H
    H --> J[Receive standard care]
    I --> K[Receive urgent care]
    E --> K
    J --> L[Decision complete]
    K --> L
```"""

        return logic_text, mermaid_chart
    
    def create_software_deployment_logic(self) -> Tuple[str, str]:
        """Generate both logic text and Mermaid for software deployment decisions."""
        
        logic_text = """SOFTWARE DEPLOYMENT DECISION LOGIC
===================================

IF code_ready_for_deployment THEN
    IF all_tests_passing = TRUE THEN
        IF code_review_required = TRUE THEN
            request_code_review()
            
            IF review_approved = TRUE THEN
                proceed_to_staging()
            ELSE
                fix_review_comments()
                GOTO code_review_required
            END IF
        ELSE
            proceed_to_staging()
        END IF
        
        staging_deployment()
        
        IF staging_tests_pass = TRUE THEN
            production_deployment()
            monitor_deployment()
            outcome = deployment_successful
        ELSE
            rollback_deployment()
            outcome = deployment_failed
        END IF
    ELSE
        fix_failing_tests()
        GOTO all_tests_passing
    END IF
END IF

GATE CONDITIONS:
- all_tests_passing: unit_tests AND integration_tests AND security_tests
- code_review_required: team_size > 3 OR production_system
- staging_tests_pass: functional_tests AND performance_tests

ROLLBACK TRIGGERS:
- error_rate > 1%
- response_time > 2x_baseline
- critical_functionality_broken
"""

        mermaid_chart = """```mermaid
flowchart TD
    A[Code ready for deployment] --> B{All tests passing?}
    B -->|No| C[Fix failing tests]
    C --> B
    B -->|Yes| D{Code review required?}
    D -->|Yes| E[Request code review]
    D -->|No| F[Proceed to staging]
    E --> G{Review approved?}
    G -->|No| H[Fix review comments]
    H --> E
    G -->|Yes| F
    F --> I[Staging deployment]
    I --> J{Staging tests pass?}
    J -->|No| K[Rollback deployment]
    J -->|Yes| L[Production deployment]
    L --> M[Monitor deployment]
    M --> N[Deployment successful]
    K --> O[Deployment failed]
    N --> P[Process complete]
    O --> P
```"""

        return logic_text, mermaid_chart
    
    def create_business_investment_logic(self) -> Tuple[str, str]:
        """Generate both logic text and Mermaid for business investment decisions."""
        
        logic_text = """BUSINESS INVESTMENT DECISION LOGIC
===================================

IF investment_opportunity_identified THEN
    conduct_market_research()
    
    IF market_size > $1M THEN
        analyze_competitive_landscape()
        
        IF competitive_advantage = TRUE THEN
            conduct_financial_analysis()
            
            IF ROI > 20% AND payback_period < 3_years THEN
                assess_risks()
                
                IF risk_score < risk_tolerance THEN
                    action = proceed_with_investment
                    outcome = investment_approved
                ELSE IF risk_score >= risk_tolerance THEN
                    IF renegotiation_possible = TRUE THEN
                        renegotiate_terms()
                        GOTO conduct_financial_analysis
                    ELSE
                        action = decline_investment
                        outcome = investment_rejected
                    END IF
                END IF
            ELSE
                action = decline_investment
                outcome = investment_rejected
            END IF
        ELSE
            action = decline_investment
            outcome = investment_rejected
        END IF
    ELSE
        action = decline_investment
        outcome = investment_rejected
    END IF
END IF

EVALUATION CRITERIA:
- market_size: total_addressable_market > $1M
- competitive_advantage: unique_value_proposition OR cost_advantage OR differentiation
- ROI_calculation: (expected_return - investment_cost) / investment_cost
- risk_score: market_risk + execution_risk + financial_risk + regulatory_risk
- risk_tolerance: organization_risk_appetite AND available_capital
"""

        mermaid_chart = """```mermaid
flowchart TD
    A[Investment opportunity identified] --> B[Conduct market research]
    B --> C{Market size > $1M?}
    C -->|No| D[Decline investment]
    C -->|Yes| E[Analyze competitive landscape]
    E --> F{Competitive advantage?}
    F -->|No| D
    F -->|Yes| G[Conduct financial analysis]
    G --> H{ROI > 20% AND payback < 3 years?}
    H -->|No| D
    H -->|Yes| I[Assess risks]
    I --> J{Risk score < tolerance?}
    J -->|Yes| K[Proceed with investment]
    J -->|No| L{Renegotiation possible?}
    L -->|Yes| M[Renegotiate terms]
    M --> G
    L -->|No| D
    K --> N[Investment approved]
    D --> O[Investment rejected]
    N --> P[Decision complete]
    O --> P
```"""

        return logic_text, mermaid_chart
    
    def save_dual_outputs(self, topic: str, logic_text: str, mermaid_chart: str, 
                         output_dir: str = "./decision_outputs"):
        """Save both logic text and mermaid chart to files."""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Save logic text
        logic_file = output_path / f"{topic}_logic.txt"
        with open(logic_file, 'w') as f:
            f.write(logic_text)
        
        # Save mermaid chart
        mermaid_file = output_path / f"{topic}_flowchart.md"
        with open(mermaid_file, 'w') as f:
            f.write(mermaid_chart)
        
        return str(logic_file), str(mermaid_file)
    
    def generate_all_examples(self, output_dir: str = "./decision_outputs"):
        """Generate all example decision outputs."""
        examples = [
            ("emergency_room", self.create_emergency_room_logic),
            ("software_deployment", self.create_software_deployment_logic),
            ("business_investment", self.create_business_investment_logic)
        ]
        
        generated_files = []
        
        for name, generator in examples:
            logic_text, mermaid_chart = generator()
            logic_file, mermaid_file = self.save_dual_outputs(
                name, logic_text, mermaid_chart, output_dir
            )
            generated_files.extend([logic_file, mermaid_file])
            print(f"Generated: {name}_logic.txt")
            print(f"Generated: {name}_flowchart.md")
        
        return generated_files


def main():
    """Generate all example decision outputs."""
    agent = DualOutputDecisionAgent()
    
    # Create output directory
    output_dir = "./decision_outputs"
    
    print("Generating dual-output decision files...")
    files = agent.generate_all_examples(output_dir)
    
    print(f"\nGenerated {len(files)} files in {output_dir}:")
    for file_path in files:
        print(f"  - {file_path}")


if __name__ == "__main__":
    main()
