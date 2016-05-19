from random import choice
import sys
import re

class Storyteller:
    def __init__(self, filePath):
        self.templateDict = {}
        # Capture group:
        #   Match the first character of the sentence 
        #   or
        #   Match "?", "!", or ".", and a space, and a single, random
        #   character
        self.sentenceRegex = r'(^.|[?!.] .)'
        # Theoretically, I could do this with a regex. Practically, I'm not.
        self.separators = set("?!.-,")

        #TODO: add null-space character; interpreted as no space between two
        # two things; OR split on @ instead of on separators, or something q.q
        # i want @color#beard ->Redbeard, Bluebeard etc

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
                elif ":" in line and not templateName:
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
            if any((c in self.separators) for c in token):
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
        # (r'(^.|[?!.] .)' 
        # https://lund.zozs.se/nb/2015-07-26-174041_873x55_scrot.png

        return re.sub(self.sentenceRegex, lambda m: m.group(0).upper(), story)
 
if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage: python storyteller.py 'template-file.txt'")

    storyteller = Storyteller(sys.argv[1])
    names = []
    for i in xrange(50):
        story = storyteller.tellStory()
        names.append(story)
    for name in set(names):
        print name
