#!/usr/bin/env python2
#from willie.module import command

import willie

@willie.module.commands('helloworld')
@willie.module.example('.helloworld', 'Hello, world!')
def helloworld(bot, trigger):
    """
    HelloWorld is a simple test module for willie.
    """
    bot.say('Hello, world!')

if __name__ == "__main__":
    from willie.test_toold import run_example_tests
    run_example_tests(__file__)
