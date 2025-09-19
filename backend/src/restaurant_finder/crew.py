import os
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool
import yaml
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class SimpleRestaurantFinder:
    def __init__(self):
        # Get API keys from environment
        self.search_tool = SerperDevTool(api_key=os.getenv("SERPER_API_KEY"))
        self.llm = LLM(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))
        self.config_dir = Path(__file__).parent / "config"
    
    def load_config(self, config_type):
        """Load YAML configuration"""
        config_path = self.config_dir / f"{config_type}.yaml"
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)
    
    def create_agents(self):
        """Create research and recommendation agents"""
        agents_config = self.load_config('agents')
        
        research_agent = Agent(
            role=agents_config['research_agent']['role'],
            goal=agents_config['research_agent']['goal'],
            backstory=agents_config['research_agent']['backstory'],
            tools=[self.search_tool],
            llm=self.llm,
            verbose=True
        )
        
        recommendation_agent = Agent(
            role=agents_config['recommendation_agent']['role'],
            goal=agents_config['recommendation_agent']['goal'],
            backstory=agents_config['recommendation_agent']['backstory'],
            llm=self.llm,
            verbose=True
        )
        
        return research_agent, recommendation_agent
    
    def create_tasks(self, agents, location="San Francisco"):
        """Create search and curation tasks"""
        tasks_config = self.load_config('tasks')
        research_agent, recommendation_agent = agents
        
        search_task = Task(
            description=tasks_config['search_restaurants']['description'].format(location=location),
            expected_output=tasks_config['search_restaurants']['expected_output'],
            agent=research_agent
        )
        
        curate_task = Task(
            description=tasks_config['curate_recommendations']['description'],
            expected_output=tasks_config['curate_recommendations']['expected_output'],
            agent=recommendation_agent,
            context=[search_task]
        )
        
        return [search_task, curate_task]
    
    def run(self, location="San Francisco"):
        """Run the restaurant finder crew"""
        print(f"🍽️ Finding restaurants in {location}...")
        
        agents = self.create_agents()
        tasks = self.create_tasks(agents, location)
        
        crew = Crew(
            agents=list(agents),
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff(inputs={"location": location})
        return result

def run():
    """Entry point for crewai run command"""
    import sys
    
    location = "San Francisco"
    if len(sys.argv) > 1:
        location = " ".join(sys.argv[1:])
    
    finder = SimpleRestaurantFinder()
    result = finder.run(location)
    
    print("\n" + "="*50)
    print("🎉 RESTAURANT RECOMMENDATIONS")
    print("="*50)
    print(result)
    
    feedback = input("\n💬 How do these look? (Enter feedback or press Enter): ")
    if feedback:
        print("Thanks for the feedback! 👍")

if __name__ == "__main__":
    run()