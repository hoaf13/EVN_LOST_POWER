from .graph_config import graph

class Selector: 
    def __init__(self):
        self.graph = graph
        print(type(self.graph))

    def generate_action(self, previous2_action, previous1_action, current_intent):
        action = None
        # print("selector: {} - {}".format(previous1_action, current_intent))

        if current_intent not in self.graph[previous1_action]:
            print(current_intent, "not in", previous1_action)
            current_intent = 'intent_fallback'


        if current_intent == 'intent_fallback':
            if previous1_action == previous2_action:
                action = "action_fallback"
            else:
                action = previous1_action
            return action
        

        action = self.graph[previous1_action][current_intent]
        return action 

    

