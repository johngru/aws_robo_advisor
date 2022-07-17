### Required Libraries ###
from datetime import datetime
from dateutil.relativedelta import relativedelta

### Functionality Helper Functions ###
def parse_int(n):
    """
    Securely converts a non-integer value to integer.
    """
    try:
        return int(n)
    except ValueError:
        return float("nan")

def parse_float(n):
    """
    Securely converts a non-numeric value to float.
    """
    try:
        return float(n)
    except ValueError:
        return float("nan")
    

def build_validation_result(is_valid, violated_slot, message_content):
    """
    Define a result message structured as Lex response.
    """
    if message_content is None:
        return {"isValid": is_valid, "violatedSlot": violated_slot}

    return {
        "isValid": is_valid,
        "violatedSlot": violated_slot,
        "message": {"contentType": "PlainText", "content": message_content},
    }


def validate_data(age, investment_amount, risk_level, intent_request):
    """
    Validates the data provided by the user.
    """

    # Validate that age is greater than zero and less than 65
    if age is not None:
        age = parse_int(
            age
        )     
        if (age<0):
            return build_validation_result(
                False,
                "age",
                "Please enter a valid age greater than 0."
            )
        elif (age>=65):
            return build_validation_result(
                False,
                "age",
                "Sorry, this service is intended for ages less than 65."
            )

    # Validate the investment amount, it should be equal to or greater than 5000
    if investment_amount is not None:
        investment_amount = parse_float(
            investment_amount
        )  # Since parameters are strings it's important to cast values
        if investment_amount < 5000:
            return build_validation_result(
                False,
                "investmentAmount",
                "The investment amount should be equal to or greater than $5,000.00."
            )
    # Ensure risk_level is typed correctly:
    if risk_level is not None:
        risk_level = risk_level.lower()
        risk_levels = ['none',
                      'low',
                      'medium',
                      'high']
        if (risk_levels.count(risk_level)==0):
            return build_validation_result(
                False,
                "riskLevel",
                "Please enter a valid risk-level: None, Low, Medium, High"
            )
    # A True results is returned if age or amount are valid
    return build_validation_result(True, None, None)    



### Dialog Actions Helper Functions ###
def get_slots(intent_request):
    """
    Fetch all the slots and their values from the current intent.
    """
    return intent_request["currentIntent"]["slots"]


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    """
    Defines an elicit slot type response.
    """

    return {
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": "ElicitSlot",
            "intentName": intent_name,
            "slots": slots,
            "slotToElicit": slot_to_elicit,
            "message": message,
        },
    }


def delegate(session_attributes, slots):
    """
    Defines a delegate slot type response.
    """

    return {
        "sessionAttributes": session_attributes,
        "dialogAction": {"type": "Delegate", "slots": slots},
    }


def close(session_attributes, fulfillment_state, message):
    """
    Defines a close slot type response.
    """

    response = {
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": fulfillment_state,
            "message": message,
        },
    }

    return response

### Intents Handlers ###
def recommend_portfolio(intent_request):
    """
    Performs dialog management and fulfillment for recommending a portfolio.
    """

    first_name = get_slots(intent_request)["firstName"]
    age = get_slots(intent_request)["age"]
    investment_amount = get_slots(intent_request)["investmentAmount"]
    risk_level = get_slots(intent_request)["riskLevel"]
    source = intent_request["invocationSource"]

    
    if source == "DialogCodeHook":
        # This code performs basic validation on the supplied input slots.

        # Gets all the slots
        slots = get_slots(intent_request)

        # Validates user's input using the validate_data function
        validation_result = validate_data(age, investment_amount, risk_level, intent_request)

        # If the data provided by the user is not valid,
        # the elicitSlot dialog action is used to re-prompt for the first violation detected.
        if not validation_result["isValid"]:
            slots[validation_result["violatedSlot"]] = None  # Cleans invalid slot

            # Returns an elicitSlot dialog to request new data for the invalid slot
            return elicit_slot(
                intent_request["sessionAttributes"],
                intent_request["currentIntent"]["name"],
                slots,
                validation_result["violatedSlot"],
                validation_result["message"],
            )

        # Fetch current session attributes
        output_session_attributes = intent_request["sessionAttributes"]

        # Once all slots are valid, a delegate dialog is returned to Lex to choose the next course of action.
        return delegate(output_session_attributes, get_slots(intent_request))    
    
    # Ensure risk_level is proper case and initialize recommendation variable:
    
    recommendation=""
    
    if risk_level is not None:
        risk_level = risk_level.lower()
       
        recommendations = {
            "none": "100% bonds (AGG), 0% equities (SPY)",
            "low":"60% bonds (AGG), 40% equities (SPY)",
            "medium":"40% bonds (AGG), 60% equities (SPY)",
            "high":"20% bonds (AGG), 80% equities (SPY)"
        }
        
        recommendation = recommendations[risk_level]
    
    return close(
        intent_request["sessionAttributes"],
        "Fulfilled",
        {
            "contentType": "PlainText",
            "content": """Thank you for entering your information;
            Based on your {} risk level, I recommend a portfolio mix
            of {}.
            """.format(
                risk_level, recommendation
            ),
        },
    )
   
### Intents Dispatcher ###
def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    intent_name = intent_request["currentIntent"]["name"]

    # Dispatch to bot's intent handlers
    if intent_name == "recommendPortfolio":
        return recommend_portfolio(intent_request)

    raise Exception("Intent with name " + intent_name + " not supported")


### Main Handler ###
def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """

    return dispatch(event)
