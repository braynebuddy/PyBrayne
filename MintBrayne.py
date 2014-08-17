#!/usr/bin/env python2
import sys
import os
import willie

sys.path.append(os.path.abspath("/home/rob/.willie/modules"))
import iTwitter

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
    #t = iTwitter("yujC3tyTWH6q7XAgIvAGg", "FqVBCDdF4B3cA7dPKBFxwZmq2jD9hAq1dub7eRBHaY",
    #                   os.path.expanduser('~/.brayne_twitter_credentials'), "Brayne Buddy")
    #resp = t.get_mentions(num=1)
    #for r in resp:
    #    print r['user']['screen_name'] + " (" + r['created_at'] + "): " + r['text']

    bot.reply('You said,"' + trigger.group(2) + '"')

if __name__ == "__main__":
    from willie.test_tools import run_example_tests
    run_example_tests(__file__)
