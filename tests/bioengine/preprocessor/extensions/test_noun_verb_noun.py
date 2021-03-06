import spacy
from unittest import TestCase

from benepar.spacy_plugin import BeneparComponent

from src.bioengine.nlp_processor.extensions import BiologicalNamedEntity
from src.bioengine.nlp_processor.extensions.svo import get_co_ref, get_noun_verb_noun_phrases_from_sentence, \
    enrich_adp, get_subjects, get_full_adj, get_dependencies, get_objs_from_prepositions


class TestNounVerbRelations(TestCase):
    """
    A test suite that tests the noun verb noun relation extensions
    """

    @classmethod
    def setUpClass(cls):
        """
        Sets up the test suite
        """
        cls.nlp = spacy.load('en_core_sci_sm', disable=['ner'])
        cls.nlp.add_pipe(BiologicalNamedEntity(cls.nlp))
        cls.nlp.add_pipe(BeneparComponent("benepar_en2"))

    @classmethod
    def tearDownClass(cls):
        """
        Tears down the test case dependencies
        """
        cls.nlp = None

    def test_get_subjects_returns_left_subject(self):
        text = 'Central diabetes insipidus is a rare disease of the hypothalamus and neurohypophysis'
        doc = self.nlp(text)
        subjects, negation = get_subjects(doc[1])
        assert negation is False
        assert str(subjects[0]) == 'rare disease'

    def test_pronoun_res(self):
        text = 'Central diabetes insipidus is a rare disease of the hypothalamus and neurohypophysis'
        doc = self.nlp(text)
        preps = get_objs_from_prepositions([doc[4]])
        pass

    def test_get_svo(self):
        text = 'Central diabetes insipidus is a rare disease of the hypothalamus and neurohypophysis'
        doc = self.nlp(text)
        svo = get_noun_verb_noun_phrases_from_sentence(list(doc.sents)[0])
        pass

    def test_pronoun_resolution_with_ambiguous_pronoun(self):
        text = 'Central diabetes insipidus is a rare disease of the hypothalamus and neurohypophysis. It is very ' \
               'unusually found in the adult with type 2 diabetes mellitus.'
        doc = self.nlp(text)
        co_reference = get_co_ref(list(doc.sents)[1][0])
        assert 'Central diabetes insipidus' == co_reference.text

    def test_pronoun_resolution_with_definititive_noun(self):
        text = 'Central diabetes insipidus is a rare disease of the hypothalamus and neurohypophysis. It is very ' \
               'unusually found in the adult with type 2 diabetes mellitus.'
        doc = self.nlp(text)
        co_reference = get_co_ref(list(doc.sents)[0][6])
        assert co_reference is None

    def test_noun_phrase_resolution(self):
        text = 'Central diabetes insipidus is a rare disease of the hypothalamus and neurohypophysis.'
        doc = self.nlp(text)
        noun_phrase = get_noun_verb_noun_phrases_from_sentence(list(doc.sents)[0])
        assert 'Central diabetes insipidus' == str(noun_phrase[0][0])
        assert 'is' == str(noun_phrase[0][1])
        assert 'rare disease' in str(noun_phrase[0][2])

    def test_adp_resolution(self):
        text = 'Central diabetes insipidus is a rare disease of the hypothalamus and neurohypophysis. It is very ' \
               'unusually found in the adult with type 2 diabetes mellitus.'
        doc = self.nlp(text)
        resolved_noun = enrich_adp(list(doc.sents)[1][5])
        assert resolved_noun.text == 'adult'

    def test_get_full_adj(self):
        text = 'Pulmonary Langerhans cell histiocytosis is an uncommon diffuse cystic lung disease in adults.'
        doc = self.nlp(text)
        resolved_noun = get_full_adj(list(doc.sents)[0][5])
        assert 'cystic lung disease' == str(resolved_noun[0])
        assert 'uncommon' == str(resolved_noun[2])

    # def test_get_subjects(self):
    #     text = 'Central diabetes insipidus is a rare disease of the hypothalamus and neurohypophysis.'
    #     doc = self.nlp(text)
    #     subjects, negation = get_subjects()

    # TODO: add enrich adj tests
    # TODO: add enrich adp tests
    # TODO: finish test_noun_phrase_resolution_with_pronouns test
