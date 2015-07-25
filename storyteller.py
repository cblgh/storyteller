from random import choice
class Storyteller:
    def __init__(self, filePath):
        self.templateDict = {}

        with open(filePath) as templates:
            lines = templates.readlines()
            readAllDefinitions = False
            templateName = ""

            for line in lines:
                if line.startswith("@") and not readAllDefinitions: 
                    definitionLine = line.split(": ")
                    # Empty definition; continue to the next one
                    if len(definitionLine) < 2:
                        continue
                    definitionName, definitionList = definitionLine
                    definitionList = [definition.strip() for definition in definitionList.split(", ")]
                    self.templateDict[definitionName] = definitionList
                # Stop reading definitions
                elif line in ["\n", "\r\n"]:
                    readAllDefinitions = True
                    templateName = ""
                elif ":" in line:
                    templateName = "@" + line.strip(":\n\r")
                    self.templateDict[templateName] = []
                    continue
                elif templateName:
                    self.templateDict[templateName].append(line.strip())
                else:
                    continue

    def pick(self, key):
        return choice(self.templateDict[key])

    def populateTemplate(self, template):
        tokenizedTemplate = template.split()
        sentence = []
        lookingForCompositeToken = False
        compositeToken = ""
        hasIndefiniteArticle = False

        for index, token in enumerate(tokenizedTemplate):
            word = token
            separator = ""
            if "," in token or "." in token:
                separator = token[-1]
                token = token[:-1]
            if "@" in token:
                if token + "s" in self.templateDict:
                    word = self.pick(token + "s")
                    word += separator
                else:
                    lookingForCompositeToken = True
                    compositeToken += token
                    continue
            # The definition is a multiple worded one, start composing a multiword
            # token until we find it in our template dictionary
            elif lookingForCompositeToken:
                compositeToken += " " + token
                if compositeToken + "s" in self.templateDict:
                    word = self.pick(compositeToken + "s") + separator
                    lookingForCompositeToken = False
                    compositeToken = ""
            elif token == "a/an":
                hasIndefiniteArticle = True
            sentence.append(word)

        # Fix and replace any indefinite articles that were found
        if hasIndefiniteArticle:
            for index, word in enumerate(sentence):
                if word == "a/an":
                    character = sentence[index+1][0:1]
                    sentence[index] = "a"
                    if character in "aeiou":
                        sentence[index] = "an"
        sentence = " ".join(sentence)

        # There are more templates to be filled!
        if sentence.find("@") != -1:
            sentence = self.populateTemplate(sentence)
        return sentence

    def tellStory(self):
        template = self.pick("@meta templates")
        story = self.populateTemplate(template)
        return ". ".join([word[0:1].upper() + word[1:] for word in story.split(". ")])

if __name__ == "__main__":
    storyteller = Storyteller("templates.txt")
    print storyteller.tellStory()
