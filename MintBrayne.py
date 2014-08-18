#!/usr/bin/env python2
import sys
import os
import willie
import nltk

sys.path.append(os.path.abspath("/home/rob/.willie/modules"))
import iTwitter
import WordNet

@willie.module.commands('helloworld')
@willie.module.example('.helloworld', 'Hello, world!')
def helloworld(bot, trigger):
    """
    HelloWorld is a simple test module for willie.
    """
    bot.say('Hello, world!')

@willie.module.rule(r'(\D?$nickname[,:])(.*)')
@willie.module.example('MintBrayne, Anything at all')
def respond(bot, trigger):
    #bot.reply('You said,"%s". Let me think...' % trigger.group(2))

    from nltk.corpus import wordnet as wn
    wnPOS = [wn.NOUN, wn.VERB, wn.ADJ, wn.ADV]

    words = nltk.wordpunct_tokenize(trigger.group(2))

    for w1 in words:
        parsed_words = WordNet.wordinfo(w1)
        #if len(parsed_words)==0:
        #    bot.reply("Sorry, I don't know '%s'" % w1)
        #else:
        if len(parsed_words) > 0:
            for w2 in parsed_words:
                bot.reply("%s (%s) - %s" % (w2[0], w2[1], w2[4]))
    

if __name__ == "__main__":
    from willie.test_tools import run_example_tests
    run_example_tests(__file__)
    
    #t = iTwitter("yujC3tyTWH6q7XAgIvAGg", "FqVBCDdF4B3cA7dPKBFxwZmq2jD9hAq1dub7eRBHaY",
    #                   os.path.expanduser('~/.brayne_twitter_credentials'), "Brayne Buddy")
    #resp = t.get_mentions(num=1)
    #for r in resp:
    #    print r['user']['screen_name'] + " (" + r['created_at'] + "): " + r['text']
    
