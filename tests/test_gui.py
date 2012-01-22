import sys
sys.path.append('..')

import urwid

from credentials import *
from turses.api import Api
from turses.timeline import Timeline
from turses.widget import TimelineBuffer, BufferList, BufferHeader

# palette
palette = [
    ('body','default', '', 'standout'),
    ('focus','dark red', '', 'standout'),
    ('header','light blue', ''),
    ('line', 'dark blue', ''),
    ('info_msg', 'dark green', ''),
    ('warn_msg', 'dark red', ''),
    ('current_tab', 'light blue', ''),
    ('other_tab', 'dark blue', ''),
    ('read', 'dark blue', ''),
    ('unread', 'dark red', ''),
    ('hashtag', 'dark green', ''),
    ('attag', 'brown', ''),
    ('highlight', 'dark red', ''),
    ('highlight_nick', 'light red', ''),
    ('help_bar', 'yellow', 'dark blue'),
    ('help_key', 'dark red', ''),
    ('header', 'white', 'black'),
    ('reveal focus', 'black', 'dark cyan', 'standout'),
]

# api
api = Api(consumer_key, consumer_secret, access_token_key, access_token_secret)
api.VerifyCredentials()
# timelines
tweets = Timeline(update_function=api.GetUserTimeline)
timeline = Timeline(api.GetFriendsTimeline)
mentions = Timeline(update_function=api.GetMentions)
search = Timeline(update_function=api.GetSearch, update_function_args='#python')

# buffers
tweets_buffer = TimelineBuffer('tweets', tweets)
tl_buffer = TimelineBuffer('timeline', timeline)
mentions_buffer = TimelineBuffer('mentions', mentions)
search_buffer = TimelineBuffer('#python', search)

buffers = [tweets_buffer, tl_buffer, mentions_buffer, search_buffer]

head = BufferHeader(' '.join([buffer.name for buffer in buffers]))
#head = urwid.AttrMap(show_key, 'header')
top = BufferList(buffers)

def show_all_input(input, raw):
    pressed = u''.join([unicode(i) for i in input])
    #show_key.set_text("Pressed " + pressed)
    if pressed == u'l':
        top.next_buffer()
    elif pressed == u'h':
        top.prev_buffer()
    elif pressed == u'r':
        top.current_buffer.update()
    elif pressed == u'd':
        top.remove_current_buffer()
    return input

def exit_on_cr(input):
    if input == 'tab':
        raise urwid.ExitMainLoop()

loop = urwid.MainLoop(top, palette, 
                      input_filter=show_all_input, unhandled_input=exit_on_cr)
loop.run()
