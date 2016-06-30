# -*- coding: utf-8 -*-

"""
Tests for a basic feed

These are test cases for a basic feed.
A basic feed does not contain entries so far.
"""

import unittest
from lxml import etree

from feedgen.person import Person
from ..feed import Podcast
import feedgen.version
import datetime
import dateutil.tz
import dateutil.parser

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):

        fg = Podcast()

        self.nsContent = "http://purl.org/rss/1.0/modules/content/"
        self.nsDc = "http://purl.org/dc/elements/1.1/"
        self.nsItunes = "http://www.itunes.com/dtds/podcast-1.0.dtd"
        self.feedUrl = "http://example.com/feeds/myfeed.rss"

        self.title = 'Some Testfeed'

        self.author = Person('John Doe', 'john@example.de')

        self.linkHref = 'http://example.com'
        self.description = 'This is a cool feed!'

        self.language = 'en'

        self.cloudDomain = 'example.com'
        self.cloudPort = '4711'
        self.cloudPath = '/ws/example'
        self.cloudRegisterProcedure = 'registerProcedure'
        self.cloudProtocol = 'SOAP 1.1'

        self.contributor = {'name':"Contributor Name", 'email': 'Contributor email'}
        self.copyright = "The copyright notice"
        self.docs = 'http://www.rssboard.org/rss-specification'
        self.skipDays = 'Tuesday'
        self.skipHours = 23

        self.programname = feedgen.version.name

        self.webMaster = Person(email='webmaster@example.com')

        fg.name(self.title)
        fg.website(href=self.linkHref)
        fg.description(self.description)
        fg.language(self.language)
        fg.cloud(domain=self.cloudDomain, port=self.cloudPort,
                path=self.cloudPath, registerProcedure=self.cloudRegisterProcedure,
                protocol=self.cloudProtocol)
        fg.copyright(self.copyright)
        fg.author(self.author)
        fg.skipDays(self.skipDays)
        fg.skipHours(self.skipHours)
        fg.webMaster(self.webMaster)
        fg.feed_url(self.feedUrl)

        self.fg = fg


    def test_baseFeed(self):
        fg = self.fg

        assert fg.name() == self.title

        assert fg.author()[0] == self.author
        assert fg.webMaster() == self.webMaster

        assert fg.website() == self.linkHref

        assert fg.description() == self.description

        assert fg.language() == self.language
        assert fg.feed_url() == self.feedUrl


    def test_rssFeedFile(self):
        fg = self.fg
        filename = 'tmp_Rssfeed.xml'
        fg.rss_file(filename=filename, xml_declaration=False)

        with open (filename, "r") as myfile:
            rssString=myfile.read().replace('\n', '')

        self.checkRssString(rssString)

    def test_rssFeedString(self):
        fg = self.fg
        rssString = fg.rss_str(xml_declaration=False)
        self.checkRssString(rssString)


    def checkRssString(self, rssString):

        feed = etree.fromstring(rssString)
        nsRss = self.nsContent
        nsAtom = "http://www.w3.org/2005/Atom"

        channel = feed.find("channel")
        assert channel != None

        assert channel.find("title").text == self.title
        assert channel.find("description").text == self.description
        assert channel.find("lastBuildDate").text != None
        assert channel.find("docs").text == "http://www.rssboard.org/rss-specification"
        assert self.programname in channel.find("generator").text
        assert channel.find("cloud").get('domain') == self.cloudDomain
        assert channel.find("cloud").get('port') == self.cloudPort
        assert channel.find("cloud").get('path') == self.cloudPath
        assert channel.find("cloud").get('registerProcedure') == self.cloudRegisterProcedure
        assert channel.find("cloud").get('protocol') == self.cloudProtocol
        assert channel.find("copyright").text == self.copyright
        assert channel.find("docs").text == self.docs
        assert self.author.email in channel.find("managingEditor").text
        assert channel.find("skipDays").find("day").text == self.skipDays
        assert int(channel.find("skipHours").find("hour").text) == self.skipHours
        assert self.webMaster.email in channel.find("webMaster").text
        assert channel.find("{%s}link" % nsAtom).get('href') == self.feedUrl
        assert channel.find("{%s}link" % nsAtom).get('rel') == 'self'
        assert channel.find("{%s}link" % nsAtom).get('type') == \
               'application/rss+xml'

    def test_feedUrlValidation(self):
        self.assertRaises(ValueError, self.fg.feed_url, "example.com/feed.rss")

    def test_generator(self):
        software_name = "My Awesome Software"
        self.fg.generator(software_name)
        rss = self.fg._create_rss()
        generator = rss.find("channel").find("generator").text
        assert software_name in generator
        assert self.programname in generator

        self.fg.generator(software_name, exclude_feedgen=True)
        generator = self.fg._create_rss().find("channel").find("generator").text
        assert software_name in generator
        assert self.programname not in generator

    def test_str(self):
        assert str(self.fg) == self.fg.rss_str(
            minimize=False,
            encoding="UTF-8",
            xml_declaration=True
        )

    def test_updated(self):
        date = datetime.datetime(2016, 1, 1, 0, 10, tzinfo=dateutil.tz.tzutc())

        def getLastBuildDateElement(fg):
            return fg._create_rss().find("channel").find("lastBuildDate")

        # Test that it has a default
        assert getLastBuildDateElement(self.fg) is not None

        # Test that it respects my custom value
        self.fg.updated(date)
        lastBuildDate = getLastBuildDateElement(self.fg)
        assert lastBuildDate is not None
        assert dateutil.parser.parse(lastBuildDate.text) == date

        # Test that it is left out when set to False
        self.fg.updated(False)
        lastBuildDate = getLastBuildDateElement(self.fg)
        assert lastBuildDate is None

    def test_AuthorEmail(self):
        # Just email - so use managingEditor, not dc:creator or itunes:author
        # This is per the RSS best practices, see the section about dc:creator
        self.fg.author(Person(None, "justan@email.address"), replace=True)
        channel = self.fg._create_rss().find("channel")
        # managingEditor uses email?
        assert channel.find("managingEditor").text == self.fg.author()[0].email
        # No dc:creator?
        assert channel.find("{%s}creator" % self.nsDc) is None
        # No itunes:author?
        assert channel.find("{%s}author" % self.nsItunes) is None

    def test_AuthorName(self):
        # Just name - use dc:creator and itunes:author, not managingEditor
        self.fg.author(Person("Just a. Name"), replace=True)
        channel = self.fg._create_rss().find("channel")
        # No managingEditor?
        assert channel.find("managingEditor") is None
        # dc:creator equals name?
        assert channel.find("{%s}creator" % self.nsDc).text == \
               self.fg.author()[0].name
        # itunes:author equals name?
        assert channel.find("{%s}author" % self.nsItunes).text == \
            self.fg.author()[0].name

    def test_AuthorNameAndEmail(self):
        # Both name and email - use managingEditor and itunes:author,
        # not dc:creator
        self.fg.author(Person("Both a name", "and_an@email.com"), replace=True)
        channel = self.fg._create_rss().find("channel")
        # Does managingEditor follow the pattern "email (name)"?
        self.assertEqual(self.fg.author()[0].email +
                         " (" + self.fg.author()[0].name + ")",
                         channel.find("managingEditor").text)
        # No dc:creator?
        assert channel.find("{%s}creator" % self.nsDc) is None
        # itunes:author uses name only?
        assert channel.find("{%s}author" % self.nsItunes).text == \
            self.fg.author()[0].name

    def test_multipleAuthors(self):
        # Multiple authors - use itunes:author and dc:creator, not
        # managingEditor.
        # Is an exception raised when a list is passed in?
        self.assertRaises(TypeError, self.fg.author,
                          [Person("A List", "is@not.allowed")])

        person1 = Person("Multiple", "authors@example.org")
        person2 = Person("Are", "cool@example.org")
        self.fg.author(person1, person2, replace=True)
        channel = self.fg._create_rss().find("channel")

        # Test dc:creator
        author_elements = \
            channel.findall("{%s}creator" % self.nsDc)
        author_texts = [e.text for e in author_elements]

        assert len(author_texts) == 2
        assert person1.name in author_texts[0]
        assert person1.email in author_texts[0]
        assert person2.name in author_texts[1]
        assert person2.email in author_texts[1]

        # Test itunes:author
        itunes_author = channel.find("{%s}author" % self.nsItunes)
        assert itunes_author is not None
        itunes_author_text = itunes_author.text
        assert person1.name in itunes_author_text
        assert person1.email not in itunes_author_text
        assert person2.name in itunes_author_text
        assert person2.email not in itunes_author_text

        # Test that managingEditor is not used
        assert channel.find("managingEditor") is None


    def test_webMaster(self):
        self.fg.webMaster(Person(None, "justan@email.address"))
        channel = self.fg._create_rss().find("channel")
        assert channel.find("webMaster").text == self.fg.webMaster().email

        self.assertRaises(ValueError, self.fg.webMaster,
                          Person("Mr. No Email Address"))

        self.fg.webMaster(Person("Both a name", "and_an@email.com"))
        channel = self.fg._create_rss().find("channel")
        # Does webMaster follow the pattern "email (name)"?
        self.assertEqual(self.fg.webMaster().email +
                         " (" + self.fg.webMaster().name + ")",
                         channel.find("webMaster").text)

if __name__ == '__main__':
    unittest.main()
