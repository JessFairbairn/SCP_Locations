from unittest import main, mock, TestCase

from search import _filter_redundant_locations
# from spacy.tests.conftest import en_vocab
from spacy.vocab import Vocab
from spacy.tokens import Span, Doc

class FilterRedundantLocationsTestCase(TestCase):
    def setUp(self):
        self.doc = Doc(Vocab(), words=["Chelsea", "London", "UK"])
        self.span1 = Span(self.doc, 0, 1)
        self.span2 = Span(self.doc, 1, 2)
        self.span3 = Span(self.doc, 2, 3)
        self.word_spans = [self.span1, self.span2, self.span3]
        self.span_all = Span(self.doc, 0, 3)

    def test_changes_nothing_if_no_compound_span(self):
        result = _filter_redundant_locations([], self.word_spans)

        self.assertEqual(self.word_spans, result)

    def test_removes_subsets(self):
        result = _filter_redundant_locations([self.span_all], self.word_spans)

        self.assertEqual([self.span_all], result)


if __name__ == "__main__":
    main()