import class_сharacteristic as chr


class Prompt_c: ##################################### characteristics
    def __init__(self, max_len_telegram_message, collection_characteristics):
        self.max_len_telegram_message = max_len_telegram_message
        self.characteristics = []
        records = collection_characteristics.find() # requests is not an async pkg
        for record in records:
             self.characteristics.append(chr.Characteristic(record['score'], record['str']))

    def __str__(self): ###
        return (f"Prompt_c(Max Message Length: {self.max_len_telegram_message}, Characteristics: "
            f"{', '.join([charact for charact in self.characteristics])})")


    def examples(self, collection_messages):
        examples_cursor = collection_messages.find({"to_use_c": True}).limit(5)

        # Check the count using the collection's count_documents method
        if collection_messages.count_documents({"to_use_c": True}) == 0:
            return ""

        string = "Take into consideration these corrections of your previous responses :\n"
        for example in examples_cursor: # sum
            string += str(example)

        return string

    def to_string(self, message, collection_messages):
        try:
            string = f"""\
                Analyze the following message and provide its characteristics.\
                Reply by numbers, one number for each criterion and nothing else.\n\n\
                {message.text[0:self.max_len_telegram_message]}\n\n"""
            for characteristic in self.characteristics:
                string += f"{self.characteristics.index(characteristic)}. " + characteristic.to_string()
            return string + self.examples(collection_messages)
            
        except TypeError as e:
            print("some mistake")
            #print(e)
            return

    def characteristics_to_string(self):
        string = ""
        for characteristic in self.characteristics:
            string += f"{str(self.characteristics.index(characteristic)).ljust(2)} {characteristic.name}\n"
        return (string)

class Prompt_a: ################################### affirmations
    def __init__(self, max_len_telegram_message):
        self.max_len_message = max_len_telegram_message

    def __str__(self):
        return f"Prompt_a(Max Message Length: {self.max_len_message})"

    def examples(self, coll_affirmations):
        examples = coll_affirmations.find({"to_use_a": True}).limit(5) # await ?
        if coll_affirmations.count_documents({"to_use_a": True}) == 0:
            return ""
        string = "For example. Here I provide examples already checked by gpt-4, with corrections = result that should appear instead, or close to it. You need understand what I mean with these examples and strictly follow :"
        for example in examples:
            string += f"\n\nMessage: {example['text']}"
            string += f"\nAffirmations: {str(example['affirmations'])}"
            string += f"\nCorrected Affirmations: {str(example['affirmations_corrections'])}"
        if len(string) == 0:
            return ""
        return string

    def to_string(self, message, collection_messages):
        # try:
        string = (
            "Please generate binary affirmations from the provided news message:\n\n"
            f"\"{message.text}\"\n\n"  # Use double quotes around the message text
            "For each affirmation:\n\n"
            "1. Extract key assertions from the message.\n"
            "2. Convert negations into their positive counterparts.\n"
            "3. Each affirmation must be standalone and provide full context. If there's an attributed source in the message, ensure it's included in the affirmation.\n"
            "4. Provide a truth value for each affirmation based on its accuracy within the message.\n\n"
            "The result should be in this format (without anything else, no introduciton, no description, nothing, just this):\n"
            "{\n"
            "    \"Binary affirmation 1\": true/false,\n"  # Use double quotes for keys
            "    \"Binary affirmation 2\": true/false,\n"  # and values in the dictionary
            "    ...\n"
            "}\n\n"
            "Ensure that each binary affirmation is concise, clear, and independent. They should almost function as a unique hash of the information they contain. And always in English no matter what language of the news\n"
        )

        # If you need to strip leading/trailing whitespace
        string = string.strip()

        return string + self.examples(collection_messages)
        # except TypeError:
        #     return ("")


####################################################### ARCHIVE, MAY BE TO USE LATER
class Prompt_s:
    def __init__(self, max_len_message):
        self.max_len_message = max_len_message

    def to_string(self, message1, message2):
            return f"""\
            Do these two messages tell about the same subject(s) AND they express similar opinions on this subject(s)?\n\
            Reply by number, one number and nothing else.\n\n\
            First message : {message1.text[0:self.max_len_message]}\n\n\
            Seconde messsage: {message2.text[0:self.max_len_message]}\n\n\
            Reply 1 if yes, 0 if no, 0 if you are not sure"""