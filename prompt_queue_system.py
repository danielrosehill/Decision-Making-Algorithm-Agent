#!/usr/bin/env python3
"""
Prompt Queue System

Processes prompts from txt/markdown files in queued/ folder
Executes them when script runs, then moves to run/ folder for tracking.
"""

import json
import os
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

from dual_output_agent import DualOutputDecisionAgent


class PromptQueueSystem:
    """
    Manages prompt queue processing with automatic execution and tracking.
    """
    
    def __init__(self, base_dir: str = "./prompts"):
        self.base_dir = Path(base_dir)
        self.queued_dir = self.base_dir / "queued"
        self.run_dir = self.base_dir / "run"
        
        # Create directories if they don't exist
        self.queued_dir.mkdir(parents=True, exist_ok=True)
        self.run_dir.mkdir(parents=True, exist_ok=True)
        
        self.agent = DualOutputDecisionAgent()
        self.execution_log = []
    
    def get_queued_prompts(self) -> List[Path]:
        """Get list of all queued prompts (txt and markdown files)."""
        queued_files = []
        
        # Find .txt files
        txt_files = list(self.queued_dir.glob("*.txt"))
        # Find .md files
        md_files = list(self.queued_dir.glob("*.md"))
        
        queued_files.extend(txt_files)
        queued_files.extend(md_files)
        
        return sorted(queued_files)
    
    def read_prompt_content(self, prompt_file: Path) -> Dict[str, str]:
        """Read and parse prompt file content."""
        content = prompt_file.read_text(encoding='utf-8')
        
        # Extract metadata and content
        lines = content.strip().split('\n')
        metadata = {}
        prompt_content = []
        
        # Simple parsing - lines starting with # or --- are metadata
        for line in lines:
            line = line.strip()
            if line.startswith('#') and ':' in line:
                key, value = line[1:].split(':', 1)
                metadata[key.strip()] = value.strip()
            elif line.startswith('---'):
                continue
            else:
                prompt_content.append(line)
        
        return {
            'filename': prompt_file.name,
            'content': '\n'.join(prompt_content).strip(),
            'metadata': metadata,
            'timestamp': datetime.now().isoformat()
        }
    
    def process_prompt(self, prompt_data: Dict[str, str]) -> Dict[str, Any]:
        """Process a single prompt and generate outputs."""
        content = prompt_data['content']
        
        # Determine topic from content
        topic = self.extract_topic(content)
        
        # Generate appropriate decision logic and mermaid based on content
        if 'emergency' in content.lower() or 'hospital' in content.lower():
            logic_text, mermaid_chart = self.agent.create_emergency_room_logic()
        elif 'software' in content.lower() or 'deployment' in content.lower():
            logic_text, mermaid_chart = self.agent.create_software_deployment_logic()
        elif 'business' in content.lower() or 'investment' in content.lower():
            logic_text, mermaid_chart = self.agent.create_business_investment_logic()
        else:
            # Default to business investment for generic prompts
            logic_text, mermaid_chart = self.agent.create_business_investment_logic()
        
        return {
            'prompt': prompt_data,
            'topic': topic,
            'logic_text': logic_text,
            'mermaid_chart': mermaid_chart,
            'processed_at': datetime.now().isoformat()
        }
    
    def extract_topic(self, content: str) -> str:
        """Extract topic from prompt content."""
        content_lower = content.lower()
        
        if 'emergency' in content_lower:
            return 'emergency_room'
        elif 'software' in content_lower or 'deployment' in content_lower:
            return 'software_deployment'
        elif 'business' in content_lower or 'investment' in content_lower:
            return 'business_investment'
        else:
            return 'generic_decision'
    
    def move_to_run(self, prompt_file: Path, result: Dict[str, Any]):
        """Move processed prompt to run folder with results."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = prompt_file.stem
        
        # Create run subdirectory for this prompt
        run_subdir = self.run_dir / f"{timestamp}_{base_name}"
        run_subdir.mkdir(exist_ok=True)
        
        # Move original prompt
        new_prompt_path = run_subdir / prompt_file.name
        shutil.move(str(prompt_file), str(new_prompt_path))
        
        # Save results
        logic_file = run_subdir / "decision_logic.txt"
        logic_file.write_text(result['logic_text'])
        
        mermaid_file = run_subdir / "flowchart.md"
        mermaid_file.write_text(result['mermaid_chart'])
        
        # Save metadata
        metadata_file = run_subdir / "execution_metadata.json"
        metadata = {
            'original_prompt': prompt_file.name,
            'processed_at': result['processed_at'],
            'topic': result['topic'],
            'files_generated': [
                str(logic_file.name),
                str(mermaid_file.name)
            ]
        }
        metadata_file.write_text(json.dumps(metadata, indent=2))
        
        return {
            'prompt_file': str(new_prompt_path),
            'logic_file': str(logic_file),
            'mermaid_file': str(mermaid_file),
            'metadata_file': str(metadata_file)
        }
    
    def process_all_prompts(self) -> List[Dict[str, Any]]:
        """Process all queued prompts."""
        queued_prompts = self.get_queued_prompts()
        
        if not queued_prompts:
            print("No prompts found in queue.")
            return []
        
        results = []
        print(f"Processing {len(queued_prompts)} prompts...")
        
        for prompt_file in queued_prompts:
            print(f"Processing: {prompt_file.name}")
            
            # Read prompt
            prompt_data = self.read_prompt_content(prompt_file)
            
            # Process prompt
            result = self.process_prompt(prompt_data)
            
            # Move to run folder
            files_created = self.move_to_run(prompt_file, result)
            
            # Log execution
            execution_record = {
                'original_file': prompt_file.name,
                'topic': result['topic'],
                'files_created': files_created,
                'processed_at': result['processed_at']
            }
            
            results.append(execution_record)
            print(f"  ✓ Generated: decision_logic.txt")
            print(f"  ✓ Generated: flowchart.md")
            print()
        
        return results
    
    def get_run_history(self) -> List[Dict[str, Any]]:
        """Get history of all processed prompts."""
        run_history = []
        
        # List all run subdirectories
        run_subdirs = [d for d in self.run_dir.iterdir() if d.is_dir()]
        run_subdirs.sort(key=lambda x: x.name, reverse=True)
        
        for subdir in run_subdirs:
            metadata_file = subdir / "execution_metadata.json"
            if metadata_file.exists():
                metadata = json.loads(metadata_file.read_text())
                run_history.append(metadata)
        
        return run_history
    
    def create_sample_prompts(self):
        """Create sample prompts for testing."""
        sample_prompts = [
            {
                "filename": "emergency_room_prompt.txt",
                "content": """# Topic: Emergency Room Decision Making
# Description: NHS guidelines for when to visit emergency room

Create a decision-making flowchart for when patients should visit the emergency room during medical emergencies. Include criteria for severe symptoms, urgency levels, and appropriate care pathways."""
            },
            {
                "filename": "software_deployment_prompt.md",
                "content": """# Topic: Software Deployment
# Description: Decision tree for deploying software to production

Generate a comprehensive decision-making flowchart for software deployment processes. Include code review requirements, testing gates, staging validation, and rollback procedures."""
            },
            {
                "filename": "business_investment_prompt.txt",
                "content": """# Topic: Business Investment
# Description: Investment decision framework for startups

Create a decision-making framework for evaluating business investment opportunities. Include market analysis, competitive assessment, financial evaluation, and risk assessment criteria."""
            }
        ]
        
        for prompt_data in sample_prompts:
            prompt_file = self.queued_dir / prompt_data["filename"]
            prompt_file.write_text(prompt_data["content"])
            print(f"Created sample prompt: {prompt_file.name}")


def main():
    """Main execution function."""
    queue_system = PromptQueueSystem()
    
    # Check if queue is empty and create samples
    queued_prompts = queue_system.get_queued_prompts()
    
    if not queued_prompts:
        print("Queue is empty. Creating sample prompts...")
        queue_system.create_sample_prompts()
        queued_prompts = queue_system.get_queued_prompts()
    
    # Process all prompts
    results = queue_system.process_all_prompts()
    
    # Display summary
    print("\n" + "="*50)
    print("PROCESSING SUMMARY")
    print("="*50)
    print(f"Prompts processed: {len(results)}")
    
    for result in results:
        print(f"\n{result['original_file']} -> {result['topic']}")
        print(f"  Files created:")
        for file_type, file_path in result['files_created'].items():
            if file_type != 'prompt_file':
                print(f"    - {file_path}")


if __name__ == "__main__":
    main()
