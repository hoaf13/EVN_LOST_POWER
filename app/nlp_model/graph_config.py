# Desciption: ALL THE LOWEST-LEVEL NODE MUST BE DIRECTED TO "END or FORWARD" NODE  

#action
nodes = ['action_start','action_dont_clear'\
,'action_all_field','action_only_home','action_provide_name'\
,'action_provide_address','action_fallback'\
,'action_all_field_yes','action_all_field_no'\
,'action_provide_address_yes','action_provide_address_no'\
,'end','forward']

#intent
edges = ['intent_provide_district','intent_dont_clear','intent_all_field'\
,'intent_only_home','intent_provide_name','intent_provide_address','intent_fallback'\
,'yes','no' # requests API
,'straight' 
] 

graph = dict()
for node in nodes:
	graph[node] = dict()
	
graph['action_start']['intent_fallback'] = 'action_fallback'
graph['action_start']['intent_provide_address'] = 'action_provide_address'

graph['action_provide_address']['intent_fallback'] = 'action_fallback'
graph['action_provide_address']['intent_dont_clear'] = 'action_dont_clear'
graph['action_provide_address']['intent_all_field'] = 'action_all_field'
graph['action_provide_address']['intent_only_home'] = 'action_only_home'

graph['action_fallback']['straight'] = 'forward' 
graph['action_dont_clear']['straight'] = 'end'
graph['action_all_field']['yes'] = 'action_all_field_yes' #request to API-EVN_SCHEDULE to check whether it been scheduled 	 
graph['action_all_field']['no'] = 'action_all_field_no'
graph['action_only_home']['intent_fallback'] = 'action_fallback'
graph['action_only_home']['intent_provide_name'] = 'action_provide_name'

graph['action_all_field_yes']['straight'] = 'end'
graph['action_all_field_yes']['straight'] = 'end'
graph['action_provide_name']['intent_fallback'] = 'action_fallback'
graph['action_provide_name']['intent_provide_address'] = 'action_provide_address'

graph['action_provide_address']['yes'] = 'action_provide_address_yes' #request to API-USER to check if existed user
graph['action_provide_address']['no'] = 'action_provide_address_no'

graph['action_provide_address_yes']['straight'] = 'end'
graph['action_provide_address_no']['straight'] = 'end' 
