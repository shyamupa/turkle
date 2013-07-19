# -*- coding: utf-8 -*-
from io import BytesIO
import django.test
from hits.models import Hit, HitTemplate
from hits.management.commands.dump_results import results_data
from hits.management.commands.publish_hits import parse_csv_file


class TestModels(django.test.TestCase):

    def setUp(self):
        """
        Sets up HitTemplate, Hit objects, and saves them to the DB.
        The HitTemplate is bare,
        the Hit has inputs and answers and refers to the HitTemplate form.
        """
        form = HitTemplate(name='test', form="<p></p>")
        form.save()

        hit = Hit(
            source_file="",
            source_line=1,
            form=form,
            input_csv_fields={u'foo': u'bar'},
            answers={
                u"comment": u"\u221e", u"userDisplayLanguage": u"",
                u"sentence_textbox_3_verb1": u"", u"city": u"",
                u"sentence_textbox_1_verb6": u"",
                u"sentence_textbox_1_verb7": u"",
                u"sentence_textbox_1_verb4": u"",
                u"sentence_textbox_1_verb5": u"",
                u"sentence_textbox_1_verb2": u"",
                u"sentence_textbox_1_verb3": u"",
                u"sentence_textbox_1_verb1": u"",
                u"sentence_textbox_2_verb4": u"",
                u"csrfmiddlewaretoken": u"7zxQ9Yyug6Nsnm4nLky9p8ObJwNipdu8",
                u"sentence_drop_2_verb3": u"foo",
                u"sentence_drop_2_verb2": u"foo",
                u"sentence_drop_2_verb1": u"foo",
                u"sentence_textbox_2_verb1": u"",
                u"sentence_textbox_2_verb3": u"",
                u"sentence_drop_2_verb4": u"foo",
                u"sentence_textbox_2_verb2": u"",
                u"submitit": u"Submit", u"browserInfo": u"",
                u"sentence_drop_1_verb1": u"foo",
                u"sentence_drop_1_verb2": u"foo",
                u"sentence_drop_1_verb3": u"foo",
                u"sentence_drop_1_verb4": u"foo",
                u"sentence_drop_1_verb5": u"foo",
                u"sentence_drop_1_verb6": u"foo",
                u"sentence_drop_1_verb7": u"foo", u"country": u"",
                u"sentence_drop_3_verb1": u"foo",
                u"ipAddress": u"", u"region": u""
            },
            completed=True,
        )
        hit.save()
        self.hit = hit

    def test_new_hit(self):
        """
        unicode(hit) should return the template's title followed by :id of the
        hit.
        """
        self.assertEqual('HIT id:1', unicode(self.hit))

    def test_result_to_dict_Answer(self):
        hit = self.hit
        self.assertEqual(
            'foo',
            hit.answers['sentence_drop_1_verb1']
        )

    def test_result_to_dict_ignore_csrfmiddlewaretoken(self):
        with self.assertRaises(KeyError):
            self.hit.answers['Answer.csrfmiddlewaretoken']

    def test_result_to_dict_should_include_inputs(self):
        hit = self.hit
        self.assertEqual(
            'foo',
            hit.answers['sentence_drop_1_verb1']
        )

    def test_result_to_dict_unicode(self):
        hit = self.hit
        self.assertEqual(
            '∞'.decode('utf-8'),
            hit.answers['comment']
        )

    def test_unicode_through_dump_results(self):
        self.assertEqual(1, len(Hit.objects.filter(completed=True)))
        _, rows = results_data(Hit.objects.filter(completed=True))
        self.assertEqual(
            '∞'.decode('utf-8'),
            rows[0]['Answer.comment']
        )
        self.assertEqual(
            u'bar',
            rows[0]['Input.foo']
        )


class TestGenerateForm(django.test.TestCase):

    def setUp(self):
        with open('hits/tests/resources/form_0.html') as f:
            form = f.read().decode('utf-8')

        self.hit_template = HitTemplate(name="filepath", form=form)
        self.hit_template.save()
        field_names = u"tweet0_id,tweet0_entity,tweet0_before_entity,tweet0_after_entity,tweet0_word0,tweet0_word1,tweet0_word2,tweet1_id,tweet1_entity,tweet1_before_entity,tweet1_after_entity,tweet1_word0,tweet1_word1,tweet1_word2,tweet2_id,tweet2_entity,tweet2_before_entity,tweet2_after_entity,tweet2_word0,tweet2_word1,tweet2_word2,tweet3_id,tweet3_entity,tweet3_before_entity,tweet3_after_entity,tweet3_word0,tweet3_word1,tweet3_word2,tweet4_id,tweet4_entity,tweet4_before_entity,tweet4_after_entity,tweet4_word0,tweet4_word1,tweet4_word2,tweet5_id,tweet5_entity,tweet5_before_entity,tweet5_after_entity,tweet5_word0,tweet5_word1,tweet5_word2",
        values = u"268,SANTOS, Muy bien America ......... y lo siento mucho , un muy buen rival,mucho,&nbsp;,&nbsp;,2472,GREGORY, Ah bueno , tampoco andes pidiendo ese tipo de milagros . @jcabrerac @CarlosCabreraR,bueno,&nbsp;,&nbsp;,478,ALEJANDRO, @aguillen19 &#44; un super abrazo mi querido , &#44; mis mejores deseos para este 2012 ... muakkk !,querido,&nbsp;,&nbsp;,906_control, PF, Acusan camioneros extorsiones de, : Transportistas acusaron que deben pagar entre 13 y 15 mil pesos a agentes que .. http://t.co/d8LUVvhP,acusaron,&nbsp;,&nbsp;,2793_control, CHICARO, Me gusta cuando chicharo hace su oracion es lo que lo hace especial .,&nbsp;,gusta,&nbsp;,&nbsp;,357,OSCAR WILDE&QUOT;, &quot; @ ifilosofia : Las pequeñas acciones de cada día son las que hacen o deshacen el carácter.&quot; , bueno !!!! Es así,bueno,&nbsp;,&nbsp;",
        self.hit = Hit(
            source_file="filepath",
            source_line=1,
            form=self.hit_template,
            input_csv_fields=dict(zip(field_names, values))
        )
        self.hit.save()

    def test_generate_form(self):
        with open('hits/tests/resources/form_0_filled.html') as f:
            form = f.read().decode('utf-8')
        expect = form
        actual = self.hit.generate_form()
        self.assertNotEqual(expect, actual)

    def test_map_fields_csv_row(self):
        hit_template = HitTemplate(
            name='test',
            form=u"""</select> con relaci&oacute;n a <span style="color: rgb(0, 0, 255);">${tweet0_entity}</span> en este mensaje.</p>"""
        )
        hit_template.save()
        hit = Hit(
            source_file="filepath",
            source_line=1,
            form=hit_template,
            input_csv_fields=dict(
                zip(
                    [u"tweet0_id", u"tweet0_entity"],
                    [u"268", u"SANTOS"],
                )
            ),
        )
        hit.save()
        expect = """</select> con relaci&oacute;n a <span style="color: rgb(0, 0, 255);">SANTOS</span> en este mensaje.</p>"""
        actual = hit.generate_form()
        self.assertEqual(expect, actual)


class TestPublishHits(django.test.TestCase):

    def setUp(self):
        csv_text = (
            u'h0,h1\r\n'
            u'"é0",ñ0\r\n'
            u'"é1, e1",ñ1'
        )
        self.csv_file = BytesIO(csv_text.encode('utf8'))

    def test_parse_csv_file_only_newline(self):
        csv_text = (
            u'h0,h1\n'
            u'"é0",ñ0\n'
            u'"é1, e1",ñ1'
        )
        csv_file = BytesIO(csv_text.encode('utf8'))

        header, data_rows = parse_csv_file(csv_file)
        rows = [row for row in data_rows]
        self.assertEqual(
            [u'h0', u'h1'],
            header
        )
        self.assertEqual(
            [
                [u'é0', u'ñ0'],
                [u'é1, e1', u'ñ1'],
            ],
            rows
        )

    def test_parse_csv_file(self):
        header, data_rows = parse_csv_file(self.csv_file)
        rows = [row for row in data_rows]
        self.assertEqual(
            [u'h0', u'h1'],
            header
        )
        self.assertEqual(
            [
                [u'é0', u'ñ0'],
                [u'é1, e1', u'ñ1'],
            ],
            rows
        )

        ht = HitTemplate(name='test', form="<p></p>")
        ht.save()

        hit = Hit(
            source_file='',
            source_line=0,
            form=ht,
            input_csv_fields=dict(zip(header, rows[1])),
        )
        hit.save()

        expect = {u"h0": u"é1, e1", u"h1": u"ñ1"}
        actual = hit.input_csv_fields
        self.assertEqual(expect, actual)