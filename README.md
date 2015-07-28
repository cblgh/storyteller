# storyteller
a small templating language and python parser for generating small stories

## The templating language
The templating language is built up out of two things: definitions and templates.

### Definitions
Definitions are comma-separated lists of words gathered under a specific name. They are declared at the top of the file 
and take the following format:
```
a templating example
@verbs: running, walking, dancing around and singing, writing a readme
@plural nouns: horses, squids, fjords, a murder of crows
``` 
You can write anything as the first line, and thereafter include as many lines of definitions you want. 
Definitions are defined with a @-symbol which is then followed by a name, and finished off by a colon. 

In addition to starting with an `@` and ending with `:`, all names also need to end with an s. 
Which is completely arbitrary! But it also felt nice when using definitions as part of templates. :100:

As seen in the example, spaces are completely fine to use as part of names.
Once you've declared all your definitions, you finish the group of definitions off with a newline. This signifies that the rest of 
the file contains templates. Or just junk, your choice. Or 50% templates, 50% junk. Any distribution of junk and templates, really.

### Templates
Templates are also grouped under a name that ends with an s and a colon. The name is then followed by one template per line,
with a newline ending that specific template group. Each template line can use the previously defined definitions to construct sentences. 

```
a template header, it's completely unnecessary and can be viewed as a comment
templates:
i am @verb with @plural noun
@plural noun hate @verb

more templates:
@plural noun, @plural noun, and @plural noun
you should have a couple of @plural noun go @verb with you

```

In addition to using definitions, templates can also use other templates.
```
meta templates:
@more template. Also fyi @template.
@template. @template.
```

### Complete example
```
a templating example
@verbs: running, walking, dancing around and singing, writing a readme
@plural nouns: horses, squids, fjords

a template header; it's completely unnecessary and can be viewed as a comment
templates:
i am @verb with @plural noun
@plural noun hate @verb

more templates:
@plural noun, @plural noun, and @plural noun
you should have a couple of @plural noun go @verb with you

meta templates:
@more template. Also fyi @template.
@template. @template.
```

#### This is probably buggy so yeah, let me know??
I also wrote this accidentally while making a bot today, so keep that in mind `O K` 
