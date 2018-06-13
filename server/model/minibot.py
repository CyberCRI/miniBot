##### LOAD LIBRARIES #####
from rasa_nlu.training_data import load_data
from rasa_nlu import config
from rasa_nlu.model import Trainer
from rasa_core import utils
from rasa_core.actions import Action
from rasa_core.agent import Agent
from rasa_core.channels.console import ConsoleInputChannel
from rasa_core.events import SlotSet
from rasa_core.featurizers import (
    MaxHistoryTrackerFeaturizer,
    BinarySingleStateFeaturizer)
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.policies.memoization import MemoizationPolicy
from rasa_core.policies.keras_policy import KerasPolicy

##### TRAIN MODEL #####
def train_nlu():
    training_data = load_data('data/nluData.json')
    trainer = Trainer(config.load("nluModelConfig.yml"))
    trainer.train(training_data)
    model_directory = trainer.persist('models/nlu/', fixed_model_name="current")

    return model_directory

def train_dialogue(domain_file="data/nluDomain.yml",
                   model_path="models/dialogue",
                   training_data_file="data/stories.md"):
    agent = Agent(domain_file,
                  policies=[MemoizationPolicy(max_history=3),
                            KerasPolicy()])

    training_data = agent.load_data(training_data_file)
    agent.train(
            training_data,
            epochs=400,
            batch_size=100,
            validation_split=0.2
    )

    agent.persist(model_path)
    return agent

def train():
    train_nlu()
    train_dialogue()

#train()


##### USE MODEL #####
agent = Agent.load("models/dialogue", interpreter=RasaNLUInterpreter("models/nlu/default/current"))

def response(sentence, userID='123', show_details=False):
    agent = Agent.load("models/dialogue", interpreter=RasaNLUInterpreter("models/nlu/default/current"))
    return agent.handle_message(sentence)[0]["text"]

print(response("Hello"))
