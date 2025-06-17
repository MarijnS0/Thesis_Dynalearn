def entity_prompt(text, topic):
    prompt = f"""
    Extract the *entities* from the text below that are relevant to the topic {topic}

    Informal definition entity: An entity is a thing that exists either physically or logically. An entity may be a physical object such as an animal or a cell, an event or a process such as a response to stimuli or the conduction of impulses, or a concept such as reproduction or adaptation.

    Return your answer as a valid Python dictionary where strings are in lower case with this format:
    "entities": []

    Do *not include*:
    - *units of measurements*, such as meter (m), liter (L), ect.
    - *relations*, such as causes, depends on, ect.
    - *adjectives*, such as high, good, big, small, ect.

    Text:
    {text}

    ### examples:

    Example_input_1 = Reproductive isolation can also occur due to differences in behavior.
    Example_output_1 = "entities": ["reproductive isolation", "behavior"]

    Example_input_2 = Rudimentary organs develop in the same way as homologous organs in related species.
    Example_output_2 = "entities": ["rudimentary organs", "homologous organs", "related species"]

    Example_input_3 = For aquatic organisms, abiotic factors such as temperature, oxygen levels, salinity, light, and current play an important role.
    Example_output_3 = "entities": ["aquatic organisms", "abiotic factors", "temperature", "oxygen levels", "salinity", "light", "current"]

    Example_input_4 = The so-called β cells of the islets of Langerhans produce the hormone insulin. Insulin promotes the uptake of glucose into cells.
    Example_output_4 = "entities": ["β cells", "islets of langerhans", "insulin", "uptake of glucose", "cells"]

    Example_input_5 = If the threshold value of the receptor cell membrane is reached, a full depolarization occurs. This opens the Ca²⁺ channels. Ca²⁺ ions flow in, and the receptor cells release an excitatory neurotransmitter into a synapse with a sensory neuron.
    Example_output_5 = "entities": ["threshold value", "receptor cell membrane", "depolarization", "ca²⁺ channels", "ca²⁺ ions", "receptor cells", "excitatory neurotransmitter", "synaps", "sensory neuron"] 

    """
    return prompt

def quantity_prompt(entity_list, text):
    prompt = f"""

    You are an assistant that identifies *quantities* from a list of entities based on a sentence context.

    Definition quantity: a measurable characteristic or property of a living thing or biological process. This can include things that can increase or descrease, like the number of organisms, the amount of a molecule or substance, or the rate of a biochemical reaction. 

    ### Task:
    Given the sentence context and a list of candidate entities, return only those that represent *quantities* in this context.

    Provided entity list = {entity_list}
    Context = {text}

    ### Rules:
    - Only select items from the provided list.
    - Return your result as a valid Python dictionary: "quantities": []
    - Use only lowercase strings.

    Do *not include*:
    - structures, organs, types of cells, or locations unless they are being explicitly described in the given text as varying in measurable amount, level, concentration, or activity.

    ### examples:

    example_sentence_1 = The blood glucose concentration will therefore rise above the standard value of 5.0 mmol/L. Cells in the islets of Langerhans will then produce more insulin.
    example_entities_input_1 = ['blood glucose concentration', 'standard value', 'islets of langerhans', 'insulin']
    example_quantities_output_1 = 'quantities': ['blood glucose concentration', 'standard value', 'insulin']

    example_sentence_2 = "Mutations increase the genetic variation within a population. The environment determines what happens to the different genotypes and phenotypes in a population. If the conditions are favorable, the selection pressure is low and many variants survive. For example, if tree leaves are abundant, giraffes with the original neck length will also survive and reproduce."
    example_entities_input_2 = ['mutations', 'genetic variation', 'population', 'environment', 'environmental conditions, 'genotypes', 'phenotypes', 'selection pressure', 'variants', 'tree leaves', 'giraffes with the original neck length']
    example_quantities_output_2 = 'quantities': ['mutations', 'genetic variation', 'selection pressure', 'variants', 'tree leaves', 'giraffes with the original neck length']

    example_sentence_3 = "In your ears are the hearing receptors and the organs of balance, and in your eyes are the light receptors. Smell receptors are located in your olfactory organ at the top of the nasal cavity, and taste receptors are located in the taste buds on your tongue."
    example_entities_input_3 = ['ears', 'hearing receptors'. 'organs of balance', 'eyes', 'light receptors', 'smell receptors', 'olfactory organ', 'nasal cavity', 'taste receptors', 'taste buds', 'tongue']
    example_quantities_output_3 = 'quantities': []

    example_sentence_4 = "Co₂ lowers the level of oxyhemoglobin in the blood in two ways. It takes the place of O₂ on the heme group, and it causes a decrease in pH through a reaction with water."
    example_entities_input_4 = ['co₂', 'oxyhemoglobin', 'blood', 'o₂', 'ph', 'water', 'heme group']
    example_quantities_output_4 = 'quantities': ['co₂', 'oxyhemoglobin', 'o₂', 'ph']

    example_sentence_5 = "Rods contain the photopigment rhodopsin. The rods have a low stimulus threshold. The breakdown of rhodopsin triggers a cascade of reactions and a secondary messenger that causes the Na⁺ channels to close, leading to hyperpolarization of the rod and a decrease in the amount of neurotransmitter it releases. At high light intensity, all rhodopsin breaks down, and it takes some time before enough rhodopsin is regenerated."
    example_entities_input_5 = ['rods', 'rhodopsin', 'stimulus threshold', 'color', 'light', 'wave length', 'humans', 'secondary messenger', 'na+ channels','rod cell hyperpolarization', 'neurotransmitter', 'light intensity']
    example_quantities_output_5 = 'quantities': ['rhodopsin', 'stimulus threshold', 'wave length', 'secondary messenger', 'rod cell hyperpolarization', 'neurotransmitter', 'light intensity']

    """

    return prompt



def relations_prompt(text, entities, quantities):
    prompt = f"""

    You are an assistent that links entities and quanties based on their *relation* in a given text.
    
    text: {text}
    entities: {entities}
    quantities: {quantities}

    Allowed relation types:
    - Configuration (only between two entities)
    - Positive influence
    - Negative influence
    - Proportionally positive
    - Proportionally negative
    - Has Property

    Definition relationship types:

    Configuration: Represents a structural relationship between two entities that describes how they relate to eachother in a system.
    Positive influence: Indicates that an increase in the influencing element causes or promotes an increase in the influenced element. The effect may be indirect.
    Negative influence: Indicates that an increase in the influencing element causes or promotes a decrease in the influenced element. The effect may be indirect.
    Proportionally positive: Specifies a direct proportional relationship: when the influencing quantity increases, the affected quantity also increases in a directly measurable way.
    Proportionally negative: Specifies an inverse proportional relationship: when the influencing quantity increases, the affected quantity decreases in a directly measurable way.
    Has property: Indicates that an entity contains a quantity.

    Usage relations:
    Configuration: This relation can only be used between entities.
    Positive influence: This relation can only be used between quantities.
    Negative influence: This relation can only be used between quantities.
    Proportionally positive: This relation can only be used between quantities.
    Proportionally negative: This relation can only be used between quantities.
    Has property: This relation can only be used between an entity and a quantity.

    Rules:
    - Every used quantity must be a property to at least one entity.
    - You do not have to use all the entities and quantities, only those that are involved in a relation, described in the given text.
    - Only use elements from the provided quantity or entity list.

    Return a list of relations as (subject, relation_type, object) triples, where subject and object must be from the list entities or the list quantities.
    
    ## Examples:

    input_text_1 = "Your food almost always contains carbohydrates. These are digested in your digestive tract, primarily into glucose.
    Glucose is absorbed into the blood in the small intestine. As a result, the blood glucose concentration will rise above the
    normal value of 5.0 mmol/L. Cells in the islets of Langerhans then begin to produce more insulin. Insulin stimulates the cells
    in the body to absorb more glucose from the blood. Cells in the liver and muscles convert the glucose into glycogen.
    This glycogen is stored in these cells. As a result, the glucose concentration will decrease."

    input_entities_1 = ['food', 'carbohydrates', 'digestive tract', 'blood', 'islets of langerhans', 'liver', 'muscles', 'body']
    input_quantities_1 = ['glucose', 'glucose concentration',  'normal value', 'insulin', 'glycogen', 'glucose absorption']

    output_relations_1 = [
    ('blood','has property','glucose concentration' ),
    ('blood', 'has property','glucose'),
    ('blood', 'has property','standard value'),
    ('islets of langerhans', 'has property', 'insulin'),
    ('liver', 'has property', 'glycogen'),
    ('muscles', 'has property', 'glycogen'),
    ('food', 'has property','carbohydrates'),
    ('carbohydrates', 'positive influence', 'glucose'),
    ('digestive tract','has property', 'glucose'),
    ('small intestine', 'has property', 'glucose absorption'),
    ( 'blood', 'has property','normal value'),
    ('glucose', 'proportional positive', 'glucose absorption'),
    ('glucose absorption', 'proportional negative', 'glucose concentration'),
    ('glucose', 'positive influence', 'insulin'),
    ('insulin', 'positive proportional', 'glucose absorption'),
    ('glycogen', 'positive proportional', 'glucose')
    ]

    input_text_2 = 'In chemoreceptors and photoreceptors, just like with hormones, a signal cascade and a secondary messenger 
    are involved. The secondary messenger binds to target molecules on the ion channels, causing them to open or close. If the stimulus
    threshold of the receptor cell membrane is reached, a full depolarization occurs. This opens the Ca²⁺ channels. Ca²⁺ ions flow in,
    and the receptor cells release an excitatory neurotransmitter into a synapse with a sensory neuron. The amount of neurotransmitter 
    released determines the impulse frequency generated in the sensory neuron. This frequency conveys information about the strength of
    the stimulus. A stronger stimulus often results in a higher impulse frequency.'

    input_entities_2 = ['chemoreceptors', 'photoreceptors', 'hormones', 'ion channels', 'receptor cell', 'synaps', 'sensory neuron', 'stimulus', 'signal cascade', 'ca²⁺ channels']

    input_quantities_2 = ['stimulus threshold', 'ca²⁺ ions', 'neurotransmitter', 'impulse frequency', 'secondary messenger']

    output_relations_2 = [
    ('ion channels', 'has property', 'secondary messenger'),
    ('receptor cell', 'has property', 'stimulus threshold'),
    ('secondary messenger', 'positive influence', 'stimulus threshold'),
    ('stimulus threshold', 'proportional positive', 'ca²⁺ ions'),
    ('ca²⁺ channels', 'has property', 'ca²⁺ ions'),
    ('ca²⁺ ions', 'proportional positive', 'neurotransmitter'),
    ( 'synaps', 'has property','sensory neuron'),
    ('neurotransmitter', 'positive proportional', 'impulse frequency'),
    ('stimulus', 'positive influence', 'impulse frequency')
    ]

    input_text_3 = "In your ears are the hearing receptors and the organs of balance, and in your eyes are the light receptors. Smell receptors are located in your olfactory organ at the top of the nasal cavity, and taste receptors are located in the taste buds on your tongue."

    input_entities_3 = ['ears', 'hearing receptors'. 'organs of balance', 'eyes', 'light receptors', 'smell receptors', 'olfactory organ', 'nasal cavity', 'taste receptors', 'taste buds', 'tongue']

    input_quantities_3 = []
    
    output_relations_3 = [
    ('ears', 'configuration', 'hearing receptors'),
    ('ears', 'configuration', 'organs of balance'),
    ('eyes', 'configuration', 'light receptors'),
    ('nasal cavity', 'configuration', 'olfactory organ'),
    ('olfactory organ', 'configuration', 'smell receptors'),
    ('tongue', 'configuration', 'taste buds'),
    ('taste buds', 'configuration', 'taste receptors')
    ]

    input_text_4 = 'Rods contain the photopigment rhodopsin. Even weak illumination causes this pigment to break down:
    rods have a low stimulus threshold. The color of the light does not play a role in this, as long as it is a wavelength
    visible to humans. The breakdown of rhodopsin triggers a cascade of reactions and a secondary messenger, which causes the
    Na⁺ channels to close, the rod cell to hyperpolarize, and the amount of neurotransmitter it releases to decrease.
    Under high light intensity, all rhodopsin breaks down, and it takes some time before enough rhodopsin is reformed.'

    input_entities_4 = ['rods', 'color', 'light', 'humans', 'na⁺ channels', 'rod cell']

    input_quantities_4 = ['rhodopsin', 'stimulus threshold', 'wavelength', 'secondary messenger', 'neurotransmitter', 'light intensity', 'hyperpolarization', 'rhodopsin breakdown']

    output_relations_4 = [
        ('rods', 'has property', 'rhodopsin'),
        ('rods', 'has property', 'stimulus threshold'),
        ('rods', 'has property', 'secondary messenger'),
        ('rod cell', 'has property', 'hyperpolarization'),
        ('secondary messenger', 'positive proportional', 'hyperpolarization'),
        ('rod cell', 'has property', 'neurotransmitter'),
        ('secondary messenger', 'negative proportional', 'neurotransmitter'),
        ('rods', 'has property', 'rhodopsin breakdown'),
        ('rods', 'has property', 'light intensity'),
        ('light intensity', 'positive proportional', 'rhodopsin breakdown'),
        ('rhodopsin breakdown', 'positive influence', 'secondary messenger')
    ]

    input_text_5 = 'Mutations increase the genetic variation within a population. Environmental conditions
    determine what happens to the different genotypes and phenotypes in a population. When conditions are favorable,
    selection pressure is low, and many different variants survive. For example, if tree leaves are abundant, giraffes
    with the original neck length will also survive and reproduce. But if conditions are unfavorable, selection pressure is high,
    and individuals with the original neck length will die due to a lack of food.'

    input_entities_5 = ['population', 'environmental conditions', 'genotypes', 'phenotypes', 'environment']

    input_quantities_5 = ['mutations', 'genetic variation', 'selection pressure', 'different variants', 'tree leaves', 'giraffes with the original neck length']

    output_relations_5 = [
        ('population', 'has property', 'mutations'),
        ('population', 'has property', 'genetic variation'),
        ('environment', 'has property', 'environmental conditions'),
        ('population', 'has property', 'selection pressure'),
        ('environmental conditions', 'negative influence', 'selection pressure'),
        ('selection pressure', 'negative influence', 'different variants'),
        ('environment', 'has property', 'tree leaves'),
        ('population', 'has property', 'giraffes with the original neck length'),
        ('tree leaves', 'positive influence', 'environmental conditions'),
        ('selection pressure', 'negative influence', 'giraffes with the original neck length'),
        ('population', 'has property', 'genotypes'),
        ('population', 'has property', 'phenotypes')
    ]

    """

    return prompt


def expansion_entities(text, entity_list, topic,  increase):
    
    prompt = f""" 
    Given this list of entities: {entity_list} 
    and this text {text}

    expand the entity list by {increase} percent, prioritizing the more important entities based on the topic {topic}.

    Informal definition entity: An entity is a thing that exists either physically or logically. An entity may be a physical object such as an animal or a cell, an event or a process such as a response to stimuli or the conduction of impulses, or a concept such as reproduction or adaptation.

    Return your answer as a valid Python dictionary where strings are in lower case with this format:
    "entities": []

    Rules:

    - Use all entities in the current list, only add entities.
    - Only add entities that are given in the text provided.
    - When all possible entities are extracted, do not increase the list further.
    
    
    Do *not include*:
    - *units of measurements*, such as meter (m), liter (L), ect.
    - *relations*, such as causes, depends on, ect.
    - *adjectives*, such as high, good, big, small, ect.


    Examples (not taken into account the amount of increase):

    example_text_input1 = Reproductive isolation can also occur due to differences in behavior.
    example_entities_input_1 = ["reproductive isolation"]
    example_expansion_entities_output_1 = "entities": ["reproductive isolation", "behavior"]

    example_text_input_2 = Rudimentary organs develop in the same way as homologous organs in related species.
    example_entities_input_2 = ["rudimentary organs", "homologous organs"]
    example_expansion_entities_output_2 = "entities": ["rudimentary organs", "homologous organs", "related species"]

    example_text_input_3 = For aquatic organisms, abiotic factors such as temperature, oxygen levels, salinity, light, and current play an important role.
    example_entities_input_3 = ["aquatic organisms", "temperature", "oxygen levels"]
    example_expansion_entities_output_3 = "entities": ["aquatic organisms", "abiotic factors", "temperature", "oxygen levels", "salinity", "light", "current"]

    example_text_input_4 = The so-called β cells of the islets of Langerhans produce the hormone insulin. Insulin promotes the uptake of glucose into cells.
    example_entities_input_4 = ["β cells", "islets of langerhans", "insulin"]
    example_expansion_entities_ouput_4 = "entities": ["β cells", "islets of langerhans", "insulin", "uptake of glucose", "cells"]

    example_text_input_5 = If the threshold value of the receptor cell membrane is reached, a full depolarization occurs. This opens the Ca²⁺ channels. Ca²⁺ ions flow in, and the receptor cells release an excitatory neurotransmitter into a synapse with a sensory neuron.
    example_entities_input_5 = ["threshold value", "receptor cell membrane", "ca²⁺ channels", "ca²⁺ ions", "receptor cells", "synaps"]
    example_expansion_entities_output_5 = "entities": ["threshold value", "receptor cell membrane", "depolarization", "ca²⁺ channels", "ca²⁺ ions", "receptor cells", "excitatory neurotransmitter", "synaps", "sensory neuron"]

    """

    return prompt

def contraction_entities(text, entity_list, topic, decrease):

    prompt = f"""
    Given this list of entities: {entity_list}
    and this text: {text}

    contract the entity list by {decrease} percent, prioritizing the more important entities based on the topic {topic}.

    Return your answer as a valid Python dictionary where strings are in lower case with this format:
    "entities": []

    Rules:

    - Only use entities from the entity list for the new refined entity list.
    - Only use the most important entities from the given entity list based on the topic {topic} and the provided text.
    """
    return prompt

def expansion_quantities(text, entity_list, quantity_list, topic,  increase):
    
    prompt = f""" 
    From this list of entities: {entity_list}, these are the ones that are identified as quantities: {quantity_list}.
    These list are made based on a text extracted from a secondary education textbook: {text}.

    Expand the quantity list by {increase} percent, by identifying more entities as quantities, prioritizing the more important quantities of the entity list based on the topic {topic}. 

    Definition quantity: a measurable characteristic or property of a living thing or biological process. This can include things like the number of individuals in a population, the amount of a specific molecule, or the rate of a biochemical reaction. 


    Rules:

    - Use all quantities in the current list, only add quantities to the current quantity list.
    - Only add quantities that are also present in the entity list.
    - When all possible quantities are identified, do not increase the list further.
    - Return your answer as a valid Python dictionary where strings are in lower case with this format: "quantities": []

    Do *not include*:
    - structures, organs, types of cells, or locations unless they are being explicitly described in the given text as varying in measurable amount, level, concentration, or activity.


    Examples (not taken into account the amount of increase):

    example_input_sentence 1 = The blood glucose concentration will therefore rise above the standard value of 5.0 mmol/L. Cells in the islets of Langerhans will then produce more insulin.
    example_entities_input_1 = ['blood glucose concentration', 'standard value', 'islets of langerhans', 'insulin']
    example_quantities_input_1 = ['blood glucose concentration', 'insulin']
    example_quantities_output_1 = 'quantities': ['blood glucose concentration', 'standard value', 'insulin']

    example_input_sentence_2 = "Mutations increase the genetic variation within a population. The environment determines what happens to the different genotypes and phenotypes in a population. If the conditions are favorable, the selection pressure is low and many variants survive. For example, if tree leaves are abundant, giraffes with the original neck length will also survive and reproduce."
    example_entities_input_2 = ['mutations', 'genetic variation', 'population', 'environment', 'environmental conditions, 'genotypes', 'phenotypes', 'selection pressure', 'variants', 'tree leaves', 'giraffes with the original neck length']
    example_quantities_input_2 = ['mutations', 'genetic variation', 'selection pressure', 'variants']
    example_quantities_output_2 = 'quantities': ['mutations', 'genetic variation', 'selection pressure', 'variants', 'tree leaves', 'giraffes with the original neck length']

    example_input_sentence_3 = "Rods contain the photopigment rhodopsin. The rods have a low stimulus threshold. The breakdown of rhodopsin triggers a cascade of reactions and a secondary messenger that causes the Na⁺ channels to close, leading to hyperpolarization of the rod and a decrease in the amount of neurotransmitter it releases. At high light intensity, all rhodopsin breaks down, and it takes some time before enough rhodopsin is regenerated."
    example_entities_input_3 = ['rods', 'rhodopsin', 'stimulus threshold', 'color', 'light', 'wave length', 'humans', 'secondary messenger', 'na+ channels','rod cell hyperpolarization', 'neurotransmitter', 'light intensity']
    example_quantities_input_3 = ['rhodopsin', 'stimulus threshold', 'secondary messenger', 'light intensity']
    example_quantities_ouput_3 = 'quantities': ['rhodopsin', 'stimulus threshold', 'wave length', 'secondary messenger', 'rod cell hyperpolarization', 'neurotransmitter', 'light intensity']

    #example of no possible expansion
    example_input_sentence_4 = "In your ears are the hearing receptors and the organs of balance, and in your eyes are the light receptors. Smell receptors are located in your olfactory organ at the top of the nasal cavity, and taste receptors are located in the taste buds on your tongue."
    example_entities_input_4 = ['ears', 'hearing receptors'. 'organs of balance', 'eyes', 'light receptors', 'smell receptors', 'olfactory organ', 'nasal cavity', 'taste receptors', 'taste buds', 'tongue']
    example_quantities_input_4 = []
    example_quantities_output_4 = 'quantities': []

    # example of no possible expansion
    example_input_sentence_5 = "Co₂ lowers the level of oxyhemoglobin in the blood in two ways. It takes the place of O₂ on the heme group, and it causes a decrease in pH through a reaction with water."
    example_entities_input_5 = ['co₂', 'oxyhemoglobin', 'blood', 'o₂', 'ph', 'water', 'heme group']
    example_quantities_input_5 = ['co₂', 'oxyhemoglobin', 'o₂', 'ph']
    example_quantities_output_5 = 'quantities': ['co₂', 'oxyhemoglobin', 'o₂', 'ph']



    """

    return prompt

def contraction_quantities(text, entity_list, quantity_list, topic, decrease):

    prompt = f"""
    From this list of entities: {entity_list}, these are the ones that are identified as quantities: {quantity_list}.
    These list are made based on a text extracted from a secondary education textbook: {text}.

    Contract the quantity list by {decrease} percent, prioritizing the more important quantities from the entity list based on the topic {topic}.

    Definition quantity: a measurable characteristic or property of a living thing or biological process. This can include things like the number of individuals in a population, the amount of a specific molecule, or the rate of a biochemical reaction. 

    Rules:

    - Only use quantities from the existing quantity list for the new refined quantity list.
    - Only use the most important quantities from the given quantity list based on the topic {topic}, the entity list, and the provided text.
    - Return your answer as a valid Python dictionary where strings are in lower case with this format: "quantities": []
    """
    return prompt



def expansion_relations(text, entity_list, quantity_list, relation_list, topic,  increase):
    
    prompt = f""" 
    From this list of entities: {entity_list}, and this list of quantities: {quantity_list}, these relations are extracted: {relation_list}
    based on this secondary education text: {text}.

    Expand the relations list by {increase} percent, by extracting relations between the provided quantities, the provided entities or both out of the provided text, prioritizing the more important relations based on the topic {topic}. 

    Allowed relation types:
    - Configuration (only between two entities)
    - Positive influence
    - Negative influence
    - Proportionally positive
    - Proportionally negative
    - Has Property

    Definition relationship types:

    Configuration: Represents a structural, spatial, or organizational relationship between two entities. It indicates how two entities are arranged or associated within a system.
    Positive influence: Indicates that an increase in the influencing element causes or promotes an increase in the influenced element. The effect may be indirect or qualitative, not strictly proportional.
    Negative influence: Indicates that an increase in the influencing element causes or promotes a decrease in the influenced element. The effect may be indirect or qualitative, not strictly proportional.
    Proportionally positive: Specifies a direct proportional relationship: when the influencing quantity increases, the affected quantity also increases in a directly measurable way.
    Proportionally negative: Specifies an inverse proportional relationship: when the influencing quantity increases, the affected quantity decreases in a directly measurable way..
    Property: Indicates that a quantity, belongs to or describes an entity.

    Usage relations:
    Configuration: This relation can only be used between entities.
    Positive influence: This relation can only be used between quantities.
    Negative influence: This relation can only be used between quantities.
    Proportionally positive: This relation can only be used between quantities.
    Proportionally negative: This relation can only be used between quantities.
    Has property: This relation can only be used between an entity and a quantity.

    Rules:

    - Use all relations in the current list, only add relations to the current relation list.
    - Only use the provided entities or quantities for the new relations.
    - Every used quantity must be a property to at least one entity.
    - When all possible relations are extracted, do not increase the list further.
    - If no new relations can be extracted, return the original relation list unchanged.
    - You can increase the list to be a maximum of 200 relations.
    - You do not have to use all the entities and quantities, only those that are involved in a relation, described in the given text.
    - Return a list of relations as [subject, relation_type, object] triples, where subject and object must be from the list entities or the list quantities. Do not include any explanation, text, or variable name. Do not use code blocks. Do not use parentheses or tuples.

    Examples:

    example_input_text_1 = "Your food almost always contains carbohydrates. These are digested in your digestive tract, primarily into glucose.
    Glucose is absorbed into the blood in the small intestine. As a result, the blood glucose concentration will rise above the
    normal value of 5.0 mmol/L. Cells in the islets of Langerhans then begin to produce more insulin. Insulin stimulates the cells
    in the body to absorb more glucose from the blood. Cells in the liver and muscles convert the glucose into glycogen.
    This glycogen is stored in these cells. As a result, the glucose concentration will decrease."

    example_input_entities_1 = ['food', 'carbohydrates', 'digestive tract', 'blood', 'islets of langerhans', 'liver', 'muscles', 'body']
    example_input_quantities_1 = ['glucose', 'glucose concentration',  'normal value', 'insulin', 'glycogen', 'glucose absorption']

    example_input_relations_1 = [
    ('blood','has property','glucose concentration' ),
    ('islets of langerhans', 'has property', 'insulin'),
    ('liver', 'has property', 'glycogen'),
    ('muscles', 'has property', 'glycogen'),
    ('food', 'has property','carbohydrates'),
    ('carbohydrates', 'positive influence', 'glucose'),
    ('small intestine', 'has property', 'glucose absorption'),
    ('blood', 'has property','normal value'),
    ('glucose', 'proportional positive', 'glucose absorption'),
    ('glucose', 'positive influence', 'insulin'),
    ('insulin', 'positive proportional', 'glucose absorption'),
    ('glycogen', 'positive proportional', 'glucose')
    ]

    example_output_relation_1 = [
    ('blood','has property','glucose concentration'),
    ('blood', 'has property','glucose'),
    ('blood', 'has property','standard value'),
    ('islets of langerhans', 'has property', 'insulin'),
    ('liver', 'has property', 'glycogen'),
    ('muscles', 'has property', 'glycogen'),
    ('food', 'has property','carbohydrates'),
    ('carbohydrates', 'positive influence', 'glucose'),
    ('digestive tract','has property', 'glucose'),
    ('small intestine', 'has property', 'glucose absorption'),
    ( 'blood', 'has property','normal value of 5.0 mmol/L'),
    ('glucose', 'proportional positive', 'glucose absorption'),
    ('glucose absorption', 'proportional negative', 'glucose concentration'),
    ('glucose', 'positive influence', 'insulin'),
    ('insulin', 'positive proportional', 'glucose absorption'),
    ('glycogen', 'positive proportional', 'glucose')
    ]

    example_input_text_2 = 'In chemoreceptors and photoreceptors, just like with hormones, a signal cascade and a secondary messenger 
    are involved. The secondary messenger binds to target molecules on the ion channels, causing them to open or close. If the stimulus
    threshold of the receptor cell membrane is reached, a full depolarization occurs. This opens the Ca²⁺ channels. Ca²⁺ ions flow in,
    and the receptor cells release an excitatory neurotransmitter into a synapse with a sensory neuron. The amount of neurotransmitter 
    released determines the impulse frequency generated in the sensory neuron. This frequency conveys information about the strength of
    the stimulus. A stronger stimulus often results in a higher impulse frequency.'

    example_input_entities_2 = ['chemoreceptors', 'photoreceptors', 'hormones', 'ion channels', 'receptor cell', 'synaps', 'sensory neuron', 'stimulus', 'signal cascade', 'ca²⁺ channels']

    example_input_quantities_2 = ['stimulus threshold', 'ca²⁺ ions', 'neurotransmitter', 'impulse frequency', 'secondary messenger']

    example_input_relations_2 = [
    ('ion channels', 'has property', 'secondary messenger'),
    ('secondary messenger', 'positive influence', 'stimulus threshold'),
    ('stimulus threshold', 'proportional positive', 'ca²⁺ ions'),
    ('ca²⁺ channels', 'has property', 'ca²⁺ ions'),
    ('ca²⁺ ions', 'proportional positive', 'neurotransmitter'),
    ('neurotransmitter', 'positive proportional', 'impulse frequency'),
    ]

    example_output_relations_2 = [
    ('ion channels', 'has property', 'secondary messenger'),
    ('receptor cell', 'has property', 'stimulus threshold'),
    ('secondary messenger', 'positive influence', 'stimulus threshold'),
    ('stimulus threshold', 'proportional positive', 'ca²⁺ ions'),
    ('ca²⁺ channels', 'has property', 'ca²⁺ ions'),
    ('ca²⁺ ions', 'proportional positive', 'neurotransmitter'),
    ( 'synaps', 'has property','sensory neuron'),
    ('neurotransmitter', 'positive proportional', 'impulse frequency'),
    ('stimulus', 'positive influence', 'impulse frequency')
    ]

    example_input_text_3 = 'This explains the complex transport of CO₂. Without the binding of H⁺ ions—produced from carbonic acid
    formation—to hemoglobin (Hb), the pH of the blood would drop to pH = 3. In reality, the pH of arterial blood is about 7.40,
    and in venous blood about 7.36. The heme groups of hemoglobin bind most of the H⁺ ions. Other proteins in the blood plasma 
    also bind H⁺ ions. Hemoglobin and the other proteins act as buffering agents and function as pH buffers. The blood pH remains
    between 7.35 and 7.45 despite fluctuations in the concentration of H⁺ ions, to which substances like lactic acid also contribute.
    The drop in pH and the increased pCO₂ in the blood during increasing physical exertion are stimuli to breathe more rapidly.
    The heart rate also increases, which accelerates the removal of CO₂.

    example_input_entities_3 = ['blood', 'arterial blood', 'venous blood', 'blood plasma', 'heme groups', 'buffering agents', 'ph buffers']

    example_input_quantities_3 = ['co₂', 'h+ ions', 'hemoglobin', 'ph', 'h+ ions binding', 'proteins', 'lactic acid', 'pco2', 'heart rate']

    example_input_relations_3 = [
    ('blood', 'has property','ph'),
    ('blood plasma', 'has property', 'proteins'),
    ('heme groups', 'has property', 'h+ ions binding'),
    ('blood plasma', 'has property', 'h+ ions binding'),
    ('blood', 'has property', 'pco2'),
    ('blood', 'has property', 'heart rate'),
    ('blood', 'has property', 'co₂'),
    ('hemoglobin', 'positive influence', 'h+ ions binding'),
    ('proteins', 'positive influence', 'h+ ions binding'),
    ('pco2', 'positive influence', 'heart rate'),
    ('heart rate', 'negative proportional', 'co₂')
    ]

    example_output_relations_3 = [
    ('blood', 'has property','ph'),
    ('arterial blood', 'has property', 'ph'),
    ('venous blood', 'has property','ph'),
    ('heme groups', 'has property', 'hemoglobin'),
    ('blood plasma', 'has property', 'proteins'),
    ('heme groups', 'has property', 'h+ ions binding'),
    ('blood plasma', 'has property', 'h+ ions binding'),
    ('blood', 'has property', 'pco2'),
    ('blood', 'has property', 'heart rate'),
    ('blood', 'has property', 'co₂'),
    ('h+ ions binding', 'positive proportional', 'ph'),
    ('hemoglobin', 'positive influence', 'h+ ions binding'),
    ('proteins', 'positive influence', 'h+ ions binding'),
    ('ph', 'negative influence', 'heart rate'),
    ('pco2', 'positive influence', 'heart rate'),
    ('heart rate', 'negative proportional', 'co₂')
    ]

    # example of no possible expansion
    example_input_text_4 = "In your ears are the hearing receptors and the organs of balance, and in your eyes are the light receptors. Smell receptors are located in your olfactory organ at the top of the nasal cavity, and taste receptors are located in the taste buds on your tongue."
    example_input_entities_4 = ['ears', 'hearing receptors'. 'organs of balance', 'eyes', 'light receptors', 'smell receptors', 'olfactory organ', 'nasal cavity', 'taste receptors', 'taste buds', 'tongue']
    example_input_quantities_4 = []
    example_input_relations_4 = [
    ('ears', 'configuration', 'hearing receptors'),
    ('ears', 'configuration', 'organs of balance'),
    ('eyes', 'configuration', 'light receptors'),
    ('nasal cavity', 'configuration', 'olfactory organ'),
    ('olfactory organ', 'configuration', 'smell receptors'),
    ('tongue', 'configuration', 'taste buds'),
    ('taste buds', 'configuration', 'taste receptors')
    ]

    example_output_relations_4 = [
    ('ears', 'configuration', 'hearing receptors'),
    ('ears', 'configuration', 'organs of balance'),
    ('eyes', 'configuration', 'light receptors'),
    ('nasal cavity', 'configuration', 'olfactory organ'),
    ('olfactory organ', 'configuration', 'smell receptors'),
    ('tongue', 'configuration', 'taste buds'),
    ('taste buds', 'configuration', 'taste receptors')
    ]

    # example of no possible expansion

    example_input_text_5 = 'Mutations increase the genetic variation within a population. Environmental conditions
    determine what happens to the different genotypes and phenotypes in a population. When conditions are favorable,
    selection pressure is low, and many different variants survive. For example, if tree leaves are abundant, giraffes
    with the original neck length will also survive and reproduce. But if conditions are unfavorable, selection pressure is high,
    and individuals with the original neck length will die due to a lack of food.'

    example_input_entities_5 = ['population', 'environmental conditions', 'genotypes', 'phenotypes', 'environment']

    example_input_quantities_5 = ['mutations', 'genetic variation', 'selection pressure', 'different variants', 'tree leaves', 'giraffes with the original neck length']

    example_input_relations_5 = [
        ('population', 'has property', 'mutations'),
        ('population', 'has property', 'genetic variation'),
        ('environment', 'has property', 'environmental conditions'),
        ('population', 'has property', 'selection pressure'),
        ('environmental conditions', 'negative influence', 'selection pressure'),
        ('selection pressure', 'negative influence', 'different variants'),
        ('environment', 'has property', 'tree leaves'),
        ('population', 'has property', 'giraffes with the original neck length'),
        ('tree leaves', 'positive influence', 'environmental conditions'),
        ('selection pressure', 'negative influence', 'giraffes with the original neck length'),
        ('population', 'has property', 'genotypes'),
        ('population', 'has property', 'phenotypes')
    ]

    example_output_relations_5 = [
        ('population', 'has property', 'mutations'),
        ('population', 'has property', 'genetic variation'),
        ('environment', 'has property', 'environmental conditions'),
        ('population', 'has property', 'selection pressure'),
        ('environmental conditions', 'negative influence', 'selection pressure'),
        ('selection pressure', 'negative influence', 'different variants'),
        ('environment', 'has property', 'tree leaves'),
        ('population', 'has property', 'giraffes with the original neck length'),
        ('tree leaves', 'positive influence', 'environmental conditions'),
        ('selection pressure', 'negative influence', 'giraffes with the original neck length'),
        ('population', 'has property', 'genotypes'),
        ('population', 'has property', 'phenotypes')
    ]
    """

    return prompt

def contraction_relations(text, entity_list, quantity_list, relation_list, topic, decrease):

    prompt = f"""

    From this list of entities: {entity_list}, and this list of quantities: {quantity_list}, these relations are extracted: {relation_list}
    based on this secondary education text: {text}.

    Contract the relations list by {decrease} percent, prioritizing the more important relations based on the topic {topic}. 

    Allowed relation types:
    - Configuration (only between two entities)
    - Positive influence
    - Negative influence
    - Proportionally positive
    - Proportionally negative
    - Has Property

    Definition relationship types:

    Configuration: Represents a structural, spatial, or organizational relationship between two entities. It indicates how two entities are arranged or associated within a system.
    Positive influence: Indicates that an increase in the influencing element causes or promotes an increase in the influenced element. The effect may be indirect or qualitative, not strictly proportional.
    Negative influence: Indicates that an increase in the influencing element causes or promotes a decrease in the influenced element. The effect may be indirect or qualitative, not strictly proportional.
    Proportionally positive: Specifies a direct proportional relationship: when the influencing quantity increases, the affected quantity also increases in a directly measurable way.
    Proportionally negative: Specifies an inverse proportional relationship: when the influencing quantity increases, the affected quantity decreases in a directly measurable way..
    Property: Indicates that a quantity, belongs to or describes an entity.

    Usage relations:
    Configuration: This relation can only be used between entities.
    Positive influence: This relation can only be used between quantities.
    Negative influence: This relation can only be used between quantities.
    Proportionally positive: This relation can only be used between quantities.
    Proportionally negative: This relation can only be used between quantities.
    Has property: This relation can only be used between an entity and a quantity.

    

    Rules:
    - Only use relations from the existing relation list for the new refined relation list.
    - Only use the most important relations from the given relation list based on the topic {topic} and the provided text.
    - Return a list of relations as [subject, relation_type, object] triples, where subject and object must be from the list entities or the list quantities. Do not include any explanation, text, or variable name. Do not use code blocks. Do not use parentheses or tuples.

    """
    return prompt


