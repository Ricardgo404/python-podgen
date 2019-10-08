======
PodGen
======

.. image:: https://travis-ci.org/tobinus/python-podgen.svg?branch=master
    :target: https://travis-ci.org/tobinus/python-podgen

.. image:: https://readthedocs.org/projects/podgen/badge/?version=latest
   :target: http://podgen.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

Don't you wish there was a **clean and simple library** which could help you
**generate podcast RSS feeds** with your Python code? Well, today's your lucky day!

   >>> from podgen import Podcast, Episode, Media
   >>> # Create the Podcast
   >>> p = Podcast(
          name="Animals Alphabetically",
          description="Every Tuesday, biologist John Doe and wildlife "
                      "photographer Foo Bar introduce you to a new animal.",
          website="http://example.org/animals-alphabetically",
          explicit=False,
       )
   >>> # Add some episodes
   >>> p.episodes += [
          Episode(
            title="Aardvark",
            media=Media("http://example.org/files/aardvark.mp3", 11932295),
            summary="With an English name adapted directly from Afrikaans "
                    '-- literally meaning "earth pig" -- this fascinating '
                    "animal has both circular teeth and a knack for "
                    "digging.",
          ),
          Episode(
             title="Alpaca",
             media=Media("http://example.org/files/alpaca.mp3", 15363464),
             summary="Thousands of years ago, alpacas were already "
                     "domesticated and bred to produce the best fibers. "
                     "Case in point: we have found clothing made from "
                     "alpaca fiber that is 2000 years old. How is this "
                     "possible, and what makes it different from llamas?",
          ),
       ]
   >>> # Generate the RSS feed
   >>> rss = p.rss_str()

You don't need to read the RSS specification, write XML by hand or wrap your
head around ambiguous, undocumented APIs. PodGen incorporates the industry's
best practices and lets you focus on collecting the necessary metadata and
publishing the podcast.

PodGen is compatible with Python 2.7 and 3.4+.

.. warning::

   As of October 7th 2019 (v1.0.1), PodGen does not support the additions and changes
   made by Apple to their podcast standards since 2016. This includes
   the new and renamed categories, the ability to mark episodes with episode and
   season number, and the ability to mark the podcast as "serial".
   It is a goal to implement those changes in a new release in 2019.
   Please refer to the :doc:`background/roadmap`.


Contents
--------

.. toctree::
   :maxdepth: 3

   background/index
   usage_guide/index
   advanced/index
   contributing
   api


External Resources
------------------

* `Changelog <https://github.com/tobinus/python-podgen/blob/master/CHANGELOG.md>`_
* `GitHub Repository <https://github.com/tobinus/python-podgen/tree/master>`_
* `Python Package Index <https://pypi.org/project/podgen/>`_
