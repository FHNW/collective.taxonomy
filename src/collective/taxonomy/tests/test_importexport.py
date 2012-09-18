import os.path
import unittest2 as unittest

from plone.app.testing import PLONE_INTEGRATION_TESTING
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login

from zope.component import queryUtility

from ..testing import INTEGRATION_TESTING
from ..interfaces import ITaxonomy


class TestImportExport(unittest.TestCase):
    layer = INTEGRATION_TESTING

    vdex_file_contents = open(os.path.dirname(__file__) + "/examples/nihms.xml").read()

    class test_environ:
        @staticmethod
        def shouldPurge():
            return True

        @staticmethod
        def getLogger(name):
            import logging
            return logging.getLogger(name)

    @property
    def adapter(self):
        from collective.taxonomy.exportimport \
        import TaxonomyImportExportAdapter

        portal = self.layer['portal']
        return TaxonomyImportExportAdapter(portal, self.test_environ)

    def test_import_example(self):
        """ Tests, that we can import and get an adequate result """
        utility_name = self.adapter.importDocument(self.vdex_file_contents)
        utility = queryUtility(ITaxonomy, name=utility_name)
        self.assertTrue(utility)
        self.assertTrue(utility.keys() == ['ru', 'de', 'en', 'da'])
        self.assertTrue([key for key in utility['en'].keys()] ==
                        ['/Information Science',
                         '/Information Science/Book Collecting',
                         '/Information Science/Chronology'])

    def test_import_export_example(self):
        """ Tests, that we can import and export getting the same result """
        utility_name = self.adapter.importDocument(self.vdex_file_contents)
        body = self.adapter.exportDocument(utility_name)
        self.assertTrue(body == self.vdex_file_contents, body)

    def test_vocabulary(self):
        """ Testing that the vocabulary contains the correct contents """
        utility_name = self.adapter.importDocument(self.vdex_file_contents)
        utility = queryUtility(ITaxonomy, name=utility_name)
        vocab = utility(self.layer['portal'])
        self.assertTrue([term.value for term in vocab.getTerms()] ==
                        ['/Information Science',
                         '/Information Science/Book Collecting',
                         '/Information Science/Chronology'])

    def test_translate(self):
        utility_name = self.adapter.importDocument(self.vdex_file_contents)
        utility = queryUtility(ITaxonomy, name=utility_name)
        self.assertTrue(utility.translate(1) == '/Information Science')
