# Twitter Finger

I saw [any.io](http://any.io)'s finger service and it looked awesome,
but there was no source code so I figured I'd write one while sitting
around.

I did this in twisted because it was way easy and figured there was a
need for a thousand or so concurrent finger requests to be handled at
any given point in time.

# Usage

## Getting Ready:

    git clone git://github.com/dustin/finger-twitter.git
    cd finger-twitter
    git submodule init
    git submodule update

## Running

Any sort of variant that makes sense for your deployment with twistd.
A quick interactive example:

    twistd -ny finger.tac
